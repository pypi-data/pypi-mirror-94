import typing as t

import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer

from bavard.nlu import constants
from bavard.nlu.data.training_example import Example, Tag
from bavard.nlu.data.nlu_data import NLUTrainingData
from bavard.nlu.utils import concat_tensor_dicts, get_char_to_word_map


class NLUDataPreprocessor:
    """
    Data preprocessing model that fits label encoders to the targets of an agent's
    NLU data and processes the raw NLU data into a tensorflow.data.Dataset instance
    ready for training.
    """

    lm_name = constants.BASE_LANGUAGE_MODEL

    def __init__(self, *, max_seq_len: int) -> None:
        self._fitted = False
        self.max_seq_len = max_seq_len

    def fit(self, nlu_data: NLUTrainingData) -> None:
        self.intents = set(nlu_data.intents)
        self.tag_types = set(nlu_data.tagTypes)

        # intents encoder
        self.intents_encoder = LabelEncoder()
        self.intents_encoder.fit(sorted(self.intents))

        # tags encoder
        tag_set = {"[CLS]", "[SEP]", "O"}
        for tag_type in sorted(self.tag_types):
            tag_set.add(f"B-{tag_type}")
            tag_set.add(f"I-{tag_type}")
        self.tag_encoder = LabelEncoder()
        self.tag_encoder.fit(list(tag_set))

        # tag and intent sizes
        self.n_tags = len(tag_set)
        self.n_intents = len(self.intents)

        # tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.lm_name)
        self._fitted = True

    def transform(self, nlu_data: NLUTrainingData) -> tf.data.Dataset:
        """
        Transform a whole training dataset of utterances and labels.
        """
        assert self._fitted
        examples = self._process_nlu_data(nlu_data)
        return self._examples_to_dataset(examples)

    def transform_utterance(self, utterance: str) -> dict:
        """
        Transform a single utterance with no labels.
        """
        tokens, word_start_mask, word_to_token_map = self._preprocess_text(utterance)

        tokens = ["[CLS]", *tokens, "[SEP]"]
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(tokens)
        word_start_mask = [0, *word_start_mask, 0]

        while len(input_ids) < self.max_seq_len:
            input_ids.append(0)
            input_mask.append(0)
            word_start_mask.append(0)

        return {
            "input_ids": tf.convert_to_tensor([input_ids]),
            "input_mask": tf.convert_to_tensor([input_mask]),
            "word_start_mask": tf.convert_to_tensor([word_start_mask]),
        }

    def transform_utterances(self, utterances: t.List[str]) -> dict:
        """
        Transform a batch of utterances with no labels.
        """
        tensor_dicts = [self.transform_utterance(u) for u in utterances]
        return concat_tensor_dicts(tensor_dicts)

    def _process_nlu_data(self, nlu_data: NLUTrainingData) -> t.List[Example]:
        result_examples: t.List[Example] = []

        examples = nlu_data.examples

        for ex in examples:
            text = ex.text
            intent = ex.intent
            raw_tags = ex.tags

            if intent not in self.intents:
                # We only allow examples for the agent's registered intents. This is probably invalid/old data.
                continue

            if any(tag.tagType not in self.tag_types for tag in raw_tags):
                # The same goes for NER tag types.
                continue

            (
                text_tokens,
                word_start_mask,
                word_to_token_map,
            ) = self._preprocess_text(text)

            char_to_word_map = get_char_to_word_map(text)

            result_tags: t.List[Tag] = []
            for tag in raw_tags:
                start = tag.start
                end = tag.end
                tag_type = tag.tagType

                start_word_idx = char_to_word_map[start]
                end_word_idx = char_to_word_map[end - 1]

                start_tok = word_to_token_map[start_word_idx]
                end_tok = word_to_token_map[end_word_idx]
                result_tags.append(
                    Tag(
                        tag_type=tag_type,
                        start=start,
                        end=end,
                        start_tok=start_tok,
                        end_tok=end_tok,
                    )
                )

            result_examples.append(
                Example(
                    text=text,
                    intent=intent,
                    tokens=text_tokens,
                    tags=result_tags,
                    word_start_mask=word_start_mask,
                    tokenizer=self.tokenizer,
                )
            )

        return result_examples

    def _preprocess_text(self, text: str):
        text = text.lower()
        text_words = text.split()
        text_tokens = []
        token_to_word_idx = []
        word_to_token_map = []
        word_start_mask = []
        for (wi, word) in enumerate(text_words):
            word_to_token_map.append(len(text_tokens))
            word_tokens = self.tokenizer.tokenize(word)
            for ti, token in enumerate(word_tokens):
                token_to_word_idx.append(wi)
                text_tokens.append(token)

                if ti == 0:
                    word_start_mask.append(1)
                else:
                    word_start_mask.append(0)

        return text_tokens, word_start_mask, word_to_token_map

    def _examples_to_dataset(self, examples: t.List[Example]) -> tf.data.Dataset:
        """
        Converts this instance's examples into a tensor dataset.
        """
        # Unpack each example's dictionary of tensors into a single dictionary
        # containing lists of tensors.
        tensor_dicts = [
            example.to_tensors(self.max_seq_len, self.tag_encoder, self.intents_encoder)
            for example in examples
        ]
        data = concat_tensor_dicts(tensor_dicts, new_axis=True)

        # Next, split them into X and Y.
        X = {k: data[k] for k in ["input_ids", "input_mask", "word_start_mask"]}
        Y = {k: data[k] for k in ["intent", "tags"]}

        return tf.data.Dataset.from_tensor_slices((X, Y))

import spacy
import tensorflow as tf
from bavard_ml_common.mlops.serialization import TypeSerializer


class KerasSerializer(TypeSerializer):
    type_name = "keras"
    ext = None

    def serialize(self, obj: tf.keras.Model, path: str) -> None:
        # Keras models support cloud storage out of the box.
        obj.save(path, save_format="tf")

    def deserialize(self, path: str) -> object:
        return tf.keras.models.load_model(path)

    def is_serializable(self, obj: object) -> bool:
        return isinstance(obj, tf.keras.Model)


class SpacyLanguageSerializer(TypeSerializer):
    type_name = "spacy_language_pipeline"
    ext = None

    def serialize(self, obj: spacy.language.Language, path: str) -> None:
        obj.to_disk(path)

    def deserialize(self, path: str) -> object:
        return spacy.load(path)

    def is_serializable(self, obj: object) -> bool:
        return isinstance(obj, spacy.language.Language)

import typing as t

from pydantic import BaseModel

from bavard.nlu.pydantics import NLUPrediction
from bavard.common.pydantics import StrPredWithConf
from bavard.dialogue_policy.data.conversations.conversation import Conversation


class ChatbotPipelinePrediction(BaseModel):
    nlu: t.Optional[NLUPrediction]
    dp: t.Optional[t.List[StrPredWithConf]]


class ChatbotPipelinePredictions(BaseModel):
    predictions: t.List[ChatbotPipelinePrediction]


class ChatbotPipelineInputs(BaseModel):
    instances: t.List[Conversation]

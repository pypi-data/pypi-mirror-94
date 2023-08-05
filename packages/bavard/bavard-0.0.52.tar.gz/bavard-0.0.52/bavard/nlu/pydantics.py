import typing as t

from pydantic import BaseModel

from bavard.common.pydantics import TagValue, StrPredWithConf


class Tag(BaseModel):
    """A tag as it appears in NLU training data.
    """
    tagType: str
    start: int
    end: int


class NLUExample(BaseModel):
    intent: t.Optional[str]
    text: str
    tags: t.List[Tag]


class NLUPrediction(BaseModel):
    intent: StrPredWithConf
    tags: t.List[TagValue]


class NLUPredictions(BaseModel):
    predictions: t.List[NLUPrediction]

from pydantic import BaseModel


class TagValue(BaseModel):
    """Represents a named entity's type and value.
    """
    tagType: str
    value: str


class Intent(BaseModel):
    name: str


class Slot(BaseModel):
    name: str


class AgentActionDefinition(BaseModel):
    name: str


class StrPredWithConf(BaseModel):
    value: str
    confidence: float

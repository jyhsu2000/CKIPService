from pydantic import BaseModel, Field


class Segment(BaseModel):
    word: str
    pos: str


class NamedEntity(BaseModel):
    word: str
    type: str
    start: int
    end: int


class Sentence(BaseModel):
    segments: list[Segment] = Field(default_factory=list)
    entities: list[NamedEntity] = Field(default_factory=list)


class TokenizeResponse(BaseModel):
    sentences: list[Sentence] = Field(default_factory=list)

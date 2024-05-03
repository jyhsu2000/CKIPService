from pydantic import BaseModel, Field


class Segment(BaseModel):
    word: str
    pos: str = Field(description='Part of speech')


class NamedEntity(BaseModel):
    word: str
    type: str = Field(description='Entity type')
    start: int = Field(description='Start position')
    end: int = Field(description='End position')


class Sentence(BaseModel):
    segments: list[Segment] = Field(default_factory=list)
    entities: list[NamedEntity] = Field(default_factory=list)


class TokenizeResponse(BaseModel):
    sentences: list[Sentence] = Field(default_factory=list)

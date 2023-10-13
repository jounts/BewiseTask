import datetime
from typing import Optional, List

from pydantic import BaseModel, datetime_parse, field_validator


class QuestionScheme(BaseModel):
    id: int
    question: str
    answer: str
    value: Optional[int]
    created_at: datetime.datetime

    @field_validator("created_at")
    def dt_validate(cls, dt):
        if isinstance(dt, datetime.datetime):
            return dt.replace(tzinfo=None)

    class Config:
        from_attributes = True


class QuestionIn(BaseModel):
    questions_num: int


class Result(BaseModel):
    questions: Optional[List[QuestionScheme]]

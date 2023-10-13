import logging
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Question
from api.schemas import QuestionScheme
from api.models import Base

logger = logging.getLogger(__name__)


class QuestionCRUD:
    def __init__(self, model: Base) -> None:
        self.model = model

    async def get_last_records(self, count: int, session: AsyncSession) -> List[QuestionScheme]:
        qry = select(self.model).order_by(self.model.id.desc()).limit(count)
        result = await session.execute(qry)
        return [QuestionScheme.model_validate(item) for item in result.scalars().all()]

    async def create(self, question: QuestionScheme, session: AsyncSession) -> QuestionScheme:
        new_question = self.model(**question.model_dump())
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return QuestionScheme.model_validate(new_question)

    async def create_list(self, questions: Sequence[QuestionScheme], session: AsyncSession):
        new_questions = [self.model(**question.model_dump(exclude=['id'])) for question in questions]
        session.add_all(new_questions)
        await session.commit()

    async def not_exists(self, questions: List[QuestionScheme], session: AsyncSession) -> List[QuestionScheme]:
        question_text_list = [item.question for item in questions]
        qry = select(self.model).filter(self.model.question.in_(question_text_list))
        result = await session.execute(qry)

        return [item for item in questions if item.question not in [i.question for i in result.scalars().all()]]


crud_question = QuestionCRUD(Question)

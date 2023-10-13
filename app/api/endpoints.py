from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Result, QuestionIn
from api.services import get_questions
from db import get_async_session

api_router = APIRouter(prefix="/questions")


@api_router.post("/", response_model=Result)
async def create_and_get(
        *,
        request: Request,
        questions: QuestionIn,
        session: AsyncSession = Depends(get_async_session)
):
    return await get_questions(questions.questions_num, session)
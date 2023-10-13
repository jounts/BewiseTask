import logging
from typing import List

import aiohttp
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import crud_question
from api.schemas import QuestionScheme, Result
from config import OUTER_SRV_URL


logger = logging.getLogger('uvicorn')


async def request_questions(count: int) -> QuestionScheme:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'{OUTER_SRV_URL}{count}') as response:
                return await response.json()
        except Exception:
            raise HTTPException(status_code=503, detail='jservice.io unavailable')


async def get_questions(count: int, session: AsyncSession) -> List[QuestionScheme]:
    result = await crud_question.get_last_records(count, session)
    await write_questions(count, session)
    if len(result) < count:
        return Result(questions=None)
    return Result(questions=result)


async def write_questions(count: int, session: AsyncSession):
    while count > 0:
        new_questions = await request_questions(count)
        try:
            not_exists = await crud_question.not_exists(
                [QuestionScheme(**item) for item in new_questions],
                session
            )
        except Exception as e:
            logger.error(f'exception: {e}')
            raise HTTPException(status_code=500, detail='database error')
        try:
            await crud_question.create_list(not_exists, session)
        except Exception as e:
            logger.error(f'exception: {e}')
            raise HTTPException(status_code=500, detail='database error')

        count -= len(not_exists)

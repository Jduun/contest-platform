from typing import Annotated

from fastapi import APIRouter, Security

import src.auth.service as auth_service
from src.ai_chat.schemas import GetLLMAnswerDTO
from src.ai_chat.service import get_llm_answer
from src.auth.models import User
from src.auth.roles import Roles

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/generate")
async def generate_answer(
    data: GetLLMAnswerDTO,
    user: Annotated[
        User,
        Security(
            auth_service.get_current_user,
            scopes=[Roles.admin, Roles.organizer, Roles.user],
        ),
    ],
) -> str:
    answer = await get_llm_answer(
        data.problem_statement,
        data.user_code,
        data.messages,
        data.programming_language
    )
    return answer

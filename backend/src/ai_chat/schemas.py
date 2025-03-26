from pydantic import BaseModel


class GetLLMAnswerDTO(BaseModel):
    messages: list[dict[str, str]]
    user_code: str
    problem_statement: str
    programming_language: str

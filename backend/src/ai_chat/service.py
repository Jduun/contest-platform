import os

from litellm import Router
from litellm.exceptions import RateLimitError

groq_api_key = os.getenv("GROQ_API_KEY")
model_alias = "groq"
model_list = [
    {
        "model_name": model_alias,
        "litellm_params": {"model": "groq/llama3-70b-8192", "api_key": groq_api_key},
    },
    {
         "model_name": model_alias,
         "litellm_params": {"model": "groq/gemma2-9b-it", "api_key": groq_api_key},
    },
    {
         "model_name": model_alias,
         "litellm_params": {"model": "groq/llama3-8b-8192", "api_key": groq_api_key},
    },
]
router = Router(
    model_list=model_list, cache_responses=True, allowed_fails=1, cooldown_time=100
)

async def get_llm_answer(
        problem_statement: str,
        user_code: str,
        messages: list[dict[str, str]],
        programming_language: str,
) -> str:
    system_prompt = f"""
    You are an assistant for competitive programming.
    Your task is to help the user solve problems without providing a full solution.
    You can:
    - Analyze code, identify errors, and suggest possible improvements.
    - Explain algorithmic concepts, problem-solving approaches,
        and provide useful hints.
    - Highlight nuances and specific features of programming languages.
    - Discuss the time and space complexity of different solutions.
    - Guide the user in the right direction by asking leading questions.
    You **must not** provide a complete solution, but you can assist with debugging,
    refining logic, breaking down the problem, and choosing an efficient algorithm.
    Your goal is to help the user arrive at the solution independently.
    In all problems, the answer doesn't need to be returned, it needs to be output.
    Current problem statement: {problem_statement}
    """

    max_tries = 10
    error_answer = ""
    chat_history = [{"role": "system", "content": system_prompt}]
    chat_history.extend(messages)
    chat_history[-1]["content"] += f"\nThe code that I have written so far in {programming_language}:\n{user_code}"  # noqa: E501
    for _ in range(max_tries):
        try:
            response = await router.acompletion(
                model=model_alias,
                messages=chat_history,
                temperature=0.2,
            )
            llm_response = response.choices[0].message.content
            return llm_response.strip()
        except RateLimitError:
            error_answer = "Rate limit error. Try later..."
        except Exception as e:
            error_answer = f"LLM Error: {e}"
    return error_answer

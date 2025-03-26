from src.ai_chat.views import chat_router
from src.auth.views import auth_router, user_router
from src.contest.views import contest_router
from src.problem.views import problem_router, stats_router
from src.submission.views import submission_router

all_routers = [
    user_router,
    auth_router,
    problem_router,
    stats_router,
    submission_router,
    contest_router,
    chat_router,
]

from src.auth.views import auth_router, user_router
from src.problem.views import problem_router
from src.submission.views import submission_router

all_routers = [
    user_router,
    auth_router,
    problem_router,
    submission_router,
]

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin import get_admin
from src.api import all_routers


def get_app() -> FastAPI:
    application = FastAPI(title="Contest Platform")
    for router in all_routers:
        application.include_router(router)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_app()
admin = get_admin(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

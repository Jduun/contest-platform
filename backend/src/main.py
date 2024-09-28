import uvicorn
from fastapi import APIRouter, FastAPI

from src.api import all_routers

app = FastAPI(title="Leetcode clone")

for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

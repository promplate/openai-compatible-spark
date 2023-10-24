from fastapi import FastAPI

from .chat import router

app = FastAPI(title="openai-compatible spark proxy")

app.include_router(router)
app.include_router(router, prefix="/v1")

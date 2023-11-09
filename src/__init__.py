from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .chat import router

app = FastAPI(title="openai-compatible spark proxy")

app.include_router(router)
app.include_router(router, prefix="/v1")

app.add_middleware(CORSMiddleware, allow_origins="*", allow_methods="*")

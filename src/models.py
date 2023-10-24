from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class CreateChatCompletion(BaseModel):
    model: Literal["v1.1", "v2.1", "v3.1"] = "v3.1"
    messages: list[Message]
    temperature: float = Field(ge=0, le=1, default=0.5)
    # top_k: int = Field(ge=1, le=6, default=4)
    max_tokens: int | None = 2048
    stream: bool = False
    user: str | None = None

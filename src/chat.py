from time import time
from uuid import uuid4

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse, StreamingResponse
from orjson import dumps
from spark_ai_sdk.spark_ai import SparkAI

from src.models import CreateChatCompletion

from .config import Config

router = APIRouter(tags=["Chat"])


def format_chunk(id, content, model, stop=False):
    if stop:
        choice = {"index": 0, "delta": {}, "finish_reason": "stop"}
    else:
        choice = {"index": 0, "delta": {"content": content, "role": "assistant"}}
    return {
        "id": id,  # implement this
        "choices": [choice],
        "created": int(time()),
        "model": model,
        "object": "chat.completion.chunk",
    }


def data_event(id, content, model, stop=False):
    return f"data: {dumps(format_chunk(id, content, model, stop)).decode()}\n\n"


@router.post("/chat/completions")
def create_chat_completions(data: CreateChatCompletion):
    if not data.stream:
        result = "".join(generate_response(data))
        print(result)
        return ORJSONResponse(
            {
                "id": data.user,
                "object": "chat.completion",
                "created": int(time()),
                "model": data.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": result,
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
        )

    def stream_output():
        for delta in generate_response(data):
            yield data_event(data.user, delta, data.model)
        yield data_event(data.user, None, data.model, True)
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream_output)


def generate_response(data: CreateChatCompletion):
    env = Config(api_url=f"wss://spark-api.xf-yun.com/{data.model}/chat")

    spark = SparkAI(env.app_id, env.api_key, env.api_secret, env.api_url)

    domain = {"v1.1": "general", "v2.1": "generalv2", "v3.1": "generalv3"}[data.model]

    last = ""

    for this, _ in spark.chat_stream(
        data.messages[-1].content,
        [msg.model_dump() for msg in data.messages[:-1]],
        data.user or uuid4().hex,
        domain,
        data.max_tokens,
        data.temperature,
    ):
        delta = this.removeprefix(last)
        last = this

        yield delta

"""
Everything related to talking to the LLM lives here.

Flow for every user message:

    user text
        -> sent to the LLM together with the ChatResponse JSON schema
        -> LLM replies using its native JSON mode (not free-form text)
        -> we parse that JSON string
        -> we validate/parse it into a ChatResponse object with Pydantic
        -> the validated object is returned to main.py

We use DeepSeek's API through the official `openai` Python SDK (DeepSeek is
OpenAI-API-compatible, so the same SDK works by pointing `base_url` at
DeepSeek's servers).
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError
from pydantic import ValidationError

from app.models import ChatResponse

# Load variables from a local .env file (if present) into the environment.
load_dotenv()

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"


class MissingAPIKeyError(RuntimeError):
    """Raised when LLM_API_KEY is not set."""


class InvalidStructuredResponseError(RuntimeError):
    """Raised when the LLM's reply isn't valid JSON or doesn't match ChatResponse."""


def _build_client() -> OpenAI:
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        # Beginner-friendly error handling: fail early with a clear message
        # instead of letting the SDK raise a confusing auth error later.
        raise MissingAPIKeyError(
            "LLM_API_KEY is not set. Copy .env.example to .env and add your DeepSeek API key."
        )
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def get_structured_response(user_message: str) -> ChatResponse:
    """Send `user_message` to the LLM and return a validated ChatResponse."""

    client = _build_client()

    # DeepSeek's "native structured output" is its JSON mode: passing
    # response_format={"type": "json_object"} forces the model to reply with
    # syntactically valid JSON instead of arbitrary free-form text.
    #
    # DeepSeek's JSON mode does not (yet) enforce a schema on its own, so we
    # hand it our schema explicitly and describe it in the system prompt.
    # This is still fundamentally different from "ask for JSON and hope":
    # the API-level JSON mode guarantees valid JSON syntax, and Pydantic
    # (below) is what guarantees the *shape* of that JSON is correct.
    schema = ChatResponse.model_json_schema()

    system_prompt = (
        "You are a helpful customer-support chatbot.\n"
        "Reply ONLY with a single JSON object that matches this JSON schema:\n"
        f"{json.dumps(schema)}\n"
        "Do not include any text outside the JSON object."
    )

    try:
        completion = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            response_format={"type": "json_object"},
            max_tokens=500,
        )
    except APIConnectionError as exc:
        raise ConnectionError(
            "Could not reach the DeepSeek API. Check your internet connection."
        ) from exc
    except APIError as exc:
        # Covers things like invalid API key, rate limits, server errors, etc.
        raise RuntimeError(f"DeepSeek API returned an error: {exc}") from exc

    raw_content = completion.choices[0].message.content

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise InvalidStructuredResponseError(
            f"LLM did not return valid JSON:\n{raw_content}"
        ) from exc

    try:
        # This is the key validation step: Pydantic checks every field
        # exists and has an allowed value/type, turning a plain dict into
        # a typed, trustworthy ChatResponse object.
        return ChatResponse.model_validate(data)
    except ValidationError as exc:
        raise InvalidStructuredResponseError(
            f"LLM response did not match the ChatResponse schema:\n{exc}"
        ) from exc

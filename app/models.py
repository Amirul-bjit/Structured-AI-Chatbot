"""
Pydantic model that defines the *exact* shape of the data we want back
from the LLM.

Why this matters:
An LLM normally replies with free-form text. Free-form text is hard for a
program to work with reliably (you'd have to guess at wording, run regexes,
hope the model didn't change its phrasing, etc.).

Instead, we tell the LLM: "reply as JSON that matches this schema", and then
we hand that JSON to Pydantic. Pydantic checks that every field is present
and has the right type/allowed value. If the LLM ever returns something
malformed, Pydantic raises a clear error instead of the app silently using
broken data.
"""

from typing import Literal

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """The structured reply we expect from the LLM for every user message."""

    # Free-text reply shown to the user, e.g. "I can help you reset your password."
    message: str = Field(description="A short, helpful reply to show the user.")

    # `Literal` restricts the value to exactly one of these strings.
    # If the LLM returns anything else (e.g. "loginproblem" or "LOGIN_PROBLEM"),
    # Pydantic validation will fail instead of letting a typo slip through.
    intent: Literal[
        "general_question",
        "login_problem",
        "billing",
        "technical_problem",
        "other",
    ] = Field(description="The category that best matches the user's message.")

    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
        "frustrated",
    ] = Field(description="The emotional tone of the user's message.")

    priority: Literal[
        "low",
        "medium",
        "high",
    ] = Field(description="How urgently this message should be handled.")

    needs_human: bool = Field(
        description="True if this request is too complex/sensitive for the bot alone."
    )

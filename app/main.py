"""
Command-line entry point for the Structured AI Chatbot.

This file only handles the conversation loop and displaying results. All
LLM/Pydantic logic lives in llm.py and models.py, so this file stays simple.
"""

from app.llm import (
    MissingAPIKeyError,
    InvalidStructuredResponseError,
    get_structured_response,
)


def print_response(response) -> None:
    """Display a validated ChatResponse object to the user."""
    print(f"\nIntent: {response.intent}")
    print(f"Sentiment: {response.sentiment}")
    print(f"Priority: {response.priority}")
    print(f"Needs human: {'Yes' if response.needs_human else 'No'}")
    print(f"\nAssistant:\n{response.message}\n")


def main() -> None:
    print("Structured AI Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_message:
            continue
        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = get_structured_response(user_message)
            print_response(response)

        except MissingAPIKeyError as exc:
            # Missing API key: nothing else will work, so stop the program.
            print(f"\nSetup error: {exc}")
            break

        except InvalidStructuredResponseError as exc:
            # The LLM replied, but not in the shape we expected.
            print(f"\nThe LLM's response could not be validated: {exc}\n")

        except (ConnectionError, RuntimeError) as exc:
            # Network issues or API-side errors (rate limit, bad key, etc.).
            print(f"\nCould not get a response from the LLM: {exc}\n")

        except Exception as exc:  # noqa: BLE001 - last-resort safety net
            # Anything else unexpected. We catch this so one bad turn
            # doesn't crash the whole chat session.
            print(f"\nUnexpected error: {exc}\n")


if __name__ == "__main__":
    main()

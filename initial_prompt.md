Build a very simple beginner-friendly Python project called **Structured AI Chatbot** to demonstrate how Pydantic can be used with an LLM API to validate structured LLM responses.

### Goal

I want a minimal chatbot where a user enters a normal text message, the application sends it to an LLM, and the LLM returns a structured response.

The project should demonstrate:

1. Calling an LLM API.
2. Defining a response schema using Pydantic.
3. Asking the LLM to return data matching that schema.
4. Validating/parsing the response with Pydantic.
5. Using the validated Python object in the application.
6. Showing the result to the user.

Keep the project intentionally simple. This is a learning project, not a production application.

### Technology

Use:

* Python 3.11+
* Pydantic
* An LLM API through the official Python SDK
* `.env` for the API key
* No database
* No frontend framework
* No LangChain
* No LangGraph
* No RAG
* No vector database
* No agents
* No unnecessary abstractions

Start with a simple command-line chatbot.

### Pydantic model

Create a model similar to:

```python
class ChatResponse(BaseModel):
    message: str
    intent: Literal[
        "general_question",
        "login_problem",
        "billing",
        "technical_problem",
        "other"
    ]
    sentiment: Literal[
        "positive",
        "neutral",
        "negative",
        "frustrated"
    ]
    priority: Literal[
        "low",
        "medium",
        "high"
    ]
    needs_human: bool
```

You may improve the model slightly if necessary, but keep it simple.

### Example

User:

"I can't log into my account and I've tried three times."

The LLM should produce something conceptually like:

```json
{
  "message": "I can help you troubleshoot your login issue.",
  "intent": "login_problem",
  "sentiment": "frustrated",
  "priority": "medium",
  "needs_human": false
}
```

The Python application should parse/validate this using Pydantic.

### Important requirement

Prefer the LLM API's native structured-output functionality if the selected API/SDK supports it.

Do NOT simply ask the LLM:

"Return JSON"

and then manually parse arbitrary text.

The purpose of this project is specifically to demonstrate reliable structured LLM output combined with Pydantic.

### Project structure

Keep the structure simple, for example:

```text
structured-ai-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── llm.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsibilities

`models.py`

Define the Pydantic `ChatResponse` model.

`llm.py`

Handle communication with the LLM API and return a validated `ChatResponse`.

`main.py`

Implement a simple command-line conversation:

```text
Structured AI Chatbot
Type 'exit' to quit.

You: I cannot login to my account.

Intent: login_problem
Sentiment: frustrated
Priority: medium
Needs human: No

Assistant:
I can help you troubleshoot your login issue.
```

### Error handling

Demonstrate basic error handling for:

* Missing API key
* API failure
* Invalid structured response
* Unexpected exceptions

Keep error handling understandable to a beginner.

### Environment variables

Use:

```text
LLM_API_KEY=your_api_key_here
```

Do not hardcode the API key.

Provide `.env.example`.

### README

Create a beginner-friendly README explaining:

1. What this project does.
2. What Pydantic is.
3. Why structured LLM output is useful.
4. How the LLM response differs from normal free-form text.
5. How Pydantic validates the response.
6. How to install dependencies.
7. How to configure the API key.
8. How to run the chatbot.
9. Show one complete example interaction.
10. Explain the architecture:

```text
User Input
    ↓
LLM API
    ↓
Structured Response
    ↓
Pydantic Validation
    ↓
ChatResponse object
    ↓
Application
```

### Learning requirement

Add comments in the code explaining the important parts, especially:

* Where the Pydantic model is defined.
* Where the schema is given to the LLM.
* Where structured output is received.
* Where Pydantic validation happens.
* Why this is safer than parsing arbitrary LLM text.

Do not over-engineer the project.

After implementing it, explain the code to me file-by-file and give me 5 small exercises I can do to practice Pydantic + structured LLM output.

FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app/ ./app/

# The chatbot reads input from the terminal, so run the container with
# `docker run -it` (see README) to get an interactive session.
CMD ["python", "-m", "app.main"]

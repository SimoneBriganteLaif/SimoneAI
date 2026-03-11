FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml server.py api.py helpers.py ./
COPY tools/ ./tools/

RUN pip install --no-cache-dir mcp httpx python-dotenv

# Le credenziali Wolico vengono passate come variabili d'ambiente
# WOLICO_BASE_URL, WOLICO_EMAIL, WOLICO_PASSWORD

# Transport: stdio (default per Claude Code)
CMD ["python", "server.py"]

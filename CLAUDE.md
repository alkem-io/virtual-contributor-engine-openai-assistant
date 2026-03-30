# virtual-contributor-engine-openai-assistant Development Guidelines

## Project Overview

AI-powered OpenAI Assistant engine for the Alkemio platform. Receives questions via RabbitMQ, manages OpenAI Assistant API threads and runs, and returns responses. Leverages OpenAI's managed features including file search, thread persistence, and tool use.

## Active Technologies
- Python 3.12+
- alkemio-virtual-contributor-engine v0.8.0 (base library)
- aio-pika 9.5.7 (RabbitMQ async client)
- OpenAI Assistant API (threads, runs, file search)

## Project Structure

```text
.
├── ai_adapter.py        # Core invocation logic (Assistant API thread/run management)
├── config.py            # Environment variable loading (Env dataclass)
├── main.py              # Entry point, request handler, engine bootstrap
├── utils.py             # Utility functions
├── pyproject.toml       # Dependencies (Poetry)
├── Dockerfile           # Container build
├── .env.default         # Environment variable documentation
└── .github/workflows/   # CI/CD pipelines
```

## Commands

```bash
# Install dependencies
poetry install

# Run the engine
poetry run python main.py

# Run linting
poetry run flake8
```

## Code Style

- Use `setup_logger(__name__)` for all logging — never `print()`/`pprint()`
- All async request handling via aio-pika — no sync HTTP endpoints
- External dependencies (OpenAI API) configured via environment variables
- Assistant IDs and API keys MUST come from environment, never hardcoded

## Key Patterns

- `Input` → OpenAI Assistant thread management → run creation → polling → `Response`
- Thread lifecycle: create/reuse per conversation, handle expiration gracefully
- Assistant configuration (instructions, tools) managed via OpenAI dashboard or API
- Model is resolved per-request from `input.engine` + `input.external_config`

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

## Recent Changes
- 001-speckit-init: Added Python 3.12+ + openai, aio-pika 9.5.7, alkemio-virtual-contributor-engine v0.8.0

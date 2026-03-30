## Multi-stage build to keep the runtime image small:
## - Builder uses Python 3.12 + Poetry to install deps into /venv
## - Runtime is slim Python 3.12

FROM python:3.12-slim-bookworm AS builder

ARG POETRY_VERSION=1.8.5

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		git \
		ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m venv /venv

ENV VIRTUAL_ENV=/venv \
	PATH="/venv/bin:$PATH" \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_NO_CACHE_DIR=1 \
	POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copy dependency files first for better layer caching
COPY pyproject.toml poetry.lock README.md ./

# Install only runtime deps (no dev)
RUN poetry install --only main --no-root --no-ansi

# Copy application code
COPY . /app/

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	VIRTUAL_ENV=/venv \
	PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv
COPY --from=builder /app /app
RUN useradd --create-home --uid 1000 appuser
USER appuser

ENTRYPOINT ["/venv/bin/python"]
CMD ["main.py"]

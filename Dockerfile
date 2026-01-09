## Multi-stage build to keep the runtime image small:
## - Builder uses Debian + Poetry to install deps into /venv
## - Runtime is distroless (no shell/package manager)

FROM debian:bookworm-slim AS builder

ARG POETRY_VERSION=1.8.5

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		python3 \
		python3-pip \
		python3-venv \
		git \
		ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a venv whose interpreter path matches distroless (/usr/bin/python3.11)
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
COPY . /app

FROM gcr.io/distroless/python3-debian12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	VIRTUAL_ENV=/venv \
	PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENTRYPOINT ["/venv/bin/python"]
CMD ["main.py"]

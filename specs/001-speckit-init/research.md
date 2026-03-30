# Research: speckit-init

**Date**: 2026-03-27 | **Branch**: `001-speckit-init`

## 1. CI Pipeline Pattern

**Decision**: Mirror expert engine's `ci.yml` — GitHub Actions with Python setup, Poetry install, flake8 lint, pytest with coverage.

**Rationale**: Consistency across Alkemio virtual contributor engines reduces maintenance burden and onboarding friction.

**Alternative considered**: Pre-commit hooks only — rejected because it does not enforce quality on CI (contributors can skip hooks) and does not match the organizational pattern.

## 2. Test Framework

**Decision**: pytest + pytest-cov.

**Rationale**: Standard Python testing stack, matches the expert engine, integrates with GitHub Actions for coverage reporting.

## 3. Flake8 Configuration

**Decision**: `max-line-length=100`, matching expert engine. Create new `.flake8` file at repository root.

**Rationale**: 100-char line limit balances readability with practical line lengths for modern displays. Consistent with the expert engine configuration.

## 4. Test Coverage Strategy

**Decision**: Mock OpenAI Assistant API calls (thread creation, run management, polling). Test `config.py`, `utils.py`, and error handling paths in `ai_adapter.py`. Target 90% coverage per constitution.

**Rationale**: External API calls are non-deterministic and require credentials. Mocking at the adapter boundary allows testing business logic without external dependencies.

**Key mock boundaries**:
- `openai.AsyncOpenAI` client — mock thread creation, message creation, run creation, run polling
- Environment variable loading — parametric tests for config
- RabbitMQ connection — not tested here (handled by base library)

## 5. Pre-existing Changes

**Decision**: Include all uncommitted changes in this feature branch:
- `.env.default` — updated environment variable documentation
- `Dockerfile` — hardened with multi-stage build improvements
- `ai_adapter.py` — async run polling improvements
- `main.py` — updated imports and initialization
- `pyproject.toml` — Python 3.12 upgrade, engine v0.8.0
- `poetry.lock` — dependency resolution for updated packages

**Rationale**: These changes represent real improvements that were in progress. Capturing them in a tracked feature branch ensures they are reviewed and documented.

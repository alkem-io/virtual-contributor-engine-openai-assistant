# Virtual Contributor Engine OpenAI Assistant Constitution

## Core Principles

### I. Assistant API Contract Integrity

All interactions MUST use the OpenAI Assistant API (threads, runs, file search)
as the primary interaction model. The engine MUST correctly manage thread
lifecycle — creating, reusing, and cleaning up threads as required. The system
MUST NOT bypass the Assistant API with direct completion calls unless explicitly
justified and documented.

**Rationale**: The engine's value proposition is leveraging OpenAI's managed
Assistant features (file search, thread persistence, tool use). Bypassing the
API contract negates these capabilities and creates maintenance burden.

### II. Async Message-Driven Architecture

All request handling MUST be fully asynchronous, using RabbitMQ as the message
broker. The engine MUST NOT expose synchronous HTTP endpoints or block the event
loop. New features MUST integrate with the existing `aio-pika` message consumer
pattern and the `alkemio-virtual-contributor-engine` base library.

**Rationale**: The engine runs as one of potentially many virtual contributors
within the Alkemio platform. Async message-driven design ensures the system
scales horizontally and integrates cleanly with the platform's event bus.

### III. Thread & Data Lifecycle Management

OpenAI Assistant thread IDs MUST be managed with clear lifecycle policies
(creation, retention, cleanup). The system MUST handle thread expiration and
API errors gracefully. File uploads to OpenAI's Assistant API MUST be reviewed
for data sensitivity before transmission. Thread data MUST follow
least-privilege and retention limit principles.

**Rationale**: Assistant threads contain user conversation data. Poor lifecycle
management leads to data accumulation, stale contexts, and potential privacy
issues as conversations persist in OpenAI's infrastructure.

### IV. Observability

All LLM interactions MUST use structured logging at appropriate levels. New
features MUST NOT degrade existing logging coverage. Error conditions MUST
produce actionable log entries with sufficient context for debugging. Assistant
run statuses and polling behavior MUST be logged.

**Rationale**: LLM-based systems are inherently non-deterministic. The
Assistant API adds additional complexity with asynchronous runs. Without
observability, diagnosing quality regressions, timeout issues, or incorrect
answers becomes impractical in production.

### V. Security & Prompt Integrity

The system MUST enforce prompt boundaries that prevent user input from
overriding assistant instructions or persona definitions. New instruction
modifications MUST be reviewed for injection vulnerabilities. Sensitive
configuration (API keys, assistant IDs, credentials) MUST be loaded from
environment variables or secrets — never hardcoded.

**Rationale**: The engine processes untrusted user input and passes it to an
LLM. Without prompt integrity enforcement, adversarial inputs could leak
system instructions or cause the assistant to behave outside its intended role.

### VI. Test Coverage

All production code MUST maintain a minimum of 90% test coverage as measured by
line coverage (`pytest --cov`). New features and bug fixes MUST include tests
that cover the changed code paths. Coverage MUST NOT decrease on any pull
request — if a PR reduces coverage below the 90% threshold, it MUST be blocked
until tests are added. Critical paths (thread management, run polling, response
building) SHOULD target 95%+ coverage.

**Rationale**: The engine relies on non-deterministic LLM interactions and
async message processing, making untested code paths high-risk for silent
regressions. A strict coverage floor ensures that refactors, dependency
upgrades, and prompt changes are validated against known-good behavior.

## Technology Stack Constraints

- **Language**: Python 3.12+
- **LLM Provider**: OpenAI Assistant API (threads, runs, file search)
- **Base Library**: `alkemio-virtual-contributor-engine` v0.8.0 — engine lifecycle,
  message handling, and shared types
- **Containerization**: Docker, deployed on Kubernetes
- **License**: EUPL-1.2

Changes to the core technology stack (LLM provider, API approach,
or base library) MUST be treated as a major architectural decision requiring
explicit justification and a migration plan.

## Development Workflow

- All changes MUST be developed on feature branches and merged via pull request
  into `develop`.
- Version bumps follow semantic versioning (MAJOR.MINOR.PATCH).
- The `Dockerfile` MUST remain buildable and produce a working container after
  every merge to `develop`.
- Environment configuration MUST be documented in `.env.default` with sensible
  placeholder values for all required variables.
- Dependencies are managed via Poetry (`pyproject.toml` / `poetry.lock`).
  Dependency additions or upgrades MUST not break the existing lock file
  without explicit intent.
- CI MUST run linting (`flake8`) and tests with coverage (`pytest --cov`) on
  every push and pull request. CI failures MUST block merges.

## Governance

This constitution defines the non-negotiable principles for the
virtual-contributor-engine-openai-assistant project. All feature specifications,
implementation plans, and code changes MUST be evaluated against these
principles.

**Amendment procedure**:
1. Propose the change with rationale in a pull request modifying this file.
2. Document the version bump (MAJOR for principle removal/redefinition,
   MINOR for new principles or material expansion, PATCH for clarifications).
3. Update the Sync Impact Report at the top of this file.
4. Verify dependent templates still align with updated principles.

**Compliance**: All PRs and reviews SHOULD verify that changes do not violate
the core principles. The Constitution Check section in implementation plans
MUST reference these principles by number.

**Version**: 1.1.0 | **Ratified**: 2026-03-27 | **Last Amended**: 2026-03-27

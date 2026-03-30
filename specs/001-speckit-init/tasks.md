# Tasks: speckit-init

**Input**: Design documents from `/specs/001-speckit-init/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Stage pre-existing uncommitted changes

- [x] T001 [US5] Stage pre-existing changes to .env.default, Dockerfile, ai_adapter.py, main.py, pyproject.toml, poetry.lock

**Checkpoint**: Pre-existing changes captured on feature branch

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 [P] Create .flake8 with max-line-length=100 and exclude=.git,__pycache__,.specify
- [x] T003 [P] Add pytest, pytest-cov, and flake8 to dev dependencies in pyproject.toml and run poetry lock
- [x] T004 Create tests/ directory with tests/__init__.py and tests/conftest.py with shared fixtures

**Checkpoint**: Foundation ready - linting and test framework configured

---

## Phase 3: User Story 1 - Speckit Development Workflow (Priority: P1) 🎯 MVP

**Goal**: Speckit workflow fully initialized with scripts, templates, constitution, and commands

**Independent Test**: Run `.specify/scripts/bash/check-prerequisites.sh`; confirm 9 speckit commands; verify constitution contains Assistant API Contract Integrity and Thread Lifecycle Management principles

### Implementation for User Story 1

- [x] T005 [US1] Verify .specify/ directory contains memory/constitution.md, scripts/bash/ (5 scripts), templates/ (6 templates), and init-options.json
- [x] T006 [US1] Verify .claude/commands/ contains all 9 speckit command files
- [x] T007 [US1] Verify constitution.md contains all 6 project-specific principles (Assistant API Contract Integrity through Test Coverage)

**Checkpoint**: Speckit workflow fully functional

---

## Phase 4: User Story 2 - CLAUDE.md Development Guidelines (Priority: P1)

**Goal**: CLAUDE.md provides accurate project documentation including OpenAI Assistant API references

**Independent Test**: CLAUDE.md contains all required sections and mentions OpenAI Assistant API

### Implementation for User Story 2

- [x] T008 [US2] Verify CLAUDE.md at repository root contains Project Overview, Active Technologies, Project Structure, Commands, Code Style, and Key Patterns; confirm OpenAI Assistant API is documented

**Checkpoint**: CLAUDE.md complete and accurate

---

## Phase 5: User Story 3 - CI Pipeline (Priority: P1)

**Goal**: GitHub Actions CI pipeline runs flake8 and pytest --cov on every push and PR

**Independent Test**: Push to any branch triggers CI; pipeline passes

### Implementation for User Story 3

- [x] T009 [US3] Create .github/workflows/ci.yml with GitHub Actions workflow: checkout, setup-python 3.12, install poetry, poetry install, flake8, pytest --cov --cov-report=term-missing
- [x] T010 [US3] Configure CI environment variables in ci.yml: LOG_LEVEL=INFO, RABBITMQ_HOST=localhost, RABBITMQ_USER=guest, RABBITMQ_PASSWORD=guest, RABBITMQ_QUEUE=test, RABBITMQ_RESULT_QUEUE=test-result

**Checkpoint**: CI pipeline configured and ready to run

---

## Phase 6: User Story 4 - Test Coverage Foundation (Priority: P2)

**Goal**: tests/ directory with baseline test scaffolding for core modules

**Independent Test**: Run `poetry run pytest --cov --cov-report=term-missing` successfully

### Implementation for User Story 4

- [x] T011 [P] [US4] Create tests/test_config.py with tests for Env dataclass initialization and validation (log level assertion, history_length default, env var loading)
- [x] T012 [P] [US4] Create tests/test_ai_adapter.py with tests for invoke() error handling (mock OpenAI Assistant API), thread creation, run polling, and response extraction
- [x] T013 [P] [US4] Create tests/test_utils.py with tests for utility functions

**Checkpoint**: pytest --cov runs with baseline coverage established

---

## Phase 7: User Story 5 - Capture Existing Changes (Priority: P2)

**Goal**: All pre-existing uncommitted changes tracked on feature branch

**Independent Test**: git diff --stat shows all changes committed

### Implementation for User Story 5

- [x] T014 [US5] Review and document all pre-existing changes: .env.default (env var updates), Dockerfile (hardening), ai_adapter.py (async polling improvements), main.py (import refactoring), pyproject.toml (dependency updates), poetry.lock (regenerated)

**Checkpoint**: All changes committed and documented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation across all user stories

- [x] T015 Run poetry run flake8 and fix any linting violations
- [x] T016 Run poetry run pytest --cov --cov-report=term-missing and verify all tests pass
- [x] T017 Run .specify/scripts/bash/check-prerequisites.sh and verify success
- [x] T018 Validate quickstart.md steps work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Can run in parallel with Phase 1
- **US1 (Phase 3)**: Verification only - can run after Phase 2
- **US2 (Phase 4)**: Verification only - can run after Phase 2
- **US3 (Phase 5)**: Depends on Phase 2
- **US4 (Phase 6)**: Depends on Phase 2
- **US5 (Phase 7)**: Independent
- **Polish (Phase 8)**: Depends on all previous phases

### User Story Dependencies

- **US1 (P1)**: Independent - verification only
- **US2 (P1)**: Independent - verification only
- **US3 (P1)**: Depends on Foundational (needs .flake8, pytest)
- **US4 (P2)**: Depends on Foundational (needs tests/ dir)
- **US5 (P2)**: Independent

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T005, T006, T007 can run in parallel (verification tasks)
- T011, T012, T013 can run in parallel (different test files)
- US3 and US4 can run in parallel after Foundational phase

---

## Implementation Strategy

### MVP First (US1 + US2 + US3)

1. Complete Phase 1: Stage existing changes
2. Complete Phase 2: Foundational (.flake8, pytest deps, tests/ dir)
3. Verify Phase 3-4: Speckit workflow and CLAUDE.md
4. Complete Phase 5: CI pipeline
5. **STOP and VALIDATE**: Push and verify CI passes

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 + US2 → Verify speckit and CLAUDE.md → Dev tooling MVP
3. US3 → CI pipeline → Automated quality gates
4. US4 → Test scaffolding → Coverage baseline
5. US5 → Changes documented → Clean branch
6. Polish → Full validation

---

## Notes

- US1 and US2 are verification tasks (files already exist)
- US3 and US4 are the main implementation work
- .flake8 needs to be created (doesn't exist yet)
- [P] tasks = different files, no dependencies
- Commit after each task or logical group

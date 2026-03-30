import pytest


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set required environment variables for testing."""
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("HISTORY_LENGTH", "20")
    monkeypatch.setenv("AI_LOCAL_PATH", "/tmp/test")

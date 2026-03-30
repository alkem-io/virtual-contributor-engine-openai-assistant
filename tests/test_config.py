import pytest


class TestEnvDataclass:
    """Tests for the Env dataclass in config.py."""

    def test_default_values(self, monkeypatch):
        """Test Env loads defaults when env vars are set."""
        monkeypatch.setenv("LOG_LEVEL", "INFO")
        monkeypatch.setenv("HISTORY_LENGTH", "20")
        monkeypatch.setenv("AI_LOCAL_PATH", "/tmp/test")

        from config import Env
        env = Env()

        assert env.log_level == "INFO"
        assert env.history_length == 20
        assert env.local_path == "/tmp/test"

    def test_custom_values(self, monkeypatch):
        """Test Env loads custom values from environment."""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("HISTORY_LENGTH", "50")
        monkeypatch.setenv("AI_LOCAL_PATH", "/custom/path")

        from config import Env
        env = Env()

        assert env.log_level == "DEBUG"
        assert env.history_length == 50
        assert env.local_path == "/custom/path"

    def test_history_length_default(self, monkeypatch):
        """Test history_length defaults to 20 when not set."""
        monkeypatch.delenv("HISTORY_LENGTH", raising=False)
        monkeypatch.setenv("LOG_LEVEL", "INFO")

        from config import Env
        env = Env()

        assert env.history_length == 20

    def test_local_path_default_empty(self, monkeypatch):
        """Test local_path defaults to empty string when not set."""
        monkeypatch.delenv("AI_LOCAL_PATH", raising=False)
        monkeypatch.setenv("LOG_LEVEL", "INFO")

        from config import Env
        env = Env()

        assert env.local_path == ""

    def test_invalid_log_level_raises(self, monkeypatch):
        """Test that invalid log level raises AssertionError."""
        monkeypatch.setenv("LOG_LEVEL", "INVALID")

        from config import Env
        with pytest.raises(AssertionError):
            Env()

    @pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    def test_valid_log_levels(self, monkeypatch, level):
        """Test all valid log levels are accepted."""
        monkeypatch.setenv("LOG_LEVEL", level)

        from config import Env
        env = Env()

        assert env.log_level == level

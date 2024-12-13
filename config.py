import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Env:
    history_length: int
    log_level: str
    local_path: str

    def __init__(self):
        self.local_path = os.getenv("AI_LOCAL_PATH", "")
        self.history_length = int(os.getenv("HISTORY_LENGTH", "20"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        assert self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


env = Env()

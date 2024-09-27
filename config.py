import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "local_path": os.getenv("LOCAL_PATH"),
    "rabbitmq_host": os.getenv("RABBITMQ_HOST"),
    "rabbitmq_user": os.getenv("RABBITMQ_USER"),
    "rabbitmq_password": os.getenv("RABBITMQ_PASSWORD"),
    "rabbitmq_queue": os.getenv("RABBITMQ_QUEUE"),
    "history_length": int(os.getenv("HISTORY_LENGTH") or "10"),
}

local_path = config["local_path"]

chunk_size = 3000
# token limit for for the completion of the chat model, this does not include the overall context length
max_token_limit = 2000

LOG_LEVEL = os.getenv(
    "LOG_LEVEL"
)  # Possible values: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
assert LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

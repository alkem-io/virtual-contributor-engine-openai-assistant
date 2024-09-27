import re

from openai.types import FileObject
from openai.types.beta.thread_create_params import MessageAttachment
from logger import setup_logger

logger = setup_logger(__name__)


def clear_tags(message):
    return re.sub(r"(-? ?\[@?.*\]\(.*?\))|}|{", "", message).strip()


def attach_file(file: FileObject) -> MessageAttachment:
    return {
        "file_id": file.id,
        "tools": [{"type": "file_search"}],
    }

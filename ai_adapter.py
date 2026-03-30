import asyncio
import os
import time

from alkemio_virtual_contributor_engine.setup_logger import setup_logger
from alkemio_virtual_contributor_engine.events.input import Input
from alkemio_virtual_contributor_engine.events.response import Response

from openai import AsyncOpenAI
from openai.types.beta.threads import TextContentBlock
from utils import attach_file

logger = setup_logger(__name__)


async def invoke(input: Input) -> Response:
    logger.info(input)
    try:
        # important to await the result before returning
        return await query_chain(input)
    except Exception as inst:
        logger.exception(inst)
        result = (
            f"{input.display_name}"
            " - the Alkemio's VirtualContributor is currently unavailable."
        )

        return Response(
            result=result,
            original_result=result,
            sources=[],
        )


async def query_chain(input: Input) -> Response:

    external_config = input.external_config
    question = input.message

    client = AsyncOpenAI(api_key=external_config.api_key)

    files = await client.files.list()

    logger.debug(f"External metadata: {input.external_metadata}")
    if input.external_metadata and input.external_metadata.thread_id:
        thread = await client.beta.threads.retrieve(
            input.external_metadata.thread_id
        )
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
            attachments=list(map(attach_file, files)),
        )
    else:
        thread = await client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "attachments": list(map(attach_file, files)),
                }
            ]
        )

    run = await client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=external_config.assistant_id
    )

    terminal_states = {
        "completed", "failed", "cancelled", "expired",
        "incomplete", "requires_action",
    }
    timeout_seconds = int(os.getenv("RUN_POLL_TIMEOUT_SECONDS", "300"))
    start = time.monotonic()
    while run.status not in terminal_states:
        elapsed = time.monotonic() - start
        if elapsed > timeout_seconds:
            logger.error(
                f"Run {run.id} timed out after {elapsed:.0f}s "
                f"(status: {run.status})"
            )
            raise TimeoutError(
                f"OpenAI run polling timed out after {timeout_seconds}s"
            )
        await asyncio.sleep(1)
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        logger.info(f"Run status: {run.status}")

    if run.status != "completed":
        error_msg = (
            run.last_error.message if run.last_error else run.status
        )
        raise RuntimeError(f"OpenAI run {run.status}: {error_msg}")

    messages = await client.beta.threads.messages.list(thread.id)

    logger.info(type(messages.data[0].content[0]))

    answer = ""

    # process image generation differently
    if isinstance(messages.data[0].content[0], TextContentBlock):
        answer = messages.data[0].content[0].text.value
        for citation in messages.data[0].content[0].text.annotations:
            answer = answer.replace(citation.text, "")

    response = Response(
        result=answer,
        thread_id=thread.id,
    )

    return response

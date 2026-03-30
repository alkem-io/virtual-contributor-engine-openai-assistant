from dotenv import load_dotenv

load_dotenv()

import asyncio  # noqa: E402
import os  # noqa: E402
from alkemio_virtual_contributor_engine.alkemio_vc_engine import (  # noqa: E402
    AlkemioVirtualContributorEngine,
)
from alkemio_virtual_contributor_engine.events.input import Input  # noqa: E402
from alkemio_virtual_contributor_engine.events.response import Response  # noqa: E402
from alkemio_virtual_contributor_engine.setup_logger import setup_logger  # noqa: E402

from config import env  # noqa: E402
import ai_adapter  # noqa: E402

logger = setup_logger(__name__)

logger.info(f"log level {os.path.basename(__file__)}: {env.log_level}")


async def on_request(input: Input) -> Response:
    logger.info(f"OpenAI Assistant engine invoked; Input is {input.model_dump()}")
    logger.info(
        f"AiPersonaID={input.persona_id} with VC name `{input.display_name}` invoked."
    )
    result = await ai_adapter.invoke(input)
    logger.info(f"LLM result: {result.model_dump()}")
    return result


engine = AlkemioVirtualContributorEngine()
engine.register_handler(on_request)
asyncio.run(engine.start())

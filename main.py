from dotenv import load_dotenv

load_dotenv()


import asyncio
import os
from alkemio_virtual_contributor_engine.alkemio_vc_engine import (
    AlkemioVirtualContributorEngine,
)
from alkemio_virtual_contributor_engine.events.input import Input
from alkemio_virtual_contributor_engine.events.response import Response
from alkemio_virtual_contributor_engine.setup_logger import setup_logger

from config import env
import ai_adapter

logger = setup_logger(__name__)

logger.info(f"log level {os.path.basename(__file__)}: {env.log_level}")


async def on_request(input: Input) -> Response:
    logger.info(f"Expert engine invoked; Input is {input.to_dict()}")
    logger.info(
        f"AiPersonaServiceID={input.persona_service_id} with VC name `{input.display_name}` invoked."
    )
    result = await ai_adapter.invoke(input)
    logger.info(f"LLM result: {result.to_dict()}")
    return result


engine = AlkemioVirtualContributorEngine()
engine.register_handler(on_request)
asyncio.run(engine.start())

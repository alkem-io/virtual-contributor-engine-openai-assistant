from alkemio_virtual_contributor_engine.alkemio_vc_engine import Input, Response
from openai import OpenAI
from openai.types.beta.threads import TextContentBlock
from logger import setup_logger
from utils import attach_file

logger = setup_logger(__name__)


async def invoke(input: Input) -> Response:
    logger.info(input)
    try:
        # important to await the result before returning
        return await query_chain(input)
    except Exception as inst:
        logger.exception(inst)
        result = f"{input.display_name} - the Alkemio's VirtualContributor is currently unavailable."

        return Response(
            {
                "result": result,
                "original_result": result,
                "sources": [],
            }
        )


async def query_chain(input: Input) -> Response:

    external_config = input.external_config
    question = input.message

    client = OpenAI(api_key=external_config["apiKey"])

    files = client.files.list()

    print(input.external_metadata)
    if "threadId" in input.external_metadata:
        thread = client.beta.threads.retrieve(input.external_metadata["threadId"])
    else:
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": question,
                    "attachments": list(map(attach_file, files)),
                }
            ]
        )

    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=external_config["assistantId"]
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread.id)

    logger.info(type(messages.data[0].content[0]))

    answer = ""

    # process image generation differently
    if isinstance(messages.data[0].content[0], TextContentBlock):
        answer = messages.data[0].content[0].text.value
        for citation in messages.data[0].content[0].text.annotations:
            answer = answer.replace(citation.text, "")

    response = Response(
        {
            "result": answer,
            "thread_id": thread.id,
            **input.to_dict(),
        }
    )
    # response.result = answer

    return response

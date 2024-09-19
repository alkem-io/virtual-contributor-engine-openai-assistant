from openai import OpenAI
from openai.types.beta.threads import TextContentBlock
from logger import setup_logger
from utils import attach_file

logger = setup_logger(__name__)


async def invoke(message):
    logger.info(message)
    try:
        # important to await the result before returning
        return await query_chain(message)
    except Exception as inst:
        logger.exception(inst)
        return f"{message['displayName']} - the Alkemio's VirtualContributor is currently unavailable."


async def query_chain(message):

    external_config = message["externalConfig"]
    question = message["question"]
    response = message
    del response["history"]

    client = OpenAI(api_key=external_config["apiKey"])

    files = client.files.list()

    if "externalMetadata" in message and "threadId" in "externalMetadata" in message:
        thread = client.beta.threads.retrieve(message["externalMetadata"]["threadId"])
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
        response["threadId"] = thread.id

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
        # for citation in messages.data[0].content[0].text.annotations:
        #     answer = answer.replace(citation.text, "")

    response["answer"] = answer

    return response

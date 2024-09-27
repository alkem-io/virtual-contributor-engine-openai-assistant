import ai_adapter
import asyncio
import os
import aio_pika
import aiormq
import json
from aio_pika import connect_robust
from config import config, LOG_LEVEL
from logger import setup_logger
from utils import clear_tags

logger = setup_logger(__name__)

logger.info(f"log level {os.path.basename(__file__)}: {LOG_LEVEL}")


class RabbitMQ:
    def __init__(self, host, login, password, queue):
        self.host = host
        self.login = login
        self.password = password
        self.queue = queue
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(
            host=self.host, login=self.login, password=self.password
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.queue, durable=True, auto_delete=False)


rabbitmq = RabbitMQ(
    host=config["rabbitmq_host"],
    login=config["rabbitmq_user"],
    password=config["rabbitmq_password"],
    queue=config["rabbitmq_queue"],
)


async def query(user_id, message_body):
    # trim the VC tag
    message_body["question"] = clear_tags(message_body["question"])

    logger.info(f"Query from user {user_id}: {message_body['question']}")

    response = await ai_adapter.invoke(message_body)

    logger.debug(f"LLM result: {response}")

    logger.info(response)

    return json.dumps(response)


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        user_id = body["data"].get("userID")

        logger.debug(body)
        response = await query(user_id, body["data"])

        if rabbitmq.connection and rabbitmq.channel:
            try:
                if rabbitmq.connection.is_closed or rabbitmq.channel.is_closed:
                    logger.error(
                        "Connection or channel is not open. Cannot publish message."
                    )
                    return

                await rabbitmq.channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(
                            {"operation": "feedback", "result": response}
                        ).encode(),
                        correlation_id=message.correlation_id,
                        reply_to=message.reply_to,
                    ),
                    routing_key=message.reply_to or "",
                )
                logger.info(
                    f"Response sent for correlation_id: {message.correlation_id}"
                )
                logger.info(f"Response sent to: {message.reply_to}")
                logger.debug(f"response: {response}")
            except (
                aio_pika.exceptions.AMQPError,
                asyncio.exceptions.CancelledError,
                aiormq.exceptions.ChannelInvalidStateError,
            ) as e:
                logger.error(f"Failed to publish message due to a RabbitMQ error: {e}")


async def main():
    logger.info("main fucntion (re)starting\n")
    # rabbitmq is an instance of the RabbitMQ class defined earlier
    await rabbitmq.connect()

    if rabbitmq.channel:
        await rabbitmq.channel.set_qos(prefetch_count=20)
        queue = await rabbitmq.channel.declare_queue(
            rabbitmq.queue, durable=True, auto_delete=False
        )

        # Start consuming messages
        asyncio.create_task(queue.consume(process_message))

        logger.info("Waiting for RPC requests")

    # Create an Event that is never set, and wait for it forever
    # This will keep the program running indefinitely
    stop_event = asyncio.Event()
    await stop_event.wait()


asyncio.run(main())

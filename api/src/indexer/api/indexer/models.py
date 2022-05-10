import asyncio

from typing import Optional

import aiokafka
from aiokafka.errors import KafkaError, KafkaTimeoutError

from fastapi import Request

from . import exceptions


class AlertsManager:

    def __init__(self, broker_url: str, topic: str):
        self.broker_url = broker_url
        self.topic = topic

    async def kafka_alerts(self, request: Request):
        loop = asyncio.get_event_loop()
        consumer = aiokafka.AIOKafkaConsumer(self.topic,
                                             loop=loop,
                                             client_id="indexer.api",
                                             group_id="indexer",
                                             bootstrap_servers=self.broker_url,
                                             enable_auto_commit=False,
                                             auto_offset_reset="earliest")
        await consumer.start()
        try:
            async for alert in consumer:

                if await request.is_disconnected():
                    break
                event = {
                    "event": "alert",
                    "id": alert.key,
                    "retry": 2000,
                    "data": alert.value
                }
                yield event
                await consumer.commit()

        except KafkaError as e:
            raise exceptions.AlertsError from e

        finally:
            await consumer.stop()

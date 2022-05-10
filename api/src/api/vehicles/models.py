import asyncio

from typing import Optional
from sqlalchemy import select, func

import aiokafka
from aiokafka.errors import KafkaError, KafkaTimeoutError

from fastapi import Request

from api.db import DB
from . import entities, exceptions


class VehiclesManager:

    def __init__(self, db: DB):
        self.db = db
        self.db.generate_db()

    def detections(self, skip: Optional[int] = None, limit: Optional[int] = None):
        stmt = select(entities.Detection)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        with self.db.session() as session:
            rs = [d for d in session.execute(stmt).all()]
        return rs

    # def add_detection(self, detection: dict[str, Any]):
    def add_detection(self, **kw):
        detection = DB.from_dict(entities.Detection, kw)
        with self.db.session() as session:
            session.add(detection)
            session.commit()

    def vehicles_by_make(self):
        stmt = select(entities.Detection.make, func.count(entities.Detection.id).label("count")).group_by(entities.Detection.make).order_by(entities.Detection.make)
        with self.db.session() as session:
            rs = [v for v in session.execute(stmt)]
        return rs


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

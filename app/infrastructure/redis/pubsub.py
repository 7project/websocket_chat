import aioredis

from application.mediator import Mediator
from domain.events.base import BaseEvent

redis = aioredis.from_url("redis://localhost")


async def redis_event_publisher(event: BaseEvent):
    await redis.publish("message_events", event.json())


async def listen_redis_events(mediator: Mediator):
    pubsub = redis.pubsub()
    await pubsub.subscribe("message_events")
    async for message in pubsub.listen():
        if message["type"] == "message":
            event = BaseEvent.parse_raw(message["data"])
            await mediator.publish(event)
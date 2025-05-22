import aioredis

from application.mediator import Mediator
from domain.events.base import BaseEvent
from settings.config import settings

redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True)

async def redis_event_publisher(event: BaseEvent):
    await redis.publish("message_events", event.json())


async def listen_redis_events(mediator: Mediator):
    pubsub = redis.pubsub()
    await pubsub.subscribe("message_events")
    async for message in pubsub.listen():
        if message["type"] == "message":
            event = BaseEvent.parse_raw(message["data"])
            await mediator.publish(event)
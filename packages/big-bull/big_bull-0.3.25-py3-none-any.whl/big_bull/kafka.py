import logging

import opentracing
from aiokafka import AIOKafkaConsumer
from big_bull import graph, jaeger

logger = logging.getLogger(__name__)

_kafka_consumer_registry = []


def get_kafka_consumer_span(message, tracer):
    logger.info("Received message with headers %s", message.headers)
    span_context = tracer.extract(
        format=opentracing.Format.HTTP_HEADERS,
        carrier=dict((x, y.decode("utf8")) for x, y in message.headers) or {},
    )
    span = tracer.start_span(
        operation_name=f"from_{message.topic}", references=opentracing.follows_from(span_context)
    )
    span.set_tag("span.kind", "consumer")
    span.set_tag("message_bus.destination", message.topic)
    span.set_tag("message_bus.timestamp", message.timestamp)
    span.set_tag("message_bus.timestamp_type", message.timestamp_type)

    return span


def get_kafka_wrapper(func, injectables={}):
    async def inner(message, *args, **kwargs):
        tracer = jaeger.tracer
        span = get_kafka_consumer_span(message, tracer)
        with tracer.scope_manager.activate(span, True):
            return await graph.inject_func(func, injectables, *args, message=message, **kwargs)
    return inner


def consumer(*args, **kwargs):
    def decorator(func):
        _kafka_consumer_registry.append((func, args, kwargs))
        return get_kafka_wrapper(func)

    return decorator


async def kafka_consumer_task(func, injectables, *args, **kwargs):
    consumer = AIOKafkaConsumer(*args, **kwargs)
    try:
        await consumer.start()
        async for message in consumer:
            await get_kafka_wrapper(func, injectables)(message=message)
    finally:
        await consumer.stop()


def register_kafka_consumers(injectables, loop):
    for (func, args, kwargs) in _kafka_consumer_registry:
        loop.create_task(kafka_consumer_task(func, injectables, *args, **kwargs))

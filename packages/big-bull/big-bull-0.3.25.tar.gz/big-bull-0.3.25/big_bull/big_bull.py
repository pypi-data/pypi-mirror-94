import argparse
import asyncio
import importlib
import logging
import logging.config
from concurrent.futures import CancelledError
from pathlib import Path

from aiohttp import web

from .route import register_route_endpoints
from .jaeger import initialize_jaeger
from .kafka import register_kafka_consumers
from .init import run_init_tasks
from .logging import get_logging_config

logger = logging.getLogger(__name__)


def handle_exception(loop, context):
    exc = context.get('exception')
    if exc:
        logging.critical("Exception", exc_info=exc)
        for task in asyncio.all_tasks():
            try:
                task.cancel()
            except CancelledError:
                pass
    else:
        loop.default_exception_handler(context)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--service-name", required=True)
    args = parser.parse_args()

    log_config = get_logging_config(level=args.log_level)
    logging.config.dictConfig(log_config)
    initialize_jaeger(service_name=args.service_name)

    logger.info("Parsing modules...")
    for path in Path(args.path).rglob("*.py"):
        logger.info("Importing %s", path)
        importlib.import_module(".".join(path.parts)[:-3])

    loop = asyncio.get_event_loop()
    logger.info("Running init tasks...")
    graph = loop.run_until_complete(run_init_tasks())

    logger.info("Registering kafka consumers...")
    loop.set_exception_handler(handle_exception)
    register_kafka_consumers(graph, loop)

    logger.info("Registering endpoints...")
    app = register_route_endpoints(graph)
    try:
        web.run_app(app, access_log=None)
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == "__main__":
    main()

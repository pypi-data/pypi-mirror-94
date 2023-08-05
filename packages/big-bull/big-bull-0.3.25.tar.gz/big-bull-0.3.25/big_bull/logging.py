import logging


class QuoteEscapingFormatter(logging.Formatter):
    def _escape_msg(self, msg):
        return str(msg).replace("\n", "\\n").replace('"', '\\"')

    def format(self, record):
        record.msg = self._escape_msg(record.msg)
        if record.exc_info:
            record.msg = self._escape_msg(super().formatException(record.exc_info))
            record.exc_info = None
            record.exc_text = None
        return super().format(record)


def get_logging_config(level):
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "()": "big_bull.logging.QuoteEscapingFormatter",
                "format": "name=%(name)s level=%(levelname)s ts=%(asctime)s "
                + 'caller=%(filename)s:%(lineno)d msg="%(message)s"',
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "default": {
                "level": level,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": level,
                "propagate": False,
            },
            "big_bull": {
                "handlers": ["default"],
                "level": level,
                "propagate": False,
            },
        },
    }

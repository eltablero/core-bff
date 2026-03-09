import sys

import structlog


def setup_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            # Si es una terminal, usa colores; si no, JSON (para Azure)
            structlog.processors.JSONRenderer()
            if not sys.stderr.isatty()
            else structlog.dev.ConsoleRenderer(),  # noqa: E501
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger()

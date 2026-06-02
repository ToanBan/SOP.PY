import logging
from datetime import datetime
import uuid
import structlog


def custom_processor(_, __, event_dict):

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "level": event_dict.pop("level", "").upper(),
        "service": event_dict.pop("service", "chat"),
        "req_id": event_dict.pop("req_id", str(uuid.uuid4())),
        "trace_id": event_dict.pop("trace_id", None),
        "user_id": event_dict.pop("user_id", None),
        "msg": event_dict.pop("event", ""),
        "extra": event_dict,
    }


def configure_logging():
    logging.basicConfig(
        filename="src/pkg/logger/logs/app.log",
        level=logging.INFO,
        format="%(message)s",
    )

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            custom_processor,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
import logging
import json
import time
import uuid


def get_logger(name: str, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s\n\n')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger

def log_structured(logger, level, msg, **kwargs):
    # Enrich with correlation id, timestamp
    log_record = {
        "timestamp": time.time(),
        "correlation_id": str(uuid.uuid4()),
        "message": msg,
        "context": kwargs
    }
    if level == "info":
        logger.info(json.dumps(log_record))
    elif level == "error":
        logger.error(json.dumps(log_record))
    elif level == "warn":
        logger.warning(json.dumps(log_record))
    else:
        logger.debug(json.dumps(log_record))

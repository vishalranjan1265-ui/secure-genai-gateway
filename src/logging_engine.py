import sys
import logging
from typing import Dict, Any
from utils import load_gateway_config

config = load_gateway_config()
log_level_str = config.get("global", {}).get("log_level", "INFO")

logging.basicConfig(
    level=getattr(logging, log_level_str, logging.INFO),
    format='{"timestamp":"%(asctime)s", "service":"GenAiGateway", "level":"%(levelname)s", "message":%(message)s}',
    stream=sys.stdout
)
logger = logging.getLogger("SecureGateway")

def log_structured_event(event_type: str, metadata: Dict[str, Any]) -> None:
    payload = {
        "event_type": event_type,
        "details": metadata
    }
    logger.info(str(payload).replace("'", '"'))
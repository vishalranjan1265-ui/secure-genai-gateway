import os
import yaml
from typing import Dict, Any

def load_gateway_config() -> Dict[str, Any]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {
            "global": {"log_level": "INFO", "server_port": 8080, "server_host": "0.0.0.0"},
            "security": {"enable_pii_scrubbing": True, "enable_injection_protection": True}
        }
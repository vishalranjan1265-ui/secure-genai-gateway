from typing import List, tuple
from utils import load_gateway_config

class ContentResponseFilter:
    def __init__(self) -> None:
        self.blocked_keywords: List[str] = load_gateway_config().get("filters", {}).get("blocked_keywords", [])

    def verify_output_safety(self, response_text: str) -> tuple[bool, List[str]]:
        violations: List[str] = []
        normalized_text = response_text.lower()
        
        for keyword in self.blocked_keywords:
            if keyword in normalized_text:
                violations.append(f"RESPONSE_LEAKAGE_SHIELD: Containment broken on term ({keyword})")
        
        is_compromised = len(violations) > 0
        return is_compromised, violations
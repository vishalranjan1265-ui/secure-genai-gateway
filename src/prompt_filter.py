import re
from typing import List, Dict, Any, tuple
from utils import load_gateway_config

class PromptVulnerabilityFilter:
    def __init__(self) -> None:
        self.config = load_gateway_config().get("filters", {})
        self.blocked_keywords: List[str] = self.config.get("blocked_keywords", [])
        
        # Precompile standard PII pattern matching matrices
        self.patterns: Dict[str, re.Pattern] = {
            name: re.compile(raw_regex) 
            for name, raw_regex in self.config.get("pii_patterns", {}).items()
        }

    def inspect_and_scrub(self, input_prompt: str) -> tuple[str, bool, List[str]]:
        triggered_violations: List[str] = []
        is_adversarial = False
        
        # 1. Prompt Injection Validations
        normalized_prompt = input_prompt.lower()
        for keyword in self.blocked_keywords:
            if keyword in normalized_prompt:
                is_adversarial = True
                triggered_violations.append(f"PROMPT_INJECTION_VECTOR: {keyword}")

        # 2. PII Tracking and Elimination Phase
        scrubbed_prompt = input_prompt
        for label, regex_compiled in self.patterns.items():
            if regex_compiled.search(scrubbed_prompt):
                triggered_violations.append(f"PII_LEAKAGE_DETECTED: {label.upper()}")
                scrubbed_prompt = regex_compiled.sub(f"[SCRUBBED_{label.upper()}]", scrubbed_prompt)

        return scrubbed_prompt, is_adversarial, triggered_violations
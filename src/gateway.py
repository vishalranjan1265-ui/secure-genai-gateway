import time
from typing import Dict, Any, List
from prompt_filter import PromptVulnerabilityFilter
from content_filter import ContentResponseFilter
from llm_client import AmazonBedrockGatewayClient
from encryption import PayloadEncryptor
from logging_engine import log_structured_event
from monitoring import metrics_engine

class GatewayOrchestratorEngine:
    def __init__(self) -> None:
        self.prompt_filter = PromptVulnerabilityFilter()
        self.content_filter = ContentResponseFilter()
        self.llm_engine = AmazonBedrockGatewayClient()
        self.encryptor = PayloadEncryptor()

    def orchestrate_request(self, raw_prompt: str) -> Dict[str, Any]:
        start_time = time.time()
        log_structured_event("INGRESS_REQUEST_STARTED", {"prompt_length": len(raw_prompt)})
        
        # 1. Ingress Analysis & Scrubbing
        scrubbed_prompt, is_adversarial, inline_violations = self.prompt_filter.inspect_and_scrub(raw_prompt)
        
        if is_adversarial:
            metrics_engine.record_transaction(time.time() - start_time, len(inline_violations))
            log_structured_event("SECURITY_INTERCEPTION_PROMPT", {"violations": inline_violations})
            return {
                "status": "BLOCKED",
                "reason": "Security controls flagged suspicious structural patterns inside input prompt.",
                "violations": inline_violations
            }

        # 2. Upstream Dispatching
        try:
            llm_result = self.llm_engine.invoke_model_endpoint(scrubbed_prompt)
            raw_output = llm_result["response_text"]
        except Exception as e:
            metrics_engine.record_transaction(time.time() - start_time, 0)
            return {"status": "ERROR", "reason": f"Upstream provider execution crash: {str(e)}"}

        # 3. Egress Analysis
        is_output_compromised, output_violations = self.content_filter.verify_output_safety(raw_output)
        if is_output_compromised:
            metrics_engine.record_transaction(time.time() - start_time, len(output_violations))
            log_structured_event("SECURITY_INTERCEPTION_RESPONSE", {"violations": output_violations})
            return {
                "status": "BLOCKED",
                "reason": "Upstream system output containment thresholds violated configuration rules.",
                "violations": output_violations
            }

        execution_latency = time.time() - start_time
        metrics_engine.record_transaction(execution_latency, len(inline_violations))
        
        # 4. Cryptographic Record Hardening
        encrypted_audit_log = self.encryptor.encrypt_data_string(f"In: {scrubbed_prompt} | Out: {raw_output}")

        log_structured_event("REQUEST_SUCCESSFUL", {
            "latency": execution_latency,
            "usage": llm_result["token_usage"]
        })

        return {
            "status": "SUCCESS",
            "output": raw_output,
            "metrics": {
                "latency_seconds": round(execution_latency, 4),
                "token_usage": llm_result["token_usage"]
            },
            "secure_audit_token": encrypted_audit_log
        }
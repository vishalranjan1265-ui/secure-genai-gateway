from fastapi import FastAPI, Depends, Security
from api_gateway import PromptPayloadSchema, GatewayResponseSchema
from auth import authenticate_gateway_request
from gateway import GatewayOrchestratorEngine
from monitoring import metrics_engine

app = FastAPI(
    title="Secure Enterprise GenAI Proxy Gateway",
    version="1.0.0",
    description="Protective firewall shield intercepts prompt injection, scrubs PII, and forces output metrics tracking."
)

orchestration_driver = GatewayOrchestratorEngine()

@app.post("/v1/chat/completions", response_model=GatewayResponseSchema, dependencies=[Depends(authenticate_gateway_request)])
def route_secure_chat_payload(payload: PromptPayloadSchema) -> Dict[str, Any]:
    response = orchestration_driver.orchestrate_request(payload.prompt)
    return response

@app.get("/health", tags=["SystemDiagnostics"])
def run_health_check() -> Dict[str, str]:
    return {"status": "HEALTHY", "engine": "GenAiShield-v1"}

@app.get("/metrics", tags=["Observability"])
def gather_runtime_telemetry(authenticated: str = Depends(authenticate_gateway_request)) -> Dict[str, Any]:
    return metrics_engine.compile_metrics_snapshot()
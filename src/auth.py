import os
from fastapi import Header, HTTPException, Security
from fastapi.security import APIKeyHeader
from utils import load_gateway_config

config = load_gateway_config()
HEADER_NAME = config.get("security", {}).get("api_key_header", "X-Gateway-API-Key")
api_key_header_auth = APIKeyHeader(name=HEADER_NAME, auto_error=False)

def authenticate_gateway_request(api_key: str = Security(api_key_header_auth)) -> str:
    expected_key = os.getenv("GATEWAY_ROOT_API_KEY", "sk-secure-genai-gateway-super-secret-key-2026")
    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=401,
            detail="Access Denied. Provided authorization token mapping matches zero verified profiles."
        )
    return "AuthenticatedAdminContext"
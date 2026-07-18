from pydantic import BaseModel, Field

class PromptPayloadSchema(BaseModel):
    prompt: str = Field(..., min_length=1, description="Raw input text targeting downstream model entities.")

class GatewayResponseSchema(BaseModel):
    status: str
    output: str = ""
    reason: str = ""
    violations: list = []
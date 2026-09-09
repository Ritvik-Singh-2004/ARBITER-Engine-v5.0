from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class NFCPayload(BaseModel):
    entity_id: str = Field(..., description="Unique ID of the NFC tag/asset")
    cryptographic_signature: str = Field(..., description="Encrypted tag signature")
    scan_timestamp: str = Field(..., description="ISO timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom JSON attributes")

class RiskAssessmentResponse(BaseModel):
    entity_id: str
    status: str
    quick_flag: bool = Field(..., description="True if UI should show warning animation")
    message: str
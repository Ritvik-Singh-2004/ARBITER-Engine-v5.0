from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class AssetScanPayload(BaseModel):
    entity_id: str = Field(..., description="Unique ID of the asset/note")
    cryptographic_signature: str = Field(..., description="Signature or hash")
    scan_timestamp: str = Field(..., description="ISO timestamp")
    
    # Optional Geo-Spatial Telemetry (from Arbiter v1)
    latitude: Optional[float] = Field(None, description="Current scan latitude")
    longitude: Optional[float] = Field(None, description="Current scan longitude")
    previous_latitude: Optional[float] = Field(None, description="Last recorded latitude")
    previous_longitude: Optional[float] = Field(None, description="Last recorded longitude")
    
    # Catch-all for whatever loose fields your team decides to add
    metadata: Dict[str, Any] = Field(default_factory=dict)
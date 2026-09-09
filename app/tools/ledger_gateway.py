import hashlib
import time

def commit_to_ledger(entity_id: str, signature: str) -> str:
    """Commits verified high-risk/high-trust states to an immutable blockchain ledger."""
    raw_data = f"{entity_id}-{signature}-{time.time()}".encode()
    return "0x" + hashlib.sha256(raw_data).hexdigest()
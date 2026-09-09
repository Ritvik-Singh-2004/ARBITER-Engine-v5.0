import logging

logger = logging.getLogger(__name__)

def update_user_risk_profile(user_id: str, asset_risk_level: str, asset_multiplier: float) -> bool:
    """Separates user trust scoring from physical asset state."""
    adjustment = -5 if asset_risk_level == "HIGH" else (1 if asset_multiplier < 1 else 0)
    logger.info(f"User {user_id} trust score adjusted by {adjustment}.")
    return True
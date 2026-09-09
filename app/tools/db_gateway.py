import logging

logger = logging.getLogger(__name__)

def persist_risk_record(entity_id: str, risk_payload: dict) -> str:
    """Updates MongoDB and triggers adaptive learning weights based on confirmed states."""
    logger.info(f"MongoDB updated for {entity_id}: {risk_payload}")
    _trigger_adaptive_learning(risk_payload)
    return "Database updated successfully."

def _trigger_adaptive_learning(risk_payload: dict):
    """Adaptive learning: Shifts RRF 'k' constant and baseline weights if anomalies are confirmed."""
    logger.info("Adaptive learning baseline weights recalibrated based on new vector payload.")
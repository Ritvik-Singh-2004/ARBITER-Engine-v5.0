from typing import Dict, Any, Tuple, List

def calculate_dynamic_risk(
    current_score: float, 
    fusion_score: float, 
    crypto_valid: bool, 
    metadata: Dict[str, Any]
) -> Tuple[float, float, str, List[str]]:
    """
    Calculates dynamic risk multiplier based on vector similarity and crypto validity.
    fusion_score: 0.0 to 1.0 (higher = closer match to authentic reference profile).
    """
    reasons: List[str] = []
    multiplier: float = 1.0

    # 1. Cryptographic Signature Check
    if not crypto_valid:
        multiplier *= 1.80  
        reasons.append("CRITICAL: Invalid cryptographic signature.")
    
    # 2. Physical Tamper Flag Check
    if metadata and metadata.get("tamper_flag"):
        multiplier *= 1.50
        reasons.append("CRITICAL: Physical tamper flag detected.")

    # 3. Vector Similarity (Fusion Score) Evaluation
    if fusion_score >= 0.75:
        # High match to genuine baseline -> Discount risk!
        multiplier *= 0.50  
        reasons.append(f"PASS: High vector match with authentic profile (RRF: {fusion_score:.2f}).")
    elif fusion_score >= 0.40:
        # Moderate drift -> Mild risk increase
        multiplier *= 1.10  
        reasons.append(f"WARNING: Moderate metadata drift observed (RRF: {fusion_score:.2f}).")
    else:
        # Low match / high anomaly -> Severe risk multiplier
        multiplier *= 1.80  
        reasons.append(f"ANOMALY: High semantic drift from authentic profile (RRF: {fusion_score:.2f}).")

    # Final score calculation strictly capped between 0 and 100
    new_risk_score = round(min(max(current_score * multiplier, 0.0), 100.0), 2)
    multiplier = round(multiplier, 2)

    if new_risk_score >= 75.0:
        risk_level = "HIGH"
    elif new_risk_score >= 40.0:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return new_risk_score, multiplier, risk_level, reasons
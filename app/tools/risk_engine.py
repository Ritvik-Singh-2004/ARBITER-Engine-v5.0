from typing import Dict, Any, Tuple, List

def calculate_dynamic_risk(current_score: float, fusion_score: float, crypto_valid: bool, metadata: Dict[str, Any]) -> str:
    """Dynamic multiplier logic, strictly capped at 100."""
    reasons: List[str] = []
    multiplier: float = 1.0

    if not crypto_valid:
        multiplier *= 1.50  
        reasons.append("CRITICAL: Invalid cryptographic signature.")
    
    if fusion_score > 0.75:
        multiplier *= 1.80  
        reasons.append(f"ANOMALY: High vector similarity to counterfeit profiles (RRF: {fusion_score:.2f}).")
    elif fusion_score > 0.40:
        multiplier *= 1.20  
    else:
        multiplier *= 0.85  
        reasons.append("PASS: Semantic vectors indicate authentic baseline profiles.")

    new_risk_score = round(min(max(current_score * multiplier, 0.0), 100.0), 2)
    return f"Score: {new_risk_score}/100, Multiplier: {multiplier:.2f}, Reasons: {reasons}"
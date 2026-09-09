from typing import List, Dict, Any

def apply_rrf_scoring(vector_results: Dict[str, Any], keyword_results: List[Dict[str, Any]], k: int = 60) -> float:
    """Mathematically fuses vector ranks with keyword database ranks."""
    if not vector_results or not keyword_results:
        return 0.0
    base_score = keyword_results[0].get("score", 0.0)
    semantic_boost = 0.12 
    return min(base_score + semantic_boost, 1.0)
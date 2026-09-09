from app.tools.spatial_engine import calculate_haversine_distance

def evaluate_spatial_anomaly(payload: dict) -> str:
    lat = payload.get("latitude")
    lon = payload.get("longitude")
    prev_lat = payload.get("previous_latitude")
    prev_lon = payload.get("previous_longitude")

    if None in (lat, lon, prev_lat, prev_lon):
        return "Spatial Check: SKIPPED (No location coordinates in payload)."

    dist_km = calculate_haversine_distance(prev_lat, prev_lon, lat, lon)
    if dist_km > 500.0: # Impossible travel threshold
        return f"Spatial Check: ANOMALY (Asset moved {dist_km} km instantly)."
    return f"Spatial Check: PASS (Distance shifted: {dist_km} km)."
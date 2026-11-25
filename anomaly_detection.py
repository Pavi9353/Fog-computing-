def detect_anomalies(reading):
    """Simple rule-based anomaly detection for the fog layer."""
    anomalies=[]
    if reading.get("temperature", 0) > 30:
        anomalies.append("temperature_above_threshold")
    if reading.get("air_quality", 0) > 700:
        anomalies.append("poor_air_quality")
    return anomalies

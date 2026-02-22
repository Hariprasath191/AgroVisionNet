def fusion_decision(disease, confidence, climate_risk):

    if confidence > 0.85:
        severity = "Severe"
    elif confidence > 0.7:
        severity = "Moderate"
    else:
        severity = "Early"

    if disease.lower() == "healthy":
        decision = "Crop is healthy."
    elif climate_risk > 0.6:
        decision = "High risk of disease spread."
    else:
        decision = "Monitor crop regularly."

    return severity, decision

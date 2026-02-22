def get_recommendation(disease, severity, risk):

    if disease.lower() == "healthy":
        return ["Crop is healthy.", "Maintain irrigation and monitoring."]

    tips = [
        "Remove infected leaves.",
        "Avoid overhead watering.",
        "Improve air circulation."
    ]

    if severity == "Severe":
        tips.append("Immediate treatment required.")
    elif severity == "Moderate":
        tips.append("Apply preventive fungicide.")
    else:
        tips.append("Monitor daily.")

    return tips

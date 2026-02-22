def get_climate_risk_from_values(temp, humidity, rain, soil):
    if humidity > 80 and rain > 1:
        return 0.8
    elif humidity > 70:
        return 0.5
    else:
        return 0.2

def make_decision(data):
    actions=[]
    if float(data.get("temperature", 0)) > 30:
        actions.append("VENTILATION_ON")
    if int(data.get("air_quality", 0)) > 700:
        actions.append("ALARM_ON")
    return actions

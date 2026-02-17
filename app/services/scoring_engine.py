def calculate_quality_score(static_output: str):
    if "error" in static_output.lower():
        return 60
    return 90


def calculate_scalability_score(code: str):
    if len(code) > 300:
        return 80
    return 90


def calculate_final_score(q, s, sc, p):
    return round((q*0.3 + s*0.25 + sc*0.15 + p*0.2), 2)

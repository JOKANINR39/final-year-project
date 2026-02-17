def analyze_security(code: str):
    issues = []
    score = 100

    if "password" in code.lower():
        issues.append("Hardcoded password detected.")
        score -= 20

    if "eval(" in code:
        issues.append("Use of eval() detected.")
        score -= 25

    if "exec(" in code:
        issues.append("Use of exec() detected.")
        score -= 25

    if "shell=True" in code:
        issues.append("subprocess with shell=True detected.")
        score -= 20

    if score < 0:
        score = 0

    return {
        "issues": issues,
        "security_score": score
    }

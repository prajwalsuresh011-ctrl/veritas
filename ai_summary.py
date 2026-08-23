def ai_summary(status, reasons):

    if status in ["SAFE", "Verified", "Likely Genuine"]:
        risk = "LOW"
        recommendation = "Safe for normal use."

    elif status in ["SUSPICIOUS", "Needs Review"]:
        risk = "MEDIUM"
        recommendation = "Verify before proceeding."

    else:
        risk = "HIGH"
        recommendation = "Avoid interacting with this content."

    if reasons:
        reason_text = "\n".join([f"• {r}" for r in reasons])
    else:
        reason_text = "No suspicious indicators detected."

    return f"""
AI Verdict

Status: {status}

Risk Level: {risk}

Analysis:
{reason_text}

Recommendation:
{recommendation}
"""

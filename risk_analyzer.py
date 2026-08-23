# ====================================================
# VERITAS - RISK ANALYZER
# ====================================================

def analyze_risk(data):
    """
    Combine verification results and generate
    a final risk assessment.
    """

    risk_score = 0
    reasons = []

    # ====================================================
    # URL ANALYSIS
    # ====================================================

    if "url" in data:

        url_result = data["url"]

        url_score = url_result.get("score")

        if url_score is not None:

            # Convert Trust Score to Risk Score
            url_risk = 100 - url_score

            risk_score += url_risk

            if url_score < 40:

                reasons.append(
                    "High-risk URL indicators detected."
                )

            elif url_score < 70:

                reasons.append(
                    "Suspicious URL indicators detected."
                )

        elif url_result.get("safe") is False:

            risk_score += 40

            reasons.append(
                "Suspicious URL detected."
            )


    # ====================================================
    # IMAGE ANALYSIS
    # ====================================================

    if "image" in data:

        image_result = data["image"]

        if image_result.get("fake") is True:

            risk_score += 30

            reasons.append(
                "Possible AI-generated or manipulated image detected."
            )


    # ====================================================
    # DOCUMENT ANALYSIS
    # ====================================================

    if "document" in data:

        document_result = data["document"]

        if document_result.get("fake") is True:

            risk_score += 30

            reasons.append(
                "Possible document authenticity issue detected."
            )


    # ====================================================
    # QR CODE ANALYSIS
    # ====================================================

    if "qr" in data:

        qr_result = data["qr"]

        if qr_result.get("unsafe") is True:

            risk_score += 20

            reasons.append(
                "Unsafe QR destination detected."
            )


    # ====================================================
    # LIMIT SCORE
    # ====================================================

    risk_score = min(
        max(risk_score, 0),
        100
    )


    # ====================================================
    # FINAL DECISION
    # ====================================================

    if risk_score >= 70:

        status = "DANGEROUS"

    elif risk_score >= 40:

        status = "SUSPICIOUS"

    else:

        status = "SAFE"


    # ====================================================
    # ANALYSIS CONFIDENCE
    # ====================================================

    if risk_score == 0:

        confidence = 90

    elif risk_score < 40:

        confidence = 75

    elif risk_score < 70:

        confidence = 85

    else:

        confidence = 95


    # ====================================================
    # DEFAULT MESSAGE
    # ====================================================

    if len(reasons) == 0:

        reasons.append(
            "No major security risk indicators were detected."
        )


    # ====================================================
    # FINAL REPORT
    # ====================================================

    return {

        "status": status,

        "risk_score": risk_score,

        "confidence": confidence,

        "reasons": reasons

    }
# ====================================================
# VERITAS - URL CHECKER
# ====================================================

from urllib.parse import urlparse
import ipaddress


def analyze_url(url):

    score = 100
    reasons = []

    # ====================================================
    # BASIC URL VALIDATION
    # ====================================================

    url = url.strip()

    if not url:

        return (
            0,
            "DANGEROUS",
            ["URL is empty."]
        )

    original_url = url

    # Add HTTPS if scheme is missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ====================================================
    # PARSE URL
    # ====================================================

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()
        hostname = parsed.hostname

        if not domain or not hostname:

            return (
                0,
                "DANGEROUS",
                ["Invalid URL or domain."]
            )

    except Exception as e:

        return (
            0,
            "DANGEROUS",
            [f"URL parsing failed: {e}"]
        )

    hostname = hostname.lower()

    # ====================================================
    # HTTPS CHECK
    # ====================================================

    if original_url.startswith("http://"):

        score -= 25

        reasons.append(
            "Website does not use HTTPS."
        )

    # ====================================================
    # IP ADDRESS CHECK
    # ====================================================

    try:

        ipaddress.ip_address(hostname)

        score -= 30

        reasons.append(
            "URL uses an IP address instead of a domain name."
        )

    except ValueError:

        pass

    # ====================================================
    # USERNAME / PASSWORD CHECK
    # ====================================================

    if parsed.username or parsed.password:

        score -= 25

        reasons.append(
            "URL contains embedded username or password information."
        )

    # ====================================================
    # @ SYMBOL CHECK
    # ====================================================

    if "@" in url:

        score -= 30

        reasons.append(
            "URL contains an @ symbol, which may hide "
            "the actual destination."
        )

    # ====================================================
    # SUSPICIOUS KEYWORDS
    # ====================================================

    suspicious_keywords = [

        "login",
        "verify",
        "verification",
        "password",
        "account",
        "secure",
        "update",
        "bank",
        "wallet",
        "claim",
        "free",
        "prize",
        "winner",
        "urgent",
        "otp",
        "payment",
        "refund",
        "bonus"
    ]

    url_lower = url.lower()

    found_keywords = []

    for keyword in suspicious_keywords:

        if keyword in url_lower:

            found_keywords.append(keyword)

    # ====================================================
    # KEYWORD RISK
    # ====================================================

    if len(found_keywords) >= 5:

        score -= 35

        reasons.append(
            "Many high-risk keywords were detected in the URL."
        )

    elif len(found_keywords) >= 3:

        score -= 25

        reasons.append(
            "Multiple suspicious keywords were detected in the URL."
        )

    elif len(found_keywords) >= 1:

        score -= 10

        reasons.append(
            "Suspicious keywords were detected in the URL."
        )

    # ====================================================
    # URL LENGTH
    # ====================================================

    if len(url) > 200:

        score -= 15

        reasons.append(
            "URL is unusually long."
        )

    elif len(url) > 120:

        score -= 8

        reasons.append(
            "URL is longer than usual."
        )

    # ====================================================
    # MULTIPLE SUBDOMAINS
    # ====================================================

    if hostname.count(".") >= 4:

        score -= 15

        reasons.append(
            "URL contains an unusually large number "
            "of subdomains."
        )

    # ====================================================
    # HYPHEN CHECK
    # ====================================================

    if hostname.count("-") >= 3:

        score -= 15

        reasons.append(
            "Domain contains multiple hyphens."
        )

    elif "-" in hostname:

        score -= 5

        reasons.append(
            "Domain contains a hyphen."
        )

    # ====================================================
    # SUSPICIOUS PORT
    # ====================================================

    try:

        port = parsed.port

        if port is not None:

            if port not in [80, 443]:

                score -= 15

                reasons.append(
                    "URL uses an unusual network port."
                )

    except ValueError:

        score -= 20

        reasons.append(
            "URL contains an invalid network port."
        )

    # ====================================================
    # ENCODED CHARACTER CHECK
    # ====================================================

    if "%" in url:

        score -= 5

        reasons.append(
            "URL contains encoded characters."
        )

    # ====================================================
    # HIGH-RISK COMBINATION
    # ====================================================

    high_risk_keywords = [

        "bank",
        "login",
        "verify",
        "password",
        "otp",
        "payment",
        "wallet"
    ]

    high_risk_count = sum(
        keyword in url_lower
        for keyword in high_risk_keywords
    )

    if high_risk_count >= 3:

        score -= 25

        reasons.append(
            "Multiple financial or account-related "
            "security indicators were detected."
        )

    # ====================================================
    # FINAL SCORE
    # ====================================================

    score = max(
        0,
        min(score, 100)
    )

    # ====================================================
    # FINAL STATUS
    # ====================================================

    if score >= 70:

        status = "SAFE"

    elif score >= 40:

        status = "SUSPICIOUS"

    else:

        status = "DANGEROUS"

    # ====================================================
    # NO SUSPICIOUS INDICATORS
    # ====================================================

    if len(reasons) == 0:

        reasons.append(
            "No major suspicious URL indicators were detected."
        )

    # ====================================================
    # RETURN RESULT
    # ====================================================

    return (
        score,
        status,
        reasons
    )
def generate_recommendation(status, reasons):

    # Convert reasons into readable text

    if len(reasons) == 0:

        reason_text = "No suspicious indicators detected."

    else:

        reason_text = ", ".join(reasons)



    # Generate AI style recommendation

    if status in [
        "SAFE",
        "Verified",
        "Likely Genuine"
    ]:

        message = f"""
🟢 This content appears safe.

Analysis:
{reason_text}

Recommendation:
You can proceed, but always verify important information before sharing personal details.
"""


    elif status in [
        "SUSPICIOUS",
        "Needs Review"
    ]:

        message = f"""
🟡 This content requires caution.

Analysis:
{reason_text}

Recommendation:
Avoid entering sensitive information.
Verify the source before downloading files or opening links.
"""


    else:

        message = f"""
🔴 This content appears dangerous.

Analysis:
{reason_text}

Recommendation:
Do not open this content.
Avoid sharing passwords, OTPs, or personal information.
"""


    return message

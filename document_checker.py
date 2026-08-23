import PyPDF2


def analyze_document(uploaded_file):

    reader = PyPDF2.PdfReader(uploaded_file)

    pages = len(reader.pages)

    score = 100
    reasons = []

    # ====================================================
    # PAGE CHECK
    # ====================================================

    if pages == 0:

        score -= 50

        reasons.append(
            "Empty document."
        )

    elif pages > 50:

        score -= 10

        reasons.append(
            "Large document. Manual review recommended."
        )

    # ====================================================
    # TEXT CHECK
    # ====================================================

    text = ""

    try:

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    except Exception:

        text = ""

    if len(text.strip()) < 30:

        score -= 15

        reasons.append(
            "Very little readable text."
        )

    # ====================================================
    # METADATA CHECK
    # ====================================================

    metadata = reader.metadata

    if metadata is None:

        score -= 10

        reasons.append(
            "Metadata missing."
        )

    # ====================================================
    # LIMIT SCORE
    # ====================================================

    score = max(
        0,
        min(score, 100)
    )

    # ====================================================
    # STATUS
    # ====================================================

    if score >= 80:

        status = "Verified"

    elif score >= 50:

        status = "Needs Review"

    else:

        status = "Suspicious"

    # ====================================================
    # NO SUSPICIOUS INDICATORS
    # ====================================================

    if len(reasons) == 0:

        reasons.append(
            "No suspicious indicators were detected."
        )

        reasons.append(
            "The document passed the available verification checks."
        )

    return (
        score,
        status,
        reasons,
        pages
    )
import re
 ollama

from url_checker import analyze_url
from database import get_history


# ====================================================
# URL EXTRACTION
# ====================================================

def extract_url(text):

    pattern = r"https?://[^\s]+"

    match = re.search(
        pattern,
        text
    )

    if match:
        return match.group(0).rstrip(".,!?")

    return None


# ====================================================
# VERITAS AI ASSISTANT
# ====================================================

def ask_veritas(question, username=None):

    # ====================================================
    # URL ANALYSIS
    # ====================================================

    url = extract_url(question)

    if url:

        try:

            score, status, reasons = analyze_url(
                url
            )

            reason_text = "\n".join(
                f"- {reason}"
                for reason in reasons
            )

            prompt = f"""
You are Veritas AI, a cybersecurity verification assistant.

The user provided this URL:

{url}

Veritas URL Analysis:

Trust Score: {score}/100
Status: {status}

Reasons:
{reason_text}

Explain the result clearly and simply.

Give practical safety advice.

Do not invent scan results.
Do not claim that the website is completely safe.
"""

        except Exception as e:

            prompt = f"""
You are Veritas AI, a cybersecurity assistant.

The user provided this URL:

{url}

The URL analysis system encountered an error:

{e}

Explain that the URL could not be fully analyzed.

Do not claim that the website is safe or dangerous.

Recommend that the user avoid opening the URL until
it can be properly verified.
"""

    # ====================================================
    # HISTORY QUESTIONS
    # ====================================================

    elif username and any(
        word in question.lower()
        for word in [
            "history",
            "previous scan",
            "recent scan",
            "last scan",
            "my scans"
        ]
    ):

        history = get_history(
            username
        )

        if len(history) == 0:

            prompt = """
You are Veritas AI.

The user has no previous verification scans.

Tell the user that their scan history is currently empty.

Suggest verifying a URL, QR code, document, or image
to create their first scan.

Keep the answer short and friendly.
"""

        else:

            history_text = ""

            for item in history[:10]:

                history_text += (
                    f"Type: {item[2]}, "
                    f"Target: {item[3]}, "
                    f"Score: {item[4]}/100, "
                    f"Status: {item[5]}, "
                    f"Date: {item[6]}\n"
                )

            prompt = f"""
You are Veritas AI.

The user's recent verification history is:

{history_text}

Answer this question:

{question}

Use only the provided history.

Do not invent scans or results.
"""

    # ====================================================
    # NORMAL CYBERSECURITY QUESTION
    # ====================================================

    else:

        prompt = f"""
You are Veritas AI, a cybersecurity assistant.

Answer the following question:

{question}

Give practical, accurate and easy-to-understand
cybersecurity advice.

Do not invent facts.

Keep the answer reasonably concise.
"""

    # ====================================================
    # OLLAMA
    # ====================================================

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Veritas AI, "
                        "a helpful cybersecurity assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return (
            "⚠️ Veritas AI could not connect to Ollama.\n\n"
            f"Error: {e}\n\n"
            "Please make sure Ollama is running and "
            "the llama3.2 model is available."
        )

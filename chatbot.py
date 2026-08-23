import re
import os

import streamlit as st

from url_checker import analyze_url
from database import get_history


# ====================================================
# OPTIONAL LOCAL OLLAMA
# ====================================================

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# ====================================================
# GEMINI
# ====================================================

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


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
# GEMINI RESPONSE
# ====================================================
# ====================================================
# GEMINI RESPONSE
# ====================================================

def ask_gemini(prompt):

    if not GEMINI_AVAILABLE:

        return (
            "⚠️ Gemini library is not installed.\n\n"
            "Please add `google-genai` to requirements.txt."
        )

    try:

        api_key = st.secrets.get(
            "GEMINI_API_KEY",
            os.getenv("GEMINI_API_KEY")
        )

        if not api_key:

            return (
                "⚠️ Gemini API key is not configured.\n\n"
                "Please add GEMINI_API_KEY to "
                "Streamlit Cloud Secrets."
            )

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        if response.text:

            return response.text

        return (
            "⚠️ Gemini returned an empty response. "
            "Please try again."
        )

    except Exception as e:

        return (
            "⚠️ Veritas AI is temporarily unavailable.\n\n"
            f"Gemini error: {e}\n\n"
            "Please try again in a few moments."
        )

# ====================================================
# OLLAMA RESPONSE
# ====================================================

def ask_ollama(prompt):

    if not OLLAMA_AVAILABLE:

        return None

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

    except Exception:

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
Base your answer only on the provided analysis.
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
    # TRY LOCAL OLLAMA FIRST
    # ====================================================

    ollama_response = ask_ollama(
        prompt
    )

    if ollama_response:

        return ollama_response

    # ====================================================
    # FALLBACK TO GEMINI
    # ====================================================

    return ask_gemini(
        prompt
    )

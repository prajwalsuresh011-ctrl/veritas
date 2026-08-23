import ollama


def ai_security_analysis(
        scan_type,
        target,
        score,
        status,
        reasons
):

    prompt = f"""
You are Veritas_AI, a cybersecurity assistant.

Analyze this verification result.

Type:
{scan_type}

Target:
{target}

Trust Score:
{score}/100

Status:
{status}

Detected Issues:
{reasons}


Give:
1. Security explanation
2. Risk level
3. User recommendation

Keep answer simple and clear.
"""


    response = ollama.chat(

        model="llama3.2",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )


    return response["message"]["content"]
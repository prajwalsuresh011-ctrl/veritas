# 🛡️ Veritas AI

**AI-Powered Digital Trust & Verification Platform**

Veritas AI is a cybersecurity and digital verification platform designed to help users analyze potentially suspicious digital content such as URLs, QR codes, documents, and images.

It combines automated security analysis, verification history, unique Verification IDs, analytics, PDF reports, and an AI-powered cybersecurity assistant in a single platform.

---

## 🌐 Live Demo

**Veritas AI:** Add your deployed Streamlit URL here

---

## 🚀 Features

* 🌐 **URL Verification** — Analyze URLs for potential security risks.
* 📱 **QR Code Verification** — Decode and analyze QR-code content.
* 📄 **Document Analysis** — Analyze uploaded PDF, DOCX, and TXT files.
* 🖼️ **Image Verification** — Analyze image properties and suspicious indicators.
* 🔐 **Verification ID System** — Generate a unique ID for every verification.
* 📊 **Security Analytics** — View scan statistics and security status.
* 🕒 **Verification History** — Access previous verification results.
* 🤖 **AI Security Assistant** — Get cybersecurity guidance using AI.
* 📄 **PDF Reports** — Generate downloadable verification reports.
* 👤 **User Authentication** — User registration and login system.
* 🔒 **User-Specific History** — Users can retrieve their own verification records.

---

## 🧠 How Veritas AI Works

```text
User
 │
 ▼
Veritas AI Dashboard
 │
 ├── URL ──────────────► URL Security Analysis
 │
 ├── QR Code ──────────► QR Decode + Analysis
 │
 ├── Document ─────────► Document Analysis
 │
 └── Image ────────────► Image Analysis
             │
             ▼
       Trust Score + Status
             │
             ▼
      Verification ID
             │
       ┌─────┴─────┐
       ▼           ▼
   History      Analytics
       │
       ▼
   Verify ID
       │
       ▼
   AI Assistant
```

---

## 🛠️ Technologies

| Technology        | Purpose                             |
| ----------------- | ----------------------------------- |
| Python            | Core application logic              |
| Streamlit         | Web application interface           |
| SQLite            | User and verification data storage  |
| OpenCV            | Image and QR processing             |
| Pillow            | Image processing                    |
| PyPDF2            | PDF processing                      |
| Plotly            | Analytics and visualization         |
| Google Gemini API | AI-powered cybersecurity assistance |
| Ollama            | Optional local AI assistant         |
| ReportLab         | PDF report generation               |

---

## 📁 Project Structure

```text
veritas/
│
├── app.py
├── auth.py
├── database.py
│
├── url_checker.py
├── qr_checker.py
├── document_checker.py
├── image_checker.py
│
├── risk_analyzer.py
├── ai_summary.py
├── ai_recommendation.py
├── chatbot.py
├── report_generator.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── veritas_logo.png
```

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd veritas
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

**Never upload `secrets.toml` to GitHub.**

### 4. Start Veritas AI

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Security

Veritas AI uses `.gitignore` to prevent sensitive and unnecessary files from being uploaded to GitHub.

The following files should remain private:

```text
*.db
.env
.streamlit/secrets.toml
.venv/
__pycache__/
```

API keys and passwords should never be hard-coded into the source code or committed to a public repository.

---

## 🔑 Verification ID

Every successful verification generates a unique ID in the following format:

```text
VERITAS-2026-XXXXXXXX
```

Example:

```text
VERITAS-2026-A1B2C3D4
```

Users can enter this ID in the **Verify ID** section to retrieve the corresponding verification result from their history.

---

## 🤖 AI Assistant

The Veritas AI Assistant can:

* Explain cybersecurity concepts.
* Provide phishing and scam awareness guidance.
* Analyze URLs using Veritas security results.
* Explain previous verification scans.
* Provide practical security recommendations.

The assistant can use **Ollama** locally when available and can fall back to **Google Gemini**.

---

## 📊 Verification Results

Veritas AI provides a Trust Score and security status for supported verification types.

Typical statuses include:

```text
🟢 SAFE
🟡 SUSPICIOUS
🔴 DANGEROUS
```

The platform also provides reasons and recommendations to help users understand the result.

---

## 📄 PDF Reports

After verification, users can generate a PDF report containing relevant verification information such as:

* Verification type
* Target
* Trust score
* Security status
* Security analysis
* Recommendations

---

## 🎯 Project Objective

The objective of Veritas AI is to provide an easy-to-use platform that helps users make safer decisions when interacting with potentially suspicious digital content.

Instead of requiring users to use multiple separate tools, Veritas AI brings several verification capabilities together into one interface.

---

## 🔮 Future Improvements

Potential future improvements include:

* 🔍 Advanced URL reputation analysis
* 🧠 Improved AI threat detection
* 🦠 Malware and file threat analysis
* 🌍 Domain reputation intelligence
* 📱 Mobile application
* ☁️ Cloud database integration
* 🔔 Real-time security alerts
* 👨‍💻 Security API integration
* 📈 Advanced threat intelligence dashboards

---

## ⚠️ Disclaimer

Veritas AI is designed as a cybersecurity assistance and educational platform.

A **SAFE** result does not guarantee that a website, document, QR code, or image is completely free from threats. Users should always exercise caution when interacting with unknown or suspicious content.

---

## 👨‍💻 Project

**Veritas AI**

AI-Powered Digital Trust & Verification Platform

Built using Python, Streamlit, SQLite, OpenCV, and AI technologies.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

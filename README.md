# 🛡️ Veritas AI

**AI-Powered Digital Trust & Verification Platform**

Veritas AI is a cybersecurity and digital verification platform that helps users analyze potentially suspicious digital content.

## 🚀 Features

* 🌐 URL Verification
* 📱 QR Code Verification
* 📄 Document Analysis
* 🖼️ Image Verification
* 🔐 Verification ID System
* 📊 Security Analytics
* 🕒 Verification History
* 🤖 AI Security Assistant
* 📄 PDF Verification Reports
* 👤 User Login & Registration

## 🛠️ Technologies

* Python
* Streamlit
* SQLite
* OpenCV
* Pillow
* PyPDF2
* Plotly
* Google Gemini API
* Ollama

## 📁 Project Structure

```text
veritas/
├── app.py
├── auth.py
├── database.py
├── url_checker.py
├── qr_checker.py
├── document_checker.py
├── image_checker.py
├── risk_analyzer.py
├── ai_summary.py
├── ai_recommendation.py
├── chatbot.py
├── report_generator.py
├── requirements.txt
├── .gitignore
├── README.md
└── veritas_logo.png
```

## ▶️ Run Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

## 🔐 Security

User databases and secret configuration files should not be uploaded to GitHub.

The following files are excluded using `.gitignore`:

```text
*.db
.env
.streamlit/secrets.toml
.venv/
__pycache__/
```

## 📌 Project

Veritas AI is designed to provide users with a simple interface for digital verification, cybersecurity analysis, and AI-assisted security guidance.

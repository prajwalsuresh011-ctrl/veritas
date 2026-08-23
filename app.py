import streamlit as st
from pathlib import Path

from streamlit_option_menu import option_menu

from url_checker import analyze_url
from image_checker import analyze_image
from document_checker import analyze_document
from qr_checker import read_qr

from database import (
    save_scan,
    get_history,
    clear_history,
    get_statistics,
    get_scan_by_verification_id
)

from report_generator import generate_report
from ai_summary import ai_summary
from risk_analyzer import analyze_risk
from ai_recommendation import generate_recommendation

from auth import register_user, login_user
from chatbot import ask_veritas

import plotly.graph_objects as go


# ====================================================
# FILE PATHS
# ====================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "veritas_logo.png"
# Page Config
# =========================
st.set_page_config(
    page_title="Veritas",
    page_icon="🛡️",
    layout="wide"
)

# ====================================================
# # ====================================================
# VERITAS AI - GLOBAL UI STYLE
# ====================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN BACKGROUND
    ================================= */

    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }


    /* ================================
       MAIN CONTENT
    ================================= */

    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }


    /* ================================
       HEADINGS
    ================================= */

    h1 {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    h2 {
        font-size: 1.7rem !important;
        color: #f8fafc !important;
    }

    h3 {
        font-size: 1.3rem !important;
        color: #e2e8f0 !important;
    }


    /* ================================
       METRIC CARDS
    ================================= */

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #172554,
            #111827
        );

        border: 1px solid #334155;

        border-radius: 14px;

        padding: 18px;

        box-shadow:
            0 4px 20px rgba(0,0,0,0.30);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }


    /* ================================
       INPUT BOXES
    ================================= */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #172033 !important;

        color: #ffffff !important;

        border: 1px solid #475569 !important;

        border-radius: 10px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;

        box-shadow:
            0 0 8px rgba(56,189,248,0.20) !important;
    }


    /* ================================
       FILE UPLOADER
    ================================= */

    [data-testid="stFileUploader"] {
        background-color: #151f32;

        border: 1px dashed #64748b;

        border-radius: 12px;

        padding: 12px;
    }


    /* ================================
       BUTTONS
    ================================= */

    .stButton > button {
        background-color: #172033;

        color: #f8fafc;

        border-radius: 10px;

        font-weight: 600;

        border: 1px solid #475569;

        padding: 0.6rem 1rem;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #1e3a5f;

        transform: translateY(-1px);

        border-color: #38bdf8;

        box-shadow:
            0 0 12px rgba(56,189,248,0.25);
    }


    /* ================================
       PRIMARY BUTTON
    ================================= */

    .stButton > button[kind="primary"] {
        background-color: #0ea5e9;

        color: white;

        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #0284c7;
    }


    /* ================================
       SIDEBAR
    ================================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #080d19,
            #0f172a
        );

        border-right: 1px solid #1e293b;
    }


    /* ================================
       ALERT BOXES
    ================================= */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ================================
       DIVIDER
    ================================= */

    hr {
        border-color: #334155 !important;
    }


    /* ================================
       CODE BLOCK
    ================================= */

    code {
        background-color: #172033 !important;
        color: #bae6fd !important;
    }


    /* ================================
       SECURITY STATUS COLORS
    ================================= */

    .safe-text {
        color: #22c55e !important;
        font-weight: 700;
    }

    .suspicious-text {
        color: #facc15 !important;
        font-weight: 700;
    }

    .dangerous-text {
        color: #ef4444 !important;
        font-weight: 700;
    }

    .info-text {
        color: #38bdf8 !important;
        font-weight: 700;
    }


    /* ================================
       SECURITY CARDS
    ================================= */

    .security-card {
        background: linear-gradient(
            145deg,
            #172033,
            #111827
        );

        border: 1px solid #334155;

        border-radius: 14px;

        padding: 18px;

        margin-bottom: 15px;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.25);

        transition: all 0.2s ease;
    }

    .security-card:hover {
        border-color: #38bdf8;

        transform: translateY(-2px);

        box-shadow:
            0 0 18px rgba(56,189,248,0.15);
    }


    /* ================================
       SCROLLBAR
    ================================= */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080d19;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True
)
    



# =========================
# Session State
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "home_navigation" not in st.session_state:
    st.session_state.home_navigation = None
# =========================
#
# ====================================================
# OPTION MENU
# ====================================================
# ====================================================
# LOGIN / # ====================================================
# LOGIN / REGISTER
# ====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


if not st.session_state.logged_in:

    # ====================================================
    # LOGIN LOGO
    # ====================================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.image(
            str(LOGO_PATH),
            width=150
        )

        st.title("🛡️ Veritas Login")

        choice = st.selectbox(
            "Select Option",
            [
                "Login",
                "Register"
            ]
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        # ====================================================
        # REGISTER
        # ====================================================

        if choice == "Register":

            if st.button("Create Account"):

                result = register_user(
                    username,
                    password
                )

                if result:

                    st.success(
                        "Account created successfully. Please login."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )

        # ====================================================
        # LOGIN
        # ====================================================

        else:

            if st.button("Login"):

                user = login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success(
                        "Login Successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password"
                    )

    # Stop ONLY when user is not logged in
    st.stop()



# ====================================================
# SIDEBAR
# ====================================================
# NAVIGATION OPTIONS
# ====================================================

navigation_options = [
    "Home",
    "URL",
    "QR Code",
    "Document",
    "Image",
    "History",
    "Analytics",
    "AI Assistant",
    "Settings"
]


# ====================================================
# SELECTED PAGE
# ====================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

if st.session_state.selected_page not in navigation_options:
    st.session_state.selected_page = "Home"


# ====================================================
# SIDEBAR
# ====================================================

with st.sidebar:

    st.image(
        str(LOGO_PATH),
        width=80
    )

    st.title("Veritas")

    selected = option_menu(
        menu_title="Navigation",

        options=navigation_options,

        icons=[
            "house-fill",
            "globe2",
            "qr-code",
            "file-earmark-text",
            "image",
            "clock-history",
            "bar-chart-fill",
            "robot",
            "gear-fill"
        ],

        menu_icon="shield-lock",

        default_index=navigation_options.index(
            st.session_state.selected_page
        ),

        orientation="vertical",

        styles={
            "container": {
                "padding": "5px"
            },

            "icon": {
                "color": "#00C853",
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px",
                "padding": "10px",
                "border-radius": "8px"
            },

            "nav-link-selected": {
                "background-color": "#00C853",
                "color": "white"
            }
        }
    )

    # Save selected page
    st.session_state.selected_page = selected

    st.divider()

    # ====================================================
    # USER INFORMATION
    # ====================================================

    st.write(
        f"👤 Logged in as: **{st.session_state.username}**"
    )

    # ====================================================
    # LOGOUT
    # ====================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.selected_page = "Home"

        st.rerun()
# ====================================================
# CLEAR TEMPORARY HOME NAVIGATION
# ====================================================





# # ====================================================

# HOME DASHBOARD

## ====================================================
# HOME DASHBOARD
# ====================================================

if selected == "Home":

    st.title("🛡️ Veritas AI")

    st.write(
        f"Welcome back, **{st.session_state.username}** 👋"
    )

    st.caption(
        "AI-Powered Digital Verification & Cybersecurity Platform"
    )

    st.divider()

    # ====================================================
    # QUICK VERIFICATION
    # ====================================================

    st.subheader("🚀 Quick Verification")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "🌐 URL",
            use_container_width=True,
            key="home_url_button"
        ):

            st.session_state.selected_page = "URL"
            st.rerun()

    with col2:

        if st.button(
            "📱 QR Code",
            use_container_width=True,
            key="home_qr_button"
        ):

            st.session_state.selected_page = "QR Code"
            st.rerun()

    with col3:

        if st.button(
            "📄 Document",
            use_container_width=True,
            key="home_document_button"
        ):

            st.session_state.selected_page = "Document"
            st.rerun()

    with col4:

        if st.button(
            "🖼️ Image",
            use_container_width=True,
            key="home_image_button"
        ):

            st.session_state.selected_page = "Image"
            st.rerun()

    st.divider()

    # ====================================================
    # SECURITY OVERVIEW
    # ====================================================

    st.subheader("📊 Security Overview")

    stats = get_statistics(
        st.session_state.username
    )

    total = stats["total"]
    safe = stats["safe"]
    suspicious = stats["suspicious"]
    dangerous = stats["dangerous"]

    # ====================================================
    # STATISTICS CARDS
    # ====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📊 Total Scans",
            total
        )

    with col2:

        st.metric(
            "🟢 Safe",
            safe
        )

    with col3:

        st.metric(
            "🟡 Suspicious",
            suspicious
        )

    with col4:

        st.metric(
            "🔴 Dangerous",
            dangerous
        )

    st.divider()

    # ====================================================
    # SECURITY STATUS
    # ====================================================

    st.subheader("🛡️ Security Status")

    if total > 0:

        safe_percentage = (
            safe / total
        ) * 100

        suspicious_percentage = (
            suspicious / total
        ) * 100

        dangerous_percentage = (
            dangerous / total
        ) * 100

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"🟢 Safe: **{safe_percentage:.1f}%**"
            )

            st.progress(
                safe_percentage / 100
            )

            st.write(
                f"🟡 Suspicious: "
                f"**{suspicious_percentage:.1f}%**"
            )

            st.progress(
                suspicious_percentage / 100
            )

            st.write(
                f"🔴 Dangerous: "
                f"**{dangerous_percentage:.1f}%**"
            )

            st.progress(
                dangerous_percentage / 100
            )

        with col2:

            if dangerous > 0:

                st.error(
                    "⚠️ Dangerous content was detected "
                    "in your previous scans."
                )

            elif suspicious > 0:

                st.warning(
                    "⚠️ Some scans require additional "
                    "verification."
                )

            else:

                st.success(
                    "✅ No dangerous scans detected "
                    "in your current history."
                )

    else:

        st.info(
            "No scans available yet. "
            "Start your first verification."
        )

    st.divider()

    # ====================================================
    # RECENT VERIFICATION ACTIVITY
    # ====================================================

    st.subheader(
        "🕒 Recent Verification Activity"
    )

    history = get_history(
        st.session_state.username
    )

    if not history:

        st.info(
            "No verification scans yet. "
            "Start your first verification!"
        )

    else:

        for scan in history[:5]:

            scan_type = scan[2]
            target = scan[3]
            score = scan[4]
            status = scan[5]
            scan_date = scan[6]

            if status in [
                "SAFE",
                "Verified",
                "Likely Genuine"
            ]:

                icon = "🟢"

            elif status in [
                "SUSPICIOUS",
                "Needs Review"
            ]:

                icon = "🟡"

            else:

                icon = "🔴"

            col1, col2, col3 = st.columns(
                [2, 5, 2]
            )

            with col1:

                st.write(
                    f"{icon} **{scan_type}**"
                )

            with col2:

                st.write(
                    str(target)[:70]
                )

            with col3:

                st.write(
                    f"**{score}/100**"
                )

            st.caption(
                f"Status: {status} • {scan_date}"
            )

            st.divider()

        # ====================================================
        # LATEST VERIFICATION ID
        # ====================================================

        latest = history[0]

        if len(latest) > 7:

            latest_verification_id = latest[7]

            st.subheader(
                "🔐 Latest Verification"
            )

            st.info(
                f"Verification ID: "
                f"**{latest_verification_id}**"
            )

            st.caption(
                "Use this ID in the Verify ID section "
                "to retrieve this verification."
            )

    st.divider()

    # ====================================================
    # ABOUT VERITAS AI
    # ====================================================

    st.info(
        """
🚀 **Veritas AI**

Veritas AI protects users by analyzing:

✔ Website URLs  
✔ QR Codes  
✔ Documents  
✔ Images  

Using AI-based threat analysis and verification.

🤖 The integrated AI Assistant can also explain
security results and help users understand potential threats.
"""
    )



# ====================================================
# I# ====================================================
# IMAGE VERIFICATION
# ====================================================

elif selected == "Image":

    st.title("🖼️ Image Verification")

    st.write(
        "Upload an image to check its resolution, size, "
        "brightness and other suspicious indicators."
    )

    st.divider()

    # ====================================================
    # IMAGE UPLOAD
    # ====================================================

    uploaded_image = st.file_uploader(
        "📤 Upload Image",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )

    if st.button(
        "🔍 Analyze Image",
        key="analyze_image_button",
        use_container_width=True
    ):

        if uploaded_image is None:

            st.warning(
                "Please upload an image."
            )

        else:

            with st.spinner(
                "🖼️ Analyzing image..."
            ):

                try:

                    # ====================================================
                    # IMAGE ANALYSIS
                    # ====================================================

                    score, status, reasons, width, height = analyze_image(
                        uploaded_image
                    )

                    # ====================================================
                    # SAVE HISTORY
                    # ====================================================

                    verification_id = save_scan(
                    st.session_state.username,
                    "Image",
                    uploaded_image.name,
                    score,
                     status
                    )

                    st.success(
                        "✅ Image analysis completed."
                    )

                    st.divider()

                    # ====================================================
                    # IMAGE PREVIEW + INFORMATION
                    # ====================================================

                    col1, col2 = st.columns(2)

                    with col1:

                        st.image(
                            uploaded_image,
                            caption="Uploaded Image",
                            width=400
                        )

                    with col2:

                        st.subheader(
                            "📐 Image Information"
                        )

                        st.write(
                            f"**Width:** {width} pixels"
                        )

                        st.write(
                            f"**Height:** {height} pixels"
                        )

                        st.write(
                            f"**File Size:** "
                            f"{uploaded_image.size / 1024:.1f} KB"
                        )

                    st.divider()

                    # ====================================================
                    # TRUST SCORE
                    # ====================================================

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "🛡️ Trust Score",
                            f"{score}/100"
                        )

                    with col2:

                        if score >= 80:


                            st.success(
                                "🟢 LIKELY GENUINE"
                            )

                        elif score >= 50:


                            st.warning(
                                "🟡 NEEDS REVIEW"
                            )

                        else:

                            st.error(
                                "🔴 SUSPICIOUS"
                            )

                    st.divider()

                    # ====================================================
                    # SECURITY ANALYSIS
                    # ====================================================

                    st.subheader(
                        "🔍 Image Analysis"
                    )

                    if len(reasons) == 0:

                        st.success(
                            "No suspicious indicators were detected."
                        )

                    else:

                        for reason in reasons:

                            st.write(
                                "✔️",
                                reason
                            )

                    # ====================================================
                    # AI VERDICT
                    # ====================================================

                    st.subheader(
                        "🧠 AI Verdict"
                    )

                    try:

                        recommendation = generate_recommendation(
                            status,
                            reasons
                        )

                        st.info(
                            recommendation
                        )

                    except Exception as e:

                        st.info(
                            "Review the image carefully before trusting it."
                        )

                    # ====================================================
                    # PDF REPORT
                    # ====================================================

                    st.subheader(
                        "📄 Verification Report"
                    )

                    try:

                        report = generate_report(
                            "Image",
                            uploaded_image.name,
                            score,
                            status,
                            reasons,
                            verification_id
                        )

                        with open(report, "rb") as pdf:

                            st.download_button(
                                "📥 Download PDF Report",
                                pdf,
                                file_name="Veritas_Image_Report.pdf",
                                mime="application/pdf",
                                key="image_report_download"
                            )

                    except Exception as e:

                        st.warning(
                            f"Report generation unavailable: {e}"
                        )

                except Exception as e:

                    st.error(
                        f"Image analysis error: {e}"
                    )
                    # ====================================================
# ====================================================
# URL
# ====================================================
# ====================================================
# URL VERIFICATION
# ====================================================

# ====================================================
# URL VERIFICATION
# ====================================================

elif selected == "URL":

    st.title("🌐 URL Verification")

    st.write(
        "Analyze a website URL and determine its potential security risk."
    )

    st.divider()

    url = st.text_input(
        "🔗 Enter Website URL",
        placeholder="https://example.com"
    )

    if st.button(
        "🔍 Analyze URL",
        key="analyze_url_button",
        use_container_width=True
    ):

        if url.strip() == "":

            st.warning(
                "Please enter a website URL."
            )

        else:

            with st.spinner(
                "🔎 Analyzing URL..."
            ):

                try:

                    score, status, reasons = analyze_url(
                        url
                    )

                    risk_data = {
                        "url": {
                            "safe": status == "SAFE",
                            "score": score
                        }
                    }

                    risk = analyze_risk(
                        risk_data
                    )

                    # ====================================================
                    # SAVE VERIFICATION
                    # ====================================================

                    verification_id = save_scan(
                        st.session_state.username,
                        "URL",
                        url,
                        score,
                        status
                    )

                    st.success(
                        "URL analysis completed."
                    )

                    st.info(
                        f"🔐 Verification ID: **{verification_id}**"
                    )

                    st.divider()
                    # RISK ASSESSMENT
                    st.subheader(
                        "🛡️ Risk Assessment"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "⚠️ Risk Score",
                            f"{risk['risk_score']}/100"
                        )

                    with col2:

                        st.metric(
                            "🎯 Confidence",
                            f"{risk['confidence']}%"
                        )

                    if risk["status"] == "SAFE":

                        st.success(
                            "🟢 Risk Level: SAFE"
                        )

                    elif risk["status"] == "SUSPICIOUS":

                        st.warning(
                            "🟡 Risk Level: SUSPICIOUS"
                        )

                    else:

                        st.error(
                            "🔴 Risk Level: DANGEROUS"
                        )

                    for reason in risk["reasons"]:

                        st.write(
                            "⚠️",
                            reason
                        )

                    st.divider()

                    # SECURITY ANALYSIS
                    st.subheader(
                        "🔍 Security Analysis"
                    )

                    if len(reasons) == 0:

                        st.success(
                            "No suspicious indicators were detected."
                        )

                    else:

                        for reason in reasons:

                            st.write(
                                "✔️",
                                reason
                            )

                    # AI VERDICT
                    st.subheader(
                        "🧠 AI Verdict"
                    )

                    try:

                        recommendation = generate_recommendation(
                            status,
                            reasons
                        )

                        st.info(
                            recommendation
                        )

                    except Exception:

                        st.info(
                            "Review the security indicators before visiting this website."
                        )

                    # PDF REPORT
                    st.subheader(
                        "📄 Verification Report"
                    )

                    try:

                        report = generate_report(
                            "URL",
                            url,
                            score,
                            status,
                            reasons,
                            verification_id
                        )

                        with open(report, "rb") as pdf:

                            st.download_button(
                                "📥 Download PDF Report",
                                pdf,
                                file_name="Veritas_URL_Report.pdf",
                                mime="application/pdf",
                                key="url_report_download"
                            )

                    except Exception as e:

                        st.warning(
                            f"Report generation unavailable: {e}"
                        )

                except Exception as e:

                    st.error(
                        f"URL analysis error: {e}"
                    )


# ====================================================
# QR CODE VERIFICATION
# ====================================================

elif selected == "QR Code":

    st.title(
        "📱 QR Code Verification"
    )

    st.write(
        "Upload a QR code image to decode and analyze its destination."
    )

    st.divider()

    # ====================================================
    # UPLOAD QR
    # ====================================================

    qr = st.file_uploader(
        "📤 Upload QR Code Image",
        type=["jpg", "jpeg", "png"],
        key="qr_upload"
    )

    # ====================================================
    # ANALYZE QR
    # ====================================================

    if st.button(
        "🔍 Analyze QR Code",
        key="analyze_qr_button",
        use_container_width=True
    ):

        if qr is None:

            st.warning(
                "Please upload a QR code image."
            )

        else:

            with st.spinner(
                "📱 Reading QR Code..."
            ):

                try:

                    url = read_qr(qr)

                    if url is None:

                        st.error(
                            "❌ QR Code could not be detected."
                        )

                    else:

                        st.success(
                            "✅ QR Code successfully decoded."
                        )

                        # ====================================================
                        # SHOW QR IMAGE
                        # ====================================================

                        col1, col2 = st.columns(2)

                        with col1:

                            st.image(
                                qr,
                                caption="Uploaded QR Code",
                                width=300
                            )

                        with col2:

                            st.subheader(
                                "🔗 Decoded URL"
                            )

                            st.code(
                                url
                            )

                        st.divider()

                        # ====================================================
                        # ANALYZE URL
                        # ====================================================

                        with st.spinner(
                            "🔎 Analyzing destination..."
                        ):

                            score, status, reasons = analyze_url(
                                url
                            )

                        
                        verification_id = save_scan(
    st.session_state.username,
    "QR Code",
    url,
    score,
    status
)

                        st.info(
    f"🆔 Verification ID: `{verification_id}`"
)
                         # ====================================================
                        # TRUST SCORE
                        # ====================================================

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "🛡️ Trust Score",
                                f"{score}/100"
                            )

                        with col2:

                            if status == "SAFE":

                                st.success(
                                    "🟢 SAFE QR CODE"
                                )

                            elif status == "SUSPICIOUS":

                                st.warning(
                                    "🟡 SUSPICIOUS QR CODE"
                                )

                            else:

                                st.error(
                                    "🔴 DANGEROUS QR CODE"
                                )

                        st.divider()

                        # ====================================================
                        # SECURITY ANALYSIS
                        # ====================================================

                        st.subheader(
                            "🔍 Security Analysis"
                        )

                        if len(reasons) == 0:

                            st.success(
                                "No suspicious indicators were detected."
                            )

                        else:

                            for reason in reasons:

                                st.write(
                                    "✔️",
                                    reason
                                )

                        # ====================================================
                        # AI VERDICT
                        # ====================================================

                        st.subheader(
                            "🧠 AI Verdict"
                        )

                        try:

                            recommendation = generate_recommendation(
                                status,
                                reasons
                            )

                            st.info(
                                recommendation
                            )

                        except Exception:

                            st.info(
                                "Review the QR destination carefully before opening it."
                            )

                        # ====================================================
                        # PDF REPORT
                        # ====================================================

                        st.subheader(
                            "📄 Verification Report"
                        )

                        try:

                            report = generate_report(
                                "QR Code",
                                url,
                                score,
                                status,
                                reasons,
                                verification_id
                            )

                            with open(report, "rb") as pdf:

                                st.download_button(
                                    "📥 Download PDF Report",
                                    pdf,
                                    file_name="Veritas_QR_Report.pdf",
                                    mime="application/pdf",
                                    key="qr_report_download"
                                )

                        except Exception as e:

                            st.warning(
                                f"Report generation unavailable: {e}"
                            )

                except Exception as e:

                    st.error(
                        f"QR analysis error: {e}"
                    )
# ====================================================
# DOCUMENT
# ====================================================

# ====================================================
# DOCUMENT
# ====================================================

# ====================================================
# DOCUMENT VERIFICATION
# ====================================================

elif selected == "Document":

    st.title("📄 Document Verification")

    st.write(
        "Upload a PDF document to check for suspicious indicators."
    )

    st.divider()

    # ====================================================
    # PDF UPLOAD
    # ====================================================

    uploaded = st.file_uploader(
        "📤 Upload PDF Document",
        type=["pdf"],
        key="document_upload"
    )

    if st.button(
        "🔍 Analyze Document",
        key="analyze_document_button",
        use_container_width=True
    ):

        if uploaded is None:

            st.warning(
                "Please upload a PDF document."
            )

        else:

            with st.spinner(
                "📄 Analyzing document..."
            ):

                try:

                    score, status, reasons, pages = analyze_document(
                        uploaded
                    )

                    # ====================================================
                    # SAVE HISTORY
                    # ====================================================

                    report = generate_report(
                      "Document",
                      uploaded_document.name,
                       score,
                         status,
                        reasons,
                            verification_id
                       )
                    st.success(
                        "✅ Document analysis completed."
                    )

                    st.divider()

                    # ====================================================
                    # DOCUMENT INFORMATION
                    # ====================================================

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "🛡️ Trust Score",
                            f"{score}/100"
                        )

                    with col2:

                        st.metric(
                            "📄 Pages",
                            pages
                        )

                    # ====================================================
                    # STATUS
                    # ====================================================

                    if status == "Verified":

                        st.success(
                            "🟢 DOCUMENT VERIFIED"
                        )

                    elif status == "Needs Review":

                        st.warning(
                            "🟡 DOCUMENT NEEDS REVIEW"
                        )

                    else:

                        st.error(
                            "🔴 SUSPICIOUS DOCUMENT"
                        )

                    st.divider()

                    # ====================================================
                    # ANALYSIS
                    # ====================================================

                    st.subheader(
                        "🔍 Document Analysis"
                    )

                    if len(reasons) == 0:

                        st.success(
                            "No suspicious indicators were detected."
                        )

                    else:

                        for reason in reasons:

                            st.write(
                                "✔️",
                                reason
                            )

                    # ====================================================
                    # AI VERDICT
                    # ====================================================

                    st.subheader(
                        "🧠 AI Verdict"
                    )

                    try:

                        recommendation = generate_recommendation(
                            status,
                            reasons
                        )

                        st.info(
                            recommendation
                        )

                    except Exception:

                        st.info(
                            "Review the document carefully before trusting its contents."
                        )

                    # ====================================================
                    # PDF REPORT
                    # ====================================================

                    st.subheader(
                        "📄 Verification Report"
                    )

                    try:

                        report = generate_report(
                            "Document",
                            uploaded.name,
                            score,
                            status,
                            reasons
                        )

                        with open(report, "rb") as pdf:

                            st.download_button(
                                "📥 Download PDF Report",
                                pdf,
                                file_name="Veritas_Document_Report.pdf",
                                mime="application/pdf",
                                key="document_report_download"
                            )

                    except Exception as e:

                        st.warning(
                            f"Report generation unavailable: {e}"
                        )

                except Exception as e:

                    st.error(
                        f"Document analysis error: {e}"
                    )
# ====================================================
# HISTORY
# ====================================================

# ====================================================
# HISTORY
# ====================================================
# ====================================================
# HISTORY
# ==========# ====================================================
# HISTORY
# ====================================================

# # ====================================================
# HISTORY
# ====================================================

elif selected == "History":

    st.title("📜 Scan History")

    st.write(
        f"Verification records for "
        f"**{st.session_state.username}**"
    )

    st.divider()

    # ====================================================
    # GET HISTORY
    # ====================================================

    history = get_history(
        st.session_state.username
    )

    if len(history) == 0:

        st.info(
            "📭 No scan history available yet."
        )

    else:

        # ====================================================
        # FILTERS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            search = st.text_input(
                "🔎 Search",
                placeholder="Search target or scan type...",
                key="history_search"
            )

        with col2:

            filter_status = st.selectbox(
                "📌 Filter by Status",
                [
                    "All",
                    "SAFE",
                    "SUSPICIOUS",
                    "DANGEROUS",
                    "Verified",
                    "Needs Review",
                    "Likely Genuine"
                ],
                key="history_status"
            )

        st.divider()

        # ====================================================
        # FILTER HISTORY
        # ====================================================

        filtered_history = []

        for item in history:

            scan_type = str(item[2])
            target = str(item[3])
            status = str(item[5])

            matches_search = (
                search.strip() == ""
                or search.lower() in scan_type.lower()
                or search.lower() in target.lower()
            )

            matches_status = (
                filter_status == "All"
                or status == filter_status
            )

            if matches_search and matches_status:

                filtered_history.append(item)

        # ====================================================
        # RESULT COUNT
        # ====================================================

        st.write(
            f"Showing **{len(filtered_history)}** "
            f"of **{len(history)}** scans"
        )

        # ====================================================
        # DISPLAY HISTORY
        # ====================================================

        if len(filtered_history) == 0:

            st.warning(
                "No matching scan records found."
            )

        else:

            for item in filtered_history:

                scan_id = item[0]
                scan_type = item[2]
                target = item[3]
                score = item[4]
                status = item[5]
                date = item[6]
                verification_id = item[7]

                # ====================================================
                # STATUS ICON
                # ====================================================

                if status in [
                    "SAFE",
                    "Verified",
                    "Likely Genuine"
                ]:

                    status_icon = "🟢"

                elif status in [
                    "SUSPICIOUS",
                    "Needs Review"
                ]:

                    status_icon = "🟡"

                else:

                    status_icon = "🔴"

                # ====================================================
                # HISTORY EXPANDER
                # ====================================================

                with st.expander(
                    f"{status_icon} #{scan_id} | "
                    f"{scan_type} | {status}"
                ):

                    col1, col2, col3 = st.columns(3)

                    # ====================================================
                    # SCAN TYPE
                    # ====================================================

                    with col1:

                        st.write(
                            "**🔍 Scan Type**"
                        )

                        st.write(
                            scan_type
                        )

                    # ====================================================
                    # TRUST SCORE
                    # ====================================================

                    with col2:

                        st.write(
                            "**🛡️ Trust Score**"
                        )

                        st.metric(
                            "Score",
                            f"{score}/100"
                        )

                    # ====================================================
                    # STATUS
                    # ====================================================

                    with col3:

                        st.write(
                            "**📌 Status**"
                        )

                        if status in [
                            "SAFE",
                            "Verified",
                            "Likely Genuine"
                        ]:

                            st.success(
                                f"🟢 {status}"
                            )

                        elif status in [
                            "SUSPICIOUS",
                            "Needs Review"
                        ]:

                            st.warning(
                                f"🟡 {status}"
                            )

                        else:

                            st.error(
                                f"🔴 {status}"
                            )

                    st.divider()

                    # ====================================================
                    # TARGET
                    # ====================================================

                    st.write(
                        "**🎯 Target:**"
                    )

                    st.code(
                        target
                    )

                    # ====================================================
                    # VERIFICATION ID
                    # ====================================================

                    st.write(
                        "**🆔 Verification ID:**"
                    )

                    st.code(
                        verification_id
                    )

                    # ====================================================
                    # DATE
                    # ====================================================

                    st.write(
                        f"**🕒 Date:** {date}"
                    )

                    st.divider()

                    # ====================================================
                    # GENERATE PDF REPORT
                    # ====================================================

                    if st.button(
                        "📄 Generate PDF Report",
                        key=f"history_report_{scan_id}",
                        use_container_width=True
                    ):

                        try:

                            report = generate_report(
                                scan_type,
                                target,
                                score,
                                status,
                                [],
                                verification_id
                            )

                            with open(
                                report,
                                "rb"
                            ) as pdf:

                                st.download_button(
                                    "📥 Download PDF Report",
                                    pdf,
                                    file_name=(
                                        f"Veritas_"
                                        f"{verification_id}.pdf"
                                    ),
                                    mime="application/pdf",
                                    key=(
                                        f"history_download_"
                                        f"{scan_id}"
                                    ),
                                    use_container_width=True
                                )

                        except Exception as e:

                            st.error(
                                f"Report generation failed: {e}"
                            )

        # ====================================================
        # CLEAR HISTORY
        # ====================================================

        st.divider()

        st.subheader(
            "🗑️ Data Management"
        )

        if st.button(
            "🗑️ Clear My Scan History",
            key="history_clear_button"
        ):

            clear_history(
                st.session_state.username
            )

            st.success(
                "Scan history cleared successfully."
            )

            st.rerun()
# VERIFICATION ID
# ====================================================

elif selected == "Verify ID":

    st.title("🛡️ Verify Verification ID")

    st.write(
        "Enter a Veritas Verification ID to retrieve "
        "the corresponding security verification result."
    )

    st.divider()

    verification_id = st.text_input(
        "🔎 Verification ID",
        placeholder="VERITAS-2026-XXXXXXXX"
    )

    if st.button(
        "🔍 Verify ID",
        use_container_width=True
    ):

        if verification_id.strip() == "":

            st.warning(
                "Please enter a Verification ID."
            )

        else:

            verification_id = (
                verification_id.strip().upper()
            )

            result = get_scan_by_verification_id(
                verification_id,
                st.session_state.username
            )

            if result:

                (
                    scan_id,
                    verification_id,
                    username,
                    scan_type,
                    target,
                    score,
                    status,
                    date
                ) = result

                st.success(
                    "✅ Verification ID found."
                )

                st.divider()

                # ====================================================
                # VERIFICATION INFORMATION
                # ====================================================

                st.subheader(
                    "📋 Verification Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "🆔 Verification ID",
                        verification_id
                    )

                    st.write(
                        f"**Verification Type:** {scan_type}"
                    )

                    st.write(
                        f"**Date:** {date}"
                    )

                with col2:

                    st.metric(
                        "🛡️ Trust Score",
                        f"{score}/100"
                    )

                    if status == "SAFE":

                        st.success(
                            "🟢 SAFE"
                        )

                    elif status == "SUSPICIOUS":

                        st.warning(
                            "🟡 SUSPICIOUS"
                        )

                    else:

                        st.error(
                            "🔴 DANGEROUS"
                        )

                st.divider()

                # ====================================================
                # TARGET
                # ====================================================

                st.subheader(
                    "🎯 Verified Target"
                )

                st.code(
                    target
                )

                st.divider()

                # ====================================================
                # RESULT
                # ====================================================

                st.subheader(
                    "🔐 Verification Result"
                )

                if status == "SAFE":

                    st.success(
                        "This verification record was classified as SAFE "
                        "by Veritas."
                    )

                elif status == "SUSPICIOUS":

                    st.warning(
                        "This verification record was classified as "
                        "SUSPICIOUS by Veritas."
                    )

                else:

                    st.error(
                        "This verification record was classified as "
                        "DANGEROUS by Veritas."
                    )

                st.info(
                    "⚠️ A Veritas verification result is based on "
                    "the security checks available at the time of scanning. "
                    "It does not guarantee that a target is completely safe."
                )

            else:

                st.error(
                    "❌ Verification ID not found."
                )

                st.write(
                    "Please check the ID and try again."
                )
elif selected == "Analytics":

    st.title("📊 Security Analytics")

    st.subheader(
        f"Verification analytics for "
        f"{st.session_state.username}"
    )

    st.divider()

    # ====================================================
    # GET STATISTICS
    # ====================================================

    stats = get_statistics(
        st.session_state.username
    )

    total = stats["total"]
    safe = stats["safe"]
    suspicious = stats["suspicious"]
    dangerous = stats["dangerous"]

    # ====================================================
    # DASHBOARD CARDS
    # ====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📊 Total Scans",
            total
        )

    with col2:

        st.metric(
            "🟢 Safe",
            safe
        )

    with col3:

        st.metric(
            "🟡 Suspicious",
            suspicious
        )

    with col4:

        st.metric(
            "🔴 Dangerous",
            dangerous
        )

    st.divider()

    # ====================================================
    # PIE CHART
    # ====================================================

    st.subheader(
        "🔍 Verification Distribution"
    )

    if total > 0:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Safe",
                        "Suspicious",
                        "Dangerous"
                    ],
                    values=[
                        safe,
                        suspicious,
                        dangerous
                    ],
                    hole=0.45
                )
            ]
        )

        fig.update_layout(
            title="Scan Result Distribution",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No verification data available yet."
        )

    st.divider()

    # ====================================================
    # SCAN ACTIVITY
    # ====================================================

    st.subheader(
        "📈 Scan Activity"
    )

    if total > 0:

        activity_fig = go.Figure()

        activity_fig.add_trace(
            go.Bar(
                x=[
                    "Safe",
                    "Suspicious",
                    "Dangerous"
                ],
                y=[
                    safe,
                    suspicious,
                    dangerous
                ],
                text=[
                    safe,
                    suspicious,
                    dangerous
                ],
                textposition="auto"
            )
        )

        activity_fig.update_layout(
            title="Verification Results",
            xaxis_title="Risk Level",
            yaxis_title="Number of Scans",
            height=400,
            showlegend=False
        )

        st.plotly_chart(
            activity_fig,
            use_container_width=True
        )

    else:

        st.info(
            "Complete some scans to generate "
            "scan activity."
        )

    st.divider()

    # ====================================================
    # SECURITY SUMMARY
    # ====================================================

    st.subheader(
        "🛡️ Security Summary"
    )

    if total > 0:

        safe_percentage = (
            safe / total
        ) * 100

        suspicious_percentage = (
            suspicious / total
        ) * 100

        dangerous_percentage = (
            dangerous / total
        ) * 100

        st.write(
            f"🟢 Safe: **{safe_percentage:.1f}%**"
        )

        st.progress(
            safe_percentage / 100
        )

        st.write(
            f"🟡 Suspicious: **{suspicious_percentage:.1f}%**"
        )

        st.progress(
            suspicious_percentage / 100
        )

        st.write(
            f"🔴 Dangerous: **{dangerous_percentage:.1f}%**"
        )

        st.progress(
            dangerous_percentage / 100
        )

    else:

        st.info(
            "Complete some scans to generate "
            "security analytics."
        )
        

# ====================================================
# AI ASSISTANT
# ====================================================

elif selected == "AI Assistant":

    st.title(
        "🤖 Veritas Assistant"
    )

    st.write(
        "Ask Veritas anything about cybersecurity."
    )

    question = st.text_area(
        "Ask a cybersecurity question",
        placeholder=(
            "Example: How can I identify "
            "a phishing website?"
        ),
        key="ai_question"
    )

    if st.button(
        "🚀 Ask Veritas",
        key="ask_veritas_button",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "🤖 Veritas is thinking..."
            ):

                try:

                    answer = ask_veritas(
                        question,
                        st.session_state.username
                    )

                    st.subheader(
                        "🧠 Veritas"
                    )

                    st.info(
                        answer
                    )

                except Exception as e:

                    st.error(
                        f"AI Assistant Error: {e}"
                    )


# ====================================================
# SETTINGS
# ====================================================

elif selected == "Settings":

    st.title(
        "⚙️ Settings"
    )

    st.write(
        "Manage your Veritas account "
        "and application preferences."
    )

    st.divider()

    # ====================================================
    # ACCOUNT INFORMATION
    # ====================================================

    st.subheader(
        "👤 Account Information"
    )

    st.write(
        f"**Username:** "
        f"{st.session_state.username}"
    )

    st.divider()

    # ====================================================
    # APPLICATION INFORMATION
    # ====================================================

    st.subheader(
        "🛡️ Veritas"
    )

    st.write(
        "**Version:** 1.0"
    )

    st.write(
        "**Platform:** "
        "AI-Powered Digital Verification System"
    )

    st.write(
        "**Verification Modules:** "
        "URL, QR Code, Document, Image"
    )

    st.divider()

    # ====================================================
    # DATA MANAGEMENT
    # ====================================================

    st.subheader(
        "🗑️ Data Management"
    )

    st.write(
        "Clear all verification history "
        "associated with your account."
    )

    if st.button(
        "🗑️ Clear My Scan History",
        key="settings_clear_history",
        use_container_width=True
    ):

        clear_history(
            st.session_state.username
        )

        st.success(
            "Your scan history has been "
            "cleared successfully."
        )

        st.rerun()

    st.divider()

    # ====================================================
    # SECURITY
    # ====================================================

    st.subheader(
        "🔐 Security"
    )

    st.success(
        "Your verification history is "
        "associated with your account."
    )

    st.info(
        "Always verify suspicious URLs, QR codes, "
        "documents and images before trusting them."
    )

    st.divider()

    # ====================================================
    # LOGOUT
    # ====================================================

    st.subheader(
        "🚪 Account"
    )

    if st.button(
        "🚪 Logout",
        key="settings_logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

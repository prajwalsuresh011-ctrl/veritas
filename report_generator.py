from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

from datetime import datetime
import os
import html
import uuid


def generate_report(
    scan_type,
    target,
    score,
    status,
    reasons
):

    # ====================================================
    # REPORT DIRECTORY
    # ====================================================

    os.makedirs(
        "reports",
        exist_ok=True
    )

    # ====================================================
    # VERIFICATION ID
    # ====================================================

    verification_id = (
        "VERITAS-"
        f"{datetime.now().year}-"
        f"{uuid.uuid4().hex[:8].upper()}"
    )

    # ====================================================
    # DATE
    # ====================================================

    verification_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    # ====================================================
    # FILE NAME
    # ====================================================

    safe_type = str(scan_type).replace(
        " ",
        "_"
    )

    filename = (
        f"reports/"
        f"Veritas_{safe_type}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    # ====================================================
    # DOCUMENT
    # ====================================================

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    # ====================================================
    # STYLES
    # ====================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "VeritasTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        leading=28,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=13,
        leading=18,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=6
    )

    center_style = ParagraphStyle(
        "Center",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=14
    )

    verification_id_style = ParagraphStyle(
        "VerificationID",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=15,
        spaceAfter=15
    )

    # ====================================================
    # STORY
    # ====================================================

    elements = []

    # ====================================================
    # HEADER
    # ====================================================

    elements.append(
        Paragraph(
            "VERITAS AI",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "AI-Powered Digital Verification Report",
            subtitle_style
        )
    )

    # ====================================================
    # VERIFICATION ID
    # ====================================================

    elements.append(
        Paragraph(
            f"<b>Verification ID</b><br/>"
            f"{verification_id}",
            verification_id_style
        )
    )

    elements.append(
        Spacer(
            1,
            5
        )
    )

    # ====================================================
    # VERIFICATION INFORMATION
    # ====================================================

    elements.append(
        Paragraph(
            "Verification Information",
            heading_style
        )
    )

    safe_target = html.escape(
        str(target)
    )

    info_data = [
        [
            Paragraph(
                "<b>Verification ID</b>",
                body_style
            ),
            Paragraph(
                verification_id,
                body_style
            )
        ],
        [
            Paragraph(
                "<b>Verification Type</b>",
                body_style
            ),
            Paragraph(
                html.escape(str(scan_type)),
                body_style
            )
        ],
        [
            Paragraph(
                "<b>Target</b>",
                body_style
            ),
            Paragraph(
                safe_target,
                body_style
            )
        ],
        [
            Paragraph(
                "<b>Trust Score</b>",
                body_style
            ),
            Paragraph(
                f"<b>{score}/100</b>",
                body_style
            )
        ],
        [
            Paragraph(
                "<b>Status</b>",
                body_style
            ),
            Paragraph(
                html.escape(str(status)),
                body_style
            )
        ],
        [
            Paragraph(
                "<b>Date</b>",
                body_style
            ),
            Paragraph(
                verification_date,
                body_style
            )
        ]
    ]

    info_table = Table(
        info_data,
        colWidths=[
            45 * mm,
            120 * mm
        ]
    )

    info_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    elements.append(
        info_table
    )

    elements.append(
        Spacer(
            1,
            10
        )
    )

    # ====================================================
    # SECURITY ANALYSIS
    # ====================================================

    elements.append(
        Paragraph(
            "Security Analysis",
            heading_style
        )
    )

    if not reasons:

        reasons = [
            "No suspicious indicators were detected.",
            "The content passed the available verification checks."
        ]

    for reason in reasons:

        safe_reason = html.escape(
            str(reason)
        )

        elements.append(
            Paragraph(
                f"✔ {safe_reason}",
                body_style
            )
        )

    # ====================================================
    # FINAL VERDICT
    # ====================================================

    elements.append(
        Paragraph(
            "Verification Verdict",
            heading_style
        )
    )

    if score >= 80:

        verdict = (
            "The analyzed content appears to be "
            "relatively safe based on the available "
            "verification checks."
        )

    elif score >= 50:

        verdict = (
            "The analyzed content requires additional "
            "review before it should be fully trusted."
        )

    else:

        verdict = (
            "The analyzed content contains potentially "
            "dangerous or suspicious indicators. "
            "Users should exercise caution."
        )

    elements.append(
        Paragraph(
            verdict,
            body_style
        )
    )

    # ====================================================
    # FOOTER
    # ====================================================

    elements.append(
        Spacer(
            1,
            20
        )
    )

    elements.append(
        Paragraph(
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            center_style
        )
    )

    elements.append(
        Paragraph(
            "<b>Veritas AI</b>",
            center_style
        )
    )

    elements.append(
        Paragraph(
            "AI-Powered Digital Verification & Cybersecurity Platform",
            center_style
        )
    )

    elements.append(
        Paragraph(
            "Verify before you trust.",
            center_style
        )
    )

    # ====================================================
    # BUILD PDF
    # ====================================================

    doc.build(
        elements
    )

    return filename

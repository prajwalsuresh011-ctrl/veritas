from PIL import Image
import cv2
import numpy as np


def analyze_image(uploaded_file):

    # ====================================================
    # OPEN IMAGE
    # ====================================================

    image = Image.open(uploaded_file)

    width, height = image.size

    img_np = np.array(image)

    score = 100
    reasons = []

    # ====================================================
    # RESOLUTION CHECK
    # ====================================================

    if width < 500 or height < 500:

        score -= 15

        reasons.append(
            "Low image resolution."
        )

    # ====================================================
    # FILE SIZE CHECK
    # ====================================================

    if uploaded_file.size < 50000:

        score -= 10

        reasons.append(
            "Image file size is unusually small."
        )

    # ====================================================
    # BRIGHTNESS CHECK
    # ====================================================

    # Handle grayscale images safely
    if len(img_np.shape) == 2:

        gray = img_np

    else:

        gray = cv2.cvtColor(
            img_np,
            cv2.COLOR_RGB2GRAY
        )

    brightness = np.mean(gray)

    if brightness < 30:

        score -= 10

        reasons.append(
            "Very dark image."
        )

    elif brightness > 230:

        score -= 10

        reasons.append(
            "Very bright image."
        )

    # ====================================================
    # LIMIT SCORE
    # ====================================================

    score = max(
        0,
        min(score, 100)
    )

    # ====================================================
    # FINAL STATUS
    # ====================================================

    if score >= 80:

        status = "Likely Genuine"

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
            "Image passed the available verification checks."
        )

    # ====================================================
    # RETURN RESULT
    # ====================================================

    return (
        score,
        status,
        reasons,
        width,
        height
    )
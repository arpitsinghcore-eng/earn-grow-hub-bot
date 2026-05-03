import pytesseract
from PIL import Image
import os


def extract_text(image_path: str) -> str:
    try:
        if not os.path.exists(image_path):
            return ""

        img = Image.open(image_path)

        # Better OCR image prep
        img = img.convert("L")      # grayscale
        img = img.resize(
            (img.width * 2, img.height * 2)
        )

        text = pytesseract.image_to_string(
            img,
            config="--psm 6"
        )

        return text.lower().strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""
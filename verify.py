import hashlib
from PIL import Image
from utils.ocr import extract_text
import re


def is_edited_image(image_path: str) -> bool:
    # Basic dummy checker
    return False


def check_time_in_text(text: str) -> bool:
    # Check time like 12:34
    return bool(re.search(r"\d{1,2}:\d{2}", text))


def get_image_hash(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None


def verify_gmail_screenshot(image_path: str, email: str):
    if is_edited_image(image_path):
        return False, "Edited Screenshot"

    text = extract_text(image_path)

    if not text:
        return False, "Could not read text from image."

    text = text.lower()

    if "gmail" not in text and "google" not in text:
        return False, "Wrong screen. Not Gmail."

    if email.lower() not in text:
        return False, "Assigned Gmail not found."

    if not check_time_in_text(text):
        return False, "Time not visible."

    return True, "Valid"


def verify_review_screenshot(image_path: str, place_name: str, keywords: str):
    if is_edited_image(image_path):
        return False, "Edited Screenshot"

    text = extract_text(image_path)

    if not text:
        return False, "Could not read text from image."

    text = text.lower()

    if place_name.lower() not in text:
        return False, "Place/App name not found."

    if not check_time_in_text(text):
        return False, "Time not visible."

    if keywords:
        kw_list = [k.strip().lower() for k in keywords.split(",")]
        found = 0

        for word in kw_list:
            if word in text:
                found += 1

        if found == 0:
            return False, "Required keywords not found."

    return True, "Valid"
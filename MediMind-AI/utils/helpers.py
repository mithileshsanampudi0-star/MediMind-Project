import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from config import Config


def generate_unique_id():
    """
    Generate unique identifier.
    """

    return str(uuid.uuid4())


def current_timestamp():
    """
    Return UTC timestamp.
    """

    return datetime.utcnow()


def current_datetime_string():
    """
    Human readable datetime.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def sanitize_filename(filename: str):
    """
    Secure uploaded filenames.
    """

    return secure_filename(filename)


def allowed_file(filename: str):
    """
    Validate file extension.
    """

    return Config.allowed_file(filename)


def save_uploaded_file(file):
    """
    Save uploaded PDF file.
    """

    if file is None:
        raise ValueError("No file provided.")

    if file.filename == "":
        raise ValueError("Empty filename.")

    if not allowed_file(file.filename):
        raise ValueError(
            "Only PDF files are allowed."
        )

    filename = sanitize_filename(
        file.filename
    )

    unique_name = (
        f"{uuid.uuid4().hex}_{filename}"
    )

    save_path = os.path.join(
        Config.UPLOAD_FOLDER,
        unique_name
    )

    file.save(save_path)

    return {
        "filename": unique_name,
        "path": save_path
    }


def generate_report_filename():
    """
    Generate PDF filename.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return (
        f"health_report_{timestamp}.pdf"
    )


def clean_text(text):
    """
    Clean text from AI responses.
    """

    if not text:
        return ""

    return (
        text.replace("\r", "")
        .replace("\t", " ")
        .strip()
    )


def format_symptom_list(symptoms):
    """
    Convert symptom list to readable text.
    """

    if isinstance(symptoms, list):
        return ", ".join(symptoms)

    return str(symptoms)


def parse_ai_sections(response_text):
    """
    Convert structured AI response
    into dictionary sections.
    """

    result = {}

    current_section = None

    for line in response_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.endswith(":"):

            current_section = line[:-1]

            result[current_section] = []

        elif current_section:

            result[current_section].append(
                line
            )

    return result


def safe_get(dictionary, key, default=""):
    """
    Safe dictionary access.
    """

    return dictionary.get(key, default)


def success_response(message, data=None):

    return {
        "success": True,
        "message": message,
        "data": data or {}
    }


def error_response(message):

    return {
        "success": False,
        "message": message
    }
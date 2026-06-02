import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


class Config:
    """
    Production-ready configuration class for MediMind AI
    """

    
    # Application Settings
    
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "medimind-ai-production-secret-key"
    )

    DEBUG = os.getenv(
        "FLASK_DEBUG",
        "False"
    ).lower() == "true"

    HOST = os.getenv(
        "FLASK_HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "FLASK_PORT",
            5000
        )
    )

    # ==========================================================
    # Project Directories
    # ==========================================================
    BASE_DIR = PROJECT_ROOT

    TEMPLATE_FOLDER = BASE_DIR / "templates"

    STATIC_FOLDER = BASE_DIR / "static"

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    GENERATED_REPORTS_FOLDER = BASE_DIR / "generated_reports"

    # ==========================================================
    # Upload Settings
    # ==========================================================
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB

    ALLOWED_EXTENSIONS = {
        "pdf"
    }

    # ==========================================================
    # MongoDB Configuration
    # ==========================================================
    MONGODB_ATLAS_URI = os.getenv(
        "MONGODB_ATLAS_URI",
        ""
    ).strip().strip('"').strip("'")

    MONGO_URI = MONGODB_ATLAS_URI or os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/"
    ).strip().strip('"').strip("'")

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "medimind_ai"
    )

    # Collections
    USERS_COLLECTION = "users"
    SYMPTOMS_COLLECTION = "symptom_records"
    REPORTS_COLLECTION = "medical_reports"
    HOSPITALS_COLLECTION = "hospital_searches"
    ANALYSIS_COLLECTION = "analysis_history"

    # ==========================================================
    # Groq Configuration
    # ==========================================================
    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    GROQ_TEMPERATURE = float(
        os.getenv(
            "GROQ_TEMPERATURE",
            0.2
        )
    )

    GROQ_MAX_TOKENS = int(
        os.getenv(
            "GROQ_MAX_TOKENS",
            4096
        )
    )

    # ==========================================================
    # Google Maps Configuration (Optional)
    # ==========================================================
    GOOGLE_MAPS_API_KEY = os.getenv(
        "GOOGLE_MAPS_API_KEY",
        ""
    )

    # ==========================================================
    # OpenStreetMap & Nominatim Configuration (Free)
    # ==========================================================
    NOMINATIM_URL = "https://nominatim.openstreetmap.org"
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    HOSPITAL_SEARCH_RADIUS = 10000  # meters
    MAX_HOSPITAL_RESULTS = 10

    # ==========================================================
    # Medical Intelligence Configuration
    # ==========================================================
    EMERGENCY_KEYWORDS = [
        "chest pain",
        "heart attack",
        "stroke",
        "severe bleeding",
        "unconscious",
        "seizure",
        "difficulty breathing",
        "shortness of breath",
        "fainting",
        "paralysis",
        "loss of vision",
        "anaphylaxis",
        "poisoning",
        "suicidal",
        "severe burns"
    ]

    HIGH_RISK_TERMS = [
        "persistent fever",
        "blood in stool",
        "blood in urine",
        "rapid weight loss",
        "chronic cough",
        "high blood pressure",
        "extreme fatigue",
        "irregular heartbeat"
    ]

    # ==========================================================
    # PDF Configuration
    # ==========================================================
    PDF_TITLE = "MediMind AI Health Assessment Report"

    PDF_AUTHOR = "MediMind AI"

    PDF_SUBJECT = "Medical Analysis Report"

    PDF_KEYWORDS = (
        "health, symptoms, disease prediction, risk analysis, hospitals"
    )

    # ==========================================================
    # Logging Configuration
    # ==========================================================
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    LOG_FORMAT = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ==========================================================
    # Security Configuration
    # ==========================================================
    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True

    JSON_SORT_KEYS = False

    # ==========================================================
    # Dashboard Configuration
    # ==========================================================
    RECENT_REPORT_LIMIT = 10

    RECENT_ANALYSIS_LIMIT = 10

    HOSPITAL_SEARCH_RADIUS = 10000  # meters

    MAX_HOSPITAL_RESULTS = 10

    # ==========================================================
    # Voice Input Configuration
    # ==========================================================
    SPEECH_LANGUAGE = "en-US"

    # ==========================================================
    # Utility Methods
    # ==========================================================
    @staticmethod
    def validate_environment():
        """
        Validate required environment variables.
        """

        missing = []

        if not Config.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")

        if not Config.GOOGLE_MAPS_API_KEY:
            missing.append("GOOGLE_MAPS_API_KEY")

        return missing

    @staticmethod
    def create_directories():
        """
        Create required project directories.
        """

        directories = [
            Config.UPLOAD_FOLDER,
            Config.GENERATED_REPORTS_FOLDER
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Validate uploaded file extension.
        """

        return (
            "." in filename and
            filename.rsplit(".", 1)[1].lower()
            in Config.ALLOWED_EXTENSIONS
        )
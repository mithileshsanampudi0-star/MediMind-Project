from services.groq_service import groq_service
from utils.prompts import EMERGENCY_DETECTION_PROMPT
from utils.helpers import clean_text
from config import Config


class EmergencyAgent:
    """
    Emergency Detection Agent

    Responsibilities:
    - Detect emergency situations
    - Recommend immediate action
    - Trigger escalation workflow
    """

    def analyze(
        self,
        symptoms,
        risk_assessment
    ):
        """
        Perform emergency triage.
        """

        try:

            response = groq_service.generate(
                prompt_template=EMERGENCY_DETECTION_PROMPT,
                variables={
                    "symptoms": symptoms,
                    "risk_assessment": risk_assessment
                }
            )

            return {
                "success": True,
                "emergency": clean_text(response)
            }

        except Exception as error:

            return {
                "success": False,
                "emergency": "",
                "error": str(error)
            }

    def keyword_screening(
        self,
        symptoms
    ):
        """
        Fast emergency screening before AI call.
        """

        symptoms_text = str(symptoms).lower()

        for keyword in Config.EMERGENCY_KEYWORDS:

            if keyword.lower() in symptoms_text:

                return {
                    "emergency": True,
                    "keyword": keyword
                }

        return {
            "emergency": False,
            "keyword": None
        }

    def is_emergency(
        self,
        emergency_text
    ):
        """
        Determine emergency status.
        """

        text = emergency_text.upper()

        return (
            "EMERGENCY STATUS:" in text
            and "YES" in text
        )

    def ambulance_required(
        self,
        emergency_text
    ):
        """
        Check ambulance recommendation.
        """

        text = emergency_text.upper()

        return (
            "AMBULANCE RECOMMENDED:" in text
            and "YES" in text
        )

    def immediate_action(
        self,
        emergency_text
    ):
        """
        Extract immediate action text.
        """

        lines = emergency_text.splitlines()

        for line in lines:

            if "IMMEDIATE ACTION" in line.upper():

                parts = line.split(":")

                if len(parts) > 1:
                    return parts[1].strip()

        return "Seek medical advice."


emergency_agent = EmergencyAgent()
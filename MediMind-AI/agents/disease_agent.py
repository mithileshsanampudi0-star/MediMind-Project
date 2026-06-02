from services.groq_service import groq_service
from utils.prompts import DISEASE_PREDICTION_PROMPT
from utils.helpers import clean_text


class DiseaseAgent:
    """
    Disease Prediction Agent

    Responsibilities:
    - Differential diagnosis
    - Condition ranking
    - Specialist recommendation
    - Confidence estimation
    """

    def predict(
        self,
        symptoms,
        symptom_analysis
    ):
        """
        Generate disease predictions.
        """

        try:

            response = groq_service.generate(
                prompt_template=DISEASE_PREDICTION_PROMPT,
                variables={
                    "symptoms": symptoms,
                    "analysis": symptom_analysis
                }
            )

            return {
                "success": True,
                "prediction": clean_text(response)
            }

        except Exception as error:

            return {
                "success": False,
                "prediction": "",
                "error": str(error)
            }

    def extract_specialist(
        self,
        prediction_text
    ):
        """
        Extract recommended specialist.
        """

        specialist = "General Physician"

        lines = prediction_text.splitlines()

        for line in lines:

            if (
                "RECOMMENDED SPECIALIST"
                in line.upper()
            ):
                parts = line.split(":")

                if len(parts) > 1:
                    specialist = parts[1].strip()

        return specialist

    def confidence_level(
        self,
        prediction_text
    ):
        """
        Extract confidence level.
        """

        confidence = "Moderate"

        lines = prediction_text.splitlines()

        for line in lines:

            if (
                "CONFIDENCE LEVEL"
                in line.upper()
            ):
                parts = line.split(":")

                if len(parts) > 1:
                    confidence = parts[1].strip()

        return confidence


disease_agent = DiseaseAgent()
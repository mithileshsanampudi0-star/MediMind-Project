from services.groq_service import groq_service
from utils.prompts import SYMPTOM_ANALYSIS_PROMPT
from utils.helpers import clean_text


class SymptomAgent:
    """
    Symptom Analysis Agent

    Responsibilities:
    - Analyze symptom descriptions
    - Identify affected systems
    - Detect warning signs
    - Determine severity
    """

    def analyze(
        self,
        symptoms,
        age=None,
        gender=None
    ):
        """
        Perform symptom analysis.
        """

        try:

            response = groq_service.generate(
                prompt_template=SYMPTOM_ANALYSIS_PROMPT,
                variables={
                    "symptoms": symptoms,
                    "age": age or "Not Provided",
                    "gender": gender or "Not Provided"
                }
            )

            return {
                "success": True,
                "analysis": clean_text(response)
            }

        except Exception as error:

            return {
                "success": False,
                "analysis": "",
                "error": str(error)
            }

    def quick_severity_check(
        self,
        symptoms
    ):
        """
        Basic severity screening before AI analysis.
        """

        symptoms_text = str(symptoms).lower()

        critical_terms = [
            "chest pain",
            "stroke",
            "seizure",
            "unconscious",
            "difficulty breathing",
            "shortness of breath",
            "severe bleeding",
            "paralysis"
        ]

        for term in critical_terms:

            if term in symptoms_text:

                return {
                    "severity": "Critical",
                    "flagged": True,
                    "reason": term
                }

        return {
            "severity": "Unknown",
            "flagged": False,
            "reason": None
        }


symptom_agent = SymptomAgent()
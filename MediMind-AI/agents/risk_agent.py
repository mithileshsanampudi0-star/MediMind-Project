from services.groq_service import groq_service
from utils.prompts import RISK_ASSESSMENT_PROMPT
from utils.helpers import clean_text


class RiskAgent:
    """
    Risk Assessment Agent

    Responsibilities:
    - Evaluate medical risk level
    - Identify complications
    - Determine urgency
    - Recommend follow-up actions
    """

    def assess(
        self,
        symptoms,
        disease_prediction
    ):
        """
        Generate risk assessment.
        """

        try:

            response = groq_service.generate(
                prompt_template=RISK_ASSESSMENT_PROMPT,
                variables={
                    "symptoms": symptoms,
                    "prediction": disease_prediction
                }
            )

            return {
                "success": True,
                "risk": clean_text(response)
            }

        except Exception as error:

            return {
                "success": False,
                "risk": "",
                "error": str(error)
            }

    def extract_risk_level(
        self,
        risk_text
    ):
        """
        Extract risk level from AI response.
        """

        risk_level = "Moderate"

        for line in risk_text.splitlines():

            if "RISK LEVEL" in line.upper():

                parts = line.split(":")

                if len(parts) > 1:
                    risk_level = parts[1].strip()

        return risk_level

    def extract_urgency(
        self,
        risk_text
    ):
        """
        Extract urgency level.
        """

        urgency = "Soon"

        for line in risk_text.splitlines():

            if "URGENCY" in line.upper():

                parts = line.split(":")

                if len(parts) > 1:
                    urgency = parts[1].strip()

        return urgency

    def is_high_risk(
        self,
        risk_text
    ):
        """
        Determine if assessment indicates
        elevated risk.
        """

        risk_level = self.extract_risk_level(
            risk_text
        ).lower()

        return risk_level in [
            "high",
            "critical"
        ]


risk_agent = RiskAgent()
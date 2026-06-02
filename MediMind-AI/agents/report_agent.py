from services.groq_service import groq_service
from services.report_generator import report_generator

from utils.prompts import (
    REPORT_ANALYSIS_PROMPT,
    HEALTH_SUMMARY_PROMPT
)

from utils.helpers import clean_text


class ReportAgent:
    """
    Medical Report Agent

    Responsibilities:
    - Analyze uploaded PDF report text
    - Generate patient summary
    - Create final healthcare PDF
    """

    def analyze_report(
        self,
        report_text
    ):
        """
        Analyze extracted report content.
        """

        try:

            response = groq_service.generate(
                prompt_template=REPORT_ANALYSIS_PROMPT,
                variables={
                    "report_text": report_text
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

    def generate_health_summary(
        self,
        symptoms,
        prediction,
        risk,
        emergency
    ):
        """
        Generate executive summary.
        """

        try:

            response = groq_service.generate(
                prompt_template=HEALTH_SUMMARY_PROMPT,
                variables={
                    "symptoms": symptoms,
                    "prediction": prediction,
                    "risk": risk,
                    "emergency": emergency
                }
            )

            return {
                "success": True,
                "summary": clean_text(response)
            }

        except Exception as error:

            return {
                "success": False,
                "summary": "",
                "error": str(error)
            }

    def generate_pdf_report(
        self,
        symptoms,
        analysis,
        prediction,
        risk,
        emergency,
        specialist,
        hospitals
    ):
        """
        Create final downloadable PDF.
        """

        try:

            report = report_generator.generate(
                symptoms=symptoms,
                analysis=analysis,
                prediction=prediction,
                risk=risk,
                emergency=emergency,
                specialist=specialist,
                hospitals=hospitals
            )

            return {
                "success": True,
                "filename": report["filename"],
                "filepath": report["filepath"]
            }

        except Exception as error:

            return {
                "success": False,
                "error": str(error)
            }


report_agent = ReportAgent()
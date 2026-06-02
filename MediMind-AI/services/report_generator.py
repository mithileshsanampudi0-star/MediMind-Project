from services.pdf_service import pdf_service
from utils.helpers import generate_report_filename


class ReportGenerator:
    """
    Central Report Generation Service
    Responsible for preparing and exporting
    complete patient assessment reports.
    """

    def generate(
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
        Generate final PDF report.
        """

        report_data = {
            "symptoms": symptoms,
            "analysis": analysis,
            "prediction": prediction,
            "risk": risk,
            "emergency": emergency,
            "specialist": specialist,
            "hospitals": hospitals
        }

        filename = generate_report_filename()

        pdf_path = pdf_service.create_health_report(
            filename=filename,
            report_data=report_data
        )

        return {
            "filename": filename,
            "filepath": pdf_path
        }


report_generator = ReportGenerator()
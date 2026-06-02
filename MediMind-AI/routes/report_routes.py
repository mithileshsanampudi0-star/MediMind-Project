import os

from flask import (
    Blueprint,
    render_template,
    request,
    send_from_directory,
    session
)

from config import Config

from agents.report_agent import (
    report_agent
)

from services.pdf_extraction_service import (
    pdf_extraction_service
)

from database.mongo import MongoDB

from utils.helpers import (
    save_uploaded_file,
    current_timestamp
)


report_bp = Blueprint(
    "reports",
    __name__
)


@report_bp.route(
    "/upload",
    methods=["GET"]
)
def upload_page():
    """
    Upload report page.
    """

    return render_template(
        "upload_report.html"
    )


@report_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_report():
    """
    Upload and analyze report.
    """

    try:

        if "report" not in request.files:

            return render_template(
                "analysis_result.html",
                error_message=
                "No report uploaded."
            )

        uploaded_file = (
            request.files["report"]
        )

        saved_file = (
            save_uploaded_file(
                uploaded_file
            )
        )

        pdf_path = saved_file["path"]

        report_text = (
            pdf_extraction_service
            .extract_text(pdf_path)
        )

        report_result = (
            report_agent
            .analyze_report(
                report_text
            )
        )

        report_analysis = (
            report_result.get(
                "analysis",
                ""
            )
        )

        pdf_result = (
            report_agent
            .generate_pdf_report(
                symptoms="N/A",
                analysis=report_analysis,
                prediction="N/A",
                risk="N/A",
                emergency="N/A",
                specialist="N/A",
                hospitals=[]
            )
        )

        generated_file = (
            pdf_result.get(
                "filename"
            )
        )

        try:

            MongoDB.reports_collection().insert_one(
                {
                    "user_id": str(session.get("user_id", "")),
                    "filename":
                        generated_file,
                    "report_analysis":
                        report_analysis,
                    "created_at":
                        current_timestamp()
                }
            )

        except Exception:
            pass

        return render_template(
            "analysis_result.html",
            report_analysis=
                report_analysis,
            symptom_analysis="",
            disease_prediction="",
            risk_assessment="",
            specialist="N/A",
            hospitals=[],
            pdf_file=generated_file
        )

    except Exception as error:

        return render_template(
            "analysis_result.html",
            error_message=str(error)
        )


@report_bp.route(
    "/download/<filename>"
)
def download_report(filename):

    file_path = os.path.join(
        Config.GENERATED_REPORTS_FOLDER,
        filename
    )

    if not os.path.isfile(file_path):

        return render_template(
            "analysis_result.html",
            error_message=
            "Requested report file not found."
        )

    return send_from_directory(
        Config.GENERATED_REPORTS_FOLDER,
        filename,
        as_attachment=True
    )
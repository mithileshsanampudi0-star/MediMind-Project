from flask import (
    Blueprint,
    render_template,
    request,
    session
)

from agents.symptom_agent import symptom_agent
from agents.disease_agent import disease_agent
from agents.risk_agent import risk_agent
from agents.emergency_agent import emergency_agent

from database.mongo import MongoDB
from utils.helpers import current_timestamp


symptom_bp = Blueprint(
    "symptoms",
    __name__
)


@symptom_bp.route("/", methods=["GET"])
def symptom_checker():
    """
    Symptom checker page.
    """

    return render_template(
        "symptom_checker.html"
    )


@symptom_bp.route(
    "/analyze",
    methods=["POST"]
)
def analyze_symptoms():
    """
    Complete symptom workflow.
    """

    symptoms = request.form.get(
        "symptoms",
        ""
    )

    age = request.form.get(
        "age",
        ""
    )

    gender = request.form.get(
        "gender",
        ""
    )

    try:

        symptom_result = (
            symptom_agent.analyze(
                symptoms=symptoms,
                age=age,
                gender=gender
            )
        )

        symptom_analysis = (
            symptom_result.get(
                "analysis",
                ""
            )
        )

        disease_result = (
            disease_agent.predict(
                symptoms=symptoms,
                symptom_analysis=symptom_analysis
            )
        )

        disease_prediction = (
            disease_result.get(
                "prediction",
                ""
            )
        )

        risk_result = (
            risk_agent.assess(
                symptoms=symptoms,
                disease_prediction=disease_prediction
            )
        )

        risk_assessment = (
            risk_result.get(
                "risk",
                ""
            )
        )

        emergency_result = (
            emergency_agent.analyze(
                symptoms=symptoms,
                risk_assessment=risk_assessment
            )
        )

        emergency_text = (
            emergency_result.get(
                "emergency",
                ""
            )
        )

        specialist = (
            disease_agent.extract_specialist(
                disease_prediction
            )
        )

        emergency_flag = (
            emergency_agent.is_emergency(
                emergency_text
            )
        )

        risk_level = (
            risk_agent.extract_risk_level(
                risk_assessment
            )
        )

        try:

            MongoDB.analysis_collection().insert_one(
                {
                    "user_id": str(session.get("user_id", "")),
                    "symptoms": symptoms,
                    "age": age,
                    "gender": gender,
                    "symptom_analysis":
                        symptom_analysis,
                    "disease_prediction":
                        disease_prediction,
                    "risk_assessment":
                        risk_assessment,
                    "specialist":
                        specialist,
                    "risk_level":
                        risk_level,
                    "emergency":
                        emergency_flag,
                    "status":
                        "Completed",
                    "created_at":
                        current_timestamp()
                }
            )

        except Exception:
            pass

        return render_template(
            "analysis_result.html",
            symptom_analysis=symptom_analysis,
            disease_prediction=disease_prediction,
            risk_assessment=risk_assessment,
            specialist=specialist,
            emergency_alert=(
                emergency_text
                if emergency_flag
                else None
            ),
            hospitals=[],
            pdf_file=None
        )

    except Exception as error:

        return render_template(
            "analysis_result.html",
            error_message=str(error)
        )
from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from database.analysis_model import (
    AnalysisModel
)

analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/")
def analytics():

    if "user_id" not in session:
        return redirect(
            "/auth/login"
        )

    user_id = (
        session["user_id"]
    )

    records = (
        AnalysisModel
        .get_user_history(
            user_id=user_id,
            limit=100
        )
    )

    risk_counts = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }

    emergency_cases = 0

    for record in records:

        risk = (
            record.get(
                "risk_level",
                ""
            )
            .title()
        )

        if risk in risk_counts:
            risk_counts[risk] += 1

        if record.get(
            "emergency",
            False
        ):
            emergency_cases += 1

    return render_template(

        "analytics.html",

        risk_counts=
            risk_counts,

        emergency_cases=
            emergency_cases,

        total_records=
            len(records)

    )
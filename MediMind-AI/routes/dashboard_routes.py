from flask import Blueprint, render_template, session, redirect
from database.mongo import MongoDB


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():
    """
    Main dashboard page with authentication check.
    """

    # -------------------------
    # AUTH CHECK
    # -------------------------
    if "user_id" not in session:
        return redirect("/login")

    # -------------------------
    # DEFAULT DATA
    # -------------------------
    stats = {
        "total_analyses": 0,
        "total_reports": 0,
        "total_hospital_searches": 0,
        "emergency_cases": 0
    }

    recent_analyses = []

    try:

        analysis_collection = MongoDB.analysis_collection()
        reports_collection = MongoDB.reports_collection()
        hospitals_collection = MongoDB.hospitals_collection()

        stats["total_analyses"] = analysis_collection.count_documents({})
        stats["total_reports"] = reports_collection.count_documents({})
        stats["total_hospital_searches"] = hospitals_collection.count_documents({})
        stats["emergency_cases"] = analysis_collection.count_documents(
            {"emergency": True}
        )

        recent_records = list(
            analysis_collection.find().sort("created_at", -1).limit(10)
        )

        for record in recent_records:
            recent_analyses.append({
                "created_at": str(record.get("created_at", "")),
                "symptoms": record.get("symptoms", ""),
                "risk_level": record.get("risk_level", "Unknown"),
                "status": record.get("status", "Completed")
            })

    except Exception:
        pass

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_analyses=recent_analyses
    )
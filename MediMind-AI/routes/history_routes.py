from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

from services.history_service import (
    HistoryService
)

history_bp = Blueprint(
    "history",
    __name__
)


@history_bp.route("/")
def history():

    if "user_id" not in session:
        return redirect("/auth/login")

    user_id = (
        session["user_id"]
    )

    records = (
        HistoryService
        .get_user_history(
            user_id
        )
    )

    summary = (
        HistoryService
        .get_history_summary(
            user_id
        )
    )

    return render_template(
        "history.html",
        records=records,
        summary=summary
    )
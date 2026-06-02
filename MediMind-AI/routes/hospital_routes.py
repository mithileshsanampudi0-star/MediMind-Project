from flask import (
    Blueprint,
    render_template,
    request
)

from agents.hospital_agent import (
    hospital_agent
)


hospital_bp = Blueprint(
    "hospitals",
    __name__
)


@hospital_bp.route(
    "/",
    methods=["GET"]
)
@hospital_bp.route(
    "/search",
    methods=["GET"]
)
def hospital_search_page():
    """
    Hospital search page.
    """

    return render_template(
        "hospital_results.html",
        hospitals=[]
    )


@hospital_bp.route(
    "/search",
    methods=["POST"]
)
def hospital_search():
    """
    Search nearby hospitals.
    """

    location = request.form.get(
        "location",
        ""
    )

    specialist = request.form.get(
        "specialist",
        ""
    )

    try:

        result = (
            hospital_agent.top_hospitals(
                location=location,
                specialist=specialist,
                limit=10
            )
        )

        if not result.get("success", False):
            return render_template(
                "hospital_results.html",
                hospitals=[],
                error_message=result.get("error", "Unable to search hospitals.")
            )

        hospitals = result.get(
            "hospitals",
            []
        )

        if not hospitals:
            return render_template(
                "hospital_results.html",
                hospitals=[],
                error_message="No hospitals found for the provided location. Please try a different address."
            )

        return render_template(
            "hospital_results.html",
            hospitals=hospitals
        )

    except Exception as error:

        return render_template(
            "hospital_results.html",
            hospitals=[],
            error_message=str(error)
        )
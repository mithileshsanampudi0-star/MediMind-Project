from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from database.profile_model import (
    ProfileModel
)

profile_bp = Blueprint(
    "profile",
    __name__
)


@profile_bp.route(
    "/",
    methods=["GET", "POST"]
)
def profile():

    if "user_id" not in session:
        return redirect("/auth/login")

    user_id = session["user_id"]

    if request.method == "POST":

        age = request.form.get(
            "age",
            ""
        )

        gender = request.form.get(
            "gender",
            ""
        )

        blood_group = request.form.get(
            "blood_group",
            ""
        )

        allergies = request.form.get(
            "allergies",
            ""
        )

        conditions = request.form.get(
            "conditions",
            ""
        )

        ProfileModel.save_profile(

            user_id=user_id,

            age=age,

            gender=gender,

            blood_group=blood_group,

            allergies=allergies,

            conditions=conditions

        )

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            "/profile"
        )

    profile = (
        ProfileModel.get_profile(
            user_id
        )
    )

    return render_template(
        "profile.html",
        profile=profile
    )
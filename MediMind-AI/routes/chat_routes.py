from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect
)

from services.chat_service import (
    ChatService
)

chat_bp = Blueprint(
    "chat",
    __name__
)


@chat_bp.route("/")
def chat_page():

    if "user_id" not in session:
        return redirect(
            "/auth/login"
        )

    history = (
        ChatService.get_chat_history(
            session["user_id"]
        )
    )

    return render_template(
        "chat_assistant.html",
        history=history
    )


@chat_bp.route(
    "/send",
    methods=["POST"]
)
def send_message():

    if "user_id" not in session:

        return jsonify(
            {
                "success": False,
                "message":
                    "Unauthorized"
            }
        )

    data = request.get_json()

    message = (
        data.get(
            "message",
            ""
        )
        .strip()
    )

    if not message:

        return jsonify(
            {
                "success": False
            }
        )

    response = (
        ChatService.medical_chat(
            session["user_id"],
            message
        )
    )

    return jsonify(
        {
            "success": True,
            "response": response
        }
    )


@chat_bp.route("/clear")
def clear_chat():

    if "user_id" not in session:
        return redirect(
            "/auth/login"
        )

    ChatService.clear_chat(
        session["user_id"]
    )

    return redirect(
        "/chat"
    )
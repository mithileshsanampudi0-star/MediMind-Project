import sys

from flask import (
    Flask,
    render_template,
    redirect,
    session,
    request
)

from config import Config

from database.mongo import (
    MongoDB,
    create_indexes
)

# ==================================================
# APP FACTORY
# ==================================================

def create_app():

    app = Flask(
        __name__,
        template_folder=str(
            Config.TEMPLATE_FOLDER
        ),
        static_folder=str(
            Config.STATIC_FOLDER
        )
    )

    # ==================================================
    # CONFIG
    # ==================================================

    app.config["SECRET_KEY"] = (
        Config.SECRET_KEY
    )

    app.config["UPLOAD_FOLDER"] = (
        str(
            Config.UPLOAD_FOLDER
        )
    )

    app.config["MAX_CONTENT_LENGTH"] = (
        Config.MAX_CONTENT_LENGTH
    )

    app.config["JSON_SORT_KEYS"] = (
        Config.JSON_SORT_KEYS
    )

    # ==================================================
    # CREATE DIRECTORIES
    # ==================================================

    Config.create_directories()

    # ==================================================
    # DATABASE
    # ==================================================

    MongoDB.initialize()

    create_indexes()

    from services.maps_service import maps_service
    maps_service.seed_hospitals()

    # ==================================================
    # BLUEPRINTS (Import after DB init)
    # ==================================================

    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.symptom_routes import symptom_bp
    from routes.hospital_routes import hospital_bp
    from routes.report_routes import report_bp
    from routes.history_routes import history_bp
    from routes.analytics_routes import analytics_bp
    from routes.chat_routes import chat_bp
    from routes.profile_routes import profile_bp

    # ==================================================
    # LOGIN PROTECTION
    # ==================================================

    @app.before_request
    def require_login():

        allowed_routes = [

            "auth.login",

            "auth.register",

            "static",

            "health_check"

        ]

        if request.endpoint in allowed_routes:
            return

        if "user_id" not in session:

            return redirect(
                "/auth/login"
            )

    # ==================================================
    # REGISTER BLUEPRINTS
    # ==================================================

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        symptom_bp,
        url_prefix="/symptoms"
    )

    app.register_blueprint(
        hospital_bp,
        url_prefix="/hospitals"
    )

    app.register_blueprint(
        report_bp,
        url_prefix="/reports"
    )

    app.register_blueprint(
        history_bp,
        url_prefix="/history"
    )

    app.register_blueprint(
        analytics_bp,
        url_prefix="/analytics"
    )

    app.register_blueprint(
        chat_bp,
        url_prefix="/chat"
    )

    app.register_blueprint(
        profile_bp,
        url_prefix="/profile"
    )

    # ==================================================
    # CONTEXT PROCESSOR
    # ==================================================

    @app.context_processor
    def inject_globals():

        return {

            "app_name":
                "MediMind AI"

        }

    # ==================================================
    # HEALTH CHECK
    # ==================================================

    @app.route("/health")
    def health_check():

        return {

            "status":
                "running",

            "application":
                "MediMind AI"

        }

    # ==================================================
    # ERROR HANDLERS
    # ==================================================

    @app.errorhandler(404)
    def not_found(error):

        return render_template(
        "404.html"
        ),404

    @app.errorhandler(413)
    def file_too_large(error):

        return render_template(
            "analysis_result.html",
            title="Upload Error",
            error_message=
            "Uploaded file is too large."
        ), 413

    @app.errorhandler(500)
    def internal_error(error):

        return render_template(
            "analysis_result.html",
            title="Server Error",
            error_message=
            "An internal server error occurred."
        ), 500
    
    @app.route("/favicon.ico")
    def favicon():
        return "", 204
    
    return app


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    missing_env = (
        Config.validate_environment()
    )

    if missing_env:

        print(
            "\nMissing Environment Variables:"
        )

        for item in missing_env:

            print(
                f" - {item}"
            )

        sys.exit(1)

    app = create_app()

    app.run(

        host=Config.HOST,

        port=Config.PORT,

        debug=Config.DEBUG

    )
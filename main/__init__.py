from flask import Flask, render_template
from config import Config

from main.logger import getLogger
from main.extensions import db, migrate

def create_app():
    app = Flask(__name__)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404_page_not_found.html"), 404

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .routes.resume_analyser import resume_analyser_bp
    from .routes.loader import loader_bp
    from .routes.suggestions import suggestions_bp
    from .routes.enhancer import enhancer_bp

    app.register_blueprint(resume_analyser_bp)
    app.register_blueprint(loader_bp)
    app.register_blueprint(suggestions_bp)
    app.register_blueprint(enhancer_bp)


    # Log application startup
    getLogger("event").info("Flask app initialized.")

    return app
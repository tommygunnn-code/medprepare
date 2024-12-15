from flask import Flask
from flask_cors import CORS
from config import load_config
from routes.pdf_routes import pdf_bp
from routes.ai_routes import ai_bp
import logging

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, static_folder="../frontend")
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",  # Allow all origins
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Accept"],
            "expose_headers": ["Content-Type"]
        }
    })

    # Load configuration
    try:
        load_config(app)
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise

    # Set up logging
    setup_logging(app)

    # Register blueprints
    app.register_blueprint(pdf_bp, url_prefix="/pdf")
    app.register_blueprint(ai_bp, url_prefix="/ai")

    @app.errorhandler(404)
    def handle_404(error):
        app.logger.error(f"404 error: {error}")
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def handle_500(error):
        app.logger.error(f"500 error: {error}")
        return {"error": "Internal server error"}, 500

    return app


def setup_logging(app):
    """Set up logging for the Flask application."""
    log_level = app.config.get("LOG_LEVEL", logging.INFO)
    log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"

    logging.basicConfig(level=log_level, format=log_format)
    app.logger.setLevel(log_level)

    app.logger.info("Logging is set up.")


if __name__ == "__main__":
    try:
        app = create_app()
        app.run(debug=app.config.get("DEBUG", True))
    except Exception as e:
        logging.critical(f"Failed to start the application: {e}", exc_info=True)

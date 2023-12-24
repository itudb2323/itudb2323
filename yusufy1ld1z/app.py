from flask import Flask
from config import Config
from db import db
from controllers.DocumentController import document_bp

# Create a Flask application instance and specify the template folder
app = Flask(__name__, template_folder="views")

# Load configuration from Config class
app.config.from_object(Config)

# Initialize the database with the Flask application
db.init_app(app)

# Register the blueprint (DocumentController) with the application
app.register_blueprint(document_bp)

# Run the Flask application if this script is the main entry point
if __name__ == "__main__":
    # Start the application with the specified host and port from the configuration
    app.run(host=Config.HOST, port=Config.PORT)

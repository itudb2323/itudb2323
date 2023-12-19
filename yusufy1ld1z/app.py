from flask import Flask
from config import Config
from db import db
from controllers.DocumentController import document_bp

app = Flask(__name__, template_folder="views")
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(document_bp)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT)

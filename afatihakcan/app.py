from flask import Flask
from db import db
from config import Config
from controllers.PersonController import person_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT)

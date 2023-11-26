from flask import Flask
from db import db
from config import Config
from controllers.ProductController import product_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(product_bp)

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT)

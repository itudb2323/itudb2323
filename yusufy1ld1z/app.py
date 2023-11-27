import os
from flask import Flask, render_template
from config import Config
from db import db
from controllers.DocumentController import document_bp

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "./views"),
)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(document_bp)


# for debugging purposes
@app.route("/")
def home():
    return render_template("base.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

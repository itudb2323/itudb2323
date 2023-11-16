from flask import Flask, render_template
import passwd_mask
import os

app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../templates"
    ),
)


@app.route("/")
def home():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)

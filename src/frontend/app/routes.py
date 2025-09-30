from flask import Flask, render_template, request
from app.pairing import generate_pairing

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        season = request.form.get("season")
        location = request.form.get("location")
        preferences = {
            "wine_style": request.form.get("wine_style"),
            "cheese_type": request.form.get("cheese_type"),
            "budget": request.form.get("budget"),
            "dietary": request.form.get("dietary")
        }
        result = generate_pairing(season, location, preferences)
    return render_template("index.html", result=result)

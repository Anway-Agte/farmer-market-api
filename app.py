from flask import Flask, jsonify, request, render_template, url_for, flash
from flask_pymongo import PyMongo
import requests
import datetime
import json
import uuid

from werkzeug.utils import redirect
from Constants.constants import CATEGORIES, UNITS

app = Flask(__name__)
app.secret_key = (
    "\xea\xf5|k\xb8\x02+\xba\x18\x90\x80v\xcb?\xab\xab\x8d\x86\x92\xe5\xff\xbe"
)
app.config["MONGO_URI"] = "mongodb://localhost:27017/farmer_marketplace"

mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def index():
    return "Hello Anway"


@app.route("/create", methods=["GET"])
def createCatalogue():
    return render_template("additem.html", categories=CATEGORIES, units=UNITS)


@app.route("/recieve", methods=["POST"])
def recieve():
    catalogueItem = {
        "_id": uuid.uuid4().hex,
        "name": request.form.get("name"),
        "category": request.form.get("category"),
        "price": int(request.form.get("price")),
        "per": int(request.form.get("per")),
        "unit": request.form.get("unit"),
        "inc_factor": 0,
        "available": True,
    }

    if catalogueItem["unit"] == "kg":
        catalogueItem["inc_factor"] = 0.25
    elif catalogueItem["unit"] == "gm":
        catalogueItem["inc_factor"] = 1
    elif catalogueItem["unit"] == "dozen":
        catalogueItem["inc_factor"] == 0.5
    else:
        catalogueItem["inc_factor"] = 1

    if mongo.db.catalogue.insert_one(catalogueItem):
        flash("Item added successfully", "success")
    else:
        flash("Please try again", "danger")
    return redirect(url_for("createCatalogue"))


@app.route("/register", method=["POST"])
def register():
    data = request.get_json()
    print(data)
    return jsonify({"status": "OK"})


@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)

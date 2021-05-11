from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests
import datetime
import json
from Constants.constants import CATEGORIES

app = Flask(__name__)

app.config["MONGO_DB"] = "farmer_marketplace"
app.config["MONGO_URI"] = "mongodb://localhost:27017/farmer_marketplace"

mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"hello": "world"})


@app.route("/register-user", methods=["POST"])
def registerUser():
    user = None

    try:
        user = request.get_json()

    except:
        pass

    if user is None:

        return ({"err": "There was an error, please try again"}, 400)

    else:
        matching_address_user = mongo.db.users.find_one(
            {
                "city": user["city"],
                "society": user["society"],
                "bldg": user["bldg"],
                "flat": user["flat"],
            }
        )

        if matching_address_user:

            return {"err": "An account with this address already exists "}

        else:

            if mongo.db.users.insert_one(user):

                return {"success": "Successfully registered", "id": user["_id"]}

            else:

                return {"We're sorry for the inconvinience, please try again."}


@app.route("/get-user/", methods=["POST"])
def get_user():

    data = None

    try:

        data = request.get_json()

    except:

        pass

    if data is None:

        return {"err": "Bad request"}

    else:

        user = None

        try:

            user = dict(mongo.db.find_one({"_id": data["_id"]}))

        except:
            pass

        if user is None:

            return {"err": "This user does not exist"}

        else:

            return (user, 200)


if __name__ == "__main__":
    app.run(debug=True)

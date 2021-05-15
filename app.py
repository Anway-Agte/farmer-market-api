from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests
import datetime
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Hello Anway"


if __name__ == "__main__":
    app.run(debug=True)

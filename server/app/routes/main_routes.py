from flask import jsonify
from . import main

@main.route('/')
def home():
    return jsonify({"message": "Welcome to EarthLens Flask backend!"})

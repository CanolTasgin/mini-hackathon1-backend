import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
  
@app.route("/data", methods=["GET"])
def get_data():
    with open("data.json") as f:
        data = json.load(f)

    return jsonify(data)
  

@app.route("/data", methods=["POST"])
def add_data():
    with open("data.json") as f:
        data = json.load(f)

    new_data = request.json

    data.update(new_data)

    with open("data.json", "w") as f:
        json.dump(data, f)

    return jsonify({"message": "Data added successfully."})
  
@app.route("/data/<int:id>", methods=["PUT"])
def update_data(id):
    with open("data.json") as f:
        data = json.load(f)

    rooms = data["rooms"]

    for room in rooms:
        if room["id"] == id:
            room.update(request.json)
            break
    else:
        return jsonify({"error": "Room not found."}), 404

    with open("data.json", "w") as f:
        json.dump(data, f)

    return jsonify({"message": "Data updated successfully."})

@app.route("/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    with open("data.json") as f:
        data = json.load(f)

    rooms = data["rooms"]

    for i, room in enumerate(rooms):
        if room["id"] == id:
            del rooms[i]
            break
    else:
        return jsonify({"error": "Room not found."}), 404

    with open("data.json", "w") as f:
        json.dump(data, f)

    return jsonify({"message": "Data deleted successfully."})


@app.route("/food", methods=["GET"])
def get_foods():
    with open("food.json") as f:
        foods = json.load(f)

    return jsonify(foods)
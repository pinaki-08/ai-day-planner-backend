from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB
from agent import get_ai_suggestion

app = Flask(__name__)
CORS(app)
db = TinyDB('db.json')

@app.route("/add-task", methods=["POST"])
def add_task():
    task = request.json.get("task")
    db.insert({"task": task})
    return jsonify({"message": "Task added"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = db.all()
    return jsonify({"tasks": tasks})

@app.route("/suggest", methods=["GET"])
def suggest_tasks():
    tasks = [t["task"] for t in db.all()]
    suggestion = get_ai_suggestion(tasks)
    return jsonify({"suggestion": suggestion})

@app.route("/clear", methods=["POST"])
def clear_tasks():
    db.truncate()
    return jsonify({"message": "All tasks cleared."})

if __name__ == "__main__":
    app.run(debug=True)

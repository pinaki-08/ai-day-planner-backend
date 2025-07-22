# Default route to show backend is running

from flask import Flask, request, jsonify
from flask_cors import CORS
from tinydb import TinyDB
from agent import get_ai_suggestion, analyze_product_url

app = Flask(__name__)
CORS(app)
db = TinyDB('db.json')

@app.route("/")
def index():
    return "AI Day Planner Backend is running."

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


# New route for clothing product analysis
@app.route("/analyze-product", methods=["POST"])
def analyze_product():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    result = analyze_product_url(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

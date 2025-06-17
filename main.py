
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask läuft! Die API ist erreichbar."

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    print("📥 Anfrage erhalten:", data)
    return jsonify({"status": "success", "message": "Analyse-Router funktioniert!", "received": data})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

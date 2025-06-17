from flask import Flask, request, jsonify
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask läuft – API bereit."

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    return jsonify({
        "message": "Analyze funktioniert!",
        "received": data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

    # Debug-Endlosschleife
    while True:
        print("✅ Flask ist aktiv – Endlosschleife läuft")
        time.sleep(10)
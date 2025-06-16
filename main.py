from flask import Flask, request, jsonify
import openai
import datetime
import json
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("partners.json", encoding="utf-8") as f:
    PARTNERS = json.load(f)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json["answers"]
    partner_id = request.args.get("partner", "default")

    partner = PARTNERS.get(partner_id, {
        "partner_name": "KI-Sicherheit.jetzt",
        "logo_url": "https://check.ki-sicherheit.jetzt/badges/ki-sicherheit-logo.png",
        "footer_text": "KI-Beratung powered by KI-Sicherheit.jetzt",
        "farbe": "#002649"
    })

    prompt = f"""Analysiere folgende Angaben eines Unternehmens zur KI-Einführung. Gib:
1. Executive Summary
2. Strategische Bewertung
3. Drei konkrete Empfehlungen inkl. Tools & To-dos
4. Förderprogramme & Ressourcen
5. Risikoprofil & Pflichten laut EU-AI-Act
6. Branchenvergleich & Trendreport
7. Visionären Ausblick

Antworten: {data}"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    analysis = response.choices[0].message["content"]

    return jsonify({
        "partner": partner,
        "score": 74,  # später: GPT-basiert oder berechnet
        "datum": datetime.datetime.now().strftime("%d.%m.%Y"),
        "report": analysis
    })
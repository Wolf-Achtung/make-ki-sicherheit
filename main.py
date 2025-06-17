
from flask import Flask, request, jsonify
import openai
import datetime
import json
import os
import requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("partners.json", encoding="utf-8") as f:
    PARTNERS = json.load(f)

@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.json["answers"]
    partner_id = request.args.get("partner", "default")

    partner = PARTNERS.get(partner_id, {
        "partner_name": "KI-Sicherheit.jetzt",
        "logo_url": "https://check.ki-sicherheit.jetzt/badges/ki-sicherheit-logo.png",
        "footer_text": "KI-Beratung powered by KI-Sicherheit.jetzt",
        "farbe": "#002649"
    })

    system_prompt = f""" 
Du bist ein professioneller KI-Berater. Analysiere die Angaben eines Unternehmens zur Einführung von KI. Antworte **ausschließlich im folgenden JSON-Format**:

{{
  "executive_summary": "...",
  "analyse": "...",
  "score": 0–100,
  "empfehlungen": [
    {{
      "titel": "...",
      "beschreibung": "...",
      "next_step": "...",
      "tool": "..."
    }}
  ],
  "ressourcen": "...",
  "zukunft": "...",
  "risikoprofil": {{
    "risikoklasse": "...",
    "begruendung": "...",
    "pflichten": ["...", "..."]
  }},
  "tooltipps": [
    {{ "name": "...", "einsatz": "...", "warum": "..." }}
  ],
  "foerdertipps": [
    {{ "programm": "...", "zielgruppe": "...", "nutzen": "..." }}
  ],
  "branchenvergleich": "...",
  "trendreport": "...",
  "visionaer": "..."
}}

- Gib keine zusätzlichen Erklärungen oder Text vor/nach dem JSON aus.
- Passe Anzahl der Empfehlungen dynamisch an: je niedriger der Score, desto mehr Empfehlungen.
- Der Score basiert auf den Angaben und dem Branchendurchschnitt.
- Empfehlungen und Inhalte müssen konkret, umsetzbar und individuell sein.
- Beachte, dass die Antwort direkt als Grundlage für ein automatisiertes PDF verwendet wird.

Unternehmensangaben:
{user_input}
"""

    def ask_gpt(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message["content"]

    def try_parse_json(raw):
        try:
            return json.loads(raw), None
        except Exception as e:
            return None, str(e)

    gpt_output = ask_gpt(system_prompt)
    result_json, error = try_parse_json(gpt_output)

    if not result_json:
        print("⚠️ GPT JSON-Parsing fehlgeschlagen. Versuche Reparatur…")
        repair_prompt = f""" 
Deine letzte Antwort war fehlerhaftes JSON. Bitte korrigiere es so, dass es exakt dem Format aus dem Prompt entspricht. Gib ausschließlich ein **gültiges JSON-Objekt** zurück.
Hier ist deine fehlerhafte Ausgabe:
{gpt_output}
"""
        repaired = ask_gpt(repair_prompt)
        result_json, error = try_parse_json(repaired)

    if not result_json:
        return jsonify({"error": "GPT JSON-Fehler", "details": error}), 500

    return jsonify({
        "partner": partner,
        "datum": datetime.datetime.now().strftime("%d.%m.%Y"),
        **result_json
    })

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    pdfmonkey_api_key = os.getenv("PDFMONKEY_API_KEY")
    pdfmonkey_template_id = os.getenv("PDFMONKEY_TEMPLATE_ID")

    data = request.json

    payload = {
        "document": {
            "document_template_id": pdfmonkey_template_id,
            "payload": data
        }
    }

    response = requests.post(
        "https://api.pdfmonkey.io/api/v1/documents",
        json=payload,
        headers={
            "Authorization": f"Bearer {pdfmonkey_api_key}",
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 201:
        download_url = response.json()["data"]["attributes"]["download_url"]
        return jsonify({"pdf_url": download_url})
    else:
        return jsonify({"error": response.text}), 400

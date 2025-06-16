# KI-Sicherheits-Check Backend

Dies ist das Flask-Backend für das Projekt `make.ki-sicherheit.jetzt`. Es verarbeitet Formularantworten, analysiert sie via GPT-4 und gibt strukturierte Ergebnisse zurück – optional für PDFMonkey.

## Lokaler Start
```
pip install flask openai
export OPENAI_API_KEY=sk-...
flask run
```

## Endpunkt
`POST /analyze?partner=partnername`

Body (JSON):
```json
{
  "answers": {
    "name": "Max Mustermann",
    "unternehmen": "Test GmbH",
    ...
  }
}
```

Antwort:
GPT-Auswertung + Partnerbranding
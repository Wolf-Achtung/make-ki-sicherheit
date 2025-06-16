# KI-Agent-Service 🚀

Ein Agentensystem zur Analyse von Unternehmensdaten via KI (GPT-4), das automatisch ein Executive Briefing mit Handlungsempfehlungen erstellt.

## 📦 Projektstruktur

- `formular/`: HTML-Frontend mit Fragebogen
- `agent-backend/`: Node.js/Express + GPT-Agentenlogik
- Deployment: Netlify (Frontend) & Railway (Backend)

## 🧠 Agenten

1. **Strategist**: analysiert Ziele, Reifegrad, Potenzial
2. **Expert**: erstellt Empfehlungen mit Tools & Roadmap
3. **Legal**: DSGVO & EU AI Act Profil & Pflichten
4. **Merger**: generiert validiertes JSON für PDF-Ausgabe

## 🚀 Setup (lokal)

```bash
cd agent-backend
cp .env.example .env
npm install
npm run dev

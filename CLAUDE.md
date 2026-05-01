# VERSA

Flask web app dengan AI personas (10 watak berbeza) untuk diskusi pembelajaran dalam kelas. Deployed live — jangan ubah kod tanpa test dulu.

## Stack

- **Python** — Flask, Groq (LLM), Gunicorn
- **Frontend** — `versa.html`, PWA-ready (`manifest.json`, `sw.js`)

## Setup

```bash
pip install -r requirements.txt
GROQ_API_KEY=your_key python versa_app.py
```

## Penting

- Repo: https://github.com/fidfathir/versa
- App sudah live — semak perubahan secara local dulu sebelum push
- API key Groq diperlukan untuk AI personas berfungsi

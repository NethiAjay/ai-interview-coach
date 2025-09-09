# AI-Interview-Coach

AI Interview Coach: a job-specific interview practice and evaluation web app built with Streamlit + OpenAI.

Features
- Upload resume (PDF/DOCX) and paste job description.
- Auto-generate role-specific interview questions (technical + behavioral) using prompt chaining.
- Simulate interviewer persona and present one question at a time.
- Accept typed answers (or paste transcript) and evaluate them with structured feedback (score, strengths, improvements).
- Export practice session and feedback as JSON / text.

Quickstart
1. Clone or unzip this project
2. Create a venv and install requirements:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Create `.env` (see `.env.example`) and add your `OPENAI_API_KEY`.
4. Run the app:

```bash
streamlit run app.py
```

Files of interest
- `app.py` - Streamlit frontend & orchestrator
- `prompts.py` - prompt templates and few-shot examples
- `utils.py` - resume parsing, scoring helpers, export helpers
- `requirements.txt`, `Dockerfile`, `Procfile`, `.github/workflows/ci.yml`

Deployment
- Use Streamlit Cloud, Hugging Face Spaces, or Docker
- Docker command:

```bash
docker build -t ai-interview-coach .
docker run -p 8501:8501 ai-interview-coach
```

License: MIT

# Selenium Test Generator

App to generate Selenium test plans and scripts from requirements and codebase analysis.

## Features
- Model selection (OpenAI, Claude, Ollama, etc.)
- Upload requirements and codebase (zip)
- Set app context (URL, pages, credentials)
- LLM-powered user story and script generation
- Download all generated Selenium scripts as a zip

## Backend (FastAPI)

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run
```bash
uvicorn app.main:app --reload
```

- API docs: http://localhost:8000/docs

## Frontend (React + Vite)

### Setup
```bash
cd frontend
npm install
```

### Run
```bash
npm run dev
```

- App: http://localhost:5173

## Usage
1. Select a model
2. Set app context (URL, pages, username, password)
3. Upload requirements (optional) and codebase (zip)
4. Generate test plan
5. Review and download Selenium scripts (as zip)

## Notes
- Requires a running LLM backend (Ollama, OpenAI, etc.)
- Scripts are generated on-the-fly and not stored on the server
- For testing, use the provided sample.html and requirements

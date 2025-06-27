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

## Step-by-Step Workflow

1. **Model Selection**
   - **Frontend:** The user selects an AI model (e.g., GPT-4, Claude, etc.) via the `ModelSelector` component.
   - **Backend:** The selected model is stored (in memory/config) for use in all subsequent AI-driven steps.

2. **Set Application Context**
   - **Frontend:** The user fills out a form (`AppContextForm`) with:
     - App URL
     - Pages (comma-separated)
     - Username (optional)
     - Password (optional)
   - **Backend:** The `/app-context/` endpoint stores this context in a global variable (`APP_CONTEXT`). This info is used to give the AI model technical context for generating relevant user stories and test cases.

3. **Generate Test Plan**
   - **Frontend:** The user uploads a zipped codebase and (optionally) enters requirements in the `TestPlanForm`.
   - **Backend:** The `/test-plan/generate` endpoint does the heavy lifting:
     - Unzips the codebase to a temp directory.
     - **Feature Extraction:** Walks through all files, extracting features (forms, buttons, API calls, routes, etc.) using regexes (`feature_extractor.py`).
     - **Requirements Processing:** Splits the requirements into a list.
     - **AI Orchestration (`user_story.py`):**
       - a. **Match requirements to features:** Uses the AI model to link user requirements to codebase features.
       - b. **Generate user stories:** Asks the AI to generate a backlog of user stories from the requirements and app context.
       - c. **Generate stories for unmatched features:** For every feature not covered by requirements, asks the AI to generate a user story.
       - d. **Combine everything into a comprehensive test plan.**
     - Returns the generated test plan (as JSON) to the frontend.

4. **Review & Download Scripts**
   - **Frontend:** The user reviews the generated test plan in the `TestPlanReview` component.
   - (Optional): The user can download the plan or generated scripts for use in Selenium or other test automation frameworks.

## Notes
- Requires a running LLM backend (Ollama, OpenAI, etc.)
- Scripts are generated on-the-fly and not stored on the server
- For testing, use the provided sample.html and requirements

# CV Match Agent 🎯

An AI agent that analyzes the fit between your CV and a job offer — and rewrites your CV to match it, without inventing anything.

## What it does

- Extracts skills from your CV and the job description
- Calculates a semantic fit score using Claude
- Identifies what you have and what you're missing
- Rewrites your CV prioritizing relevant experience for that specific offer
- Downloads the adapted CV as a Word document

## Stack

- **Backend**: Python · LangGraph · FastAPI · Claude Haiku (Anthropic)
- **Frontend**: React · Vite
- **Package manager**: uv

## How to run it

### Backend
```bash
uv run uvicorn api:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Add your Anthropic API key to `.env`:
ANTHROPIC_API_KEY=your_key_here

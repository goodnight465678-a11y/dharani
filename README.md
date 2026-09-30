# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A
- Beginner-friendly concept explanations
- 3-question / 4-option MCQ quiz generation
- Educational text summarization
- Beginner-to-advanced learning paths

## Architecture

```text
Browser (HTML/CSS/JS)
        |
        v
FastAPI REST API
  |      |      |      |      |
 /qa  /explain /quiz /summarize /learn/recommendations
  |      |      |      |      |
  +------ Gemini client / optional LaMini local model
```

The project keeps the module names and endpoints described in the original document while adding input validation, a health endpoint, structured quiz output, error handling, automated tests, and VS Code launch settings.

## 1. Prerequisites

- Python 3.10 or newer
- A Gemini API key from Google AI Studio
- VS Code (recommended)

## 2. Create the environment

### Windows PowerShell

```powershell
cd EduGenie
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
cd EduGenie
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and put your API key in `GEMINI_API_KEY`.

Example:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
GEMINI_MODEL=gemini-2.5-flash
EXPLANATION_BACKEND=gemini
```

Never commit `.env` or expose the API key in frontend JavaScript.

## 4. Run

```bash
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

FastAPI's API documentation is available at `/docs`.

## 5. Test

With the virtual environment activated:

```bash
pytest -q
```

The tests cover the home page, health endpoint, and request validation without calling Gemini.

## 6. Test the AI features manually

- **Ask a Question:** `Which is the largest ocean?`
- **Explain:** `Explain the Pythagorean theorem for a beginner.`
- **Quiz:** paste a short educational passage.
- **Summarize:** paste a long passage.
- **Learning Path:** `I want to learn SQL from beginner to advanced.`

## 7. Optional LaMini local explanation model

The supplied documentation specifies LaMini-Flan-T5-783M for the explanation module. This implementation supports it without forcing every installation to download PyTorch and the model.

Install the optional packages:

```bash
pip install "transformers>=4.45,<5.0" "torch>=2.2"
```

Then set:

```env
EXPLANATION_BACKEND=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local-model request downloads model files. If the local model cannot load, the module attempts a Gemini fallback.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa -H "Content-Type: application/json" -d "{\"text\":\"What is photosynthesis?\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz -H "Content-Type: application/json" -d "{\"text\":\"Photosynthesis converts light energy into chemical energy in plants.\"}"
```

## Troubleshooting

**`GEMINI_API_KEY is not configured`** — create `.env` from `.env.example` and add your key.

**Gemini request failed** — verify the key, model name, internet connection, and API access/quota.

**Local explanation model is slow or uses too much memory** — use `EXPLANATION_BACKEND=gemini`, which is the default lightweight setup.

**Port 8000 is already in use** — run `python -m uvicorn main:app --reload --port 8001` and open http://127.0.0.1:8001.

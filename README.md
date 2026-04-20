# AI Resume Reviewer

Upload a PDF resume and get a structured AI review — score, strengths, weaknesses, ATS feedback, and improvement suggestions.

Built with FastAPI and Google Gemini.

---

## Stack

- **Backend** — FastAPI, PyMuPDF, Google Gemini API
- **Frontend** — HTML, CSS, Vanilla JS
- **Other** — marked.js for markdown rendering

---

## Setup

1. Clone the repo and navigate into it

```bash
git clone https://github.com/your-username/ai-resume-reviewer.git
cd ai-resume-reviewer
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add your Gemini API key — create a `.env` file:

```env
GEMINI_API_KEY=your_key_here
```

4. Start the server

```bash
uvicorn main:app --reload
```

5. Open `http://127.0.0.1:8000`

---

## Project Structure
├── main.py
├── index.html
├── .env
├── requirements.txt
└── README.md


---

## Notes

- Only PDF files are supported
- Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com)
- `.env` is gitignored — never commit your API key
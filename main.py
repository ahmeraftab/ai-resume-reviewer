from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import pdfplumber
from google import genai
import os
import io
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/review")
async def review_resume(
    file: UploadFile = File(...),
    jd: str = Form("")
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()

    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    jd_section = f"""
## Job Description Match
You have been given a job description. Compare the resume against it:
- List the key required skills/keywords FOUND in the resume
- List the key required skills/keywords MISSING from the resume
- Give a match percentage estimate
- Suggest how to tailor the resume for this role

Job Description:
{jd}
""" if jd.strip() else ""

    prompt = f"""
You are a senior technical recruiter and professional resume coach with 15+ years of experience.
Analyze the resume below and return your review using EXACTLY this markdown structure.
Do not add extra sections. Do not skip any section. Keep headings exactly as written.

## Overall Summary
Write 2-3 sentences summarizing the candidate's profile and give an overall score as: Score: X/10

## Strengths
- List exactly 4 specific strengths with brief explanations

## Weaknesses
- List exactly 4 specific weaknesses with brief explanations

## Suggestions
- List exactly 5 concrete, actionable improvements the candidate should make

## ATS Compatibility
- State whether the resume is ATS-friendly or not
- List keywords that are present
- List important keywords that are missing
- Give formatting tips specific to this resume
{jd_section}

Resume:
{text}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return {"review": response.text}
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                raise HTTPException(status_code=503, detail=str(e))
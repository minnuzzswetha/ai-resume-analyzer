import streamlit as str
import pdfplumber
from google import genai

# Paste your real API Key inside these quotes!
GOOGLE_API_KEY = "AQ.Ab8RN6JzCm_3Hj6knp7nYM9tgtLnDUFqWHNctAnDsIVUSq-Szw"

# This initializes the client using your key directly
client = genai.Client(api_key=GOOGLE_API_KEY)

str.title("🤖 AI Resume Analyzer")
str.write("Upload your resume and paste a job description to check your match score!")

# Input fields
uploaded_file = str.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = str.text_area("Paste Job Description Here")

if str.button("Analyze My Resume"):
    if uploaded_file is not None and job_description:
        with str.spinner("Analyzing..."):
            # Extract text from PDF
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = ""
                for page in pdf.pages:
                    resume_text += page.extract_text()
            
            # Ask Gemini to analyze using the stable gemini-2.5-flash model
            prompt = f"""
            Analyze the following resume against the job description.
            Provide a match percentage score, missing keywords, and brief suggestions.
            
            Job Description: {job_description}
            Resume Text: {resume_text}
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            str.subheader("Analysis Result")
            str.write(response.text)
    else:
        str.warning("Please upload a resume and paste a job description.")

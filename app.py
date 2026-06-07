import streamlit as str
import pdfplumber
import os
from google import genai

# Explicitly set the environment variable right inside the code
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6JzCm_3Hj6knp7nYM9tgtLnDUFqWHNctAnDsIVUSq-Szw"

# Initialize without explicit parameters so it pulls directly from the environment
client = genai.Client()

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
            
            # Construct analysis request
            prompt = f"""
            Analyze the following resume against the job description.
            Provide a match percentage score, missing keywords, and brief suggestions.
            
            Job Description: {job_description}
            Resume Text: {resume_text}
            """
            
            # Use the universally supported stable model target
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            str.subheader("Analysis Result")
            str.write(response.text)
    else:
        str.warning("Please upload a resume and paste a job description.")
             

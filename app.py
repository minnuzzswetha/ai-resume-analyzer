import streamlit as str
import pdfplumber
import requests

# Paste your real Gemini API Key inside these quotes!
GOOGLE_API_KEY = "AQ.Ab8RN6LNIr56RzJWEn12v2bxPOLSa6JBtqbUvkgE2LrusWQsBA"

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
            
            # Formulate the prompt
            prompt_text = f"Analyze the following resume against the job description. Provide a match percentage score, missing keywords, and brief suggestions.\n\nJob Description:\n{job_description}\n\nResume Text:\n{resume_text}"
            
            # Directly call Google's API via a secure web request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{
                    "parts": [{"text": prompt_text}]
                }]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result_json = response.json()
                try:
                    ai_analysis = result_json['candidates'][0]['content']['parts'][0]['text']
                    str.subheader("Analysis Result")
                    str.write(ai_analysis)
                except (KeyError, IndexError):
                    str.error("Failed to parse the response from the AI model.")
            else:
                str.error(f"API Error ({response.status_code}): {response.text}")
    else:        str.warning("Please upload a resume and paste a job description.")

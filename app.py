import streamlit as str
import pdfplumber
import google.generativeai as genai

# Configure your Gemini API Key
GOOGLE_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

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
            
            # Ask Gemini to analyze
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Analyze the following resume against the job description.
            Provide a match percentage score, missing keywords, and brief suggestions.
            
            Job Description: {job_description}
            Resume Text: {resume_text}
            """
            response = model.generate_content(prompt)
            str.subheader("Analysis Result")
            str.write(response.text)
    else:
        str.warning("Please upload a resume and paste a job description.")

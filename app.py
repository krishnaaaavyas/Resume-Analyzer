import streamlit as st

from utils.analyzer import calculate_similarity, analyze_skill_gap,extract_skills, load_skills
from utils.parser import extract_text_from_pdf

st.title("Resume Skill Gap Analyzer")

st.write(
    "Upload your resume and compare it against a job description."
)

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description here"
)

analyze_button = st.button("Analyze")

if analyze_button:
  if uploaded_file is None:
    st.error("Please upload a resume.")
  elif not job_description:
    st.error("Please enter a job description.")
  else:
    resume_text = extract_text_from_pdf(uploaded_file)
    similarity = calculate_similarity(resume_text,job_description)
    analysis = analyze_skill_gap(resume_text,job_description)
    st.write(similarity)
    st.write(analysis)
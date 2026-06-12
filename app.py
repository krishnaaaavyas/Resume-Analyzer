import streamlit as st

from utils.analyzer import calculate_similarity, analyze_skill_gap
from utils.parser import extract_text_from_pdf

st.title("Resume Skill Gap Analyzer")

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
    with st.spinner("Analyzing resume..."):
      resume_text = extract_text_from_pdf(uploaded_file)
      similarity = calculate_similarity(resume_text,job_description)
      analysis = analyze_skill_gap(resume_text,job_description)
      
    col1, col2 = st.columns(2)
    with col1:
      st.metric(
        "Similarity Score",
        f"{similarity}%"
            )
    with col2:
      st.metric(
          "Skill Match %",
          f'{analysis["skill_match_percentage"]}%'
      )

    st.progress(int(analysis["skill_match_percentage"]))

    st.subheader("Matched Skills")
    if analysis["matched_skills"]:
        for skill in analysis["matched_skills"]:
            st.success(skill)
    else:
      st.warning("No matching skills found.")


    st.subheader("Missing Skills")
    if analysis["missing_skills"]:
      for skill in analysis["missing_skills"]:
        st.error(skill)
    else:
      st.success("No missing skills found!")

    st.write(f"Matched {analysis['match_count']} out of {len(analysis['job_skills'])} required skills")
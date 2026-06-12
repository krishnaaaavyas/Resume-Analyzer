import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def load_skills():
    with open("data/skills.txt", "r") as f:
        skills = [line.strip() for line in f if line.strip()]
    return skills


SKILLS = load_skills()

def extract_skills(text):
    text = text.lower()
    text = text.replace("node.js", "nodejs")
    text = text.replace("react.js", "react")
    text = re.sub(r'[^\w\s+]', ' ', text)


    found_skills = set()
    words = text.split()
    for skill in SKILLS:
        if len(skill.split()) == 1:
          if skill in words:
            found_skills.add(skill)
        else:
            if skill.lower() in text:
                found_skills.add(skill)
    return found_skills


def calculate_similarity(resume_text,job_description):
    vectors = vectorizer.fit_transform([resume_text, job_description])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score*100, 2)


def analyze_skill_gap(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills
    
    if len(job_skills) > 0:
        skill_match_percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_match_percentage = 0

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "match_count": len(matched_skills),
        "skill_match_percentage": round(skill_match_percentage, 2)
    }

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data.skill_aliases import SKILL_ALIASES

vectorizer = TfidfVectorizer()


def extract_skills(text):
    text = text.lower()
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    text = re.sub(r'[^\w\s+]', ' ', text)

    found_skills = set()
    words = text.split()

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            alias = alias.lower()

            # single-word alias
            if len(alias.split()) == 1:

                if alias in words:
                    found_skills.add(skill)
                    break

            # multi-word alias
            else:
                phrase = alias.split()
                for i in range(len(words) - len(phrase) + 1):
                    if words[i:i+len(phrase)] == phrase:
                        found_skills.add(skill)
                        break

    return found_skills


def calculate_similarity(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    resume_string = " ".join(resume_skills)
    job_string = " ".join(job_skills)

    vectors = vectorizer.fit_transform(
        [resume_string, job_string]
    )

    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(score * 100, 2)


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

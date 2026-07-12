import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.skill_aliases import SKILL_ALIASES


def normalize_text(text: str) -> str:
    """Convert raw text into a consistent form for skill matching."""
    text = text.lower()
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    text = re.sub(r"[^\w\s+]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize_text(normalized_text: str) -> list[str]:
    """Split already-normalized text into individual tokens."""
    return normalized_text.split()


def contains_phrase(words: list[str], phrase_words: list[str]) -> bool:
    """Check whether all phrase words appear consecutively."""
    phrase_length = len(phrase_words)

    for index in range(len(words) - phrase_length + 1):
        if words[index:index + phrase_length] == phrase_words:
            return True

    return False


def extract_skills(text: str) -> set[str]:
    normalized_text = normalize_text(text)
    words = tokenize_text(normalized_text)

    found_skills = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_text(alias)

            if not normalized_alias:
                continue

            alias_words = tokenize_text(normalized_alias)

            if contains_phrase(words, alias_words):
                found_skills.add(canonical_skill)
                break

    return found_skills


def analyze_skill_gap(
    resume_text: str,
    job_description: str
) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills

    if job_skills:
        skill_match_percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_match_percentage = 0.0

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "match_count": len(matched_skills),
        "skill_match_percentage": round(
            skill_match_percentage,
            2
        )
    }


def calculate_similarity(
    resume_text: str,
    job_description: str
) -> float:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if not resume_skills or not job_skills:
        return 0.0

    resume_string = " ".join(sorted(resume_skills))
    job_string = " ".join(sorted(job_skills))

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(
        [resume_string, job_string]
    )

    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(score * 100, 2)
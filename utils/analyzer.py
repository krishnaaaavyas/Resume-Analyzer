import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.skill_aliases import SKILL_ALIASES
from data.confidence_rules import (
    HIGH_CONFIDENCE_PHRASES,
    MEDIUM_CONFIDENCE_PHRASES,
    LOW_CONFIDENCE_PHRASES,
    NEGATION_PHRASES,
)

CONFIDENCE_SCORES = {
    "rejected": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}

def contains_any_phrase(
    words: list[str],
    phrases: list[str]
) -> bool:
    """Check whether any configured phrase occurs consecutively."""

    for phrase in phrases:
        normalized_phrase = normalize_text(phrase)

        if not normalized_phrase:
            continue

        phrase_words = tokenize_text(normalized_phrase)

        if contains_phrase(words, phrase_words):
            return True

    return False

def determine_confidence(sentence: str) -> str:
    """Assign confidence based on the evidence present in one sentence."""

    normalized_sentence = normalize_text(sentence)
    words = tokenize_text(normalized_sentence)

    # Negation must be checked first.
    if contains_any_phrase(words, NEGATION_PHRASES):
        return "rejected"

    if contains_any_phrase(words, HIGH_CONFIDENCE_PHRASES):
        return "high"

    # Direct skill-list sentences should count as strong evidence.
    skill_section_markers = [
        "skills",
        "technical skills",
        "technologies",
        "tech stack",
    ]

    if contains_any_phrase(words, skill_section_markers):
        return "high"

    if contains_any_phrase(words, MEDIUM_CONFIDENCE_PHRASES):
        return "medium"

    if contains_any_phrase(words, LOW_CONFIDENCE_PHRASES):
        return "low"

    # A skill was explicitly mentioned, but no stronger context was found.
    return "medium"

def normalize_text(text: str) -> str:
    """Convert raw text into a consistent form for skill matching."""
    text = text.lower()
    text = text.replace("c++", "cpp")
    text = text.replace("c#", "csharp")
    text = re.sub(r"[^\w\s+]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_qualified_resume_skills(
    resume_text: str
) -> set[str]:
    evidence = extract_skill_evidence(resume_text)

    accepted_confidences = {
        "high",
        "medium",
    }

    return {
        skill
        for skill, details in evidence.items()
        if details["confidence"] in accepted_confidences
    }

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

def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

def extract_skill_evidence(text: str) -> dict:
    """
    Extract skills sentence by sentence and retain the strongest
    evidence found for each skill.
    """

    skill_evidence = {}

    for sentence in split_into_sentences(text):
        sentence_skills = extract_skills(sentence)

        if not sentence_skills:
            continue

        confidence = determine_confidence(sentence)
        confidence_score = CONFIDENCE_SCORES[confidence]

        for skill in sentence_skills:
            existing_evidence = skill_evidence.get(skill)

            should_replace = (
                existing_evidence is None
                or confidence_score
                > existing_evidence["confidence_score"]
            )

            if should_replace:
                skill_evidence[skill] = {
                    "confidence": confidence,
                    "confidence_score": confidence_score,
                    "evidence_text": sentence,
                }

    return skill_evidence

def analyze_skill_gap(
    resume_text: str,
    job_description: str
) -> dict:
    resume_evidence = extract_skill_evidence(resume_text)

    resume_skills = {
        skill
        for skill, details in resume_evidence.items()
        if details["confidence"] in {"high", "medium"}
    }

    job_skills = extract_skills(job_description)

    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills

    skill_match_percentage = (
        len(matched_skills) / len(job_skills) * 100
        if job_skills
        else 0.0
    )

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "resume_skill_evidence": resume_evidence,
        "match_count": len(matched_skills),
        "skill_match_percentage": round(
            skill_match_percentage,
            2
        ),
    }

def calculate_similarity(
    resume_text: str,
    job_description: str
) -> float:
    resume_skills = extract_qualified_resume_skills(resume_text)
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


if __name__ == "__main__":
    sample = """
    Currently learning React.
    Developed a React dashboard with authentication.
    Worked with Python during coursework.
    No experience with AWS.
    Technical Skills: Git and MongoDB.
    """

    print(extract_skill_evidence(sample))
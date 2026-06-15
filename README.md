# Resume Skill Gap Analyzer

A web application that analyzes resumes against job descriptions and identifies missing skills to help candidates improve their job fit.

## Features

* Upload Resume PDF
* Extract text from resumes
* Skill extraction and normalization
* Alias-based skill matching
* Skill gap analysis
* TF-IDF similarity scoring
* Interactive Streamlit interface

## Tech Stack

* Python
* Streamlit
* PDFPlumber
* Scikit-learn
* Regular Expressions (Regex)

## How It Works

1. Upload a resume in PDF format.
2. Paste a job description.
3. The application extracts text from both sources.
4. Skills are identified using alias-based matching.
5. Matching and missing skills are calculated.
6. A similarity score is generated using TF-IDF Vectorization and Cosine Similarity.

## Project Structure

```text
project/
│
├── app.py
├── data/
│   └── skill_aliases.py
├── utils/
│   ├── parser.py
│   └── analyzer.py
└── requirements.txt
```

## Installation

```bash
git clone <repository-url>
cd resume-skill-gap-analyzer

pip install -r requirements.txt

streamlit run app.py
```

## Screenshots

(Add screenshots here)

## Live Demo

(Add deployment link here)

## Future Improvements

* Advanced NLP-based skill extraction
* Semantic matching using embeddings
* Resume improvement recommendations
* ATS compatibility scoring

## Author

Krishna Vyas

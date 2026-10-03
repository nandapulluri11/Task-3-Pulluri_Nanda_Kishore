# Tech Stack Recommender

## Overview

Tech Stack Recommender is a content-based Python application that suggests the top three career paths from selected technical skills. It is designed to be easy to explain in an internship or capstone demonstration.

## Problem Statement and Objective

Choosing a career path from a growing list of technical skills can be difficult. This project compares a user skill profile against the skills listed for each job role and ranks the closest three roles.

## Features

- Skill onboarding from the dataset with at least three-skill validation
- Duplicate, empty, and invalid CLI input handling, plus retry and quit commands
- TF-IDF vectorization and cosine-similarity ranking
- Top-three results with role skills and direct matching-skill explanations
- A reusable recommendation service shared by the CLI and Streamlit UI
- Tests for core profiles, ranking, matching skills, and validation

## How It Works

Content-based recommendation uses the content of items—in this case, job-role skill lists—to make recommendations. TF-IDF turns skills into weighted numeric vectors: a skill receives more useful weight when it helps distinguish one role from others. Cosine similarity compares the direction of the user vector and each role vector. The app calculates one score per role, sorts scores descending, and filters the first three results (Top-N filtering).

The percentage displayed is a cosine-similarity score. It is not a probability of employment, job success, or being hired.

## Architecture

```text
USER → INPUT / ONBOARDING → DATASET → TF-IDF VECTORIZATION
     → COSINE SIMILARITY → SCORING → SORTING → TOP-3 FILTERING
     → EXPLAINABLE RESULTS → CLI or STREAMLIT UI
```

`data_loader.py` validates and loads data; `vectorizer.py` fits job-role vectors and transforms the user profile with the same vectorizer; `recommender.py` ranks roles and finds direct skill matches; `service.py` is the shared application layer; `main.py` and `app.py` provide the CLI and web UI respectively.

## Dataset

`data/raw_skills.csv` contains `job_role` and comma-separated `skills` fields. The dataset is the source of truth for all available skills and role descriptions.

## Cold Start Handling

The system cannot infer preferences for a new user without input. The onboarding screen addresses this cold-start condition by asking users to choose at least three known technical skills before recommendation.

## Project Structure

```text
data/raw_skills.csv
src/data_loader.py     # loading and validation
src/vectorizer.py      # TF-IDF creation and transformations
src/recommender.py     # similarity ranking and explanations
src/service.py         # shared application service
src/utils.py           # CLI selection validation
src/main.py            # CLI entry point
tests/test_recommender.py
app.py                 # Streamlit entry point
```

## Technology Stack

Python, pandas, scikit-learn, and Streamlit.

## Installation and Running

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python src/main.py
```

For the web interface:

```bash
streamlit run app.py
```

## Example Output

Selecting `AWS`, `Cloud`, and `Python` produces three ranked role cards. Each card shows its computed similarity score, only the selected skills that are also in that role, and the complete role-skill list.

## Testing

```bash
python -m unittest discover -s tests -v
```

The tests exercise five demo profiles, numerical scores, descending ranking, exactly three dataset roles, multi-word matching, duplicate selections, invalid selection, and insufficient selection.

## Limitations and Future Improvements

Results depend on the small curated dataset and do not account for experience, interests, education, or market demand. Future work could expand and maintain the dataset, add user-selected interests, and add accessibility or deployment configuration without changing the recommendation pipeline.

## Screenshots

Run the Streamlit app locally and capture the skill-selection and recommendation-result screens for a project presentation.

## Author

Nanda Kishore

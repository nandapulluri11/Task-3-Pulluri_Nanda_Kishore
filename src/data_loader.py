from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"job_role", "skills"}


def load_dataset(dataset_path=None):
    """Load and validate the job-role dataset."""
    path = Path(dataset_path or Path(__file__).resolve().parents[1] / "data" / "raw_skills.csv")
    if not path.is_file():
        raise FileNotFoundError("Dataset file not found.")
    try:
        data = pd.read_csv(path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        raise ValueError("Unable to load the recommendation dataset.") from error
    if data.empty:
        raise ValueError("No recommendation data is available.")
    if not REQUIRED_COLUMNS.issubset(data.columns):
        raise ValueError("Dataset must contain job_role and skills columns.")
    data = data.copy()
    data["job_role"] = data["job_role"].fillna("").astype(str).str.strip()
    data["skills"] = data["skills"].fillna("").astype(str).str.strip()
    if (data["job_role"] == "").any() or (data["skills"] == "").any():
        raise ValueError("Dataset contains an empty job role or skill field.")
    if data["job_role"].duplicated().any():
        raise ValueError("Dataset contains duplicate job roles.")
    return data


def get_available_skills(data):
    skills = set()

    for skill_list in data["skills"]:
        for skill in skill_list.split(","):
            cleaned_skill = skill.strip()
            if cleaned_skill:
                skills.add(cleaned_skill)

    return sorted(skills)

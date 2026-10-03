"""Application service shared by the CLI and Streamlit interface."""

from data_loader import get_available_skills, load_dataset
from recommender import calculate_similarity, get_matching_skills, get_top_recommendations, rank_recommendations
from vectorizer import create_vectorizer, create_vectors, transform_user_skills


class RecommendationService:
    """Fit job-role vectors once and recommend roles for selected skills."""

    def __init__(self, dataset_path=None):
        self.data = load_dataset(dataset_path)
        self.available_skills = get_available_skills(self.data)
        self.vectorizer = create_vectorizer()
        self.job_vectors = create_vectors(self.vectorizer, self.data["skills"].tolist())

    def recommend(self, selected_skills, top_n=3):
        normalized_skills = {skill.strip().casefold() for skill in selected_skills}
        if len(normalized_skills) < 3:
            raise ValueError("Please select at least 3 different skills.")
        available_skill_keys = {skill.casefold() for skill in self.available_skills}
        unknown_skills = [
            skill for skill in selected_skills
            if skill.strip().casefold() not in available_skill_keys
        ]
        if unknown_skills:
            raise ValueError("Selected skills are not available in the dataset.")
        user_vector = transform_user_skills(self.vectorizer, selected_skills)
        scores = calculate_similarity(user_vector, self.job_vectors)
        ranked = rank_recommendations(self.data["job_role"].tolist(), scores)
        results = []
        for role, score in get_top_recommendations(ranked, top_n):
            role_skills = self.data.loc[self.data["job_role"] == role, "skills"].iloc[0]
            results.append({"job_role": role, "score": float(score), "role_skills": role_skills,
                            "matching_skills": get_matching_skills(selected_skills, role_skills)})
        return results

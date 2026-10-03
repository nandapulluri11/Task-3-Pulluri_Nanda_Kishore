from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(user_vector, job_vectors):
    scores = cosine_similarity(user_vector, job_vectors)

    return scores[0]


def rank_recommendations(job_roles, scores):
    recommendations = list(zip(job_roles, scores))

    recommendations.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return recommendations


def get_top_recommendations(recommendations, top_n=3):
    return recommendations[:top_n]


def get_matching_skills(selected_skills, role_skills):
    """Return selected skills that occur in this role, preserving user order."""
    role_skill_keys = {skill.strip().casefold() for skill in role_skills.split(",")}
    matches = []
    for skill in selected_skills:
        if skill.strip().casefold() in role_skill_keys and skill not in matches:
            matches.append(skill)
    return matches

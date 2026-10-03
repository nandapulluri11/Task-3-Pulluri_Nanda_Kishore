from pathlib import Path
import sys

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from service import RecommendationService


@st.cache_resource
def get_service():
    return RecommendationService()


st.set_page_config(page_title="Tech Stack Recommender", page_icon="🧭", layout="wide")
st.title("Tech Stack Recommender")
st.write("Discover career paths using your technical skills and content-based recommendations.")
st.caption("Select at least three skills. Scores are TF-IDF cosine similarity, not employment probabilities.")

try:
    service = get_service()
    selected_skills = st.multiselect(
        "Select your technical skills", service.available_skills, key="selected_skills"
    )
    left, right = st.columns(2)
    if left.button("Get Recommendations", type="primary"):
        if len(selected_skills) < 3:
            st.error("Please select at least 3 different skills.")
        else:
            with st.spinner("Analyzing your skills..."):
                st.session_state.results = service.recommend(selected_skills)
    if right.button("Reset"):
        st.session_state.pop("results", None)
        st.session_state.pop("selected_skills", None)
        st.rerun()
    for rank, result in enumerate(st.session_state.get("results", []), start=1):
        with st.container(border=True):
            st.subheader(f"#{rank} {result['job_role']}")
            st.write(f"Similarity: **{result['score']:.2%}**")
            st.write("Matching Skills: " + (" • ".join(result["matching_skills"]) or "None"))
            st.write("Role Skills: " + result["role_skills"])
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))

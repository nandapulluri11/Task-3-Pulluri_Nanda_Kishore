from sklearn.feature_extraction.text import TfidfVectorizer


def create_vectorizer():
    return TfidfVectorizer()


def create_vectors(vectorizer, documents):
    return vectorizer.fit_transform(documents)


def transform_user_skills(vectorizer, selected_skills):
    return vectorizer.transform([" ".join(selected_skills)])

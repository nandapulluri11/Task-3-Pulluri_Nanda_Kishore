from service import RecommendationService
from utils import parse_skill_selection


def print_available_skills(available_skills):
    print("\nAvailable Skills:")
    for number, skill in enumerate(available_skills, start=1):
        print(f"{number}. {skill}")


def print_recommendations(recommendations):
    print("\n============================================")
    print("          TOP 3 CAREER PATHS")
    print("============================================")
    for rank, result in enumerate(recommendations, start=1):
        print(f"\n{rank}. {result['job_role']}")
        print(f"   Similarity: {result['score']:.2%}")
        print("\n   Matching Skills:")
        for skill in result["matching_skills"]:
            print(f"   ✓ {skill}")
        if not result["matching_skills"]:
            print("   No selected skills directly match this role.")
        print(f"\n   Role Skills:\n   {result['role_skills']}")
        print("\n--------------------------------------------")
    print("Similarity is a TF-IDF cosine-similarity score, not an employment probability.")


def run_cli():
    try:
        service = RecommendationService()
    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")
        return

    print("\n============================================")
    print("          TECH STACK RECOMMENDER")
    print("============================================")
    print("Discover career paths based on your technical skills.")

    while True:
        print_available_skills(service.available_skills)
        print("\nSelect at least 3 different skills. Enter q to quit.")
        selected_skills, error = parse_skill_selection(input("Your selection: "), service.available_skills)
        if selected_skills is None:
            print("Goodbye!")
            return
        if error:
            print(f"Error: {error}")
            continue
        print("\nSelected Skills:")
        for skill in selected_skills:
            print(f"✓ {skill}")
        print("\nAnalyzing your skills...")
        print_recommendations(service.recommend(selected_skills))
        restart = input("\nPress Enter to try again, or type q to quit: ").strip().casefold()
        if restart in {"q", "quit", "exit"}:
            print("Goodbye!")
            return


if __name__ == "__main__":
    run_cli()

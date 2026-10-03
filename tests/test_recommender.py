import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from recommender import get_matching_skills
from service import RecommendationService
from utils import parse_skill_selection


class RecommendationServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = RecommendationService()

    def test_demo_profiles_return_three_sorted_dataset_roles(self):
        profiles = [["Python", "SQL", "Machine Learning"], ["Docker", "Kubernetes", "AWS"],
                    ["HTML", "CSS", "JavaScript"], ["Python", "Cloud", "Automation"],
                    ["Java", "Kotlin", "Android"]]
        dataset_roles = set(self.service.data["job_role"])
        for profile in profiles:
            with self.subTest(profile=profile):
                results = self.service.recommend(profile)
                self.assertEqual(len(results), 3)
                self.assertTrue(all(isinstance(item["score"], float) for item in results))
                self.assertEqual([item["score"] for item in results], sorted(
                    (item["score"] for item in results), reverse=True))
                self.assertTrue(all(item["job_role"] in dataset_roles for item in results))

    def test_matching_skills_preserves_multi_word_skill(self):
        matches = get_matching_skills(["Python", "Machine Learning", "Docker"],
                                     "Python, SQL, Machine Learning, Statistics")
        self.assertEqual(matches, ["Python", "Machine Learning"])

    def test_input_validation_handles_invalid_and_duplicate_selections(self):
        skills = ["AWS", "Docker", "Python"]
        selected, error = parse_skill_selection("1 1 2 3", skills)
        self.assertEqual(selected, skills)
        self.assertIsNone(error)
        self.assertEqual(parse_skill_selection("1 9 2", skills)[1], "Please enter valid skill numbers.")
        self.assertEqual(parse_skill_selection("1 2", skills)[1], "Please select at least 3 different skills.")

    def test_unknown_skills_are_rejected_gracefully(self):
        with self.assertRaisesRegex(ValueError, "not available in the dataset"):
            self.service.recommend(["Python", "SQL", "Made Up Skill"])


if __name__ == "__main__":
    unittest.main()

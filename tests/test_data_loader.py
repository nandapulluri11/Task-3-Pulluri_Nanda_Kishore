import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_loader import load_dataset


class DataLoaderTests(unittest.TestCase):
    def test_current_dataset_has_required_valid_data(self):
        data = load_dataset()
        self.assertTrue({"job_role", "skills"}.issubset(data.columns))
        self.assertFalse(data["job_role"].duplicated().any())
        self.assertFalse((data["skills"] == "").any())

    def test_invalid_dataset_is_rejected_gracefully(self):
        with tempfile.TemporaryDirectory() as directory:
            invalid_path = Path(directory) / "invalid.csv"
            invalid_path.write_text("job_role,skills\nDeveloper,\nDeveloper,Python\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "empty job role or skill field"):
                load_dataset(invalid_path)

    def test_missing_dataset_has_clear_error(self):
        with self.assertRaisesRegex(FileNotFoundError, "Dataset file not found"):
            load_dataset("does-not-exist.csv")


if __name__ == "__main__":
    unittest.main()

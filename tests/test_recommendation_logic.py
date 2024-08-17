import unittest
from src.recommendation_logic import recommend_content

class TestRecommendationLogic(unittest.TestCase):

    def test_recommend_content(self):
        # Test case with sample interests
        interests = ["Python", "Blockchain"]
        expected_output = [
            {"title": "Recommended video for Python 1"},
            {"title": "Recommended video for Python 2"},
            {"title": "Recommended video for Blockchain 1"},
            {"title": "Recommended video for Blockchain 2"}
        ]
        result = recommend_content(interests)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

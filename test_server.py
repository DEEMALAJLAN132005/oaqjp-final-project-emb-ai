"""Flask app tests that avoid external dependency on Watson's service."""

import unittest
from unittest.mock import patch

from server import app


class TestServer(unittest.TestCase):
    """Verify homepage, successful analysis, blank input, and service errors."""

    def setUp(self):
        """Configure the Flask test client."""
        self.client = app.test_client()

    def test_homepage(self):
        """The app serves the actual web interface."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NLP - Emotion Detection", response.data)

    def test_blank_input(self):
        """Empty input shows the expected error response."""
        response = self.client.get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid text! Please try again!", response.data)

    @patch("server.emotion_detector")
    def test_valid_prediction(self, mock_detector):
        """Formatted response prints numeric scores and dominant emotion."""
        mock_detector.return_value = {
            "anger": 0.01, "disgust": 0.02, "fear": 0.03,
            "joy": 0.91, "sadness": 0.04, "dominant_emotion": "joy",
        }
        response = self.client.get("/emotionDetector?textToAnalyze=happy")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"dominant emotion is joy", response.data)

    @patch("server.emotion_detector", side_effect=ValueError("upstream failure"))
    def test_upstream_error(self, _mock_detector):
        """Errors from the external model are not passed off as a prediction."""
        response = self.client.get("/emotionDetector?textToAnalyze=happy")
        self.assertEqual(response.status_code, 502)
        self.assertIn(b"temporarily unavailable", response.data)


if __name__ == "__main__":
    unittest.main()

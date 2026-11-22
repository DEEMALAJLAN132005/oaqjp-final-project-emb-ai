"""Unit tests for the Watson NLP response formatter using mocked service data."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


def mock_prediction(winner):
    """Return the same response structure as Watson with controlled scores."""
    scores = {
        "anger": 0.01,
        "disgust": 0.02,
        "fear": 0.03,
        "joy": 0.04,
        "sadness": 0.05,
    }
    scores[winner] = 0.99
    response = Mock(status_code=200)
    response.json.return_value = {
        "emotionPredictions": [{"emotion": scores}]
    }
    return response


class TestEmotionDetection(unittest.TestCase):
    """Test score extraction, dominant emotion, and invalid input."""

    def check_emotion(self, sentence, expected):
        """Check a mock Watson response for the expected dominant score."""
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=mock_prediction(expected),
        ) as mock_post:
            result = emotion_detector(sentence)
        self.assertEqual(result["dominant_emotion"], expected)
        self.assertEqual(result[expected], 0.99)
        self.assertEqual(len(result), 6)
        self.assertEqual(
            mock_post.call_args.kwargs["json"],
            {"raw_document": {"text": sentence}},
        )

    def test_joy(self):
        """Test extraction of joy."""
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Test extraction of anger."""
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Test extraction of disgust."""
        self.check_emotion("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Test extraction of sadness."""
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Test extraction of fear."""
        self.check_emotion("I am really afraid this will happen", "fear")

    def test_blank(self):
        """Empty input does not trigger a network request."""
        with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
            result = emotion_detector(" ")
        mock_post.assert_not_called()
        self.assertTrue(all(value is None for value in result.values()))

    def test_http_400(self):
        """Watson HTTP 400 causes all-null scores and dominant emotion."""
        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=Mock(status_code=400),
        ):
            result = emotion_detector("invalid")
        self.assertTrue(all(value is None for value in result.values()))


if __name__ == "__main__":
    unittest.main()

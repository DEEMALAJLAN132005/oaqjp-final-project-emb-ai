"""Detect emotion scores using IBM Watson NLP's hosted EmotionPredict API."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def empty_emotion_result():
    """Return the specified result for invalid text."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    return result


def emotion_detector(text_to_analyse):
    """Return five emotion scores and a dominant emotion for the given text."""
    if not isinstance(text_to_analyse, str) or not text_to_analyse.strip():
        return empty_emotion_result()

    response = requests.post(
        WATSON_URL,
        json={"raw_document": {"text": text_to_analyse}},
        headers=MODEL_HEADERS,
        timeout=20,
    )
    if response.status_code == 400:
        return empty_emotion_result()
    response.raise_for_status()

    emotions = response.json()["emotionPredictions"][0]["emotion"]
    scores = {emotion: float(emotions[emotion]) for emotion in EMOTIONS}
    scores["dominant_emotion"] = max(EMOTIONS, key=scores.get)
    return scores

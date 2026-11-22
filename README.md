# Emotion Detector — IBM Skills Network Final Project

This public project implements an **Emotion Detector** using IBM Watson NLP EmotionPredict, Python, Flask, unit testing, input error handling, and static code analysis.

## Project files

- `EmotionDetection/emotion_detection.py`: IBM Watson request, five scores, dominant emotion and HTTP 400 handling.
- `EmotionDetection/__init__.py`: importable Python package.
- `server.py`: Flask web application and error handling.
- `test_emotion_detection.py`: emotion tests for five classes plus invalid inputs.
- `test_server.py`: tests of Flask routes.
- `templates/index.html`, `static/mywebscript.js`: interactive website.

## How to run

```bash
python -m pip install -r requirements.txt
python server.py
```

Open http://localhost:5000/, or run these checks:

```bash
python -m unittest discover -v
python -m pylint server.py
python -c "from EmotionDetection import emotion_detector; print(emotion_detector('I am happy today'))"
```

Tests mock IBM service responses so that pass/fail does not depend on external availability. The live model needs access to the IBM-hosted API. On each push, GitHub Actions executes real tests, runs Flask, captures real browser screenshots, and attempts an independent live-model check. The resulting logs and screenshots appear as an **emotion-detector-evidence** artifact under the workflow run.

Reference: https://www.ibm.com/docs/en/watson-libraries?topic=catalog-emotion

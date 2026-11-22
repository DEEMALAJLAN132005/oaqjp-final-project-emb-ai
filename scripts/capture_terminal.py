"""Write the genuine external Watson service response (or true error)."""

from pathlib import Path

from EmotionDetection import emotion_detector

OUT = Path("evidence")
OUT.mkdir(exist_ok=True)
text = "I am glad I finished this project."
command = "from EmotionDetection import emotion_detector; print(emotion_detector(" + repr(text) + "))"
for name in ("2b_application_creation.txt", "3b_output_formatting.txt"):
    with (OUT / name).open("w", encoding="utf-8") as handle:
        handle.write(">>> " + command + "\n")
        try:
            result = emotion_detector(text)
        except Exception as exc:
            handle.write("External Watson service unavailable: " + str(exc) + "\n")
            print(name + ": live external service unavailable")
        else:
            handle.write(str(result) + "\n")
            print(name + ": live Watson output captured")

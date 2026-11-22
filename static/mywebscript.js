// Send input to Flask and show actual Watson NLP results.
function RunSentimentAnalysis() {
    const text = document.getElementById("textToAnalyze").value;
    const result = document.getElementById("system_response");
    result.textContent = "Analyzing...";
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
            result.textContent = xhr.responseText ||
                "Unable to reach the emotion detection service.";
        }
    };
    xhr.open("GET", "/emotionDetector?textToAnalyze=" +
        encodeURIComponent(text), true);
    xhr.send();
}

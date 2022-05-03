import os
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Data Received")
    return render_template('index.html')


@app.route('/speech', methods=['GET', 'POST'])
def speech():
    transcript = ""

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="second-hexagon-337209-bdc54c2d14fc.json"

    from google.cloud import speech

    client = speech.SpeechClient()

    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        transcript = format(result.alternatives[0].transcript)
        return render_template('index.html', transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

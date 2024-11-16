import subprocess
import os
import base64
import requests

GOOGLE_API_KEY = os.getenv('stt')

def transcribe_video(video_url):
    audio_file = "temp_audio.wav"

    # Use yt-dlp to download and convert audio
    try:
        subprocess.run(
            [
                "yt-dlp",
                "-x",  # Extract audio only
                "--audio-format", "wav",  # Convert audio to WAV
                "--output", "temp_audio.%(ext)s",  # Output filename
                video_url
            ],
            check=True
        )
    except subprocess.CalledProcessError:
        return "Error: Failed to download or convert video audio."

    # Ensure the file exists before proceeding
    if not os.path.exists(audio_file):
        return "Error: Audio file not found."

    # Read the audio file and encode it in Base64
    with open(audio_file, "rb") as f:
        audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")  # Proper Base64 encoding

    # Prepare payload for Google Speech-to-Text
    url = f"https://speech.googleapis.com/v1/speech:recognize?key={GOOGLE_API_KEY}"
    config = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "en-US"
        },
        "audio": {
            "content": audio_base64
        }
    }

    # Send the transcription request
    response = requests.post(url, json=config)
    os.remove(audio_file)  # Clean up the temp file

    if response.status_code != 200:
        return f"Transcription failed. Error: {response.text}"

    result = response.json()
    transcript = " ".join([item["transcript"] for item in result.get("results", [])])
    return transcript

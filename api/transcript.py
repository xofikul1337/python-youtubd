from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to YouTube Transcript API!"})

@app.route("/transcribe", methods=["GET"])
def transcribe():
    # Get the YouTube video ID from the request
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    try:
        # Fetch transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel requires `app` or `handler`
handler = app

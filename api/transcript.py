from http import HTTPStatus
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

async def handle_errors(error):
    error_messages = {
        TranscriptsDisabled: "Subtitles are disabled for this video",
        NoTranscriptFound: "No subtitles available for this video",
        VideoUnavailable: "Video is unavailable or doesn't exist"
    }
    
    for error_type, message in error_messages.items():
        if isinstance(error, error_type):
            return {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": {
                    "error": message,
                    "success": False
                }
            }
    
    return {
        "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
        "body": {
            "error": "An unexpected error occurred",
            "success": False
        }
    }

async def main(request):
    try:
        # Get video ID from query params
        video_id = request.query.get('video_id')
        if not video_id:
            return {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "body": {
                    "error": "video_id parameter is required",
                    "success": False
                }
            }

        # Optional language parameter
        languages = request.query.get('languages', 'en').split(',')

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=languages
        )

        return {
            "statusCode": HTTPStatus.OK,
            "body": {
                "transcript": transcript,
                "success": True,
                "video_id": video_id,
                "language": languages[0]
            }
        }

    except Exception as e:
        return await handle_errors(e)

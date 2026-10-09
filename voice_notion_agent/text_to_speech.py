"""Speech-to-text via the Groq Whisper API."""

from groq import Groq

from . import config
from .logging_utils import log_stage


_client = Groq(api_key=config.GROQ_API_KEY)


def transcribe_audio(file_path: str) -> str:
    """Transcribe a local audio file using Groq's Whisper API."""

    log_stage(
        "Mic -> Groq Whisper",
        input=f"<audio file: {file_path}>"
    )

    with open(file_path, "rb") as audio_file:
        transcript = _client.audio.transcriptions.create(
            model=config.STT_MODEL,
            file=audio_file,
        )

    text = transcript.text.strip()

    log_stage(
        "Groq Whisper -> Orchestrator",
        output=text
    )

    return text
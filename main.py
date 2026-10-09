"""Main entry point: Record audio from mic, transcribe via Groq Whisper, and summarize with Groq LLM."""

import argparse
import os
import sys
from voice_notion_agent.audio_recorder import record_audio
from voice_notion_agent.speech_to_text import transcribe_audio
from voice_notion_agent.summarizer import summarize_text


def process_voice_note(audio_path: str) -> None:
    """Transcribe and summarize an audio file."""
    print("\n⏳ Transcribing audio with Groq Whisper...")
    try:
        transcript = transcribe_audio(audio_path)
    except Exception as e:
        print(f"\n❌ Error during transcription: {e}")
        return

    if not transcript:
        print("\n⚠️ No speech was detected in the recording.")
        return

    print("\n" + "=" * 50)
    print("📝 TRANSCRIBED TEXT:")
    print("=" * 50)
    print(transcript)

    print("\n⏳ Generating summary with Groq LLM...")
    try:
        summary = summarize_text(transcript)
    except Exception as e:
        print(f"\n❌ Error during summarization: {e}")
        return

    print("\n" + "=" * 50)
    print("✨ SUMMARY:")
    print("=" * 50)
    print(summary)
    print("=" * 50 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AutoOwl: Record from microphone, transcribe, and summarize speech."
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Optional path to an existing audio file instead of recording from microphone.",
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Optional recording duration in seconds (if omitted, press Enter to stop).",
    )
    args = parser.parse_args()

    if args.file:
        if not os.path.isfile(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        process_voice_note(args.file)
        return

    print("=" * 50)
    print("🦉 AutoOwl Voice Summarizer")
    print("=" * 50)
    input("Press [Enter] to start recording from your microphone...")

    audio_file = None
    try:
        audio_file = record_audio(duration=args.duration)
        process_voice_note(audio_file)
    finally:
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
            except OSError:
                pass


if __name__ == "__main__":
    main()

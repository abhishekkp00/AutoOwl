"""Summarization module using Groq LLM."""

from groq import Groq
from . import config
from .logging_utils import log_stage

_client = Groq(api_key=config.GROQ_API_KEY)


def summarize_text(text: str) -> str:
    """Summarize the given text using Groq LLM."""
    if not text or not text.strip():
        return "No speech was detected to summarize."

    log_stage("Orchestrator -> Groq LLM", input=text)

    prompt = (
        "You are an expert executive assistant. "
        "Summarize what the user spoke concisely and clearly. "
        "Highlight the key points and action items (if any).\n\n"
        f"Transcribed Speech:\n\"\"\"{text}\"\"\"\n\n"
        "Summary:"
    )

    response = _client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise summarization assistant. Provide a structured and helpful summary of spoken notes.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()

    log_stage("Groq LLM -> Orchestrator", output=summary)
    return summary

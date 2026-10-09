"""Logging utilities for voice_notion_agent."""

import logging
from typing import Any, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("voice_notion_agent")


def log_stage(
    stage: str,
    input: Optional[Any] = None,
    output: Optional[Any] = None,
    **kwargs: Any,
) -> None:
    """Log the progress and input/output of a pipeline stage."""
    parts = [f"[{stage}]"]
    if input is not None:
        parts.append(f"Input: {input}")
    if output is not None:
        parts.append(f"Output: {output}")
    for key, value in kwargs.items():
        parts.append(f"{key}: {value}")
    logger.info(" | ".join(parts))

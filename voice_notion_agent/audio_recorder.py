"""Microphone audio recording utility using ALSA arecord."""

import os
import signal
import subprocess
import tempfile
import time
from typing import Optional
from .logging_utils import log_stage


def record_audio(
    output_path: Optional[str] = None,
    duration: Optional[int] = None,
    sample_rate: int = 16000,
) -> str:
    """Record audio from the microphone into a WAV file.
    
    If duration is specified, records for that many seconds.
    If duration is None, records until the user presses Enter.
    """
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="voice_input_")
        os.close(fd)

    cmd = [
        "arecord",
        "-f", "S16_LE",
        "-r", str(sample_rate),
        "-c", "1",
        "-t", "wav",
        output_path,
    ]

    if duration is not None:
        cmd.extend(["-d", str(duration)])
        log_stage("Mic Recording", input=f"Recording for {duration} seconds to {output_path}")
        print(f"🎙️  Recording for {duration} seconds... Speak now!")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("⏹️  Recording finished.")
    else:
        log_stage("Mic Recording", input=f"Recording until user stops, saving to {output_path}")
        print("\n🎙️  Recording started... Speak into your microphone!")
        print("👉 Press [Enter] to STOP recording: ", end="", flush=True)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )

        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            # Send SIGINT so arecord writes the WAV header properly before exiting
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGINT)
                process.wait(timeout=2)
            except Exception:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except Exception:
                    pass

        print("⏹️  Recording stopped.")

    log_stage("Mic Recording", output=f"Audio saved at {output_path}")
    return output_path

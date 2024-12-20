import whisper
from urllib.parse import quote
from datetime import datetime
import os
import shutil
import time


def is_file_ready(file_path, wait_time=2):
    """Check if the file is stable (not being written to)."""
    initial_size = os.path.getsize(file_path)
    time.sleep(wait_time)
    current_size = os.path.getsize(file_path)
    return initial_size == current_size


def format_timestamp(seconds):
    """Format timestamp as HH:MM:SS."""
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def transcribe_audio(input_path, output_path, base_name, obsidian_folder):
    """Run Whisper using the Python API to transcribe the audio file."""
    try:
        # Load the Whisper model
        # switch device to mps for gpu power, run mps_test.py first.
        # Model is set to "base", run "tiny" if ur gear sucks.
        model = whisper.load_model("base", device="cpu")
        # Transcribe the audio file
        result = model.transcribe(input_path, task="transcribe", language="en", verbose=False)

        # Extract transcription segments with timestamps
        segments = result.get("segments", [])
        transcription_with_timestamps = ""

        encoded_path = quote(input_path.split('/')[-1])  # Initialize encoded_path before usage

        for segment in segments:
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"].strip()

            # Create clickable timestamp with HTTP links
            timestamp_link = f"[{start_time} --> {end_time}](http://localhost:8000/{encoded_path}#t={int(segment['start'])})"
            transcription_with_timestamps += f"{timestamp_link} {text}\n"

        # Markdown file path
        md_file_path = os.path.join(output_path, f"{base_name}.md")

        # Add a link to the original MP3 file
        audio_link = f"[Original Audio File](http://localhost:8000/{encoded_path})"

        # Ensure monthly directory exists
        current_month = datetime.now().strftime('%m-%Y')
        monthly_dir = os.path.join(obsidian_folder, current_month)
        os.makedirs(monthly_dir, exist_ok=True)

        # Write to Markdown with formatting
        content = f"""
# Transcription: {base_name}

## Overview
Transcription generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.

## Original Audio
{audio_link}

## Content
{transcription_with_timestamps}
"""
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(content)
        print(f"Markdown transcription saved: {md_file_path}")

        # Generate a timestamped filename for Obsidian Vault
        timestamped_name = datetime.now().strftime('%Y%m%d %H:%M Recording') + ".md"
        obsidian_file_path = os.path.join(monthly_dir, timestamped_name)

        # Copy and rename for Obsidian Vault
        shutil.copy(md_file_path, obsidian_file_path)
        print(f"File copied to Obsidian Vault: {obsidian_file_path}")

    except Exception as e:
        raise RuntimeError(f"Error during transcription: {e}")
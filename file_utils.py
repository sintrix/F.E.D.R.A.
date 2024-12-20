import os
from datetime import datetime


def ensure_monthly_directory_exists(base_path):
    """Ensure a directory for the current month and year exists."""
    current_month = datetime.now().strftime('%m-%Y')
    monthly_dir = os.path.join(base_path, current_month)
    os.makedirs(monthly_dir, exist_ok=True)
    return monthly_dir


def get_audio_files(folder):
    """Get a list of audio files in the folder."""
    return [f for f in os.listdir(folder) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]


def get_transcribed_files(folder):
    """Get a list of already transcribed markdown files in the folder."""
    return [os.path.splitext(f)[0] for f in os.listdir(folder) if f.lower().endswith('.md')]
import os
import signal
import time
import warnings

from file_utils import get_audio_files, get_transcribed_files
from logging_utils import setup_logging
from transcription import transcribe_audio, is_file_ready
from web_server import start_web_server

# Suppress This Warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Tired of taking notes and missing out on quantifiable career sustaining data?
# Company too cheap to buy some llamas (>(.)_(.)>
# Scurd that big bad hacker gonna gobbles up your datas: transcript locality is ground zero!
# Broke and saving money to pay dem taxes? All about that taxxx life? FREEWAREZ HUZZAH!
# Need a bio break just to find out you missed the real shit show? PFFFT!!!
# No I won't maintain, so wreck shop!

"""
FEDRA: File Encoding, Data, and Recording Archiver

Basically it takes a directory of audio files and transcribes them to markdown. 
It then hosts these audio files on a localhost web server.
The markdown has a timestamp link with the transcription.
If you click the link it opens the audiofile in your browser at the time stamp you pick.
Or you can start from the beginning.

I use Audio Hijack, you can use virtual audio cables to.. to basically record these files 
in real time while i am in meetings. After I hit stop this server chews it up and puts the md
files into my obsidian notes vault. It also created a sub directory for each month of the year.

Now I can run a search and find any meeting, anything said in that meeting, and I have an 
audiofile of what was said in that meeting. Great for training, never missing a beat, or
just remember berries of long salubrious nights with boss and crew. This shit is camp!
"""

# Just run this app in the background and it will update all the shit.
# version 5000.2024 ~SiN

# Paths
input_folder = "/Users/K/Music/Audio Hijack"
output_folder = "/Users/K/Scripts/transcription/output"
obsidian_folder = "/Users/K/Documents/Obsidian Vault/Meeting Notes"
log_file = "/Users/K/Scripts/transcription/transcribe.log"

# Graceful shutdown flag
stop_program = False


def signal_handler(_signum, _frame):
    """Handle termination signals (e.g., SIGINT, SIGTERM)."""
    global stop_program
    print("\nGracefully shutting down...")
    stop_program = True


def main():
    setup_logging(log_file)
    start_web_server(input_folder)  # Start the web server if not already running

    while not stop_program:
        try:
            audio_files = get_audio_files(input_folder)
            transcribed_files = get_transcribed_files(output_folder)

            for audio_file in audio_files:
                base_name = os.path.splitext(audio_file)[0]
                input_path = os.path.join(input_folder, audio_file)

                if base_name in transcribed_files:
                    continue

                if is_file_ready(input_path):
                    print(f"Transcribing: {audio_file}")
                    transcribe_audio(input_path, output_folder, base_name, obsidian_folder)
                    print(f"Completed transcription for: {audio_file}")
                else:
                    print(f"File is not ready yet: {audio_file}")

            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {e}")

    print("Program stopped.")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signal

    main()
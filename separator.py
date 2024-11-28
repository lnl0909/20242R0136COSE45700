import os
import subprocess
import librosa
import numpy as np
from spleeter.separator import Separator

# Step 1: Download the audio from YouTube using yt-dlp
def download_audio_yt_dlp(url):
    audio_file = "youtube_audio.mp3"  # Change to mp3 for compatibility with Spleeter
    
    # Run yt-dlp command with subprocess
    result = subprocess.run(
        ["yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", "-o", audio_file, url],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Error downloading audio:", result.stderr)
        raise RuntimeError("yt-dlp failed to download audio")
    
    return audio_file

# Enter YouTube URL
youtube_url = 'https://youtu.be/wpRywAyeZkY'  # Use clean URL without parameters
audio_path = download_audio_yt_dlp(youtube_url)

# Verify if the audio file exists
if not os.path.exists(audio_path):
    raise FileNotFoundError("The audio file was not downloaded. Check yt-dlp settings and URL validity.")

# Step 2: Separate vocals using Spleeter
separator = Separator('spleeter:2stems')
output_path = './audio_output'  # Separate output directory
separator.separate_to_file(audio_path, output_path)

# Find the path of the separated vocal file
vocal_path = os.path.join(output_path, 'youtube_audio', 'vocals.wav')
if not os.path.exists(vocal_path):
    raise FileNotFoundError("The vocal track was not found. Check Spleeter output.")

# Step 3: Detect vocal onset times with Librosa (adjusted for broader detection)
# Load the separated vocal audio
y, sr = librosa.load(vocal_path, sr=None)

# Adjusted onset detection parameters
onset_frames = librosa.onset.onset_detect(
    y=y, 
    sr=sr, 
    backtrack=True,        # Move onsets slightly backward for early detection
    pre_max=10,            # Maximum filter size before onset
    post_max=10,           # Maximum filter size after onset
    pre_avg=10,            # Average filter size before onset
    post_avg=10,           # Average filter size after onset
    delta=0.1              # Lowering the threshold for more sensitivity
)

# Convert frames to time
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

# Step 4: Save onset times to a text file
with open("vocal_onset_times_adjusted.txt", "w") as f:
    for onset_time in onset_times:
        f.write(f"{onset_time:.2f}\n")

print("Adjusted vocal onset times have been saved to 'vocal_onset_times_adjusted.txt'")
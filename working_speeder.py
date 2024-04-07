from io import BytesIO
from audiostretchy.stretch import AudioStretch
import soundfile as sf

# Define the input and output file paths
input_file = "test/set-1.wav"
output_file = "output_speedup.wav"

output_data = []
# Load the input audio file
with open(input_file, "rb") as f:
    input_data = BytesIO(f.read())

# Initialize AudioStretch object
audio_stretch = AudioStretch()

# Open the input audio file
audio_stretch.open(file=input_data, format="wav")

print("audio_stretch: ", audio_stretch)

# Define parameters
initial_ratio = 1.0   # Initial stretch ratio
increment = 0.01       # Increment for stretch ratio
final_ratio = 1.5     # Final stretch ratio
current_ratio = initial_ratio

# Loop to gradually speed up the audio
while current_ratio <= final_ratio:
    # Stretch the audio with the current ratio
    audio_stretch.stretch(
        ratio=current_ratio,
        gap_ratio=1.2,  # You can adjust this if needed
        upper_freq=333,  # You can adjust this if needed
        lower_freq=55,   # You can adjust this if needed
        buffer_ms=25,    # You can adjust this if needed
        threshold_gap_db=-40,  # You can adjust this if needed
        fast_detection=False,
        normal_detection=False,
    )
    
    # Increase the stretch ratio for the next iteration
    current_ratio += increment

# Resample the stretched audio
audio_stretch.resample(framerate=44100)  # Adjust sample rate as needed

# Save the output audio to a file
with open(output_file, "wb") as f:
    audio_stretch.save(file=f, format="wav")
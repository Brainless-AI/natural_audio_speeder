import os
import numpy as np
from io import BytesIO
import soundfile as sf
from pydub import AudioSegment
from audiostretchy.stretch import stretch_audio


# GET AUDIO SEGMENTS
def get_audio_segments(audio_path, segment_dir, speed_up_start, speed_up_end, slow_down_start, slow_down_end):

  # Load the audio
  sound = AudioSegment.from_wav(audio_path)
  for i in range(5):
    os.makedirs(os.path.join(segment_dir, str(i)), exist_ok=True)

  # 0: First section (normal speed)
  sound[:speed_up_start * 1000].export(f'{segment_dir}/0/segment-0.wav', format="wav")

  # 1: Speeding up section
  for i in range(10):
    start = (speed_up_start + (i/10)*(speed_up_end-speed_up_start)) * 1000 if not i == 0 else speed_up_start * 1000
    end = (speed_up_start + ((i+1)/10)*(speed_up_end-speed_up_start)) * 1000 if not i == 9 else speed_up_end * 1000
    sound[start:end].export(f'{segment_dir}/1/segment-{i}.wav', format="wav")

  # 2: Constant speed section
  sound[speed_up_end * 1000:slow_down_start * 1000].export(f'{segment_dir}/2/segment-0.wav', format="wav")
  
  # 3: Speeding down section
  for i in range(10):
    start = (slow_down_start + (i/10)*(slow_down_end-slow_down_start)) * 1000 if not i == 0 else slow_down_start * 1000
    end = (slow_down_start + ((i+1)/10)*(slow_down_end-slow_down_start)) * 1000 if not i == 9 else slow_down_end * 1000
    sound[start:end].export(f'{segment_dir}/3/segment-{i}.wav', format="wav")

  # 4: Last section (normal speed)
  sound[slow_down_end * 1000:].export(f'{segment_dir}/4/segment-0.wav', format="wav")

# MERGE AUDIO FILES
def merge_audio_files(input_dir, output_path):
    data = []
    
    # Iterate through each file path
    for i in range(5):
        for item in range(len(os.listdir(os.path.join(input_dir, str(i))))):
            file = os.path.join(input_dir, str(i), 'segment-'+str(item)+'.wav')
            
            # Read the audio data and sampling rate
            audio_data, samplerate = sf.read(file)
            # Append the audio data to the list
            data.append(audio_data)
    
    # Concatenate the audio data along the time axis
    merged_data = np.concatenate(data)
    
    # Write the merged audio data to a new file
    sf.write(output_path, merged_data, samplerate)

# GET PROGRESSIVE SPEEDING
def get_progressive_speeding(input_dir, processing_dir, max_speed):
    
    # 1: Speeding up section
    output_segment_dir = os.path.join(processing_dir, '1')
    os.makedirs(output_segment_dir, exist_ok=True)
    for item in range(len(os.listdir(os.path.join(input_dir, '1')))):
        file = os.path.join(input_dir, '1', 'segment-'+str(item)+'.wav')
        output_segment_path = os.path.join(output_segment_dir, 'segment-'+str(item)+'.wav')
        stretch_audio(file, output_segment_path, ratio=(1/(1+item*((max_speed-1)/10))))

    # 2: Constant speed section
    output_segment_dir = os.path.join(processing_dir, '2')
    os.makedirs(output_segment_dir, exist_ok=True)
    file = os.path.join(input_dir, '2', 'segment-0.wav')
    stretch_audio(file, output_segment_path, ratio=(1/max_speed))

    # 3: Speeding down section
    output_segment_dir = os.path.join(processing_dir, '3')
    os.makedirs(output_segment_dir, exist_ok=True)
    for item in range(len(os.listdir(os.path.join(input_dir, '3')))):
        file = os.path.join(input_dir, '3', 'segment-'+str(item)+'.wav')
        output_segment_path = os.path.join(output_segment_dir, 'segment-'+str(item)+'.wav')
        stretch_audio(file, output_segment_path, ratio=(1/(max_speed-item*((max_speed-1)/10))))

# MERGE FINAL AUDIO SEGMENTS
def merge_final_audio_segments(input_dir, output_path):
    # Initialize an empty list to hold the data of all audio files
    data = []
    audio_data, samplerate = sf.read('audio_segments/0/segment-0.wav')
    data.append(audio_data)
    
    # Iterate through each file path
    for i in range(1, 4):
        for item in range(len(os.listdir(os.path.join(input_dir, str(i))))):
            file = os.path.join(input_dir, str(i), 'segment-'+str(item)+'.wav')
            
            # Read the audio data and sampling rate
            audio_data, samplerate = sf.read(file)
            # Append the audio data to the list
            data.append(audio_data)

    audio_data, samplerate = sf.read('audio_segments/4/segment-0.wav')
    data.append(audio_data)
    
    # Concatenate the audio data along the time axis
    merged_data = np.concatenate(data)
    
    # Write the merged audio data to a new file
    sf.write(output_path, merged_data, samplerate)
    # print("Audio files merged successfully!")
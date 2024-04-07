# 1. Change the audio speed
import shutil
from utils import get_audio_segments, merge_audio_files, get_progressive_speeding, merge_final_audio_segments
def audio_speed_up(audio_path, output_path, max_speed, split_segment_length=10):
  # Define your audio file path
  segment_dir = "audio_segments"
  speed_up_start = 2
  speed_up_end = 30
  slow_down_start = 60
  slow_down_end = 80

  get_audio_segments(audio_path, segment_dir, split_segment_length, speed_up_start, speed_up_end, slow_down_start, slow_down_end)
  print('Got the Audio Segments!!!')

  processing_dir = "processing_segments"
  get_progressive_speeding(segment_dir, processing_dir, max_speed)
  print('Applied Progressive Speeding!!!')

  # Example usage:
  merge_final_audio_segments(processing_dir, output_path)
  print('Merged the final audio segments!!!')
  shutil.rmtree("audio_segments")
  shutil.rmtree("processing_segments")


if __name__ == "__main__":
  audio_path = "testing_files/set-1.wav"
  output_path = "testing_files/merged_audio.wav"
  max_speed = 1.5
  split_segment_length = 30
  audio_speed_up(audio_path, output_path, max_speed, split_segment_length)
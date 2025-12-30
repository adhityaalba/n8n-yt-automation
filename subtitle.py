import sys
import whisper
import os
import datetime

def generate_srt(video_path, output_srt_path):
    # 1. Load Model (Pakai 'small' biar agak cepat tapi akurat)
    model = whisper.load_model("small")
    print(f"Transcribing: {video_path}...")
    
    # 2. Transkrip
    result = model.transcribe(video_path)
    segments = result['segments']

    # 3. Tulis ke format .SRT
    with open(output_srt_path, 'w', encoding='utf-8') as srtFile:
        for segment in segments:
            startTime = str(0)+str(datetime.timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(datetime.timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text'].strip()
            segmentId = segment['id'] + 1
            segmentStr = f"{segmentId}\n{startTime} --> {endTime}\n{text}\n\n"
            srtFile.write(segmentStr)
    
    print(output_srt_path)

if __name__ == "__main__":
    # Argumen 1: File Video Masuk
    # Argumen 2: File SRT Keluar
    if len(sys.argv) < 3:
        print("Error: Butuh input file dan output srt")
    else:
        generate_srt(sys.argv[1], sys.argv[2])
import sys
import whisper
import json
import warnings
import os

# Matikan warning agar output bersih
warnings.filterwarnings("ignore")

def transcribe_video(file_path):
    # Cek apakah file ada
    if not os.path.exists(file_path):
        print(json.dumps({"error": "File not found"}))
        return

    # Load model Whisper
    # Opsi model: 'tiny', 'base', 'small', 'medium', 'large'
    # Kita pakai 'base' dulu biar cepat untuk testing.
    # Nanti ganti ke 'medium' kalau butuh akurasi tinggi (tapi lebih lambat).
    model = whisper.load_model("base")
    
    # Proses transkripsi
    # fp16=False disarankan jika CPU tidak support half-precision, 
    result = model.transcribe(file_path, fp16=False)
    
    # Outputkan hasil JSON ke console agar n8n bisa baca
    print(json.dumps({
        "text": result["text"],
        "segments": result["segments"]
    }))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided"}))
    else:
        video_path = sys.argv[1]
        transcribe_video(video_path)
# YT Automation Suite

Kumpulan skrip Python untuk mengotomatisasi alur kerja video YouTube, mulai dari transkripsi, pembuatan subtitle, hingga upload otomatis. Proyek ini dirancang untuk dapat diintegrasikan dengan alat otomatisasi seperti **n8n**.

## Fitur Utama

1.  **Transkripsi Video (`transcribe.py`)**  
    Menggunakan model **OpenAI Whisper** untuk mengubah suara dari video menjadi teks dalam format JSON.
2.  **Pembuatan Subtitle (`subtitle.py`)**  
    Menghasilkan file `.srt` secara otomatis menggunakan AI Whisper dengan akurasi tinggi.
3.  **Upload ke YouTube (`upload.py`)**  
    Mengunggah video langsung ke channel YouTube menggunakan YouTube Data API v3, lengkap dengan pengaturan judul, deskripsi, dan status privasi.

## Struktur Folder

-   `transcribe.py`: Skrip untuk transkripsi video ke JSON.
-   `subtitle.py`: Skrip untuk generate file subtitle SRT.
-   `upload.py`: Skrip untuk upload video ke YouTube.
-   `downloads/`: Tempat penyimpanan file video yang diunduh.
-   `output/`: Folder untuk menyimpan hasil proses.
-   `RESULT/`: Folder hasil akhir.
-   `.gitignore`: Melindungi file sensitif seperti `client_secrets.json` dan `token.json`.

## Persiapan & Instalasi

### 1. Instalasi Library
Pastikan Anda sudah menginstal Python 3.x, kemudian instal dependensi yang diperlukan:

```bash
pip install openai-whisper google-api-python-client google-auth-oauthlib google-auth-httplib2
```

*Catatan: Whisper membutuhkan `ffmpeg` terinstal di sistem Anda.*

### 2. Konfigurasi YouTube API
-   Buka [Google Cloud Console](https://console.cloud.google.com/).
-   Buat project baru dan aktifkan **YouTube Data API v3**.
-   Buat credentials OAuth 2.0 dan unduh file JSON-nya.
-   Simpan file tersebut dengan nama `client_secrets.json` di root direktori project ini.

## Cara Penggunaan

### Transkripsi Video
```bash
python transcribe.py path/to/video.mp4
```

### Membuat Subtitle (SRT)
```bash
python subtitle.py path/to/video.mp4 path/to/output.srt
```

### Upload ke YouTube
```bash
python upload.py --file "video.mp4" --title "Judul Keren" --desc "Deskripsi Video" --privacy "private"
```

## Integrasi n8n
Skrip ini dirancang agar mudah dipanggil melalui node **Execute Command** di n8n. Pastikan path file video yang diberikan sesuai dengan lokasi file di server n8n Anda.

---

**Keamanan**: Jangan pernah membagikan atau meng-upload file `client_secrets.json` dan `token.json` ke publik (seperti GitHub). File-file ini sudah masuk dalam `.gitignore`.

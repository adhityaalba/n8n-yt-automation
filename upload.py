import os
import sys
import argparse
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# --- KONFIGURASI ---
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"  # File ini akan dibuat otomatis setelah login pertama

def get_authenticated_service():
    creds = None
    # 1. Cek apakah sudah pernah login sebelumnya (token.json ada?)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # 2. Jika belum login atau token expired, minta login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Ini akan membuka Browser untuk login manual
            print("Membuka browser untuk login...")
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Simpan token biar besok gak perlu login lagi
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file_path, title, description, category_id, privacy_status):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    # Upload File
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    print(f"Mulai Upload: {title}...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"SUKSES! Video ID: {response['id']}")
    return response['id']

if __name__ == "__main__":
    # Setup argumen biar bisa dipanggil dari n8n
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path video file")
    parser.add_argument("--title", required=True, help="Judul video")
    parser.add_argument("--desc", required=True, help="Deskripsi video")
    parser.add_argument("--privacy", default="private", help="private/public")
    
    args = parser.parse_args()

    try:
        upload_video(args.file, args.title, args.desc, "22", args.privacy)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
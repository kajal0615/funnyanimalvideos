import os
import random  # <-- Ye naya import hai random title ke liye
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 1. GitHub Secrets se Data lena
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
SOURCE_FOLDER = os.environ["DRIVE_FOLDER_ID"]
DEST_FOLDER = os.environ["DONE_FOLDER_ID"]

def get_services():
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    if not creds.valid:
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
    
    drive = build('drive', 'v3', credentials=creds)
    youtube = build('youtube', 'v3', credentials=creds)
    return drive, youtube

def main():
    try:
        drive, youtube = get_services()
        print("Login Successful!")

        # 2. Drive Check Karna
        query = f"'{SOURCE_FOLDER}' in parents and mimeType contains 'video/' and trashed=false"
        results = drive.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            print("No videos found to upload.")
            return

        video = files[0]
        print(f"Found video file: {video['name']}")

        # 3. Video Download Karna
        print("Downloading video...")
        request = drive.files().get_media(fileId=video['id'])
        with open("video.mp4", "wb") as f:
            f.write(request.execute())

        # 4. RANDOM VIRAL TITLE GENERATOR (Funny Animals Edition)
        print("Generating Viral Title...")

        # Ye list hai viral titles ki, bot inme se koi ek chunega
        viral_titles_list = [
            "You Won't Believe What This Dog Did! 😂",
            "Funniest Animal Fails of The Week 🐶",
            "Try Not To Laugh Challenge: Animals 🤣",
            "Cute Cat Moments That Will Melt Your Heart 😻",
            "This Dog is Smarter Than Me! 😲",
            "Wait For The End... 😂🐶",
            "Instant Serotonin Boost: Cute Animals 💖",
            "Why Cats Are The Boss 😼",
            "Hilarious Dog Reaction! 🐕",
            "Best Animal Fails 2025 🤣",
            "This is Why I Love Dogs ❤️",
            "Baby Animals Being Cute & Funny 🍼",
            "Cat vs Dog: Who Won? 🥊",
            "The Ending is So Funny! 😂",
            "Funny Pets Doing Stupid Things 🤪",
            "Golden Retriever Being Goofy 🐕",
            "Laugh Out Loud Animal Moments 😆",
            "Animals That Think They Are Humans 🧍‍♂️",
            "Crazy Cat Moments 🐈",
            "Most Viral Animal Video Right Now 📈"
        ]

        # Random title select karna
        selected_title = random.choice(viral_titles_list)
        
        # Title ke aage main hashtags
        final_title = f"{selected_title} #Shorts #Funny"

        print(f"Selected Title: {final_title}")

        # --- VIRAL DESCRIPTION & KEYWORDS ---
        description_text = f"""
{selected_title}

Watch the funniest and cutest animal moments! 🐶🐱
Subscribe for your daily dose of laughter.

👇 SUBSCRIBE for More!
https://www.youtube.com/channel/UCUVawWRFsWOcRzcVLN8MBAg

---
#shorts #funny #animals #dogs #cats #pets #fails #humor #cute #viral #trending #comedy #wholesome #laugh #trynottolaugh
"""

        # --- TRENDING TAGS FOR SEO ---
        viral_tags = [
            'shorts', 'funny', 'animals', 'pets', 'dogs', 'cats', 'cute', 
            'viral', 'trending', 'funny animals', 'cat videos', 'dog videos', 
            'fails', 'try not to laugh', 'comedy', 'humor', 'wholesome', 'pet fails'
        ]

        body = {
            'snippet': {
                'title': final_title,  
                'description': description_text,
                'tags': viral_tags,
                'categoryId': '15' # Category 15 = Pets & Animals
            },
            'status': {
                'privacyStatus': 'public', 
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload("video.mp4", chunksize=-1, resumable=True)
        upload = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        ).execute()

        print(f"Uploaded Successfully! Video ID: {upload['id']}")

        # 5. Video Move Karna
        print("Moving video to Done folder...")
        file = drive.files().get(fileId=video['id'], fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))
        
        drive.files().update(
            fileId=video['id'],
            addParents=DEST_FOLDER,
            removeParents=previous_parents
        ).execute()
        print("Process Complete!")

    except Exception as e:
        print(f"Error aa gaya: {e}")
        exit(1)

if __name__ == "__main__":
    main()

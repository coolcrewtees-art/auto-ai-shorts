"upload_youtube.py"

import os
import json
import hashlib
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

VIDEO_FILE = "final_short.mp4"
STORY_FILE = "story.json"
HISTORY_FILE = "youtube_upload_history.json"
RESULT_FILE = "upload_result.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
IST = ZoneInfo("Asia/Kolkata")


def load_json(path, default):
    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def get_story_details():
    story = load_json(STORY_FILE, {})

    if isinstance(story, dict):
        title = (
            story.get("title")
            or story.get("headline")
            or "AI Mania Short"
        )

        description = (
            story.get("description")
            or story.get("script")
            or story.get("story")
            or "An original AI-generated short by AI Mania."
        )
    else:
        title = "AI Mania Short"
        description = str(story)

    title = str(title).strip()[:100]
    description = str(description).strip()

    if "#Shorts" not in title:
        title = f"{title} #Shorts"

    return title, description


def next_publish_time():
    """Choose the next 9 AM or 7:30 PM IST publishing slot."""
    now = datetime.now(IST)

    slots = [
        now.replace(hour=9, minute=0, second=0, microsecond=0),
        now.replace(hour=19, minute=30, second=0, microsecond=0),
    ]

    future_slots = [slot for slot in slots if slot > now]

    if future_slots:
        return future_slots[0]

    tomorrow = now + timedelta(days=1)

    return tomorrow.replace(
        hour=9, minute=0, second=0, microsecond=0
    )


def get_youtube_client():
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError(
            "Missing YouTube credentials. Check the three "
            "YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET and "
            "YOUTUBE_REFRESH_TOKEN GitHub Actions secrets."
        )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    credentials.refresh(Request())

    return build(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


def main():
    if not os.path.isfile(VIDEO_FILE):
        raise FileNotFoundError(
            f"{VIDEO_FILE} does not exist."
        )

    if os.path.getsize(VIDEO_FILE) == 0:
        raise RuntimeError("The generated video is empty.")

    video_hash = sha256_file(VIDEO_FILE)
    title, description = get_story_details()

    history = load_json(HISTORY_FILE, [])

    if not isinstance(history, list):
        raise RuntimeError(
            f"{HISTORY_FILE} must contain a JSON list."
        )

    # Prevent uploading the exact same video file twice.
    for item in history:
        if item.get("video_sha256") == video_hash:
            result = {
                "status": "skipped_duplicate",
                "reason": "This exact video file was already uploaded.",
                "previous_video_id": item.get("video_id"),
            }

            save_json(RESULT_FILE, result)
            print(json.dumps(result, indent=2))
            return

    youtube = get_youtube_client()
    publish_at = next_publish_time()

    body = {
        "snippet": {
            "title": title,
            "description": description + "\n\n#Shorts #AI",
            "tags": ["Shorts", "AI", "AI Mania"],
            "categoryId": "24",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.astimezone(
                ZoneInfo("UTC")
            ).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        VIDEO_FILE,
        mimetype="video/mp4",
        resumable=True,
        chunksize=8 * 1024 * 1024,
    )

    print(f"Uploading: {title}")
    print(f"Scheduled time (IST): {publish_at.isoformat()}")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None

    while response is None:
        status, response = request.next_chunk()

        if status:
            print(
                f"Upload progress: {int(status.progress() * 100)}%"
            )

    video_id = response["id"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    history.append({
        "video_id": video_id,
        "video_url": video_url,
        "title": title,
        "video_sha256": video_hash,
        "publish_at": body["status"]["publishAt"],
        "uploaded_at": datetime.now(IST).isoformat(),
    })

    # Save history immediately after a successful YouTube response.
    save_json(HISTORY_FILE, history)

    result = {
        "status": "scheduled",
        "video_id": video_id,
        "video_url": video_url,
        "title": title,
        "publish_at": body["status"]["publishAt"],
    }

    save_json(RESULT_FILE, result)

    print("\nSUCCESS: YouTube accepted the video.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (HttpError, Exception) as error:
        save_json(RESULT_FILE, {
            "status": "error",
            "error": str(error),
        })
        print(f"UPLOAD FAILED: {error}")
        raise
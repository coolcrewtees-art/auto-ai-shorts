import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# ============================================================
# CONFIGURATION
# ============================================================

STORY_FILE = Path("story.json")
VIDEO_FILE = Path("final_short.mp4")
HISTORY_FILE = Path("youtube_upload_history.json")
RESULT_FILE = Path("upload_result.json")

CHANNEL_NAME = "AI MANIA"
CATEGORY_ID = "24"  # Entertainment

IST = timezone(timedelta(hours=5, minutes=30))

# Publication times in Indian Standard Time
PUBLISH_SLOTS = [
    (9, 0),
    (19, 30),
]

MINIMUM_SCHEDULE_GAP = timedelta(minutes=10)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


# ============================================================
# CATEGORY METADATA
# ============================================================

CATEGORY_METADATA = {
    "indian mythology": {
        "hashtags": [
            "#Shorts", "#IndianMythology",
            "#Mythology", "#AIStory"
        ],
        "tags": [
            "indian mythology", "mythology story",
            "mythological stories"
        ],
    },
    "indian folktales": {
        "hashtags": [
            "#Shorts", "#IndianFolktales",
            "#Folktale", "#AIStory"
        ],
        "tags": [
            "indian folktales", "indian stories",
            "folk tale"
        ],
    },
    "indian legends": {
        "hashtags": [
            "#Shorts", "#IndianLegends",
            "#Legend", "#AIStory"
        ],
        "tags": [
            "indian legends", "legend story",
            "indian stories"
        ],
    },
    "supernatural": {
        "hashtags": [
            "#Shorts", "#MysteryStory",
            "#Supernatural", "#HorrorShorts",
            "#AIStory"
        ],
        "tags": [
            "mystery story", "supernatural story",
            "horror story", "dark mystery"
        ],
    },
    "mystery": {
        "hashtags": [
            "#Shorts", "#MysteryStory",
            "#Mystery", "#PlotTwist",
            "#AIStory"
        ],
        "tags": [
            "mystery story", "mystery",
            "plot twist", "unexpected ending"
        ],
    },
    "fantasy": {
        "hashtags": [
            "#Shorts", "#FantasyStory",
            "#DarkFantasy", "#AIStory"
        ],
        "tags": [
            "fantasy story", "dark fantasy",
            "fantasy shorts"
        ],
    },
    "dark fantasy": {
        "hashtags": [
            "#Shorts", "#DarkFantasy",
            "#FantasyStory", "#AIStory"
        ],
        "tags": [
            "dark fantasy", "fantasy story",
            "mystery story"
        ],
    },
    "romance": {
        "hashtags": [
            "#Shorts", "#LoveStory",
            "#RomanceStory", "#AIStory"
        ],
        "tags": [
            "love story", "romance story",
            "emotional story"
        ],
    },
    "romance drama": {
        "hashtags": [
            "#Shorts", "#LoveStory",
            "#RomanceStory", "#Drama",
            "#AIStory"
        ],
        "tags": [
            "love story", "romance story",
            "emotional story", "drama story"
        ],
    },
    "comedy": {
        "hashtags": [
            "#Shorts", "#FunnyStory",
            "#ComedyShorts", "#PlotTwist"
        ],
        "tags": [
            "funny story", "comedy story",
            "plot twist", "unexpected ending"
        ],
    },
}


# ============================================================
# GENERAL HELPERS
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_text(value):
    return clean_text(value).lower()


def load_json(path, default):
    if not path.exists():
        return default

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        print(f"WARNING: Could not read {path}; using default.")
        return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = path.with_suffix(path.suffix + ".tmp")

    with temporary_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    temporary_path.replace(path)


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


# ============================================================
# STORY HELPERS
# ============================================================

def get_story_title(story):
    for key in ("title_hook", "title", "hook_title", "name"):
        value = clean_text(story.get(key))

        if value:
            return value

    raise ValueError(
        "No story title found in story.json. "
        "Expected title_hook, title, hook_title, or name."
    )


def get_story_category(story):
    return normalize_text(story.get("category", "mystery"))


def get_story_part(story):
    try:
        return max(1, int(story.get("part", 1)))
    except (TypeError, ValueError):
        return 1


def get_story_id(story):
    return clean_text(story.get("story_id") or story.get("id"))


def get_story_fingerprint(story):
    """
    Use an existing fingerprint when supplied.
    Otherwise calculate one from the story content.
    """
    existing = clean_text(story.get("fingerprint"))

    if existing:
        return existing

    serialized = json.dumps(
        story,
        sort_keys=True,
        ensure_ascii=False,
    )

    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def get_video_description_text(story):
    """
    Extract available story text for optional context.
    """
    keys = (
        "hook", "opening", "opening_1", "opening_2",
        "conflict", "escalation", "escalation_1",
        "escalation_2", "reveal", "final",
        "final_punch", "narration", "script",
    )

    parts = []

    for key in keys:
        value = story.get(key)

        if isinstance(value, str) and clean_text(value):
            parts.append(clean_text(value))

    return " ".join(parts)


# ============================================================
# TITLE GENERATION
# ============================================================

def build_title(story):
    original = re.sub(
        r"#shorts",
        "",
        get_story_title(story),
        flags=re.IGNORECASE,
    ).strip(" .")

    category = get_story_category(story)
    part = get_story_part(story)

    # Avoid adding generic clickbait to every story.
    if part > 1:
        suffix = f" | Part {part} #Shorts"
        title = original[:100 - len(suffix)].rstrip() + suffix

    elif "mythology" in category:
        title = f"{original} | Indian Mythology #Shorts"

    elif "romance" in category:
        title = f"{original} 💔 #Shorts"

    elif "comedy" in category:
        title = f"{original} 😂 #Shorts"

    elif any(word in category for word in (
        "mystery", "supernatural", "horror", "dark fantasy"
    )):
        title = f"{original} 😨 #Shorts"

    else:
        title = f"{original} #Shorts"

    # YouTube video titles have a 100-character limit.
    if len(title) > 100:
        suffix = " #Shorts"
        title = original[:100 - len(suffix)].rstrip() + suffix

    return title


# ============================================================
# DESCRIPTION AND HASHTAGS
# ============================================================

def get_category_metadata(category):
    if category in CATEGORY_METADATA:
        return CATEGORY_METADATA[category]

    # Allow combined categories such as supernatural/mystery.
    for key, metadata in CATEGORY_METADATA.items():
        if key in category or category in key:
            return metadata

    return {
        "hashtags": [
            "#Shorts", "#AIStory",
            "#StoryTime", "#PlotTwist"
        ],
        "tags": [
            "ai story", "short story",
            "story shorts", "plot twist"
        ],
    }


def build_description(story):
    title = get_story_title(story)
    category = get_story_category(story)
    part = get_story_part(story)

    metadata = get_category_metadata(category)
    hashtags = metadata["hashtags"]

    if part > 1:
        opening = (
            f"The story continues: {title}\n"
            "Discover what happens next."
        )
    else:
        opening = (
            f"{title}\n"
            "An original short story with a twist."
        )

    description = (
        f"{opening}\n\n"
        "Watch till the end and share your interpretation "
        "in the comments.\n\n"
        f"🎬 Original AI-assisted storytelling by {CHANNEL_NAME}.\n\n"
        + " ".join(hashtags)
    )

    # Keep the description within YouTube's limit.
    return description[:5000]


def build_tags(story):
    category = get_story_category(story)
    metadata = get_category_metadata(category)

    tags = [
        CHANNEL_NAME,
        "AI story",
        "short story",
        "story shorts",
        "youtube shorts",
    ]

    tags.extend(metadata["tags"])

    # Add title words as relevant search terms.
    title = get_story_title(story)

    title_words = re.findall(r"[A-Za-z0-9]+", title.lower())

    if title_words:
        tags.append(" ".join(title_words[:8]))

    unique = []
    seen = set()
    total_chars = 0

    for tag in tags:
        tag = clean_text(tag)
        key = tag.lower()

        if not tag or key in seen:
            continue

        cost = len(tag) + (1 if unique else 0)

        if total_chars + cost > 450:
            continue

        unique.append(tag)
        seen.add(key)
        total_chars += cost

    return unique


# ============================================================
# DUPLICATE PROTECTION
# ============================================================

def make_story_key(story):
    story_id = get_story_id(story)
    fingerprint = get_story_fingerprint(story)
    part = get_story_part(story)

    if story_id:
        identity = f"id:{story_id}"
    else:
        identity = f"fingerprint:{fingerprint}"

    return f"{identity}|part:{part}"


def check_duplicate(history, story, video_hash):
    """
    Return (True, reason) for duplicates.
    Return (False, "") when it is safe to proceed.

    Supports records written by the previous uploader as well.
    """
    story_key = make_story_key(story)
    story_id = get_story_id(story)
    fingerprint = get_story_fingerprint(story)
    title = normalize_text(get_story_title(story))
    part = get_story_part(story)

    for record in history:
        if not isinstance(record, dict):
            continue

        old_hash = clean_text(record.get("video_sha256"))

        # Exact video match.
        if old_hash and old_hash == video_hash:
            return True, "This exact video file was already uploaded."

        old_key = clean_text(record.get("story_key"))

        # Match records from the earlier uploader.
        if old_key and old_key == story_key:
            return True, "This story key was already uploaded."

        old_id = clean_text(
            record.get("story_id") or record.get("id")
        )

        old_part = record.get("part", 1)

        try:
            old_part = int(old_part)
        except (TypeError, ValueError):
            old_part = 1

        if story_id and old_id == story_id and old_part == part:
            return True, "This story ID and part were already uploaded."

        old_fingerprint = clean_text(
            record.get("story_fingerprint")
        )

        if (
            fingerprint
            and old_fingerprint == fingerprint
            and old_part == part
        ):
            return True, "This story fingerprint was already uploaded."

        old_title = normalize_text(record.get("title"))

        # A title match is a useful final safeguard.
        if title and old_title == title and old_part == part:
            return True, "This story title and part were already uploaded."

    return False, ""


def mark_skip_result(story, reason):
    save_json(RESULT_FILE, {
        "status": "skipped_duplicate",
        "reason": reason,
        "title": get_story_title(story),
        "story_id": get_story_id(story),
        "time": datetime.now(timezone.utc).isoformat(),
    })


def append_upload_history(
    history,
    story,
    video_hash,
    video_id,
    title,
    publish_ist,
    publish_utc,
):
    history.append({
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "youtube_video_id": video_id,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
        "title": title,
        "story_id": get_story_id(story),
        "part": get_story_part(story),
        "story_key": make_story_key(story),
        "story_fingerprint": get_story_fingerprint(story),
        "video_sha256": video_hash,
        "category": get_story_category(story),
        "publish_time_ist": publish_ist.isoformat(),
        "publish_time_utc": publish_utc.isoformat(),
        "status": "scheduled",
    })

    # Preserve the newest 500 records.
    if len(history) > 500:
        del history[:-500]


# ============================================================
# PUBLISH SCHEDULING
# ============================================================

def next_publish_time():
    now = datetime.now(IST)
    earliest = now + MINIMUM_SCHEDULE_GAP

    candidates = []

    for hour, minute in PUBLISH_SLOTS:
        candidate = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

        if candidate > earliest:
            candidates.append(candidate)

    if candidates:
        publish_ist = min(candidates)
    else:
        tomorrow = now + timedelta(days=1)
        hour, minute = PUBLISH_SLOTS[0]

        publish_ist = tomorrow.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )

    publish_utc = publish_ist.astimezone(timezone.utc)

    return publish_ist, publish_utc


def youtube_datetime(dt):
    # YouTube API expects a UTC timestamp.
    return dt.astimezone(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


# ============================================================
# YOUTUBE CLIENT
# ============================================================

def build_youtube_client():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    missing = []

    if not client_id:
        missing.append("YOUTUBE_CLIENT_ID")

    if not client_secret:
        missing.append("YOUTUBE_CLIENT_SECRET")

    if not refresh_token:
        missing.append("YOUTUBE_REFRESH_TOKEN")

    if missing:
        raise RuntimeError(
            "Missing GitHub Actions secrets: " + ", ".join(missing)
        )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    return build(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


# ============================================================
# UPLOAD
# ============================================================

def upload_video(
    youtube,
    title,
    description,
    tags,
    publish_utc,
):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": CATEGORY_ID,
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": youtube_datetime(publish_utc),
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(VIDEO_FILE),
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024,
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None

    print("\nUploading video to YouTube...")

    while response is None:
        status, response = request.next_chunk()

        if status:
            percentage = int(status.progress() * 100)
            print(f"Upload progress: {percentage}%")

    video_id = response.get("id")

    if not video_id:
        raise RuntimeError(
            "YouTube did not return a video ID."
        )

    return video_id


# ============================================================
# MAIN
# ============================================================

def main():
    # Validate input files.
    if not STORY_FILE.exists():
        raise RuntimeError(f"{STORY_FILE} was not found.")

    if not VIDEO_FILE.exists():
        raise RuntimeError(f"{VIDEO_FILE} was not found.")

    if VIDEO_FILE.stat().st_size < 10_000:
        raise RuntimeError(
            "The video file is too small or invalid."
        )

    story = load_json(STORY_FILE, None)

    if not isinstance(story, dict) or not story:
        raise RuntimeError(
            "story.json must contain a valid JSON object."
        )

    # Build metadata before uploading.
    title = build_title(story)
    description = build_description(story)
    tags = build_tags(story)

    # Read the existing upload history.
    history = load_json(HISTORY_FILE, [])

    if not isinstance(history, list):
        raise RuntimeError(
            "Upload history is not a JSON list. "
            "Back up the history file and repair it before proceeding."
        )

    # Check for duplicates BEFORE making an API upload request.
    video_hash = sha256_file(VIDEO_FILE)

    duplicate, reason = check_duplicate(
        history,
        story,
        video_hash,
    )

    if duplicate:
        print("\nDUPLICATE DETECTED")
        print(reason)
        print("Upload skipped. No new video was uploaded.")

        mark_skip_result(story, reason)

        # IMPORTANT: returning normally makes this script exit
        # successfully instead of failing with RuntimeError.
        return

    # Calculate publication time.
    publish_ist, publish_utc = next_publish_time()

    print("\n" + "=" * 45)
    print(CHANNEL_NAME + " YOUTUBE UPLOADER")
    print("=" * 45)
    print("\nTitle:", title)
    print("\nDescription:\n", description)
    print("\nTags:", ", ".join(tags))
    print(
        "\nScheduled publication:",
        publish_ist.strftime("%d %b %Y, %I:%M %p IST"),
    )

    # Upload.
    youtube = build_youtube_client()

    video_id = upload_video(
        youtube=youtube,
        title=title,
        description=description,
        tags=tags,
        publish_utc=publish_utc,
    )

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Record the upload only after YouTube returns a video ID.
    append_upload_history(
        history=history,
        story=story,
        video_hash=video_hash,
        video_id=video_id,
        title=title,
        publish_ist=publish_ist,
        publish_utc=publish_utc,
    )

    save_json(HISTORY_FILE, history)

    save_json(RESULT_FILE, {
        "status": "scheduled",
        "video_id": video_id,
        "url": video_url,
        "title": title,
        "publish_time_ist": publish_ist.isoformat(),
        "publish_time_utc": publish_utc.isoformat(),
        "time": datetime.now(timezone.utc).isoformat(),
    })

    print("\n" + "=" * 45)
    print("UPLOAD SUCCESSFUL")
   
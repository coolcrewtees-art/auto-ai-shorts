import hashlib
import json
import os

from datetime import (
    datetime,
    timedelta,
    timezone,
)

from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# ============================================================
# FILES
# ============================================================

VIDEO_FILE = Path(
    "final_short.mp4"
)

STORY_FILE = Path(
    "story.json"
)

UPLOAD_HISTORY_FILE = Path(
    "youtube_upload_history.json"
)


# ============================================================
# YOUTUBE OAUTH
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


# ============================================================
# TIMEZONE
# ============================================================

IST = timezone(
    timedelta(
        hours=5,
        minutes=30
    )
)


# ============================================================
# PUBLISH SLOTS
#
# Morning: 9:00 AM IST
# Evening: 7:30 PM IST
# ============================================================

PUBLISH_SLOTS = [
    (9, 0),
    (19, 30),
]


# ============================================================
# LOAD HISTORY
# ============================================================

def load_history():

    if not UPLOAD_HISTORY_FILE.exists():

        return []


    try:

        data = json.loads(
            UPLOAD_HISTORY_FILE.read_text(
                encoding="utf-8"
            )
        )

        if isinstance(
            data,
            list
        ):

            return data


        return []


    except Exception as error:

        print(
            "Could not read upload history:",
            error
        )

        return []


# ============================================================
# SAVE HISTORY
# ============================================================

def save_history(
    history
):

    UPLOAD_HISTORY_FILE.write_text(
        json.dumps(
            history,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


# ============================================================
# HASH FILE
# ============================================================

def sha256_file(
    path
):

    digest = hashlib.sha256()


    with open(
        path,
        "rb"
    ) as file:

        while True:

            chunk = file.read(
                1024 * 1024
            )

            if not chunk:

                break


            digest.update(
                chunk
            )


    return digest.hexdigest()


# ============================================================
# STORY KEY
# ============================================================

def story_key(
    story
):

    fingerprint = story.get(
        "fingerprint"
    )


    if fingerprint:

        return fingerprint


    source = "|".join([
        str(
            story.get(
                "story_id",
                ""
            )
        ),

        str(
            story.get(
                "part",
                ""
            )
        ),

        story.get(
            "title_hook",
            ""
        ),
    ])


    return hashlib.sha256(
        source.encode(
            "utf-8"
        )
    ).hexdigest()


# ============================================================
# GET NEXT PUBLISH TIME
# ============================================================

def next_publish_time():

    now = datetime.now(
        IST
    )


    candidates = []


    for hour, minute in PUBLISH_SLOTS:

        candidate = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0,
        )


        # Give workflow/upload at least
        # 10 minutes before publishing.
        if candidate > (
            now
            + timedelta(
                minutes=10
            )
        ):

            candidates.append(
                candidate
            )


    # ========================================================
    # NO SLOT LEFT TODAY
    # ========================================================

    if not candidates:

        tomorrow = (
            now
            + timedelta(
                days=1
            )
        )


        target = tomorrow.replace(
            hour=PUBLISH_SLOTS[0][0],
            minute=PUBLISH_SLOTS[0][1],
            second=0,
            microsecond=0,
        )


    else:

        target = min(
            candidates
        )


    target_utc = target.astimezone(
        timezone.utc
    )


    return (
        target,
        target_utc
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # CHECK FILES
    # ========================================================

    if not VIDEO_FILE.exists():

        raise RuntimeError(
            "final_short.mp4 not found"
        )


    if not STORY_FILE.exists():

        raise RuntimeError(
            "story.json not found"
        )


    if VIDEO_FILE.stat().st_size == 0:

        raise RuntimeError(
            "final_short.mp4 is empty"
        )


    # ========================================================
    # LOAD STORY
    # ========================================================

    story = json.loads(
        STORY_FILE.read_text(
            encoding="utf-8"
        )
    )


    # ========================================================
    # LOAD HISTORY
    # ========================================================

    history = load_history()


    current_story_key = story_key(
        story
    )


    current_video_hash = sha256_file(
        VIDEO_FILE
    )


    # ========================================================
    # DUPLICATE PROTECTION
    # ========================================================

    for item in history:

        if (
            item.get(
                "story_key"
            )
            == current_story_key
        ):

            raise RuntimeError(
                "STOPPED: this story has already been uploaded."
            )


        if (
            item.get(
                "video_sha256"
            )
            == current_video_hash
        ):

            raise RuntimeError(
                "STOPPED: this exact video file has already been uploaded."
            )


    # ========================================================
    # LOAD SECRETS
    # ========================================================

    client_id = os.environ[
        "YOUTUBE_CLIENT_ID"
    ]


    client_secret = os.environ[
        "YOUTUBE_CLIENT_SECRET"
    ]


    refresh_token = os.environ[
        "YOUTUBE_REFRESH_TOKEN"
    ]


    # ========================================================
    # GOOGLE AUTH
    # ========================================================

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=(
            "https://oauth2.googleapis.com/token"
        ),
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )


    youtube = build(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


    # ========================================================
    # TITLE
    # ========================================================

    title = story.get(
        "title_hook",
        "AI Mania Story"
    ).strip()


    if "#Shorts" not in title:

        title += " #Shorts"


    title = title[:100]


    # ========================================================
    # CATEGORY
    # ========================================================

    category = (
        story.get(
            "category",
            "story"
        )
        .replace(
            "_",
            " "
        )
        .title()
    )


    # ========================================================
    # DESCRIPTION
    # ========================================================

    description = (
        f"{story.get('title_hook', '')}\n\n"
        f"A cinematic short story from AI MANIA.\n\n"
        f"Category: {category}\n\n"
        "#Shorts #AIMania #Story "
        "#Storytelling #CinematicStory "
        "#Mystery #AIStory"
    )


    # ========================================================
    # GET NEXT SLOT
    # ========================================================

    local_publish, utc_publish = (
        next_publish_time()
    )


    publish_at = (
        utc_publish
        .isoformat()
        .replace(
            "+00:00",
            "Z"
        )
    )


    # ========================================================
    # VIDEO BODY
    # ========================================================

    body = {

        "snippet": {

            "title":
                title,

            "description":
                description,

            "categoryId":
                "24",

            "tags": [
                "AI Mania",
                "shorts",
                "story",
                "storytelling",
                "AI story",
                "cinematic story",
                "mystery",
                "short story",
            ],
        },


        "status": {

            # Scheduled videos must
            # initially be private.

            "privacyStatus":
                "private",

            "publishAt":
                publish_at,

            "selfDeclaredMadeForKids":
                False,
        },
    }


    # ========================================================
    # MEDIA
    # ========================================================

    media = MediaFileUpload(
        str(
            VIDEO_FILE
        ),

        mimetype="video/mp4",

        resumable=True,
    )


    # ========================================================
    # DEBUG INFO
    # ========================================================

    print("")
    print(
        "================================="
    )

    print(
        "AI MANIA YOUTUBE UPLOAD"
    )

    print(
        "================================="
    )


    print(
        "Title:",
        title
    )


    print(
        "Publish time IST:",
        local_publish.strftime(
            "%d %B %Y %I:%M %p"
        )
    )


    print(
        "Publish time UTC:",
        publish_at
    )


    # ========================================================
    # UPLOAD REQUEST
    # ========================================================

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )


    response = None


    while response is None:

        status, response = (
            request.next_chunk()
        )


        if status:

            percent = int(
                status.progress()
                * 100
            )


            print(
                f"Upload progress: {percent}%"
            )


    video_id = response[
        "id"
    ]


    # ========================================================
    # SUCCESS
    # ========================================================

    print("")
    print(
        "================================="
    )

    print(
        "UPLOAD SUCCESSFUL"
    )

    print(
        "================================="
    )


    print(
        "Video ID:",
        video_id
    )


    print(
        "URL:",
        f"https://youtube.com/watch?v={video_id}"
    )


    # ========================================================
    # SAVE UPLOAD RECORD
    # ========================================================

    history.append({

        "story_key":
            current_story_key,

        "story_id":
            story.get(
                "story_id"
            ),

        "part":
            story.get(
                "part"
            ),

        "title":
            title,

        "video_id":
            video_id,

        "video_sha256":
            current_video_hash,

        "scheduled_publish_at":
            publish_at,

        "uploaded_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

    })


    # Keep last 500 uploads.
    save_history(
        history[-500:]
    )


if __name__ == "__main__":

    main()
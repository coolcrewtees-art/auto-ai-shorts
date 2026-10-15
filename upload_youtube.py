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
# FILES
# ============================================================

STORY_FILE = Path("story.json")
VIDEO_FILE = Path("final_short.mp4")
HISTORY_FILE = Path("youtube_upload_history.json")


# ============================================================
# YOUTUBE CREDENTIALS
# ============================================================

CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")


if not CLIENT_ID:
    raise RuntimeError("YOUTUBE_CLIENT_ID missing")

if not CLIENT_SECRET:
    raise RuntimeError("YOUTUBE_CLIENT_SECRET missing")

if not REFRESH_TOKEN:
    raise RuntimeError("YOUTUBE_REFRESH_TOKEN missing")


# ============================================================
# TIME / PUBLISHING
# ============================================================

IST = timezone(
    timedelta(
        hours=5,
        minutes=30
    )
)

PUBLISH_SLOTS = [
    (9, 0),
    (19, 30),
]

MINIMUM_SCHEDULE_GAP = timedelta(
    minutes=10
)


# ============================================================
# CHANNEL
# ============================================================

CHANNEL_NAME = "AI MANIA"

CATEGORY_ID = "24"  # Entertainment


# ============================================================
# CATEGORY HASHTAGS
# ============================================================

CATEGORY_HASHTAGS = {

    "indian mythology": [
        "#Shorts",
        "#IndianMythology",
        "#Mythology",
        "#AIStory",
        "#StoryTime",
    ],

    "indian folktales": [
        "#Shorts",
        "#IndianFolktales",
        "#Folktale",
        "#AIStory",
        "#StoryTime",
    ],

    "indian legends": [
        "#Shorts",
        "#IndianLegends",
        "#Legend",
        "#AIStory",
        "#StoryTime",
    ],

    "supernatural": [
        "#Shorts",
        "#MysteryStory",
        "#Supernatural",
        "#HorrorShorts",
        "#AIStory",
    ],

    "mystery": [
        "#Shorts",
        "#MysteryStory",
        "#Mystery",
        "#DarkStory",
        "#AIStory",
    ],

    "supernatural/mystery": [
        "#Shorts",
        "#MysteryStory",
        "#Supernatural",
        "#HorrorShorts",
        "#AIStory",
    ],

    "fantasy": [
        "#Shorts",
        "#FantasyStory",
        "#DarkFantasy",
        "#AIStory",
        "#StoryTime",
    ],

    "dark fantasy": [
        "#Shorts",
        "#DarkFantasy",
        "#FantasyStory",
        "#MysteryStory",
        "#AIStory",
    ],

    "fantasy/dark fantasy": [
        "#Shorts",
        "#DarkFantasy",
        "#FantasyStory",
        "#MysteryStory",
        "#AIStory",
    ],

    "romance": [
        "#Shorts",
        "#LoveStory",
        "#RomanceStory",
        "#Drama",
        "#AIStory",
    ],

    "romance drama": [
        "#Shorts",
        "#LoveStory",
        "#RomanceStory",
        "#Drama",
        "#AIStory",
    ],

    "comedy": [
        "#Shorts",
        "#FunnyStory",
        "#ComedyShorts",
        "#PlotTwist",
        "#AIStory",
    ],

    "comedy/absurd twist": [
        "#Shorts",
        "#FunnyStory",
        "#ComedyShorts",
        "#PlotTwist",
        "#AIStory",
    ],
}


# ============================================================
# YOUTUBE SEARCH TAGS
# ============================================================

CATEGORY_TAGS = {

    "indian mythology": [
        "indian mythology",
        "mythology story",
        "mythological stories",
        "ai story",
        "short story",
        "youtube shorts",
    ],

    "indian folktales": [
        "indian folktales",
        "indian stories",
        "folk tale",
        "ai story",
        "short story",
        "youtube shorts",
    ],

    "indian legends": [
        "indian legends",
        "legend story",
        "indian stories",
        "ai story",
        "short story",
        "youtube shorts",
    ],

    "supernatural/mystery": [
        "mystery story",
        "supernatural story",
        "horror story",
        "dark mystery",
        "ai story",
        "youtube shorts",
    ],

    "fantasy/dark fantasy": [
        "dark fantasy",
        "fantasy story",
        "mystery story",
        "ai story",
        "short story",
        "youtube shorts",
    ],

    "romance drama": [
        "love story",
        "romance story",
        "emotional story",
        "drama story",
        "ai story",
        "youtube shorts",
    ],

    "comedy/absurd twist": [
        "funny story",
        "comedy story",
        "plot twist",
        "unexpected ending",
        "ai story",
        "youtube shorts",
    ],
}


# ============================================================
# HELPERS
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value)

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def load_json(path, default):

    if not path.exists():
        return default

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        return default


def save_json(path, data):

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def sha256_file(path):

    sha = hashlib.sha256()

    with path.open("rb") as file:

        while True:

            chunk = file.read(
                1024 * 1024
            )

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()


# ============================================================
# STORY HELPERS
# ============================================================

def get_story_title(story):

    possible = [
        story.get("title_hook"),
        story.get("title"),
        story.get("hook_title"),
        story.get("name"),
    ]

    for value in possible:

        value = clean_text(value)

        if value:
            return value

    return "A Story You Won't Forget"


def get_story_category(story):

    category = clean_text(
        story.get(
            "category",
            "mystery"
        )
    )

    return category.lower()


def get_story_part(story):

    try:

        return int(
            story.get(
                "part",
                1
            )
        )

    except Exception:

        return 1


def get_story_id(story):

    value = clean_text(
        story.get("story_id")
    )

    if value:
        return value

    return clean_text(
        story.get("title_hook")
    )


def get_story_fingerprint(story):

    value = clean_text(
        story.get("fingerprint")
    )

    if value:
        return value

    base = json.dumps(
        story,
        sort_keys=True,
        ensure_ascii=False
    )

    return hashlib.sha256(
        base.encode("utf-8")
    ).hexdigest()


def get_story_text(story):

    chunks = []

    possible_keys = [
        "hook",
        "opening",
        "opening_1",
        "opening_2",
        "conflict",
        "escalation",
        "escalation_1",
        "escalation_2",
        "reveal",
        "final",
        "final_punch",
        "narration",
        "script",
    ]

    for key in possible_keys:

        value = story.get(key)

        if isinstance(
            value,
            str
        ):

            value = clean_text(value)

            if value:
                chunks.append(value)

    return " ".join(chunks)


# ============================================================
# TITLE GENERATION
# ============================================================

def strip_existing_shorts(title):

    title = re.sub(
        r"#shorts",
        "",
        title,
        flags=re.IGNORECASE
    )

    return clean_text(title)


def build_title(story):

    original = strip_existing_shorts(
        get_story_title(story)
    )

    category = get_story_category(
        story
    )

    part = get_story_part(
        story
    )


    # --------------------------------------------------------
    # PART 2
    # --------------------------------------------------------

    if part >= 2:

        candidates = [

            f"{original} 😨 | Part {part} #Shorts",

            f"{original}... It Gets Worse 😳 | Part {part} #Shorts",

            f"{original} — The Truth Is Worse 😨 #Shorts",
        ]

    # --------------------------------------------------------
    # MYSTERY / SUPERNATURAL
    # --------------------------------------------------------

    elif (
        "mystery" in category
        or "supernatural" in category
        or "dark fantasy" in category
    ):

        candidates = [

            f"{original}... Then THIS Happened 😨 #Shorts",

            f"{original} — But Something Was Wrong 😳 #Shorts",

            f"{original}... Until They Discovered the Truth 😨 #Shorts",
        ]

    # --------------------------------------------------------
    # MYTHOLOGY
    # --------------------------------------------------------

    elif "mythology" in category:

        candidates = [

            f"{original} — The Part Nobody Tells You ⚡ #Shorts",

            f"{original}... But There Was a Twist ⚡ #Shorts",

            f"{original} | Indian Mythology #Shorts",
        ]

    # --------------------------------------------------------
    # LEGEND / FOLKTALE
    # --------------------------------------------------------

    elif (
        "legend" in category
        or "folktale" in category
    ):

        candidates = [

            f"{original}... But the Ending Changes Everything 😳 #Shorts",

            f"{original} — An Indian Legend You Need to Hear #Shorts",

            f"{original} | Incredible Indian Story #Shorts",
        ]

    # --------------------------------------------------------
    # ROMANCE
    # --------------------------------------------------------

    elif "romance" in category:

        candidates = [

            f"{original}... Then Everything Changed 💔 #Shorts",

            f"{original} — A Love Story With a Twist 💔 #Shorts",

            f"{original}... But She Never Expected This 😳 #Shorts",
        ]

    # --------------------------------------------------------
    # COMEDY
    # --------------------------------------------------------

    elif "comedy" in category:

        candidates = [

            f"{original}... This Escalated Quickly 😂 #Shorts",

            f"{original} — The Ending Is Ridiculous 😂 #Shorts",

            f"{original}... Nobody Expected THAT 😂 #Shorts",
        ]

    else:

        candidates = [
            f"{original}... Then Everything Changed 😳 #Shorts"
        ]


    title = candidates[0]


    # YouTube title limit
    if len(title) > 100:

        suffix = " #Shorts"

        max_original = (
            100
            - len(suffix)
            - 3
        )

        title = (
            original[:max_original]
            .rstrip(
                " .,-"
            )
            + "..."
            + suffix
        )


    return title


# ============================================================
# DESCRIPTION GENERATION
# ============================================================

def get_description_hook(story):

    title = strip_existing_shorts(
        get_story_title(story)
    )

    category = get_story_category(
        story
    )

    part = get_story_part(
        story
    )


    if part >= 2:

        return (
            f"The story continues.\n\n"
            f"{title} takes an even darker turn — "
            f"and the truth is not what it first seemed."
        )


    if (
        "mystery" in category
        or "supernatural" in category
    ):

        return (
            f"{title} seemed impossible.\n\n"
            f"But the deeper they looked, "
            f"the stranger the truth became."
        )


    if "dark fantasy" in category:

        return (
            f"{title} begins like a legend.\n\n"
            f"Then something impossible changes everything."
        )


    if "mythology" in category:

        return (
            f"{title} hides a story of power, fate and consequence.\n\n"
            f"Watch till the end for the full twist."
        )


    if (
        "folktale" in category
        or "legend" in category
    ):

        return (
            f"{title} sounds like an ordinary tale at first.\n\n"
            f"The ending tells a very different story."
        )


    if "romance" in category:

        return (
            f"{title} begins with a simple connection.\n\n"
            f"What happens next changes everything."
        )


    if "comedy" in category:

        return (
            f"{title} starts normally enough.\n\n"
            f"Then things get completely out of control."
        )


    return (
        f"{title} begins normally.\n\n"
        f"Then everything changes."
    )


def get_hashtags(category):

    category = category.lower()


    if category in CATEGORY_HASHTAGS:

        return CATEGORY_HASHTAGS[
            category
        ]


    for key, value in CATEGORY_HASHTAGS.items():

        if (
            key in category
            or category in key
        ):

            return value


    return [
        "#Shorts",
        "#AIStory",
        "#StoryTime",
        "#PlotTwist",
        "#MysteryStory",
    ]


def build_description(story):

    category = get_story_category(
        story
    )

    hook = get_description_hook(
        story
    )

    hashtags = get_hashtags(
        category
    )


    lines = [

        hook,

        "",

        "Watch till the end for the twist.",

        "",

        "🎬 Original cinematic AI story by AI MANIA.",

        "",

        " ".join(
            hashtags
        ),
    ]


    description = "\n".join(
        lines
    )


    return description[:5000]


# ============================================================
# YOUTUBE TAG GENERATION
# ============================================================

def build_tags(story):

    category = get_story_category(
        story
    )

    result = [
        "AI MANIA",
        "AI story",
        "short story",
        "story shorts",
        "youtube shorts",
        "shorts",
        "plot twist",
    ]


    if category in CATEGORY_TAGS:

        result.extend(
            CATEGORY_TAGS[
                category
            ]
        )

    else:

        for key, values in CATEGORY_TAGS.items():

            if (
                key in category
                or category in key
            ):

                result.extend(
                    values
                )

                break


    unique = []

    seen = set()


    for tag in result:

        tag = clean_text(tag)

        lower = tag.lower()

        if (
            tag
            and lower not in seen
        ):

            unique.append(tag)

            seen.add(lower)


    # Stay safely within YouTube's total tag limit
    final = []

    total = 0


    for tag in unique:

        extra = len(tag) + 1

        if total + extra > 450:
            break

        final.append(tag)

        total += extra


    return final


# ============================================================
# PUBLISH TIME
# ============================================================

def next_publish_time():

    now = datetime.now(
        IST
    )

    minimum_time = (
        now
        + MINIMUM_SCHEDULE_GAP
    )


    candidates = []


    for hour, minute in PUBLISH_SLOTS:

        candidate = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if candidate > minimum_time:

            candidates.append(
                candidate
            )


    if candidates:

        publish_ist = min(
            candidates
        )

    else:

        tomorrow = (
            now
            + timedelta(days=1)
        )

        first_hour, first_minute = (
            PUBLISH_SLOTS[0]
        )

        publish_ist = tomorrow.replace(
            hour=first_hour,
            minute=first_minute,
            second=0,
            microsecond=0
        )


    publish_utc = publish_ist.astimezone(
        timezone.utc
    )


    return (
        publish_ist,
        publish_utc
    )


def youtube_datetime(dt):

    return (
        dt.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        + "Z"
    )


# ============================================================
# DUPLICATE PROTECTION
# ============================================================

def make_story_key(story):

    story_id = get_story_id(
        story
    )

    part = get_story_part(
        story
    )

    fingerprint = get_story_fingerprint(
        story
    )

    return (
        f"{story_id}"
        f"|part={part}"
        f"|{fingerprint}"
    )


def check_duplicate(
    history,
    story_key,
    video_hash
):

    for record in history:

        old_key = clean_text(
            record.get(
                "story_key"
            )
        )

        old_hash = clean_text(
            record.get(
                "video_sha256"
            )
        )


        if (
            old_key
            and old_key == story_key
        ):

            raise RuntimeError(
                "Duplicate upload blocked: "
                "this story has already been uploaded."
            )


        if (
            old_hash
            and old_hash == video_hash
        ):

            raise RuntimeError(
                "Duplicate upload blocked: "
                "this exact video file has already been uploaded."
            )


# ============================================================
# YOUTUBE CLIENT
# ============================================================

def build_youtube_client():

    credentials = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=[
            "https://www.googleapis.com/auth/youtube.upload"
        ],
    )


    youtube = build(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


    return youtube


# ============================================================
# UPLOAD
# ============================================================

def upload_video(
    youtube,
    story,
    title,
    description,
    tags,
    publish_at_utc,
):

    body = {

        "snippet": {

            "title":
                title,

            "description":
                description,

            "tags":
                tags,

            "categoryId":
                CATEGORY_ID,
        },

        "status": {

            "privacyStatus":
                "private",

            "publishAt":
                youtube_datetime(
                    publish_at_utc
                ),

            "selfDeclaredMadeForKids":
                False,
        },
    }


    media = MediaFileUpload(
        str(VIDEO_FILE),
        mimetype="video/mp4",
        resumable=True,
        chunksize=-1,
    )


    request = (
        youtube
        .videos()
        .insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
    )


    print("")
    print(
        "Uploading video to YouTube..."
    )


    response = None


    while response is None:

        status, response = (
            request.next_chunk()
        )


        if status:

            percentage = int(
                status.progress()
                * 100
            )

            print(
                f"Upload progress: "
                f"{percentage}%"
            )


    video_id = response.get(
        "id"
    )


    if not video_id:

        raise RuntimeError(
            "YouTube upload completed "
            "but no video ID was returned."
        )


    return video_id


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # VALIDATE FILES
    # --------------------------------------------------------

    if not STORY_FILE.exists():

        raise RuntimeError(
            "story.json not found"
        )


    if not VIDEO_FILE.exists():

        raise RuntimeError(
            "final_short.mp4 not found"
        )


    if VIDEO_FILE.stat().st_size < 10000:

        raise RuntimeError(
            "final_short.mp4 looks invalid "
            "or too small."
        )


    # --------------------------------------------------------
    # LOAD STORY
    # --------------------------------------------------------

    story = load_json(
        STORY_FILE,
        {}
    )


    if not story:

        raise RuntimeError(
            "story.json is empty "
            "or invalid."
        )


    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    title = build_title(
        story
    )

    description = build_description(
        story
    )

    tags = build_tags(
        story
    )


    # --------------------------------------------------------
    # DUPLICATE CHECK
    # --------------------------------------------------------

    video_hash = sha256_file(
        VIDEO_FILE
    )

    story_key = make_story_key(
        story
    )


    history = load_json(
        HISTORY_FILE,
        []
    )


    if not isinstance(
        history,
        list
    ):

        history = []


    check_duplicate(
        history,
        story_key,
        video_hash
    )


    # --------------------------------------------------------
    # SCHEDULE TIME
    # --------------------------------------------------------

    publish_ist, publish_utc = (
        next_publish_time()
    )


    print("")
    print(
        "========================================"
    )

    print(
        "AI MANIA YOUTUBE UPLOADER"
    )

    print(
        "========================================"
    )

    print("")
    print(
        "Title:"
    )

    print(
        title
    )

    print("")
    print(
        "Description:"
    )

    print(
        description
    )

    print("")
    print(
        "Tags:"
    )

    print(
        ", ".join(
            tags
        )
    )

    print("")
    print(
        "Publish time IST:"
    )

    print(
        publish_ist.strftime(
            "%Y-%m-%d %I:%M %p"
        )
    )

    print("")
    print(
        "Publish time UTC:"
    )

    print(
        youtube_datetime(
            publish_utc
        )
    )


    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    youtube = build_youtube_client()


    video_id = upload_video(
        youtube=youtube,
        story=story,
        title=title,
        description=description,
        tags=tags,
        publish_at_utc=publish_utc,
    )


    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    record = {

        "uploaded_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "youtube_video_id":
            video_id,

        "youtube_url":
            (
                "https://www.youtube.com/watch?v="
                + video_id
            ),

        "title":
            title,

        "category":
            get_story_category(
                story
            ),

        "story_id":
            get_story_id(
                story
            ),

        "part":
            get_story_part(
                story
            ),

        "story_key":
            story_key,

        "story_fingerprint":
            get_story_fingerprint(
                story
            ),

        "video_sha256":
            video_hash,

        "publish_time_ist":
            publish_ist.isoformat(),

        "publish_time_utc":
            publish_utc.isoformat(),

        "status":
            "scheduled",
    }


    history.append(
        record
    )


    # Keep history reasonably sized
    if len(history) > 500:

        history = history[-500:]


    save_json(
        HISTORY_FILE,
        history
    )


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print("")
    print(
        "========================================"
    )

    print(
        "UPLOAD SUCCESSFUL"
    )

    print(
        "========================================"
    )

    print("")
    print(
        "Video ID:",
        video_id
    )

    print(
        "Scheduled:",
        publish_ist.strftime(
            "%d %b %Y, %I:%M %p IST"
        )
    )

    print(
        "URL:",
        (
            "https://www.youtube.com/watch?v="
            + video_id
        )
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
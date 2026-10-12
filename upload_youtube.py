import json
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


VIDEO_FILE = Path("final_short.mp4")
STORY_FILE = Path("story.json")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


def main():

    # --------------------------------------------------------
    # CHECK FILES
    # --------------------------------------------------------

    if not VIDEO_FILE.exists():
        raise FileNotFoundError(
            "final_short.mp4 not found"
        )

    if not STORY_FILE.exists():
        raise FileNotFoundError(
            "story.json not found"
        )


    # --------------------------------------------------------
    # LOAD STORY
    # --------------------------------------------------------

    story = json.loads(
        STORY_FILE.read_text(
            encoding="utf-8"
        )
    )


    # --------------------------------------------------------
    # LOAD GITHUB SECRETS
    # --------------------------------------------------------

    client_id = os.environ[
        "YOUTUBE_CLIENT_ID"
    ]

    client_secret = os.environ[
        "YOUTUBE_CLIENT_SECRET"
    ]

    refresh_token = os.environ[
        "YOUTUBE_REFRESH_TOKEN"
    ]


    # --------------------------------------------------------
    # GOOGLE AUTH
    # --------------------------------------------------------

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
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


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = story.get(
        "title_hook",
        "An Incredible Story"
    ).strip()

    # YouTube title limit
    title = title[:95]

    if "#Shorts" not in title:
        title += " #Shorts"


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    category = story.get(
        "category",
        "story"
    )

    description = (
        f"{story.get('title_hook', '')}\n\n"
        f"A cinematic short story.\n\n"
        f"Category: {category.replace('_', ' ').title()}\n\n"
        "#Shorts #Story #Storytelling "
        "#AIStory #Mystery #Cinematic"
    )


    # --------------------------------------------------------
    # VIDEO METADATA
    # --------------------------------------------------------

    body = {

        "snippet": {

            "title": title,

            "description": description,

            "categoryId": "24",

            "tags": [
                "shorts",
                "story",
                "storytelling",
                "cinematic story",
                "AI story",
                "mystery",
                "short story",
            ],
        },

        "status": {

            # FIRST TEST = PRIVATE
            "privacyStatus": "private",

            "selfDeclaredMadeForKids": False,
        },
    }


    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    media = MediaFileUpload(
        str(VIDEO_FILE),
        mimetype="video/mp4",
        resumable=True,
        chunksize=-1,
    )


    print("")
    print("================================")
    print("UPLOADING TO YOUTUBE")
    print("================================")

    print("Title:", title)
    print("Privacy: PRIVATE")


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
                status.progress() * 100
            )

            print(
                f"Upload progress: {percent}%"
            )


    video_id = response["id"]


    print("")
    print("==============================")
    print("YOUTUBE UPLOAD SUCCESSFUL")
    print("==============================")

    print(
        "Video ID:",
        video_id
    )

    print(
        "URL:",
        f"https://youtube.com/watch?v={video_id}"
    )


if __name__ == "__main__":
    main()
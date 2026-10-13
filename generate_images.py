import base64
import json
import os
import re
import time
from pathlib import Path

import requests


# ============================================================
# FILES
# ============================================================

SCENES_FILE = Path("scenes.json")

OUTPUT_DIR = Path("images")


# ============================================================
# CLOUDFLARE
# ============================================================

ACCOUNT_ID = os.environ.get(
    "CLOUDFLARE_ACCOUNT_ID"
)

API_TOKEN = os.environ.get(
    "CLOUDFLARE_API_TOKEN"
)


MODEL = "@cf/black-forest-labs/flux-1-schnell"


# ============================================================
# VALIDATION
# ============================================================

if not ACCOUNT_ID:
    raise RuntimeError(
        "CLOUDFLARE_ACCOUNT_ID missing"
    )

if not API_TOKEN:
    raise RuntimeError(
        "CLOUDFLARE_API_TOKEN missing"
    )


API_URL = (
    "https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL}"
)


HEADERS = {
    "Authorization":
        f"Bearer {API_TOKEN}",

    "Content-Type":
        "application/json",
}


# ============================================================
# HELPERS
# ============================================================

def has_any(
    text,
    words
):
    lower = text.lower()

    return any(
        word in lower
        for word in words
    )


def scene_is_object_heavy(
    narration
):

    objects = [
        "mirror",
        "door",
        "phone",
        "message",
        "train",
        "station",
        "room",
        "palace",
        "portrait",
        "painting",
        "clock",
        "letter",
        "throne",
        "window",
        "bed",
        "bottle",
        "wall",
        "guards",
        "relatives",
        "family",
        "market",
        "fire",
        "flames",
    ]

    return has_any(
        narration,
        objects
    )


def scene_needs_character(
    narration
):

    lower = (
        " "
        + narration.lower()
        + " "
    )

    words = [
        " he ",
        " him ",
        " his ",
        " she ",
        " her ",
        " prince ",
        " king ",
        " traveler ",
        " warrior ",
        " aarav ",
        " rohan ",
        " dev ",
        " kabir ",
    ]

    return any(
        word in lower
        for word in words
    )


# ============================================================
# PROMPT STRATEGIES
# ============================================================

def prompt_attempt_one(
    scene
):

    return scene.get(
        "prompt",
        ""
    )


def prompt_attempt_two(
    scene
):

    narration = scene.get(
        "narration",
        ""
    )

    beat = scene.get(
        "beat",
        ""
    )

    original = scene.get(
        "prompt",
        ""
    )

    return f"""
Photorealistic cinematic movie still, vertical 9:16.

Create a WIDE ENVIRONMENTAL STORY SHOT.

Narrated event:
{narration}

Scene beat:
{beat}

Important:
The exact physical event above must be visibly happening.

Do not create a portrait.
Do not create a centered face.
Do not create a head-and-shoulders shot.
Do not have the character staring into camera.

Show the environment, objects, action, secondary characters,
architecture and supernatural event clearly.

The main character should occupy less than one third of the frame
unless absolutely necessary.

Use cinematic staging with depth:
foreground, subject/action, background.

Prefer:
wide shot,
medium-wide shot,
over-the-shoulder shot,
object-dominant composition,
action composition.

Avoid:
close-up face,
beauty portrait,
fashion portrait,
static pose,
symmetrical headshot.

No text.
No watermark.
No subtitles.

Additional original scene context:
{original}
""".strip()[:2048]


def prompt_attempt_three(
    scene
):

    narration = scene.get(
        "narration",
        ""
    )

    beat = scene.get(
        "beat",
        ""
    )

    object_heavy = scene_is_object_heavy(
        narration
    )

    needs_character = scene_needs_character(
        narration
    )


    if object_heavy:

        focus_rule = (
            "The important object/location/event must dominate the frame. "
            "The protagonist is secondary."
        )

    else:

        focus_rule = (
            "Show the physical action and environment, not a posed character."
        )


    if not needs_character:

        character_rule = (
            "Do NOT show the protagonist at all. "
            "Use only the location, object, secondary characters "
            "or supernatural event."
        )

    else:

        character_rule = (
            "If a protagonist is visible, show them from the side, back, "
            "three-quarter angle, or small in frame while performing the action. "
            "Never use a portrait composition."
        )


    return f"""
Cinematic vertical 9:16 storytelling frame.

ABSOLUTE VISUAL PRIORITY:
{narration}

{focus_rule}

{character_rule}

Composition:
environment-dominant,
action-dominant,
object-dominant,
wide or medium-wide,
cinematic depth,
dramatic lighting,
realistic anatomy,
photorealistic.

The viewer must understand the event with sound muted.

Do NOT produce:
portrait photography,
headshot,
close-up face,
person staring at camera,
fashion pose,
centered face,
empty generic character shot.

Scene type:
{beat}

No text.
No subtitles.
No logo.
No watermark.
""".strip()[:2048]


# ============================================================
# API CALL
# ============================================================

def call_cloudflare(
    prompt
):

    payload = {
        "prompt":
            prompt[:2048],

        "steps":
            4,
    }


    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=120,
    )


    # ========================================================
    # QUOTA EXHAUSTION
    # ========================================================

    if response.status_code == 429:

        text = response.text

        if (
            "daily free allocation"
            in text.lower()
            or '"code":4006'
            in text
        ):

            raise RuntimeError(
                "CLOUDFLARE_DAILY_QUOTA_EXHAUSTED"
            )


    if response.status_code != 200:

        raise RuntimeError(
            f"Cloudflare error "
            f"{response.status_code}: "
            f"{response.text}"
        )


    data = response.json()


    if not data.get(
        "success",
        False
    ):

        raise RuntimeError(
            "Cloudflare returned success=false: "
            + json.dumps(
                data
            )
        )


    image_base64 = (
        data
        .get(
            "result",
            {}
        )
        .get(
            "image"
        )
    )


    if not image_base64:

        raise RuntimeError(
            "Cloudflare returned no image data"
        )


    return base64.b64decode(
        image_base64
    )


# ============================================================
# GENERATE ONE IMAGE
# ============================================================

def generate_scene_image(
    scene,
    index
):

    prompts = [
        prompt_attempt_one(
            scene
        ),

        prompt_attempt_two(
            scene
        ),

        prompt_attempt_three(
            scene
        ),
    ]


    last_error = None


    for attempt_number, prompt in enumerate(
        prompts,
        start=1
    ):

        print("")
        print(
            f"Scene {index} - attempt "
            f"{attempt_number}/3"
        )


        try:

            image_bytes = call_cloudflare(
                prompt
            )


            output_file = (
                OUTPUT_DIR
                / f"scene_{index:02d}.jpg"
            )


            output_file.write_bytes(
                image_bytes
            )


            if (
                not output_file.exists()
                or output_file.stat().st_size < 1000
            ):

                raise RuntimeError(
                    "Generated image file is invalid"
                )


            print(
                "Saved:",
                output_file
            )


            return


        except RuntimeError as error:

            last_error = error


            if (
                str(error)
                == "CLOUDFLARE_DAILY_QUOTA_EXHAUSTED"
            ):

                print("")
                print(
                    "Cloudflare daily free quota exhausted."
                )

                print(
                    "Stopping immediately to avoid useless retries."
                )

                raise


            print(
                "Attempt failed:",
                error
            )


            if attempt_number < 3:

                time.sleep(
                    2
                )


    raise RuntimeError(
        f"Scene {index} failed after 3 different prompt strategies. "
        f"Last error: {last_error}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    if not SCENES_FILE.exists():

        raise RuntimeError(
            "scenes.json not found"
        )


    scenes = json.loads(
        SCENES_FILE.read_text(
            encoding="utf-8"
        )
    )


    if not isinstance(
        scenes,
        list
    ):

        raise RuntimeError(
            "scenes.json must contain a list"
        )


    if len(scenes) != 8:

        raise RuntimeError(
            f"Expected 8 scenes, got {len(scenes)}"
        )


    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    # ========================================================
    # CLEAR OLD IMAGES
    # ========================================================

    for old_file in OUTPUT_DIR.glob(
        "*.jpg"
    ):

        old_file.unlink()


    print("")
    print(
        "================================="
    )

    print(
        "AI MANIA IMAGE GENERATOR"
    )

    print(
        "================================="
    )

    print(
        "Scenes:",
        len(scenes)
    )


    # ========================================================
    # GENERATE
    # ========================================================

    for index, scene in enumerate(
        scenes
    ):

        generate_scene_image(
            scene,
            index
        )


    # ========================================================
    # FINAL VALIDATION
    # ========================================================

    generated = list(
        OUTPUT_DIR.glob(
            "*.jpg"
        )
    )


    print("")
    print(
        "Generated image count:",
        len(generated)
    )


    if len(generated) != len(
        scenes
    ):

        raise RuntimeError(
            f"Expected {len(scenes)} images "
            f"but got {len(generated)}"
        )


    print("")
    print(
        "All scene images generated successfully."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
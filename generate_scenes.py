import json
import re
from pathlib import Path


STORY_FILE = Path("story.json")
OUTPUT_FILE = Path("scenes.json")


# ============================================================
# BASE VISUAL STYLE
# ============================================================

BASE_STYLE = (
    "photorealistic cinematic movie still, vertical 9:16, "
    "high detail, realistic lighting, dramatic composition, "
    "environmental storytelling, realistic anatomy, "
    "cinematic depth of field, premium film look"
)


# ============================================================
# CATEGORY STYLES
# ============================================================

CATEGORY_STYLE = {

    "indian_mythology":
        "epic ancient Indian mythological cinema, authentic period environment",

    "indian_folktale":
        "dark Indian folklore cinema, atmospheric rural India",

    "indian_legend":
        "ancient Indian royal palace, stone architecture, torchlight, royal mystery",

    "supernatural_mystery":
        "grounded supernatural thriller, eerie realistic environment",

    "fantasy":
        "dark fantasy cinema, realistic magical environment",

    "romance_drama":
        "emotional modern cinematic drama",

    "comedy":
        "energetic cinematic comedy, expressive physical action",
}


# ============================================================
# SCENE CAMERA RULES
# ============================================================

SHOT_RULES = {

    "title_hook": (
        "dramatic wide establishing shot. "
        "Show the central mystery or location, not a face."
    ),

    "opening_1": (
        "wide environmental storytelling shot. "
        "Show the location and physical situation."
    ),

    "opening_2": (
        "medium-wide action shot. "
        "Show the event happening."
    ),

    "conflict": (
        "dynamic action or discovery shot. "
        "The conflict must be physically visible."
    ),

    "escalation_1": (
        "over-the-shoulder or environmental discovery shot. "
        "Focus on the important object or event."
    ),

    "escalation_2": (
        "dramatic object/action shot. "
        "Show a new visual event, not another portrait."
    ),

    "dramatic_reveal": (
        "large cinematic reveal shot. "
        "Show the reveal clearly with multiple story elements visible."
    ),

    "final_punch": (
        "wide cinematic consequence shot. "
        "Show the final twist itself, not merely someone's reaction."
    ),
}


# ============================================================
# TEXT SPLITTING
# ============================================================

def split_sentences(text):

    pieces = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        x.strip()
        for x in pieces
        if x.strip()
    ]


def split_balanced(text):

    parts = split_sentences(text)

    if len(parts) <= 1:

        words = text.split()

        middle = max(
            1,
            len(words) // 2
        )

        return (
            " ".join(
                words[:middle]
            ),

            " ".join(
                words[middle:]
            )
        )


    total_words = sum(
        len(x.split())
        for x in parts
    )

    halfway = total_words / 2


    first = []
    second = []

    count = 0


    for sentence in parts:

        if count < halfway:

            first.append(
                sentence
            )

            count += len(
                sentence.split()
            )

        else:

            second.append(
                sentence
            )


    if not second:

        second.append(
            first.pop()
        )


    return (
        " ".join(first),
        " ".join(second)
    )


# ============================================================
# FIND VISUAL OBJECTS
# ============================================================

VISUAL_KEYWORDS = [

    "mirror",
    "mirrors",

    "door",
    "doors",

    "phone",
    "message",

    "train",
    "station",

    "room",
    "palace",

    "painting",
    "portrait",

    "photograph",
    "photo",

    "window",

    "clock",

    "letter",

    "throne",

    "sword",
    "arrow",

    "forest",

    "house",

    "temple",

    "stairs",

    "fire",

    "flames",

    "guards",

    "relatives",

    "family",

    "wall",

    "name",

    "bed",

    "shadow",

    "market",

    "bottle",

    "corridor",

]


def find_objects(text):

    lower = text.lower()

    found = []

    for word in VISUAL_KEYWORDS:

        if word in lower:

            found.append(
                word
            )


    return found[:5]


# ============================================================
# DETERMINE WHETHER CHARACTER IS REQUIRED
# ============================================================

def character_needed(
    story,
    narration
):

    text = (
        " "
        + narration.lower()
        + " "
    )


    main_figure = story.get(
        "main_figure",
        ""
    ).lower()


    if main_figure:

        words = re.findall(
            r"[a-zA-Z]+",
            main_figure
        )

        for word in words:

            if (
                len(word) >= 4
                and word in text
            ):

                return True


    pronouns = [

        " he ",
        " him ",
        " his ",

        " she ",
        " her ",

        " prince ",
        " traveler ",
        " king ",
        " warrior ",
    ]


    return any(
        word in text
        for word in pronouns
    )


# ============================================================
# SCENE-SPECIFIC EMPHASIS
# ============================================================

def special_visual_rules(
    narration
):

    lower = narration.lower()

    rules = []


    if "mirror" in lower:

        rules.append(
            "Mirrors must be clearly visible and important in the composition."
        )


    if "relative" in lower or "family" in lower:

        rules.append(
            "Show multiple family members or relatives physically in the scene."
        )


    if "guard" in lower:

        rules.append(
            "Show palace guards visibly performing the narrated action."
        )


    if "throne" in lower:

        rules.append(
            "The throne and whoever occupies it must dominate the frame."
        )


    if "phone" in lower or "message" in lower:

        rules.append(
            "The phone or message must be visually central; do not replace it with a face."
        )


    if "train" in lower:

        rules.append(
            "The train interior, platform, carriage or railway environment must be clearly visible."
        )


    if "door" in lower:

        rules.append(
            "The door must be clearly visible as a major story object."
        )


    if "portrait" in lower or "painting" in lower:

        rules.append(
            "The portrait or painting must dominate the visual storytelling."
        )


    if "bed" in lower:

        rules.append(
            "Show the bed and the relevant physical space clearly."
        )


    if "clock" in lower:

        rules.append(
            "The clock must be an obvious central story object."
        )


    return " ".join(
        rules
    )


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(
    story,
    beat,
    narration
):

    category = story.get(
        "category",
        ""
    )


    category_style = CATEGORY_STYLE.get(
        category,
        "cinematic storytelling"
    )


    setting = story.get(
        "setting",
        "cinematic environment"
    )


    mood = story.get(
        "mood",
        "dramatic"
    )


    main_figure = story.get(
        "main_figure",
        "main character"
    )


    shot = SHOT_RULES.get(
        beat,
        "cinematic storytelling shot"
    )


    objects = find_objects(
        narration
    )


    object_text = (
        ", ".join(objects)
        if objects
        else "the physical environment and narrated action"
    )


    if character_needed(
        story,
        narration
    ):

        character_rule = (
            f"If the protagonist appears, use {main_figure}. "
            "Keep appearance approximately consistent, "
            "but the character must be performing the narrated action. "
            "Do NOT pose them for a portrait."
        )

    else:

        character_rule = (
            "Do not show the protagonist unless required. "
            "Prioritize the environment, object, secondary characters "
            "or supernatural event."
        )


    extra = special_visual_rules(
        narration
    )


    prompt = f"""
{BASE_STYLE}.

STYLE:
{category_style}.

SETTING:
{setting}.

MOOD:
{mood}.

CAMERA:
{shot}

THIS EXACT STORY MOMENT MUST BE SHOWN:
{narration}

IMPORTANT VISIBLE ELEMENTS:
{object_text}.

{character_rule}

{extra}

STRICT VISUAL RULES:

The narration above is the single source of truth.

Show the literal physical event described in the narration.

Do NOT create a generic protagonist portrait.

Do NOT create a centered headshot.

Do NOT show someone merely standing and staring into camera.

Do NOT use the same composition as a previous scene.

If an object, room, mirror, door, phone, train, relative,
guard, throne, portrait, supernatural event or other physical
detail is mentioned, it must be clearly visible.

Faces are secondary to the story event.

Prefer wide and medium-wide cinematic storytelling shots.

The viewer must understand what is happening even with sound muted.

No text.
No subtitles.
No letters written into the image.
No watermark.
No logo.
""".strip()


    return prompt[:2048]


# ============================================================
# IMPORTANCE
# ============================================================

def get_importance(
    beat
):

    if beat in [
        "dramatic_reveal",
        "final_punch",
    ]:

        return "major"


    if beat in [
        "title_hook",
        "conflict",
        "escalation_2",
    ]:

        return "high"


    return "medium"


# ============================================================
# COMMA MOTION POINTS
# ============================================================

def comma_motion_points(
    text
):

    return max(
        1,
        min(
            text.count(",") + 1,
            4
        )
    )


# ============================================================
# MAIN
# ============================================================

def main():

    if not STORY_FILE.exists():

        raise RuntimeError(
            "story.json not found"
        )


    story = json.loads(
        STORY_FILE.read_text(
            encoding="utf-8"
        )
    )


    opening_1, opening_2 = split_balanced(
        story["opening"]
    )


    escalation_1, escalation_2 = split_balanced(
        story["escalation"]
    )


    scene_plan = [

        (
            "title_hook",
            "title_hook",
            story["title_hook"]
        ),

        (
            "opening_1",
            "opening",
            opening_1
        ),

        (
            "opening_2",
            "opening",
            opening_2
        ),

        (
            "conflict",
            "conflict",
            story["conflict"]
        ),

        (
            "escalation_1",
            "escalation",
            escalation_1
        ),

        (
            "escalation_2",
            "escalation",
            escalation_2
        ),

        (
            "dramatic_reveal",
            "dramatic_reveal",
            story["dramatic_reveal"]
        ),

        (
            "final_punch",
            "final_punch",
            story["final_punch"]
        ),

    ]


    scenes = []


    for index, (
        beat,
        timing_section,
        narration
    ) in enumerate(
        scene_plan
    ):

        prompt = build_prompt(
            story,
            beat,
            narration
        )


        scene = {

            "scene":
                index,

            "beat":
                beat,

            "timing_section":
                timing_section,

            "narration":
                narration,

            "importance":
                get_importance(
                    beat
                ),

            "comma_motion_points":
                comma_motion_points(
                    narration
                ),

            "prompt":
                prompt,

        }


        scenes.append(
            scene
        )


    # ========================================================
    # VALIDATION
    # ========================================================

    if len(scenes) != 8:

        raise RuntimeError(
            f"Expected 8 scenes, got {len(scenes)}"
        )


    OUTPUT_FILE.write_text(

        json.dumps(
            scenes,
            indent=2,
            ensure_ascii=False
        ),

        encoding="utf-8"

    )


    print("")
    print(
        "================================="
    )

    print(
        "SCENE PROMPTS CREATED"
    )

    print(
        "================================="
    )


    for scene in scenes:

        print("")
        print(
            "Scene:",
            scene["scene"] + 1
        )

        print(
            "Beat:",
            scene["beat"]
        )

        print(
            "Narration:",
            scene["narration"]
        )

        print(
            "Objects:",
            find_objects(
                scene["narration"]
            )
        )


    print("")
    print(
        "8 scene prompts saved successfully."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
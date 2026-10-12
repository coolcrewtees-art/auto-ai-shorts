import json
import re
from pathlib import Path


STORY_FILE = Path("story.json")
SCENES_FILE = Path("scenes.json")


BASE_STYLE = (
    "photorealistic cinematic movie frame, vertical 9:16, "
    "realistic anatomy, realistic lighting, realistic environment, "
    "strong environmental storytelling, dramatic depth, "
    "premium film cinematography, no text, no subtitles, "
    "no watermark, no logo"
)


CATEGORY_STYLES = {
    "indian_mythology":
        "epic ancient Indian mythological cinema, authentic Indian setting",

    "indian_folktale":
        "dark atmospheric Indian folklore cinema, rural traditional setting",

    "indian_legend":
        "ancient Indian royal palace cinema, torchlight, stone architecture",

    "supernatural_mystery":
        "grounded supernatural thriller, eerie realistic atmosphere",

    "fantasy":
        "dark fantasy cinema, realistic medieval architecture",

    "romance_drama":
        "emotional cinematic drama, realistic contemporary setting",

    "comedy":
        "energetic cinematic comedy adventure, expressive action",
}


# ============================================================
# TEXT HELPERS
# ============================================================

def sentences(text):
    result = re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )

    return [
        x.strip()
        for x in result
        if x.strip()
    ]


def split_balanced(text):

    parts = sentences(text)

    if len(parts) <= 1:
        words = text.split()

        middle = max(
            1,
            len(words) // 2
        )

        return (
            " ".join(words[:middle]),
            " ".join(words[middle:])
        )

    total = sum(
        len(x.split())
        for x in parts
    )

    half = total / 2

    first = []
    second = []

    count = 0

    for item in parts:

        if count < half:
            first.append(item)
            count += len(item.split())
        else:
            second.append(item)

    if not second:
        second.append(first.pop())

    return (
        " ".join(first),
        " ".join(second)
    )


# ============================================================
# VISUAL EVENT SELECTION
# ============================================================

ACTION_WORDS = [
    "opened",
    "closed",
    "entered",
    "walked",
    "ran",
    "pointed",
    "grabbed",
    "smashed",
    "broke",
    "fell",
    "vanished",
    "appeared",
    "left",
    "arrived",
    "turned",
    "looked",
    "found",
    "discovered",
    "lifted",
    "knocked",
    "stood",
    "collapsed",
]


OBJECT_WORDS = [
    "door",
    "mirror",
    "phone",
    "message",
    "letter",
    "train",
    "station",
    "platform",
    "palace",
    "room",
    "window",
    "painting",
    "portrait",
    "clock",
    "temple",
    "forest",
    "house",
    "stairs",
    "arrow",
    "sword",
    "throne",
    "wall",
    "photograph",
    "screen",
    "grave",
]


def visual_score(text):

    lower = text.lower()

    score = 0

    for word in ACTION_WORDS:
        if word in lower:
            score += 4

    for word in OBJECT_WORDS:
        if word in lower:
            score += 3

    abstract = [
        "thought",
        "believed",
        "remembered",
        "realized",
        "felt",
        "understood",
        "wondered",
        "knew",
    ]

    for word in abstract:
        if word in lower:
            score -= 2

    return score


def select_visual_event(
    narration,
    prefer_late=False
):

    parts = sentences(narration)

    if not parts:
        return narration

    scored = []

    for i, part in enumerate(parts):

        score = visual_score(part)

        if prefer_late:
            score += i * 0.8

        scored.append(
            (
                score,
                i,
                part
            )
        )

    scored.sort(
        key=lambda item: (
            item[0],
            item[1]
        ),
        reverse=True
    )

    return scored[0][2]


# ============================================================
# CHARACTER REQUIREMENT
# ============================================================

def protagonist_required(
    story,
    event
):

    lower = event.lower()

    main = story.get(
        "main_figure",
        ""
    ).lower()

    if main:

        name = (
            main
            .split(",")[0]
            .split()[0]
        )

        if name and name in lower:
            return True

    pronouns = [
        " he ",
        " his ",
        " him ",
        " she ",
        " her ",
    ]

    padded = f" {lower} "

    return any(
        word in padded
        for word in pronouns
    )


# ============================================================
# CAMERA PLAN
# ============================================================

SHOT_TYPES = {
    "title_hook":
        "wide mystery establishing shot",

    "opening_1":
        "wide environmental shot",

    "opening_2":
        "medium action shot",

    "conflict":
        "dynamic conflict shot",

    "escalation_1":
        "over-the-shoulder discovery shot",

    "escalation_2":
        "important object or action close shot",

    "dramatic_reveal":
        "wide dramatic reveal shot",

    "final_punch":
        "cinematic consequence shot",
}


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_prompt(
    story,
    beat,
    event
):

    category_style = CATEGORY_STYLES.get(
        story.get("category"),
        "cinematic storytelling"
    )

    shot = SHOT_TYPES.get(
        beat,
        "cinematic story frame"
    )

    setting = story.get(
        "setting",
        "realistic environment"
    )

    mood = story.get(
        "mood",
        "dramatic"
    )

    protagonist = story.get(
        "main_figure",
        "main protagonist"
    )


    if protagonist_required(
        story,
        event
    ):

        character_instruction = (
            f"The recurring protagonist may appear: {protagonist}. "
            "Keep approximate age, face, hairstyle and clothing consistent. "
            "Do not pose them for a portrait."
        )

    else:

        character_instruction = (
            "Do NOT show the protagonist unless absolutely necessary. "
            "Show the object, location, secondary character or physical event instead."
        )


    prompt = f"""
{BASE_STYLE}.
{category_style}.
Setting: {setting}.
Mood: {mood}.
Camera: {shot}.

EXACT EVENT THAT MUST BE VISIBLE:
{event}

{character_instruction}

CRITICAL RULES:
Show the exact physical event above.
Do not summarize the whole story.
Do not create a generic character portrait.
Do not show a person merely staring into the camera.
Do not use a centered head-and-shoulders composition.
If the event mentions a door, mirror, phone, message, train, room,
letter, object, secondary character or supernatural event,
that thing must visibly dominate the frame.
Environment and actions are more important than faces.
The image must make sense even with the sound turned off.
No written text.
No subtitles.
No watermark.
""".strip()

    return prompt[:2048]


# ============================================================
# IMPORTANCE
# ============================================================

def importance(beat):

    if beat in [
        "title_hook",
        "dramatic_reveal",
        "final_punch",
    ]:
        return "major"

    if beat in [
        "conflict",
        "escalation_2",
    ]:
        return "high"

    return "medium"


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


    plan = [
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


    output = []


    for index, (
        beat,
        timing,
        narration
    ) in enumerate(plan):

        prefer_late = beat in [
            "dramatic_reveal",
            "final_punch",
        ]

        event = select_visual_event(
            narration,
            prefer_late
        )

        prompt = build_prompt(
            story,
            beat,
            event
        )


        output.append({
            "scene": index,
            "beat": beat,
            "timing_section": timing,
            "narration": narration,
            "visual_event": event,
            "importance": importance(
                beat
            ),
            "prompt": prompt,
        })


    if len(output) != 8:
        raise RuntimeError(
            "Scene count must equal 8"
        )


    SCENES_FILE.write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print(
        "\n=== VISUAL EVENTS ==="
    )

    for scene in output:

        print(
            "\nScene",
            scene["scene"] + 1
        )

        print(
            "Beat:",
            scene["beat"]
        )

        print(
            "Visual:",
            scene["visual_event"]
        )


if __name__ == "__main__":
    main()
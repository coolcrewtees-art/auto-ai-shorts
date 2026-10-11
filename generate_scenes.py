import json
import re
from pathlib import Path


# ============================================================
# FILES
# ============================================================

STORY_FILE = Path("story.json")
SCENES_FILE = Path("scenes.json")


# ============================================================
# VISUAL STYLES
# ============================================================

BASE_STYLE = (
    "cinematic photorealistic storytelling frame, "
    "vertical 9:16 composition for YouTube Shorts, "
    "premium film still, realistic skin and anatomy, "
    "dramatic cinematic lighting, strong depth, "
    "detailed environment, atmospheric perspective, "
    "natural facial expression, emotional body language, "
    "high contrast, realistic textures, "
    "no text, no subtitles, no watermark, no logo"
)


CATEGORY_STYLES = {

    "indian_mythology": (
        "epic ancient Indian mythological cinema, "
        "historically inspired Indian clothing and armor, "
        "grand scale, sacred atmosphere, dramatic skies, "
        "rich Indian visual details"
    ),

    "indian_folktale": (
        "dark Indian folklore cinema, old Indian village, "
        "traditional clothing, warm lamps, moonlight, "
        "mysterious rural atmosphere, grounded realism"
    ),

    "indian_legend": (
        "cinematic Indian royal legend, ancient palace architecture, "
        "royal Indian costumes, moody torchlight, "
        "grand mysterious atmosphere"
    ),

    "supernatural_mystery": (
        "modern supernatural thriller, unsettling atmosphere, "
        "realistic locations, eerie shadows, cinematic suspense, "
        "subtle paranormal elements"
    ),

    "fantasy": (
        "dark fantasy cinema, realistic medieval world, "
        "grand architecture, dramatic magical atmosphere, "
        "grounded photorealistic fantasy"
    ),

    "romance_drama": (
        "emotional cinematic drama, realistic contemporary world, "
        "beautiful natural lighting, intimate composition, "
        "subtle melancholy, premium romantic film aesthetic"
    ),

    "comedy": (
        "cinematic adventure comedy, expressive characters, "
        "energetic composition, realistic environment, "
        "slightly exaggerated reactions while remaining photorealistic"
    ),
}


# ============================================================
# HELPERS
# ============================================================

def split_sentences(text):
    """
    Break narration into sentence-like chunks while keeping
    dialogue reasonably intact.
    """

    text = text.strip()

    if not text:
        return []

    pattern = r'.+?(?:[.!?](?:[\'"])?(?=\s|$)|$)'

    parts = re.findall(
        pattern,
        text,
        flags=re.DOTALL
    )

    parts = [
        part.strip()
        for part in parts
        if part.strip()
    ]

    return parts


def split_balanced(text):
    """
    Divide a section into two reasonably balanced pieces.
    Useful for turning one narration beat into two visuals.
    """

    sentences = split_sentences(text)

    if len(sentences) <= 1:
        words = text.split()

        if len(words) < 8:
            return text, text

        middle = len(words) // 2

        first = " ".join(
            words[:middle]
        )

        second = " ".join(
            words[middle:]
        )

        return first, second

    total_words = sum(
        len(sentence.split())
        for sentence in sentences
    )

    target = total_words / 2

    first = []
    second = []

    current = 0

    for sentence in sentences:

        words = len(
            sentence.split()
        )

        if (
            current < target
            or not first
        ):
            first.append(sentence)
            current += words

        else:
            second.append(sentence)

    if not second:
        second.append(
            first.pop()
        )

    return (
        " ".join(first),
        " ".join(second)
    )


def punctuation_motion_points(text):
    """
    Estimates how many internal camera changes can happen
    without requiring a new generated image.
    """

    commas = text.count(",")

    dramatic = len(
        re.findall(
            r"[;:—…!?]",
            text
        )
    )

    short_sentence_breaks = max(
        len(split_sentences(text)) - 1,
        0
    )

    return (
        commas
        + dramatic
        + short_sentence_breaks
    )


def importance_for(beat):

    if beat in (
        "title_hook",
        "dramatic_reveal",
        "final_punch",
    ):
        return "major"

    if beat in (
        "conflict",
        "escalation_2",
    ):
        return "high"

    return "medium"


# ============================================================
# PROMPT BUILDER
# ============================================================

def make_prompt(
    story,
    scene_number,
    beat,
    narration,
):

    category = story.get(
        "category",
        ""
    )

    category_style = CATEGORY_STYLES.get(
        category,
        "cinematic photorealistic dramatic storytelling"
    )

    main_figure = story.get(
        "main_figure",
        "the main character"
    )

    setting = story.get(
        "setting",
        "a cinematic environment"
    )

    mood = story.get(
        "mood",
        "dramatic and cinematic"
    )

    # Repeating this anchor in every prompt gives Flux
    # the best possible chance of keeping the same person.
    character_anchor = (
        f"The recurring main character is {main_figure}. "
        "Keep the recurring character visually consistent across all scenes: "
        "same approximate age, same face structure, same hairstyle, "
        "same skin tone, same core clothing design and accessories. "
        "Do not randomly redesign the main character."
    )

    composition_rules = (
        "Show the exact story moment visually instead of creating "
        "a generic portrait. Use characters interacting with the environment. "
        "Prefer action, reaction, discovery, movement or meaningful objects. "
        "Avoid characters simply standing and staring at the camera. "
        "Do not add unrelated people or objects."
    )

    if beat == "title_hook":

        shot_instruction = (
            "Create an instantly attention-grabbing opening frame. "
            "Show the mystery or central danger immediately. "
            "Strong foreground subject and dramatic environment. "
            "Do not create a title card and do not put words in the image."
        )

    elif beat.startswith("opening"):

        shot_instruction = (
            "Establish the world while showing active story progression. "
            "Use a cinematic medium or wide shot with environmental storytelling."
        )

    elif beat == "conflict":

        shot_instruction = (
            "Show the conflict physically happening. "
            "Use tension, strong facial reaction and clear visual stakes."
        )

    elif beat == "escalation_1":

        shot_instruction = (
            "Show the situation becoming more dangerous or emotionally intense. "
            "Use a dynamic cinematic angle and strong sense of movement."
        )

    elif beat == "escalation_2":

        shot_instruction = (
            "Push the tension higher than the previous scene. "
            "Show a new visual development, not a repetition of the previous shot."
        )

    elif beat == "dramatic_reveal":

        shot_instruction = (
            "This is the major reveal. "
            "Make the discovery immediately understandable visually. "
            "Use the most dramatic composition so far, powerful reaction, "
            "high visual contrast and cinematic shock."
        )

    elif beat == "final_punch":

        shot_instruction = (
            "Create the final unforgettable image of the story. "
            "It should feel conclusive, haunting, emotional, funny or powerful "
            "depending on the story. Use a visually memorable composition."
        )

    else:

        shot_instruction = (
            "Show this exact narrative moment clearly and cinematically."
        )


    prompt = (
        f"{BASE_STYLE}. "
        f"{category_style}. "
        f"Story setting: {setting}. "
        f"Overall mood: {mood}. "
        f"{character_anchor} "
        f"{shot_instruction} "
        f"{composition_rules} "
        f"Scene {scene_number + 1} story moment: {narration}"
    )

    # Cloudflare prompt limit safety
    return prompt[:2048]


# ============================================================
# MAIN
# ============================================================

def main():

    if not STORY_FILE.exists():
        raise FileNotFoundError(
            "story.json does not exist"
        )

    story = json.loads(
        STORY_FILE.read_text(
            encoding="utf-8"
        )
    )


    # ========================================================
    # SPLIT LONGER STORY SECTIONS
    #
    # 6 narration sections become 8 visual scenes:
    #
    # 1 title
    # 2 opening A
    # 3 opening B
    # 4 conflict
    # 5 escalation A
    # 6 escalation B
    # 7 reveal
    # 8 ending
    # ========================================================

    opening_1, opening_2 = split_balanced(
        story["opening"]
    )

    escalation_1, escalation_2 = split_balanced(
        story["escalation"]
    )


    scene_plan = [

        {
            "beat": "title_hook",
            "timing_section": "title_hook",
            "narration":
                story["title_hook"],
        },

        {
            "beat": "opening_1",
            "timing_section": "opening",
            "narration":
                opening_1,
        },

        {
            "beat": "opening_2",
            "timing_section": "opening",
            "narration":
                opening_2,
        },

        {
            "beat": "conflict",
            "timing_section": "conflict",
            "narration":
                story["conflict"],
        },

        {
            "beat": "escalation_1",
            "timing_section": "escalation",
            "narration":
                escalation_1,
        },

        {
            "beat": "escalation_2",
            "timing_section": "escalation",
            "narration":
                escalation_2,
        },

        {
            "beat": "dramatic_reveal",
            "timing_section": "dramatic_reveal",
            "narration":
                story["dramatic_reveal"],
        },

        {
            "beat": "final_punch",
            "timing_section": "final_punch",
            "narration":
                story["final_punch"],
        },
    ]


    scenes = []


    for index, item in enumerate(
        scene_plan
    ):

        narration = (
            item["narration"].strip()
        )

        scene = {

            "scene":
                index,

            "beat":
                item["beat"],

            # This tells our NEXT video editor which
            # voice section this image belongs to.
            "timing_section":
                item["timing_section"],

            "narration":
                narration,

            "importance":
                importance_for(
                    item["beat"]
                ),

            "comma_motion_points":
                punctuation_motion_points(
                    narration
                ),

            "prompt":
                make_prompt(
                    story,
                    index,
                    item["beat"],
                    narration,
                ),
        }


        scenes.append(
            scene
        )


    # ========================================================
    # VERIFY EXACTLY 8
    # ========================================================

    if len(scenes) != 8:
        raise RuntimeError(
            f"Expected 8 scenes but generated {len(scenes)}"
        )


    # ========================================================
    # SAVE
    # ========================================================

    SCENES_FILE.write_text(
        json.dumps(
            scenes,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    # ========================================================
    # LOG
    # ========================================================

    print("")
    print(
        "===================================="
    )

    print(
        "8-SCENE VISUAL PLAN GENERATED"
    )

    print(
        "===================================="
    )


    for scene in scenes:

        print("")
        print(
            f"SCENE {scene['scene'] + 1}"
        )

        print(
            "Beat:",
            scene["beat"]
        )

        print(
            "Voice section:",
            scene["timing_section"]
        )

        print(
            "Importance:",
            scene["importance"]
        )

        print(
            "Motion points:",
            scene[
                "comma_motion_points"
            ]
        )

        print(
            "Narration:",
            scene["narration"]
        )


    print("")
    print(
        "Total scenes:",
        len(scenes)
    )

    print(
        "Saved:",
        SCENES_FILE
    )

    print(
        "===================================="
    )


if __name__ == "__main__":
    main()
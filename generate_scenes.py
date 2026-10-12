import json
import re
from pathlib import Path


STORY_FILE = Path("story.json")
SCENES_FILE = Path("scenes.json")


# ============================================================
# BASE STYLE
# ============================================================

BASE_STYLE = (
    "cinematic photorealistic storytelling frame, "
    "vertical 9:16 composition for YouTube Shorts, "
    "premium movie still, realistic anatomy, "
    "strong environmental storytelling, "
    "dynamic camera composition, varied shot types, "
    "dramatic cinematic lighting, realistic textures, "
    "strong depth and atmospheric perspective, "
    "no text, no subtitles, no watermark, no logo"
)


CATEGORY_STYLES = {

    "indian_mythology": (
        "epic ancient Indian mythological cinema, "
        "historically inspired Indian costumes and armor, "
        "grand scale, sacred atmosphere, dramatic skies"
    ),

    "indian_folktale": (
        "dark Indian folklore cinema, traditional Indian village, "
        "oil lamps, moonlight, dense forest, realistic rural environment"
    ),

    "indian_legend": (
        "ancient Indian royal palace cinema, "
        "traditional royal clothing, stone architecture, "
        "torchlight, stormy atmosphere, mysterious royal setting"
    ),

    "supernatural_mystery": (
        "modern supernatural thriller, realistic locations, "
        "unnerving shadows, eerie atmosphere, grounded paranormal horror"
    ),

    "fantasy": (
        "dark cinematic fantasy, realistic medieval kingdom, "
        "grand architecture, dramatic atmosphere, grounded fantasy realism"
    ),

    "romance_drama": (
        "premium emotional drama, contemporary realistic world, "
        "natural cinematic lighting, intimate environments, subtle melancholy"
    ),

    "comedy": (
        "cinematic adventure comedy, energetic framing, "
        "expressive physical reactions, realistic world, playful atmosphere"
    ),
}


# ============================================================
# TEXT HELPERS
# ============================================================

def split_sentences(text):

    text = text.strip()

    if not text:
        return []

    pieces = re.findall(
        r".+?(?:[.!?](?:['\"])?(?=\s|$)|$)",
        text,
        flags=re.DOTALL
    )

    return [
        piece.strip()
        for piece in pieces
        if piece.strip()
    ]


def split_balanced(text):

    sentences = split_sentences(
        text
    )

    if len(sentences) <= 1:

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
        len(sentence.split())
        for sentence in sentences
    )

    halfway = total_words / 2

    first = []
    second = []

    running = 0

    for sentence in sentences:

        if running < halfway:
            first.append(
                sentence
            )

            running += len(
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


def motion_points(text):

    commas = text.count(",")

    dramatic = len(
        re.findall(
            r"[;:!?…]",
            text
        )
    )

    sentence_changes = max(
        len(
            split_sentences(text)
        ) - 1,
        0
    )

    return (
        commas
        + dramatic
        + sentence_changes
    )


# ============================================================
# SHOT TYPE
# ============================================================

def shot_type_for(
    beat,
    scene_number
):

    if beat == "title_hook":

        return (
            "dramatic cinematic establishing shot"
        )

    if beat == "opening_1":

        return (
            "wide environmental establishing shot"
        )

    if beat == "opening_2":

        return (
            "medium action shot with strong environment"
        )

    if beat == "conflict":

        return (
            "dynamic action or discovery shot"
        )

    if beat == "escalation_1":

        return (
            "over-the-shoulder or environmental reaction shot"
        )

    if beat == "escalation_2":

        return (
            "object-focused or action-focused cinematic shot"
        )

    if beat == "dramatic_reveal":

        return (
            "wide dramatic reveal shot focused on the supernatural event or discovery"
        )

    if beat == "final_punch":

        return (
            "memorable final consequence shot"
        )

    return (
        "cinematic storytelling shot"
    )


# ============================================================
# PROMPT
# ============================================================

def make_prompt(
    story,
    scene_number,
    beat,
    narration
):

    category = story.get(
        "category",
        ""
    )

    category_style = (
        CATEGORY_STYLES.get(
            category,
            "cinematic photorealistic storytelling"
        )
    )

    character = story.get(
        "main_figure",
        "the main character"
    )

    setting = story.get(
        "setting",
        "cinematic environment"
    )

    mood = story.get(
        "mood",
        "dramatic"
    )

    shot_type = shot_type_for(
        beat,
        scene_number
    )


    # --------------------------------------------------------
    # MOST IMPORTANT CHANGE:
    # EVENT > CHARACTER
    # --------------------------------------------------------

    event_priority = (
        "The exact narrated event is the highest visual priority. "
        "The image must show the important action, object, environment, "
        "discovery, danger or supernatural event described in the narration. "
        "The viewer should understand what is happening even with audio muted. "
    )


    anti_portrait = (
        "Do not default to a portrait. "
        "Do not make the character simply stand and stare at the camera. "
        "Do not use generic heroic poses. "
        "Do not fill the entire frame with a face unless the narration specifically "
        "requires a facial reaction. "
    )


    variation = (
        f"Use a {shot_type}. "
        "Make this composition clearly different from the previous scenes. "
        "Use the environment and important story objects prominently. "
    )


    character_consistency = (
        f"If {character} appears, preserve the same approximate age, "
        "face structure, hairstyle, skin tone, clothing design and accessories. "
        "Character consistency matters, but the character does not need "
        "to dominate every frame. "
    )


    # --------------------------------------------------------
    # SPECIAL BEAT RULES
    # --------------------------------------------------------

    if beat == "title_hook":

        specific = (
            "Immediately visualize the central mystery or danger. "
            "Create curiosity in the first frame. "
            "No title card and no visible written title."
        )


    elif beat.startswith(
        "opening"
    ):

        specific = (
            "Establish the place while showing an actual event occurring. "
            "Prioritize environmental storytelling."
        )


    elif beat == "conflict":

        specific = (
            "Show the conflict physically happening. "
            "Clearly show the dangerous object, action or discovery."
        )


    elif beat == "escalation_1":

        specific = (
            "Show a new development that increases tension. "
            "Do not repeat the previous framing."
        )


    elif beat == "escalation_2":

        specific = (
            "Show the next important clue, object or event. "
            "Prefer an object-focused or environmental composition "
            "rather than another character portrait."
        )


    elif beat == "dramatic_reveal":

        specific = (
            "THIS IS THE MAJOR REVEAL. "
            "Do NOT create a portrait. "
            "The actual reveal must dominate the frame. "
            "Clearly show the supernatural event, hidden object, trapped people, "
            "mirror, doorway, creature, discovery or other key reveal described. "
            "The reveal must be understandable visually with the sound muted."
        )


    elif beat == "final_punch":

        specific = (
            "Show the consequence of the ending or final twist itself. "
            "Do not simply show the protagonist's face. "
            "Create an unforgettable final visual."
        )


    else:

        specific = (
            "Show the exact narrated event."
        )


    prompt = (
        f"{BASE_STYLE}. "
        f"{category_style}. "
        f"Setting: {setting}. "
        f"Mood: {mood}. "
        f"{event_priority}"
        f"{variation}"
        f"{character_consistency}"
        f"{anti_portrait}"
        f"{specific} "
        f"Exact story moment: {narration}. "
        "No text, no captions, no letters, no watermark."
    )


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

        raise FileNotFoundError(
            "story.json not found"
        )


    story = json.loads(
        STORY_FILE.read_text(
            encoding="utf-8"
        )
    )


    # --------------------------------------------------------
    # 6 narration sections -> 8 image scenes
    # --------------------------------------------------------

    opening_1, opening_2 = (
        split_balanced(
            story["opening"]
        )
    )


    escalation_1, escalation_2 = (
        split_balanced(
            story["escalation"]
        )
    )


    plan = [

        {
            "beat":
                "title_hook",

            "timing_section":
                "title_hook",

            "narration":
                story["title_hook"],
        },


        {
            "beat":
                "opening_1",

            "timing_section":
                "opening",

            "narration":
                opening_1,
        },


        {
            "beat":
                "opening_2",

            "timing_section":
                "opening",

            "narration":
                opening_2,
        },


        {
            "beat":
                "conflict",

            "timing_section":
                "conflict",

            "narration":
                story["conflict"],
        },


        {
            "beat":
                "escalation_1",

            "timing_section":
                "escalation",

            "narration":
                escalation_1,
        },


        {
            "beat":
                "escalation_2",

            "timing_section":
                "escalation",

            "narration":
                escalation_2,
        },


        {
            "beat":
                "dramatic_reveal",

            "timing_section":
                "dramatic_reveal",

            "narration":
                story[
                    "dramatic_reveal"
                ],
        },


        {
            "beat":
                "final_punch",

            "timing_section":
                "final_punch",

            "narration":
                story[
                    "final_punch"
                ],
        },
    ]


    scenes = []


    for index, item in enumerate(
        plan
    ):

        narration = (
            item["narration"]
            .strip()
        )


        scenes.append({

            "scene":
                index,

            "beat":
                item["beat"],

            "timing_section":
                item[
                    "timing_section"
                ],

            "narration":
                narration,

            "importance":
                importance(
                    item["beat"]
                ),

            "comma_motion_points":
                motion_points(
                    narration
                ),

            "prompt":
                make_prompt(
                    story,
                    index,
                    item["beat"],
                    narration
                ),
        })


    if len(scenes) != 8:

        raise RuntimeError(
            f"Expected 8 scenes, got {len(scenes)}"
        )


    SCENES_FILE.write_text(
        json.dumps(
            scenes,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


    print(
        "8 visual scenes created"
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
            "Prompt:",
            scene["prompt"]
        )


if __name__ == "__main__":
    main()
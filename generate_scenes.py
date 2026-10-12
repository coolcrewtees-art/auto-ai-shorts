import json
import re
from pathlib import Path


# ============================================================
# FILES
# ============================================================

STORY_FILE = Path("story.json")
SCENES_FILE = Path("scenes.json")


# ============================================================
# VISUAL STYLE
# ============================================================

BASE_STYLE = (
    "cinematic photorealistic movie still, "
    "vertical 9:16 composition for YouTube Shorts, "
    "realistic anatomy, realistic environment, "
    "dynamic cinematic camera angle, "
    "strong environmental storytelling, "
    "dramatic lighting, atmospheric depth, "
    "high detail, realistic textures, "
    "not a poster, not a character portrait, "
    "no text, no subtitles, no watermark, no logo"
)


CATEGORY_STYLES = {

    "indian_mythology": (
        "epic ancient Indian mythological cinema, "
        "authentic Indian-inspired armor and clothing, "
        "large-scale environment, sacred atmosphere"
    ),

    "indian_folktale": (
        "dark Indian folklore cinema, "
        "old rural Indian village, traditional clothing, "
        "oil lamps, moonlight, eerie forest atmosphere"
    ),

    "indian_legend": (
        "ancient Indian royal palace cinema, "
        "traditional royal clothing, stone architecture, "
        "torchlight, monsoon storm atmosphere"
    ),

    "supernatural_mystery": (
        "grounded supernatural thriller, "
        "realistic locations, eerie shadows, "
        "subtle paranormal horror"
    ),

    "fantasy": (
        "dark fantasy cinema, medieval architecture, "
        "grounded photorealistic fantasy, dramatic atmosphere"
    ),

    "romance_drama": (
        "emotional premium drama film, "
        "realistic contemporary setting, "
        "natural cinematic lighting, intimate atmosphere"
    ),

    "comedy": (
        "cinematic adventure comedy, "
        "expressive physical action, energetic framing, "
        "realistic environment"
    ),
}


# ============================================================
# SENTENCE HELPERS
# ============================================================

def split_sentences(text):

    text = text.strip()

    if not text:
        return []

    results = re.findall(
        r".+?(?:[.!?](?:['\"])?(?=\s|$)|$)",
        text,
        flags=re.DOTALL
    )

    return [
        item.strip()
        for item in results
        if item.strip()
    ]


def split_balanced(text):

    sentences = split_sentences(text)

    if len(sentences) < 2:

        words = text.split()

        middle = max(
            1,
            len(words) // 2
        )

        return (
            " ".join(words[:middle]),
            " ".join(words[middle:])
        )

    total_words = sum(
        len(sentence.split())
        for sentence in sentences
    )

    target = total_words / 2

    first = []
    second = []

    running = 0

    for sentence in sentences:

        if running < target:

            first.append(sentence)

            running += len(
                sentence.split()
            )

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


# ============================================================
# VISUAL KEYWORDS
#
# Sentences containing these are preferred because they
# describe things an image model can actually show.
# ============================================================

VISUAL_WORDS = [

    # objects
    "mirror",
    "door",
    "window",
    "wall",
    "painting",
    "portrait",
    "photograph",
    "phone",
    "message",
    "letter",
    "map",
    "train",
    "platform",
    "station",
    "room",
    "palace",
    "temple",
    "forest",
    "house",
    "stairs",
    "staircase",
    "floor",
    "trapdoor",
    "arrow",
    "arrows",
    "battlefield",
    "chair",

    # supernatural
    "reflection",
    "creature",
    "ghost",
    "bride",
    "shadow",
    "footprints",
    "trapped",
    "screaming",

    # actions
    "opened",
    "closed",
    "entered",
    "walked",
    "pointed",
    "smashed",
    "broke",
    "ran",
    "grabbed",
    "looked",
    "stood",
    "appeared",
    "vanished",
    "disappeared",
    "collapsed",
    "lifted",
    "knocked",
    "moved",

    # visually useful people
    "guards",
    "soldiers",
    "queen",
    "king",
    "prince",
    "prisoner",
    "conductor",
    "passenger",
]


# ============================================================
# SCORE A SENTENCE BY HOW VISUAL IT IS
# ============================================================

def visual_score(sentence):

    lower = sentence.lower()

    score = 0

    for word in VISUAL_WORDS:

        if word in lower:
            score += 3

    # Concrete action usually makes a better frame.
    if re.search(
        r"\b(opened|walked|ran|stood|pointed|smashed|looked|appeared|moved|entered|lifted|fell)\b",
        lower
    ):
        score += 4

    # Dialogue alone is usually poor for image generation.
    quote_count = (
        sentence.count("'")
        + sentence.count('"')
    )

    if quote_count >= 2:
        score -= 2

    # Abstract statements are less useful.
    abstract_words = [
        "thought",
        "believed",
        "understood",
        "remembered",
        "felt",
        "knew",
        "wondered",
        "realized",
    ]

    for word in abstract_words:

        if word in lower:
            score -= 1

    return score


# ============================================================
# SELECT ONE CONCRETE VISUAL MOMENT
# ============================================================

def choose_visual_moment(
    narration,
    beat
):

    sentences = split_sentences(
        narration
    )

    if not sentences:
        return narration

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    if beat == "title_hook":
        return narration

    # --------------------------------------------------------
    # REVEAL / ENDING
    #
    # Prefer the later visually strong sentence because
    # that's usually where the actual reveal happens.
    # --------------------------------------------------------

    scored = []

    for index, sentence in enumerate(
        sentences
    ):

        score = visual_score(
            sentence
        )

        if beat in [
            "dramatic_reveal",
            "final_punch",
        ]:
            score += index * 0.7

        scored.append(
            (
                score,
                index,
                sentence
            )
        )

    scored.sort(
        key=lambda x: (
            x[0],
            x[1]
        ),
        reverse=True
    )

    best_sentence = scored[0][2]

    # --------------------------------------------------------
    # OPTIONAL SECOND SENTENCE
    #
    # Add a neighboring sentence only if it makes the visual
    # clearer, but never send the whole paragraph.
    # --------------------------------------------------------

    best_index = sentences.index(
        best_sentence
    )

    candidates = [
        best_sentence
    ]

    if best_index + 1 < len(sentences):

        next_sentence = sentences[
            best_index + 1
        ]

        if visual_score(
            next_sentence
        ) >= 3:

            candidates.append(
                next_sentence
            )

    visual_moment = " ".join(
        candidates
    )

    return visual_moment


# ============================================================
# REMOVE DIALOGUE-HEAVY / ABSTRACT WORDING
# ============================================================

def clean_visual_moment(text):

    text = text.strip()

    # Remove speech quotes because image models sometimes
    # try to draw visible text.
    text = text.replace(
        '"',
        ""
    )

    text = text.replace(
        "'",
        ""
    )

    # Avoid accidental attempts to render quoted text.
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# DOES THE MAIN CHARACTER NEED TO APPEAR?
# ============================================================

def character_needed(
    story,
    visual_moment
):

    lower = visual_moment.lower()

    main_figure = story.get(
        "main_figure",
        ""
    ).lower()

    # Explicit names / roles.
    keywords = [

        "he ",
        "she ",
        "his ",
        "her ",
        "him ",
        "king",
        "prince",
        "traveler",
        "rohan",
        "arjun",
        "milo",
        "bhishma",
        "warrior",

    ]

    if main_figure:

        first_name = (
            main_figure
            .split(",")[0]
            .split()[0]
        )

        if first_name in lower:
            return True

    return any(
        word in lower
        for word in keywords
    )


# ============================================================
# SHOT TYPE
# ============================================================

def get_shot_type(
    beat,
    scene_index
):

    shots = {

        "title_hook":
            "wide cinematic mystery establishing shot",

        "opening_1":
            "wide environmental establishing shot",

        "opening_2":
            "medium-wide action shot",

        "conflict":
            "dynamic action shot",

        "escalation_1":
            "over-the-shoulder discovery shot",

        "escalation_2":
            "close environmental or important-object shot",

        "dramatic_reveal":
            "wide reveal composition showing the entire discovery",

        "final_punch":
            "dramatic final consequence shot",
    }

    return shots.get(
        beat,
        "cinematic storytelling shot"
    )


# ============================================================
# BEAT INSTRUCTION
# ============================================================

def beat_instruction(beat):

    if beat == "title_hook":

        return (
            "Show the central mystery immediately. "
            "The image must create curiosity without using written text."
        )

    if beat.startswith("opening"):

        return (
            "Establish the location while showing a concrete event. "
            "Environment should occupy a large part of the frame."
        )

    if beat == "conflict":

        return (
            "Show the conflict actually happening. "
            "The object or action causing the problem must be visible."
        )

    if beat.startswith("escalation"):

        return (
            "Show the new clue, action or danger itself. "
            "Use a different framing from earlier shots."
        )

    if beat == "dramatic_reveal":

        return (
            "This is the major reveal. "
            "The reveal itself must dominate the image. "
            "Do not replace the reveal with a reaction portrait."
        )

    if beat == "final_punch":

        return (
            "Show the actual consequence or final twist. "
            "The ending should be visually understandable without narration."
        )

    return (
        "Show the exact physical event."
    )


# ============================================================
# BUILD PROMPT
# ============================================================

def build_prompt(
    story,
    beat,
    visual_moment,
    scene_index
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

    shot = get_shot_type(
        beat,
        scene_index
    )

    instruction = beat_instruction(
        beat
    )

    # --------------------------------------------------------
    # CHARACTER TEXT IS ONLY ADDED WHEN NEEDED
    # --------------------------------------------------------

    if character_needed(
        story,
        visual_moment
    ):

        character_text = (
            f"If the recurring protagonist appears, they are {main_figure}. "
            "Keep their face, approximate age, hair, clothing and accessories "
            "consistent with previous scenes. "
        )

    else:

        character_text = (
            "The protagonist does NOT need to appear in this shot. "
            "Prioritize the environment, important object or event instead. "
        )

    prompt = (
        f"{BASE_STYLE}. "
        f"{category_style}. "
        f"Setting: {setting}. "
        f"Mood: {mood}. "
        f"Camera: {shot}. "
        f"{instruction} "
        f"{character_text}"
        "IMPORTANT: show ONE specific visual moment, not a summary of the story. "
        "Do not generate a generic portrait. "
        "Do not make anybody stare directly at the camera. "
        "Do not use a centered head-and-shoulders composition unless absolutely necessary. "
        "The environment, action, object or reveal should occupy most of the frame. "
        f"EXACT VISUAL MOMENT TO SHOW: {visual_moment}. "
        "No written words, no readable letters, no captions, no logo."
    )

    return prompt[:2048]


# ============================================================
# MOTION POINTS
# ============================================================

def motion_points(text):

    return (
        text.count(",")
        + len(
            re.findall(
                r"[;:!?…]",
                text
            )
        )
        + max(
            len(
                split_sentences(text)
            ) - 1,
            0
        )
    )


# ============================================================
# IMPORTANCE
# ============================================================

def get_importance(beat):

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

    # ========================================================
    # SPLIT LONG SECTIONS
    # ========================================================

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


    # ========================================================
    # 8 VISUAL SCENES
    # ========================================================

    plan = [

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
            "timing_section":
                "dramatic_reveal",
            "narration":
                story[
                    "dramatic_reveal"
                ],
        },

        {
            "beat": "final_punch",
            "timing_section":
                "final_punch",
            "narration":
                story[
                    "final_punch"
                ],
        },
    ]


    scenes = []


    # ========================================================
    # BUILD SCENES
    # ========================================================

    for index, item in enumerate(
        plan
    ):

        narration = (
            item["narration"]
            .strip()
        )

        # ----------------------------------------------------
        # NEW:
        # Pick one actual visual moment
        # ----------------------------------------------------

        visual_moment = (
            choose_visual_moment(
                narration,
                item["beat"]
            )
        )

        visual_moment = (
            clean_visual_moment(
                visual_moment
            )
        )


        prompt = build_prompt(
            story,
            item["beat"],
            visual_moment,
            index
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

            # Voice/edit timing still uses full narration.
            "narration":
                narration,

            # Image generator uses ONLY this.
            "visual_moment":
                visual_moment,

            "importance":
                get_importance(
                    item["beat"]
                ),

            "comma_motion_points":
                motion_points(
                    narration
                ),

            "prompt":
                prompt,
        })


    # ========================================================
    # VALIDATION
    # ========================================================

    if len(scenes) != 8:

        raise RuntimeError(
            f"Expected 8 scenes, got {len(scenes)}"
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
    # DEBUG OUTPUT
    # ========================================================

    print("")
    print(
        "========================================"
    )

    print(
        "EVENT-FOCUSED VISUAL SCENES CREATED"
    )

    print(
        "========================================"
    )


    for scene in scenes:

        print("")
        print(
            "SCENE",
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
            "VISUAL MOMENT:",
            scene["visual_moment"]
        )

        print(
            "Prompt:",
            scene["prompt"]
        )


    print("")
    print(
        "Total scenes:",
        len(scenes)
    )


if __name__ == "__main__":
    main()
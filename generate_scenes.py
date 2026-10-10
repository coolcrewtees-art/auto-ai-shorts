import json
import re
from pathlib import Path

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

BASE_STYLE = (
    "cinematic photorealistic storytelling image, vertical 9:16 composition, "
    "dramatic lighting, strong depth, realistic textures, clear visual storytelling, "
    "high detail, no text, no watermark"
)

CATEGORY_STYLE = {
    "indian_mythology": (
        "epic Indian mythological atmosphere, ancient Indian architecture, "
        "ornate traditional clothing, sacred symbolism, dramatic divine lighting"
    ),

    "indian_folktale": (
        "Indian folktale atmosphere, rural or old-world Indian setting, "
        "authentic regional textures, mysterious cinematic mood"
    ),

    "indian_legend": (
        "legendary Indian royal or village atmosphere, timeless dramatic visual style, "
        "rich architecture and traditional clothing"
    ),

    "supernatural_mystery": (
        "eerie supernatural atmosphere, cinematic shadows, suspenseful composition, "
        "subtle horror without gore"
    ),

    "fantasy": (
        "dark fantasy cinematic atmosphere, magical environment, dramatic scale, "
        "mysterious lighting"
    ),

    "romance_drama": (
        "emotional cinematic romance, expressive faces, soft dramatic lighting, "
        "beautiful atmosphere"
    ),

    "comedy": (
        "cinematic comedic storytelling, expressive reactions, playful visual timing, "
        "slightly heightened but realistic situations"
    ),
}

genre_style = CATEGORY_STYLE.get(
    story["category"],
    "cinematic dramatic storytelling"
)

BEATS = [
    {
        "name": "title_hook",
        "text": story["title_hook"],
        "importance": "major",
        "shot": "striking cinematic hook shot",
        "direction": (
            "Create immediate curiosity. Show the most intriguing visual idea "
            "without revealing the entire twist."
        ),
    },

    {
        "name": "opening",
        "text": story["opening"],
        "importance": "medium",
        "shot": "wide or medium establishing shot",
        "direction": (
            "Clearly establish who, where, and what is happening. "
            "This should feel like the true beginning of the story."
        ),
    },

    {
        "name": "conflict",
        "text": story["conflict"],
        "importance": "medium",
        "shot": "focused dramatic medium shot",
        "direction": (
            "Show the central problem clearly. The visual must communicate danger, "
            "tension, emotion, or complication."
        ),
    },

    {
        "name": "escalation",
        "text": story["escalation"],
        "importance": "medium",
        "shot": "dynamic action or tension shot",
        "direction": (
            "Escalate the situation. Avoid a generic portrait. "
            "Show action, discovery, movement, confrontation, or a meaningful visual clue."
        ),
    },

    {
        "name": "dramatic_reveal",
        "text": story["dramatic_reveal"],
        "importance": "major",
        "shot": "powerful reveal shot",
        "direction": (
            "This is the biggest visual reveal of the story. "
            "Make it immediately understandable, dramatic, and visually different."
        ),
    },

    {
        "name": "final_punch",
        "text": story["final_punch"],
        "importance": "major",
        "shot": "memorable final cinematic shot",
        "direction": (
            "Create a strong final image with emotional, eerie, romantic, or ironic impact. "
            "It must feel like a closing punch."
        ),
    },
]

scenes = []

for index, beat in enumerate(BEATS):

    comma_count = beat["text"].count(",")

    pause_count = len(
        re.findall(
            r"[;:—…]",
            beat["text"]
        )
    )

    prompt = (
        f"{BASE_STYLE}. "
        f"{genre_style}. "
        f"Story title: {story['title_hook']}. "
        f"Main figure: {story['main_figure']}. "
        f"Setting: {story['setting']}. "
        f"Mood: {story['mood']}. "
        f"Exact narration to visualize: {beat['text']} "
        f"Shot type: {beat['shot']}. "
        f"{beat['direction']} "
        "Keep recurring characters visually consistent in age, face, hair, clothing, "
        "and major accessories whenever they appear again. "
        "Avoid unrelated extra people. "
        "No written words inside the image."
    )

    scenes.append({
        "scene": index,
        "beat": beat["name"],
        "narration": beat["text"],
        "importance": beat["importance"],

        # Later used for zoom/crop changes,
        # NOT new image generation.
        "comma_motion_points": comma_count + pause_count,

        "prompt": prompt
    })

Path("scenes.json").write_text(
    json.dumps(
        scenes,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(f"Generated {len(scenes)} story scenes.")
print(
    json.dumps(
        scenes,
        indent=2,
        ensure_ascii=False
    )
)
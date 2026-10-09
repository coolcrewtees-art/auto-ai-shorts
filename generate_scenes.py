import json
from pathlib import Path

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

title = story["title"]
category = story["category"]
main_figure = story["main_figure"]
setting = story["setting"]
mood = story["mood"]
beats = story["beats"]

BASE_STYLE = (
    "cinematic photorealistic storytelling visual, vertical 9:16 composition, "
    "dramatic lighting, realistic textures, atmospheric depth, "
    "professional film still, visually clear storytelling, no text, no watermark"
)

# Style tweaks by genre
CATEGORY_STYLE = {
    "indian_mythology": (
        "epic Indian mythological aesthetic, ancient Indian architecture, "
        "ornate traditional clothing and armor, divine atmosphere, rich gold and deep shadows"
    ),
    "indian_history": (
        "historically inspired Indian setting, realistic period clothing, "
        "authentic architecture and battlefield atmosphere"
    ),
    "international_history": (
        "historically inspired period setting, realistic clothing and architecture, "
        "documentary-cinematic visual style"
    ),
    "fantasy": (
        "dark fantasy cinematic aesthetic, magical atmosphere, dramatic environments"
    ),
    "romance_drama": (
        "emotional cinematic romance aesthetic, expressive faces, soft dramatic lighting"
    ),
    "comedy": (
        "cinematic but playful visual storytelling, expressive reactions, slightly exaggerated situation"
    ),
}

genre_style = CATEGORY_STYLE.get(
    category,
    "cinematic dramatic storytelling aesthetic"
)

# One presenter image reused in the final edit
presenter = {
    "scene": 0,
    "type": "presenter",
    "purpose": "presenter",
    "prompt": (
        f"{BASE_STYLE}. "
        "A charismatic young Indian male storyteller in a premium dark studio, "
        "simple black outfit, facing the camera, confident mysterious expression, "
        "soft rim lighting, blurred cinematic background, waist-up framing, "
        "high-end social media storytelling host aesthetic."
    )
}

# Shot styles keep the reel visually varied
SHOT_STYLES = [
    "dramatic wide establishing shot",
    "intense medium shot",
    "dynamic action shot",
    "cinematic close-up reaction shot",
    "powerful final wide shot"
]

story_scenes = []

for index, beat in enumerate(beats, start=1):

    beat_type = beat["type"]
    beat_text = beat["text"]

    shot = SHOT_STYLES[min(index - 1, len(SHOT_STYLES) - 1)]

    extra_direction = ""

    if beat_type == "hook":
        extra_direction = (
            "The image must instantly create curiosity. "
            "Show the most visually striking moment related to the hook."
        )

    elif beat_type == "conflict":
        extra_direction = (
            "Clearly show the central problem or danger. "
            "The viewer should understand that something serious is happening."
        )

    elif beat_type == "escalation":
        extra_direction = (
            "Increase tension and intensity. Show action, danger, confrontation, "
            "or a powerful emotional moment."
        )

    elif beat_type == "twist":
        extra_direction = (
            "Show the shocking reveal visually. "
            "This should feel like the biggest visual moment of the reel."
        )

    elif beat_type == "ending":
        extra_direction = (
            "Create a memorable final frame with emotional or dramatic impact. "
            "It should feel like a strong ending, not a generic portrait."
        )

    prompt = (
        f"{BASE_STYLE}. "
        f"{genre_style}. "
        f"Story: {title}. "
        f"Main figure: {main_figure}. "
        f"Setting: {setting}. "
        f"Overall mood: {mood}. "
        f"Exact story beat to visualize: {beat_text}. "
        f"Shot type: {shot}. "
        f"{extra_direction} "
        "Avoid unrelated extra characters unless required by the story. "
        "Keep the visual focused on the exact event being narrated."
    )

    story_scenes.append({
        "scene": index,
        "type": "story",
        "purpose": beat_type,
        "narration": beat_text,
        "prompt": prompt
    })

all_scenes = [presenter] + story_scenes

Path("scenes.json").write_text(
    json.dumps(
        all_scenes,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print(f"Generated {len(all_scenes)} scenes:")
print(json.dumps(all_scenes, indent=2, ensure_ascii=False))
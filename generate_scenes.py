import json
from pathlib import Path

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

title = story["title"]
category = story["category"]
main_figure = story["main_figure"]
setting = story["setting"]
era = story["era"]
mood = story["mood"]
beats = story["beats"]

STYLE = (
    "cinematic photorealistic scene, vertical 9:16 composition, "
    "dramatic lighting, rich atmosphere, high detail, realistic textures, "
    "Indian aesthetic accuracy, professional storytelling visual, "
    "no text, no watermark"
)

# Consistent presenter image
presenter_scene = {
    "scene": 0,
    "type": "presenter",
    "prompt": (
        f"{STYLE}. A charismatic young Indian male storyteller in a dark premium studio, "
        "wearing a black outfit, facing the camera, confident and mysterious expression, "
        "soft cinematic rim lighting, blurred dark background, waist-up portrait, "
        "social media storytelling host aesthetic."
    )
}

story_scenes = []

for i, beat in enumerate(beats, start=1):
    story_scenes.append({
        "scene": i,
        "type": "story",
        "purpose": f"beat_{i}",
        "prompt": (
            f"{STYLE}. Story title inspiration: {title}. "
            f"Category: {category}. "
            f"Main figure: {main_figure}. "
            f"Setting: {setting}. Era: {era}. Mood: {mood}. "
            f"Visualize this exact story beat clearly and dramatically: {beat}. "
            "Strong cinematic composition. Make the image clear and narrative, not random."
        )
    })

all_scenes = [presenter_scene] + story_scenes

Path("scenes.json").write_text(
    json.dumps(all_scenes, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Generated storytelling scenes:")
print(json.dumps(all_scenes, indent=2, ensure_ascii=False))
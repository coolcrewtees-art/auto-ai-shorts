import json
from pathlib import Path

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

character = story["character"]
setting = story["setting"]
goal = story["goal"]
obstacle = story["obstacle"]
twist = story["twist"]
mood = story["mood"]

style = (
    "cinematic photorealistic movie still, vertical 9:16, "
    "dramatic lighting, realistic textures, atmospheric depth, "
    "high detail, consistent character design, same face and clothing, "
    "no text, no watermark"
)

scene_descriptions = [
    f"A mysterious exterior view of the {setting}, immediately intriguing and {mood}.",

    f"The {character} approaches the {setting}, unaware of what is waiting inside.",

    f"The {character} enters the {setting}, cautiously observing the surroundings.",

    f"A close-up of the {character} noticing the first strange clue.",

    f"The {character} begins trying to {goal}.",

    f"The environment becomes more threatening as {obstacle}.",

    f"The {character} investigates a disturbing detail hidden in the {setting}.",

    f"A tense close-up as the {character} realizes something does not make sense.",

    f"The {character} moves deeper into the {setting}, surrounded by increasingly strange clues.",

    f"A dangerous or unsettling event suddenly interrupts the investigation.",

    f"The {character} discovers evidence pointing toward a shocking truth.",

    f"A dramatic moment immediately before the revelation, intense suspense.",

    f"The shocking truth becomes clear: {twist}.",

    f"Close-up of the {character} reacting emotionally to the revelation.",

    f"The {character} stands alone in the {setting} after the revelation, unresolved cliffhanger ending."
]

scenes = []

for i, description in enumerate(scene_descriptions, start=1):
    scenes.append({
        "scene": i,
        "prompt": (
            f"{style}. "
            f"{description} "
            f"Overall atmosphere: {mood}. "
            "Strong cinematic composition."
        )
    })

Path("scenes.json").write_text(
    json.dumps(scenes, indent=2),
    encoding="utf-8"
)

print(f"Generated {len(scenes)} visual scenes.")
print(json.dumps(scenes, indent=2))
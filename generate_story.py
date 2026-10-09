import json
import random
import hashlib
from pathlib import Path

HISTORY_FILE = Path("story_history.json")

genres = [
    "sci-fi", "mystery", "psychological thriller", "fantasy",
    "horror", "adventure", "dystopian", "supernatural"
]

settings = [
    "abandoned moon colony",
    "underwater research station",
    "city frozen in time",
    "deserted space station",
    "underground megacity",
    "ancient temple beneath a modern city",
    "train that never reaches its final station",
    "remote Arctic laboratory",
    "floating city above the clouds",
    "abandoned amusement park"
]

characters = [
    "young engineer",
    "memory-wiped android",
    "stranded astronaut",
    "rookie detective",
    "teenage inventor",
    "lonely scientist",
    "runaway artificial intelligence",
    "mysterious traveller",
    "rescue pilot",
    "archaeologist"
]

goals = [
    "escape before time runs out",
    "discover who erased their memories",
    "save someone trapped inside",
    "decode a mysterious transmission",
    "find the truth about the location",
    "stop an approaching disaster",
    "reach a forbidden chamber",
    "return home",
    "find a missing person",
    "survive until sunrise"
]

obstacles = [
    "the exits suddenly disappear",
    "an AI begins lying to them",
    "time keeps resetting",
    "someone is secretly following them",
    "their memories contradict reality",
    "the building begins changing shape",
    "all communication stops",
    "their equipment begins failing",
    "they discover someone else is controlling the system",
    "every clue leads back to themselves"
]

twists = [
    "they caused the disaster themselves",
    "the world outside no longer exists",
    "the person they are searching for is actually them",
    "everything happened hundreds of years ago",
    "the supposed villain was protecting them",
    "they have been inside a simulation",
    "their memories belong to someone else",
    "the rescue signal came from the future",
    "they were never human",
    "escaping would actually cause the catastrophe"
]

moods = [
    "tense", "emotional", "eerie", "mysterious",
    "cinematic", "dark", "hopeful", "unsettling"
]

ending_styles = [
    "cliffhanger",
    "shocking reveal",
    "emotional reveal",
    "unanswered mystery",
    "unexpected victory"
]


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return []
    return []


def fingerprint(story):
    key = "|".join([
        story["genre"],
        story["setting"],
        story["character"],
        story["goal"],
        story["obstacle"],
        story["twist"]
    ])
    return hashlib.sha256(key.encode()).hexdigest()


history = load_history()

recent = history[-15:]

for _ in range(500):

    idea = {
        "genre": random.choice(genres),
        "setting": random.choice(settings),
        "character": random.choice(characters),
        "goal": random.choice(goals),
        "obstacle": random.choice(obstacles),
        "twist": random.choice(twists),
        "mood": random.choice(moods),
        "ending_style": random.choice(ending_styles)
    }

    fp = fingerprint(idea)

    # Never allow an exact previous story DNA
    if any(item.get("fingerprint") == fp for item in history):
        continue

    # Avoid repeating major ingredients too soon
    if recent:
        if sum(x.get("setting") == idea["setting"] for x in recent[-5:]) > 0:
            continue

        if sum(x.get("character") == idea["character"] for x in recent[-5:]) > 0:
            continue

        if sum(x.get("twist") == idea["twist"] for x in recent[-8:]) > 0:
            continue

    break

else:
    raise RuntimeError("Could not find a sufficiently unique story idea.")


title = f"The {random.choice(['Last', 'Hidden', 'Lost', 'Final', 'Silent', 'Unknown'])} {random.choice(['Signal', 'Door', 'Memory', 'Message', 'Station', 'Secret'])}"

story = {
    "title": title,
    **idea,

    "hook": (
        f"A {idea['character']} enters an {idea['setting']} "
        f"and discovers something is terribly wrong."
    ),

    "screenplay": (
        f"A {idea['character']} is trapped in an {idea['setting']}. "
        f"Their only goal is to {idea['goal']}. "
        f"But {idea['obstacle']}. "
        "Every clue makes the situation stranger. "
        f"Then the truth is revealed: {idea['twist']}. "
        "The story ends before the character fully understands what this means."
    ),

    "fingerprint": fp
}


Path("story.json").write_text(
    json.dumps(story, indent=2),
    encoding="utf-8"
)

history.append(story)

Path("story_history.json").write_text(
    json.dumps(history, indent=2),
    encoding="utf-8"
)

print("Generated unique story:")
print(json.dumps(story, indent=2))
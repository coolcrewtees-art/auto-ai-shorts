import json
import random
import hashlib
from pathlib import Path

HISTORY_FILE = Path("story_history.json")

CATEGORIES = [
    "indian_mythology",
    "indian_folktale",
    "indian_legend",
    "supernatural_mystery",
    "fantasy",
    "romance_drama",
    "comedy",
]

STORIES = [
    {
        "category": "indian_mythology",
        "title_hook": "The Warrior Who Gave Away His Invincibility",
        "topic": "Karna gives away his kavach and kundal",
        "main_figure": "Karna",
        "setting": "ancient India before the Kurukshetra war",
        "mood": "tragic, intense, heroic",
        "opening": "Karna knew the stranger asking for charity was no ordinary beggar.",
        "conflict": "The stranger wanted the divine armor and earrings Karna was born with, the very protection that made him almost impossible to kill.",
        "escalation": "Karna also understood what giving them away could mean in the war that was coming.",
        "dramatic_reveal": "But even after realizing that Indra had come in disguise, Karna still cut away his own protection and gave it to him.",
        "final_punch": "He became weaker as a warrior, and larger than life as a legend."
    },
    {
        "category": "indian_mythology",
        "title_hook": "The Curse That Was Worse Than Death",
        "topic": "Ashwatthama's curse",
        "main_figure": "Ashwatthama",
        "setting": "the final days of the Mahabharata war",
        "mood": "dark, haunting, supernatural",
        "opening": "The war was almost over, but Ashwatthama's anger was not.",
        "conflict": "Driven by revenge, he crossed a line that even a brutal battlefield could not excuse.",
        "escalation": "What followed was remembered not as another act of war, but as something much darker.",
        "dramatic_reveal": "According to tradition, Krishna did not grant him a warrior's death. Ashwatthama was cursed to wander in suffering.",
        "final_punch": "For him, death might have been mercy. The punishment was to keep living."
    },
    {
        "category": "indian_folktale",
        "title_hook": "The Bride Who Vanished Every Full Moon",
        "topic": "a mysterious village bride",
        "main_figure": "a newly married woman",
        "setting": "a remote Indian village beside an abandoned temple",
        "mood": "eerie, romantic, mysterious",
        "opening": "Every full moon, just before midnight, the new bride left her house without saying a word.",
        "conflict": "Her husband followed her one night and watched her disappear beside an abandoned temple in the forest.",
        "escalation": "The next morning she was back home, calm, smiling, and acting as if nothing had happened.",
        "dramatic_reveal": "Inside the temple, he found an old painting of the same woman wearing the same bridal clothes, dated more than a hundred years earlier.",
        "final_punch": "Under the painting were five words: she always comes back married."
    },
    {
        "category": "indian_folktale",
        "title_hook": "The Well That Whispered One Name",
        "topic": "a haunted village well",
        "main_figure": "a curious village boy",
        "setting": "an old village in Rajasthan",
        "mood": "mysterious, eerie, tense",
        "opening": "Every night, the abandoned well whispered the same name.",
        "conflict": "Nobody in the village admitted knowing who the name belonged to, and everyone warned the boy never to look inside.",
        "escalation": "One night he ignored them, leaned over the stone rim, and heard the whisper come from directly behind him.",
        "dramatic_reveal": "The name was his own, and carved into the wall of the well was a date from fifty years before he was born.",
        "final_punch": "The village had been waiting for him longer than he had been alive."
    },
    {
        "category": "indian_legend",
        "title_hook": "The King Who Played Chess With Death",
        "topic": "a legendary king bargaining with death",
        "main_figure": "a proud king",
        "setting": "an ancient hill kingdom in India",
        "mood": "mythic, clever, ominous",
        "opening": "A king was told he would die before sunrise.",
        "conflict": "Instead of praying, he challenged the messenger of death to a game of chess and demanded one extra hour for every piece he captured.",
        "escalation": "The game stretched through the night, and the king began to believe he had outsmarted fate itself.",
        "dramatic_reveal": "When the final piece fell, the sun rose, and the king smiled, until he realized the board had been his own funeral clock.",
        "final_punch": "He had not delayed death. He had spent his last hours playing with it."
    },
    {
        "category": "indian_legend",
        "title_hook": "The Queen Who Never Appeared in a Mirror",
        "topic": "a cursed queen legend",
        "main_figure": "a mysterious queen",
        "setting": "a forgotten palace in the Aravalli hills",
        "mood": "royal, eerie, tragic",
        "opening": "Servants noticed something terrifying about the queen: no mirror in the palace showed her reflection.",
        "conflict": "The king ordered every mirror destroyed, but rumors spread that she had made a bargain to stay young forever.",
        "escalation": "Years passed, everyone around her aged, and the queen looked exactly the same.",
        "dramatic_reveal": "When the palace finally fell into ruin, workers found one untouched mirror in a sealed room, and inside it was an old woman screaming to get out.",
        "final_punch": "The queen had never escaped age. She had only trapped it somewhere else."
    },
    {
        "category": "supernatural_mystery",
        "title_hook": "The Hotel Room That Called Its Own Guests",
        "topic": "a haunted hotel room",
        "main_figure": "a night receptionist",
        "setting": "an isolated mountain hotel",
        "mood": "creepy, suspenseful, modern",
        "opening": "Every night at 3:07, the front desk phone rang from room 307.",
        "conflict": "The problem was that room 307 had been locked and empty for years.",
        "escalation": "One night the receptionist answered, and a terrified voice whispered his name and told him not to open the lobby door.",
        "dramatic_reveal": "Seconds later, someone outside started knocking, and through the glass he saw himself standing there.",
        "final_punch": "The call had not come from an empty room. It had come from a warning he had not lived through yet."
    },
    {
        "category": "supernatural_mystery",
        "title_hook": "The Train That Had No Final Station",
        "topic": "a supernatural night train",
        "main_figure": "a tired traveler",
        "setting": "a lonely railway line at night",
        "mood": "dreamlike, unsettling, mysterious",
        "opening": "A traveler boarded the last train home and noticed every passenger was completely silent.",
        "conflict": "Station after station passed, but none of the names existed on his map.",
        "escalation": "When he asked the conductor where the train ended, the conductor quietly asked why he thought he was still alive.",
        "dramatic_reveal": "The traveler looked out the window and saw his own crashed car beside the railway line.",
        "final_punch": "He had not boarded the wrong train. He had boarded the last one."
    },
    {
        "category": "fantasy",
        "title_hook": "The King Who Could Hear Every Lie",
        "topic": "a cursed king who hears lies as screams",
        "main_figure": "a young king",
        "setting": "an ancient mountain kingdom",
        "mood": "dark fantasy, tense, mysterious",
        "opening": "The king's gift sounded perfect: every lie sounded like a scream.",
        "conflict": "At first, nobody could deceive him.",
        "escalation": "Then the screams became constant: advisers, friends, servants, even his own family.",
        "dramatic_reveal": "The loudest scream came when he looked into a mirror and said, I am a good king.",
        "final_punch": "The curse was never meant to expose everyone else. It was meant to expose him."
    },
    {
        "category": "fantasy",
        "title_hook": "The Dragon Guarded an Empty Vault",
        "topic": "a dragon guarding an empty vault",
        "main_figure": "a thief",
        "setting": "a ruined mountain fortress",
        "mood": "adventurous, mysterious, dark",
        "opening": "For three hundred years, a dragon guarded the same vault.",
        "conflict": "Everyone believed unimaginable treasure was inside, and one thief spent years preparing to steal it.",
        "escalation": "He survived traps, fire, and the dragon itself just to reach the door.",
        "dramatic_reveal": "When he opened the vault, it was empty. The dragon had been guarding the world from what used to be inside.",
        "final_punch": "The dragon was never guarding treasure. The dragon was the lock."
    },
    {
        "category": "romance_drama",
        "title_hook": "She Waited at the Same Station for Twenty Years",
        "topic": "a tragic railway station romance",
        "main_figure": "a woman waiting for her first love",
        "setting": "an old railway station",
        "mood": "emotional, bittersweet, cinematic",
        "opening": "Every year on the same date, she returned to the same railway platform.",
        "conflict": "Years earlier, the man she loved had promised to meet her there after leaving for work.",
        "escalation": "He never returned, but she never stopped believing there had been a reason.",
        "dramatic_reveal": "Two decades later, a stranger brought her an unopened letter found among his belongings after his death.",
        "final_punch": "He had never forgotten the meeting. He simply never lived long enough to return."
    },
    {
        "category": "romance_drama",
        "title_hook": "He Fell in Love With a Woman Who Only Existed at Midnight",
        "topic": "a supernatural romance",
        "main_figure": "a lonely prince",
        "setting": "a moonlit palace garden",
        "mood": "romantic, magical, melancholic",
        "opening": "Every night at midnight, the same woman appeared in the palace garden.",
        "conflict": "The prince fell in love with her, but she vanished every sunrise and refused to explain why.",
        "escalation": "He searched every village and every royal record, but nobody alive had ever seen her.",
        "dramatic_reveal": "Then he found her portrait in a sealed room, painted exactly one hundred years earlier.",
        "final_punch": "He had fallen in love with someone the moon refused to let die."
    },
    {
        "category": "comedy",
        "title_hook": "The Thief Who Accidentally Became Royal Adviser",
        "topic": "a thief mistaken for a strategist",
        "main_figure": "an unlucky thief",
        "setting": "a chaotic medieval kingdom",
        "mood": "funny, absurd, fast-paced",
        "opening": "A thief broke into the royal palace to steal gold and walked out with a government job.",
        "conflict": "Guards caught him hiding behind a war map, and the king assumed he was a secret military strategist.",
        "escalation": "Too scared to admit the truth, he started giving random advice.",
        "dramatic_reveal": "By pure luck, one ridiculous suggestion actually worked and saved the kingdom.",
        "final_punch": "He never stole the crown jewels. Somehow, he stole a career instead."
    },
    {
        "category": "comedy",
        "title_hook": "The Wizard Who Won by Forgetting His Spell",
        "topic": "a forgetful wizard",
        "main_figure": "an overconfident wizard",
        "setting": "a magical academy",
        "mood": "absurd, playful, chaotic",
        "opening": "The most famous wizard in the kingdom entered a duel and forgot the spell everyone came to see.",
        "conflict": "His opponent immediately realized something was wrong.",
        "escalation": "The wizard pretended everything was planned while accidentally turning furniture into chickens.",
        "dramatic_reveal": "His opponent surrendered because he thought the chaos was terrifying advanced magic.",
        "final_punch": "He won using the oldest trick in magic: confidently having no idea what he was doing."
    },
]


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def fingerprint(item):
    raw = f"{item['category']}|{item['topic']}|{item['title_hook']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def choose_story(history):
    used = {item.get("fingerprint") for item in history}
    recent_topics = {item.get("topic") for item in history[-10:]}

    category = random.choice(CATEGORIES)

    candidates = [
        s for s in STORIES
        if s["category"] == category
        and fingerprint(s) not in used
        and s["topic"] not in recent_topics
    ]

    if not candidates:
        candidates = [
            s for s in STORIES
            if s["category"] == category
            and s["topic"] not in recent_topics
        ]

    if not candidates:
        candidates = [
            s for s in STORIES
            if s["category"] == category
        ]

    return random.choice(candidates)


def build_story(item):
    return {
        "title_hook": item["title_hook"],
        "category": item["category"],
        "topic": item["topic"],
        "main_figure": item["main_figure"],
        "setting": item["setting"],
        "mood": item["mood"],
        "opening": item["opening"],
        "conflict": item["conflict"],
        "escalation": item["escalation"],
        "dramatic_reveal": item["dramatic_reveal"],
        "final_punch": item["final_punch"],
        "screenplay": " ".join([
            item["title_hook"] + ".",
            item["opening"],
            item["conflict"],
            item["escalation"],
            item["dramatic_reveal"],
            item["final_punch"],
        ]),
        "fingerprint": fingerprint(item)
    }


history = load_history()
story = build_story(choose_story(history))

Path("story.json").write_text(
    json.dumps(story, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

history.append(story)

Path("story_history.json").write_text(
    json.dumps(history, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Generated story:")
print(json.dumps(story, indent=2, ensure_ascii=False))
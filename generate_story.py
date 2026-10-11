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
    # ========================================================
    # INDIAN MYTHOLOGY
    # ========================================================

    {
        "category": "indian_mythology",
        "title_hook": "The Curse Worse Than Death",
        "topic": "Ashwatthama's curse",
        "main_figure": "Ashwatthama",
        "setting": "the final night of the Mahabharata war",
        "mood": "dark, haunting, intense",

        "opening": (
            "The war was almost over. "
            "But Ashwatthama wanted revenge."
        ),

        "conflict": (
            "And that night... he crossed a line even war could not excuse."
        ),

        "escalation": (
            "Everyone expected Krishna to kill him."
        ),

        "dramatic_reveal": (
            "He didn't. "
            "According to tradition, Krishna cursed him to keep living... and suffering."
        ),

        "final_punch": (
            "For Ashwatthama, death would have been mercy."
        ),
    },

    {
        "category": "indian_mythology",
        "title_hook": "Karna Gave Away His Invincibility",
        "topic": "Karna gives away his divine armor",
        "main_figure": "Karna",
        "setting": "ancient India before the Kurukshetra war",
        "mood": "heroic, tragic, intense",

        "opening": (
            "Karna knew the beggar standing before him was hiding something."
        ),

        "conflict": (
            "The man wanted Karna's divine armor... the armor protecting his life."
        ),

        "escalation": (
            "And Karna knew giving it away could get him killed."
        ),

        "dramatic_reveal": (
            "He gave it away anyway. "
            "The beggar was Indra himself."
        ),

        "final_punch": (
            "Karna became weaker that day... but his legend became stronger."
        ),
    },

    {
        "category": "indian_mythology",
        "title_hook": "Hanuman Couldn't Find the Herb",
        "topic": "Hanuman carries the mountain",
        "main_figure": "Hanuman",
        "setting": "the war in Lanka",
        "mood": "urgent, heroic, spectacular",

        "opening": (
            "Lakshmana was dying. "
            "Only one herb could save him."
        ),

        "conflict": (
            "Hanuman reached the mountain... but couldn't identify it."
        ),

        "escalation": (
            "There was no time to make a mistake."
        ),

        "dramatic_reveal": (
            "So he stopped searching... and lifted the entire mountain."
        ),

        "final_punch": (
            "When one herb was impossible to find, Hanuman brought them all."
        ),
    },

    # ========================================================
    # INDIAN FOLKTALES
    # ========================================================

    {
        "category": "indian_folktale",
        "title_hook": "The Bride Who Vanished Every Full Moon",
        "topic": "the disappearing village bride",
        "main_figure": "a mysterious newly married woman",
        "setting": "a remote Indian village beside an abandoned temple",
        "mood": "eerie, mysterious, supernatural",

        "opening": (
            "Every full moon... the new bride disappeared."
        ),

        "conflict": (
            "Her husband followed her into the forest one night."
        ),

        "escalation": (
            "She walked toward an abandoned temple... and vanished."
        ),

        "dramatic_reveal": (
            "Inside, he found her portrait. "
            "It had been painted a hundred years earlier."
        ),

        "final_punch": (
            "Under it were five words... she always comes back married."
        ),
    },

    {
        "category": "indian_folktale",
        "title_hook": "The Well That Knew His Name",
        "topic": "the haunted village well",
        "main_figure": "a curious village boy",
        "setting": "an old village in Rajasthan",
        "mood": "creepy, mysterious, tense",

        "opening": (
            "Every night, the abandoned well whispered one name."
        ),

        "conflict": (
            "Nobody would tell the boy whose name it was."
        ),

        "escalation": (
            "So one night... he looked inside."
        ),

        "dramatic_reveal": (
            "The whisper said his name. "
            "And it was carved inside the well... fifty years before he was born."
        ),

        "final_punch": (
            "The village had been waiting for him longer than he'd been alive."
        ),
    },

    # ========================================================
    # INDIAN LEGENDS
    # ========================================================

    {
        "category": "indian_legend",
        "title_hook": "The Queen With No Reflection",
        "topic": "the queen trapped inside a mirror",
        "main_figure": "a mysterious queen",
        "setting": "a forgotten palace in the Aravalli hills",
        "mood": "royal, eerie, tragic",

        "opening": (
            "There was one strange thing about the queen."
        ),

        "conflict": (
            "No mirror in the palace showed her reflection."
        ),

        "escalation": (
            "Years passed. Everyone aged... except her."
        ),

        "dramatic_reveal": (
            "Then workers opened a sealed room. "
            "Inside one mirror... an old woman was screaming to get out."
        ),

        "final_punch": (
            "The queen hadn't escaped age. She had trapped it."
        ),
    },

    {
        "category": "indian_legend",
        "title_hook": "The King Who Challenged Death",
        "topic": "the king who plays chess with death",
        "main_figure": "a proud king",
        "setting": "an ancient Indian hill kingdom",
        "mood": "ominous, clever, legendary",

        "opening": (
            "A king was told he would die before sunrise."
        ),

        "conflict": (
            "So he challenged Death to a game of chess."
        ),

        "escalation": (
            "Every captured piece bought him more time."
        ),

        "dramatic_reveal": (
            "The sun finally rose... and the king smiled. "
            "Then Death showed him the board."
        ),

        "final_punch": (
            "It wasn't a game. It had been counting down his final hours."
        ),
    },

    # ========================================================
    # SUPERNATURAL / MYSTERY
    # ========================================================

    {
        "category": "supernatural_mystery",
        "title_hook": "Room 307 Called the Front Desk",
        "topic": "the haunted hotel room",
        "main_figure": "a night receptionist",
        "setting": "an isolated mountain hotel",
        "mood": "creepy, suspenseful, modern",

        "opening": (
            "Every night at 3:07... room 307 called reception."
        ),

        "conflict": (
            "There was just one problem. "
            "Room 307 had been locked for years."
        ),

        "escalation": (
            "One night, the receptionist finally answered."
        ),

        "dramatic_reveal": (
            "The voice whispered... don't open the front door. "
            "Then someone started knocking."
        ),

        "final_punch": (
            "Through the glass... he saw himself standing outside."
        ),
    },

    {
        "category": "supernatural_mystery",
        "title_hook": "The Train With No Final Station",
        "topic": "the supernatural night train",
        "main_figure": "a tired traveler",
        "setting": "a lonely railway line at night",
        "mood": "unsettling, mysterious, dreamlike",

        "opening": (
            "He boarded the last train home."
        ),

        "conflict": (
            "But none of the stations existed on his map."
        ),

        "escalation": (
            "Then the conductor asked him one strange question..."
        ),

        "dramatic_reveal": (
            "Why do you think you're still alive? "
            "Outside the window... he saw his own crashed car."
        ),

        "final_punch": (
            "He hadn't boarded the wrong train. He'd boarded the last one."
        ),
    },

    # ========================================================
    # FANTASY
    # ========================================================

    {
        "category": "fantasy",
        "title_hook": "The King Who Could Hear Every Lie",
        "topic": "the king cursed to hear lies",
        "main_figure": "a young king",
        "setting": "an ancient mountain kingdom",
        "mood": "dark fantasy, tense, mysterious",

        "opening": (
            "The king had one incredible gift."
        ),

        "conflict": (
            "Whenever somebody lied... he heard a scream."
        ),

        "escalation": (
            "Soon the palace became deafening."
        ),

        "dramatic_reveal": (
            "Then he looked into a mirror and said... I'm a good king. "
            "The loudest scream came from himself."
        ),

        "final_punch": (
            "The curse was never meant to expose them. It was meant to expose him."
        ),
    },

    {
        "category": "fantasy",
        "title_hook": "The Dragon Guarded an Empty Vault",
        "topic": "the dragon guarding the forbidden vault",
        "main_figure": "a fearless thief",
        "setting": "a ruined mountain fortress",
        "mood": "dark, adventurous, mysterious",

        "opening": (
            "For three hundred years, a dragon guarded one vault."
        ),

        "conflict": (
            "Everyone assumed unimaginable treasure was inside."
        ),

        "escalation": (
            "One thief finally defeated the dragon... and opened it."
        ),

        "dramatic_reveal": (
            "The vault was empty. "
            "The dragon wasn't protecting the treasure."
        ),

        "final_punch": (
            "It was protecting the world from whatever had escaped."
        ),
    },

    # ========================================================
    # ROMANCE DRAMA
    # ========================================================

    {
        "category": "romance_drama",
        "title_hook": "She Waited Twenty Years",
        "topic": "the railway station love letter",
        "main_figure": "a woman waiting for her first love",
        "setting": "an old railway station",
        "mood": "emotional, bittersweet, cinematic",

        "opening": (
            "Every year... she returned to the same railway platform."
        ),

        "conflict": (
            "Twenty years earlier, he had promised to meet her there."
        ),

        "escalation": (
            "He never came."
        ),

        "dramatic_reveal": (
            "Then a stranger handed her an unopened letter... found after his death."
        ),

        "final_punch": (
            "He never forgot her. He simply never lived long enough to return."
        ),
    },

    {
        "category": "romance_drama",
        "title_hook": "She Only Existed After Midnight",
        "topic": "the midnight palace romance",
        "main_figure": "a lonely prince",
        "setting": "a moonlit palace garden",
        "mood": "romantic, magical, melancholic",

        "opening": (
            "Every midnight, the same woman appeared in the palace garden."
        ),

        "conflict": (
            "The prince fell in love with her."
        ),

        "escalation": (
            "But every sunrise... she disappeared."
        ),

        "dramatic_reveal": (
            "Then he found her portrait in a sealed room. "
            "It was painted a hundred years earlier."
        ),

        "final_punch": (
            "He had fallen in love with someone the moon refused to forget."
        ),
    },

    # ========================================================
    # COMEDY
    # ========================================================

    {
        "category": "comedy",
        "title_hook": "The Thief Who Accidentally Got a Government Job",
        "topic": "the thief mistaken for a royal strategist",
        "main_figure": "an unlucky thief",
        "setting": "a chaotic medieval kingdom",
        "mood": "fast, absurd, playful",

        "opening": (
            "A thief broke into the palace to steal gold."
        ),

        "conflict": (
            "Guards caught him hiding behind a war map."
        ),

        "escalation": (
            "The king assumed he was a secret military genius."
        ),

        "dramatic_reveal": (
            "Too scared to confess, the thief gave completely random advice... and it worked."
        ),

        "final_punch": (
            "He failed to steal the gold. Somehow, he stole a career."
        ),
    },

    {
        "category": "comedy",
        "title_hook": "The Wizard Who Forgot His Spell",
        "topic": "the wizard who accidentally wins",
        "main_figure": "an overconfident wizard",
        "setting": "a magical academy",
        "mood": "chaotic, funny, playful",

        "opening": (
            "The kingdom's greatest wizard entered a duel."
        ),

        "conflict": (
            "Then he forgot his spell."
        ),

        "escalation": (
            "He panicked... and accidentally turned the furniture into chickens."
        ),

        "dramatic_reveal": (
            "His opponent thought it was terrifying advanced magic... and surrendered."
        ),

        "final_punch": (
            "He won by confidently having absolutely no idea what he was doing."
        ),
    },
]


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(
            HISTORY_FILE.read_text(encoding="utf-8")
        )

        return data if isinstance(data, list) else []

    except Exception:
        return []


def fingerprint(item):
    raw = (
        f"{item['category']}|"
        f"{item['topic']}|"
        f"{item['title_hook']}"
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def choose_story(history):

    used = {
        item.get("fingerprint")
        for item in history
    }

    recent_topics = {
        item.get("topic")
        for item in history[-10:]
    }

    # Every category has exactly the same chance.
    category = random.choice(CATEGORIES)

    choices = [
        item
        for item in STORIES
        if item["category"] == category
        and fingerprint(item) not in used
        and item["topic"] not in recent_topics
    ]

    if not choices:
        choices = [
            item
            for item in STORIES
            if item["category"] == category
            and item["topic"] not in recent_topics
        ]

    if not choices:
        choices = [
            item
            for item in STORIES
            if item["category"] == category
        ]

    return random.choice(choices)


def build_story(item):

    # Caption/display version.
    screenplay = " ".join([
        item["title_hook"] + ".",
        item["opening"],
        item["conflict"],
        item["escalation"],
        item["dramatic_reveal"],
        item["final_punch"],
    ])

    return {
        **item,
        "screenplay": screenplay,
        "fingerprint": fingerprint(item),
    }


history = load_history()

chosen = choose_story(history)
story = build_story(chosen)

Path("story.json").write_text(
    json.dumps(
        story,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

history.append(story)

Path("story_history.json").write_text(
    json.dumps(
        history,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

word_count = len(
    story["screenplay"].split()
)

print("")
print("==============================")
print("FAST SHORT-FORM STORY CREATED")
print("==============================")
print("Category:", story["category"])
print("Title:", story["title_hook"])
print("Words:", word_count)
print("")
print(story["screenplay"])
print("==============================")
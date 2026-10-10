import json
import random
import hashlib
from pathlib import Path

HISTORY_FILE = Path("story_history.json")

STORIES = [
    {
        "category": "indian_mythology",
        "title": "Karna Knew He Was Being Tricked",
        "topic": "Karna gives away his kavach and kundal",
        "main_figure": "Karna",
        "setting": "ancient India before the Kurukshetra war",
        "mood": "tragic, intense, heroic",
        "hook": "Karna knew the man asking for his armor was not an ordinary beggar.",
        "conflict": "He understood that giving away his divine armor and earrings could leave him vulnerable in the coming war.",
        "escalation": "But Karna had built his identity around never refusing someone who came to him asking for charity.",
        "twist": "So even after realizing that Indra had come in disguise, Karna still removed the protection from his own body and gave it away.",
        "final_line": "He became weaker as a warrior, but greater as a legend."
    },
    {
        "category": "indian_mythology",
        "title": "Krishna Gave Ashwatthama a Fate Worse Than Death",
        "topic": "Ashwatthama's curse",
        "main_figure": "Ashwatthama",
        "setting": "the final days of the Mahabharata war",
        "mood": "dark, haunting, supernatural",
        "hook": "The war was almost over, but Ashwatthama wanted revenge badly enough to cross a line nobody could forgive.",
        "conflict": "Driven by rage after his father's death, he attacked when his enemies were least prepared.",
        "escalation": "What followed was remembered not as another act of war, but as something far darker.",
        "twist": "According to tradition, Krishna cursed Ashwatthama to wander the earth in suffering instead of granting him a warrior's death.",
        "final_line": "For Ashwatthama, death might have been mercy. The punishment was to keep living."
    },
    {
        "category": "indian_mythology",
        "title": "Hanuman Didn't Know Which Herb to Take",
        "topic": "Hanuman carrying the mountain",
        "main_figure": "Hanuman",
        "setting": "the war in Lanka",
        "mood": "heroic, urgent, spectacular",
        "hook": "Lakshmana was dying, and Hanuman had one job: bring back the herb that could save him.",
        "conflict": "When Hanuman reached the mountain, he could not identify the exact herb.",
        "escalation": "Every second mattered, and choosing the wrong plant could cost Lakshmana his life.",
        "twist": "So Hanuman stopped trying to choose and carried the entire mountain back.",
        "final_line": "When the mission mattered more than the method, Hanuman simply moved the mountain."
    },
    {
        "category": "indian_mythology",
        "title": "Shiva Drank What Could Destroy Everything",
        "topic": "Shiva drinks Halahala",
        "main_figure": "Lord Shiva",
        "setting": "the cosmic churning of the ocean",
        "mood": "cosmic, intense, divine",
        "hook": "Before the nectar of immortality appeared, something far more dangerous came out first.",
        "conflict": "A deadly poison emerged from the cosmic ocean and threatened gods, demons, and the world itself.",
        "escalation": "Nobody could safely contain it, and the danger kept spreading.",
        "twist": "Shiva drank the poison and held it in his throat, which turned blue.",
        "final_line": "That is why Neelkanth became a symbol of taking suffering upon oneself to protect others."
    },
    {
        "category": "indian_history",
        "title": "Shivaji Walked Into Agra and Realized He Was Trapped",
        "topic": "Shivaji's escape from Agra",
        "main_figure": "Chhatrapati Shivaji Maharaj",
        "setting": "Agra during the Mughal era",
        "mood": "tense, clever, rebellious",
        "hook": "Shivaji entered Agra expecting diplomacy. Very quickly, he realized he was effectively trapped.",
        "conflict": "His movements were restricted, and simply walking out was no longer an option.",
        "escalation": "The longer he stayed, the more dangerous the situation became, so escape had to rely on deception rather than force.",
        "twist": "Popular accounts describe a daring escape built on concealment and misdirection rather than a direct battle.",
        "final_line": "The remarkable part was not that he fought his way out. It was that he outthought the prison around him."
    },
    {
        "category": "indian_history",
        "title": "Ashoka Won Kalinga and Hated What He Saw",
        "topic": "Ashoka after Kalinga",
        "main_figure": "Emperor Ashoka",
        "setting": "the battlefield of Kalinga",
        "mood": "grim, reflective, powerful",
        "hook": "Ashoka won the war. Then he saw what victory had actually cost.",
        "conflict": "The Kalinga campaign brought enormous suffering, death, and displacement.",
        "escalation": "For a ruler known for conquest, the battlefield became something impossible to ignore.",
        "twist": "After Kalinga, Ashoka increasingly turned toward dhamma, moral governance, and Buddhist ideals.",
        "final_line": "He conquered Kalinga with an army, but Kalinga changed the emperor."
    },
    {
        "category": "indian_history",
        "title": "Maharana Pratap Lost the Field, Not the Fight",
        "topic": "Maharana Pratap after Haldighati",
        "main_figure": "Maharana Pratap",
        "setting": "Mewar after the Battle of Haldighati",
        "mood": "defiant, rugged, heroic",
        "hook": "Haldighati was brutal, but the real story of Maharana Pratap did not end with that battle.",
        "conflict": "He faced military pressure, loss of territory, and years of hardship.",
        "escalation": "Instead of surrendering, he continued resistance from difficult terrain and rebuilt his position.",
        "twist": "He later recovered significant parts of Mewar.",
        "final_line": "His legend was built not on one battle, but on refusing to disappear after it."
    },
    {
        "category": "indian_history",
        "title": "The Cholas Didn't Stop at India's Coast",
        "topic": "Rajendra Chola's naval campaign",
        "main_figure": "Rajendra Chola I",
        "setting": "the Bay of Bengal and Southeast Asian trade routes",
        "mood": "grand, adventurous, powerful",
        "hook": "A medieval Indian empire once sent fleets across the sea to project power far beyond the subcontinent.",
        "conflict": "Control of maritime trade routes mattered enormously, and the Cholas had the naval strength to act.",
        "escalation": "Their fleets crossed the Bay of Bengal and struck targets connected to powerful Southeast Asian trading networks.",
        "twist": "The Chola Empire was not only a land power famous for temples. It was also capable of major overseas operations.",
        "final_line": "For a moment in medieval history, Indian power travelled by sea."
    },
    {
        "category": "international_history",
        "title": "Napoleon Invaded Russia With an Army and Returned With a Warning",
        "topic": "Napoleon's invasion of Russia",
        "main_figure": "Napoleon Bonaparte",
        "setting": "Russia in 1812",
        "mood": "massive, bleak, dramatic",
        "hook": "Napoleon entered Russia with an enormous army. Most of it would never return.",
        "conflict": "Russian forces avoided giving him the clean victory he wanted while retreating deeper into the country.",
        "escalation": "Supplies failed, distance grew, and winter turned every mile into a disaster.",
        "twist": "The campaign became less about defeating Russia and more about surviving the retreat.",
        "final_line": "Napoleon invaded with soldiers. Russia answered with distance, fire, hunger, and cold."
    },
    {
        "category": "international_history",
        "title": "The City That Vanished Under Ash",
        "topic": "Pompeii and Mount Vesuvius",
        "main_figure": "the people of Pompeii",
        "setting": "Pompeii in 79 CE",
        "mood": "eerie, catastrophic, tragic",
        "hook": "A normal Roman city woke up one morning with no idea it was about to disappear.",
        "conflict": "Mount Vesuvius erupted, filling the sky with ash and volcanic debris.",
        "escalation": "People tried to escape as darkness, heat, and falling material overwhelmed the city.",
        "twist": "Centuries later, the destruction preserved buildings and traces of daily life with haunting detail.",
        "final_line": "Pompeii was destroyed in hours, but that destruction froze part of its world in time."
    },
    {
        "category": "fantasy",
        "title": "The King Who Could Hear Lies",
        "topic": "a cursed king who hears lies as screams",
        "main_figure": "a young king",
        "setting": "an ancient mountain kingdom",
        "mood": "dark fantasy, tense, mysterious",
        "hook": "The king's gift sounded perfect: every time someone lied, he heard a scream.",
        "conflict": "At first, it made him almost impossible to deceive.",
        "escalation": "Then the screams became constant — advisers, friends, servants, even his own family.",
        "twist": "The loudest scream came when he looked into a mirror and said, 'I am a good king.'",
        "final_line": "The curse was never meant to expose everyone else. It was meant to expose him."
    },
    {
        "category": "fantasy",
        "title": "The Dragon Guarded Nothing",
        "topic": "a dragon guarding an empty vault",
        "main_figure": "a thief",
        "setting": "a ruined mountain fortress",
        "mood": "adventurous, mysterious, ironic",
        "hook": "For three hundred years, a dragon guarded the same vault. Everyone assumed unimaginable treasure was inside.",
        "conflict": "A thief spent years preparing to steal it.",
        "escalation": "He survived traps, fire, and the dragon itself just to reach the door.",
        "twist": "When he opened the vault, it was empty. The dragon had been guarding the world from what used to be inside.",
        "final_line": "The treasure was never what the dragon protected. The dragon was the lock."
    },
    {
        "category": "romance_drama",
        "title": "She Waited at the Same Station for 20 Years",
        "topic": "a tragic railway station romance",
        "main_figure": "a woman waiting for her first love",
        "setting": "an old railway station",
        "mood": "emotional, bittersweet, cinematic",
        "hook": "Every year on the same date, she returned to the same railway platform.",
        "conflict": "Years earlier, the man she loved had promised to meet her there after leaving for work.",
        "escalation": "He never returned, but she never stopped believing there had been a reason.",
        "twist": "Years later, a stranger brought her an unopened letter found among his belongings after his death.",
        "final_line": "He had never forgotten the meeting. He simply never lived long enough to return."
    },
    {
        "category": "comedy",
        "title": "The Thief Who Accidentally Became Royal Adviser",
        "topic": "a thief mistaken for a genius strategist",
        "main_figure": "an unlucky thief",
        "setting": "a chaotic medieval kingdom",
        "mood": "funny, absurd, fast-paced",
        "hook": "A thief broke into the royal palace to steal gold and walked out with a government job.",
        "conflict": "Guards caught him hiding behind a war map, and the king assumed he was a secret military strategist.",
        "escalation": "Too scared to admit the truth, the thief started giving random advice.",
        "twist": "By pure luck, one ridiculous suggestion actually worked and saved the kingdom.",
        "final_line": "He never stole the crown jewels. Somehow, he stole a career instead."
    },
    {
        "category": "comedy",
        "title": "The Wizard Who Forgot His Own Spell",
        "topic": "a forgetful wizard",
        "main_figure": "an overconfident wizard",
        "setting": "a magical academy",
        "mood": "absurd, playful, chaotic",
        "hook": "The most famous wizard in the kingdom entered a duel and forgot the spell everyone came to see.",
        "conflict": "His opponent immediately realized something was wrong.",
        "escalation": "The wizard pretended everything was planned while accidentally turning furniture into chickens.",
        "twist": "His opponent surrendered because he thought the chaos was terrifying advanced magic.",
        "final_line": "He won using the oldest trick in magic: confidently having no idea what he was doing."
    }
]

CATEGORY_WEIGHTS = {
    "indian_mythology": 40,
    "indian_history": 25,
    "international_history": 15,
    "fantasy": 10,
    "romance_drama": 5,
    "comedy": 5
}


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
        f"{item['title']}"
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def weighted_category():
    names = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())

    return random.choices(
        names,
        weights=weights,
        k=1
    )[0]


def choose_story(history):
    used = {
        item.get("fingerprint")
        for item in history
    }

    for _ in range(100):
        category = weighted_category()

        options = [
            item
            for item in STORIES
            if item["category"] == category
            and fingerprint(item) not in used
        ]

        if options:
            return random.choice(options)

    recent_topics = {
        item.get("topic")
        for item in history[-10:]
    }

    options = [
        item
        for item in STORIES
        if item["topic"] not in recent_topics
    ]

    return random.choice(
        options or STORIES
    )


def build_screenplay(item):
    return " ".join([
        item["hook"],
        item["conflict"],
        item["escalation"],
        item["twist"],
        item["final_line"]
    ])


def build_beats(item):
    return [
        {
            "type": "hook",
            "text": item["hook"]
        },
        {
            "type": "conflict",
            "text": item["conflict"]
        },
        {
            "type": "escalation",
            "text": item["escalation"]
        },
        {
            "type": "twist",
            "text": item["twist"]
        },
        {
            "type": "ending",
            "text": item["final_line"]
        }
    ]


history = load_history()

chosen = choose_story(history)

fp = fingerprint(chosen)

story = {
    **chosen,
    "screenplay": build_screenplay(chosen),
    "beats": build_beats(chosen),
    "fingerprint": fp
}

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

print("Generated high-drama story:")
print(
    json.dumps(
        story,
        indent=2,
        ensure_ascii=False
    )
)
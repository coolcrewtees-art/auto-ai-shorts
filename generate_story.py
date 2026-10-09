import json
import random
import hashlib
from pathlib import Path

HISTORY_FILE = Path("story_history.json")

# --------------------------------------------------
# Content pools
# --------------------------------------------------

MYTHOLOGY_TOPICS = [
    {
        "category": "mythology",
        "title": "Why Bhishma Chose the Bed of Arrows",
        "topic": "Bhishma on the bed of arrows",
        "main_figure": "Bhishma",
        "setting": "the battlefield of Kurukshetra",
        "era": "Mahabharata era",
        "mood": "solemn and epic",
        "hook": "Why would a warrior choose to remain alive on a bed of arrows?",
        "summary": (
            "After being struck down in Kurukshetra, Bhishma did not die immediately. "
            "Because of the boon of choosing the time of his death, he remained on a bed of arrows, "
            "waiting for the right cosmic moment. Even in pain, he continued teaching dharma and statecraft."
        ),
        "reveal": "His final act was not about survival, but about duty, wisdom, and timing.",
        "ending": "That is why Bhishma’s bed of arrows became one of the most powerful moments in Indian mythology."
    },
    {
        "category": "mythology",
        "title": "The Mystery of Ashwatthama’s Curse",
        "topic": "Ashwatthama's curse",
        "main_figure": "Ashwatthama",
        "setting": "the aftermath of the Mahabharata war",
        "era": "Mahabharata era",
        "mood": "dark and haunting",
        "hook": "What if one warrior from the Mahabharata was cursed to wander forever?",
        "summary": (
            "Ashwatthama, the son of Dronacharya, committed a horrifying act after the war. "
            "As punishment, Krishna cursed him with endless suffering and eternal wandering. "
            "In many traditions, he is said to still roam the earth, carrying the burden of his actions."
        ),
        "reveal": "His story is remembered not as a victory, but as a warning about rage and revenge.",
        "ending": "That is why Ashwatthama remains one of the most mysterious and tragic figures in Indian mythology."
    },
    {
        "category": "mythology",
        "title": "How Hanuman Brought the Mountain",
        "topic": "Hanuman and the Sanjeevani mountain",
        "main_figure": "Hanuman",
        "setting": "the war in Lanka",
        "era": "Ramayana era",
        "mood": "heroic and fast-paced",
        "hook": "Why did Hanuman carry an entire mountain instead of one herb?",
        "summary": (
            "When Lakshmana was struck down in battle, only the Sanjeevani herb could save him. "
            "Hanuman was sent to fetch it, but when he could not identify the exact herb, "
            "he lifted the whole mountain and brought it back. His strength was matched by his devotion."
        ),
        "reveal": "The moment is legendary because Hanuman chose certainty over delay when a life was at stake.",
        "ending": "That is why the image of Hanuman carrying the mountain became a symbol of unstoppable devotion."
    },
    {
        "category": "mythology",
        "title": "Why Karna Gave Away His Armor",
        "topic": "Karna giving away his kavach and kundal",
        "main_figure": "Karna",
        "setting": "before the Kurukshetra war",
        "era": "Mahabharata era",
        "mood": "tragic and noble",
        "hook": "Why would a warrior give away the very armor that made him nearly invincible?",
        "summary": (
            "Karna was born with divine armor and earrings that protected him. "
            "Indra, knowing Karna’s power, came disguised as a Brahmin and asked for them as alms. "
            "Even though Karna understood the danger, he still gave them away, staying true to his vow of generosity."
        ),
        "reveal": "That decision made him more vulnerable in battle, but greater in legend.",
        "ending": "That is why Karna is remembered not only as a warrior, but also as one of the greatest givers in mythology."
    },
    {
        "category": "mythology",
        "title": "The Vow That Created Bhishma",
        "topic": "Devavrata becoming Bhishma",
        "main_figure": "Devavrata",
        "setting": "the court of Hastinapura",
        "era": "Mahabharata era",
        "mood": "grand and emotional",
        "hook": "What kind of vow is so terrifying that it changes a prince’s name forever?",
        "summary": (
            "Devavrata was the rightful heir to Hastinapura, but to fulfill his father Shantanu’s wish, "
            "he gave up the throne and also swore lifelong celibacy. "
            "The vow was so severe that the gods themselves were astonished, and from that moment he became Bhishma."
        ),
        "reveal": "His greatness was born from sacrifice, not ambition.",
        "ending": "That is why Bhishma’s vow is still remembered as one of the most powerful promises in Indian mythology."
    },
    {
        "category": "mythology",
        "title": "Why Shiva Drank the Poison",
        "topic": "Shiva and the Halahala poison",
        "main_figure": "Lord Shiva",
        "setting": "the churning of the cosmic ocean",
        "era": "Puranic era",
        "mood": "cosmic and intense",
        "hook": "Why did Shiva drink a poison powerful enough to destroy the universe?",
        "summary": (
            "During the Samudra Manthan, a deadly poison called Halahala emerged before the nectar of immortality. "
            "Its power threatened all existence. To save the universe, Shiva consumed it and held it in his throat, "
            "which then turned blue, earning him the name Neelkanth."
        ),
        "reveal": "Before immortality came danger, and before reward came sacrifice.",
        "ending": "That is why Shiva’s blue throat became a symbol of cosmic protection."
    },
    {
        "category": "mythology",
        "title": "How Abhimanyu Entered the Chakravyuha",
        "topic": "Abhimanyu in the Chakravyuha",
        "main_figure": "Abhimanyu",
        "setting": "the battlefield of Kurukshetra",
        "era": "Mahabharata era",
        "mood": "brave and heartbreaking",
        "hook": "How did a young warrior become one of the bravest names in the Mahabharata?",
        "summary": (
            "Abhimanyu knew how to enter the deadly Chakravyuha formation but not how to escape it. "
            "Even so, he entered the formation during battle and fought fearlessly against far older warriors. "
            "His courage became legendary, even though the odds were against him."
        ),
        "reveal": "His story is remembered because bravery is not measured by survival alone.",
        "ending": "That is why Abhimanyu remains one of the most admired heroes of the Mahabharata."
    },
    {
        "category": "mythology",
        "title": "The Day Ganga Took the Child Away",
        "topic": "Ganga and the birth of Bhishma",
        "main_figure": "Ganga",
        "setting": "the kingdom of Hastinapura",
        "era": "Mahabharata era",
        "mood": "mysterious and emotional",
        "hook": "Why would a mother carry away her own child into the river?",
        "summary": (
            "King Shantanu fell in love with Ganga, who agreed to marry him on one condition: he would never question her actions. "
            "When their children were born, she took them away one by one into the river. "
            "Only later was the hidden divine reason revealed, and the surviving child would become Bhishma."
        ),
        "reveal": "What looked cruel on the surface was tied to a larger cosmic fate.",
        "ending": "That is why the story of Ganga and Bhishma is remembered as one of destiny, sacrifice, and mystery."
    },
]

HISTORY_TOPICS = [
    {
        "category": "history",
        "title": "How Ashoka Changed After Kalinga",
        "topic": "Ashoka after the Kalinga war",
        "main_figure": "Emperor Ashoka",
        "setting": "the battlefield of Kalinga",
        "era": "Mauryan Empire",
        "mood": "dramatic and reflective",
        "hook": "How did one of India’s most powerful conquerors turn toward peace?",
        "summary": (
            "Ashoka’s victory in the Kalinga war came at a terrible human cost. "
            "According to historical tradition, the suffering he witnessed deeply affected him. "
            "After that, he moved toward dhamma, moral governance, and the spread of Buddhist ideals."
        ),
        "reveal": "His greatest transformation came not before war, but after seeing its consequences.",
        "ending": "That is why Ashoka is remembered not only as a conqueror, but also as a ruler transformed by conscience."
    },
    {
        "category": "history",
        "title": "The Chola Fleet That Crossed the Sea",
        "topic": "Rajendra Chola's naval campaign",
        "main_figure": "Rajendra Chola I",
        "setting": "the Indian Ocean trade world",
        "era": "Chola Empire",
        "mood": "powerful and adventurous",
        "hook": "Did you know medieval India once launched a naval campaign across the seas?",
        "summary": (
            "Under Rajendra Chola I, the Chola Empire developed major maritime power. "
            "Its fleets moved across the Bay of Bengal and projected influence far beyond the subcontinent. "
            "This campaign showed that Indian power was not limited to land empires alone."
        ),
        "reveal": "The Cholas were not just temple builders, but also one of the great naval powers of their age.",
        "ending": "That is why Rajendra Chola’s maritime campaigns remain one of the most impressive chapters of Indian history."
    },
    {
        "category": "history",
        "title": "The Last Stand of Rani Durgavati",
        "topic": "Rani Durgavati's final battle",
        "main_figure": "Rani Durgavati",
        "setting": "central India",
        "era": "16th century",
        "mood": "brave and tragic",
        "hook": "Who was the queen who chose resistance over surrender?",
        "summary": (
            "Rani Durgavati ruled with courage and determination in central India. "
            "When powerful forces advanced against her kingdom, she led resistance instead of giving in. "
            "Her final stand turned her into a lasting symbol of courage and honor."
        ),
        "reveal": "Her power came not only from rulership, but from refusing to abandon her people.",
        "ending": "That is why Rani Durgavati is remembered as one of the bravest queens in Indian history."
    },
    {
        "category": "history",
        "title": "How Lachit Borphukan Defended Assam",
        "topic": "Lachit Borphukan and the Battle of Saraighat",
        "main_figure": "Lachit Borphukan",
        "setting": "the Brahmaputra at Saraighat",
        "era": "Ahom kingdom",
        "mood": "bold and patriotic",
        "hook": "How did one commander stop a mighty invasion on the Brahmaputra?",
        "summary": (
            "Lachit Borphukan led the Ahom defense in the Battle of Saraighat. "
            "Using deep knowledge of the terrain and determined leadership, he resisted a far larger imperial force. "
            "His leadership became a symbol of strategy, courage, and devotion to the homeland."
        ),
        "reveal": "The battle proved that resolve and strategy can outweigh sheer size.",
        "ending": "That is why Lachit Borphukan remains one of the greatest military heroes in Indian history."
    },
    {
        "category": "history",
        "title": "What Happened After Haldighati",
        "topic": "Maharana Pratap after Haldighati",
        "main_figure": "Maharana Pratap",
        "setting": "the hills and forests of Mewar",
        "era": "16th century",
        "mood": "defiant and resilient",
        "hook": "Most people know the Battle of Haldighati, but what happened after it is just as powerful.",
        "summary": (
            "Even after the fierce Battle of Haldighati, Maharana Pratap did not give up. "
            "He endured years of hardship, regrouped, and continued resistance for the cause of Mewar. "
            "His long struggle made him a lasting symbol of independence and endurance."
        ),
        "reveal": "His legend was built not on a single battle, but on refusing to surrender afterward.",
        "ending": "That is why Maharana Pratap is remembered for resilience as much as for valor."
    },
    {
        "category": "history",
        "title": "The Scholar and the Emperor",
        "topic": "Chanakya and Chandragupta",
        "main_figure": "Chanakya and Chandragupta Maurya",
        "setting": "ancient northern India",
        "era": "Mauryan rise",
        "mood": "strategic and intense",
        "hook": "What happens when a brilliant strategist finds the ruler he has been waiting for?",
        "summary": (
            "Chanakya was a master strategist and political thinker. "
            "He became the guide of Chandragupta Maurya and helped shape the rise of one of India’s great empires. "
            "Their partnership is remembered as one of the most powerful combinations of intellect and ambition."
        ),
        "reveal": "Empires are not built by strength alone, but also by planning, patience, and vision.",
        "ending": "That is why Chanakya and Chandragupta remain one of the most iconic duos in Indian history."
    },
    {
        "category": "history",
        "title": "How Ahilyabai Holkar Rebuilt Sacred India",
        "topic": "Ahilyabai Holkar's legacy",
        "main_figure": "Ahilyabai Holkar",
        "setting": "across major sacred sites in India",
        "era": "18th century",
        "mood": "graceful and inspiring",
        "hook": "Which ruler quietly rebuilt some of India’s most sacred places?",
        "summary": (
            "Ahilyabai Holkar ruled with wisdom, justice, and deep religious devotion. "
            "She supported temples, pilgrimage routes, and public works across India. "
            "Her legacy was built not on conquest, but on restoration, service, and good governance."
        ),
        "reveal": "Her greatness came from preserving civilization rather than expanding a battlefield empire.",
        "ending": "That is why Ahilyabai Holkar is remembered as one of the most respected rulers in Indian history."
    },
    {
        "category": "history",
        "title": "The Burning of Nalanda",
        "topic": "Nalanda University",
        "main_figure": "Nalanda Mahavihara",
        "setting": "ancient Bihar",
        "era": "medieval India",
        "mood": "somber and powerful",
        "hook": "What happens when one of the world’s greatest centers of learning is destroyed?",
        "summary": (
            "Nalanda was one of the most famous centers of learning in the ancient world. "
            "Students and scholars came there from many regions to study philosophy, science, and literature. "
            "Its destruction became one of the most heartbreaking losses in the history of knowledge."
        ),
        "reveal": "The fall of Nalanda was not just the loss of buildings, but the loss of an intellectual world.",
        "ending": "That is why Nalanda still stands as a symbol of India’s scholarly greatness and its loss."
    },
]

ALL_TOPICS = MYTHOLOGY_TOPICS + HISTORY_TOPICS


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def make_fingerprint(item):
    key = f"{item['category']}|{item['topic']}|{item['title']}"
    return hashlib.sha256(key.encode()).hexdigest()


def choose_topic(history):
    recent = history[-10:]

    used_fingerprints = {item.get("fingerprint") for item in history}
    recent_topics = {item.get("topic") for item in recent}
    recent_categories = [item.get("category") for item in recent[-4:]]

    candidates = []

    for item in ALL_TOPICS:
        fp = make_fingerprint(item)

        if fp in used_fingerprints:
            continue

        if item["topic"] in recent_topics:
            continue

        # prevent too many consecutive mythology or history stories
        if len(recent_categories) >= 3 and all(cat == item["category"] for cat in recent_categories[-3:]):
            continue

        candidates.append(item)

    if not candidates:
        # fallback if all topics have been used
        candidates = ALL_TOPICS[:]

    return random.choice(candidates)


def make_screenplay(item):
    # ~90–115 words, good for short-form narration
    return (
        f"{item['hook']} "
        f"This story takes us to {item['setting']}, during {item['era']}. "
        f"At the center of it is {item['main_figure']}. "
        f"{item['summary']} "
        f"{item['reveal']} "
        f"{item['ending']}"
    )


def make_beats(item):
    return [
        f"Hook moment introducing the mystery or dramatic question: {item['hook']}",
        f"Show {item['setting']} during {item['era']}, establishing the atmosphere.",
        f"Introduce {item['main_figure']} as the central figure of the story.",
        f"Show the key turning point of the story: {item['summary']}",
        f"Show the reveal or emotional realization: {item['reveal']}",
        f"End with a powerful final visual that reflects: {item['ending']}"
    ]


# --------------------------------------------------
# Main
# --------------------------------------------------

history = load_history()
chosen = choose_topic(history)
fingerprint = make_fingerprint(chosen)

story = {
    "title": chosen["title"],
    "category": chosen["category"],
    "topic": chosen["topic"],
    "main_figure": chosen["main_figure"],
    "setting": chosen["setting"],
    "era": chosen["era"],
    "mood": chosen["mood"],
    "hook": chosen["hook"],
    "screenplay": make_screenplay(chosen),
    "beats": make_beats(chosen),
    "fingerprint": fingerprint
}

Path("story.json").write_text(
    json.dumps(story, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

history.append(story)

Path("story_history.json").write_text(
    json.dumps(history, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Generated India-focused story:")
print(json.dumps(story, indent=2, ensure_ascii=False))
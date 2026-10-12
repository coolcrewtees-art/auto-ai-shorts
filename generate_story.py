import json
import random
import hashlib
from pathlib import Path


HISTORY_FILE = Path("story_history.json")
OUTPUT_FILE = Path("story.json")

MIN_WORDS = 175
MAX_WORDS = 260


CATEGORIES = [
    "indian_mythology",
    "indian_folktale",
    "indian_legend",
    "supernatural_mystery",
    "fantasy",
    "romance_drama",
    "comedy",
]


# ============================================================
# PART ONE STORIES
# ============================================================

STORIES = [

    # ========================================================
    # SUPERNATURAL
    # ========================================================

    {
        "story_id": "memory_train",
        "part": 1,
        "category": "supernatural_mystery",

        "title_hook":
            "The Train That Charged Passengers With Memories",

        "topic":
            "a mysterious train where memories are used as fare",

        "main_figure":
            "Rohan, a young Indian man traveling alone at night",

        "setting":
            "an endless midnight train traveling through a dark surreal landscape",

        "mood":
            "unsettling, mysterious, emotional, cinematic",

        "opening": (
            "Rohan missed the last normal train home. "
            "Then, at exactly midnight, another train arrived. "
            "No number. No destination. "
            "The doors opened anyway. "
            "Inside, every passenger sat completely silent. "
            "Rohan took a seat. "
            "A conductor approached and asked for his ticket. "
            "Rohan reached for his wallet. "
            "The conductor smiled. "
            "'We don't take money here.'"
        ),

        "conflict": (
            "Instead, the conductor touched Rohan's forehead. "
            "Instantly, Rohan forgot his tenth birthday. "
            "The conductor whispered, "
            "'One memory. One station.' "
            "Rohan thought it was some bizarre trick. "
            "Then the train stopped. "
            "A passenger stood, surrendered another memory, "
            "and walked through the doors into complete darkness."
        ),

        "escalation": (
            "Station after station, Rohan kept paying. "
            "His first day of school vanished. "
            "Then his first kiss. "
            "Then the sound of his father's voice. "
            "Rohan finally shouted for the train to stop. "
            "The conductor calmly said, "
            "'You chose to keep traveling.' "
            "Rohan looked around. "
            "The other passengers were not silent because they were frightened. "
            "They had forgotten how to speak."
        ),

        "dramatic_reveal": (
            "Finally, the train reached the last station. "
            "The conductor demanded one final memory. "
            "Rohan searched his mind. "
            "Only his mother's face remained. "
            "He refused to surrender it. "
            "The conductor smiled and said, "
            "'Then you cannot leave.' "
            "Rohan looked outside. "
            "Hundreds of confused people stood on the platform. "
            "Every one of them had once been a passenger."
        ),

        "final_punch": (
            "The conductor leaned close and whispered, "
            "'People think forgetting makes pain disappear.' "
            "'It doesn't.' "
            "'It only makes you forget why you're hurting.' "
            "The doors slammed shut. "
            "And the train continued deeper into the darkness."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # FANTASY
    # ========================================================

    {
        "story_id": "lying_king",
        "part": 1,
        "category": "fantasy",

        "title_hook":
            "The King Who Could Hear Every Lie",

        "topic":
            "a king cursed to hear lies",

        "main_figure":
            "a young king wearing dark royal armor",

        "setting":
            "a vast medieval fantasy kingdom and royal palace",

        "mood":
            "dark fantasy, psychological, royal, dramatic",

        "opening": (
            "The king possessed one gift no ruler should ever have. "
            "Whenever somebody lied to him, he heard a scream. "
            "At first, he loved it. "
            "A merchant said his prices were fair. "
            "Scream. "
            "A general claimed every soldier adored him. "
            "Scream. "
            "No adviser could deceive him."
        ),

        "conflict": (
            "Soon, the gift became an obsession. "
            "Servants were punished. "
            "Friends were banished. "
            "Ministers were imprisoned. "
            "Eventually his wife begged him to stop. "
            "The king looked at her and asked, "
            "'Do you still love me?' "
            "She answered yes. "
            "For the first time in months, there was complete silence."
        ),

        "escalation": (
            "That should have comforted him. "
            "Instead, it frightened him. "
            "The following morning, his wife disappeared. "
            "The king interrogated the entire palace. "
            "Scream after scream filled his head. "
            "Finally, an old prisoner began laughing. "
            "The king demanded to know why. "
            "The prisoner replied, "
            "'Because you still don't understand your curse.'"
        ),

        "dramatic_reveal": (
            "The prisoner pointed toward a mirror. "
            "'Your gift doesn't reveal every lie people tell.' "
            "'It reveals lies you desperately want to believe.' "
            "The king stared at his reflection. "
            "He whispered, "
            "'My people love me.' "
            "A scream exploded through the chamber. "
            "Then he said, "
            "'I am a good king.' "
            "The scream became unbearable."
        ),

        "final_punch": (
            "Finally he asked the question he'd avoided. "
            "'Did my wife leave because she stopped loving me?' "
            "Silence. "
            "That silence hurt more than every scream combined. "
            "She had loved him. "
            "She had simply become terrified of the man he had become."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # INDIAN FOLKTALE — PART 1
    # ========================================================

    {
        "story_id": "unlocked_village",
        "part": 1,
        "category": "indian_folktale",

        "title_hook":
            "The Village Where Nobody Locked Their Doors",

        "topic":
            "a village with a mysterious night visitor",

        "main_figure":
            "a skeptical young Indian traveler",

        "setting":
            "an isolated old Indian village surrounded by dense forest",

        "mood":
            "Indian folklore, eerie, atmospheric, suspenseful",

        "opening": (
            "A traveler reached a tiny village shortly before sunset. "
            "Something immediately felt wrong. "
            "Not one house had a lock. "
            "Even the jewellery shop stood completely unsecured. "
            "He asked an old shopkeeper, "
            "'Aren't you afraid of thieves?' "
            "The old man smiled strangely. "
            "'Thieves don't survive the night here.'"
        ),

        "conflict": (
            "The traveler assumed the man was joking. "
            "Before nightfall, villagers gave him only one warning. "
            "'After midnight, if someone knocks three times, do not open the door.' "
            "He laughed. "
            "Then midnight arrived. "
            "Knock. "
            "Knock. "
            "Knock. "
            "A frightened woman's voice whispered from outside, "
            "'Please... let me in.'"
        ),

        "escalation": (
            "The traveler looked through a crack in the window. "
            "A woman wearing red bridal clothes stood outside. "
            "Her feet were covered in mud. "
            "She looked terrified. "
            "Then she whispered his name. "
            "The traveler froze. "
            "Nobody in the village knew his name. "
            "Suddenly the knocking started again. "
            "But this time... it came from the wall behind him."
        ),

        "dramatic_reveal": (
            "At sunrise, everything stopped. "
            "The traveler rushed to the old shopkeeper. "
            "The man quietly pulled out a faded photograph. "
            "The same bride was standing in it. "
            "The photograph was almost eighty years old. "
            "The traveler asked why the dead woman wanted inside. "
            "The old man shook his head. "
            "'She wasn't trying to enter your room.' "
            "'She was warning you.'"
        ),

        "final_punch": (
            "The traveler slowly returned to the house. "
            "Behind it were enormous muddy footprints. "
            "But they weren't coming toward his window. "
            "They were leading away from the house. "
            "Something else had been inside the room with him all night."
        ),

        "has_next_part": True,
    },


    # ========================================================
    # INDIAN MYTHOLOGY
    # ========================================================

    {
        "story_id": "bhishma_death",
        "part": 1,
        "category": "indian_mythology",

        "title_hook":
            "The Warrior Who Chose His Own Death",

        "topic":
            "Bhishma and the boon of choosing the time of his death",

        "main_figure":
            "Bhishma, an elderly legendary Indian warrior",

        "setting":
            "the battlefield of Kurukshetra during the Mahabharata war",

        "mood":
            "epic, tragic, powerful, mythological",

        "opening": (
            "Imagine being given an impossible power. "
            "Not immortality. "
            "Something stranger. "
            "The ability to decide when you die. "
            "According to the Mahabharata, Bhishma possessed exactly that boon. "
            "And during the war of Kurukshetra, "
            "it created one of the epic's most unforgettable moments."
        ),

        "conflict": (
            "Bhishma was almost impossible to defeat. "
            "He was older than most warriors around him, "
            "yet entire forces struggled to stop him. "
            "Eventually, Arjuna's arrows brought him down. "
            "But Bhishma never touched the ground. "
            "So many arrows pierced his body that they formed a bed beneath him."
        ),

        "escalation": (
            "Everyone expected him to die. "
            "He didn't. "
            "Days passed. "
            "Bhishma remained alive on the bed of arrows. "
            "He was wounded. "
            "He was suffering. "
            "But because of his boon, "
            "death could not take him until he permitted it."
        ),

        "dramatic_reveal": (
            "Bhishma was waiting for something. "
            "According to tradition, he waited for Uttarayana, "
            "the period connected with the sun's northward journey. "
            "Only when the moment he considered auspicious finally arrived "
            "did Bhishma choose to release his life."
        ),

        "final_punch": (
            "Most warriors spend their final battle desperately avoiding death. "
            "Bhishma's final battle was different. "
            "Death was already waiting beside him. "
            "And according to the epic, "
            "death itself had to wait for Bhishma."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # ROMANCE
    # ========================================================

    {
        "story_id": "future_messages",
        "part": 1,
        "category": "romance_drama",

        "title_hook":
            "He Received Her Messages Five Years After She Died",

        "topic":
            "scheduled messages from a lost love",

        "main_figure":
            "Arjun, a young man grieving the woman he loved",

        "setting":
            "a modern Indian city, rainy apartment and old cafe",

        "mood":
            "emotional, bittersweet, mysterious, cinematic",

        "opening": (
            "Five years after Mira died, Arjun's phone suddenly buzzed. "
            "The message came from her old number. "
            "It read, "
            "'You still order coffee without sugar, don't you?' "
            "Arjun nearly dropped the phone. "
            "The number had been disconnected for years."
        ),

        "conflict": (
            "One week later, another message arrived. "
            "'Stop keeping my blue sweater.' "
            "Then another. "
            "'Your mother still worries when you skip dinner.' "
            "Nobody else knew those details. "
            "Arjun slowly became convinced that somehow, "
            "Mira was still reaching him."
        ),

        "escalation": (
            "For months the messages continued. "
            "Sometimes they were funny. "
            "Sometimes painfully specific. "
            "Then one night a message appeared. "
            "'Tomorrow. Our old cafe. Table seven.' "
            "Arjun barely slept. "
            "The following evening he arrived early. "
            "Someone was already sitting there."
        ),

        "dramatic_reveal": (
            "It was Mira's younger sister. "
            "She placed an old laptop on the table. "
            "Before Mira died, she had written hundreds of messages "
            "and scheduled them years into the future. "
            "She knew Arjun would struggle to move on. "
            "So she had designed a goodbye that would take years to finish."
        ),

        "final_punch": (
            "Arjun opened Mira's final scheduled message. "
            "It read, "
            "'If you're reading this, you've survived the part "
            "where you thought you couldn't.' "
            "'Now stop waiting for me.' "
            "'Go live enough for both of us.'"
        ),

        "has_next_part": False,
    },


    # ========================================================
    # COMEDY
    # ========================================================

    {
        "story_id": "lucky_thief",
        "part": 1,
        "category": "comedy",

        "title_hook":
            "The Thief Who Accidentally Became Prime Minister",

        "topic":
            "a terrible thief mistaken for a brilliant strategist",

        "main_figure":
            "Milo, a nervous young thief",

        "setting":
            "a chaotic medieval fantasy kingdom",

        "mood":
            "fast, funny, absurd, energetic",

        "opening": (
            "Milo broke into the royal palace for exactly one reason. "
            "Gold. "
            "Nothing heroic. "
            "Nothing complicated. "
            "Unfortunately, he chose the worst possible room to hide in. "
            "The king's military strategy chamber."
        ),

        "conflict": (
            "Guards burst through the door. "
            "Milo panicked and pointed randomly at a military map. "
            "'Attack there!' "
            "The king walked in at exactly that moment. "
            "Everyone became silent. "
            "The king stared at the map and whispered, "
            "'Brilliant.' "
            "Milo had accidentally pointed at the enemy's weakest position."
        ),

        "escalation": (
            "By morning, Milo had been promoted to royal adviser. "
            "He tried to resign. "
            "The king mistook it for humility. "
            "Milo deliberately gave terrible advice. "
            "It somehow worked. "
            "'Move the army left!' "
            "A bridge collapsed on the right. "
            "'Don't attack today!' "
            "A storm destroyed the enemy camp."
        ),

        "dramatic_reveal": (
            "Within a month, everyone called Milo the greatest strategist alive. "
            "Then the king announced his retirement. "
            "Milo smiled politely. "
            "Until the king continued, "
            "'And you shall replace me.' "
            "For the first time in his criminal career, "
            "Milo genuinely wanted the guards to arrest him."
        ),

        "final_punch": (
            "Years later, historians called him Milo the Brilliant. "
            "His greatest secret never became public. "
            "He hadn't correctly predicted a single event in his entire life. "
            "He was simply the luckiest idiot the kingdom had ever seen."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # INDIAN LEGEND — PART 1
    # ========================================================

    {
        "story_id": "black_door_palace",
        "part": 1,
        "category": "indian_legend",

        "title_hook":
            "The Palace Room That Was Never Opened",

        "topic":
            "a forbidden royal chamber containing a supernatural mirror",

        "main_figure":
            "a young Indian prince wearing dark traditional royal clothing",

        "setting":
            "an ancient Indian hill palace during a violent thunderstorm",

        "mood":
            "royal mystery, eerie, suspenseful, supernatural",

        "opening": (
            "For generations, one room in the palace remained locked. "
            "No servant cleaned it. "
            "No guard entered it. "
            "Even the king refused to explain why. "
            "There was only one rule. "
            "Never open the black door after sunset."
        ),

        "conflict": (
            "Naturally, the king's youngest son became obsessed with it. "
            "One stormy night, the prince stole the key. "
            "The black door opened surprisingly easily. "
            "Inside were only three things. "
            "A wooden chair. "
            "A giant antique mirror. "
            "And hundreds of names carved into the stone wall."
        ),

        "escalation": (
            "The prince stepped closer. "
            "Every name belonged to somebody from his own family. "
            "Kings. Queens. Children. "
            "Beside every name was a date. "
            "Then the prince noticed the final line. "
            "His own name was already carved into the wall. "
            "Beside it was tomorrow's date."
        ),

        "dramatic_reveal": (
            "The prince ran for the door. "
            "It slammed shut. "
            "Then his reflection moved without him. "
            "The reflection slowly smiled and placed one finger against the glass. "
            "Behind it stood dozens of terrified people. "
            "Every missing member of the royal family "
            "was trapped inside the mirror."
        ),

        "final_punch": (
            "The prince grabbed a metal candle stand and smashed the mirror. "
            "The chamber instantly became silent. "
            "The following morning, guards opened the black door. "
            "The prince was gone. "
            "But a new mirror stood against the wall. "
            "And inside it... the prince was screaming."
        ),

        "has_next_part": True,
    },
]


# ============================================================
# PART TWO STORIES
# =====================================
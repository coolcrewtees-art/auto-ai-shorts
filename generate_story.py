import json
import random
import hashlib
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

HISTORY_FILE = Path("story_history.json")
OUTPUT_FILE = Path("story.json")

# Around 190-230 words works much better for ~60 sec narration
MIN_WORDS = 185
TARGET_MAX_WORDS = 235


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
# STORY LIBRARY
#
# IMPORTANT:
# These are written like spoken Shorts.
# Short lines.
# Frequent mini-reveals.
# Dialogue.
# Escalation.
# Strong ending.
#
# Same fields are preserved so generate_scenes.py,
# generate_voice.py and make_video.py still work.
# ============================================================

STORIES = [

    # ========================================================
    # SUPERNATURAL / MYSTERY
    # ========================================================

    {
        "category": "supernatural_mystery",

        "title_hook":
            "The Train That Charged Passengers With Memories",

        "topic":
            "a mysterious train where memories are used as fare",

        "main_figure":
            "a young man traveling alone at night",

        "setting":
            "an endless midnight train moving through a surreal dark landscape",

        "mood":
            "mysterious, unsettling, emotional, cinematic",

        "opening": (
            "Rohan missed the last normal train home. "
            "Then, at exactly midnight, another train arrived. "
            "No number. No destination. "
            "The doors opened anyway. "
            "Inside, every passenger was completely silent. "
            "Rohan sat down. "
            "A conductor approached him and said, "
            "'Ticket, please.' "
            "Rohan reached for his wallet. "
            "The conductor shook his head. "
            "'We don't take money here.'"
        ),

        "conflict": (
            "Instead, the conductor touched Rohan's forehead. "
            "Suddenly, Rohan couldn't remember his tenth birthday. "
            "The conductor smiled. "
            "'One memory. One station.' "
            "Rohan laughed nervously. "
            "He thought it was some kind of trick. "
            "Then the train stopped. "
            "One passenger stood up... "
            "gave the conductor another memory... "
            "and walked into the darkness outside."
        ),

        "escalation": (
            "Station after station, Rohan kept paying. "
            "His first day of school disappeared. "
            "Then his first kiss. "
            "Then the sound of his father's voice. "
            "He panicked. "
            "'Stop the train!' "
            "The conductor calmly replied, "
            "'You chose to keep traveling.' "
            "Rohan looked around. "
            "The other passengers weren't quiet because they were afraid. "
            "They had simply forgotten how to speak."
        ),

        "dramatic_reveal": (
            "Finally, the train reached the last station. "
            "The conductor asked for one final memory. "
            "Rohan searched his mind. "
            "Nothing remained... except his mother's face. "
            "He refused. "
            "The conductor smiled. "
            "'Then you cannot leave.' "
            "Rohan turned toward the window. "
            "Hundreds of people stood on the platform outside. "
            "All of them looked lost. "
            "All of them had once been passengers."
        ),

        "final_punch": (
            "The doors opened. "
            "The conductor leaned closer and whispered, "
            "'People think forgetting makes pain disappear.' "
            "'It doesn't.' "
            "'It only makes you forget why you're hurting.' "
            "Then the doors closed... "
            "and the train continued into the dark."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # FANTASY
    # ========================================================

    {
        "category": "fantasy",

        "title_hook":
            "The King Who Could Hear Every Lie",

        "topic":
            "a king cursed with the ability to hear lies",

        "main_figure":
            "a powerful young king wearing dark royal armor",

        "setting":
            "a giant medieval fantasy kingdom",

        "mood":
            "dark fantasy, psychological, dramatic, royal",

        "opening": (
            "The king had a gift no ruler should ever have. "
            "Whenever somebody lied to him... "
            "he heard a scream. "
            "At first, he loved it. "
            "A merchant said, 'My prices are fair.' "
            "Scream. "
            "A general said, 'My soldiers adore you.' "
            "Scream. "
            "Even his own advisers couldn't fool him."
        ),

        "conflict": (
            "Soon, the king trusted nobody. "
            "Servants were punished. "
            "Friends were banished. "
            "Ministers were imprisoned. "
            "His wife finally begged him to stop. "
            "'Not every lie is meant to hurt you.' "
            "The king asked, "
            "'Do you still love me?' "
            "She answered yes. "
            "Silence. "
            "For the first time in months... no scream."
        ),

        "escalation": (
            "That should have comforted him. "
            "Instead, it terrified him. "
            "Because the next morning she disappeared. "
            "The king became obsessed. "
            "He questioned everyone in the palace. "
            "Scream after scream filled his head. "
            "Finally, an old prisoner laughed at him. "
            "'You still don't understand your curse.'"
        ),

        "dramatic_reveal": (
            "The king demanded an explanation. "
            "The prisoner pointed toward a mirror. "
            "'It doesn't reveal lies told to you.' "
            "'It reveals lies you choose to believe.' "
            "The king stared at himself. "
            "Then he whispered, "
            "'My people love me.' "
            "A scream exploded through the room. "
            "He tried again. "
            "'I am a good king.' "
            "The scream became unbearable."
        ),

        "final_punch": (
            "Then he finally asked the question he'd avoided for years. "
            "'Did my wife leave because she stopped loving me?' "
            "Silence. "
            "And that silence hurt more than every scream combined. "
            "She had loved him. "
            "She had simply become afraid of the man he had become."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # INDIAN FOLKTALE
    # ========================================================

    {
        "category": "indian_folktale",

        "title_hook":
            "The Village Where Nobody Locked Their Doors",

        "topic":
            "a village protected by a mysterious night visitor",

        "main_figure":
            "a skeptical young traveler",

        "setting":
            "an isolated old Indian village surrounded by forest",

        "mood":
            "Indian folklore, eerie, mysterious, atmospheric",

        "opening": (
            "A traveler reached a tiny village just before sunset. "
            "Something immediately felt strange. "
            "Not one house had a lock. "
            "Not even the jewellery shop. "
            "He asked an old shopkeeper, "
            "'Aren't you afraid of thieves?' "
            "The old man smiled. "
            "'Thieves don't survive the night here.'"
        ),

        "conflict": (
            "The traveler assumed he was joking. "
            "That evening, villagers gave him one warning. "
            "'After midnight, if someone knocks three times... don't open the door.' "
            "He laughed. "
            "Then midnight came. "
            "Knock. "
            "Knock. "
            "Knock. "
            "A woman's voice whispered from outside, "
            "'Please... let me in.'"
        ),

        "escalation": (
            "He looked through a crack in the window. "
            "A woman stood outside wearing red bridal clothes. "
            "Her feet were covered in mud. "
            "She looked terrified. "
            "Then she whispered his name. "
            "The traveler froze. "
            "Nobody in the village knew his name. "
            "The knocking started again. "
            "This time... from the wall behind him."
        ),

        "dramatic_reveal": (
            "At sunrise, everything stopped. "
            "The traveler rushed to the shopkeeper. "
            "The old man listened quietly. "
            "Then he pulled out a faded photograph. "
            "The same bride stood in it. "
            "The picture was almost eighty years old. "
            "'She wasn't trying to enter your room,' the old man said. "
            "'She was warning you.'"
        ),

        "final_punch": (
            "The traveler slowly turned around. "
            "Behind the house were deep footprints. "
            "Not coming toward his window... "
            "but leading away from it. "
            "Something else had been inside the room with him all night."
        ),

        "has_next_part": True,
    },


    # ========================================================
    # INDIAN MYTHOLOGY
    # ========================================================

    {
        "category": "indian_mythology",

        "title_hook":
            "The Warrior Who Chose His Own Death",

        "topic":
            "Bhishma and the boon of choosing the time of his death",

        "main_figure":
            "Bhishma, an ancient warrior lying upon a bed of arrows",

        "setting":
            "the battlefield of Kurukshetra",

        "mood":
            "epic, tragic, powerful, mythological",

        "opening": (
            "Imagine being given one impossible power. "
            "Not immortality. "
            "Something stranger. "
            "The ability to decide when you die. "
            "According to the Mahabharata, Bhishma possessed exactly that boon. "
            "And during the great war of Kurukshetra... "
            "that power created one of its most unforgettable moments."
        ),

        "conflict": (
            "Bhishma was almost impossible to defeat. "
            "He was older than most warriors fighting against him. "
            "Yet even armies struggled to stop him. "
            "Eventually, Arjuna's arrows brought him down. "
            "But Bhishma didn't fall onto the earth. "
            "So many arrows pierced his body that they held him above the ground... "
            "forming a bed beneath him."
        ),

        "escalation": (
            "Everyone expected him to die. "
            "He didn't. "
            "Days passed. "
            "Bhishma remained alive on that bed of arrows. "
            "He was wounded. "
            "He was suffering. "
            "But because of his boon... death could not take him until he allowed it."
        ),

        "dramatic_reveal": (
            "And Bhishma was waiting for something. "
            "In Hindu tradition, he waited for Uttarayana... "
            "the period associated with the sun's northward journey. "
            "Only when he believed the right moment had arrived "
            "did he finally choose to let go."
        ),

        "final_punch": (
            "Most warriors spend their final battle trying desperately not to die. "
            "Bhishma's final battle was completely different. "
            "Death was already waiting beside him. "
            "And according to the epic... "
            "death itself had to wait for Bhishma."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # ROMANCE / DRAMA
    # ========================================================

    {
        "category": "romance_drama",

        "title_hook":
            "He Received Her Messages Five Years After She Died",

        "topic":
            "scheduled messages from a lost love",

        "main_figure":
            "a young man grieving the woman he loved",

        "setting":
            "a modern city apartment during rainy nights",

        "mood":
            "emotional, bittersweet, mysterious",

        "opening": (
            "Five years after Mira died, Arjun's phone buzzed. "
            "The message was from her number. "
            "It said, "
            "'You still order coffee without sugar, don't you?' "
            "He nearly dropped the phone. "
            "That number had been disconnected for years."
        ),

        "conflict": (
            "The next week, another message arrived. "
            "'Stop keeping my blue sweater.' "
            "Then another. "
            "'Your mother still worries when you skip dinner.' "
            "Nobody else knew these things. "
            "Arjun became convinced that somehow... Mira was still reaching him."
        ),

        "escalation": (
            "For months, the messages continued. "
            "Sometimes funny. "
            "Sometimes painfully specific. "
            "Then one night a message appeared: "
            "'Tomorrow, go to our old café. Table seven.' "
            "Arjun barely slept. "
            "The next evening he arrived early. "
            "Someone was already sitting there."
        ),

        "dramatic_reveal": (
            "It was Mira's younger sister. "
            "She placed an old laptop on the table. "
            "Before Mira died, she had written hundreds of messages "
            "and scheduled them years into the future. "
            "She knew Arjun would struggle to move on. "
            "So she had created a goodbye that would take years to finish."
        ),

        "final_punch": (
            "Arjun looked at the final scheduled message. "
            "It read, "
            "'If you're reading this, you've survived the part where you thought you couldn't.' "
            "'Now please stop waiting for me.' "
            "'Go live enough for both of us.'"
        ),

        "has_next_part": False,
    },


    # ========================================================
    # COMEDY
    # ========================================================

    {
        "category": "comedy",

        "title_hook":
            "The Thief Who Accidentally Became Prime Minister",

        "topic":
            "an incompetent thief mistaken for a brilliant strategist",

        "main_figure":
            "a nervous but strangely lucky thief",

        "setting":
            "a ridiculous medieval fantasy kingdom",

        "mood":
            "fast, funny, absurd, energetic",

        "opening": (
            "A thief named Milo broke into the royal palace for one reason. "
            "Gold. "
            "Nothing heroic. "
            "Nothing complicated. "
            "Unfortunately, he chose the worst possible room to hide in... "
            "the king's military strategy chamber."
        ),

        "conflict": (
            "Guards burst through the door. "
            "Milo panicked and pointed randomly at a map. "
            "'Attack... there!' "
            "The king walked in at exactly that moment. "
            "Everyone went silent. "
            "The king stared at the map. "
            "'Brilliant,' he whispered. "
            "Milo had accidentally pointed at the enemy army's weakest position."
        ),

        "escalation": (
            "By morning, Milo had been promoted to royal adviser. "
            "He tried to resign. "
            "The king thought it was humility. "
            "He tried giving terrible advice. "
            "It somehow worked. "
            "'Move the army left!' "
            "A bridge collapsed on the right. "
            "'Don't attack today!' "
            "A storm destroyed the enemy camp."
        ),

        "dramatic_reveal": (
            "Within a month, people were calling Milo the greatest strategist alive. "
            "Then the king announced, "
            "'I am retiring.' "
            "Milo smiled politely... until the king continued. "
            "'And you shall replace me.' "
            "For the first time in his criminal career, Milo genuinely wanted to be arrested."
        ),

        "final_punch": (
            "Years later, historians called him Milo the Brilliant. "
            "His greatest secret never became public. "
            "He hadn't predicted a single thing correctly in his entire life. "
            "He was simply the luckiest idiot the kingdom had ever seen."
        ),

        "has_next_part": False,
    },


    # ========================================================
    # INDIAN LEGEND
    # ========================================================

    {
        "category": "indian_legend",

        "title_hook":
            "The Palace Room That Was Never Opened",

        "topic":
            "a sealed royal chamber hiding a strange secret",

        "main_figure":
            "a young prince investigating an abandoned palace chamber",

        "setting":
            "an ancient Indian hill palace during a thunderstorm",

        "mood":
            "royal mystery, eerie, suspenseful",

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
            "One stormy night, he stole the key. "
            "The door opened surprisingly easily. "
            "Inside was almost nothing. "
            "A chair. "
            "A giant mirror. "
            "And hundreds of names carved into the wall."
        ),

        "escalation": (
            "The prince stepped closer. "
            "Every name belonged to someone from his own family. "
            "Kings. Queens. Children. "
            "And beside every name was a date. "
            "Then he noticed the final line. "
            "His own name was already there. "
            "Beside it... tomorrow's date."
        ),

        "dramatic_reveal": (
            "He ran toward the door. "
            "It slammed shut. "
            "Then his reflection moved without him. "
            "The reflection smiled and placed one finger against the glass. "
            "Behind it stood dozens of people. "
            "Every missing member of the royal family was trapped inside the mirror."
        ),

        "final_punch": (
            "The prince smashed the glass. "
            "The room instantly became silent. "
            "The next morning, guards finally opened the door. "
            "The prince was gone. "
            "But a new mirror stood against the wall. "
            "And inside it... the prince was screaming."
        ),

        "has_next_part": True,
    },
]


# ============================================================
# HISTORY
# ============================================================

def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(
            HISTORY_FILE.read_text(
                encoding="utf-8"
   
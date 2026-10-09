import json
import random
import hashlib
from pathlib import Path

HISTORY_FILE = Path("story_history.json")

# ============================================================
# CONTENT POOLS
# ============================================================

INDIAN_MYTHOLOGY = [
    {
        "category": "indian_mythology",
        "title": "Karna Knew He Was Being Tricked",
        "topic": "Karna gives away his kavach and kundal",
        "main_figure": "Karna",
        "setting": "ancient India before the Kurukshetra war",
        "mood": "tragic, intense, heroic",
        "hook": "Karna knew the man asking for his armor was not an ordinary beggar.",
        "conflict": (
            "He understood that giving away his divine armor and earrings could leave him vulnerable in the coming war."
        ),
        "escalation": (
            "But Karna had built his entire identity around never refusing someone who came to him asking for charity."
        ),
        "twist": (
            "So even after realizing that Indra had come in disguise, Karna still removed the protection from his own body and gave it away."
        ),
        "final_line": (
            "He did not lose his greatness when he became weaker. That was the moment his legend became even bigger."
        )
    },

    {
        "category": "indian_mythology",
        "title": "Krishna Gave Ashwatthama a Fate Worse Than Death",
        "topic": "Ashwatthama's curse",
        "main_figure": "Ashwatthama",
        "setting": "the final days of the Mahabharata war",
        "mood": "dark, haunting, supernatural",
        "hook": "The war was almost over, but Ashwatthama wanted revenge so badly that he crossed a line nobody could forgive.",
        "conflict": (
            "Driven by rage after his father's death, he attacked when his enemies were least prepared."
        ),
        "escalation": (
            "What followed was not treated as another act of war. It was seen as something far darker."
        ),
        "twist": (
            "Krishna did not simply kill him. According to tradition, Ashwatthama was cursed to wander the earth in suffering."
        ),
        "final_line": (
            "For a warrior, death might have been mercy. Instead, the punishment was to keep living."
        )
    },

    {
        "category": "indian_mythology",
        "title": "Why Bhishma Refused to Die",
        "topic": "Bhishma on the bed of arrows",
        "main_figure": "Bhishma",
        "setting": "Kurukshetra battlefield",
        "mood": "epic, solemn, emotional",
        "hook": "Bhishma had already fallen in battle. But he still refused to die.",
        "conflict": (
            "His body was covered in arrows, yet he possessed the boon of choosing the moment of his death."
        ),
        "escalation": (
            "Instead of letting go, he remained alive through the suffering and continued advising kings and warriors."
        ),
        "twist": (
            "He waited for an auspicious time before finally allowing himself to die."
        ),
        "final_line": (
            "Even after defeat, Bhishma turned his final days into one last act of duty."
        )
    },

    {
        "category": "indian_mythology",
        "title": "Hanuman Didn't Know Which Herb to Take",
        "topic": "Hanuman carrying the mountain",
        "main_figure": "Hanuman",
        "setting": "the war in Lanka",
        "mood": "heroic, urgent, spectacular",
        "hook": "Lakshmana was dying, and Hanuman had only one job: bring back a life-saving herb.",
        "conflict": (
            "The problem was that when he reached the mountain, he could not identify the correct herb."
        ),
        "escalation": (
            "Every second mattered. Choosing the wrong plant could cost Lakshmana his life."
        ),
        "twist": (
            "So Hanuman stopped trying to choose. He lifted the entire mountain and carried it back."
        ),
        "final_line": (
            "When the mission mattered more than the method, Hanuman simply moved the mountain."
        )
    },

    {
        "category": "indian_mythology",
        "title": "The Vow That Destroyed a Prince's Future",
        "topic": "Bhishma's terrible vow",
        "main_figure": "Devavrata",
        "setting": "the royal court of Hastinapura",
        "mood": "dramatic, emotional, grand",
        "hook": "A prince gave up not just his throne, but his entire future for one promise.",
        "conflict": (
            "Devavrata wanted his father to marry the woman he loved, but her family feared that Devavrata's children would one day claim the throne."
        ),
        "escalation": (
            "Giving up the crown was not enough to remove that fear."
        ),
        "twist": (
            "So he swore lifelong celibacy, ending his own royal line before it even began."
        ),
        "final_line": (
            "The vow was so severe that Devavrata was remembered from then on as Bhishma — the man of the terrible oath."
        )
    },

    {
        "category": "indian_mythology",
        "title": "Shiva Drank What Could Destroy Everything",
        "topic": "Shiva drinks Halahala",
        "main_figure": "Lord Shiva",
        "setting": "the cosmic churning of the ocean",
        "mood": "cosmic, intense, divine",
        "hook": "Before the nectar of immortality appeared, something far worse came out first.",
        "conflict": (
            "A deadly poison emerged from the cosmic ocean, threatening gods, demons, and the entire world."
        ),
        "escalation": (
            "Nobody could safely contain it, and the danger kept spreading."
        ),
        "twist": (
            "Shiva drank the poison himself and held it in his throat instead of letting it enter his body."
        ),
        "final_line": (
            "The poison turned his throat blue, and Neelkanth became a symbol of taking suffering upon oneself to protect others."
        )
    }
]


INDIAN_HISTORY = [
    {
        "category": "indian_history",
        "title": "Shivaji Walked Into Agra and Realized He Was Trapped",
        "topic": "Shivaji's escape from Agra",
        "main_figure": "Chhatrapati Shivaji Maharaj",
        "setting": "Agra during the Mughal era",
        "mood": "tense, clever, rebellious",
        "hook": "Shivaji entered Agra expecting diplomacy. Very quickly, he realized he was effectively trapped.",
        "conflict": (
            "His movements were restricted, and simply walking out was no longer an option."
        ),
        "escalation": (
            "The longer he stayed, the greater the danger became, so escape had to rely on deception rather than force."
        ),
        "twist": (
            "According to popular accounts, Shivaji escaped under disguise and concealment, turning captivity into one of the most famous escapes in Indian history."
        ),
        "final_line": (
            "The remarkable part was not that he fought his way out. It was that he outthought the prison around him."
        )
    },

    {
        "category": "indian_history",
        "title": "Maharana Pratap Lost the Field, Not the Fight",
        "topic": "Maharana Pratap after Haldighati",
        "main_figure": "Maharana Pratap",
        "setting": "Mewar after the Battle of Haldighati",
        "mood": "defiant, rugged, heroic",
        "hook": "Haldighati was brutal, but the real story of Maharana Pratap begins after the battle.",
        "conflict": (
            "He faced military pressure, loss of territory, and years of hardship."
        ),
        "escalation": (
            "Instead of surrendering, he continued resistance from difficult terrain and slowly rebuilt his position."
        ),
        "twist": (
            "The battle did not end his struggle. He later recovered significant parts of Mewar."
        ),
        "final_line": (
            "That is why his legend is less about one battle and more about refusing to disappear after it."
        )
    },

    {
        "category": "indian_history",
        "title": "Ashoka Won Kalinga and Hated What He Saw",
        "topic": "Ashoka after Kalinga",
        "main_figure": "Emperor Ashoka",
        "setting": "the battlefield of Kalinga",
        "mood": "grim, reflective, powerful",
        "hook": "Ashoka won the war. Then he saw what victory had actually cost.",
        "conflict": (
            "The Kalinga campaign brought enormous suffering, death, and displacement."
        ),
        "escalation": (
            "For a ruler known for conquest, the battlefield became something impossible to ignore."
        ),
        "twist": (
            "Instead of celebrating, Ashoka's reign increasingly turned toward dhamma, moral governance, and Buddhist ideals."
        ),
        "final_line": (
            "He conquered Kalinga with an army, but Kalinga changed the emperor."
        )
    },

    {
        "category": "indian_history",
        "title": "The Cholas Didn't Stop at India's Coast",
        "topic": "Rajendra Chola's naval campaign",
        "main_figure": "Rajendra Chola I",
        "setting": "the Bay of Bengal and Southeast Asian trade routes",
        "mood": "grand, adventurous, powerful",
        "hook": "A medieval Indian empire once sent fleets across the sea to project power far beyond the subcontinent.",
        "conflict": (
            "Control of maritime trade routes mattered enormously, and the Cholas had the naval strength to act."
        ),
        "escalation": (
            "Their fleets crossed the Bay of Bengal and struck targets connected to powerful Southeast Asian trading networks."
        ),
        "twist": (
            "The Chola Empire was not only a land power famous for temples. It was also capable of major overseas military operations."
        ),
        "final_line": (
            "For a moment in medieval history, Indian power travelled by sea."
        )
    },

    {
        "category": "indian_history",
        "title": "Lachit Borphukan Fought While Seriously Ill",
        "topic": "Battle of Saraighat",
        "main_figure": "Lachit Borphukan",
        "setting": "the Brahmaputra River at Saraighat",
        "mood": "urgent, brave, patriotic",
        "hook": "Lachit Borphukan was sick, but when the battle began to turn, he still entered the fight.",
        "conflict": (
            "The Ahom forces faced a powerful Mughal attack, and morale was under pressure."
        ),
        "escalation": (
            "The commander himself was physically weak, but staying away risked collapse."
        ),
        "twist": (
            "Lachit personally returned to the battle and helped rally his forces in the river fight at Saraighat."
        ),
        "final_line": (
            "Sometimes the strongest thing a commander can do is simply appear when everyone thinks he cannot."
        )
    },

    {
        "category": "indian_history",
        "title": "Rani Lakshmibai Refused the Ending Chosen for Her",
        "topic": "Rani Lakshmibai's final resistance",
        "main_figure": "Rani Lakshmibai",
        "setting": "Jhansi and central India during 1857",
        "mood": "fiery, tragic, heroic",
        "hook": "The British expected Jhansi to fall quietly. Rani Lakshmibai had another answer.",
        "conflict": (
            "Political pressure, annexation, and rebellion pushed the kingdom into open conflict."
        ),
        "escalation": (
            "Lakshmibai became one of the central resistance figures and continued fighting even after losing control of Jhansi."
        ),
        "twist": (
            "Her death in battle turned a defeated ruler into one of the most enduring symbols of resistance in Indian history."
        ),
        "final_line": (
            "She lost the kingdom, but history never forgot the queen."
        )
    }
]


INTERNATIONAL_HISTORY = [
    {
        "category": "international_history",
        "title": "Napoleon Won Battles but Lost to Winter",
        "topic": "Napoleon's invasion of Russia",
        "main_figure": "Napoleon Bonaparte",
        "setting": "Russia in 1812",
        "mood": "massive, bleak, dramatic",
        "hook": "Napoleon entered Russia with one of the largest armies Europe had seen. Most of it would never return.",
        "conflict": (
            "Russian forces avoided giving him the clean victory he wanted while retreating deeper into the country."
        ),
        "escalation": (
            "Supplies failed, distance grew, and winter turned every mile into a disaster."
        ),
        "twist": (
            "The campaign became less about defeating the enemy and more about surviving the retreat."
        ),
        "final_line": (
            "Napoleon invaded with an army. Russia answered with distance, fire, and cold."
        )
    },

    {
        "category": "international_history",
        "title": "The City That Vanished Under Ash",
        "topic": "Pompeii and Mount Vesuvius",
        "main_figure": "the people of Pompeii",
        "setting": "Pompeii in 79 CE",
        "mood": "eerie, catastrophic, tragic",
        "hook": "A normal Roman city woke up one morning and had no idea it was about to disappear.",
        "conflict": (
            "Mount Vesuvius erupted, filling the sky with ash and volcanic debris."
        ),
        "escalation": (
            "People tried to escape as darkness, heat, and falling material overwhelmed the city."
        ),
        "twist": (
            "Centuries later, the destruction preserved buildings and traces of daily life with haunting detail."
        ),
        "final_line": (
            "Pompeii was destroyed in hours, but that destruction accidentally froze part of its world in time."
        )
    },

    {
        "category": "international_history",
        "title": "The Emperor Who Was Told Rome Was Burning",
        "topic": "Nero and the Great Fire of Rome",
        "main_figure": "Emperor Nero",
        "setting": "Rome in 64 CE",
        "mood": "chaotic, political, controversial",
        "hook": "Rome burned for days, and one emperor's reputation would burn with it for centuries.",
        "conflict": (
            "A massive fire devastated large parts of the city and created panic and political suspicion."
        ),
        "escalation": (
            "Rumors spread that Nero had somehow allowed or even encouraged the disaster."
        ),
        "twist": (
            "Historians still debate many popular stories about his role, including the famous image of him playing music while Rome burned."
        ),
        "final_line": (
            "Sometimes the legend survives longer than the evidence."
        )
    }
]


FANTASY = [
    {
        "category": "fantasy",
        "title": "The Prince Who Fell in Love With Midnight",
        "topic": "a woman who only exists after midnight",
        "main_figure": "a lonely prince",
        "setting": "a cursed moonlit kingdom",
        "mood": "romantic, magical, melancholic",
        "hook": "Every night at exactly midnight, a woman appeared in the palace garden. At sunrise, she vanished.",
        "conflict": (
            "The prince fell in love with her, but she refused to tell him where she came from."
        ),
        "escalation": (
            "He began staying awake every night just to spend a few hours with her."
        ),
        "twist": (
            "Eventually he discovered she was not visiting the kingdom at all. She was someone who had died there a century earlier."
        ),
        "final_line": (
            "He had fallen in love with a memory that the moon refused to forget."
        )
    },

    {
        "category": "fantasy",
        "title": "The King Who Could Hear Lies",
        "topic": "a cursed king who hears lies as screams",
        "main_figure": "a young king",
        "setting": "an ancient mountain kingdom",
        "mood": "dark fantasy, tense, mysterious",
        "hook": "The king's gift sounded useful: every time someone lied, he heard a scream.",
        "conflict": (
            "At first, it made him impossible to deceive."
        ),
        "escalation": (
            "Then the screams became constant — advisers, friends, servants, even his own family."
        ),
        "twist": (
            "The worst scream came when he looked into a mirror and said, 'I am a good king.'"
        ),
        "final_line": (
            "The curse never existed to expose everyone else. It existed to expose him."
        )
    },

    {
        "category": "fantasy",
        "title": "The Dragon Guarded Nothing",
        "topic": "a dragon guarding an empty vault",
        "main_figure": "a thief",
        "setting": "a ruined mountain fortress",
        "mood": "adventurous, mysterious, ironic",
        "hook": "For three hundred years, a dragon guarded the same vault. Everyone assumed unimaginable treasure was inside.",
        "conflict": (
            "A thief spent years preparing to steal it."
        ),
        "escalation": (
            "He survived traps, fire, and the dragon itself just to reach the door."
        ),
        "twist": (
            "When he finally opened the vault, it was empty. The dragon had been guarding the world from what used to be inside."
        ),
        "final_line": (
            "The treasure was never what the dragon protected. The dragon was the lock."
        )
    }
]


ROMANCE_DRAMA = [
    {
        "category": "romance_drama",
        "title": "She Waited at the Same Station for 20 Years",
        "topic": "a tragic railway station romance",
        "main_figure": "a woman waiting for her first love",
        "setting": "an old railway station",
        "mood": "emotional, bittersweet, cinematic",
        "hook": "Every year on the same date, she returned to the same railway platform.",
        "conflict": (
            "Decades earlier, the man she loved had promised to meet her there after leaving for work."
        ),
        "escalation": (
            "He never came back, but she never stopped believing there had been a reason."
        ),
        "twist": (
            "Years later, a stranger brought her an unopened letter that had been found among his belongings after his death."
        ),
        "final_line": (
            "He had never forgotten the meeting. He simply never lived long enough to return."
        )
    },

    {
        "category": "romance_drama",
        "title": "He Married the Wrong Twin",
        "topic": "romantic mistaken identity drama",
        "main_figure": "a young nobleman",
        "setting": "a wealthy family estate",
        "mood": "dramatic, romantic, tense",
        "hook": "He thought he was marrying the woman he loved. Then she walked into the wedding.",
        "conflict": (
            "The bride looked exactly like her, because she was her twin."
        ),
        "escalation": (
            "A family secret, a hidden engagement, and years of resentment came crashing together in one room."
        ),
        "twist": (
            "The woman he loved had secretly arranged the marriage herself because she believed her sister deserved the life she could never have."
        ),
        "final_line": (
            "He came looking for betrayal and found sacrifice instead."
        )
    }
]


COMEDY = [
    {
        "category": "comedy",
        "title": "The Thief Who Accidentally Became Royal Adviser",
        "topic": "a thief mistaken for a genius strategist",
        "main_figure": "an unlucky thief",
        "setting": "a chaotic medieval kingdom",
        "mood": "funny, absurd, fast-paced",
        "hook": "A thief broke into the royal palace to steal gold and walked out with a government job.",
        "conflict": (
            "When guards caught him hiding behind a war map, the king assumed he was a secret military 
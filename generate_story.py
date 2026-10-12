import hashlib
import json
import random

from pathlib import Path


# ============================================================
# FILES
# ============================================================

OUTPUT_FILE = Path("story.json")

HISTORY_FILE = Path(
    "story_history.json"
)


# ============================================================
# CATEGORIES
# ============================================================

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
# STORY POOL
#
# Part 1 stories only.
# ============================================================

STORIES = [


    # ========================================================
    # SUPERNATURAL / MYSTERY
    # ========================================================

    {
        "story_id": "memory_train",

        "part": 1,

        "has_next_part": False,

        "category":
            "supernatural_mystery",

        "title_hook":
            "The Train That Charged Passengers With Memories",

        "topic":
            "A supernatural train takes memories instead of money.",

        "main_figure":
            "a young Indian man named Aarav wearing a dark jacket",

        "setting":
            "an impossible midnight train moving through empty darkness",

        "mood":
            "eerie, emotional, mysterious",

        "opening":
            "Aarav boarded the last train home and immediately noticed something strange. There was no ticket collector, no destination board, and every passenger sat completely silent. Then a conductor appeared and told him that this train did not accept money.",

        "conflict":
            "At the first station, the conductor asked Aarav to pay with one memory. Aarav laughed until he suddenly forgot his tenth birthday. At the next station, he lost the memory of his first kiss. Then he forgot the sound of his father's voice.",

        "escalation":
            "Aarav looked around and finally understood why the other passengers were silent. Some had forgotten how to speak. Others stared at photographs but could no longer recognize the people inside them. The train kept stopping, and every station demanded another memory.",

        "dramatic_reveal":
            "At the final station, the conductor asked for the memory Aarav valued most. Aarav saw his mother's face in his mind and refused. The doors locked. The lights went out. Then the passengers began whispering that nobody had ever refused the final payment.",

        "final_punch":
            "Aarav woke up at home the next morning. His mother hugged him, crying with relief. He hugged her back politely and asked, Who are you?"
    },


    # ========================================================
    # FANTASY
    # ========================================================

    {
        "story_id": "lying_king",

        "part": 1,

        "has_next_part": False,

        "category":
            "fantasy",

        "title_hook":
            "The King Who Could Hear Every Lie",

        "topic":
            "A king gains the ability to hear lies as screams.",

        "main_figure":
            "a young king wearing black and gold royal clothing",

        "setting":
            "a vast ancient royal kingdom and stone palace",

        "mood":
            "dark fantasy, royal, unsettling",

        "opening":
            "After surviving an assassination attempt, a young king woke with a strange gift. Every time someone lied near him, he heard a painful scream that nobody else could hear. At first, he thought the power would make him the greatest ruler alive.",

        "conflict":
            "Merchants lied about prices. Generals lied about victories. Ministers lied about loyalty. Even his closest friends lied about loving him. The screams followed him through every corridor of the palace until he trusted nobody.",

        "escalation":
            "One evening, the queen told him she still loved him. The king heard a scream so violent that he ordered her imprisoned. The next morning she disappeared. Soon he was locking away anyone whose words caused the sound.",

        "dramatic_reveal":
            "An old prisoner finally asked the king to stand before a giant mirror. He said the curse did not scream when other people lied. It screamed whenever the king heard something he desperately wanted to believe.",

        "final_punch":
            "The king stared into the mirror and whispered, My people love me. For the first time, the scream came from inside his own mouth."
    },


    # ========================================================
    # INDIAN FOLKTALE
    # ========================================================

    {
        "story_id": "unlocked_village",

        "part": 1,

        "has_next_part": True,

        "category":
            "indian_folktale",

        "title_hook":
            "The Village Where Nobody Locked Their Doors",

        "topic":
            "A peaceful village hides a supernatural reason for leaving every door unlocked.",

        "main_figure":
            "a young traveler wearing simple traditional Indian clothing",

        "setting":
            "an isolated old Indian village surrounded by forest",

        "mood":
            "folk horror, mysterious, atmospheric",

        "opening":
            "A traveler reached a tiny village just before sunset and noticed something impossible. Every house had a door, but none had a lock. Gold jewellery sat openly near windows, yet nobody seemed afraid of thieves.",

        "conflict":
            "When the traveler asked why, the villagers became nervous. An old woman warned him that doors were never locked after dark. She refused to explain further and simply told him to sleep with his door wide open.",

        "escalation":
            "That night the traveler heard slow footsteps outside. They stopped at every house. Something entered one home, crossed through it, exited from the back, and moved to the next. The footsteps eventually reached his room.",

        "dramatic_reveal":
            "Terrified, the traveler slammed his door shut and locked it. The footsteps stopped outside immediately. Then someone knocked three times. A child's voice whispered from the other side, You weren't supposed to make it notice you.",

        "final_punch":
            "The traveler backed away from the door. Then he heard the same child's voice whisper again, this time from underneath his bed."
    },


    # ========================================================
    # INDIAN MYTHOLOGY
    # ========================================================

    {
        "story_id": "bhishma_death",

        "part": 1,

        "has_next_part": False,

        "category":
            "indian_mythology",

        "title_hook":
            "The Warrior Who Chose the Moment of His Own Death",

        "topic":
            "The extraordinary boon of Bhishma from the Mahabharata.",

        "main_figure":
            "Bhishma, an elderly legendary Indian warrior with white hair and royal armor",

        "setting":
            "the battlefield of Kurukshetra in ancient India",

        "mood":
            "epic, tragic, spiritual",

        "opening":
            "Bhishma was not simply one of the greatest warriors of the Mahabharata. He carried an extraordinary boon called Iccha Mrityu, the power to choose the moment of his own death.",

        "conflict":
            "During the battle of Kurukshetra, Arjuna faced Bhishma with Shikhandi before him. Bhishma refused to raise his weapons against Shikhandi, allowing Arjuna's arrows to strike him again and again.",

        "escalation":
            "So many arrows pierced Bhishma that when he finally fell, his body never touched the ground. He rested upon a bed made entirely of arrows while warriors from both armies gathered around him.",

        "dramatic_reveal":
            "But Bhishma still did not die. Because of his boon, death could not take him until he allowed it. He chose to remain alive on the battlefield until the sun began its northward journey.",

        "final_punch":
            "For weeks Bhishma lay upon the arrows, teaching kings and warriors. Only when the moment he had chosen finally arrived did one of India's greatest warriors willingly release his life."
    },


    # ========================================================
    # ROMANCE / DRAMA
    # ========================================================

    {
        "story_id": "future_messages",

        "part": 1,

        "has_next_part": False,

        "category":
            "romance_drama",

        "title_hook":
            "He Received Her Messages Five Years After She Died",

        "topic":
            "A man begins receiving impossible messages from his dead girlfriend.",

        "main_figure":
            "a young Indian man named Rohan wearing modern casual clothing",

        "setting":
            "a modern Indian city, apartment rooms and quiet streets at night",

        "mood":
            "romantic, melancholic, mysterious",

        "opening":
            "Five years after losing his girlfriend Maya in an accident, Rohan's phone buzzed at exactly midnight. The message was from Maya's old number. It simply said, Don't take the highway tomorrow.",

        "conflict":
            "Rohan assumed it was a cruel prank, but the next morning a major accident blocked the same highway. Another message arrived that night telling him to call his mother. Minutes after he called, she collapsed and he managed to get help in time.",

        "escalation":
            "The messages continued. Each one warned him about something that had not happened yet. Rohan tried calling the number, but it was disconnected. He visited the old phone company and learned that Maya's number had never been reassigned.",

        "dramatic_reveal":
            "Then one final message appeared. It said, Tomorrow you will meet me again. Rohan spent the entire day terrified until a little girl approached him at a railway station and handed him an old phone he instantly recognized as Maya's.",

        "final_punch":
            "The phone contained one unsent message dated five years earlier. Maya had written, If there is any way back to you, I promise I'll find it."
    },


    # ========================================================
    # COMEDY
    # ========================================================

    {
        "story_id": "lucky_thief",

        "part": 1,

        "has_next_part": False,

        "category":
            "comedy",

        "title_hook":
            "The Thief Who Accidentally Became Prime Minister",

        "topic":
            "A terrible thief repeatedly fails upward.",

        "main_figure":
            "a nervous young thief wearing shabby dark clothes",

        "setting":
            "a fictional colourful kingdom filled with markets and royal buildings",

        "mood":
            "fast, absurd, comedic",

        "opening":
            "A thief named Kallu decided to rob the royal treasury. Unfortunately, he entered the wrong building and accidentally walked into a secret government meeting where everyone assumed he was the new economic adviser.",

        "conflict":
            "Kallu tried escaping, but every nonsense sentence he spoke was treated as genius. When he suggested hiding the treasury so thieves could not find it, the ministers called it revolutionary financial security.",

        "escalation":
            "Within a week he became finance minister. He tried getting himself fired by proposing ridiculous ideas, but each disaster somehow improved the kingdom. Taxes became simpler. Corruption dropped. Even food prices fell by accident.",

        "dramatic_reveal":
            "The king finally announced that he was retiring and named Kallu as his successor. Kallu panicked and confessed that he was actually a thief who had entered the palace to steal gold.",

        "final_punch":
            "The ministers applauded. They said it was the first honest statement any politician had made in years and promoted him immediately."
    },


    # ========================================================
    # INDIAN LEGEND
    # ========================================================

    {
        "story_id": "black_door_palace",

        "part": 1,

        "has_next_part": True,

        "category":
            "indian_legend",

        "title_hook":
            "The Palace Room That Was Never Opened",

        "topic":
            "A prince opens a forbidden room inside an ancient palace.",

        "main_figure":
            "a young Indian prince wearing dark traditional royal clothing",

        "setting":
            "an enormous ancient Indian palace during a storm",

        "mood":
            "royal, supernatural, ominous",

        "opening":
            "For hundreds of years, one black door inside the royal palace had never been opened. Every ruler was given the same warning. The room behind it belonged to the dead, and no living person was permitted to enter.",

        "conflict":
            "A young prince eventually decided the warning was nothing more than superstition. During a violent storm, he stole the ancient key and opened the black door while the palace guards slept.",

        "escalation":
            "Inside he found no treasure. The chamber contained dozens of mirrors and names carved into the stone walls. Every name belonged to a member of the royal family who had disappeared without explanation.",

        "dramatic_reveal":
            "The prince stepped toward the largest mirror. Instead of his own reflection, he saw his missing relatives standing inside it. Behind them stood another version of the prince, smiling directly at him.",

        "final_punch":
            "The guards heard the prince scream and rushed toward the chamber. When they opened the door, the room was empty. A new name had been carved into the wall."
    },
]


# ============================================================
# PART TWO STORIES
# ============================================================

PART_TWOS = {


    # ========================================================
    # UNLOCKED VILLAGE PART 2
    # ========================================================

    "unlocked_village": {

        "story_id":
            "unlocked_village",

        "part":
            2,

        "has_next_part":
            False,

        "category":
            "indian_folktale",

        "title_hook":
            "The Thing That Was Already Inside the House",

        "topic":
            "The mystery of the unlocked village continues.",

        "main_figure":
            "the same young traveler wearing simple traditional Indian clothing",

        "setting":
            "the isolated old Indian village at night",

        "mood":
            "folk horror, dark, supernatural",

        "opening":
            "The traveler froze when the child's voice came from underneath his bed. He slowly looked down, expecting to see someone hiding there. But beneath the bed was completely empty.",

        "conflict":
            "Outside, the villagers began screaming for him to open the door. They warned him that locking the house had trapped the wandering thing inside with him. The traveler rushed toward the door, but something began walking behind him.",

        "escalation":
            "He turned and saw nothing. Then every family portrait on the wall changed at once. A pale stranger now stood behind each family, smiling. In the newest portrait, the traveler himself appeared inside the house.",

        "dramatic_reveal":
            "The old woman shouted through the window that the creature never entered houses at night. The open doors allowed it to leave. By locking the door, the traveler had prevented something that was already inside from escaping.",

        "final_punch":
            "The traveler unlocked the door and ran outside. At sunrise everyone was safe. But in the portrait inside the house, the stranger was gone and the traveler was still trapped inside the frame."
    },


    # ========================================================
    # BLACK DOOR PALACE PART 2
    # ========================================================

    "black_door_palace": {

        "story_id":
            "black_door_palace",

        "part":
            2,

        "has_next_part":
            False,

        "category":
            "indian_legend",

        "title_hook":
            "The Prince Wasn't Trapped Alone",

        "topic":
            "The forbidden palace room reveals its true purpose.",

        "main_figure":
            "the same young Indian prince wearing dark traditional royal clothing",

        "setting":
            "the ancient Indian palace and supernatural mirror chamber",

        "mood":
            "royal, supernatural, terrifying",

        "opening":
            "The prince opened his eyes and found himself standing inside the mirror world. The palace looked almost identical, but the corridors were silent and every torch burned with cold blue fire.",

        "conflict":
            "His missing relatives emerged from the darkness. Some had been trapped for decades. Others had vanished centuries earlier. They told him the chamber was not a tomb. It was a prison.",

        "escalation":
            "The prince searched desperately for a way out. Every mirror showed the real palace on the other side. He could see guards searching the empty room, but no matter how hard he struck the glass, nobody could hear him.",

        "dramatic_reveal":
            "Then one relative revealed the truth. Every time someone entered the chamber, the mirror created a copy. The copy escaped into the real world while the original remained trapped forever.",

        "final_punch":
            "Outside the chamber, the guards finally found the prince walking calmly through the palace. But inside the mirror, the real prince watched his smiling copy sit upon the throne."
    },
}


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
            )
        )


        if isinstance(
            data,
            list
        ):

            return data


        return []


    except Exception as error:

        print(
            "Could not load story history:",
            error
        )

        return []


# ============================================================
# SAVE HISTORY
# ============================================================

def save_history(
    history
):

    HISTORY_FILE.write_text(
        json.dumps(
            history,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


# ============================================================
# STORY FINGERPRINT
# ============================================================

def make_fingerprint(
    story
):

    source = "|".join([
        str(
            story.get(
                "story_id",
                ""
            )
        ),

        str(
            story.get(
                "part",
                ""
            )
        ),

        story.get(
            "title_hook",
            ""
        ),
    ])


    return hashlib.sha256(
        source.encode(
            "utf-8"
        )
    ).hexdigest()


# ============================================================
# CHECK FOR REQUIRED PART TWO
# =======================

# ============================================================
# RELIABLE RUNNER - KEEP THIS AT VERY BOTTOM
# ============================================================

def main():
    import json
    import random
    import hashlib
    from pathlib import Path

    output_file = Path("story.json")
    history_file = Path("story_history.json")

    print("AI MANIA reliable story runner started")

    # --------------------------------------------------------
    # LOAD HISTORY
    # --------------------------------------------------------

    history = []

    if history_file.exists():
        try:
            data = json.loads(
                history_file.read_text(
                    encoding="utf-8"
                )
            )

            if isinstance(data, list):
                history = data

        except Exception as error:
            print(
                "History warning:",
                error
            )


    # --------------------------------------------------------
    # GET EXISTING STORY POOL
    # --------------------------------------------------------

    story_pool = globals().get(
        "STORIES",
        []
    )

    part_twos = globals().get(
        "PART_TWOS",
        {}
    )


    if not isinstance(
        story_pool,
        list
    ):
        story_pool = []


    if not isinstance(
        part_twos,
        dict
    ):
        part_twos = {}


    # --------------------------------------------------------
    # EMERGENCY FALLBACK
    #
    # Means workflow STILL works even if the large story pool
    # above gets damaged later.
    # --------------------------------------------------------

    fallback_stories = [

        {
            "story_id": "memory_clock",
            "part": 1,
            "has_next_part": False,
            "category": "supernatural_mystery",
            "title_hook":
                "The Clock That Counted Down His Memories",
            "topic":
                "A mysterious clock erases one memory every hour.",
            "main_figure":
                "a young Indian man named Kabir",
            "setting":
                "a small apartment in an Indian city at midnight",
            "mood":
                "mysterious, emotional, supernatural",

            "opening":
                "Kabir bought an antique clock from a shop that disappeared the very next day. At midnight, the clock began counting backward instead of forward. When it struck eleven, Kabir suddenly forgot the name of his childhood school.",

            "conflict":
                "At ten, he forgot his best friend's face. At nine, an entire year of college vanished from his memory. Kabir smashed the clock against the floor, but the broken hands kept moving backward.",

            "escalation":
                "He searched inside the clock and discovered tiny photographs hidden behind its face. Every photograph showed a memory he had already lost. One final picture showed his mother standing beside him.",

            "dramatic_reveal":
                "The clock reached one minute before midnight. Kabir realized the final photograph was not showing a memory from the past. It showed his mother standing outside his apartment at that exact moment.",

            "final_punch":
                "Someone knocked on the door. Kabir opened it and saw the woman from the photograph. She hugged him tightly. Kabir stared at her and asked, Have we met before?"
        },

        {
            "story_id": "shadow_market",
            "part": 1,
            "has_next_part": False,
            "category": "indian_folktale",
            "title_hook":
                "The Market That Opened Only After Midnight",
            "topic":
                "A traveler discovers a marketplace where memories are sold.",
            "main_figure":
                "a young Indian traveler named Dev",
            "setting":
                "an ancient Indian market hidden inside narrow streets at midnight",
            "mood":
                "mysterious, magical, unsettling",

            "opening":
                "Dev became lost in an old city just after midnight and discovered a crowded market that had not existed during the day. Nobody sold food, jewellery or clothes. Every stall sold memories.",

            "conflict":
                "One merchant offered Dev the memory of becoming rich. Another offered the happiest day of a stranger's life. Dev laughed until he found a small bottle labelled with his own name.",

            "escalation":
                "Inside the bottle he saw himself returning home the following morning. His family was crying, but nobody could see him standing beside them. Dev demanded to know who had placed his future inside the bottle.",

            "dramatic_reveal":
                "The merchant quietly pointed toward an empty stall across the market. A sign above it carried Dev's name. Beneath the sign was tomorrow's date.",

            "final_punch":
                "Dev ran from the market before sunrise. When he reached home, his mother opened the door, looked straight through him, and asked who was there."
        }

    ]


    # --------------------------------------------------------
    # IF ORIGINAL POOL IS EMPTY, USE FALLBACK
    # --------------------------------------------------------

    if not story_pool:

        print(
            "WARNING: original STORIES pool missing."
        )

        print(
            "Using emergency fallback stories."
        )

        story_pool = fallback_stories


    # --------------------------------------------------------
    # CHECK WHETHER PART 2 IS PENDING
    # --------------------------------------------------------

    selected = None

    if history:

        latest = history[-1]

        if isinstance(
            latest,
            dict
        ):

            pending = latest.get(
                "next_part_pending",
                False
            )

            pending_id = latest.get(
                "story_id"
            )

            if (
                pending
                and pending_id
                in part_twos
            ):

                selected = dict(
                    part_twos[
                        pending_id
                    ]
                )

                print(
                    "Generating pending Part 2:",
                    pending_id
                )


    # --------------------------------------------------------
    # SELECT FRESH STORY
    # --------------------------------------------------------

    if selected is None:

        recently_used = set()

        for item in history[-6:]:

            if isinstance(
                item,
                dict
            ):

                story_id = item.get(
                    "story_id"
                )

                if story_id:

                    recently_used.add(
                        story_id
                    )


        available = [

            story

            for story in story_pool

            if story.get(
                "story_id"
            )
            not in recently_used

        ]


        if not available:

            available = story_pool


        selected = dict(
            random.choice(
                available
            )
        )

        print(
            "Fresh story selected:",
            selected.get(
                "story_id"
            )
        )


    # --------------------------------------------------------
    # REQUIRED DEFAULTS
    # --------------------------------------------------------

    selected.setdefault(
        "story_id",
        "ai_mania_story"
    )

    selected.setdefault(
        "part",
        1
    )

    selected.setdefault(
        "has_next_part",
        False
    )

    selected.setdefault(
        "category",
        "supernatural_mystery"
    )

    selected.setdefault(
        "title_hook",
        "An Impossible Story"
    )

    selected.setdefault(
        "topic",
        selected[
            "title_hook"
        ]
    )

    selected.setdefault(
        "main_figure",
        "a mysterious traveler"
    )

    selected.setdefault(
        "setting",
        "a cinematic mysterious location"
    )

    selected.setdefault(
        "mood",
        "cinematic and mysterious"
    )


    # --------------------------------------------------------
    # VALIDATE STORY TEXT
    # --------------------------------------------------------

    required_story_sections = [

        "opening",
        "conflict",
        "escalation",
        "dramatic_reveal",
        "final_punch",

    ]


    missing = [

        key

        for key
        in required_story_sections

        if not selected.get(
            key
        )

    ]


    if missing:

        raise RuntimeError(
            "Selected story missing: "
            + ", ".join(
                missing
            )
        )


    # --------------------------------------------------------
    # CONTINUATION LINE
    # --------------------------------------------------------

    if selected.get(
        "has_next_part",
        False
    ):

        if (
            "part two"
            not in selected[
                "final_punch"
            ].lower()
        ):

            selected[
                "final_punch"
            ] += (
                " But this story isn't over. "
                "Part two is next."
            )


    # --------------------------------------------------------
    # SCREENPLAY
    # --------------------------------------------------------

    selected[
        "screenplay"
    ] = " ".join([

        selected[
            "title_hook"
        ]
        + ".",

        selected[
            "opening"
        ],

        selected[
            "conflict"
        ],

        selected[
            "escalation"
        ],

        selected[
            "dramatic_reveal"
        ],

        selected[
            "final_punch"
        ],

    ])


    # --------------------------------------------------------
    # FINGERPRINT
    # --------------------------------------------------------

    fingerprint_source = "|".join([

        str(
            selected[
                "story_id"
            ]
        ),

        str(
            selected[
                "part"
            ]
        ),

        selected[
            "title_hook"
        ],

    ])


    selected[
        "fingerprint"
    ] = hashlib.sha256(

        fingerprint_source.encode(
            "utf-8"
        )

    ).hexdigest()


    # --------------------------------------------------------
    # WRITE STORY.JSON
    # --------------------------------------------------------

    output_file.write_text(

        json.dumps(
            selected,
            indent=2,
            ensure_ascii=False
        ),

        encoding="utf-8"

    )


    if not output_file.exists():

        raise RuntimeError(
            "story.json was not created"
        )


    if output_file.stat().st_size < 100:

        raise RuntimeError(
            "story.json is too small"
        )


    # --------------------------------------------------------
    # UPDATE HISTORY
    # --------------------------------------------------------

    history.append({

        "story_id":
            selected[
                "story_id"
            ],

        "part":
            selected[
                "part"
            ],

        "category":
            selected[
                "category"
            ],

        "title_hook":
            selected[
                "title_hook"
            ],

        "fingerprint":
            selected[
                "fingerprint"
            ],

        "next_part_pending":
            bool(
                selected.get(
                    "has_next_part",
                    False
                )
            ),

    })


    history_file.write_text(

        json.dumps(
            history[-200:],
            indent=2,
            ensure_ascii=False
        ),

        encoding="utf-8"

    )


    print("")
    print(
        "================================="
    )

    print(
        "STORY CREATED SUCCESSFULLY"
    )

    print(
        "================================="
    )

    print(
        "Title:",
        selected[
            "title_hook"
        ]
    )

    print(
        "Part:",
        selected[
            "part"
        ]
    )

    print(
        "Words:",
        len(
            selected[
                "screenplay"
            ].split()
        )
    )

    print(
        "story.json:",
        output_file.stat().st_size,
        "bytes"
    )


# ============================================================
# DO NOT REMOVE THESE TWO LINES
# ============================================================

if __name__ == "__main__":
    main()
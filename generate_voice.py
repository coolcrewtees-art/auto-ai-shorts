import asyncio
import json
import re
import edge_tts

# Voices
INDIAN_VOICE = "en-IN-PrabhatNeural"
GLOBAL_VOICE = "en-US-AndrewMultilingualNeural"

# These substitutions affect ONLY speech.
# story.json and captions remain correctly spelled.
PRONUNCIATIONS = {
    "Ashwatthama": "Ashwatthaama",
    "Bhishma": "Bheeshma",
    "Karna": "Karn",
    "Kurukshetra": "Kuru kshetra",
    "Dronacharya": "Dronaachaarya",
    "Duryodhana": "Duryodhan",
    "Yudhishthira": "Yudhishthir",
    "Arjuna": "Arjun",
    "Lakshmana": "Lakshman",
    "Hanuman": "Hunoomaan",
    "Halahala": "Halaa hala",
    "Neelkanth": "Neel kanth",
    "Shivaji": "Shivaaji",
    "Chhatrapati": "Chhatrapati",
    "Maharaj": "Mahaaraaj",
    "Maharana": "Mahaaraana",
    "Pratap": "Prataap",
    "Haldighati": "Haldee ghaatee",
    "Lachit Borphukan": "Laachit Borphukan",
    "Saraighat": "Saraai ghaat",
    "Rajendra Chola": "Raajendra Chola",
    "Kalinga": "Kalinga",
    "Mewar": "Maywaar"
}


def fix_pronunciation(text):
    for original, spoken in PRONUNCIATIONS.items():
        text = re.sub(
            rf"\b{re.escape(original)}\b",
            spoken,
            text,
            flags=re.IGNORECASE
        )

    return text


async def main():

    with open("story.json", "r", encoding="utf-8") as f:
        story = json.load(f)

    text = story["screenplay"]
    category = story.get("category", "")

    # Indian content gets Indian English pronunciation
    if category in ["indian_mythology", "indian_history"]:
        voice = INDIAN_VOICE
        text = fix_pronunciation(text)

        rate = "-3%"
        pitch = "-2Hz"

    else:
        voice = GLOBAL_VOICE

        rate = "-4%"
        pitch = "-2Hz"

    print("Category:", category)
    print("Voice:", voice)
    print("Speech text:", text)

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume="+0%"
    )

    await communicate.save("voice.mp3")

    print("Narration generated successfully.")


asyncio.run(main())
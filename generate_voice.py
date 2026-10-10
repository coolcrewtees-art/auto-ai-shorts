import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts


TEMP_DIR = Path("voice_parts")
TEMP_DIR.mkdir(exist_ok=True)

OUTPUT_AUDIO = "voice.mp3"
TIMING_FILE = "voice_timing.json"


# ============================================================
# VOICES
# ============================================================

INDIAN_VOICE = "en-IN-PrabhatNeural"
GLOBAL_VOICE = "en-US-AndrewMultilingualNeural"


# ============================================================
# PRONUNCIATION FIXES
# Only affects spoken audio, not captions.
# ============================================================

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
    "Neelkanth": "Neel kanth",
    "Shivaji": "Shivaaji",
    "Maharana": "Mahaaraana",
    "Pratap": "Prataap",
    "Haldighati": "Haldee ghaatee",
    "Mewar": "Maywaar",
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


# ============================================================
# AUDIO HELPERS
# ============================================================

def duration(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(filename)
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


def make_silence(filename, seconds):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(seconds),
            "-q:a", "9",
            "-acodec", "libmp3lame",
            str(filename)
        ],
        check=True
    )


async def speak(text, voice, rate, pitch, filename):

    communication = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume="+0%"
    )

    await communication.save(str(filename))


# ============================================================
# MAIN
# ============================================================

async def main():

    with open("story.json", "r", encoding="utf-8") as f:
        story = json.load(f)

    category = story["category"]

    if category.startswith("indian_"):
        voice = INDIAN_VOICE
    else:
        voice = GLOBAL_VOICE
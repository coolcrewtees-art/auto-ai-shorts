import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts


# ============================================================
# PATHS
# ============================================================

TEMP_DIR = Path("voice_parts")
TEMP_DIR.mkdir(exist_ok=True)

OUTPUT_AUDIO = Path("voice.mp3")
TIMING_FILE = Path("voice_timing.json")


# ============================================================
# VOICES
# ============================================================

INDIAN_VOICE = "en-IN-PrabhatNeural"
GLOBAL_VOICE = "en-US-AndrewMultilingualNeural"


# ============================================================
# PRONUNCIATION FIXES
# These affect speech only, not written captions.
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
            flags=re.IGNORECASE,
        )
    return text


# ============================================================
# HELPERS
# ============================================================

def get_duration(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(filename),
        ],
        capture_output=True,
        text=True,
        check=True,
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
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            str(filename),
        ],
        check=True,
    )


async def speak(text, voice, rate, pitch, filename):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume="+0%",
    )

    await communicate.save(str(filename))

    if not filename.exists():
        raise RuntimeError(
            f"TTS failed to create {filename}"
        )


# ============================================================
# MAIN
# ============================================================

async def main():

    with open("story.json", "r", encoding="utf-8") as f:
        story = json.load(f)

    category = story.get("category", "")

    if category.startswith("indian_"):
        voice = INDIAN_VOICE
    else:
        voice = GLOBAL_VOICE

    print("Category:", category)
    print("Voice:", voice)

    # --------------------------------------------------------
    # EXPRESSIVE STORY PARTS
    # --------------------------------------------------------

    parts = [
        {
            "name": "title_hook",
            "text": story["title_hook"],
            "rate": "-10%",
            "pitch": "-4Hz",
            "pause_after": 0.80,
            "expression": "dramatic_hook",
        },
        {
            "name": "opening",
            "text": story["opening"],
            "rate": "+5%",
            "pitch": "-1Hz",
            "pause_after": 0.20,
            "expression": "story",
        },
        {
            "name": "conflict",
            "text": story["conflict"],
            "rate": "+7%",
            "pitch": "-1Hz",
            "pause_after": 0.20,
            "expression": "tension",
        },
        {
            "name": "escalation",
            "text": story["escalation"],
            "rate": "+10%",
            "pitch": "+0Hz",
            "pause_after": 0.18,
            "expression": "urgent",
        },
        {
            "name": "dramatic_reveal",
            "text": story["dramatic_reveal"],
            "rate": "-3%",
            "pitch": "-4Hz",
            "pause_after": 0.65,
            "expression": "reveal",
        },
        {
            "name": "final_punch",
            "text": story["final_punch"],
            "rate": "-7%",
            "pitch": "-5Hz",
            "pause_after": 0.70,
            "expression": "final",
        },
    ]

    concat_entries = []
    timing = []
    current_time = 0.0

    # --------------------------------------------------------
    # GENERATE EACH PART
    # --------------------------------------------------------

    for index, part in enumerate(parts):

        spoken_text = part["text"]

        if category.startswith("indian_"):
            spoken_text = fix_pronunciation(
                spoken_text
            )

        audio_file = TEMP_DIR / (
            f"{index:02d}_{part['name']}.mp3"
        )

        print(
            f"Generating {part['name']} "
            f"| rate={part['rate']} "
            f"| pitch={part['pitch']}"
        )

        await speak(
            spoken_text,
            voice,
            part["rate"],
            part["pitch"],
            audio_file,
        )

        part_duration = get_duration(audio_file)

        start = current_time
        end = start + part_duration

        timing.append(
            {
                "name": part["name"],
                "text": part["text"],
                "expression": part["expression"],
                "start": round(start, 3),
                "end": round(end, 3),
                "duration": round(
                    part_duration,
                    3,
                ),
            }
        )

        concat_entries.append(audio_file)

        current_time = end

        # ----------------------------------------
        # ADD PAUSE AFTER SECTION
        # ----------------------------------------

        pause = part["pause_after"]

        if pause > 0:
            silence_file = TEMP_DIR / (
                f"{index:02d}_pause.mp3"
            )

            make_silence(
                silence_file,
                pause,
            )

            concat_entries.append(
                silence_file
            )

            current_time += pause

    # --------------------------------------------------------
    # CONCAT LIST
    # --------------------------------------------------------

    concat_file = TEMP_DIR / "concat.txt"

    with open(
        concat_file,
        "w",
        encoding="utf-8"
    ) as f:

        for item in concat_entries:
            f.write(
                f"file '{item.resolve()}'\n"
            )

    # --------------------------------------------------------
    # BUILD FINAL VOICE.MP3
    # --------------------------------------------------------

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            str(OUTPUT_AUDIO),
        ],
        check=True,
    )

    # --------------------------------------------------------
    # VERIFY OUTPUT
    # --------------------------------------------------------

    if not OUTPUT_AUDIO.exists():
        raise RuntimeError(
            "voice.mp3 was not created"
        )

    if OUTPUT_AUDIO.stat().st_size < 5000:
        raise RuntimeError(
            "voice.mp3 was created but is suspiciously small"
        )

    final_duration = get_duration(
        OUTPUT_AUDIO
    )

    # --------------------------------------------------------
    # SAVE TIMING DATA
    # --------------------------------------------------------

    TIMING_FILE.write_text(
        json.dumps(
            timing,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    if not TIMING_FILE.exists():
        raise RuntimeError(
            "voice_timing.json was not created"
        )

    print("")
    print("==============================")
    print("EXPRESSIVE NARRATION CREATED")
    print("==============================")
    print("Voice:", voice)
    print("File:", OUTPUT_AUDIO)
    print(
        f"Duration: "
        f"{final_duration:.2f}s"
    )
    print(
        f"Size: "
        f"{OUTPUT_AUDIO.stat().st_size} bytes"
    )
    print(
        "Timing file:",
        TIMING_FILE
    )
    print("==============================")


# ============================================================
# ACTUALLY RUN MAIN
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())
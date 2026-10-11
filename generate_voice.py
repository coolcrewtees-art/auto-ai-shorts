import asyncio
import json
import re
import subprocess
from pathlib import Path

import edge_tts


TEMP_DIR = Path("voice_parts")
TEMP_DIR.mkdir(exist_ok=True)

OUTPUT_AUDIO = Path("voice.mp3")
TIMING_FILE = Path("voice_timing.json")

# Use the voice you originally liked for EVERYTHING.
VOICE = "en-US-AndrewMultilingualNeural"


# ============================================================
# PRONUNCIATION FIXES
#
# Only the spoken version is modified.
# Captions/story.json keep the proper spelling.
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
    "Halahala": "Halaa hala",
    "Krishna": "Krishna",
    "Indra": "Indra",
    "Mahabharata": "Mahaa bhaarata",
    "Ramayana": "Raamaayana",
}


def pronunciation_fix(text):
    for original, spoken in PRONUNCIATIONS.items():
        text = re.sub(
            rf"\b{re.escape(original)}\b",
            spoken,
            text,
            flags=re.IGNORECASE,
        )

    return text


# ============================================================
# AUDIO HELPERS
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


def make_pause(filename, seconds):
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


async def create_voice(
    text,
    rate,
    pitch,
    filename,
):
    text = pronunciation_fix(text)

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
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

    with open(
        "story.json",
        "r",
        encoding="utf-8",
    ) as f:
        story = json.load(f)

    # Faster and more contrast between story sections.
    sections = [
        {
            "name": "title_hook",
            "text": story["title_hook"],
            "rate": "+4%",
            "pitch": "-6Hz",
            "pause": 0.42,
        },

        {
            "name": "opening",
            "text": story["opening"],
            "rate": "+17%",
            "pitch": "-1Hz",
            "pause": 0.08,
        },

        {
            "name": "conflict",
            "text": story["conflict"],
            "rate": "+19%",
            "pitch": "+0Hz",
            "pause": 0.06,
        },

        {
            "name": "escalation",
            "text": story["escalation"],
            "rate": "+22%",
            "pitch": "+1Hz",
            "pause": 0.06,
        },

        {
            "name": "dramatic_reveal",
            "text": story["dramatic_reveal"],
            "rate": "+10%",
            "pitch": "-5Hz",
            "pause": 0.30,
        },

        {
            "name": "final_punch",
            "text": story["final_punch"],
            "rate": "+6%",
            "pitch": "-6Hz",
            "pause": 0.20,
        },
    ]

    files = []
    timing = []

    current_time = 0.0

    for index, section in enumerate(sections):

        output = (
            TEMP_DIR
            / f"{index:02d}_{section['name']}.mp3"
        )

        print(
            f"Generating {section['name']} "
            f"| rate {section['rate']} "
            f"| pitch {section['pitch']}"
        )

        await create_voice(
            section["text"],
            section["rate"],
            section["pitch"],
            output,
        )

        part_duration = get_duration(output)

        start = current_time
        end = start + part_duration

        timing.append(
            {
                "name": section["name"],
                "text": section["text"],
                "start": round(start, 3),
                "end": round(end, 3),
                "duration": round(
                    part_duration,
                    3,
                ),
            }
        )

        files.append(output)

        current_time = end

        if section["pause"] > 0:

            pause_file = (
                TEMP_DIR
                / f"{index:02d}_pause.mp3"
            )

            make_pause(
                pause_file,
                section["pause"],
            )

            files.append(
                pause_file
            )

            current_time += (
                section["pause"]
            )

    # --------------------------------------------------------
    # CONCAT EVERYTHING
    # --------------------------------------------------------

    concat_file = (
        TEMP_DIR / "concat.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8",
    ) as f:

        for file in files:
            f.write(
                f"file '{file.resolve()}'\n"
            )

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

    if not OUTPUT_AUDIO.exists():
        raise RuntimeError(
            "voice.mp3 was not created"
        )

    if OUTPUT_AUDIO.stat().st_size < 5000:
        raise RuntimeError(
            "voice.mp3 is suspiciously small"
        )

    TIMING_FILE.write_text(
        json.dumps(
            timing,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    total_duration = get_duration(
        OUTPUT_AUDIO
    )

    print("")
    print("==============================")
    print("NARRATION CREATED")
    print("==============================")
    print("Voice:", VOICE)
    print(
        "Duration:",
        round(total_duration, 2),
        "seconds",
    )
    print(
        "Audio:",
        OUTPUT_AUDIO,
    )
    print(
        "Timing:",
        TIMING_FILE,
    )
    print("==============================")


if __name__ == "__main__":
    asyncio.run(main())
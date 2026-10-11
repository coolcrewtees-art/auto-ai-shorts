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

INDIAN_VOICE = "en-IN-PrabhatNeural"
GLOBAL_VOICE = "en-US-AndrewMultilingualNeural"


PRONUNCIATIONS = {
    "Ashwatthama": "Ashwatthaama",
    "Bhishma": "Bheeshma",
    "Karna": "Karn",
    "Kurukshetra": "Kuru kshetra",
    "Dronacharya": "Dronaachaarya",
    "Duryodhana": "Duryodhan",
    "Arjuna": "Arjun",
    "Lakshmana": "Lakshman",
    "Hanuman": "Hunoomaan",
    "Neelkanth": "Neel kanth",
}


def pronunciation(text):

    for original, spoken in PRONUNCIATIONS.items():

        text = re.sub(
            rf"\b{re.escape(original)}\b",
            spoken,
            text,
            flags=re.IGNORECASE
        )

    return text


def duration(filename):

    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(filename)
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(
        result.stdout.strip()
    )


async def speak(
    text,
    voice,
    rate,
    pitch,
    filename
):

    tts = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )

    await tts.save(
        str(filename)
    )


def make_pause(
    filename,
    seconds
):

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f", "lavfi",
            "-i",
            "anullsrc=r=44100:cl=stereo",
            "-t", str(seconds),
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            str(filename)
        ],
        check=True
    )


async def main():

    with open(
        "story.json",
        "r",
        encoding="utf-8"
    ) as f:

        story = json.load(f)

    category = story["category"]

    if category.startswith("indian_"):
        voice = INDIAN_VOICE
    else:
        voice = GLOBAL_VOICE

    # Much faster than the previous version.
    sections = [
        {
            "name": "title_hook",
            "text": story["title_hook"],
            "rate": "+2%",
            "pitch": "-5Hz",
            "pause": 0.55,
        },

        {
            "name": "opening",
            "text": story["opening"],
            "rate": "+15%",
            "pitch": "-1Hz",
            "pause": 0.10,
        },

        {
            "name": "conflict",
            "text": story["conflict"],
            "rate": "+17%",
            "pitch": "+0Hz",
            "pause": 0.08,
        },

        {
            "name": "escalation",
            "text": story["escalation"],
            "rate": "+20%",
            "pitch": "+1Hz",
            "pause": 0.08,
        },

        {
            "name": "dramatic_reveal",
            "text": story["dramatic_reveal"],
            "rate": "+8%",
            "pitch": "-4Hz",
            "pause": 0.38,
        },

        {
            "name": "final_punch",
            "text": story["final_punch"],
            "rate": "+4%",
            "pitch": "-5Hz",
            "pause": 0.25,
        },
    ]

    files = []
    timing = []

    current_time = 0.0

    for index, section in enumerate(sections):

        spoken = section["text"]

        if category.startswith("indian_"):
            spoken = pronunciation(
                spoken
            )

        output = (
            TEMP_DIR /
            f"{index:02d}_{section['name']}.mp3"
        )

        print(
            "Generating:",
            section["name"],
            "|",
            section["rate"]
        )

        await speak(
            spoken,
            voice,
            section["rate"],
            section["pitch"],
            output
        )

        length = duration(
            output
        )

        timing.append({
            "name": section["name"],
            "text": section["text"],
            "start": round(
                current_time,
                3
            ),
            "end": round(
                current_time + length,
                3
            ),
            "duration": round(
                length,
                3
            )
        })

        files.append(
            output
        )

        current_time += length

        pause = section["pause"]

        if pause:

            pause_file = (
                TEMP_DIR /
                f"{index:02d}_pause.mp3"
            )

            make_pause(
                pause_file,
                pause
            )

            files.append(
                pause_file
            )

            current_time += pause

    concat_file = (
        TEMP_DIR /
        "concat.txt"
    )

    with open(
        concat_file,
        "w",
        encoding="utf-8"
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
            str(OUTPUT_AUDIO)
        ],
        check=True
    )

    if not OUTPUT_AUDIO.exists():
        raise RuntimeError(
            "voice.mp3 was not created"
        )

    TIMING_FILE.write_text(
        json.dumps(
            timing,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    final_length = duration(
        OUTPUT_AUDIO
    )

    print("")
    print("==============================")
    print("FAST NARRATION CREATED")
    print("==============================")
    print("Voice:", voice)
    print(
        "Duration:",
        round(final_length, 2),
        "seconds"
    )
    print("==============================")


if __name__ == "__main__":
    asyncio.run(main())
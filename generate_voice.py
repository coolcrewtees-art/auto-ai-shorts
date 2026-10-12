import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro


# ============================================================
# FILES
# ============================================================

STORY_FILE = Path("story.json")

MODEL_FILE = Path("kokoro-v1.0.onnx")
VOICES_FILE = Path("voices-v1.0.bin")

TEMP_DIR = Path("voice_parts")
TEMP_DIR.mkdir(exist_ok=True)

OUTPUT_WAV = Path("voice.wav")
OUTPUT_MP3 = Path("voice.mp3")
TIMING_FILE = Path("voice_timing.json")


# ============================================================
# VOICE
# ============================================================

VOICE = "bm_george"
LANG = "en-gb"


# ============================================================
# PRONUNCIATION FIXES
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
    "Hanuman": "Hanoomaan",
    "Mahabharata": "Mahaa bhaarata",
    "Ramayana": "Raamaayana",
    "Uttarayana": "Uttaraayana",
}


def fix_pronunciation(text):
    for original, replacement in PRONUNCIATIONS.items():
        text = re.sub(
            rf"\b{re.escape(original)}\b",
            replacement,
            text,
            flags=re.IGNORECASE,
        )

    return text


# ============================================================
# HELPERS
# ============================================================

def make_silence(seconds, sample_rate):
    samples = int(seconds * sample_rate)

    return np.zeros(
        samples,
        dtype=np.float32
    )


def audio_duration(audio, sample_rate):
    return len(audio) / sample_rate


def save_mp3():
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(OUTPUT_WAV),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(OUTPUT_MP3),
        ],
        check=True,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Starting Kokoro narration...")

    # --------------------------------------------------------
    # VERIFY FILES
    # --------------------------------------------------------

    if not STORY_FILE.exists():
        raise FileNotFoundError(
            "story.json is missing"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "kokoro-v1.0.onnx is missing"
        )

    if not VOICES_FILE.exists():
        raise FileNotFoundError(
            "voices-v1.0.bin is missing"
        )

    # --------------------------------------------------------
    # LOAD STORY
    # --------------------------------------------------------

    with open(
        STORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        story = json.load(f)

    # --------------------------------------------------------
    # LOAD KOKORO
    # --------------------------------------------------------

    print("Loading Kokoro model...")

    tts = Kokoro(
        str(MODEL_FILE),
        str(VOICES_FILE)
    )

    # --------------------------------------------------------
    # PERFORMANCE SETTINGS
    #
    # Faster middle.
    # Slower hook/reveal/final.
    # --------------------------------------------------------

    sections = [

        {
            "name": "title_hook",
            "text": story["title_hook"],
            "speed": 1.03,
            "pause": 0.42,
        },

        {
            "name": "opening",
            "text": story["opening"],
            "speed": 1.14,
            "pause": 0.08,
        },

        {
            "name": "conflict",
            "text": story["conflict"],
            "speed": 1.17,
            "pause": 0.07,
        },

        {
            "name": "escalation",
            "text": story["escalation"],
            "speed": 1.20,
            "pause": 0.07,
        },

        {
            "name": "dramatic_reveal",
            "text": story["dramatic_reveal"],
            "speed": 1.08,
            "pause": 0.32,
        },

        {
            "name": "final_punch",
            "text": story["final_punch"],
            "speed": 1.04,
            "pause": 0.25,
        },
    ]

    all_audio = []
    timings = []

    current_time = 0.0
    sample_rate = None

    # --------------------------------------------------------
    # GENERATE EACH SECTION
    # --------------------------------------------------------

    for index, section in enumerate(sections):

        spoken_text = fix_pronunciation(
            section["text"]
        )

        print("")
        print(
            "Generating:",
            section["name"],
            "| speed:",
            section["speed"]
        )

        audio, sr = tts.create(
            spoken_text,
            voice=VOICE,
            speed=section["speed"],
            lang=LANG,
        )

        if sample_rate is None:
            sample_rate = sr

        if sr != sample_rate:
            raise RuntimeError(
                "Kokoro returned inconsistent sample rates"
            )

        audio = np.asarray(
            audio,
            dtype=np.float32
        )

        if len(audio) == 0:
            raise RuntimeError(
                f"No audio generated for {section['name']}"
            )

        # Save debug section
        section_file = (
            TEMP_DIR
            / f"{index:02d}_{section['name']}.wav"
        )

        sf.write(
            section_file,
            audio,
            sample_rate,
            subtype="PCM_16"
        )

        duration = audio_duration(
            audio,
            sample_rate
        )

        start = current_time
        end = start + duration

        timings.append(
            {
                "name": section["name"],
                "text": section["text"],
                "start": round(start, 3),
                "end": round(end, 3),
                "duration": round(duration, 3),
            }
        )

        all_audio.append(
            audio
        )

        current_time = end

        # ----------------------------------------------------
        # ADD PAUSE
        # ----------------------------------------------------

        pause = section["pause"]

        if pause > 0:

            silence = make_silence(
                pause,
                sample_rate
            )

            all_audio.append(
                silence
            )

            current_time += pause

    # --------------------------------------------------------
    # JOIN ALL AUDIO
    # --------------------------------------------------------

    if not all_audio:
        raise RuntimeError(
            "No narration audio was generated"
        )

    final_audio = np.concatenate(
        all_audio
    )

    # --------------------------------------------------------
    # NORMALIZE SAFELY
    # --------------------------------------------------------

    peak = np.max(
        np.abs(final_audio)
    )

    if peak > 0:
        final_audio = (
            final_audio
            / peak
            * 0.92
        )

    # --------------------------------------------------------
    # SAVE WAV
    # --------------------------------------------------------

    sf.write(
        OUTPUT_WAV,
        final_audio,
        sample_rate,
        subtype="PCM_16"
    )

    if not OUTPUT_WAV.exists():
        raise RuntimeError(
            "voice.wav was not created"
        )

    # --------------------------------------------------------
    # CONVERT TO MP3
    # --------------------------------------------------------

    save_mp3()

    if not OUTPUT_MP3.exists():
        raise RuntimeError(
            "voice.mp3 was not created"
        )

    if OUTPUT_MP3.stat().st_size < 5000:
        raise RuntimeError(
            "voice.mp3 is suspiciously small"
        )

    # --------------------------------------------------------
    # SAVE TIMINGS
    # --------------------------------------------------------

    TIMING_FILE.write_text(
        json.dumps(
            timings,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    if not TIMING_FILE.exists():
        raise RuntimeError(
            "voice_timing.json was not created"
        )

    final_duration = (
        len(final_audio)
        / sample_rate
    )

    # --------------------------------------------------------
    # LOG
    # --------------------------------------------------------

    print("")
    print(
        "===================================="
    )

    print(
        "KOKORO NARRATION CREATED"
    )

    print(
        "===================================="
    )

    print(
        "Voice:",
        VOICE
    )

    print(
        "Language:",
        LANG
    )

    print(
        "Sample rate:",
        sample_rate
    )

    print(
        "Duration:",
        round(
            final_duration,
            2
        ),
        "seconds"
    )

    print(
        "Output:",
        OUTPUT_MP3
    )

    print(
        "Timing:",
        TIMING_FILE
    )

    print(
        "===================================="
    )


if __name__ == "__main__":
    main()
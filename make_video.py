import json
import re
import subprocess
from pathlib import Path

FPS = 30
WIDTH = 1080
HEIGHT = 1920

IMAGE_DIR = Path("images")
TEMP_DIR = Path("temp_clips")

AUDIO_FILE = "voice.mp3"
OUTPUT_FILE = "final_short.mp4"
CAPTION_FILE = "captions.ass"

TEMP_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def run(cmd):
    print("Running:")
    print(" ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def get_duration(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filename
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())


def ass_time(seconds):
    if seconds < 0:
        seconds = 0

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60

    return f"{hours}:{minutes:02d}:{secs:05.2f}"


# ============================================================
# LOAD STORY
# ============================================================

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

screenplay = story["screenplay"]

audio_duration = get_duration(AUDIO_FILE)

print(f"Narration duration: {audio_duration:.2f}s")


# ============================================================
# FIND IMAGES
# ============================================================

images = sorted(IMAGE_DIR.glob("scene_*.jpg"))

if not images:
    raise RuntimeError("No generated images found.")

print(f"Images found: {len(images)}")


# ============================================================
# VIDEO TIMINGS
#
# Presenter = only first 2.5 seconds.
# Remaining time goes to story visuals.
# ============================================================

PRESENTER_DURATION = min(2.5, audio_duration * 0.12)

if len(images) > 1:
    remaining_duration = audio_duration - PRESENTER_DURATION
    story_scene_duration = remaining_duration / (len(images) - 1)
else:
    PRESENTER_DURATION = audio_duration
    story_scene_duration = audio_duration

print(f"Presenter duration: {PRESENTER_DURATION:.2f}s")
print(f"Story image duration: {story_scene_duration:.2f}s")


# ============================================================
# CREATE MOVING IMAGE CLIPS
# ============================================================

clips = []

for index, image in enumerate(images):

    scene_number = index
    output_clip = TEMP_DIR / f"clip_{scene_number:02d}.mp4"

    if index == 0:
        duration = PRESENTER_DURATION
    else:
        duration = story_scene_duration

    # Alternate movements so every shot isn't identical.
    if index % 3 == 0:
        zoom = "min(max(zoom,pzoom)+0.00045,1.08)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"

    elif index % 3 == 1:
        zoom = "min(max(zoom,pzoom)+0.00060,1.10)"
        x = "(iw-iw/zoom)*0.35"
        y = "ih/2-(ih/zoom/2)"

    else:
        zoom = "min(max(zoom,pzoom)+0.00055,1.09)"
        x = "(iw-iw/zoom)*0.65"
        y = "ih/2-(ih/zoom/2)"

    vf = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},"
        f"zoompan="
        f"z='{zoom}':"
        f"x='{x}':"
        f"y='{y}':"
        f"d=1:"
        f"s={WIDTH}x{HEIGHT}:"
        f"fps={FPS},"
        f"format=yuv420p"
    )

    run([
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-framerate", str(FPS),
        "-i", str(image),
        "-t", str(duration),
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        str(output_clip)
    ])

    clips.append(output_clip)


# ============================================================
# CONCAT VISUALS
# ============================================================

concat_file = TEMP_DIR / "clips.txt"

with open(concat_file, "w", encoding="utf-8") as f:
    for clip in clips:
        f.write(f"file '{clip.resolve()}'\n")

visual_video = TEMP_DIR / "visuals.mp4"

run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(visual_video)
])


# ============================================================
# CAPTION GENERATOR
# ============================================================

def create_caption_chunks(text, max_words=5):

    # Clean spaces.
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()

    chunks = []
    current = []

    for word in words:

        current.append(word)

        # Prefer breaking at punctuation.
        punctuation_break = (
            len(current) >= 2
            and word.endswith((".", "!", "?", ",", ";", ":"))
        )

        size_break = len(current) >= max_words

        if punctuation_break or size_break:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


caption_chunks = create_caption_chunks(
    screenplay,
    max_words=5
)

total_caption_words = sum(
    len(chunk.split())
    for chunk in caption_chunks
)

if total_caption_words == 0:
    raise RuntimeError("No caption words generated.")


# ============================================================
# CREATE ASS SUBTITLE FILE
# ============================================================

ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Caption,DejaVu Sans,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,1,2,80,80,245,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

current_time = 0.0

caption_lines = []

for i, chunk in enumerate(caption_chunks):

    word_count = len(chunk.split())

    duration = (
        audio_duration
        * word_count
        / total_caption_words
    )

    # Don't make captions flash too quickly.
    duration = max(duration, 0.55)

    start = current_time
    end = min(
        start + duration,
        audio_duration
    )

    safe_chunk = (
        chunk
        .replace("\\", r"\\")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )

    caption_lines.append(
        "Dialogue: 0,"
        f"{ass_time(start)},"
        f"{ass_time(end)},"
        "Caption,,0,0,0,,"
        f"{safe_chunk}"
    )

    current_time = end


with open(CAPTION_FILE, "w", encoding="utf-8") as f:
    f.write(ass_header)

    for line in caption_lines:
        f.write(line + "\n")

print(f"Generated {len(caption_lines)} caption chunks.")


# ============================================================
# BURN CAPTIONS + ADD AUDIO
# ============================================================

run([
    "ffmpeg",
    "-y",

    "-i", str(visual_video),
    "-i", AUDIO_FILE,

    "-filter:v",
    f"ass={CAPTION_FILE}",

    "-map", "0:v:0",
    "-map", "1:a:0",

    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",

    "-c:a", "aac",
    "-b:a", "192k",

    "-shortest",
    "-movflags", "+faststart",

    OUTPUT_FILE
])


# ============================================================
# VERIFY
# ============================================================

final_duration = get_duration(OUTPUT_FILE)

print("")
print("====================================")
print("SHORT CREATED SUCCESSFULLY")
print(f"File: {OUTPUT_FILE}")
print(f"Duration: {final_duration:.2f}s")
print(f"Images: {len(images)}")
print(f"Captions: {len(caption_lines)}")
print("====================================")
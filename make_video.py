import json
import subprocess
from pathlib import Path

FPS = 30
WIDTH = 1080
HEIGHT = 1920

IMAGE_DIR = Path("images")
TEMP_DIR = Path("temp_clips")
OUTPUT_FILE = "final_short.mp4"
AUDIO_FILE = "voice.mp3"

TEMP_DIR.mkdir(exist_ok=True)


def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


# --------------------------------------------------
# Get narration duration
# --------------------------------------------------

result = subprocess.run(
    [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        AUDIO_FILE,
    ],
    capture_output=True,
    text=True,
    check=True,
)

audio_duration = float(result.stdout.strip())

print(f"Narration duration: {audio_duration:.2f} seconds")


# --------------------------------------------------
# Find all scene images
# --------------------------------------------------

images = sorted(IMAGE_DIR.glob("scene_*.jpg"))

if not images:
    raise RuntimeError("No scene images found.")

print(f"Images found: {len(images)}")


# Give every image equal screen time
scene_duration = audio_duration / len(images)

print(f"Each image duration: {scene_duration:.2f} seconds")


# --------------------------------------------------
# Turn each image into a moving video clip
# --------------------------------------------------

clips = []

for index, image in enumerate(images, start=1):

    output_clip = TEMP_DIR / f"clip_{index:02d}.mp4"

    # Alternate slight zoom direction/style
    if index % 2 == 0:
        zoom = "min(max(zoom,pzoom)+0.0007,1.10)"
    else:
        zoom = "min(max(zoom,pzoom)+0.0005,1.08)"

    vf = (
        f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},"
        f"zoompan="
        f"z='{zoom}':"
        f"x='iw/2-(iw/zoom/2)':"
        f"y='ih/2-(ih/zoom/2)':"
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
        "-t", str(scene_duration),
        "-vf", vf,
        "-an",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        str(output_clip),
    ])

    clips.append(output_clip)


# --------------------------------------------------
# Create FFmpeg concat list
# --------------------------------------------------

concat_file = TEMP_DIR / "clips.txt"

with open(concat_file, "w", encoding="utf-8") as f:
    for clip in clips:
        f.write(f"file '{clip.resolve()}'\n")


# --------------------------------------------------
# Join all visual clips
# --------------------------------------------------

visual_video = TEMP_DIR / "visuals.mp4"

run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(visual_video),
])


# --------------------------------------------------
# Add narration
# --------------------------------------------------

run([
    "ffmpeg",
    "-y",
    "-i", str(visual_video),
    "-i", AUDIO_FILE,
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    OUTPUT_FILE,
])


print("")
print("====================================")
print("✅ SHORT CREATED SUCCESSFULLY")
print(f"🎬 {OUTPUT_FILE}")
print(f"⏱ Duration: {audio_duration:.2f}s")
print(f"🖼 Images: {len(images)}")
print("====================================")
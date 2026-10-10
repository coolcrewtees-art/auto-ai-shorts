import json
import math
import re
import subprocess
from pathlib import Path


FPS = 30
WIDTH = 1080
HEIGHT = 1920

IMAGE_DIR = Path("images")
TEMP_DIR = Path("temp_video")

TEMP_DIR.mkdir(exist_ok=True)

AUDIO_FILE = "voice.mp3"
TIMING_FILE = "voice_timing.json"

FINAL_FILE = "final_short.mp4"
CAPTION_FILE = "captions.ass"


# ============================================================
# HELPERS
# ============================================================

def run(cmd):
    print(" ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def ass_time(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    secs = seconds % 60

    return f"{hours}:{minutes:02d}:{secs:05.2f}"


# ============================================================
# LOAD DATA
# ============================================================

with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

with open("scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

with open(TIMING_FILE, "r", encoding="utf-8") as f:
    timings = json.load(f)


images = sorted(
    IMAGE_DIR.glob("scene_*.jpg")
)

if len(images) != len(scenes):
    raise RuntimeError(
        f"{len(images)} images but "
        f"{len(scenes)} scenes."
    )


# ============================================================
# CREATE SOUND EFFECTS
# ============================================================

impact_sound = TEMP_DIR / "impact.wav"
whoosh_sound = TEMP_DIR / "whoosh.wav"
soft_hit_sound = TEMP_DIR / "soft_hit.wav"


# Deep reveal impact
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "sine=frequency=70:duration=0.32",
    "-filter:a",
    "volume=0.35,afade=t=out:st=0.05:d=0.27",
    str(impact_sound)
])


# Transition whoosh
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "anoisesrc=color=white:duration=0.22",
    "-filter:a",
    "highpass=f=450,lowpass=f=5000,"
    "volume=0.06,"
    "afade=t=in:st=0:d=0.05,"
    "afade=t=out:st=0.09:d=0.13",
    str(whoosh_sound)
])


# Small hook hit
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "sine=frequency=120:duration=0.18",
    "-filter:a",
    "volume=0.18,afade=t=out:st=0.02:d=0.16",
    str(soft_hit_sound)
])


# ============================================================
# CREATE VIDEO CLIPS
# ============================================================

clips = []

for i, scene in enumerate(scenes):

    image = images[i]

    timing = timings[i]

    # Include pause before next line naturally.
    if i < len(timings) - 1:
        duration = (
            timings[i + 1]["start"]
            - timing["start"]
        )
    else:
        duration = (
            timing["duration"] + 0.7
        )

    output = TEMP_DIR / f"clip_{i:02d}.mp4"

    beat = scene["beat"]

    # --------------------------------------------------------
    # TITLE HOOK
    # Quick punch-in
    # --------------------------------------------------------

    if beat == "title_hook":

        vf = (
            f"scale=1180:2100,"
            f"crop={WIDTH}:{HEIGHT}:"
            f"x='(iw-{WIDTH})/2':"
            f"y='(ih-{HEIGHT})/2',"
            f"zoompan="
            f"z='min(1.0+0.0017*on,1.15)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d=1:"
            f"s={WIDTH}x{HEIGHT}:"
            f"fps={FPS},"
            f"fade=t=in:st=0:d=0.18,"
            f"format=yuv420p"
        )

    # --------------------------------------------------------
    # OPENING
    # Gentle cinematic movement
    # --------------------------------------------------------

    elif beat == "opening":

        vf = (
            f"scale=1180:2100,"
            f"crop={WIDTH}:{HEIGHT}:"
            f"x='40+15*sin(t*0.7)':"
            f"y='90',"
            f"format=yuv420p"
        )

    # --------------------------------------------------------
    # CONFLICT
    # Faster creeping zoom
    # --------------------------------------------------------

    elif beat == "conflict":

        vf = (
            f"scale={WIDTH}:{HEIGHT}:"
            f"force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan="
            f"z='min(max(zoom,pzoom)+0.0010,1.12)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d=1:"
            f"s={WIDTH}x{HEIGHT}:"
            f"fps={FPS},"
            f"format=yuv420p"
        )

    # --------------------------------------------------------
    # ESCALATION
    # More aggressive movement
    # --------------------------------------------------------

    elif beat == "escalation":

        vf = (
            f"scale=1200:2140,"
            f"crop={WIDTH}:{HEIGHT}:"
            f"x='60+18*sin(t*2.3)':"
            f"y='110+10*cos(t*1.8)',"
            f"format=yuv420p"
        )

    # --------------------------------------------------------
    # DRAMATIC REVEAL
    # Flash + punch + micro-shake
    # --------------------------------------------------------

    elif beat == "dramatic_reveal":

        vf = (
            f"scale=1220:2170,"
            f"crop={WIDTH}:{HEIGHT}:"
            f"x='70+8*sin(t*35)':"
            f"y='125+8*cos(t*31)',"
            f"eq="
            f"brightness='if(lt(t,0.10),0.35,"
            f"if(lt(t,0.22),0.10,0))':"
            f"eval=frame,"
            f"format=yuv420p"
        )

    # --------------------------------------------------------
    # FINAL PUNCH
    # Slow dark cinematic hold
    # --------------------------------------------------------

    else:

        vf = (
            f"scale={WIDTH}:{HEIGHT}:"
            f"force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan="
            f"z='min(max(zoom,pzoom)+0.00045,1.07)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d=1:"
            f"s={WIDTH}x{HEIGHT}:"
            f"fps={FPS},"
            f"vignette=PI/5,"
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
        "-crf", "19",
        str(output)
    ])

    clips.append(output)


# ============================================================
# CONCAT VIDEO
# ============================================================

concat_file = TEMP_DIR / "clips.txt"

with open(concat_file, "w", encoding="utf-8") as f:

    for clip in clips:
        f.write(
            f"file '{clip.resolve()}'\n"
        )


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
# CAPTIONS
# ============================================================

ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Normal,DejaVu Sans,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,-1,0,0,0,100,100,0,0,1,5,1,2,75,75,250,1
Style: Hook,DejaVu Sans,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,-1,0,0,0,100,100,0,0,1,6,2,5,85,85,0,1
Style: Reveal,DejaVu Sans,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,-1,0,0,0,100,100,0,0,1,6,2,2,70,70,260,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


caption_lines = []


def chunk_text(text, max_words=4):

    words = text.split()

    chunks = []

    current = []

    for word in words:

        current.append(word)

        punctuation = word.endswith(
            (",", ".", "!", "?", ":", ";")
        )

        if len(current) >= max_words or (
            punctuation and len(current) >= 2
        ):

            chunks.append(
                " ".join(current)
            )

            current = []

    if current:
        chunks.append(
            " ".join(current)
        )

    return chunks


for item in timings:

    chunks = chunk_text(
        item["text"],
        max_words=4
    )

    total_words = sum(
        len(c.split())
        for c in chunks
    )

    current = item["start"]

    for chunk in chunks:

        words = len(chunk.split())

        fraction = words / total_words

        chunk_duration = (
            item["duration"]
            * fraction
        )

        chunk_duration = max(
            chunk_duration,
            0.42
        )

        start = current
        end = min(
            start + chunk_duration,
            item["end"]
        )

        style = "Normal"

        if item["name"] == "title_hook":
            style = "Hook"

        elif item["name"] in [
            "dramatic_reveal",
            "final_punch"
        ]:
            style = "Reveal"

        safe = (
            chunk
            .replace("\\", r"\\")
            .replace("{", r"\{")
            .replace("}", r"\}")
        )

        caption_lines.append(
            f"Dialogue: 0,"
            f"{ass_time(start)},"
            f"{ass_time(end)},"
            f"{style},,0,0,0,,"
            f"{safe}"
        )

        current = end


with open(
    CAPTION_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(ass_header)

    for line in caption_lines:
        f.write(line + "\n")


# ============================================================
# EFFECT TIMESTAMPS
# ============================================================

hook_time = timings[0]["start"]

reveal_time = next(
    item["start"]
    for item in timings
    if item["name"] == "dramatic_reveal"
)

ending_time = next(
    item["start"]
    for item in timings
    if item["name"] == "final_punch"
)


hook_delay = int(
    hook_time * 1000
)

reveal_delay = int(
    reveal_time * 1000
)

ending_delay = int(
    ending_time * 1000
)


# ============================================================
# FINAL AUDIO + VIDEO MIX
# ============================================================

filter_complex = (
    f"[1:a]volume=1.0[voice];"
    f"[2:a]adelay={hook_delay}|{hook_delay},"
    f"volume=0.7[hook];"
    f"[3:a]adelay={reveal_delay}|{reveal_delay},"
    f"volume=1.0[impact];"
    f"[4:a]adelay={ending_delay}|{ending_delay},"
    f"volume=0.55[ending];"
    f"[voice][hook][impact][ending]"
    f"amix=inputs=4:"
    f"duration=longest:"
    f"normalize=0[aout]"
)


run([
    "ffmpeg",
    "-y",

    "-i", str(visual_video),
    "-i", AUDIO_FILE,
    "-i", str(soft_hit_sound),
    "-i", str(impact_sound),
    "-i", str(whoosh_sound),

    "-filter_complex",
    filter_complex,

    "-filter:v",
    f"ass={CAPTION_FILE}",

    "-map", "0:v:0",
    "-map", "[aout]",

    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",

    "-c:a", "aac",
    "-b:a", "192k",

    "-shortest",
    "-movflags", "+faststart",

    FINAL_FILE
])


print("")
print("===================================")
print("FINAL SHORT CREATED")
print("===================================")
print("Voice expression: YES")
print("Captions: YES")
print("Hook effect: YES")
print("Reveal flash/shake: YES")
print("Impact SFX: YES")
print("Final vignette: YES")
print("Output:", FINAL_FILE)
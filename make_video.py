import json
import math
import subprocess
from pathlib import Path


# ============================================================
# BASIC SETTINGS
# ============================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30

IMAGE_DIR = Path("images")
TEMP_DIR = Path("temp_video")
TEMP_DIR.mkdir(exist_ok=True)

VOICE_FILE = Path("voice.mp3")
TIMING_FILE = Path("voice_timing.json")

OUTPUT_FILE = Path("final_short.mp4")
CAPTION_FILE = Path("captions.ass")


# ============================================================
# HELPERS
# ============================================================

def run(command):
    print("")
    print(" ".join(str(x) for x in command))
    subprocess.run(
        command,
        check=True,
    )


def ass_time(seconds):

    seconds = max(
        0,
        seconds,
    )

    hours = int(
        seconds // 3600
    )

    minutes = int(
        (seconds % 3600) // 60
    )

    secs = (
        seconds % 60
    )

    return (
        f"{hours}:"
        f"{minutes:02d}:"
        f"{secs:05.2f}"
    )


# ============================================================
# LOAD STORY DATA
# ============================================================

with open(
    "story.json",
    "r",
    encoding="utf-8",
) as f:
    story = json.load(f)


with open(
    "scenes.json",
    "r",
    encoding="utf-8",
) as f:
    scenes = json.load(f)


with open(
    TIMING_FILE,
    "r",
    encoding="utf-8",
) as f:
    timings = json.load(f)


images = sorted(
    IMAGE_DIR.glob(
        "scene_*.jpg"
    )
)


if len(images) != len(scenes):
    raise RuntimeError(
        f"Expected {len(scenes)} images "
        f"but found {len(images)}"
    )


if len(timings) != len(scenes):
    raise RuntimeError(
        f"Expected {len(scenes)} timing sections "
        f"but found {len(timings)}"
    )


# ============================================================
# CREATE SIMPLE SOUND EFFECTS
# ============================================================

hook_hit = (
    TEMP_DIR / "hook_hit.wav"
)

reveal_hit = (
    TEMP_DIR / "reveal_hit.wav"
)

whoosh = (
    TEMP_DIR / "whoosh.wav"
)


# Hook thump
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i",
    "sine=frequency=95:duration=0.20",
    "-filter:a",
    (
        "volume=0.22,"
        "afade=t=out:st=0.03:d=0.17"
    ),
    str(hook_hit),
])


# Reveal bass impact
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i",
    "sine=frequency=55:duration=0.38",
    "-filter:a",
    (
        "volume=0.36,"
        "afade=t=out:st=0.06:d=0.32"
    ),
    str(reveal_hit),
])


# Small whoosh
run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i",
    "anoisesrc=color=white:duration=0.18",
    "-filter:a",
    (
        "highpass=f=700,"
        "lowpass=f=5500,"
        "volume=0.035,"
        "afade=t=in:st=0:d=0.04,"
        "afade=t=out:st=0.06:d=0.12"
    ),
    str(whoosh),
])


# ============================================================
# MICRO-CUT GENERATION
#
# One generated image can create several visual cuts.
# ============================================================

micro_clips = []

clip_counter = 0


for index, scene in enumerate(scenes):

    image = images[index]
    timing = timings[index]

    start_time = timing["start"]

    if index < len(timings) - 1:
        end_time = timings[index + 1]["start"]
    else:
        end_time = (
            timing["end"] + 0.25
        )

    scene_duration = max(
        end_time - start_time,
        0.8,
    )

    # commas / punctuation allow extra motion cuts
    punctuation_points = int(
        scene.get(
            "comma_motion_points",
            0,
        )
    )

    # Normally 2 cuts per image,
    # 3 for longer/more punctuated lines.
    if (
        scene_duration >= 4.0
        or punctuation_points >= 2
    ):
        cut_count = 3
    else:
        cut_count = 2

    # Title/reveal are deliberately faster.
    if scene["beat"] in [
        "title_hook",
        "dramatic_reveal",
    ]:
        cut_count = max(
            cut_count,
            2,
        )

    cut_duration = (
        scene_duration
        / cut_count
    )

    for sub_index in range(
        cut_count
    ):

        output = (
            TEMP_DIR
            / f"micro_{clip_counter:03d}.mp4"
        )

        # ------------------------------------
        # DIFFERENT FRAMING FOR EACH CUT
        # ------------------------------------

        mode = (
            clip_counter % 5
        )

        if mode == 0:

            movement = (
                "zoompan="
                "z='min(1+0.0015*on,1.14)':"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )

        elif mode == 1:

            movement = (
                "zoompan="
                "z='1.10':"
                "x='(iw-iw/zoom)*0.20':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )

        elif mode == 2:

            movement = (
                "zoompan="
                "z='1.13':"
                "x='(iw-iw/zoom)*0.80':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )

        elif mode == 3:

            movement = (
                "zoompan="
                "z='min(1.12-0.0008*on,1.12)':"
                "x='iw/2-(iw/zoom/2)':"
                "y='(ih-ih/zoom)*0.28':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )

        else:

            movement = (
                "zoompan="
                "z='1.08':"
                "x='iw/2-(iw/zoom/2)':"
                "y='(ih-ih/zoom)*0.70':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        # ------------------------------------
        # BEAT-SPECIFIC EFFECTS
        # ------------------------------------

        extra_effect = ""

        if scene["beat"] == "title_hook":

            extra_effect = (
                ",fade=t=in:"
                "st=0:d=0.10"
            )

        elif (
            scene["beat"]
            == "dramatic_reveal"
            and sub_index == 0
        ):

            extra_effect = (
                ",eq="
                "brightness="
                "'if(lt(t,0.08),0.32,"
                "if(lt(t,0.16),0.10,0))':"
                "eval=frame"
            )

        elif (
            scene["beat"]
            == "final_punch"
        ):

            extra_effect = (
                ",vignette=PI/5"
            )


        vf = (
            f"scale={WIDTH}:{HEIGHT}:"
            "force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"{movement}"
            f"{extra_effect},"
            "setsar=1,"
            "format=yuv420p"
        )


        run([
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-framerate",
            str(FPS),
            "-i",
            str(image),
            "-t",
            str(cut_duration),
            "-vf",
            vf,
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            "-pix_fmt",
            "yuv420p",
            str(output),
        ])


        micro_clips.append(
            output
        )

        clip_counter += 1


# ============================================================
# CONCAT ALL MICRO CUTS
# ============================================================

concat_file = (
    TEMP_DIR / "micro_concat.txt"
)


with open(
    concat_file,
    "w",
    encoding="utf-8",
) as f:

    for clip in micro_clips:

        f.write(
            f"file '{clip.resolve()}'\n"
        )


visual_video = (
    TEMP_DIR / "visuals.mp4"
)


run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i",
    str(concat_file),
    "-c:v",
    "libx264",
    "-preset",
    "veryfast",
    "-crf",
    "19",
    "-vf",
    "setsar=1",
    "-pix_fmt",
    "yuv420p",
    "-an",
    str(visual_video),
])


# ============================================================
# CAPTION FILE
# ============================================================

ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Normal,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,5,1,2,85,85,245,1
Style: Hook,DejaVu Sans,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,5,80,80,0,1
Style: Reveal,DejaVu Sans,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,80,80,250,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


def chunks(text):

    words = text.split()

    result = []
    current = []

    for word in words:

        current.append(
            word
        )

        punctuation = (
            word.endswith(
                (
                    ",",
                    ".",
                    "?",
                    "!",
                    "…",
                    ":",
                    ";",
                )
            )
        )

        if (
            len(current) >= 3
            or (
                punctuation
                and len(current) >= 2
            )
        ):

            result.append(
                " ".join(current)
            )

            current = []

    if current:

        result.append(
            " ".join(current)
        )

    return result


caption_lines = []


for item in timings:

    text_chunks = chunks(
        item["text"]
    )

    total_words = sum(
        len(x.split())
        for x in text_chunks
    )

    current = item["start"]

    for chunk in text_chunks:

        word_count = len(
            chunk.split()
        )

        duration = (
            item["duration"]
            * (
                word_count
                / total_words
            )
        )

        duration = max(
            duration,
            0.32,
        )

        start = current

        end = min(
            start + duration,
            item["end"],
        )

        style = "Normal"

        if (
            item["name"]
            == "title_hook"
        ):
            style = "Hook"

        elif (
            item["name"]
            in [
                "dramatic_reveal",
                "final_punch",
            ]
        ):
            style = "Reveal"


        safe = (
            chunk
            .replace(
                "\\",
                r"\\",
            )
            .replace(
                "{",
                r"\{",
            )
            .replace(
                "}",
                r"\}",
            )
        )


        caption_lines.append(
            "Dialogue: 0,"
            f"{ass_time(start)},"
            f"{ass_time(end)},"
            f"{style},,"
            "0,0,0,,"
            f"{safe}"
        )

        current = end


with open(
    CAPTION_FILE,
    "w",
    encoding="utf-8",
) as f:

    f.write(
        ass_header
    )

    for line in caption_lines:

        f.write(
            line + "\n"
        )


# ============================================================
# EFFECT TIMESTAMPS
# ============================================================

hook_time = (
    timings[0]["start"]
)


reveal_time = next(
    x["start"]
    for x in timings
    if x["name"]
    == "dramatic_reveal"
)


final_time = next(
    x["start"]
    for x in timings
    if x["name"]
    == "final_punch"
)


hook_delay = int(
    hook_time * 1000
)

reveal_delay = int(
    reveal_time * 1000
)

final_delay = int(
    final_time * 1000
)


# ============================================================
# AUDIO MIX
# ============================================================

audio_filter = (
    f"[1:a]volume=1.0[voice];"

    f"[2:a]"
    f"adelay={hook_delay}|{hook_delay},"
    f"volume=0.70[hook];"

    f"[3:a]"
    f"adelay={reveal_delay}|{reveal_delay},"
    f"volume=0.95[reveal];"

    f"[4:a]"
    f"adelay={final_delay}|{final_delay},"
    f"volume=0.45[finalfx];"

    "[voice][hook][reveal][finalfx]"
    "amix="
    "inputs=4:"
    "duration=longest:"
    "normalize=0[aout]"
)


# ============================================================
# FINAL VIDEO
# ============================================================

run([
    "ffmpeg",
    "-y",

    "-i",
    str(visual_video),

    "-i",
    str(VOICE_FILE),

    "-i",
    str(hook_hit),

    "-i",
    str(reveal_hit),

    "-i",
    str(whoosh),

    "-filter_complex",
    audio_filter,

    "-vf",
    (
        f"ass={CAPTION_FILE},"
        "setsar=1"
    ),

    "-map",
    "0:v:0",

    "-map",
    "[aout]",

    "-c:v",
    "libx264",

    "-preset",
    "veryfast",

    "-crf",
    "18",

    "-pix_fmt",
    "yuv420p",

    "-aspect",
    "9:16",

    "-c:a",
    "aac",

    "-b:a",
    "192k",

    "-movflags",
    "+faststart",

    "-shortest",

    str(OUTPUT_FILE),
])


print("")
print("================================")
print("FINAL SHORT CREATED")
print("================================")
print(
    "Resolution:",
    WIDTH,
    "x",
    HEIGHT,
)
print("Aspect ratio: 9:16")
print("SAR: 1:1")
print(
    "Visual cuts:",
    len(micro_clips),
)
print(
    "Captions:",
    len(caption_lines),
)
print(
    "Output:",
    OUTPUT_FILE,
)
print("================================")
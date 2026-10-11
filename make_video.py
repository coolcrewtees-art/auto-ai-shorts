import json
import subprocess
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

WIDTH = 1080
HEIGHT = 1920
FPS = 30

IMAGE_DIR = Path("images")
TEMP_DIR = Path("temp_video")

VOICE_FILE = Path("voice.mp3")
TIMING_FILE = Path("voice_timing.json")

SCENES_FILE = Path("scenes.json")

OUTPUT_FILE = Path("final_short.mp4")
CAPTION_FILE = Path("captions.ass")

TEMP_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def run(command):

    print("")
    print(
        " ".join(
            str(part)
            for part in command
        )
    )

    subprocess.run(
        command,
        check=True
    )


def ass_time(seconds):

    seconds = max(
        0,
        float(seconds)
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


def word_count(text):

    return max(
        1,
        len(
            text.split()
        )
    )


# ============================================================
# VERIFY REQUIRED FILES
# ============================================================

for required in [
    VOICE_FILE,
    TIMING_FILE,
    SCENES_FILE,
]:

    if not required.exists():

        raise FileNotFoundError(
            f"Missing required file: {required}"
        )


# ============================================================
# LOAD FILES
# ============================================================

with open(
    SCENES_FILE,
    "r",
    encoding="utf-8"
) as f:

    scenes = json.load(f)


with open(
    TIMING_FILE,
    "r",
    encoding="utf-8"
) as f:

    timings = json.load(f)


images = sorted(
    IMAGE_DIR.glob(
        "scene_*.jpg"
    )
)


# ============================================================
# VALIDATION
# ============================================================

if len(scenes) != 8:

    raise RuntimeError(
        f"Expected 8 scenes but got {len(scenes)}"
    )


if len(images) != len(scenes):

    raise RuntimeError(
        f"Expected {len(scenes)} images "
        f"but found {len(images)}"
    )


timing_by_name = {

    item["name"]: item
    for item in timings
}


required_timing_names = [

    "title_hook",
    "opening",
    "conflict",
    "escalation",
    "dramatic_reveal",
    "final_punch",

]


for name in required_timing_names:

    if name not in timing_by_name:

        raise RuntimeError(
            f"Missing narration timing: {name}"
        )


# ============================================================
# CALCULATE EXACT VISUAL TIME FOR EACH OF 8 SCENES
#
# Example:
#
# opening narration = one audio section
#
# but:
# opening_1 gets one image
# opening_2 gets another image
#
# We divide the opening timing between them based
# on how many words each visual scene contains.
# ============================================================

scene_timings = []


for timing_name in required_timing_names:

    timing = timing_by_name[
        timing_name
    ]

    related_scene_indexes = [

        index
        for index, scene
        in enumerate(scenes)

        if scene.get(
            "timing_section"
        ) == timing_name
    ]


    if not related_scene_indexes:

        continue


    total_words = sum(

        word_count(
            scenes[index][
                "narration"
            ]
        )

        for index
        in related_scene_indexes
    )


    cursor = float(
        timing["start"]
    )


    timing_end = float(
        timing["end"]
    )


    timing_duration = (
        timing_end
        - cursor
    )


    for position, scene_index in enumerate(
        related_scene_indexes
    ):

        scene_words = word_count(
            scenes[scene_index][
                "narration"
            ]
        )


        # Last scene gets remaining duration,
        # avoiding accumulated rounding errors.
        if (
            position
            == len(related_scene_indexes) - 1
        ):

            scene_end = timing_end

        else:

            fraction = (
                scene_words
                / total_words
            )

            scene_duration = (
                timing_duration
                * fraction
            )

            scene_end = (
                cursor
                + scene_duration
            )


        scene_timings.append({

            "scene_index":
                scene_index,

            "start":
                cursor,

            "end":
                scene_end,

            "duration":
                max(
                    0.35,
                    scene_end - cursor
                ),

        })


        cursor = scene_end


# Put back into actual scene order.
scene_timings.sort(
    key=lambda item:
    item["scene_index"]
)


# ============================================================
# LOG SCENE TIMING
# ============================================================

print("")
print(
    "===================================="
)

print(
    "VISUAL SCENE TIMINGS"
)

print(
    "===================================="
)


for item in scene_timings:

    scene = scenes[
        item["scene_index"]
    ]

    print(
        f"Scene {item['scene_index'] + 1}:",
        scene["beat"],
        "|",
        round(
            item["duration"],
            2
        ),
        "sec"
    )


# ============================================================
# CREATE SOUND EFFECTS
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


# ------------------------------------------------------------
# HOOK THUMP
# ------------------------------------------------------------

run([

    "ffmpeg",
    "-y",

    "-f",
    "lavfi",

    "-i",
    "sine=frequency=90:duration=0.22",

    "-filter:a",
    (
        "volume=0.22,"
        "afade=t=out:"
        "st=0.04:"
        "d=0.18"
    ),

    str(hook_hit),

])


# ------------------------------------------------------------
# REVEAL IMPACT
# ------------------------------------------------------------

run([

    "ffmpeg",
    "-y",

    "-f",
    "lavfi",

    "-i",
    "sine=frequency=52:duration=0.42",

    "-filter:a",
    (
        "volume=0.38,"
        "afade=t=out:"
        "st=0.06:"
        "d=0.36"
    ),

    str(reveal_hit),

])


# ------------------------------------------------------------
# WHOOSH
# ------------------------------------------------------------

run([

    "ffmpeg",
    "-y",

    "-f",
    "lavfi",

    "-i",
    "anoisesrc=color=white:duration=0.22",

    "-filter:a",
    (
        "highpass=f=850,"
        "lowpass=f=5000,"
        "volume=0.035,"
        "afade=t=in:"
        "st=0:"
        "d=0.05,"
        "afade=t=out:"
        "st=0.08:"
        "d=0.14"
    ),

    str(whoosh),

])


# ============================================================
# MICRO-CUT CREATION
#
# 8 generated images
# become roughly 18-24 visual cuts.
# ============================================================

micro_clips = []

clip_number = 0


for timing_info in scene_timings:

    scene_index = timing_info[
        "scene_index"
    ]

    scene = scenes[
        scene_index
    ]

    image = images[
        scene_index
    ]

    scene_duration = float(
        timing_info[
            "duration"
        ]
    )


    motion_points = int(
        scene.get(
            "comma_motion_points",
            0
        )
    )


    # --------------------------------------------------------
    # HOW MANY CUTS?
    # --------------------------------------------------------

    if scene_duration >= 8:

        cut_count = 4

    elif scene_duration >= 5:

        cut_count = 3

    else:

        cut_count = 2


    # More punctuation means more possible motion.
    if (
        motion_points >= 5
        and scene_duration >= 5
    ):

        cut_count = max(
            cut_count,
            3
        )


    # Major beats should feel more active.
    if scene.get(
        "importance"
    ) == "major":

        cut_count = max(
            cut_count,
            2
        )


    cut_duration = (
        scene_duration
        / cut_count
    )


    # --------------------------------------------------------
    # CREATE CUTS FROM SAME IMAGE
    # --------------------------------------------------------

    for cut_index in range(
        cut_count
    ):

        output = (
            TEMP_DIR
            / f"micro_{clip_number:03d}.mp4"
        )


        movement_mode = (
            clip_number % 6
        )


        # ====================================================
        # CAMERA MOVEMENT
        # ====================================================

        if movement_mode == 0:

            movement = (
                "zoompan="
                "z='min(1+0.0018*on,1.16)':"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        elif movement_mode == 1:

            movement = (
                "zoompan="
                "z='1.13':"
                "x='(iw-iw/zoom)*0.15':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        elif movement_mode == 2:

            movement = (
                "zoompan="
                "z='1.13':"
                "x='(iw-iw/zoom)*0.85':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        elif movement_mode == 3:

            movement = (
                "zoompan="
                "z='1.12':"
                "x='iw/2-(iw/zoom/2)':"
                "y='(ih-ih/zoom)*0.18':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        elif movement_mode == 4:

            movement = (
                "zoompan="
                "z='1.11':"
                "x='iw/2-(iw/zoom/2)':"
                "y='(ih-ih/zoom)*0.82':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        else:

            movement = (
                "zoompan="
                "z='min(1.15-0.0007*on,1.15)':"
                "x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':"
                "d=1:"
                f"s={WIDTH}x{HEIGHT}:"
                f"fps={FPS}"
            )


        # ====================================================
        # BEAT-SPECIFIC VIDEO EFFECTS
        # ====================================================

        extra = ""


        # Hook appears sharply.
        if (
            scene["beat"]
            == "title_hook"
            and cut_index == 0
        ):

            extra = (
                ",fade=t=in:"
                "st=0:"
                "d=0.08"
            )


        # Reveal gets flash.
        elif (
            scene["beat"]
            == "dramatic_reveal"
            and cut_index == 0
        ):

            extra = (
                ",fade="
                "t=in:"
                "st=0:"
                "d=0.05:"
                "color=white"
            )


        # Final punch gets slight vignette.
        elif (
            scene["beat"]
            == "final_punch"
        ):

            extra = (
                ",vignette=PI/5"
            )


        # ====================================================
        # FULL VIDEO FILTER
        #
        # setsar=1 fixes previous squeezed video bug.
        # ====================================================

        vf = (

            f"scale="
            f"{WIDTH}:"
            f"{HEIGHT}:"
            "force_original_aspect_ratio=increase,"

            f"crop="
            f"{WIDTH}:"
            f"{HEIGHT},"

            f"{movement}"

            f"{extra},"

            "setsar=1,"

            "format=yuv420p"

        )


        run([

            "ffmpeg",
            "-y",

            "-loop",
            "1",

            "-framerate",
            str(FPS),

            "-i",
            str(image),

            "-t",
            f"{cut_duration:.3f}",

            "-vf",
            vf,

            "-an",

            "-c:v",
            "libx264",

            "-preset",
            "veryfast",

            "-crf",
            "18",

            "-pix_fmt",
            "yuv420p",

            str(output),

        ])


        micro_clips.append(
            output
        )

        clip_number += 1


# ============================================================
# CONCAT VISUALS
# ============================================================

concat_file = (
    TEMP_DIR
    / "visual_concat.txt"
)


with open(
    concat_file,
    "w",
    encoding="utf-8"
) as f:

    for clip in micro_clips:

        f.write(
            f"file '{clip.resolve()}'\n"
        )


visual_video = (
    TEMP_DIR
    / "visuals.mp4"
)


run([

    "ffmpeg",
    "-y",

    "-f",
    "concat",

    "-safe",
    "0",

    "-i",
    str(concat_file),

    "-c:v",
    "libx264",

    "-preset",
    "veryfast",

    "-crf",
    "18",

    "-vf",
    "setsar=1",

    "-pix_fmt",
    "yuv420p",

    "-an",

    str(visual_video),

])


# ============================================================
# CAPTIONS
# ============================================================

ASS_HEADER = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Normal,DejaVu Sans,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H6E000000,-1,0,0,0,100,100,0,0,1,5,1,2,80,80,255,1
Style: Hook,DejaVu Sans,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H76000000,-1,0,0,0,100,100,0,0,1,6,2,5,75,75,0,1
Style: Reveal,DejaVu Sans,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H76000000,-1,0,0,0,100,100,0,0,1,6,2,2,75,75,255,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""


def caption_chunks(text):

    words = text.split()

    chunks = []
    current = []


    for word in words:

        current.append(
            word
        )


        punctuation = word.endswith(
            (
                ".",
                ",",
                "?",
                "!",
                ":",
                ";",
                "…",
            )
        )


        # Short captions feel faster and more Reel-like.
        if (
            len(current) >= 3
            or (
                punctuation
                and len(current) >= 2
            )
        ):

            chunks.append(
                " ".join(
                    current
                )
            )

            current = []


    if current:

        chunks.append(
            " ".join(
                current
            )
        )


    return chunks


caption_lines = []


for timing in timings:

    chunks = caption_chunks(
        timing["text"]
    )


    if not chunks:
        continue


    total_words = sum(

        word_count(chunk)

        for chunk in chunks
    )


    cursor = float(
        timing["start"]
    )


    end_limit = float(
        timing["end"]
    )


    for chunk_index, chunk in enumerate(
        chunks
    ):

        chunk_words = word_count(
            chunk
        )


        if (
            chunk_index
            == len(chunks) - 1
        ):

            chunk_end = (
                end_limit
            )

        else:

            fraction = (
                chunk_words
                / total_words
            )

            estimated = (
                float(
                    timing[
                        "duration"
                    ]
                )
                * fraction
            )

            estimated = max(
                0.30,
                estimated
            )

            chunk_end = min(
                cursor
                + estimated,
                end_limit
            )


        style = "Normal"


        if (
            timing["name"]
            == "title_hook"
        ):

            style = "Hook"


        elif timing["name"] in [

            "dramatic_reveal",
            "final_punch",

        ]:

            style = "Reveal"


        safe_text = (
            chunk
            .replace(
                "\\",
                r"\\"
            )
            .replace(
                "{",
                r"\{"
            )
            .replace(
                "}",
                r"\}"
            )
        )


        caption_lines.append(

            "Dialogue: 0,"
            f"{ass_time(cursor)},"
            f"{ass_time(chunk_end)},"
            f"{style},,"
            "0,0,0,,"
            f"{safe_text}"

        )


        cursor = chunk_end


with open(
    CAPTION_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        ASS_HEADER
    )

    for line in caption_lines:

        f.write(
            line
            + "\n"
        )


# ============================================================
# EFFECT TIMESTAMPS
# ============================================================

hook_time = float(
    timing_by_name[
        "title_hook"
    ][
        "start"
    ]
)


reveal_time = float(
    timing_by_name[
        "dramatic_reveal"
    ][
        "start"
    ]
)


final_time = float(
    timing_by_name[
        "final_punch"
    ][
        "start"
    ]
)


hook_delay = int(
    hook_time
    * 1000
)


reveal_delay = int(
    reveal_time
    * 1000
)


final_delay = int(
    final_time
    * 1000
)


# ============================================================
# AUDIO MIX
# ============================================================

audio_filter = (

    "[1:a]"
    "volume=1.0"
    "[voice];"

    "[2:a]"
    f"adelay={hook_delay}|{hook_delay},"
    "volume=0.65"
    "[hook];"

    "[3:a]"
    f"adelay={reveal_delay}|{reveal_delay},"
    "volume=0.90"
    "[reveal];"

    "[4:a]"
    f"adelay={final_delay}|{final_delay},"
    "volume=0.40"
    "[ending];"

    "[voice]"
    "[hook]"
    "[reveal]"
    "[ending]"

    "amix="
    "inputs=4:"
    "duration=longest:"
    "normalize=0"

    "[aout]"

)


# ============================================================
# FINAL RENDER
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

    # Explicit Shorts/Reels display ratio
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


# ============================================================
# VERIFY FINAL VIDEO
# ============================================================

if not OUTPUT_FILE.exists():

    raise RuntimeError(
        "final_short.mp4 was not created"
    )


# ==================================================
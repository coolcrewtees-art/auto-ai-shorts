import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

SCENES_FILE = "scenes.json"
OUTPUT_DIR = Path("images")

OUTPUT_DIR.mkdir(exist_ok=True)

with open(SCENES_FILE, "r", encoding="utf-8") as f:
    scenes = json.load(f)

def download_image(url, output_path):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        data = response.read()

    with open(output_path, "wb") as f:
        f.write(data)

for scene in scenes:
    number = scene["scene"]
    prompt = scene["prompt"]

    filename = OUTPUT_DIR / f"scene_{number:02d}.jpg"

    encoded_prompt = urllib.parse.quote(prompt)

    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width=576"
        f"&height=1024"
        f"&model=flux"
        f"&nologo=true"
        f"&seed={1000 + number}"
    )

    print(f"Generating scene {number}...")

    success = False

    for attempt in range(3):
        try:
            download_image(url, filename)

            if filename.exists() and filename.stat().st_size > 10000:
                print(f"Scene {number} saved: {filename}")
                success = True
                break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(10)

    if not success:
        raise RuntimeError(f"Could not generate scene {number}")

    # Be polite to the free service
    time.sleep(6)

print("All images generated successfully!")
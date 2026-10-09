import base64
import json
import os
import time
from pathlib import Path

import requests

ACCOUNT_ID = os.environ["CLOUDFLARE_ACCOUNT_ID"]
API_TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]

MODEL = "@cf/black-forest-labs/flux-1-schnell"

API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL}"
)

OUTPUT_DIR = Path("images")
OUTPUT_DIR.mkdir(exist_ok=True)

with open("scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def generate_image(prompt, scene_number):
    payload = {
        "prompt": prompt[:2048],
        "steps": 4
    }

    for attempt in range(1, 4):
        print(f"Generating scene {scene_number} — attempt {attempt}/3")

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=180,
            )

            if response.status_code != 200:
                print(
                    f"Cloudflare error {response.status_code}: "
                    f"{response.text[:500]}"
                )

                if attempt < 3:
                    time.sleep(10 * attempt)
                    continue

                raise RuntimeError(
                    f"Cloudflare failed for scene {scene_number}"
                )

            data = response.json()

            if not data.get("success"):
                raise RuntimeError(
                    f"Cloudflare returned failure: {data}"
                )

            result = data.get("result", {})
            image_b64 = result.get("image")

            if not image_b64:
                raise RuntimeError(
                    f"No image returned for scene {scene_number}"
                )

            image_bytes = base64.b64decode(image_b64)

            output_path = OUTPUT_DIR / f"scene_{scene_number:02d}.jpg"

            with open(output_path, "wb") as f:
                f.write(image_bytes)

            if output_path.stat().st_size < 5000:
                raise RuntimeError(
                    f"Generated image is suspiciously small: "
                    f"{output_path.stat().st_size} bytes"
                )

            print(f"✅ Scene {scene_number} saved → {output_path}")
            return

        except Exception as e:
            print(f"Scene {scene_number} attempt {attempt} failed: {e}")

            if attempt == 3:
                raise

            time.sleep(10 * attempt)

for scene in scenes:
    scene_number = int(scene["scene"])
    prompt = scene["prompt"]

    generate_image(prompt, scene_number)

    time.sleep(2)

print(f"✅ Successfully generated {len(scenes)} images.")
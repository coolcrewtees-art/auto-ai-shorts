import asyncio
import json
import edge_tts

VOICE = "en-US-AndrewMultilingualNeural"

async def main():
    with open("story.json", "r", encoding="utf-8") as f:
        story = json.load(f)

    text = story["screenplay"]

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-4%",
        pitch="-2Hz",
        volume="+0%"
    )

    await communicate.save("voice.mp3")

    print("Narration generated successfully.")

asyncio.run(main())
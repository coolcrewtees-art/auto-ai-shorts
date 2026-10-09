import asyncio
import json
import edge_tts

VOICE = "en-US-AdamMultilingualNeural"

async def main():
    with open("story.json", "r", encoding="utf-8") as f:
        story = json.load(f)

    text = story["screenplay"]

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-5%",
        pitch="-2Hz",
        volume="+0%"
    )

    await communicate.save("voice.mp3")

    print("Voice generated successfully: voice.mp3")

asyncio.run(main())
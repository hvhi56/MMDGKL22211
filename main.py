import asyncio
from telethon import TelegramClient, events
from keep_alive import keep_alive
import os
from dotenv import load_dotenv

# טען משתנים מקובץ .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

source_channel = -1001778387051  # בלי @
target_channel = -1002255057047   # בלי @

# התחברות עם session של המשתמש
client = TelegramClient("user_session", api_id, api_hash)

# התחברות עם בוט לשליחה
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=source_channel))
async def forward(event):
    try:
        message = event.message

        # אם יש מדיה (תמונה, וידאו, קובץ וכו')
        if message.media:
            await bot.send_file(
                target_channel,
                file=message.media,
                caption=message.text or "",  # טקסט אם יש
                force_document=False
            )
        else:
            # אם זה טקסט בלבד
            if message.text:
                await bot.send_message(target_channel, message.text)

    except Exception as e:
        print("❌ שגיאה בשליחה:", e)

async def start_clients():
    await client.start()
    print("✅ User session connected.")
    await bot.start()
    print("🤖 Bot connected.")
    print("📡 Bot is running...")

    keep_alive()  # שמירה על החיבור חי
    await client.run_until_disconnected()

# ניהול לולאת האירועים – בצורה ידנית (avoiding asyncio.run)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_clients())

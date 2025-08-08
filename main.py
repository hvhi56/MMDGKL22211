import asyncio
import os
from telethon import TelegramClient, events
from keep_alive import keep_alive
from dotenv import load_dotenv

# טוען משתנים מקובץ .env
load_dotenv()

# פרטי ההתחברות ל-Telegram
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# שמות ערוצים - בלי @
source_channel = "Moshepargod"
target_channel = "forfkf46ig"

# יצירת לקוחות Telethon
client = TelegramClient("user_session", api_id, api_hash)
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# מאזין להודעות בערוץ המקור
@client.on(events.NewMessage(chats=source_channel))
async def forward(event):
    try:
        await bot.send_message(target_channel, event.message)
        print("הודעה הועברה")
    except Exception as e:
        print(f"שגיאה בהעברה: {e}")

async def main():
    await client.start()
    print("User session connected.")

    await bot.start()
    print("Bot session connected.")

    # הפעלת שרת Flask קטן כדי לשמור על Render חי
    keep_alive()

    print("Bot is running and waiting for messages...")
    await client.run_until_disconnected()

# הרצת הלולאה הראשית
asyncio.run(main())

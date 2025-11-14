import asyncio
from telethon import TelegramClient, events
from keep_alive import keep_alive
import os
import time
from dotenv import load_dotenv

# טען משתנים מקובץ .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

source_channel = -1001778387051  # בלי @
target_channel = -1002255057047  # בלי @

# התחברות עם session של המשתמש
client = TelegramClient("my_session", api_id, api_hash)

# התחברות עם בוט (עדיין נתחבר אליו לשימור הטריק, אבל לא נשתמש בו לשליחה)
bot = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=source_channel))
async def forward(event):
    print(f"📥 התקבלה הודעה מהערוץ המקור: {event.id}")
    try:
        message = event.message

        # אם יש מדיה (תמונה, וידאו, קובץ וכו')
        if message.media:
            print("📸 שולח מדיה לערוץ היעד...")
            await client.send_file(
                target_channel,
                file=message.media,
                caption=message.text or "",
                force_document=False
            )
        else:
            # אם זה טקסט בלבד
            if message.text:
                print("💬 שולח טקסט לערוץ היעד...")
                await client.send_message(target_channel, message.text)

        print("✅ ההודעה נשלחה בהצלחה!")

    except Exception as e:
        print("❌ שגיאה בשליחה:", e)

async def start_clients():
    while True:
        try:
            await client.start()
            print("✅ User session connected.")
            await bot.start()  # נשאר בשביל הטריק
            print("🤖 Bot connected.")
            print("📡 Bot is running...")

            keep_alive()  # שמירה על החיבור חי
            await client.run_until_disconnected()

            print("⚠️ החיבור נותק — מנסה להתחבר מחדש בעוד 5 שניות...")
            await asyncio.sleep(5)

        except Exception as e:
            print("❌ שגיאה בחיבור:", e)
            await asyncio.sleep(5)

# ניהול לולאת האירועים – בצורה ידנית
loop = asyncio.get_event_loop()

while True:
    try:
        loop.run_until_complete(start_clients())
    except Exception as e:
        print("❌ שגיאה כללית בלולאה הראשית:", e)
        time.sleep(5)  # לחכות 5 שניות לפני ניסיון נוסף


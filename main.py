import asyncio
import os
import signal
from telethon import TelegramClient, events
from dotenv import load_dotenv
from keep_alive import keep_alive

# טעינת משתני סביבה
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

source_channel = -1001778387051
target_channel = -1002255057047

# חשוב מאוד: שימוש בתיקיית TMP של Render כדי למנוע שחיתת session
client = TelegramClient("/tmp/user_session", api_id, api_hash)
bot = TelegramClient("/tmp/bot_session", api_id, api_hash).start(bot_token=bot_token)

# -----------------------------------------------------------------------------------
# אירוע העברת הודעות מהערוץ המקור לערוץ יעד
# -----------------------------------------------------------------------------------

@client.on(events.NewMessage(chats=source_channel))
async def forward(event):
    print(f"📥 התקבלה הודעה מהערוץ המקור: {event.id}")

    try:
        message = event.message

        # שליחת מדיה
        if message.media:
            print("📸 שולח מדיה לערוץ היעד...")
            await client.send_file(
                target_channel,
                file=message.media,
                caption=message.text or "",
                force_document=False
            )

        # שליחת טקסט בלבד
        else:
            if message.text:
                print("💬 שולח טקסט לערוץ היעד...")
                await client.send_message(target_channel, message.text)

        print("✅ ההודעה נשלחה בהצלחה!")

    except Exception as e:
        print("❌ שגיאה בשליחה:", e)

# -----------------------------------------------------------------------------------
# פונקציית הריצה הראשית – ללא לולאות! Render יבצע restart לבד
# -----------------------------------------------------------------------------------

async def main():
    print("🚀 מתחבר לטלגרם...")
    await client.start()
    print("👤 User session connected.")

    await bot.start()
    print("🤖 Bot session connected.")

    # מפעיל שרת keep-alive עבור UptimeRobot
    keep_alive()

    print("📡 המערכת פועלת. ממתין להודעות...")
    await client.run_until_disconnected()

# -----------------------------------------------------------------------------------
# טיפול ב-SIGTERM כדי למנוע קריסת session כש-Render הורג את השרת
# -----------------------------------------------------------------------------------

def shutdown_handler(*args):
    print("⚠️ Render שלח SIGTERM — סוגר יפה...")
    try:
        loop.stop()
    except:
        pass

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

# -----------------------------------------------------------------------------------
# הפעלת הלולאה הראשית בצורה תקינה (אסור while True)
# -----------------------------------------------------------------------------------

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

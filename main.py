import asyncio
from telethon import TelegramClient, events
from keep_alive import keep_alive

# --- הגדרות הבוט והערוצים ---
api_id = 25863606
api_hash = '34f981178528c8167680f1429bb526c6'
bot_token = '8000668793:AAE428DuqA1E21e8nDmakzguoNX40hJvXR4'

source_channel = 'Moshepargod'  # בלי @
target_channel = 'forfkf46ig'   # בלי @

# --- התחברות ל-Telegram עם בוט ---
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# --- האירוע שמאזין להודעות חדשות ---
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    await client.send_message(target_channel, event.message)

# --- מפעיל שרת Flask קטן כדי לשמור על התהליך פעיל (לרמות את Render)
keep_alive()

# --- הרצת הלקוח של Telethon לנצח ---
print("Bot is running...")
client.run_until_disconnected()

from telethon import TelegramClient, events
import asyncio
import os
import socket

# הפרטים שלך
api_id = 25863606
api_hash = '34f981178528c8167680f1429bb526c6'
bot_token = '8000668793:AAE428DuqA1E21e8nDmakzguoNX40hJvXR4'

# הקישורים לערוצים
source_channel = 'https://t.me/Moshepargod'
target_channel = 'https://t.me/forfkf46ig'

# יצירת לקוח טלגרם
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# העברת הודעות אוטומטית
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    await client.forward_messages(target_channel, event.message)

print("Bot is running...")

# הטריק – פתיחת פורט פיקטיבי כדי ש-Render לא יתלונן
async def keep_alive():
    port = int(os.environ.get("PORT", 8080))  # ברירת מחדל 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        print(f"Listening on port {port} to keep Render happy...")
        while True:
            conn, addr = s.accept()
            conn.close()

async def main():
    await asyncio.gather(
        keep_alive(),
        client.run_until_disconnected()
    )

asyncio.run(main())

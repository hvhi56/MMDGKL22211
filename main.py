from telethon import TelegramClient, events

# הפרטים שלך
api_id = 25863606
api_hash = '34f981178528c8167680f1429bb526c6'
bot_token = '8000668793:AAE428DuqA1E21e8nDmakzguoNX40hJvXR4'

# הקישורים לערוצים
source_channel = 'https://t.me/Moshepargod'      # ערוץ ציבורי שלא בבעלותך
target_channel = 'https://t.me/forfkf46ig'        # ערוץ בבעלותך

# יצירת לקוח טלגרם
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# כאשר מתקבלת הודעה חדשה בערוץ המקור – תשלח לערוץ היעד
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    await client.forward_messages(target_channel, event.message)

print("Bot is running...")  # הודעה שEverything works
client.run_until_disconnected()

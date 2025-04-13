# from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# BOT_TOKEN = "7739287666:AAGJrWFW3TGE1aNScxfzfRaHwR_QSxdTyTY"

# async def get_chat_id(update, context):
#     chat_id = update.effective_chat.id
#     print("Your chat ID is:", chat_id)
#     await update.message.reply_text("✅ Bot is ready!")

# app = ApplicationBuilder().token(BOT_TOKEN).build()
# app.add_handler(MessageHandler(filters.TEXT, get_chat_id))
# app.run_polling()

import requests

BOT_TOKEN = "7739287666:AAGJrWFW3TGE1aNScxfzfRaHwR_QSxdTyTY"
CHAT_ID = '7567367075'

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=payload)
    return response.status_code

from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

async def handle_message(update, context):
    text = update.message.text
    print(f"You said: {text}")
    
    # Example: route based on message content
    if "email" in text.lower():
        await update.message.reply_text("📬 Checking your email...")
        # Trigger your AI assistant's email logic here
    elif "task" in text.lower():
        await update.message.reply_text("📝 Adding task to Google Tasks...")
        # Trigger task logic
    else:
        await update.message.reply_text("🤖 Command received! (but not sure what to do yet)")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
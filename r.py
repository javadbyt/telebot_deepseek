import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

# تنظیمات
TELEGRAM_TOKEN = '7461713881:AAHBsr13LnQMAyZxkNlzDHeQboXw9m1Imms'
DEEPSEEK_API_KEY = 'sk-21360ba9b3664009ad873590b039d7bb'
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        
        # ارسال درخواست به DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": user_message}]
        }
        
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()
        
        # استخراج پاسخ
        ai_response = response_data['choices'][0]['message']['content']
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("warning in process")

if __name__ == "__main__":
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # شروع ربات با حالت پولینگ
    application.run_polling()

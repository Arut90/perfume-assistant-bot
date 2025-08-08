import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Загрузка токена из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я — твой ассистент по выбору парфюма 💐")

# Обработчик всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    # Пример простой логики
    if "сладкий" in text:
        reply = "Рекомендую: Viktor & Rolf Bonbon 🍬"
    elif "свежий" in text:
        reply = "Рекомендую: Dior Homme Cologne 🌊"
    else:
        reply = "Можешь описать, какой аромат тебе нравится? Например: свежий, древесный, восточный..."
    await update.message.reply_text(reply)

# Главная функция
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

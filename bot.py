import os
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Загружаем токен из переменных окружения (или можно напрямую прописать для теста)
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_ОТСЮДА")

# Загружаем базу ароматов
with open("perfumes.json", "r", encoding="utf-8") as f:
    perfumes = json.load(f)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу подобрать аромат 💐\nНапиши, какой запах тебе нравится (например: свежий, сладкий, древесный).")

# Поиск ароматов
def find_perfumes(query):
    query = query.lower()
    results = []
    for perfume in perfumes:
        if any(note in query for note in perfume["notes"]) or perfume["category"] in query:
            results.append(perfume)
    return results[:3]  # максимум 3 результата

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    results = find_perfumes(text)
    if results:
        for perfume in results:
            caption = f"{perfume['name']} ({perfume['brand']})\nНоты: {', '.join(perfume['notes'])}\nСезон: {perfume['season']} | Пол: {perfume['gender']}"
            await update.message.reply_photo(photo=perfume["image"], caption=caption)
    else:
        await update.message.reply_text("Не нашёл подходящий аромат 🙈 Попробуй другие слова: свежий, сладкий, древесный, восточный...")

# Главная функция
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from tgbot.config import BOT_TOKEN
from Constants import PHONE_NUMBER

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Предопределённые ответы на часто задаваемые вопросы (временно вместо БД)
faq_answers = {
    "где находится паркинг": "Паркинги расположены рядом с терминалами D, E и F. Следуйте указателям.",
    "цены на парковку": "Стоимость зависит от типа парковки. Краткосрочная — от 200 руб/час, долгосрочная — от 600 руб/сутки.",
    "как оплатить парковку": "Оплата доступна через терминалы на парковке, а также через приложение или сайт аэропорта.",
    "работает ли парковка ночью": "Да, парковка работает круглосуточно."
}


# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Извините, я пока не знаю ответа на этот вопрос. Попробуйте переформулировать или позвоните по номеру поддержки: {PHONE_NUMBER}"
    )


# Обработчик сообщений (вопросов)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Здесь позже будет подключение к БД 
    # answer = get_answer_from_db(user_message)

    # Пока что используем заранее заданные ответы
    response = None
    for question, answer in faq_answers.items():
        if question in user_message:
            response = answer
            break

    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(
            f"Извините, я пока не знаю ответа на этот вопрос. Попробуйте переформулировать или позвоните по номеру поддержки: {PHONE_NUMBER}")


# Основная функция
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()

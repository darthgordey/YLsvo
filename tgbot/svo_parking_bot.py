import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from tgbot.config import BOT_TOKEN
from Constants import *

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Обработчик команд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я ваш помощник по парковке. Чем могу помочь?",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Если не знаете, с чего начать — просто напишите вопрос или нажмите кнопку.\nТелефон поддержки: {PHONE_NUMBER}"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Ответы на часто задаваемые вопросы
    if user_message in faq_answers:
        await update.message.reply_text(faq_answers[user_message])
        return

    # Обработка подменю
    if user_message in submenus:
        reply_markup = ReplyKeyboardMarkup(submenus[user_message], resize_keyboard=True)
        await update.message.reply_text(f"Выберите действие: {user_message}", reply_markup=reply_markup)
        return

    # Действия для кнопок подменю
    if user_message == "🚀 Забронировать онлайн":
        await update.message.reply_text(f"Перейдите по ссылке для бронирования: {BOOKING_URL}")
        return
    if user_message == "💰 Оплатить онлайн":
        await update.message.reply_text(f"Перейдите по ссылке для оплаты: {PAYMENT_URL}")
        return
    if user_message == "🔍 Поиск авто":
        await update.message.reply_text(f"Перейдите для поиска автомобиля: {FIND_CAR_URL}")
        return
    if user_message == "📞 Позвонить оператору":
        await update.message.reply_text(f"Позвоните оператору по номеру: {PHONE_NUMBER}")
        return
    if user_message == "✉️ Онлайн-чат":
        # Отправка сообщения оператору (например, через CRM или службу поддержки)
        await update.message.reply_text("Сообщение отправлено в онлайн-чат оператора.")
        return
    if user_message == "✉️ Подать жалобу":
        # Перенаправление жалобы в CRM или отдел качества
        await update.message.reply_text("Ваша жалоба передана в отдел качества.")
        return
    if user_message == "💰 Запросить возврат":
        # Перенаправление запроса на возврат средств
        await update.message.reply_text("Запрос на возврат средств отправлен.")
        return
    if user_message == "ℹ️ Условия бронирования":
        await update.message.reply_text(f"Условия бронирования можно узнать на сайте: {BOOKING_URL}")
        return
    if user_message == "💳 Способы оплаты":
        await update.message.reply_text(f"Оплата возможна через сайт: {PAYMENT_URL}")
        return

    # Назад в главное меню
    if user_message == "🔙 Назад":
        reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=reply_markup)
        return

    await update.message.reply_text("Извините, я пока не знаю ответа на этот вопрос.")


# Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()

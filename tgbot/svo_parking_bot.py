import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from tgbot.config import BOT_TOKEN
from Constants import PHONE_NUMBER

# Логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# FAQ: Автоматические ответы
faq_answers = {
    "🅿️ тарифы и стоимость": "Вот актуальные тарифы:\n— Терминал B: 800 ₽/час, 1800 ₽/сутки\n— P18: 1000 ₽/сутки\n— P12: 400 ₽/сутки",
    "📅 бронирование": "Чтобы забронировать парковку, укажите даты и площадку. Я пришлю ссылку.",
    "💳 оплата": "Оплатить можно онлайн или на месте. Хотите ссылку на оплату?",
    "🎟 льготы": "Уточните вашу категорию (многодетные, ЛОВЗ, сотрудники) — я подскажу, как оформить.",
    "🔍 найти авто / помощь": "Укажите парковку и госномер — я передам запрос в техслужбу. 🔧",
    "📩 жалобы и возврат": "Опишите суть обращения. Прикрепите фото, если нужно. Я передам в отдел качества.",
    "🗺 интерактивная схема": "Напишите терминал, и я пришлю схему.",
    "🚗 выбор парковки": "Уточните терминал, длительность стоянки и предпочтения. Я подберу подходящий вариант.",
    "👨‍💼 связаться с оператором": f"Запрос передан оператору. Также вы можете позвонить: {PHONE_NUMBER}",
    "работает ли парковка ночью": "Да, все парковки работают круглосуточно."
}

# Сценарии, требующие оператора по файлу маршрутизации
requires_operator = [
    "жалоба", "возврат", "ошибка оплаты", "не работает", "поддержка", "оператор", "не нашёл машину",
    "проблема", "не открывается", "сел аккумулятор"
]


# TODO: Заглушки под интеграции из файла "Матрица интеграций_MVP"
def send_to_crm(user_id, message_text):
    logger.info(f"[CRM] Отправлен запрос от {user_id}: {message_text}")
    # Здесь будет интеграция с CRM


def forward_to_support(user_id, message_text):
    logger.info(f"[Техподдержка] Заявка от {user_id}: {message_text}")
    # Здесь будет интеграция с техслужбой


def forward_to_operator(user_id, message_text):
    logger.info(f"[Оператор] Перенаправлено сообщение от {user_id}: {message_text}")
    # Здесь будет отправка в чат с оператором или CRM
    send_to_crm(user_id, message_text)


# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🅿️ Тарифы и стоимость", "📅 Бронирование"],
        ["💳 Оплата", "🎟 Льготы"],
        ["🔍 Найти авто / помощь", "📩 Жалобы и возврат"],
        ["🗺 Интерактивная схема", "🚗 Выбор парковки"],
        ["👨‍💼 Связаться с оператором"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Здравствуйте! Я ваш помощник по парковке. Чем могу помочь?",
        reply_markup=reply_markup
    )


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Если не знаете, с чего начать — просто напишите вопрос или нажмите кнопку.\nТелефон поддержки: {PHONE_NUMBER}"
    )


# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_id = update.message.from_user.id

    # Поиск ответа из базы знаний
    for question, answer in faq_answers.items():
        if question.lower() in user_message:
            await update.message.reply_text(answer)
            return

    # Маршрутизация по ключевым словам
    if any(keyword in user_message for keyword in requires_operator):
        forward_to_operator(user_id, user_message)
        await update.message.reply_text(
            "Ваш запрос передан оператору. Ожидайте ответа или позвоните по номеру поддержки."
        )
        return

    # Если нет совпадений — стандартный ответ
    await update.message.reply_text(
        f"Извините, я пока не знаю ответа на этот вопрос. Попробуйте переформулировать или позвоните: {PHONE_NUMBER}"
    )


# Запуск бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()
  
import logging
import telegram
import asyncio
from telegram import Message, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
) #импортированные библиотеки

import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7682952936:AAGjkGlBk45iskGZouGk_ofW53e4DNrRsO0"  # ТГ ID бота
ADMIN_ID = 5642938812  # ТГ ID админа

messages_queue = {}
user_email_requests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("❗️Частые вопросы"),
         KeyboardButton("💬Связь с администрацией"),
         KeyboardButton("🔑Восстановить пароль")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите один из вариантов:", reply_markup=reply_markup)

async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("🛡FAQ"), KeyboardButton("🛡Авторы")],
        [KeyboardButton("🔙Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.message.from_user.id, text="Пожалуйста, выберите вопрос:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        if update.message.text == "❗️Частые вопросы":
            await show_questions(update, context)
        elif update.message.text == "💬Связь с администрацией":
            await context.bot.send_message(chat_id=user_id, text="Напишите ваше сообщение администратору через бота\n❗️смотрите в личные сообщения, администратор напишет туда\nили нажмите '🔙Назад' для возврата:", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
        elif update.message.text == "🔑Восстановить пароль":
            user_email_requests[user_id] = True  # Устанавливаем флаг для ожидания почты
            await context.bot.send_message(chat_id=user_id, text="Пожалуйста, введите вашу почту:")
        elif update.message.text in user_email_requests and user_email_requests[user_id]:
            email = update.message.text
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"Запрос на восстановление пароля от @{update.message.from_user.username}. Почта: {email}")
            await context.bot.send_message(chat_id=user_id, text="Ваш запрос на восстановление пароля отправлен администратору.")
            del user_email_requests[user_id]  # Удаляем флаг после обработки
        elif update.message.text == "🛡FAQ":
            await context.bot.send_message(chat_id=user_id, text="1.Не открывается какая-либо вкладка сайта?\n✅Вы можете нажать кнопку '💬Связь с администрацией' и описать всю проблему,\n2.Как зарегестрироватьсяn✅Все просто. Заходите на сайт, нажимаете кнопку 'регестрация' и заполняете данные😊\nМы очень рады ответить на все ваши вопросыnЕсли остались вопросы, но тут их нет, свяжитесь с нами через кнопку '💬Связь с администрацией'\n\nНажмите '🔙Назад', чтобы вернуться.", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
        elif update.message.text == "🛡Авторы":            await context.bot.send_message(chat_id=user_id, text="Авторы:\nИван - Python - Чат-Бот developer\nЯков - Программист Сайта №1\nДмитрий - Программист Сайта №2\nАндрей - Дизайнер Сайта\n\nили нажмите '🔙Назад' для возврата: .", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
        elif update.message.text == "🔙Назад":
            await start(update, context) 
        else:
            await context.bot.send_message(chat_id=user_id, text="Ваше сообщение отправлено администратору.")
            messages_queue[user_id] = update.message.text
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новое сообщение от @{update.message.from_user.username}: {update.message.text}")
    else:
        await handle_admin_reply(update.message)

async def handle_admin_reply(message: Message) -> None:
    if message.reply_to_message and message.reply_to_message.from_user.id in messages_queue:
        user_id = message.reply_to_message.from_user.id
        await message.bot.send_message(chat_id=user_id, text=f"Ответ от администратора: {message.text}")
        del messages_queue[user_id]

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()

async def send_test_message():
       bot = telegram.Bot(token=TOKEN)
       try:
           await bot.send_message(chat_id=ADMIN_ID, text="Тестовое сообщение")
           print("Сообщение отправлено успешно.")
       except telegram.error.BadRequest as e:
           print(f"Ошибка отправки сообщения: {e}")

if __name__ == "__main__":
       asyncio.run(send_test_message())
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
       user_id = update.message.from_user.id
       if user_id != ADMIN_ID:
           messages_queue[user_id] = update.message.text
           try:
               await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новое сообщение от @{update.message.from_user.username}: {update.message.text}")
               await update.message.reply_text("Ваше сообщение отправлено администратору.")
           except telegram.error.BadRequest as e:
               logger.error(f"Не удалось отправить сообщение администратору: {e}")
       else:
           await handle_admin_reply(update.message)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    admin_id = 5642938812
    try:
        await context.bot.send_message(chat_id=admin_id, text="Сообщение!")
    except telegram.error.BadRequest as e:
        print(f"Не удалось отправить сообщение: {e}")
        
if __name__ == "__main__":
       asyncio.run(send_test_message())
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
       user_id = update.message.from_user.id
       if user_id == ADMIN_ID:
           messages_queue[user_id] = update.message.text
           try:
               await context.bot.send_message(chat_id=ADMIN_ID, text=f"Новое сообщение от @{update.message.from_user.username}: {update.message.text}")
               await update.message.reply_text("Ваше сообщение отправлено пользователю.")
           except telegram.error.BadRequest as e:
               logger.error(f"Не удалось отправить сообщение пользователю: {e}")
       else:
           await handle_admin_reply(update.message)



   

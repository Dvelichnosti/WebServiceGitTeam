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

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7682952936:AAGjkGlBk45iskGZouGk_ofW53e4DNrRsO0" #тг айди бота
ADMIN_ID = 5642938812 #тг айди админа

messages_queue = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("❗️Частые вопросы"),
         KeyboardButton("💬Связь с администрацией")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите один из вариантов:", reply_markup=reply_markup)

async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("✅Вопрос 1"), KeyboardButton("✅Вопрос 2")],
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
            await context.bot.send_message(chat_id=user_id, text="Напишите ваше сообщение администратору через бота\n❗смотрите в личные сообщения, администратор напишет туда\nили нажмите '🔙Назад' для возврата:", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
        elif update.message.text == "✅Вопрос 1":
            await context.bot.send_message(chat_id=user_id, text="Ответ на вопрос 1: Кто же мы такие🧐?\nмы команда GitTeam, 4 подростка, которые увлекаются созданием нового.😊\nМы очень рады представить вам данный проект \n\nНажмите '🔙Назад', чтобы вернуться.", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
        elif update.message.text == "✅Вопрос 2":
            await context.bot.send_message(chat_id=user_id, text="Ответ на вопрос 2: Для чего нужен этот бот🧐?\nЭтот бот нужен для обратной связи с нами,\nВ нем вы можете:\nСвязаться с нами, а также найти ответы на нужные вопросы\nНажмите '🔙Назад', чтобы вернуться.", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙Назад")]], resize_keyboard=True, one_time_keyboard=True))
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
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text="Сообщение!")
    except telegram.error.BadRequest as e:
        print(f"Не удалось отправить сообщение: {e}")


   

import logging
import time
import tracemalloc

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from constants import *
from cows_and_bulls_update.config import TOKEN
import random
from pet import Pet
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


run = False


# print(f"Мои статы: любовь: {pet.love}, сытость: {pet.satiety}, счастье: {pet.happiness}, энергия: {pet.energy}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global pet, run
    pet = Pet(update.effective_user.username)
    run = True
    keyboard = [
        [InlineKeyboardButton(LOVE, callback_data=LOVE_ID)],
        [InlineKeyboardButton(EAT, callback_data=EAT_ID)],
        [InlineKeyboardButton(PLAY, callback_data=PLAY_ID)],
        [InlineKeyboardButton(DEAD, callback_data=DEAD_ID)],
        [InlineKeyboardButton(SLEEP, callback_data=SLEEP_ID)],
        [InlineKeyboardButton(STATUS, callback_data=STATUS_ID)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # context.job_queue.run_once(miss_you, 1, chat_id=update.effective_chat.id, data=1)
    sticker, message = pet.hello()
    await context.bot.send_sticker(update.effective_chat.id, sticker)
    await context.bot.send_message(update.effective_chat.id, text=message, reply_markup=reply_markup)
    await do_delay_job(update, context)

    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(LOVE, callback_data=LOVE_ID)],
        [InlineKeyboardButton(EAT, callback_data=EAT_ID)],
        [InlineKeyboardButton(PLAY, callback_data=PLAY_ID)],
        [InlineKeyboardButton(DEAD, callback_data=DEAD_ID)],
        [InlineKeyboardButton(SLEEP, callback_data=SLEEP_ID)],
        [InlineKeyboardButton(STATUS, callback_data=STATUS_ID)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sticker, message = pet.hello()
    await context.bot.send_sticker(update.effective_chat.id, sticker)
    await query.edit_message_text(text=message, reply_markup=reply_markup)
    await do_delay_job(update, context)
    return START_ROUTES


async def delete_rubbish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.delete_message(update.effective_message.message_id-1)
    await update.effective_chat.delete_message(update.effective_message.message_id)


async def make_love(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Действие кнопки "Погладить" """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад в меню", callback_data=MENU)
        ],
        [
            InlineKeyboardButton("Еще погладить", callback_data=LOVE_ID)
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sticker, bot_message = pet.increase_love()
    bot_message += f" Уровень любви повышен: {pet.love}"
    await do_delay_job(update, context)
    if bot_message != query.message.text:
        await delete_rubbish(update, context)
        await context.bot.send_sticker(update.effective_chat.id, sticker)
        await context.bot.send_message(update.effective_chat.id, bot_message, reply_markup=reply_markup)
    return START_ROUTES


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Удалить"""
    await context.bot.send_sticker(update.effective_chat.id, NOT_GOOD_STICK)
    await context.bot.send_message(update.effective_chat.id, "За что, хозяин? Я ведь лишь старался быть любимым...")
    return ConversationHandler.END


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()

async def do_delay_job(update:Update, context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    due = 60 * 60 
    job_removed = remove_job_if_exists(str(chat_id), context)
    # await context.job_queue.run_repeating(miss_you, due, chat_id=chat_id, name=str(chat_id), data=update.effective_user.username)
    await context.job_queue.run_once(miss_you, due, chat_id=chat_id, name=str(chat_id), data=due)



async def miss_you(context: ContextTypes.DEFAULT_TYPE) -> int:
    """Скучает"""
    bot_message = random.choice(MISS_PHRASES)
    for i in range(random.randint(1, 5)):
        pet.decrease_stats(True)
    job = context.job
    await context.bot.send_message(job.chat_id, bot_message)
    


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Действие кнопки Положить корм"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("Назад в меню", callback_data=MENU)
        ],
        [
            InlineKeyboardButton("Еще покормить", callback_data=EAT_ID)
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sticker, bot_message = pet.increase_satiety()
    await do_delay_job(update, context)
    if bot_message != query.message.text:
        await context.bot.send_sticker(update.effective_chat.id, sticker)
        await context.bot.send_message(update.effective_chat.id, bot_message, reply_markup=reply_markup)
    return START_ROUTES


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Действие кнопки "Играть" """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад в меню", callback_data=MENU)
        ],
        [
            InlineKeyboardButton("Еще поиграть", callback_data=PLAY_ID)
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    sticker, bot_message = pet.increase_happiness()
    await do_delay_job(update, context)
    if bot_message != query.message.text:
        await context.bot.send_sticker(update.effective_chat.id, sticker)
        await context.bot.send_message(update.effective_chat.id, bot_message, reply_markup=reply_markup)
    return START_ROUTES


async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Действие кнопки "Уложить спать" """
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад в меню", callback_data=MENU)
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    pet.increase_energy()
    bot_message = f"Вы уложили спать тамагочи, чтобы у него были силы для новых свершений! Уровень энергии: {pet.energy}"
    await do_delay_job(update, context)
    if bot_message != query.message.text:
        await context.bot.send_sticker(update.effective_chat.id, LOVE2_STICK)
        await context.bot.send_message(update.effective_chat.id, bot_message)
        time.sleep(10)
        await context.bot.send_message(update.effective_chat.id, "Тамагочи проснулся!", reply_markup=reply_markup)
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    bot_message = "Возвращайся скорее, я буду ждать тебя. Твой Тамагочи"
    await context.bot.send_sticker(update.effective_chat.id, REST_STICK)
    await context.bot.send_message(update.effective_chat.id, bot_message)
    return ConversationHandler.END
# async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Действие кнопки Положить корм"""
#     query = update.callback_query
#     await query.answer()
#     keyboard = [
#         [
#             InlineKeyboardButton("Назад в меню", callback_data=MENU)
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await query.delete_message()
#     await context.bot.send_animation(update.effective_chat.id, IMG_SLEEP,caption=f"Тамагочи лег спать. Не будите его")
#     for i in range(5):
#         pet.increase_happiness()
#         time.sleep(2)
#     await context.bot.delete_message(update.effective_chat.id, update.effective_message.id-1)
#     await context.bot.send_animation(update.effective_chat.id, IMG_SLEEP,caption=f"Тамагочи лег спать. Не будите его", reply_markup=reply_markup)
#     # await query.edit_message_caption(
#     #     caption="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
#     # )
#     return END_ROUTES


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Действие кнопки Положить корм"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Назад в меню", callback_data=MENU)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.delete_message()
    bot_message = f"Мои статы:\nЛюбовь: {pet.love}\nСытость: {pet.satiety}\nСчастье: {pet.happiness}\nЭнергия: {pet.energy}"
    await context.bot.send_sticker(update.effective_chat.id, BIRTHDAY_STICK)
    await context.bot.send_message(update.effective_chat.id, bot_message, reply_markup=reply_markup)
    await do_delay_job(update, context)
    return START_ROUTES


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """

    await context.bot.send_message(update.effective_chat.id, "Случается какая-то хуйня")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()
    # job_queue = application.job_queue

    # job_minute = job_queue.run_repeating(miss_you, chat_id=ContextTypes.DEFAULT_TYPE._chat_id,  interval=60, first=1)
    # job_minute.enabled = run

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(make_love, pattern=f"^{LOVE_ID}$"),
                CallbackQueryHandler(feed, pattern=f"^{EAT_ID}$"),
                CallbackQueryHandler(play, pattern=f"^{PLAY_ID}$"),
                CallbackQueryHandler(sleep, pattern=f"^{SLEEP_ID}$"),
                CallbackQueryHandler(stats, pattern=f"^{STATUS_ID}$"),
                CallbackQueryHandler(start, pattern="^" + str(MENU) + "$"),
                CallbackQueryHandler(delete, pattern="^" + str(DEAD_ID) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    # Планировщик
    # scheduler = BackgroundScheduler()
    # scheduler.add_jobstore('memory')

    # scheduler.add_job(miss_you, IntervalTrigger(minutes=1), kwargs={'context': application})

    # scheduler.start()

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT, delete_rubbish))

    # application.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Стартовая команда
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["Показать статус"],
        ["Покормить", "Напоить"],
        ["Поиграть", "Уложить спать"],
        ["Очистить", "Помощь"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Привет! Я твой тамагочи. Что ты хочешь сделать?", reply_markup=reply_markup)
    # Сохраним chat_id для отправки сообщений по расписанию
    context.user_data['chat_id'] = update.message.chat_id

# Обработчики команд
def show_status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Статус тамагочи: \nГолод: 50\nЖажда: 50\nСчастье: 50\nУсталость: 50\nЧистота: 50")

def feed(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ты покормил тамагочи. Голод уменьшился, счастье увеличилось!")

def drink(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ты напоил тамагочи. Жажда уменьшилась, счастье увеличилось!")

def play(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ты поиграл с тамагочи. Счастье увеличилось, усталость уменьшилась!")

def sleep(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ты уложил тамагочи спать. Усталость уменьшилась, энергия восстановилась!")

def clean(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ты очистил тамагочи. Чистота увеличилась!")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Список доступных команд: \n"
                              "/start - Начать работу с ботом\n"
                              "/status - Показать статус\n"
                              "/feed - Покормить\n"
                              "/drink - Напоить\n"
                              "/play - Поиграть\n"
                              "/sleep - Уложить спать\n"
                              "/clean - Очистить\n"
                              "/help - Помощь")

# Функция для отправки сообщений по расписанию
def scheduled_message(context: CallbackContext) -> None:
    job = context.job
    chat_id = job.context['chat_id']
    context.bot.send_message(chat_id=chat_id, text="Не забудь позаботиться о своем тамагочи!")

# Основная функция
def main() -> None:
    updater = Updater("YOUR_TOKEN_HERE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", show_status))
    dispatcher.add_handler(CommandHandler("feed", feed))
    dispatcher.add_handler(CommandHandler("drink", drink))
    dispatcher.add_handler(CommandHandler("play", play))
    dispatcher.add_handler(CommandHandler("sleep", sleep))
    dispatcher.add_handler(CommandHandler("clean", clean))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Планировщик
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore('memory')

    # Добавление задачи для отправки сообщений каждые 6 часов
    scheduler.add_job(scheduled_message, IntervalTrigger(hours=6), context=dispatcher)

    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



'''
Объяснение:
Логирование - настроено для отслеживания действий бота.
Планировщик - используется apscheduler.schedulers.background.BackgroundScheduler для создания и запуска задач в фоновом режиме.
Сохранение chat_id - в context.user_data для использования его в планировщике.
Функция scheduled_message - отправляет запланированные сообщения в чат.
Добавление задачи - планировщик добавляет задачу, которая будет выполняться каждые 6 часов, отправляя напоминание позаботиться о тамагочи.


'''
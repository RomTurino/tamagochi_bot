from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler,  ContextTypes
from constants import *
from user_work import User
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = User(update, context)
    context.user_data["user"] = user
    if not user.is_pet():
        await update.message.reply_text("Введи, как зовут твоего питомца: ")
    else:
        keyboard = [[InlineKeyboardButton(GO, callback_data=GO)]]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Твой питомец {user.pet} заждался тебя! Хорошо, что ты здесь❤️ Жми на кнопку для перехода к меню", reply_markup=markup)
    return CHOICE
    
    
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Вы в меню")
    
    user = context.user_data["user"]
    if update.message:
        message = update.message.text
        pet_name = await user.write_pet_name(message)
        context.user_data["pet_name"] = pet_name
    
    pet_name = user.pet
    
    tag =  morph.parse(pet_name)[0]
    nomn = tag.inflect({"nomn"}).word.capitalize()
    gent = tag.inflect({"gent"}).word.capitalize()
    datv = tag.inflect({"datv"}).word.capitalize()
    accs = tag.inflect({"accs"}).word.capitalize()
    ablt = tag.inflect({"ablt"}).word.capitalize()
    loct = tag.inflect({"loct"}).word.capitalize()
    keyboard = [
        [
            InlineKeyboardButton(EAT+" "+datv, callback_data=EAT),
            InlineKeyboardButton(SLEEP+" "+accs, callback_data=SLEEP),
        ],
        [InlineKeyboardButton(BUY+"\n"+datv, callback_data=BUY),
         InlineKeyboardButton(REST+"\n"+f"с {ablt}", callback_data=REST)],
        
        [InlineKeyboardButton(WORK +"\n"+ datv, callback_data=WORK),
         InlineKeyboardButton(STATS +"\n"+ gent, callback_data=STATS)],
        
        [InlineKeyboardButton(LOVE +"\n"+ accs, callback_data=LOVE),
         InlineKeyboardButton(DEAD +"\n"+ accs, callback_data=DEAD)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(update.effective_chat.id, "Выберите действие:", reply_markup=reply_markup)
    return CHOICE





async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Используй /start чтобы высветилось меню")

async def delete_rubbish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Возвращайся скорее с помощью команды /start")
    return ConversationHandler.END

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from constants import WORK, CHOICE, MENU

money = 0
async def make_money(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global money
    user = context.user_data["user"]
    query = update.callback_query
    await query.answer()
    # if query.data == str(MENU):
    #     print("Возврат в меню")
    #     return MENU
    keyboard = [[InlineKeyboardButton(f"Монет: {user.money}", callback_data=WORK)],
                [InlineKeyboardButton(f"Назад в меню", callback_data=MENU)]]
    markup = InlineKeyboardMarkup(keyboard)
    user.money += 1
    user.save_money()
    await query.edit_message_text("Жми на кнопку, чтобы увеличить количество монет!", reply_markup=markup)
    return CHOICE
    # return ConversationHandler.END
from telegram import  Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ConversationHandler, CommandHandler,filters, MessageHandler
from cows_and_bulls_update.config import TOKEN

from constants import *
from main_menu import * 
from earn_money import make_money





application = ApplicationBuilder().token(TOKEN).build()
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        # MENU: [],
        CHOICE:[CallbackQueryHandler(menu, pattern=f"^({MENU}|{GO})$"),
                CallbackQueryHandler(make_money, pattern=f"^({WORK})$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, menu)]
        },
    fallbacks=[CommandHandler("end", end)]
)

application.add_handler(conv_handler)
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT, delete_rubbish))
print("Server started")
application.run_polling(allowed_updates=Update.ALL_TYPES)



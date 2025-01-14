from telegram import Update
from telegram.ext import CallbackContext

def handle_start(update: Update,context:CallbackContext):
    update.message.reply_text("Welcome to the bot! Type /help for more options.")

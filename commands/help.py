from telegram import Update
from telegram.ext import CallbackContext

def handle_help(update: Update,context:CallbackContext):
    update.message.reply_text("Here are the available commands: /start, /help, /custom_command.")

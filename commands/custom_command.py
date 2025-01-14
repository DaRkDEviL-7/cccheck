from telegram import Update
from telegram.ext import CallbackContext

def handle_custom_command(update: Update,context:CallbackContext):
    update.message.reply_text("This is your custom command response!")

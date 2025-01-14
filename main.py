from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import importlib

from config import BOT_TOKEN
from commands import cc_check
# Function to dynamically load commands
def load_commands(dispatcher):
    command_dir = "commands"
    for filename in os.listdir(command_dir):
        if filename.endswith(".py"): #check for python scripts
            command_name = filename[:-3] #Remove .py extension
            module = imporlib.import_module(f"{command_dir}.{command_name}")
            handler_function = getattr(module, f"handle_{command_name}")
            dispatcher.add_handler(CommandHandler(command_name, handler_fuction))
#Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    #Load all commands dynamically
    load_commands(dispatcher)
    dispatcher.add_handler(Commandhandler("cccheck", cc_check.handle_cccheck))

    #start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()




from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, DictPersistence
import telegram
import logging
from bot import bot_config
from bot.commands.commands_setup import BotCommands
from bot.commands.chooser import Chooser
from exceptions.exception_classes import NoDataFound, NoLocation
from conf import logfile
from bot.helper_functions import keyboard_location as kl
from bot.helper_functions import helper_functions
import json
logger = logging.getLogger(__name__)

class TelegramInit(bot_config.Config):

    def __init__(self):

        super().__init__()

        dp = DictPersistence()

        self.updater = Updater(self.token, persistence=dp, use_context=True)
        self.dispatch = self.updater.dispatcher
        get_location_handler = MessageHandler(Filters.location, loc,  pass_job_queue=True, pass_chat_data=True, pass_user_data=True)
        self.dispatch.add_handler(get_location_handler)
        self.dispatch.add_handler(CommandHandler("location", get_location,
                                              pass_args=True,
                                              pass_job_queue=True,
                                              pass_chat_data=True))
        self.dispatch.add_handler(CommandHandler("help", start))
        self.dispatch.add_handler(CommandHandler("start", start))
        self.dispatch.add_handler(CommandHandler("now", starter,
                                      pass_args=True,
                                      pass_job_queue=True,
                                      pass_chat_data=True))
        self.dispatch.add_handler(CommandHandler("daily", starter,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True
        ))
        self.dispatch.add_handler(CommandHandler("forecast", starter,
                                pass_args=True,
                                pass_job_queue=True,
                                pass_chat_data=True
        ))
        self.dispatch.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
        self.dispatch.add_error_handler(error)
        self.updater.start_polling()
        self.updater.idle()

def start(update, context):

    update.message.reply_text("Hi! Use /daily <location> to set a daily"
                              "weather info for location or /now <location> for weather info for location now."
                              "Use /forecast <location> if you wish to see the weather forecast of the day."
                              "With using /location <now/daily/forecast> the gps location is used to show the weather info"
                              "now, daily or now with forecast."
                              )


def unset(update, context):
    """ Remove all running jobs.
    """
    if "job" not in context.chat_data:
        update.message.reply_text("No active location")
        return
    job = context.chat_data["job"]
    job.schedule_removal()
    del context.chat_data["job"]
    update.message.reply_text("Successfully unset")

@logfile.logging_decorator
def error(update, context):
    logger.warning("Update %s caused error %s", update, context.error)


def get_bot(update, context, *args):

    print(update)
    if args:
        command = args[0]
    else:
        command = update["message"]["text"].split()
        command = command[0]
    user_command = [{ 'command' : command }]
    with open("commands.json", "w") as f:
        json.dump(user_command, f)
    print(command)


def loc(update, context):
    start_bot(update, context)

def starter(update, context):
    get_bot(update, context)
    start_bot(update, context)

def start_bot(update, context):

    command = helper_functions.read_json_file("commands.json")
    botcommand = BotCommands(update, context, command)
    try:
        botcommand.location()
    except (IndexError, ValueError):
        update.message.reply_text("Usage /now <location>, /daily <location>, /forecast <location> or /location <daily/now/forecast>. The last option gets the gps location.")
        raise NoLocation("Location couldn't be set correctly.")

def get_location(update, context):

    command = "".join(context.args)
    get_bot(update, context, command)
    kl.get_keyboard_location(update)

if __name__ == "__main__":
    TelegramInit()

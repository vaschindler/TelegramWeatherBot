import logging
from conf.logfile import logging_decorator
from bot.commands.chooser import Chooser
from exceptions.exception_classes import NoDataFound, NoLocation

logger = logging.getLogger(__name__)


class BotCommands:
    def __init__(self, update, context, command):
        self.update = update
        self.context = context
        self.command = command


    def location(self):
        chat_id = self.update.message.chat_id
        print(self.context.args)
        if self.context.args is None:
            print(self.update.message.location.latitude)
            latitude = self.update.message.location.latitude
            longitude = self.update.message.location.longitude
            args = {"chat_id": chat_id, "location" : "location", "latitude": latitude, "longitude" : longitude}
        else:
            location = " ".join(self.context.args)
            if location is None:
                self.update.message.reply_text("Sorry no location was set")
            args = {"chat_id":chat_id, "location" : location}
        print(args)
        choose = Chooser(self.update, self.context, self.command)
        choose.run_message(args)

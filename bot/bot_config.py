import os
import configparser
import functools
import logging
from conf import logfile

logger = logging.getLogger(__name__)


class Config:

    def __init__(self):
        self.confpath = "conf/config.ini"
        self.parser = self._parser()
        self.token
        self.weatherapi

    @logfile.logging_decorator
    def _parser(self):
        """Config of Telegram Bot
        """
        config = configparser.ConfigParser()
        if not os.path.exists(self.confpath):
            logger.info("Creating the config file. \n"
                        "Please insert the Token from the telegram API in STUB in the {0} file.".format(self.confpath))
            config["DEFAULT"] = {"Token": "STUB"}
            with open(self.confpath, "wt") as configfile:
                config.write(configfile)
        config.read(self.confpath)
        self.token = config["DEFAULT"]["TOKEN"]
        self.weatherapi = config["OPENWEATHERMAP"]["KEY"]
        return self.token, self.weatherapi


from bot.weatherinfo.weather_setup import WeatherInfo
import datetime

class Chooser:

    def __init__(self, update, context, command):

        self.update = update
        self.context = context
        self.command = command

    def run_message(self, args):

        weatherinfo = WeatherInfo()
        self.update.message.reply_text("Show weather information!")
        if self.command == "now":
            self.update.message.reply_text("Show weather now for {0} location".format(args["location"]))
            new_job = self.context.job_queue.run_once(weatherinfo.weather_now, 1, context=args)
            self.context.chat_data["job"] = new_job
            self.update.message.reply_text("Location successfully set!")
        if self.command == "forecast":
            self.update.message.reply_text("Show weather forecast for {0} location".format(args["location"]))
            new_job = self.context.job_queue.run_once(weatherinfo.weather_forecast, 1, context=args)
            self.context.chat_data["job"] = new_job
            self.update.message.reply_text("Location successfully set!")
        if self.command == "daily":
            self.update.message.reply_text("Set daily weather information!")
            set_time = datetime.time(8, 30, 00, 000000)
            new_job = self.context.job_queue.run_daily(weatherinfo.weather_forecast, set_time, context=args)
            self.context.chat_data["job"] = new_job
            self.update.message.reply_text("Location successfully set!")

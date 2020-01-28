from bot.weatherinfo.receive_data import ReceiveData
from bot.helper_functions import helper_functions
from exceptions.exception_classes import NoDataFound, NoLocation
import datetime

class WeatherForecast():

    def __init__(self, context):
        self.context = context
        self.location = self.context.job.context["location"]
        self.chat_id = self.context.job.context["chat_id"]

    def _get_forecast(self, **location):
        base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        data = ReceiveData(self.chat_id, base_url, **location).receive_data()
        return data

    def weather_message_location(self):
        location = {"location":self.location}
        data = self._get_forecast(**location)
        self.send_weather_forecast(data)

    def send_weather_forecast(self, data):
        date_today = str(datetime.date.today())
        if data["cod"] == "404":
            self.context.bot.send_message(self.chat_id, text="Location is not known. Please try again with different naming.")
            raise NoDataFound("Site is not reachable")
        main = data["list"]
        for i in range(len(main)):
            temp = main[i]["main"]["temp"]
            weather_state = main[i]["weather"][0]["main"]
            weather_icon = main[i]["weather"][0]["icon"]
            image = helper_functions.get_image(weather_icon)
            date = main[i]["dt_txt"]

            print(type(date.split()[0]))
            if date.split()[0] == date_today:
                celsius_temp = helper_functions.kelvin_to_celsius(temp)
                self.context.bot.send_message(self.chat_id, text="This is the temp. at {0}: {1} Grad".format(date, format(celsius_temp, ".2f")))
                self.context.bot.send_message(self.chat_id, text="The weather right now is: {0}". format(weather_state))
                self.context.bot.send_photo(self.chat_id, image)

    def weather_message_lat_lon(self, latitude, longitude):
        location = {"lat": latitude, "lon": longitude}
        data = self._get_forecast(**location)
        self.send_weather_forecast(data)

from bot.weatherinfo.receive_data import ReceiveData
from bot.helper_functions import helper_functions
from exceptions.exception_classes import NoDataFound, NoLocation

class WeatherNow():

    def __init__(self, context):
        self.context = context
        self.chat_id = self.context.job.context["chat_id"]
        self.location = self.context.job.context["location"]

    def get_weather_now(self, **location):

        base_url= "http://api.openweathermap.org/data/2.5/weather?"
        print("TAHDH")
        data = ReceiveData(self.chat_id, base_url, **location).receive_data()
        return data

    def weather_message_location(self):
        location = {"location":self.location}
        data = self.get_weather_now(**location)
        self.send_weather_message(data)

    def send_weather_message(self, data):
        if data["cod"] == "404":
            self.context.bot.send_message(self.chat_id, text="Location is not known. Please try again with different naming.")
            raise NoDataFound("Site is not reachable")
        main = data["main"]
        temp = main["temp"]
        celsius_temp = helper_functions.kelvin_to_celsius(temp)
        for i in range(len(data["weather"])):
            weather = data["weather"][i]
            weather_state = weather["main"]
            weather_icon = weather["icon"]
            image = helper_functions.get_image(weather_icon)
        self.context.bot.send_message(self.chat_id, text="This is the temp. right now: {0} Grad".format(format(celsius_temp, ".2f")))
        self.context.bot.send_message(self.chat_id, text="The weather right now is: {0}". format(weather_state))
        self.context.bot.send_photo(self.chat_id, photo=image)

    def weather_message_lat_lon(self, latitude, longitude):
        location = {"lat": latitude, "lon": longitude}
        data = self.get_weather_now(**location)
        self.send_weather_message(data)

from bot.bot_config import Config
from bot.weatherinfo.weather_now import WeatherNow
from bot.weatherinfo.weather_forecast import WeatherForecast

class WeatherInfo(Config):
    def __init__(self):
        super().__init__()


    def _location_chooser(self, context, func):
        location = context.job.context["location"]
        if location == "location":
            latitude = context.job.context["latitude"]
            longitude = context.job.context["longitude"]
            func.weather_message_lat_lon(latitude, longitude)
        else:
            func.weather_message_location()

    def weather_now(self, context):
        """ Gets the weather information from openweathermap and
            outputs the data to the user.
        """
        self._location_chooser(context, WeatherNow(context))

    def weather_forecast(self, context):

        self._location_chooser(context, WeatherForecast(context))

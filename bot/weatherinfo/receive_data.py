import requests
from bot.bot_config import Config
from exceptions.exception_classes import NoDataFound, NoLocation

class ReceiveData(Config):
    def __init__(self, chat_id, base_url, **kwargs):
        super().__init__()
        if "location" in kwargs:
            self.location = kwargs["location"]
            self.url = "&q=" + str(self.location)
        elif "lat" in kwargs:
            self.latitude = kwargs["lat"]
            self.longitude = kwargs["lon"]
            self.url =  "&lat=" + str(self.latitude) + "&lon=" + str(self.longitude)
        self.chat_id = chat_id
        self.base_url = base_url

    def receive_data(self):
        complete_url = self.base_url + "appid=" + self.weatherapi + self.url
        response = requests.get(complete_url)
        data = response.json()
        return data

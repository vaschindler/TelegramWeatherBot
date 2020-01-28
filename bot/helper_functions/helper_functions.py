def kelvin_to_celsius(kelvin):
    celsius_temp = kelvin - 273.15
    return celsius_temp

def get_image(weather_icon):
    base_url= "http://openweathermap.org/img/wn/"
    complete_url = base_url + weather_icon + "@2x.png"
    return complete_url

def read_json_file(file):
    import json
    with open(file, "r") as f:
        data = json.load(f)
        print(str(data)+"HHHHH")
        command = data[0]["command"]
        command = command.strip("/")
        return command

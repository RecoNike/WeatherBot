import json
import requests
import config
from datetime import datetime

def get_coord(city):
    headers = {'Accept': 'application/json'}

    r = requests.get(f'https://geocode.maps.co/search?q={city}&api_key={config.GEO_API}', headers=headers)

    print(f'Coords get : {[float(r.json()[0]['lat']), float(r.json()[0]['lon'])]}')
    return [float(r.json()[0]['lat']), float(r.json()[0]['lon'])]


def getWeather(city):
    headers = {
    'Accept': 'application/json',
    'User-Agent': 'WeatherTGbot/1.0 (reconike@gmail.com)'
    }
    coords = get_coord(city)

    weat = requests.get(f'https://api.met.no/weatherapi/locationforecast/2.0/complete?lat={coords[0]}&lon={coords[1]}&altitude=90', headers = headers)
    print(weat.status_code)
    print(type(weat))
    # print(weat.text)
    with open("response.json", "w", encoding="utf-8") as file:
        file.write(weat.text)


    weather_data = weat.json()
    
    timeseries = weather_data["properties"]["timeseries"][:6]
    
    forecast_text = "🌦 **Прогноз на ближайшие 6 часов:**\n\n"

    for entry in timeseries:
        time_str = entry["time"]
        details = entry["data"]["instant"]["details"]
        precipitation_prob = entry["data"]["next_12_hours"]["details"]["probability_of_precipitation"]

        # Преобразуем время в читаемый формат
        time_obj = datetime.fromisoformat(time_str[:-1])
        time_formatted = time_obj.strftime("%H:%M")

        # Извлекаем нужные данные
        temp = details["air_temperature"]
        cloudiness = details["cloud_area_fraction"]
        wind_speed = details["wind_speed"]
        wind_direction = details["wind_from_direction"]
        pressure = details["air_pressure_at_sea_level"]

        # Подбираем эмодзи по погоде
        weather_icon = "☁️" if cloudiness > 50 else "🌤"
        wind_icon = "🍃" if wind_speed < 2 else "💨"
        rain_icon = "🌧" if precipitation_prob > 50 else "🌂"

        # Формируем строку прогноза с отступом
        forecast_text += (
            f"🕒 **{time_formatted}**\n"
            f"🌡 **Температура:** {temp}°C\n"
            f"{weather_icon} **Облачность:** {cloudiness}%\n"
            f"{wind_icon} **Ветер:** {wind_speed} м/с ({wind_direction}°)\n"
            f"📊 **Давление:** {pressure} hPa\n"
            f"{rain_icon} **Вероятность осадков:** {precipitation_prob}%\n\n"
        )

    return forecast_text
    
    
    
    #return weat.json()['properties']['timeseries'][0]
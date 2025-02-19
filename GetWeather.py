import json
import requests
import config

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
    print(weat.text)
    with open("response.xml", "w", encoding="utf-8") as file:
        file.write(weat.text)


    weather_data = weat.json()
    
    try:
        first_hour_forecast = weather_data['properties']['timeseries'][1]
    except (KeyError, IndexError) as e:
        print("Error extracting forecast data:", e)
        #return None
    print(weat.status_code)

    return first_hour_forecast
    
    
    
    #return weat.json()['properties']['timeseries'][0]
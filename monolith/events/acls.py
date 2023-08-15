import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_photo(city, state):
    # Create the URL for the request with the city and state
    url = 'https://api.pexels.com/v1/search'
    params = {
        "query": f'{city},{state}',
        "per_page": 1
    }
    # Create a dictionary for the headers to use in the request
    headers = {"Authorization": PEXELS_API_KEY}

    # Make the request
    response = requests.get(url, headers=headers, params=params)

    # Parse the JSON response
    api_dict = response.json()

    # Return a dictionary that contains a "picture_url" key and
    # one of the URLs for one of the pictures in the response
    return {"picture_url": api_dict['photos'][0]['src']['original']}


def get_weather_data(city, state):

    # Use the Open Weather API
    # Create the URL for the geocoding API with the city and state
    geo_url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {
        "q": f'{city},{state},US',
        "appid": OPEN_WEATHER_API_KEY
    }

    # Make the request
    geo_response = requests.get(geo_url, params=params)

    # Parse the JSON response
    geo_dict = geo_response.json()

    # Get the latitude and longitude from the response
    # Return None if not found
    try:
        latitude = geo_dict[0]['lat']
        longitude = geo_dict[0]['lon']
    except (KeyError, IndexError):
        return None

    # Create the URL for the current weather API with the lat and lon
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    # Make the request
    weather_response = requests.get(weather_url, params=params)

    # Parse the JSON response
    weather_dict = weather_response.json()

    # Get the main temp and the weather's description
    # Return None if not found
    try:
        temperature = weather_dict['main']['temp']
        description = weather_dict['weather'][0]['description']
    except (KeyError, IndexError):
        return None

    # Return dictionary
    return {
            "temp": temperature,
            "description": description
        }

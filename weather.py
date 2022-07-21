

from configparser import ConfigParser

def _get_api_key():
    # Private function to fetch API key from config file

    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

import argparse 
import json
import sys
from configparser import ConfigParser
from urllib import error, parse, request
from pprint import pp

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def read_user_cli_args():
    # Handles command line user interactions
# fa
    parser = argparse.ArgumentParser(
        description = "gets weather and temperature information"
    )

    parser.add_argument(
        "city", nargs="+", type=str, help='enter the city name'
    )

    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units"
    )



    return parser.parse_args()


def build_weather_query(city_input, imperial=False):
    # Builds URL for API request
    # Arguments: name of city (str), imperial (bool) to determine if imperial units are used
    # Returns URL

    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name) # Replaces spaces with plus signs
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url



def get_weather_data(query_url):
    # Makes API request to URL and returns the data as a Python object
    # Arguements: URL formatted for OpenWeather(str)
    # Returns weather info (dict) for specific city

    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: # Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404: # Not found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")

    response = request.urlopen(query_url)
    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")

    return json.loads(data) # Parses JSON string and converts it to a dictionary

if __name__=="__main__":
    user_args=read_user_cli_args()
    query_url = build_weather_query(user_args.city,user_args.imperial)
    weather_data = get_weather_data(query_url)
    pp(weather_data)
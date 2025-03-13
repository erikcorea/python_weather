from configparser import ConfigParser
import argparse
from urllib import parse

BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def read_user_cli_args():
  parser = argparse.ArgumentParser(
    description="gets weather and temperature information for a city"
  )
  parser.add_argument(
    "city", nargs="+", type=str, help="enter the city name"
  )
  parser.add_argument(
    "-m",
    "--metric",
    action="store_true",
    help="display the temperature in metric units"
  )
  return parser.parse_args()

def build_weather_query(city_input, metric=False):
  """
  Builds the URL for the API request to OpenWeather
    
  Args:
    city_input (list[str]): Name of a city as collected by argparse
    metric (bool): Whether or not to use metric units
  
  Returns:
    str: URL formatted for a call to OpenWeather's city name endpoint
  """
  api_key = _get_api_key()
  city_name = " ".join(city_input)
  url_encoded_city_name = parse.quote_plus(city_name)
  units = "metric" if metric else "imperial"
  url = (
    f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
    f"&units={units}&appid={api_key}"
  )
  return url

def _get_api_key():
  """
  Fetch the API key from your config file.

  Expects a config file named "secrets.ini" with structure:
    [openweather]
    api_key=apikey
  """
  config = ConfigParser()
  config.read("secrets.ini")
  return config["openweather"]["api_key"]

if __name__ == "__main__":
  user_args = read_user_cli_args()
  query_url = build_weather_query(user_args.city, user_args.metric)
  print(query_url)

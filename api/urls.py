from api.handlers.temperature_checker import TemperatureHandler

api_urls = [
    (r'/temperature_check', TemperatureHandler),
]

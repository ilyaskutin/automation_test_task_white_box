import json

from api_server.api.handlers.basic_handlers import JSONHandler
from tornado.gen import coroutine
from tornado.web import HTTPError
from voluptuous.error import Invalid

from api_server.api.schema import temperature_validator

TEMPERATURE_SCALE_SYSTEM = {
    'C': 'Celsius',  # TODO: maybe this wrong?
    'K': 'Kelvin',
    'F': 'Fahrenheit'
}

WATER_STATES = {  # TODO: rewrite this and use limits
    'Celsius': {
        'steam': tuple(range(100, 999999)),
        'liquid': tuple(range(0, 100)),
        'ice': tuple(range(-273, 1)),
    },
    'Kelvin': {
        'steam': tuple(range(374, 1000271)),
        'liquid': tuple(range(274, 374)),
        'ice': tuple(range(0, 274)),
    },
    'Fahrenheit': {
        'steam': tuple(range(212, 1800029)),
        'liquid': tuple(range(33, 212)),
        'ice': tuple(range(-459, 33)),
    }
}


class TemperatureHandler(JSONHandler):
    scale_system = 'Celsius'

    @coroutine
    def get(self):
        raw_temperature = self.get_argument('temperature')
        try:
            temperature = temperature_validator(raw_temperature)
        except Invalid as err:
            raise HTTPError(
                400,
                reason=err.error_message
            )
            return
        if temperature.isdigit():
            scale_system = self.scale_system
            digit_temperature = json.loads(temperature)
        else:
            try:
                scale_system = self.scale_system
                digit_temperature = round(float(temperature))
            except ValueError:
                scale_system = TEMPERATURE_SCALE_SYSTEM[temperature[-1]]
                digit_temperature = round(float(json.loads(temperature[:-1])))

        water_states = WATER_STATES.get(scale_system)
        if water_states is None:
            raise HTTPError(
                400,
                reason='Unknown temperature scale system {}, with temperature {}'.format(
                    scale_system, temperature)
            )
            return
        for state, ranges in water_states.items():
            if digit_temperature in ranges:
                self.finish(state)
                return
        else:
            self.finish('unknown')
            return

from __future__ import annotations

import abc
import decimal
import logging
import os
from datetime import datetime, time
import caldav
import django.db.models
import icalendar
import pyowm
from users.models import CustomUser
from . import models, exceptions
from typing import Type


class AbstractDataSource(abc.ABC):
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def retrieve_data(self, query: datetime) -> dict[str, any]:
        pass


class AbstractDataSourceConfigurator(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def configure(cls, user: CustomUser) -> AbstractDataSource:
        pass


class AbstractDatabaseDataSourceConfigurator(AbstractDataSourceConfigurator):
    settings_model: Type[django.db.models.Model] = None
    data_source: Type[AbstractDataSource] = None

    @classmethod
    def configure(cls, user: CustomUser) -> AbstractDataSource:
        try:
            settings = cls.settings_model.objects.get(user=user)
        except cls.settings_model.DoesNotExist:
            raise exceptions.SettingsNotConfigured(service_class=cls.data_source)

        return cls.data_source(**vars(settings))


class CalDavDataSource(AbstractDataSource):
    def __init__(self, caldav_url: str, calendar_url: str, username: str, password: str, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.caldav_client = caldav.DAVClient(
            url=caldav_url,
            username=username,
            password=password,
        )
        self.calendar: caldav.Calendar = self.caldav_client.calendar(url=calendar_url)

    def retrieve_data(self, query: datetime) -> dict[str, any]:
        data: dict[str, any] = {
            'events': []
        }

        raw_events = self.calendar.search(  # noqa
            start=datetime.combine(query, time.min),  # start of day
            end=datetime.combine(query, time.max),  # end of day
            event=True,
            expand=True,  # cause recurring events to be expanded
        )  # noqa
        self.logger.debug(f'# events: {len(raw_events)}')

        for raw_event in raw_events:
            ical_calendar = icalendar.Calendar.from_ical(raw_event.data)  # parse from ical format
            for component in ical_calendar.walk():
                # only interested in the 'VEVENT' component
                if component.name == 'VEVENT':
                    event_summary = component.get('summary')  # the user defined 'name'

                    if event_summary:  # check if empty string
                        self.logger.debug(f'event: {event_summary}')
                        data['events'].append(event_summary)

        return data


class OpenWeatherDataSource(AbstractDataSource):
    units = os.getenv('OWM_UNITS')
    open_weather_map = pyowm.owm.OWM(api_key=os.getenv('OWM_API_KEY'))
    weather_manager = open_weather_map.weather_manager()

    def __init__(self, latitude: decimal.Decimal, longitude: decimal.Decimal, **kwargs):
        super().__init__(**kwargs)

        self.latitude = latitude
        self.longitude = longitude

    def retrieve_data(self, query: datetime) -> dict[str, any]:
        one_call: pyowm.owm.weather_manager.one_call.OneCall = self.weather_manager.one_call(
            lat=float(self.latitude),
            lon=float(self.longitude),
            units=self.units,
        )
        current_weather: pyowm.owm.weather_manager.one_call.Weather = one_call.current

        return {
            'general_description': current_weather.detailed_status,
            'reference_time': f'{current_weather.reference_time(timeformat="iso")}',
            'sunrise_time': f'{current_weather.sunrise_time(timeformat="iso")}',
            'sunset_time': f'{current_weather.sunset_time(timeformat="iso")}',
            'temperature': f'{current_weather.temp} celsius',
            'dewpoint': f'{current_weather.dewpoint} celsius',
            'humidity': f'{current_weather.humidity} %',
            'cloudiness': f'{current_weather.clouds} %',
            'wind': f'{current_weather.wind(unit="meters_sec")} m/s',
            'rain': f'{current_weather.rain} mm/h',
            'snow': f'{current_weather.snow} mm/h',
        }


class CalDavDataSourceConfigurator(AbstractDatabaseDataSourceConfigurator):
    settings_model: Type[django.db.models.Model] = models.CalDavSettings
    data_source: Type[AbstractDataSource] = CalDavDataSource


class OpenWeatherDataSourceConfigurator(AbstractDatabaseDataSourceConfigurator):
    settings_model: Type[django.db.models.Model] = models.OpenWeatherSettings
    data_source: Type[AbstractDataSource] = OpenWeatherDataSource


class DataSourceManager(AbstractDataSource):
    DATA_SOURCE_ClASSES: dict[str, Type[AbstractDataSourceConfigurator]] = {
        'calendar': CalDavDataSourceConfigurator,
        'weather': OpenWeatherDataSourceConfigurator,
    }

    def __init__(self, user: CustomUser, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    def retrieve_data(self, query: datetime) -> dict[str, any]:
        data: dict[str, any] = dict()

        for key, data_source_class in self.DATA_SOURCE_ClASSES.items():
            data_source_instance = data_source_class.configure(user=self.user)
            data[key] = data_source_instance.retrieve_data(query=query)

        return data

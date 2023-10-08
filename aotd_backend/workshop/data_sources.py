from __future__ import annotations

import abc
import logging
from datetime import datetime, time
import caldav
import django.db.models
import icalendar
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


class CalDavDataSourceConfigurator(AbstractDatabaseDataSourceConfigurator):
    settings_model: Type[django.db.models.Model] = models.CalDavSettings
    data_source: Type[AbstractDataSource] = CalDavDataSource


# class CalDavDataSourceConfigurator(AbstractDataSourceConfigurator):
#     def configure(self, user: CustomUser) -> AbstractDataSource:
#         try:
#             settings = models.CalDavSettings.objects.get(user=user)
#         except models.CalDavSettings.DoesNotExist:
#             raise exceptions.SettingsNotConfigured(service_class=CalDavDataSource.__class__)
#
#         return CalDavDataSource(
#             caldav_url=settings.caldav_url,
#             calendar_url=settings.calendar_url,
#             username=settings.username,
#             password=settings.password,
#         )

class DataSourceManager(AbstractDataSource):
    DATA_SOURCE_ClASSES: dict[str, Type[AbstractDataSourceConfigurator]] = {
        'calendar': CalDavDataSourceConfigurator,
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

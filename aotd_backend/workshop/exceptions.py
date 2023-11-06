from typing import Type


class SettingsNotConfigured(Exception):
    def __init__(self, service_class: Type[any]):
        self.service_class: Type[any] = service_class
        message = f'settings are not configured for {service_class.__name__}'
        super().__init__(message)

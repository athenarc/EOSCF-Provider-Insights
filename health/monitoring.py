import json

import cronitor
from health.health_checks import service_health_test
from settings import APP_SETTINGS


class CronitorMonitoring:
    def __init__(self, is_prod, api_key):
        self.is_prod = is_prod
        cronitor.api_key = api_key

        self.heartbeat_monitor = cronitor.Monitor('provider-heartbeat')

    def send_heartbeat_message(self):
        if self.is_prod:
            self.heartbeat_monitor.ping(message=json.dumps(
                {
                    "version": APP_SETTINGS['BACKEND']['VERSION_NAME'],
                    "health": service_health_test()
                }
            ))


cronitor_monitoring = CronitorMonitoring(
    is_prod=APP_SETTINGS['BACKEND']['PROD'],
    api_key=APP_SETTINGS['CREDENTIALS']['CRONITOR_API_KEY']
)

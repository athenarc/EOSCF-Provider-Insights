import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from routes.add_routes import initialize_routes
from scheduler import start_scheduler_process
from settings import APP_SETTINGS

logging.basicConfig(level=logging.INFO if APP_SETTINGS['BACKEND']['PROD'] else logging.DEBUG,
                    format='%(levelname)s | %(asctime)s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

sentry_sdk.init(
    dsn=APP_SETTINGS['CREDENTIALS']['SENTRY_SDN'],
    traces_sample_rate=1.0
)
if not APP_SETTINGS['BACKEND']['PROD']:
    sentry_sdk.init()  # Disable sentry if we are not in a dev environment

app = FastAPI()
initialize_routes(app)


def main():
    start_scheduler_process()

    uvicorn.run("main:app",
                host=APP_SETTINGS['BACKEND']['FASTAPI']['HOST'],
                port=APP_SETTINGS['BACKEND']['FASTAPI']['PORT'],
                reload=APP_SETTINGS['BACKEND']['FASTAPI']['RELOAD'],
                debug=APP_SETTINGS['BACKEND']['FASTAPI']['DEBUG'],
                workers=APP_SETTINGS['BACKEND']['FASTAPI']['WORKERS'],
                reload_dirs=["provider_statistics/"])


if __name__ == '__main__':
    main()

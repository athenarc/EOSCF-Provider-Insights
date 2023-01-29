import sentry_sdk
import uvicorn
from fastapi import FastAPI
from routes.add_routes import initialize_routes
from settings import APP_SETTINGS

sentry_sdk.init(
    dsn=APP_SETTINGS['CREDENTIALS']['SENTRY_SDN'],
    traces_sample_rate=1.0
)
if not APP_SETTINGS['BACKEND']['PROD']:
    sentry_sdk.init()  # Disable sentry if we are not in a dev environment

app = FastAPI()
initialize_routes(app)


def main():
    uvicorn.run("main:app",
                host=APP_SETTINGS['BACKEND']['FASTAPI']['HOST'],
                port=APP_SETTINGS['BACKEND']['FASTAPI']['PORT'],
                reload=APP_SETTINGS['BACKEND']['FASTAPI']['RELOAD'],
                debug=APP_SETTINGS['BACKEND']['FASTAPI']['DEBUG'],
                workers=APP_SETTINGS['BACKEND']['FASTAPI']['WORKERS'],
                reload_dirs=["provider_statistics/"])


if __name__ == '__main__':
    main()

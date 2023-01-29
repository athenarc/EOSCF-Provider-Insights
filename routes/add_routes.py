from routes import health, statistics


def initialize_routes(app):
    app.include_router(health.router)
    app.include_router(statistics.router)

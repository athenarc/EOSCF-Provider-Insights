from dateutil.parser import parse
from dbs.collaborative_rs.queries import CollaborativeRSMongo


def find_recommendations_per_day(provider_id, service_id=None):
    db = CollaborativeRSMongo()

    if service_id is not None:
        statistics = db.get_number_of_recommendations_daily([service_id])
    else:
        services = db.get_services_of_provider(provider_id)
        statistics = db.get_number_of_recommendations_daily(services)

    return {
        parse(f'{statistic[0]["year"]}-{statistic[0]["month"]}-{statistic[0]["day"]}').strftime('%Y-%m-%d'):
            statistic[1]
        for statistic in statistics
    }


def find_most_recommended(provider_id):
    db = CollaborativeRSMongo()

    services = db.get_services_of_provider(provider_id)
    statistics = db.get_most_recommended(services)

    return {
            statistic[0]['service_id']: statistic[1]
            for statistic in statistics
        }

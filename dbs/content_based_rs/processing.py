from collections import Counter, defaultdict

from dateutil.parser import parse
from dbs.collaborative_rs.queries import CollaborativeRSMongo
from dbs.content_based_rs.queries import ContentBasedRSMongo


def find_recommendations_per_day(provider_id, service_id=None):
    # We need the collaborative mongo to find the services of a provider
    services_db = CollaborativeRSMongo()
    recommender_db = ContentBasedRSMongo()

    if service_id is not None:
        statistics = recommender_db.get_number_of_recommendations_daily([service_id])
    else:
        services = services_db.get_services_of_provider(provider_id)
        statistics = recommender_db.get_number_of_recommendations_daily(services)

    return {
        parse(f'{statistic[0]["year"]}-{statistic[0]["month"]}-{statistic[0]["day"]}').strftime('%Y-%m-%d'):
            statistic[1]
        for statistic in statistics
    }


def find_most_recommended(provider_id):
    services_db = CollaborativeRSMongo()
    recommender_db = ContentBasedRSMongo()

    services = services_db.get_services_of_provider(provider_id)
    statistics = recommender_db.get_most_recommended(services)

    return {
            statistic[0]['service_id']: statistic[1]
            for statistic in statistics
        }


def find_services_recommended_next_to_your_service(provider_id, service_id):
    if service_id is None:
        services_db = CollaborativeRSMongo()
        your_services = services_db.get_services_of_provider(provider_id)
    else:
        your_services = [service_id]

    recommender_db = ContentBasedRSMongo()

    recs_that_include_your_service = recommender_db.get_services_recommended_along_your_services(your_services)

    # Transform the list of lists to a list of sets
    recs_that_include_your_service = [set(recs) for recs in recs_that_include_your_service]
    your_services = set(your_services)

    def find_your_services_in_rec(service_ids):
        return your_services.intersection(service_ids)

    # We keep the count to immediately know which services got the most recommendations
    recs_per_service = defaultdict(lambda: {'recommendations_count': 0, 'services': []})

    for rec_set in recs_that_include_your_service:
        your_services_in_rec = find_your_services_in_rec(rec_set)
        for your_service in your_services_in_rec:
            competitor_services = rec_set.difference(your_services_in_rec)

            recs_per_service[your_service]['services'] += list(competitor_services)
            recs_per_service[your_service]['recommendations_count'] += len(competitor_services)

    for _, your_service in recs_per_service.items():
        your_service['services'] = Counter(your_service['services'])

    return recs_per_service

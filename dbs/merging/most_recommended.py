from dbs.collaborative_rs.processing import \
    find_most_recommended as find_collaborative_most_recommended
from dbs.content_based_rs.processing import \
    find_most_recommended as find_content_based_most_recommended

MOST_RECOMMENDED_STATISTICS_GETTERS = [find_collaborative_most_recommended,
                                       find_content_based_most_recommended]


def get_most_recommended_from_all_dbs(provider_id, top_n):
    statistics_per_db = [get_most_recommended_statistic(provider_id)
                         for get_most_recommended_statistic in MOST_RECOMMENDED_STATISTICS_GETTERS]

    final_results = statistics_per_db[0].copy()

    for db_stat in statistics_per_db[1:]:
        for service_id, recommendation in db_stat.items():
            if service_id in final_results:
                final_results[service_id] += recommendation
            else:
                final_results[service_id] = recommendation

    most_recommended = sorted([
        {
            'service_id': service_id,
            'recommendations': recommendations
        }
        for service_id, recommendations in final_results.items()
    ], key=lambda x: x['recommendations'], reverse=True)

    return most_recommended[:top_n]

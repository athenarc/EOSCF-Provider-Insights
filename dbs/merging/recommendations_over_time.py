from dbs.collaborative_rs.processing import \
    find_recommendations_per_day as find_collaborative_per_day
from dbs.content_based_rs.processing import \
    find_recommendations_per_day as find_content_based_per_day

DAILY_STATISTICS_GETTERS = [find_collaborative_per_day,
                            find_content_based_per_day]


def get_daily_recommendations_from_all_dbs(provider_id, service_id):
    statistics_per_db = [get_daily_statistic(provider_id, service_id)
                         for get_daily_statistic in DAILY_STATISTICS_GETTERS]

    final_results = statistics_per_db[0].copy()

    for db_stat in statistics_per_db[1:]:
        for date, recommendation in db_stat.items():
            if date in final_results:
                final_results[date] += recommendation
            else:
                final_results[date] = recommendation

    daily_recommendations = [
        {
            'date': date,
            'recommendations': recommendations
        }
        for date, recommendations in final_results.items()
    ]

    return daily_recommendations

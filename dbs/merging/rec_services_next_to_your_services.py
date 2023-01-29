from dbs.content_based_rs.processing import \
    find_services_recommended_next_to_your_service

MOST_RECOMMENDED_ALONG_YOUR_SERVICES_STATISTICS_GETTERS = [find_services_recommended_next_to_your_service]


def get_services_recommended_next_to_your_service_from_all_dbs(provider_id, service_id, top_n):
    recs_per_service = [get_recommended_along_your_service(provider_id, service_id)
                        for get_recommended_along_your_service in
                        MOST_RECOMMENDED_ALONG_YOUR_SERVICES_STATISTICS_GETTERS]

    recs_per_service = recs_per_service[0]  # TODO: Will fix it when we need to integrate to more than 1 databases

    recs_per_service_list = [
        {
            "service_id": service_id,
            "total_competitor_recommendations": recs['recommendations_count'],
            "competitors": [
                {"service_id": service_id, "recommendations": recommendations}
                for service_id, recommendations in recs['services'].items()]
        }
        for service_id, recs in recs_per_service.items()
    ]

    recs_per_service_list = sorted(recs_per_service_list,
                                   key=lambda x: x['total_competitor_recommendations'],
                                   reverse=True)

    return recs_per_service_list[:top_n]

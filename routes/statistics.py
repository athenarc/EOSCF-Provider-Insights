from typing import List

from auth.access_token_dependency import verify_access_token
from dbs.exceptions import IdNotFound, PidNotFound
from dbs.merging.most_recommended import get_most_recommended_from_all_dbs
from dbs.merging.rec_services_next_to_your_services import \
    get_services_recommended_next_to_your_service_from_all_dbs
from dbs.merging.recommendations_over_time import \
    get_daily_recommendations_from_all_dbs
from fastapi import APIRouter, Depends, HTTPException
from routes import model_interface

router = APIRouter(prefix='/v1')
model_mapper = model_interface.PidMapper()


@router.post(
    "/statistics/rs/daily",
    response_model=List[model_interface.DailyRecommendations],
    tags=["statistics"]
)
def get_daily_recommendations(request_info: model_interface.RequestRecommendationsPerDayWithPIDs,
                              dependencies=Depends(verify_access_token)):
    try:
        recommendations_per_day_request = model_mapper.transform_daily_recommendations_request(request_info)
    except PidNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    resp = get_daily_recommendations_from_all_dbs(recommendations_per_day_request.provider_id,
                                                  recommendations_per_day_request.service_id)

    return resp


@router.post(
    "/statistics/rs/most_recommended/",
    response_model=List[model_interface.MostRecommendedWithPIDs],
    tags=["statistics"]
)
def get_total_recommendations(request_info: model_interface.RequestMostRecommendedWithPIDs,
                              dependencies=Depends(verify_access_token)):
    try:
        most_recommended_request = model_mapper.transform_most_recommended_request(request_info)
    except PidNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    most_recommended_services = get_most_recommended_from_all_dbs(most_recommended_request.provider_id,
                                                                  most_recommended_request.top_n)

    try:
        resp = model_mapper.transform_most_recommended_response(most_recommended_services)
    except IdNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return resp


@router.post(
    "/statistics/rs/most_recommended_along_your_services/",
    response_model=List[model_interface.RecommendationsAlongYourServicesWithPIDs],
    tags=["statistics"]
)
def get_most_recommended_along_your_services(
        request_info: model_interface.RequestRecommendationsAlongYourServicesWithPIDs,
        dependencies=Depends(verify_access_token)):
    try:
        competitor_recommendations_request = model_mapper.transform_competitor_recs_request(request_info)
    except PidNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    competitor_recs = get_services_recommended_next_to_your_service_from_all_dbs(
        competitor_recommendations_request.provider_id,
        competitor_recommendations_request.service_id,
        competitor_recommendations_request.top_services_numb,
        competitor_recommendations_request.top_competitors_numb)

    try:
        resp = model_mapper.transform_competitor_recs_response(competitor_recs)
    except IdNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return resp

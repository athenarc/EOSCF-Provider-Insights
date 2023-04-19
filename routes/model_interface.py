from typing import List, Optional

from dbs.collaborative_rs.queries import CollaborativeRSMongo
from pydantic import BaseModel


class RequestRecommendationsPerDayWithPIDs(BaseModel):
    provider_id: str
    service_id: Optional[str]


class MostRecommended(BaseModel):
    service_id: str
    recommendations: int


class RequestMostRecommended(BaseModel):
    provider_id: int
    top_n: Optional[int] = 5


class RequestRecommendationsPerDay(BaseModel):
    provider_id: int
    service_id: Optional[int]


class DailyRecommendations(BaseModel):
    date: str
    recommendations: int


class RequestMostRecommendedWithPIDs(BaseModel):
    provider_id: str
    top_n: Optional[int] = 5


class MostRecommendedWithPIDs(BaseModel):
    service_id: str
    recommendations: int


class RequestRecommendationsAlongYourServicesWithPIDs(BaseModel):
    provider_id: str
    service_id: Optional[str] = None
    top_services_numb: Optional[int] = 5
    top_competitors_numb: Optional[int] = 5


class RequestRecommendationsAlongYourServices(BaseModel):
    provider_id: int
    service_id: Optional[int] = None
    top_services_numb: Optional[int] = 5
    top_competitors_numb: Optional[int] = 5


class CompetitorRecommendationsWithPIDs(BaseModel):
    service_id: str
    recommendations: int


class CompetitorRecommendations(BaseModel):
    service_id: int
    recommendations: int


class RecommendationsAlongYourServicesWithPIDs(BaseModel):
    service_id: str
    total_competitor_recommendations: int
    competitors: List[CompetitorRecommendationsWithPIDs]


class RecommendationsAlongYourServices(BaseModel):
    service_id: int
    total_competitor_recommendations: int
    competitors: List[CompetitorRecommendations]


class PidMapper:
    def __init__(self):
        self.rs_db = CollaborativeRSMongo()

    def _provider_pid_to_id(self, pid: str) -> int:
        return self.rs_db.get_provider_id_from_pid(pid)

    def _service_pid_to_id(self, pid: str) -> int:
        return self.rs_db.get_service_id_from_pid(pid)

    def _service_id_to_pid(self, service_id: int) -> str:
        return self.rs_db.get_service_pid_from_id(service_id)

    def transform_daily_recommendations_request(self, request: RequestRecommendationsPerDayWithPIDs) \
            -> RequestRecommendationsPerDay:
        return RequestRecommendationsPerDay(
            provider_id=self._provider_pid_to_id(request.provider_id),
            service_id=self._service_pid_to_id(request.service_id) if request.service_id is not None else None
        )

    def transform_most_recommended_request(self, request: RequestMostRecommendedWithPIDs) -> RequestMostRecommended:
        return RequestMostRecommended(
            provider_id=self._provider_pid_to_id(request.provider_id),
            top_n=request.top_n
        )

    def transform_most_recommended_response(self, response: MostRecommended) -> List[MostRecommendedWithPIDs]:
        return [
            MostRecommendedWithPIDs(
                service_id=self._service_id_to_pid(most_recommended_service['service_id']),
                recommendations=most_recommended_service['recommendations']
            )
            for most_recommended_service in response
        ]

    def transform_competitor_recs_request(self, request: RequestRecommendationsAlongYourServicesWithPIDs) \
            -> RequestRecommendationsAlongYourServices:
        return RequestRecommendationsAlongYourServices(
            provider_id=self._provider_pid_to_id(request.provider_id),
            service_id=self._service_pid_to_id(request.service_id) if request.service_id is not None else None,
            top_services_numb=request.top_services_numb,
            top_competitors_numb=request.top_competitors_numb
        )

    def transform_competitors_for_service(self, competitors) \
            -> List[CompetitorRecommendationsWithPIDs]:
        return [
            CompetitorRecommendationsWithPIDs(
                service_id=self._service_id_to_pid(competitor['service_id']),
                recommendations=competitor['recommendations']
            )
            for competitor in competitors
        ]

    def transform_competitor_recs_response(self, response) \
            -> List[RecommendationsAlongYourServicesWithPIDs]:
        return [
            RecommendationsAlongYourServicesWithPIDs(
                service_id=self._service_id_to_pid(your_service['service_id']),
                total_competitor_recommendations=your_service['total_competitor_recommendations'],
                competitors=self.transform_competitors_for_service(your_service['competitors'])
            )
            for your_service in response
        ]

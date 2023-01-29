from fastapi import APIRouter
from health.test_health import service_health_test

router = APIRouter(prefix='/v1')


@router.get(
    "/health",
    summary="Make sure that all needed components are working",
    tags=["health"]
)
def service_health():
    return service_health_test()

from auth.access_token_dependency import verify_access_token
from fastapi import APIRouter, Depends
from health.health_checks import service_health_test

router = APIRouter(prefix='/v1')


@router.get(
    "/health",
    summary="Make sure that all needed components are working",
    tags=["health"]
)
def service_health(dependencies=Depends(verify_access_token)):
    return service_health_test()

from fastapi import APIRouter

from models import UpdateHealthCheckUseCase

router = APIRouter(prefix="/client")


"""
    Receiving IP ADDRESS from queryParam because
    the config from some balancers of charge
    send the IP as the localhost.
"""


@router.get("/health-check", status_code=204)
async def update_health_check(ip_address: str):
    update_use_case = UpdateHealthCheckUseCase(ip_address)
    update_use_case.call()

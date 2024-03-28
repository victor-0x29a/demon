from fastapi import APIRouter, Request, Query
from typing import Annotated

from useCases import UpdateHealthCheckUseCase
from constants import IPV4_REGEX


router = APIRouter(prefix="/client")


"""
    Receiving IP ADDRESS from queryParam because
    the config from some balancers of charge
    send the IP as the localhost.
"""


@router.get("/health-check", status_code=204)
async def update_health_check(request: Request, ip_address: Annotated[str, Query(pattern=IPV4_REGEX)]):
    collection = request.app.database['host']
    update_use_case = UpdateHealthCheckUseCase(collection, ip_address)
    update_use_case.call()

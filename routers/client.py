from fastapi import APIRouter, Request, Query
from typing import Annotated

from use_cases import UpdateHealthCheckUseCase, ViewTaskUseCase
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


@router.get("/current-task", status_code=200)
async def get_current_task(request: Request, ip_address: Annotated[str, Query(pattern=IPV4_REGEX)]):
    collection = request.app.database['host']
    view_task_use_case = ViewTaskUseCase(host_collection=collection, ip_address=ip_address)
    view_task_use_case.call()

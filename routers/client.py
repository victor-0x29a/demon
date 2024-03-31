from fastapi import APIRouter, Request, Query, Body
from typing import Annotated

from use_cases import UpdateHealthCheckUseCase, AddTaskUseCase
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


@router.post("/add-task", status_code=204)
async def add_task(
    request: Request,
    ip_address: Annotated[str, Query(pattern=IPV4_REGEX)],
    task_name: Annotated[str, Body()],
    task_args: Annotated[list[str], Body()]
):
    collection = request.app.database['host']

    add_task_use_case = AddTaskUseCase(
        ip_address=ip_address,
        task_name=task_name,
        task_args=task_args or [],
        host_collection=collection
    )

    add_task_use_case.call()

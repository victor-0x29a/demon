from fastapi import APIRouter, Request, Query, Body
from typing import Annotated

from use_cases import AddTaskUseCase, RemoveTaskUseCase
from models import parse_host
from utils import date_in_range, str_to_date
from constants import IPV4_REGEX, CLIENT_HEALTH_CHECK_LOOP_TIME


router = APIRouter(prefix="/server")


@router.post("/task/add", status_code=204)
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


@router.post("/task/remove", status_code=204)
async def remove_task(
    request: Request,
    ip_address: Annotated[str, Query(pattern=IPV4_REGEX)]
):
    collection = request.app.database["host"]

    remove_task_use_case = RemoveTaskUseCase(
        host_collection=collection,
        ip_address=ip_address
    )

    remove_task_use_case.call()


@router.get("/client/online", status_code=200)
async def get_clients_online(
    request: Request
):
    collection = request.app.database["host"]

    full_clients = collection.find({})

    clients_online = []

    for client in full_clients:
        last_health_check_datetime = str_to_date(client["health_check_datetime"])

        if date_in_range(
            date=last_health_check_datetime,
            max_minute=CLIENT_HEALTH_CHECK_LOOP_TIME
        ):
            clients_online.append(parse_host(client))

    return clients_online

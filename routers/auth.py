from fastapi import APIRouter, Response, Body
from typing import Annotated

from use_cases import AuthenticateUseCase

router = APIRouter(prefix="/auth")


@router.post("/gen", status_code=204)
async def gen_authentication(
    response: Response,
    username: Annotated[str, Body()],
    password: Annotated[str, Body()]
):
    authentication_use_case = AuthenticateUseCase(username, password)

    token = authentication_use_case.call()

    response.headers["Authorization"] = token

    return

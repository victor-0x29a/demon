from fastapi import Header
from typing import Annotated
from fastapi.exceptions import HTTPException
from constants import SECRET
from utils import token_is_valid


async def requires_login(Authorization: Annotated[str, Header()]):
    not_authorized = HTTPException(status_code=401)
    try:
        token = Authorization

        if not token:
            raise not_authorized

        if not token_is_valid(token, SECRET):
            raise not_authorized
    except Exception:
        raise not_authorized

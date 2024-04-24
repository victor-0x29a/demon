from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

from .task import Task


class Host(BaseModel):
    ip_address: str = Field(alias="_id")
    # task = Optional[Field(Task)]
    task: Optional[Task] = Field(default=None)
    health_check_datetime: str = datetime.now().isoformat()


def parse_host(host: Host):
    host.pop("_id")
    return host

from redis_om import JsonModel
from typing import Optional

from .task import Task


class Host(JsonModel):
    ip_address: str
    task: Optional[Task]
    health_check_datetime_string: str
    is_active: int

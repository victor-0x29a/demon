from redis_om import HashModel

from .task import Task


class Host(HashModel):
    ip_address: str
    task: Task
    health_check_datetime_string: str
    is_active: int

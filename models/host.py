from redis_om import HashModel


class Host(HashModel):
    ip_address: str
    current_task_name: str
    current_task_args: str
    health_check_datetime_string: str
    is_active: int

from redis_om import HashModel


class Task(HashModel):
    name: str
    args: str

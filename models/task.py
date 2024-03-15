from redis_om import EmbeddedJsonModel


class Task(EmbeddedJsonModel):
    name: str
    args: str

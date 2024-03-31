from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str = Field()
    args: list[str] = Field()

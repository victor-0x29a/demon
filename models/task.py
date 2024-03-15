from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str = Field()
    args: str = Field()

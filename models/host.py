from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

from .task import Task


class Host(BaseModel):
    ip_address: str = Field(alias="_id")
    task: Task = Optional[Field(Task)]
    health_check_datetime: str = datetime.now().isoformat()

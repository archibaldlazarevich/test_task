from datetime import datetime

from pydantic import BaseModel, Field


class TaskSch(BaseModel):
    id: int
    task_name: str
    task_type: str
    time_add: datetime = Field(default_factory=datetime.now)
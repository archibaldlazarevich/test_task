from datetime import datetime

from pydantic import BaseModel, Field


class TaskSchIn(BaseModel):
    """
    Схема для эндпоинтов по добавлению/обновлению данных
    """

    task_name: str
    task_type: str
    time_add: datetime = Field(default_factory=datetime.now)


class TaskSchOut(TaskSchIn):
    """
    Схема для эндпоинтов по получению данных
    """

    id: int

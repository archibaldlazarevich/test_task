from typing import Any, List, Optional, Sequence, Union

from fastapi import FastAPI, HTTPException

import src.database.func as data_func
from src.app.schemas import TaskSchIn, TaskSchOut
from src.database.models import Task

app: FastAPI = FastAPI()


@app.post("/task/create", response_model=TaskSchIn)
async def create_task(task: TaskSchIn) -> Union[Task, HTTPException]:
    """
    Эндпоинт по добавлению нового задания.

    :param task: TaskSchIn - данные для создания задачи
    :return: Task - созданная задача или HTTPException при ошибке
    """
    data: dict[str, Any] = task.model_dump()
    data["time_add"] = data["time_add"].replace(tzinfo=None)

    result: Optional[Task] = await data_func.create_new_task(data=data)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404,
            detail="Задача не была добавлена, ошибка в исходных данных, "
            "пожалуйста, проверьте введенные данные.",
        )


@app.get("/task/{task_id}", response_model=TaskSchOut)
async def get_task_by_id(task_id: int) -> Union[Task, HTTPException]:
    """
    Эндпоинт по получению задачи по ее id.

    :param task_id: int - ID задачи
    :return: Task - найденная задача или HTTPException если не найдена
    """
    result: Optional[Task] = await data_func.get_task_by_id(task_id=task_id)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Задачи с id = {task_id} не существует. "
            f"Пожалуйста, введите другой id.",
        )


@app.get("/task", response_model=List[TaskSchOut])
async def get_all_task() -> Sequence[Task]:
    """
    Эндпоинт по получению всех задач из БД.

    :return: Список всех задач
    """
    result: Sequence[Task] = await data_func.get_all_task()
    return result


@app.patch("/task/{task_id}", response_model=TaskSchIn)
async def update_task(
    task: TaskSchIn, task_id: int
) -> Union[Task, HTTPException]:
    """
    Эндпоинт по обновлению задачи по ее id.

    :param task: TaskSchIn - новые данные задачи
    :param task_id: int - ID обновляемой задачи
    :return: Обновленная задача или HTTPException, если задача не найдена
    """
    data: dict[str, Any] = task.model_dump()
    if data.get("time_add"):
        data["time_add"] = data["time_add"].replace(tzinfo=None)
    result: Optional[Task] = await data_func.update_task(
        task_id=task_id, data=data
    )

    if result:
        return result
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Задачи с id = {task_id} не существует. "
            f"Пожалуйста, введите другой id.",
        )


@app.delete("/task/{task_id}", response_model=TaskSchOut)
async def delete_task(task_id: int) -> Union[Task, HTTPException]:
    """
    Эндпоинт по удалению задачи по ее id.

    :param task_id: int - ID удаляемой задачи
    :return: Удаленная задача или HTTPException, если задача не найдена
    """
    result: Optional[Task] = await data_func.delete_task(task_id=task_id)

    if result:
        return result
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Задачи с id = {task_id} не существует."
            f" Пожалуйста, введите другой id.",
        )

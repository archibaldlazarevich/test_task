from typing import Any, Sequence, List

from fastapi import FastAPI, HTTPException
from src.app.schemas import TaskSch
from src.database.models import Task

import src.database.func as data_func

app = FastAPI()

@app.post('/task/create', response_model=TaskSch)
async def create_task(task: TaskSch):
    """
    Эндпоинт по добавлению нового задания
    :return:
    """
    data: dict[str, Any] = task.model_dump()
    data['time_add'] = data['time_add'].replace(tzinfo=None)

    result: Task | None = await data_func.create_new_task(data = data)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f'Задача не была добавлена, ошибка в исходных данных, пожалуйста, проверьте введенные данные.')



@app.get('/task/{task_id}', response_model=TaskSch)
async def get_task_by_id(task_id: int):
    """
    Эндпоинт по получению задачи по ее id
    :return:
    """
    result: Task | None = await data_func.get_task_by_id(task_id= task_id)
    print(1)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f'Задачи с id = {task_id} не существует. Пожалуйста, введите другой id.')


@app.get('/task', response_model=List[TaskSch])
async def get_all_task():
    """
    Эндпоинт по получению всех задач из бд
    :return:
    """
    result: Sequence[List] = await data_func.get_all_task()

    return result

@app.patch('/task/{task_id}', response_model=TaskSch)
async def update_task(task: TaskSch, task_id: int):
    """
    Эндпоинт по обновлению задачи по ее id
    :return:
    """
    data: dict[str, Any] = task.model_dump()
    if data.get('time_add'):
        data['time_add'] = data['time_add'].replace(tzinfo=None)
    result: Task | None = await data_func.update_task(task_id=task_id, data= data)

    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail=f'Задачи с id = {task_id} не существует. Пожалуйста, введите другой id.')


@app.delete('/task/{task_id}', response_model=TaskSch)
async def delete_task(task_id: int):
    """
    Эндпоинт по удалению задачи по ее id
    :return:
    """
    result: Task | None = await data_func.delete_task(task_id=task_id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404,
                            detail=f'Задачи с id = {task_id} не существует. Пожалуйста, введите другой id.')
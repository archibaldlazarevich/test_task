from sqlalchemy import select, insert, update, delete
from typing import Sequence, List

from src.database.models import Task
from src.database.create_db import get_db_session


async def get_all_task() -> Sequence[List]:
    """
    Метод который возвращает список всех задач
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(select(Task).order_by(Task.id))
        result = result_data.scalars().all()
    return result


async def get_task_by_id(task_id: int) -> None | Task:
    """
    Метод, который возвращает задачу по ее id
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(select(Task).where(Task.id == task_id))
        result = result_data.scalar_one_or_none()
    return result


async def create_new_task(data: dict) -> None | Task:
    """
    Метод для создания новой задачи
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(insert(Task).values(**data).returning(Task))
        result = result_data.scalar_one_or_none()
        await session.commit()
    return result


async def update_task(task_id: int, data: dict) -> None | Task:
    """
    Метод для обновления задачи
    :param task_id:
    :param data:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(update(Task).where(Task.id == task_id).values(**data).returning(Task))
        result = result_data.scalar_one_or_none()
        await session.commit()
    return result


async def delete_task(task_id: int) -> None | Task:
    """
    Метод для удаления задачи
    :param task_id:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(delete(Task).where(Task.id == task_id).returning(Task))
        result = result_data.scalar_one_or_none()
        await session.commit()
    return result
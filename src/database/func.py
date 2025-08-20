from typing import Optional, Sequence

from sqlalchemy import delete, insert, select, update

from src.database.create_db import get_db_session
from src.database.models import Task


async def get_all_task() -> Sequence[Task]:
    """
    Метод который возвращает список всех задач

    :return: Список объектов Task
    """
    async with get_db_session() as session:
        result_data = await session.execute(select(Task).order_by(Task.id))
        result: Sequence[Task] = result_data.scalars().all()
    return result


async def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Метод, который возвращает задачу по ее id

    :param task_id: ID задачи
    :return: Объект Task или None, если задача не найдена
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(Task).where(Task.id == task_id)
        )
        result: Optional[Task] = result_data.scalar_one_or_none()
    return result


async def create_new_task(data: dict[str, object]) -> Optional[Task]:
    """
    Метод для создания новой задачи

    :param data: Словарь с данными для создания задачи
    :return: Созданный объект Task либо None
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            insert(Task).values(**data).returning(Task)
        )
        result: Optional[Task] = result_data.scalar_one_or_none()
        await session.commit()
    return result


async def update_task(task_id: int, data: dict[str, object]) -> Optional[Task]:
    """
    Метод для обновления задачи

    :param task_id: ID задачи для обновления
    :param data: Словарь с новыми данными задачи
    :return: Обновленный объект Task либо None
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(**data)
            .returning(Task)
        )
        result: Optional[Task] = result_data.scalar_one_or_none()
        await session.commit()
    return result


async def delete_task(task_id: int) -> Optional[Task]:
    """
    Метод для удаления задачи

    :param task_id: ID задачи для удаления
    :return: Удалённый объект Task либо None
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            delete(Task).where(Task.id == task_id).returning(Task)
        )
        result: Optional[Task] = result_data.scalar_one_or_none()
        await session.commit()
    return result

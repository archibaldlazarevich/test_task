from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def naive_now():
    return datetime.now().replace(tzinfo=None)

class Task(Base):
    """
    Модель для создания таблицы для задач
    """
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column(String, nullable= False)
    time_add: Mapped[datetime] = mapped_column(
        DateTime, default=naive_now
    )
    task_type: Mapped[str] = mapped_column(String(length=20), nullable=False)

    def to_json(self, names: list):
        """ Метод для преобразования экземпляра класса в json-словарь"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in names}

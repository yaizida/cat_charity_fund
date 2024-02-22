from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Таким  обрзаром мы назавем имя таблицы
        # именем модели в нижнем регистре
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


# Асинхроный генератор сессий.
async def get_async_session():
    # Через асинхронный котекстный менеджер и sessionmaker
    # открыывается сессия.
    async with AsyncSessionLocal() as async_session:
        yield async_session
        # Когда HTTP-запрос отработает - выолнение кода вернется сюдя,
        # и при выходн из контекстоного менеджера сессия будет закрта.
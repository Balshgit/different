from typing import Any, Tuple, Union, Type

from sqlalchemy_study.sqlalchemy import Table, Column, Integer, DATETIME, TIMESTAMP, func
from sqlalchemy_study.sqlalchemy import as_declarative

from db.meta import meta
from settings import settings

DB_TIME_FORMAT: Type[Union[DATETIME, TIMESTAMP]] = DATETIME if settings.USE_DATABASE == 'mysql' else TIMESTAMP


@as_declarative(metadata=meta)
class BaseModel:
    """
    BaseModel for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    __tablename__: str
    __table__: Table
    __table_args__: Tuple[Any, ...]
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(DB_TIME_FORMAT, default=func.now(), index=True)
    updated_at = Column(DB_TIME_FORMAT, nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id!r})>"

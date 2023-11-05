from datetime import datetime
from typing import Type, Union

from sqlalchemy import DATETIME, INTEGER, TIMESTAMP, Table, func
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column

from db.meta import meta
from settings import settings

DB_TIME_FORMAT: Type[Union[DATETIME, TIMESTAMP]] = DATETIME if settings.USE_DATABASE == "mysql" else TIMESTAMP


@as_declarative(metadata=meta)
class BaseModel:
    """
    Base for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    __table__: Table
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        "id",
        INTEGER(),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column("created_at", DB_TIME_FORMAT, default=func.now(), index=True)
    updated_at: Mapped[datetime | None] = mapped_column("updated_at", DB_TIME_FORMAT, nullable=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id!r})>"

from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEAN, Integer

from db.base import BaseModel


class Coin(BaseModel):
    """Model for coin."""

    __tablename__ = "coins"

    name: Mapped[str] = mapped_column("coin_name", VARCHAR(50), unique=True)
    enabled: Mapped[bool] = mapped_column("enabled", BOOLEAN, default=True)

    coin_type_id = relationship(
        "CoinType",
        primaryjoin="Coin.id == CoinType.coin_id",
        back_populates="coin",
        uselist=False,
        viewonly=True,
        lazy="raise",
    )
    employee = relationship("Employee", back_populates="coin")


class CoinType(BaseModel):
    """Model for coin type."""

    __tablename__ = "coin_types"

    name: Mapped[str] = mapped_column("coin_name", VARCHAR(50))
    coin_id: Mapped[int] = mapped_column(Integer, ForeignKey("coins.id", ondelete="CASCADE"))
    coin = relationship(Coin, back_populates="coin_type_id")

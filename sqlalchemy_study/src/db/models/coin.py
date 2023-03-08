from sqlalchemy_study.sqlalchemy import VARCHAR
from sqlalchemy_study.sqlalchemy import relationship
from sqlalchemy_study.sqlalchemy import Column
from sqlalchemy_study.sqlalchemy import ForeignKey
from sqlalchemy_study.sqlalchemy import Integer, BOOLEAN

from db.base import BaseModel


class Coin(BaseModel):
    """Model for coin."""

    __tablename__ = "coins"

    name = Column('coin_name', VARCHAR(50), unique=True)
    enabled = Column('enabled', BOOLEAN)

    coin_type_id = relationship("CoinType",
                                primaryjoin="Coin.id == CoinType.coin_id",
                                back_populates='coin',
                                uselist=False,
                                viewonly=True,
                                lazy="raise",
                                )
    employee = relationship('Employee', back_populates='coin')


class CoinType(BaseModel):
    """Model for coin type."""

    __tablename__ = "coin_types"

    name = Column('coin_name', VARCHAR(50))
    coin_id = Column(Integer, ForeignKey('coins.id', ondelete='CASCADE'))
    coin = relationship(Coin, back_populates='coin_type_id')

from datetime import datetime

from sqlalchemy import VARCHAR, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel
from db.models.coin import Coin


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=True)
    hash_password: Mapped[str] = mapped_column(String(255))
    auth_token: Mapped[str] = mapped_column(String(255))
    last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    def __repr__(self) -> str:
        return f"User: id:{self.id}, name: {self.username}"

    employee = relationship(
        "Employee",
        primaryjoin="foreign(User.id)==remote(Employee.id)",
        lazy="noload",
        backref="user_employee",
    )


class Employee(BaseModel):
    __tablename__ = "employees"

    first_name: Mapped[str] = mapped_column("first_name", VARCHAR(128), nullable=False)
    last_name: Mapped[str] = mapped_column("last_name", VARCHAR(128), nullable=False)
    phone: Mapped[str | None] = mapped_column("phone", VARCHAR(30), unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column("description", VARCHAR(255), nullable=True)
    coin_id: Mapped[int | None] = mapped_column("coin_id", ForeignKey("coins.id", ondelete="SET NULL"), nullable=True)

    coin = relationship(
        Coin,
        back_populates="employee",
        primaryjoin="Employee.coin_id==Coin.id",
        lazy="noload",
        uselist=False,
    )

    skills = relationship(
        "Skill",
        secondary="employees_skills",
        lazy="noload",
        uselist=True,
    )

    department = relationship(
        "EmployeeDepartments",
        lazy="noload",
        backref="employee",
        uselist=False,
    )

    user = relationship(
        "User",
        primaryjoin="foreign(Employee.id)==remote(User.id)",
        lazy="raise",
        backref="user_employee",
    )

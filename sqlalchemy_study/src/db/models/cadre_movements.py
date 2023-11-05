from sqlalchemy import VARCHAR, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel
from db.models.department import Department


class CadreMovement(BaseModel):
    __tablename__ = "cadre_movements"

    employee: Mapped[int] = mapped_column(
        Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True
    )
    old_department: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    new_department: Mapped[int] = mapped_column(
        Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reason: Mapped[str | None] = mapped_column(VARCHAR(500), nullable=True)

    department = relationship(Department, foreign_keys=new_department, lazy="select")

from sqlalchemy import VARCHAR, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import BaseModel
from db.models.user import Employee


class Skill(BaseModel):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column("name", VARCHAR(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column("description", Text, nullable=True)


class EmployeesSkills(BaseModel):
    __tablename__ = "employees_skills"
    __table_args__ = (UniqueConstraint("employee_id", "skill_id"),)

    employee_id: Mapped[int] = mapped_column(ForeignKey(Employee.id, ondelete="CASCADE"), nullable=False, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey(Skill.id, ondelete="CASCADE"), nullable=False, index=True)

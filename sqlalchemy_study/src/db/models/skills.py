from sqlalchemy_study.sqlalchemy import Column, ForeignKey, VARCHAR, Text, UniqueConstraint

from db.base import BaseModel
from db.models.user import Employee


class Skill(BaseModel):
    __tablename__ = 'skills'

    name = Column(VARCHAR(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)


class EmployeesSkills(BaseModel):
    __tablename__ = 'employees_skills'
    __table_args__ = (UniqueConstraint("employee_id", "skill_id"),)

    employee_id = Column(ForeignKey(Employee.id, ondelete='CASCADE'), nullable=False, index=True)
    skill_id = Column(ForeignKey(Skill.id, ondelete='CASCADE'), nullable=False, index=True)

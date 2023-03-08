import datetime

from sqlalchemy_study.sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy_study.sqlalchemy import VARCHAR
from sqlalchemy_study.sqlalchemy import relationship

from db.base import BaseModel
from db.models.coin import Coin


class User(BaseModel):
    __tablename__ = 'users'

    username: str = Column(String(255), unique=True)
    email: str = Column(String(255), index=True, unique=True, nullable=True)
    hash_password: str = Column(String(255))
    auth_token: str = Column(String(255))
    last_login: datetime.datetime = Column(DateTime, default=datetime.datetime.now, index=True)

    def __repr__(self):
        return f'User: id:{self.id}, name: {self.username}'

    employee = relationship('Employee',
                            primaryjoin='foreign(User.id)==remote(Employee.id)',
                            lazy='noload',
                            backref='user_employee',
                            )
    
    
class Employee(BaseModel):
    __tablename__ = 'employees'

    first_name = Column(VARCHAR(128), nullable=False)
    last_name = Column(VARCHAR(128), nullable=False)
    phone = Column(VARCHAR(30), unique=True, nullable=True)
    description = Column(VARCHAR(255), nullable=True)
    coin_id = Column('coin_id', ForeignKey('coins.id', ondelete='SET NULL'), nullable=True)

    coin = relationship(Coin,
                        back_populates='employee',
                        primaryjoin='Employee.coin_id==Coin.id',
                        lazy='noload',
                        uselist=False,
                        )

    skills = relationship('Skill',
                          secondary="employees_skills",
                          lazy='noload',
                          uselist=True,
                          )

    department = relationship('EmployeeDepartments',
                              lazy='noload',
                              backref='employee',
                              uselist=False,
                              )

    user = relationship('User',
                        primaryjoin='foreign(Employee.id)==remote(User.id)',
                        lazy='raise',
                        backref='user_employee',
                        )

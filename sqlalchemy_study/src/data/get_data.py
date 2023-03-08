import asyncio

from settings.logger import logger
from sqlalchemy_study.sqlalchemy import select
from sqlalchemy_study.sqlalchemy import load_only, contains_eager, joinedload

from db.dependencies import get_async_db_session
from db.models.coin import Coin
from db.models.department import EmployeeDepartments, Department
from db.models.skills import Skill
from db.models.user import Employee, User


async def get_data() -> list[Employee]:

    query = (
        select(Employee)
        .join(Employee.coin).options(
            contains_eager(Employee.coin).options(load_only(Coin.name,
                                                            Coin.enabled)))
        .join(Employee.skills).options(
            contains_eager(Employee.skills).load_only(Skill.name)
        ).options(load_only(Employee.id,
                            Employee.first_name,
                            Employee.phone,
                            )
                  )
        .outerjoin(Employee.department).options(
            contains_eager(Employee.department).options(
                joinedload(EmployeeDepartments.department)
                .options(load_only(Department.name,
                                   Department.description, )
                         )
            )
        )
        .outerjoin(Employee.user).options(
            contains_eager(Employee.user).options(load_only(User.username,
                                                            )
                                                  )
        )
    ).order_by(Employee.id, Skill.name)

    async with get_async_db_session() as session:
        result = await session.execute(query)
        data = result.unique().scalars().all()
        return data

employees = asyncio.run(get_data())


for employee in employees:
    print(''.center(40, '-'), '\nEmployee id: {0}\nFirst name: {1}\nPhone: {2}\nSkills: {3}\n'
          'Coin name: {4}\nCoin enabled: {5}\nDepartment: {6} -> {7}\nUsername: {8}'
          .format(employee.id,
                  employee.first_name,
                  employee.phone,
                  ', '.join([skill.name for skill in employee.skills[:5]]),
                  employee.coin.name,
                  employee.coin.enabled,
                  employee.department.department.name,
                  employee.department.department.description,
                  employee.user.username if hasattr(employee.user, 'username') else None,
                  )
          )

logger.info(f'Total employees: {len(employees)}')

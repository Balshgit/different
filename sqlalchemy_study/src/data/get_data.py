import asyncio

from sqlalchemy import select
from sqlalchemy.orm import contains_eager, joinedload, load_only

from db.dependencies import get_async_db_session
from db.models.coin import Coin
from db.models.department import Department, EmployeeDepartments
from db.models.skills import Skill
from db.models.user import Employee, User
from settings.logger import logger


async def get_data() -> list[Employee]:
    query = (
        select(Employee)
        .join(Employee.coin)
        .options(contains_eager(Employee.coin).options(load_only(Coin.name, Coin.enabled)))
        .join(Employee.skills)
        .options(contains_eager(Employee.skills).load_only(Skill.name))
        .options(
            load_only(
                Employee.id,
                Employee.first_name,
                Employee.phone,
            )
        )
        .outerjoin(Employee.department)
        .options(
            contains_eager(Employee.department).options(
                joinedload(EmployeeDepartments.department).options(
                    load_only(
                        Department.name,
                        Department.description,
                    )
                )
            )
        )
        .outerjoin(Employee.user)
        .options(
            contains_eager(Employee.user).options(
                load_only(
                    User.username,
                )
            )
        )
    ).order_by(Employee.id, Skill.name)

    async with get_async_db_session() as session:
        result = await session.execute(query)
        return result.unique().scalars().all()


employees = asyncio.run(get_data())


for employee in employees:
    print(
        "".center(40, "-"),
        "\nEmployee id: {id}\nFirst name: {first_name}\nPhone: {phone}\nSkills: {skills}\n"
        "Coin name: {coin_name}\nCoin enabled: {coin_enabled}\nDepartment: {department_name} -> "
        "{department_description}\nUsername: {user_username}".format(
            id=employee.id,
            first_name=employee.first_name,
            phone=employee.phone,
            skills=", ".join([skill.name for skill in employee.skills[:5]]),
            coin_name=employee.coin.name,
            coin_enabled=employee.coin.enabled,
            department_name=employee.department.department.name,
            department_description=employee.department.department.description,
            user_username=employee.user.username if hasattr(employee.user, "username") else None,
        ),
    )

logger.info(f"Total employees: {len(employees)}")

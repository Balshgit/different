import asyncio
import random
import uuid

from factory import fuzzy
from faker import Faker

from data.factories import (
    CoinModelFactory,
    DepartmentFactory,
    EmployeeDepartmentFactory,
    EmployeeFactory,
    EmployeesSkillsFactory,
    SkillFactory,
    UserFactory,
)
from db.dependencies import get_async_db_session
from db.models.user import User
from settings.logger import logger

faker = Faker("ru_RU")


async def add_users_data() -> None:
    async with get_async_db_session() as session:
        users = [
            User(
                username=faker.profile(fields=["username"])["username"],
                hash_password=faker.password(),
                auth_token=str(uuid.uuid4()),
            )
            for _ in range(10)
        ]

        session.add_all(users)


def get_random_skill(skills: list[int]) -> list[int]:
    return random.sample(skills, random.randint(2, 9))  # noqa: S311


def fill_database() -> None:
    # async add faker data
    asyncio.run(add_users_data())

    # sync factory boy add data
    coins = [coin.id for coin in CoinModelFactory.create_batch(42)]

    jonny = EmployeeFactory(first_name="Tony", last_name="Stark", coin_id=fuzzy.FuzzyChoice(coins))
    karl = EmployeeFactory(first_name="Karl", coin_id=fuzzy.FuzzyChoice(coins))
    employees = EmployeeFactory.create_batch(40, coin_id=fuzzy.FuzzyChoice(coins))

    skills = [skill.id for skill in SkillFactory.create_batch(size=faker.random_int(min=20, max=42))]

    for skill in get_random_skill(skills):
        EmployeesSkillsFactory(employee_id=jonny.id, skill_id=skill)

    for skill in get_random_skill(skills):
        EmployeesSkillsFactory(employee_id=karl.id, skill_id=skill)

    for employee in employees:
        for skill in get_random_skill(skills):
            EmployeesSkillsFactory(employee_id=employee.id, skill_id=skill)

    # User data (first 20 rows if not exists)
    for user_id in range(20, 30):
        UserFactory(id=user_id, username=faker.profile(fields=["username"])["username"])

    # Department data
    departments = DepartmentFactory.create_batch(5)
    departments = [department.id for department in departments]

    for employee in [jonny, karl, *employees]:
        EmployeeDepartmentFactory(employee_id=employee.id, department_id=fuzzy.FuzzyChoice(departments))

    logger.info("All data has been created. You can run data/get_data.py script")

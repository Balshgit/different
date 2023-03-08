from datetime import datetime, timedelta
from typing import Optional

import factory
from factory import fuzzy
from faker import Faker

from db.dependencies import get_sync_db_session
from db.models.coin import Coin, CoinType
from db.models.department import Department, EmployeeDepartments
from db.models.skills import Skill, EmployeesSkills
from db.models.user import User, Employee

faker = Faker('ru_RU')


Session = get_sync_db_session()


class BaseModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_session = Session


class UserFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    username = faker.profile(fields=['username'])['username']
    email = factory.Faker('email')
    hash_password = factory.Faker('password')
    auth_token = factory.Faker('uuid4')

    class Meta:
        model = User
        sqlalchemy_get_or_create = (
            'username',
            )


class CoinModelFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('cryptocurrency_name')
    enabled = fuzzy.FuzzyChoice((0, 1))

    class Meta:
        model = Coin
        sqlalchemy_get_or_create = (
            'name',
        )

    @factory.post_generation
    def coin_type(obj, create: bool, extracted: Optional[Coin], *args, **kwargs) -> None:
        if create:
            CoinTypeFactory.create_batch(faker.random_int(min=3, max=7), coin_id=obj.id)


class CoinTypeFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('cryptocurrency_code')

    class Meta:
        model = CoinType
        sqlalchemy_get_or_create = ('id',
                                    )


class SkillFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('job', locale='ru_ru')
    description = factory.Faker('text', max_nb_chars=160, locale='ru_RU')
    updated_at = factory.LazyFunction(datetime.now)

    class Meta:
        model = Skill
        sqlalchemy_get_or_create = ('name',
                                    )


class EmployeeFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    phone = factory.Faker('phone_number')
    description = factory.Faker('text', max_nb_chars=80, locale='ru_RU')
    coin_id = factory.Faker('random_int')

    class Meta:
        model = Employee
        sqlalchemy_get_or_create = ('id',
                                    )


class EmployeesSkillsFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    employee_id = factory.Faker('random_int')
    skill_id = factory.Faker('random_int')
    updated_at = factory.Faker(
        'date_time_between_dates', datetime_start=datetime.now() - timedelta(days=30), datetime_end=datetime.now()
    )

    class Meta:
        model = EmployeesSkills
        sqlalchemy_get_or_create = (
            'id',
            'employee_id',
            'skill_id'
        )


class DepartmentFactory(BaseModelFactory):

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('company')
    description = factory.Faker('bs')
    updated_at = factory.Faker(
        'date_time_between_dates', datetime_start=datetime.now() - timedelta(days=30), datetime_end=datetime.now()
    )

    class Meta:
        model = Department
        sqlalchemy_get_or_create = (
            'id',
            'name',
        )


class EmployeeDepartmentFactory(BaseModelFactory):

    employee_id = factory.Faker('random_int')
    department_id = factory.Faker('random_int')
    created_at = factory.Faker(
        'date_time_between_dates',
        datetime_start=datetime.now() - timedelta(days=30),
        datetime_end=datetime.now() - timedelta(days=10)
    )
    updated_at = factory.Faker(
        'date_time_between_dates',
        datetime_start=datetime.now() - timedelta(days=10),
        datetime_end=datetime.now()
    )

    class Meta:
        model = EmployeeDepartments

"""postgres init migrations

Revision ID: postgres_init_migrations
Revises:
Create Date: 2022-06-14 00:29:28.932954

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "postgres_init_migrations"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "coins",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("coin_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("enabled", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("coin_name"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_coins_created_at"), "coins", ["created_at"], unique=False)
    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("description", sa.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_departments_created_at"), "departments", ["created_at"], unique=False)
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_skills_created_at"), "skills", ["created_at"], unique=False)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("hash_password", sa.String(length=255), nullable=True),
        sa.Column("auth_token", sa.String(length=255), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_last_login"), "users", ["last_login"], unique=False)
    op.create_table(
        "coin_types",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("coin_name", sa.VARCHAR(length=50), nullable=True),
        sa.Column("coin_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["coin_id"], ["coins.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_coin_types_created_at"), "coin_types", ["created_at"], unique=False)
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("first_name", mysql.VARCHAR(length=128), nullable=False),
        sa.Column("last_name", mysql.VARCHAR(length=128), nullable=False),
        sa.Column("phone", mysql.VARCHAR(length=30), nullable=True),
        sa.Column("description", mysql.VARCHAR(length=255), nullable=True),
        sa.Column("coin_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["coin_id"], ["coins.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("phone"),
    )
    op.create_index(op.f("ix_employees_created_at"), "employees", ["created_at"], unique=False)
    op.create_table(
        "cadre_movements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("employee", sa.Integer(), nullable=False),
        sa.Column("old_department", sa.Integer(), nullable=False),
        sa.Column("new_department", sa.Integer(), nullable=False),
        sa.Column("reason", sa.VARCHAR(length=500), nullable=True),
        sa.ForeignKeyConstraint(["employee"], ["employees.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["new_department"], ["departments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["old_department"], ["departments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_cadre_movements_created_at"), "cadre_movements", ["created_at"], unique=False)
    op.create_index(op.f("ix_cadre_movements_employee"), "cadre_movements", ["employee"], unique=False)
    op.create_index(op.f("ix_cadre_movements_new_department"), "cadre_movements", ["new_department"], unique=False)
    op.create_index(op.f("ix_cadre_movements_old_department"), "cadre_movements", ["old_department"], unique=False)
    op.create_table(
        "employee_departments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_employee_departments_created_at"), "employee_departments", ["created_at"], unique=False)
    op.create_index(
        op.f("ix_employee_departments_department_id"), "employee_departments", ["department_id"], unique=False
    )
    op.create_index(op.f("ix_employee_departments_employee_id"), "employee_departments", ["employee_id"], unique=False)
    op.create_table(
        "employees_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_id"], ["skills.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("employee_id", "skill_id"),
        sa.UniqueConstraint("id"),
    )
    op.create_index(op.f("ix_employees_skills_created_at"), "employees_skills", ["created_at"], unique=False)
    op.create_index(op.f("ix_employees_skills_employee_id"), "employees_skills", ["employee_id"], unique=False)
    op.create_index(op.f("ix_employees_skills_skill_id"), "employees_skills", ["skill_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_employees_skills_skill_id"), table_name="employees_skills")
    op.drop_index(op.f("ix_employees_skills_employee_id"), table_name="employees_skills")
    op.drop_index(op.f("ix_employees_skills_created_at"), table_name="employees_skills")
    op.drop_table("employees_skills")
    op.drop_index(op.f("ix_employee_departments_employee_id"), table_name="employee_departments")
    op.drop_index(op.f("ix_employee_departments_department_id"), table_name="employee_departments")
    op.drop_index(op.f("ix_employee_departments_created_at"), table_name="employee_departments")
    op.drop_table("employee_departments")
    op.drop_index(op.f("ix_cadre_movements_old_department"), table_name="cadre_movements")
    op.drop_index(op.f("ix_cadre_movements_new_department"), table_name="cadre_movements")
    op.drop_index(op.f("ix_cadre_movements_employee"), table_name="cadre_movements")
    op.drop_index(op.f("ix_cadre_movements_created_at"), table_name="cadre_movements")
    op.drop_table("cadre_movements")
    op.drop_index(op.f("ix_employees_created_at"), table_name="employees")
    op.drop_table("employees")
    op.drop_index(op.f("ix_coin_types_created_at"), table_name="coin_types")
    op.drop_table("coin_types")
    op.drop_index(op.f("ix_users_last_login"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_skills_created_at"), table_name="skills")
    op.drop_table("skills")
    op.drop_index(op.f("ix_departments_created_at"), table_name="departments")
    op.drop_table("departments")
    op.drop_index(op.f("ix_coins_created_at"), table_name="coins")
    op.drop_table("coins")
    # ### end Alembic commands ###

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from src.database import engine, User, Problem, Role


class RoleAdmin(ModelView, model=Role):
    icon = "fa-solid fa-lock"
    column_list = [Role.id, Role.name, Role.permissions]
    column_details_list = column_list
    form_columns = column_list


class UserAdmin(ModelView, model=User):
    icon = "fa-solid fa-user"
    column_list = [
        User.id,
        User.username,
        User.password,
        User.role_id,
        User.rating,
        User.registered_at,
    ]
    column_details_list = column_list
    form_columns = column_list
    column_searchable_list = [User.username]
    column_sortable_list = [User.username, User.rating, User.registered_at]


class ProblemAdmin(ModelView, model=Problem):
    icon = "fa-solid fa-list-check"
    column_list = [
        Problem.id,
        Problem.author_id,
        Problem.title,
        Problem.statement,
        Problem.tests,
        Problem.difficulty,
        Problem.is_in_contest,
        Problem.created_at,
        Problem.updated_at,
    ]
    column_details_list = column_list
    form_columns = column_list
    column_searchable_list = [Problem.title, Problem.statement]
    column_sortable_list = [
        Problem.title,
        Problem.difficulty,
        Problem.is_in_contest,
        Problem.created_at,
        Problem.updated_at,
    ]


def get_admin(app: FastAPI) -> Admin:
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(ProblemAdmin)
    admin.add_view(RoleAdmin)
    return admin

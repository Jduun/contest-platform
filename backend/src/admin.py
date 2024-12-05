from datetime import timedelta
from typing import Any

import jwt
from fastapi import FastAPI, Request
from jwt.exceptions import InvalidTokenError
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from wtforms import TextAreaField

import src.auth.service as auth_service
from src.auth.exceptions import CredentialsError
from src.auth.roles import Roles
from src.auth.schemas import UserLogin
from src.config import settings
from src.database import (
    Contest,
    ContestProblem,
    ContestUser,
    Problem,
    Role,
    Submission,
    User,
    async_session,
    engine,
)


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)
        self.permitted_roles = [Roles.admin, Roles.organizer]

    async def login(self, request: Request) -> bool:
        async with async_session() as db_session:
            form = await request.form()
            username, password = form["username"], form["password"]
            try:
                user = await auth_service.authenticate(
                    db_session, UserLogin(username=username, password=password)
                )
                if user.role.name not in self.permitted_roles:
                    return False
            except CredentialsError:
                return False
            access_token = auth_service.create_access_token(
                token_data={
                    "username": user.username,
                    "role": user.role.name,
                },
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
            request.session.update({"token": access_token})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    # Will be called for validating each incoming request.
    async def authenticate(self, request: Request) -> bool:
        async with async_session() as db_session:
            token = request.session.get("token")
            if not token:
                return False
            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
                )
            except InvalidTokenError:
                return False
            username = payload.get("username")
            user = await auth_service.get_user_by_username(db_session, username)
            if user is None:
                return False
            return True


def get_role_from_request(request: Request):
    token = request.session.get("token")
    if not token:
        return None
    try:
        payload = auth_service.get_token_payload(token)
    except InvalidTokenError:
        return None
    role = payload.get("role")
    if not role:
        return None
    return role


class RoleAdmin(ModelView, model=Role):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin]:
            return False

        self.can_view_details = role in [Roles.admin]
        self.can_create = role in [Roles.admin]
        self.can_edit = role in [Roles.admin]
        self.can_delete = role in [Roles.admin]
        self.can_export = role in [Roles.admin]

        return True

    icon = "fa-solid fa-lock"
    column_list = [Role.id, Role.name]
    column_details_list = column_list
    form_columns = column_list


class UserAdmin(ModelView, model=User):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin]:
            return False

        self.can_view_details = role in [Roles.admin]
        self.can_create = role in [Roles.admin]
        self.can_edit = role in [Roles.admin]
        self.can_delete = role in [Roles.admin]
        self.can_export = role in [Roles.admin]

        return True

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        password = data.get("password")
        if password:
            data["password"] = auth_service.get_password_hash(password)

    icon = "fa-solid fa-user"
    column_list = [
        User.id,
        User.username,
        User.password,
        User.registered_at,
        User.role,
    ]
    form_include_pk = True
    column_details_list = [
        User.username,
        User.password,
        User.role,
    ]
    form_columns = column_details_list
    column_searchable_list = [User.username]
    column_sortable_list = [User.username, User.registered_at]


class ProblemAdmin(ModelView, model=Problem):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin, Roles.organizer]:
            return False

        self.can_view_details = role in [Roles.admin, Roles.organizer]
        self.can_create = role in [Roles.admin, Roles.organizer]
        self.can_edit = role in [Roles.admin, Roles.organizer]
        self.can_delete = role in [Roles.admin, Roles.organizer]
        self.can_export = role in [Roles.admin, Roles.organizer]

        return True

    icon = "fa-solid fa-puzzle-piece"
    column_list = [
        Problem.id,
        Problem.author,
        Problem.title,
        Problem.statement,
        Problem.tests,
        Problem.difficulty,
        Problem.memory_limit,
        Problem.time_limit,
        Problem.is_public,
        Problem.created_at,
        Problem.updated_at,
    ]
    column_details_list = column_list
    form_columns = [
        Problem.id,
        Problem.title,
        Problem.statement,
        Problem.tests,
        Problem.difficulty,
        Problem.memory_limit,
        Problem.time_limit,
        Problem.is_public,
    ]
    column_searchable_list = [Problem.title, Problem.statement]
    column_sortable_list = [
        Problem.title,
        Problem.difficulty,
        Problem.is_public,
        Problem.created_at,
        Problem.updated_at,
    ]
    form_overrides = {
        "statement": TextAreaField,
        "tests": TextAreaField,
    }
    column_formatters = {
        Problem.statement: lambda m, a: m.statement[:20],
        Problem.tests: lambda m, a: m.tests[:20],
    }
    create_template = "custom_create.html"
    edit_template = "custom_edit.html"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        async with async_session() as db_session:
            if is_created:
                token = request.session.get("token")
                try:
                    payload = auth_service.get_token_payload(token)
                except InvalidTokenError:
                    return None
                username = payload.get("username")
                user = await auth_service.get_user_by_username(db_session, username)
                data["author_id"] = user.id


class ContestAdmin(ModelView, model=Contest):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin, Roles.organizer]:
            return False

        self.can_view_details = role in [Roles.admin, Roles.organizer]
        self.can_create = role in [Roles.admin, Roles.organizer]
        self.can_edit = role in [Roles.admin, Roles.organizer]
        self.can_delete = role in [Roles.admin, Roles.organizer]
        self.can_export = role in [Roles.admin, Roles.organizer]

        return True

    icon = "fa-solid fa-trophy"
    column_list = [
        Contest.id,
        Contest.name,
        Contest.start_time,
        Contest.end_time,
        Contest.created_at,
        Contest.updated_at,
    ]
    column_details_list = column_list
    form_columns = [
        Contest.id,
        Contest.name,
        Contest.start_time,
        Contest.end_time,
    ]
    column_searchable_list = [Contest.name]
    column_sortable_list = [
        Contest.name,
        Contest.start_time,
        Contest.end_time,
        Contest.created_at,
        Contest.updated_at,
    ]


class SubmissionAdmin(ModelView, model=Submission):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin, Roles.organizer]:
            return False

        self.can_view_details = role in [Roles.admin, Roles.organizer]
        self.can_create = role in [Roles.admin]
        self.can_edit = role in [Roles.admin]
        self.can_delete = role in [Roles.admin]
        self.can_export = role in [Roles.admin, Roles.organizer]

        return True

    icon = "fa-solid fa-paper-plane"
    column_list = [
        Submission.id,
        Submission.code,
        Submission.language_id,
        Submission.status,
        Submission.stderr,
        Submission.user,
        Submission.problem,
        Submission.submitted_at,
    ]

    column_details_list = column_list
    form_columns = column_list
    column_searchable_list = [
        Submission.user_id,
        Submission.problem_id,
    ]
    column_sortable_list = [Submission.submitted_at]
    column_formatters = {Submission.code: lambda m, a: m.code[:20]}


class ContestUserAdmin(ModelView, model=ContestUser):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin, Roles.organizer]:
            return False

        self.can_view_details = role in [Roles.admin, Roles.organizer]
        self.can_create = role in [Roles.admin, Roles.organizer]
        self.can_edit = role in [Roles.admin, Roles.organizer]
        self.can_delete = role in [Roles.admin, Roles.organizer]
        self.can_export = role in [Roles.admin, Roles.organizer]

        return True

    icon = "fa-solid fa-id-badge"
    column_list = [
        ContestUser.contest_id,
        ContestUser.user_id,
    ]
    form_include_pk = True
    column_details_list = column_list
    form_columns = column_list
    column_searchable_list = column_list
    column_sortable_list = []


class ContestProblemAdmin(ModelView, model=ContestProblem):
    def is_accessible(self, request: Request) -> bool:
        role = get_role_from_request(request)
        if role not in [Roles.admin, Roles.organizer]:
            return False

        self.can_view_details = role in [Roles.admin, Roles.organizer]
        self.can_create = role in [Roles.admin, Roles.organizer]
        self.can_edit = role in [Roles.admin, Roles.organizer]
        self.can_delete = role in [Roles.admin, Roles.organizer]
        self.can_export = role in [Roles.admin, Roles.organizer]

        return True

    icon = "fa-solid fa-list"
    column_list = [
        ContestProblem.contest_id,
        ContestProblem.problem_id,
    ]
    form_include_pk = True
    column_details_list = column_list
    form_columns = column_list
    column_searchable_list = column_list
    column_sortable_list = []


def get_admin(app: FastAPI) -> Admin:
    authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        templates_dir="/backend/src/templates/sqladmin",
    )
    admin.add_view(UserAdmin)
    admin.add_view(ProblemAdmin)
    admin.add_view(RoleAdmin)
    admin.add_view(ContestAdmin)
    admin.add_view(SubmissionAdmin)
    admin.add_view(ContestUserAdmin)
    admin.add_view(ContestProblemAdmin)
    return admin

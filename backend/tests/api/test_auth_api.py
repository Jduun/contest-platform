from uuid import uuid4

import pytest
from faker import Faker
from fastapi import status
from sqlalchemy import insert, select

from src.auth.models import Role, User
from src.auth.schemas import UserResponse
from src.auth.service import get_password_hash, get_token_payload, verify_password

faker = Faker()


@pytest.mark.asyncio
async def test_login_success(db_session, client):
    role_id = uuid4()
    role_name = "user"
    add_role_query = insert(Role).values(id=role_id, name=role_name)
    await db_session.execute(add_role_query)
    await db_session.commit()

    user_id = uuid4()
    username, password = faker.name(), faker.password()
    password_hash = get_password_hash(password)
    add_user_query = insert(User).values(
        id=user_id, username=username, password=password_hash, role_id=role_id
    )
    await db_session.execute(add_user_query)
    await db_session.commit()

    response = await client.post(
        "/login", data={"username": username, "password": password}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"
    token_data = get_token_payload(data["access_token"])
    assert token_data.get("username") == username
    assert token_data.get("role") == role_name


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, entered_username, entered_password",
    [
        (
            "correct_username",
            "correct_password",
            "correct_username",
            "incorrect_password",
        ),
        (
            "correct_username",
            "correct_password",
            "incorrect_username",
            "correct_password",
        ),
        (
            "correct_username",
            "correct_password",
            "incorrect_username",
            "incorrect_password",
        ),
    ],
)
async def test_login_failure(
    db_session,
    client,
    username: str,
    password: str,
    entered_username: str,
    entered_password: str,
):
    role_id = uuid4()
    add_role_query = insert(Role).values(id=role_id, name="user")
    await db_session.execute(add_role_query)
    await db_session.commit()

    user_id = uuid4()
    password_hash = get_password_hash(password)
    add_user_query = insert(User).values(
        id=user_id, username=username, password=password_hash, role_id=role_id
    )
    await db_session.execute(add_user_query)
    await db_session.commit()

    response = await client.post(
        "/login", data={"username": entered_username, "password": entered_password}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data.get("detail") == "Incorrect username or password"


@pytest.mark.asyncio
async def test_register_success(db_session, client):
    role_id = uuid4()
    add_role_query = insert(Role).values(id=role_id, name="user")
    await db_session.execute(add_role_query)
    await db_session.commit()

    username, password = faker.name(), faker.password()
    response = await client.post(
        "/register", json={"username": username, "password": password}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    user_model = UserResponse.model_validate(data)
    assert user_model.username == username
    query = select(User).filter_by(username=username)
    res = await db_session.execute(query)
    user = res.scalar()
    assert user.username == username
    assert verify_password(password, user.password)


@pytest.mark.asyncio
async def test_register_conflict_username(db_session, client):
    role_id = uuid4()
    add_role_query = insert(Role).values(id=role_id, name="user")
    await db_session.execute(add_role_query)
    await db_session.commit()

    username, password = faker.name(), faker.password()
    # Register user with same username
    for _i in range(2):
        response = await client.post(
            "/register", json={"username": username, "password": password}
        )

    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data["detail"] == "User with the same name already exists"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password",
    [
        ("username", "1"),
        ("username", "1234"),
        ("username", "1234567"),
        ("", "12345678"),
        ("", "1"),
        ("", "1234"),
        ("", "1234567"),
    ],
)
async def test_register_invalid_data_format(
    db_session, client, username: str, password: str
):
    role_id = uuid4()
    add_role_query = insert(Role).values(id=role_id, name="user")
    await db_session.execute(add_role_query)
    await db_session.commit()

    response = await client.post(
        "/register", json={"username": username, "password": password}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

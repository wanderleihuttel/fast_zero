# https://github.com/astral-sh/uv-fastapi-example/tree/main
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password_hash,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.scalar(
        select(User).where((User.email == form_data.username))
    )

    if not db_user or not verify_password_hash(
        form_data.password, db_user.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Incorrect email or password!',
        )
    access_token = create_access_token(data={'sub': db_user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists!',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists!',
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    db_users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': db_users}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user_exercicio(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )
    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Not enough permission!'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    # session.add(db_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Not enough permission!'
        )

    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted!'}

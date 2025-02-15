from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password_hash

router = APIRouter(prefix='/auth', tags=['auth'])

# Boa prática na definição de tipos T_
T_OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(session: T_Session, form_data: T_OAuthForm):
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

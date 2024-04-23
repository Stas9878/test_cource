import time
import uuid
from fastapi import (APIRouter, Depends, 
                     HTTPException, status, 
                     Header, Response,
                     Cookie)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from auth.schemas import UserSchema, TokenInfo
from auth.utils import (encode_jwt, validate_auth_user, 
                        get_current_active_auth_user, get_current_token_payload)
import secrets


router = APIRouter(
    prefix='/demo-auth', 
    tags=['Demo auth']
)


security = HTTPBasic()


@router.get('/basic-auth/')
def demo_basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'message': 'g',
        'username': credentials.username,
        'password': credentials.password
    }


username_to_pass = {
    'admin': 'admin',
    'john': 'pass'
}


static_auth_token = {
    'qwerty123': 'admin',
    '321ytrewq': 'john'
}


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
        headers={'WWW-Authenticate': 'Basic'}
    )

    password = username_to_pass.get(credentials.username, None)

    if password is None:
        raise unauthed_exc
    
    #secrets
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        password.encode('utf-8')
    ):
        raise unauthed_exc

    return credentials.username


def get_username_by_static_auth_token(static_token: str = Header(alias='xxx-auth-token')) -> str:
    if static_token not in static_auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid',
        )
    return static_auth_token[static_token]


@router.get('/basic-auth-username/')
def demo_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        'message': f'Hi, {auth_username}',
        'username': auth_username,
    }


@router.get('/some-http-header-auth/')
def demo_auth_http_header(username: str = Depends(get_username_by_static_auth_token)):
    return {
        'message': f'Hi, {username}',
        'username': username,
    }


COOKIES: dict[str, dict] = {}
COOKIE_SESSION_ID_KEY = 'web-app-cookie-session-id'


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post('/login-cookie/')
def demo_auth_login_cookie(response: Response, #auth_username: str = Depends(get_auth_user_username),
                           username: str = Depends(get_username_by_static_auth_token)):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time.time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        'result': 'ok',
        'user': username
    }


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    print(COOKIES, session_id)
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not auth'
        )
    return COOKIES[session_id]


@router.get('/check-cookie/')
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data['username']
    return {
        'message': f'Hi, {username}',
        **user_session_data
    }


@router.get('/logout-cookie/')
def dem_auth_logout(response: Response,
                    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
                    user_session_data: dict = Depends(get_session_data)):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data['username']
    return {
        'message': f'Bye, {username}'
    }

#JWT

@router.post('/login_jwt/')
def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)) -> TokenInfo:
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
    }

    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


@router.get('/users/me/')
def auth_user_check_self_info(payload: dict = Depends(get_current_token_payload),
                              user: UserSchema = Depends(get_current_active_auth_user)):
    iat = payload.get('iat')
    return {
        'username': user.username,
        'email': user.email,
        'logged_in_at': iat    
    }
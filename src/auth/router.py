from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
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
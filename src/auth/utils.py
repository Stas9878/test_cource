from fastapi import (HTTPException, status, 
                     Form, Depends)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.schemas import UserSchema
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError
import jwt
import bcrypt
from config import settings


http_bearer = HTTPBearer()


def encode_jwt(payload: dict, 
               private_key: str = settings.auth_jwt.private_key_path.read_text(), 
               algorithm: str = settings.auth_jwt.algorithm,
               expire_timedelta: timedelta | None = None,
               expire_minutes: int = settings.auth_jwt.access_token_expire_minutes):
    
    to_encode = payload.copy()
    
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire.timestamp(),
        iat=now.timestamp(),
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(token: dict, 
               public_key: str = settings.auth_jwt.public_key_path.read_text(), 
               algorithm: str = settings.auth_jwt.algorithm):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms = [algorithm]

    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password)


john = UserSchema(
    username='john',
    password=hash_password('secret'),
    email='john@example.com'
)

sam = UserSchema(
    username='sam',
    password=hash_password('secret')
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam
}


def validate_auth_user(username: str = Form(),
                       password: str = Form()) -> UserSchema:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password'
    )

    if not (user := users_db.get(username)):
        raise unauthed_exc
    
    if not validate_password(password=password,hash_password=user.password):
        raise unauthed_exc
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive'

        )
    return user


def get_current_token_payload(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token
        )
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'invalid token error: {e}'
        )


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    username: str | None = payload.get('sub')
    if user := users_db.get(username):
        return user
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid'
        )
    

def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)) -> UserSchema:
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive'
    )
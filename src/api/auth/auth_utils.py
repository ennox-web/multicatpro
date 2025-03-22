"""Auth Testing Ground"""

from functools import cached_property
from typing import Annotated, Union
from datetime import timedelta, datetime, timezone

from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer #, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from strawberry.fastapi import BaseContext
from mongoengine.errors import DoesNotExist

from api.auth.config import JWT_SECRET_KEY, JWT_ALGO, ACCESS_TOKEN_EXPIRE_MINUTES
from api.db.user import User
from api.utils import verify_password
from api.db.jwt_token import Token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

class UserModel(BaseModel):
    """User Model."""
    username: str
    email: str
    password: str
    provider: str


class TokenModel(BaseModel):
    """Token Model."""
    user_id: str
    username: str
    access_token: str
    refresh_token: str


# Figure out how all below can be part of the GraphQL CONTEXT
# Refresh token??
# https://fastapi.tiangolo.com/tutorial/security/first-steps/#the-password-flow
# https://strawberry.rocks/docs/integrations/fastapi
# https://gh0stfrk.medium.com/token-based-authentication-with-fastapi-7d6a22a127bf

def authenticate_user(username: str, password: str) -> User:
    """Authenticates the user."""
    # Get user from DB
    # Pass password and user.hashed_password to verify_password()
    # Return false if passwords don't match
    credentials_exception =  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        user = User.objects.get(username=username)
        if not user or user.blacklisted or not verify_password(password, user.password):
            raise credentials_exception
    except DoesNotExist:
        raise credentials_exception from DoesNotExist

    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGO)


def blacklist_token(access_token: str) -> None:
    """Blacklist a token."""
    token = Token.objects(access_token=access_token).first()
    if not token:
        raise HTTPException(status_code=401, detail="Access denied.")
    token.blacklisted = True
    token.save()


def verify_and_refresh_token(refresh_token: str) -> TokenModel | None:
    """Refresh Token"""
    http_exception = HTTPException(status_code=401, detail="Unable to refresh token")
    token = Token.objects(refresh_token=refresh_token).first()
    if not token or token.blacklist_token:
        raise http_exception
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
    username: str = payload.get("sub").split("username:")[1]
    if not username:
        raise http_exception
    user = User.objects(username=username).first()
    if not user or user.blacklisted:
        raise http_exception

    access_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": f"username:{user.username}"},
        expires_delta=access_expiration
    )

    token.access_token = new_access_token
    token.access_expiration = access_expiration
    token.save()

    return TokenModel(
        user_id=str(user.id),
        username=user.username,
        email=user.email,
        access_token=new_access_token,
        refresh_token=token
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User | None:
    """Gets the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception  # pylint: disable=raise-missing-from

    user = User.objects.get(username=username)
    if user is None:
        raise credentials_exception

    return user


# async def get_context(user=Depends(get_current_user)) -> dict:
#     """For context_gettr GraphQL."""
#     return {"user": user}


class Context(BaseContext):
    """GraphQL Context."""

    @cached_property
    def user(self) -> User | None:
        """Authenticate user."""
        if not self.request:
            return None
        authorization = self.request.headers.get("Authorization", None)
        print(f"Request Headers: {self.request.headers}")
        # try:
        #     authorized_user = get_current_user(authorization)
        #     if authorized_user:
        #         print(f"authed_user {authorized_user.username}")
        #     else:
        #         print("No authed user.")
        # except Exception as e:
        #     print(f"Got exception {e}")

        user = User.objects.get(username="blep")
        return user


async def get_context() -> Context:
    return Context()

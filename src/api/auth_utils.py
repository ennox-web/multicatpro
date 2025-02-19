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

from api.config import JWT_SECRET_KEY, JWT_ALGO, ACCESS_TOKEN_EXPIRE_MINUTES
from api.db.user import User
from api.utils import verify_password
from api.db.token_blacklist import TokenBlacklist


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

class Token(BaseModel):
    """Token Model."""
    user_id: str
    username: str
    email: str
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
        if not user or not verify_password(password, user.password):
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


def blacklist_token(token: str) -> None:
    """Blacklist a token."""
    data = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
    expiration = datetime.fromtimestamp(data.get("exp"))
    TokenBlacklist(token=token, expiration=expiration).save()


def verify_and_refresh_token(token: str) -> Token | None:
    """Refresh Token"""
    blacklisted_token = TokenBlacklist.objects(token=token).first()
    if blacklisted_token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        username: str = payload.get("sub").split("username:")[1]
        if not username:
            return None
        user = User.objects(username=username).first()
        if not user:
            return None

        new_access_token = create_access_token(
            data={"sub": f"username:{user.username}"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return Token(
            user_id=str(user.id),
            username=user.username,
            email=user.email,
            access_token=new_access_token,
            refresh_token=token
        )

    except InvalidTokenError:  # pylint: disable=broad-exception-caught
        return None
    return None


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
        # authorization = self.request.headers.get("Authorization", None)
        # print(f"Request Headers: {self.request.headers}")
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

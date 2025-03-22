"""FastAPI Server."""
from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine import disconnect
from strawberry.fastapi import GraphQLRouter

from api.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from api.schemas.schema import schema
from api.db.client import client
from api.db.jwt_token import Token

from api.auth.auth_utils import (
    authenticate_user,
    create_access_token,
    TokenModel,
    get_context,
    verify_and_refresh_token,
    blacklist_token,
    oauth2_scheme,
)


app = FastAPI()
graphql_router = GraphQLRouter(schema, graphql_ide="apollo-sandbox", context_getter=get_context)
app.include_router(graphql_router, prefix="/api/graphql")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://localhost:8000',
        'https://127.0.0.1:8000',
        'http://frontend:3000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(HTTPSRedirectMiddleware)


@app.get('/api/hello')
async def hello_world():
    """Test API endpoint."""
    return {"message": "Hello World!"}


@app.on_event("startup")
def startup_db_client():
    """Startup MongoDB client."""
    try:
        print(f"MongoDB connection established successfully. {client.admin.command('ping')}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error connection to MongoDB: {e}")


@app.on_event("shutdown")
def shutdown_db_client():
    """Shutdown MongoDB client."""
    disconnect()


@app.post("/api/login", response_model=TokenModel)
async def login(auth: OAuth2PasswordRequestForm = Depends()):
    """Login."""
    user = authenticate_user(auth.username, auth.password)
    access_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expiration = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": f"username:{user.username}"},
        expires_delta=access_expiration
    )
    refresh_token = create_access_token(
        data={"sub": f"username:{user.username}"},
        expires_delta=refresh_expiration
    )

    Token(
        access_token=access_token,
        refresh_token=refresh_token,
        access_expiration_date=datetime.now() + access_expiration,
        refresh_expiration_date=datetime.now() + refresh_expiration
    ).save()

    return TokenModel(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        username=user.username,
        email=user.email,
    )


@app.post("/api/refresh", response_model=TokenModel)
async def refresh(refresh_token: str = Depends(oauth2_scheme)):
    """Refresh JWT token."""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No valid refresh token.")
    return verify_and_refresh_token(refresh_token)


@app.post("/api/logout")
async def logout(access_token: str = Depends(oauth2_scheme)):
    """Logout."""
    blacklist_token(access_token=access_token)
    return {"message": "Logout successful"}

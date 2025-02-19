"""FastAPI Server."""
from datetime import timedelta

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine import disconnect
from strawberry.fastapi import GraphQLRouter

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from api.schemas.schema import schema
from api.db.client import client

from api.auth_utils import authenticate_user,
    create_access_token,
    Token,
    get_context,
    verify_and_refresh_token,
    blacklist_token,
    oauth2_scheme


app = FastAPI()
graphql_router = GraphQLRouter(schema, graphql_ide="apollo-sandbox", context_getter=get_context)
app.include_router(graphql_router, prefix="/api/graphql")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://frontend:3000',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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


@app.post("/api/login", response_model=Token)
async def login(auth: OAuth2PasswordRequestForm = Depends()):
    """Login."""
    user = authenticate_user(auth.username, auth.password)
    access_token = create_access_token(
        data={"sub": f"username:{user.username}"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_access_token(
        data={"sub": f"username:{user.username}"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=str(user.id),
        username=user.username,
        email=user.email,
    )


@app.post("/api/refresh", response_model=Token)
async def refresh(refresh_token: str = Depends(oauth2_scheme)):
    """Refresh JWT token."""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No valid refresh token.")
    new_access_token = verify_and_refresh_token(refresh_token)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="No valid refresh token.")
    return new_access_token


@app.post("/api/logout")
async def logout(request: Request):
    """Logout."""
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    blacklist_token(refresh_token)
    blacklist_token(access_token)
    return {"message": "Logout successful"}

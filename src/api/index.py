"""FastAPI Server."""
from datetime import timedelta

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine import disconnect
from strawberry.fastapi import GraphQLRouter

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from api.schemas.schema import schema
from api.db.client import client

from api.auth_utils import authenticate_user, create_access_token, Token, get_context


app = FastAPI()
graphql_router = GraphQLRouter(schema, graphql_ide="apollo-sandbox", context_getter=get_context)
app.include_router(graphql_router, prefix="/api/graphql")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
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


@app.post("/login", response_model=Token)
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
    return Token(access_token=access_token, refresh_token=refresh_token)


# @app.post("/refresh")

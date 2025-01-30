from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from src.api.mongodb import client
# from src.api.config import DB_NAME
# from mongodb import client
# from config import DB_NAME
from mongoengine import disconnect
from strawberry.fastapi import GraphQLRouter

from api.schemas.schema import schema
from api.db.client import client


app = FastAPI()
graphql_router = GraphQLRouter(schema, graphql_ide="apollo-sandbox")
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
    return {"message": "Hello World!"}


@app.on_event("startup")
def startup_db_client():
    try:
        print(f"MongoDB connection established successfully. {client.admin.command('ping')}")
    except Exception as e:
        print(f"Error connection to MongoDB: {e}")


@app.on_event("shutdown")
def shutdown_db_client():
    disconnect()

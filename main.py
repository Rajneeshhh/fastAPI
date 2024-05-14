from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from dotenv import load_dotenv
import os

# Import SQLAlchemy models
from models import Base

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Connect to the database
database_url = os.getenv("DATABASE_URL")
database = Database(database_url)

# Define your table model (optional)
metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("age", Integer)
)

# Event handler for startup
@app.on_event("startup")
async def startup_event():
    await database.connect()
    print("Connected to the database successfully.")

# Define endpoint
@app.get("/users/")
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

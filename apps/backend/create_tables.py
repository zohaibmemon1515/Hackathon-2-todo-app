from sqlmodel import SQLModel
from src.database.database import engine
from src.models.task import Task
from src.models.user import User
from src.models.message import Message
from src.models.conversation import Conversation

SQLModel.metadata.drop_all(engine)  # drops all tables
SQLModel.metadata.create_all(engine)  # recreates all tables
print("Tables recreated with new columns")
"""
Database migration scripts for AI Chatbot feature
Handles creation and removal of Conversation, Message, and Task tables
"""
from sqlmodel import Session, create_engine, SQLModel
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.task import Task
from .database import DATABASE_URL


def create_tables():
    """Create all required tables for the AI Chatbot feature."""
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints SQL statements

    # Create all tables defined in metadata (Conversation, Message, Task)
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully")


def drop_tables():
    """Drop all tables for the AI Chatbot feature."""
    engine = create_engine(DATABASE_URL, echo=True)

    # Drop all tables defined in metadata
    SQLModel.metadata.drop_all(engine)
    print("✅ Tables dropped successfully")


def seed_data():
    """Add initial seed data if needed."""
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        # Example: Add a test task for your user
        from uuid import UUID
        from datetime import datetime

        # Replace with a real user UUID
        test_user_id = UUID("3db56ed5-1105-4ad2-a42f-c0840bee3b64")

        test_task = Task(
            title="Test Task",
            description="This is a seed task",
            is_completed=False,
            priority="medium",
            user_id=test_user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(test_task)
        session.commit()
        print("✅ Seed data inserted successfully")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "create":
            create_tables()
        elif sys.argv[1] == "drop":
            drop_tables()
        elif sys.argv[1] == "seed":
            seed_data()
        else:
            print("Usage: python migrate.py [create|drop|seed]")
    else:
        print("Usage: python migrate.py [create|drop|seed]")

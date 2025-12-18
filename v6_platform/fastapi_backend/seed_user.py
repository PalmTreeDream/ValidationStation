import asyncio
from app.database import create_db_and_tables, async_session_maker
from app.users import UserManager
from app.schemas import UserCreate
from app.models import User
from fastapi_users.db import SQLAlchemyUserDatabase

async def create_user():
    print("Creating tables...")
    await create_db_and_tables()
    print("Tables created.")

    async with async_session_maker() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)
        
        try:
            user = await user_manager.create(
                UserCreate(
                    email="admin@example.com",
                    password="Password123!",
                    is_active=True,
                    is_superuser=True,
                    is_verified=True
                )
            )
            print(f"User created: {user.email}")
        except Exception as e:
            print(f"Skipping creation (likely exists or error): {str(e)}")

if __name__ == "__main__":
    asyncio.run(create_user())

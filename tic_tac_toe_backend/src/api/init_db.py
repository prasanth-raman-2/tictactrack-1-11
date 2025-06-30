"""
Example script to initialize the Tic Tac Toe database and create tables using SQLAlchemy.
Run this script once to initialize the database (for development).
"""

import asyncio
from .db import engine, Base


# PUBLIC_INTERFACE
async def init_models():
    """Creates all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created.")


if __name__ == "__main__":
    asyncio.run(init_models())

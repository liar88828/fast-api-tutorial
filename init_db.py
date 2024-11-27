import asyncio

from database.config import engine
from database.table import product
from database.table import user


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(product.Base.metadata.create_all)
        await conn.run_sync(user.Base.metadata.create_all, )
    print("Database initialized!")


# Run the initialization
if __name__ == "__main__":
    asyncio.run(init_db())

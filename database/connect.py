from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from key import DATABASE_URL

engine = create_async_engine(DATABASE_URL,
                             echo=True
                             # connect_args={"check_same_thread": False}
                             )
# noinspection PyTypeChecker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    # autocommit=False,
    # autoflush=False

)


def get_db():
    # async with async_session() as session:
    #     yield session
    db = async_session()
    try:
        yield db
    finally:
        db.close()

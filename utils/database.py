from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import config

async_engine = create_async_engine(
    url=config.connection_string_asyncpg,
    echo=config.DB_ECHO,
)

async_session_factory = async_sessionmaker(async_engine)

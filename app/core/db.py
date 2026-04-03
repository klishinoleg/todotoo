from asyncpg import InternalServerError
from tortoise import Tortoise, connections, BaseDBAsyncClient, ConfigurationError

from core.config.settings import settings

MASTER_CONNECTION = "default"
SLAVE_CONNECTION = "read"

# ----------------------------------------------------------------------
# Main Tortoise config (via connection params)
# ----------------------------------------------------------------------
TORTOISE_ORM = {
    "connections": {
        MASTER_CONNECTION: {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.db.host,
                "port": settings.db.port,
                "user": settings.db.user,
                "password": settings.db.password,
                "database": settings.db.name,
                "minsize": 1,
                "maxsize": 5,
                "ssl": False,
            },
        },
        SLAVE_CONNECTION: {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.db.host,
                "port": settings.db.port,
                "user": settings.db.user,
                "password": settings.db.password,
                "database": settings.db.name,
                "minsize": 1,
                "maxsize": 3,
                "ssl": False,
            },
        },
    },
    "apps": {
        "models": {
            "models": [
                "infrastructure.repository.tortoise.models",
                "aerich.models",
            ],
            "default_connection": MASTER_CONNECTION,
        },
    },
    "default_schema": "public",
}

# ----------------------------------------------------------------------
# Direct URL config (for migrations or local tools)
# ----------------------------------------------------------------------
TORTOISE_ORM_DIRECT = {
    "connections": {
        MASTER_CONNECTION: settings.db.get_db_url(),
        SLAVE_CONNECTION: settings.db.slave_url or settings.db.get_db_url(),
    },
    "apps": {
        "models": {
            "models": [
                "infrastructure.repository.tortoise.models",
                "aerich.models",
            ],
            "default_connection": MASTER_CONNECTION,
        }
    },
    "default_schema": "public",
}


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
async def ensure_db_functions() -> None:
    """
    Ensures required PostgreSQL SQL functions exist.
    Called after startup or migrations.
    """
    conn = get_master_connection()
    try:
        # add SQL initializers here when needed
        ...
    except InternalServerError:
        return


# ----------------------------------------------------------------------
# Lifecycle
# ----------------------------------------------------------------------
async def init_tortoise(with_schema: bool = False) -> None:
    """
    Initialize Tortoise ORM and load all model modules.
    """
    await Tortoise.init(config=TORTOISE_ORM)
    await ensure_db_functions()

    if with_schema:
        await Tortoise.generate_schemas()


async def close_tortoise() -> None:
    """Close all database connections."""
    await connections.close_all()


# ----------------------------------------------------------------------
# Direct access helpers
# ----------------------------------------------------------------------
def get_master_connection() -> BaseDBAsyncClient:
    conn = connections.get(MASTER_CONNECTION)
    if not conn:
        raise ConfigurationError("Master connection does not exist")
    return conn


def get_slave_connection() -> BaseDBAsyncClient:
    conn = connections.get(SLAVE_CONNECTION)
    if not conn:
        raise ConfigurationError("Slave connection does not exist")
    return conn

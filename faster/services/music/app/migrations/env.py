from logging import getLogger
from os.path import dirname, join

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

from db.base import Base, engine

# This is the Alembic Config object, which provides
# access to the values within the main configuration file.
config = context.config

# Interpret the config file for Python modules, if needed.
# context.configure(
#     url=config.get_main_option("sqlalchemy.url"),
#     target_metadata=Base.metadata,
#     render_as_batch=True,
# )

# Add your model's MetaData object to this configuration object.
target_metadata = Base.metadata

# Other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

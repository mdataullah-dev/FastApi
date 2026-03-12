from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

#!changed imports below 
#*-------------------------------------------
from src.utils.settings import settings
from src.tasks.models import TaskModel
from src.user.models import UserModel
from src.utils.db import Base
#*---------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
#?----------------------------added this line----------------------------
config.set_main_option(
    "sqlalchemy.url",
    settings.DB_CONNECTION.replace("%", "%%")
)  #* for alembic =>     @ is %%

'''
|| RUN THIS COMMAND || => alembic revision --autogenerate -m "add user_id to tasks"
                           this command will generate a file inside ./migration/version/c69af660c806_add_user_id_to_tasks.py
                           
|| after this file created => run this command :   alembic upgrade head

||   now succes ke baad user_id naam ka column hamari db mein dikhne lagega

'''
#?---------------------------------------------------------------------------

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

#?----------------------------------added this line-----------------
target_metadata = Base.metadata
#?--------------------------------------------------------------------
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

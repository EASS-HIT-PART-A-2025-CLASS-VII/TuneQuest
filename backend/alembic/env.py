import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.base import Base
from app.models.user import User
from app.models.favorite import Favorite
from app.models.history import AiHistory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_URL = os.getenv("MIGRATION_DB_URL")
if not DB_URL:
    raise RuntimeError("DB_URL not set in .env")

# Configure Alembic
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", DB_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in offline mode."""
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
    """Run migrations in online mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

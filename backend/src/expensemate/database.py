from collections.abc import AsyncGenerator

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from expensemate.settings import settings


engine = create_async_engine(settings.database_url, future=True, echo=False)


def _run_simple_migrations(connection) -> None:
    inspector = inspect(connection)
    tables = set(inspector.get_table_names())

    required_columns = {
        'expenses': ['user_id'],
        'budgets': ['user_id'],
        'recurring_expenses': ['user_id'],
    }

    for table_name, columns in required_columns.items():
        if table_name not in tables:
            continue
        existing = {column['name'] for column in inspector.get_columns(table_name)}
        for column_name in columns:
            if column_name in existing:
                continue
            connection.execute(text(f'ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER'))


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
        await connection.run_sync(_run_simple_migrations)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

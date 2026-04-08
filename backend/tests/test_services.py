from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from expensemate.models import (
    BudgetUpdate,
    CategoryBudgetUpsert,
    ExpenseCreate,
    RecurringExpenseCreate,
    User,
)
from expensemate.services import (
    category_budget_statuses,
    create_expense,
    create_recurring_expense,
    generate_due_recurring_expenses,
    handle_assistant_message,
    overview,
    set_budget,
    set_category_budget,
)


@pytest.mark.asyncio
async def test_budget_and_category_budget_flow() -> None:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        user = User(name='Test User', email='test@example.com', password_hash='hash')
        session.add(user)
        await session.commit()
        await session.refresh(user)

        await create_expense(
            session,
            user,
            ExpenseCreate(
                amount=Decimal('12.50'),
                category='Food',
                description='Lunch',
                spent_on=date.today(),
            ),
        )
        await create_expense(
            session,
            user,
            ExpenseCreate(
                amount=Decimal('7.20'),
                category='Transport',
                description='Bus',
                spent_on=date.today(),
            ),
        )
        await set_budget(session, user, BudgetUpdate(monthly_limit=Decimal('500.00')))
        await set_category_budget(session, user, CategoryBudgetUpsert(category='Food', monthly_limit=Decimal('100.00')))

        statuses = await category_budget_statuses(session, user)
        assert len(statuses) == 1
        assert statuses[0].category == 'Food'
        assert statuses[0].spent_this_month == Decimal('12.50')

        summary = await overview(session, user, period='this_month')
        assert summary.budget_status is not None
        assert summary.category_budget_statuses

    await engine.dispose()


@pytest.mark.asyncio
async def test_recurring_generation_and_assistant_commands() -> None:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', future=True)
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        user = User(name='Assistant User', email='assistant@example.com', password_hash='hash')
        session.add(user)
        await session.commit()
        await session.refresh(user)

        await create_recurring_expense(
            session,
            user,
            RecurringExpenseCreate(
                amount=Decimal('20.00'),
                category='Bills',
                description='Spotify',
                frequency='monthly',
                start_date=date.today(),
            ),
        )
        result = await generate_due_recurring_expenses(session, user)
        assert result.created_count == 1

        response = await handle_assistant_message(session, user, 'Set food category budget 120')
        assert response.action == 'set_category_budget'
        assert '€120.00' in response.answer

        response = await handle_assistant_message(session, user, 'What is my food budget status?')
        assert response.action == 'category_budget_status'
        assert 'Food:' in response.answer

    await engine.dispose()

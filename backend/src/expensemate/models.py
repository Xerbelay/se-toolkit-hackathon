from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from sqlmodel import Field as SQLField, SQLModel


def utcnow_naive() -> datetime:
    return datetime.utcnow()


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = SQLField(default=None, primary_key=True)
    name: str = SQLField(max_length=120)
    email: str = SQLField(max_length=255, index=True, sa_column_kwargs={'unique': True})
    password_hash: str = SQLField(max_length=255)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class UserSession(SQLModel, table=True):
    __tablename__ = 'user_sessions'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(foreign_key='users.id', index=True, nullable=False)
    token_hash: str = SQLField(max_length=64, index=True, sa_column_kwargs={'unique': True})
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)
    expires_at: datetime = SQLField(nullable=False)


class AuthRegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class AuthLoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class AuthUserRead(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class ExpenseBase(SQLModel):
    amount: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0.01)
    category: str = SQLField(max_length=50, default='Other')
    description: str = SQLField(max_length=255, default='')
    spent_on: date = SQLField(default_factory=date.today)


class Expense(ExpenseBase, table=True):
    __tablename__ = 'expenses'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(default=None, foreign_key='users.id', index=True)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Decimal = Field(ge=0.01)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(max_length=255)
    spent_on: date


class ExpenseRead(ExpenseBase):
    id: int
    created_at: datetime


class Budget(SQLModel, table=True):
    __tablename__ = 'budgets'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(default=None, foreign_key='users.id', index=True)
    monthly_limit: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0.01)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)
    updated_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class BudgetUpdate(BaseModel):
    monthly_limit: Decimal = Field(ge=0.01)


class BudgetRead(BaseModel):
    monthly_limit: Decimal | None = None
    updated_at: datetime | None = None


class BudgetStatus(BaseModel):
    monthly_limit: Decimal
    spent_this_month: Decimal
    remaining_amount: Decimal
    percent_used: int
    is_over_budget: bool
    projected_total: Decimal | None = None
    projected_percent_used: int | None = None


class CategoryBudget(SQLModel, table=True):
    __tablename__ = 'category_budgets'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(default=None, foreign_key='users.id', index=True)
    category: str = SQLField(max_length=50, index=True)
    monthly_limit: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0.01)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)
    updated_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class CategoryBudgetUpsert(BaseModel):
    category: str = Field(min_length=1, max_length=50)
    monthly_limit: Decimal = Field(ge=0.01)


class CategoryBudgetRead(BaseModel):
    id: int
    category: str
    monthly_limit: Decimal
    updated_at: datetime


class CategoryBudgetStatus(BaseModel):
    id: int
    category: str
    monthly_limit: Decimal
    spent_this_month: Decimal
    remaining_amount: Decimal
    percent_used: int
    is_over_budget: bool


class SavingsGoalBase(SQLModel):
    title: str = SQLField(max_length=120)
    target_amount: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0.01)
    current_amount: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0)
    target_date: date | None = SQLField(default=None, nullable=True)
    note: str = SQLField(max_length=255, default='')


class SavingsGoal(SavingsGoalBase, table=True):
    __tablename__ = 'savings_goals'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(default=None, foreign_key='users.id', index=True)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)
    updated_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class SavingsGoalCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    target_amount: Decimal = Field(ge=0.01)
    current_amount: Decimal = Field(default=Decimal('0.00'), ge=0)
    target_date: date | None = None
    note: str = Field(default='', max_length=255)


class SavingsGoalUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    target_amount: Decimal = Field(ge=0.01)
    current_amount: Decimal = Field(ge=0)
    target_date: date | None = None
    note: str = Field(default='', max_length=255)


class SavingsGoalRead(BaseModel):
    id: int
    title: str
    target_amount: Decimal
    current_amount: Decimal
    target_date: date | None
    note: str
    created_at: datetime
    updated_at: datetime


class SavingsGoalStatus(BaseModel):
    id: int
    title: str
    target_amount: Decimal
    current_amount: Decimal
    remaining_amount: Decimal
    progress_percent: int
    target_date: date | None
    monthly_required: Decimal | None = None
    is_completed: bool
    note: str = ''


class SummaryCard(BaseModel):
    label: str
    value: str
    help_text: str


class CategoryBreakdown(BaseModel):
    category: str
    total_amount: Decimal
    count: int


class DailySpendPoint(BaseModel):
    day: date
    total_amount: Decimal


class MonthlySpendPoint(BaseModel):
    month_key: str
    month_label: str
    total_amount: Decimal


class InsightRead(BaseModel):
    title: str
    detail: str
    tone: str = 'neutral'


class CoachSummary(BaseModel):
    health_score: int
    headline: str
    wins: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class RecurringExpenseBase(SQLModel):
    amount: Decimal = SQLField(max_digits=10, decimal_places=2, ge=0.01)
    category: str = SQLField(max_length=50, default='Other')
    description: str = SQLField(max_length=255, default='')
    frequency: str = SQLField(max_length=20, default='monthly')
    start_date: date = SQLField(default_factory=date.today)


class RecurringExpense(RecurringExpenseBase, table=True):
    __tablename__ = 'recurring_expenses'

    id: int | None = SQLField(default=None, primary_key=True)
    user_id: int = SQLField(default=None, foreign_key='users.id', index=True)
    next_due_on: date = SQLField(default_factory=date.today, nullable=False)
    last_generated_on: date | None = SQLField(default=None, nullable=True)
    is_active: bool = SQLField(default=True, nullable=False)
    created_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)
    updated_at: datetime = SQLField(default_factory=utcnow_naive, nullable=False)


class RecurringExpenseCreate(RecurringExpenseBase):
    frequency: str = Field(pattern='^(weekly|monthly)$')


class RecurringExpenseUpdate(BaseModel):
    amount: Decimal = Field(ge=0.01)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(max_length=255)
    frequency: str = Field(pattern='^(weekly|monthly)$')
    start_date: date
    is_active: bool = True


class RecurringExpenseRead(RecurringExpenseBase):
    id: int
    next_due_on: date
    last_generated_on: date | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class RecurringGenerationResponse(BaseModel):
    created_count: int
    created_expense_ids: list[int] = Field(default_factory=list)
    through_date: date


class CsvImportPreviewRequest(BaseModel):
    csv_text: str = Field(min_length=1, max_length=50_000)


class CsvImportPreviewRow(BaseModel):
    row_number: int
    spent_on: date | None = None
    description: str | None = None
    category: str | None = None
    amount: Decimal | None = None
    is_valid: bool
    is_duplicate: bool = False
    error_message: str | None = None


class CsvImportPreviewResponse(BaseModel):
    detected_columns: dict[str, str]
    total_rows: int
    valid_rows: int
    duplicate_rows: int
    invalid_rows: int
    preview_rows: list[CsvImportPreviewRow] = Field(default_factory=list)


class CsvImportResult(BaseModel):
    imported_count: int
    duplicate_rows: int
    invalid_rows: int
    total_rows: int


class DueRecurringSummary(BaseModel):
    due_today_count: int
    due_next_7_days_count: int
    next_due_items: list[RecurringExpenseRead] = Field(default_factory=list)


class OverviewResponse(BaseModel):
    period_label: str
    cards: list[SummaryCard]
    budget_status: BudgetStatus | None = None
    category_budget_statuses: list[CategoryBudgetStatus] = Field(default_factory=list)
    due_recurring_summary: DueRecurringSummary | None = None
    goals: list[SavingsGoalStatus] = Field(default_factory=list)


class AssistantMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    lang: str | None = Field(default=None, pattern='^(en|ru)$')


class AssistantMessageResponse(BaseModel):
    answer: str
    action: str
    created_expense: ExpenseRead | None = None
    created_recurring: RecurringExpenseRead | None = None
    created_goal: SavingsGoalRead | None = None
    suggestions: list[str] = Field(default_factory=list)

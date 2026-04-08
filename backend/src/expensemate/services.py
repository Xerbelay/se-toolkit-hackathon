from __future__ import annotations

import calendar
import csv
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation

import httpx
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from expensemate.models import (
    AssistantMessageResponse,
    Budget,
    BudgetRead,
    BudgetStatus,
    BudgetUpdate,
    CategoryBreakdown,
    CategoryBudget,
    CategoryBudgetRead,
    CategoryBudgetStatus,
    CategoryBudgetUpsert,
    CoachSummary,
    CsvImportPreviewResponse,
    CsvImportPreviewRow,
    CsvImportResult,
    DailySpendPoint,
    DueRecurringSummary,
    Expense,
    ExpenseCreate,
    ExpenseRead,
    InsightRead,
    MonthlySpendPoint,
    OverviewResponse,
    RecurringExpense,
    RecurringExpenseCreate,
    RecurringExpenseRead,
    RecurringExpenseUpdate,
    RecurringGenerationResponse,
    SavingsGoal,
    SavingsGoalCreate,
    SavingsGoalRead,
    SavingsGoalStatus,
    SavingsGoalUpdate,
    SummaryCard,
    User,
)
from expensemate.settings import settings



def extract_json_object(text: str) -> dict:
    text = (text or '').strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else None
    if candidate is None:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end + 1]
    if not candidate:
        return {}
    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}

DEFAULT_CATEGORIES = [
    'Food',
    'Transport',
    'Shopping',
    'Bills',
    'Health',
    'Education',
    'Entertainment',
    'Other',
]

PERIOD_LABELS = {
    'en': {
        'this_week': 'This week',
        'this_month': 'This month',
        'last_30_days': 'Last 30 days',
        'all_time': 'All time',
    },
    'ru': {
        'this_week': 'Эта неделя',
        'this_month': 'Этот месяц',
        'last_30_days': 'Последние 30 дней',
        'all_time': 'За всё время',
    },
}

CARD_LABELS = {
    'en': {
        'total': 'Total spent',
        'count': 'Expenses logged',
        'average': 'Average expense',
        'largest': 'Largest expense',
    },
    'ru': {
        'total': 'Всего потрачено',
        'count': 'Записей о тратах',
        'average': 'Средняя трата',
        'largest': 'Самая большая трата',
    },
}

MONTH_LABELS = {
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'ru': ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
}

CATEGORY_WORD_MAP = {
    'food': 'Food',
    'groceries': 'Food',
    'еда': 'Food',
    'продукты': 'Food',
    'transport': 'Transport',
    'taxi': 'Transport',
    'bus': 'Transport',
    'транспорт': 'Transport',
    'такси': 'Transport',
    'shopping': 'Shopping',
    'shop': 'Shopping',
    'покупки': 'Shopping',
    'шопинг': 'Shopping',
    'bills': 'Bills',
    'rent': 'Bills',
    'utilities': 'Bills',
    'счета': 'Bills',
    'аренда': 'Bills',
    'коммуналка': 'Bills',
    'health': 'Health',
    'medicine': 'Health',
    'здоровье': 'Health',
    'лекарства': 'Health',
    'education': 'Education',
    'study': 'Education',
    'учеба': 'Education',
    'обучение': 'Education',
    'entertainment': 'Entertainment',
    'movie': 'Entertainment',
    'развлечения': 'Entertainment',
    'кино': 'Entertainment',
    'other': 'Other',
    'другое': 'Other',
}

SUPPORTED_CATEGORY_PATTERN = '|'.join(sorted(map(re.escape, CATEGORY_WORD_MAP.keys()), key=len, reverse=True))
SUPPORTED_FREQUENCIES = ('weekly', 'monthly')

IMPORT_COLUMN_ALIASES = {
    'spent_on': {'date', 'spent_on', 'spent on', 'day', 'transaction date', 'expense date'},
    'description': {'description', 'details', 'merchant', 'title', 'name', 'note'},
    'category': {'category', 'type', 'group'},
    'amount': {'amount', 'sum', 'value', 'price', 'total', 'cost'},
}


@dataclass(slots=True)
class DateWindow:
    start: date | None
    end: date | None
    label: str


@dataclass(slots=True)
class ParsedImportRow:
    row_number: int
    spent_on: date | None = None
    description: str | None = None
    category: str | None = None
    amount: Decimal | None = None
    error_message: str | None = None
    is_duplicate: bool = False

    @property
    def is_valid(self) -> bool:
        return (
            self.error_message is None
            and self.spent_on is not None
            and self.description is not None
            and self.category is not None
            and self.amount is not None
        )


class ExpenseFilterParams:
    def __init__(
        self,
        *,
        category: str | None = None,
        search: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> None:
        self.category = category
        self.search = search
        self.start_date = start_date
        self.end_date = end_date


# ---------- General helpers ----------


def tr(lang: str, en: str, ru: str) -> str:
    return ru if lang == 'ru' else en



def detect_language(text: str, preferred: str | None = None) -> str:
    if preferred in {'en', 'ru'}:
        return preferred
    return 'ru' if re.search(r'[А-Яа-яЁё]', text or '') else 'en'



def q2(value: Decimal | int | float | str | None) -> Decimal:
    if value is None:
        return Decimal('0.00')
    if isinstance(value, Decimal):
        return value.quantize(Decimal('0.01'))
    return Decimal(str(value)).quantize(Decimal('0.01'))



def money_value(value: Decimal | int | float | str | None) -> str:
    return f'€{q2(value):.2f}'



def normalize_category(raw: str) -> str:
    value = raw.strip().lower()
    if value in CATEGORY_WORD_MAP:
        return CATEGORY_WORD_MAP[value]
    if not value:
        return 'Other'
    return raw.strip().title()



def category_label(category: str, lang: str) -> str:
    mapping = {
        'Food': tr(lang, 'Food', 'Еда'),
        'Transport': tr(lang, 'Transport', 'Транспорт'),
        'Shopping': tr(lang, 'Shopping', 'Покупки'),
        'Bills': tr(lang, 'Bills', 'Счета'),
        'Health': tr(lang, 'Health', 'Здоровье'),
        'Education': tr(lang, 'Education', 'Учёба'),
        'Entertainment': tr(lang, 'Entertainment', 'Развлечения'),
        'Other': tr(lang, 'Other', 'Другое'),
    }
    return mapping.get(category, category)



def get_window(period: str, lang: str = 'en') -> DateWindow:
    today = date.today()
    if period == 'this_week':
        start = today - timedelta(days=today.weekday())
        return DateWindow(start=start, end=today, label=PERIOD_LABELS[lang]['this_week'])
    if period == 'this_month':
        start = today.replace(day=1)
        return DateWindow(start=start, end=today, label=PERIOD_LABELS[lang]['this_month'])
    if period == 'last_30_days':
        return DateWindow(start=today - timedelta(days=29), end=today, label=PERIOD_LABELS[lang]['last_30_days'])
    return DateWindow(start=None, end=None, label=PERIOD_LABELS[lang]['all_time'])



def month_key_for(day: date) -> str:
    return f'{day.year:04d}-{day.month:02d}'



def month_label_for(day: date, lang: str = 'en') -> str:
    return f"{MONTH_LABELS[lang][day.month - 1]} {day.year}"



def iter_month_starts(months: int) -> list[date]:
    if months < 1:
        return []
    today = date.today().replace(day=1)
    result: list[date] = []
    year = today.year
    month = today.month
    for offset in range(months - 1, -1, -1):
        shifted_month = month - offset
        shifted_year = year
        while shifted_month <= 0:
            shifted_month += 12
            shifted_year -= 1
        result.append(date(shifted_year, shifted_month, 1))
    return result



def apply_period(query, period: str):
    window = get_window(period)
    if window.start is not None:
        query = query.where(Expense.spent_on >= window.start)
    if window.end is not None:
        query = query.where(Expense.spent_on <= window.end)
    return query



def apply_expense_filters(query, params: ExpenseFilterParams):
    if params.category:
        query = query.where(Expense.category == normalize_category(params.category))
    if params.search:
        query = query.where(Expense.description.ilike(f'%{params.search.strip()}%'))
    if params.start_date is not None:
        query = query.where(Expense.spent_on >= params.start_date)
    if params.end_date is not None:
        query = query.where(Expense.spent_on <= params.end_date)
    return query



def _unwrap_scalar(value):
    if hasattr(value, '_mapping'):
        return value[0]
    if isinstance(value, tuple):
        return value[0]
    return value



def _expense_scope(user: User):
    return Expense.user_id == user.id



def _recurring_scope(user: User):
    return RecurringExpense.user_id == user.id



def _budget_scope(user: User):
    return Budget.user_id == user.id



def _category_budget_scope(user: User):
    return CategoryBudget.user_id == user.id



def _goal_scope(user: User):
    return SavingsGoal.user_id == user.id



def advance_recurring_date(current: date, frequency: str) -> date:
    if frequency == 'weekly':
        return current + timedelta(days=7)
    year = current.year + (1 if current.month == 12 else 0)
    month = 1 if current.month == 12 else current.month + 1
    day = min(current.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)



def project_month_total(spent_this_month: Decimal) -> Decimal:
    today = date.today()
    days_elapsed = max(today.day, 1)
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    projected = (spent_this_month / Decimal(days_elapsed)) * Decimal(days_in_month)
    return q2(projected)


# ---------- Expenses ----------


async def list_expenses(
    session: AsyncSession,
    user: User,
    *,
    category: str | None = None,
    search: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Expense]:
    params = ExpenseFilterParams(
        category=category,
        search=search,
        start_date=start_date,
        end_date=end_date,
    )
    query = select(Expense).where(_expense_scope(user)).order_by(Expense.spent_on.desc(), Expense.id.desc())
    query = apply_expense_filters(query, params)
    result = await session.exec(query)
    return list(result.all())


async def create_expense(session: AsyncSession, user: User, payload: ExpenseCreate) -> Expense:
    expense = Expense(
        user_id=user.id,
        amount=q2(payload.amount),
        category=normalize_category(payload.category),
        description=payload.description.strip(),
        spent_on=payload.spent_on,
    )
    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return expense


async def update_expense(session: AsyncSession, user: User, expense_id: int, payload) -> Expense | None:
    expense = await session.get(Expense, expense_id)
    if expense is None or expense.user_id != user.id:
        return None
    expense.amount = q2(payload.amount)
    expense.category = normalize_category(payload.category)
    expense.description = payload.description.strip()
    expense.spent_on = payload.spent_on
    session.add(expense)
    await session.commit()
    await session.refresh(expense)
    return expense


async def delete_expense(session: AsyncSession, user: User, expense_id: int) -> bool:
    expense = await session.get(Expense, expense_id)
    if expense is None or expense.user_id != user.id:
        return False
    await session.delete(expense)
    await session.commit()
    return True


async def _existing_expense_signatures(session: AsyncSession, user: User) -> set[tuple[date, str, str, Decimal]]:
    result = await session.exec(select(Expense).where(_expense_scope(user)))
    expenses = list(result.all())
    return {
        (
            item.spent_on,
            item.description.strip().casefold(),
            normalize_category(item.category).casefold(),
            q2(item.amount),
        )
        for item in expenses
    }


# ---------- CSV import ----------


def _normalize_import_header(value: str) -> str:
    return ' '.join(value.strip().lower().replace('-', ' ').replace('_', ' ').split())



def _parse_import_amount(raw: str) -> Decimal:
    cleaned = raw.strip().replace('€', '').replace('$', '').replace('£', '').replace(' ', '')
    if not cleaned:
        raise ValueError('Amount is empty')
    if ',' in cleaned and '.' in cleaned:
        if cleaned.rfind(',') > cleaned.rfind('.'):
            cleaned = cleaned.replace('.', '').replace(',', '.')
        else:
            cleaned = cleaned.replace(',', '')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')
    amount = Decimal(cleaned)
    if amount <= 0:
        raise ValueError('Amount must be greater than zero')
    return q2(amount)



def _parse_import_date(raw: str) -> date:
    value = raw.strip()
    if not value:
        raise ValueError('Date is empty')
    date_formats = ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d', '%d-%m-%Y')
    for fmt in date_formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError('Unsupported date format')



def _detect_import_columns(fieldnames: list[str] | None) -> dict[str, str]:
    if not fieldnames:
        raise ValueError('CSV header row is required')

    normalized_to_original = {
        _normalize_import_header(name): name
        for name in fieldnames
        if name and name.strip()
    }
    resolved: dict[str, str] = {}
    for target, aliases in IMPORT_COLUMN_ALIASES.items():
        for alias in aliases:
            original = normalized_to_original.get(alias)
            if original:
                resolved[target] = original
                break
        if target not in resolved:
            raise ValueError(f'Missing required column: {target}')
    return resolved



def _parse_csv_text(csv_text: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    lines = [line for line in csv_text.splitlines() if line.strip()]
    if not lines:
        raise ValueError('CSV text is empty')

    sample = '\n'.join(lines[:5])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ','

    reader = csv.DictReader(lines, delimiter=delimiter)
    columns = _detect_import_columns(reader.fieldnames)
    rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError('CSV contains no data rows')
    return rows, columns



def _parse_import_rows(
    rows: list[dict[str, str]],
    columns: dict[str, str],
    existing_signatures: set[tuple[date, str, str, Decimal]],
) -> list[ParsedImportRow]:
    parsed_rows: list[ParsedImportRow] = []
    seen_signatures: set[tuple[date, str, str, Decimal]] = set()

    for index, row in enumerate(rows, start=2):
        try:
            spent_on = _parse_import_date(row.get(columns['spent_on'], '') or '')
            description = (row.get(columns['description'], '') or '').strip()
            category = normalize_category(row.get(columns['category'], '') or 'Other')
            amount = _parse_import_amount(row.get(columns['amount'], '') or '')
            if not description:
                raise ValueError('Description is empty')
            signature = (spent_on, description.casefold(), category.casefold(), amount)
            parsed = ParsedImportRow(
                row_number=index,
                spent_on=spent_on,
                description=description,
                category=category,
                amount=amount,
                is_duplicate=signature in existing_signatures or signature in seen_signatures,
            )
            seen_signatures.add(signature)
        except (ValueError, ArithmeticError, InvalidOperation) as error:
            parsed = ParsedImportRow(row_number=index, error_message=str(error))
        parsed_rows.append(parsed)

    return parsed_rows


async def preview_expense_csv_import(session: AsyncSession, user: User, csv_text: str) -> CsvImportPreviewResponse:
    rows, columns = _parse_csv_text(csv_text)
    existing_signatures = await _existing_expense_signatures(session, user)
    parsed_rows = _parse_import_rows(rows, columns, existing_signatures)
    valid_rows = sum(1 for item in parsed_rows if item.is_valid and not item.is_duplicate)
    duplicate_rows = sum(1 for item in parsed_rows if item.is_duplicate)
    invalid_rows = sum(1 for item in parsed_rows if not item.is_valid)
    return CsvImportPreviewResponse(
        detected_columns=columns,
        total_rows=len(parsed_rows),
        valid_rows=valid_rows,
        duplicate_rows=duplicate_rows,
        invalid_rows=invalid_rows,
        preview_rows=[
            CsvImportPreviewRow(
                row_number=item.row_number,
                spent_on=item.spent_on,
                description=item.description,
                category=item.category,
                amount=item.amount,
                is_valid=item.is_valid,
                is_duplicate=item.is_duplicate,
                error_message=item.error_message,
            )
            for item in parsed_rows[:30]
        ],
    )


async def import_expenses_from_csv(session: AsyncSession, user: User, csv_text: str) -> CsvImportResult:
    rows, columns = _parse_csv_text(csv_text)
    existing_signatures = await _existing_expense_signatures(session, user)
    parsed_rows = _parse_import_rows(rows, columns, existing_signatures)
    valid_rows = [item for item in parsed_rows if item.is_valid and not item.is_duplicate]
    expenses = [
        Expense(
            user_id=user.id,
            amount=item.amount,
            category=item.category,
            description=item.description,
            spent_on=item.spent_on,
        )
        for item in valid_rows
    ]
    if expenses:
        session.add_all(expenses)
        await session.commit()

    return CsvImportResult(
        imported_count=len(valid_rows),
        duplicate_rows=sum(1 for item in parsed_rows if item.is_duplicate),
        invalid_rows=sum(1 for item in parsed_rows if not item.is_valid),
        total_rows=len(parsed_rows),
    )


# ---------- Budgets ----------


async def get_budget(session: AsyncSession, user: User) -> BudgetRead:
    result = await session.exec(select(Budget).where(_budget_scope(user)).order_by(Budget.id.asc()).limit(1))
    budget = result.first()
    if budget is None:
        return BudgetRead(monthly_limit=None, updated_at=None)
    return BudgetRead(monthly_limit=budget.monthly_limit, updated_at=budget.updated_at)


async def set_budget(session: AsyncSession, user: User, payload: BudgetUpdate) -> BudgetRead:
    result = await session.exec(select(Budget).where(_budget_scope(user)).order_by(Budget.id.asc()).limit(1))
    budget = result.first()
    now = datetime.utcnow()
    if budget is None:
        budget = Budget(user_id=user.id, monthly_limit=q2(payload.monthly_limit), created_at=now, updated_at=now)
    else:
        budget.monthly_limit = q2(payload.monthly_limit)
        budget.updated_at = now
    session.add(budget)
    await session.commit()
    await session.refresh(budget)
    return BudgetRead(monthly_limit=budget.monthly_limit, updated_at=budget.updated_at)


async def list_category_budgets(session: AsyncSession, user: User) -> list[CategoryBudget]:
    query = select(CategoryBudget).where(_category_budget_scope(user)).order_by(CategoryBudget.category.asc())
    result = await session.exec(query)
    return list(result.all())


async def set_category_budget(session: AsyncSession, user: User, payload: CategoryBudgetUpsert) -> CategoryBudget:
    category = normalize_category(payload.category)
    query = select(CategoryBudget).where(_category_budget_scope(user)).where(CategoryBudget.category == category).limit(1)
    result = await session.exec(query)
    budget = result.first()
    now = datetime.utcnow()
    if budget is None:
        budget = CategoryBudget(
            user_id=user.id,
            category=category,
            monthly_limit=q2(payload.monthly_limit),
            created_at=now,
            updated_at=now,
        )
    else:
        budget.monthly_limit = q2(payload.monthly_limit)
        budget.updated_at = now
    session.add(budget)
    await session.commit()
    await session.refresh(budget)
    return budget


async def delete_category_budget(session: AsyncSession, user: User, category_budget_id: int) -> bool:
    item = await session.get(CategoryBudget, category_budget_id)
    if item is None or item.user_id != user.id:
        return False
    await session.delete(item)
    await session.commit()
    return True



def build_category_budget_read(item: CategoryBudget) -> CategoryBudgetRead:
    return CategoryBudgetRead(
        id=item.id,
        category=item.category,
        monthly_limit=item.monthly_limit,
        updated_at=item.updated_at,
    )


async def category_budget_statuses(session: AsyncSession, user: User) -> list[CategoryBudgetStatus]:
    budgets = await list_category_budgets(session, user)
    if not budgets:
        return []

    query = apply_period(
        select(Expense.category, func.coalesce(func.sum(Expense.amount), 0))
        .where(_expense_scope(user))
        .group_by(Expense.category),
        'this_month',
    )
    result = await session.exec(query)
    spent_by_category = {row[0]: q2(row[1]) for row in result.all()}

    statuses: list[CategoryBudgetStatus] = []
    for item in budgets:
        spent = spent_by_category.get(item.category, Decimal('0.00'))
        remaining = q2(item.monthly_limit - spent)
        percent_used = int(min((spent / item.monthly_limit) * Decimal('100'), Decimal('999'))) if item.monthly_limit > 0 else 0
        statuses.append(
            CategoryBudgetStatus(
                id=item.id,
                category=item.category,
                monthly_limit=item.monthly_limit,
                spent_this_month=spent,
                remaining_amount=remaining,
                percent_used=percent_used,
                is_over_budget=remaining < 0,
            )
        )
    statuses.sort(key=lambda entry: (entry.is_over_budget, entry.percent_used, entry.spent_this_month), reverse=True)
    return statuses


async def current_budget_status(session: AsyncSession, user: User) -> BudgetStatus | None:
    budget = await get_budget(session, user)
    if budget.monthly_limit is None:
        return None

    month_query = apply_period(select(func.coalesce(func.sum(Expense.amount), 0)).where(_expense_scope(user)), 'this_month')
    spent_this_month = q2(_unwrap_scalar((await session.exec(month_query)).one()) or 0)
    remaining = q2(budget.monthly_limit - spent_this_month)
    percent_used = int(min((spent_this_month / budget.monthly_limit) * Decimal('100'), Decimal('999'))) if budget.monthly_limit > 0 else 0
    projected_total = project_month_total(spent_this_month)
    projected_percent = int(min((projected_total / budget.monthly_limit) * Decimal('100'), Decimal('999'))) if budget.monthly_limit > 0 else 0
    return BudgetStatus(
        monthly_limit=budget.monthly_limit,
        spent_this_month=spent_this_month,
        remaining_amount=remaining,
        percent_used=percent_used,
        is_over_budget=remaining < 0,
        projected_total=projected_total,
        projected_percent_used=projected_percent,
    )


# ---------- Goals ----------


async def list_goals(session: AsyncSession, user: User) -> list[SavingsGoal]:
    result = await session.exec(select(SavingsGoal).where(_goal_scope(user)).order_by(SavingsGoal.target_date.asc().nulls_last(), SavingsGoal.id.asc()))
    return list(result.all())


async def create_goal(session: AsyncSession, user: User, payload: SavingsGoalCreate) -> SavingsGoal:
    now = datetime.utcnow()
    goal = SavingsGoal(
        user_id=user.id,
        title=payload.title.strip(),
        target_amount=q2(payload.target_amount),
        current_amount=q2(payload.current_amount),
        target_date=payload.target_date,
        note=payload.note.strip(),
        created_at=now,
        updated_at=now,
    )
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return goal


async def update_goal(session: AsyncSession, user: User, goal_id: int, payload: SavingsGoalUpdate) -> SavingsGoal | None:
    goal = await session.get(SavingsGoal, goal_id)
    if goal is None or goal.user_id != user.id:
        return None
    goal.title = payload.title.strip()
    goal.target_amount = q2(payload.target_amount)
    goal.current_amount = q2(payload.current_amount)
    goal.target_date = payload.target_date
    goal.note = payload.note.strip()
    goal.updated_at = datetime.utcnow()
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return goal


async def delete_goal(session: AsyncSession, user: User, goal_id: int) -> bool:
    goal = await session.get(SavingsGoal, goal_id)
    if goal is None or goal.user_id != user.id:
        return False
    await session.delete(goal)
    await session.commit()
    return True



def build_goal_read(goal: SavingsGoal) -> SavingsGoalRead:
    return SavingsGoalRead(
        id=goal.id,
        title=goal.title,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        target_date=goal.target_date,
        note=goal.note,
        created_at=goal.created_at,
        updated_at=goal.updated_at,
    )



def _months_until(target_date: date | None) -> int | None:
    if target_date is None:
        return None
    today = date.today()
    if target_date <= today:
        return 1
    months = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    if target_date.day >= today.day:
        months += 1
    return max(months, 1)


async def goal_statuses(session: AsyncSession, user: User) -> list[SavingsGoalStatus]:
    goals = await list_goals(session, user)
    statuses: list[SavingsGoalStatus] = []
    for goal in goals:
        remaining = q2(goal.target_amount - goal.current_amount)
        progress_percent = int(min((goal.current_amount / goal.target_amount) * Decimal('100'), Decimal('100'))) if goal.target_amount > 0 else 0
        months_until = _months_until(goal.target_date)
        monthly_required = None if remaining <= 0 else (q2(remaining / Decimal(months_until)) if months_until else None)
        statuses.append(
            SavingsGoalStatus(
                id=goal.id,
                title=goal.title,
                target_amount=goal.target_amount,
                current_amount=goal.current_amount,
                remaining_amount=remaining if remaining > 0 else Decimal('0.00'),
                progress_percent=progress_percent,
                target_date=goal.target_date,
                monthly_required=monthly_required,
                is_completed=goal.current_amount >= goal.target_amount,
                note=goal.note,
            )
        )
    return statuses


async def add_to_goal(session: AsyncSession, user: User, goal_id: int, amount: Decimal) -> SavingsGoal | None:
    goal = await session.get(SavingsGoal, goal_id)
    if goal is None or goal.user_id != user.id:
        return None
    goal.current_amount = q2(goal.current_amount + amount)
    goal.updated_at = datetime.utcnow()
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    return goal


async def find_goal_by_title(session: AsyncSession, user: User, title_fragment: str) -> SavingsGoal | None:
    title_fragment = title_fragment.strip().lower()
    if not title_fragment:
        return None
    goals = await list_goals(session, user)
    exact = next((goal for goal in goals if goal.title.strip().lower() == title_fragment), None)
    if exact:
        return exact
    return next((goal for goal in goals if title_fragment in goal.title.strip().lower()), None)


# ---------- Recurring ----------


async def list_recurring_expenses(session: AsyncSession, user: User, *, include_inactive: bool = True) -> list[RecurringExpense]:
    query = select(RecurringExpense).where(_recurring_scope(user)).order_by(RecurringExpense.next_due_on.asc(), RecurringExpense.id.asc())
    if not include_inactive:
        query = query.where(RecurringExpense.is_active.is_(True))
    result = await session.exec(query)
    return list(result.all())


async def create_recurring_expense(session: AsyncSession, user: User, payload: RecurringExpenseCreate) -> RecurringExpense:
    now = datetime.utcnow()
    recurring = RecurringExpense(
        user_id=user.id,
        amount=q2(payload.amount),
        category=normalize_category(payload.category),
        description=payload.description.strip(),
        frequency=payload.frequency,
        start_date=payload.start_date,
        next_due_on=payload.start_date,
        created_at=now,
        updated_at=now,
    )
    session.add(recurring)
    await session.commit()
    await session.refresh(recurring)
    return recurring


async def update_recurring_expense(session: AsyncSession, user: User, recurring_id: int, payload: RecurringExpenseUpdate) -> RecurringExpense | None:
    recurring = await session.get(RecurringExpense, recurring_id)
    if recurring is None or recurring.user_id != user.id:
        return None
    recurring.amount = q2(payload.amount)
    recurring.category = normalize_category(payload.category)
    recurring.description = payload.description.strip()
    recurring.frequency = payload.frequency
    recurring.start_date = payload.start_date
    recurring.is_active = payload.is_active
    if recurring.last_generated_on is None:
        recurring.next_due_on = payload.start_date
    elif recurring.next_due_on < recurring.last_generated_on:
        recurring.next_due_on = advance_recurring_date(recurring.last_generated_on, payload.frequency)
    recurring.updated_at = datetime.utcnow()
    session.add(recurring)
    await session.commit()
    await session.refresh(recurring)
    return recurring


async def delete_recurring_expense(session: AsyncSession, user: User, recurring_id: int) -> bool:
    recurring = await session.get(RecurringExpense, recurring_id)
    if recurring is None or recurring.user_id != user.id:
        return False
    await session.delete(recurring)
    await session.commit()
    return True


async def generate_due_recurring_expenses(session: AsyncSession, user: User, *, through_date: date | None = None) -> RecurringGenerationResponse:
    through = through_date or date.today()
    query = (
        select(RecurringExpense)
        .where(_recurring_scope(user))
        .where(RecurringExpense.is_active.is_(True))
        .where(RecurringExpense.next_due_on <= through)
        .order_by(RecurringExpense.next_due_on.asc(), RecurringExpense.id.asc())
    )
    result = await session.exec(query)
    templates = list(result.all())

    created_ids: list[int] = []
    for recurring in templates:
        while recurring.next_due_on <= through:
            expense = Expense(
                user_id=user.id,
                amount=recurring.amount,
                category=recurring.category,
                description=recurring.description,
                spent_on=recurring.next_due_on,
            )
            session.add(expense)
            await session.flush()
            created_ids.append(expense.id or 0)
            recurring.last_generated_on = recurring.next_due_on
            recurring.next_due_on = advance_recurring_date(recurring.next_due_on, recurring.frequency)
            recurring.updated_at = datetime.utcnow()
            session.add(recurring)

    await session.commit()
    return RecurringGenerationResponse(created_count=len(created_ids), created_expense_ids=created_ids, through_date=through)


async def due_recurring_summary(session: AsyncSession, user: User, *, days: int = 7) -> DueRecurringSummary:
    today = date.today()
    end = today + timedelta(days=max(days, 0))
    base = select(RecurringExpense).where(_recurring_scope(user)).where(RecurringExpense.is_active.is_(True))
    due_today_query = base.where(RecurringExpense.next_due_on <= today)
    due_next_query = base.where(RecurringExpense.next_due_on <= end)
    next_items_query = base.order_by(RecurringExpense.next_due_on.asc(), RecurringExpense.id.asc()).limit(5)

    due_today = len((await session.exec(due_today_query)).all())
    due_next = len((await session.exec(due_next_query)).all())
    items = [build_recurring_read(item) for item in (await session.exec(next_items_query)).all()]
    return DueRecurringSummary(due_today_count=due_today, due_next_7_days_count=due_next, next_due_items=items)


# ---------- Analytics ----------


async def overview(session: AsyncSession, user: User, *, period: str, lang: str = 'en') -> OverviewResponse:
    window = get_window(period, lang)
    total_query = apply_period(select(func.coalesce(func.sum(Expense.amount), 0)).where(_expense_scope(user)), period)
    count_query = apply_period(select(func.count(Expense.id)).where(_expense_scope(user)), period)
    max_query = apply_period(select(func.max(Expense.amount)).where(_expense_scope(user)), period)

    total = q2(_unwrap_scalar((await session.exec(total_query)).one()) or 0)
    count = int(_unwrap_scalar((await session.exec(count_query)).one()) or 0)
    max_result = await session.exec(max_query)
    max_value = q2(_unwrap_scalar(max_result.one()) or 0)
    average = q2(total / Decimal(count)) if count else Decimal('0.00')

    cards = [
        SummaryCard(label=CARD_LABELS[lang]['total'], value=money_value(total), help_text=window.label),
        SummaryCard(label=CARD_LABELS[lang]['count'], value=str(count), help_text=tr(lang, 'Number of saved records', 'Количество сохранённых записей')),
        SummaryCard(label=CARD_LABELS[lang]['average'], value=money_value(average), help_text=tr(lang, 'Average per expense', 'Среднее значение одной траты')),
        SummaryCard(label=CARD_LABELS[lang]['largest'], value=money_value(max_value), help_text=tr(lang, 'Highest single expense in the selected period', 'Самая крупная трата за выбранный период')),
    ]
    return OverviewResponse(
        period_label=window.label,
        cards=cards,
        budget_status=await current_budget_status(session, user),
        category_budget_statuses=await category_budget_statuses(session, user),
        due_recurring_summary=await due_recurring_summary(session, user),
        goals=await goal_statuses(session, user),
    )


async def category_breakdown(session: AsyncSession, user: User, *, period: str) -> list[CategoryBreakdown]:
    query = apply_period(
        select(Expense.category, func.coalesce(func.sum(Expense.amount), 0), func.count(Expense.id))
        .where(_expense_scope(user))
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc()),
        period,
    )
    result = await session.exec(query)
    return [CategoryBreakdown(category=row[0], total_amount=q2(row[1]), count=row[2]) for row in result.all()]


async def daily_spending(session: AsyncSession, user: User, *, days: int = 14) -> list[DailySpendPoint]:
    start = date.today() - timedelta(days=max(days - 1, 0))
    query = (
        select(Expense.spent_on, func.coalesce(func.sum(Expense.amount), 0))
        .where(_expense_scope(user))
        .where(Expense.spent_on >= start)
        .group_by(Expense.spent_on)
        .order_by(Expense.spent_on.asc())
    )
    result = await session.exec(query)
    totals = {row[0]: q2(row[1]) for row in result.all()}
    return [DailySpendPoint(day=start + timedelta(days=offset), total_amount=totals.get(start + timedelta(days=offset), Decimal('0.00'))) for offset in range(days)]


async def monthly_spending(session: AsyncSession, user: User, *, months: int = 6, lang: str = 'en') -> list[MonthlySpendPoint]:
    months = max(1, min(months, 24))
    starts = iter_month_starts(months)
    if not starts:
        return []

    start = starts[0]
    result = await session.exec(select(Expense).where(_expense_scope(user)).where(Expense.spent_on >= start).order_by(Expense.spent_on.asc(), Expense.id.asc()))
    expenses = list(result.all())

    totals: dict[str, Decimal] = {month_key_for(item): Decimal('0.00') for item in starts}
    labels: dict[str, str] = {month_key_for(item): month_label_for(item, lang) for item in starts}

    for expense in expenses:
        key = month_key_for(expense.spent_on)
        if key in totals:
            totals[key] += q2(expense.amount)

    return [MonthlySpendPoint(month_key=month_key_for(item), month_label=labels[month_key_for(item)], total_amount=q2(totals[month_key_for(item)])) for item in starts]


async def spending_insights(session: AsyncSession, user: User, lang: str = 'en') -> list[InsightRead]:
    insights: list[InsightRead] = []
    this_month_categories = await category_breakdown(session, user, period='this_month')
    if this_month_categories:
        top = this_month_categories[0]
        insights.append(
            InsightRead(
                title=tr(lang, 'Top category this month', 'Главная категория месяца'),
                detail=tr(
                    lang,
                    f'{category_label(top.category, lang)} leads with {money_value(top.total_amount)} across {top.count} expense(s).',
                    f'Категория {category_label(top.category, lang)} лидирует: {money_value(top.total_amount)} и {top.count} трат(ы).',
                ),
                tone='neutral',
            )
        )

    monthly_points = await monthly_spending(session, user, months=2, lang=lang)
    if len(monthly_points) == 2:
        previous, current = monthly_points
        current_total = q2(current.total_amount)
        previous_total = q2(previous.total_amount)
        diff = q2(current_total - previous_total)
        if previous_total == 0 and current_total > 0:
            detail = tr(lang, f'Spending started at {money_value(current_total)} this month after no spending in {previous.month_label}.', f'В этом месяце траты появились и уже составили {money_value(current_total)}, тогда как в {previous.month_label} их не было.')
            tone = 'warning'
        elif diff > 0:
            detail = tr(lang, f'You are spending {money_value(diff)} more than in {previous.month_label}.', f'Ты тратишь на {money_value(diff)} больше, чем в {previous.month_label}.')
            tone = 'warning'
        elif diff < 0:
            detail = tr(lang, f'You are spending {money_value(abs(diff))} less than in {previous.month_label}.', f'Ты тратишь на {money_value(abs(diff))} меньше, чем в {previous.month_label}.')
            tone = 'positive'
        else:
            detail = tr(lang, f'Spending matches {previous.month_label} exactly so far.', f'Пока траты совпадают с {previous.month_label}.')
            tone = 'neutral'
        insights.append(InsightRead(title=tr(lang, 'Month-over-month change', 'Сравнение с прошлым месяцем'), detail=detail, tone=tone))

    budget_status = await current_budget_status(session, user)
    if budget_status is not None:
        if budget_status.is_over_budget:
            detail = tr(lang, f'You are already over budget by {money_value(abs(budget_status.remaining_amount))}.', f'Ты уже вышел за бюджет на {money_value(abs(budget_status.remaining_amount))}.')
            tone = 'warning'
        elif budget_status.projected_percent_used and budget_status.projected_percent_used > 100:
            detail = tr(lang, f'At the current pace you may finish the month at {money_value(budget_status.projected_total)}.', f'Если траты пойдут в том же темпе, месяц закончится на уровне {money_value(budget_status.projected_total)}.')
            tone = 'warning'
        else:
            detail = tr(lang, f'{money_value(budget_status.remaining_amount)} remains in your monthly budget.', f'В месячном бюджете осталось {money_value(budget_status.remaining_amount)}.')
            tone = 'positive'
        insights.append(InsightRead(title=tr(lang, 'Budget status', 'Статус бюджета'), detail=detail, tone=tone))

    category_statuses = await category_budget_statuses(session, user)
    over_budget = [item for item in category_statuses if item.is_over_budget]
    near_limit = [item for item in category_statuses if not item.is_over_budget and item.percent_used >= 85]
    if over_budget:
        names = ', '.join(category_label(item.category, lang) for item in over_budget[:3])
        insights.append(InsightRead(title=tr(lang, 'Category budgets need attention', 'Лимиты по категориям требуют внимания'), detail=tr(lang, f'You are over budget in: {names}.', f'Превышение лимита в категориях: {names}.'), tone='warning'))
    elif near_limit:
        most_used = near_limit[0]
        insights.append(InsightRead(title=tr(lang, 'Category budget almost reached', 'Категорийный лимит почти исчерпан'), detail=tr(lang, f'{category_label(most_used.category, lang)} is already at {most_used.percent_used}% with {money_value(most_used.remaining_amount)} left.', f'Категория {category_label(most_used.category, lang)} уже использовала {most_used.percent_used}% лимита, осталось {money_value(most_used.remaining_amount)}.'), tone='warning'))

    goal_items = await goal_statuses(session, user)
    active_goal = next((goal for goal in goal_items if not goal.is_completed), None)
    if active_goal is not None:
        detail = tr(
            lang,
            f'Goal “{active_goal.title}” is {active_goal.progress_percent}% funded with {money_value(active_goal.remaining_amount)} left.',
            f'Цель «{active_goal.title}» закрыта на {active_goal.progress_percent}%, осталось {money_value(active_goal.remaining_amount)}.',
        )
        insights.append(InsightRead(title=tr(lang, 'Savings goal progress', 'Прогресс по цели'), detail=detail, tone='positive' if active_goal.progress_percent >= 50 else 'neutral'))

    due_summary = await due_recurring_summary(session, user)
    if due_summary.due_next_7_days_count > 0:
        due_cutoff = date.today() + timedelta(days=7)
        due_total = q2(sum((q2(item.amount) for item in due_summary.next_due_items if item.next_due_on <= due_cutoff), Decimal('0.00')))
        insights.append(InsightRead(title=tr(lang, 'Recurring due soon', 'Скоро списания'), detail=tr(lang, f'{due_summary.due_next_7_days_count} recurring expense(s) are due within 7 days for about {money_value(due_total)} total.', f'В течение 7 дней ожидается {due_summary.due_next_7_days_count} регулярных списаний примерно на {money_value(due_total)}.'), tone='neutral'))

    if not insights:
        insights.append(InsightRead(title=tr(lang, 'Not enough data yet', 'Пока мало данных'), detail=tr(lang, 'Add a few expenses or seed demo data to unlock personalized insights.', 'Добавь несколько трат или демо-данные, чтобы увидеть персональные подсказки.'), tone='neutral'))

    return insights[:5]


async def coach_summary(session: AsyncSession, user: User, lang: str = 'en') -> CoachSummary:
    budget = await current_budget_status(session, user)
    categories = await category_budget_statuses(session, user)
    goals = await goal_statuses(session, user)
    due = await due_recurring_summary(session, user)
    insights = await spending_insights(session, user, lang)

    score = 82
    wins: list[str] = []
    risks: list[str] = []
    next_actions: list[str] = []

    if budget is None:
        score -= 8
        risks.append(tr(lang, 'No monthly budget is set yet.', 'Месячный бюджет пока не установлен.'))
        next_actions.append(tr(lang, 'Set a monthly budget so the app can forecast the rest of the month.', 'Установи месячный бюджет, чтобы приложение могло прогнозировать остаток месяца.'))
    else:
        if budget.is_over_budget:
            score -= 25
            risks.append(tr(lang, f'You are over budget by {money_value(abs(budget.remaining_amount))}.', f'Ты вышел за бюджет на {money_value(abs(budget.remaining_amount))}.'))
        elif budget.percent_used <= 65:
            wins.append(tr(lang, f'You are using only {budget.percent_used}% of your monthly budget.', f'Использовано только {budget.percent_used}% месячного бюджета.'))
        if budget.projected_percent_used and budget.projected_percent_used > 100:
            score -= 12
            next_actions.append(tr(lang, f'At the current pace you may finish near {money_value(budget.projected_total)}. Slow down in your top categories.', f'При текущем темпе месяц может закончиться на уровне {money_value(budget.projected_total)}. Стоит снизить траты в главных категориях.'))

    over_categories = [item for item in categories if item.is_over_budget]
    if over_categories:
        score -= min(18, len(over_categories) * 8)
        risks.append(tr(lang, f'Category budgets exceeded: {", ".join(category_label(item.category, lang) for item in over_categories[:3])}.', f'Превышены лимиты по категориям: {", ".join(category_label(item.category, lang) for item in over_categories[:3])}.'))
    elif categories:
        wins.append(tr(lang, 'Category budgets are helping keep spending under control.', 'Лимиты по категориям помогают держать траты под контролем.'))

    if due.due_next_7_days_count > 0:
        next_actions.append(tr(lang, f'{due.due_next_7_days_count} recurring charge(s) are due soon. Consider generating them and checking cash flow.', f'Скоро ожидается {due.due_next_7_days_count} регулярных списаний. Сгенерируй их и проверь свободный остаток.'))

    if goals:
        completed = [goal for goal in goals if goal.is_completed]
        active = [goal for goal in goals if not goal.is_completed]
        if completed:
            score += 5
            wins.append(tr(lang, f'Completed goals: {", ".join(goal.title for goal in completed[:2])}.', f'Завершённые цели: {", ".join(goal.title for goal in completed[:2])}.'))
        if active:
            nearest = active[0]
            if nearest.monthly_required and budget and nearest.monthly_required > q2(max(budget.remaining_amount, Decimal('0.00'))):
                score -= 8
                risks.append(tr(lang, f'Goal “{nearest.title}” needs about {money_value(nearest.monthly_required)} per month, which is higher than your current free budget.', f'Для цели «{nearest.title}» нужно около {money_value(nearest.monthly_required)} в месяц, что больше текущего свободного остатка бюджета.'))
            else:
                wins.append(tr(lang, f'Goal “{nearest.title}” is moving forward.', f'Цель «{nearest.title}» движется вперёд.'))
    else:
        next_actions.append(tr(lang, 'Create a savings goal to turn the tracker into a real financial planner.', 'Создай цель накоплений, чтобы трекер стал полноценным финансовым планировщиком.'))

    if len(insights) > 0 and not wins:
        wins.append(insights[0].detail)
    if len(insights) > 1 and not risks:
        risks.append(insights[1].detail)

    score = max(25, min(100, score))
    if score >= 85:
        headline = tr(lang, 'Your finances look stable this month.', 'В этом месяце финансовая картина выглядит устойчиво.')
    elif score >= 65:
        headline = tr(lang, 'You are doing well, but a few categories need attention.', 'В целом всё неплохо, но нескольким категориям нужно внимание.')
    else:
        headline = tr(lang, 'You should tighten control over spending and upcoming commitments.', 'Стоит сильнее контролировать траты и ближайшие обязательства.')

    return CoachSummary(
        health_score=score,
        headline=headline,
        wins=wins[:3],
        risks=risks[:3],
        next_actions=next_actions[:4],
    )


async def available_categories(session: AsyncSession, user: User) -> list[str]:
    expense_query = select(Expense.category).where(_expense_scope(user)).distinct()
    recurring_query = select(RecurringExpense.category).where(_recurring_scope(user)).distinct()
    category_budget_query = select(CategoryBudget.category).where(_category_budget_scope(user)).distinct()
    expense_values = [_unwrap_scalar(row) for row in (await session.exec(expense_query)).all() if _unwrap_scalar(row)]
    recurring_values = [_unwrap_scalar(row) for row in (await session.exec(recurring_query)).all() if _unwrap_scalar(row)]
    category_budget_values = [_unwrap_scalar(row) for row in (await session.exec(category_budget_query)).all() if _unwrap_scalar(row)]
    return sorted(set(DEFAULT_CATEGORIES + expense_values + recurring_values + category_budget_values))



async def seed_demo_data(session: AsyncSession, user: User) -> dict[str, int]:
    today = date.today()

    demo_expenses = [
        ExpenseCreate(amount=Decimal('5.20'), category='Food', description='Coffee', spent_on=today),
        ExpenseCreate(amount=Decimal('24.90'), category='Transport', description='Monthly bus top-up', spent_on=today - timedelta(days=1)),
        ExpenseCreate(amount=Decimal('48.00'), category='Shopping', description='T-shirt', spent_on=today - timedelta(days=3)),
        ExpenseCreate(amount=Decimal('13.50'), category='Food', description='Lunch', spent_on=today - timedelta(days=4)),
        ExpenseCreate(amount=Decimal('62.00'), category='Bills', description='Phone bill', spent_on=today - timedelta(days=6)),
        ExpenseCreate(amount=Decimal('18.70'), category='Entertainment', description='Cinema', spent_on=today - timedelta(days=8)),
    ]
    demo_recurring = [
        RecurringExpenseCreate(amount=Decimal('15.00'), category='Bills', description='Music subscription', frequency='monthly', start_date=today.replace(day=1)),
        RecurringExpenseCreate(amount=Decimal('320.00'), category='Bills', description='Rent', frequency='monthly', start_date=today.replace(day=1)),
    ]
    demo_category_budgets = [
        CategoryBudgetUpsert(category='Food', monthly_limit=Decimal('120.00')),
        CategoryBudgetUpsert(category='Transport', monthly_limit=Decimal('60.00')),
        CategoryBudgetUpsert(category='Bills', monthly_limit=Decimal('450.00')),
    ]
    demo_goals = [
        SavingsGoalCreate(title='Trip to Prague', target_amount=Decimal('900.00'), current_amount=Decimal('250.00'), target_date=today + timedelta(days=180), note='Summer vacation'),
        SavingsGoalCreate(title='Emergency fund', target_amount=Decimal('1500.00'), current_amount=Decimal('420.00'), target_date=today + timedelta(days=240), note='3-month safety cushion'),
    ]

    existing_expenses = await list_expenses(session, user)
    existing_expense_keys = {(item.description.strip().lower(), item.spent_on, Decimal(item.amount).quantize(Decimal('0.01'))) for item in existing_expenses}
    created_expenses = 0
    for item in demo_expenses:
        key = (item.description.strip().lower(), item.spent_on, Decimal(item.amount).quantize(Decimal('0.01')))
        if key in existing_expense_keys:
            continue
        await create_expense(session, user, item)
        existing_expense_keys.add(key)
        created_expenses += 1

    existing_recurring = await list_recurring_expenses(session, user, include_inactive=True)
    existing_recurring_keys = {(item.description.strip().lower(), item.frequency, Decimal(item.amount).quantize(Decimal('0.01'))) for item in existing_recurring}
    created_recurring = 0
    for item in demo_recurring:
        key = (item.description.strip().lower(), item.frequency, Decimal(item.amount).quantize(Decimal('0.01')))
        if key in existing_recurring_keys:
            continue
        await create_recurring_expense(session, user, item)
        existing_recurring_keys.add(key)
        created_recurring += 1

    budget = await get_budget(session, user)
    if budget.monthly_limit is None:
        await set_budget(session, user, BudgetUpdate(monthly_limit=Decimal('650.00')))
        budget_created = 1
    else:
        budget_created = 0

    existing_category_budgets = await list_category_budgets(session, user)
    existing_budget_categories = {item.category for item in existing_category_budgets}
    created_category_budgets = 0
    for item in demo_category_budgets:
        if item.category in existing_budget_categories:
            continue
        await set_category_budget(session, user, item)
        existing_budget_categories.add(item.category)
        created_category_budgets += 1

    existing_goals = await list_goals(session, user)
    existing_goal_titles = {item.title.strip().lower() for item in existing_goals}
    created_goals = 0
    for item in demo_goals:
        if item.title.strip().lower() in existing_goal_titles:
            continue
        await create_goal(session, user, item)
        existing_goal_titles.add(item.title.strip().lower())
        created_goals += 1

    return {
        'created_expenses': created_expenses,
        'created_recurring': created_recurring,
        'created_category_budgets': created_category_budgets,
        'created_goals': created_goals,
        'created_budget': budget_created,
    }


# ---------- Read models ----------



def build_expense_read(expense: Expense) -> ExpenseRead:
    return ExpenseRead(
        id=expense.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        spent_on=expense.spent_on,
        created_at=expense.created_at,
    )



def build_recurring_read(recurring: RecurringExpense) -> RecurringExpenseRead:
    return RecurringExpenseRead(
        id=recurring.id,
        amount=recurring.amount,
        category=recurring.category,
        description=recurring.description,
        frequency=recurring.frequency,
        start_date=recurring.start_date,
        next_due_on=recurring.next_due_on,
        last_generated_on=recurring.last_generated_on,
        is_active=recurring.is_active,
        created_at=recurring.created_at,
        updated_at=recurring.updated_at,
    )


# ---------- Assistant parsing ----------



def _extract_amount(text: str) -> Decimal | None:
    match = re.search(r'(\d+(?:[.,]\d{1,2})?)', text)
    if not match:
        return None
    return q2(match.group(1).replace(',', '.'))



def _extract_frequency(text: str) -> str | None:
    lowered = text.lower()
    if any(token in lowered for token in ('weekly', 'every week', 'each week', 'еженед', 'каждую неделю')):
        return 'weekly'
    if any(token in lowered for token in ('monthly', 'every month', 'each month', 'ежемесяч', 'каждый месяц')):
        return 'monthly'
    return None



def _extract_category_from_text(text: str) -> str | None:
    lowered = text.lower()
    match = re.search(rf'\b({SUPPORTED_CATEGORY_PATTERN})\b', lowered)
    if not match:
        return None
    return normalize_category(match.group(1))



def parse_assistant_add_command(message: str) -> ExpenseCreate | None:
    normalized = message.strip().lower()
    if not any(keyword in normalized for keyword in ('add', 'spent', 'log', 'добав', 'потрат', 'запиши', 'трата')):
        return None
    if 'recurring' in normalized or 'регуляр' in normalized or 'goal' in normalized or 'цель' in normalized:
        return None
    amount = _extract_amount(message)
    if amount is None:
        return None
    category = _extract_category_from_text(message) or 'Other'
    description = message
    cleanup = ('add', 'spent', 'log', 'expense', 'for', 'on', 'добавь', 'добавить', 'потратил', 'потратилa', 'трата', 'запиши', 'расход')
    for token in cleanup:
        description = re.sub(rf'\b{re.escape(token)}\b', '', description, flags=re.IGNORECASE)
    if category:
        description = re.sub(category, '', description, flags=re.IGNORECASE)
    description = re.sub(r'\d+(?:[.,]\d{1,2})?', '', description).strip(' -:,.')
    if not description:
        description = f'{category} expense'
    return ExpenseCreate(amount=amount, category=category, description=description, spent_on=date.today())



def parse_budget_command(message: str) -> Decimal | None:
    lowered = message.lower()
    if 'budget' not in lowered and 'бюджет' not in lowered:
        return None
    if not any(word in lowered for word in ('set', 'update', 'change', 'budget', 'установ', 'измени', 'постав')):
        return None
    return _extract_amount(message)



def parse_category_budget_command(message: str) -> CategoryBudgetUpsert | None:
    lowered = message.lower().strip()
    if 'budget' not in lowered and 'бюджет' not in lowered and 'лимит' not in lowered:
        return None
    amount = _extract_amount(message)
    category = _extract_category_from_text(message)
    if amount is None or category is None:
        return None
    if not any(keyword in lowered for keyword in ('set', 'change', 'update', 'limit', 'budget', 'установ', 'измени', 'лимит', 'категор')):
        return None
    return CategoryBudgetUpsert(category=category, monthly_limit=amount)



def parse_recurring_command(message: str) -> RecurringExpenseCreate | None:
    lowered = message.lower().strip()
    if not any(token in lowered for token in ('recurring', 'every month', 'every week', 'monthly', 'weekly', 'регуляр', 'ежемесяч', 'еженед', 'подписк')):
        return None
    if not any(keyword in lowered for keyword in ('add', 'create', 'set', 'track', 'добав', 'создай', 'отслеж')):
        return None
    amount = _extract_amount(message)
    frequency = _extract_frequency(message) or 'monthly'
    if amount is None:
        return None
    category = _extract_category_from_text(message) or 'Other'
    description = message
    cleanup_tokens = ('add', 'create', 'set', 'track', 'recurring', 'expense', 'every month', 'every week', 'monthly', 'weekly', 'for', 'on', 'добавь', 'создай', 'регулярный', 'ежемесячный', 'еженедельный', 'подписка', 'расход')
    for token in cleanup_tokens:
        description = re.sub(rf'\b{re.escape(token)}\b', '', description, flags=re.IGNORECASE)
    description = re.sub(r'\d+(?:[.,]\d{1,2})?', '', description).strip(' -:,.')
    if not description:
        description = f'{category} recurring expense'
    return RecurringExpenseCreate(amount=amount, category=category, description=description, frequency=frequency, start_date=date.today())



def parse_goal_create_command(message: str) -> SavingsGoalCreate | None:
    lowered = message.lower().strip()
    if not any(keyword in lowered for keyword in ('goal', 'цель', 'копилк')):
        return None
    if not any(keyword in lowered for keyword in ('create', 'set', 'add', 'save for', 'создай', 'добавь', 'хочу накопить', 'накопить')):
        return None
    amount = _extract_amount(message)
    if amount is None:
        return None
    date_match = re.search(r'(20\d{2}-\d{2}-\d{2})', message)
    target_date = datetime.strptime(date_match.group(1), '%Y-%m-%d').date() if date_match else None
    title = re.sub(r'(create|set|add|goal|save for|by|создай|добавь|цель|к|до|накопить)', ' ', message, flags=re.IGNORECASE)
    title = re.sub(r'20\d{2}-\d{2}-\d{2}', ' ', title)
    title = re.sub(r'\d+(?:[.,]\d{1,2})?', ' ', title)
    title = ' '.join(title.split()).strip(' -:,.')
    if len(title) < 2:
        title = tr(detect_language(message), 'New goal', 'Новая цель')
    return SavingsGoalCreate(title=title, target_amount=amount, current_amount=Decimal('0.00'), target_date=target_date, note='')



def parse_goal_add_money_command(message: str) -> tuple[Decimal, str] | None:
    lowered = message.lower().strip()
    if not any(keyword in lowered for keyword in ('goal', 'цель')):
        return None
    if not any(keyword in lowered for keyword in ('add', 'put', 'save', 'deposit', 'добав', 'отлож', 'полож')):
        return None
    amount = _extract_amount(message)
    if amount is None:
        return None
    title = re.sub(r'(add|put|save|deposit|to|into|for|goal|добавь|отложи|положи|в|цель)', ' ', message, flags=re.IGNORECASE)
    title = re.sub(r'\d+(?:[.,]\d{1,2})?', ' ', title)
    title = ' '.join(title.split()).strip(' -:,.')
    if not title:
        return None
    return amount, title



def wants_savings_tips(message: str) -> bool:
    lowered = message.lower()
    return any(token in lowered for token in ('saving tips', 'save money', 'economize', 'advice', 'совет', 'эконом', 'как сократить', 'как уменьшить'))



def wants_analysis(message: str) -> bool:
    lowered = message.lower()
    return any(token in lowered for token in ('analyze', 'analysis', 'review my spending', 'проанализ', 'разбери', 'разбор', 'что не так'))



def wants_forecast(message: str) -> bool:
    lowered = message.lower()
    return any(token in lowered for token in ('forecast', 'projection', 'what will happen this month', 'прогноз', 'что будет к концу месяца'))


async def answer_with_rules(session: AsyncSession, user: User, message: str, preferred_lang: str | None = None) -> AssistantMessageResponse | None:
    lang = detect_language(message, preferred_lang)
    lowered = message.lower().strip()

    goal_add_command = parse_goal_add_money_command(message)
    if goal_add_command is not None:
        amount, title = goal_add_command
        goal = await find_goal_by_title(session, user, title)
        if goal is None:
            return AssistantMessageResponse(
                answer=tr(lang, f'I could not find a goal matching “{title}”.', f'Не нашёл цель, похожую на «{title}».'),
                action='goal_not_found',
                suggestions=[tr(lang, 'Show my goals', 'Покажи мои цели'), tr(lang, 'Create goal Laptop 1200 by 2026-12-31', 'Создай цель Ноутбук 1200 до 2026-12-31')],
            )
        updated = await add_to_goal(session, user, goal.id, amount)
        status = (await goal_statuses(session, user))
        current = next((item for item in status if item.id == updated.id), None)
        answer = tr(
            lang,
            f'Added {money_value(amount)} to “{updated.title}”. Progress is now {current.progress_percent}% with {money_value(current.remaining_amount)} left.' if current else f'Added {money_value(amount)} to “{updated.title}”.',
            f'Добавил {money_value(amount)} в цель «{updated.title}». Сейчас прогресс {current.progress_percent}%, осталось {money_value(current.remaining_amount)}.' if current else f'Добавил {money_value(amount)} в цель «{updated.title}».',
        )
        return AssistantMessageResponse(answer=answer, action='goal_contribution', suggestions=[tr(lang, 'Show my goals', 'Покажи мои цели'), tr(lang, 'Analyze my spending', 'Проанализируй мои траты')])

    goal_create = parse_goal_create_command(message)
    if goal_create is not None:
        created = await create_goal(session, user, goal_create)
        return AssistantMessageResponse(
            answer=tr(lang, f'Created goal “{created.title}” with target {money_value(created.target_amount)}.', f'Создал цель «{created.title}» с суммой {money_value(created.target_amount)}.'),
            action='create_goal',
            created_goal=build_goal_read(created),
            suggestions=[tr(lang, 'Show my goals', 'Покажи мои цели'), tr(lang, 'Add 50 to goal', 'Добавь 50 в цель')],
        )

    category_budget_command = parse_category_budget_command(message)
    if category_budget_command is not None and ('category budget' in lowered or 'катег' in lowered or _extract_category_from_text(message) is not None):
        created_budget = await set_category_budget(session, user, category_budget_command)
        category_name = category_label(created_budget.category, lang)
        return AssistantMessageResponse(
            answer=tr(lang, f'Set the monthly {category_name} budget to {money_value(created_budget.monthly_limit)}.', f'Установил лимит по категории {category_name}: {money_value(created_budget.monthly_limit)}.'),
            action='set_category_budget',
            suggestions=[tr(lang, f'How is my {category_name.lower()} budget?', f'Как мой бюджет по категории {category_name.lower()}?'), tr(lang, 'Show category budgets', 'Покажи лимиты по категориям')],
        )

    recurring_command = parse_recurring_command(message)
    if recurring_command is not None:
        created = await create_recurring_expense(session, user, recurring_command)
        category_name = category_label(created.category, lang)
        return AssistantMessageResponse(
            answer=tr(lang, f'Created recurring expense “{created.description}” for {money_value(created.amount)} in {category_name}. Next due on {created.next_due_on.isoformat()}.', f'Создал регулярную трату «{created.description}» на {money_value(created.amount)} в категории {category_name}. Следующая дата: {created.next_due_on.isoformat()}.'),
            action='create_recurring',
            created_recurring=build_recurring_read(created),
            suggestions=[tr(lang, 'What subscriptions are due soon?', 'Какие списания скоро?'), tr(lang, 'Generate due recurring expenses', 'Сгенерируй регулярные траты')],
        )

    add_command = parse_assistant_add_command(message)
    if add_command is not None:
        created = await create_expense(session, user, add_command)
        category_name = category_label(created.category, lang)
        return AssistantMessageResponse(
            answer=tr(lang, f'Added {created.description} for {money_value(created.amount)} in {category_name} on {created.spent_on.isoformat()}.', f'Добавил трату «{created.description}» на {money_value(created.amount)} в категории {category_name} за {created.spent_on.isoformat()}.'),
            action='create_expense',
            created_expense=build_expense_read(created),
            suggestions=[tr(lang, 'How much did I spend this month?', 'Сколько я потратил в этом месяце?'), tr(lang, 'What is my budget status?', 'Какой у меня статус бюджета?')],
        )

    if 'generate due recurring' in lowered or 'generate recurring' in lowered or 'run recurring' in lowered or 'сгенерируй регуляр' in lowered:
        generated = await generate_due_recurring_expenses(session, user)
        return AssistantMessageResponse(
            answer=tr(lang, f'Generated {generated.created_count} expense(s) from recurring templates.', f'Сгенерировал {generated.created_count} трат(ы) из регулярных шаблонов.'),
            action='generate_recurring',
            suggestions=[tr(lang, 'Show this month summary', 'Покажи итоги месяца'), tr(lang, 'What subscriptions are due soon?', 'Какие списания скоро?')],
        )

    if 'show my goals' in lowered or 'my goals' in lowered or 'goals' in lowered or 'мои цели' in lowered or 'цели' in lowered:
        statuses = await goal_statuses(session, user)
        if not statuses:
            return AssistantMessageResponse(
                answer=tr(lang, 'You do not have any savings goals yet. Try: “Create goal Laptop 1200 by 2026-12-31”.', 'Пока нет целей накоплений. Попробуй: «Создай цель Ноутбук 1200 до 2026-12-31».'),
                action='goals_summary',
                suggestions=[tr(lang, 'Create goal Laptop 1200 by 2026-12-31', 'Создай цель Ноутбук 1200 до 2026-12-31')],
            )
        preview = '; '.join(f'{goal.title}: {goal.progress_percent}% ({money_value(goal.current_amount)} / {money_value(goal.target_amount)})' for goal in statuses[:3])
        return AssistantMessageResponse(
            answer=tr(lang, f'Your goals: {preview}.', f'Твои цели: {preview}.'),
            action='goals_summary',
            suggestions=[tr(lang, 'Add 50 to goal Laptop', 'Добавь 50 в цель Ноутбук'), tr(lang, 'Analyze my spending', 'Проанализируй мои траты')],
        )

    if 'show category budgets' in lowered or 'category budgets' in lowered or 'budget by category' in lowered or 'лимиты по категориям' in lowered:
        statuses = await category_budget_statuses(session, user)
        if not statuses:
            return AssistantMessageResponse(
                answer=tr(lang, 'You do not have any category budgets yet. Try: “Set food category budget 120”.', 'Пока нет лимитов по категориям. Попробуй: «Установи лимит на еду 120».'),
                action='category_budget_status',
                suggestions=[tr(lang, 'Set food category budget 120', 'Установи лимит на еду 120'), tr(lang, 'Set transport category budget 60', 'Установи лимит на транспорт 60')],
            )
        preview = ', '.join(f'{category_label(item.category, lang)}: {money_value(item.spent_this_month)} / {money_value(item.monthly_limit)}' for item in statuses[:4])
        return AssistantMessageResponse(answer=tr(lang, f'Current category budgets for this month: {preview}.', f'Лимиты по категориям за этот месяц: {preview}.'), action='category_budget_status', suggestions=[tr(lang, 'What is my budget status?', 'Какой у меня статус бюджета?')])

    if 'due soon' in lowered or 'subscriptions' in lowered or 'recurring expenses' in lowered or 'скоро' in lowered or 'подписк' in lowered:
        summary = await due_recurring_summary(session, user)
        if not summary.next_due_items:
            return AssistantMessageResponse(
                answer=tr(lang, 'You do not have any recurring expenses yet. Try: “Create recurring rent 320 bills monthly”.', 'Пока нет регулярных трат. Попробуй: «Создай регулярную трату аренда 320 счета ежемесячно».'),
                action='query_recurring',
                suggestions=[tr(lang, 'Create recurring rent 320 bills monthly', 'Создай регулярную трату аренда 320 счета ежемесячно')],
            )
        preview = ', '.join(f'{item.description} on {item.next_due_on.isoformat()}' for item in summary.next_due_items[:3])
        return AssistantMessageResponse(
            answer=tr(lang, f'{summary.due_today_count} recurring expense(s) are due today and {summary.due_next_7_days_count} are due within the next 7 days. Next up: {preview}.', f'Сегодня ожидается {summary.due_today_count} регулярных трат, а в ближайшие 7 дней — {summary.due_next_7_days_count}. Ближайшие: {preview}.'),
            action='query_recurring',
            suggestions=[tr(lang, 'Generate due recurring expenses', 'Сгенерируй регулярные траты'), tr(lang, 'How much did I spend this month?', 'Сколько я потратил в этом месяце?')],
        )

    if 'this week' in lowered or 'на этой неделе' in lowered:
        period = 'this_week'
    elif 'month' in lowered or 'месяц' in lowered:
        period = 'this_month'
    elif '30' in lowered:
        period = 'last_30_days'
    else:
        period = 'all_time'

    category_in_message = _extract_category_from_text(message)
    if category_in_message is not None and ('budget' in lowered or 'бюджет' in lowered or 'лимит' in lowered) and any(word in lowered for word in ('status', 'remaining', 'left', 'how', 'used', 'осталось', 'статус')):
        statuses = await category_budget_statuses(session, user)
        status_item = next((item for item in statuses if item.category == category_in_message), None)
        category_name = category_label(category_in_message, lang)
        if status_item is None:
            return AssistantMessageResponse(answer=tr(lang, f'You have not set a {category_name.lower()} budget yet. Try: “Set {category_name.lower()} category budget 120”.', f'Для категории {category_name.lower()} лимит ещё не задан. Попробуй: «Установи лимит {category_name.lower()} 120». '), action='category_budget_status')
        answer = tr(lang, f'{category_name}: {money_value(status_item.spent_this_month)} spent out of {money_value(status_item.monthly_limit)} this month. ', f'{category_name}: потрачено {money_value(status_item.spent_this_month)} из {money_value(status_item.monthly_limit)} за этот месяц. ')
        answer += tr(lang, f'You are over by {money_value(abs(status_item.remaining_amount))}.' if status_item.is_over_budget else f'{money_value(status_item.remaining_amount)} remains.', f'Превышение на {money_value(abs(status_item.remaining_amount))}.' if status_item.is_over_budget else f'Осталось {money_value(status_item.remaining_amount)}.')
        return AssistantMessageResponse(answer=answer, action='category_budget_status', suggestions=[tr(lang, 'Show category budgets', 'Покажи лимиты по категориям')])

    budget_command = parse_budget_command(message)
    if budget_command is not None:
        saved = await set_budget(session, user, BudgetUpdate(monthly_limit=budget_command))
        return AssistantMessageResponse(answer=tr(lang, f'Monthly budget set to {money_value(saved.monthly_limit)}.', f'Месячный бюджет установлен на {money_value(saved.monthly_limit)}.'), action='set_budget', suggestions=[tr(lang, 'What is my budget status?', 'Какой у меня статус бюджета?')])

    if 'budget status' in lowered or ('budget' in lowered and any(word in lowered for word in ('status', 'remaining', 'left', 'осталось', 'статус'))):
        budget_status = await current_budget_status(session, user)
        if budget_status is None:
            return AssistantMessageResponse(answer=tr(lang, 'You have not set a monthly budget yet. Try: “Set budget 500”.', 'Месячный бюджет пока не задан. Попробуй: «Установи бюджет 500». '), action='budget_status')
        answer = tr(lang, f'This month you spent {money_value(budget_status.spent_this_month)} out of {money_value(budget_status.monthly_limit)}. ', f'В этом месяце ты потратил {money_value(budget_status.spent_this_month)} из {money_value(budget_status.monthly_limit)}. ')
        answer += tr(lang, f'You are over budget by {money_value(abs(budget_status.remaining_amount))}.' if budget_status.is_over_budget else f'You have {money_value(budget_status.remaining_amount)} left.', f'Превышение на {money_value(abs(budget_status.remaining_amount))}.' if budget_status.is_over_budget else f'Осталось {money_value(budget_status.remaining_amount)}.')
        if budget_status.projected_total:
            answer += tr(lang, f' Projected month end: {money_value(budget_status.projected_total)}.', f' Прогноз на конец месяца: {money_value(budget_status.projected_total)}.')
        return AssistantMessageResponse(answer=answer, action='budget_status', suggestions=[tr(lang, 'Analyze my spending', 'Проанализируй мои траты')])

    if wants_analysis(message):
        coach = await coach_summary(session, user, lang)
        insights = await spending_insights(session, user, lang)
        detail = ' '.join([coach.headline] + [item.detail for item in insights[:2]])
        return AssistantMessageResponse(answer=detail, action='analysis', suggestions=[tr(lang, 'Give me savings tips', 'Дай советы по экономии'), tr(lang, 'Forecast this month', 'Сделай прогноз на месяц')])

    if wants_savings_tips(message):
        coach = await coach_summary(session, user, lang)
        advice = coach.next_actions or coach.risks or [tr(lang, 'Start by setting budgets and reducing the top category from this month.', 'Начни с установки бюджетов и сокращения самой крупной категории за этот месяц.')]
        return AssistantMessageResponse(answer=' '.join(advice[:3]), action='tips', suggestions=[tr(lang, 'Analyze my spending', 'Проанализируй мои траты'), tr(lang, 'Show my goals', 'Покажи мои цели')])

    if wants_forecast(message):
        budget = await current_budget_status(session, user)
        if budget is None:
            return AssistantMessageResponse(answer=tr(lang, 'Set a monthly budget first so I can compare the forecast with your limit.', 'Сначала задай месячный бюджет, чтобы я мог сравнить прогноз с лимитом.'), action='forecast')
        return AssistantMessageResponse(answer=tr(lang, f'At the current pace, this month may end around {money_value(budget.projected_total)}. That is {budget.projected_percent_used}% of your budget.', f'При текущем темпе месяц может закончиться примерно на {money_value(budget.projected_total)}. Это {budget.projected_percent_used}% твоего бюджета.'), action='forecast', suggestions=[tr(lang, 'Give me savings tips', 'Дай советы по экономии')])

    if 'largest expense' in lowered or 'biggest expense' in lowered or 'highest expense' in lowered or 'самая большая трата' in lowered:
        query = apply_period(select(Expense).where(_expense_scope(user)).order_by(Expense.amount.desc(), Expense.spent_on.desc()).limit(1), period)
        result = await session.exec(query)
        expense = result.first()
        if expense is None:
            return AssistantMessageResponse(answer=tr(lang, 'I could not find any expenses for that period yet.', 'Я пока не нашёл трат за этот период.'), action='query_summary')
        category_name = category_label(expense.category, lang)
        return AssistantMessageResponse(answer=tr(lang, f'The largest expense in {get_window(period, lang).label.lower()} is {money_value(expense.amount)} for {expense.description} ({category_name}) on {expense.spent_on.isoformat()}.', f'Самая большая трата за период «{get_window(period, lang).label.lower()}» — {money_value(expense.amount)} на {expense.description} ({category_name}) от {expense.spent_on.isoformat()}.'), action='query_summary')

    if 'how much' in lowered or 'total' in lowered or 'summary' in lowered or 'сколько' in lowered or 'итог' in lowered:
        if category_in_message is not None:
            query = apply_period(select(func.coalesce(func.sum(Expense.amount), 0)).where(_expense_scope(user)).where(Expense.category == category_in_message), period)
            total = q2(_unwrap_scalar((await session.exec(query)).one()) or 0)
            return AssistantMessageResponse(answer=tr(lang, f'You spent {money_value(total)} on {category_label(category_in_message, lang)} during {get_window(period, lang).label.lower()}.', f'На категорию {category_label(category_in_message, lang)} за период «{get_window(period, lang).label.lower()}» потрачено {money_value(total)}.'), action='query_summary')
        summary = await overview(session, user, period=period, lang=lang)
        total_card = next(card for card in summary.cards if card.label == CARD_LABELS[lang]['total'])
        count_card = next(card for card in summary.cards if card.label == CARD_LABELS[lang]['count'])
        return AssistantMessageResponse(answer=tr(lang, f'{summary.period_label}: {total_card.value} across {count_card.value} logged expenses.', f'{summary.period_label}: {total_card.value}, записей: {count_card.value}.'), action='query_summary')

    if 'category breakdown' in lowered or 'categories' in lowered or 'категории' in lowered:
        categories = await category_breakdown(session, user, period=period)
        if not categories:
            return AssistantMessageResponse(answer=tr(lang, 'No expenses found yet. Add one or seed the demo data to see breakdowns.', 'Пока нет трат. Добавь запись или демо-данные, чтобы увидеть разбивку.'), action='query_summary')
        preview = ', '.join(f'{category_label(item.category, lang)}: {money_value(item.total_amount)}' for item in categories[:4])
        return AssistantMessageResponse(answer=tr(lang, f'Top categories for {get_window(period, lang).label.lower()}: {preview}.', f'Основные категории за период «{get_window(period, lang).label.lower()}»: {preview}.'), action='query_summary')

    return None


def _normalize_llm_content(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text_value = item.get('text') or item.get('content') or ''
                if isinstance(text_value, str):
                    parts.append(text_value)
        return '\n'.join(part for part in parts if part).strip()
    return ''


def _default_assistant_suggestions(lang: str) -> list[str]:
    return [
        tr(lang, 'Analyze my spending', 'Проанализируй мои траты'),
        tr(lang, 'What should I do this month?', 'Что мне делать в этом месяце?'),
        tr(lang, 'Can I afford 80 for entertainment?', 'Могу ли я позволить себе 80 на развлечения?'),
        tr(lang, 'Show my goals', 'Покажи мои цели'),
        tr(lang, 'What subscriptions are due soon?', 'Какие списания скоро?'),
    ]


async def local_smart_answer(
    session: AsyncSession,
    user: User,
    message: str,
    preferred_lang: str | None = None,
    *,
    llm_error: str | None = None,
) -> AssistantMessageResponse:
    lang = detect_language(message, preferred_lang)
    lowered = message.lower().strip()
    summary = await overview(session, user, period='this_month', lang=lang)
    categories = await category_breakdown(session, user, period='this_month')
    budget = await current_budget_status(session, user)
    recurring_summary = await due_recurring_summary(session, user)
    goals = await goal_statuses(session, user)
    coach = await coach_summary(session, user, lang)
    category_statuses = await category_budget_statuses(session, user)

    def top_category_text() -> str:
        if not categories:
            return tr(lang, 'no spending data yet', 'пока нет данных по тратам')
        top = categories[0]
        return tr(lang, f'{category_label(top.category, lang)} ({money_value(top.total_amount)})', f'{category_label(top.category, lang)} ({money_value(top.total_amount)})')

    over_budget_categories = [item for item in category_statuses if item.is_over_budget]
    next_due_preview = ', '.join(item.description for item in recurring_summary.next_due_items[:3])

    if any(token in lowered for token in ('what can you do', 'help', 'помощь', 'что ты умеешь', 'что ты можешь')):
        answer = tr(
            lang,
            'I can log expenses, set the monthly budget, set category budgets, create recurring payments, create savings goals, summarize spending, estimate month-end spending, and suggest what to improve.',
            'Я умею добавлять траты, задавать месячный бюджет и лимиты по категориям, создавать регулярные платежи и цели накоплений, подводить итоги, оценивать конец месяца и подсказывать, что улучшить.',
        )
        if llm_error:
            answer += tr(lang, ' Live AI is temporarily unavailable, so I am using the built-in assistant mode.', ' Внешний ИИ временно недоступен, поэтому я работаю во встроенном режиме.')
        return AssistantMessageResponse(answer=answer, action='help', suggestions=_default_assistant_suggestions(lang))

    if any(token in lowered for token in ('what should i do', 'what do i do', 'what should i improve', 'что мне делать', 'что улучшить', 'что исправить', 'что делать дальше', 'как улучшить')):
        actions: list[str] = []
        if budget is not None and budget.is_over_budget:
            actions.append(tr(lang, f'You are over budget by {money_value(abs(budget.remaining_amount))}, so start by reducing {top_category_text()}.', f'Ты вышел за бюджет на {money_value(abs(budget.remaining_amount))}, начни с сокращения {top_category_text()}.'))
        elif budget is not None and budget.projected_total and budget.projected_total > budget.monthly_limit:
            actions.append(tr(lang, f'At the current pace you may finish the month at {money_value(budget.projected_total)}, above the limit, so reduce {top_category_text()}.', f'При текущем темпе месяц может закончиться на {money_value(budget.projected_total)}, выше лимита, поэтому сократи {top_category_text()}.'))
        else:
            actions.append(tr(lang, f'Your biggest spending area this month is {top_category_text()}; review that category first.', f'Самая крупная категория трат в этом месяце — {top_category_text()}, начни проверку с неё.'))
        if over_budget_categories:
            preview = ', '.join(category_label(item.category, lang) for item in over_budget_categories[:3])
            actions.append(tr(lang, f'Over-budget category limits: {preview}.', f'Лимиты с перерасходом: {preview}.'))
        if recurring_summary.due_next_7_days_count:
            actions.append(tr(lang, f'{recurring_summary.due_next_7_days_count} recurring payment(s) are due soon: {next_due_preview}.', f'В ближайшие дни ожидается {recurring_summary.due_next_7_days_count} регулярных платежей: {next_due_preview}.'))
        if goals:
            closest_goal = min((goal for goal in goals if goal.remaining_amount > 0), key=lambda goal: goal.remaining_amount, default=None)
            if closest_goal is not None:
                actions.append(tr(lang, f'Closest savings goal: “{closest_goal.title}”, {money_value(closest_goal.remaining_amount)} left.', f'Ближайшая цель накоплений: «{closest_goal.title}», осталось {money_value(closest_goal.remaining_amount)}.'))
        return AssistantMessageResponse(answer=' '.join(actions[:4]), action='plan', suggestions=_default_assistant_suggestions(lang))

    if any(token in lowered for token in ('can i afford', 'afford', 'могу ли позволить', 'хватит ли', 'потяну ли')):
        amount = _extract_amount(message)
        category = _extract_category_from_text(message)
        if amount is None:
            return AssistantMessageResponse(answer=tr(lang, 'Tell me the amount, for example: “Can I afford 80 for entertainment?”', 'Укажи сумму, например: «Могу ли я позволить себе 80 на развлечения?»'), action='affordability', suggestions=_default_assistant_suggestions(lang))
        if budget is None:
            return AssistantMessageResponse(answer=tr(lang, f'You have no monthly budget yet. For now, {money_value(amount)} would be compared only against your cash flow history. Set a budget to get a clearer answer.', f'У тебя пока нет месячного бюджета. Сейчас {money_value(amount)} можно сравнить только с историей трат. Задай бюджет, чтобы получить более точный ответ.'), action='affordability', suggestions=[tr(lang, 'Set budget 500', 'Установи бюджет 500')])
        remaining = budget.remaining_amount
        category_note = ''
        if category is not None:
            status = next((item for item in category_statuses if item.category == category), None)
            if status is not None:
                category_note = tr(lang, f' Category {category_label(category, lang)} has {money_value(status.remaining_amount)} left.', f' По категории {category_label(category, lang)} осталось {money_value(status.remaining_amount)}.')
        if remaining >= amount:
            answer = tr(lang, f'Yes, {money_value(amount)} fits into the remaining monthly budget. You still have {money_value(remaining - amount)} left afterwards.', f'Да, {money_value(amount)} помещается в оставшийся месячный бюджет. После этого останется {money_value(remaining - amount)}.') + category_note
        elif remaining > 0:
            answer = tr(lang, f'Partly: you still have {money_value(remaining)} left this month, so spending {money_value(amount)} would push you over by {money_value(amount - remaining)}.', f'Частично: в этом месяце осталось {money_value(remaining)}, поэтому трата {money_value(amount)} превысит лимит на {money_value(amount - remaining)}.') + category_note
        else:
            answer = tr(lang, f'Not really: your current monthly budget is already exhausted by {money_value(abs(remaining))}, so {money_value(amount)} would increase the overspend.', f'Скорее нет: текущий месячный бюджет уже исчерпан с превышением на {money_value(abs(remaining))}, поэтому {money_value(amount)} только увеличит перерасход.') + category_note
        return AssistantMessageResponse(answer=answer, action='affordability', suggestions=[tr(lang, 'What should I do this month?', 'Что мне делать в этом месяце?'), tr(lang, 'Set entertainment category budget 80', 'Установи лимит на развлечения 80')])

    if any(token in lowered for token in ('biggest category', 'top category', 'where does my money go', 'куда уходят деньги', 'главная категория', 'больше всего трачу')):
        if not categories:
            return AssistantMessageResponse(answer=tr(lang, 'I do not see enough expenses yet. Add a few records or seed demo data.', 'Я пока не вижу достаточно трат. Добавь несколько записей или демо-данные.'), action='analysis', suggestions=_default_assistant_suggestions(lang))
        top = categories[0]
        answer = tr(lang, f'Your biggest category this month is {category_label(top.category, lang)} with {money_value(top.total_amount)}. That is {top.percent_of_total}% of this month’s spending.', f'Самая большая категория в этом месяце — {category_label(top.category, lang)}: {money_value(top.total_amount)}. Это {top.percent_of_total}% трат месяца.')
        return AssistantMessageResponse(answer=answer, action='analysis', suggestions=[tr(lang, 'Give me savings tips', 'Дай советы по экономии'), tr(lang, 'What should I do this month?', 'Что мне делать в этом месяце?')])

    if any(token in lowered for token in ('goals', 'goal progress', 'цели', 'накопления', 'прогресс цели')):
        if not goals:
            return AssistantMessageResponse(answer=tr(lang, 'You do not have any goals yet. Create one and I will help track progress.', 'У тебя пока нет целей. Создай цель, и я помогу следить за прогрессом.'), action='goals_summary', suggestions=[tr(lang, 'Create goal Laptop 1200 by 2026-12-31', 'Создай цель Ноутбук 1200 до 2026-12-31')])
        preview = '; '.join(
            tr(lang, f'{goal.title}: {goal.progress_percent}% complete, {money_value(goal.remaining_amount)} left', f'{goal.title}: {goal.progress_percent}% выполнено, осталось {money_value(goal.remaining_amount)}')
            for goal in goals[:3]
        )
        return AssistantMessageResponse(answer=preview, action='goals_summary', suggestions=[tr(lang, 'Add 50 to goal Laptop', 'Добавь 50 в цель Ноутбук'), tr(lang, 'What should I do this month?', 'Что мне делать в этом месяце?')])

    fallback_bits = [coach.headline]
    if categories:
        fallback_bits.append(tr(lang, f'Top category this month: {top_category_text()}.', f'Главная категория в этом месяце: {top_category_text()}.'))
    if budget is not None:
        fallback_bits.append(
            tr(
                lang,
                f'Budget usage: {budget.percent_used}% ({money_value(budget.spent_this_month)} of {money_value(budget.monthly_limit)}).',
                f'Использование бюджета: {budget.percent_used}% ({money_value(budget.spent_this_month)} из {money_value(budget.monthly_limit)}).',
            )
        )
    if recurring_summary.due_next_7_days_count:
        fallback_bits.append(tr(lang, f'Recurring due soon: {recurring_summary.due_next_7_days_count}.', f'Скоро регулярных списаний: {recurring_summary.due_next_7_days_count}.'))
    if llm_error:
        fallback_bits.append(tr(lang, 'The external AI model is temporarily unavailable, so I answered from your current project data.', 'Внешняя ИИ-модель временно недоступна, поэтому я ответил по данным проекта.'))
    return AssistantMessageResponse(
        answer=' '.join(fallback_bits),
        action='smart_fallback',
        suggestions=_default_assistant_suggestions(lang),
    )



async def llm_answer(session: AsyncSession, user: User, message: str, preferred_lang: str | None = None) -> AssistantMessageResponse | None:
    if not settings.llm_enabled:
        return None
    lang = detect_language(message, preferred_lang)
    summary = await overview(session, user, period='this_month', lang=lang)
    categories = await category_breakdown(session, user, period='this_month')
    recent = await list_expenses(session, user)
    budget_status = await current_budget_status(session, user)
    recurring = await list_recurring_expenses(session, user, include_inactive=True)
    category_budgets = await category_budget_statuses(session, user)
    goals = await goal_statuses(session, user)
    coach = await coach_summary(session, user, lang)
    context = {
        'summary': summary.model_dump(mode='json'),
        'budget_status': budget_status.model_dump(mode='json') if budget_status is not None else None,
        'categories': [item.model_dump(mode='json') for item in categories],
        'recent_expenses': [build_expense_read(item).model_dump(mode='json') for item in recent[:12]],
        'recurring_expenses': [build_recurring_read(item).model_dump(mode='json') for item in recurring[:10]],
        'category_budgets': [item.model_dump(mode='json') for item in category_budgets],
        'goals': [item.model_dump(mode='json') for item in goals],
        'coach': coach.model_dump(mode='json'),
    }
    prompt = (
        'You are a concise financial assistant inside a personal expense tracker. '
        f'Respond in {"Russian" if lang == "ru" else "English"}. '
        'Base your answer only on the provided JSON context. '
        'If the context is insufficient, say so. '
        'Return JSON with keys answer and suggestions when possible. Suggestions must be short strings. If JSON is not possible, answer in plain text.\n\n'
        f'Context JSON:\n{json.dumps(context, default=str, ensure_ascii=False)}\n\n'
        f'User message: {message}'
    )
    payload = {
        'model': settings.openai_model,
        'messages': [
            {'role': 'system', 'content': 'You are a practical personal finance assistant.'},
            {'role': 'user', 'content': prompt},
        ],
    }
    headers = {
        'Authorization': f'Bearer {settings.openai_api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': settings.openrouter_site_url,
        'X-OpenRouter-Title': settings.openrouter_app_title,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(f"{settings.openai_api_base_url.rstrip('/')}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    content = data['choices'][0]['message']['content']
    parsed = extract_json_object(content)
    answer = parsed.get('answer') if isinstance(parsed, dict) else None
    if not answer:
        answer = content.strip() or tr(lang, 'I could not produce an answer.', 'Не удалось сформировать ответ.')
    suggestions = parsed.get('suggestions', []) if isinstance(parsed, dict) else []
    if not isinstance(suggestions, list):
        suggestions = []
    return AssistantMessageResponse(answer=answer, action='llm_answer', suggestions=suggestions[:5])


async def handle_assistant_message(session: AsyncSession, user: User, message: str, preferred_lang: str | None = None) -> AssistantMessageResponse:
    rules = await answer_with_rules(session, user, message, preferred_lang)
    if rules is not None:
        return rules
    llm = await llm_answer(session, user, message, preferred_lang)
    if llm is not None:
        return llm
    lang = detect_language(message, preferred_lang)
    return AssistantMessageResponse(
        answer=tr(lang, 'I can add expenses, create recurring payments, set budgets, manage category budgets, create savings goals, analyze spending, and forecast the end of the month.', 'Я умею добавлять траты, создавать регулярные платежи, настраивать бюджеты и лимиты, создавать цели накоплений, анализировать траты и делать прогноз на конец месяца.'),
        action='help',
        suggestions=[
            tr(lang, 'Add coffee 4.50 food', 'Добавь кофе 4.50 еда'),
            tr(lang, 'Set budget 500', 'Установи бюджет 500'),
            tr(lang, 'Create goal Laptop 1200 by 2026-12-31', 'Создай цель Ноутбук 1200 до 2026-12-31'),
            tr(lang, 'Analyze my spending', 'Проанализируй мои траты'),
            tr(lang, 'Forecast this month', 'Сделай прогноз на месяц'),
        ],
    )

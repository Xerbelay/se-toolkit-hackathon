from __future__ import annotations

import csv
from contextlib import asynccontextmanager
from datetime import date
from io import StringIO

from fastapi import Cookie, Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from expensemate.auth import (
    AuthError,
    authenticate_user,
    build_user_read,
    create_session,
    get_user_by_session_token,
    register_user,
    revoke_session_token,
)
from expensemate.database import get_session, init_db
from expensemate.models import (
    AssistantMessageRequest,
    AssistantMessageResponse,
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthUserRead,
    BudgetRead,
    BudgetUpdate,
    CategoryBreakdown,
    CategoryBudgetRead,
    CategoryBudgetStatus,
    CategoryBudgetUpsert,
    CoachSummary,
    CsvImportPreviewRequest,
    CsvImportPreviewResponse,
    CsvImportResult,
    DailySpendPoint,
    DueRecurringSummary,
    ExpenseCreate,
    ExpenseRead,
    ExpenseUpdate,
    InsightRead,
    MonthlySpendPoint,
    OverviewResponse,
    RecurringExpenseCreate,
    RecurringExpenseRead,
    RecurringExpenseUpdate,
    RecurringGenerationResponse,
    SavingsGoalCreate,
    SavingsGoalRead,
    SavingsGoalStatus,
    SavingsGoalUpdate,
    User,
)
from expensemate.services import (
    available_categories,
    build_category_budget_read,
    build_expense_read,
    build_goal_read,
    build_recurring_read,
    category_breakdown,
    category_budget_statuses,
    coach_summary,
    create_expense,
    create_goal,
    create_recurring_expense,
    daily_spending,
    delete_category_budget,
    delete_expense,
    delete_goal,
    delete_recurring_expense,
    due_recurring_summary,
    generate_due_recurring_expenses,
    get_budget,
    goal_statuses,
    handle_assistant_message,
    import_expenses_from_csv,
    list_category_budgets,
    list_expenses,
    list_goals,
    list_recurring_expenses,
    monthly_spending,
    overview,
    preview_expense_csv_import,
    seed_demo_data,
    set_budget,
    set_category_budget,
    spending_insights,
    update_expense,
    update_goal,
    update_recurring_expense,
)
from expensemate.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    description='Expense tracking backend with authentication, planning, AI assistant, and analytics.',
    lifespan=lifespan,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_headers=['*'],
    allow_methods=['*'],
    allow_credentials=True,
)


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok', 'version': '1.0.0'}


@app.get('/api/meta')
async def get_meta() -> dict[str, str]:
    return {'app_name': settings.app_name, 'version': '1.0.0', 'llm_enabled': str(settings.llm_enabled).lower()}



def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        max_age=settings.session_max_age_seconds,
        samesite='lax',
        secure=settings.session_cookie_secure,
        path='/',
    )



def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.session_cookie_name, path='/')


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> User:
    user = await get_user_by_session_token(session, session_token)
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    return user


# ---------- Auth ----------


@app.post('/api/auth/register', response_model=AuthUserRead, status_code=status.HTTP_201_CREATED)
async def post_register(
    payload: AuthRegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthUserRead:
    try:
        user = await register_user(session, payload)
        token = await create_session(session, user)
    except AuthError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    set_auth_cookie(response, token)
    return build_user_read(user)


@app.post('/api/auth/login', response_model=AuthUserRead)
async def post_login(
    payload: AuthLoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthUserRead:
    try:
        user, token = await authenticate_user(session, payload)
    except AuthError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
    set_auth_cookie(response, token)
    return build_user_read(user)


@app.get('/api/auth/me', response_model=AuthUserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> AuthUserRead:
    return build_user_read(current_user)


@app.post('/api/auth/logout', status_code=status.HTTP_204_NO_CONTENT)
async def post_logout(
    response: Response,
    session: AsyncSession = Depends(get_session),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> Response:
    await revoke_session_token(session, session_token)
    clear_auth_cookie(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


# ---------- Categories / expenses ----------


@app.get('/api/categories', response_model=list[str])
async def get_categories(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[str]:
    return await available_categories(session, current_user)


@app.get('/api/expenses', response_model=list[ExpenseRead])
async def get_expenses(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[ExpenseRead]:
    expenses = await list_expenses(session, current_user, category=category, search=search, start_date=start_date, end_date=end_date)
    return [build_expense_read(item) for item in expenses]


@app.get('/api/expenses/export', response_class=PlainTextResponse)
async def export_expenses_csv(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Response:
    expenses = await list_expenses(session, current_user, category=category, search=search, start_date=start_date, end_date=end_date)
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['id', 'date', 'description', 'category', 'amount', 'created_at'])
    for expense in expenses:
        writer.writerow([expense.id, expense.spent_on.isoformat(), expense.description, expense.category, f'{expense.amount:.2f}', expense.created_at.isoformat()])
    return Response(content=buffer.getvalue(), media_type='text/csv; charset=utf-8', headers={'Content-Disposition': 'attachment; filename="expenses.csv"'})


@app.post('/api/expenses', response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def post_expense(
    payload: ExpenseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ExpenseRead:
    expense = await create_expense(session, current_user, payload)
    return build_expense_read(expense)


@app.put('/api/expenses/{expense_id}', response_model=ExpenseRead)
async def put_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ExpenseRead:
    expense = await update_expense(session, current_user, expense_id, payload)
    if expense is None:
        raise HTTPException(status_code=404, detail='Expense not found')
    return build_expense_read(expense)


@app.delete('/api/expenses/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_expense(
    expense_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Response:
    deleted = await delete_expense(session, current_user, expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Expense not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---------- Import ----------


@app.post('/api/import/csv/preview', response_model=CsvImportPreviewResponse)
async def post_import_csv_preview(
    payload: CsvImportPreviewRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CsvImportPreviewResponse:
    return await preview_expense_csv_import(session, current_user, payload.csv_text)


@app.post('/api/import/csv', response_model=CsvImportResult)
async def post_import_csv(
    payload: CsvImportPreviewRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CsvImportResult:
    return await import_expenses_from_csv(session, current_user, payload.csv_text)


# ---------- Recurring ----------


@app.get('/api/recurring', response_model=list[RecurringExpenseRead])
async def get_recurring_expenses(
    include_inactive: bool = Query(default=True),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[RecurringExpenseRead]:
    items = await list_recurring_expenses(session, current_user, include_inactive=include_inactive)
    return [build_recurring_read(item) for item in items]


@app.post('/api/recurring', response_model=RecurringExpenseRead, status_code=status.HTTP_201_CREATED)
async def post_recurring_expense(
    payload: RecurringExpenseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> RecurringExpenseRead:
    recurring = await create_recurring_expense(session, current_user, payload)
    return build_recurring_read(recurring)


@app.put('/api/recurring/{recurring_id}', response_model=RecurringExpenseRead)
async def put_recurring_expense(
    recurring_id: int,
    payload: RecurringExpenseUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> RecurringExpenseRead:
    recurring = await update_recurring_expense(session, current_user, recurring_id, payload)
    if recurring is None:
        raise HTTPException(status_code=404, detail='Recurring expense not found')
    return build_recurring_read(recurring)


@app.delete('/api/recurring/{recurring_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_recurring_expense(
    recurring_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Response:
    deleted = await delete_recurring_expense(session, current_user, recurring_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Recurring expense not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post('/api/recurring/generate', response_model=RecurringGenerationResponse)
async def post_generate_recurring(
    through_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> RecurringGenerationResponse:
    return await generate_due_recurring_expenses(session, current_user, through_date=through_date)


@app.get('/api/recurring/due-soon', response_model=DueRecurringSummary)
async def get_due_recurring(
    days: int = Query(default=7, ge=1, le=60),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> DueRecurringSummary:
    return await due_recurring_summary(session, current_user, days=days)


# ---------- Goals ----------


@app.get('/api/goals', response_model=list[SavingsGoalRead])
async def get_goals(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[SavingsGoalRead]:
    items = await list_goals(session, current_user)
    return [build_goal_read(item) for item in items]


@app.post('/api/goals', response_model=SavingsGoalRead, status_code=status.HTTP_201_CREATED)
async def post_goal(
    payload: SavingsGoalCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> SavingsGoalRead:
    goal = await create_goal(session, current_user, payload)
    return build_goal_read(goal)


@app.put('/api/goals/{goal_id}', response_model=SavingsGoalRead)
async def put_goal(
    goal_id: int,
    payload: SavingsGoalUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> SavingsGoalRead:
    goal = await update_goal(session, current_user, goal_id, payload)
    if goal is None:
        raise HTTPException(status_code=404, detail='Goal not found')
    return build_goal_read(goal)


@app.delete('/api/goals/{goal_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_goal(
    goal_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Response:
    deleted = await delete_goal(session, current_user, goal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Goal not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/api/goals/status', response_model=list[SavingsGoalStatus])
async def get_goal_statuses(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[SavingsGoalStatus]:
    return await goal_statuses(session, current_user)


# ---------- Budgets ----------


@app.get('/api/budget', response_model=BudgetRead)
async def get_budget_settings(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> BudgetRead:
    return await get_budget(session, current_user)


@app.put('/api/budget', response_model=BudgetRead)
async def put_budget_settings(
    payload: BudgetUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> BudgetRead:
    return await set_budget(session, current_user, payload)


@app.get('/api/budget/categories', response_model=list[CategoryBudgetRead])
async def get_category_budget_settings(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[CategoryBudgetRead]:
    items = await list_category_budgets(session, current_user)
    return [build_category_budget_read(item) for item in items]


@app.put('/api/budget/categories', response_model=CategoryBudgetRead)
async def put_category_budget_settings(
    payload: CategoryBudgetUpsert,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CategoryBudgetRead:
    item = await set_category_budget(session, current_user, payload)
    return build_category_budget_read(item)


@app.delete('/api/budget/categories/{category_budget_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_category_budget_settings(
    category_budget_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Response:
    deleted = await delete_category_budget(session, current_user, category_budget_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Category budget not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get('/api/budget/categories/status', response_model=list[CategoryBudgetStatus])
async def get_category_budget_status(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[CategoryBudgetStatus]:
    return await category_budget_statuses(session, current_user)


# ---------- Analytics ----------


@app.get('/api/stats/overview', response_model=OverviewResponse)
async def get_overview(
    period: str = Query(default='this_month', pattern='^(this_week|this_month|last_30_days|all_time)$'),
    lang: str = Query(default='en', pattern='^(en|ru)$'),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> OverviewResponse:
    return await overview(session, current_user, period=period, lang=lang)


@app.get('/api/stats/by-category', response_model=list[CategoryBreakdown])
async def get_category_breakdown(
    period: str = Query(default='this_month', pattern='^(this_week|this_month|last_30_days|all_time)$'),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[CategoryBreakdown]:
    return await category_breakdown(session, current_user, period=period)


@app.get('/api/stats/daily', response_model=list[DailySpendPoint])
async def get_daily_spending(
    days: int = Query(default=14, ge=1, le=90),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[DailySpendPoint]:
    return await daily_spending(session, current_user, days=days)


@app.get('/api/stats/monthly', response_model=list[MonthlySpendPoint])
async def get_monthly_spending(
    months: int = Query(default=6, ge=1, le=24),
    lang: str = Query(default='en', pattern='^(en|ru)$'),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[MonthlySpendPoint]:
    return await monthly_spending(session, current_user, months=months, lang=lang)


@app.get('/api/stats/insights', response_model=list[InsightRead])
async def get_spending_insights(
    lang: str = Query(default='en', pattern='^(en|ru)$'),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[InsightRead]:
    return await spending_insights(session, current_user, lang)


@app.get('/api/coach/summary', response_model=CoachSummary)
async def get_coach_summary(
    lang: str = Query(default='en', pattern='^(en|ru)$'),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CoachSummary:
    return await coach_summary(session, current_user, lang)


# ---------- Demo + assistant ----------


@app.post('/api/demo/seed')
async def post_demo_seed(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, int]:
    return await seed_demo_data(session, current_user)


@app.post('/api/assistant/message', response_model=AssistantMessageResponse)
async def post_assistant_message(
    payload: AssistantMessageRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> AssistantMessageResponse:
    try:
        return await handle_assistant_message(session, current_user, payload.message, payload.lang)
    except Exception:
        lang = payload.lang or 'en'
        return AssistantMessageResponse(
            answer=(
                'The assistant is temporarily unavailable. Try refreshing the page and ask again.'
                if lang == 'en'
                else 'Ассистент временно недоступен. Обнови страницу и попробуй ещё раз.'
            ),
            action='assistant_error',
            suggestions=(
                ['Analyze my spending', 'What is my budget status?', 'Show my goals']
                if lang == 'en'
                else ['Проанализируй мои траты', 'Какой у меня статус бюджета?', 'Покажи мои цели']
            ),
        )

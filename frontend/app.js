const translations = {
  en: {
    'hero.eyebrow': 'Personal finance workspace',
    'hero.copy': 'Track spending, plan budgets, manage recurring payments, save for goals, and get useful coaching from the assistant.',
    'hero.guest': 'Sign in to keep your expenses, goals, and recurring payments private.',
    'auth.title': 'Sign in or create an account',
    'auth.subtitle': 'Every account gets its own expenses, budgets, recurring schedules, and goals.',
    'auth.create': 'Create account',
    'auth.signIn': 'Sign in',
    'auth.name': 'Name',
    'auth.email': 'Email',
    'auth.password': 'Password',
    'auth.namePlaceholder': 'Ivan Ivanov',
    'auth.emailPlaceholder': 'student@example.com',
    'auth.passwordPlaceholder': 'At least 8 characters',
    'auth.signInPasswordPlaceholder': 'Your password',
    'auth.createButton': 'Create account',
    'auth.signInButton': 'Sign in',
    'auth.logout': 'Log out',
    'app.seed': 'Seed demo data',
    'app.refresh': 'Refresh',
    'expense.formTitle': 'Add expense',
    'expense.editTitle': 'Edit expense',
    'expense.formSubtitle': 'Quickly log a spending record and keep the dashboard up to date.',
    'expense.amount': 'Amount (€)',
    'expense.category': 'Category',
    'expense.description': 'Description',
    'expense.descriptionPlaceholder': 'Lunch near campus',
    'expense.date': 'Date',
    'expense.save': 'Save expense',
    'budget.title': 'Monthly budget',
    'budget.subtitle': 'Set a limit and see how much room is left this month.',
    'budget.limit': 'Budget limit (€)',
    'budget.save': 'Save budget',
    'assistant.title': 'Expense assistant',
    'assistant.subtitle': 'Ask for summaries, budgets, savings tips, goal updates, forecasts, or quick actions.',
    'assistant.empty': 'Ask something like “Analyze my spending” or “Create goal Laptop 1200 by 2026-12-31”.',
    'assistant.placeholder': 'Ask about your spending, budgets, goals, or recurring payments',
    'assistant.send': 'Send',
    'dashboard.title': 'Dashboard',
    'dashboard.subtitle': 'Understand spending, spot risks, and see what deserves attention right now.',
    'dashboard.period': 'Period',
    'dashboard.insights': 'Key insights',
    'dashboard.monthlyTrend': 'Monthly trend',
    'dashboard.byCategory': 'Spending by category',
    'dashboard.dailyTrend': 'Daily trend',
    'dashboard.recurringSoon': 'Upcoming recurring',
    'period.thisWeek': 'This week',
    'period.thisMonth': 'This month',
    'period.last30Days': 'Last 30 days',
    'period.allTime': 'All time',
    'expenses.title': 'Expenses',
    'expenses.subtitle': 'Filter, review, edit, and export your saved records.',
    'expenses.export': 'Export CSV',
    'expenses.search': 'Search',
    'expenses.searchPlaceholder': 'coffee, rent, taxi...',
    'expenses.from': 'From',
    'expenses.to': 'To',
    'expenses.clearFilters': 'Clear filters',
    'goals.title': 'Savings goals',
    'goals.editTitle': 'Edit goal',
    'goals.subtitle': 'Track what you are saving for and how much you still need.',
    'goals.name': 'Goal name',
    'goals.namePlaceholder': 'Laptop, vacation, emergency fund',
    'goals.target': 'Target amount (€)',
    'goals.current': 'Already saved (€)',
    'goals.date': 'Target date',
    'goals.note': 'Note',
    'goals.notePlaceholder': 'Optional note',
    'goals.save': 'Save goal',
    'categoryBudgets.title': 'Category budgets',
    'categoryBudgets.editTitle': 'Edit category budget',
    'categoryBudgets.subtitle': 'Limit specific categories like food or transport and catch overspending earlier.',
    'categoryBudgets.limit': 'Monthly limit (€)',
    'categoryBudgets.save': 'Save category budget',
    'categoryBudgets.spent': 'Spent this month',
    'categoryBudgets.remaining': 'Remaining',
    'categoryBudgets.progress': 'Progress',
    'recurring.title': 'Recurring payments',
    'recurring.editTitle': 'Edit recurring payment',
    'recurring.subtitle': 'Manage subscriptions, rent, utilities, and other repeating expenses.',
    'recurring.descriptionPlaceholder': 'Spotify, rent, internet',
    'recurring.frequency': 'Frequency',
    'recurring.monthly': 'Monthly',
    'recurring.weekly': 'Weekly',
    'recurring.startDate': 'Start date',
    'recurring.save': 'Save recurring payment',
    'recurring.generate': 'Generate due now',
    'recurring.nextDue': 'Next due',
    'recurring.state': 'State',
    'import.title': 'Import expenses from CSV',
    'import.subtitle': 'Paste bank exports or spreadsheet rows, preview them, then import only valid items.',
    'import.csvLabel': 'CSV text',
    'import.placeholder': 'date,description,category,amount\n2026-04-01,Coffee,Food,4.50',
    'import.preview': 'Preview import',
    'import.confirm': 'Import valid rows',
    'import.clear': 'Clear',
    'import.empty': 'Paste CSV data and preview it before importing.',
    'import.statusCol': 'Status',
    'common.actions': 'Actions',
    'common.cancelEdit': 'Cancel edit',
    'common.allCategories': 'All categories',
    'common.edit': 'Edit',
    'common.delete': 'Delete',
    'common.activate': 'Activate',
    'common.pause': 'Pause',
    'common.left': 'left',
    'common.due': 'Due',
    'common.saved': 'saved',
    'status.loggedIn': 'You are signed in.',
    'status.registered': 'Account created successfully.',
    'status.expenseSaved': 'Expense saved.',
    'status.expenseUpdated': 'Expense updated.',
    'status.expenseDeleted': 'Expense deleted.',
    'status.budgetSaved': 'Budget saved.',
    'status.goalSaved': 'Goal saved.',
    'status.goalUpdated': 'Goal updated.',
    'status.goalDeleted': 'Goal deleted.',
    'status.categoryBudgetSaved': 'Category budget saved.',
    'status.categoryBudgetDeleted': 'Category budget deleted.',
    'status.recurringSaved': 'Recurring payment saved.',
    'status.recurringUpdated': 'Recurring payment updated.',
    'status.recurringDeleted': 'Recurring payment deleted.',
    'status.recurringGenerated': 'Due recurring payments were generated.',
    'status.seeded': 'Demo data added.',
    'status.importPreviewReady': 'Import preview is ready.',
    'status.importDone': 'Import finished.',
    'status.loggedOut': 'You have logged out.',
    'activeFilters.none': 'No filters applied.',
    'activeFilters.label': 'Active filters:',
    'coach.score': 'Health score',
    'coach.wins': 'What is going well',
    'coach.risks': 'What needs attention',
    'coach.actions': 'Next actions',
    'budget.spent': 'Spent this month',
    'budget.remaining': 'Remaining',
    'budget.projected': 'Projected month end',
    'budget.categories': 'Category budgets',
    'budget.used': 'used',
    'goal.remaining': 'Remaining',
    'goal.monthlyNeed': 'Needed each month',
    'goal.noDate': 'No target date',
    'goal.completed': 'Completed',
    'goal.inProgress': 'In progress',
    'import.ready': 'Ready',
    'import.duplicate': 'Duplicate',
    'import.invalid': 'Invalid',
    'empty.expenses': 'No expenses yet. Add your first one on the left.',
    'empty.goals': 'No savings goals yet. Create one to start planning ahead.',
    'empty.categoryBudgets': 'No category budgets yet.',
    'empty.recurring': 'No recurring payments yet.',
    'empty.breakdown': 'No data yet for this period.',
    'empty.daily': 'No daily trend yet.',
    'empty.monthly': 'No monthly trend data yet.',
    'empty.due': 'No upcoming recurring expenses.',
  },
  ru: {
    'hero.eyebrow': 'Пространство для личных финансов',
    'hero.copy': 'Отслеживай траты, планируй бюджеты, управляй регулярными платежами, копи на цели и получай полезные подсказки от ассистента.',
    'hero.guest': 'Войди в аккаунт, чтобы хранить траты, цели и регулярные платежи приватно.',
    'auth.title': 'Войти или создать аккаунт',
    'auth.subtitle': 'У каждого аккаунта свои траты, бюджеты, регулярные платежи и цели.',
    'auth.create': 'Создать аккаунт',
    'auth.signIn': 'Войти',
    'auth.name': 'Имя',
    'auth.email': 'Email',
    'auth.password': 'Пароль',
    'auth.namePlaceholder': 'Иван Иванов',
    'auth.emailPlaceholder': 'student@example.com',
    'auth.passwordPlaceholder': 'Минимум 8 символов',
    'auth.signInPasswordPlaceholder': 'Ваш пароль',
    'auth.createButton': 'Создать аккаунт',
    'auth.signInButton': 'Войти',
    'auth.logout': 'Выйти',
    'app.seed': 'Заполнить демо-данными',
    'app.refresh': 'Обновить',
    'expense.formTitle': 'Добавить трату',
    'expense.editTitle': 'Редактировать трату',
    'expense.formSubtitle': 'Быстро записывай траты и сразу обновляй дашборд.',
    'expense.amount': 'Сумма (€)',
    'expense.category': 'Категория',
    'expense.description': 'Описание',
    'expense.descriptionPlaceholder': 'Обед возле кампуса',
    'expense.date': 'Дата',
    'expense.save': 'Сохранить трату',
    'budget.title': 'Месячный бюджет',
    'budget.subtitle': 'Задай лимит и смотри, сколько ещё осталось в этом месяце.',
    'budget.limit': 'Лимит бюджета (€)',
    'budget.save': 'Сохранить бюджет',
    'assistant.title': 'Финансовый ассистент',
    'assistant.subtitle': 'Спроси про сводки, бюджеты, советы по экономии, цели, прогнозы или быстрые действия.',
    'assistant.empty': 'Спроси что-то вроде «Проанализируй мои траты» или «Создай цель Ноутбук 1200 до 2026-12-31».',
    'assistant.placeholder': 'Спроси про траты, бюджеты, цели или регулярные платежи',
    'assistant.send': 'Отправить',
    'dashboard.title': 'Дашборд',
    'dashboard.subtitle': 'Понимай расходы, замечай риски и быстро находи, чему нужно внимание.',
    'dashboard.period': 'Период',
    'dashboard.insights': 'Ключевые выводы',
    'dashboard.monthlyTrend': 'Тренд по месяцам',
    'dashboard.byCategory': 'Траты по категориям',
    'dashboard.dailyTrend': 'Дневной тренд',
    'dashboard.recurringSoon': 'Ближайшие регулярные',
    'period.thisWeek': 'Эта неделя',
    'period.thisMonth': 'Этот месяц',
    'period.last30Days': 'Последние 30 дней',
    'period.allTime': 'За всё время',
    'expenses.title': 'Траты',
    'expenses.subtitle': 'Фильтруй, просматривай, редактируй и выгружай свои записи.',
    'expenses.export': 'Экспорт CSV',
    'expenses.search': 'Поиск',
    'expenses.searchPlaceholder': 'кофе, аренда, такси...',
    'expenses.from': 'От',
    'expenses.to': 'До',
    'expenses.clearFilters': 'Сбросить фильтры',
    'goals.title': 'Цели накоплений',
    'goals.editTitle': 'Редактировать цель',
    'goals.subtitle': 'Следи, на что копишь и сколько ещё осталось.',
    'goals.name': 'Название цели',
    'goals.namePlaceholder': 'Ноутбук, отпуск, подушка безопасности',
    'goals.target': 'Целевая сумма (€)',
    'goals.current': 'Уже накоплено (€)',
    'goals.date': 'Дата цели',
    'goals.note': 'Заметка',
    'goals.notePlaceholder': 'Необязательно',
    'goals.save': 'Сохранить цель',
    'categoryBudgets.title': 'Лимиты по категориям',
    'categoryBudgets.editTitle': 'Редактировать лимит категории',
    'categoryBudgets.subtitle': 'Ограничивай отдельные категории вроде еды или транспорта и раньше замечай перерасход.',
    'categoryBudgets.limit': 'Месячный лимит (€)',
    'categoryBudgets.save': 'Сохранить лимит',
    'categoryBudgets.spent': 'Потрачено в этом месяце',
    'categoryBudgets.remaining': 'Осталось',
    'categoryBudgets.progress': 'Прогресс',
    'recurring.title': 'Регулярные платежи',
    'recurring.editTitle': 'Редактировать регулярный платёж',
    'recurring.subtitle': 'Управляй подписками, арендой, коммуналкой и другими повторяющимися тратами.',
    'recurring.descriptionPlaceholder': 'Spotify, аренда, интернет',
    'recurring.frequency': 'Частота',
    'recurring.monthly': 'Ежемесячно',
    'recurring.weekly': 'Еженедельно',
    'recurring.startDate': 'Дата начала',
    'recurring.save': 'Сохранить платёж',
    'recurring.generate': 'Сгенерировать начисления',
    'recurring.nextDue': 'Следующая дата',
    'recurring.state': 'Состояние',
    'import.title': 'Импорт трат из CSV',
    'import.subtitle': 'Вставь выгрузку из банка или таблицы, посмотри превью и импортируй только корректные строки.',
    'import.csvLabel': 'CSV текст',
    'import.placeholder': 'date,description,category,amount\n2026-04-01,Coffee,Food,4.50',
    'import.preview': 'Предпросмотр импорта',
    'import.confirm': 'Импортировать валидные строки',
    'import.clear': 'Очистить',
    'import.empty': 'Вставь CSV и сначала посмотри превью.',
    'import.statusCol': 'Статус',
    'common.actions': 'Действия',
    'common.cancelEdit': 'Отменить редактирование',
    'common.allCategories': 'Все категории',
    'common.edit': 'Редактировать',
    'common.delete': 'Удалить',
    'common.activate': 'Активировать',
    'common.pause': 'Пауза',
    'common.left': 'осталось',
    'common.due': 'Срок',
    'common.saved': 'накоплено',
    'status.loggedIn': 'Вход выполнен.',
    'status.registered': 'Аккаунт успешно создан.',
    'status.expenseSaved': 'Трата сохранена.',
    'status.expenseUpdated': 'Трата обновлена.',
    'status.expenseDeleted': 'Трата удалена.',
    'status.budgetSaved': 'Бюджет сохранён.',
    'status.goalSaved': 'Цель сохранена.',
    'status.goalUpdated': 'Цель обновлена.',
    'status.goalDeleted': 'Цель удалена.',
    'status.categoryBudgetSaved': 'Лимит категории сохранён.',
    'status.categoryBudgetDeleted': 'Лимит категории удалён.',
    'status.recurringSaved': 'Регулярный платёж сохранён.',
    'status.recurringUpdated': 'Регулярный платёж обновлён.',
    'status.recurringDeleted': 'Регулярный платёж удалён.',
    'status.recurringGenerated': 'Начисления по регулярным платежам созданы.',
    'status.seeded': 'Демо-данные добавлены.',
    'status.importPreviewReady': 'Предпросмотр импорта готов.',
    'status.importDone': 'Импорт завершён.',
    'status.loggedOut': 'Вы вышли из аккаунта.',
    'activeFilters.none': 'Фильтры не применены.',
    'activeFilters.label': 'Активные фильтры:',
    'coach.score': 'Оценка состояния',
    'coach.wins': 'Что идёт хорошо',
    'coach.risks': 'Что требует внимания',
    'coach.actions': 'Следующие шаги',
    'budget.spent': 'Потрачено в этом месяце',
    'budget.remaining': 'Осталось',
    'budget.projected': 'Прогноз на конец месяца',
    'budget.categories': 'Лимиты по категориям',
    'budget.used': 'использовано',
    'goal.remaining': 'Осталось',
    'goal.monthlyNeed': 'Нужно в месяц',
    'goal.noDate': 'Без даты',
    'goal.completed': 'Выполнена',
    'goal.inProgress': 'В процессе',
    'import.ready': 'Готово',
    'import.duplicate': 'Дубликат',
    'import.invalid': 'Ошибка',
    'empty.expenses': 'Пока нет трат. Добавь первую запись слева.',
    'empty.goals': 'Пока нет целей накоплений. Создай цель, чтобы начать планировать.',
    'empty.categoryBudgets': 'Пока нет лимитов по категориям.',
    'empty.recurring': 'Пока нет регулярных платежей.',
    'empty.breakdown': 'За этот период пока нет данных.',
    'empty.daily': 'Пока нет дневного тренда.',
    'empty.monthly': 'Пока нет данных по месяцам.',
    'empty.due': 'Пока нет ближайших регулярных платежей.',
  },
};

const state = {
  lang: localStorage.getItem('expensemate-lang') || 'en',
  user: null,
  categories: [],
  expenses: [],
  recurringExpenses: [],
  goals: [],
  categoryBudgetStatuses: [],
  overview: null,
  categoryBreakdown: [],
  dailyTrend: [],
  monthlyTrend: [],
  insights: [],
  coach: null,
  dueSummary: null,
  assistantSuggestions: [],
  assistantMessages: [],
  importPreview: null,
  editingExpenseId: null,
  editingRecurringId: null,
  editingGoalId: null,
  editingCategoryBudgetId: null,
};

const periodSelect = document.getElementById('period-select');
const authPanel = document.getElementById('auth-panel');
const appMain = document.getElementById('app-main');
const guestCopy = document.getElementById('guest-copy');
const userBox = document.getElementById('user-box');
const userName = document.getElementById('user-name');
const userEmail = document.getElementById('user-email');
const appActions = document.getElementById('app-actions');
const langButtons = { en: document.getElementById('lang-en-btn'), ru: document.getElementById('lang-ru-btn') };

const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');
const registerStatus = document.getElementById('register-status');
const loginStatus = document.getElementById('login-status');
const logoutBtn = document.getElementById('logout-btn');
const seedDemoBtn = document.getElementById('seed-demo-btn');
const refreshBtn = document.getElementById('refresh-btn');

const expenseForm = document.getElementById('expense-form');
const expenseFormTitle = document.getElementById('expense-form-title');
const expenseIdInput = document.getElementById('expense-id-input');
const expenseSubmitBtn = document.getElementById('expense-submit-btn');
const cancelExpenseEditBtn = document.getElementById('cancel-expense-edit-btn');
const categorySelect = document.getElementById('category-select');
const spentOnInput = document.getElementById('spent-on-input');
const expenseStatus = document.getElementById('expense-status');
const budgetForm = document.getElementById('budget-form');
const budgetInput = document.getElementById('budget-input');
const budgetStatus = document.getElementById('budget-status');

const assistantForm = document.getElementById('assistant-form');
const assistantInput = document.getElementById('assistant-input');
const assistantResponse = document.getElementById('assistant-response');
const assistantSuggestions = document.getElementById('assistant-suggestions');

const cardsContainer = document.getElementById('cards');
const budgetSummaryPanel = document.getElementById('budget-summary-panel');
const coachPanel = document.getElementById('coach-panel');
const insightsList = document.getElementById('insights-list');
const monthlyTrendContainer = document.getElementById('monthly-trend');
const categoryBreakdownContainer = document.getElementById('category-breakdown');
const dailyTrendContainer = document.getElementById('daily-trend');
const dueRecurringList = document.getElementById('due-recurring-list');

const searchInput = document.getElementById('search-input');
const filterCategorySelect = document.getElementById('filter-category-select');
const startDateInput = document.getElementById('start-date-input');
const endDateInput = document.getElementById('end-date-input');
const clearFiltersBtn = document.getElementById('clear-filters-btn');
const activeFilters = document.getElementById('active-filters');
const expensesBody = document.getElementById('expenses-body');
const exportBtn = document.getElementById('export-btn');

const goalForm = document.getElementById('goal-form');
const goalFormTitle = document.getElementById('goal-form-title');
const goalIdInput = document.getElementById('goal-id-input');
const goalSubmitBtn = document.getElementById('goal-submit-btn');
const cancelGoalEditBtn = document.getElementById('cancel-goal-edit-btn');
const goalStatus = document.getElementById('goal-status');
const goalCards = document.getElementById('goal-cards');

const categoryBudgetForm = document.getElementById('category-budget-form');
const categoryBudgetFormTitle = document.getElementById('category-budget-form-title');
const categoryBudgetIdInput = document.getElementById('category-budget-id-input');
const categoryBudgetSelect = document.getElementById('category-budget-select');
const categoryBudgetSubmitBtn = document.getElementById('category-budget-submit-btn');
const cancelCategoryBudgetEditBtn = document.getElementById('cancel-category-budget-edit-btn');
const categoryBudgetStatus = document.getElementById('category-budget-status');
const categoryBudgetBody = document.getElementById('category-budget-body');

const recurringForm = document.getElementById('recurring-form');
const recurringFormTitle = document.getElementById('recurring-form-title');
const recurringIdInput = document.getElementById('recurring-id-input');
const recurringCategorySelect = document.getElementById('recurring-category-select');
const recurringSubmitBtn = document.getElementById('recurring-submit-btn');
const cancelRecurringEditBtn = document.getElementById('cancel-recurring-edit-btn');
const recurringGenerateBtn = document.getElementById('generate-recurring-btn');
const recurringStatus = document.getElementById('recurring-status');
const recurringBody = document.getElementById('recurring-body');

const importCsvInput = document.getElementById('import-csv-input');
const previewImportBtn = document.getElementById('preview-import-btn');
const confirmImportBtn = document.getElementById('confirm-import-btn');
const clearImportBtn = document.getElementById('clear-import-btn');
const importStatus = document.getElementById('import-status');
const importSummary = document.getElementById('import-summary');
const importPreviewBody = document.getElementById('import-preview-body');

function t(key) {
  return translations[state.lang]?.[key] || translations.en[key] || key;
}

function setLang(lang) {
  state.lang = lang === 'ru' ? 'ru' : 'en';
  localStorage.setItem('expensemate-lang', state.lang);
  document.documentElement.lang = state.lang;
  Object.entries(langButtons).forEach(([code, btn]) => btn.classList.toggle('active', code === state.lang));
  applyTranslations();
  renderAll();
  if (state.user) {
    refreshAll().catch(handleGlobalError);
  }
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (key) el.textContent = t(key);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (key) el.setAttribute('placeholder', t(key));
  });
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function categoryLabel(category) {
  const map = {
    Food: { en: 'Food', ru: 'Еда' },
    Transport: { en: 'Transport', ru: 'Транспорт' },
    Shopping: { en: 'Shopping', ru: 'Покупки' },
    Bills: { en: 'Bills', ru: 'Счета' },
    Health: { en: 'Health', ru: 'Здоровье' },
    Education: { en: 'Education', ru: 'Учёба' },
    Entertainment: { en: 'Entertainment', ru: 'Развлечения' },
    Other: { en: 'Other', ru: 'Другое' },
  };
  return map[category]?.[state.lang] || category;
}

function money(value) {
  const number = Number(value || 0);
  return new Intl.NumberFormat(state.lang === 'ru' ? 'ru-RU' : 'en-IE', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(number);
}

function formatDate(value) {
  if (!value) return '—';
  const dt = new Date(`${value}T00:00:00`);
  return new Intl.DateTimeFormat(state.lang === 'ru' ? 'ru-RU' : 'en-IE', { dateStyle: 'medium' }).format(dt);
}

function formatApiError(data, status) {
  if (!data) return `HTTP ${status}`;
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => {
      const path = Array.isArray(item.loc) ? item.loc.join('.') : 'field';
      return `${path}: ${item.msg}`;
    }).join('; ');
  }
  if (typeof data.message === 'string') return data.message;
  return `HTTP ${status}`;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(formatApiError(data, response.status));
    error.status = response.status;
    throw error;
  }
  return data;
}

function setStatus(el, message = '', tone = '') {
  el.textContent = message;
  el.className = 'status';
  if (tone) el.classList.add(tone);
}

function handleGlobalError(error) {
  console.error(error);
  const message = error?.message || 'Unexpected error';
  setStatus(expenseStatus, message, 'error');
}

function getExpenseFilters() {
  const params = new URLSearchParams();
  if (searchInput.value.trim()) params.set('search', searchInput.value.trim());
  if (filterCategorySelect.value) params.set('category', filterCategorySelect.value);
  if (startDateInput.value) params.set('start_date', startDateInput.value);
  if (endDateInput.value) params.set('end_date', endDateInput.value);
  return params;
}

function fillCategorySelect(selectEl, includeAll = false) {
  const options = [];
  if (includeAll) options.push(`<option value="">${escapeHtml(t('common.allCategories'))}</option>`);
  state.categories.forEach((category) => {
    options.push(`<option value="${escapeHtml(category)}">${escapeHtml(categoryLabel(category))}</option>`);
  });
  selectEl.innerHTML = options.join('');
}

function applyCategorySelects() {
  const currentExpenseCategory = categorySelect.value;
  const currentRecurringCategory = recurringCategorySelect.value;
  const currentFilterCategory = filterCategorySelect.value;
  const currentCategoryBudget = categoryBudgetSelect.value;

  fillCategorySelect(categorySelect, false);
  fillCategorySelect(recurringCategorySelect, false);
  fillCategorySelect(filterCategorySelect, true);
  fillCategorySelect(categoryBudgetSelect, false);

  if (currentExpenseCategory) categorySelect.value = currentExpenseCategory;
  if (currentRecurringCategory) recurringCategorySelect.value = currentRecurringCategory;
  if (currentFilterCategory) filterCategorySelect.value = currentFilterCategory;
  if (currentCategoryBudget) categoryBudgetSelect.value = currentCategoryBudget;
  if (!categorySelect.value && categorySelect.options.length) categorySelect.selectedIndex = 0;
  if (!recurringCategorySelect.value && recurringCategorySelect.options.length) recurringCategorySelect.selectedIndex = 0;
  if (!categoryBudgetSelect.value && categoryBudgetSelect.options.length) categoryBudgetSelect.selectedIndex = 0;
}

function getAssistantDefaults() {
  return state.lang === 'ru'
    ? ['Проанализируй мои траты', 'Установи бюджет 500', 'Создай цель Ноутбук 1200 до 2026-12-31', 'Сделай прогноз на месяц', 'Покажи мои цели']
    : ['Analyze my spending', 'Set budget 500', 'Create goal Laptop 1200 by 2026-12-31', 'Forecast this month', 'Show my goals'];
}

function resetAssistantConversation() {
  state.assistantMessages = [{
    role: 'assistant',
    tone: 'hint',
    content: t('assistant.empty'),
  }];
}

function pushAssistantMessage(role, content, tone = '') {
  state.assistantMessages.push({ role, content, tone });
}

function updatePendingAssistantMessage(content, tone = '') {
  for (let index = state.assistantMessages.length - 1; index >= 0; index -= 1) {
    const item = state.assistantMessages[index];
    if (item.role === 'assistant' && item.tone === 'pending') {
      item.content = content;
      item.tone = tone;
      return;
    }
  }
  pushAssistantMessage('assistant', content, tone);
}

function renderAssistantConversation() {
  if (!state.assistantMessages.length) {
    resetAssistantConversation();
  }

  assistantResponse.classList.remove('empty-state');
  assistantResponse.innerHTML = state.assistantMessages.map((item) => `
    <article class="assistant-bubble assistant-bubble-${escapeHtml(item.role)} ${item.tone ? `assistant-bubble-${escapeHtml(item.tone)}` : ''}">
      <div class="assistant-bubble-label">${item.role === 'user' ? escapeHtml(state.lang === 'ru' ? 'Вы' : 'You') : escapeHtml(state.lang === 'ru' ? 'Ассистент' : 'Assistant')}</div>
      <div class="assistant-bubble-text">${escapeHtml(item.content || '')}</div>
    </article>
  `).join('');

  assistantResponse.scrollTop = assistantResponse.scrollHeight;
}

async function loadCurrentUser() {
  try {
    const user = await api('/api/auth/me');
    state.user = user;
    return user;
  } catch (error) {
    if (error.status === 401) {
      state.user = null;
      return null;
    }
    throw error;
  }
}

async function refreshAll() {
  const filters = getExpenseFilters();
  const [categories, expenses, overview, breakdown, daily, monthly, insights, recurring, budget, categoryBudgetStatuses, goals, coach] = await Promise.all([
    api('/api/categories'),
    api(`/api/expenses?${filters.toString()}`),
    api(`/api/stats/overview?period=${encodeURIComponent(periodSelect.value)}&lang=${state.lang}`),
    api(`/api/stats/by-category?period=${encodeURIComponent(periodSelect.value)}`),
    api('/api/stats/daily?days=14'),
    api(`/api/stats/monthly?months=6&lang=${state.lang}`),
    api(`/api/stats/insights?lang=${state.lang}`),
    api('/api/recurring'),
    api('/api/budget'),
    api('/api/budget/categories/status'),
    api('/api/goals/status'),
    api(`/api/coach/summary?lang=${state.lang}`),
  ]);

  state.categories = categories;
  state.expenses = expenses;
  state.overview = overview;
  state.categoryBreakdown = breakdown;
  state.dailyTrend = daily;
  state.monthlyTrend = monthly;
  state.insights = insights;
  state.recurringExpenses = recurring;
  state.budget = budget;
  state.categoryBudgetStatuses = categoryBudgetStatuses;
  state.goals = goals;
  state.coach = coach;
  state.dueSummary = overview.due_recurring_summary;
  applyCategorySelects();
  renderAll();
}

function renderCards() {
  if (!state.overview?.cards?.length) {
    cardsContainer.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.breakdown'))}</div>`;
    return;
  }
  cardsContainer.innerHTML = state.overview.cards.map((card) => `
    <article class="card">
      <div class="card-label">${escapeHtml(card.label)}</div>
      <div class="card-value">${escapeHtml(card.value)}</div>
      <div class="card-help">${escapeHtml(card.help_text)}</div>
    </article>
  `).join('');
}

function renderBudgetSummary() {
  const budgetStatus = state.overview?.budget_status;
  if (!budgetStatus) {
    budgetSummaryPanel.innerHTML = '';
    budgetInput.value = state.budget?.monthly_limit ? Number(state.budget.monthly_limit).toFixed(2) : '';
    return;
  }
  budgetInput.value = budgetStatus.monthly_limit ? Number(budgetStatus.monthly_limit).toFixed(2) : '';
  budgetSummaryPanel.innerHTML = `
    <section class="budget-hero">
      <div class="budget-hero-grid">
        <article class="mini-stat">
          <div class="mini-stat-label">${escapeHtml(t('budget.spent'))}</div>
          <div class="mini-stat-value">${money(budgetStatus.spent_this_month)}</div>
        </article>
        <article class="mini-stat">
          <div class="mini-stat-label">${escapeHtml(t('budget.remaining'))}</div>
          <div class="mini-stat-value ${budgetStatus.is_over_budget ? 'danger-text' : ''}">${budgetStatus.is_over_budget ? '-' : ''}${money(Math.abs(Number(budgetStatus.remaining_amount)))}</div>
        </article>
        <article class="mini-stat">
          <div class="mini-stat-label">${escapeHtml(t('budget.projected'))}</div>
          <div class="mini-stat-value">${money(budgetStatus.projected_total)}</div>
        </article>
        <article class="mini-stat">
          <div class="mini-stat-label">${escapeHtml(t('budget.categories'))}</div>
          <div class="mini-stat-value">${state.categoryBudgetStatuses.length}</div>
        </article>
      </div>
    </section>
  `;
}

function renderCoach() {
  if (!state.coach) {
    coachPanel.innerHTML = '';
    return;
  }
  const listBlock = (title, items) => `
    <div class="coach-list">
      <h4>${escapeHtml(title)}</h4>
      <ul>${(items.length ? items : ['—']).map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
    </div>
  `;
  coachPanel.innerHTML = `
    <section class="coach-shell">
      <div class="coach-score">
        <div class="coach-score-circle">
          <div>
            <div class="coach-score-value">${state.coach.health_score}</div>
            <div class="coach-score-label">${escapeHtml(t('coach.score'))}</div>
          </div>
        </div>
      </div>
      <div class="coach-details">
        <h3>${escapeHtml(state.coach.headline)}</h3>
        <p class="coach-headline"></p>
        <div class="coach-lists">
          ${listBlock(t('coach.wins'), state.coach.wins || [])}
          ${listBlock(t('coach.risks'), state.coach.risks || [])}
          ${listBlock(t('coach.actions'), state.coach.next_actions || [])}
        </div>
      </div>
    </section>
  `;
}

function renderInsights() {
  if (!state.insights.length) {
    insightsList.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.breakdown'))}</div>`;
    return;
  }
  insightsList.innerHTML = state.insights.map((item) => `
    <article class="insight-card insight-${escapeHtml(item.tone || 'neutral')}">
      <div class="insight-title">${escapeHtml(item.title)}</div>
      <p>${escapeHtml(item.detail)}</p>
    </article>
  `).join('');
}

function renderMonthlyTrend() {
  if (!state.monthlyTrend.length) {
    monthlyTrendContainer.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.monthly'))}</div>`;
    return;
  }
  const max = Math.max(...state.monthlyTrend.map((item) => Number(item.total_amount)), 1);
  monthlyTrendContainer.innerHTML = state.monthlyTrend.map((item) => {
    const height = Math.max((Number(item.total_amount) / max) * 170, 10);
    return `
      <article class="month-bar-card">
        <div class="month-bar-wrap"><div class="month-bar" style="height:${height}px"></div></div>
        <div class="month-amount">${money(item.total_amount)}</div>
        <div class="month-label">${escapeHtml(item.month_label)}</div>
      </article>
    `;
  }).join('');
}

function renderCategoryBreakdown() {
  if (!state.categoryBreakdown.length) {
    categoryBreakdownContainer.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.breakdown'))}</div>`;
    return;
  }
  const max = Math.max(...state.categoryBreakdown.map((item) => Number(item.total_amount)), 1);
  categoryBreakdownContainer.innerHTML = state.categoryBreakdown.map((item) => `
    <div class="breakdown-row">
      <div class="row-meta">
        <strong>${escapeHtml(categoryLabel(item.category))}</strong>
        <span>${money(item.total_amount)} · ${item.count}</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:${(Number(item.total_amount) / max) * 100}%"></div></div>
    </div>
  `).join('');
}

function renderDailyTrend() {
  if (!state.dailyTrend.length) {
    dailyTrendContainer.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.daily'))}</div>`;
    return;
  }
  const max = Math.max(...state.dailyTrend.map((item) => Number(item.total_amount)), 1);
  dailyTrendContainer.innerHTML = state.dailyTrend.map((item) => `
    <div class="trend-row">
      <div class="row-meta">
        <strong>${escapeHtml(formatDate(item.day))}</strong>
        <span>${money(item.total_amount)}</span>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:${(Number(item.total_amount) / max) * 100}%"></div></div>
    </div>
  `).join('');
}

function renderDueRecurring() {
  if (!state.dueSummary?.next_due_items?.length) {
    dueRecurringList.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.due'))}</div>`;
    return;
  }
  dueRecurringList.innerHTML = state.dueSummary.next_due_items.map((item) => `
    <div class="breakdown-row">
      <div class="row-meta">
        <strong>${escapeHtml(item.description)}</strong>
        <span>${money(item.amount)}</span>
      </div>
      <div class="row-meta">
        <span>${escapeHtml(categoryLabel(item.category))} · ${escapeHtml(item.frequency)}</span>
        <span>${escapeHtml(formatDate(item.next_due_on))}</span>
      </div>
    </div>
  `).join('');
}

function renderExpenses() {
  if (!state.expenses.length) {
    expensesBody.innerHTML = `<tr><td colspan="5"><div class="empty-state">${escapeHtml(t('empty.expenses'))}</div></td></tr>`;
  } else {
    expensesBody.innerHTML = state.expenses.map((item) => `
      <tr>
        <td>${escapeHtml(formatDate(item.spent_on))}</td>
        <td>${escapeHtml(item.description)}</td>
        <td><span class="chip">${escapeHtml(categoryLabel(item.category))}</span></td>
        <td class="money">${money(item.amount)}</td>
        <td>
          <div class="table-actions">
            <button class="secondary table-btn" type="button" data-expense-edit="${item.id}">${escapeHtml(t('common.edit'))}</button>
            <button class="danger table-btn" type="button" data-expense-delete="${item.id}">${escapeHtml(t('common.delete'))}</button>
          </div>
        </td>
      </tr>
    `).join('');
  }
  expensesBody.querySelectorAll('[data-expense-edit]').forEach((button) => {
    button.addEventListener('click', () => {
      const item = state.expenses.find((entry) => entry.id === Number(button.dataset.expenseEdit));
      if (item) startEditingExpense(item);
    });
  });
  expensesBody.querySelectorAll('[data-expense-delete]').forEach((button) => {
    button.addEventListener('click', async () => {
      try {
        await api(`/api/expenses/${button.dataset.expenseDelete}`, { method: 'DELETE' });
        if (state.editingExpenseId === Number(button.dataset.expenseDelete)) resetExpenseForm();
        setStatus(expenseStatus, t('status.expenseDeleted'), 'success');
        await refreshAll();
      } catch (error) {
        setStatus(expenseStatus, error.message, 'error');
      }
    });
  });
}

function renderGoals() {
  if (!state.goals.length) {
    goalCards.innerHTML = `<div class="empty-state">${escapeHtml(t('empty.goals'))}</div>`;
    return;
  }
  goalCards.innerHTML = state.goals.map((goal) => `
    <article class="goal-card">
      <div class="goal-head">
        <div>
          <div class="goal-title">${escapeHtml(goal.title)}</div>
          <div class="goal-meta">${escapeHtml(goal.note || '')}</div>
        </div>
        <span class="goal-pill ${goal.is_completed ? 'done' : 'active'}">${escapeHtml(goal.is_completed ? t('goal.completed') : t('goal.inProgress'))}</span>
      </div>
      <div class="row-meta">
        <span>${money(goal.current_amount)} ${escapeHtml(t('common.saved'))}</span>
        <strong>${money(goal.target_amount)}</strong>
      </div>
      <div class="bar-track"><div class="bar-fill" style="width:${Math.min(goal.progress_percent, 100)}%"></div></div>
      <div class="goal-footer">
        <div class="goal-meta">
          <div>${escapeHtml(t('goal.remaining'))}: ${money(goal.remaining_amount)}</div>
          <div>${goal.target_date ? escapeHtml(formatDate(goal.target_date)) : escapeHtml(t('goal.noDate'))}</div>
          <div>${goal.monthly_required ? `${escapeHtml(t('goal.monthlyNeed'))}: ${money(goal.monthly_required)}` : ''}</div>
        </div>
        <div class="goal-actions">
          <button class="secondary table-btn" type="button" data-goal-edit="${goal.id}">${escapeHtml(t('common.edit'))}</button>
          <button class="danger table-btn" type="button" data-goal-delete="${goal.id}">${escapeHtml(t('common.delete'))}</button>
        </div>
      </div>
    </article>
  `).join('');
  goalCards.querySelectorAll('[data-goal-edit]').forEach((button) => {
    button.addEventListener('click', () => {
      const item = state.goals.find((entry) => entry.id === Number(button.dataset.goalEdit));
      if (item) startEditingGoal(item);
    });
  });
  goalCards.querySelectorAll('[data-goal-delete]').forEach((button) => {
    button.addEventListener('click', async () => {
      try {
        await api(`/api/goals/${button.dataset.goalDelete}`, { method: 'DELETE' });
        if (state.editingGoalId === Number(button.dataset.goalDelete)) resetGoalForm();
        setStatus(goalStatus, t('status.goalDeleted'), 'success');
        await refreshAll();
      } catch (error) {
        setStatus(goalStatus, error.message, 'error');
      }
    });
  });
}

function renderCategoryBudgets() {
  if (!state.categoryBudgetStatuses.length) {
    categoryBudgetBody.innerHTML = `<tr><td colspan="6"><div class="empty-state">${escapeHtml(t('empty.categoryBudgets'))}</div></td></tr>`;
    return;
  }
  categoryBudgetBody.innerHTML = state.categoryBudgetStatuses.map((item) => {
    const over = Number(item.remaining_amount) < 0;
    return `
      <tr>
        <td><span class="chip">${escapeHtml(categoryLabel(item.category))}</span></td>
        <td class="money">${money(item.monthly_limit)}</td>
        <td class="money">${money(item.spent_this_month)}</td>
        <td class="${over ? 'danger-text' : ''}">${over ? '-' : ''}${money(Math.abs(Number(item.remaining_amount)))}</td>
        <td>
          <div class="table-progress">
            <div class="bar-track"><div class="bar-fill ${over ? 'bar-fill-warning' : ''}" style="width:${Math.min(item.percent_used, 100)}%"></div></div>
            <div class="table-progress-label">${item.percent_used}% ${escapeHtml(t('budget.used'))}</div>
          </div>
        </td>
        <td>
          <div class="table-actions">
            <button class="secondary table-btn" type="button" data-category-budget-edit="${item.id}">${escapeHtml(t('common.edit'))}</button>
            <button class="danger table-btn" type="button" data-category-budget-delete="${item.id}">${escapeHtml(t('common.delete'))}</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
  categoryBudgetBody.querySelectorAll('[data-category-budget-edit]').forEach((button) => {
    button.addEventListener('click', () => {
      const item = state.categoryBudgetStatuses.find((entry) => entry.id === Number(button.dataset.categoryBudgetEdit));
      if (item) startEditingCategoryBudget(item);
    });
  });
  categoryBudgetBody.querySelectorAll('[data-category-budget-delete]').forEach((button) => {
    button.addEventListener('click', async () => {
      try {
        await api(`/api/budget/categories/${button.dataset.categoryBudgetDelete}`, { method: 'DELETE' });
        if (state.editingCategoryBudgetId === Number(button.dataset.categoryBudgetDelete)) resetCategoryBudgetForm();
        setStatus(categoryBudgetStatus, t('status.categoryBudgetDeleted'), 'success');
        await refreshAll();
      } catch (error) {
        setStatus(categoryBudgetStatus, error.message, 'error');
      }
    });
  });
}

function renderRecurring() {
  if (!state.recurringExpenses.length) {
    recurringBody.innerHTML = `<tr><td colspan="7"><div class="empty-state">${escapeHtml(t('empty.recurring'))}</div></td></tr>`;
    return;
  }
  recurringBody.innerHTML = state.recurringExpenses.map((item) => `
    <tr>
      <td>${escapeHtml(item.description)}</td>
      <td><span class="chip">${escapeHtml(categoryLabel(item.category))}</span></td>
      <td>${escapeHtml(item.frequency)}</td>
      <td>${escapeHtml(formatDate(item.next_due_on))}</td>
      <td class="money">${money(item.amount)}</td>
      <td>${item.is_active ? `<span class="badge badge-active">${state.lang === 'ru' ? 'Активен' : 'Active'}</span>` : `<span class="badge badge-inactive">${state.lang === 'ru' ? 'Пауза' : 'Paused'}</span>`}</td>
      <td>
        <div class="table-actions">
          <button class="secondary table-btn" type="button" data-recurring-edit="${item.id}">${escapeHtml(t('common.edit'))}</button>
          <button class="secondary table-btn" type="button" data-recurring-toggle="${item.id}">${escapeHtml(item.is_active ? t('common.pause') : t('common.activate'))}</button>
          <button class="danger table-btn" type="button" data-recurring-delete="${item.id}">${escapeHtml(t('common.delete'))}</button>
        </div>
      </td>
    </tr>
  `).join('');
  recurringBody.querySelectorAll('[data-recurring-edit]').forEach((button) => {
    button.addEventListener('click', () => {
      const item = state.recurringExpenses.find((entry) => entry.id === Number(button.dataset.recurringEdit));
      if (item) startEditingRecurring(item);
    });
  });
  recurringBody.querySelectorAll('[data-recurring-toggle]').forEach((button) => {
    button.addEventListener('click', async () => {
      const item = state.recurringExpenses.find((entry) => entry.id === Number(button.dataset.recurringToggle));
      if (!item) return;
      try {
        await api(`/api/recurring/${item.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            amount: Number(item.amount),
            category: item.category,
            description: item.description,
            frequency: item.frequency,
            start_date: item.start_date,
            is_active: !item.is_active,
          }),
        });
        setStatus(recurringStatus, state.lang === 'ru' ? 'Статус регулярного платежа обновлён.' : 'Recurring payment state updated.', 'success');
        await refreshAll();
      } catch (error) {
        setStatus(recurringStatus, error.message, 'error');
      }
    });
  });
  recurringBody.querySelectorAll('[data-recurring-delete]').forEach((button) => {
    button.addEventListener('click', async () => {
      try {
        await api(`/api/recurring/${button.dataset.recurringDelete}`, { method: 'DELETE' });
        if (state.editingRecurringId === Number(button.dataset.recurringDelete)) resetRecurringForm();
        setStatus(recurringStatus, t('status.recurringDeleted'), 'success');
        await refreshAll();
      } catch (error) {
        setStatus(recurringStatus, error.message, 'error');
      }
    });
  });
}

function renderImportPreview() {
  if (!state.importPreview) {
    importSummary.className = 'import-summary empty-state';
    importSummary.textContent = t('import.empty');
    importPreviewBody.innerHTML = '';
    confirmImportBtn.disabled = true;
    return;
  }
  const payload = state.importPreview;
  confirmImportBtn.disabled = payload.valid_rows === 0;
  importSummary.className = 'import-summary';
  importSummary.innerHTML = `
    <div class="import-summary-grid">
      <div class="mini-stat"><div class="mini-stat-label">Rows</div><div class="mini-stat-value">${payload.total_rows}</div></div>
      <div class="mini-stat"><div class="mini-stat-label">${state.lang === 'ru' ? 'Готово к импорту' : 'Ready to import'}</div><div class="mini-stat-value">${payload.valid_rows}</div></div>
      <div class="mini-stat"><div class="mini-stat-label">${state.lang === 'ru' ? 'Дубликаты' : 'Duplicates'}</div><div class="mini-stat-value">${payload.duplicate_rows}</div></div>
      <div class="mini-stat"><div class="mini-stat-label">${state.lang === 'ru' ? 'Ошибки' : 'Invalid'}</div><div class="mini-stat-value">${payload.invalid_rows}</div></div>
    </div>
  `;
  importPreviewBody.innerHTML = payload.preview_rows.map((row) => {
    let statusText = t('import.ready');
    let className = 'preview-ready';
    if (row.error_message) {
      statusText = `${t('import.invalid')}: ${row.error_message}`;
      className = 'preview-error';
    } else if (row.is_duplicate) {
      statusText = t('import.duplicate');
      className = 'preview-warning';
    }
    return `
      <tr>
        <td>${row.row_number}</td>
        <td>${escapeHtml(row.spent_on || '—')}</td>
        <td>${escapeHtml(row.description || '—')}</td>
        <td>${escapeHtml(row.category ? categoryLabel(row.category) : '—')}</td>
        <td>${row.amount ? money(row.amount) : '—'}</td>
        <td class="${className}">${escapeHtml(statusText)}</td>
      </tr>
    `;
  }).join('');
}

function renderAssistantSuggestions(extra = null) {
  if (Array.isArray(extra)) state.assistantSuggestions = extra;
  const items = [...new Set([...(state.assistantSuggestions || []), ...getAssistantDefaults()])].slice(0, 6);
  assistantSuggestions.innerHTML = items.map((item) => `<button class="suggestion-chip" type="button">${escapeHtml(item)}</button>`).join('');
  assistantSuggestions.querySelectorAll('.suggestion-chip').forEach((button) => {
    button.addEventListener('click', () => {
      assistantInput.value = button.textContent;
      assistantForm.requestSubmit();
    });
  });
}

function renderActiveFilters() {
  const parts = [];
  if (searchInput.value.trim()) parts.push(`${t('expenses.search')}: ${searchInput.value.trim()}`);
  if (filterCategorySelect.value) parts.push(`${t('expense.category')}: ${categoryLabel(filterCategorySelect.value)}`);
  if (startDateInput.value) parts.push(`${t('expenses.from')}: ${formatDate(startDateInput.value)}`);
  if (endDateInput.value) parts.push(`${t('expenses.to')}: ${formatDate(endDateInput.value)}`);
  activeFilters.textContent = parts.length ? `${t('activeFilters.label')} ${parts.join(' · ')}` : t('activeFilters.none');
}


function syncEditLabels() {
  expenseFormTitle.textContent = state.editingExpenseId ? t('expense.editTitle') : t('expense.formTitle');
  expenseSubmitBtn.textContent = state.editingExpenseId ? t('common.edit') : t('expense.save');
  cancelExpenseEditBtn.classList.toggle('hidden', !state.editingExpenseId);

  goalFormTitle.textContent = state.editingGoalId ? t('goals.editTitle') : t('goals.title');
  goalSubmitBtn.textContent = state.editingGoalId ? t('common.edit') : t('goals.save');
  cancelGoalEditBtn.classList.toggle('hidden', !state.editingGoalId);

  categoryBudgetFormTitle.textContent = state.editingCategoryBudgetId ? t('categoryBudgets.editTitle') : t('categoryBudgets.title');
  categoryBudgetSubmitBtn.textContent = state.editingCategoryBudgetId ? t('common.edit') : t('categoryBudgets.save');
  cancelCategoryBudgetEditBtn.classList.toggle('hidden', !state.editingCategoryBudgetId);

  recurringFormTitle.textContent = state.editingRecurringId ? t('recurring.editTitle') : t('recurring.title');
  recurringSubmitBtn.textContent = state.editingRecurringId ? t('common.edit') : t('recurring.save');
  cancelRecurringEditBtn.classList.toggle('hidden', !state.editingRecurringId);
}

function renderAuthState() {
  const signedIn = Boolean(state.user);
  authPanel.classList.toggle('hidden', signedIn);
  appMain.classList.toggle('hidden', !signedIn);
  userBox.classList.toggle('hidden', !signedIn);
  appActions.classList.toggle('hidden', !signedIn);
  guestCopy.classList.toggle('hidden', signedIn);
  if (signedIn) {
    userName.textContent = state.user.name;
    userEmail.textContent = state.user.email;
  }
}

function renderAll() {
  applyTranslations();
  renderAuthState();
  if (!state.user) {
    renderAssistantSuggestions();
    return;
  }
  applyCategorySelects();
  renderCards();
  renderBudgetSummary();
  renderCoach();
  renderInsights();
  renderMonthlyTrend();
  renderCategoryBreakdown();
  renderDailyTrend();
  renderDueRecurring();
  renderExpenses();
  renderGoals();
  renderCategoryBudgets();
  renderRecurring();
  renderImportPreview();
  renderAssistantConversation();
  renderAssistantSuggestions();
  renderActiveFilters();
  syncEditLabels();
}

function resetExpenseForm() {
  state.editingExpenseId = null;
  expenseIdInput.value = '';
  expenseForm.reset();
  spentOnInput.value = new Date().toISOString().slice(0, 10);
  if (state.categories[0]) categorySelect.value = state.categories[0];
  expenseFormTitle.textContent = t('expense.formTitle');
  expenseSubmitBtn.textContent = t('expense.save');
  cancelExpenseEditBtn.classList.add('hidden');
}

function startEditingExpense(item) {
  state.editingExpenseId = item.id;
  expenseIdInput.value = item.id;
  expenseForm.elements.namedItem('amount').value = Number(item.amount).toFixed(2);
  categorySelect.value = item.category;
  expenseForm.elements.namedItem('description').value = item.description;
  spentOnInput.value = item.spent_on;
  expenseFormTitle.textContent = t('expense.editTitle');
  expenseSubmitBtn.textContent = t('common.edit');
  cancelExpenseEditBtn.classList.remove('hidden');
  expenseForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetGoalForm() {
  state.editingGoalId = null;
  goalIdInput.value = '';
  goalForm.reset();
  goalFormTitle.textContent = t('goals.title');
  goalSubmitBtn.textContent = t('goals.save');
  cancelGoalEditBtn.classList.add('hidden');
}

function startEditingGoal(item) {
  state.editingGoalId = item.id;
  goalIdInput.value = item.id;
  goalForm.elements.namedItem('title').value = item.title;
  goalForm.elements.namedItem('target_amount').value = Number(item.target_amount).toFixed(2);
  goalForm.elements.namedItem('current_amount').value = Number(item.current_amount).toFixed(2);
  goalForm.elements.namedItem('target_date').value = item.target_date || '';
  goalForm.elements.namedItem('note').value = item.note || '';
  goalFormTitle.textContent = t('goals.editTitle');
  goalSubmitBtn.textContent = t('common.edit');
  cancelGoalEditBtn.classList.remove('hidden');
  goalForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetCategoryBudgetForm() {
  state.editingCategoryBudgetId = null;
  categoryBudgetIdInput.value = '';
  categoryBudgetForm.reset();
  if (state.categories[0]) categoryBudgetSelect.value = state.categories[0];
  categoryBudgetFormTitle.textContent = t('categoryBudgets.title');
  categoryBudgetSubmitBtn.textContent = t('categoryBudgets.save');
  cancelCategoryBudgetEditBtn.classList.add('hidden');
}

function startEditingCategoryBudget(item) {
  state.editingCategoryBudgetId = item.id;
  categoryBudgetIdInput.value = item.id;
  categoryBudgetSelect.value = item.category;
  categoryBudgetForm.elements.namedItem('monthly_limit').value = Number(item.monthly_limit).toFixed(2);
  categoryBudgetFormTitle.textContent = t('categoryBudgets.editTitle');
  categoryBudgetSubmitBtn.textContent = t('common.edit');
  cancelCategoryBudgetEditBtn.classList.remove('hidden');
  categoryBudgetForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetRecurringForm() {
  state.editingRecurringId = null;
  recurringIdInput.value = '';
  recurringForm.reset();
  recurringForm.elements.namedItem('start_date').value = new Date().toISOString().slice(0, 10);
  if (state.categories[0]) recurringCategorySelect.value = state.categories[0];
  recurringFormTitle.textContent = t('recurring.title');
  recurringSubmitBtn.textContent = t('recurring.save');
  cancelRecurringEditBtn.classList.add('hidden');
}

function startEditingRecurring(item) {
  state.editingRecurringId = item.id;
  recurringIdInput.value = item.id;
  recurringForm.elements.namedItem('amount').value = Number(item.amount).toFixed(2);
  recurringCategorySelect.value = item.category;
  recurringForm.elements.namedItem('description').value = item.description;
  recurringForm.elements.namedItem('frequency').value = item.frequency;
  recurringForm.elements.namedItem('start_date').value = item.start_date;
  recurringFormTitle.textContent = t('recurring.editTitle');
  recurringSubmitBtn.textContent = t('common.edit');
  cancelRecurringEditBtn.classList.remove('hidden');
  recurringForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function initializeApp() {
  setLang(state.lang);
  spentOnInput.value = new Date().toISOString().slice(0, 10);
  recurringForm.elements.namedItem('start_date').value = new Date().toISOString().slice(0, 10);
  resetAssistantConversation();
  renderAssistantSuggestions();
  applyTranslations();
  await loadCurrentUser();
  if (state.user) {
    await refreshAll();
  }
  renderAll();
}

registerForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  setStatus(registerStatus, '');
  try {
    const payload = {
      name: registerForm.elements.namedItem('name').value.trim(),
      email: registerForm.elements.namedItem('email').value.trim(),
      password: registerForm.elements.namedItem('password').value,
    };
    state.user = await api('/api/auth/register', { method: 'POST', body: JSON.stringify(payload) });
    setStatus(registerStatus, t('status.registered'), 'success');
    setStatus(loginStatus, '');
    registerForm.reset();
    resetAssistantConversation();
    await refreshAll();
    renderAll();
  } catch (error) {
    setStatus(registerStatus, error.message, 'error');
  }
});

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  setStatus(loginStatus, '');
  try {
    const payload = { email: loginForm.elements.namedItem('email').value.trim(), password: loginForm.elements.namedItem('password').value };
    state.user = await api('/api/auth/login', { method: 'POST', body: JSON.stringify(payload) });
    setStatus(loginStatus, t('status.loggedIn'), 'success');
    setStatus(registerStatus, '');
    loginForm.reset();
    resetAssistantConversation();
    await refreshAll();
    renderAll();
  } catch (error) {
    setStatus(loginStatus, error.message, 'error');
  }
});

logoutBtn.addEventListener('click', async () => {
  try {
    await api('/api/auth/logout', { method: 'POST' });
  } catch (_error) {
    // ignore network errors during logout cleanup
  }
  state.user = null;
  state.expenses = [];
  state.recurringExpenses = [];
  state.goals = [];
  state.categoryBudgetStatuses = [];
  resetAssistantConversation();
  renderAll();
  setStatus(loginStatus, t('status.loggedOut'), 'success');
});

expenseForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const payload = {
      amount: Number(expenseForm.elements.namedItem('amount').value),
      category: categorySelect.value,
      description: expenseForm.elements.namedItem('description').value.trim(),
      spent_on: expenseForm.elements.namedItem('spent_on').value,
    };
    const method = state.editingExpenseId ? 'PUT' : 'POST';
    const url = state.editingExpenseId ? `/api/expenses/${state.editingExpenseId}` : '/api/expenses';
    await api(url, { method, body: JSON.stringify(payload) });
    setStatus(expenseStatus, t(state.editingExpenseId ? 'status.expenseUpdated' : 'status.expenseSaved'), 'success');
    resetExpenseForm();
    await refreshAll();
  } catch (error) {
    setStatus(expenseStatus, error.message, 'error');
  }
});
cancelExpenseEditBtn.addEventListener('click', resetExpenseForm);

budgetForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    await api('/api/budget', { method: 'PUT', body: JSON.stringify({ monthly_limit: Number(budgetInput.value) }) });
    setStatus(budgetStatus, t('status.budgetSaved'), 'success');
    await refreshAll();
  } catch (error) {
    setStatus(budgetStatus, error.message, 'error');
  }
});

goalForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const payload = {
      title: goalForm.elements.namedItem('title').value.trim(),
      target_amount: Number(goalForm.elements.namedItem('target_amount').value),
      current_amount: Number(goalForm.elements.namedItem('current_amount').value || 0),
      target_date: goalForm.elements.namedItem('target_date').value || null,
      note: goalForm.elements.namedItem('note').value.trim(),
    };
    const method = state.editingGoalId ? 'PUT' : 'POST';
    const url = state.editingGoalId ? `/api/goals/${state.editingGoalId}` : '/api/goals';
    await api(url, { method, body: JSON.stringify(payload) });
    setStatus(goalStatus, t(state.editingGoalId ? 'status.goalUpdated' : 'status.goalSaved'), 'success');
    resetGoalForm();
    await refreshAll();
  } catch (error) {
    setStatus(goalStatus, error.message, 'error');
  }
});
cancelGoalEditBtn.addEventListener('click', resetGoalForm);

categoryBudgetForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const payload = { category: categoryBudgetSelect.value, monthly_limit: Number(categoryBudgetForm.elements.namedItem('monthly_limit').value) };
    await api('/api/budget/categories', { method: 'PUT', body: JSON.stringify(payload) });
    setStatus(categoryBudgetStatus, t('status.categoryBudgetSaved'), 'success');
    resetCategoryBudgetForm();
    await refreshAll();
  } catch (error) {
    setStatus(categoryBudgetStatus, error.message, 'error');
  }
});
cancelCategoryBudgetEditBtn.addEventListener('click', resetCategoryBudgetForm);

recurringForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const payload = {
      amount: Number(recurringForm.elements.namedItem('amount').value),
      category: recurringCategorySelect.value,
      description: recurringForm.elements.namedItem('description').value.trim(),
      frequency: recurringForm.elements.namedItem('frequency').value,
      start_date: recurringForm.elements.namedItem('start_date').value,
      is_active: true,
    };
    const method = state.editingRecurringId ? 'PUT' : 'POST';
    const url = state.editingRecurringId ? `/api/recurring/${state.editingRecurringId}` : '/api/recurring';
    await api(url, { method, body: JSON.stringify(payload) });
    setStatus(recurringStatus, t(state.editingRecurringId ? 'status.recurringUpdated' : 'status.recurringSaved'), 'success');
    resetRecurringForm();
    await refreshAll();
  } catch (error) {
    setStatus(recurringStatus, error.message, 'error');
  }
});
cancelRecurringEditBtn.addEventListener('click', resetRecurringForm);

recurringGenerateBtn.addEventListener('click', async () => {
  try {
    await api('/api/recurring/generate', { method: 'POST' });
    setStatus(recurringStatus, t('status.recurringGenerated'), 'success');
    await refreshAll();
  } catch (error) {
    setStatus(recurringStatus, error.message, 'error');
  }
});

assistantForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = assistantInput.value.trim();
  if (!message) return;

  pushAssistantMessage('user', message);
  pushAssistantMessage('assistant', state.lang === 'ru' ? 'Думаю…' : 'Thinking…', 'pending');
  renderAssistantConversation();
  assistantInput.value = '';

  try {
    const response = await api('/api/assistant/message', { method: 'POST', body: JSON.stringify({ message, lang: state.lang }) });
    updatePendingAssistantMessage(response.answer || (state.lang === 'ru' ? 'Не удалось получить ответ.' : 'Could not get a response.'));
    renderAssistantConversation();
    renderAssistantSuggestions(response.suggestions || []);
    await refreshAll();
  } catch (error) {
    updatePendingAssistantMessage(error.message || (state.lang === 'ru' ? 'Произошла ошибка.' : 'Something went wrong.'), 'error');
    renderAssistantConversation();
  }
});

periodSelect.addEventListener('change', () => refreshAll().catch(handleGlobalError));
[searchInput, startDateInput, endDateInput].forEach((input) => input.addEventListener('input', () => refreshAll().catch(handleGlobalError)));
filterCategorySelect.addEventListener('change', () => refreshAll().catch(handleGlobalError));
clearFiltersBtn.addEventListener('click', () => {
  searchInput.value = '';
  filterCategorySelect.value = '';
  startDateInput.value = '';
  endDateInput.value = '';
  refreshAll().catch(handleGlobalError);
});

previewImportBtn.addEventListener('click', async () => {
  try {
    const payload = await api('/api/import/csv/preview', { method: 'POST', body: JSON.stringify({ csv_text: importCsvInput.value }) });
    state.importPreview = payload;
    setStatus(importStatus, t('status.importPreviewReady'), 'success');
    renderImportPreview();
  } catch (error) {
    state.importPreview = null;
    renderImportPreview();
    setStatus(importStatus, error.message, 'error');
  }
});

confirmImportBtn.addEventListener('click', async () => {
  try {
    const result = await api('/api/import/csv', { method: 'POST', body: JSON.stringify({ csv_text: importCsvInput.value }) });
    setStatus(importStatus, `${t('status.importDone')} ${result.imported_count}/${result.total_rows}`, 'success');
    state.importPreview = null;
    renderImportPreview();
    importCsvInput.value = '';
    await refreshAll();
  } catch (error) {
    setStatus(importStatus, error.message, 'error');
  }
});

clearImportBtn.addEventListener('click', () => {
  importCsvInput.value = '';
  state.importPreview = null;
  setStatus(importStatus, '');
  renderImportPreview();
});

seedDemoBtn.addEventListener('click', async () => {
  try {
    const result = await api('/api/demo/seed', { method: 'POST' });
    const totalCreated = (result.created_expenses || 0) + (result.created_recurring || 0) + (result.created_category_budgets || 0) + (result.created_goals || 0) + (result.created_budget || 0);
    const message = totalCreated > 0
      ? `${t('status.seeded')} (${result.created_expenses || 0} expenses, ${result.created_recurring || 0} recurring, ${result.created_category_budgets || 0} category budgets, ${result.created_goals || 0} goals${result.created_budget ? ', budget' : ''}).`
      : (state.lang === 'ru' ? 'Демо-данные уже были добавлены раньше.' : 'Demo data was already present.');
    setStatus(expenseStatus, message, 'success');
    await refreshAll();
  } catch (error) {
    setStatus(expenseStatus, error.message, 'error');
  }
});

refreshBtn.addEventListener('click', () => refreshAll().catch(handleGlobalError));
exportBtn.addEventListener('click', () => {
  const params = getExpenseFilters();
  window.open(`/api/expenses/export?${params.toString()}`, '_blank');
});

langButtons.en.addEventListener('click', () => setLang('en'));
langButtons.ru.addEventListener('click', () => setLang('ru'));

initializeApp().catch(handleGlobalError);

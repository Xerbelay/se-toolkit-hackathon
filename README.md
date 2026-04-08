# ExpenseMate

A web-based personal expense tracker with an assistant that helps users log expenses and understand spending patterns.

## Demo

Add screenshots here after you deploy the UI. Suggested screenshots:
- authentication screen
- expense form and expense table
- dashboard with analytics cards and monthly trend
- assistant answering a spending question
- recurring expenses section

## Product context

### End users
- students
- anyone who wants a simple way to track personal expenses

### Problem
People often do not understand where their money goes because tracking expenses manually is slow and inconvenient.

### Solution
ExpenseMate makes expense tracking fast through a simple web interface and adds an assistant that can summarize spending, manage budgets, and log an expense from natural-language input.

## Features

### Implemented
- create an account, sign in, and keep data isolated per user
- add, edit, delete, and list expenses
- categorize expenses
- filter expenses by category, search text, and date range
- export the current filtered expense list to CSV
- preview and import expenses from CSV with duplicate detection
- set a monthly budget and see the remaining amount for the current month
- set per-category monthly budgets such as Food, Transport, and Bills
- see summary cards for this week, this month, last 30 days, or all time
- see spending breakdown by category
- see daily spending trend for the last 14 days
- see monthly spending trend for the last 6 months
- see automatic insights such as top category, month-over-month change, budget warning, category budget warnings, and recurring due soon
- create recurring expenses for subscriptions or bills
- edit, pause, activate, or delete recurring expense schedules from the UI
- generate due recurring expenses automatically
- see dashboard cards for recurring expenses due today and due soon
- seed demo data for easier testing
- use an assistant with built-in commands such as:
  - `Add coffee 4.50 food`
  - `Set budget 500`
  - `Set food category budget 120`
  - `What is my food budget status?`
  - `Show category budgets`
  - `How much did I spend this month?`
  - `How much did I spend on food?`
  - `What is my largest expense this month?`
  - `What is my budget status?`
  - `Create recurring rent 320 bills monthly`
  - `What subscriptions are due soon?`
  - `Generate due recurring expenses`

### Not yet implemented
- recurring reminders or notifications by email/chat
- receipt upload and OCR
- richer LLM workflows using external APIs or tool calling
- mobile client

## Architecture

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Frontend:** static web app served through Caddy
- **Agent:** assistant endpoint with deterministic commands, contextual local fallback, and optional OpenRouter/OpenAI-compatible LLM support
- **Deployment:** Docker Compose on Ubuntu 24.04

## Usage

After starting the app:
- open `http://localhost:8080`
- create an account or sign in
- add an expense from the form or edit an existing one
- optionally click **Seed demo data**
- save a monthly budget in the left panel
- optionally set category-specific budgets such as Food or Transport
- use filters and export CSV from the expenses table
- paste CSV rows into the import panel, preview the detected columns, and import valid rows in bulk
- add recurring expenses such as rent, internet, or subscriptions
- click **Generate due now** to create expense entries from due recurring schedules
- explore analytics, category budget watchlist, and upcoming recurring items in the dashboard
- ask the assistant a question or add an expense through chat

Example assistant prompts:
- `Add lunch 12.50 food`
- `Set budget 500`
- `Set food category budget 120`
- `What is my food budget status?`
- `Show category budgets`
- `How much did I spend this week?`
- `How much did I spend on transport?`
- `What is my largest expense this month?`
- `What is my budget status?`
- `Show category breakdown`
- `Create recurring gym 19.99 health monthly`
- `What subscriptions are due soon?`
- `Generate due recurring expenses`

## Deployment

### VM operating system
Ubuntu 24.04

### What should be installed on the VM
- Docker Engine
- Docker Compose plugin
- Git

### Step-by-step deployment instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   ```

2. Create the environment file:
   ```bash
   cp .env.example .env
   ```

3. Start the project:
   ```bash
   docker compose up --build
   ```

4. Open the product in the browser:
   ```text
   http://localhost:8080
   ```

5. Stop the app when needed:
   ```bash
   docker compose down
   ```


### Useful helper files
- `scripts/check_project.sh` — quick local sanity check before a demo or deploy
- `docs/sample-expenses.csv` — example CSV for testing the import flow

### Running tests locally

From the `backend` directory:

```bash
pip install -e .[test]
pytest -q
```

## Optional LLM configuration

By default, the assistant works without any external API key using built-in rules.

To enable a more flexible OpenRouter/OpenAI-compatible LLM response path, set these variables in `.env`:
- `OPENAI_API_KEY`
- `OPENAI_API_BASE_URL`
- `OPENAI_MODEL`
- `OPENROUTER_SITE_URL`
- `OPENROUTER_APP_TITLE`

Recommended OpenRouter setup:

```env
OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openrouter/free
OPENROUTER_SITE_URL=http://localhost:8080
OPENROUTER_APP_TITLE=ExpenseMate
```

If the external model is temporarily unavailable, the assistant still falls back to built-in analytics and action guidance instead of returning a server error.

## Repository requirements checklist

- repository name: `se-toolkit-hackathon`
- MIT `LICENSE` file included
- `README.md` included
- backend + database + web + agent covered
- Dockerized services
- ready for VM deployment
- backend smoke tests included in `backend/tests`
- GitHub Actions CI workflow included

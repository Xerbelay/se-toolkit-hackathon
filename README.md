# ExpenseMate

A web-based personal expense tracker with an LLM-powered assistant that helps users log expenses and understand their spending.

## Demo

> Screenshots will be added after the UI is finalized during Version 2.
>
> Recommended screenshots to place in this section later:
> - dashboard page with expense list and category summary
> - AI assistant page answering a spending-related question

<!-- Example markdown to replace with real files later:
![Dashboard](docs/screenshots/dashboard.png)
![AI Assistant](docs/screenshots/assistant.png)
-->

## Product context

### End users

- Students
- Anyone who wants a simple way to track personal spending

### Problem that the product solves for end users

Many people do not clearly understand where their money goes. They often record expenses inconsistently, forget small purchases, and do not have a quick way to see spending patterns by category or by time period.

### Our solution

ExpenseMate is a simple expense tracking web application with an integrated LLM-powered assistant. It allows users to record expenses, browse expense history, and ask questions in natural language such as:

- “How much did I spend this week?”
- “How much did I spend on food this month?”
- “What is my largest expense?”

The project is intentionally built as a web app instead of a Telegram bot because Telegram bots are blocked on the university VM. This keeps the product fully compatible with the hackathon requirements while still including a user-facing client, backend, database, and AI agent.

## Implementation overview

### Architecture

- **Frontend:** web application for expense management and AI chat
- **Backend:** REST API for expense CRUD operations, summaries, and assistant tool endpoints
- **Database:** PostgreSQL for persistent storage of expenses and categories
- **LLM-powered agent:** web-based assistant connected to the backend and expense data
- **Deployment:** Docker Compose on Ubuntu 24.04 VM

### Version 1

Version 1 focuses on one core feature: **expense tracking**.

Planned Version 1 functionality:
- add a new expense
- view saved expenses in a list
- store expense amount, category, description, and date
- persist data in PostgreSQL
- connect web frontend to backend API

### Version 2

Version 2 improves the product and makes it more useful.

Planned Version 2 functionality:
- spending statistics by category
- weekly and monthly summaries
- filtering by date and category
- LLM-powered assistant in the web app
- containerized deployment on a VM
- improved UI/UX and final documentation

## Features

### Implemented / planned core features for the project

- expense creation
- expense history view
- category-based organization
- weekly and monthly summaries
- filtering by date and category
- LLM-powered natural-language assistant
- Dockerized deployment on a VM

### Not yet implemented / possible future improvements

- recurring expenses
- budget limits and alerts
- export to CSV
- charts and advanced analytics
- authentication for multiple users
- mobile client

## Usage

After the project is deployed, the product can be used as follows:

1. Open the web application in a browser.
2. Add a new expense by entering:
   - amount
   - category
   - description
   - date
3. View the saved expense history.
4. Use filters to inspect spending by category or by time period.
5. Open the AI assistant and ask questions about your spending in natural language.

### Example user actions

- add a food expense of 9.50 EUR
- check all expenses from this week
- ask the assistant how much was spent on transport this month

## Deployment

### VM operating system

This project is designed to run on **Ubuntu 24.04**.

### What should be installed on the VM

Install the following tools:

- Git
- Docker Engine
- Docker Compose plugin

Optional but convenient:

- curl
- make

### Environment variables

Create a `.env` file in the project root based on `.env.example` and fill in the required values.

Typical variables:

```env
POSTGRES_DB=expensemate
POSTGRES_USER=expensemate
POSTGRES_PASSWORD=change_me
DATABASE_URL=postgresql://expensemate:change_me@db:5432/expensemate
LLM_API_KEY=your_llm_api_key
LLM_API_BASE_URL=your_llm_api_base_url
LLM_MODEL=your_model_name
APP_PORT=80
```

### Step-by-step deployment instructions

1. Clone the repository on the VM:

```bash
git clone https://github.com/Xerbelay/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

2. Create the environment file:

```bash
cp .env.example .env
```

3. Edit `.env` and set the required secrets and configuration values.

4. Build and start all services:

```bash
docker compose up --build -d
```

5. Check that the containers are running:

```bash
docker compose ps
```

6. Open the product in the browser:

```text
http://<VM_IP>
```

7. To view logs if needed:

```bash
docker compose logs -f
```

8. To stop the application:

```bash
docker compose down
```

## Repository notes

- Repository name: `se-toolkit-hackathon`
- License: MIT
- The project should be fully containerized before final submission.
- The deployed Version 2 should be accessible for demonstration.

## Development notes

The recommended implementation stack for this project is:

- **Frontend:** React
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **AI integration:** LLM-powered assistant with tool access to expense data
- **Containerization:** Docker Compose

This stack matches the tooling used in the course and keeps the project simple, realistic, and easy to explain during the demo.

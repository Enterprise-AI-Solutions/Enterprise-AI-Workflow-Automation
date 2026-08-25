# ⚡ Enterprise AI Workflow Automation

> A production-ready AI-powered business workflow automation platform using **FastAPI**, **Claude AI**, **Google Workspace** (Gmail · Calendar · Drive · **Sheets**), **Airtable**, **n8n**, **Google Apps Script**, and **Docker**.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Claude AI](https://img.shields.io/badge/Claude-3.5_Sonnet-orange?logo=anthropic)](https://anthropic.com)
[![Google Sheets](https://img.shields.io/badge/Google_Sheets-API_v4-34A853?logo=googlesheets)](https://developers.google.com/sheets)
[![n8n](https://img.shields.io/badge/n8n-Workflow_Engine-EA4B71?logo=n8n)](https://n8n.io)
[![Airtable](https://img.shields.io/badge/Airtable-Database-18BFFF?logo=airtable)](https://airtable.com)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render)](https://render.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 What It Does

### The Big Picture — For Everyone

Imagine you run a business. Every day your team manually:
- Reads dozens of emails and decides who should handle them
- Copies invoice details from PDFs into spreadsheets by hand
- Schedules meetings by sending emails back and forth
- Pastes customer information into your CRM one row at a time

**This platform automates all of that using AI.** It watches your business tools (Gmail, Google Sheets, Google Drive, etc.), understands what's happening using AI, and takes the right action — all without anyone lifting a finger.

---

### How It Works — Step by Step

#### 📧 Example 1: A customer sends you an email

```
Customer emails you
       ↓
AI reads the email and decides: "This is a Sales Inquiry"
       ↓
Automatically adds the customer to your CRM spreadsheet (Airtable)
       ↓
Sends the customer an instant auto-reply
       ↓
You get a notification — no manual work needed
```

#### 🧾 Example 2: An invoice arrives

```
Invoice PDF lands in your inbox
       ↓
AI extracts: vendor name, amount ($40,702), due date (Aug 15)
       ↓
Logs it into your Airtable finance tracker automatically
       ↓
Emails your finance team: "New invoice from Cloud Services Ltd"
       ↓
Everything is recorded — no manual data entry
```

#### 📊 Example 3: You open Google Sheets

```
You open a Google Sheet with customer data
       ↓
Click ⚡ AI Workflows → "Classify selected rows"
       ↓
AI reads each row and adds a category column: "Hot Lead", "Support", etc.
       ↓
Or click "AI-fill sheet" → AI generates 10 rows of realistic test data
       ↓
No formulas. No manual typing. Done in seconds.
```

---

### What Each Tool Does

| Tool | What it is | Why we use it |
|---|---|---|
| **FastAPI** | The brain of the system — a web server that receives requests and coordinates everything | Fast, reliable, used by Netflix and Uber |
| **Claude AI** (Anthropic) | An AI that reads text and understands it like a human — classifies emails, extracts invoice fields, generates summaries | The smartest part of every workflow |
| **Gmail API** | Reads your inbox and sends emails automatically | Triggers workflows from real emails |
| **Google Calendar API** | Creates and reads calendar events | Schedules meetings without back-and-forth |
| **Google Drive API** | Reads files from your Drive | Monitors folders for new documents |
| **Google Sheets API** | Reads and writes spreadsheet data | Your live data dashboard and CRM |
| **Google Apps Script** | Small scripts that run inside Google Sheets | Adds a custom AI menu right in your spreadsheet |
| **Airtable** | A spreadsheet-database hybrid — great for CRMs, trackers, project management | Stores structured business data from workflows |
| **n8n** | A visual workflow builder (like Zapier, but self-hosted and free) | Connects everything without coding |
| **SQLite / PostgreSQL** | A database that stores your workflows, run history, and settings | The memory of the system |
| **Docker** | Packages everything so it runs the same on any computer or server | One command to start the whole stack |

---

### What You Can Build With This

- 📬 **Email triage system** — AI reads, classifies, and routes every email automatically
- 🧾 **Invoice processor** — AI extracts data from invoice text and logs it to Airtable
- 📅 **Meeting scheduler** — AI parses meeting requests and creates calendar events
- 📊 **Smart CRM** — Google Form submissions are AI-enriched and saved to your sheet
- 📁 **Document monitor** — New files in Drive are summarised and routed to the right team
- 🤖 **AI Sheets assistant** — Right-click menu in Google Sheets to classify, summarise, or AI-generate data

---

### What We Are NOT Using (and Why)

| Tool | Status | Reason |
|---|---|---|
| **Streamlit** | ❌ Not used | Streamlit is great for data science dashboards but is single-user and not suitable for multi-user business APIs. We use **FastAPI + HTML templates** instead — it's faster, production-ready, and supports real-time APIs. |
| **Render** | ✅ Added as deployment option | Render is a cloud platform (like Heroku) with a **free tier**. Deployment instructions are in the [Quick Start](#-quick-start) section below. |

---

## 🎭 Demo Mode — Works With Zero API Keys

You can run the **entire platform right now** without creating a single account or entering any API key. Every integration has a built-in demo mode that returns realistic sample data.

| Feature | With Zero API Keys | With Real API Keys |
|---|---|---|
| Dashboard UI | ✅ Fully works | ✅ Fully works |
| All API endpoints | ✅ Return realistic demo data | ✅ Return real data |
| AI classify / summarise / extract | ✅ Returns demo AI responses | ✅ Real Claude AI responses |
| Gmail read / send | ✅ Returns 5 sample emails | ✅ Reads your real inbox |
| Google Calendar | ✅ Returns 3 sample events | ✅ Your real calendar |
| Google Sheets read/write | ✅ Returns sample spreadsheet data | ✅ Your real spreadsheets |
| Airtable records | ✅ Returns demo CRM records | ✅ Your real Airtable base |
| n8n workflows | ✅ Returns demo workflow list | ✅ Your real n8n instance |
| Workflow execution | ✅ Simulates execution with logs | ✅ Runs real workflow steps |
| All 28 tests | ✅ Pass completely | ✅ Pass completely |

**To start in demo mode:**
```bash
uvicorn app.main:app --reload
```
That's it. No `.env` setup needed. Open http://localhost:8000 and explore everything.

---

## 💰 API Keys & Cost — Free vs Paid

All integrations have a **free tier or free alternative**. Here's the full breakdown:

### Claude AI (for AI features)

| Option | Cost | How to get it |
|---|---|---|
| **Anthropic Claude** | 💳 Paid (~$3–15 per million tokens) | [console.anthropic.com](https://console.anthropic.com) — add `ANTHROPIC_API_KEY` |
| **Google Gemini** ⭐ Free | ✅ Free tier (15 req/min, 1M tokens/day) | [aistudio.google.com](https://aistudio.google.com) — get `GEMINI_API_KEY` |
| **Groq** ⭐ Free | ✅ Completely free (LLaMA 3, Mixtral) | [console.groq.com](https://console.groq.com) — get `GROQ_API_KEY` |
| **Ollama** ⭐ Free | ✅ Free, runs locally on your computer | [ollama.com](https://ollama.com) — no API key needed |

> 💡 **Recommendation for getting started:** Use **Groq** (100% free, no credit card) or **Google Gemini** (free tier). Both give you real AI responses at zero cost.

### Google Workspace (Gmail, Calendar, Drive, Sheets)

| Cost | Details |
|---|---|
| ✅ **Free** | Included with any Google account. Just enable the APIs in [Google Cloud Console](https://console.cloud.google.com). The APIs themselves are free within generous limits. |

**Steps to get free Google API access:**
```
1. Go to console.cloud.google.com
2. Create a project (free)
3. Enable: Gmail API, Google Calendar API, Google Drive API, Google Sheets API
4. Create OAuth 2.0 credentials → download as credentials.json
5. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env
```

### Airtable

| Plan | Cost | Limits |
|---|---|---|
| **Free tier** ✅ | $0/month | 5 bases, 1,000 records/base, 1 GB storage |
| **Team** | $20/month | Unlimited records, more features |

Get your free API key: [airtable.com/create/tokens](https://airtable.com/create/tokens)

### n8n (Workflow Engine)

| Option | Cost | Notes |
|---|---|---|
| **Self-hosted** ✅ | Free forever | Runs via Docker in this project (`docker-compose up`) |
| **n8n Cloud** | Free tier (5 workflows, 5K executions/month) | [n8n.io/cloud](https://n8n.io/cloud) |

### Summary — Getting Started for Free

```
Step 1: Start in demo mode          → No keys needed, works instantly
Step 2: Add Google APIs             → Free, just enable in Google Cloud Console  
Step 3: Add Groq or Gemini AI      → Free, get key in 2 minutes
Step 4: Add Airtable (optional)    → Free tier available
Step 5: n8n runs via Docker        → Free, already in docker-compose.yml
```

**Total cost to run this platform: $0** using free tiers.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│            External Triggers & Entry Points                                     │
│  Gmail · Google Calendar · Google Drive · Google Sheets                         │
│  HTTP Webhooks · Cron Jobs                                                      │
│  Google Apps Script (apps_script/) — onEdit · onFormSubmit · menu clicks        │
└─────────────────────────────────┬───────────────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────────────────┐
│                        FastAPI Backend  app/  (port 8000)                       │
│                                                                                 │
│  app/routers/          → health · workflows · executions · ai                  │
│                          google_workspace · google_sheets · airtable · n8n      │
│                                                                                 │
│  app/services/ai/      → claude_service.py  (chat · classify · extract)        │
│  app/services/integrations/ → google_workspace · google_sheets · airtable · n8n│
│  app/services/workflow/ → workflow_service · execution_service                 │
│                                                                                 │
│  app/models/           → workflow · execution · user  (SQLAlchemy ORM)         │
│  app/templates/        → base.html · dashboard.html  (Jinja2 UI)               │
│  app/static/           → css/main.css · js/main.js                             │
│  app/utils/            → logger · helpers · exceptions                         │
└──────────┬──────────────────────────────────────────┬───────────────────────────┘
           │                                          │
    ┌──────▼───────────────┐              ┌───────────▼───────────────────┐
    │   Database           │              │   Claude AI  (Anthropic)      │
    │   SQLite (dev)       │              │   chat · classify · extract   │
    │   PostgreSQL (prod)  │              │   summarize · generate        │
    │   alembic/ migrations│              └───────────────────────────────┘
    └──────────────────────┘
┌────────────────────────────────────────────────────────────────────────────────┐
│  n8n Workflow Engine   n8n/workflows/  (port 5678)                             │
│  email_triage.json · invoice_processing.json · meeting_scheduler.json          │
└────────────────────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────────────────────┐
│  Google Apps Script   apps_script/                                             │
│  Config.gs · WorkflowAutomation.gs · EmailProcessor.gs                         │
│  SheetTriggers.gs · InvoiceProcessor.gs                                        │
└────────────────────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────────────────────┐
│  Deployment                                                                    │
│  docker/Dockerfile · docker-compose.yml  (app + PostgreSQL + Redis + n8n)      │
│  Render (free cloud) · GitHub Codespaces (browser dev)                         │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
Enterprise-AI-Workflow-Automation/
│
├── alembic/                               # Database migrations
│   └── versions/                          # Migration scripts
│
├── app/                                   # FastAPI application
│   ├── __init__.py
│   ├── main.py                            # App entry point & router registration
│   ├── config.py                          # Pydantic settings (reads from .env)
│   │
│   ├── api/
│   │   └── deps.py                        # Shared dependency injection
│   │
│   ├── models/
│   │   ├── execution.py                   # WorkflowExecution ORM model
│   │   ├── user.py                        # User model
│   │   └── workflow.py                    # Workflow ORM model
│   │
│   ├── routers/
│   │   ├── ai.py                          # Claude AI endpoints
│   │   ├── airtable.py                    # Airtable CRUD
│   │   ├── executions.py                  # Execution history & stats
│   │   ├── google_sheets.py               # Sheets CRUD + AI-fill
│   │   ├── google_workspace.py            # Gmail / Calendar / Drive
│   │   ├── health.py                      # GET /api/v1/health
│   │   ├── n8n.py                         # n8n management
│   │   └── workflows.py                   # Workflow CRUD + execute
│   │
│   ├── services/
│   │   ├── ai/
│   │   │   └── claude_service.py          # Anthropic Claude wrapper
│   │   ├── database/
│   │   │   ├── base.py                    # ORM base + timestamp mixin
│   │   │   └── session.py                 # Async SQLAlchemy engine
│   │   ├── integrations/
│   │   │   ├── __init__.py
│   │   │   ├── airtable.py                # Airtable REST API
│   │   │   ├── google_sheets.py           # Google Sheets API v4
│   │   │   ├── google_workspace.py        # Gmail, Calendar, Drive
│   │   │   └── n8n.py                     # n8n webhooks & REST API
│   │   └── workflow/
│   │       ├── execution_service.py       # Execution history
│   │       └── workflow_service.py        # Workflow CRUD + execution logic
│   │
│   ├── static/
│   │   ├── css/main.css                   # Dark-mode design system
│   │   └── js/main.js                     # Dashboard JavaScript
│   │
│   ├── templates/
│   │   ├── base.html                      # Base Jinja2 layout
│   │   └── dashboard.html                 # Interactive web dashboard
│   │
│   └── utils/
│       ├── exceptions.py                  # Custom HTTP exceptions
│       ├── helpers.py                     # Utility functions
│       └── logger.py                      # Structured logging
│
├── apps_script/                           # Google Apps Script (runs inside Sheets)
│   ├── appsscript.json                    # OAuth scopes manifest
│   ├── Config.gs                          # Shared helpers: apiPost, apiGet, toast
│   ├── EmailProcessor.gs                  # Gmail → Sheet triage pipeline
│   ├── InvoiceProcessor.gs                # AI invoice extraction + Airtable sync
│   ├── README.md                          # Setup guide
│   ├── SheetTriggers.gs                   # onEdit, onFormSubmit, Calendar sync
│   └── WorkflowAutomation.gs              # AI Workflows menu + health check
│
├── config/
│   └── logging_config.py                  # Logging configuration
│
├── docker/
│   ├── Dockerfile                         # Production image
│   └── Dockerfile.dev                     # Dev image with hot reload
│
├── docs/
│   ├── architecture.md                    # Detailed system architecture
│   └── deployment.md                      # Deployment guide
│
├── examples/
│   ├── crm/                               # CRM lead scoring
│   ├── engineering_docs/                  # Document summarisation
│   ├── gmail_processing/                  # Email triage walkthrough
│   ├── google_sheets/                     # Sheets read/write + AI-fill
│   │   ├── ai_fill_payload.json
│   │   ├── README.md
│   │   └── write_payload.json
│   └── invoice_processing/                # Invoice AI extraction
│
├── n8n/
│   └── workflows/                         # Importable n8n workflow JSON files
│       ├── email_triage.json
│       ├── invoice_processing.json
│       └── meeting_scheduler.json
│
├── scripts/
│   ├── seed_data.py                       # Sample workflow seeder
│   └── setup.py                           # One-shot environment setup
│
├── tests/
│   ├── conftest.py                        # Pytest fixtures (async client, DB)
│   ├── test_ai.py
│   ├── test_google_sheets.py
│   ├── test_health.py
│   ├── test_integrations.py
│   └── test_workflows.py
│
├── .env.example                           # All environment variables documented
├── .gitignore
├── alembic.ini                            # Alembic migration config
├── docker-compose.yml                     # Full stack: app + PostgreSQL + Redis + n8n
├── LICENSE
├── pytest.ini                             # Pytest configuration
├── README.md
├── requirements-dev.txt                   # Dev/test dependencies
└── requirements.txt                       # Production dependencies
```

---

## 🚀 Quick Start

### Option 1 — Local Development

#### 1. Clone the repository
```bash
git clone https://github.com/Enterprise-AI-Soutions/Enterprise-AI-Workflow-Automation.git
```

```bash
cd Enterprise-AI-Workflow-Automation
```

#### 2. Create and activate a virtual environment

**Windows (PowerShell)**
```powershell
python -m venv venv
```
```powershell
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables
```bash
cp .env.example .env
```

Open `.env` and fill in your API keys. The app runs fully in **demo mode** if you leave them blank.

**Windows (Notepad)**
```powershell
notepad .env
```

**macOS / Linux**
```bash
nano .env
```

#### 5. Run the development server
```bash
uvicorn app.main:app --reload
```

#### 6. (Optional) Seed sample workflow data
```bash
python scripts/seed_data.py
```

#### 7. Open in browser

| URL | Description |
|---|---|
| http://localhost:8000 | 🖥 Interactive Dashboard |
| http://localhost:8000/docs | 📖 Swagger API Docs |
| http://localhost:8000/redoc | 📄 ReDoc API Reference |
| http://localhost:8000/api/v1/health | 💚 Integration Health Check |

---

### Option 2 — Docker (Full Stack)

#### 1. Copy environment file
```bash
cp .env.example .env
```

#### 2. Start all services
```bash
docker-compose up --build -d
```

#### 3. Check all containers are running
```bash
docker-compose ps
```

#### 4. View application logs
```bash
docker-compose logs -f app
```

#### 5. Stop all services
```bash
docker-compose down
```

| Service | URL | Notes |
|---|---|---|
| FastAPI App | http://localhost:8000 | Main application |
| n8n Editor | http://localhost:5678 | `admin` / `changeme` |
| PostgreSQL | localhost:5432 | Internal only |
| Redis | localhost:6379 | Internal only |

---

### Option 3 — VSCode Setup

#### 1. Open the project in VSCode

**Windows (PowerShell):**
```powershell
code .
```

**macOS / Linux:**
```bash
code .
```

A popup will appear: **"Do you want to install the recommended extensions?"** — click **Install All**.

Extensions installed automatically from `.vscode/extensions.json`:
- **Python + Pylance** — IntelliSense, auto-complete, type checking
- **Ruff** — Fast linting (replaces flake8/pylint)
- **Black Formatter** — Auto-format your code on save
- **mypy** — Static type checking as you write
- **Docker** — Manage containers from the sidebar
- **REST Client** — Test API endpoints directly from `.http` files
- **DotENV** — Colour-coded `.env` file syntax
- **ErrorLens** — See errors inline instead of hovering

#### 2. Select the Python interpreter (point VSCode to your venv)

**Windows:**
```
Ctrl+Shift+P  ->  Python: Select Interpreter  ->  .\venv\Scripts\python.exe
```

**macOS / Linux:**
```
Ctrl+Shift+P  ->  Python: Select Interpreter  ->  ./venv/bin/python
```

#### 3. Add a debug launch config (press F5 to run)

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI: Dev Server",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload", "--port", "8000"],
      "jinja": true,
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

Press **F5** (or Run → Start Debugging) to launch with full breakpoint debugging.

#### 4. Configure and run tests visually

**macOS / Linux / Windows:**
```
Ctrl+Shift+P  ->  Python: Configure Tests  ->  pytest  ->  select "tests" folder
```

Click the **Testing** (beaker) icon in the left sidebar to run all 28 tests with a visual pass/fail report.

Or from the integrated terminal:
```bash
pytest tests/ -v
```

---

### Option 4 — GitHub Codespaces

No Python installation, no Docker, no local setup. GitHub spins up a full cloud environment with VSCode built into your browser.

> GitHub gives **60 free hours/month** on the free plan.

#### 1. Open in Codespaces

Go to the GitHub repo page, click the green **Code** button, then the **Codespaces** tab:
```
Code button  ->  Codespaces tab  ->  "Create codespace on main"
```

#### 2. Wait for the environment to build (about 60 seconds)

#### 3. Install dependencies (in the Codespace terminal)
```bash
pip install -r requirements.txt
```

#### 4. Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 5. Open the app in your browser

Codespaces shows an **"Open in Browser"** popup automatically. Or go to the **Ports** tab at the bottom and click the link next to port `8000`.

---

### Option 5 — Deploy to Render (Free Cloud Hosting)

[Render](https://render.com) hosts your app live on the internet for free. No credit card required for the free tier.

#### 1. Fork this repo on GitHub

#### 2. Sign up at render.com (free, no credit card)

#### 3. Create a new Web Service
```
Dashboard  ->  New  ->  Web Service  ->  Connect your GitHub fork
```

#### 4. Configure the build settings

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free |

#### 5. Add your environment variables
```
Render Dashboard  ->  Environment tab  ->  add keys from your .env file
```

#### 6. Click "Create Web Service" and wait for the build

Your app will be live at:
```
https://your-app-name.onrender.com
```

> **Free tier note:** Render sleeps after 15 min of inactivity — the first request after sleep takes ~30s to wake up. Upgrade to Starter ($7/month) for always-on hosting.

---

### Running Tests

Install dev dependencies first:
```bash
pip install -r requirements-dev.txt
```

Run all tests:
```bash
pytest tests/ -v
```

Run with a coverage report:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Run a single test file:
```bash
pytest tests/test_google_sheets.py -v
```

All **28 tests** pass with zero API keys — demo mode fallbacks are used for every integration.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | App + all integration statuses |
| GET | `/api/v1/workflows` | List all workflows |
| POST | `/api/v1/workflows` | Create workflow |
| GET | `/api/v1/workflows/{id}` | Get workflow |
| PUT | `/api/v1/workflows/{id}` | Update workflow |
| DELETE | `/api/v1/workflows/{id}` | Delete workflow |
| POST | `/api/v1/workflows/{id}/execute` | Run workflow |
| GET | `/api/v1/executions` | Execution history |
| GET | `/api/v1/executions/stats` | Success/failure stats |
| **POST** | **`/api/v1/ai/chat`** | Claude AI chat |
| **POST** | **`/api/v1/ai/summarize`** | Summarise text |
| **POST** | **`/api/v1/ai/classify`** | Classify text into categories |
| **POST** | **`/api/v1/ai/extract`** | Extract structured fields |
| **POST** | **`/api/v1/ai/generate-workflow`** | AI-generate workflow steps |
| GET | `/api/v1/google/gmail/messages` | List emails |
| POST | `/api/v1/google/gmail/send` | Send email |
| GET | `/api/v1/google/calendar/events` | List calendar events |
| POST | `/api/v1/google/calendar/events` | Create calendar event |
| GET | `/api/v1/google/drive/files` | List Drive files |
| **GET** | **`/api/v1/google/sheets`** | List spreadsheets from Drive ✨ |
| **POST** | **`/api/v1/google/sheets`** | Create new spreadsheet ✨ |
| **GET** | **`/api/v1/google/sheets/{id}`** | Get spreadsheet metadata ✨ |
| **GET** | **`/api/v1/google/sheets/{id}/values/{range}`** | Read cell values ✨ |
| **PUT** | **`/api/v1/google/sheets/{id}/values/{range}`** | Write cell values ✨ |
| **POST** | **`/api/v1/google/sheets/{id}/append`** | Append rows ✨ |
| **DELETE** | **`/api/v1/google/sheets/{id}/values/{range}`** | Clear range ✨ |
| **POST** | **`/api/v1/google/sheets/{id}/batch-read`** | Read multiple ranges ✨ |
| **POST** | **`/api/v1/google/sheets/{id}/format-headers`** | Style header row ✨ |
| **POST** | **`/api/v1/google/sheets/{id}/ai-fill`** | Claude generates data into sheet ✨ |
| GET | `/api/v1/airtable/bases` | List Airtable bases |
| GET | `/api/v1/airtable/bases/{b}/tables/{t}/records` | List records |
| POST | `/api/v1/airtable/bases/{b}/tables/{t}/records` | Create record |
| GET | `/api/v1/n8n/workflows` | List n8n workflows |
| POST | `/api/v1/n8n/trigger` | Trigger n8n webhook |

---

## 🔌 Integrations

| Integration | Env Variables | Docs |
|---|---|---|
| Claude AI | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| Gmail | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | [Google Cloud Console](https://console.cloud.google.com) |
| Google Calendar | Same as Gmail | — |
| Google Drive | Same as Gmail | — |
| **Google Sheets** | Same as Gmail | [Sheets API](https://developers.google.com/sheets/api) ✨ |
| Airtable | `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID` | [airtable.com/account](https://airtable.com/account) |
| n8n | `N8N_API_KEY`, `N8N_BASE_URL` | [docs.n8n.io](https://docs.n8n.io) |
| **Google Apps Script** | Script Properties (`API_BASE_URL`) | [apps_script/README.md](apps_script/README.md) ✨ |

---

## 📊 Google Sheets Features

### REST API Endpoints
Read, write, append, clear, batch-read, and format spreadsheets directly from the API.

```bash
# AI-generate a spreadsheet full of realistic data
curl -X POST http://localhost:8000/api/v1/google/sheets/YOUR_SHEET_ID/ai-fill \
  -H "Content-Type: application/json" \
  -d '{
    "headers": ["Name", "Email", "Company", "Revenue", "Status"],
    "prompt": "B2B SaaS leads from the US tech sector",
    "rows": 10
  }'
```

### Google Apps Script (in-sheet menu)
Paste the `apps_script/*.gs` files into any Google Sheet for a native **⚡ AI Workflows** menu:

| Menu Action | What It Does |
|---|---|
| 🤖 Classify selected rows | AI-classifies text in selected cells → writes category to next column |
| 📄 Summarise selected cell | Claude summarises a long text cell |
| 📧 Process inbox emails | Reads Gmail, classifies with AI, logs to **Email Triage** sheet |
| 📅 Sync calendar events | Pulls next 20 events into a **Calendar** sheet |
| ✨ AI-fill sheet with data | Claude generates structured rows into the active sheet |
| 🔄 Trigger workflow via API | Pick and run any workflow from the backend |
| 💚 Check API health | Shows all integration statuses in a dialog |
| 📋 View execution logs | Dumps execution history into an **Execution Logs** sheet |

**Setup:** See [apps_script/README.md](apps_script/README.md) for the 3-step installation guide.

---


## 📊 n8n Workflow Examples

Import these from `n8n/workflows/` via the n8n UI (Settings → Import Workflow).
See [`n8n/README.md`](n8n/README.md) for full setup instructions.

| # | Workflow | Trigger | AI Step | Actions |
|---|---|---|---|---|
| 1 | `email_triage.json` | Gmail webhook | Claude classify | Airtable CRM + auto-reply |
| 2 | `invoice_processing.json` | HTTP webhook | Claude extract | Airtable log + Gmail notify |
| 3 | `meeting_scheduler.json` | HTTP webhook | Claude extract | Calendar create + Gmail confirm |
| 4 | `lead_qualification.json` | HTTP webhook | Claude extract + score | Airtable CRM + Gmail sales alert |
| 5 | `daily_kpi_report.json` | Schedule (08:00) | Claude summarize | Google Sheets log + Gmail report |
| 6 | `support_ticket_auto_responder.json` | HTTP webhook | Claude classify + draft | Airtable log + Gmail reply + escalation |


---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and add tests
4. Run `pytest` and `ruff check .`
5. Open a Pull Request

---

## 📄 License

MIT — see [LICENSE](LICENSE)

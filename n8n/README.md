# n8n Workflows

This folder contains **6 production-ready n8n workflow JSON files** that integrate with the Enterprise AI Workflow Automation backend. Each workflow is fully importable into n8n Cloud or self-hosted n8n.

---

## How to Import

1. Open your **n8n Cloud** dashboard → [app.n8n.cloud](https://app.n8n.cloud)
2. Click **"Add Workflow"** → **"Import from File"**
3. Select one of the `.json` files from this folder
4. Set the required credentials and environment variables (see table below)
5. Click **"Activate"** to enable the workflow

---

## The 6 Workflows

| # | File | Trigger | What It Does |
|---|---|---|---|
| 1 | [`email_triage.json`](workflows/email_triage.json) | Webhook (Gmail) | Claude classifies incoming email → routes Sales leads to Airtable CRM → auto-replies |
| 2 | [`invoice_processing.json`](workflows/invoice_processing.json) | HTTP Webhook | Claude extracts invoice fields (vendor, amount, date) → logs to Airtable → Gmail notification |
| 3 | [`meeting_scheduler.json`](workflows/meeting_scheduler.json) | HTTP Webhook | Claude extracts meeting details from natural language → creates Google Calendar event → Gmail confirmation |
| 4 | [`lead_qualification.json`](workflows/lead_qualification.json) | Webhook | Claude extracts + scores lead quality → logs enriched record to Airtable → alerts sales team on hot leads |
| 5 | [`daily_kpi_report.json`](workflows/daily_kpi_report.json) | Schedule (08:00 daily) | Pulls Airtable + API stats → Claude writes executive summary → logs to Google Sheets + emails stakeholders |
| 6 | [`support_ticket_auto_responder.json`](workflows/support_ticket_auto_responder.json) | Webhook | Claude classifies ticket + drafts reply → logs to Airtable → sends AI-drafted reply → escalates urgent tickets |

---

## Architecture

All workflows connect to the FastAPI backend (`app` service, port 8000) rather than calling external AI/CRM APIs directly. This keeps credentials centralised and makes the workflows reusable across environments.

```
n8n Workflow
    │
    ├── Webhook / Schedule Trigger
    │
    ├── HTTP Request → http://app:8000/api/v1/ai/classify   (Claude AI)
    ├── HTTP Request → http://app:8000/api/v1/ai/extract    (Claude AI)
    ├── HTTP Request → http://app:8000/api/v1/ai/chat       (Claude AI)
    │
    ├── HTTP Request → http://app:8000/api/v1/airtable/...  (Airtable)
    ├── HTTP Request → http://app:8000/api/v1/google/gmail  (Gmail)
    └── HTTP Request → http://app:8000/api/v1/google/sheets (Google Sheets)
```

---

## Environment Variables Required

Set these in your `.env` file (see [`.env.example`](../.env.example)) **and** in your n8n instance:

| Variable | Used By | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | All AI nodes | Claude AI API key |
| `AIRTABLE_API_KEY` | Airtable nodes | Airtable personal access token |
| `AIRTABLE_BASE_ID` | Airtable nodes | Your Airtable base ID (`appXXXXXXXX`) |
| `GOOGLE_CLIENT_ID` | Gmail / Sheets / Calendar | Google OAuth 2.0 client ID |
| `GOOGLE_CLIENT_SECRET` | Gmail / Sheets / Calendar | Google OAuth 2.0 client secret |
| `N8N_API_KEY` | Backend → n8n | n8n API key for `/api/v1/n8n/*` endpoints |
| `N8N_BASE_URL` | Backend → n8n | Your n8n instance URL (e.g. `https://yourorg.app.n8n.cloud`) |
| `SALES_TEAM_EMAIL` | `lead_qualification` | Email address to alert on hot leads |
| `STAKEHOLDER_EMAILS` | `daily_kpi_report` | Comma-separated emails for daily KPI report |
| `SUPPORT_ESCALATION_EMAIL` | `support_ticket_auto_responder` | Email to escalate urgent tickets to |
| `KPI_SHEET_ID` | `daily_kpi_report` | Google Sheets ID for KPI log |
| `KPI_SHEET_URL` | `daily_kpi_report` | Public URL of the KPI Google Sheet |

---

## Workflow Details

### 1. Email Triage (`email_triage.json`)
**Trigger:** POST to `/webhook/email-triage`

```
Gmail Webhook → Claude Classify (Sales/Support/Finance/HR/Spam)
    → [Sales] → Airtable CRM (Leads table)
    → [Other] → Gmail Auto-Reply
```

### 2. Invoice Processing (`invoice_processing.json`)
**Trigger:** POST to `/webhook/invoice-processing`

```
HTTP Webhook → Claude Extract (vendor, amount, date, due_date, invoice_number)
    → Airtable (Invoices table)
    → Gmail Notify (finance team)
```

### 3. Meeting Scheduler (`meeting_scheduler.json`)
**Trigger:** POST to `/webhook/meeting-scheduler`

```
HTTP Webhook → Claude Extract (title, date, time, duration, attendees, agenda)
    → Google Calendar (create event)
    → Gmail (send confirmation to all attendees)
```

### 4. Lead Qualification (`lead_qualification.json`)
**Trigger:** POST to `/webhook/lead-qualification`

```
HTTP Webhook
    ├── Claude Extract (company, industry, size, use_case, budget, urgency)
    └── Claude Score  (Hot / Warm / Cold / Not a Fit)
    → Route: Hot Lead?
        → [Yes] Airtable CRM + Gmail Alert to sales team
        → [No]  Airtable CRM only
```

### 5. Daily KPI Report (`daily_kpi_report.json`)
**Trigger:** Schedule — every day at 08:00

```
Schedule Trigger
    ├── Airtable → Fetch executions
    ├── API → Get execution stats
    └── Airtable → Fetch leads data
    → Claude Summarize (executive KPI report)
        ├── Google Sheets → Log KPI entry
        └── Gmail → Email to stakeholders
```

### 6. Support Ticket Auto-Responder (`support_ticket_auto_responder.json`)
**Trigger:** POST to `/webhook/support-ticket`

```
HTTP Webhook
    ├── Claude Classify (Billing/Technical Bug/Feature Request/Account/General/Urgent)
    └── Claude Draft Response (AI-written reply email)
    → Route: Urgent?
        → [Yes] Airtable Log + Gmail to Customer + Gmail Escalation
        → [No]  Airtable Log + Gmail to Customer
```

---

## Local Development with Docker

When running locally via Docker Compose, n8n and the backend app run on the same Docker network. The `http://app:8000` URL resolves automatically inside the container.

```bash
# Start all services including n8n
docker-compose up -d

# n8n UI available at:
http://localhost:5678

# Backend API available at:
http://localhost:8000
```

Import workflows via the n8n UI at `localhost:5678`.

---

## Adding New Workflows

1. Design and test your workflow in the n8n UI
2. Click the workflow menu **⋮** → **Download** → save the `.json` to this folder
3. Name the file descriptively using `snake_case`: `my_workflow_name.json`
4. Update this README's workflow table
5. Commit and push

```bash
git add n8n/workflows/my_workflow_name.json n8n/README.md
git commit -m "feat(n8n): add my_workflow_name workflow"
git push origin main
```

"""n8n workflow automation integration."""

from __future__ import annotations

from typing import Any, Optional

import httpx

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

import random
from datetime import datetime, timezone, timedelta

_DEMO_WORKFLOWS = [
    {"id": "1", "name": "Email Triage Workflow",               "active": True,  "tags": ["email", "ai", "crm"]},
    {"id": "2", "name": "Invoice Processing",                  "active": True,  "tags": ["finance", "ai"]},
    {"id": "3", "name": "Meeting Scheduler",                   "active": True,  "tags": ["calendar", "ai"]},
    {"id": "4", "name": "Lead Qualification & CRM Enrichment", "active": True,  "tags": ["leads", "crm", "ai"]},
    {"id": "5", "name": "Daily KPI Report Generator",          "active": True,  "tags": ["reporting", "scheduled"]},
    {"id": "6", "name": "Support Ticket Auto-Responder",       "active": True,  "tags": ["support", "ai"]},
    {"id": "7", "name": "SAP Maintenance AI Alert (IW38)",     "active": True,  "tags": ["sap", "plant-maintenance", "ai"]},
]


def _make_demo_executions() -> list[dict]:
    """Generate realistic demo execution history for all 7 n8n workflows."""
    now = datetime.now(timezone.utc)
    wf_meta = [
        {"id": "1", "name": "Email Triage Workflow",               "emoji": "📧"},
        {"id": "2", "name": "Invoice Processing",                  "emoji": "🧾"},
        {"id": "3", "name": "Meeting Scheduler",                   "emoji": "📅"},
        {"id": "4", "name": "Lead Qualification & CRM Enrichment", "emoji": "🎯"},
        {"id": "5", "name": "Daily KPI Report Generator",          "emoji": "📊"},
        {"id": "6", "name": "Support Ticket Auto-Responder",       "emoji": "🎫"},
        {"id": "7", "name": "SAP Maintenance AI Alert (IW38)",     "emoji": "🏭"},
    ]
    statuses = ["success", "success", "success", "success", "error", "running"]
    output_templates = {
        "1": lambda s: {"category": random.choice(["Sales Inquiry","Support Request","Finance"]), "email_replied": s=="success", "airtable_logged": s=="success"},
        "2": lambda s: {"vendor": "Acme Corp", "amount": f"${random.randint(1000,50000):,}", "invoice_logged": s=="success"},
        "3": lambda s: {"event_title": "Product Sync", "calendar_created": s=="success", "attendees_notified": s=="success"},
        "4": lambda s: {"company": "TechCorp Ltd", "score": random.choice(["Hot Lead","Warm Lead"]), "crm_updated": s=="success"},
        "5": lambda s: {"total_workflows": random.randint(40,80), "success_rate": f"{random.randint(85,99)}%", "report_emailed": s=="success"},
        "6": lambda s: {"ticket_category": random.choice(["Technical Bug","Billing","General"]), "auto_replied": s=="success", "airtable_logged": s=="success"},
        "7": lambda s: {"sap_orders_found": random.randint(3,8), "p1_count": random.randint(1,3), "p2_count": random.randint(1,4), "alert_emailed": s=="success", "alert_recipient": "pinkpearl918@gmail.com"},
    }
    error_msgs = [
        "Connection timeout to external service",
        "AI API rate limit exceeded — retrying",
        "Gmail OAuth token expired",
        "SAP API UCON 403 — falling back to mock data",
        "Airtable base not found",
    ]
    executions = []
    exec_id = 1000
    for i in range(35):
        wf = wf_meta[i % len(wf_meta)]
        status = random.choices(statuses, weights=[40,30,20,10,8,5])[0]
        started = now - timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))
        duration = round(random.uniform(1.2, 18.5), 1) if status != "running" else None
        finished = (started + timedelta(seconds=duration)) if duration else None
        executions.append({
            "id": str(exec_id + i),
            "workflowId": wf["id"],
            "workflowName": wf["name"],
            "workflowEmoji": wf["emoji"],
            "status": status,
            "startedAt": started.isoformat(),
            "stoppedAt": finished.isoformat() if finished else None,
            "duration_seconds": duration,
            "mode": random.choice(["trigger", "webhook", "manual"]),
            "output": output_templates[wf["id"]](status) if status == "success" else None,
            "error": random.choice(error_msgs) if status == "error" else None,
        })
    # Sort newest first
    executions.sort(key=lambda x: x["startedAt"], reverse=True)
    return executions


class N8NService:
    """Triggers and monitors n8n workflows via REST API. Falls back to demo mode if n8n is unavailable."""

    def __init__(self) -> None:
        self._base_url = settings.N8N_BASE_URL.rstrip("/")
        self._api_key = settings.N8N_API_KEY
        if self._api_key:
            logger.info("n8n integration enabled (url=%s)", self._base_url)
        else:
            logger.info("N8N_API_KEY not set — n8n running in demo mode")

    @property
    def enabled(self) -> bool:
        return bool(self._api_key)

    def _headers(self) -> dict:
        return {"X-N8N-API-KEY": self._api_key, "Content-Type": "application/json"}

    async def list_workflows(self) -> list[dict]:
        if not self.enabled:
            return _DEMO_WORKFLOWS
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{self._base_url}/api/v1/workflows", headers=self._headers())
                resp.raise_for_status()
                return resp.json().get("data", [])
        except Exception as exc:
            logger.error("n8n list_workflows error: %s", exc)
            return _DEMO_WORKFLOWS

    async def trigger_webhook(self, webhook_path: str, payload: dict) -> dict:
        """POST to an n8n webhook URL."""
        url = f"{self._base_url}/webhook/{webhook_path}"
        if not self.enabled:
            return {"status": "demo", "message": f"Would POST to {url}", "payload": payload}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                return {"status": "triggered", "response": resp.json()}
        except Exception as exc:
            logger.error("n8n trigger_webhook error: %s", exc)
            return {"status": "error", "message": str(exc)}

    async def get_execution(self, execution_id: str) -> dict:
        if not self.enabled:
            return {"id": execution_id, "status": "demo", "data": {}}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self._base_url}/api/v1/executions/{execution_id}",
                    headers=self._headers(),
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as exc:
            logger.error("n8n get_execution error: %s", exc)
            return {"status": "error", "message": str(exc)}

    async def activate_workflow(self, workflow_id: str, active: bool = True) -> dict:
        if not self.enabled:
            return {"status": "demo", "workflowId": workflow_id, "active": active}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.patch(
                    f"{self._base_url}/api/v1/workflows/{workflow_id}",
                    headers=self._headers(),
                    json={"active": active},
                )
                resp.raise_for_status()
                return resp.json()
        except Exception as exc:
            logger.error("n8n activate_workflow error: %s", exc)
            return {"status": "error", "message": str(exc)}

    async def list_executions(
        self,
        limit: int = 50,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[dict]:
        """Return n8n execution history. Falls back to realistic demo data."""
        if not self.enabled:
            execs = _make_demo_executions()
            if workflow_id:
                execs = [e for e in execs if e["workflowId"] == workflow_id]
            if status:
                execs = [e for e in execs if e["status"] == status]
            return execs[:limit]
        try:
            params: dict = {"limit": limit, "includeData": True}
            if workflow_id:
                params["workflowId"] = workflow_id
            if status:
                params["status"] = status
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"{self._base_url}/api/v1/executions",
                    headers=self._headers(),
                    params=params,
                )
                resp.raise_for_status()
                data = resp.json().get("data", [])
                # Normalise n8n API response to our schema
                normalised = []
                for ex in data:
                    wf = ex.get("workflowData", {})
                    normalised.append({
                        "id": str(ex.get("id", "")),
                        "workflowId": str(ex.get("workflowId", "")),
                        "workflowName": wf.get("name", "Unknown Workflow"),
                        "workflowEmoji": "⚡",
                        "status": ex.get("finished", False) and "success" or ex.get("stoppedAt") and "error" or "running",
                        "startedAt": ex.get("startedAt"),
                        "stoppedAt": ex.get("stoppedAt"),
                        "duration_seconds": ex.get("data", {}).get("executionTime"),
                        "mode": ex.get("mode", "trigger"),
                        "output": ex.get("data", {}).get("resultData", {}).get("lastNodeExecuted"),
                        "error": ex.get("data", {}).get("resultData", {}).get("error", {}).get("message") if not ex.get("finished") else None,
                    })
                return normalised
        except Exception as exc:
            logger.error("n8n list_executions error: %s", exc)
            return _make_demo_executions()[:limit]

    async def execution_stats(self) -> dict:
        """Aggregate statistics across all n8n executions."""
        execs = await self.list_executions(limit=200)
        total = len(execs)
        by_status = {"success": 0, "error": 0, "running": 0}
        by_workflow: dict = {}
        durations = []
        for ex in execs:
            s = ex.get("status", "unknown")
            if s in by_status:
                by_status[s] += 1
            wname = ex.get("workflowName", "Unknown")
            by_workflow[wname] = by_workflow.get(wname, {"success": 0, "error": 0, "running": 0, "total": 0})
            by_workflow[wname]["total"] += 1
            if s in by_workflow[wname]:
                by_workflow[wname][s] += 1
            if ex.get("duration_seconds"):
                durations.append(ex["duration_seconds"])
        success_rate = round((by_status["success"] / total * 100) if total else 0, 1)
        avg_duration = round(sum(durations) / len(durations), 1) if durations else 0
        return {
            "total": total,
            "by_status": by_status,
            "success_rate_pct": success_rate,
            "avg_duration_seconds": avg_duration,
            "by_workflow": [
                {"name": k, **v, "success_rate_pct": round(v["success"] / v["total"] * 100, 1) if v["total"] else 0}
                for k, v in sorted(by_workflow.items(), key=lambda x: x[1]["total"], reverse=True)
            ],
            "demo_mode": not self.enabled,
        }


# Singleton
n8n_service = N8NService()

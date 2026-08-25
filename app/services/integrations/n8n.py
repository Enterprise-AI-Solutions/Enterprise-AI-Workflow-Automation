"""n8n workflow automation integration — with auto-discovery from n8n/workflows/ folder."""

from __future__ import annotations

import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

import httpx

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Workflow folder auto-discovery ────────────────────────────────────────────
# Resolve relative to repo root (two levels up from this file: app/services/integrations/)
_REPO_ROOT = Path(__file__).resolve().parents[3]
_WORKFLOWS_DIR = _REPO_ROOT / "n8n" / "workflows"

# Emoji heuristics — match against workflow name / tags
_EMOJI_MAP: list[tuple[list[str], str]] = [
    (["email", "triage", "gmail", "mail"],          "📧"),
    (["invoice", "finance", "billing", "payment"],  "🧾"),
    (["meeting", "calendar", "schedule", "event"],  "📅"),
    (["lead", "crm", "qualification", "sales"],     "🎯"),
    (["kpi", "report", "daily", "analytics"],       "📊"),
    (["support", "ticket", "helpdesk", "zendesk"],  "🎫"),
    (["sap", "maintenance", "iw38", "plant"],       "🏭"),
    (["slack", "notification", "alert"],            "🔔"),
    (["database", "postgres", "mysql", "sqlite"],   "🗄️"),
    (["api", "http", "webhook", "rest"],            "🌐"),
    (["ai", "claude", "gpt", "llm"],               "🤖"),
    (["airtable", "sheet", "spreadsheet"],          "🗃️"),
]

def _guess_emoji(name: str, tags: list[str]) -> str:
    haystack = (name + " " + " ".join(tags)).lower()
    for keywords, emoji in _EMOJI_MAP:
        if any(k in haystack for k in keywords):
            return emoji
    return "⚡"

def _build_output_template(name: str, tags: list[str]):
    """Return a lambda that generates realistic demo output for a workflow."""
    lower = (name + " " + " ".join(tags)).lower()
    if any(k in lower for k in ["email", "triage", "gmail"]):
        return lambda s: {"category": random.choice(["Sales", "Support", "Finance"]), "replied": s == "success", "airtable_logged": s == "success"}
    if any(k in lower for k in ["invoice", "finance"]):
        return lambda s: {"vendor": "Acme Corp", "amount": f"${random.randint(500, 50000):,}", "logged": s == "success"}
    if any(k in lower for k in ["meeting", "calendar", "schedule"]):
        return lambda s: {"event": "Product Sync", "calendar_created": s == "success", "guests_notified": s == "success"}
    if any(k in lower for k in ["lead", "crm", "qualification"]):
        return lambda s: {"company": "TechCorp Ltd", "score": random.choice(["Hot", "Warm", "Cold"]), "crm_updated": s == "success"}
    if any(k in lower for k in ["kpi", "report", "daily"]):
        return lambda s: {"workflows_run": random.randint(40, 120), "success_rate": f"{random.randint(85, 99)}%", "emailed": s == "success"}
    if any(k in lower for k in ["support", "ticket"]):
        return lambda s: {"category": random.choice(["Bug", "Billing", "General"]), "replied": s == "success", "logged": s == "success"}
    if any(k in lower for k in ["sap", "maintenance", "iw38"]):
        return lambda s: {"orders_found": random.randint(2, 10), "p1": random.randint(0, 3), "p2": random.randint(1, 5), "alert_sent": s == "success", "email": "pinkpearl918@gmail.com"}
    # Generic fallback
    return lambda s: {"status": s, "items_processed": random.randint(1, 50), "completed": s == "success"}


def scan_workflow_files() -> list[dict]:
    """
    Scan n8n/workflows/*.json and return structured metadata for every workflow.
    Works even if n8n Cloud API is unavailable.
    Results are sorted alphabetically by workflow name.
    """
    if not _WORKFLOWS_DIR.exists():
        logger.warning("n8n workflows directory not found: %s", _WORKFLOWS_DIR)
        return []

    discovered: list[dict] = []
    for idx, path in enumerate(sorted(_WORKFLOWS_DIR.glob("*.json")), start=1):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            name = raw.get("name", path.stem.replace("_", " ").title())
            tags = raw.get("tags", [])
            # tags can be list[str] or list[dict] (n8n format)
            tag_names: list[str] = [
                t if isinstance(t, str) else t.get("name", "") for t in tags
            ]
            # Detect trigger type from nodes
            nodes = raw.get("nodes", [])
            trigger_node = next(
                (n for n in nodes if "Trigger" in n.get("type", "") or "scheduleTrigger" in n.get("type", "")),
                None,
            )
            trigger_type = "manual"
            if trigger_node:
                t = trigger_node["type"].lower()
                if "schedule" in t:   trigger_type = "schedule"
                elif "webhook" in t:  trigger_type = "webhook"
                elif "email" in t:    trigger_type = "email"
                elif "trigger" in t:  trigger_type = "trigger"

            discovered.append({
                "id": str(idx),
                "name": name,
                "file": path.name,
                "tags": tag_names,
                "emoji": _guess_emoji(name, tag_names),
                "trigger_type": trigger_type,
                "node_count": len(nodes),
                "active": raw.get("active", False),
                "description": raw.get("meta", {}).get("description", ""),
                "output_template": _build_output_template(name, tag_names),
            })
        except Exception as exc:
            logger.warning("Failed to parse workflow file %s: %s", path.name, exc)

    logger.info("Auto-discovered %d workflow(s) from %s", len(discovered), _WORKFLOWS_DIR)
    return discovered


# ── Demo execution generator (uses auto-discovered workflows) ─────────────────

_ERROR_MSGS = [
    "Connection timeout to external API",
    "Claude AI rate limit exceeded — will retry",
    "Gmail OAuth token expired — re-auth required",
    "SAP UCON 403 — falling back to mock data",
    "Airtable base not found",
    "Webhook endpoint unreachable",
    "Node execution failed: TypeError in Code node",
]

def _make_demo_executions(workflows: list[dict]) -> list[dict]:
    """
    Generate realistic demo execution history for every discovered workflow.
    Each workflow gets ~5 executions spread over the last 72 hours.
    """
    if not workflows:
        return []

    now = datetime.now(timezone.utc)
    executions: list[dict] = []
    exec_id = 1000

    for wf in workflows:
        # 5 executions per workflow, spread over last 72h
        for _ in range(5):
            status = random.choices(
                ["success", "success", "success", "error", "running"],
                weights=[50, 30, 20, 15, 5],
            )[0]
            started = now - timedelta(
                hours=random.randint(0, 72),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )
            duration = round(random.uniform(1.2, 20.0), 1) if status != "running" else None
            finished = (started + timedelta(seconds=duration)) if duration else None

            executions.append({
                "id": str(exec_id),
                "workflowId": wf["id"],
                "workflowName": wf["name"],
                "workflowFile": wf["file"],
                "workflowEmoji": wf["emoji"],
                "tags": wf["tags"],
                "status": status,
                "startedAt": started.isoformat(),
                "stoppedAt": finished.isoformat() if finished else None,
                "duration_seconds": duration,
                "mode": random.choice(["trigger", "webhook", "manual", "schedule"]),
                "output": wf["output_template"](status) if status == "success" else None,
                "error": random.choice(_ERROR_MSGS) if status == "error" else None,
            })
            exec_id += 1

    # Sort newest first
    executions.sort(key=lambda x: x["startedAt"], reverse=True)
    return executions


# ── N8N Service ───────────────────────────────────────────────────────────────

class N8NService:
    """
    Manages n8n workflow automation.

    - If N8N_API_KEY is set: calls real n8n Cloud REST API.
    - Otherwise: runs in demo mode using auto-discovered workflows from
      n8n/workflows/*.json to generate realistic execution history.

    Adding a new .json file to n8n/workflows/ is sufficient for it to
    appear automatically in the dashboard — no code changes needed.
    """

    def __init__(self) -> None:
        self._base_url = settings.N8N_BASE_URL.rstrip("/")
        self._api_key = settings.N8N_API_KEY
        if self._api_key:
            logger.info("n8n integration enabled (url=%s)", self._base_url)
        else:
            logger.info("N8N_API_KEY not set — n8n running in demo mode (auto-discovery active)")

    @property
    def enabled(self) -> bool:
        return bool(self._api_key)

    def _headers(self) -> dict:
        return {"X-N8N-API-KEY": self._api_key, "Content-Type": "application/json"}

    # ── Workflow file discovery ───────────────────────────────────────────────

    def get_local_workflows(self) -> list[dict]:
        """Return metadata for every workflow JSON in n8n/workflows/."""
        wfs = scan_workflow_files()
        # Strip internal output_template (not JSON-serialisable)
        return [{k: v for k, v in wf.items() if k != "output_template"} for wf in wfs]

    # ── Workflow list ─────────────────────────────────────────────────────────

    async def list_workflows(self) -> list[dict]:
        """List workflows — real n8n API first, falls back to local files."""
        if not self.enabled:
            return self.get_local_workflows()
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self._base_url}/api/v1/workflows", headers=self._headers()
                )
                resp.raise_for_status()
                return resp.json().get("data", [])
        except Exception as exc:
            logger.error("n8n list_workflows error: %s — falling back to local files", exc)
            return self.get_local_workflows()

    # ── Webhook trigger ───────────────────────────────────────────────────────

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

    # ── Single execution lookup ───────────────────────────────────────────────

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

    # ── Activate / deactivate ─────────────────────────────────────────────────

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

    # ── Execution history ─────────────────────────────────────────────────────

    async def list_executions(
        self,
        limit: int = 50,
        workflow_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[dict]:
        """
        Return n8n execution history.
        Demo mode: generates realistic history for every workflow in n8n/workflows/.
        Adding a new workflow JSON file = it automatically gets executions too.
        """
        if not self.enabled:
            workflows = scan_workflow_files()
            execs = _make_demo_executions(workflows)
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
                normalised = []
                for ex in data:
                    wf_data = ex.get("workflowData", {})
                    wf_name = wf_data.get("name", "Unknown Workflow")
                    wf_tags = [t.get("name", "") if isinstance(t, dict) else t for t in wf_data.get("tags", [])]
                    normalised.append({
                        "id": str(ex.get("id", "")),
                        "workflowId": str(ex.get("workflowId", "")),
                        "workflowName": wf_name,
                        "workflowFile": None,
                        "workflowEmoji": _guess_emoji(wf_name, wf_tags),
                        "tags": wf_tags,
                        "status": (
                            "success" if ex.get("finished") and not ex.get("data", {}).get("resultData", {}).get("error")
                            else "error" if ex.get("stoppedAt") and not ex.get("finished")
                            else "running"
                        ),
                        "startedAt": ex.get("startedAt"),
                        "stoppedAt": ex.get("stoppedAt"),
                        "duration_seconds": ex.get("data", {}).get("executionTime"),
                        "mode": ex.get("mode", "trigger"),
                        "output": ex.get("data", {}).get("resultData", {}).get("lastNodeExecuted"),
                        "error": ex.get("data", {}).get("resultData", {}).get("error", {}).get("message") if not ex.get("finished") else None,
                    })
                return normalised
        except Exception as exc:
            logger.error("n8n list_executions error: %s — using demo data", exc)
            workflows = scan_workflow_files()
            return _make_demo_executions(workflows)[:limit]

    # ── Aggregate stats ───────────────────────────────────────────────────────

    async def execution_stats(self) -> dict:
        """Aggregate KPI statistics across all n8n executions."""
        execs = await self.list_executions(limit=500)
        total = len(execs)
        by_status: dict = {"success": 0, "error": 0, "running": 0}
        by_workflow: dict = {}
        durations: list[float] = []

        for ex in execs:
            s = ex.get("status", "unknown")
            if s in by_status:
                by_status[s] += 1
            wname = ex.get("workflowName", "Unknown")
            wemoji = ex.get("workflowEmoji", "⚡")
            wfile  = ex.get("workflowFile")
            key = wname
            if key not in by_workflow:
                by_workflow[key] = {"name": wname, "emoji": wemoji, "file": wfile,
                                    "success": 0, "error": 0, "running": 0, "total": 0}
            by_workflow[key]["total"] += 1
            if s in by_workflow[key]:
                by_workflow[key][s] += 1
            if ex.get("duration_seconds"):
                durations.append(ex["duration_seconds"])

        success_rate = round(by_status["success"] / total * 100, 1) if total else 0
        avg_dur = round(sum(durations) / len(durations), 1) if durations else 0

        breakdown = sorted(by_workflow.values(), key=lambda x: x["total"], reverse=True)
        for b in breakdown:
            b["success_rate_pct"] = round(b["success"] / b["total"] * 100, 1) if b["total"] else 0

        return {
            "total": total,
            "by_status": by_status,
            "success_rate_pct": success_rate,
            "avg_duration_seconds": avg_dur,
            "by_workflow": breakdown,
            "workflow_count": len(by_workflow),
            "demo_mode": not self.enabled,
        }


# Singleton
n8n_service = N8NService()

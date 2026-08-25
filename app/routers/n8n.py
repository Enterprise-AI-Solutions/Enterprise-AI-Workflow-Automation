"""n8n integration router."""

from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.services.integrations import n8n_service
from app.services.integrations.n8n import scan_workflow_files

router = APIRouter(prefix="/n8n", tags=["n8n"])


class TriggerWebhookRequest(BaseModel):
    webhook_path: str
    payload: dict = {}


class ActivateWorkflowRequest(BaseModel):
    active: bool = True


@router.get("/workflows", summary="List n8n workflows (real API or local files)")
async def list_n8n_workflows():
    workflows = await n8n_service.list_workflows()
    return {"workflows": workflows, "count": len(workflows), "demo_mode": not n8n_service.enabled}


@router.get("/workflow-files", summary="Scan n8n/workflows/ folder and return all discovered workflows")
async def list_workflow_files():
    """
    Auto-scans the n8n/workflows/ directory and returns metadata for every
    .json file found. This is the source of truth for the dashboard filter
    dropdown — no manual registration needed when adding new workflows.
    """
    workflows = scan_workflow_files()
    # Strip non-serialisable output_template
    serialisable = [{k: v for k, v in wf.items() if k != "output_template"} for wf in workflows]
    return {
        "workflows": serialisable,
        "count": len(serialisable),
        "directory": "n8n/workflows/",
    }


@router.post("/trigger", summary="Trigger an n8n webhook")
async def trigger_webhook(request: TriggerWebhookRequest):
    result = await n8n_service.trigger_webhook(request.webhook_path, request.payload)
    return {**result, "demo_mode": not n8n_service.enabled}


@router.get("/executions", summary="List n8n execution history")
async def list_n8n_executions(
    limit: int = Query(50, ge=1, le=200),
    workflow_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="Filter by status: success | error | running"),
):
    executions = await n8n_service.list_executions(limit=limit, workflow_id=workflow_id, status=status)
    return {
        "executions": executions,
        "count": len(executions),
        "demo_mode": not n8n_service.enabled,
    }


@router.get("/executions/stats", summary="n8n execution statistics across all workflows")
async def n8n_execution_stats():
    return await n8n_service.execution_stats()


@router.get("/executions/{execution_id}", summary="Get n8n execution status")
async def get_n8n_execution(execution_id: str):
    result = await n8n_service.get_execution(execution_id)
    return {**result, "demo_mode": not n8n_service.enabled}


@router.get("/workflows/{workflow_id}/executions", summary="Executions for a specific workflow")
async def get_workflow_executions(
    workflow_id: str,
    limit: int = Query(20, ge=1, le=100),
):
    executions = await n8n_service.list_executions(limit=limit, workflow_id=workflow_id)
    return {
        "workflow_id": workflow_id,
        "executions": executions,
        "count": len(executions),
        "demo_mode": not n8n_service.enabled,
    }


@router.patch("/workflows/{workflow_id}/activate", summary="Activate/deactivate n8n workflow")
async def activate_workflow(workflow_id: str, request: ActivateWorkflowRequest):
    result = await n8n_service.activate_workflow(workflow_id, active=request.active)
    return {**result, "demo_mode": not n8n_service.enabled}


@router.get("/status", summary="n8n integration status")
async def n8n_status():
    return {
        "enabled": n8n_service.enabled,
        "base_url": n8n_service._base_url,
        "demo_mode": not n8n_service.enabled,
    }

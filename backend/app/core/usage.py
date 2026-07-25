from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.models import SubscriptionPlan, UsageEvent, UserAccount

EVENT_CONTENT_GENERATED = "content_generated"
EVENT_AI_CREDITS_USED = "ai_credits_used"
EVENT_PROPERTY_CREATED = "property_created"
EVENT_CALENDAR_CREATED = "calendar_created"
EVENT_MARKETDNA_SOURCE_CREATED = "marketdna_source_created"
EVENT_PIPELINE_CREATED = "pipeline_created"

AI_CREDITS_BY_ACTION = {
    "generate": 6,
    "variation": 2,
    "manual_content": 1,
}

def get_plan(db: Session, workspace_id: int) -> SubscriptionPlan | None:
    return db.query(SubscriptionPlan).filter(SubscriptionPlan.workspace_id == workspace_id).first()

def get_usage_total(db: Session, workspace_id: int, event_type: str) -> int:
    events = db.query(UsageEvent).filter(
        UsageEvent.workspace_id == workspace_id,
        UsageEvent.event_type == event_type,
    ).all()
    return sum(int(e.amount or 0) for e in events)

def usage_snapshot(db: Session, workspace_id: int) -> dict:
    plan = get_plan(db, workspace_id)
    content_used = get_usage_total(db, workspace_id, EVENT_CONTENT_GENERATED)
    ai_used = get_usage_total(db, workspace_id, EVENT_AI_CREDITS_USED)
    property_created = get_usage_total(db, workspace_id, EVENT_PROPERTY_CREATED)
    calendar_created = get_usage_total(db, workspace_id, EVENT_CALENDAR_CREATED)
    marketdna_created = get_usage_total(db, workspace_id, EVENT_MARKETDNA_SOURCE_CREATED)
    pipeline_created = get_usage_total(db, workspace_id, EVENT_PIPELINE_CREATED)

    monthly_content_limit = int(getattr(plan, "monthly_content_limit", 0) or 0)
    ai_credit_limit = int(getattr(plan, "ai_credit_limit", 0) or 0)
    seats_limit = int(getattr(plan, "seats_limit", 0) or 0)
    status = getattr(plan, "status", "unknown")

    return {
        "plan": getattr(plan, "plan_name", "Sin plan"),
        "status": status,
        "monthly_content_limit": monthly_content_limit,
        "ai_credit_limit": ai_credit_limit,
        "seats_limit": seats_limit,
        "content_used": content_used,
        "ai_credits_used": ai_used,
        "property_created": property_created,
        "calendar_created": calendar_created,
        "marketdna_created": marketdna_created,
        "pipeline_created": pipeline_created,
        "content_remaining": max(monthly_content_limit - content_used, 0),
        "ai_credits_remaining": max(ai_credit_limit - ai_used, 0),
        "content_pct": round((content_used / monthly_content_limit) * 100, 1) if monthly_content_limit else 0,
        "ai_pct": round((ai_used / ai_credit_limit) * 100, 1) if ai_credit_limit else 0,
    }

def assert_can_consume(db: Session, workspace_id: int, content_units: int = 0, ai_credits: int = 0):
    snap = usage_snapshot(db, workspace_id)
    if snap["status"] not in ("trial", "active"):
        raise HTTPException(status_code=402, detail="El plan no está activo.")
    if content_units and snap["content_used"] + content_units > snap["monthly_content_limit"]:
        raise HTTPException(status_code=402, detail="Límite mensual de contenidos alcanzado.")
    if ai_credits and snap["ai_credits_used"] + ai_credits > snap["ai_credit_limit"]:
        raise HTTPException(status_code=402, detail="Límite mensual de créditos IA alcanzado.")

def record_usage(db: Session, user: UserAccount, event_type: str, amount: int = 1, meta: str | None = None):
    ev = UsageEvent(
        workspace_id=user.workspace_id,
        event_type=event_type,
        amount=amount,
        meta=meta,
    )
    db.add(ev)
    db.commit()
    return ev

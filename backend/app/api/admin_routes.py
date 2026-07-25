from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.usage import usage_snapshot
from app.core.auth_tokens import current_user_from_request, require_role
from app.core.models import (
    Workspace,
    UserAccount,
    SubscriptionPlan,
    UsageEvent,
    Property,
    ContentItem,
    PipelineItem,
    CalendarItem,
    MarketDNASource,
)

router = APIRouter(prefix="/admin", tags=["admin-master"])

def require_super_admin(request: Request, db: Session) -> UserAccount:
    user = current_user_from_request(request, db)
    require_role(user, {"super_admin"})
    return user

@router.get("/overview")
def overview(request: Request, db: Session = Depends(get_db)):
    require_super_admin(request, db)
    workspaces = db.query(Workspace).all()
    users = db.query(UserAccount).all()
    plans = db.query(SubscriptionPlan).all()
    usage_events = db.query(UsageEvent).all()

    content_usage = sum(e.amount for e in usage_events if e.event_type == "content_generated")
    ai_usage = sum(e.amount for e in usage_events if e.event_type == "ai_credits_used")

    active = [w for w in workspaces if w.status == "active"]
    return {
        "kpis": {
            "clients_total": len(workspaces),
            "clients_active": len(active),
            "users_total": len(users),
            "subscriptions_total": len(plans),
            "content_generated": content_usage,
            "ai_credits_used": ai_usage,
            "mrr_mock": "$840K",
        },
        "clients": [
            {
                "id": w.id,
                "name": w.name,
                "slug": w.slug,
                "status": w.status,
                "plan": w.plan,
                "users": len([u for u in users if u.workspace_id == w.id]),
                "properties": db.query(Property).filter(Property.workspace_id == w.id).count(),
                "contents": db.query(ContentItem).filter(ContentItem.workspace_id == w.id).count(),
                "pipeline": db.query(PipelineItem).filter(PipelineItem.workspace_id == w.id).count(),
                "calendar": db.query(CalendarItem).filter(CalendarItem.workspace_id == w.id).count(),
                "sources": db.query(MarketDNASource).filter(MarketDNASource.workspace_id == w.id).count(),
                "usage": usage_snapshot(db, w.id),
            }
            for w in workspaces
        ],
        "plans": [
            {
                "workspace_id": p.workspace_id,
                "plan_name": p.plan_name,
                "status": p.status,
                "monthly_content_limit": p.monthly_content_limit,
                "ai_credit_limit": p.ai_credit_limit,
                "seats_limit": p.seats_limit,
            }
            for p in plans
        ],
        "mode": "protected-admin-master",
    }

@router.get("/me")
def admin_me(request: Request, db: Session = Depends(get_db)):
    user = require_super_admin(request, db)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

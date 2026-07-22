from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.models import Workspace, UserAccount, SubscriptionPlan, UsageEvent, Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource
from app.core.security import slugify, hash_password

router = APIRouter(prefix="/workspace", tags=["workspace"])

def workspace_id(request: Request) -> int:
    raw = request.headers.get("x-workspace-id") or request.query_params.get("workspace_id") or "1"
    try:
        return int(raw)
    except ValueError:
        return 1

class MemberCreate(BaseModel):
    name: str
    email: str
    role: str = "member"

class WorkspaceCreate(BaseModel):
    name: str
    owner_name: str = "Agustín"
    owner_email: str = "owner@marketprop.local"
    plan: str = "Básico"

@router.get("/current")
def current_workspace(request: Request, db: Session = Depends(get_db)):
    wid = workspace_id(request)
    workspace = db.get(Workspace, wid)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace no encontrado")
    members = db.query(UserAccount).filter(UserAccount.workspace_id == wid).order_by(UserAccount.id.asc()).all()
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.workspace_id == wid).first()
    counts = {
        "properties": db.query(Property).filter(Property.workspace_id == wid).count(),
        "contents": db.query(ContentItem).filter(ContentItem.workspace_id == wid).count(),
        "pipeline": db.query(PipelineItem).filter(PipelineItem.workspace_id == wid).count(),
        "calendar": db.query(CalendarItem).filter(CalendarItem.workspace_id == wid).count(),
        "sources": db.query(MarketDNASource).filter(MarketDNASource.workspace_id == wid).count(),
    }
    used_content = db.query(UsageEvent).filter(UsageEvent.workspace_id == wid, UsageEvent.event_type == "content_generated").all()
    used_ai = db.query(UsageEvent).filter(UsageEvent.workspace_id == wid, UsageEvent.event_type == "ai_credits_used").all()
    usage = {
        "content_generated": sum(x.amount for x in used_content),
        "ai_credits_used": sum(x.amount for x in used_ai),
    }
    return {
        "workspace": {"id": workspace.id, "name": workspace.name, "slug": workspace.slug, "status": workspace.status, "plan": workspace.plan},
        "members": [{"id": m.id, "name": m.name, "email": m.email, "role": m.role, "status": m.status} for m in members],
        "plan": None if not plan else {"plan_name": plan.plan_name, "status": plan.status, "monthly_content_limit": plan.monthly_content_limit, "ai_credit_limit": plan.ai_credit_limit, "seats_limit": plan.seats_limit},
        "counts": counts,
        "usage": usage,
        "mode": "workspace-prepared-local"
    }

@router.post("/members")
def add_member(payload: MemberCreate, request: Request, db: Session = Depends(get_db)):
    wid = workspace_id(request)
    existing = db.query(UserAccount).filter(UserAccount.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ese email ya existe")
    member = UserAccount(workspace_id=wid, name=payload.name, email=payload.email, password_hash=hash_password("123456"), role=payload.role, status="invited")
    db.add(member); db.commit(); db.refresh(member)
    return {"id": member.id, "name": member.name, "email": member.email, "role": member.role, "status": member.status}

@router.post("/create-demo")
def create_demo_workspace(payload: WorkspaceCreate, db: Session = Depends(get_db)):
    base_slug = slugify(payload.name)
    slug = base_slug
    n = 2
    while db.query(Workspace).filter(Workspace.slug == slug).first():
        slug = f"{base_slug}-{n}"; n += 1
    workspace = Workspace(name=payload.name, slug=slug, plan=payload.plan, status="active")
    db.add(workspace); db.flush()
    user = UserAccount(workspace_id=workspace.id, name=payload.owner_name, email=payload.owner_email, password_hash=hash_password("123456"), role="owner", status="active")
    plan = SubscriptionPlan(workspace_id=workspace.id, plan_name=payload.plan, status="trial", monthly_content_limit=500, ai_credit_limit=100000, seats_limit=2)
    db.add_all([user, plan]); db.commit()
    return {"workspace_id": workspace.id, "name": workspace.name, "slug": workspace.slug, "owner_email": user.email}

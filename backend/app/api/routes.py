from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.marketmind.orchestrator import MarketMindOrchestrator
from app.marketmind.providers.registry import registry
from app.marketmind.analytics.mock_data import PIPELINE_DETAIL, PIPELINE_STATUSES, CALENDAR_DETAIL, MARKETDNA_SOURCES_DETAIL
from app.marketmind.analytics.mock_data import COMMAND_CENTER, PIPELINE, CALENDAR, SOURCES
from app.core.db import SessionLocal
from app.core.models import Workspace, UserAccount, SubscriptionPlan
from app.core.security import hash_password, verify_password, slugify
from app.core.auth_tokens import issue_token, current_user_from_request
from app.core.usage import assert_can_consume, record_usage, EVENT_CONTENT_GENERATED, EVENT_AI_CREDITS_USED, AI_CREDITS_BY_ACTION

router = APIRouter()
marketmind = MarketMindOrchestrator()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    organization_name: str
    email: str
    password: str

class GenerateRequest(BaseModel):
    url: str
    style: str = "auto"

class VariationRequest(BaseModel):
    platform: str
    property_data: dict
    style: str = "auto"

class PropertyRequest(BaseModel):
    title: str
    url: str | None = None
    location: str | None = None
    price: str | None = None

PROPERTIES = []

def user_payload(user: UserAccount, workspace: Workspace, plan: SubscriptionPlan | None = None):
    return {
        "id": user.id,
        "workspace_id": workspace.id,
        "name": user.name,
        "email": user.email,
        "organization_name": workspace.name,
        "workspace_slug": workspace.slug,
        "role": user.role,
        "plan": plan.plan_name if plan else workspace.plan
    }

@router.post("/auth/login")
def login(req: LoginRequest):
    if not req.email or not req.password:
        raise HTTPException(400, "Completá email y contraseña.")
    with SessionLocal() as db:
        found = db.query(UserAccount).filter(UserAccount.email == req.email).first()
        if not found:
            raise HTTPException(401, "Usuario no encontrado.")
        if found.status not in ("active", "invited"):
            raise HTTPException(403, "Usuario inactivo.")
        if not verify_password(req.password, found.password_hash):
            raise HTTPException(401, "Contraseña incorrecta.")
        workspace = db.get(Workspace, found.workspace_id)
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.workspace_id == workspace.id).first()
        return {"token": issue_token(found), "user": user_payload(found, workspace, plan)}


@router.post("/auth/register")
def register(req: RegisterRequest):
    if not req.name or not req.organization_name or not req.email or not req.password:
        raise HTTPException(400, "Completá todos los campos.")
    with SessionLocal() as db:
        if db.query(UserAccount).filter(UserAccount.email == req.email).first():
            raise HTTPException(400, "Ese email ya está registrado.")
        base_slug = slugify(req.organization_name)
        slug = base_slug
        n = 2
        while db.query(Workspace).filter(Workspace.slug == slug).first():
            slug = f"{base_slug}-{n}"; n += 1
        workspace = Workspace(name=req.organization_name, slug=slug, plan="Básico", status="active")
        db.add(workspace); db.flush()
        usr = UserAccount(workspace_id=workspace.id, name=req.name, email=req.email, password_hash=hash_password(req.password), role="owner", status="active")
        plan = SubscriptionPlan(workspace_id=workspace.id, plan_name="Básico", status="trial", monthly_content_limit=500, ai_credit_limit=100000, seats_limit=2)
        db.add_all([usr, plan]); db.commit(); db.refresh(usr); db.refresh(workspace)
        return {"token": issue_token(usr), "user": user_payload(usr, workspace, plan)}

@router.get("/auth/me")
def me(request: Request):
    with SessionLocal() as db:
        user = current_user_from_request(request, db)
        workspace = db.get(Workspace, user.workspace_id)
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.workspace_id == workspace.id).first()
        return {"user": user_payload(user, workspace, plan)}


@router.post("/generate")
async def generate(req: GenerateRequest, request: Request):
    if not req.url.startswith(("http://", "https://")):
        raise HTTPException(400, "Pegá un link válido que empiece con http:// o https://")
    with SessionLocal() as db:
        user = current_user_from_request(request, db)
        ai_credits = AI_CREDITS_BY_ACTION["generate"]
        assert_can_consume(db, user.workspace_id, content_units=1, ai_credits=ai_credits)
        result = marketmind.generate(req.url, req.style)
        record_usage(db, user, EVENT_CONTENT_GENERATED, 1, "generate")
        record_usage(db, user, EVENT_AI_CREDITS_USED, ai_credits, "generate")
        return result

@router.post("/variation")
async def variation(req: VariationRequest, request: Request):
    try:
        with SessionLocal() as db:
            user = current_user_from_request(request, db)
            ai_credits = AI_CREDITS_BY_ACTION["variation"]
            assert_can_consume(db, user.workspace_id, content_units=0, ai_credits=ai_credits)
            result = marketmind.variation(req.platform, req.property_data, req.style)
            record_usage(db, user, EVENT_AI_CREDITS_USED, ai_credits, "variation")
            return result
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/marketmind/health")
def health():
    return {"marketmind": "active", "version": "0.3.13", "mode": "usage-metering-plan-limits"}

@router.get("/marketmind/providers")
def providers():
    return {"demo_mode": registry.demo_mode(), "providers": registry.status()}

@router.get("/analytics/command-center")
def command_center():
    return COMMAND_CENTER

@router.get("/analytics/pipeline")
def pipeline():
    return {"items": PIPELINE}

@router.get("/analytics/calendar")
def calendar():
    return {"items": CALENDAR}

@router.get("/marketdna/sources")
def sources():
    return {"items": SOURCES}

@router.get("/properties")
def list_properties():
    return {"items": PROPERTIES}

@router.post("/properties")
def create_property(req: PropertyRequest):
    item = req.model_dump()
    item["id"] = len(PROPERTIES) + 1
    PROPERTIES.append(item)
    return {"item": item}


@router.get("/analytics/pipeline-detail")
def pipeline_detail():
    return {"statuses": PIPELINE_STATUSES, "items": PIPELINE_DETAIL}

@router.get("/analytics/calendar-detail")
def calendar_detail():
    return {"items": CALENDAR_DETAIL}

@router.get("/analytics/marketdna-sources-detail")
def marketdna_sources_detail():
    return {"items": MARKETDNA_SOURCES_DETAIL}

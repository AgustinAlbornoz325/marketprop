from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.marketmind.orchestrator import MarketMindOrchestrator
from app.marketmind.providers.registry import registry
from app.marketmind.analytics.mock_data import COMMAND_CENTER, PIPELINE, CALENDAR, SOURCES

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

def user(name="Agustín", org="Forja Propiedades"):
    return {"name": name, "organization_name": org, "plan": "Plan Básico"}

@router.post("/auth/login")
def login(req: LoginRequest):
    if not req.email or not req.password:
        raise HTTPException(400, "Completá email y contraseña.")
    return {"token": "demo-token", "user": user()}

@router.post("/auth/register")
def register(req: RegisterRequest):
    if not req.name or not req.organization_name or not req.email or not req.password:
        raise HTTPException(400, "Completá todos los campos.")
    return {"token": "demo-token", "user": user(req.name, req.organization_name)}

@router.post("/generate")
async def generate(req: GenerateRequest):
    if not req.url.startswith(("http://", "https://")):
        raise HTTPException(400, "Pegá un link válido que empiece con http:// o https://")
    return marketmind.generate(req.url, req.style)

@router.post("/variation")
async def variation(req: VariationRequest):
    try:
        return marketmind.variation(req.platform, req.property_data, req.style)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/marketmind/health")
def health():
    return {"marketmind": "active", "version": "0.3.7", "mode": "consolidated-command-center"}

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

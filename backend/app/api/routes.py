from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.marketmind.orchestrator import MarketMindOrchestrator
from app.marketmind.model_router import ModelRouter
router = APIRouter(); marketmind = MarketMindOrchestrator()
router_engine = ModelRouter()
class LoginRequest(BaseModel): email: str; password: str
class RegisterRequest(BaseModel): name: str; organization_name: str; email: str; password: str
class GenerateRequest(BaseModel): url: str; style: str = "auto"
class VariationRequest(BaseModel): platform: str; property_data: dict; style: str = "auto"
def user(name="Agustín", org="Forja Propiedades"): return {"name":name, "organization_name":org, "plan":"Plan Básico"}
@router.post("/auth/login")
def login(req: LoginRequest):
    if not req.email or not req.password: raise HTTPException(400, "Completá email y contraseña.")
    return {"token":"demo-token", "user":user()}
@router.post("/auth/register")
def register(req: RegisterRequest):
    if not req.name or not req.organization_name or not req.email or not req.password: raise HTTPException(400, "Completá todos los campos.")
    return {"token":"demo-token", "user":user(req.name, req.organization_name)}
@router.post("/generate")
def generate(req: GenerateRequest):
    if not req.url.startswith(("http://", "https://")): raise HTTPException(400, "Pegá un link válido que empiece con http:// o https://")
    return marketmind.generate(req.url, req.style)
@router.post("/variation")
def variation(req: VariationRequest):
    try: return marketmind.variation(req.platform, req.property_data, req.style)
    except ValueError as e: raise HTTPException(400, str(e))
@router.get("/marketmind/health")
def health(): return {"marketmind":"active", "version":"0.3.3", "mode":"orchestrator"}


@router.get("/marketmind/providers")
def providers():
    return {"providers": router_engine.provider_status(), "note": "Sin API keys usa mock. Con API keys MarketMind puede enrutar tareas."}

from fastapi import APIRouter,Header,HTTPException
from pydantic import BaseModel
from app.services.auth import register_user,login_user,by_token
from app.services.extractor import extract_property
from app.services.marketai import generate_all_content,generate_variation

router=APIRouter()

class RegisterRequest(BaseModel):
    name:str; email:str; password:str; organization_name:str
class LoginRequest(BaseModel):
    email:str; password:str
class GenerateRequest(BaseModel):
    url:str
class VariationRequest(BaseModel):
    platform:str; property_data:dict

@router.get("/health")
def health(): return {"status":"ok","version":"0.2.0 Alpha"}

@router.post("/auth/register")
def register(req:RegisterRequest):
    try:
        token,user=register_user(req.name,req.email,req.password,req.organization_name)
        return {"token":token,"user":user}
    except ValueError as e: raise HTTPException(400,detail=str(e))

@router.post("/auth/login")
def login(req:LoginRequest):
    try:
        token,user=login_user(req.email,req.password)
        return {"token":token,"user":user}
    except ValueError as e: raise HTTPException(401,detail=str(e))

@router.get("/auth/me")
def me(authorization:str=Header(default="")):
    user=by_token(authorization.replace("Bearer ","").strip())
    if not user: raise HTTPException(401,detail="Sesión inválida.")
    return {"user":user}

@router.post("/generate")
def generate(req:GenerateRequest, authorization:str=Header(default="")):
    prop=extract_property(req.url)
    return {"property":prop,"content":generate_all_content(prop)}

@router.post("/variation")
def variation(req:VariationRequest):
    return {"platform":req.platform,"variation":generate_variation(req.platform,req.property_data)}

@router.get("/master/overview")
def master(): return {"clients_active":1,"mrr":0,"organizations":1,"status":"mock"}

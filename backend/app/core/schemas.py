from pydantic import BaseModel, EmailStr
from typing import Optional

class WorkspaceCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    plan: Optional[str] = "Básico"

class WorkspaceOut(BaseModel):
    id: int
    name: str
    slug: str
    status: str
    plan: str
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = "member"

class UserOut(BaseModel):
    id: int
    workspace_id: int
    name: str
    email: str
    role: str
    status: str
    class Config:
        from_attributes = True

class PlanOut(BaseModel):
    id: int
    workspace_id: int
    plan_name: str
    status: str
    monthly_content_limit: int
    ai_credit_limit: int
    seats_limit: int
    class Config:
        from_attributes = True

class PropertyCreate(BaseModel):
    title: str
    url: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    price: Optional[str] = None
    status: Optional[str] = "Activa"
    notes: Optional[str] = None
    workspace_id: Optional[int] = 1

class PropertyOut(PropertyCreate):
    id: int
    class Config:
        from_attributes = True

class ContentCreate(BaseModel):
    property_id: Optional[int] = None
    platform: str
    format: Optional[str] = None
    style: Optional[str] = None
    title: Optional[str] = None
    body: str
    score: Optional[int] = 0
    status: Optional[str] = "Contenido generado"
    workspace_id: Optional[int] = 1

class ContentOut(ContentCreate):
    id: int
    class Config:
        from_attributes = True

class PipelineCreate(BaseModel):
    property_title: str
    platform: str
    format: Optional[str] = None
    objective: Optional[str] = None
    status: Optional[str] = "Propiedad cargada"
    owner: Optional[str] = "Agus"
    score: Optional[int] = 80
    next_action: Optional[str] = None
    blocker: Optional[str] = None
    source: Optional[str] = None
    workspace_id: Optional[int] = 1

class PipelineOut(PipelineCreate):
    id: int
    class Config:
        from_attributes = True

class CalendarCreate(BaseModel):
    day: str
    time: str
    title: str
    platform: str
    property_title: Optional[str] = None
    goal: Optional[str] = None
    score: Optional[int] = 80
    workspace_id: Optional[int] = 1

class CalendarOut(CalendarCreate):
    id: int
    class Config:
        from_attributes = True

class SourceCreate(BaseModel):
    name: str
    source_type: str
    status: Optional[str] = "Mock"
    value: Optional[str] = None
    signals: Optional[str] = None
    workspace_id: Optional[int] = 1

class SourceOut(SourceCreate):
    id: int
    class Config:
        from_attributes = True

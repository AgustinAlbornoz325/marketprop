from pydantic import BaseModel
from typing import Optional

class PropertyCreate(BaseModel):
    title: str
    url: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    price: Optional[str] = None
    status: Optional[str] = "Activa"
    notes: Optional[str] = None
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
class SourceOut(SourceCreate):
    id: int
    class Config:
        from_attributes = True

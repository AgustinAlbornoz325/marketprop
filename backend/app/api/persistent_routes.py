from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.models import Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource, UserAccount
from app.core.schemas import (
    PropertyCreate, PropertyOut,
    ContentCreate, ContentOut,
    PipelineCreate, PipelineOut,
    CalendarCreate, CalendarOut,
    SourceCreate, SourceOut
)
from app.core.auth_tokens import (
    current_user_from_request,
    require_workspace_manager,
    require_workspace_owner,
)

router = APIRouter(prefix="/data", tags=["persistent-data"])

def get_current_user(request: Request, db: Session) -> UserAccount:
    return current_user_from_request(request, db)

def get_or_404(db, model, item_id: int):
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

def assert_same_workspace(item, user: UserAccount):
    if user.role == "super_admin":
        return
    if getattr(item, "workspace_id", None) != user.workspace_id:
        raise HTTPException(status_code=403, detail="No podés acceder a datos de otro workspace")

@router.get("/permissions")
def permissions(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return {
        "role": user.role,
        "can_manage_workspace": user.role in ("owner", "admin", "super_admin"),
        "can_delete_core_data": user.role in ("owner", "super_admin"),
        "can_create_content": user.role in ("member", "admin", "owner", "super_admin"),
        "can_access_admin_master": user.role == "super_admin",
        "rules": {
            "member": [
                "Puede ver datos de su inmobiliaria.",
                "Puede generar y guardar contenido.",
                "No puede crear/eliminar propiedades base.",
                "No puede modificar fuentes MarketDNA.",
                "No puede administrar usuarios, planes ni facturación."
            ],
            "admin": [
                "Puede gestionar propiedades, pipeline, calendario y fuentes.",
                "No puede acceder al Admin Master global."
            ],
            "owner": [
                "Puede administrar su inmobiliaria.",
                "No puede ver clientes de MarketProp ni facturación global."
            ],
            "super_admin": [
                "Puede acceder al Admin Master y ver datos globales."
            ]
        }
    }

@router.get("/properties", response_model=list[PropertyOut])
def list_properties(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    q = db.query(Property)
    if user.role != "super_admin":
        q = q.filter(Property.workspace_id == user.workspace_id)
    return q.order_by(Property.id.desc()).all()

@router.post("/properties", response_model=PropertyOut)
def create_property(payload: PropertyCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_manager(user)
    data = payload.model_dump()
    data["workspace_id"] = user.workspace_id
    item = Property(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/properties/{item_id}")
def delete_property(item_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_owner(user)
    item = get_or_404(db, Property, item_id)
    assert_same_workspace(item, user)
    db.delete(item)
    db.commit()
    return {"ok": True}

@router.get("/contents", response_model=list[ContentOut])
def list_contents(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    q = db.query(ContentItem)
    if user.role != "super_admin":
        q = q.filter(ContentItem.workspace_id == user.workspace_id)
    return q.order_by(ContentItem.id.desc()).all()

@router.post("/contents", response_model=ContentOut)
def create_content(payload: ContentCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    data = payload.model_dump()
    data["workspace_id"] = user.workspace_id
    item = ContentItem(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/pipeline", response_model=list[PipelineOut])
def list_pipeline(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    q = db.query(PipelineItem)
    if user.role != "super_admin":
        q = q.filter(PipelineItem.workspace_id == user.workspace_id)
    return q.order_by(PipelineItem.id.desc()).all()

@router.post("/pipeline", response_model=PipelineOut)
def create_pipeline(payload: PipelineCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_manager(user)
    data = payload.model_dump()
    data["workspace_id"] = user.workspace_id
    item = PipelineItem(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.patch("/pipeline/{item_id}/status")
def update_pipeline_status(item_id: int, status: str, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_manager(user)
    item = get_or_404(db, PipelineItem, item_id)
    assert_same_workspace(item, user)
    item.status = status
    db.commit()
    return {"ok": True, "id": item_id, "status": status}

@router.get("/calendar", response_model=list[CalendarOut])
def list_calendar(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    q = db.query(CalendarItem)
    if user.role != "super_admin":
        q = q.filter(CalendarItem.workspace_id == user.workspace_id)
    return q.order_by(CalendarItem.id.desc()).all()

@router.post("/calendar", response_model=CalendarOut)
def create_calendar(payload: CalendarCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_manager(user)
    data = payload.model_dump()
    data["workspace_id"] = user.workspace_id
    item = CalendarItem(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/sources", response_model=list[SourceOut])
def list_sources(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    q = db.query(MarketDNASource)
    if user.role != "super_admin":
        q = q.filter(MarketDNASource.workspace_id == user.workspace_id)
    return q.order_by(MarketDNASource.id.desc()).all()

@router.post("/sources", response_model=SourceOut)
def create_source(payload: SourceCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    require_workspace_manager(user)
    data = payload.model_dump()
    data["workspace_id"] = user.workspace_id
    item = MarketDNASource(**data)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.models import Workspace, UserAccount, SubscriptionPlan, UsageEvent, Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource
from app.core.schemas import PropertyCreate, PropertyOut, ContentCreate, ContentOut, PipelineCreate, PipelineOut, CalendarCreate, CalendarOut, SourceCreate, SourceOut

router = APIRouter(prefix="/data", tags=["persistent-data"])

def workspace_id(request: Request) -> int:
    raw = request.headers.get("x-workspace-id") or request.query_params.get("workspace_id") or "1"
    try:
        return int(raw)
    except ValueError:
        return 1

def get_or_404(db, model, item_id: int):
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@router.get("/properties", response_model=list[PropertyOut])
def list_properties(request: Request, db: Session = Depends(get_db)):
    wid = workspace_id(request)
    return db.query(Property).filter(Property.workspace_id == wid).order_by(Property.id.desc()).all()

@router.post("/properties", response_model=PropertyOut)
def create_property(payload: PropertyCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(); data["workspace_id"] = workspace_id(request)
    item = Property(**data)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.delete("/properties/{item_id}")
def delete_property(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = get_or_404(db, Property, item_id)
    if item.workspace_id != workspace_id(request):
        raise HTTPException(status_code=403, detail="No pertenece a este workspace")
    db.delete(item); db.commit()
    return {"ok": True}

@router.get("/contents", response_model=list[ContentOut])
def list_contents(request: Request, db: Session = Depends(get_db)):
    return db.query(ContentItem).filter(ContentItem.workspace_id == workspace_id(request)).order_by(ContentItem.id.desc()).all()

@router.post("/contents", response_model=ContentOut)
def create_content(payload: ContentCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(); data["workspace_id"] = workspace_id(request)
    item = ContentItem(**data)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/pipeline", response_model=list[PipelineOut])
def list_pipeline(request: Request, db: Session = Depends(get_db)):
    return db.query(PipelineItem).filter(PipelineItem.workspace_id == workspace_id(request)).order_by(PipelineItem.id.desc()).all()

@router.post("/pipeline", response_model=PipelineOut)
def create_pipeline(payload: PipelineCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(); data["workspace_id"] = workspace_id(request)
    item = PipelineItem(**data)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.patch("/pipeline/{item_id}/status")
def update_pipeline_status(item_id: int, status: str, request: Request, db: Session = Depends(get_db)):
    item = get_or_404(db, PipelineItem, item_id)
    if item.workspace_id != workspace_id(request):
        raise HTTPException(status_code=403, detail="No pertenece a este workspace")
    item.status = status; db.commit()
    return {"ok": True, "id": item_id, "status": status}

@router.get("/calendar", response_model=list[CalendarOut])
def list_calendar(request: Request, db: Session = Depends(get_db)):
    return db.query(CalendarItem).filter(CalendarItem.workspace_id == workspace_id(request)).order_by(CalendarItem.id.desc()).all()

@router.post("/calendar", response_model=CalendarOut)
def create_calendar(payload: CalendarCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(); data["workspace_id"] = workspace_id(request)
    item = CalendarItem(**data)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/sources", response_model=list[SourceOut])
def list_sources(request: Request, db: Session = Depends(get_db)):
    return db.query(MarketDNASource).filter(MarketDNASource.workspace_id == workspace_id(request)).order_by(MarketDNASource.id.desc()).all()

@router.post("/sources", response_model=SourceOut)
def create_source(payload: SourceCreate, request: Request, db: Session = Depends(get_db)):
    data = payload.model_dump(); data["workspace_id"] = workspace_id(request)
    item = MarketDNASource(**data)
    db.add(item); db.commit(); db.refresh(item)
    return item

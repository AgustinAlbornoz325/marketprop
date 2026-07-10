from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.models import Property, ContentItem, PipelineItem, CalendarItem, MarketDNASource
from app.core.schemas import PropertyCreate, PropertyOut, ContentCreate, ContentOut, PipelineCreate, PipelineOut, CalendarCreate, CalendarOut, SourceCreate, SourceOut

router = APIRouter(prefix="/data", tags=["persistent-data"])

def get_or_404(db, model, item_id: int):
    item = db.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@router.get("/properties", response_model=list[PropertyOut])
def list_properties(db: Session = Depends(get_db)):
    return db.query(Property).order_by(Property.id.desc()).all()

@router.post("/properties", response_model=PropertyOut)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    item = Property(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.delete("/properties/{item_id}")
def delete_property(item_id: int, db: Session = Depends(get_db)):
    item = get_or_404(db, Property, item_id)
    db.delete(item); db.commit()
    return {"ok": True}

@router.get("/contents", response_model=list[ContentOut])
def list_contents(db: Session = Depends(get_db)):
    return db.query(ContentItem).order_by(ContentItem.id.desc()).all()

@router.post("/contents", response_model=ContentOut)
def create_content(payload: ContentCreate, db: Session = Depends(get_db)):
    item = ContentItem(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/pipeline", response_model=list[PipelineOut])
def list_pipeline(db: Session = Depends(get_db)):
    return db.query(PipelineItem).order_by(PipelineItem.id.desc()).all()

@router.post("/pipeline", response_model=PipelineOut)
def create_pipeline(payload: PipelineCreate, db: Session = Depends(get_db)):
    item = PipelineItem(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.patch("/pipeline/{item_id}/status")
def update_pipeline_status(item_id: int, status: str, db: Session = Depends(get_db)):
    item = get_or_404(db, PipelineItem, item_id)
    item.status = status; db.commit()
    return {"ok": True, "id": item_id, "status": status}

@router.get("/calendar", response_model=list[CalendarOut])
def list_calendar(db: Session = Depends(get_db)):
    return db.query(CalendarItem).order_by(CalendarItem.id.desc()).all()

@router.post("/calendar", response_model=CalendarOut)
def create_calendar(payload: CalendarCreate, db: Session = Depends(get_db)):
    item = CalendarItem(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/sources", response_model=list[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.query(MarketDNASource).order_by(MarketDNASource.id.desc()).all()

@router.post("/sources", response_model=SourceOut)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    item = MarketDNASource(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

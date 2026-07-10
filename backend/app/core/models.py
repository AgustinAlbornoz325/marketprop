from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.db import Base

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(180), nullable=False)
    url = Column(Text, nullable=True)
    location = Column(String(180), nullable=True)
    property_type = Column(String(80), nullable=True)
    price = Column(String(80), nullable=True)
    status = Column(String(80), default="Activa")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ContentItem(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=True)
    platform = Column(String(80), nullable=False)
    format = Column(String(80), nullable=True)
    style = Column(String(80), nullable=True)
    title = Column(String(180), nullable=True)
    body = Column(Text, nullable=False)
    score = Column(Integer, default=0)
    status = Column(String(80), default="Contenido generado")
    created_at = Column(DateTime, default=datetime.utcnow)

class PipelineItem(Base):
    __tablename__ = "pipeline_items"
    id = Column(Integer, primary_key=True, index=True)
    property_title = Column(String(180), nullable=False)
    platform = Column(String(80), nullable=False)
    format = Column(String(80), nullable=True)
    objective = Column(String(180), nullable=True)
    status = Column(String(80), default="Propiedad cargada")
    owner = Column(String(80), default="Agus")
    score = Column(Integer, default=80)
    next_action = Column(Text, nullable=True)
    blocker = Column(Text, nullable=True)
    source = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CalendarItem(Base):
    __tablename__ = "calendar_items"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)
    title = Column(String(180), nullable=False)
    platform = Column(String(80), nullable=False)
    property_title = Column(String(180), nullable=True)
    goal = Column(String(180), nullable=True)
    score = Column(Integer, default=80)
    created_at = Column(DateTime, default=datetime.utcnow)

class MarketDNASource(Base):
    __tablename__ = "marketdna_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), nullable=False)
    source_type = Column(String(120), nullable=False)
    status = Column(String(80), default="Mock")
    value = Column(Text, nullable=True)
    signals = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.core.db import Base

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(180), nullable=False)
    slug = Column(String(120), nullable=False, unique=True, index=True)
    status = Column(String(40), default="active")
    plan = Column(String(80), default="Básico")
    created_at = Column(DateTime, default=datetime.utcnow)

class UserAccount(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(140), nullable=False)
    email = Column(String(180), nullable=False, unique=True, index=True)
    password_hash = Column(String(128), nullable=True)
    role = Column(String(60), default="owner")
    status = Column(String(40), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    plan_name = Column(String(80), default="Básico")
    status = Column(String(40), default="trial")
    monthly_content_limit = Column(Integer, default=500)
    ai_credit_limit = Column(Integer, default=100000)
    seats_limit = Column(Integer, default=2)
    created_at = Column(DateTime, default=datetime.utcnow)

class UsageEvent(Base):
    __tablename__ = "usage_events"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    event_type = Column(String(80), nullable=False)
    amount = Column(Integer, default=1)
    meta = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), default=1, index=True)
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
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), default=1, index=True)
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
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), default=1, index=True)
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
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), default=1, index=True)
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
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), default=1, index=True)
    name = Column(String(180), nullable=False)
    source_type = Column(String(120), nullable=False)
    status = Column(String(80), default="Mock")
    value = Column(Text, nullable=True)
    signals = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

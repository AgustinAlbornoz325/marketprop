from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.persistent_routes import router as data_router
from app.api.workspace_routes import router as workspace_router
from app.api.admin_routes import router as admin_router
from app.core.db import Base, engine, SessionLocal
from app.core.seed import seed_database
from app.core.migrations import run_light_migrations

app = FastAPI(title="MarketProp API", version="0.3.13 Usage Metering Plan Limits")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)
run_light_migrations(engine)
with SessionLocal() as db:
    seed_database(db)

app.include_router(router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(workspace_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

@app.get("/")
def root():
    return {"app": "MarketProp", "version": "0.3.13 Usage Metering Plan Limits", "status": "running"}

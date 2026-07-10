from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.persistent_routes import router as data_router
from app.core.db import Base, engine, SessionLocal
from app.core.seed import seed_database

app = FastAPI(title="MarketProp API", version="0.3.9 SaaS Foundation Database")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_database(db)

app.include_router(router, prefix="/api")
app.include_router(data_router, prefix="/api")

@app.get("/")
def root():
    return {"app": "MarketProp", "version": "0.3.9 SaaS Foundation Database", "status": "running"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import init_db

app=FastAPI(title="MarketProp Enterprise API", version="0.2.0 Alpha")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router,prefix="/api")

@app.get("/")
def root():
    return {"app":"MarketProp Enterprise","version":"0.2.0 Alpha","status":"running"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from schemas import Lead
from database import db, create_document, get_documents

app = FastAPI(title="Credit Broker API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = [
    "mutuo casa",
    "surroga mutuo",
    "mutuo liquidità",
    "mutuo ristrutturazione",
    "mutuo consolidamento debiti",
    "cessione del quinto e prestiti",
]


@app.get("/", tags=["health"]) 
def root():
    return {"status": "ok", "services": SERVICES}


@app.get("/test", tags=["health"]) 
def test_db():
    try:
        # a lightweight operation to ensure db connectivity
        _ = db.list_collection_names()
        return {"db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/lead", tags=["leads"]) 
async def create_lead(lead: Lead):
    if lead.service not in SERVICES:
        raise HTTPException(status_code=400, detail="Servizio non valido")

    data = lead.dict()
    data["created_at"] = datetime.utcnow()
    try:
        doc_id = create_document("lead", data)
        return {"success": True, "id": str(doc_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads", tags=["leads"]) 
async def list_leads(limit: int = 50, service: Optional[str] = None):
    try:
        filter_dict = {"service": service} if service else {}
        docs = get_documents("lead", filter_dict=filter_dict, limit=limit)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

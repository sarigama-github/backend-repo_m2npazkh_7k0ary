import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]


def create_document(collection_name: str, data: Dict[str, Any]):
    data = {**data, "created_at": data.get("created_at", datetime.utcnow())}
    res = db[collection_name].insert_one(data)
    return res.inserted_id


def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    cur = db[collection_name].find(filter_dict or {}).sort("created_at", -1).limit(limit)
    docs = []
    for d in cur:
        d["id"] = str(d.pop("_id"))
        docs.append(d)
    return docs

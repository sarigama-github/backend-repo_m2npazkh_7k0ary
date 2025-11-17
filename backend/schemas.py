from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    service: str = Field(..., description="Requested service")
    message: Optional[str] = Field(None, max_length=2000)
    created_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mario Rossi",
                "email": "mario.rossi@example.com",
                "phone": "+39 333 1234567",
                "service": "mutuo casa",
                "message": "Vorrei un preventivo per un mutuo prima casa da 200k€.",
            }
        }

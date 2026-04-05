from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    couple_id: Optional[str] = None
    has_partner: bool = False

class CoupleJoin(BaseModel):
    couple_id: str

class MemoryCreate(BaseModel):
    title: str
    description: str
    emotion: str
    
class MemoryResponse(MemoryCreate):
    id: int
    user_id: int
    date: datetime
    class Config:
        from_attributes = True

class ConflictCreate(BaseModel):
    severity: int
    reason: str
    resolved: bool = False

class ConflictResponse(ConflictCreate):
    id: int
    user_id: int
    date: datetime
    class Config:
        from_attributes = True

class WeeklyCheckCreate(BaseModel):
    mood: str
    conflict_status: bool

class WeeklyCheckResponse(WeeklyCheckCreate):
    id: int
    user_id: int
    date: datetime
    class Config:
        from_attributes = True

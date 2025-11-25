from pydantic import BaseModel
from typing import Optional, List

class Candidate(BaseModel):
    id: str
    candidate_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[str] = None
    experience: Optional[int] = None
    skills: Optional[List[str]] = None
    rating: Optional[float] = None
    notes: Optional[str] = None
    embeddings: Optional[List[float]] = None

class CandidateResponse(BaseModel):
    id: str
    candidate_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[str] = None
    experience: Optional[int] = None
    skills: Optional[List[str]] = None
    rating: Optional[float] = None
    notes: Optional[str] = None

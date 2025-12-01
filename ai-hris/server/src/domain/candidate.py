from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Any, Dict, Union

class Education(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    institution: str
    degree: str
    field_of_study: str = Field(..., alias="fieldOfStudy")
    graduation_year: int = Field(..., alias="graduationYear")
    gpa: Optional[float] = None

class WorkExperience(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    company: str
    position: str
    start_date: str = Field(..., alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")
    is_current: bool = Field(False, alias="isCurrent")
    description: Optional[str] = None

class BoundingBoxDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    content: Optional[str] = None
    page_number: Optional[int] = Field(None, alias="pageNumber")
    polygons: Optional[List[int]] = None

class ExtractedContent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bounding_boxes: Optional[List[Dict[str, Any]]] = Field(None, alias="boundingBoxes")
    content: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = Field(None, alias="structuredData")

class Note(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    author: str
    role: str
    message: str

class Address(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    detail: str
    city: str
    country: str
    zip: Optional[int] = None

class LegalDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    type: str  # RESUME, KTP, KARTU_KELUARGA, IJAZAH, etc.
    name: str
    url: str
    last_updated: str = Field(..., alias="lastUpdated")
    extracted_content: Optional[ExtractedContent] = Field(None, alias="extractedContent")

class InterviewScore(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    label: str
    value: float

class Interview(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    summary: Optional[str] = None
    score_details: Optional[List[InterviewScore]] = Field(None, alias="scoreDetails")
    interview_scores: Optional[List[InterviewScore]] = Field(None, alias="interviewScores")
    signals: Optional[list[str]] = None


class BriefData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    occupation: Optional[str] = None
    contact: Optional[str] = None


class FamilyMember(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    relationship: str
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    brief_data: Optional[BriefData] = Field(None, alias="briefData")


class Candidate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # Allow both snake_case and camelCase
        from_attributes=True
    )
    
    id: str
    candidate_id: str = Field(..., alias="candidateId")
    name: str
    photo_url: Optional[str] = Field(None, alias="photoUrl")
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    address: Optional[Address] = None
    position: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[str] = Field(None, alias="appliedDate")
    experience: Optional[Union[int, float]] = None
    skills: Optional[List[str]] = None
    rating: Optional[float] = None
    notes: Optional[Union[List[Note], str]] = None
    resume: Optional[List[LegalDocument]] = None
    legal_documents: Optional[List[LegalDocument]] = Field(None, alias="legalDocuments")
    education: Optional[List[Education]] = None
    work_experiences: Optional[List[WorkExperience]] = Field(None, alias="workExperiences")
    family_members: Optional[List[FamilyMember]] = Field(None, alias="familyMembers")
    embeddings: Optional[List[float]] = None
    interview: Optional[Interview] = None
    
    @field_validator('experience', mode='before')
    @classmethod
    def coerce_experience_to_float(cls, v):
        """Convert experience to float, handling both int and float types."""
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return v
    
    @field_validator('notes', mode='before')
    @classmethod
    def normalize_notes(cls, v):
        """Normalize notes to ensure it's a list of Note objects or a string."""
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if isinstance(v, list):
            # Try to convert list items to Note objects if they're dicts
            result = []
            for item in v:
                if isinstance(item, dict):
                    try:
                        result.append(Note(**item))
                    except Exception:
                        # If conversion fails, keep the dict as is
                        result.append(item)
                elif isinstance(item, Note):
                    result.append(item)
                else:
                    result.append(item)
            return result
        return v


class CandidateResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
    
    id: str
    candidate_id: str = Field(..., alias="candidateId")
    name: str
    photo_url: Optional[str] = Field(None, alias="photoUrl")
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    address: Optional[Address] = None
    position: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[str] = Field(None, alias="appliedDate")
    experience: Optional[Union[int, float]] = None
    skills: Optional[List[str]] = None
    rating: Optional[float] = None
    notes: Optional[Union[List[Note], str]] = None
    resume: Optional[List[LegalDocument]] = None
    legal_documents: Optional[List[LegalDocument]] = Field(None, alias="legalDocuments")
    education: Optional[List[Education]] = None
    work_experiences: Optional[List[WorkExperience]] = Field(None, alias="workExperiences")
    family_members: Optional[List[FamilyMember]] = Field(None, alias="familyMembers")
    embeddings: Optional[List[float]] = None
    interview: Optional[Interview] = None
    
    @field_validator('experience', mode='before')
    @classmethod
    def coerce_experience_to_float(cls, v):
        """Convert experience to float, handling both int and float types."""
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return None
        return v
    
    @field_validator('notes', mode='before')
    @classmethod
    def normalize_notes(cls, v):
        """Normalize notes to ensure it's a list of Note objects or a string."""
        if v is None:
            return None
        if isinstance(v, str):
            return v
        if isinstance(v, list):
            # Try to convert list items to Note objects if they're dicts
            result = []
            for item in v:
                if isinstance(item, dict):
                    try:
                        result.append(Note(**item))
                    except Exception:
                        # If conversion fails, keep the dict as is
                        result.append(item)
                elif isinstance(item, Note):
                    result.append(item)
                else:
                    result.append(item)
            return result
        return v

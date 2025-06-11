from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"  # "user", "admin", "recruiter"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CVCreate(BaseModel):
    data: str

class CVOut(BaseModel):
    id: int
    data: str
    skills: Optional[str] = None
    evaluation: Optional[str] = None
    file_pdf: Optional[str] = None
    file_docx: Optional[str] = None

    class Config:
        from_attributes = True

class NLPAnalysis(BaseModel):
    text: str

class SkillsRequest(BaseModel):
    skills: list[str]
    job_title: str

class TestAnswers(BaseModel):
    test_id: int
    answers: Dict[str, Any]  # ID de question -> réponse

class PersonalityProfile(BaseModel):
    profile_type: str  # ex: "INTJ", "Analytique", etc.
    description: str
    strengths: List[str]
    weaknesses: List[str]
    career_suggestions: List[str]
    detailed_results: Dict[str, Any]

class DashboardStats(BaseModel):
    total_cvs: int
    views_last_30_days: int
    downloads_last_30_days: int
    profile_completion: float  # pourcentage 0-100
    last_login: Optional[datetime] = None

class RecruiterSearchParams(BaseModel):
    skills: Optional[List[str]] = None
    education_level: Optional[int] = None
    min_experience: Optional[int] = None
    location: Optional[str] = None
    skip: int = 0
    limit: int = 20

class PublicCVOut(BaseModel):
    id: int
    user_id: int
    user_name: str
    skills: Optional[str] = None
    education_level: int
    years_experience: int
    location: Optional[str] = None

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    technologies: List[str]

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    technologies: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssistantRequest(BaseModel):
    text: str
    job_title: Optional[str] = None

class AssistantResponse(BaseModel):
    message: str
    suggestions: List[str]
    next_step: Optional[str] = None

class CoverLetterRequest(BaseModel):
    job_title: str
    company_name: str
    cv_id: int
    tone: str = "professional"  # professional, friendly, enthusiastic

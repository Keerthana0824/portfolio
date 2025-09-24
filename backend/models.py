from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


# Profile Models
class PersonalInfo(BaseModel):
    name: str
    title: str
    location: str
    email: EmailStr
    phone: str
    linkedin: str
    summary: str
    current_role: str


class Skills(BaseModel):
    programming: List[str] = []
    data_visualization: List[str] = []
    cloud_technologies: List[str] = []
    machine_learning: List[str] = []
    business_intelligence: List[str] = []


class Experience(BaseModel):
    company: str
    position: str
    duration: str
    location: str
    achievements: List[str] = []
    technologies: List[str] = []


class Education(BaseModel):
    degree: str
    institution: str
    location: str
    duration: str
    relevant_courses: List[str] = []


class Certification(BaseModel):
    name: str
    issuer: str
    year: str
    credential_id: str


class Profile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    personal: PersonalInfo
    skills: Skills
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[Certification] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Project Models
class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    company: str
    type: str  # "Professional Project" or "Academic Project"
    description: str
    impact: List[str] = []
    technologies: List[str] = []
    details: str
    featured: bool = True
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectCreate(BaseModel):
    title: str
    company: str
    type: str
    description: str
    impact: List[str] = []
    technologies: List[str] = []
    details: str
    featured: bool = True
    display_order: int = 0


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    impact: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    details: Optional[str] = None
    featured: Optional[bool] = None
    display_order: Optional[int] = None


# Contact Models
class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    subject: str
    message: str
    is_read: bool = False
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


# Analytics Models
class AnalyticsEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str  # "visit", "download", "contact"
    page: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyticsCreate(BaseModel):
    event_type: str
    page: Optional[str] = None


# Visualization Models
class Visualization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    metrics: List[str] = []
    chart_type: str
    chart_data: Dict[str, Any] = {}
    is_active: bool = True
    display_order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Response Models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class AnalyticsStats(BaseModel):
    total_visits: int
    total_downloads: int
    total_contacts: int
    recent_visits: List[Dict[str, Any]] = []
    top_pages: List[Dict[str, Any]] = []
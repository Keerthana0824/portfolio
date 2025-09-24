from fastapi import APIRouter, HTTPException, Request, Depends
from typing import List, Optional
import logging
from datetime import datetime

from models import (
    Profile, Project, ProjectCreate, ProjectUpdate, 
    ContactCreate, ContactMessage, AnalyticsCreate, 
    AnalyticsEvent, Visualization, APIResponse, AnalyticsStats
)
from database import DatabaseManager
from seed_data import seed_initial_data

logger = logging.getLogger(__name__)

# Create database manager instance
db_manager = None

def get_db_manager():
    global db_manager
    if db_manager is None:
        import os
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'portfolio')
        db_manager = DatabaseManager(mongo_url, db_name)
    return db_manager

def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "unknown"

router = APIRouter(prefix="/api", tags=["Portfolio"])

# Profile endpoints
@router.get("/profile", response_model=Profile)
async def get_profile():
    """Get complete profile information"""
    try:
        db = get_db_manager()
        profile_data = await db.get_profile()
        
        if not profile_data:
            # If no profile exists, seed initial data
            await seed_initial_data(db)
            profile_data = await db.get_profile()
            
        if not profile_data:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        return profile_data
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/profile", response_model=APIResponse)
async def update_profile(profile: Profile):
    """Update profile information (admin only)"""
    try:
        db = get_db_manager()
        success = await db.create_or_update_profile(profile.dict())
        
        if success:
            return APIResponse(success=True, message="Profile updated successfully")
        else:
            raise HTTPException(status_code=500, detail="Failed to update profile")
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Project endpoints
@router.get("/projects", response_model=List[Project])
async def get_projects(project_type: Optional[str] = None):
    """Get all projects, optionally filtered by type"""
    try:
        db = get_db_manager()
        projects = await db.get_projects(project_type)
        return projects
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/projects", response_model=APIResponse)
async def create_project(project: ProjectCreate):
    """Create a new project (admin only)"""
    try:
        db = get_db_manager()
        project_id = await db.create_project(project.dict())
        
        if project_id:
            return APIResponse(
                success=True, 
                message="Project created successfully", 
                data={"project_id": project_id}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create project")
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/projects/{project_id}", response_model=APIResponse)
async def update_project(project_id: str, project: ProjectUpdate):
    """Update a project (admin only)"""
    try:
        db = get_db_manager()
        success = await db.update_project(project_id, project.dict(exclude_unset=True))
        
        if success:
            return APIResponse(success=True, message="Project updated successfully")
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/projects/{project_id}", response_model=APIResponse)
async def delete_project(project_id: str):
    """Delete a project (admin only)"""
    try:
        db = get_db_manager()
        success = await db.delete_project(project_id)
        
        if success:
            return APIResponse(success=True, message="Project deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Contact endpoints
@router.post("/contact", response_model=APIResponse)
async def submit_contact_form(contact: ContactCreate, request: Request):
    """Submit contact form"""
    try:
        db = get_db_manager()
        
        # Add request metadata
        contact_data = contact.dict()
        contact_data['ip_address'] = get_client_ip(request)
        contact_data['user_agent'] = request.headers.get("User-Agent", "")
        
        message_id = await db.create_contact_message(contact_data)
        
        if message_id:
            # Log contact analytics event
            await db.create_analytics_event({
                "event_type": "contact",
                "page": "contact",
                "ip_address": contact_data['ip_address'],
                "user_agent": contact_data['user_agent']
            })
            
            return APIResponse(
                success=True, 
                message="Message sent successfully! I'll get back to you within 24 hours.",
                data={"message_id": message_id}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to send message")
    except Exception as e:
        logger.error(f"Error submitting contact form: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/contact", response_model=List[ContactMessage])
async def get_contact_messages():
    """Get all contact messages (admin only)"""
    try:
        db = get_db_manager()
        messages = await db.get_contact_messages()
        return messages
    except Exception as e:
        logger.error(f"Error getting contact messages: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/contact/{message_id}/read", response_model=APIResponse)
async def mark_message_read(message_id: str):
    """Mark message as read (admin only)"""
    try:
        db = get_db_manager()
        success = await db.mark_message_read(message_id)
        
        if success:
            return APIResponse(success=True, message="Message marked as read")
        else:
            raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        logger.error(f"Error marking message as read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Analytics endpoints
@router.post("/analytics/visit", response_model=APIResponse)
async def log_visit(analytics: AnalyticsCreate, request: Request):
    """Log a page visit"""
    try:
        db = get_db_manager()
        
        event_data = analytics.dict()
        event_data['ip_address'] = get_client_ip(request)
        event_data['user_agent'] = request.headers.get("User-Agent", "")
        event_data['referrer'] = request.headers.get("Referer", "")
        
        success = await db.create_analytics_event(event_data)
        
        if success:
            return APIResponse(success=True, message="Visit logged")
        else:
            raise HTTPException(status_code=500, detail="Failed to log visit")
    except Exception as e:
        logger.error(f"Error logging visit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analytics/download", response_model=APIResponse)
async def log_download(request: Request):
    """Log a resume download"""
    try:
        db = get_db_manager()
        
        event_data = {
            "event_type": "download",
            "page": "resume",
            "ip_address": get_client_ip(request),
            "user_agent": request.headers.get("User-Agent", ""),
            "referrer": request.headers.get("Referer", "")
        }
        
        success = await db.create_analytics_event(event_data)
        
        if success:
            return APIResponse(success=True, message="Download logged")
        else:
            raise HTTPException(status_code=500, detail="Failed to log download")
    except Exception as e:
        logger.error(f"Error logging download: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/analytics/stats", response_model=AnalyticsStats)
async def get_analytics_stats():
    """Get analytics statistics (admin only)"""
    try:
        db = get_db_manager()
        stats = await db.get_analytics_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting analytics stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Resume endpoints
@router.get("/resume/download")
async def download_resume(request: Request):
    """Download resume and log the event"""
    try:
        # Log download event
        db = get_db_manager()
        await db.create_analytics_event({
            "event_type": "download",
            "page": "resume",
            "ip_address": get_client_ip(request),
            "user_agent": request.headers.get("User-Agent", "")
        })
        
        # For now, return a mock response - in production, serve actual PDF file
        return APIResponse(
            success=True, 
            message="Resume download initiated",
            data={"filename": "Keerthana_Madisetty_Resume.pdf"}
        )
    except Exception as e:
        logger.error(f"Error downloading resume: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Visualization endpoints
@router.get("/visualizations", response_model=List[Visualization])
async def get_visualizations():
    """Get all active visualizations"""
    try:
        db = get_db_manager()
        visualizations = await db.get_visualizations()
        return visualizations
    except Exception as e:
        logger.error(f"Error getting visualizations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
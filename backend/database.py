from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, mongo_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[db_name]
        
    async def close_connection(self):
        self.client.close()

    # Profile operations
    async def get_profile(self) -> Optional[Dict]:
        """Get the main profile document"""
        try:
            profile = await self.db.profile.find_one({})
            if profile:
                profile['_id'] = str(profile['_id'])
            return profile
        except Exception as e:
            logger.error(f"Error getting profile: {e}")
            return None

    async def create_or_update_profile(self, profile_data: Dict) -> bool:
        """Create or update the profile document"""
        try:
            profile_data['updated_at'] = datetime.utcnow()
            
            existing = await self.db.profile.find_one({})
            if existing:
                # Update existing profile
                await self.db.profile.update_one(
                    {"_id": existing["_id"]}, 
                    {"$set": profile_data}
                )
            else:
                # Create new profile
                profile_data['created_at'] = datetime.utcnow()
                await self.db.profile.insert_one(profile_data)
            
            return True
        except Exception as e:
            logger.error(f"Error creating/updating profile: {e}")
            return False

    # Project operations
    async def get_projects(self, project_type: Optional[str] = None) -> List[Dict]:
        """Get all projects, optionally filtered by type"""
        try:
            query = {}
            if project_type:
                query["type"] = project_type
            
            cursor = self.db.projects.find(query).sort("display_order", 1)
            projects = []
            async for project in cursor:
                project['_id'] = str(project['_id'])
                projects.append(project)
            return projects
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return []

    async def create_project(self, project_data: Dict) -> Optional[str]:
        """Create a new project"""
        try:
            project_data['created_at'] = datetime.utcnow()
            project_data['updated_at'] = datetime.utcnow()
            
            result = await self.db.projects.insert_one(project_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return None

    async def update_project(self, project_id: str, project_data: Dict) -> bool:
        """Update an existing project"""
        try:
            from bson import ObjectId
            project_data['updated_at'] = datetime.utcnow()
            
            result = await self.db.projects.update_one(
                {"_id": ObjectId(project_id)}, 
                {"$set": project_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating project: {e}")
            return False

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        try:
            from bson import ObjectId
            result = await self.db.projects.delete_one({"_id": ObjectId(project_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            return False

    # Contact operations
    async def create_contact_message(self, message_data: Dict) -> Optional[str]:
        """Create a new contact message"""
        try:
            message_data['created_at'] = datetime.utcnow()
            message_data['is_read'] = False
            
            result = await self.db.contact_messages.insert_one(message_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating contact message: {e}")
            return None

    async def get_contact_messages(self) -> List[Dict]:
        """Get all contact messages"""
        try:
            cursor = self.db.contact_messages.find({}).sort("created_at", -1)
            messages = []
            async for message in cursor:
                message['_id'] = str(message['_id'])
                messages.append(message)
            return messages
        except Exception as e:
            logger.error(f"Error getting contact messages: {e}")
            return []

    async def mark_message_read(self, message_id: str) -> bool:
        """Mark a contact message as read"""
        try:
            from bson import ObjectId
            result = await self.db.contact_messages.update_one(
                {"_id": ObjectId(message_id)}, 
                {"$set": {"is_read": True}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False

    # Analytics operations
    async def create_analytics_event(self, event_data: Dict) -> bool:
        """Create a new analytics event"""
        try:
            event_data['timestamp'] = datetime.utcnow()
            await self.db.analytics.insert_one(event_data)
            return True
        except Exception as e:
            logger.error(f"Error creating analytics event: {e}")
            return False

    async def get_analytics_stats(self) -> Dict[str, Any]:
        """Get analytics statistics"""
        try:
            # Total counts
            total_visits = await self.db.analytics.count_documents({"event_type": "visit"})
            total_downloads = await self.db.analytics.count_documents({"event_type": "download"})
            total_contacts = await self.db.contact_messages.count_documents({})
            
            # Recent visits
            recent_cursor = self.db.analytics.find({"event_type": "visit"}).sort("timestamp", -1).limit(10)
            recent_visits = []
            async for visit in recent_cursor:
                recent_visits.append({
                    "page": visit.get("page", "/"),
                    "timestamp": visit["timestamp"],
                    "ip_address": visit.get("ip_address", "unknown")
                })
            
            # Top pages
            pipeline = [
                {"$match": {"event_type": "visit"}},
                {"$group": {"_id": "$page", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 5}
            ]
            
            top_pages = []
            async for page in self.db.analytics.aggregate(pipeline):
                top_pages.append({
                    "page": page["_id"] or "/",
                    "visits": page["count"]
                })
            
            return {
                "total_visits": total_visits,
                "total_downloads": total_downloads,
                "total_contacts": total_contacts,
                "recent_visits": recent_visits,
                "top_pages": top_pages
            }
        except Exception as e:
            logger.error(f"Error getting analytics stats: {e}")
            return {
                "total_visits": 0,
                "total_downloads": 0,
                "total_contacts": 0,
                "recent_visits": [],
                "top_pages": []
            }

    # Visualizations operations
    async def get_visualizations(self) -> List[Dict]:
        """Get all active visualizations"""
        try:
            cursor = self.db.visualizations.find({"is_active": True}).sort("display_order", 1)
            visualizations = []
            async for viz in cursor:
                viz['_id'] = str(viz['_id'])
                visualizations.append(viz)
            return visualizations
        except Exception as e:
            logger.error(f"Error getting visualizations: {e}")
            return []

    async def create_visualization(self, viz_data: Dict) -> Optional[str]:
        """Create a new visualization"""
        try:
            viz_data['created_at'] = datetime.utcnow()
            viz_data['updated_at'] = datetime.utcnow()
            
            result = await self.db.visualizations.insert_one(viz_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return None
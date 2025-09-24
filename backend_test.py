#!/usr/bin/env python3
"""
Portfolio Backend API Testing Suite
Tests all portfolio API endpoints for functionality and data integrity
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Get backend URL from frontend environment
BACKEND_URL = "https://pro-portfolio-116.preview.emergentagent.com/api"

class PortfolioAPITester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.failed_tests = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success:
            self.failed_tests.append(test_name)
        print()
    
    async def test_profile_api(self):
        """Test Profile API endpoints"""
        print("=== Testing Profile API ===")
        
        try:
            # Test GET /api/profile
            async with self.session.get(f"{BACKEND_URL}/profile") as response:
                if response.status == 200:
                    profile_data = await response.json()
                    
                    # Check required profile structure
                    required_fields = ['personal', 'skills', 'experience', 'education', 'certifications']
                    missing_fields = [field for field in required_fields if field not in profile_data]
                    
                    if not missing_fields:
                        # Check personal info structure
                        personal = profile_data.get('personal', {})
                        personal_required = ['name', 'title', 'location', 'email', 'phone', 'linkedin', 'summary']
                        missing_personal = [field for field in personal_required if field not in personal]
                        
                        if not missing_personal:
                            self.log_test(
                                "Profile API - GET /api/profile", 
                                True, 
                                f"Profile retrieved successfully with all required fields",
                                {"profile_name": personal.get('name', 'Unknown')}
                            )
                        else:
                            self.log_test(
                                "Profile API - GET /api/profile", 
                                False, 
                                f"Missing personal info fields: {missing_personal}"
                            )
                    else:
                        self.log_test(
                            "Profile API - GET /api/profile", 
                            False, 
                            f"Missing required profile fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Profile API - GET /api/profile", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
                    
        except Exception as e:
            self.log_test("Profile API - GET /api/profile", False, f"Exception: {str(e)}")
    
    async def test_projects_api(self):
        """Test Projects API endpoints"""
        print("=== Testing Projects API ===")
        
        try:
            # Test GET /api/projects (all projects)
            async with self.session.get(f"{BACKEND_URL}/projects") as response:
                if response.status == 200:
                    projects = await response.json()
                    
                    if isinstance(projects, list):
                        self.log_test(
                            "Projects API - GET /api/projects", 
                            True, 
                            f"Retrieved {len(projects)} projects",
                            {"project_count": len(projects)}
                        )
                        
                        # Test project structure if projects exist
                        if projects:
                            project = projects[0]
                            required_fields = ['title', 'company', 'type', 'description', 'impact', 'technologies']
                            missing_fields = [field for field in required_fields if field not in project]
                            
                            if not missing_fields:
                                self.log_test(
                                    "Projects API - Project Structure", 
                                    True, 
                                    "Project contains all required fields"
                                )
                            else:
                                self.log_test(
                                    "Projects API - Project Structure", 
                                    False, 
                                    f"Missing project fields: {missing_fields}"
                                )
                    else:
                        self.log_test(
                            "Projects API - GET /api/projects", 
                            False, 
                            "Response is not a list"
                        )
                else:
                    self.log_test(
                        "Projects API - GET /api/projects", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
            
            # Test filtering by project type
            for project_type in ["Professional Project", "Academic Project"]:
                async with self.session.get(f"{BACKEND_URL}/projects?project_type={project_type}") as response:
                    if response.status == 200:
                        filtered_projects = await response.json()
                        
                        # Verify all projects match the filter
                        all_match = all(p.get('type') == project_type for p in filtered_projects)
                        
                        self.log_test(
                            f"Projects API - Filter by {project_type}", 
                            all_match, 
                            f"Retrieved {len(filtered_projects)} {project_type.lower()}s" if all_match 
                            else "Some projects don't match the filter"
                        )
                    else:
                        self.log_test(
                            f"Projects API - Filter by {project_type}", 
                            False, 
                            f"HTTP {response.status}: {await response.text()}"
                        )
                        
        except Exception as e:
            self.log_test("Projects API", False, f"Exception: {str(e)}")
    
    async def test_contact_api(self):
        """Test Contact Form API"""
        print("=== Testing Contact API ===")
        
        try:
            # Test POST /api/contact with valid data
            contact_data = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "subject": "Test Contact Form",
                "message": "This is a test message from the API testing suite."
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/contact", 
                json=contact_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get('success'):
                        self.log_test(
                            "Contact API - POST /api/contact", 
                            True, 
                            f"Contact form submitted successfully: {result.get('message', '')}"
                        )
                    else:
                        self.log_test(
                            "Contact API - POST /api/contact", 
                            False, 
                            f"API returned success=false: {result.get('message', '')}"
                        )
                else:
                    self.log_test(
                        "Contact API - POST /api/contact", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
            
            # Test validation - missing required fields
            invalid_data = {"name": "Test User"}  # Missing email, subject, message
            
            async with self.session.post(
                f"{BACKEND_URL}/contact", 
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                # Should return validation error (422 or 400)
                if response.status in [400, 422]:
                    self.log_test(
                        "Contact API - Validation", 
                        True, 
                        f"Properly rejected invalid data with HTTP {response.status}"
                    )
                else:
                    self.log_test(
                        "Contact API - Validation", 
                        False, 
                        f"Should reject invalid data but got HTTP {response.status}"
                    )
                    
        except Exception as e:
            self.log_test("Contact API", False, f"Exception: {str(e)}")
    
    async def test_analytics_api(self):
        """Test Analytics API endpoints"""
        print("=== Testing Analytics API ===")
        
        try:
            # Test POST /api/analytics/visit
            visit_data = {
                "event_type": "visit",
                "page": "/test-page"
            }
            
            async with self.session.post(
                f"{BACKEND_URL}/analytics/visit", 
                json=visit_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get('success'):
                        self.log_test(
                            "Analytics API - POST /api/analytics/visit", 
                            True, 
                            f"Visit logged successfully: {result.get('message', '')}"
                        )
                    else:
                        self.log_test(
                            "Analytics API - POST /api/analytics/visit", 
                            False, 
                            f"API returned success=false: {result.get('message', '')}"
                        )
                else:
                    self.log_test(
                        "Analytics API - POST /api/analytics/visit", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
            
            # Test POST /api/analytics/download
            async with self.session.post(
                f"{BACKEND_URL}/analytics/download",
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get('success'):
                        self.log_test(
                            "Analytics API - POST /api/analytics/download", 
                            True, 
                            f"Download logged successfully: {result.get('message', '')}"
                        )
                    else:
                        self.log_test(
                            "Analytics API - POST /api/analytics/download", 
                            False, 
                            f"API returned success=false: {result.get('message', '')}"
                        )
                else:
                    self.log_test(
                        "Analytics API - POST /api/analytics/download", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
                    
        except Exception as e:
            self.log_test("Analytics API", False, f"Exception: {str(e)}")
    
    async def test_resume_api(self):
        """Test Resume Download API"""
        print("=== Testing Resume API ===")
        
        try:
            # Test GET /api/resume/download
            async with self.session.get(f"{BACKEND_URL}/resume/download") as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get('success'):
                        self.log_test(
                            "Resume API - GET /api/resume/download", 
                            True, 
                            f"Resume download initiated: {result.get('message', '')}"
                        )
                    else:
                        self.log_test(
                            "Resume API - GET /api/resume/download", 
                            False, 
                            f"API returned success=false: {result.get('message', '')}"
                        )
                else:
                    self.log_test(
                        "Resume API - GET /api/resume/download", 
                        False, 
                        f"HTTP {response.status}: {await response.text()}"
                    )
                    
        except Exception as e:
            self.log_test("Resume API", False, f"Exception: {str(e)}")
    
    async def test_error_handling(self):
        """Test Error Handling and CORS"""
        print("=== Testing Error Handling ===")
        
        try:
            # Test 404 for invalid endpoint
            async with self.session.get(f"{BACKEND_URL}/nonexistent-endpoint") as response:
                if response.status == 404:
                    self.log_test(
                        "Error Handling - 404 for invalid endpoint", 
                        True, 
                        "Properly returns 404 for invalid endpoints"
                    )
                else:
                    self.log_test(
                        "Error Handling - 404 for invalid endpoint", 
                        False, 
                        f"Expected 404 but got HTTP {response.status}"
                    )
            
            # Test CORS headers
            async with self.session.options(f"{BACKEND_URL}/profile") as response:
                cors_headers = {
                    'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                    'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                    'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
                }
                
                has_cors = any(cors_headers.values())
                
                self.log_test(
                    "CORS Configuration", 
                    has_cors, 
                    f"CORS headers present: {has_cors}" if has_cors 
                    else "No CORS headers found"
                )
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
    
    async def test_database_integration(self):
        """Test Database Integration by checking data consistency"""
        print("=== Testing Database Integration ===")
        
        try:
            # Check if profile data exists (indicates seed data was loaded)
            async with self.session.get(f"{BACKEND_URL}/profile") as response:
                if response.status == 200:
                    profile = await response.json()
                    has_data = bool(profile.get('personal', {}).get('name'))
                    
                    self.log_test(
                        "Database Integration - Seed Data", 
                        has_data, 
                        "Profile seed data loaded successfully" if has_data 
                        else "No profile data found - seed data may not be loaded"
                    )
                else:
                    self.log_test(
                        "Database Integration - Seed Data", 
                        False, 
                        f"Cannot access profile data: HTTP {response.status}"
                    )
            
            # Check projects data
            async with self.session.get(f"{BACKEND_URL}/projects") as response:
                if response.status == 200:
                    projects = await response.json()
                    has_projects = len(projects) > 0
                    
                    self.log_test(
                        "Database Integration - Projects Data", 
                        has_projects, 
                        f"Found {len(projects)} projects in database" if has_projects 
                        else "No projects found in database"
                    )
                else:
                    self.log_test(
                        "Database Integration - Projects Data", 
                        False, 
                        f"Cannot access projects data: HTTP {response.status}"
                    )
                    
        except Exception as e:
            self.log_test("Database Integration", False, f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all API tests"""
        print(f"Starting Portfolio Backend API Tests")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 60)
        
        # Run all test suites
        await self.test_profile_api()
        await self.test_projects_api()
        await self.test_contact_api()
        await self.test_analytics_api()
        await self.test_resume_api()
        await self.test_error_handling()
        await self.test_database_integration()
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print("\nFAILED TESTS:")
            for test in self.failed_tests:
                print(f"  ❌ {test}")
        
        print("\nDETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}")
            if result['details']:
                print(f"    {result['details']}")
        
        return {
            'total': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'failed_tests': self.failed_tests,
            'results': self.test_results
        }

async def main():
    """Main test runner"""
    async with PortfolioAPITester() as tester:
        results = await tester.run_all_tests()
        
        # Exit with error code if tests failed
        if results['failed'] > 0:
            sys.exit(1)
        else:
            print("\n🎉 All tests passed!")
            sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
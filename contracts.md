# Portfolio Backend Integration Contracts

## Overview
This document outlines the API contracts and integration plan for Keerthana's professional portfolio, transitioning from mock data to a fully functional backend.

## Current Mock Data Structure

### 1. Personal Information
```javascript
personal: {
  name, title, location, email, phone, linkedin, summary, currentRole
}
```

### 2. Skills Categories
```javascript
skills: {
  programming: Array<string>,
  dataVisualization: Array<string>, 
  cloudTechnologies: Array<string>,
  machineLearning: Array<string>,
  businessIntelligence: Array<string>
}
```

### 3. Experience Records
```javascript
experience: [{
  company, position, duration, location, achievements: Array<string>, technologies: Array<string>
}]
```

### 4. Projects
```javascript
projects: [{
  title, company, type, description, impact: Array<string>, technologies: Array<string>, details
}]
```

### 5. Education & Certifications
```javascript
education: [{ degree, institution, location, duration, relevantCourses }]
certifications: [{ name, issuer, year, credentialId }]
```

### 6. Visualizations
```javascript
visualizations: [{ title, description, metrics: Array<string>, chartType }]
```

## API Endpoints to Implement

### Portfolio Data Management
- `GET /api/profile` - Get complete profile information
- `PUT /api/profile` - Update profile information (admin only)
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Add new project (admin only)
- `PUT /api/projects/:id` - Update project (admin only)
- `DELETE /api/projects/:id` - Delete project (admin only)

### Contact Management
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all contact messages (admin only)
- `PUT /api/contact/:id/read` - Mark message as read (admin only)

### Analytics & Tracking
- `POST /api/analytics/visit` - Log page visit
- `POST /api/analytics/download` - Log resume download
- `GET /api/analytics/stats` - Get visit statistics (admin only)

### Resume Management
- `GET /api/resume/download` - Download latest resume
- `POST /api/resume/upload` - Upload new resume (admin only)

## Database Schema

### Profile Collection
```javascript
{
  _id: ObjectId,
  personal: {
    name: String,
    title: String,
    location: String,
    email: String,
    phone: String,
    linkedin: String,
    summary: String,
    currentRole: String
  },
  skills: {
    programming: [String],
    dataVisualization: [String],
    cloudTechnologies: [String],
    machineLearning: [String],
    businessIntelligence: [String]
  },
  experience: [{
    company: String,
    position: String,
    duration: String,
    location: String,
    achievements: [String],
    technologies: [String]
  }],
  education: [{
    degree: String,
    institution: String,
    location: String,
    duration: String,
    relevantCourses: [String]
  }],
  certifications: [{
    name: String,
    issuer: String,
    year: String,
    credentialId: String
  }],
  createdAt: Date,
  updatedAt: Date
}
```

### Projects Collection
```javascript
{
  _id: ObjectId,
  title: String,
  company: String,
  type: String, // "Professional Project" | "Academic Project"
  description: String,
  impact: [String],
  technologies: [String],
  details: String,
  featured: Boolean,
  displayOrder: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### Contact Messages Collection
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  subject: String,
  message: String,
  isRead: Boolean,
  ipAddress: String,
  userAgent: String,
  createdAt: Date
}
```

### Analytics Collection
```javascript
{
  _id: ObjectId,
  eventType: String, // "visit" | "download" | "contact"
  page: String,
  ipAddress: String,
  userAgent: String,
  referrer: String,
  timestamp: Date
}
```

### Visualizations Collection
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  metrics: [String],
  chartType: String,
  chartData: Object, // Store actual chart configuration
  isActive: Boolean,
  displayOrder: Number,
  createdAt: Date,
  updatedAt: Date
}
```

## Frontend Integration Plan

### 1. API Service Layer
Create `src/services/api.js` with:
- Axios configuration with base URL
- Error handling and retry logic
- Request/response interceptors

### 2. Data Hooks
Replace mock data with React hooks:
- `useProfile()` - Get profile data
- `useProjects()` - Get projects with filtering
- `useContact()` - Handle contact form submission
- `useAnalytics()` - Track user interactions

### 3. Component Updates
- Replace `mockData` imports with API hooks
- Add loading states for all data fetching
- Implement error handling and fallbacks
- Add success/error notifications

### 4. Key Integration Points

#### Header Component
- Replace `mockFunctions.downloadResume` with real API call
- Add analytics tracking for download events

#### Projects Component  
- Replace `mockData.projects` with `useProjects()` hook
- Add loading skeleton while fetching
- Implement real project filtering from backend

#### Contact Component
- Replace `mockFunctions.sendMessage` with real API endpoint
- Add form validation and submission feedback
- Implement email notifications (optional)

#### Visualizations Component
- Replace mock chart data with real visualization configs
- Add interactive data updates from backend
- Implement real-time metrics (if needed)

## Implementation Priority

### Phase 1: Core Backend (Essential)
1. Profile data management API
2. Projects CRUD operations  
3. Contact form submission
4. Basic analytics tracking

### Phase 2: Enhanced Features (Important)
1. Resume upload/download functionality
2. Admin authentication for content management
3. Email notifications for contact forms
4. Advanced analytics and reporting

### Phase 3: Advanced Features (Nice to have)
1. Real-time dashboard metrics
2. Content versioning
3. SEO optimization endpoints
4. Performance monitoring

## Error Handling Strategy

### Backend Errors
- Validate all input data
- Return consistent error format: `{ success: false, message: string, code: number }`
- Log errors for debugging
- Handle database connection failures gracefully

### Frontend Errors  
- Show user-friendly error messages
- Implement retry mechanisms for failed requests
- Fallback to cached/default data when possible
- Track errors for monitoring

## Security Considerations

### Data Protection
- Sanitize all user inputs
- Implement rate limiting on contact form
- Validate email addresses and phone numbers
- Store minimal analytics data (no PII)

### Admin Features
- Simple password-based authentication for content updates
- Separate admin routes with protection middleware
- Input validation for all admin operations

This contract ensures a smooth transition from mock data to a fully functional portfolio backend while maintaining the existing user experience.
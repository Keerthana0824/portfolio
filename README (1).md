# Professional Portfolio - Venkata Keerthana Madisetty

A modern, responsive portfolio website showcasing my experience as a Business Data Analyst with expertise in data analytics, machine learning, and business intelligence.

## 🚀 Live Demo

[Portfolio Website](https://your-portfolio-url.com)

## 🛠️ Technologies Used

### Frontend
- **React 19** - Modern UI library
- **Tailwind CSS** - Utility-first CSS framework  
- **Shadcn/UI** - Modern component library
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation

### Deployment
- **Frontend**: Vercel/Netlify
- **Backend**: Railway/Render
- **Database**: MongoDB Atlas

## 📋 Features

- **Responsive Design** - Optimized for all device sizes
- **Interactive Components** - Smooth animations and transitions
- **Contact Form** - Direct email integration
- **Analytics Tracking** - Visit and interaction logging
- **Resume Download** - PDF download functionality
- **Real-time Data** - Dynamic content from backend API

## 🏗️ Project Structure

```
portfolio/
├── frontend/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── ...
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── models.py           # Data models
│   ├── database.py         # Database operations
│   ├── portfolio_routes.py # API endpoints
│   ├── seed_data.py        # Initial data
│   └── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and yarn
- Python 3.11+
- MongoDB

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set environment variables
   export MONGO_URL="mongodb://localhost:27017"
   export DB_NAME="portfolio"
   
   # Start backend
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   yarn install
   
   # Set environment variables
   echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
   
   # Start frontend  
   yarn start
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001/docs

## 📊 Portfolio Sections

### About
- Professional summary and background
- Current role and location
- Core competencies and skills

### Experience  
- **Liberty Mutual Insurance** - Business Data Analyst (2025-Present)
- **Hexaware Technologies** - Jr. Business Data Analyst (2021-2023)

### Education
- **MS Data Science** - George Washington University (2025)
- **B.Tech Computer Science** - MVJ College of Engineering (2022)

### Projects
- Claims360 Analytics Platform
- Unified Claims & Credit Risk Analytics  
- Customer Churn Prediction Model
- Healthcare Analytics Dashboard

### Skills
- **Programming**: Python, R, SQL, DAX
- **Data Visualization**: Power BI, Tableau, Excel
- **Cloud Technologies**: AWS, Azure
- **Machine Learning**: Predictive Modeling, Fraud Detection
- **Business Intelligence**: KPI Development, Regulatory Reporting

### Certifications
- AWS Certified Cloud Practitioner
- Salesforce Certified: Tableau Desktop Foundations

## 🌐 Deployment

### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### Backend Deployment (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
cd backend
railway login
railway init
railway up
```

## 📧 Contact

- **Email**: keerthanamadisetty2@gmail.com
- **Phone**: (202) 681-9470
- **LinkedIn**: [linkedin.com/in/keerthana-madisetty-60a10b214](https://www.linkedin.com/in/keerthana-madisetty-60a10b214)
- **Location**: Arlington, VA

## 📈 Key Achievements

- 🎯 **22%** improvement in fraud detection efficiency
- ⚡ **33%** reduction in claims settlement cycle time  
- 📊 **40%** increase in insights visibility
- 🎓 **MS Data Science** Graduate (2025)
- 📜 **2 Professional Certifications** 

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ by Venkata Keerthana Madisetty

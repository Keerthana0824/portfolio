from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

async def seed_initial_data(db_manager):
    """Seed the database with Keerthana's initial portfolio data"""
    try:
        # Check if profile already exists
        existing_profile = await db_manager.get_profile()
        if existing_profile:
            logger.info("Profile already exists, skipping seed data")
            return
            
        # Profile data from extracted resume information
        profile_data = {
            "personal": {
                "name": "Venkata Keerthana Madisetty",
                "title": "Business Data Analyst",
                "location": "Arlington, VA",
                "email": "keerthanamadisetty2@gmail.com",
                "phone": "(202) 681-9470",
                "linkedin": "https://www.linkedin.com/in/keerthana-madisetty-60a10b214",
                "summary": "Experienced Business Data Analyst with 3+ years of expertise in analyzing complex datasets, developing predictive models, and delivering actionable insights. Specialized in fraud detection, claims automation, and regulatory reporting with proven track record of improving operational efficiency by 33% and fraud detection accuracy by 22%.",
                "current_role": "Business Data Analyst at Liberty Mutual Insurance"
            },
            "skills": {
                "programming": [
                    "Python (Pandas, NumPy, Scikit-learn, Matplotlib)",
                    "R (Statistical Analysis)",
                    "SQL (Complex Joins, CTEs, Window Functions)",
                    "DAX (Power BI)"
                ],
                "data_visualization": [
                    "Power BI (Advanced Dashboards, RLS, Power Query)",
                    "Tableau (Desktop & Server)",
                    "SAP BusinessObjects",
                    "Excel (Pivot Tables, Power Query, VBA)"
                ],
                "cloud_technologies": [
                    "AWS (S3, Glue, Redshift, SageMaker)",
                    "Azure (Data Lake, Data Factory, Synapse Analytics, ML Studio)",
                    "ETL Processes & Data Pipelines",
                    "Data Warehousing"
                ],
                "machine_learning": [
                    "Predictive Modeling",
                    "Fraud Detection Algorithms",
                    "Risk Scoring Models",
                    "Statistical Analysis & Hypothesis Testing"
                ],
                "business_intelligence": [
                    "KPI Development & Framework Design",
                    "Regulatory Compliance Reporting (IRDA, RBI)",
                    "Cross-functional Stakeholder Management",
                    "Agile Methodologies (JIRA, Confluence)"
                ]
            },
            "experience": [
                {
                    "company": "Liberty Mutual Insurance",
                    "position": "Business Data Analyst",
                    "duration": "Apr 2025 - Present",
                    "location": "USA",
                    "achievements": [
                        "Delivered Liberty Claims360 analytics platform, partnering with stakeholders to define reporting requirements",
                        "Improved fraud detection efficiency by 22% using predictive analytics with Python and AWS SageMaker",
                        "Accelerated claims settlement by 33% through optimized data pipeline using AWS Glue, Power BI, and SQL",
                        "Enhanced insights visibility by 40% with Power BI dashboards integrated with AWS Redshift",
                        "Extracted and consolidated data using SQL and Excel, leveraging AWS S3 and Glue for data processing"
                    ],
                    "technologies": ["AWS (S3, Glue, Redshift, SageMaker)", "Power BI", "Python", "SQL", "Excel"]
                },
                {
                    "company": "Hexaware Technologies",
                    "position": "Jr. Business Data Analyst",
                    "duration": "Feb 2021 - Jul 2023",
                    "location": "India",
                    "achievements": [
                        "Improved loan risk assessment accuracy by 23% through predictive risk scoring models using Python and Azure ML",
                        "Automated regulatory reporting using SAP BusinessObjects, ensuring IRDA and RBI compliance",
                        "Built interactive dashboards in Power BI and Tableau integrated with Azure Synapse Analytics",
                        "Collaborated with stakeholders using JIRA and Confluence to translate requirements into actionable user stories",
                        "Optimized claims settlement processes and refined loan eligibility rules through customer behavior analysis"
                    ],
                    "technologies": ["Azure (Data Lake, Data Factory, Synapse)", "Python", "Power BI", "Tableau", "SAP BusinessObjects"]
                }
            ],
            "education": [
                {
                    "degree": "Master of Science in Data Science",
                    "institution": "George Washington University",
                    "location": "Washington DC, USA",
                    "duration": "Graduated May 2025",
                    "relevant_courses": ["Machine Learning", "Statistical Methods", "Data Mining", "Big Data Analytics", "Business Intelligence"]
                },
                {
                    "degree": "Bachelor of Technology in Computer Science",
                    "institution": "MVJ College of Engineering",
                    "location": "Bangalore, India",
                    "duration": "Graduated May 2022",
                    "relevant_courses": ["Database Management Systems", "Data Structures", "Algorithms", "Software Engineering"]
                }
            ],
            "certifications": [
                {
                    "name": "Salesforce Certified: Tableau Desktop Foundations",
                    "issuer": "Salesforce",
                    "year": "2024",
                    "credential_id": "TDF-2024-001"
                },
                {
                    "name": "AWS Certified Cloud Practitioner",
                    "issuer": "Amazon Web Services",
                    "year": "2023",
                    "credential_id": "AWS-CCP-2023-001"
                }
            ]
        }
        
        # Create profile
        success = await db_manager.create_or_update_profile(profile_data)
        if not success:
            logger.error("Failed to create profile during seeding")
            return
            
        # Projects data
        projects_data = [
            {
                "title": "Claims360 Analytics Platform",
                "company": "Liberty Mutual Insurance",
                "type": "Professional Project",
                "description": "End-to-end analytics platform for claims intelligence, fraud detection, and process automation",
                "impact": [
                    "22% improvement in fraud detection efficiency",
                    "33% reduction in claims settlement cycle time",
                    "40% increase in insights visibility for stakeholders"
                ],
                "technologies": ["AWS (S3, Glue, Redshift, SageMaker)", "Python", "Power BI", "SQL"],
                "details": "Designed and implemented comprehensive analytics solution including automated ETL pipelines, predictive fraud detection models, and real-time interactive dashboards for claims performance monitoring.",
                "featured": True,
                "display_order": 1
            },
            {
                "title": "Unified Claims & Credit Risk Analytics",
                "company": "Hexaware Technologies",
                "type": "Professional Project",
                "description": "Centralized Azure-based analytics platform for financial services client",
                "impact": [
                    "23% improvement in loan risk assessment accuracy",
                    "Automated IRDA and RBI regulatory compliance reporting",
                    "Streamlined credit risk evaluation processes"
                ],
                "technologies": ["Azure (Data Factory, Synapse Analytics, ML Studio)", "Python", "Power BI", "Tableau"],
                "details": "Built integrated analytics solution with automated data pipelines, predictive risk scoring models, and comprehensive regulatory reporting capabilities.",
                "featured": True,
                "display_order": 2
            },
            {
                "title": "Customer Churn Prediction Model",
                "company": "George Washington University",
                "type": "Academic Project",
                "description": "Machine learning model to predict customer churn for subscription-based business",
                "impact": [
                    "Achieved 85% accuracy in churn prediction",
                    "Identified top 5 factors contributing to customer churn",
                    "Developed actionable retention strategies"
                ],
                "technologies": ["Python", "Scikit-learn", "Pandas", "Matplotlib", "Jupyter"],
                "details": "Developed end-to-end ML pipeline including data preprocessing, feature engineering, model selection, and performance evaluation using various algorithms including Random Forest and Logistic Regression.",
                "featured": True,
                "display_order": 3
            },
            {
                "title": "Healthcare Analytics Dashboard",
                "company": "George Washington University",
                "type": "Academic Project",
                "description": "Interactive dashboard analyzing healthcare utilization patterns and patient outcomes",
                "impact": [
                    "Visualized trends across 50,000+ patient records",
                    "Identified cost optimization opportunities",
                    "Created predictive models for patient readmission risk"
                ],
                "technologies": ["Tableau", "Python", "SQL", "Statistical Analysis"],
                "details": "Comprehensive analysis of healthcare data including patient demographics, treatment patterns, and outcome metrics with interactive visualizations for healthcare administrators.",
                "featured": True,
                "display_order": 4
            }
        ]
        
        # Create projects
        for project_data in projects_data:
            project_id = await db_manager.create_project(project_data)
            if not project_id:
                logger.error(f"Failed to create project: {project_data['title']}")
                
        # Visualizations data
        visualizations_data = [
            {
                "title": "Claims Performance Dashboard",
                "description": "Interactive Power BI dashboard showing claims processing metrics and KPIs",
                "metrics": ["Average Settlement Time: 12 days", "Fraud Detection Rate: 94%", "Customer Satisfaction: 4.2/5"],
                "chart_type": "Multi-metric Dashboard",
                "chart_data": {
                    "claims_processed": 892,
                    "fraud_detected": 94,
                    "avg_settlement": 12,
                    "customer_satisfaction": 4.2
                },
                "is_active": True,
                "display_order": 1
            },
            {
                "title": "Risk Score Distribution Analysis",
                "description": "Statistical analysis of risk scoring model performance across different customer segments",
                "metrics": ["Model Accuracy: 89%", "Precision: 87%", "Recall: 91%"],
                "chart_type": "Performance Metrics",
                "chart_data": {
                    "accuracy": 89,
                    "precision": 87,
                    "recall": 91,
                    "risk_distribution": {"low": 65, "medium": 28, "high": 7}
                },
                "is_active": True,
                "display_order": 2
            },
            {
                "title": "Customer Churn Prediction Analysis",
                "description": "Machine learning model results showing feature importance and prediction accuracy",
                "metrics": ["Churn Prediction Accuracy: 85%", "Top Risk Factor: Usage Decline", "Monthly Savings: $50K"],
                "chart_type": "ML Model Results",
                "chart_data": {
                    "churn_rate": 15.2,
                    "monthly_savings": 48000,
                    "top_factors": ["Usage Decline", "Support Tickets", "Payment Delays", "Feature Adoption", "Login Frequency"]
                },
                "is_active": True,
                "display_order": 3
            }
        ]
        
        # Create visualizations
        for viz_data in visualizations_data:
            viz_id = await db_manager.create_visualization(viz_data)
            if not viz_id:
                logger.error(f"Failed to create visualization: {viz_data['title']}")
                
        logger.info("Successfully seeded initial portfolio data")
        
    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
        raise
# 🚀 Deployment Guide - Keerthana's Portfolio

This guide will help you deploy your portfolio to production with frontend on Vercel and backend on Railway.

## 📋 Prerequisites

1. **GitHub Account** - For code repository
2. **Vercel Account** - For frontend deployment (free tier available)
3. **Railway Account** - For backend deployment (free tier available)  
4. **MongoDB Atlas Account** - For production database (free tier available)

## 🗂️ Step 1: GitHub Repository Setup

### 1.1 Create GitHub Repository
```bash
# Initialize git in your project
cd /app
git init
git add .
git commit -m "Initial commit: Professional Portfolio"

# Create repository on GitHub (replace with your username)
gh repo create keerthana-portfolio --public --source=. --push
# Or manually create at: https://github.com/new
```

### 1.2 Push to GitHub
```bash
git remote add origin https://github.com/yourusername/keerthana-portfolio.git
git branch -M main
git push -u origin main
```

## 🎯 Step 2: Backend Deployment (Railway)

### 2.1 Deploy to Railway
1. Visit [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your portfolio repository
5. Railway will auto-detect the Python backend

### 2.2 Configure Environment Variables
In Railway dashboard:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=portfolio_prod
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### 2.3 Backend URL
After deployment, Railway provides a URL like: `https://your-app-production.up.railway.app`

## 🌐 Step 3: Frontend Deployment (Vercel)

### 3.1 Deploy to Vercel
1. Visit [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project" → Import your repository
4. Select `frontend` folder as root directory
5. Configure build settings:
   - **Build Command**: `yarn build`
   - **Output Directory**: `build`
   - **Install Command**: `yarn install`

### 3.2 Configure Environment Variables
In Vercel dashboard → Settings → Environment Variables:
```
REACT_APP_BACKEND_URL=https://your-railway-backend.up.railway.app
```

### 3.3 Custom Domain (Optional)
- Add your custom domain in Vercel dashboard
- Update DNS settings as instructed

## 🗄️ Step 4: MongoDB Atlas Setup

### 4.1 Create Cluster
1. Visit [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for simplicity)

### 4.2 Get Connection String
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/portfolio_prod
```

## ✅ Step 5: Verification Checklist

### 5.1 Backend Verification
- [ ] Railway deployment successful
- [ ] Environment variables configured
- [ ] API endpoints accessible: `https://your-backend.railway.app/docs`
- [ ] Database connection working

### 5.2 Frontend Verification  
- [ ] Vercel deployment successful
- [ ] Environment variables configured
- [ ] Portfolio loads correctly
- [ ] Contact form works
- [ ] All sections display properly

### 5.3 Integration Testing
- [ ] Frontend connects to backend
- [ ] Profile data loads from database
- [ ] Contact form submissions work
- [ ] Analytics tracking functional
- [ ] Resume download works

## 🔧 Troubleshooting

### Common Issues

**Backend Issues:**
```bash
# Check Railway logs
railway logs

# Common fixes:
- Verify MONGO_URL format
- Check CORS_ORIGINS includes frontend domain
- Ensure PORT environment variable is used
```

**Frontend Issues:**
```bash
# Check Vercel function logs
# Common fixes:
- Verify REACT_APP_BACKEND_URL points to Railway
- Check build output for errors
- Ensure API endpoints return CORS headers
```

**Database Issues:**
```bash
# MongoDB Atlas checklist:
- Network access (IP whitelist)
- Database user permissions
- Connection string format
- Database name matches backend
```

## 🎉 Step 6: Going Live

### 6.1 Update URLs
1. Update README.md with live URLs
2. Add live demo links to GitHub repository
3. Update LinkedIn/resume with portfolio URL

### 6.2 Performance Optimization
```bash
# Frontend optimizations
- Enable Vercel Analytics
- Configure caching headers
- Optimize images and assets

# Backend optimizations  
- Enable Railway metrics
- Configure database indexing
- Implement API rate limiting
```

## 📈 Monitoring & Maintenance

### Analytics Setup
- **Vercel Analytics**: Built-in traffic monitoring
- **Railway Metrics**: Backend performance monitoring  
- **MongoDB Charts**: Database usage visualization

### Regular Updates
- Keep dependencies updated
- Monitor performance metrics
- Backup database regularly
- Review and update content

## 🔗 Quick Links

- **Live Portfolio**: https://your-domain.vercel.app
- **API Documentation**: https://your-backend.railway.app/docs
- **GitHub Repository**: https://github.com/yourusername/keerthana-portfolio
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Railway Dashboard**: https://railway.app/dashboard
- **MongoDB Atlas**: https://cloud.mongodb.com

---

## 💡 Next Steps

1. **Custom Domain**: Purchase and configure custom domain
2. **SSL Certificate**: Ensure HTTPS is enabled (automatic with Vercel/Railway)
3. **SEO Optimization**: Add meta tags, sitemap, robots.txt
4. **Performance Monitoring**: Set up alerts and monitoring
5. **Continuous Deployment**: Automatic deployments on git push

**Need Help?** 
- Vercel Documentation: https://vercel.com/docs
- Railway Documentation: https://docs.railway.app
- MongoDB Atlas Documentation: https://docs.atlas.mongodb.com

---

**Deployment Status**: ✅ Ready for Production

Your portfolio is now ready to showcase your professional experience to potential employers!
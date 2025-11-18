# 🚀 Quick Start Guide - PhD Application Automator

## ✅ Current Status

**The application is COMPLETE and READY TO USE!**

- ✅ Backend API running on http://localhost:5000
- ✅ Database initialized with 8 tables
- ✅ Sample data loaded (10 universities, multiple professors)
- ✅ Test user created (john@example.com / password123)
- ✅ All code committed and pushed to GitHub
- ✅ Gemini AI connected and working

---

## 🎯 What You Have

### Complete Full-Stack Application:
1. **Backend** - Flask REST API with 20+ endpoints
2. **Frontend** - React app with 9 beautiful pages
3. **Database** - SQLite with complete schema
4. **AI Integration** - Google Gemini for email generation
5. **Authentication** - JWT-based secure login
6. **Tests** - Comprehensive test suite
7. **Scripts** - One-command setup and start

---

## 🏃 How to Run the Application

### Option 1: One-Command Start (Recommended)

```bash
# From the project root directory
./scripts/start.sh
```

This will:
- Start the Flask backend on port 5000
- Start the React frontend on port 3000
- Open the app in your browser

### Option 2: Manual Start

**Backend:**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install  # First time only
npm start
```

---

## 🌐 Access Points

Once running:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **API Docs**: http://localhost:5000/ (lists all endpoints)

---

## 👤 Test Account

Use this to login and test:

- **Email**: john@example.com
- **Password**: password123

---

## 📱 Using the Application

### 1. Register/Login
- Go to http://localhost:3000
- Login with test account or register a new one

### 2. Set Your Profile
- Click "Profile" in the navigation
- Add your research interests (e.g., "Machine Learning, Aerospace, Manufacturing")
- Add target countries (e.g., "USA, UK, Germany, China")
- Save changes

### 3. Discover Universities
- Go to "Universities" page
- Click "🔍 Discover Universities"
- Browse the 10 sample universities (MIT, Stanford, Cambridge, etc.)
- Filter by country or scholarship availability

### 4. Find Professors
- Go to "Professors" page
- Click "🔍 Discover Professors"
- View professors with their research interests
- See match scores based on your profile

### 5. Generate Emails (AI-Powered)
- Create applications for professors
- Use AI to generate personalized emails
- Review and edit the generated content
- Send emails to professors

### 6. Track Applications
- Go to "Applications" page
- Monitor status (draft → sent → opened → replied)
- Add notes and follow-ups
- Track your progress

### 7. View Analytics
- Go to "Analytics" page
- See success rates
- View applications by country
- Monitor email statistics

---

## 🔧 Configuration

### Backend Configuration (backend/.env)

Already set up with:
- ✅ Database path
- ✅ Gemini AI API key
- ✅ JWT secret keys
- ✅ SMTP settings (configure for real email sending)

### Frontend Configuration (frontend/.env)

Already set up with:
- ✅ API URL pointing to localhost:5000

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

---

## 📊 Sample Data Included

### 10 Top Universities (All with Funding):
1. MIT (USA)
2. Stanford University (USA)
3. University of Cambridge (UK)
4. ETH Zurich (Switzerland)
5. Tsinghua University (China)
6. National University of Singapore
7. Technical University of Munich (Germany)
8. University of Toronto (Canada)
9. Australian National University
10. Delft University of Technology (Netherlands)

### Professor Profiles:
- Sample professors for each university
- Complete with emails, research interests, H-index
- Ready for email generation

---

## 🎓 Key Features to Try

1. **AI Email Generation**
   - Personalized emails based on professor's research
   - Mentions shared research interests
   - Professional tone and format

2. **Research Matching**
   - Automatic match score calculation
   - Based on your research interests
   - Helps prioritize professors

3. **Batch Email Management**
   - Generate multiple emails at once
   - Review and approve before sending
   - Track sending status

4. **Application Tracking**
   - Complete application lifecycle
   - Status updates
   - Notes and reminders

5. **Analytics Dashboard**
   - Visual statistics
   - Success rate tracking
   - Country distribution

---

## 🐛 Troubleshooting

### Backend won't start?
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend won't start?
```bash
cd frontend
npm install
npm start
```

### Database issues?
```bash
cd backend
source venv/bin/activate
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Port already in use?
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

---

## 📚 API Documentation

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- POST `/api/auth/logout` - Logout user

### Universities
- GET `/api/universities/search` - Search universities
- POST `/api/universities/discover` - Discover new universities
- GET `/api/universities/:id` - Get university details

### Professors
- GET `/api/professors/search` - Search professors
- POST `/api/professors/discover` - Discover professors
- GET `/api/professors/:id` - Get professor details

### Applications
- GET `/api/applications/` - Get all applications
- POST `/api/applications/` - Create application
- PUT `/api/applications/:id` - Update application

### Emails
- POST `/api/emails/generate` - Generate AI emails
- GET `/api/emails/` - Get emails
- POST `/api/emails/send` - Send emails

### Analytics
- GET `/api/analytics/dashboard` - Get dashboard stats
- GET `/api/analytics/by-country` - Get country stats

---

## 🚀 Next Steps

1. ✅ **Run the application** - `./scripts/start.sh`
2. ✅ **Login** - Use test account or register
3. ✅ **Set profile** - Add research interests
4. ✅ **Discover** - Find universities and professors
5. ✅ **Generate emails** - Use AI to create personalized emails
6. ✅ **Track applications** - Monitor your progress
7. 📝 **Deploy** - When ready, deploy to Vercel + Render.com

---

## 🌍 Production Deployment

### Frontend (Vercel - Free)
1. Push code to GitHub ✅ (Already done!)
2. Connect repository to Vercel
3. Deploy with one click
4. Get free HTTPS domain

### Backend (Render.com - Free)
1. Connect GitHub repository
2. Select "Web Service"
3. Set environment variables
4. Deploy automatically

### Database (ElephantSQL - Free)
1. Create free PostgreSQL instance
2. Update DATABASE_URL in backend/.env
3. Run migrations

---

## 💡 Tips

1. **Customize Email Templates**: Edit `backend/services/ai/email_generator.py`
2. **Add More Universities**: Modify `backend/services/scraper/university_scraper.py`
3. **Adjust Match Algorithm**: Edit `backend/services/ai/matching_engine.py`
4. **Change UI Colors**: Update `frontend/tailwind.config.js`
5. **Add New Features**: Follow the existing code patterns

---

## 📞 Support

If you encounter issues:
1. Check backend logs: `backend/logs/app.log`
2. Check console for errors
3. Review this guide
4. Check the comprehensive README.md
5. Review PROJECT_SUMMARY.md for detailed info

---

## 🎉 You're All Set!

Your PhD Application Automator is ready to help you apply to PhD programs worldwide!

**Start now**: `./scripts/start.sh`

Good luck with your PhD applications! 🎓🚀

---

**Last Updated**: 2025-11-18
**Version**: 1.0.0
**Status**: Production Ready ✅

# Quick Deployment Reference

## Your Database Credentials

```
Host: dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com
Database: earthlens
User: earthlens_user
Password: WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw

Connection String:
postgresql://earthlens_user:WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw@dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com/earthlens
```

## Quick Deploy Commands

### Backend (Render)

```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy backend"
git push origin main

# 2. After Render deployment, initialize database
# Use Render Shell or connect via psql:
PGPASSWORD=WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw psql -h dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com -U earthlens_user earthlens

# Then run:
flask db upgrade
python seed.py  # Optional: seed initial data
```

### Frontend (Vercel)

```bash
# 1. Create .env.production in Client folder
cd Client
echo "VITE_API_URL=https://your-backend.onrender.com/api" > .env.production

# 2. Deploy to Vercel
npm install -g vercel
vercel login
vercel --prod

# Or push to GitHub and deploy via Vercel dashboard
```

## Environment Variables to Set

### Render (Backend)
```env
FLASK_ENV=production
SECRET_KEY=<generate-random-string>
JWT_SECRET_KEY=<generate-random-string>
DATABASE_URL=postgresql://earthlens_user:WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw@dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com/earthlens
GROQ_API_KEY=<your-groq-api-key>
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=500
FRONTEND_URL=https://your-app.vercel.app
```

### Vercel (Frontend)
```env
VITE_API_URL=https://your-backend.onrender.com/api
```

## Generate Secret Keys

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use online generator
# https://randomkeygen.com/
```

## Test Deployment

```bash
# Test backend health
curl https://your-backend.onrender.com/api/health

# Expected response:
# {"status":"healthy","message":"EarthLens API is running","version":"1.0.0","environment":"production"}

# Test frontend
# Open https://your-app.vercel.app in browser
# Check browser console for errors
```

## Troubleshooting Quick Fixes

### CORS Error
```bash
# Update FRONTEND_URL in Render to match Vercel URL exactly
# Format: https://your-app.vercel.app (no trailing slash)
```

### Database Connection Error
```bash
# Test connection
PGPASSWORD=WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw psql -h dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com -U earthlens_user earthlens -c "SELECT version();"
```

### Build Error
```bash
# Backend - Check Render logs
# Frontend - Check Vercel logs

# Common fix: Clear cache and rebuild
# Render: Manual Deploy → Clear build cache
# Vercel: Redeploy with "Clear Cache"
```

## Important Links

- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Groq Console**: https://console.groq.com
- **GitHub Repository**: [Your repo URL]

## Post-Deployment Checklist

- [ ] Backend health endpoint returns 200
- [ ] Frontend loads without errors
- [ ] User can register/login
- [ ] CORS working (no errors in console)
- [ ] Database queries working
- [ ] AI features working
- [ ] Images uploading correctly

## Deployment Status

- **Backend URL**: _____________________
- **Frontend URL**: _____________________
- **Deployment Date**: _____________________
- **Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Completed

---

**Need Help?** Check DEPLOYMENT.md for detailed instructions.

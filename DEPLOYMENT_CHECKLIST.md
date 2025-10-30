# EarthLens Deployment Checklist

## Pre-Deployment Checklist

### Backend Preparation
- [x] Updated to use Groq API instead of OpenAI
- [x] CORS configuration uses environment-based origins
- [x] Database connection string configured for PostgreSQL
- [x] Environment variables documented in `.env.example`
- [x] Gunicorn configured in `render.yaml`
- [x] Health check endpoint available at `/api/health`
- [ ] Get Groq API key from https://console.groq.com
- [ ] Test all API endpoints locally
- [ ] Run database migrations: `flask db upgrade`

### Frontend Preparation
- [x] API URL uses environment variable (`VITE_API_URL`)
- [x] `.env.example` created with configuration template
- [x] Axios configured with `withCredentials: true`
- [ ] Test build locally: `npm run build`
- [ ] Verify all API calls work with production backend URL
- [ ] Check for hardcoded localhost URLs in components

### Security
- [ ] Generate strong `SECRET_KEY` for Flask
- [ ] Generate strong `JWT_SECRET_KEY`
- [ ] Verify no sensitive data in git history
- [ ] Ensure `.env` files are in `.gitignore`
- [ ] Review CORS origins (no wildcards in production)

---

## Deployment Steps

### Step 1: Deploy Backend to Render

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to https://render.com/dashboard
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Select `server` as root directory
   - Use Python 3 runtime

3. **Configure Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-strong-key>
   JWT_SECRET_KEY=<generate-strong-key>
   DATABASE_URL=postgresql://earthlens_user:WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw@dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com/earthlens
   GROQ_API_KEY=<your-groq-api-key>
   GROQ_MODEL=llama-3.1-70b-versatile
   GROQ_TEMPERATURE=0.7
   GROQ_MAX_TOKENS=500
   FRONTEND_URL=<will-update-after-frontend-deployment>
   ```

4. **Deploy and verify**
   - Wait for build to complete
   - Visit `https://your-app.onrender.com/api/health`
   - Should return `{"status": "healthy"}`

5. **Initialize Database**
   - Use Render Shell or connect via psql
   ```bash
   flask db upgrade
   python seed.py  # Optional
   ```

### Step 2: Deploy Frontend to Vercel

1. **Create `.env.production` in Client folder**
   ```env
   VITE_API_URL=https://your-backend.onrender.com/api
   ```

2. **Deploy to Vercel**
   - Go to https://vercel.com/dashboard
   - Click "Add New" → "Project"
   - Import GitHub repository
   - Set root directory to `Client`
   - Add environment variable: `VITE_API_URL`

3. **Verify deployment**
   - Visit your Vercel URL
   - Open browser console (F12)
   - Check for errors
   - Test login/signup functionality

### Step 3: Update CORS Configuration

1. **Get your Vercel URL** (e.g., `https://earthlens.vercel.app`)

2. **Update Backend Environment Variable**
   - Go to Render Dashboard
   - Select your web service
   - Environment → Edit
   - Update `FRONTEND_URL` to your Vercel URL
   - Save and redeploy

3. **Test CORS**
   - Open frontend in browser
   - Open DevTools → Network tab
   - Make an API request
   - Check response headers for `Access-Control-Allow-Origin`

---

## Post-Deployment Verification

### Backend Tests
- [ ] Health endpoint: `GET /api/health` returns 200
- [ ] User registration: `POST /api/auth/register` works
- [ ] User login: `POST /api/auth/login` returns token
- [ ] Protected routes require authentication
- [ ] AI endpoints respond correctly
- [ ] Database queries execute successfully
- [ ] File uploads work (if applicable)

### Frontend Tests
- [ ] Homepage loads correctly
- [ ] User can register new account
- [ ] User can login
- [ ] User can create reports
- [ ] Images upload successfully
- [ ] AI analysis works
- [ ] Navigation works across all pages
- [ ] Logout functionality works
- [ ] No console errors

### Integration Tests
- [ ] Frontend can communicate with backend
- [ ] CORS headers present in all API responses
- [ ] Authentication tokens persist across page refreshes
- [ ] API errors display properly in frontend
- [ ] Loading states work correctly

---

## Monitoring Setup

### Backend Monitoring
- [ ] Check Render logs for errors
- [ ] Monitor response times
- [ ] Track Groq API usage
- [ ] Monitor database connections
- [ ] Set up error alerting (optional)

### Frontend Monitoring
- [ ] Check Vercel deployment logs
- [ ] Monitor build times
- [ ] Check for runtime errors in Vercel dashboard
- [ ] Test on different browsers/devices

---

## Rollback Plan

### If Backend Deployment Fails
1. Check Render logs for error messages
2. Verify all environment variables are set
3. Test database connection
4. Rollback to previous deployment in Render dashboard

### If Frontend Deployment Fails
1. Check Vercel build logs
2. Verify environment variables
3. Test build locally: `npm run build`
4. Rollback to previous deployment in Vercel dashboard

---

## Common Issues & Solutions

### Issue: CORS Error
**Symptoms**: Browser console shows CORS policy error

**Solutions**:
1. Verify `FRONTEND_URL` matches Vercel URL exactly (including https://)
2. Check CORS configuration in `app/__init__.py`
3. Ensure `withCredentials: true` in axios config
4. Clear browser cache and try again

### Issue: 502 Bad Gateway
**Symptoms**: Backend returns 502 error

**Solutions**:
1. Check Render logs for application errors
2. Verify gunicorn is starting correctly
3. Check database connection string
4. Ensure all dependencies installed correctly

### Issue: Database Connection Failed
**Symptoms**: Backend can't connect to PostgreSQL

**Solutions**:
1. Verify `DATABASE_URL` format is correct
2. Check database is running in Render dashboard
3. Test connection with psql:
   ```bash
   psql postgresql://earthlens_user:WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw@dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com/earthlens
   ```

### Issue: Environment Variables Not Loading
**Symptoms**: App uses default values instead of env vars

**Solutions**:
1. Verify variables are set in Render/Vercel dashboard
2. Check variable names match exactly (case-sensitive)
3. Redeploy after adding variables
4. Check for typos in variable names

### Issue: Build Fails
**Symptoms**: Deployment build fails

**Backend Solutions**:
- Check `requirements.txt` for version conflicts
- Verify Python version compatibility
- Check for missing dependencies

**Frontend Solutions**:
- Check `package.json` for dependency issues
- Clear node_modules and reinstall
- Verify build command is correct
- Check for TypeScript/ESLint errors

---

## Performance Optimization

### After Successful Deployment

1. **Enable Caching**
   - Add caching headers for static assets
   - Consider Redis for session storage

2. **Database Optimization**
   - Add indexes for frequently queried fields
   - Monitor slow queries
   - Consider connection pooling

3. **API Optimization**
   - Implement rate limiting
   - Add request/response compression
   - Optimize database queries

4. **Frontend Optimization**
   - Enable code splitting
   - Optimize images
   - Use lazy loading for routes
   - Minimize bundle size

---

## Maintenance Schedule

### Daily
- [ ] Check error logs
- [ ] Monitor API response times
- [ ] Verify critical functionality

### Weekly
- [ ] Review Groq API usage
- [ ] Check database storage
- [ ] Review security logs
- [ ] Test backup restoration

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize database
- [ ] Audit security settings
- [ ] Review and update documentation

---

## Emergency Contacts & Resources

- **Render Status**: https://status.render.com
- **Vercel Status**: https://www.vercel-status.com
- **Groq Support**: https://console.groq.com/docs
- **Database Backup Location**: Render Dashboard → Database → Backups

---

## Success Criteria

Deployment is successful when:
- ✅ Backend health endpoint returns 200
- ✅ Frontend loads without errors
- ✅ Users can register and login
- ✅ CORS is properly configured
- ✅ Database connections work
- ✅ AI features function correctly
- ✅ All API endpoints respond correctly
- ✅ No console errors in production
- ✅ SSL/HTTPS working on both frontend and backend

---

**Deployment Date**: _____________

**Deployed By**: _____________

**Backend URL**: _____________

**Frontend URL**: _____________

**Notes**: 
_____________________________________________
_____________________________________________
_____________________________________________

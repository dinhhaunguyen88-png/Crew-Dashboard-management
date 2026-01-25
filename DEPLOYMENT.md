# Deployment Guide - Crew Dashboard

## 🚀 Deployment Options

You have **3 deployment options** depending on your needs:

---

## Option 1: Static Deployment (Cloudflare Pages) - Current

**Best for:** Production deployment without server costs

**Features Available:**
- ✅ All dashboard visualizations
- ✅ Manual CSV upload via web interface
- ✅ Date filtering
- ❌ Auto-refresh on file changes (needs server)
- ❌ Real-time notifications (needs server)
- ❌ File watcher (needs local server)

**How to Deploy:**

```powershell
# Run the existing script
.\update.ps1
```

This will:
1. Process all CSV files locally
2. Generate `deploy_static/dashboard_data.json`
3. Deploy to Cloudflare Pages
4. URL: https://crew-dashboard.pages.dev

**When to update:**
- Run `update.ps1` whenever CSV data changes
- Manual process, but simple and free

---

## Option 2: Full Server Deployment (Recommended for New Features)

**Best for:** Using ALL new features including auto-refresh

**Features Available:**
- ✅ All dashboard visualizations
- ✅ Manual CSV upload
- ✅ **Auto-refresh on file changes** ⭐
- ✅ **Real-time notifications** ⭐
- ✅ **File watcher monitoring** ⭐
- ✅ Supabase integration

**Deployment Platforms:**

### A. Render.com (Easiest)

1. **Create account:** https://render.com

2. **Create New Web Service:**
   - Connect your GitHub repository
   - OR use "Deploy with Render" button

3. **Settings:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn api_server:app
   ```

4. **Environment Variables:**
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   AIMS_ENABLED=false
   ```

5. **Deploy!**
   - URL: https://crew-dashboard.onrender.com
   - Free tier: Spins down after 15 min of inactivity
   - Paid tier: Always on ($7/month)

### B. Railway.app

1. **Create account:** https://railway.app

2. **New Project → Deploy from GitHub**

3. **Settings:**
   ```
   Start Command: python api_server.py
   ```

4. **Add Environment Variables** (same as Render)

5. **Deploy!**
   - Free tier: $5 credit/month
   - Very fast deployments

### C. Heroku

1. **Create account:** https://heroku.com

2. **Create new app**

3. **Install Heroku CLI and deploy:**
   ```bash
   heroku login
   heroku create crew-dashboard
   git push heroku main
   ```

4. **Your `Procfile` is already configured:**
   ```
   web: gunicorn api_server:app
   ```

---

## Option 3: Hybrid Approach

**Best for:** Combining static deployment + local development

**Setup:**

1. **Production (Cloudflare):** Static deployment for public access
   ```powershell
   .\update.ps1
   ```

2. **Development (Local):** Full server with all features
   ```bash
   python api_server.py
   ```

**Workflow:**
- Develop and test locally with auto-refresh
- Use `update.ps1` to publish to production
- Public users see static version
- You work with full-featured local version

---

## 📊 Comparison Table

| Feature | Cloudflare Static | Server Deployment | Hybrid |
|---------|------------------|-------------------|--------|
| Cost | Free | $0-7/month | Free |
| Auto-refresh | ❌ | ✅ | Local only |
| File watcher | ❌ | ✅ | Local only |
| Real-time updates | ❌ | ✅ | Local only |
| CSV upload | ✅ | ✅ | ✅ |
| Always online | ✅ | ✅ paid | ✅ static |
| Setup difficulty | Easy | Medium | Easy |

---

## 🎯 My Recommendation

**For Development/Testing:**
→ **Run locally** with `python api_server.py` to enjoy all new features

**For Production:**
→ **Deploy to Render.com** (free tier) if you want auto-refresh in production
→ **OR use Cloudflare** (existing setup) for simple static deployment

---

## 🚀 Quick Deploy to Render.com

Since you already have a working Flask app, here's the fastest path:

### Step 1: Create `render.yaml` (I'll create this for you)

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Add auto-refresh and drag-drop features"
git push origin main
```

### Step 3: Connect to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Select your repository
5. Click "Apply"

Render will automatically:
- Read `render.yaml`
- Install dependencies
- Start your server
- Give you a URL

**Done!** 🎉

---

## 📝 Notes

**File Watcher on Cloud:**
- Cloudflare Pages: Static only, no file watcher
- Render/Railway/Heroku: ⚠️ File system is ephemeral
  - Files uploaded via web interface work fine
  - Direct file editing on server won't persist
  - **Recommendation:** Use Supabase for data storage (already integrated!)

**Best Practice:**
- Upload CSV files via web interface
- Data sync to Supabase automatically
- Auto-refresh notifies all connected clients
- Works perfectly on cloud deployments!

---

## 🤔 Which Should You Choose?

**Choose Cloudflare (update.ps1) if:**
- You want free hosting
- Don't need real-time auto-refresh
- Happy to run update script when data changes

**Choose Render/Railway if:**
- You want the full auto-refresh experience
- Need real-time notifications
- Want CSV upload via web interface
- Willing to pay $0-7/month OR use free tier

**Choose Hybrid if:**
- You develop locally often
- Production users can use static version
- Want best of both worlds

---

## Need Help?

Let me know which option you prefer and I can:
1. Create the deployment config files
2. Guide you through the process
3. Help troubleshoot any issues

# 🚀 Render.com Deployment Guide - Step by Step

## ✅ Prerequisites Complete
- ✅ `render.yaml` created
- ✅ `requirements.txt` updated with watchdog
- ✅ Flask app ready (`api_server.py`)
- ✅ Local testing successful

---

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your GitHub Repository

**If you haven't pushed to GitHub yet:**

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Add auto-refresh, drag-drop, and real-time features"

# Create repository on GitHub (go to github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/crew-dashboard.git
git branch -M main
git push -u origin main
```

**If you already have a GitHub repo:**

```bash
# Just push the latest changes
git add .
git commit -m "Add Render.com deployment with auto-refresh features"
git push origin main
```

---

### Step 2: Sign Up for Render.com

1. Go to https://render.com
2. Click **Get Started for Free**
3. Sign up with GitHub (recommended) or email
4. Authorize Render to access your GitHub repositories

---

### Step 3: Create New Web Service

1. **Click "New +"** in the top right
2. Select **"Web Service"**
3. **Connect your GitHub repository:**
   - If using Blueprint: Select "Blueprint" and choose your repo
   - If manual: Select "Web Service" and choose your repo

4. **Configure the service:**

```
Name: crew-dashboard
Region: Singapore (closest to Vietnam)
Branch: main
Root Directory: (leave empty)

Build Command: pip install -r requirements.txt
Start Command: gunicorn api_server:app --bind 0.0.0.0:$PORT
```

5. **Select Plan:**
   - Choose **"Free"** (first option)
   - ⚠️ Note: Free tier spins down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds

---

### Step 4: Add Environment Variables

**IMPORTANT:** Add these before deploying!

In the Render dashboard, scroll to **"Environment Variables"** section:

```
SUPABASE_URL = https://lohfgbeyxmnjlomoqhse.supabase.co
SUPABASE_KEY = [your API key from .env file]
AIMS_ENABLED = false
PYTHON_VERSION = 3.12
```

**To get your Supabase credentials:**
- Check your `.env` file
- Or get from: https://supabase.com/dashboard/project/YOUR_PROJECT/settings/api

---

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Watch the logs for:
   ```
   ✅ File watcher started - monitoring...
   ✅ Auto-reload enabled
   ```

4. Your URL will be: `https://crew-dashboard.onrender.com`

---

## ✨ After Deployment

### Test Your New Features:

1. **Open your Render URL**
2. **Test CSV Upload:**
   - Click "📂 Upload CSV"
   - Drag & drop a CSV file
   - See real-time upload feedback

3. **Test Auto-Refresh:**
   - Upload a new CSV file
   - Watch for green notification
   - Page auto-refreshes!

---

## 🔧 Troubleshooting

### Issue: "Application failed to respond"
**Solution:** Make sure start command includes `--bind 0.0.0.0:$PORT`
```bash
gunicorn api_server:app --bind 0.0.0.0:$PORT
```

### Issue: "Module not found: watchdog"
**Solution:** Check `requirements.txt` includes `watchdog>=3.0.0`

### Issue: "Supabase connection failed"
**Solution:** 
1. Verify environment variables are set
2. Check SUPABASE_URL and SUPABASE_KEY are correct
3. View logs in Render dashboard

### Issue: "Site is slow to respond"
**Solution:** This is normal on free tier after 15 min inactivity
- First request wakes up the service (30-60 sec)
- Subsequent requests are fast
- Upgrade to paid tier ($7/mo) for always-on

---

## 🎯 What Works on Render (vs Cloudflare)

| Feature | Cloudflare | Render.com |
|---------|-----------|------------|
| Static Dashboard | ✅ | ✅ |
| CSV Upload | ✅ | ✅ |
| **Auto-Refresh** | ❌ | ✅ ⭐ |
| **File Watcher** | ❌ | ✅ ⭐ |
| **Real-time Notifications** | ❌ | ✅ ⭐ |
| Supabase Sync | Via Script | ✅ Live |
| Cost | Free | Free |
| Always On | ✅ | Paid only |

---

## 💡 Pro Tips

1. **Keep Both Deployments:**
   - Cloudflare: Fast, always-on static version
   - Render: Full features for development/testing

2. **Monitor Your Service:**
   - Render Dashboard → Logs
   - Watch for auto-refresh messages
   - Check error logs if issues

3. **Upgrade When Ready:**
   - $7/month for always-on
   - No spin-down delay
   - Better for production

4. **File Uploads:**
   - Files uploaded via web interface work perfectly
   - Data syncs to Supabase automatically
   - Survives service restarts

---

## 📊 Cost Breakdown

**Free Tier:**
- 750 hours/month
- Spins down after 15 min inactivity
- Perfect for testing/development

**Starter Tier ($7/month):**
- Always on
- No spin-down
- Better for production use

---

## 🤔 Need Help?

If you get stuck:
1. Check the Render logs (Dashboard → Logs tab)
2. Verify environment variables are set
3. Make sure GitHub repo is up to date
4. Check that `render.yaml` is in the root directory

---

## ✅ Success Checklist

Before clicking Deploy:

- [ ] GitHub repo is up to date
- [ ] `render.yaml` is in root directory
- [ ] `requirements.txt` includes watchdog
- [ ] Environment variables added to Render
- [ ] Selected Free tier
- [ ] Start command: `gunicorn api_server:app --bind 0.0.0.0:$PORT`

**Ready? Let's deploy!** 🚀

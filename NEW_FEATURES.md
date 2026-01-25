# Crew Dashboard - New Features Guide

## 🎉 What's New

### 1. Automatic CSV File Monitoring ✨

The dashboard now automatically detects when CSV files change and refreshes the data in real-time!

**How it works:**
- File watcher monitors CSV files in the project directory
- When you save changes to any CSV file, the dashboard automatically processes it
- Browser receives a notification and refreshes to show updated data
- No more manual refresh needed!

**Setup:**
```bash
# Install the watchdog package
pip install watchdog>=3.0.0

# Run the server
python api_server.py
```

When you see:
```
✅ Auto-reload enabled - CSV changes will update dashboard
```
You're good to go! Just edit your CSV files and watch the magic happen.

---

### 2. Drag & Drop File Upload 🎯

Upload CSV files with a beautiful drag-and-drop interface!

**Features:**
- Drag CSV files directly onto the upload zone
- Automatic file type detection (DayRepReport, SacutilReport, etc.)
- Visual feedback with file size display
- Progress indicators
- Better error messages

**How to use:**
1. Click "📂 Upload CSV" button in the header
2. Either:
   - **Drag & drop** files onto the blue zone, OR
   - **Click** the zone to browse files
3. Files are automatically assigned to the correct field
4. Click "Upload & Refresh" to process

---

### 3. Real-Time Update Notifications 🔔

Get notified when data changes!

**How it works:**
- Dashboard polls server every 5 seconds  
- When CSV files change (via file upload OR direct file edit), you see a green notification
- Page automatically refreshes after 2 seconds
- Always see the latest data without manual refresh

---

## 📊 How to Update Dashboard Data

### Method 1: Direct File Edit (Recommended for Development)
1. Open any CSV file in Excel or text editor:
   - `DayRepReport15Jan2026.csv`
   - `SacutilReport1.csv`
   - `RolCrTotReport 28Feb26.csv`
   - `Crew schedule Feb2026.csv`

2. Make your changes

3. **Save the file**

4. Dashboard automatically detects the change and updates!
   - You'll see: `[Auto-Refresh] CSV file modified: filename.csv`
   - Browser shows green notification: "Data Updated!"
   - Page refreshes automatically

### Method 2: Upload via Web Interface
1. Click "📂 Upload CSV" button

2. Drag & drop or select files

3. Click "Upload & Refresh"

4. Done! Data is processed and synced to Supabase

### Method 3: PowerShell Script (For Production Deployment)
```powershell
.\update.ps1
```
This script:
- Processes all CSV files
- Updates dashboard_data.json
- Deploys to Cloudflare Pages

---

## 🎨 Enhanced Upload Experience

### File Detection
The system automatically recognizes files by name:
- Contains "dayrep" → DayRepReport
- Contains "sacutil" → SacutilReport  
- Contains "rolcr" → RolCrTotReport
- Contains "crew" and "schedule" → Crew Schedule

### Visual Feedback
- ✓ Shows file name and size when selected
- Green border when dragging files over drop zone
- Error messages if file is empty or invalid
- Success confirmation after upload

---

## 🔧 Technical Details

### File Watcher
- **Library:** watchdog 3.0.0+
- **Debounce:** 2 seconds (prevents multiple triggers)
- **Monitored:** Project root directory
- **File types:** .csv, .CSV

### Auto-Refresh
- **Polling interval:** 5 seconds
- **API endpoint:** `/api/check_updates`
- **Auto-reload delay:** 2 seconds after notification
- **Can be disabled:** Set `autoRefreshEnabled = false` in browser console

### Data Processing
- CSV files processed in-memory
- Automatic encoding detection (UTF-8, CP1252, Latin1)
- Data synced to Supabase in real-time
- Validation and error handling

---

## 🐛 Troubleshooting

### File watcher not working?
```
⚠️  Warning: watchdog not installed. Auto-reload disabled.
```
**Solution:** Run `pip install watchdog>=3.0.0`

### Files not updating?
1. Check console for `[Auto-Refresh]` messages
2. Verify file name matches expected pattern
3. Make sure file is saved properly
4. Check for CSV format errors

### Upload fails?
- Ensure file is not empty
- Check file is valid CSV format
- Look for error messages in browser console
- Verify Supabase connection (green "DB Connected" badge)

---

## 💡 Tips & Best Practices

1. **Use descriptive file names** that include keywords:
   - `DayRepReport_Jan2026.csv` ✅
   - `report.csv` ❌

2. **Keep files reasonable size**:
   - < 5MB: Fast
   - 5-15MB: Ok
   - \> 15MB: May be slow

3. **Check data before uploading**:
   - Verify CSV format
   - Ensure headers match expected format
   - Remove any extra blank rows

4. **Monitor the console** for helpful messages:
   - File changes detected
   - Processing status
   - Error details

---

## 🚀 Next Steps

Want to add more features? Here are some ideas:

- **Date range filtering** - View data across multiple dates
- **Crew search** - Find specific crew members quickly
- **Export to Excel/PDF** - Download reports
- **Email alerts** - Get notified of critical events
- **Dark/Light mode** - Theme switcher

Check the `implementation_plan.md` for more details!

---

## 📝 Summary

✅ **Automatic CSV monitoring** - Edit files, see results instantly  
✅ **Drag & drop upload** - Beautiful, intuitive interface  
✅ **Real-time notifications** - Never miss an update  
✅ **Better error handling** - Know what went wrong  
✅ **Improved UX** - Faster, smoother, more reliable

**Enjoy your enhanced Crew Dashboard! 🎉**

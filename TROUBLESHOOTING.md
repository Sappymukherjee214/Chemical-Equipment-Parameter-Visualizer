# Troubleshooting Guide

Common issues and solutions for the Chemical Equipment Parameter Visualizer.

## Backend Issues

### Issue: Port 8000 already in use

**Symptoms:**
```
Error: That port is already in use.
```

**Solutions:**
1. Find and kill the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

2. Or run on a different port:
```bash
python manage.py runserver 8001
```
Then update `API_BASE_URL` in frontend code to `http://localhost:8001/api`

### Issue: Database errors after migration

**Symptoms:**
```
django.db.utils.OperationalError: no such table
```

**Solution:**
```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'rest_framework'
```

**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CSV upload fails with validation error

**Symptoms:**
```
{"error": "Missing required columns: ..."}
```

**Solution:**
Ensure your CSV has exactly these columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Use the provided `sample_data.csv` as a template.

### Issue: CORS errors

**Symptoms:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Ensure `django-cors-headers` is installed
2. Check `INSTALLED_APPS` includes `'corsheaders'`
3. Check `MIDDLEWARE` includes `'corsheaders.middleware.CorsMiddleware'`
4. For development, `CORS_ALLOW_ALL_ORIGINS = True` should be set

---

## Web Frontend Issues

### Issue: npm install fails

**Symptoms:**
```
npm ERR! code ERESOLVE
```

**Solutions:**
```bash
# Try with legacy peer deps
npm install --legacy-peer-deps

# Or clear cache and retry
npm cache clean --force
npm install
```

### Issue: Port 3000 already in use

**Symptoms:**
```
Something is already running on port 3000
```

**Solution:**
React will automatically prompt to use a different port (3001). Press 'Y' to accept.

### Issue: Blank page after npm start

**Symptoms:**
Browser shows blank page, console shows errors

**Solutions:**
1. Check browser console for errors
2. Ensure backend is running on port 8000
3. Clear browser cache and reload
4. Check `API_BASE_URL` in `src/services/api.js`

### Issue: Login fails with "Invalid credentials"

**Symptoms:**
Login form shows error even with correct credentials

**Solutions:**
1. Ensure backend is running
2. Check backend console for errors
3. Verify superuser was created correctly
4. Try creating a new superuser:
```bash
python manage.py createsuperuser
```

### Issue: Charts not displaying

**Symptoms:**
Analytics page shows but charts are blank

**Solutions:**
1. Check browser console for Chart.js errors
2. Ensure dataset has data
3. Try refreshing the page
4. Check that analytics data is being fetched (Network tab)

---

## Desktop Frontend Issues

### Issue: PyQt5 installation fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement PyQt5
```

**Solutions:**

**Windows:**
```bash
pip install PyQt5==5.15.10
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-pyqt5
pip install PyQt5==5.15.10
```

**Mac:**
```bash
brew install pyqt5
pip install PyQt5==5.15.10
```

### Issue: "Connection refused" error

**Symptoms:**
```
requests.exceptions.ConnectionError: Connection refused
```

**Solutions:**
1. Ensure Django backend is running on port 8000
2. Check `API_BASE_URL` in `main.py` is correct
3. Test backend directly in browser: http://localhost:8000/api/

### Issue: Login dialog freezes

**Symptoms:**
Application becomes unresponsive during login

**Solutions:**
1. Check backend is responding
2. Increase timeout in `main.py` (currently 5 seconds)
3. Check firewall settings

### Issue: Charts not rendering

**Symptoms:**
Charts tab is blank or shows errors

**Solutions:**
1. Ensure matplotlib is installed correctly:
```bash
pip install matplotlib==3.8.2
```

2. Check if dataset has equipment records
3. Try selecting a different chart type

### Issue: PDF download fails

**Symptoms:**
Error when clicking "Download PDF Report"

**Solutions:**
1. Ensure you have write permissions in the selected directory
2. Check backend logs for PDF generation errors
3. Verify ReportLab is installed:
```bash
pip install reportlab==4.0.7
```

---

## General Issues

### Issue: Authentication keeps failing

**Symptoms:**
Both web and desktop apps reject valid credentials

**Solutions:**
1. Verify superuser exists:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(is_superuser=True)
```

2. Reset superuser password:
```bash
python manage.py changepassword <username>
```

3. Create new superuser:
```bash
python manage.py createsuperuser
```

### Issue: Slow performance with large datasets

**Symptoms:**
Upload or analytics takes very long

**Solutions:**
1. Limit CSV file size (currently 10MB max)
2. Reduce number of records
3. Check system resources (CPU, RAM)
4. For production, migrate to PostgreSQL

### Issue: "No datasets uploaded yet"

**Symptoms:**
Dataset list is empty even after upload

**Solutions:**
1. Check backend logs for upload errors
2. Verify file was actually uploaded (check `media/datasets/`)
3. Check database:
```bash
python manage.py shell
>>> from api.models import Dataset
>>> Dataset.objects.all()
```

---

## Development Issues

### Issue: Changes not reflecting

**Symptoms:**
Code changes don't appear in running application

**Solutions:**

**Backend:**
- Django auto-reloads, but sometimes needs manual restart
- Press Ctrl+C and run `python manage.py runserver` again

**Web Frontend:**
- React hot-reload should work automatically
- If not, stop (Ctrl+C) and run `npm start` again
- Clear browser cache

**Desktop:**
- Always restart the application after code changes
- Close and run `python main.py` again

### Issue: Import errors after adding new files

**Symptoms:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solutions:**
1. Check file paths are correct
2. Ensure `__init__.py` exists in package directories
3. Restart the application
4. Check for circular imports

---

## Database Issues

### Issue: "Database is locked"

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solutions:**
1. Close all connections to database
2. Restart backend server
3. For production, use PostgreSQL instead of SQLite

### Issue: Old datasets not being deleted

**Symptoms:**
More than 5 datasets exist in database

**Solutions:**
The cleanup happens in the `Dataset.save()` method. If it's not working:
1. Check the model's save method
2. Manually delete old datasets:
```bash
python manage.py shell
>>> from api.models import Dataset
>>> old_datasets = Dataset.objects.all()[5:]
>>> for ds in old_datasets:
...     ds.delete()
```

---

## Testing & Debugging

### Enable Debug Mode

**Backend:**
In `backend/settings.py`:
```python
DEBUG = True
```

**Check Backend Logs:**
Backend prints logs to console. Look for:
- Request URLs
- Error tracebacks
- SQL queries (if DEBUG=True)

**Check Web Frontend Console:**
Open browser DevTools (F12):
- Console tab: JavaScript errors
- Network tab: API requests/responses
- Application tab: localStorage (credentials)

**Desktop App Debugging:**
Add print statements in `main.py`:
```python
print(f"API Response: {response.json()}")
```

---

## Quick Diagnostics

Run these commands to check system status:

**Backend Health:**
```bash
curl http://localhost:8000/api/datasets/
# Should return JSON or authentication error
```

**Database Check:**
```bash
python manage.py shell
>>> from api.models import Dataset
>>> print(Dataset.objects.count())
```

**Frontend Build:**
```bash
cd web-frontend
npm run build
# Should complete without errors
```

---

## Getting Help

If issues persist:

1. **Check Documentation:**
   - README.md
   - ARCHITECTURE.md
   - Code comments

2. **Review Logs:**
   - Backend console output
   - Browser console (F12)
   - Desktop app console

3. **Verify Setup:**
   - Run `verify_setup.ps1`
   - Check all dependencies installed
   - Ensure correct Python/Node versions

4. **Test with Sample Data:**
   - Use provided `sample_data.csv`
   - Verify it works before using custom data

5. **Fresh Start:**
   - Delete virtual environments
   - Delete `node_modules`
   - Delete `db.sqlite3`
   - Reinstall everything from scratch

---

## Prevention Tips

1. **Always activate virtual environment** before running Python commands
2. **Keep dependencies updated** but test after updates
3. **Use sample data first** to verify setup
4. **Check backend is running** before starting frontends
5. **Read error messages carefully** - they usually indicate the problem
6. **Keep backups** of working database before major changes

---

**Still having issues?** Review the code - it's well-commented and should help identify the problem!

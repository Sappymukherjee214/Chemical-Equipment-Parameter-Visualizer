# Quick Start Guide

This guide will help you get the Chemical Equipment Parameter Visualizer up and running quickly.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Quick Setup (All Components)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (follow prompts)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

Backend will be available at: http://localhost:8000

### 2. Web Frontend Setup

Open a new terminal:

```bash
# Navigate to web frontend directory
cd web-frontend

# Install dependencies
npm install

# Start development server
npm start
```

Web app will be available at: http://localhost:3000

### 3. Desktop Frontend Setup

Open a new terminal:

```bash
# Navigate to desktop frontend directory
cd desktop-frontend

# Create virtual environment (or use backend's)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

## First Time Usage

1. **Login**: Use the superuser credentials you created during backend setup

2. **Upload Sample Data**: 
   - A sample CSV file is provided in `backend/sample_data.csv`
   - Use either the web or desktop interface to upload it

3. **Explore Features**:
   - View dataset list
   - Select a dataset to see analytics
   - View charts and visualizations
   - Download PDF reports

## Testing the API

You can test the API directly using curl or Postman:

```bash
# Login and get datasets (replace credentials)
curl -u username:password http://localhost:8000/api/datasets/

# Upload CSV
curl -u username:password -F "name=Test Dataset" -F "file=@sample_data.csv" http://localhost:8000/api/upload/
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
python manage.py runserver 8001
# Update API_BASE_URL in frontend code accordingly
```

**Database errors:**
```bash
# Delete db.sqlite3 and re-run migrations
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Web Frontend Issues

**Port 3000 already in use:**
- The app will prompt to use a different port automatically

**CORS errors:**
- Ensure backend is running
- Check CORS settings in backend/backend/settings.py

### Desktop Frontend Issues

**Connection refused:**
- Ensure backend is running on http://localhost:8000

**PyQt5 installation issues:**
```bash
# Try installing with pip
pip install PyQt5==5.15.10

# On Linux, you may need system packages:
sudo apt-get install python3-pyqt5
```

## Next Steps

- Read the full README.md for detailed documentation
- Explore the API endpoints at http://localhost:8000/api/
- Access Django admin at http://localhost:8000/admin/
- Customize the application for your needs

## Project Structure

```
Chemical Equipment Parameter Visualizer/
├── backend/                 # Django REST API
├── web-frontend/           # React web app
├── desktop-frontend/       # PyQt5 desktop app
├── README.md              # Main documentation
└── QUICKSTART.md          # This file
```

## Support

For issues or questions:
1. Check the main README.md
2. Review the code comments
3. Check Django/React/PyQt5 documentation

---

**Happy Analyzing! 🔬📊**

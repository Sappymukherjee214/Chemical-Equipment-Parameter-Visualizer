# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for analyzing and visualizing chemical equipment parameters from CSV data.

## 🎯 Project Overview

This application provides both web and desktop interfaces to upload, analyze, and visualize chemical equipment data. It features:

- **Django REST Framework Backend** - Handles CSV parsing, data storage, and analytics
- **React.js Web Frontend** - Modern web interface with Chart.js visualizations
- **PyQt5 Desktop Frontend** - Native desktop application with Matplotlib charts
- **SQLite Database** - Stores the last 5 uploaded datasets
- **PDF Report Generation** - Export summary reports
- **Basic Authentication** - Secure API access

## 📁 Project Structure

```
Chemical Equipment Parameter Visualizer/
├── backend/                    # Django REST Framework backend
│   ├── api/                   # Main API application
│   ├── backend/               # Django project settings
│   ├── media/                 # Uploaded CSV files
│   ├── reports/               # Generated PDF reports
│   ├── manage.py
│   └── requirements.txt
├── web-frontend/              # React.js web application
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── desktop-frontend/          # PyQt5 desktop application
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── README.md                  # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (for authentication):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Web Frontend Setup

1. Navigate to the web-frontend directory:
```bash
cd web-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web application will be available at `http://localhost:3000`

### Desktop Frontend Setup

1. Navigate to the desktop-frontend directory:
```bash
cd desktop-frontend
```

2. Create a virtual environment (if not using the backend's):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the desktop application:
```bash
python main.py
```

## 📊 CSV Data Format

The application expects CSV files with the following columns:

| Column Name      | Type    | Description                    |
|-----------------|---------|--------------------------------|
| Equipment Name  | String  | Name of the equipment          |
| Type            | String  | Equipment type/category        |
| Flowrate        | Float   | Flow rate value                |
| Pressure        | Float   | Pressure value                 |
| Temperature     | Float   | Temperature value              |

### Example CSV:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,25.3,85.2
Reactor-001,Reactor,200.0,30.5,120.5
Heat Exchanger-001,Heat Exchanger,175.2,28.0,95.0
```

## 🔐 Authentication

Both web and desktop applications require authentication:

- **Username**: Created during superuser setup
- **Password**: Created during superuser setup

The desktop application will prompt for credentials on startup.
The web application has a login page.

## 📈 Features

### Backend API Endpoints

- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - List all datasets (last 5)
- `GET /api/datasets/{id}/` - Get specific dataset details
- `GET /api/datasets/{id}/analytics/` - Get analytics for a dataset
- `GET /api/datasets/{id}/download-report/` - Download PDF report

### Web Frontend Features

- User authentication
- CSV file upload with drag-and-drop
- Dataset listing and selection
- Interactive charts (Chart.js):
  - Equipment type distribution (Pie chart)
  - Temperature distribution (Bar chart)
  - Pressure vs Flowrate (Scatter plot)
- Summary statistics table
- PDF report download

### Desktop Frontend Features

- Login dialog
- CSV file upload via file browser
- Dataset selection dropdown
- Matplotlib visualizations:
  - Equipment type distribution (Pie chart)
  - Parameter distributions (Histograms)
  - Correlation plots
- Summary statistics display
- PDF report generation

## 🛠️ Technology Stack

### Backend
- Django 4.2
- Django REST Framework
- Pandas (data processing)
- ReportLab (PDF generation)
- SQLite (database)

### Web Frontend
- React.js 18
- Chart.js (visualizations)
- Axios (HTTP client)
- CSS3 (styling)

### Desktop Frontend
- PyQt5 (GUI framework)
- Matplotlib (visualizations)
- Requests (HTTP client)

## 📝 API Usage Examples

### Upload CSV
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Basic <base64_credentials>" \
  -F "file=@equipment_data.csv" \
  -F "name=Dataset 1"
```

### Get Analytics
```bash
curl -X GET http://localhost:8000/api/datasets/1/analytics/ \
  -H "Authorization: Basic <base64_credentials>"
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Web Frontend Tests
```bash
cd web-frontend
npm test
```

## 📦 Deployment Considerations

- Set `DEBUG = False` in Django settings for production
- Configure proper database (PostgreSQL recommended)
- Set up static file serving (WhiteNoise or CDN)
- Use environment variables for sensitive data
- Enable CORS for web frontend domain
- Use HTTPS in production

## 🤝 Contributing

This project was created as an internship screening task demonstrating:
- Full-stack development skills
- API design and implementation
- Multiple frontend technologies
- Data processing and visualization
- Clean code organization

## 📄 License

MIT License

## 👤 Author

Created for internship screening demonstration

---

**Note**: This is a demonstration project showcasing hybrid application development with shared backend architecture.

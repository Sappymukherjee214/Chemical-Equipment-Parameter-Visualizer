# Architecture Documentation

## System Overview

The Chemical Equipment Parameter Visualizer is a hybrid application consisting of three main components that share a common backend API:

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
├──────────────────────────┬──────────────────────────────────┤
│   React Web Frontend     │   PyQt5 Desktop Frontend         │
│   (Port 3000)           │   (Native Application)            │
│   - Chart.js            │   - Matplotlib                    │
│   - Axios               │   - Requests                      │
└──────────────┬───────────┴──────────────┬───────────────────┘
               │                          │
               │    HTTP/REST API         │
               │    (Basic Auth)          │
               └──────────┬───────────────┘
                          │
               ┌──────────▼──────────┐
               │  Django Backend     │
               │  (Port 8000)        │
               │  - REST Framework   │
               │  - Pandas           │
               │  - ReportLab        │
               └──────────┬──────────┘
                          │
               ┌──────────▼──────────┐
               │  SQLite Database    │
               │  - Datasets (max 5) │
               │  - Equipment Data   │
               └─────────────────────┘
```

## Backend Architecture

### Technology Stack
- **Framework**: Django 4.2
- **API**: Django REST Framework 3.14
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Data Processing**: Pandas 2.1
- **PDF Generation**: ReportLab 4.0
- **CORS**: django-cors-headers

### Key Components

#### 1. Models (`api/models.py`)

**Dataset Model**
- Stores metadata about uploaded CSV files
- Maintains analytics cache (avg values, equipment counts)
- Automatically deletes oldest datasets when count exceeds 5
- Fields: name, file, uploaded_by, uploaded_at, analytics fields

**EquipmentData Model**
- Stores individual equipment records
- Foreign key relationship to Dataset
- Fields: equipment_name, type, flowrate, pressure, temperature

#### 2. API Endpoints (`api/views.py`)

**DatasetViewSet**
- `GET /api/datasets/` - List all datasets
- `GET /api/datasets/{id}/` - Retrieve dataset details
- `DELETE /api/datasets/{id}/` - Delete dataset
- `GET /api/datasets/{id}/analytics/` - Get analytics
- `GET /api/datasets/{id}/download-report/` - Download PDF
- `GET /api/datasets/{id}/equipment/` - Get equipment records

**UploadViewSet**
- `POST /api/upload/` - Upload and process CSV file

#### 3. Data Processing (`api/utils.py`)

**CSV Parsing**
- Validates CSV structure
- Checks for required columns
- Handles data type conversion
- Removes invalid rows

**Analytics Calculation**
- Computes averages (flowrate, pressure, temperature)
- Calculates min/max values
- Generates equipment type distribution
- Uses Pandas for efficient processing

#### 4. PDF Generation (`api/pdf_generator.py`)

**Report Structure**
- Dataset information table
- Summary statistics
- Equipment type distribution
- Detailed equipment list (first 50 records)
- Professional formatting with ReportLab

### Authentication

- **Method**: HTTP Basic Authentication
- **Storage**: Django's built-in User model
- **Security**: Credentials encoded in Base64
- **Production**: Should use token-based auth (JWT)

### Data Flow

```
CSV Upload → Validation → Pandas Processing → Database Storage → Analytics Cache
     ↓
API Request → Authentication → Query Database → Serialize → JSON Response
```

## Web Frontend Architecture

### Technology Stack
- **Framework**: React 18
- **Charts**: Chart.js 4.4 with react-chartjs-2
- **HTTP Client**: Axios 1.6
- **Styling**: Vanilla CSS with gradients and animations

### Component Structure

```
App.js (Main Container)
├── Login.js (Authentication)
├── Upload.js (CSV Upload with Drag & Drop)
├── DatasetList.js (Dataset Cards Grid)
└── Analytics.js (Charts & Statistics)
    ├── Summary Stats Cards
    ├── Pie Chart (Equipment Distribution)
    ├── Bar Chart (Parameter Comparison)
    └── Scatter Plot (Correlation)
```

### State Management

- **Local State**: React useState hooks
- **Authentication**: localStorage for credentials
- **Data Flow**: Props drilling (suitable for app size)

### API Service (`services/api.js`)

- Centralized API calls
- Axios interceptors for auth headers
- Error handling
- File download handling

### Design Principles

- **Modern Aesthetics**: Gradient backgrounds, smooth animations
- **Responsive**: Grid layouts adapt to screen size
- **Interactive**: Hover effects, transitions
- **User Feedback**: Loading states, error messages

## Desktop Frontend Architecture

### Technology Stack
- **GUI Framework**: PyQt5 5.15
- **Charts**: Matplotlib 3.8
- **HTTP Client**: Requests 2.31
- **Threading**: QThread for async operations

### Application Structure

```
main.py
├── LoginDialog (Authentication Dialog)
├── MainWindow (Main Application)
│   ├── Header (Title & User Info)
│   ├── Control Panel (Upload, Select, Refresh, Download)
│   └── Tab Widget
│       ├── Summary Tab (Text Display)
│       ├── Charts Tab (Matplotlib Canvas)
│       └── Data Table Tab (QTableWidget)
├── DataLoader (QThread for API calls)
└── ChartWidget (Matplotlib Integration)
```

### Key Features

**Threading**
- Non-blocking API calls using QThread
- Signals/slots for communication
- Prevents UI freezing

**Charts**
- Embedded Matplotlib figures
- Interactive chart type selection
- Professional styling

**Data Display**
- Formatted text summary
- Sortable data table
- Real-time updates

## Database Schema

### Dataset Table
```sql
CREATE TABLE dataset (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    file VARCHAR(100),
    uploaded_by_id INTEGER FOREIGN KEY,
    uploaded_at DATETIME,
    total_equipment INTEGER,
    avg_flowrate FLOAT,
    avg_pressure FLOAT,
    avg_temperature FLOAT,
    equipment_types JSON
);
```

### EquipmentData Table
```sql
CREATE TABLE equipment_data (
    id INTEGER PRIMARY KEY,
    dataset_id INTEGER FOREIGN KEY,
    equipment_name VARCHAR(255),
    equipment_type VARCHAR(100),
    flowrate FLOAT,
    pressure FLOAT,
    temperature FLOAT
);
```

## Security Considerations

### Current Implementation
- Basic HTTP Authentication
- CORS enabled for development
- No HTTPS (development only)

### Production Recommendations
1. **Authentication**: Implement JWT tokens
2. **HTTPS**: Use SSL/TLS certificates
3. **CORS**: Restrict to specific domains
4. **Input Validation**: Enhanced CSV validation
5. **Rate Limiting**: Prevent abuse
6. **File Size Limits**: Already implemented (10MB)

## Performance Optimizations

### Backend
- **Bulk Insert**: Uses `bulk_create()` for equipment records
- **Analytics Cache**: Stores computed values in Dataset model
- **Pagination**: DRF pagination for large datasets
- **Database Indexing**: On foreign keys and timestamps

### Frontend
- **Lazy Loading**: Charts render only when tab is active
- **Memoization**: Could add React.memo for components
- **Debouncing**: Could add for search/filter features

### Desktop
- **Threading**: Async API calls
- **Table Optimization**: Shows limited records
- **Chart Caching**: Matplotlib figure reuse

## Scalability Considerations

### Current Limitations
- SQLite (single-file database)
- 5 dataset limit (by design)
- No caching layer
- No load balancing

### Scaling Path
1. **Database**: Migrate to PostgreSQL
2. **Caching**: Add Redis for analytics
3. **Storage**: Use S3 for CSV files
4. **API**: Add rate limiting and pagination
5. **Deployment**: Docker + Kubernetes
6. **CDN**: Serve static files from CDN

## Testing Strategy

### Backend Testing
```python
# Unit tests for models
python manage.py test api.tests.ModelTests

# Integration tests for API
python manage.py test api.tests.APITests

# CSV parsing tests
python manage.py test api.tests.UtilsTests
```

### Frontend Testing
```bash
# Component tests
npm test

# E2E tests (could add Cypress)
npm run cypress
```

## Deployment Architecture

### Development
```
localhost:8000 (Django) + localhost:3000 (React) + Desktop App
```

### Production (Recommended)
```
┌─────────────────┐
│   Nginx/CDN     │ (Static files, SSL)
└────────┬────────┘
         │
┌────────▼────────┐
│   Gunicorn      │ (WSGI server)
└────────┬────────┘
         │
┌────────▼────────┐
│   Django App    │ (Application server)
└────────┬────────┘
         │
┌────────▼────────┐
│   PostgreSQL    │ (Database)
└─────────────────┘
```

## API Documentation

Full API documentation available at:
- Browsable API: http://localhost:8000/api/
- Admin Interface: http://localhost:8000/admin/

## Future Enhancements

1. **Real-time Updates**: WebSocket support
2. **Advanced Analytics**: ML predictions, anomaly detection
3. **Export Options**: Excel, JSON exports
4. **Collaboration**: Multi-user editing
5. **Notifications**: Email alerts for uploads
6. **Mobile App**: React Native version
7. **Data Validation**: Advanced CSV validation rules
8. **Audit Logs**: Track all changes
9. **Backup/Restore**: Automated backups
10. **API Versioning**: v1, v2 endpoints

## Conclusion

This architecture provides a solid foundation for a hybrid application with:
- Clean separation of concerns
- Reusable API design
- Modern frontend technologies
- Professional desktop interface
- Room for growth and enhancement

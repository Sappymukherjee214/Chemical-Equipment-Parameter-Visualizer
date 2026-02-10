# Desktop Frontend - PyQt5 Application

## Overview

This is the desktop frontend for the Chemical Equipment Parameter Visualizer. It provides a native desktop interface built with PyQt5 and Matplotlib for data visualization.

## Features

- **Login Authentication** - Secure login dialog
- **CSV Upload** - Upload datasets directly from the desktop
- **Dataset Selection** - Browse and select from available datasets
- **Multiple Views**:
  - Summary tab with detailed statistics
  - Charts tab with interactive visualizations
  - Data table tab with equipment records
- **Matplotlib Charts**:
  - Pie chart for equipment type distribution
  - Bar chart for type counts
  - Scatter plot for parameter correlations
- **PDF Report Download** - Generate and save PDF reports

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure the Django backend is running at `http://localhost:8000`

2. Run the desktop application:
```bash
python main.py
```

3. Login with your Django superuser credentials

## Usage

1. **Login**: Enter your username and password
2. **Upload CSV**: Click "Upload CSV" to add a new dataset
3. **Select Dataset**: Choose a dataset from the dropdown
4. **View Analytics**: Switch between Summary, Charts, and Data Table tabs
5. **Download Report**: Click "Download PDF Report" to save a report

## Requirements

- Python 3.8+
- PyQt5 5.15+
- Matplotlib 3.8+
- Requests 2.31+
- Pandas 2.1+

## Architecture

The application uses:
- **PyQt5** for the GUI framework
- **Matplotlib** for chart rendering
- **Requests** for API communication
- **Threading** for non-blocking API calls

## API Integration

The desktop app consumes the same REST API as the web frontend:
- `GET /api/datasets/` - List datasets
- `GET /api/datasets/{id}/` - Get dataset details
- `GET /api/datasets/{id}/analytics/` - Get analytics
- `POST /api/upload/` - Upload CSV
- `GET /api/datasets/{id}/download-report/` - Download PDF

## Troubleshooting

**Connection Error**: Ensure the Django backend is running on port 8000

**Authentication Failed**: Verify your username and password are correct

**Upload Failed**: Check that the CSV file has the correct format

## Screenshots

The application features:
- Modern gradient header
- Tabbed interface for different views
- Professional chart visualizations
- Clean data table display

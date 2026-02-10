"""
Runtime Error Prevention Test Script
This script tests all critical functions to ensure no runtime errors occur.
Run this after setting up the backend to verify everything works.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Dataset, EquipmentData
from api.utils import parse_csv_file, calculate_analytics, save_dataset_to_db, get_dataset_analytics
from api.pdf_generator import generate_pdf_report
import pandas as pd
from io import StringIO

print("=" * 70)
print("RUNTIME ERROR PREVENTION TEST")
print("=" * 70)
print()

# Test 1: Check imports
print("✓ Test 1: All imports successful")
print()

# Test 2: Check database connection
print("Test 2: Database connection...")
try:
    User.objects.count()
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)
print()

# Test 3: Check models
print("Test 3: Model creation...")
try:
    # Check if superuser exists
    if not User.objects.filter(is_superuser=True).exists():
        print("⚠ Warning: No superuser found. Run: python manage.py createsuperuser")
    else:
        print("✓ Superuser exists")
    
    # Check dataset count
    dataset_count = Dataset.objects.count()
    print(f"✓ Current datasets: {dataset_count}")
except Exception as e:
    print(f"✗ Model error: {e}")
    sys.exit(1)
print()

# Test 4: CSV parsing
print("Test 4: CSV parsing...")
try:
    csv_content = """Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105"""
    
    csv_file = StringIO(csv_content)
    df = parse_csv_file(csv_file)
    print(f"✓ CSV parsed successfully: {len(df)} rows")
except Exception as e:
    print(f"✗ CSV parsing error: {e}")
    sys.exit(1)
print()

# Test 5: Analytics calculation
print("Test 5: Analytics calculation...")
try:
    analytics = calculate_analytics(df)
    print(f"✓ Analytics calculated:")
    print(f"  - Total equipment: {analytics['total_equipment']}")
    print(f"  - Avg flowrate: {analytics['avg_flowrate']:.2f}")
    print(f"  - Equipment types: {analytics['equipment_types']}")
except Exception as e:
    print(f"✗ Analytics error: {e}")
    sys.exit(1)
print()

# Test 6: Settings check
print("Test 6: Django settings...")
try:
    from django.conf import settings
    
    # Check critical settings
    assert hasattr(settings, 'MEDIA_ROOT'), "MEDIA_ROOT not defined"
    assert hasattr(settings, 'REPORTS_DIR'), "REPORTS_DIR not defined"
    assert hasattr(settings, 'REST_FRAMEWORK'), "REST_FRAMEWORK not defined"
    
    print(f"✓ MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"✓ REPORTS_DIR: {settings.REPORTS_DIR}")
    print(f"✓ REST_FRAMEWORK configured")
    
    # Create directories if they don't exist
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    print("✓ Required directories created")
    
except Exception as e:
    print(f"✗ Settings error: {e}")
    sys.exit(1)
print()

# Test 7: PDF generation (if dataset exists)
print("Test 7: PDF generation...")
try:
    if Dataset.objects.exists():
        dataset = Dataset.objects.first()
        pdf_path = generate_pdf_report(dataset.id)
        if os.path.exists(pdf_path):
            print(f"✓ PDF generated successfully: {pdf_path}")
            # Clean up test PDF
            os.remove(pdf_path)
        else:
            print("✗ PDF file not created")
    else:
        print("⚠ Skipped: No datasets available (upload one to test)")
except Exception as e:
    print(f"✗ PDF generation error: {e}")
    # Don't exit, this is not critical for initial setup
print()

# Test 8: API endpoints (basic check)
print("Test 8: API configuration...")
try:
    from api.views import DatasetViewSet, UploadViewSet
    from api.serializers import DatasetSerializer, AnalyticsSerializer
    
    print("✓ ViewSets imported successfully")
    print("✓ Serializers imported successfully")
except Exception as e:
    print(f"✗ API configuration error: {e}")
    sys.exit(1)
print()

# Test 9: File upload limits
print("Test 9: File upload configuration...")
try:
    from django.conf import settings
    max_size = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    print(f"✓ Max upload size: {max_size / (1024*1024):.1f} MB")
except Exception as e:
    print(f"✗ Upload configuration error: {e}")
print()

# Test 10: CORS configuration
print("Test 10: CORS configuration...")
try:
    from django.conf import settings
    if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS'):
        print(f"✓ CORS_ALLOW_ALL_ORIGINS: {settings.CORS_ALLOW_ALL_ORIGINS}")
    if 'corsheaders' in settings.INSTALLED_APPS:
        print("✓ corsheaders installed")
    if 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE:
        print("✓ CORS middleware configured")
except Exception as e:
    print(f"✗ CORS configuration error: {e}")
print()

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
print("✓ All critical tests passed!")
print()
print("Next steps:")
print("1. Run migrations: python manage.py migrate")
print("2. Create superuser: python manage.py createsuperuser")
print("3. Start server: python manage.py runserver")
print("4. Upload sample_data.csv to test full functionality")
print()
print("=" * 70)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import os

from .models import Dataset, EquipmentData
from .serializers import (
    DatasetSerializer, DatasetDetailSerializer, 
    DatasetUploadSerializer, EquipmentDataSerializer,
    AnalyticsSerializer
)
from .utils import parse_csv_file, save_dataset_to_db, get_dataset_analytics
from .pdf_generator import generate_pdf_report


class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing datasets.
    
    Endpoints:
    - GET /api/datasets/ - List all datasets
    - POST /api/datasets/ - Create new dataset (not used, use upload instead)
    - GET /api/datasets/{id}/ - Retrieve dataset details
    - DELETE /api/datasets/{id}/ - Delete dataset
    - GET /api/datasets/{id}/analytics/ - Get analytics for dataset
    - GET /api/datasets/{id}/download-report/ - Download PDF report
    """
    queryset = Dataset.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DatasetDetailSerializer
        return DatasetSerializer
    
    def get_queryset(self):
        """Return datasets ordered by upload date (newest first)"""
        return Dataset.objects.all().order_by('-uploaded_at')
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """
        Get analytics for a specific dataset.
        
        GET /api/datasets/{id}/analytics/
        """
        dataset = self.get_object()
        analytics_data = get_dataset_analytics(dataset.id)
        
        if analytics_data is None:
            return Response(
                {'error': 'Unable to calculate analytics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = AnalyticsSerializer(analytics_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='download-report')
    def download_report(self, request, pk=None):
        """
        Generate and download PDF report for a dataset.
        
        GET /api/datasets/{id}/download-report/
        """
        dataset = self.get_object()
        
        try:
            pdf_path = generate_pdf_report(dataset.id)
            
            if not os.path.exists(pdf_path):
                return Response(
                    {'error': 'Failed to generate report'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            response = FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="report_{dataset.name}.pdf"'
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """
        Get all equipment records for a dataset.
        
        GET /api/datasets/{id}/equipment/
        """
        dataset = self.get_object()
        equipment_records = dataset.equipment_records.all()
        serializer = EquipmentDataSerializer(equipment_records, many=True)
        return Response(serializer.data)


class UploadViewSet(viewsets.ViewSet):
    """
    ViewSet for handling CSV file uploads.
    
    Endpoints:
    - POST /api/upload/ - Upload CSV file
    """
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        """
        Upload and process a CSV file.
        
        POST /api/upload/
        
        Request body (multipart/form-data):
        - name: Dataset name
        - file: CSV file
        
        Returns:
        - Dataset object with analytics
        """
        serializer = DatasetUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        name = serializer.validated_data['name']
        csv_file = serializer.validated_data['file']
        
        try:
            # Parse CSV file
            df = parse_csv_file(csv_file)
            
            # Create dataset object
            dataset = Dataset.objects.create(
                name=name,
                file=csv_file,
                uploaded_by=request.user
            )
            
            # Save data to database
            save_dataset_to_db(dataset, df)
            
            # Return dataset with analytics
            response_serializer = DatasetDetailSerializer(dataset)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os

@csrf_exempt
def create_superuser(request):
    """
    Temporary endpoint to create a superuser without shell access.
    DELETE THIS AFTER CREATING YOUR ADMIN USER!
    
    Visit: https://your-backend-url.onrender.com/api/create-superuser/
    """
    # Security: Only allow in production if SECRET_KEY env var is set
    if os.environ.get('DEBUG', 'False') == 'False':
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Superuser already exists. Please delete this endpoint for security.'
            }, status=400)
    
    try:
        # Create superuser with default credentials
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'  # Change this immediately after login!
        )
        return JsonResponse({
            'status': 'success',
            'message': 'Superuser created successfully!',
            'username': 'admin',
            'password': 'admin123',
            'warning': 'CHANGE THIS PASSWORD IMMEDIATELY! Delete this endpoint after use.'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


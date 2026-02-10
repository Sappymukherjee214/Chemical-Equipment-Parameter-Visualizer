from rest_framework import serializers
from .models import Dataset, EquipmentData


class EquipmentDataSerializer(serializers.ModelSerializer):
    """Serializer for individual equipment records"""
    
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for dataset with basic information"""
    uploaded_by = serializers.StringRelatedField(read_only=True)
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'file', 'uploaded_by', 'uploaded_at',
            'total_equipment', 'avg_flowrate', 'avg_pressure', 
            'avg_temperature', 'equipment_types', 'equipment_count'
        ]
        read_only_fields = [
            'uploaded_by', 'uploaded_at', 'total_equipment',
            'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment_types'
        ]
    
    def get_equipment_count(self, obj):
        return obj.total_equipment


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer including all equipment records"""
    uploaded_by = serializers.StringRelatedField(read_only=True)
    equipment_records = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'file', 'uploaded_by', 'uploaded_at',
            'total_equipment', 'avg_flowrate', 'avg_pressure',
            'avg_temperature', 'equipment_types', 'equipment_records'
        ]


class DatasetUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    name = serializers.CharField(max_length=255)
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate that the uploaded file is a CSV"""
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value


class AnalyticsSerializer(serializers.Serializer):
    """Serializer for analytics data"""
    total_equipment = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    equipment_types = serializers.DictField()
    min_flowrate = serializers.FloatField()
    max_flowrate = serializers.FloatField()
    min_pressure = serializers.FloatField()
    max_pressure = serializers.FloatField()
    min_temperature = serializers.FloatField()
    max_temperature = serializers.FloatField()

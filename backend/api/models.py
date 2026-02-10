from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Dataset(models.Model):
    """
    Model to store uploaded CSV datasets.
    Only the last 5 datasets are kept in the database.
    """
    name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='datasets/',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Analytics fields (cached for performance)
    total_equipment = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    equipment_types = models.JSONField(default=dict)  # {type: count}
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Override save to maintain only last 5 datasets"""
        super().save(*args, **kwargs)
        
        # Keep only the last 5 datasets
        datasets = Dataset.objects.all()
        if datasets.count() > 5:
            # Delete oldest datasets
            datasets_to_delete = datasets[5:]
            for dataset in datasets_to_delete:
                # Delete associated file
                if dataset.file:
                    dataset.file.delete(save=False)
                dataset.delete()


class EquipmentData(models.Model):
    """
    Model to store individual equipment records from CSV.
    """
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment_records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['equipment_name']
        
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"

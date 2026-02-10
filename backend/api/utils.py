import pandas as pd
from django.db import transaction
from .models import Dataset, EquipmentData


def parse_csv_file(file_obj):
    """
    Parse CSV file and return a pandas DataFrame.
    
    Args:
        file_obj: Django UploadedFile object
        
    Returns:
        pandas.DataFrame: Parsed data
        
    Raises:
        ValueError: If CSV format is invalid
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_obj)
        
        # Expected columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Remove any rows with missing values
        df = df.dropna(subset=required_columns)
        
        # Validate numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with invalid numeric values
        df = df.dropna(subset=numeric_columns)
        
        if len(df) == 0:
            raise ValueError("No valid data rows found in CSV file")
        
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format")
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")


def calculate_analytics(df):
    """
    Calculate analytics from DataFrame.
    
    Args:
        df: pandas.DataFrame with equipment data
        
    Returns:
        dict: Analytics data
    """
    analytics = {
        'total_equipment': len(df),
        'avg_flowrate': float(df['Flowrate'].mean()),
        'avg_pressure': float(df['Pressure'].mean()),
        'avg_temperature': float(df['Temperature'].mean()),
        'min_flowrate': float(df['Flowrate'].min()),
        'max_flowrate': float(df['Flowrate'].max()),
        'min_pressure': float(df['Pressure'].min()),
        'max_pressure': float(df['Pressure'].max()),
        'min_temperature': float(df['Temperature'].min()),
        'max_temperature': float(df['Temperature'].max()),
        'equipment_types': df['Type'].value_counts().to_dict(),
    }
    
    return analytics


@transaction.atomic
def save_dataset_to_db(dataset_obj, df):
    """
    Save parsed DataFrame to database.
    
    Args:
        dataset_obj: Dataset model instance
        df: pandas.DataFrame with equipment data
    """
    # Calculate analytics
    analytics = calculate_analytics(df)
    
    # Update dataset with analytics
    dataset_obj.total_equipment = analytics['total_equipment']
    dataset_obj.avg_flowrate = analytics['avg_flowrate']
    dataset_obj.avg_pressure = analytics['avg_pressure']
    dataset_obj.avg_temperature = analytics['avg_temperature']
    dataset_obj.equipment_types = analytics['equipment_types']
    dataset_obj.save()
    
    # Create equipment records
    equipment_records = []
    for _, row in df.iterrows():
        equipment_records.append(
            EquipmentData(
                dataset=dataset_obj,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
        )
    
    # Bulk create for performance
    EquipmentData.objects.bulk_create(equipment_records)


def get_dataset_analytics(dataset_id):
    """
    Get analytics for a specific dataset.
    
    Args:
        dataset_id: ID of the dataset
        
    Returns:
        dict: Analytics data
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        
        # Get all equipment records
        equipment_records = dataset.equipment_records.all()
        
        if not equipment_records.exists():
            return None
        
        # Convert to DataFrame for analysis
        data = list(equipment_records.values(
            'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature'
        ))
        df = pd.DataFrame(data)
        df.rename(columns={
            'equipment_name': 'Equipment Name',
            'equipment_type': 'Type',
            'flowrate': 'Flowrate',
            'pressure': 'Pressure',
            'temperature': 'Temperature'
        }, inplace=True)
        
        # Calculate analytics
        analytics = calculate_analytics(df)
        
        return analytics
        
    except Dataset.DoesNotExist:
        return None

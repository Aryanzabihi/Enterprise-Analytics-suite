import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_inventory_dataset(num_items=100):
    """
    Generate a comprehensive sample inventory dataset.
    
    Args:
        num_items (int): Number of inventory items to generate
    
    Returns:
        pd.DataFrame: Sample inventory dataset
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate item IDs and names
    item_ids = [f"ITEM_{i:04d}" for i in range(1, num_items + 1)]
    
    # Sample item names and categories
    item_names = [
        "Laptop Computer", "Wireless Mouse", "USB Cable", "External Hard Drive",
        "Monitor Stand", "Keyboard", "Webcam", "Headphones", "Power Adapter",
        "Network Switch", "Router", "Ethernet Cable", "Wireless Adapter",
        "Bluetooth Speaker", "Microphone", "Graphics Card", "RAM Module",
        "SSD Drive", "Cooling Fan", "Motherboard", "Processor", "Case Fan",
        "Power Supply", "Optical Drive", "Sound Card", "Network Card",
        "Video Capture Card", "USB Hub", "Card Reader", "Cable Organizer",
        "Desk Lamp", "Office Chair", "Filing Cabinet", "Whiteboard",
        "Projector Screen", "Document Scanner", "Printer", "Ink Cartridge",
        "Paper Tray", "Stapler", "Paper Shredder", "Label Maker",
        "Calculator", "Notebook", "Pen Set", "Desk Organizer",
        "Coffee Mug", "Water Bottle", "Lunch Box", "Backpack",
        "Umbrella", "First Aid Kit", "Fire Extinguisher", "Security Camera",
        "Door Lock", "Access Card", "Time Clock", "Employee Badge",
        "Conference Phone", "Video Conference System", "Presentation Remote",
        "Laser Pointer", "Flip Chart", "Easel", "Display Stand",
        "Trade Show Booth", "Banner Stand", "Pop-up Display", "Table Cover",
        "Chair Cover", "Table Runner", "Centerpiece", "Flower Vase",
        "Picture Frame", "Wall Clock", "Mirror", "Rug",
        "Curtain", "Blind", "Shelf Unit", "Bookcase",
        "Filing Tray", "Inbox", "Outbox", "Mail Organizer",
        "Calendar", "Planner", "Sticky Notes", "Index Cards",
        "Binder", "Folder", "Envelope", "Paper Clip",
        "Rubber Band", "Tape Dispenser", "Glue Stick", "Scissors",
        "Ruler", "Protractor", "Compass", "Pencil Sharpener"
    ]
    
    categories = [
        "Electronics", "Computer Hardware", "Networking", "Audio/Video",
        "Office Supplies", "Furniture", "Safety Equipment", "Security",
        "Communications", "Presentation", "Trade Show", "Decor",
        "Organization", "Writing Supplies", "Paper Products", "Tools"
    ]
    
    suppliers = [
        "TechCorp Inc.", "OfficeMax Solutions", "Global Supply Co.",
        "Premium Electronics", "Quality Hardware Ltd.", "Smart Systems",
        "Innovation Tech", "Reliable Parts", "Fast Delivery Co.",
        "Budget Supplies", "Professional Equipment", "Enterprise Solutions"
    ]
    
    warehouse_locations = [
        "Main Warehouse", "East Wing", "West Wing", "North Section",
        "South Section", "Upper Level", "Lower Level", "Loading Dock",
        "Cold Storage", "Secure Vault", "Express Pick", "Bulk Storage"
    ]
    
    # Generate data
    data = []
    
    for i in range(num_items):
        # Basic item information
        item_id = item_ids[i]
        item_name = random.choice(item_names)
        category = random.choice(categories)
        supplier_id = random.choice(suppliers)
        warehouse_location = random.choice(warehouse_locations)
        
        # Generate description
        description = f"High-quality {item_name.lower()} for professional use"
        
        # Stock levels
        current_stock = random.randint(0, 500)
        reorder_point = random.randint(10, 100)
        max_stock = random.randint(100, 1000)
        
        # Costs
        unit_cost = round(random.uniform(5.0, 500.0), 2)
        holding_cost_rate = round(random.uniform(15.0, 25.0), 1)
        
        # Performance metrics
        turnover_rate = round(random.uniform(2.0, 12.0), 2)
        forecast_accuracy = round(random.uniform(70.0, 95.0), 1)
        
        # Demand patterns
        quantity = random.randint(1, 100)
        seasonality_score = round(random.uniform(0.0, 1.0), 2)
        demand_volatility = round(random.uniform(0.1, 0.8), 2)
        
        # Supplier performance
        supplier_performance = round(random.uniform(60.0, 95.0), 1)
        lead_time = random.randint(1, 30)
        quality_score = round(random.uniform(80.0, 100.0), 1)
        on_time_delivery = round(random.uniform(85.0, 98.0), 1)
        
        # Warehouse operations
        storage_volume = random.randint(1, 100)
        pick_time = round(random.uniform(1.0, 15.0), 1)
        pick_route = f"Route_{random.randint(1, 5)}"
        
        # Generate dates for time series data
        base_date = datetime.now() - timedelta(days=365)
        date = base_date + timedelta(days=random.randint(0, 365))
        
        # Create item record
        item_record = {
            'item_id': item_id,
            'item_name': item_name,
            'category': category,
            'description': description,
            'supplier_id': supplier_id,
            'warehouse_location': warehouse_location,
            'current_stock': current_stock,
            'reorder_point': reorder_point,
            'max_stock': max_stock,
            'unit_cost': unit_cost,
            'holding_cost_rate': holding_cost_rate,
            'turnover_rate': turnover_rate,
            'forecast_accuracy': forecast_accuracy,
            'quantity': quantity,
            'date': date,
            'seasonality_score': seasonality_score,
            'demand_volatility': demand_volatility,
            'supplier_performance': supplier_performance,
            'lead_time': lead_time,
            'quality_score': quality_score,
            'on_time_delivery': on_time_delivery,
            'storage_volume': storage_volume,
            'pick_time': pick_time,
            'pick_route': pick_route
        }
        
        data.append(item_record)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add calculated fields
    df = add_calculated_fields(df)
    
    return df

def add_calculated_fields(df):
    """
    Add calculated fields to the inventory dataset.
    
    Args:
        df (pd.DataFrame): Raw inventory data
    
    Returns:
        pd.DataFrame: Data with calculated fields
    """
    if df.empty:
        return df
    
    # Calculate ABC categories
    df['stock_value'] = df['current_stock'] * df['unit_cost']
    df['abc_category'] = calculate_abc_categories(df)
    
    # Calculate stockout risk
    df['stockout_risk_score'] = np.where(
        df['current_stock'] <= df['reorder_point'],
        100,  # High risk
        np.where(
            df['current_stock'] <= df['reorder_point'] * 1.5,
            50,   # Medium risk
            0     # Low risk
        )
    )
    
    # Calculate space utilization
    df['space_utilization'] = (df['current_stock'] / df['storage_volume']) * 100
    df['space_utilization'] = df['space_utilization'].clip(0, 100)
    
    # Calculate pick efficiency
    if df['pick_time'].max() > 0:
        df['pick_efficiency'] = ((df['pick_time'].max() - df['pick_time']) / df['pick_time'].max()) * 100
    else:
        df['pick_efficiency'] = 0
    
    # Calculate supplier risk
    df['supplier_risk_score'] = calculate_supplier_risk_score(df)
    
    # Calculate EOQ
    df['eoq'] = calculate_eoq(df)
    
    # Calculate optimal pick time
    df['optimal_pick_time'] = df['pick_time'] * 0.8  # Assume 20% improvement potential
    df['optimal_route'] = df['pick_route']  # For now, same as current
    
    # Calculate daily demand (simplified)
    df['daily_demand'] = df['quantity'] / 30  # Assume monthly data
    
    return df

def calculate_abc_categories(df):
    """
    Calculate ABC categories based on stock value.
    
    Args:
        df (pd.DataFrame): Inventory data with stock_value column
    
    Returns:
        pd.Series: ABC categories
    """
    if 'stock_value' not in df.columns:
        return pd.Series(['C'] * len(df))
    
    # Sort by stock value
    sorted_df = df.sort_values('stock_value', ascending=False)
    
    # Calculate cumulative percentage
    total_value = sorted_df['stock_value'].sum()
    sorted_df['cumulative_percentage'] = (sorted_df['stock_value'].cumsum() / total_value) * 100
    
    # Assign categories
    categories = pd.Series(['C'] * len(df), index=df.index)
    categories.loc[sorted_df[sorted_df['cumulative_percentage'] <= 80].index] = 'A'
    categories.loc[sorted_df[(sorted_df['cumulative_percentage'] > 80) & 
                             (sorted_df['cumulative_percentage'] <= 95)].index] = 'B'
    
    return categories

def calculate_supplier_risk_score(df):
    """
    Calculate supplier risk score based on performance metrics.
    
    Args:
        df (pd.DataFrame): Inventory data with supplier metrics
    
    Returns:
        pd.Series: Supplier risk scores
    """
    risk_score = pd.Series(0.0, index=df.index)
    
    # Performance risk
    if 'supplier_performance' in df.columns:
        performance_risk = (100 - df['supplier_performance']) * 0.4
        risk_score += performance_risk
    
    # Lead time risk
    if 'lead_time' in df.columns:
        lead_time_risk = (df['lead_time'] / df['lead_time'].max()) * 30
        risk_score += lead_time_risk
    
    # Quality risk
    if 'quality_score' in df.columns:
        quality_risk = (100 - df['quality_score']) * 0.3
        risk_score += quality_risk
    
    return risk_score

def calculate_eoq(df):
    """
    Calculate Economic Order Quantity.
    
    Args:
        df (pd.DataFrame): Inventory data
    
    Returns:
        pd.Series: EOQ values
    """
    if 'quantity' not in df.columns or 'unit_cost' not in df.columns:
        return pd.Series(0, index=df.index)
    
    # Simplified EOQ calculation
    # EOQ = sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
    
    annual_demand = df['quantity'] * 12  # Assume monthly data
    ordering_cost = 50  # Fixed ordering cost
    holding_cost_per_unit = df['unit_cost'] * 0.2  # 20% holding cost rate
    
    eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
    eoq = eoq.fillna(0)
    eoq = eoq.replace([np.inf, -np.inf], 0)
    
    return eoq.round(0)

# ============================================================================
# DATA VALIDATION AND CLEANING
# ============================================================================

def validate_inventory_data(df):
    """
    Validate inventory data for required fields and data quality.
    
    Args:
        df (pd.DataFrame): Inventory data to validate
    
    Returns:
        dict: Validation results
    """
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'missing_fields': [],
        'data_quality_score': 0
    }
    
    if df.empty:
        validation_results['is_valid'] = False
        validation_results['errors'].append("Dataset is empty")
        return validation_results
    
    # Required fields
    required_fields = ['item_id', 'item_name', 'current_stock']
    missing_fields = [field for field in required_fields if field not in df.columns]
    
    if missing_fields:
        validation_results['missing_fields'] = missing_fields
        validation_results['warnings'].append(f"Missing required fields: {missing_fields}")
    
    # Data quality checks
    quality_score = 0
    total_checks = 0
    
    # Check for duplicate item IDs
    if 'item_id' in df.columns:
        total_checks += 1
        if df['item_id'].duplicated().any():
            validation_results['warnings'].append("Duplicate item IDs found")
        else:
            quality_score += 1
    
    # Check for negative stock levels
    if 'current_stock' in df.columns:
        total_checks += 1
        if (df['current_stock'] < 0).any():
            validation_results['errors'].append("Negative stock levels found")
        else:
            quality_score += 1
    
    # Check for negative costs
    if 'unit_cost' in df.columns:
        total_checks += 1
        if (df['unit_cost'] < 0).any():
            validation_results['errors'].append("Negative unit costs found")
        else:
            quality_score += 1
    
    # Check for missing values in critical fields
    critical_fields = ['item_name', 'current_stock']
    for field in critical_fields:
        if field in df.columns:
            total_checks += 1
            missing_count = df[field].isna().sum()
            if missing_count > 0:
                validation_results['warnings'].append(f"{missing_count} missing values in {field}")
            else:
                quality_score += 1
    
    # Calculate overall quality score
    if total_checks > 0:
        validation_results['data_quality_score'] = (quality_score / total_checks) * 100
    
    # Determine if data is valid
    if validation_results['errors']:
        validation_results['is_valid'] = False
    
    return validation_results

def clean_inventory_data(df):
    """
    Clean and prepare inventory data for analysis.
    
    Args:
        df (pd.DataFrame): Raw inventory data
    
    Returns:
        pd.DataFrame: Cleaned data
    """
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    if 'current_stock' in df_clean.columns:
        df_clean['current_stock'] = df_clean['current_stock'].fillna(0)
    
    if 'unit_cost' in df_clean.columns:
        df_clean['unit_cost'] = df_clean['unit_cost'].fillna(0)
    
    if 'reorder_point' in df_clean.columns:
        df_clean['reorder_point'] = df_clean['reorder_point'].fillna(0)
    
    # Ensure non-negative values
    numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        if col in ['current_stock', 'unit_cost', 'reorder_point', 'max_stock']:
            df_clean[col] = df_clean[col].clip(lower=0)
    
    # Clean text fields
    if 'item_name' in df_clean.columns:
        df_clean['item_name'] = df_clean['item_name'].astype(str).str.strip()
    
    if 'category' in df_clean.columns:
        df_clean['category'] = df_clean['category'].astype(str).str.strip()
    
    # Convert date columns
    if 'date' in df_clean.columns:
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    
    return df_clean

# ============================================================================
# DATA EXPORT AND TEMPLATE GENERATION
# ============================================================================

def create_inventory_template():
    """
    Create an Excel template for inventory data.
    
    Returns:
        bytes: Excel file content
    """
    # Create empty DataFrames with the correct schema
    inventory_template = pd.DataFrame(columns=[
        'item_id', 'item_name', 'category', 'description', 'supplier_id',
        'warehouse_location', 'current_stock', 'reorder_point', 'max_stock',
        'unit_cost', 'holding_cost_rate', 'turnover_rate', 'forecast_accuracy',
        'quantity', 'date', 'seasonality_score', 'demand_volatility',
        'supplier_performance', 'lead_time', 'quality_score', 'on_time_delivery',
        'storage_volume', 'pick_time', 'pick_route'
    ])
    
    # Add sample data row for reference
    sample_row = {
        'item_id': 'ITEM_0001',
        'item_name': 'Sample Item',
        'category': 'Electronics',
        'description': 'Sample description',
        'supplier_id': 'Sample Supplier',
        'warehouse_location': 'Main Warehouse',
        'current_stock': 100,
        'reorder_point': 20,
        'max_stock': 200,
        'unit_cost': 25.50,
        'holding_cost_rate': 20.0,
        'turnover_rate': 6.0,
        'forecast_accuracy': 85.0,
        'quantity': 50,
        'date': datetime.now(),
        'seasonality_score': 0.3,
        'demand_volatility': 0.4,
        'supplier_performance': 85.0,
        'lead_time': 14,
        'quality_score': 95.0,
        'on_time_delivery': 92.0,
        'storage_volume': 10,
        'pick_time': 5.0,
        'pick_route': 'Route_1'
    }
    
    inventory_template = pd.concat([inventory_template, pd.DataFrame([sample_row])], ignore_index=True)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write template
        inventory_template.to_excel(writer, sheet_name='Inventory_Template', index=False)
        
        # Add instructions sheet
        instructions_data = {
            'Field Name': [
                'item_id', 'item_name', 'category', 'description', 'supplier_id',
                'warehouse_location', 'current_stock', 'reorder_point', 'max_stock',
                'unit_cost', 'holding_cost_rate', 'turnover_rate', 'forecast_accuracy',
                'quantity', 'date', 'seasonality_score', 'demand_volatility',
                'supplier_performance', 'lead_time', 'quality_score', 'on_time_delivery',
                'storage_volume', 'pick_time', 'pick_route'
            ],
            'Required': [
                'Yes', 'Yes', 'No', 'No', 'No',
                'No', 'Yes', 'No', 'No',
                'No', 'No', 'No', 'No',
                'No', 'No', 'No', 'No',
                'No', 'No', 'No', 'No',
                'No', 'No', 'No'
            ],
            'Data Type': [
                'Text', 'Text', 'Text', 'Text', 'Text',
                'Text', 'Number', 'Number', 'Number',
                'Number', 'Number', 'Number', 'Number',
                'Number', 'Date', 'Number', 'Number',
                'Number', 'Number', 'Number', 'Number',
                'Number', 'Number', 'Text'
            ],
            'Description': [
                'Unique identifier for the item',
                'Name or description of the item',
                'Category classification',
                'Detailed description',
                'Supplier identifier',
                'Warehouse location',
                'Current stock level',
                'Reorder point threshold',
                'Maximum stock level',
                'Unit cost in currency',
                'Annual holding cost rate (%)',
                'Annual turnover rate',
                'Forecast accuracy percentage',
                'Demand quantity',
                'Date of record',
                'Seasonality score (0-1)',
                'Demand volatility measure',
                'Supplier performance score',
                'Lead time in days',
                'Quality score (0-100)',
                'On-time delivery percentage',
                'Storage volume requirement',
                'Pick time in minutes',
                'Pick route identifier'
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    output.seek(0)
    return output.getvalue()

def export_inventory_data(df, format_type='excel'):
    """
    Export inventory data in various formats.
    
    Args:
        df (pd.DataFrame): Inventory data to export
        format_type (str): Export format ('excel', 'csv', 'json')
    
    Returns:
        bytes: Exported file content
    """
    if df.empty:
        return None
    
    if format_type.lower() == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Inventory_Data', index=False)
            
            # Add summary sheet
            summary_data = {
                'Metric': ['Total Items', 'Total Value', 'Average Turnover', 'Stockout Risk Items'],
                'Value': [
                    len(df),
                    df['current_stock'].sum() if 'current_stock' in df.columns else 0,
                    df['turnover_rate'].mean() if 'turnover_rate' in df.columns else 0,
                    len(df[df['current_stock'] <= df['reorder_point']]) if 'reorder_point' in df.columns else 0
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    elif format_type.lower() == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    
    elif format_type.lower() == 'json':
        return df.to_json(orient='records', indent=2).encode('utf-8')
    
    else:
        raise ValueError(f"Unsupported format: {format_type}")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_inventory_summary_stats(df):
    """
    Get summary statistics for inventory data.
    
    Args:
        df (pd.DataFrame): Inventory data
    
    Returns:
        dict: Summary statistics
    """
    if df.empty:
        return {}
    
    summary = {}
    
    # Basic counts
    summary['total_items'] = len(df)
    summary['unique_categories'] = df['category'].nunique() if 'category' in df.columns else 0
    summary['unique_suppliers'] = df['supplier_id'].nunique() if 'supplier_id' in df.columns else 0
    
    # Stock metrics
    if 'current_stock' in df.columns:
        summary['total_stock'] = df['current_stock'].sum()
        summary['avg_stock'] = df['current_stock'].mean()
        summary['stockout_items'] = len(df[df['current_stock'] == 0])
    
    # Cost metrics
    if 'unit_cost' in df.columns:
        summary['total_value'] = (df['current_stock'] * df['unit_cost']).sum() if 'current_stock' in df.columns else 0
        summary['avg_unit_cost'] = df['unit_cost'].mean()
        summary['highest_cost_item'] = df.loc[df['unit_cost'].idxmax(), 'item_name'] if 'item_name' in df.columns else 'N/A'
    
    # Performance metrics
    if 'turnover_rate' in df.columns:
        summary['avg_turnover'] = df['turnover_rate'].mean()
        summary['high_turnover_items'] = len(df[df['turnover_rate'] > 8])
    
    # ABC analysis
    if 'abc_category' in df.columns:
        abc_counts = df['abc_category'].value_counts()
        summary['abc_distribution'] = abc_counts.to_dict()
    
    return summary

def filter_inventory_data(df, filters=None):
    """
    Filter inventory data based on specified criteria.
    
    Args:
        df (pd.DataFrame): Inventory data
        filters (dict): Filter criteria
    
    Returns:
        pd.DataFrame: Filtered data
    """
    if df.empty or not filters:
        return df
    
    filtered_df = df.copy()
    
    for field, value in filters.items():
        if field in filtered_df.columns:
            if isinstance(value, (list, tuple)):
                filtered_df = filtered_df[filtered_df[field].isin(value)]
            elif isinstance(value, dict):
                if 'min' in value:
                    filtered_df = filtered_df[filtered_df[field] >= value['min']]
                if 'max' in value:
                    filtered_df = filtered_df[filtered_df[field] <= value['max']]
            else:
                filtered_df = filtered_df[filtered_df[field] == value]
    
    return filtered_df

def sort_inventory_data(df, sort_by=None, ascending=True):
    """
    Sort inventory data by specified columns.
    
    Args:
        df (pd.DataFrame): Inventory data
        sort_by (str or list): Column(s) to sort by
        ascending (bool or list): Sort order
    
    Returns:
        pd.DataFrame: Sorted data
    """
    if df.empty or not sort_by:
        return df
    
    return df.sort_values(by=sort_by, ascending=ascending)

# Import io for Excel export
import io

def create_comprehensive_inventory_template():
    """Create a comprehensive Excel template with multiple sheets for inventory management."""
    
    # Create main inventory items template
    inventory_template = pd.DataFrame(columns=[
        'item_id', 'item_name', 'category', 'description', 'sku', 'barcode',
        'current_stock', 'reorder_point', 'max_stock', 'min_stock', 'unit_cost',
        'holding_cost_rate', 'supplier_id', 'supplier_name', 'lead_time',
        'warehouse_location', 'storage_volume', 'pick_route', 'pick_time',
        'turnover_rate', 'forecast_accuracy', 'seasonality_score', 'abc_category',
        'last_updated', 'status'
    ])
    
    # Add sample inventory item
    inventory_template.loc[0] = [
        'INV001', 'Laptop Computer', 'Electronics', 'High-performance laptop for business use', 
        'LAP001', '1234567890123', 50, 10, 100, 5, 899.99, 0.25, 'SUP001', 
        'Tech Supplies Inc.', 7, 'Warehouse A', 0.5, 'Route A', 3.0, 12.5, 
        0.85, 0.3, 'A', datetime.now(), 'Active'
    ]
    
    # Create suppliers template
    suppliers_template = pd.DataFrame(columns=[
        'supplier_id', 'supplier_name', 'contact_person', 'email', 'phone',
        'address', 'rating', 'performance_score', 'lead_time_avg', 'status'
    ])
    
    # Add sample supplier
    suppliers_template.loc[0] = [
        'SUP001', 'Tech Supplies Inc.', 'John Smith', 'john@techsupplies.com',
        '+1-555-0123', '123 Tech Street, Tech City, TC 12345', 'A', 95, 7, 'Active'
    ]
    
    # Create transactions template
    transactions_template = pd.DataFrame(columns=[
        'transaction_id', 'item_id', 'transaction_type', 'quantity', 'unit_cost',
        'transaction_date', 'reference', 'notes', 'user_id', 'location'
    ])
    
    # Add sample transaction
    transactions_template.loc[0] = [
        'TXN001', 'INV001', 'In', 100, 899.99, datetime.now(), 'PO-2024-001',
        'Initial stock order', 'USER001', 'Warehouse A'
    ]
    
    # Create locations template
    locations_template = pd.DataFrame(columns=[
        'location_id', 'location_name', 'location_type', 'address', 'capacity',
        'manager', 'phone', 'status'
    ])
    
    # Add sample location
    locations_template.loc[0] = [
        'LOC001', 'Warehouse A', 'Warehouse', '456 Warehouse Blvd, City, ST 12345',
        10000, 'Jane Manager', '+1-555-0456', 'Active'
    ]
    
    # Create instructions template
    instructions_data = {
        'Sheet Name': ['Inventory_Items', 'Suppliers', 'Transactions', 'Locations'],
        'Purpose': [
            'Main inventory catalog with all item details',
            'Supplier information and performance metrics',
            'Stock movement and transaction history',
            'Warehouse and storage location details'
        ],
        'Key Fields': [
            'item_id, item_name, category, current_stock, reorder_point, unit_cost',
            'supplier_id, supplier_name, contact_person, performance_score',
            'transaction_id, item_id, transaction_type, quantity, date',
            'location_id, location_name, location_type, capacity, manager'
        ],
        'Required Fields': [
            'item_id, item_name, current_stock, unit_cost',
            'supplier_id, supplier_name',
            'transaction_id, item_id, quantity, date',
            'location_id, location_name'
        ]
    }
    instructions_template = pd.DataFrame(instructions_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each template to a separate sheet
        inventory_template.to_excel(writer, sheet_name='Inventory_Items', index=False)
        suppliers_template.to_excel(writer, sheet_name='Suppliers', index=False)
        transactions_template.to_excel(writer, sheet_name='Transactions', index=False)
        locations_template.to_excel(writer, sheet_name='Locations', index=False)
        instructions_template.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Get the workbook for formatting
        workbook = writer.book
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        # Apply formatting to headers
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for col_num, value in enumerate(writer.sheets[sheet_name].get_worksheet().table.columns):
                worksheet.write(0, col_num, value.name, header_format)
                worksheet.set_column(col_num, col_num, 15)  # Set column width
        
        # Add instructions sheet formatting
        instructions_worksheet = writer.sheets['Instructions']
        instructions_worksheet.set_column(0, 0, 15)  # Sheet Name
        instructions_worksheet.set_column(1, 1, 30)  # Purpose
        instructions_worksheet.set_column(2, 2, 40)  # Key Fields
        instructions_worksheet.set_column(3, 3, 25)  # Required Fields
    
    output.seek(0)
    return output.getvalue()

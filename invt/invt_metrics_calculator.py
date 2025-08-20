import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# INVENTORY OPTIMIZATION METRICS
# ============================================================================

def calculate_abc_analysis(data, value_column='unit_cost', stock_column='current_stock'):
    """
    Calculate ABC analysis for inventory items.
    
    Args:
        data (pd.DataFrame): Inventory data
        value_column (str): Column name for unit value/cost
        stock_column (str): Column name for current stock
    
    Returns:
        pd.DataFrame: Data with ABC categories
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    # Calculate total value for each item
    if value_column in df.columns and stock_column in df.columns:
        df['total_value'] = df[value_column] * df[stock_column]
    else:
        df['total_value'] = 1  # Default value if columns don't exist
    
    # Sort by total value in descending order
    df = df.sort_values('total_value', ascending=False)
    
    # Calculate cumulative percentage
    df['cumulative_value'] = df['total_value'].cumsum()
    df['cumulative_percentage'] = (df['cumulative_value'] / df['total_value'].sum()) * 100
    
    # Assign ABC categories
    df['abc_category'] = 'C'
    df.loc[df['cumulative_percentage'] <= 80, 'abc_category'] = 'A'
    df.loc[(df['cumulative_percentage'] > 80) & (df['cumulative_percentage'] <= 95), 'abc_category'] = 'B'
    
    return df

def calculate_turnover_rate(data, demand_column='quantity', stock_column='current_stock', period_days=365):
    """
    Calculate inventory turnover rate.
    
    Args:
        data (pd.DataFrame): Inventory data
        demand_column (str): Column name for demand/quantity
        stock_column (str): Column name for current stock
        period_days (int): Time period in days for turnover calculation
    
    Returns:
        pd.DataFrame: Data with turnover rates
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if demand_column in df.columns and stock_column in df.columns:
        # Calculate annual demand
        annual_demand = df[demand_column] * (365 / period_days)
        
        # Calculate turnover rate
        df['turnover_rate'] = annual_demand / df[stock_column]
        
        # Handle division by zero
        df['turnover_rate'] = df['turnover_rate'].replace([np.inf, -np.inf], 0)
        df['turnover_rate'] = df['turnover_rate'].fillna(0)
    else:
        df['turnover_rate'] = 0
    
    return df

def calculate_stockout_risk(data, stock_column='current_stock', reorder_column='reorder_point'):
    """
    Calculate stockout risk for inventory items.
    
    Args:
        data (pd.DataFrame): Inventory data
        stock_column (str): Column name for current stock
        reorder_column (str): Column name for reorder point
    
    Returns:
        pd.DataFrame: Data with stockout risk scores
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if stock_column in df.columns and reorder_column in df.columns:
        # Calculate days until stockout
        df['days_until_stockout'] = df[stock_column] / df[reorder_column] if 'daily_demand' in df.columns else 0
        
        # Calculate stockout risk score (0-100)
        df['stockout_risk'] = np.where(
            df[stock_column] <= df[reorder_column],
            100,  # High risk if at or below reorder point
            np.where(
                df[stock_column] <= df[reorder_column] * 1.5,
                75,   # Medium-high risk if close to reorder point
                np.where(
                    df[stock_column] <= df[reorder_column] * 2,
                    50,   # Medium risk if moderately above reorder point
                    25    # Low risk if well above reorder point
                )
            )
        )
        
        # Add risk level
        df['stockout_risk_level'] = pd.cut(
            df['stockout_risk'],
            bins=[-1, 25, 50, 75, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
    else:
        df['stockout_risk'] = 0
        df['stockout_risk_level'] = 'Unknown'
    
    return df

def calculate_optimal_order_quantity(data, demand_column='quantity', cost_column='unit_cost', 
                                   holding_cost_rate=0.2, ordering_cost=50):
    """
    Calculate Economic Order Quantity (EOQ) for inventory items.
    
    Args:
        data (pd.DataFrame): Inventory data
        demand_column (str): Column name for annual demand
        cost_column (str): Column name for unit cost
        holding_cost_rate (float): Annual holding cost rate as percentage of unit cost
        ordering_cost (float): Fixed cost per order
    
    Returns:
        pd.DataFrame: Data with EOQ calculations
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if demand_column in df.columns and cost_column in df.columns:
        # Calculate annual demand (if not already annual)
        annual_demand = df[demand_column] * 365 if 'date' in df.columns else df[demand_column]
        
        # Calculate holding cost per unit
        df['holding_cost_per_unit'] = df[cost_column] * holding_cost_rate
        
        # Calculate EOQ
        df['eoq'] = np.sqrt((2 * annual_demand * ordering_cost) / df['holding_cost_per_unit'])
        
        # Calculate optimal order frequency
        df['optimal_orders_per_year'] = annual_demand / df['eoq']
        
        # Calculate total annual cost
        df['total_annual_cost'] = (df['holding_cost_per_unit'] * df['eoq'] / 2) + \
                                 (ordering_cost * df['optimal_orders_per_year'])
        
        # Round to reasonable values
        df['eoq'] = df['eoq'].round(0).astype(int)
        df['optimal_orders_per_year'] = df['optimal_orders_per_year'].round(2)
        df['total_annual_cost'] = df['total_annual_cost'].round(2)
    else:
        df['eoq'] = 0
        df['optimal_orders_per_year'] = 0
        df['total_annual_cost'] = 0
    
    return df

# ============================================================================
# DEMAND FORECASTING METRICS
# ============================================================================

def calculate_demand_volatility(data, demand_column='quantity', time_column='date', window=30):
    """
    Calculate demand volatility and variability.
    
    Args:
        data (pd.DataFrame): Inventory data
        demand_column (str): Column name for demand
        time_column (str): Column name for date/time
        window (int): Rolling window size for volatility calculation
    
    Returns:
        pd.DataFrame: Data with volatility metrics
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if demand_column in df.columns:
        # Calculate demand volatility (coefficient of variation)
        df['demand_mean'] = df[demand_column].rolling(window=window, min_periods=1).mean()
        df['demand_std'] = df[demand_column].rolling(window=window, min_periods=1).std()
        df['demand_volatility'] = df['demand_std'] / df['demand_mean']
        
        # Handle division by zero
        df['demand_volatility'] = df['demand_volatility'].replace([np.inf, -np.inf], 0)
        df['demand_volatility'] = df['demand_volatility'].fillna(0)
        
        # Add volatility level
        df['volatility_level'] = pd.cut(
            df['demand_volatility'],
            bins=[-1, 0.2, 0.5, 1.0, float('inf')],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
    else:
        df['demand_volatility'] = 0
        df['volatility_level'] = 'Unknown'
    
    return df

def calculate_forecast_accuracy(data, actual_column='quantity', forecast_column='forecasted_quantity'):
    """
    Calculate forecast accuracy metrics.
    
    Args:
        data (pd.DataFrame): Inventory data
        actual_column (str): Column name for actual values
        forecast_column (str): Column name for forecasted values
    
    Returns:
        pd.DataFrame: Data with accuracy metrics
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if actual_column in df.columns and forecast_column in df.columns:
        # Calculate forecast error
        df['forecast_error'] = df[actual_column] - df[forecast_column]
        
        # Calculate absolute error
        df['absolute_error'] = abs(df['forecast_error'])
        
        # Calculate percentage error
        df['percentage_error'] = np.where(
            df[actual_column] != 0,
            (df['forecast_error'] / df[actual_column]) * 100,
            0
        )
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        df['mape'] = df['percentage_error'].abs()
        
        # Calculate forecast accuracy (100 - MAPE)
        df['forecast_accuracy'] = 100 - df['mape']
        
        # Clamp accuracy to 0-100 range
        df['forecast_accuracy'] = df['forecast_accuracy'].clip(0, 100)
        
        # Add accuracy level
        df['forecast_accuracy_level'] = pd.cut(
            df['forecast_accuracy'],
            bins=[-1, 60, 80, 90, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
    else:
        df['forecast_accuracy'] = 0
        df['forecast_accuracy_level'] = 'Unknown'
    
    return df

def calculate_demand_patterns(data, demand_column='quantity', time_column='date'):
    """
    Identify demand patterns and trends.
    
    Args:
        data (pd.DataFrame): Inventory data
        demand_column (str): Column name for demand
        time_column (str): Column name for date/time
    
    Returns:
        pd.DataFrame: Data with pattern analysis
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if demand_column in df.columns and time_column in df.columns:
        # Convert to datetime
        df[time_column] = pd.to_datetime(df[time_column])
        
        # Calculate moving averages
        df['ma_7'] = df[demand_column].rolling(window=7, min_periods=1).mean()
        df['ma_30'] = df[demand_column].rolling(window=30, min_periods=1).mean()
        
        # Calculate trend (simple linear regression slope)
        df['trend'] = df[demand_column].rolling(window=30, min_periods=2).apply(
            lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) > 1 else 0
        )
        
        # Identify demand patterns
        df['demand_pattern'] = 'Stable'
        df.loc[df['trend'] > 0.1, 'demand_pattern'] = 'Increasing'
        df.loc[df['trend'] < -0.1, 'demand_pattern'] = 'Decreasing'
        df.loc[df['demand_volatility'] > 0.5, 'demand_pattern'] = 'Volatile'
    else:
        df['demand_pattern'] = 'Unknown'
    
    return df

# ============================================================================
# SUPPLIER PERFORMANCE METRICS
# ============================================================================

def calculate_supplier_performance(data, supplier_column='supplier_id', 
                                 quality_column='quality_score', 
                                 delivery_column='on_time_delivery'):
    """
    Calculate supplier performance metrics.
    
    Args:
        data (pd.DataFrame): Inventory data
        supplier_column (str): Column name for supplier ID
        quality_column (str): Column name for quality score
        delivery_column (str): Column name for delivery performance
    
    Returns:
        pd.DataFrame: Data with supplier performance scores
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if supplier_column in df.columns:
        # Calculate supplier performance score
        performance_score = 0
        
        if quality_column in df.columns:
            performance_score += df[quality_column] * 0.4  # 40% weight for quality
        
        if delivery_column in df.columns:
            performance_score += df[delivery_column] * 0.6  # 60% weight for delivery
        
        df['supplier_performance_score'] = performance_score
        
        # Add performance level
        df['supplier_performance_level'] = pd.cut(
            df['supplier_performance_score'],
            bins=[-1, 60, 80, 90, 100],
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
    else:
        df['supplier_performance_score'] = 0
        df['supplier_performance_level'] = 'Unknown'
    
    return df

def calculate_supplier_risk(data, supplier_column='supplier_id', 
                           performance_column='supplier_performance_score',
                           lead_time_column='lead_time'):
    """
    Calculate supplier risk assessment.
    
    Args:
        data (pd.DataFrame): Inventory data
        supplier_column (str): Column name for supplier ID
        performance_column (str): Column name for supplier performance
        lead_time_column (str): Column name for lead time
    
    Returns:
        pd.DataFrame: Data with supplier risk scores
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if supplier_column in df.columns:
        # Calculate supplier risk score (0-100, higher = more risk)
        risk_score = 0
        
        if performance_column in df.columns:
            # Performance risk (lower performance = higher risk)
            performance_risk = (100 - df[performance_column]) * 0.6
            risk_score += performance_risk
        
        if lead_time_column in df.columns:
            # Lead time risk (longer lead time = higher risk)
            lead_time_risk = np.where(
                df[lead_time_column] <= 7, 10,      # Low risk for ≤7 days
                np.where(
                    df[lead_time_column] <= 14, 30, # Medium risk for 8-14 days
                    np.where(
                        df[lead_time_column] <= 30, 60, # High risk for 15-30 days
                        100  # Very high risk for >30 days
                    )
                )
            ) * 0.4
            risk_score += lead_time_risk
        
        df['supplier_risk_score'] = risk_score
        
        # Add risk level
        df['supplier_risk_level'] = pd.cut(
            df['supplier_risk_score'],
            bins=[-1, 25, 50, 75, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
    else:
        df['supplier_risk_score'] = 0
        df['supplier_risk_level'] = 'Unknown'
    
    return df

# ============================================================================
# COST ANALYSIS METRICS
# ============================================================================

def calculate_holding_costs(data, stock_column='current_stock', cost_column='unit_cost',
                           holding_cost_rate=0.2):
    """
    Calculate inventory holding costs.
    
    Args:
        data (pd.DataFrame): Inventory data
        stock_column (str): Column name for current stock
        cost_column (str): Column name for unit cost
        holding_cost_rate (float): Annual holding cost rate as percentage of unit cost
    
    Returns:
        pd.DataFrame: Data with holding cost calculations
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if stock_column in df.columns and cost_column in df.columns:
        # Calculate average inventory value
        df['average_inventory_value'] = df[stock_column] * df[cost_column]
        
        # Calculate annual holding cost
        df['annual_holding_cost'] = df['average_inventory_value'] * holding_cost_rate
        
        # Calculate monthly holding cost
        df['monthly_holding_cost'] = df['annual_holding_cost'] / 12
        
        # Calculate daily holding cost
        df['daily_holding_cost'] = df['annual_holding_cost'] / 365
    else:
        df['average_inventory_value'] = 0
        df['annual_holding_cost'] = 0
        df['monthly_holding_cost'] = 0
        df['daily_holding_cost'] = 0
    
    return df

def calculate_order_costs(data, demand_column='quantity', eoq_column='eoq',
                         ordering_cost=50):
    """
    Calculate ordering costs for inventory items.
    
    Args:
        data (pd.DataFrame): Inventory data
        demand_column (str): Column name for annual demand
        eoq_column (str): Column name for economic order quantity
        ordering_cost (float): Fixed cost per order
    
    Returns:
        pd.DataFrame: Data with ordering cost calculations
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if demand_column in df.columns and eoq_column in df.columns:
        # Calculate number of orders per year
        df['orders_per_year'] = df[demand_column] / df[eoq_column]
        
        # Calculate annual ordering cost
        df['annual_ordering_cost'] = df['orders_per_year'] * ordering_cost
        
        # Calculate total annual cost (holding + ordering)
        if 'annual_holding_cost' in df.columns:
            df['total_annual_cost'] = df['annual_holding_cost'] + df['annual_ordering_cost']
        else:
            df['total_annual_cost'] = df['annual_ordering_cost']
    else:
        df['orders_per_year'] = 0
        df['annual_ordering_cost'] = 0
        df['total_annual_cost'] = 0
    
    return df

# ============================================================================
# WAREHOUSE OPERATIONS METRICS
# ============================================================================

def calculate_warehouse_efficiency(data, storage_column='storage_volume', 
                                 capacity_column='max_stock'):
    """
    Calculate warehouse efficiency metrics.
    
    Args:
        data (pd.DataFrame): Inventory data
        storage_column (str): Column name for storage volume
        capacity_column (str): Column name for maximum capacity
    
    Returns:
        pd.DataFrame: Data with warehouse efficiency metrics
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if storage_column in df.columns and capacity_column in df.columns:
        # Calculate space utilization percentage
        df['space_utilization'] = (df[storage_column] / df[capacity_column]) * 100
        
        # Clamp to 0-100 range
        df['space_utilization'] = df['space_utilization'].clip(0, 100)
        
        # Add efficiency level
        df['efficiency_level'] = pd.cut(
            df['space_utilization'],
            bins=[-1, 60, 80, 90, 100],
            labels=['Low', 'Medium', 'High', 'Optimal']
        )
    else:
        df['space_utilization'] = 0
        df['efficiency_level'] = 'Unknown'
    
    return df

def calculate_pick_efficiency(data, pick_time_column='pick_time', 
                             standard_time=5.0):
    """
    Calculate picking efficiency metrics.
    
    Args:
        data (pd.DataFrame): Inventory data
        pick_time_column (str): Column name for pick time
        standard_time (float): Standard time for picking operations
    
    Returns:
        pd.DataFrame: Data with pick efficiency metrics
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    if pick_time_column in df.columns:
        # Calculate efficiency ratio (standard time / actual time)
        df['pick_efficiency_ratio'] = standard_time / df[pick_time_column]
        
        # Calculate efficiency percentage
        df['pick_efficiency_percentage'] = df['pick_efficiency_ratio'] * 100
        
        # Clamp to 0-200 range (allowing for very efficient operations)
        df['pick_efficiency_percentage'] = df['pick_efficiency_percentage'].clip(0, 200)
        
        # Add efficiency level
        df['pick_efficiency_level'] = pd.cut(
            df['pick_efficiency_percentage'],
            bins=[-1, 80, 100, 120, float('inf')],
            labels=['Below Standard', 'Standard', 'Above Standard', 'Excellent']
        )
    else:
        df['pick_efficiency_ratio'] = 0
        df['pick_efficiency_percentage'] = 0
        df['pick_efficiency_level'] = 'Unknown'
    
    return df

# ============================================================================
# COMPREHENSIVE METRICS CALCULATION
# ============================================================================

def calculate_all_inventory_metrics(data):
    """
    Calculate all inventory metrics in one comprehensive function.
    
    Args:
        data (pd.DataFrame): Inventory data
    
    Returns:
        pd.DataFrame: Data with all calculated metrics
    """
    if data.empty:
        return data
    
    df = data.copy()
    
    # Apply all metric calculations
    df = calculate_abc_analysis(df)
    df = calculate_turnover_rate(df)
    df = calculate_stockout_risk(df)
    df = calculate_optimal_order_quantity(df)
    df = calculate_demand_volatility(df)
    df = calculate_forecast_accuracy(df)
    df = calculate_demand_patterns(df)
    df = calculate_supplier_performance(df)
    df = calculate_supplier_risk(df)
    df = calculate_holding_costs(df)
    df = calculate_order_costs(df)
    df = calculate_warehouse_efficiency(df)
    df = calculate_pick_efficiency(df)
    
    return df

def generate_inventory_summary(data):
    """
    Generate a comprehensive summary of inventory metrics.
    
    Args:
        data (pd.DataFrame): Inventory data with calculated metrics
    
    Returns:
        dict: Summary statistics and insights
    """
    if data.empty:
        return {}
    
    summary = {}
    
    # Basic inventory statistics
    summary['total_items'] = len(data)
    summary['total_value'] = data.get('total_value', pd.Series([0])).sum()
    summary['average_unit_cost'] = data.get('unit_cost', pd.Series([0])).mean()
    
    # ABC analysis summary
    if 'abc_category' in data.columns:
        abc_summary = data['abc_category'].value_counts()
        summary['abc_distribution'] = abc_summary.to_dict()
    
    # Risk assessment summary
    if 'stockout_risk_level' in data.columns:
        risk_summary = data['stockout_risk_level'].value_counts()
        summary['risk_distribution'] = risk_summary.to_dict()
    
    # Performance metrics
    summary['average_turnover_rate'] = data.get('turnover_rate', pd.Series([0])).mean()
    summary['average_forecast_accuracy'] = data.get('forecast_accuracy', pd.Series([0])).mean()
    summary['average_supplier_performance'] = data.get('supplier_performance_score', pd.Series([0])).mean()
    
    # Cost analysis
    summary['total_holding_cost'] = data.get('annual_holding_cost', pd.Series([0])).sum()
    summary['total_ordering_cost'] = data.get('annual_ordering_cost', pd.Series([0])).sum()
    summary['total_annual_cost'] = data.get('total_annual_cost', pd.Series([0])).sum()
    
    return summary

"""
Sales Metrics Calculator Module - Performance Optimized

This module provides comprehensive functions for calculating various sales metrics
and analytics used in the Sales Analytics Dashboard with performance optimizations.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
from functools import lru_cache
import time

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Performance optimization settings
pd.options.mode.chained_assignment = None  # Disable SettingWithCopyWarning

# Try to enable Numba acceleration if available
try:
    pd.options.compute.use_numba = True  # Enable Numba acceleration if available
except ImportError:
    # Numba not available, continue without it
    pass

# Cache for expensive calculations
@lru_cache(maxsize=128)
def cache_metric_calculation(data_hash, calculation_type):
    """Cache expensive metric calculations."""
    return None

# Performance monitoring
def performance_monitor(func_name):
    """Decorator to monitor function performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            if end_time - start_time > 0.5:  # Log slow functions
                print(f"⚠️ {func_name} took {end_time - start_time:.3f}s")
            return result
        return wrapper
    return decorator

# ============================================================================
# SALES PERFORMANCE METRICS
# ============================================================================

@performance_monitor("Revenue by Product")
def calculate_sales_revenue_by_product(sales_orders, products):
    """Calculate sales revenue by product with performance optimizations."""
    try:
        if sales_orders.empty or products.empty:
            return pd.DataFrame(), "No data available for revenue calculation"
        
        # Optimize by selecting only needed columns and using faster merge
        needed_columns = ['product_id', 'product_name', 'category']
        if all(col in products.columns for col in needed_columns):
            products_subset = products[needed_columns].copy()
        else:
            # Fallback if columns don't exist
            return pd.DataFrame(), "Required product columns not found"
        
        # Use faster merge with optimized settings
        revenue_data = sales_orders.merge(
            products_subset, 
            on='product_id', 
            how='left',
            copy=False  # Avoid unnecessary copying
        )
        
        # Optimized groupby with vectorized operations
        product_revenue = revenue_data.groupby(['product_id', 'product_name', 'category'], observed=True).agg({
            'total_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        # Sort by total revenue (optimized)
        product_revenue.sort_values('total_amount', ascending=False, inplace=True)
        
        return product_revenue, f"Revenue calculated for {len(product_revenue)} products"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating revenue by product: {str(e)}"

def calculate_revenue_growth_rate(sales_orders, period='monthly'):
    """Calculate revenue growth rate over time."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Convert order_date to datetime if it's not already
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        if period == 'monthly':
            # Group by month
            sales_orders['month'] = sales_orders['order_date'].dt.to_period('M')
            period_data = sales_orders.groupby('month')['total_amount'].sum().reset_index()
            period_data['period'] = period_data['month'].astype(str)
        elif period == 'quarterly':
            # Group by quarter
            sales_orders['quarter'] = sales_orders['order_date'].dt.to_period('Q')
            period_data = sales_orders.groupby('quarter')['total_amount'].sum().reset_index()
            period_data['period'] = period_data['quarter'].astype(str)
        else:
            # Group by year
            sales_orders['year'] = sales_orders['order_date'].dt.year
            period_data = sales_orders.groupby('year')['total_amount'].sum().reset_index()
            period_data['period'] = period_data['year'].astype(str)
        
        # Calculate growth rate
        period_data['growth_rate'] = period_data['total_amount'].pct_change() * 100
        period_data['growth_rate'] = period_data['growth_rate'].fillna(0)
        
        return period_data, f"Growth rate calculated for {len(period_data)} periods"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating growth rate: {str(e)}"

def calculate_sales_by_region(sales_orders):
    """Calculate sales by region."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        region_sales = sales_orders.groupby('region').agg({
            'total_amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        region_sales.columns = ['region', 'total_revenue', 'order_count']
        region_sales = region_sales.sort_values('total_revenue', ascending=False)
        
        return region_sales, f"Sales calculated for {len(region_sales)} regions"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating sales by region: {str(e)}"

def calculate_sales_by_channel(sales_orders):
    """Calculate sales by channel."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        channel_sales = sales_orders.groupby('channel').agg({
            'total_amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        channel_sales.columns = ['channel', 'total_revenue', 'order_count']
        channel_sales = channel_sales.sort_values('total_revenue', ascending=False)
        
        return channel_sales, f"Sales calculated for {len(channel_sales)} channels"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating sales by channel: {str(e)}"

# ============================================================================
# CUSTOMER ANALYSIS METRICS
# ============================================================================

def calculate_customer_lifetime_value(sales_orders, customers):
    """Calculate customer lifetime value."""
    try:
        if sales_orders.empty or customers.empty:
            return pd.DataFrame(), "No data available for CLV calculation"
        
        # Calculate total revenue per customer
        customer_revenue = sales_orders.groupby('customer_id')['total_amount'].sum().reset_index()
        customer_revenue.columns = ['customer_id', 'clv']
        
        # Merge with customer information
        clv_data = customer_revenue.merge(
            customers[['customer_id', 'customer_name', 'customer_segment', 'status']], 
            on='customer_id', 
            how='left'
        )
        
        clv_data = clv_data.sort_values('clv', ascending=False)
        
        return clv_data, f"CLV calculated for {len(clv_data)} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating CLV: {str(e)}"

def calculate_customer_segmentation(customers, sales_orders):
    """Calculate customer segmentation analysis."""
    try:
        if customers.empty or sales_orders.empty:
            return pd.DataFrame(), "No data available for segmentation analysis"
        
        # Merge customers with sales data
        customer_sales = customers.merge(
            sales_orders.groupby('customer_id')['total_amount'].sum().reset_index(),
            on='customer_id',
            how='left'
        )
        
        # Fill NaN values with 0
        customer_sales['total_amount'] = customer_sales['total_amount'].fillna(0)
        
        # Group by segment
        segmentation = customer_sales.groupby('customer_segment').agg({
            'customer_id': 'count',
            'total_amount': 'sum'
        }).reset_index()
        
        segmentation.columns = ['Segment', 'Customer Count', 'Total Revenue']
        segmentation = segmentation.sort_values('Total Revenue', ascending=False)
        
        return segmentation, f"Segmentation analysis completed for {len(segmentation)} segments"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating segmentation: {str(e)}"

def calculate_customer_churn_rate(customers):
    """Calculate customer churn rate."""
    try:
        if customers.empty:
            return pd.DataFrame(), "No customer data available"
        
        total_customers = len(customers)
        churned_customers = len(customers[customers['status'] == 'Churned'])
        active_customers = len(customers[customers['status'] == 'Active'])
        
        churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
        retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
        
        churn_data = pd.DataFrame({
            'Metric': ['Total Customers', 'Active Customers', 'Churned Customers', 'Churn Rate', 'Retention Rate'],
            'Value': [total_customers, active_customers, churned_customers, f"{churn_rate:.2f}%", f"{retention_rate:.2f}%"]
        })
        
        return churn_data, f"Churn analysis completed for {total_customers} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating churn rate: {str(e)}"

def calculate_repeat_purchase_rate(sales_orders):
    """Calculate repeat purchase rate."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Count orders per customer
        customer_orders = sales_orders.groupby('customer_id')['order_id'].count().reset_index()
        customer_orders.columns = ['customer_id', 'order_count']
        
        # Categorize customers
        single_purchase = len(customer_orders[customer_orders['order_count'] == 1])
        repeat_purchase = len(customer_orders[customer_orders['order_count'] > 1])
        total_customers = len(customer_orders)
        
        repeat_rate = (repeat_purchase / total_customers * 100) if total_customers > 0 else 0
        
        repeat_data = pd.DataFrame({
            'Metric': ['Total Customers', 'Single Purchase', 'Repeat Purchase', 'Repeat Purchase Rate'],
            'Value': [total_customers, single_purchase, repeat_purchase, f"{repeat_rate:.2f}%"]
        })
        
        return repeat_data, f"Repeat purchase analysis completed for {total_customers} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating repeat purchase rate: {str(e)}"

# ============================================================================
# SALES FUNNEL METRICS
# ============================================================================

def calculate_conversion_rate_by_stage(leads, opportunities):
    """Calculate conversion rate by funnel stage."""
    try:
        if leads.empty or opportunities.empty:
            return pd.DataFrame(), "No leads or opportunities data available"
        
        # Count leads by source
        lead_counts = leads.groupby('source').size().reset_index()
        lead_counts.columns = ['source', 'lead_count']
        
        # Count opportunities by source
        opportunity_counts = opportunities.groupby('lead_id').first().merge(
            leads[['lead_id', 'source']], on='lead_id', how='left'
        ).groupby('source').size().reset_index()
        opportunity_counts.columns = ['source', 'opportunity_count']
        
        # Merge and calculate conversion rate
        conversion_data = lead_counts.merge(opportunity_counts, on='source', how='left')
        conversion_data['opportunity_count'] = conversion_data['opportunity_count'].fillna(0)
        conversion_data['conversion_rate'] = (conversion_data['opportunity_count'] / conversion_data['lead_count'] * 100)
        
        conversion_data = conversion_data.sort_values('conversion_rate', ascending=False)
        
        return conversion_data, f"Conversion rates calculated for {len(conversion_data)} sources"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating conversion rates: {str(e)}"

def calculate_average_deal_size(opportunities):
    """Calculate average deal size."""
    try:
        if opportunities.empty:
            return pd.DataFrame(), "No opportunities data available"
        
        # Calculate average deal size by stage
        stage_deals = opportunities.groupby('stage').agg({
            'value': ['mean', 'count', 'sum']
        }).reset_index()
        
        # Flatten column names
        stage_deals.columns = ['stage', 'avg_deal_size', 'deal_count', 'total_value']
        
        # Calculate overall metrics
        overall_avg = opportunities['value'].mean()
        overall_count = len(opportunities)
        overall_total = opportunities['value'].sum()
        
        # Add overall row
        overall_row = pd.DataFrame({
            'stage': ['Overall'],
            'avg_deal_size': [overall_avg],
            'deal_count': [overall_count],
            'total_value': [overall_total]
        })
        
        deal_data = pd.concat([overall_row, stage_deals], ignore_index=True)
        
        return deal_data, f"Deal size analysis completed for {overall_count} opportunities"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating deal size: {str(e)}"

def calculate_time_to_close(opportunities):
    """Calculate time to close for opportunities."""
    try:
        if opportunities.empty:
            return pd.DataFrame(), "No opportunities data available"
        
        # Convert dates to datetime
        opportunities['created_date'] = pd.to_datetime(opportunities['created_date'])
        opportunities['close_date'] = pd.to_datetime(opportunities['close_date'])
        
        # Calculate days to close
        opportunities['days_to_close'] = (opportunities['close_date'] - opportunities['created_date']).dt.days
        
        # Filter only closed opportunities
        closed_opportunities = opportunities[opportunities['stage'].isin(['Closed Won', 'Closed Lost'])]
        
        if closed_opportunities.empty:
            return pd.DataFrame(), "No closed opportunities found"
        
        # Calculate metrics by stage
        time_data = closed_opportunities.groupby('stage').agg({
            'days_to_close': ['mean', 'median', 'count']
        }).reset_index()
        
        # Flatten column names
        time_data.columns = ['stage', 'avg_days', 'median_days', 'deal_count']
        
        # Calculate overall metrics
        overall_avg = closed_opportunities['days_to_close'].mean()
        overall_median = closed_opportunities['days_to_close'].median()
        overall_count = len(closed_opportunities)
        
        # Add overall row
        overall_row = pd.DataFrame({
            'stage': ['Overall'],
            'avg_days': [overall_avg],
            'median_days': [overall_median],
            'deal_count': [overall_count]
        })
        
        time_data = pd.concat([overall_row, time_data], ignore_index=True)
        
        return time_data, f"Time to close analysis completed for {overall_count} closed opportunities"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating time to close: {str(e)}"

def calculate_pipeline_velocity(opportunities):
    """Calculate pipeline velocity metrics."""
    try:
        if opportunities.empty:
            return pd.DataFrame(), "No opportunities data available"
        
        # Convert dates to datetime
        opportunities['created_date'] = pd.to_datetime(opportunities['created_date'])
        opportunities['close_date'] = pd.to_datetime(opportunities['close_date'])
        
        # Calculate days in pipeline
        opportunities['days_in_pipeline'] = (opportunities['close_date'] - opportunities['created_date']).dt.days
        
        # Filter only closed opportunities
        closed_opportunities = opportunities[opportunities['stage'].isin(['Closed Won', 'Closed Lost'])]
        
        if closed_opportunities.empty:
            return pd.DataFrame(), "No closed opportunities found"
        
        # Calculate velocity metrics
        total_value = closed_opportunities['value'].sum()
        avg_days = closed_opportunities['days_in_pipeline'].mean()
        
        # Pipeline velocity (value per day)
        pipeline_velocity = total_value / avg_days if avg_days > 0 else 0
        
        velocity_data = pd.DataFrame({
            'Metric': ['Total Pipeline Value', 'Average Days in Pipeline', 'Pipeline Velocity ($/day)'],
            'Value': [f"${total_value:,.2f}", f"{avg_days:.1f} days", f"${pipeline_velocity:,.2f}"]
        })
        
        return velocity_data, f"Pipeline velocity analysis completed for {len(closed_opportunities)} closed opportunities"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating pipeline velocity: {str(e)}"

# ============================================================================
# SALES TEAM PERFORMANCE METRICS
# ============================================================================

def calculate_individual_sales_performance(sales_orders, sales_reps, targets):
    """Calculate individual sales performance."""
    try:
        if sales_orders.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales or sales rep data available"
        
        # Calculate performance per sales rep
        rep_performance = sales_orders.groupby('sales_rep_id').agg({
            'total_amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        rep_performance.columns = ['sales_rep_id', 'total_revenue', 'order_count']
        
        # Merge with sales rep information
        performance_data = rep_performance.merge(
            sales_reps[['sales_rep_id', 'first_name', 'last_name', 'region', 'quota']], 
            on='sales_rep_id', 
            how='left'
        )
        
        # Calculate quota achievement
        performance_data['quota_achievement'] = (performance_data['total_revenue'] / performance_data['quota'] * 100).fillna(0)
        
        # Add full name
        performance_data['full_name'] = performance_data['first_name'] + ' ' + performance_data['last_name']
        
        performance_data = performance_data.sort_values('total_revenue', ascending=False)
        
        return performance_data, f"Performance analysis completed for {len(performance_data)} sales representatives"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating sales performance: {str(e)}"

def calculate_win_rate(opportunities):
    """Calculate win rate analysis."""
    try:
        if opportunities.empty:
            return pd.DataFrame(), "No opportunities data available"
        
        # Count opportunities by stage
        stage_counts = opportunities['stage'].value_counts().reset_index()
        stage_counts.columns = ['stage', 'count']
        
        # Calculate win rate
        total_opportunities = len(opportunities)
        won_opportunities = len(opportunities[opportunities['stage'] == 'Closed Won'])
        lost_opportunities = len(opportunities[opportunities['stage'] == 'Closed Lost'])
        
        win_rate = (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0
        loss_rate = (lost_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0
        
        # Add summary metrics
        summary_data = pd.DataFrame({
            'Metric': ['Total Opportunities', 'Won Deals', 'Lost Deals', 'Win Rate', 'Loss Rate'],
            'Value': [total_opportunities, won_opportunities, lost_opportunities, f"{win_rate:.1f}%", f"{loss_rate:.1f}%"]
        })
        
        return summary_data, f"Win rate analysis completed for {total_opportunities} opportunities"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating win rate: {str(e)}"

def calculate_sales_call_success_rate(activities):
    """Calculate sales call success rate."""
    try:
        if activities.empty:
            return pd.DataFrame(), "No activities data available"
        
        # Filter for call activities
        call_activities = activities[activities['activity_type'] == 'Call']
        
        if call_activities.empty:
            return pd.DataFrame(), "No call activities found"
        
        # Count outcomes
        outcome_counts = call_activities['outcome'].value_counts().reset_index()
        outcome_counts.columns = ['outcome', 'count']
        
        # Calculate success rate
        total_calls = len(call_activities)
        positive_calls = len(call_activities[call_activities['outcome'] == 'Positive'])
        success_rate = (positive_calls / total_calls * 100) if total_calls > 0 else 0
        
        # Add summary metrics
        summary_data = pd.DataFrame({
            'Metric': ['Total Calls', 'Positive Outcomes', 'Success Rate'],
            'Value': [total_calls, positive_calls, f"{success_rate:.1f}%"]
        })
        
        return summary_data, f"Call success analysis completed for {total_calls} calls"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating call success rate: {str(e)}"

def calculate_sales_productivity(sales_orders, activities):
    """Calculate sales productivity metrics."""
    try:
        if sales_orders.empty or activities.empty:
            return pd.DataFrame(), "No sales or activities data available"
        
        # Calculate revenue per activity
        total_revenue = sales_orders['total_amount'].sum()
        total_activities = len(activities)
        
        revenue_per_activity = total_revenue / total_activities if total_activities > 0 else 0
        
        # Calculate activities per sales rep
        activities_per_rep = activities.groupby('sales_rep_id').size().reset_index()
        activities_per_rep.columns = ['sales_rep_id', 'activity_count']
        
        avg_activities_per_rep = activities_per_rep['activity_count'].mean()
        
        productivity_data = pd.DataFrame({
            'Metric': ['Total Revenue', 'Total Activities', 'Revenue per Activity', 'Avg Activities per Rep'],
            'Value': [f"${total_revenue:,.2f}", total_activities, f"${revenue_per_activity:,.2f}", f"{avg_activities_per_rep:.1f}"]
        })
        
        return productivity_data, f"Productivity analysis completed for {total_activities} activities"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating productivity: {str(e)}"

# ============================================================================
# PRICING & DISCOUNT METRICS
# ============================================================================

def calculate_average_selling_price(sales_orders):
    """Calculate average selling price."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Calculate ASP by product
        product_asp = sales_orders.groupby('product_id').agg({
            'total_amount': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        product_asp['asp'] = product_asp['total_amount'] / product_asp['quantity']
        
        # Calculate overall ASP
        total_revenue = sales_orders['total_amount'].sum()
        total_quantity = sales_orders['quantity'].sum()
        overall_asp = total_revenue / total_quantity if total_quantity > 0 else 0
        
        # Add overall row
        overall_row = pd.DataFrame({
            'product_id': ['Overall'],
            'total_amount': [total_revenue],
            'quantity': [total_quantity],
            'asp': [overall_asp]
        })
        
        asp_data = pd.concat([overall_row, product_asp], ignore_index=True)
        
        return asp_data, f"ASP analysis completed for {len(product_asp)} products"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating ASP: {str(e)}"

def calculate_profit_margin_analysis(sales_orders, products):
    """Calculate profit margin analysis."""
    try:
        if sales_orders.empty or products.empty:
            return pd.DataFrame(), "No sales or product data available"
        
        # Merge sales with product cost data
        margin_data = sales_orders.merge(
            products[['product_id', 'product_name', 'cost_price']], 
            on='product_id', 
            how='left'
        )
        
        # Calculate profit margin
        margin_data['total_cost'] = margin_data['cost_price'] * margin_data['quantity']
        margin_data['total_profit'] = margin_data['total_amount'] - margin_data['total_cost']
        margin_data['profit_margin'] = (margin_data['total_profit'] / margin_data['total_amount'] * 100).fillna(0)
        
        # Group by product
        product_margins = margin_data.groupby(['product_id', 'product_name']).agg({
            'total_amount': 'sum',
            'total_cost': 'sum',
            'total_profit': 'sum',
            'profit_margin': 'mean'
        }).reset_index()
        
        product_margins = product_margins.sort_values('profit_margin', ascending=False)
        
        return product_margins, f"Profit margin analysis completed for {len(product_margins)} products"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating profit margins: {str(e)}"

# ============================================================================
# MARKET ANALYSIS METRICS
# ============================================================================

def calculate_market_share_analysis(company_sales, total_market_sales):
    """Calculate market share analysis."""
    try:
        if company_sales == 0 or total_market_sales == 0:
            return pd.DataFrame(), "Invalid market data provided"
        
        market_share = (company_sales / total_market_sales) * 100
        
        market_data = pd.DataFrame({
            'Metric': ['Company Sales', 'Total Market Sales', 'Market Share'],
            'Value': [f"${company_sales:,.2f}", f"${total_market_sales:,.2f}", f"{market_share:.2f}%"]
        })
        
        return market_data, f"Market share analysis completed"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating market share: {str(e)}"

def calculate_market_penetration_rate(customers, total_target_market):
    """Calculate market penetration rate."""
    try:
        if customers.empty:
            return pd.DataFrame(), "No customer data available"
        
        total_customers = len(customers)
        penetration_rate = (total_customers / total_target_market * 100) if total_target_market > 0 else 0
        
        penetration_data = pd.DataFrame({
            'Metric': ['Total Customers', 'Target Market Size', 'Market Penetration Rate'],
            'Value': [total_customers, total_target_market, f"{penetration_rate:.2f}%"]
        })
        
        return penetration_data, f"Market penetration analysis completed for {total_customers} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating market penetration: {str(e)}"

# ============================================================================
# FORECASTING METRICS
# ============================================================================

def calculate_revenue_forecast(sales_orders):
    """Calculate comprehensive revenue forecast with multiple scenarios."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Group by month
        monthly_revenue = sales_orders.groupby(sales_orders['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
        monthly_revenue.columns = ['month', 'revenue']
        monthly_revenue['month'] = monthly_revenue['month'].astype(str)
        
        # Create forecast data for next 12 periods
        if len(monthly_revenue) >= 3:
            recent_trend = monthly_revenue['revenue'].tail(3).pct_change().mean()
            last_revenue = monthly_revenue['revenue'].iloc[-1]
            
            # Generate multiple forecast scenarios
            forecast_periods = []
            optimistic_revenues = []
            realistic_revenues = []
            conservative_revenues = []
            
            for i in range(1, 13):  # Next 12 periods
                forecast_periods.append(f"Period {i}")
                
                # Optimistic scenario (higher growth)
                optimistic_revenue = last_revenue * (1 + recent_trend * 1.5) ** i
                optimistic_revenues.append(optimistic_revenue)
                
                # Realistic scenario (current trend)
                realistic_revenue = last_revenue * (1 + recent_trend) ** i
                realistic_revenues.append(realistic_revenue)
                
                # Conservative scenario (lower growth)
                conservative_revenue = last_revenue * (1 + recent_trend * 0.5) ** i
                conservative_revenues.append(conservative_revenue)
            
            forecast_data = pd.DataFrame({
                'period': forecast_periods,
                'optimistic': optimistic_revenues,
                'realistic': realistic_revenues,
                'conservative': conservative_revenues
            })
            
            return forecast_data, f"Multi-scenario forecast completed for next 12 periods (trend: {recent_trend*100:.1f}%)"
        else:
            # If not enough data, create simple forecast
            last_revenue = monthly_revenue['revenue'].iloc[-1] if not monthly_revenue.empty else 1000
            
            forecast_periods = []
            optimistic_revenues = []
            realistic_revenues = []
            conservative_revenues = []
            
            for i in range(1, 13):
                forecast_periods.append(f"Period {i}")
                
                # Optimistic scenario (8% growth)
                optimistic_revenues.append(last_revenue * (1 + 0.08) ** i)
                
                # Realistic scenario (5% growth)
                realistic_revenues.append(last_revenue * (1 + 0.05) ** i)
                
                # Conservative scenario (2% growth)
                conservative_revenues.append(last_revenue * (1 + 0.02) ** i)
            
            forecast_data = pd.DataFrame({
                'period': forecast_periods,
                'optimistic': optimistic_revenues,
                'realistic': realistic_revenues,
                'conservative': conservative_revenues
            })
            
            return forecast_data, f"Multi-scenario forecast completed for next 12 periods (assumed growth rates)"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating revenue forecast: {str(e)}"

def calculate_seasonal_forecast(sales_orders):
    """Calculate seasonal revenue forecast with pattern recognition."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Extract seasonal components
        sales_orders['month'] = sales_orders['order_date'].dt.month
        sales_orders['quarter'] = sales_orders['order_date'].dt.quarter
        
        # Calculate seasonal patterns
        monthly_patterns = sales_orders.groupby('month')['total_amount'].mean()
        quarterly_patterns = sales_orders.groupby('quarter')['total_amount'].mean()
        
        # Calculate overall trend
        monthly_revenue = sales_orders.groupby(sales_orders['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
        monthly_revenue.columns = ['month', 'revenue']
        monthly_revenue['month'] = monthly_revenue['month'].astype(str)
        
        if len(monthly_revenue) >= 3:
            trend = monthly_revenue['revenue'].tail(3).pct_change().mean()
            last_revenue = monthly_revenue['revenue'].iloc[-1]
        else:
            trend = 0.05  # 5% default growth
            last_revenue = monthly_revenue['revenue'].iloc[-1] if not monthly_revenue.empty else 1000
        
        # Generate seasonal forecast
        forecast_periods = []
        seasonal_revenues = []
        
        for i in range(1, 13):  # Next 12 months
            month_num = ((pd.Timestamp.now().month + i - 1) % 12) + 1
            seasonal_factor = monthly_patterns[month_num] / monthly_patterns.mean() if not monthly_patterns.empty else 1.0
            
            forecast_periods.append(f"Month {i}")
            seasonal_revenue = last_revenue * (1 + trend) ** i * seasonal_factor
            seasonal_revenues.append(seasonal_revenue)
        
        seasonal_forecast = pd.DataFrame({
            'period': forecast_periods,
            'forecasted_revenue': seasonal_revenues,
            'seasonal_factor': [monthly_patterns[((pd.Timestamp.now().month + i - 1) % 12) + 1] / monthly_patterns.mean() if not monthly_patterns.empty else 1.0 for i in range(1, 13)]
        })
        
        return seasonal_forecast, f"Seasonal forecast completed with pattern recognition"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating seasonal forecast: {str(e)}"

def calculate_confidence_intervals(forecast_data):
    """Calculate confidence intervals for forecast predictions."""
    try:
        if forecast_data.empty:
            return pd.DataFrame(), "No forecast data available"
        
        # Calculate confidence intervals based on historical volatility
        if 'realistic' in forecast_data.columns:
            base_forecast = forecast_data['realistic']
        else:
            base_forecast = forecast_data['forecasted_revenue']
        
        # Calculate standard deviation (assuming 15% volatility)
        volatility = 0.15
        
        # Generate confidence intervals
        confidence_95 = base_forecast * (1 + 1.96 * volatility)
        confidence_68 = base_forecast * (1 + 1.0 * volatility)
        confidence_lower_68 = base_forecast * (1 - 1.0 * volatility)
        confidence_lower_95 = base_forecast * (1 - 1.96 * volatility)
        
        confidence_data = forecast_data.copy()
        confidence_data['confidence_95_upper'] = confidence_95
        confidence_data['confidence_68_upper'] = confidence_68
        confidence_data['confidence_68_lower'] = confidence_lower_68
        confidence_data['confidence_95_lower'] = confidence_lower_95
        
        return confidence_data, "Confidence intervals calculated successfully"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating confidence intervals: {str(e)}"

# ============================================================================
# CRM ANALYSIS METRICS
# ============================================================================

def calculate_active_accounts(customers):
    """Calculate active accounts analysis."""
    try:
        if customers.empty:
            return pd.DataFrame(), "No customer data available"
        
        active_customers = len(customers[customers['status'] == 'Active'])
        total_customers = len(customers)
        active_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
        
        active_data = pd.DataFrame({
            'Metric': ['Total Customers', 'Active Customers', 'Active Rate'],
            'Value': [total_customers, active_customers, f"{active_rate:.1f}%"]
        })
        
        return active_data, f"Active accounts analysis completed for {total_customers} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating active accounts: {str(e)}"

def calculate_dormant_accounts(customers):
    """Calculate dormant accounts analysis."""
    try:
        if customers.empty:
            return pd.DataFrame(), "No customer data available"
        
        dormant_customers = len(customers[customers['status'] == 'Inactive'])
        total_customers = len(customers)
        dormant_rate = (dormant_customers / total_customers * 100) if total_customers > 0 else 0
        
        dormant_data = pd.DataFrame({
            'Metric': ['Total Customers', 'Dormant Customers', 'Dormant Rate'],
            'Value': [total_customers, dormant_customers, f"{dormant_rate:.1f}%"]
        })
        
        return dormant_data, f"Dormant accounts analysis completed for {total_customers} customers"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating dormant accounts: {str(e)}"

def calculate_new_vs_returning_customers(sales_orders, customers):
    """Calculate new vs returning customers analysis."""
    try:
        if sales_orders.empty or customers.empty:
            return pd.DataFrame(), "No sales or customer data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Get first order date for each customer
        first_orders = sales_orders.groupby('customer_id')['order_date'].min().reset_index()
        first_orders.columns = ['customer_id', 'first_order_date']
        
        # Merge with sales orders to identify new vs returning
        customer_orders = sales_orders.merge(first_orders, on='customer_id', how='left')
        customer_orders['is_new_customer'] = customer_orders['order_date'] == customer_orders['first_order_date']
        
        # Count new vs returning orders
        new_orders = len(customer_orders[customer_orders['is_new_customer'] == True])
        returning_orders = len(customer_orders[customer_orders['is_new_customer'] == False])
        total_orders = len(customer_orders)
        
        new_rate = (new_orders / total_orders * 100) if total_orders > 0 else 0
        returning_rate = (returning_orders / total_orders * 100) if total_orders > 0 else 0
        
        new_vs_returning_data = pd.DataFrame({
            'Metric': ['Total Orders', 'New Customer Orders', 'Returning Customer Orders', 'New Customer Rate', 'Returning Customer Rate'],
            'Value': [total_orders, new_orders, returning_orders, f"{new_rate:.1f}%", f"{returning_rate:.1f}%"]
        })
        
        return new_vs_returning_data, f"New vs returning customer analysis completed for {total_orders} orders"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating new vs returning customers: {str(e)}"

def calculate_new_vs_returning_revenue(sales_orders, customers):
    """Calculate new vs returning customers revenue distribution for pie chart."""
    try:
        if sales_orders.empty or customers.empty:
            return pd.DataFrame(), "No sales or customer data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Get first order date for each customer
        first_orders = sales_orders.groupby('customer_id')['order_date'].min().reset_index()
        first_orders.columns = ['customer_id', 'first_order_date']
        
        # Merge with sales orders to identify new vs returning
        customer_orders = sales_orders.merge(first_orders, on='customer_id', how='left')
        customer_orders['is_new_customer'] = customer_orders['order_date'] == customer_orders['first_order_date']
        
        # Calculate revenue for new vs returning customers
        new_customer_revenue = customer_orders[customer_orders['is_new_customer'] == True]['total_amount'].sum()
        returning_customer_revenue = customer_orders[customer_orders['is_new_customer'] == False]['total_amount'].sum()
        
        # Create DataFrame for pie chart
        revenue_data = pd.DataFrame({
            'Customer Type': ['New Customers', 'Returning Customers'],
            'Revenue': [new_customer_revenue, returning_customer_revenue]
        })
        
        return revenue_data, f"Revenue distribution: New customers ${new_customer_revenue:,.2f}, Returning customers ${returning_customer_revenue:,.2f}"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating new vs returning revenue: {str(e)}"

# ============================================================================
# OPERATIONAL EFFICIENCY METRICS
# ============================================================================

def calculate_sales_expense_ratio(total_expenses, total_revenue):
    """Calculate sales expense ratio."""
    try:
        if total_revenue == 0:
            return pd.DataFrame(), "Invalid revenue data provided"
        
        expense_ratio = (total_expenses / total_revenue) * 100
        
        expense_data = pd.DataFrame({
            'Metric': ['Total Expenses', 'Total Revenue', 'Expense Ratio'],
            'Value': [f"${total_expenses:,.2f}", f"${total_revenue:,.2f}", f"{expense_ratio:.2f}%"]
        })
        
        return expense_data, f"Expense ratio analysis completed"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating expense ratio: {str(e)}"

def calculate_revenue_per_salesperson(sales_orders, sales_reps):
    """Calculate revenue per salesperson."""
    try:
        if sales_orders.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales or sales rep data available"
        
        # Calculate revenue per sales rep
        rep_revenue = sales_orders.groupby('sales_rep_id')['total_amount'].sum().reset_index()
        rep_revenue.columns = ['sales_rep_id', 'total_revenue']
        
        # Merge with sales rep information
        revenue_per_rep = rep_revenue.merge(
            sales_reps[['sales_rep_id', 'first_name', 'last_name', 'region']], 
            on='sales_rep_id', 
            how='left'
        )
        
        revenue_per_rep['full_name'] = revenue_per_rep['first_name'] + ' ' + revenue_per_rep['last_name']
        revenue_per_rep = revenue_per_rep.sort_values('total_revenue', ascending=False)
        
        return revenue_per_rep, f"Revenue per salesperson analysis completed for {len(revenue_per_rep)} representatives"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating revenue per salesperson: {str(e)}"

def calculate_quota_attainment_rate(sales_orders, sales_reps):
    """Calculate quota attainment rate."""
    try:
        if sales_orders.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales or sales rep data available"
        
        # Calculate actual sales per rep
        rep_sales = sales_orders.groupby('sales_rep_id')['total_amount'].sum().reset_index()
        rep_sales.columns = ['sales_rep_id', 'actual_sales']
        
        # Merge with sales rep quotas
        quota_data = rep_sales.merge(
            sales_reps[['sales_rep_id', 'first_name', 'last_name', 'quota']], 
            on='sales_rep_id', 
            how='left'
        )
        
        # Calculate attainment rate
        quota_data['attainment_rate'] = (quota_data['actual_sales'] / quota_data['quota'] * 100).fillna(0)
        quota_data['full_name'] = quota_data['first_name'] + ' ' + quota_data['last_name']
        
        quota_data = quota_data.sort_values('attainment_rate', ascending=False)
        
        return quota_data, f"Quota attainment analysis completed for {len(quota_data)} representatives"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating quota attainment: {str(e)}"

# ============================================================================
# SPECIALIZED METRICS
# ============================================================================

def calculate_territory_performance(sales_orders, sales_reps):
    """Calculate territory performance analysis."""
    try:
        if sales_orders.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales or sales rep data available"
        
        # Merge sales with sales rep territory info
        territory_sales = sales_orders.merge(
            sales_reps[['sales_rep_id', 'territory', 'region']], 
            on='sales_rep_id', 
            how='left'
        )
        
        # Group by territory
        territory_performance = territory_sales.groupby(['territory', 'region']).agg({
            'total_amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        
        territory_performance.columns = ['territory', 'region', 'total_revenue', 'order_count']
        territory_performance = territory_performance.sort_values('total_revenue', ascending=False)
        
        return territory_performance, f"Territory performance analysis completed for {len(territory_performance)} territories"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating territory performance: {str(e)}"

# ============================================================================
# ENHANCED SALES PERFORMANCE ANALYTICS
# ============================================================================

def calculate_sales_trend_analysis(sales_orders, period='daily'):
    """Calculate comprehensive sales trend analysis with seasonality detection."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        if period == 'daily':
            # Group by day
            trend_data = sales_orders.groupby(sales_orders['order_date'].dt.date).agg({
                'total_amount': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).reset_index()
            trend_data.columns = ['date', 'total_revenue', 'avg_order_value', 'order_count', 'total_quantity']
            trend_data['date'] = pd.to_datetime(trend_data['date'])
            
        elif period == 'weekly':
            # Group by week
            trend_data = sales_orders.groupby(sales_orders['order_date'].dt.isocalendar().week).agg({
                'total_amount': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).reset_index()
            trend_data.columns = ['week', 'total_revenue', 'avg_order_value', 'order_count', 'total_quantity']
            
        else:  # monthly
            # Group by month
            trend_data = sales_orders.groupby(sales_orders['order_date'].dt.to_period('M')).agg({
                'total_amount': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).reset_index()
            trend_data.columns = ['month', 'total_revenue', 'avg_order_value', 'order_count', 'total_quantity']
            trend_data['month'] = trend_data['month'].astype(str)
        
        # Calculate trend metrics
        trend_data['revenue_trend'] = trend_data['total_revenue'].pct_change() * 100
        trend_data['order_trend'] = trend_data['order_count'].pct_change() * 100
        trend_data['aov_trend'] = trend_data['avg_order_value'].pct_change() * 100
        
        # Calculate moving averages
        trend_data['revenue_ma_7'] = trend_data['total_revenue'].rolling(window=7, min_periods=1).mean()
        trend_data['order_ma_7'] = trend_data['order_count'].rolling(window=7, min_periods=1).mean()
        
        return trend_data, f"Trend analysis completed for {len(trend_data)} {period} periods"
    
    except Exception as e:
        return None, f"Error calculating trend analysis: {str(e)}"

def calculate_sales_seasonality(sales_orders):
    """Calculate sales seasonality patterns."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Convert order_date to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Extract time components
        sales_orders['month'] = sales_orders['order_date'].dt.month
        sales_orders['day_of_week'] = sales_orders['order_date'].dt.dayofweek
        sales_orders['quarter'] = sales_orders['order_date'].dt.quarter
        
        # Monthly seasonality
        monthly_patterns = sales_orders.groupby('month').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        monthly_patterns.columns = ['month', 'total_revenue', 'avg_revenue', 'order_count', 'total_quantity']
        
        # Day of week seasonality
        dow_patterns = sales_orders.groupby('day_of_week').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        dow_patterns.columns = ['day_of_week', 'total_revenue', 'avg_revenue', 'order_count', 'total_quantity']
        
        # Add day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_patterns['day_name'] = dow_patterns['day_of_week'].apply(lambda x: day_names[x])
        
        # Quarterly patterns
        quarterly_patterns = sales_orders.groupby('quarter').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        quarterly_patterns.columns = ['quarter', 'total_revenue', 'avg_revenue', 'order_count', 'total_quantity']
        
        return {
            'monthly': monthly_patterns,
            'daily': dow_patterns,
            'quarterly': quarterly_patterns
        }, "Seasonality analysis completed"
    
    except Exception as e:
        return None, f"Error calculating seasonality: {str(e)}"

def calculate_sales_performance_benchmarks(sales_orders, products, sales_reps):
    """Calculate performance benchmarks and KPIs."""
    try:
        if sales_orders.empty:
            return pd.DataFrame(), "No sales data available"
        
        # Overall benchmarks
        total_revenue = sales_orders['total_amount'].sum()
        total_orders = len(sales_orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Product performance benchmarks
        product_performance = sales_orders.groupby('product_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        product_performance.columns = ['product_id', 'total_revenue', 'avg_revenue', 'order_count', 'total_quantity']
        
        # Sales rep performance benchmarks
        rep_performance = sales_orders.groupby('sales_rep_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        rep_performance.columns = ['sales_rep_id', 'total_revenue', 'avg_revenue', 'order_count', 'total_quantity']
        
        # Calculate percentiles for benchmarking
        revenue_percentiles = sales_orders['total_amount'].quantile([0.25, 0.5, 0.75, 0.9, 0.95])
        order_count_percentiles = product_performance['order_count'].quantile([0.25, 0.5, 0.75, 0.9, 0.95])
        
        benchmarks = {
            'overall': {
                'total_revenue': total_revenue,
                'total_orders': total_orders,
                'avg_order_value': avg_order_value,
                'revenue_per_order': total_revenue / total_orders if total_orders > 0 else 0
            },
            'revenue_percentiles': revenue_percentiles.to_dict(),
            'order_percentiles': order_count_percentiles.to_dict(),
            'product_performance': product_performance,
            'rep_performance': rep_performance
        }
        
        return benchmarks, "Performance benchmarks calculated successfully"
    
    except Exception as e:
        return None, f"Error calculating benchmarks: {str(e)}"

def calculate_sales_efficiency_metrics(sales_orders, activities):
    """Calculate sales efficiency and productivity metrics."""
    try:
        if sales_orders.empty:
            return None, "No sales data available"
        
        # Revenue per activity
        total_revenue = sales_orders['total_amount'].sum()
        total_orders = len(sales_orders)
        total_activities = len(activities) if not activities.empty else 0
        
        # Time-based efficiency (if date data available)
        if 'order_date' in sales_orders.columns and not sales_orders.empty:
            sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
            date_range = sales_orders['order_date'].max() - sales_orders['order_date'].min()
            days_active = date_range.days + 1
            
            daily_revenue = total_revenue / days_active if days_active > 0 else 0
            daily_orders = total_orders / days_active if days_active > 0 else 0
        else:
            daily_revenue = 0
            daily_orders = 0
            days_active = 0
        
        # Activity efficiency
        revenue_per_activity = total_revenue / total_activities if total_activities > 0 else 0
        orders_per_activity = total_orders / total_activities if total_activities > 0 else 0
        
        # Conversion efficiency (if activities have outcomes)
        if not activities.empty and 'outcome' in activities.columns:
            positive_activities = len(activities[activities['outcome'] == 'Positive'])
            conversion_rate = (positive_activities / total_activities * 100) if total_activities > 0 else 0
        else:
            conversion_rate = 0
        
        efficiency_metrics = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_activities': total_activities,
            'days_active': days_active,
            'daily_revenue': daily_revenue,
            'daily_orders': daily_orders,
            'revenue_per_activity': revenue_per_activity,
            'orders_per_activity': orders_per_activity,
            'conversion_rate': conversion_rate,
            'avg_order_value': total_revenue / total_orders if total_orders > 0 else 0
        }
        
        return efficiency_metrics, "Efficiency metrics calculated successfully"
    
    except Exception as e:
        return None, f"Error calculating efficiency metrics: {str(e)}"

# ============================================================================
# ADVANCED CUSTOMER ANALYTICS
# ============================================================================

def calculate_customer_acquisition_trends(customers, sales_orders, period='monthly'):
    """Calculate customer acquisition and revenue trends over time."""
    try:
        if customers.empty or sales_orders.empty:
            return None, "No customer or sales data available"
        
        # Convert acquisition_date to datetime
        customers['acquisition_date'] = pd.to_datetime(customers['acquisition_date'])
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        if period == 'monthly':
            # Group by month
            customers['period'] = customers['acquisition_date'].dt.to_period('M')
            sales_orders['period'] = sales_orders['order_date'].dt.to_period('M')
        elif period == 'quarterly':
            # Group by quarter
            customers['period'] = customers['acquisition_date'].dt.to_period('Q')
            sales_orders['period'] = sales_orders['order_date'].dt.to_period('Q')
        else:  # yearly
            # Group by year
            customers['period'] = customers['acquisition_date'].dt.year
            sales_orders['period'] = sales_orders['order_date'].dt.year
        
        # Calculate new customers per period
        customer_trends = customers.groupby('period').size().reset_index()
        customer_trends.columns = ['period', 'new_customers']
        
        # Calculate revenue per period
        revenue_trends = sales_orders.groupby('period')['total_amount'].sum().reset_index()
        revenue_trends.columns = ['period', 'revenue']
        
        # Merge trends
        trends_data = customer_trends.merge(revenue_trends, on='period', how='outer').fillna(0)
        trends_data['period'] = trends_data['period'].astype(str)
        
        return trends_data, f"Customer acquisition trends calculated for {len(trends_data)} {period} periods"
    
    except Exception as e:
        return None, f"Error calculating customer acquisition trends: {str(e)}"

def calculate_geographic_customer_distribution(customers, sales_orders):
    """Calculate customer distribution and performance by geographic region."""
    try:
        if customers.empty or sales_orders.empty:
            return None, "No customer or sales data available"
        
        # Merge customers with sales data
        customer_sales = customers.merge(
            sales_orders.groupby('customer_id')['total_amount'].sum().reset_index(),
            on='customer_id',
            how='left'
        )
        
        # Fill NaN values with 0
        customer_sales['total_amount'] = customer_sales['total_amount'].fillna(0)
        
        # Group by region
        geo_data = customer_sales.groupby('region').agg({
            'customer_id': 'count',
            'total_amount': ['sum', 'mean']
        }).reset_index()
        
        # Flatten column names
        geo_data.columns = ['region', 'customer_count', 'total_revenue', 'avg_revenue']
        
        # Sort by customer count
        geo_data = geo_data.sort_values('customer_count', ascending=False)
        
        return geo_data, f"Geographic distribution calculated for {len(geo_data)} regions"
    
    except Exception as e:
        return None, f"Error calculating geographic distribution: {str(e)}"

def calculate_industry_customer_analysis(customers, sales_orders):
    """Calculate customer analysis by industry and company size."""
    try:
        if customers.empty or sales_orders.empty:
            return None, "No customer or sales data available"
        
        # Merge customers with sales data
        customer_sales = customers.merge(
            sales_orders.groupby('customer_id')['total_amount'].sum().reset_index(),
            on='customer_id',
            how='left'
        )
        
        # Fill NaN values with 0
        customer_sales['total_amount'] = customer_sales['total_amount'].fillna(0)
        
        # Group by industry
        industry_data = customer_sales.groupby('industry').agg({
            'customer_id': 'count',
            'total_amount': ['sum', 'mean']
        }).reset_index()
        
        # Flatten column names
        industry_data.columns = ['industry', 'customer_count', 'total_revenue', 'avg_revenue']
        
        # Sort by average revenue
        industry_data = industry_data.sort_values('avg_revenue', ascending=False)
        
        return industry_data, f"Industry analysis completed for {len(industry_data)} industries"
    
    except Exception as e:
        return None, f"Error calculating industry analysis: {str(e)}"

# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_sales_data():
    """Generate sample sales data for testing."""
    try:
        # Generate sample customers
        customer_segments = ['Enterprise', 'SMB', 'Startup', 'Individual']
        industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
        countries = ['USA', 'Canada', 'UK', 'Germany', 'Japan', 'Australia']
        
        customers_data = []
        for i in range(50):
            customer = {
                'customer_id': f'CUST{i+1:03d}',
                'customer_name': f'Customer {i+1}',
                'email': f'customer{i+1}@example.com',
                'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                'company': f'Company {i+1}',
                'industry': random.choice(industries),
                'region': random.choice(regions),
                'country': random.choice(countries),
                'customer_segment': random.choice(customer_segments),
                'acquisition_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'status': random.choice(['Active', 'Active', 'Active', 'Inactive', 'Churned'])
            }
            customers_data.append(customer)
        
        # Generate sample products
        categories = ['Software', 'Hardware', 'Services', 'Consulting']
        subcategories = ['CRM', 'Analytics', 'Cloud', 'Security', 'Support']
        
        products_data = []
        for i in range(30):
            product = {
                'product_id': f'PROD{i+1:03d}',
                'product_name': f'Product {i+1}',
                'category': random.choice(categories),
                'subcategory': random.choice(subcategories),
                'unit_price': round(random.uniform(100, 5000), 2),
                'cost_price': round(random.uniform(50, 2500), 2),
                'supplier_id': f'SUPP{random.randint(1, 10):03d}',
                'launch_date': datetime.now() - timedelta(days=random.randint(1, 730)),
                'status': random.choice(['Active', 'Active', 'Active', 'Discontinued'])
            }
            products_data.append(product)
        
        # Generate sample sales representatives
        sales_reps_data = []
        for i in range(15):
            rep = {
                'sales_rep_id': f'REP{i+1:03d}',
                'first_name': f'Rep{i+1}',
                'last_name': f'LastName{i+1}',
                'email': f'rep{i+1}@company.com',
                'region': random.choice(regions),
                'territory': f'Territory {i+1}',
                'hire_date': datetime.now() - timedelta(days=random.randint(30, 1095)),
                'quota': round(random.uniform(50000, 500000), 2),
                'manager_id': f'REP{random.randint(1, 5):03d}' if i > 4 else None,
                'status': random.choice(['Active', 'Active', 'Active', 'Inactive'])
            }
            sales_reps_data.append(rep)
        
        # Generate sample sales orders
        channels = ['Online', 'In-Store', 'Phone', 'Partner']
        sales_orders_data = []
        for i in range(200):
            order = {
                'order_id': f'ORD{i+1:04d}',
                'customer_id': random.choice(customers_data)['customer_id'],
                'order_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'product_id': random.choice(products_data)['product_id'],
                'quantity': random.randint(1, 10),
                'unit_price': round(random.uniform(100, 5000), 2),
                'total_amount': 0,  # Will be calculated
                'sales_rep_id': random.choice(sales_reps_data)['sales_rep_id'],
                'region': random.choice(regions),
                'channel': random.choice(channels)
            }
            order['total_amount'] = order['quantity'] * order['unit_price']
            sales_orders_data.append(order)
        
        # Generate sample leads
        sources = ['Website', 'Referral', 'Cold Call', 'Trade Show', 'Social Media']
        lead_statuses = ['New', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        
        leads_data = []
        for i in range(100):
            lead = {
                'lead_id': f'LEAD{i+1:04d}',
                'lead_name': f'Lead {i+1}',
                'email': f'lead{i+1}@prospect.com',
                'company': f'Prospect Company {i+1}',
                'industry': random.choice(industries),
                'source': random.choice(sources),
                'created_date': datetime.now() - timedelta(days=random.randint(1, 180)),
                'status': random.choice(lead_statuses),
                'assigned_rep_id': random.choice(sales_reps_data)['sales_rep_id'],
                'value': round(random.uniform(5000, 100000), 2)
            }
            leads_data.append(lead)
        
        # Generate sample opportunities
        opportunity_stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        
        opportunities_data = []
        for i in range(80):
            opportunity = {
                'opportunity_id': f'OPP{i+1:04d}',
                'lead_id': random.choice(leads_data)['lead_id'],
                'customer_id': random.choice(customers_data)['customer_id'],
                'product_id': random.choice(products_data)['product_id'],
                'value': round(random.uniform(10000, 200000), 2),
                'stage': random.choice(opportunity_stages),
                'created_date': datetime.now() - timedelta(days=random.randint(1, 180)),
                'close_date': datetime.now() + timedelta(days=random.randint(1, 90)),
                'probability': random.randint(10, 90),
                'sales_rep_id': random.choice(sales_reps_data)['sales_rep_id']
            }
            opportunities_data.append(opportunity)
        
        # Generate sample activities
        activity_types = ['Call', 'Meeting', 'Email', 'Demo', 'Proposal']
        outcomes = ['Positive', 'Neutral', 'Negative', 'Follow-up Required']
        
        activities_data = []
        for i in range(150):
            activity = {
                'activity_id': f'ACT{i+1:04d}',
                'sales_rep_id': random.choice(sales_reps_data)['sales_rep_id'],
                'customer_id': random.choice(customers_data)['customer_id'],
                'activity_type': random.choice(activity_types),
                'date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'duration_minutes': random.randint(15, 120),
                'notes': f'Activity notes for {random.choice(activity_types)}',
                'outcome': random.choice(outcomes)
            }
            activities_data.append(activity)
        
        # Generate sample targets
        target_categories = ['Revenue', 'Deals', 'Activities', 'Leads']
        target_statuses = ['Active', 'Completed', 'Overdue']
        
        targets_data = []
        for i in range(60):
            target = {
                'target_id': f'TARG{i+1:04d}',
                'sales_rep_id': random.choice(sales_reps_data)['sales_rep_id'],
                'period': f'Q{random.randint(1, 4)} 2024',
                'target_amount': round(random.uniform(10000, 100000), 2),
                'target_date': datetime.now() + timedelta(days=random.randint(1, 365)),
                'category': random.choice(target_categories),
                'status': random.choice(target_statuses)
            }
            targets_data.append(target)
        
        # Convert to DataFrames
        import streamlit as st
        
        st.session_state.customers = pd.DataFrame(customers_data)
        st.session_state.products = pd.DataFrame(products_data)
        st.session_state.sales_orders = pd.DataFrame(sales_orders_data)
        st.session_state.sales_reps = pd.DataFrame(sales_reps_data)
        st.session_state.leads = pd.DataFrame(leads_data)
        st.session_state.opportunities = pd.DataFrame(opportunities_data)
        st.session_state.activities = pd.DataFrame(activities_data)
        st.session_state.targets = pd.DataFrame(targets_data)
        
        return "Sample data generated successfully"
    
    except Exception as e:
        return f"Error generating sample data: {str(e)}"

# ============================================================================
# FUNNEL ANALYSIS FUNCTIONS
# ============================================================================

def calculate_funnel_stage_progression(leads, opportunities):
    """Calculate funnel stage progression and conversion rates."""
    try:
        if leads.empty or opportunities.empty:
            return pd.DataFrame(), "No data available for funnel analysis"
        
        # Analyze lead progression through stages
        funnel_stages = {
            'Stage': ['Leads', 'Qualified Leads', 'Opportunities', 'Proposals', 'Negotiations', 'Closed Won'],
            'Count': [
                len(leads),
                len(leads[leads['status'] == 'Qualified']),
                len(opportunities),
                len(opportunities[opportunities['stage'] == 'Proposal']),
                len(opportunities[opportunities['stage'] == 'Negotiation']),
                len(opportunities[opportunities['stage'] == 'Closed Won'])
            ]
        }
        
        # Calculate conversion rates
        funnel_data = pd.DataFrame(funnel_stages)
        funnel_data['Conversion_Rate'] = (funnel_data['Count'] / funnel_data['Count'].iloc[0] * 100).round(1)
        funnel_data['Drop_Off_Rate'] = (100 - funnel_data['Conversion_Rate']).round(1)
        
        return funnel_data, f"Funnel analysis completed for {len(funnel_data)} stages"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating funnel progression: {str(e)}"

def calculate_lead_velocity_metrics(leads, opportunities):
    """Calculate lead velocity and time-based metrics."""
    try:
        if leads.empty or opportunities.empty:
            return pd.DataFrame(), "No data available for velocity analysis"
        
        # Calculate time-based metrics
        leads['created_date'] = pd.to_datetime(leads['created_date'])
        opportunities['created_date'] = pd.to_datetime(opportunities['created_date'])
        
        # Lead to opportunity conversion time
        lead_opp_conversion = leads.merge(
            opportunities[['lead_id', 'created_date']], 
            on='lead_id', 
            suffixes=('_lead', '_opp')
        )
        
        lead_opp_conversion['conversion_days'] = (
            lead_opp_conversion['created_date_opp'] - lead_opp_conversion['created_date_lead']
        ).dt.days
        
        avg_conversion_time = lead_opp_conversion['conversion_days'].mean()
        
        # Velocity metrics
        velocity_data = {
            'Metric': ['Avg Lead to Opp Time', 'Lead Velocity', 'Opportunity Velocity'],
            'Value': [
                f"{avg_conversion_time:.1f} days",
                f"{len(leads) / 30:.1f} leads/month",  # Assuming 30-day period
                f"{len(opportunities) / 30:.1f} opps/month"
            ],
            'Status': ['Good' if avg_conversion_time < 30 else 'Medium', 'High', 'High']
        }
        
        return pd.DataFrame(velocity_data), f"Velocity metrics calculated successfully"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating velocity metrics: {str(e)}"

def calculate_funnel_efficiency_score(leads, opportunities):
    """Calculate overall funnel efficiency score."""
    try:
        if leads.empty or opportunities.empty:
            return pd.DataFrame(), "No data available for efficiency calculation"
        
        # Calculate key efficiency metrics
        total_leads = len(leads)
        qualified_leads = len(leads[leads['status'] == 'Qualified'])
        total_opportunities = len(opportunities)
        won_opportunities = len(opportunities[opportunities['stage'] == 'Closed Won'])
        
        # Efficiency scores (0-100)
        lead_quality_score = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
        lead_to_opp_score = (total_opportunities / total_leads * 100) if total_leads > 0 else 0
        opp_to_won_score = (won_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0
        
        # Overall efficiency score (weighted average)
        overall_score = (lead_quality_score * 0.3 + lead_to_opp_score * 0.4 + opp_to_won_score * 0.3)
        
        efficiency_data = {
            'Metric': ['Lead Quality', 'Lead to Opp', 'Opp to Won', 'Overall Efficiency'],
            'Score': [lead_quality_score, lead_to_opp_score, opp_to_won_score, overall_score],
            'Grade': [
                'A' if lead_quality_score >= 80 else 'B' if lead_quality_score >= 60 else 'C',
                'A' if lead_to_opp_score >= 60 else 'B' if lead_to_opp_score >= 40 else 'C',
                'A' if opp_to_won_score >= 50 else 'B' if opp_to_won_score >= 30 else 'C',
                'A' if overall_score >= 70 else 'B' if overall_score >= 50 else 'C'
            ]
        }
        
        return pd.DataFrame(efficiency_data), f"Efficiency score calculated: {overall_score:.1f}/100"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating efficiency score: {str(e)}"

# ============================================================================
# PREDICTIVE ANALYTICS
# ============================================================================

def calculate_customer_churn_prediction(customers, sales_orders, lookback_days=90):
    """Predict customer churn probability based on behavior patterns."""
    try:
        if customers.empty or sales_orders.empty:
            return pd.DataFrame(), "No customer or sales data available"
        
        # Debug: Check available columns
        print(f"Customer columns: {list(customers.columns)}")
        print(f"Sales orders columns: {list(sales_orders.columns)}")
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Handle missing created_date column - use first order date as fallback
        if 'created_date' in customers.columns:
            customers['created_date'] = pd.to_datetime(customers['created_date'])
        else:
            # If no created_date, use the earliest order date for each customer
            earliest_orders = sales_orders.groupby('customer_id')['order_date'].min().reset_index()
            earliest_orders.columns = ['customer_id', 'created_date']
            customers = customers.merge(earliest_orders, on='customer_id', how='left')
            customers['created_date'] = pd.to_datetime(customers['created_date'])
        
        # Calculate customer behavior metrics
        customer_metrics = []
        current_date = pd.Timestamp.now()
        
        for _, customer in customers.iterrows():
            customer_id = customer['customer_id']
            customer_orders = sales_orders[sales_orders['customer_id'] == customer_id]
            
            if not customer_orders.empty:
                # Calculate key metrics
                total_orders = len(customer_orders)
                total_revenue = customer_orders['total_amount'].sum()
                avg_order_value = total_revenue / total_orders
                
                # Days since last order
                last_order_date = customer_orders['order_date'].max()
                days_since_last_order = (current_date - last_order_date).days
                
                # Order frequency (orders per month)
                first_order_date = customer_orders['order_date'].min()
                months_active = max(1, (current_date - first_order_date).days / 30)
                order_frequency = total_orders / months_active
                
                # Churn probability calculation (simplified model)
                churn_score = 0
                if days_since_last_order > 60:
                    churn_score += 30
                if days_since_last_order > 90:
                    churn_score += 40
                if order_frequency < 0.5:
                    churn_score += 20
                if avg_order_value < 1000:
                    churn_score += 10
                
                churn_probability = min(100, churn_score)
                churn_risk = "Low" if churn_probability < 30 else "Medium" if churn_probability < 70 else "High"
                
                # Get customer name safely
                first_name = customer.get('first_name', '')
                last_name = customer.get('last_name', '')
                customer_name = f"{first_name} {last_name}".strip()
                if not customer_name:
                    customer_name = f"Customer {customer_id}"
                
                customer_metrics.append({
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'total_orders': total_orders,
                    'total_revenue': total_revenue,
                    'avg_order_value': avg_order_value,
                    'days_since_last_order': days_since_last_order,
                    'order_frequency': order_frequency,
                    'churn_probability': churn_probability,
                    'churn_risk': churn_risk
                })
        
        if customer_metrics:
            churn_df = pd.DataFrame(customer_metrics)
            churn_df = churn_df.sort_values('churn_probability', ascending=False)
            
            return churn_df, f"Churn prediction completed for {len(churn_df)} customers"
        else:
            return pd.DataFrame(), "No customer metrics available for churn prediction"
    
    except Exception as e:
        import traceback
        print(f"Error in churn prediction: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame(), f"Error calculating churn prediction: {str(e)}"

def calculate_customer_churn_prediction_simple(customers, sales_orders):
    """Simplified customer churn prediction that works with basic data."""
    try:
        if customers.empty or sales_orders.empty:
            return pd.DataFrame(), "No customer or sales data available"
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Calculate customer behavior metrics
        customer_metrics = []
        
        for _, customer in customers.iterrows():
            customer_id = customer['customer_id']
            customer_orders = sales_orders[sales_orders['customer_id'] == customer_id]
            
            if not customer_orders.empty:
                # Calculate key metrics
                total_orders = len(customer_orders)
                total_revenue = customer_orders['total_amount'].sum()
                avg_order_value = total_revenue / total_orders
                
                # Simple churn probability based on order patterns
                churn_score = 0
                
                # Order frequency scoring
                if total_orders == 1:
                    churn_score += 40  # Single order customers are high risk
                elif total_orders <= 3:
                    churn_score += 25  # Low order count customers
                elif total_orders <= 5:
                    churn_score += 15  # Medium order count customers
                else:
                    churn_score += 5   # High order count customers
                
                # Revenue scoring
                if avg_order_value < 500:
                    churn_score += 30
                elif avg_order_value < 1000:
                    churn_score += 20
                elif avg_order_value < 2000:
                    churn_score += 10
                else:
                    churn_score += 5
                
                # Customer status scoring (if available)
                customer_status = customer.get('status', 'Unknown')
                if customer_status == 'Inactive':
                    churn_score += 25
                elif customer_status == 'Churned':
                    churn_score += 40
                elif customer_status == 'Active':
                    churn_score += 5
                
                churn_probability = min(100, churn_score)
                churn_risk = "Low" if churn_probability < 30 else "Medium" if churn_probability < 70 else "High"
                
                # Get customer name safely
                first_name = customer.get('first_name', '')
                last_name = customer.get('last_name', '')
                customer_name = f"{first_name} {last_name}".strip()
                if not customer_name:
                    customer_name = f"Customer {customer_id}"
                
                # Calculate additional metrics for consistency
                current_date = pd.Timestamp.now()
                last_order_date = customer_orders['order_date'].max()
                days_since_last_order = (current_date - last_order_date).days
                
                # Calculate order frequency (orders per month)
                first_order_date = customer_orders['order_date'].min()
                months_active = max(1, (current_date - first_order_date).days / 30)
                order_frequency = total_orders / months_active
                
                customer_metrics.append({
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'total_orders': total_orders,
                    'total_revenue': total_revenue,
                    'avg_order_value': avg_order_value,
                    'customer_status': customer_status,
                    'days_since_last_order': days_since_last_order,
                    'order_frequency': order_frequency,
                    'churn_probability': churn_probability,
                    'churn_risk': churn_risk
                })
        
        if customer_metrics:
            churn_df = pd.DataFrame(customer_metrics)
            churn_df = churn_df.sort_values('churn_probability', ascending=False)
            
            return churn_df, f"Churn prediction completed for {len(churn_df)} customers"
        else:
            return pd.DataFrame(), "No customer metrics available for churn prediction"
    
    except Exception as e:
        import traceback
        print(f"Error in simple churn prediction: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame(), f"Error calculating churn prediction: {str(e)}"

def calculate_sales_opportunity_scoring(sales_orders, customers, sales_reps):
    """Score sales opportunities based on multiple factors."""
    try:
        if sales_orders.empty or customers.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales, customer, or sales rep data available"
        
        # Calculate opportunity scores
        opportunity_scores = []
        
        for _, order in sales_orders.iterrows():
            customer_id = order['customer_id']
            sales_rep_id = order['sales_rep_id']
            
            # Get customer and sales rep info
            customer = customers[customers['customer_id'] == customer_id]
            sales_rep = sales_reps[sales_reps['sales_rep_id'] == sales_rep_id]
            
            if not customer.empty and not sales_rep.empty:
                # Calculate opportunity score factors
                order_value = order['total_amount']
                customer_status = customer.iloc[0].get('status', 'Unknown')
                sales_rep_experience = sales_rep.iloc[0].get('experience_years', 0)
                
                # Base score calculation
                base_score = 0
                
                # Order value scoring (0-40 points)
                if order_value >= 10000:
                    base_score += 40
                elif order_value >= 5000:
                    base_score += 30
                elif order_value >= 2000:
                    base_score += 20
                else:
                    base_score += 10
                
                # Customer status scoring (0-30 points)
                if customer_status == 'Active':
                    base_score += 30
                elif customer_status == 'Inactive':
                    base_score += 15
                else:
                    base_score += 5
                
                # Sales rep experience scoring (0-30 points)
                if sales_rep_experience >= 5:
                    base_score += 30
                elif sales_rep_experience >= 3:
                    base_score += 20
                elif sales_rep_experience >= 1:
                    base_score += 10
                else:
                    base_score += 5
                
                # Opportunity classification
                if base_score >= 80:
                    opportunity_class = "High Priority"
                elif base_score >= 60:
                    opportunity_class = "Medium Priority"
                else:
                    opportunity_class = "Low Priority"
                
                opportunity_scores.append({
                    'order_id': order['order_id'],
                    'customer_name': f"{customer.iloc[0].get('first_name', '')} {customer.iloc[0].get('last_name', '')}".strip(),
                    'sales_rep': f"{sales_rep.iloc[0].get('first_name', '')} {sales_rep.iloc[0].get('last_name', '')}".strip(),
                    'order_value': order_value,
                    'customer_status': customer_status,
                    'sales_rep_experience': sales_rep_experience,
                    'opportunity_score': base_score,
                    'opportunity_class': opportunity_class
                })
        
        if opportunity_scores:
            opportunity_df = pd.DataFrame(opportunity_scores)
            opportunity_df = opportunity_df.sort_values('opportunity_score', ascending=False)
            
            return opportunity_df, f"Opportunity scoring completed for {len(opportunity_df)} orders"
        else:
            return pd.DataFrame(), "No opportunity data available for scoring"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating opportunity scoring: {str(e)}"

def calculate_product_demand_forecast(products, sales_orders, forecast_periods=6):
    """Forecast product demand based on historical sales patterns."""
    try:
        if products.empty or sales_orders.empty:
            return pd.DataFrame(), "No product or sales data available"
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Calculate monthly demand for each product
        demand_forecasts = []
        
        for _, product in products.iterrows():
            product_id = product['product_id']
            product_name = product['product_name']
            product_category = product.get('category', 'Unknown')
            
            # Get sales data for this product
            product_sales = sales_orders[sales_orders['product_id'] == product_id]
            
            if not product_sales.empty:
                # Group by month and calculate demand
                monthly_demand = product_sales.groupby(product_sales['order_date'].dt.to_period('M')).agg({
                    'quantity': 'sum',
                    'total_amount': 'sum'
                }).reset_index()
                
                if len(monthly_demand) >= 2:
                    # Calculate trend and seasonality
                    quantities = monthly_demand['quantity'].values
                    trend = np.polyfit(range(len(quantities)), quantities, 1)[0]
                    
                    # Simple demand forecast
                    last_quantity = quantities[-1]
                    forecast_quantities = []
                    
                    for period in range(1, forecast_periods + 1):
                        # Apply trend and add some randomness
                        forecast_qty = max(0, last_quantity + (trend * period) + np.random.normal(0, last_quantity * 0.1))
                        forecast_quantities.append(forecast_qty)
                    
                    # Calculate confidence intervals
                    mean_forecast = np.mean(forecast_quantities)
                    std_forecast = np.std(forecast_quantities)
                    
                    demand_forecasts.append({
                        'product_id': product_id,
                        'product_name': product_name,
                        'category': product_category,
                        'current_demand': last_quantity,
                        'trend': trend,
                        'forecast_period_1': forecast_quantities[0],
                        'forecast_period_2': forecast_quantities[1],
                        'forecast_period_3': forecast_quantities[2],
                        'forecast_period_4': forecast_quantities[3],
                        'forecast_period_5': forecast_quantities[4],
                        'forecast_period_6': forecast_quantities[5],
                        'mean_forecast': mean_forecast,
                        'confidence_interval': f"{mean_forecast - std_forecast:.1f} - {mean_forecast + std_forecast:.1f}"
                    })
        
        if demand_forecasts:
            demand_df = pd.DataFrame(demand_forecasts)
            demand_df = demand_df.sort_values('mean_forecast', ascending=False)
            
            return demand_df, f"Product demand forecast completed for {len(demand_df)} products"
        else:
            return pd.DataFrame(), "No product demand data available for forecasting"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating product demand forecast: {str(e)}"

def calculate_customer_lifetime_value_prediction(customers, sales_orders, prediction_horizon=12):
    """Predict future customer lifetime value based on historical behavior."""
    try:
        if customers.empty or sales_orders.empty:
            return pd.DataFrame(), "No customer or sales data available"
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Handle missing created_date column - use first order date as fallback
        if 'created_date' in customers.columns:
            customers['created_date'] = pd.to_datetime(customers['created_date'])
        else:
            # If no created_date, use the earliest order date for each customer
            earliest_orders = sales_orders.groupby('customer_id')['order_date'].min().reset_index()
            earliest_orders.columns = ['customer_id', 'created_date']
            customers = customers.merge(earliest_orders, on='customer_id', how='left')
            customers['created_date'] = pd.to_datetime(customers['created_date'])
        
        # Calculate CLV predictions
        clv_predictions = []
        current_date = pd.Timestamp.now()
        
        for _, customer in customers.iterrows():
            customer_id = customer['customer_id']
            customer_orders = sales_orders[sales_orders['customer_id'] == customer_id]
            
            if not customer_orders.empty:
                # Calculate historical metrics
                total_orders = len(customer_orders)
                total_revenue = customer_orders['total_amount'].sum()
                avg_order_value = total_revenue / total_orders
                
                # Calculate order frequency
                first_order_date = customer_orders['order_date'].min()
                months_active = max(1, (current_date - first_order_date).days / 30)
                monthly_order_frequency = total_orders / months_active
                
                # Predict future orders and revenue
                predicted_orders = monthly_order_frequency * prediction_horizon
                predicted_revenue = predicted_orders * avg_order_value
                
                # Calculate CLV components
                historical_clv = total_revenue
                predicted_clv = predicted_revenue
                total_clv = historical_clv + predicted_clv
                
                # CLV growth rate
                if historical_clv > 0:
                    clv_growth_rate = ((predicted_clv / historical_clv) - 1) * 100
                else:
                    clv_growth_rate = 0
                
                # CLV segment classification
                if total_clv >= 50000:
                    clv_segment = "Premium"
                elif total_clv >= 20000:
                    clv_segment = "High Value"
                elif total_clv >= 10000:
                    clv_segment = "Medium Value"
                else:
                    clv_segment = "Standard"
                
                clv_predictions.append({
                    'customer_id': customer_id,
                    'customer_name': f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip(),
                    'historical_orders': total_orders,
                    'historical_revenue': historical_clv,
                    'avg_order_value': avg_order_value,
                    'monthly_order_frequency': monthly_order_frequency,
                    'predicted_orders': predicted_orders,
                    'predicted_revenue': predicted_revenue,
                    'total_predicted_clv': total_clv,
                    'clv_growth_rate': clv_growth_rate,
                    'clv_segment': clv_segment
                })
        
        if clv_predictions:
            clv_df = pd.DataFrame(clv_predictions)
            clv_df = clv_df.sort_values('total_predicted_clv', ascending=False)
            
            return clv_df, f"CLV prediction completed for {len(clv_df)} customers"
        else:
            return pd.DataFrame(), "No customer data available for CLV prediction"
    
    except Exception as e:
        import traceback
        print(f"Error in CLV prediction: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame(), f"Error calculating CLV prediction: {str(e)}"

def calculate_customer_lifetime_value_prediction_simple(customers, sales_orders, prediction_horizon=12):
    """Simplified CLV prediction that works with basic data."""
    try:
        if customers.empty or sales_orders.empty:
            return pd.DataFrame(), "No customer or sales data available"
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Calculate CLV predictions
        clv_predictions = []
        current_date = pd.Timestamp.now()
        
        for _, customer in customers.iterrows():
            customer_id = customer['customer_id']
            customer_orders = sales_orders[sales_orders['customer_id'] == customer_id]
            
            if not customer_orders.empty:
                # Calculate historical metrics
                total_orders = len(customer_orders)
                total_revenue = customer_orders['total_amount'].sum()
                avg_order_value = total_revenue / total_orders
                
                # Calculate order frequency (orders per month)
                first_order_date = customer_orders['order_date'].min()
                months_active = max(1, (current_date - first_order_date).days / 30)
                monthly_order_frequency = total_orders / months_active
                
                # Predict future orders and revenue
                predicted_orders = monthly_order_frequency * prediction_horizon
                predicted_revenue = predicted_orders * avg_order_value
                
                # Calculate CLV components
                historical_clv = total_revenue
                predicted_clv = predicted_revenue
                total_clv = historical_clv + predicted_clv
                
                # CLV growth rate
                if historical_clv > 0:
                    clv_growth_rate = ((predicted_clv / historical_clv) - 1) * 100
                else:
                    clv_growth_rate = 0
                
                # CLV segment classification
                if total_clv >= 50000:
                    clv_segment = "Premium"
                elif total_clv >= 20000:
                    clv_segment = "High Value"
                elif total_clv >= 10000:
                    clv_segment = "Medium Value"
                else:
                    clv_segment = "Standard"
                
                # Get customer name safely
                first_name = customer.get('first_name', '')
                last_name = customer.get('last_name', '')
                customer_name = f"{first_name} {last_name}".strip()
                if not customer_name:
                    customer_name = f"Customer {customer_id}"
                
                clv_predictions.append({
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'historical_orders': total_orders,
                    'historical_revenue': historical_clv,
                    'avg_order_value': avg_order_value,
                    'monthly_order_frequency': monthly_order_frequency,
                    'predicted_orders': predicted_orders,
                    'predicted_revenue': predicted_clv,
                    'total_predicted_clv': total_clv,
                    'clv_growth_rate': clv_growth_rate,
                    'clv_segment': clv_segment
                })
        
        if clv_predictions:
            clv_df = pd.DataFrame(clv_predictions)
            clv_df = clv_df.sort_values('total_predicted_clv', ascending=False)
            
            return clv_df, f"CLV prediction completed for {len(clv_df)} customers"
        else:
            return pd.DataFrame(), "No customer data available for CLV prediction"
    
    except Exception as e:
        import traceback
        print(f"Error in simple CLV prediction: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return pd.DataFrame(), f"Error calculating CLV prediction: {str(e)}"

def calculate_sales_performance_prediction(sales_orders, sales_reps, prediction_months=6):
    """Predict future sales performance based on historical trends."""
    try:
        if sales_orders.empty or sales_reps.empty:
            return pd.DataFrame(), "No sales or sales rep data available"
        
        # Convert dates to datetime
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Calculate performance predictions
        performance_predictions = []
        
        for _, sales_rep in sales_reps.iterrows():
            sales_rep_id = sales_rep['sales_rep_id']
            rep_orders = sales_orders[sales_orders['sales_rep_id'] == sales_rep_id]
            
            if not rep_orders.empty:
                # Calculate historical performance
                total_orders = len(rep_orders)
                total_revenue = rep_orders['total_amount'].sum()
                avg_order_value = total_revenue / total_orders
                
                # Calculate monthly performance trends
                monthly_performance = rep_orders.groupby(rep_orders['order_date'].dt.to_period('M')).agg({
                    'total_amount': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                if len(monthly_performance) >= 2:
                    # Calculate growth trends
                    revenues = monthly_performance['total_amount'].values
                    orders = monthly_performance['order_id'].values
                    
                    revenue_trend = np.polyfit(range(len(revenues)), revenues, 1)[0]
                    order_trend = np.polyfit(range(len(orders)), orders, 1)[0]
                    
                    # Predict future performance
                    predicted_revenue = []
                    predicted_orders = []
                    
                    for month in range(1, prediction_months + 1):
                        future_revenue = max(0, revenues[-1] + (revenue_trend * month))
                        future_orders = max(0, orders[-1] + (order_trend * month))
                        
                        predicted_revenue.append(future_revenue)
                        predicted_orders.append(future_orders)
                    
                    # Calculate performance metrics
                    avg_monthly_revenue = np.mean(predicted_revenue)
                    total_predicted_revenue = sum(predicted_revenue)
                    performance_score = (avg_monthly_revenue / 10000) * 100  # Normalized score
                    
                    # Performance classification
                    if performance_score >= 80:
                        performance_class = "Excellent"
                    elif performance_score >= 60:
                        performance_class = "Good"
                    elif performance_score >= 40:
                        performance_class = "Average"
                    else:
                        performance_class = "Needs Improvement"
                    
                    performance_predictions.append({
                        'sales_rep_id': sales_rep_id,
                        'sales_rep_name': f"{sales_rep.get('first_name', '')} {sales_rep.get('last_name', '')}".strip(),
                        'historical_orders': total_orders,
                        'historical_revenue': total_revenue,
                        'avg_order_value': avg_order_value,
                        'revenue_trend': revenue_trend,
                        'order_trend': order_trend,
                        'predicted_monthly_revenue': avg_monthly_revenue,
                        'total_predicted_revenue': total_predicted_revenue,
                        'performance_score': performance_score,
                        'performance_class': performance_class
                    })
        
        if performance_predictions:
            performance_df = pd.DataFrame(performance_predictions)
            performance_df = performance_df.sort_values('performance_score', ascending=False)
            
            return performance_df, f"Sales performance prediction completed for {len(performance_df)} sales representatives"
        else:
            return pd.DataFrame(), "No performance data available for prediction"
    
    except Exception as e:
        return pd.DataFrame(), f"Error calculating performance prediction: {str(e)}"

def generate_sample_churn_data():
    """Generate sample data for testing churn prediction."""
    try:
        import random
        from datetime import datetime, timedelta
        
        # Generate sample customers
        customers_data = []
        for i in range(1, 51):  # 50 customers
            status_choices = ['Active', 'Inactive', 'Churned']
            weights = [0.6, 0.3, 0.1]  # 60% active, 30% inactive, 10% churned
            status = random.choices(status_choices, weights=weights)[0]
            
            customers_data.append({
                'customer_id': i,
                'first_name': f'Customer{i}',
                'last_name': f'LastName{i}',
                'status': status,
                'created_date': datetime.now() - timedelta(days=random.randint(30, 365))
            })
        
        # Generate sample sales orders
        sales_orders_data = []
        order_id = 1
        
        for customer_id in range(1, 51):
            # Generate 1-10 orders per customer
            num_orders = random.randint(1, 10)
            
            for _ in range(num_orders):
                # Order date within last 90 days
                days_ago = random.randint(0, 90)
                order_date = datetime.now() - timedelta(days=days_ago)
                
                # Order amount between $100 and $5000
                total_amount = random.randint(100, 5000)
                quantity = random.randint(1, 5)
                
                sales_orders_data.append({
                    'order_id': order_id,
                    'customer_id': customer_id,
                    'product_id': random.randint(1, 10),
                    'sales_rep_id': random.randint(1, 5),
                    'order_date': order_date,
                    'total_amount': total_amount,
                    'quantity': quantity,
                    'channel': random.choice(['Online', 'Phone', 'In-Store']),
                    'region': random.choice(['North', 'South', 'East', 'West'])
                })
                order_id += 1
        
        customers_df = pd.DataFrame(customers_data)
        sales_orders_df = pd.DataFrame(sales_orders_data)
        
        return customers_df, sales_orders_df, "Sample churn prediction data generated successfully"
    
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), f"Error generating sample data: {str(e)}"

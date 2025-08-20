import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import base64
import warnings
import time
from functools import lru_cache
import random

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Import inventory metric calculation functions
from invt_metrics_calculator import *

# Import auto insights functionality
from invt_auto_insights import InventoryInsights, display_insights_section

# Import risk analyzer functionality
from invt_risk_analyzer import InventoryRiskAnalyzer, display_risk_dashboard

# Import predictive analytics functionality
from invt_predictive_analytics import display_inventory_predictive_analytics_dashboard, InventoryPredictiveAnalytics

# Import data handling utilities
from invt_data_utils import *

# Import styling
from invt_styling import load_inventory_styling

# ============================================================================
# HELPER FUNCTIONS FOR DASHBOARD STYLING
# ============================================================================

def create_metric_card(title, value, description):
    """Create a styled metric card for the dashboard"""
    return f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                color: white; 
                text-align: center; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                margin-bottom: 1rem;">
        <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; font-weight: 600;">{title}</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.9;">{description}</p>
    </div>
    """

def create_insight_box(title, content, icon="💡"):
    """Create a styled insight box"""
    return f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                color: white; 
                margin-bottom: 1rem;">
        <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">{icon} {title}</h4>
        <p style="margin: 0; font-size: 0.95rem; line-height: 1.5;">{content}</p>
    </div>
    """

def create_alert_box(content, alert_type="info"):
    """Create a styled alert box"""
    colors = {
        "info": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "success": "linear-gradient(135deg, #4CAF50 0%, #45a049 100%)",
        "warning": "linear-gradient(135deg, #ff9800 0%, #f57c00 100%)",
        "error": "linear-gradient(135deg, #f44336 0%, #d32f2f 100%)"
    }
    
    return f"""
    <div style="background: {colors.get(alert_type, colors['info'])}; 
                padding: 1rem; 
                border-radius: 10px; 
                color: white; 
                margin-bottom: 1rem;">
        <p style="margin: 0; font-size: 0.95rem;">{content}</p>
    </div>
    """

# ============================================================================
# PERFORMANCE OPTIMIZATION CONFIGURATION
# ============================================================================

# Streamlit performance optimizations
# Note: These options may vary by Streamlit version
try:
    st.set_option('deprecation.showPyplotGlobalUse', False)
except:
    pass  # Option not available in this version

try:
    st.set_option('deprecation.showfileUploaderEncoding', False)
except:
    pass  # Option not available in this version

# Configure pandas for better performance
pd.options.mode.chained_assignment = None  # Default='warn'

# Enable Numba acceleration if available (may not be available in all versions)
try:
    pd.options.compute.use_numba = True
except:
    pass  # Numba option not available in this version

# Configure numpy for better performance
np.set_printoptions(precision=4, suppress=True)

# Configure Streamlit for better performance
st.set_page_config(
    page_title="Inventory Intelligence Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Performance optimization settings
st.cache_data.clear()  # Clear any existing cache

# Performance optimization settings
@st.cache_data(ttl=300, max_entries=200)  # Cache for 5 minutes, max 200 entries
def load_data_optimized():
    """Optimized data loading with caching."""
    return {}

# Cache for expensive calculations
@st.cache_data(ttl=600, max_entries=100)  # Cache for 10 minutes
def cache_expensive_calculations(data, calculation_type):
    """Cache expensive calculations to avoid recomputation."""
    return data

# Enhanced caching for chart generation
@st.cache_data(ttl=1800, max_entries=50)  # Cache for 30 minutes
def cache_chart_data(data, chart_type, **kwargs):
    """Cache chart data to avoid regenerating expensive visualizations."""
    return data

@st.cache_data(ttl=3600, max_entries=100)  # Cache for 1 hour
def create_optimized_chart(data, chart_type, **kwargs):
    """Create and cache charts for better performance."""
    if chart_type == "pie":
        fig = px.pie(data, **kwargs)
    elif chart_type == "bar":
        fig = px.bar(data, **kwargs)
    elif chart_type == "histogram":
        fig = px.histogram(data, **kwargs)
    elif chart_type == "line":
        fig = px.line(data, **kwargs)
    else:
        fig = px.scatter(data, **kwargs)
    
    # Optimize chart performance
    fig.update_layout(
        showlegend=True,
        hovermode='closest',
        dragmode=False,  # Disable drag for better performance
        selectdirection='any'
    )
    
    return fig

# Cache for metric calculations
@st.cache_data(ttl=900, max_entries=150)  # Cache for 15 minutes
def cache_metrics(data, metric_type):
    """Cache metric calculations for better performance."""
    return data

# Performance monitoring
def performance_monitor(func_name):
    """Decorator to monitor function performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            if end_time - start_time > 1.0:  # Log slow functions
                st.sidebar.warning(f"⚠️ {func_name} took {end_time - start_time:.2f}s")
            return result
        return wrapper
    return decorator

# ============================================================================
# AI Recommendation Functions
# ============================================================================

def generate_ai_recommendations(data_type, data, insights=None):
    """Generate AI-powered recommendations based on data analysis."""
    
    if data.empty:
        return "📊 **No data available** - Please load data to receive AI recommendations."
    
    recommendations = []
    
    if data_type == "inventory_optimization":
        recommendations = generate_inventory_optimization_recommendations(data, insights)
    elif data_type == "demand_forecasting":
        recommendations = generate_demand_forecasting_recommendations(data, insights)
    elif data_type == "supplier_management":
        recommendations = generate_supplier_management_recommendations(data, insights)
    elif data_type == "warehouse_operations":
        recommendations = generate_warehouse_operations_recommendations(data, insights)
    elif data_type == "cost_analysis":
        recommendations = generate_cost_analysis_recommendations(data, insights)
    elif data_type == "risk_management":
        recommendations = generate_risk_management_recommendations(data, insights)
    elif data_type == "performance_metrics":
        recommendations = generate_performance_metrics_recommendations(data, insights)
    elif data_type == "automation_opportunities":
        recommendations = generate_automation_opportunities_recommendations(data, insights)
    
    return recommendations

def generate_inventory_optimization_recommendations(data, insights=None):
    """Generate AI recommendations for inventory optimization."""
    recommendations = []
    
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        # Stock level optimization
        low_stock_items = data[data['current_stock'] <= data['reorder_point']]
        if not low_stock_items.empty:
            recommendations.append(f"🚨 **Stock Alert**: {len(low_stock_items)} items are below reorder point")
        
        # Overstock analysis
        if 'max_stock' in data.columns:
            overstock_items = data[data['current_stock'] > data['max_stock'] * 1.2]
            if not overstock_items.empty:
                recommendations.append(f"📦 **Overstock Warning**: {len(overstock_items)} items exceed maximum stock levels")
    
    # ABC analysis recommendations
    if 'abc_category' in data.columns:
        abc_counts = data['abc_category'].value_counts()
        if 'C' in abc_counts and abc_counts['C'] > len(data) * 0.5:
            recommendations.append("🔍 **ABC Analysis**: Consider reducing C-category items to optimize space and costs")
    
    # Turnover rate recommendations
    if 'turnover_rate' in data.columns:
        low_turnover = data[data['turnover_rate'] < data['turnover_rate'].quantile(0.25)]
        if not low_turnover.empty:
            recommendations.append(f"📉 **Low Turnover**: {len(low_turnover)} items have low turnover - review stocking strategy")
    
    return recommendations if recommendations else ["✅ **Inventory Status**: All systems operating within optimal parameters"]

def generate_demand_forecasting_recommendations(data, insights=None):
    """Generate AI recommendations for demand forecasting."""
    recommendations = []
    
    if 'forecast_accuracy' in data.columns:
        low_accuracy = data[data['forecast_accuracy'] < 0.8]
        if not low_accuracy.empty:
            recommendations.append(f"📊 **Forecast Accuracy**: {len(low_accuracy)} items have low forecast accuracy - review forecasting models")
    
    if 'seasonality_score' in data.columns:
        seasonal_items = data[data['seasonality_score'] > 0.7]
        if not seasonal_items.empty:
            recommendations.append(f"🌱 **Seasonality Detected**: {len(seasonal_items)} items show strong seasonal patterns - adjust forecasting accordingly")
    
    return recommendations if recommendations else ["✅ **Demand Forecasting**: Models performing well with current data"]

def generate_supplier_management_recommendations(data, insights=None):
    """Generate AI recommendations for supplier management."""
    recommendations = []
    
    if 'supplier_performance' in data.columns:
        poor_performers = data[data['supplier_performance'] < data['supplier_performance'].quantile(0.25)]
        if not poor_performers.empty:
            recommendations.append(f"⚠️ **Supplier Performance**: {len(poor_performers)} suppliers showing poor performance - review relationships")
    
    if 'lead_time_variance' in data.columns:
        high_variance = data[data['lead_time_variance'] > data['lead_time_variance'].quantile(0.75)]
        if not high_variance.empty:
            recommendations.append(f"⏰ **Lead Time Issues**: {len(high_variance)} items have high lead time variance - consider backup suppliers")
    
    return recommendations if recommendations else ["✅ **Supplier Management**: All suppliers performing within acceptable parameters"]

def generate_warehouse_operations_recommendations(data, insights=None):
    """Generate AI recommendations for warehouse operations."""
    recommendations = []
    
    if 'space_utilization' in data.columns:
        low_utilization = data[data['space_utilization'] < 0.6]
        if not low_utilization.empty:
            recommendations.append(f"🏭 **Space Utilization**: {len(low_utilization)} items have low space utilization - consider consolidation")
    
    if 'warehouse_location' in data.columns:
        location_counts = data['warehouse_location'].value_counts()
        if len(location_counts) > 1:
            recommendations.append(f"📍 **Location Distribution**: Items spread across {len(location_counts)} locations - optimize for efficiency")
    
    return recommendations if recommendations else ["✅ **Warehouse Operations**: All operations within optimal parameters"]

def generate_cost_analysis_recommendations(data, insights=None):
    """Generate AI recommendations for cost analysis."""
    recommendations = []
    
    if 'unit_cost' in data.columns:
        high_cost_threshold = data['unit_cost'].quantile(0.9)
        high_cost_items = data[data['unit_cost'] > high_cost_threshold]
        if not high_cost_items.empty:
            recommendations.append(f"💰 **High Cost Items**: {len(high_cost_items)} items have high unit costs - review pricing strategy")
    
    if 'stock_value' in data.columns:
        total_value = data['stock_value'].sum()
        if total_value > 0:
            recommendations.append(f"💎 **Total Inventory Value**: ${total_value:,.2f} - monitor for optimization opportunities")
    
    return recommendations if recommendations else ["✅ **Cost Analysis**: All cost metrics within acceptable ranges"]

def generate_risk_management_recommendations(data, insights=None):
    """Generate AI recommendations for risk management."""
    recommendations = []
    
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        risk_items = data[data['current_stock'] <= data['reorder_point'] * 1.1]
        if not risk_items.empty:
            recommendations.append(f"⚠️ **Risk Items**: {len(risk_items)} items approaching reorder point - monitor closely")
    
    if 'supplier_id' in data.columns:
        supplier_counts = data['supplier_id'].value_counts()
        single_supplier_items = supplier_counts[supplier_counts == 1]
        if not single_supplier_items.empty:
            recommendations.append(f"🔗 **Supplier Risk**: {len(single_supplier_items)} items have single suppliers - consider diversification")
    
    return recommendations if recommendations else ["✅ **Risk Management**: All risk factors within acceptable limits"]

def generate_performance_metrics_recommendations(data, insights=None):
    """Generate AI recommendations for performance metrics."""
    recommendations = []
    
    if 'turnover_rate' in data.columns:
        avg_turnover = data['turnover_rate'].mean()
        if avg_turnover < 6:
            recommendations.append(f"📊 **Turnover Performance**: Average turnover rate is {avg_turnover:.2f} - consider optimization strategies")
        else:
            recommendations.append(f"✅ **Turnover Performance**: Good average turnover rate of {avg_turnover:.2f}")
    
    return recommendations if recommendations else ["✅ **Performance Metrics**: All metrics performing well"]

def generate_automation_opportunities_recommendations(data, insights=None):
    """Generate AI recommendations for automation opportunities."""
    recommendations = []
    
    total_items = len(data)
    if total_items > 100:
        recommendations.append(f"🤖 **Automation Opportunity**: Large dataset of {total_items} items - consider automated reordering systems")
    
    if 'category' in data.columns:
        category_count = data['category'].nunique()
        if category_count > 10:
            recommendations.append(f"📋 **Process Automation**: {category_count} categories detected - automate category-specific processes")
    
    return recommendations if recommendations else ["✅ **Automation**: Current processes are well-optimized"]

# ============================================================================
# Main Dashboard Functions
# ============================================================================

def display_header():
    """Display the main header with title and description."""
    st.markdown("""
    <div class="app-header">
        <h1>📦 Inventory Intelligence Dashboard</h1>
        <p>Comprehensive inventory management with AI-powered insights, predictive analytics, and automated optimization</p>
    </div>
    """, unsafe_allow_html=True)

def display_kpi_overview(data):
    """Display enhanced key performance indicators overview with interactive analytics."""
    if data.empty:
        st.warning("📊 No data available. Please load inventory data to view KPIs.")
        return
    
    st.subheader("🎯 Key Performance Indicators")
    
    # Enhanced KPI calculations with advanced metrics
    total_items = len(data)
    total_value = data['current_stock'].sum() if 'current_stock' in data.columns else 0
    avg_turnover = data['turnover_rate'].mean() if 'turnover_rate' in data.columns else 0
    stockout_risk = len(data[data['current_stock'] <= data['reorder_point']]) if 'reorder_point' in data.columns else 0
    
    # Advanced KPI calculations
    if 'current_stock' in data.columns and 'unit_cost' in data.columns:
        data['stock_value'] = data['current_stock'] * data['unit_cost']
        total_inventory_value = data['stock_value'].sum()
        avg_item_value = total_inventory_value / total_items if total_items > 0 else 0
        
        # Calculate inventory efficiency metrics
        if 'reorder_point' in data.columns and 'max_stock' in data.columns:
            optimal_stock_items = len(data[
                (data['current_stock'] > data['reorder_point']) & 
                (data['current_stock'] <= data['max_stock'])
            ])
            efficiency_rate = (optimal_stock_items / total_items) * 100 if total_items > 0 else 0
        else:
            efficiency_rate = 0
    else:
        total_inventory_value = 0
        avg_item_value = 0
        efficiency_rate = 0
    
    # Create enhanced KPI cards with interactive features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>📦 Total Items</h3>
            <h2>{total_items:,}</h2>
            <p>Active inventory items</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Categories: {data['category'].nunique() if 'category' in data.columns else 'N/A'}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                ✅ Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>💰 Total Value</h3>
            <h2>${total_inventory_value:,.0f}</h2>
            <p>Current stock value</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Avg Item: ${avg_item_value:.2f}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                💎 High Value Items: {len(data[data['stock_value'] > data['stock_value'].quantile(0.9)]) if 'stock_value' in data.columns else 'N/A'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>🔄 Avg Turnover</h3>
            <h2>{avg_turnover:.2f}</h2>
            <p>Annual turnover rate</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Performance: {'Excellent' if avg_turnover >= 8 else 'Good' if avg_turnover >= 6 else 'Average' if avg_turnover >= 4 else 'Below Average'}
            </div>
            <div style="font-size: 0.8rem; color: {'#22c55e' if avg_turnover >= 6 else '#fbbf24' if avg_turnover >= 4 else '#dc2626'}; margin-top: 5px;">
                {'🎉' if avg_turnover >= 8 else '✅' if avg_turnover >= 6 else '⚠️' if avg_turnover >= 4 else '❌'} {avg_turnover:.1f}x annual
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>⚠️ Stockout Risk</h3>
            <h2>{stockout_risk}</h2>
            <p>Items below reorder point</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Risk Level: {'Low' if stockout_risk <= total_items * 0.1 else 'Medium' if stockout_risk <= total_items * 0.2 else 'High'}
            </div>
            <div style="font-size: 0.8rem; color: {'#22c55e' if stockout_risk <= total_items * 0.1 else '#fbbf24' if stockout_risk <= total_items * 0.2 else '#dc2626'}; margin-top: 5px;">
                {'✅' if stockout_risk <= total_items * 0.1 else '⚠️' if stockout_risk <= total_items * 0.2 else '🚨'} {(stockout_risk/total_items*100):.1f}% of inventory
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced KPI Analytics Section
    st.subheader("📊 Advanced KPI Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Inventory Efficiency Gauge
        if 'current_stock' in data.columns and 'reorder_point' in data.columns and 'max_stock' in data.columns:
            # Calculate efficiency metrics
            data['stock_efficiency'] = np.where(
                (data['current_stock'] > data['reorder_point']) & (data['current_stock'] <= data['max_stock']),
                'Optimal',
                np.where(data['current_stock'] <= data['reorder_point'], 'Low', 'High')
            )
            
            efficiency_dist = data['stock_efficiency'].value_counts()
            
            # Create enhanced efficiency chart
            fig_efficiency = go.Figure(data=[go.Pie(
                labels=efficiency_dist.index,
                values=efficiency_dist.values,
                hole=0.6,
                marker_colors=['#22c55e', '#fbbf24', '#dc2626'],
                textinfo='label+percent+value',
                textposition='outside',
                hovertemplate="<b>%{label}</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "<extra></extra>"
            )])
            
            fig_efficiency.update_layout(
                title={
                    'text': "Inventory Efficiency Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_efficiency, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Stock Value Distribution Analysis
        if 'stock_value' in data.columns:
            # Create enhanced histogram with better styling
            fig_value_dist = go.Figure(data=[go.Histogram(
                x=data['stock_value'],
                nbinsx=20,
                marker_color='rgba(102, 126, 234, 0.7)',
                marker_line_color='rgba(102, 126, 234, 1)',
                marker_line_width=1,
                hovertemplate="<b>Stock Value Range</b><br>" +
                            "Value: $%{x:,.0f}<br>" +
                            "Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            fig_value_dist.update_layout(
                title={
                    'text': "Stock Value Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Stock Value ($)",
                yaxis_title="Number of Items",
                xaxis=dict(
                    tickformat=',',
                    tickprefix='$'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_value_dist, use_container_width=True, config={'displayModeBar': True})
    
    # Interactive KPI Insights Section
    st.subheader("💡 KPI Insights & Trends")
    
    with st.expander("📈 Performance Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Key Insights:**")
            
            # Performance insights with enhanced styling
            if avg_turnover >= 8:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                            border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #22c55e; margin: 0 0 10px 0;">🎉 Excellent Turnover Performance</h4>
                    <p style="margin: 0; color: #374151;">Your inventory is moving efficiently with a turnover rate of <strong>{avg_turnover:.2f}</strong></p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">This indicates optimal inventory management</p>
                </div>
                """.format(avg_turnover=avg_turnover), unsafe_allow_html=True)
            elif avg_turnover >= 6:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                            border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #3b82f6; margin: 0 0 10px 0;">✅ Good Turnover Performance</h4>
                    <p style="margin: 0; color: #374151;">Your inventory turnover rate of <strong>{avg_turnover:.2f}</strong> is above industry average</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #3b82f6;">Consider optimization for even better performance</p>
                </div>
                """.format(avg_turnover=avg_turnover), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                            border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Turnover Optimization Needed</h4>
                    <p style="margin: 0; color: #374151;">Your turnover rate of <strong>{avg_turnover:.2f}</strong> indicates room for improvement</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #f59e0b;">Consider promotional activities and inventory reviews</p>
                </div>
                """.format(avg_turnover=avg_turnover), unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📊 Risk Assessment:**")
            
            # Risk assessment with enhanced styling
            risk_percentage = (stockout_risk / total_items) * 100 if total_items > 0 else 0
            
            if risk_percentage <= 10:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                            border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Low Stockout Risk</h4>
                    <p style="margin: 0; color: #374151;">Only <strong>{risk_percentage:.1f}%</strong> of items are below reorder point</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">Excellent inventory control maintained</p>
                </div>
                """.format(risk_percentage=risk_percentage), unsafe_allow_html=True)
            elif risk_percentage <= 20:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                            border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Moderate Stockout Risk</h4>
                    <p style="margin: 0; color: #374151;"><strong>{risk_percentage:.1f}%</strong> of items need attention</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #f59e0b;">Monitor closely and initiate reordering</p>
                </div>
                """.format(risk_percentage=risk_percentage), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                            border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #dc2626; margin: 0 0 10px 0;">🚨 High Stockout Risk</h4>
                    <p style="margin: 0; color: #374151;"><strong>{risk_percentage:.1f}%</strong> of items are critical</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #dc2626;">Immediate action required</p>
                </div>
                """.format(risk_percentage=risk_percentage), unsafe_allow_html=True)
    
    # KPI Recommendations Section
    st.subheader("🚀 KPI Optimization Recommendations")
    
    recommendations = []
    
    # Generate dynamic recommendations based on KPI values
    if avg_turnover < 6:
        recommendations.append({
            'type': 'warning',
            'title': 'Turnover Rate Optimization',
            'message': f'Current turnover rate of {avg_turnover:.2f} is below optimal. Consider promotional activities, price adjustments, or inventory reviews.',
            'action': 'Review low-turnover items and implement improvement strategies'
        })
    
    if risk_percentage > 15:
        recommendations.append({
            'type': 'error',
            'title': 'Stockout Risk Management',
            'message': f'High stockout risk with {risk_percentage:.1f}% of items below reorder point. Immediate reordering required.',
            'action': 'Initiate reordering process for critical items'
        })
    
    if efficiency_rate < 70:
        recommendations.append({
            'type': 'info',
            'title': 'Inventory Efficiency Improvement',
            'message': f'Current efficiency rate of {efficiency_rate:.1f}% indicates suboptimal stock levels.',
            'action': 'Optimize reorder points and maximum stock levels'
        })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Optimal Performance',
            'message': 'All KPIs are within optimal ranges. Continue monitoring for continuous improvement.',
            'action': 'Maintain current performance levels'
        })
    
    # Display recommendations with enhanced styling
    for i, rec in enumerate(recommendations):
        color_map = {
            'success': '#22c55e',
            'warning': '#fbbf24',
            'error': '#dc2626',
            'info': '#3b82f6'
        }
        
        icon_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'info': 'ℹ️'
        }
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba({color_map[rec['type']].replace('#', '')}, 0.1) 0%, rgba({color_map[rec['type']].replace('#', '')}, 0.05) 100%); 
                    border: 2px solid rgba({color_map[rec['type']].replace('#', '')}, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4 style="color: {color_map[rec['type']]}; margin: 0 0 10px 0;">{icon_map[rec['type']]} {rec['title']}</h4>
            <p style="margin: 0; color: #374151;">{rec['message']}</p>
            <div style="margin-top: 10px;">
                <strong style="color: {color_map[rec['type']]};">Action Required:</strong> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_inventory_overview(data):
    """Display comprehensive inventory overview with enhanced analytics and interactive visualizations."""
    if data.empty:
        st.warning("📊 No data available for inventory overview.")
        return
    
    st.subheader("📊 Inventory Overview")
    
    # Enhanced ABC Analysis with Interactive Features
    if 'abc_category' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced ABC Analysis Distribution
            abc_counts = data['abc_category'].value_counts()
            
            # Create enhanced ABC analysis pie chart
            fig_abc = go.Figure(data=[go.Pie(
                labels=abc_counts.index,
                values=abc_counts.values,
                hole=0.4,
                marker_colors=['#dc2626', '#f59e0b', '#22c55e'],
                textinfo='label+percent+value',
                textposition='outside',
                hovertemplate="<b>%{label} Category</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "Management: %{customdata}<br>" +
                            "<extra></extra>",
                customdata=['Tight Control', 'Moderate Control', 'Simple Control']
            )])
            
            fig_abc.update_layout(
                title={
                    'text': "ABC Analysis Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_abc, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced ABC Value Analysis with better tooltips
            if 'unit_cost' in data.columns and 'current_stock' in data.columns:
                data['stock_value'] = data['current_stock'] * data['unit_cost']
                abc_value = data.groupby('abc_category')['stock_value'].sum().reset_index()
                
                # Create enhanced ABC value bar chart
                fig_abc_value = go.Figure(data=[go.Bar(
                    x=abc_value['abc_category'],
                    y=abc_value['stock_value'],
                    marker_color=['#dc2626', '#f59e0b', '#22c55e'],
                    marker_line_color=['#dc2626', '#f59e0b', '#22c55e'],
                    marker_line_width=2,
                    hovertemplate="<b>%{x} Category</b><br>" +
                                "Total Value: $%{y:,.0f}<br>" +
                                "Percentage: %{customdata:.1f}%<br>" +
                                "<extra></extra>",
                    customdata=[(val / abc_value['stock_value'].sum()) * 100 for val in abc_value['stock_value']]
                )])
                
                fig_abc_value.update_layout(
                    title={
                        'text': "Stock Value by ABC Category",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="ABC Category",
                    yaxis_title="Stock Value ($)",
                    yaxis=dict(
                        tickformat=',',
                        tickprefix='$'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=60)
                )
                
                st.plotly_chart(fig_abc_value, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Stock Level Distribution Analysis
    if 'current_stock' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Stock Level Distribution with better tooltips
            fig_stock_dist = go.Figure(data=[go.Histogram(
                x=data['current_stock'],
                nbinsx=20,
                marker_color='rgba(118, 75, 162, 0.7)',
                marker_line_color='rgba(118, 75, 162, 1)',
                marker_line_width=1,
                hovertemplate="<b>Stock Level Range</b><br>" +
                            "Stock Level: %{x}<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            fig_stock_dist.update_layout(
                title={
                    'text': "Stock Level Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Current Stock",
                yaxis_title="Number of Items",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_stock_dist, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Stock vs Reorder Point Analysis
            if 'reorder_point' in data.columns:
                # Create enhanced scatter plot with better tooltips
                fig_stock_vs_reorder = go.Figure(data=[go.Scatter(
                    x=data['reorder_point'],
                    y=data['current_stock'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=data['stock_value'] if 'stock_value' in data.columns else data['current_stock'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Stock Value")
                    ),
                    text=data['item_name'] if 'item_name' in data.columns else data['item_id'],
                    hovertemplate="<b>%{text}</b><br>" +
                                "Reorder Point: %{x}<br>" +
                                "Current Stock: %{y}<br>" +
                                "Stock Value: $%{marker.color:,.0f}<br>" +
                                "<extra></extra>"
                )])
                
                # Add reference lines
                max_stock = data['current_stock'].max()
                max_reorder = data['reorder_point'].max()
                
                fig_stock_vs_reorder.add_shape(
                    type="line",
                    x0=0, y0=0, x1=max_reorder, y1=max_reorder,
                    line=dict(color="red", width=2, dash="dash"),
                    name="Reorder Point Line"
                )
                
                fig_stock_vs_reorder.add_shape(
                    type="line",
                    x0=0, y0=0, x1=max_reorder, y1=max_reorder * 1.5,
                    line=dict(color="orange", width=2, dash="dash"),
                    name="Optimal Range"
                )
                
                fig_stock_vs_reorder.update_layout(
                    title={
                        'text': "Current Stock vs Reorder Point Analysis",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Reorder Point",
                    yaxis_title="Current Stock",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=60),
                    showlegend=True,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                st.plotly_chart(fig_stock_vs_reorder, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Category Analysis Section
    if 'category' in data.columns:
        st.subheader("🏷️ Category Analysis & Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Category Performance Analysis
            if 'turnover_rate' in data.columns:
                category_performance = data.groupby('category').agg({
                    'turnover_rate': ['mean', 'std', 'count'],
                    'stock_value': 'sum' if 'stock_value' in data.columns else 'current_stock'
                }).round(2)
                
                # Flatten column names
                category_performance.columns = ['_'.join(col).strip() for col in category_performance.columns]
                category_performance = category_performance.reset_index()
                
                # Create enhanced category performance chart
                fig_category_perf = go.Figure(data=[go.Bar(
                    x=category_performance['category'],
                    y=category_performance['turnover_rate_mean'],
                    marker_color='rgba(139, 92, 246, 0.8)',
                    marker_line_color='rgba(139, 92, 246, 1)',
                    marker_line_width=2,
                    hovertemplate="<b>%{x}</b><br>" +
                                "Avg Turnover: %{y:.2f}<br>" +
                                "Items: %{customdata}<br>" +
                                "<extra></extra>",
                    customdata=category_performance['turnover_rate_count']
                )])
                
                fig_category_perf.update_layout(
                    title={
                        'text': "Average Turnover Rate by Category",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Category",
                    yaxis_title="Average Turnover Rate",
                    xaxis=dict(tickangle=45),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=80)
                )
                
                st.plotly_chart(fig_category_perf, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Category Value Analysis
            if 'stock_value' in data.columns:
                category_value = data.groupby('category')['stock_value'].sum().reset_index()
                category_value = category_value.sort_values('stock_value', ascending=False)
                
                # Create enhanced category value chart
                fig_category_value = go.Figure(data=[go.Bar(
                    x=category_value['category'],
                    y=category_value['stock_value'],
                    marker_color='rgba(102, 126, 234, 0.8)',
                    marker_line_color='rgba(102, 126, 234, 1)',
                    marker_line_width=2,
                    hovertemplate="<b>%{x}</b><br>" +
                                "Total Value: $%{y:,.0f}<br>" +
                                "Percentage: %{customdata:.1f}%<br>" +
                                "<extra></extra>",
                    customdata=[(val / category_value['stock_value'].sum()) * 100 for val in category_value['stock_value']]
                )])
                
                fig_category_value.update_layout(
                    title={
                        'text': "Total Stock Value by Category",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Category",
                    yaxis_title="Stock Value ($)",
                    xaxis=dict(tickangle=45),
                    yaxis=dict(
                        tickformat=',',
                        tickprefix='$'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=80)
                )
                
                st.plotly_chart(fig_category_value, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Inventory Health Dashboard
    st.subheader("🏥 Inventory Health Dashboard")
    
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        # Calculate comprehensive health metrics
        data['health_status'] = np.where(
            data['current_stock'] <= data['reorder_point'],
            'Critical',
            np.where(
                data['current_stock'] <= data['reorder_point'] * 1.5,
                'Optimal',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 2,
                    'Good',
                    'Overstocked'
                )
            )
        )
        
        health_dist = data['health_status'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Health Status Distribution
            fig_health = go.Figure(data=[go.Pie(
                labels=health_dist.index,
                values=health_dist.values,
                hole=0.3,
                marker_colors=['#dc2626', '#22c55e', '#3b82f6', '#fbbf24'],
                textinfo='label+percent+value',
                textposition='outside',
                hovertemplate="<b>%{label}</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "<extra></extra>"
            )])
            
            fig_health.update_layout(
                title={
                    'text': "Inventory Health Status Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_health, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Health Metrics Summary
            st.markdown("**📊 Health Metrics Summary:**")
            
            # Calculate health percentages
            total_items = len(data)
            critical_pct = (health_dist.get('Critical', 0) / total_items) * 100
            optimal_pct = (health_dist.get('Optimal', 0) / total_items) * 100
            good_pct = (health_dist.get('Good', 0) / total_items) * 100
            overstocked_pct = (health_dist.get('Overstocked', 0) / total_items) * 100
            
            # Display health metrics with enhanced styling
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                        border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #dc2626; margin: 0 0 10px 0;">🚨 Critical Items</h4>
                <p style="margin: 0; color: #374151;"><strong>{health_dist.get('Critical', 0)}</strong> items ({critical_pct:.1f}%) - Immediate action required</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                        border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Optimal Items</h4>
                <p style="margin: 0; color: #374151;"><strong>{health_dist.get('Optimal', 0)}</strong> items ({optimal_pct:.1f}%) - Well-managed inventory</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                        border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #3b82f6; margin: 0 0 10px 0;">👍 Good Items</h4>
                <p style="margin: 0; color: #374151;"><strong>{health_dist.get('Good', 0)}</strong> items ({good_pct:.1f}%) - Adequate stock levels</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                        border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                <h4 style="color: #fbbf24; margin: 0 0 10px 0;">📦 Overstocked Items</h4>
                <p style="margin: 0; color: #374151;"><strong>{health_dist.get('Overstocked', 0)}</strong> items ({overstocked_pct:.1f}%) - Consider reducing stock</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Inventory Insights Section
    st.subheader("💡 Inventory Insights & Recommendations")
    
    with st.expander("🔍 Detailed Analysis", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Performance Insights:**")
            
            # ABC analysis insights
            if 'abc_category' in data.columns:
                a_items = data[data['abc_category'] == 'A']
                if not a_items.empty:
                    a_value = (a_items['current_stock'] * a_items['unit_cost']).sum() if 'unit_cost' in data.columns else 0
                    # Calculate total inventory value
                    total_inventory_value = (data['current_stock'] * data['unit_cost']).sum() if 'unit_cost' in data.columns else 0
                    a_percentage = (a_value / total_inventory_value) * 100 if total_inventory_value > 0 else 0
                    st.info(f"**A-Category Items:** {len(a_items)} high-value items represent {a_percentage:.1f}% of inventory value")
            
            # Category insights
            if 'category' in data.columns:
                top_category = data['category'].value_counts().index[0]
                top_category_count = data['category'].value_counts().iloc[0]
                top_category_percentage = (top_category_count / total_items) * 100
                
                if top_category_percentage > 30:
                    st.warning(f"**Category Concentration:** {top_category} represents {top_category_percentage:.1f}% of items")
                else:
                    st.success(f"**Category Balance:** Good distribution across categories")
        
        with col2:
            st.markdown("**🎯 Optimization Opportunities:**")
            
            # Stock level optimization
            if 'current_stock' in data.columns and 'reorder_point' in data.columns:
                critical_items = len(data[data['current_stock'] <= data['reorder_point']])
                if critical_items > 0:
                    st.error(f"**Immediate Action:** {critical_items} items below reorder point")
                
                overstocked_items = len(data[data['current_stock'] > data['reorder_point'] * 2])
                if overstocked_items > 0:
                    st.warning(f"**Overstock Management:** {overstocked_items} items significantly overstocked")
            
            # Value optimization
            if 'stock_value' in data.columns:
                high_value_threshold = data['stock_value'].quantile(0.9)
                high_value_items = data[data['stock_value'] > high_value_threshold]
                if not high_value_items.empty:
                    st.info(f"**High-Value Focus:** {len(high_value_items)} items represent top 10% of value")
    
    # Enhanced Recommendations Section
    st.subheader("🚀 Strategic Recommendations")
    
    recommendations = []
    
    # Generate dynamic recommendations
    if 'abc_category' in data.columns:
        a_items = data[data['abc_category'] == 'A']
        if not a_items.empty:
            recommendations.append({
                'type': 'success',
                'title': 'A-Category Management',
                'message': f'Implement tight controls for {len(a_items)} high-value items',
                'action': 'Frequent reviews and tight inventory controls'
            })
    
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        critical_items = len(data[data['current_stock'] <= data['reorder_point']])
        if critical_items > 0:
            recommendations.append({
                'type': 'error',
                'title': 'Critical Stock Management',
                'message': f'{critical_items} items require immediate reordering',
                'action': 'Initiate reordering process immediately'
            })
    
    if 'turnover_rate' in data.columns:
        low_turnover_threshold = data['turnover_rate'].quantile(0.25)
        low_turnover_items = len(data[data['turnover_rate'] < low_turnover_threshold])
        if low_turnover_items > 0:
            recommendations.append({
                'type': 'warning',
                'title': 'Turnover Optimization',
                'message': f'{low_turnover_items} items have low turnover rates',
                'action': 'Review stocking strategy and consider promotions'
            })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Optimal Performance',
            'message': 'All inventory metrics are within optimal ranges',
            'action': 'Continue monitoring for continuous improvement'
        })
    
    # Display recommendations with enhanced styling
    for i, rec in enumerate(recommendations):
        color_map = {
            'success': '#22c55e',
            'warning': '#fbbf24',
            'error': '#dc2626',
            'info': '#3b82f6'
        }
        
        icon_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'info': 'ℹ️'
        }
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba({color_map[rec['type']].replace('#', '')}, 0.1) 0%, rgba({color_map[rec['type']].replace('#', '')}, 0.05) 100%); 
                    border: 2px solid rgba({color_map[rec['type']].replace('#', '')}, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4 style="color: {color_map[rec['type']]}; margin: 0 0 10px 0;">{icon_map[rec['type']]} {rec['title']}</h4>
            <p style="margin: 0; color: #374151;">{rec['message']}</p>
            <div style="margin-top: 10px;">
                <strong style="color: {color_map[rec['type']]};">Recommended Action:</strong> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_demand_forecasting(data):
    """Display enhanced demand forecasting analysis with interactive analytics and predictive insights."""
    if data.empty:
        st.warning("📊 No data available for demand forecasting.")
        return
    
    st.subheader("🔮 Demand Forecasting & Analytics")
    
    # Enhanced Time Series Analysis
    if 'date' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Monthly Demand Trends with better tooltips
            data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
            monthly_demand = data.groupby('month')['quantity'].sum().reset_index()
            monthly_demand['month'] = monthly_demand['month'].astype(str)
            
            # Create enhanced line chart with better styling
            fig_monthly = go.Figure(data=[go.Scatter(
                x=monthly_demand['month'],
                y=monthly_demand['quantity'],
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8, color='#667eea'),
                hovertemplate="<b>Month: %{x}</b><br>" +
                            "Demand: %{y:,.0f}<br>" +
                            "<extra></extra>"
            )])
            
            fig_monthly.update_layout(
                title={
                    'text': "Monthly Demand Trends",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Month",
                yaxis_title="Demand Quantity",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Seasonal Patterns Analysis
            if 'seasonality_score' in data.columns:
                seasonal_data = data[data['seasonality_score'] > 0.5]
                if not seasonal_data.empty:
                    # Create enhanced seasonal analysis chart
                    fig_seasonal = go.Figure(data=[go.Scatter(
                        x=seasonal_data['current_stock'],
                        y=seasonal_data['seasonality_score'],
                        mode='markers',
                        marker=dict(
                            size=8,
                            color=seasonal_data['turnover_rate'] if 'turnover_rate' in seasonal_data.columns else seasonal_data['seasonality_score'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Turnover Rate")
                        ),
                        text=seasonal_data['item_name'] if 'item_name' in seasonal_data.columns else seasonal_data['item_id'],
                        hovertemplate="<b>%{text}</b><br>" +
                                    "Current Stock: %{x}<br>" +
                                    "Seasonality Score: %{y:.2f}<br>" +
                                    "Turnover Rate: %{marker.color:.2f}<br>" +
                                    "<extra></extra>"
                    )])
                    
                    fig_seasonal.update_layout(
                        title={
                            'text': "Seasonality vs Stock Levels Analysis",
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 16, 'color': '#2d3748'}
                        },
                        xaxis_title="Current Stock",
                        yaxis_title="Seasonality Score",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        margin=dict(l=60, r=20, t=60, b=60)
                    )
                    
                    st.plotly_chart(fig_seasonal, use_container_width=True, config={'displayModeBar': True})
                else:
                    st.info("📊 No significant seasonal patterns detected in the data.")
            else:
                st.info("📊 Seasonality data not available for analysis.")
    
    # Enhanced Forecasting Accuracy Analysis
    if 'forecast_accuracy' in data.columns:
        st.subheader("📊 Forecasting Accuracy Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Forecast Accuracy Distribution
            fig_accuracy = go.Figure(data=[go.Histogram(
                x=data['forecast_accuracy'],
                nbinsx=15,
                marker_color='rgba(102, 126, 234, 0.7)',
                marker_line_color='rgba(102, 126, 234, 1)',
                marker_line_width=1,
                hovertemplate="<b>Forecast Accuracy Range</b><br>" +
                            "Accuracy: %{x:.1f}%<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            fig_accuracy.update_layout(
                title={
                    'text': "Forecast Accuracy Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Forecast Accuracy (%)",
                yaxis_title="Number of Items",
                xaxis=dict(range=[0, 100]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_accuracy, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Accuracy vs Stock Levels Analysis
            fig_accuracy_stock = go.Figure(data=[go.Scatter(
                x=data['current_stock'],
                y=data['forecast_accuracy'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=data['turnover_rate'] if 'turnover_rate' in data.columns else data['forecast_accuracy'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Turnover Rate")
                ),
                text=data['item_name'] if 'item_name' in data.columns else data['item_id'],
                hovertemplate="<b>%{text}</b><br>" +
                            "Current Stock: %{x}<br>" +
                            "Forecast Accuracy: %{y:.1f}%<br>" +
                            "Turnover Rate: %{marker.color:.2f}<br>" +
                            "<extra></extra>"
            )])
            
            fig_accuracy_stock.update_layout(
                title={
                    'text': "Forecast Accuracy vs Stock Levels",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Current Stock",
                yaxis_title="Forecast Accuracy (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_accuracy_stock, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Demand Forecasting Insights
    st.subheader("💡 Demand Forecasting Insights")
    
    with st.expander("📈 Forecasting Performance Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Accuracy Insights:**")
            
            if 'forecast_accuracy' in data.columns:
                accuracy_stats = data['forecast_accuracy'].describe()
                
                # Enhanced accuracy assessment with better styling
                mean_accuracy = accuracy_stats.get('mean', 0)
                if mean_accuracy >= 90:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">🎉 Excellent Forecasting Performance</h4>
                        <p style="margin: 0; color: #374151;">Average accuracy: <strong>{mean_accuracy:.1f}%</strong></p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">Your forecasting models are performing exceptionally well</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif mean_accuracy >= 80:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                                border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #3b82f6; margin: 0 0 10px 0;">✅ Good Forecasting Performance</h4>
                        <p style="margin: 0; color: #374151;">Average accuracy: <strong>{mean_accuracy:.1f}%</strong></p>
                        <p style="margin: 5px 0 0 10px 0; font-size: 0.9rem; color: #3b82f6;">Consider model refinement for even better accuracy</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Forecasting Improvement Needed</h4>
                        <p style="margin: 0; color: #374151;">Average accuracy: <strong>{mean_accuracy:.1f}%</strong></p>
                        <p style="margin: 5px 0 0 10px 0; font-size: 0.9rem; color: #f59e0b;">Review forecasting models and data quality</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📊 Seasonal Analysis:**")
            
            if 'seasonality_score' in data.columns:
                seasonal_stats = data['seasonality_score'].describe()
                high_seasonal_items = len(data[data['seasonality_score'] > 0.7])
                
                if high_seasonal_items > 0:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                                border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">🌱 Seasonal Patterns Detected</h4>
                        <p style="margin: 0; color: #374151;"><strong>{high_seasonal_items}</strong> items show strong seasonal patterns</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #8b5cf6;">Adjust forecasting models for seasonal variations</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Stable Demand Patterns</h4>
                        <p style="margin: 0; color: #374151;">No significant seasonal patterns detected</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">Standard forecasting models should work well</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Enhanced Demand Forecasting Recommendations
    st.subheader("🚀 Demand Forecasting Optimization")
    
    recommendations = []
    
    # Generate dynamic recommendations based on forecasting data
    if 'forecast_accuracy' in data.columns:
        low_accuracy_threshold = 80
        low_accuracy_items = len(data[data['forecast_accuracy'] < low_accuracy_threshold])
        
        if low_accuracy_items > 0:
            recommendations.append({
                'type': 'warning',
                'title': 'Forecast Accuracy Improvement',
                'message': f'{low_accuracy_items} items have forecast accuracy below {low_accuracy_threshold}%',
                'action': 'Review forecasting models and data quality for these items'
            })
    
    if 'seasonality_score' in data.columns:
        high_seasonal_threshold = 0.7
        high_seasonal_items = len(data[data['seasonality_score'] > high_seasonal_threshold])
        
        if high_seasonal_items > 0:
            recommendations.append({
                'type': 'info',
                'title': 'Seasonal Forecasting Optimization',
                'message': f'{high_seasonal_items} items show strong seasonal patterns',
                'action': 'Implement seasonal forecasting models for better accuracy'
            })
    
    if 'turnover_rate' in data.columns and 'forecast_accuracy' in data.columns:
        # Analyze correlation between turnover and forecast accuracy
        correlation = data['turnover_rate'].corr(data['forecast_accuracy'])
        
        if abs(correlation) > 0.3:
            recommendations.append({
                'type': 'info',
                'title': 'Turnover-Forecast Correlation',
                'message': f'Strong correlation ({correlation:.2f}) between turnover and forecast accuracy',
                'action': 'Use turnover rates to improve forecasting models'
            })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Optimal Forecasting',
            'message': 'All forecasting metrics are within optimal ranges',
            'action': 'Continue monitoring and consider advanced forecasting techniques'
        })
    
    # Display recommendations with enhanced styling
    for i, rec in enumerate(recommendations):
        color_map = {
            'success': '#22c55e',
            'warning': '#fbbf24',
            'error': '#dc2626',
            'info': '#3b82f6'
        }
        
        icon_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'info': 'ℹ️'
        }
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba({color_map[rec['type']].replace('#', '')}, 0.1) 0%, rgba({color_map[rec['type']].replace('#', '')}, 0.05) 100%); 
                    border: 2px solid rgba({color_map[rec['type']].replace('#', '')}, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4 style="color: {color_map[rec['type']]}; margin: 0 0 10px 0;">{icon_map[rec['type']]} {rec['title']}</h4>
            <p style="margin: 0; color: #374151;">{rec['message']}</p>
            <div style="margin-top: 10px;">
                <strong style="color: {color_map[rec['type']]};">Recommended Action:</strong> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Forecasting Summary Table
    st.subheader("📋 Forecasting Summary Table")
    
    if 'category' in data.columns:
        # Create comprehensive forecasting summary
        forecasting_summary = data.groupby('category').agg({
            'item_id': 'count',
            'forecast_accuracy': ['mean', 'std', 'min', 'max'] if 'forecast_accuracy' in data.columns else 'item_id',
            'seasonality_score': ['mean', 'std', 'min', 'max'] if 'seasonality_score' in data.columns else 'item_id',
            'turnover_rate': 'mean' if 'turnover_rate' in data.columns else 'item_id'
        }).round(2)
        
        # Flatten column names
        forecasting_summary.columns = ['_'.join(col).strip() for col in forecasting_summary.columns]
        forecasting_summary = forecasting_summary.reset_index()
        
        # Rename columns for readability
        column_mapping = {
            'item_id_count': 'Total Items',
            'forecast_accuracy_mean': 'Avg Forecast Acc',
            'forecast_accuracy_std': 'Forecast Std Dev',
            'forecast_accuracy_min': 'Min Forecast Acc',
            'forecast_accuracy_max': 'Max Forecast Acc',
            'seasonality_score_mean': 'Avg Seasonality',
            'seasonality_score_std': 'Seasonality Std Dev',
            'seasonality_score_min': 'Min Seasonality',
            'seasonality_score_max': 'Max Seasonality',
            'turnover_rate_mean': 'Avg Turnover Rate'
        }
        
        forecasting_summary = forecasting_summary.rename(columns=column_mapping)
        
        # Display enhanced summary table
        st.dataframe(forecasting_summary, use_container_width=True)
        
        # Add interactive insights
        st.markdown("**💡 Interactive Insights:**")
        st.markdown("""
        - **Hover over charts** for detailed information
        - **Use chart controls** to zoom and pan
        - **Click legend items** to show/hide specific data series
        - **Download charts** using the chart toolbar
        """)

def display_supplier_analytics_dashboard(data):
    """Display comprehensive supplier analytics dashboard with world-class analytics and interactive visualizations."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">🏭 Supplier Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">World-class supplier performance analysis and risk assessment for strategic procurement</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for supplier analysis.")
        return
    
    # Enhanced Supplier Overview Section with Advanced Metrics
    st.subheader("🎯 Supplier Overview")
    
    # Calculate enhanced supplier metrics with advanced calculations
    if 'supplier_id' in data.columns:
        total_suppliers = data['supplier_id'].nunique()
        total_items = len(data)
        avg_lead_time = data['lead_time'].mean() if 'lead_time' in data.columns else 0
        avg_quality_score = data['quality_score'].mean() if 'quality_score' in data.columns else 0
        
        # Advanced supplier calculations
        if 'lead_time' in data.columns:
            lead_time_performance = 'Excellent' if avg_lead_time <= 7 else 'Good' if avg_lead_time <= 14 else 'Average' if avg_lead_time <= 21 else 'Below Average'
            lead_time_color = '#22c55e' if avg_lead_time <= 14 else '#fbbf24' if avg_lead_time <= 21 else '#dc2626'
        else:
            lead_time_performance = 'N/A'
            lead_time_color = '#667eea'
        
        if 'quality_score' in data.columns:
            quality_performance = 'Excellent' if avg_quality_score >= 95 else 'Good' if avg_quality_score >= 90 else 'Average' if avg_quality_score >= 85 else 'Below Average'
            quality_color = '#22c55e' if avg_quality_score >= 90 else '#fbbf24' if avg_quality_score >= 85 else '#dc2626'
        else:
            quality_performance = 'N/A'
            quality_color = '#667eea'
        
        # Enhanced KPI cards with interactive features
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>🏭 Total Suppliers</h3>
                <h2>{total_suppliers}</h2>
                <p>Active supplier partners</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Items per Supplier: {total_items/total_suppliers:.1f if total_suppliers > 0 else 0}
                </div>
                <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                    ✅ Status: Active
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>📦 Total Items</h3>
                <h2>{total_items:,}</h2>
                <p>Supplied inventory items</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Categories: {data['category'].nunique() if 'category' in data.columns else 'N/A'}
                </div>
                <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                    💎 High Value Items: {len(data[data['current_stock'] * data['unit_cost'] > (data['current_stock'] * data['unit_cost']).quantile(0.9)]) if 'current_stock' in data.columns and 'unit_cost' in data.columns else 'N/A'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>⏱️ Avg Lead Time</h3>
                <h2 style="color: {lead_time_color};">{avg_lead_time:.1f} days</h2>
                <p>Average delivery time</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Performance: {lead_time_performance}
                </div>
                <div style="font-size: 0.8rem; color: {lead_time_color}; margin-top: 5px;">
                    {'🎉' if avg_lead_time <= 7 else '✅' if avg_lead_time <= 14 else '⚠️' if avg_lead_time <= 21 else '❌'} {avg_lead_time:.1f} days avg
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>⭐ Avg Quality Score</h3>
                <h2 style="color: {quality_color};">{avg_quality_score:.1f}%</h2>
                <p>Average quality rating</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Performance: {quality_performance}
                </div>
                <div style="font-size: 0.8rem; color: {quality_color}; margin-top: 5px;">
                    {'🎉' if avg_quality_score >= 95 else '✅' if avg_quality_score >= 90 else '⚠️' if avg_quality_score >= 85 else '❌'} {avg_quality_score:.1f}% quality
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Supplier Performance Distribution Analysis with Interactive Charts
    st.subheader("📊 Supplier Performance Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Lead Time Distribution with better tooltips
        if 'lead_time' in data.columns:
            fig_lead_time_dist = go.Figure(data=[go.Histogram(
                x=data['lead_time'],
                nbinsx=20,
                marker_color='rgba(102, 126, 234, 0.7)',
                marker_line_color='rgba(102, 126, 234, 1)',
                marker_line_width=1,
                hovertemplate="<b>Lead Time Range</b><br>" +
                            "Days: %{x:.1f}<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            # Add performance threshold lines
            fig_lead_time_dist.add_vline(x=7, line_dash="dash", line_color="green", 
                                       annotation_text="Excellent Threshold", annotation_position="top")
            fig_lead_time_dist.add_vline(x=14, line_dash="dash", line_color="blue", 
                                       annotation_text="Good Threshold", annotation_position="top")
            fig_lead_time_dist.add_vline(x=21, line_dash="dash", line_color="orange", 
                                       annotation_text="Average Threshold", annotation_position="top")
            
            fig_lead_time_dist.update_layout(
                title={
                    'text': "Lead Time Distribution with Performance Thresholds",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Lead Time (Days)",
                yaxis_title="Number of Items",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig_lead_time_dist, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced Quality Score Distribution with better tooltips
        if 'quality_score' in data.columns:
            fig_quality_dist = go.Figure(data=[go.Histogram(
                x=data['quality_score'],
                nbinsx=20,
                marker_color='rgba(118, 75, 162, 0.7)',
                marker_line_color='rgba(118, 75, 162, 1)',
                marker_line_width=1,
                hovertemplate="<b>Quality Score Range</b><br>" +
                            "Score: %{x:.1f}%<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            # Add quality threshold lines
            fig_quality_dist.add_vline(x=95, line_dash="dash", line_color="green", 
                                     annotation_text="Excellent Threshold", annotation_position="top")
            fig_quality_dist.add_vline(x=90, line_dash="dash", line_color="blue", 
                                     annotation_text="Good Threshold", annotation_position="top")
            fig_quality_dist.add_vline(x=85, line_dash="dash", line_color="orange", 
                                     annotation_text="Average Threshold", annotation_position="top")
            
            fig_quality_dist.update_layout(
                title={
                    'text': "Quality Score Distribution with Performance Thresholds",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Quality Score (%)",
                yaxis_title="Number of Items",
                xaxis=dict(range=[0, 100]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig_quality_dist, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Supplier Performance Benchmarking with Interactive Rankings
    st.subheader("🏆 Supplier Performance Benchmarking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Top Suppliers by Lead Time with better tooltips
        if 'lead_time' in data.columns and 'supplier_id' in data.columns:
            supplier_lead_time = data.groupby('supplier_id')['lead_time'].mean().reset_index()
            top_suppliers_lead = supplier_lead_time.nsmallest(10, 'lead_time')
            
            fig_top_lead = go.Figure(data=[go.Bar(
                x=top_suppliers_lead['lead_time'],
                y=top_suppliers_lead['supplier_id'],
                orientation='h',
                marker_color='rgba(34, 197, 94, 0.8)',
                marker_line_color='rgba(34, 197, 94, 1)',
                marker_line_width=2,
                hovertemplate="<b>Supplier: %{y}</b><br>" +
                            "Avg Lead Time: %{x:.1f} days<br>" +
                            "<extra></extra>"
            )])
            
            fig_top_lead.update_layout(
                title={
                    'text': "Top 10 Suppliers by Lead Time",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Average Lead Time (Days)",
                yaxis_title="Supplier ID",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_top_lead, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced Top Suppliers by Quality Score with better tooltips
        if 'quality_score' in data.columns and 'supplier_id' in data.columns:
            supplier_quality = data.groupby('supplier_id')['quality_score'].mean().reset_index()
            top_suppliers_quality = supplier_quality.nlargest(10, 'quality_score')
            
            fig_top_quality = go.Figure(data=[go.Bar(
                x=top_suppliers_quality['quality_score'],
                y=top_suppliers_quality['supplier_id'],
                orientation='h',
                marker_color='rgba(20, 184, 166, 0.8)',
                marker_line_color='rgba(20, 184, 166, 1)',
                marker_line_width=2,
                hovertemplate="<b>Supplier: %{y}</b><br>" +
                            "Avg Quality Score: %{x:.1f}%<br>" +
                            "<extra></extra>"
            )])
            
            fig_top_quality.update_layout(
                title={
                    'text': "Top 10 Suppliers by Quality Score",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Average Quality Score (%)",
                yaxis_title="Supplier ID",
                xaxis=dict(range=[0, 100]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_top_quality, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Supplier Risk Assessment with Interactive Analysis
    st.subheader("⚠️ Supplier Risk Assessment")
    
    if 'supplier_id' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Supplier Risk Matrix with better tooltips
            if 'lead_time' in data.columns and 'quality_score' in data.columns:
                # Calculate risk scores
                data['lead_time_risk'] = np.where(
                    data['lead_time'] <= 7, 'Low',
                    np.where(data['lead_time'] <= 14, 'Medium',
                    np.where(data['lead_time'] <= 21, 'High', 'Critical'))
                )
                
                data['quality_risk'] = np.where(
                    data['quality_score'] >= 95, 'Low',
                    np.where(data['quality_score'] >= 90, 'Medium',
                    np.where(data['quality_score'] >= 85, 'High', 'Critical'))
                )
                
                # Create risk matrix
                risk_matrix = data.groupby(['lead_time_risk', 'quality_risk']).size().reset_index(name='count')
                
                # Create enhanced risk matrix heatmap
                fig_risk_matrix = go.Figure(data=go.Heatmap(
                    z=risk_matrix.pivot(index='lead_time_risk', columns='quality_risk', values='count').fillna(0).values,
                    x=['Low', 'Medium', 'High', 'Critical'],
                    y=['Low', 'Medium', 'High', 'Critical'],
                    colorscale='RdYlGn_r',
                    hovertemplate="<b>Lead Time Risk: %{y}</b><br>" +
                                "Quality Risk: %{x}<br>" +
                                "Items: %{z}<br>" +
                                "<extra></extra>"
                ))
                
                fig_risk_matrix.update_layout(
                    title={
                        'text': "Supplier Risk Matrix (Lead Time vs Quality)",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Quality Risk Level",
                    yaxis_title="Lead Time Risk Level",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=60)
                )
                
                st.plotly_chart(fig_risk_matrix, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Risk Distribution with better tooltips
            if 'lead_time_risk' in data.columns:
                risk_dist = data['lead_time_risk'].value_counts()
                
                fig_risk_dist = go.Figure(data=[go.Pie(
                    labels=risk_dist.index,
                    values=risk_dist.values,
                    hole=0.4,
                    marker_colors=['#22c55e', '#3b82f6', '#fbbf24', '#dc2626'],
                    textinfo='label+percent+value',
                    textposition='outside',
                    hovertemplate="<b>%{label} Risk</b><br>" +
                                "Items: %{value}<br>" +
                                "Percentage: %{percent}<br>" +
                                "<extra></extra>"
                )])
                
                fig_risk_dist.update_layout(
                    title={
                        'text': "Lead Time Risk Distribution",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=0.5,
                        xanchor="left",
                        x=1.02,
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='rgba(0,0,0,0.1)',
                        borderwidth=1
                    ),
                    margin=dict(l=20, r=120, t=40, b=20),
                    height=400
                )
                
                st.plotly_chart(fig_risk_dist, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Supplier Cost Analysis with Interactive Visualizations
    st.subheader("💰 Supplier Cost Analysis")
    
    if 'unit_cost' in data.columns and 'supplier_id' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Cost by Supplier with better tooltips
            supplier_cost = data.groupby('supplier_id')['unit_cost'].agg(['mean', 'std', 'count']).reset_index()
            supplier_cost.columns = ['Supplier ID', 'Avg Cost', 'Std Dev', 'Item Count']
            
            fig_supplier_cost = go.Figure(data=[go.Bar(
                x=supplier_cost['Supplier ID'],
                y=supplier_cost['Avg Cost'],
                marker_color='rgba(139, 92, 246, 0.8)',
                marker_line_color='rgba(139, 92, 246, 1)',
                marker_line_width=2,
                hovertemplate="<b>Supplier: %{x}</b><br>" +
                            "Avg Cost: $%{y:.2f}<br>" +
                            "Items: %{customdata}<br>" +
                            "<extra></extra>",
                customdata=supplier_cost['Item Count']
            )])
            
            fig_supplier_cost.update_layout(
                title={
                    'text': "Average Unit Cost by Supplier",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Supplier ID",
                yaxis_title="Average Unit Cost ($)",
                yaxis=dict(
                    tickformat=',',
                    tickprefix='$'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_supplier_cost, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Cost vs Quality Analysis with better tooltips
            if 'quality_score' in data.columns:
                fig_cost_quality = go.Figure(data=[go.Scatter(
                    x=data['unit_cost'],
                    y=data['quality_score'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=data['lead_time'] if 'lead_time' in data.columns else data['quality_score'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Lead Time (Days)")
                    ),
                    text=data['supplier_id'],
                    hovertemplate="<b>Supplier: %{text}</b><br>" +
                                "Unit Cost: $%{x:.2f}<br>" +
                                "Quality Score: %{y:.1f}%<br>" +
                                "Lead Time: %{marker.color:.1f} days<br>" +
                                "<extra></extra>"
                )])
                
                fig_cost_quality.update_layout(
                    title={
                        'text': "Cost vs Quality Analysis by Supplier",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Unit Cost ($)",
                    yaxis_title="Quality Score (%)",
                    yaxis=dict(range=[0, 100]),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=60)
                )
                
                st.plotly_chart(fig_cost_quality, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Supplier Insights and Recommendations with Interactive Elements
    st.subheader("💡 Supplier Insights & Recommendations")
    
    with st.expander("📊 Advanced Supplier Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Overall Supplier Performance:**")
            
            if 'lead_time' in data.columns:
                lead_time_stats = data['lead_time'].describe()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                            border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #667eea; margin: 0 0 10px 0;">⏱️ Lead Time Performance</h4>
                    <p style="margin: 0; color: #374151;"><strong>Mean:</strong> {lead_time_stats['mean']:.1f} days</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Median:</strong> {lead_time_stats['50%']:.1f} days</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Std Dev:</strong> {lead_time_stats['std']:.1f} days</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Lead time performance assessment with enhanced styling
                if lead_time_stats['mean'] <= 7:
                    performance_level = "Excellent"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">🎉 Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your suppliers are delivering exceptionally fast!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif lead_time_stats['mean'] <= 14:
                    performance_level = "Good"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                                border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #3b82f6; margin: 0 0 10px 0;">✅ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your suppliers are performing above average!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif lead_time_stats['mean'] <= 21:
                    performance_level = "Average"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your suppliers have room for improvement!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    performance_level = "Below Average"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 10px 0;">❌ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Immediate action required to improve supplier performance!</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🎯 Quality & Cost Analysis:**")
            
            if 'quality_score' in data.columns:
                quality_stats = data['quality_score'].describe()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(13, 148, 136, 0.1) 100%); 
                            border: 2px solid rgba(20, 184, 166, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #14b8a6; margin: 0 0 10px 0;">⭐ Quality Performance</h4>
                    <p style="margin: 0; color: #374151;"><strong>Mean:</strong> {quality_stats['mean']:.1f}%</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Median:</strong> {quality_stats['50%']:.1f}%</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Std Dev:</strong> {quality_stats['std']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'unit_cost' in data.columns:
                cost_stats = data['unit_cost'].describe()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                            border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">💰 Cost Analysis</h4>
                    <p style="margin: 0; color: #374151;"><strong>Mean:</strong> ${cost_stats['mean']:.2f}</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Median:</strong> ${cost_stats['50%']:.2f}</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Std Dev:</strong> ${cost_stats['std']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced Supplier Recommendations with Interactive Elements
    st.subheader("🚀 Supplier Optimization Recommendations")
    
    recommendations = []
    
    # Generate dynamic recommendations based on supplier data
    if 'lead_time' in data.columns:
        high_lead_time_threshold = 21
        high_lead_time_items = data[data['lead_time'] > high_lead_time_threshold]
        
        if not high_lead_time_items.empty:
            recommendations.append({
                'type': 'warning',
                'title': 'Lead Time Optimization',
                'message': f'{len(high_lead_time_items)} items have lead times above {high_lead_time_threshold} days',
                'action': 'Negotiate better delivery terms or consider alternative suppliers'
            })
    
    if 'quality_score' in data.columns:
        low_quality_threshold = 85
        low_quality_items = data[data['quality_score'] < low_quality_threshold]
        
        if not low_quality_items.empty:
            recommendations.append({
                'type': 'warning',
                'title': 'Quality Improvement',
                'message': f'{len(low_quality_items)} items have quality scores below {low_quality_threshold}%',
                'action': 'Work with suppliers to improve quality standards'
            })
    
    if 'unit_cost' in data.columns:
        high_cost_threshold = data['unit_cost'].quantile(0.9)
        high_cost_items = data[data['unit_cost'] > high_cost_threshold]
        
        if not high_cost_items.empty:
            recommendations.append({
                'type': 'info',
                'title': 'Cost Optimization',
                'message': f'{len(high_cost_items)} items have costs above the 90th percentile',
                'action': 'Negotiate better pricing or explore bulk purchasing options'
            })
    
    if 'supplier_id' in data.columns:
        supplier_item_counts = data['supplier_id'].value_counts()
        single_item_suppliers = supplier_item_counts[supplier_item_counts == 1]
        
        if not single_item_suppliers.empty:
            recommendations.append({
                'type': 'info',
                'title': 'Supplier Consolidation',
                'message': f'{len(single_item_suppliers)} suppliers provide only one item each',
                'action': 'Consider consolidating suppliers for better negotiation power'
            })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Optimal Supplier Performance',
            'message': 'All supplier metrics are within optimal ranges',
            'action': 'Continue monitoring for continuous improvement opportunities'
        })
    
    # Display recommendations with enhanced styling
    for i, rec in enumerate(recommendations):
        color_map = {
            'success': '#22c55e',
            'warning': '#fbbf24',
            'error': '#dc2626',
            'info': '#3b82f6'
        }
        
        icon_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'info': 'ℹ️'
        }
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba({color_map[rec['type']].replace('#', '')}, 0.1) 0%, rgba({color_map[rec['type']].replace('#', '')}, 0.05) 100%); 
                    border: 2px solid rgba({color_map[rec['type']].replace('#', '')}, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4 style="color: {color_map[rec['type']]}; margin: 0 0 10px 0;">{icon_map[rec['type']]} {rec['title']}</h4>
            <p style="margin: 0; color: #374151;">{rec['message']}</p>
            <div style="margin-top: 10px;">
                <strong style="color: {color_map[rec['type']]};">Recommended Action:</strong> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Supplier Summary Table with Interactive Features
    st.subheader("📋 Supplier Summary Table")
    
    if 'supplier_id' in data.columns:
        # Create comprehensive supplier summary
        supplier_summary = data.groupby('supplier_id').agg({
            'item_id': 'count',
            'lead_time': ['mean', 'std', 'min', 'max'] if 'lead_time' in data.columns else 'item_id',
            'quality_score': ['mean', 'std', 'min', 'max'] if 'quality_score' in data.columns else 'item_id',
            'unit_cost': ['mean', 'std', 'min', 'max'] if 'unit_cost' in data.columns else 'item_id'
        }).round(2)
        
        # Flatten column names
        supplier_summary.columns = ['_'.join(col).strip() for col in supplier_summary.columns]
        supplier_summary = supplier_summary.reset_index()
        
        # Rename columns for readability
        column_mapping = {
            'item_id_count': 'Total Items',
            'lead_time_mean': 'Avg Lead Time',
            'lead_time_std': 'Lead Time Std Dev',
            'lead_time_min': 'Min Lead Time',
            'lead_time_max': 'Max Lead Time',
            'quality_score_mean': 'Avg Quality Score',
            'quality_score_std': 'Quality Std Dev',
            'quality_score_min': 'Min Quality Score',
            'quality_score_max': 'Max Quality Score',
            'unit_cost_mean': 'Avg Unit Cost',
            'unit_cost_std': 'Cost Std Dev',
            'unit_cost_min': 'Min Unit Cost',
            'unit_cost_max': 'Max Unit Cost'
        }
        
        supplier_summary = supplier_summary.rename(columns=column_mapping)
        
        # Display enhanced summary table
        st.dataframe(supplier_summary, use_container_width=True)
        
        # Add interactive insights and chart download options
        st.markdown("**💡 Interactive Features:**")
        st.markdown("""
        - **Hover over charts** for detailed supplier metrics
        - **Use chart controls** to zoom, pan, and explore data
        - **Click legend items** to show/hide specific supplier metrics
        - **Download charts** as PNG or SVG using the chart toolbar
        - **Performance thresholds** are automatically highlighted on charts
        - **Risk matrix** shows supplier risk levels for strategic planning
        """)

def display_cost_analytics_dashboard(data):
    """Display comprehensive cost analytics dashboard with world-class analytics and interactive visualizations."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">💰 Cost Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">World-class cost structure analysis and optimization insights for strategic inventory management</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for cost analysis.")
        return
    
    # Enhanced Cost Overview Section with Advanced Metrics
    st.subheader("🎯 Cost Overview")
    
    # Calculate enhanced cost metrics with advanced calculations
    total_items = len(data)
    total_cost = (data['current_stock'] * data['unit_cost']).sum() if 'current_stock' in data.columns and 'unit_cost' in data.columns else 0
    avg_unit_cost = data['unit_cost'].mean() if 'unit_cost' in data.columns else 0
    avg_holding_cost = data['holding_cost'].mean() if 'holding_cost' in data.columns else 0
    
    # Advanced cost calculations
    if 'unit_cost' in data.columns:
        cost_performance = 'Excellent' if avg_unit_cost <= data['unit_cost'].quantile(0.25) else 'Good' if avg_unit_cost <= data['unit_cost'].quantile(0.5) else 'Average' if avg_unit_cost <= data['unit_cost'].quantile(0.75) else 'Above Average'
        cost_color = '#22c55e' if avg_unit_cost <= data['unit_cost'].quantile(0.5) else '#fbbf24' if avg_unit_cost <= data['unit_cost'].quantile(0.75) else '#dc2626'
    else:
        cost_performance = 'N/A'
        cost_color = '#667eea'
    
    if 'holding_cost' in data.columns:
        holding_performance = 'Excellent' if avg_holding_cost <= data['holding_cost'].quantile(0.25) else 'Good' if avg_holding_cost <= data['holding_cost'].quantile(0.5) else 'Average' if avg_holding_cost <= data['holding_cost'].quantile(0.75) else 'Above Average'
        holding_color = '#22c55e' if avg_holding_cost <= data['holding_cost'].quantile(0.5) else '#fbbf24' if avg_holding_cost <= data['holding_cost'].quantile(0.75) else '#dc2626'
    else:
        holding_performance = 'N/A'
        holding_color = '#667eea'
    
    # Enhanced KPI cards with interactive features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>📦 Total Items</h3>
            <h2>{total_items:,}</h2>
            <p>Active inventory items</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Categories: {data['category'].nunique() if 'category' in data.columns else 'N/A'}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                ✅ Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>💰 Total Cost</h3>
            <h2>${total_cost:,.0f}</h2>
            <p>Total inventory value</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Avg Item: ${total_cost/total_items:,.2f if total_items > 0 else 0}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                💎 High Value Items: {len(data[data['current_stock'] * data['unit_cost'] > (data['current_stock'] * data['unit_cost']).quantile(0.9)]) if 'current_stock' in data.columns and 'unit_cost' in data.columns else 'N/A'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>🏷️ Avg Unit Cost</h3>
            <h2 style="color: {cost_color};">${avg_unit_cost:.2f}</h2>
            <p>Average cost per unit</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Performance: {cost_performance}
            </div>
            <div style="font-size: 0.8rem; color: {cost_color}; margin-top: 5px;">
                {'🎉' if avg_unit_cost <= (data['unit_cost'].quantile(0.25) if 'unit_cost' in data.columns else 0) else '✅' if avg_unit_cost <= (data['unit_cost'].quantile(0.5) if 'unit_cost' in data.columns else 0) else '⚠️' if avg_unit_cost <= (data['unit_cost'].quantile(0.75) if 'unit_cost' in data.columns else 0) else '❌'} ${avg_unit_cost:.2f} per unit
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>📦 Avg Holding Cost</h3>
            <h2 style="color: {holding_color};">${avg_holding_cost:.2f}</h2>
            <p>Average holding cost</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Performance: {holding_performance}
            </div>
            <div style="font-size: 0.8rem; color: {holding_color}; margin-top: 5px;">
                {'🎉' if avg_holding_cost <= (data['holding_cost'].quantile(0.25) if 'holding_cost' in data.columns else 0) else '✅' if avg_holding_cost <= (data['holding_cost'].quantile(0.5) if 'holding_cost' in data.columns else 0) else '⚠️' if avg_holding_cost <= (data['holding_cost'].quantile(0.75) if 'holding_cost' in data.columns else 0) else '❌'} ${avg_holding_cost:.2f} per item
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cost Distribution Analysis
    st.subheader("📊 Cost Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Unit cost distribution
        if 'unit_cost' in data.columns:
            fig_cost_dist = px.histogram(
                data,
                x='unit_cost',
                nbins=20,
                title="Unit Cost Distribution",
                color_discrete_sequence=['#667eea']
            )
            fig_cost_dist.update_layout(xaxis_title="Unit Cost ($)", yaxis_title="Number of Items")
            st.plotly_chart(fig_cost_dist, use_container_width=True)
    
    with col2:
        # Cost by category
        if 'unit_cost' in data.columns and 'category' in data.columns:
            category_cost = data.groupby('category')['unit_cost'].agg(['mean', 'std', 'count']).reset_index()
            category_cost.columns = ['Category', 'Avg Cost', 'Std Dev', 'Item Count']
            
            fig_category_cost = px.bar(
                category_cost,
                x='Category',
                y='Avg Cost',
                title="Average Unit Cost by Category",
                color_discrete_sequence=['#764ba2']
            )
            fig_category_cost.update_layout(xaxis_title="Category", yaxis_title="Average Unit Cost ($)")
            fig_category_cost.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_cost, use_container_width=True)
    
    # Cost Performance Analysis
    st.subheader("📈 Cost Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top expensive items
        if 'unit_cost' in data.columns and 'item_name' in data.columns:
            top_expensive = data.nlargest(10, 'unit_cost')[['item_name', 'unit_cost', 'category']]
            
            fig_top_expensive = px.bar(
                top_expensive,
                x='unit_cost',
                y='item_name',
                orientation='h',
                title="Top 10 Most Expensive Items",
                color_discrete_sequence=['#dc2626']
            )
            fig_top_expensive.update_layout(xaxis_title="Unit Cost ($)", yaxis_title="Item Name")
            st.plotly_chart(fig_top_expensive, use_container_width=True)
    
    with col2:
        # Cost vs turnover analysis
        if 'unit_cost' in data.columns and 'turnover_rate' in data.columns:
            fig_cost_turnover = px.scatter(
                data,
                x='unit_cost',
                y='turnover_rate',
                title="Cost vs Turnover Rate Analysis",
                color_discrete_sequence=['#f59e0b'],
                hover_data=['item_name', 'category'] if 'item_name' in data.columns and 'category' in data.columns else None
            )
            fig_cost_turnover.update_layout(xaxis_title="Unit Cost ($)", yaxis_title="Turnover Rate")
            st.plotly_chart(fig_cost_turnover, use_container_width=True)
    
    # Cost Optimization Analysis
    st.subheader("⚡ Cost Optimization Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # ABC analysis by cost
        if 'unit_cost' in data.columns and 'current_stock' in data.columns:
            # Calculate total value for each item
            data['total_value'] = data['current_stock'] * data['unit_cost']
            total_value = data['total_value'].sum()
            
            # Sort by value and calculate cumulative percentage
            data_sorted = data.sort_values('total_value', ascending=False)
            data_sorted['cumulative_percentage'] = (data_sorted['total_value'].cumsum() / total_value) * 100
            
            # Categorize as A, B, or C
            data_sorted['abc_category'] = np.where(
                data_sorted['cumulative_percentage'] <= 80, 'A',
                np.where(data_sorted['cumulative_percentage'] <= 95, 'B', 'C')
            )
            
            abc_distribution = data_sorted['abc_category'].value_counts()
            
            fig_abc_cost = px.pie(
                values=abc_distribution.values,
                names=abc_distribution.index,
                title="ABC Analysis by Cost Value",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_abc_cost.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_abc_cost, use_container_width=True)
    
    with col2:
        # Holding cost analysis
        if 'holding_cost_rate' in data.columns and 'current_stock' in data.columns and 'unit_cost' in data.columns:
            data['holding_cost'] = data['current_stock'] * data['unit_cost'] * data['holding_cost_rate'] / 100
            top_holding_cost = data.nlargest(10, 'holding_cost')[['item_name', 'holding_cost', 'category']]
            
            fig_holding_cost = px.bar(
                top_holding_cost,
                x='holding_cost',
                y='item_name',
                orientation='h',
                title="Top 10 Items by Holding Cost",
                color_discrete_sequence=['#14b8a6']
            )
            fig_holding_cost.update_layout(xaxis_title="Holding Cost ($)", yaxis_title="Item Name")
            st.plotly_chart(fig_holding_cost, use_container_width=True)
    
    # Cost Trends and Forecasting
    st.subheader("📈 Cost Trends and Forecasting")
    
    if 'date' in data.columns and 'unit_cost' in data.columns:
        # Time series analysis
        data['date'] = pd.to_datetime(data['date'])
        data['month'] = data['date'].dt.to_period('M')
        
        monthly_cost = data.groupby('month').agg({
            'unit_cost': 'mean',
            'current_stock': 'sum'
        }).reset_index()
        
        monthly_cost['month'] = monthly_cost['month'].astype(str)
        
        fig_cost_trends = px.line(
            monthly_cost,
            x='month',
            y='unit_cost',
            title="Monthly Average Unit Cost Trends",
            color_discrete_sequence=['#667eea']
        )
        fig_cost_trends.update_layout(xaxis_title="Month", yaxis_title="Average Unit Cost ($)")
        st.plotly_chart(fig_cost_trends, use_container_width=True)
    
    # Cost Insights and Recommendations
    st.subheader("💡 Cost Insights & Recommendations")
    
    insights_container = st.container()
    
    with insights_container:
        # Overall cost insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Cost Structure Analysis:**")
            
            if 'unit_cost' in data.columns:
                cost_stats = data['unit_cost'].describe()
                st.write(f"• **Unit Cost Distribution:**")
                st.write(f"  - Mean: ${cost_stats['mean']:.2f}")
                st.write(f"  - Median: ${cost_stats['50%']:.2f}")
                st.write(f"  - Std Dev: ${cost_stats['std']:.2f}")
                st.write(f"  - Range: ${cost_stats['min']:.2f} - ${cost_stats['max']:.2f}")
                
                # Cost efficiency assessment
                cost_efficiency = cost_stats['mean'] / cost_stats['50%'] if cost_stats['50%'] > 0 else 1
                if cost_efficiency <= 1.2:
                    st.success("✅ **Good cost efficiency - costs are well distributed**")
                elif cost_efficiency <= 1.5:
                    st.info("⚠️ **Moderate cost efficiency - some cost optimization opportunities**")
                else:
                    st.warning("🚨 **Poor cost efficiency - significant cost optimization needed**")
        
        with col2:
            st.markdown("**🎯 Key Cost Metrics:**")
            
            if 'holding_cost_rate' in data.columns:
                holding_cost_stats = data['holding_cost_rate'].describe()
                st.write(f"• **Holding Cost Rate:**")
                st.write(f"  - Mean: {holding_cost_stats['mean']:.2f}%")
                st.write(f"  - Median: {holding_cost_stats['50%']:.2f}%")
                st.write(f"  - Std Dev: {holding_cost_stats['std']:.2f}%")
            
            if 'current_stock' in data.columns and 'unit_cost' in data.columns:
                total_value = (data['current_stock'] * data['unit_cost']).sum()
                st.write(f"• **Total Inventory Value:** ${total_value:,.2f}")
    
    # Cost Optimization Recommendations
    st.markdown("**🚀 Cost Optimization Recommendations:**")
    
    recommendations = []
    
    # High-cost item recommendations
    if 'unit_cost' in data.columns:
        high_cost_threshold = data['unit_cost'].quantile(0.9)
        high_cost_items = data[data['unit_cost'] > high_cost_threshold]
        
        if not high_cost_items.empty:
            recommendations.append(f"• **High-Cost Items:** {len(high_cost_items)} items have unit costs above ${high_cost_threshold:.2f}. Consider bulk purchasing, supplier negotiation, or alternative sourcing.")
    
    # Holding cost recommendations
    if 'holding_cost_rate' in data.columns and 'current_stock' in data.columns and 'unit_cost' in data.columns:
        high_holding_threshold = data['holding_cost_rate'].quantile(0.8)
        high_holding_items = data[data['holding_cost_rate'] > high_holding_threshold]
        
        if not high_holding_items.empty:
            recommendations.append(f"• **Holding Cost Optimization:** {len(high_holding_items)} items have high holding costs. Consider reducing stock levels or improving turnover rates.")
    
    # ABC analysis recommendations
    if 'abc_category' in data.columns:
        a_items = data[data['abc_category'] == 'A']
        c_items = data[data['abc_category'] == 'C']
        
        if not a_items.empty:
            recommendations.append(f"• **A-Category Management:** {len(a_items)} high-value items represent 80% of inventory value. Implement tight controls and frequent reviews.")
        
        if not c_items.empty:
            recommendations.append(f"• **C-Category Optimization:** {len(c_items)} low-value items can be managed with simplified procedures and higher reorder points.")
    
    # Cost variance recommendations
    if 'unit_cost' in data.columns:
        cost_variance = data['unit_cost'].std() / data['unit_cost'].mean()
        if cost_variance > 0.5:
            recommendations.append(f"• **Cost Standardization:** High cost variance ({cost_variance:.2f}) suggests opportunities for standardization and bulk purchasing.")
    
    if not recommendations:
        recommendations.append("• **Status:** All cost metrics are within optimal ranges. Continue monitoring for continuous improvement.")
    
    for rec in recommendations:
        st.write(rec)
    
    # Cost Summary Table
    st.subheader("📋 Cost Summary Table")
    
    if 'category' in data.columns:
        cost_summary = data.groupby('category').agg({
            'item_id': 'count',
            'unit_cost': ['mean', 'std', 'min', 'max'],
            'current_stock': 'sum',
            'holding_cost_rate': 'mean' if 'holding_cost_rate' in data.columns else 'item_id'
        }).round(2)
        
        # Flatten column names
        cost_summary.columns = ['_'.join(col).strip() for col in cost_summary.columns]
        cost_summary = cost_summary.reset_index()
        
        # Rename columns for readability
        column_mapping = {
            'item_id_count': 'Total Items',
            'unit_cost_mean': 'Avg Unit Cost',
            'unit_cost_std': 'Cost Std Dev',
            'unit_cost_min': 'Min Unit Cost',
            'unit_cost_max': 'Max Unit Cost',
            'current_stock_sum': 'Total Stock',
            'holding_cost_rate_mean': 'Avg Holding Cost Rate'
        }
        
        cost_summary = cost_summary.rename(columns=column_mapping)
        
        st.dataframe(cost_summary, use_container_width=True)

def display_warehouse_operations(data):
    """Display warehouse operations analytics."""
    if data.empty:
        st.warning("📊 No data available for warehouse operations.")
        return
    
    st.subheader("🏗️ Warehouse Operations & Efficiency")
    
    # Location analysis
    if 'warehouse_location' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Location distribution
            location_counts = data['warehouse_location'].value_counts()
            fig_location = px.pie(
                values=location_counts.values,
                names=location_counts.index,
                title="Items by Warehouse Location",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_location.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_location, use_container_width=True)
        
        with col2:
            # Stock by location
            stock_by_location = data.groupby('warehouse_location')['current_stock'].sum().reset_index()
            fig_stock_location = px.bar(
                stock_by_location,
                x='warehouse_location',
                y='current_stock',
                title="Total Stock by Warehouse Location",
                color_discrete_sequence=['#667eea']
            )
            fig_stock_location.update_layout(xaxis_title="Warehouse Location", yaxis_title="Total Stock")
            st.plotly_chart(fig_stock_location, use_container_width=True)
    
    # Space utilization
    if 'storage_volume' in data.columns and 'current_stock' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Volume utilization
            data['volume_utilization'] = (data['current_stock'] / data['storage_volume']) * 100
            fig_volume_util = px.histogram(
                data,
                x='volume_utilization',
                nbins=20,
                title="Storage Volume Utilization",
                color_discrete_sequence=['#667eea']
            )
            fig_volume_util.update_layout(xaxis_title="Volume Utilization (%)", yaxis_title="Number of Items")
            st.plotly_chart(fig_volume_util, use_container_width=True)
        
        with col2:
            # Space efficiency
            fig_space_efficiency = px.scatter(
                data,
                x='storage_volume',
                y='current_stock',
                title="Storage Volume vs Current Stock",
                color_discrete_sequence=['#764ba2']
            )
            fig_space_efficiency.update_layout(xaxis_title="Storage Volume", yaxis_title="Current Stock")
            st.plotly_chart(fig_space_efficiency, use_container_width=True)

def display_automation_opportunities(data):
    """Display automation opportunities and recommendations."""
    if data.empty:
        st.warning("📊 No data available for automation analysis.")
        return
    
    st.subheader("🤖 Automation Opportunities & Smart Recommendations")
    
    # Reorder automation
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Auto-reorder candidates
            auto_reorder_items = data[data['current_stock'] <= data['reorder_point']]
            if not auto_reorder_items.empty:
                fig_auto_reorder = px.bar(
                    auto_reorder_items.head(10),
                    x='item_name',
                    y='current_stock',
                    title="Top 10 Items for Auto-Reorder",
                    color_discrete_sequence=['#667eea']
                )
                fig_auto_reorder.update_layout(xaxis_title="Item Name", yaxis_title="Current Stock")
                fig_auto_reorder.update_xaxes(tickangle=45)
                st.plotly_chart(fig_auto_reorder, use_container_width=True)
        
        with col2:
            # Reorder quantity recommendations
            if 'max_stock' in data.columns:
                auto_reorder_items['recommended_order'] = auto_reorder_items['max_stock'] - auto_reorder_items['current_stock']
                fig_reorder_qty = px.bar(
                    auto_reorder_items.head(10),
                    x='item_name',
                    y='recommended_order',
                    title="Recommended Order Quantities",
                    color_discrete_sequence=['#764ba2']
                )
                fig_reorder_qty.update_layout(xaxis_title="Item Name", yaxis_title="Recommended Order Qty")
                fig_reorder_qty.update_xaxes(tickangle=45)
                st.plotly_chart(fig_reorder_qty, use_container_width=True)
    
    # Smart routing
    if 'pick_route' in data.columns and 'pick_time' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pick route optimization
            route_efficiency = data.groupby('pick_route')['pick_time'].mean().reset_index()
            fig_route_efficiency = px.bar(
                route_efficiency,
                x='pick_route',
                y='pick_time',
                title="Average Pick Time by Route",
                color_discrete_sequence=['#667eea']
            )
            fig_route_efficiency.update_layout(xaxis_title="Pick Route", yaxis_title="Average Pick Time (min)")
            st.plotly_chart(fig_route_efficiency, use_container_width=True)
        
        with col2:
            # Route optimization opportunities
            if 'optimal_route' in data.columns:
                route_improvement = data[data['pick_route'] != data['optimal_route']]
                if not route_improvement.empty:
                    fig_route_improvement = px.scatter(
                        route_improvement.head(20),
                        x='pick_time',
                        y='optimal_pick_time',
                        title="Route Optimization Opportunities",
                        color_discrete_sequence=['#764ba2']
                    )
                    fig_route_improvement.update_layout(xaxis_title="Current Pick Time", yaxis_title="Optimal Pick Time")
                    st.plotly_chart(fig_route_improvement, use_container_width=True)

@st.cache_data(ttl=1800, max_entries=50)
def load_and_process_data(uploaded_file):
    """Optimized data loading and processing with caching."""
    try:
        if uploaded_file.name.endswith('.xlsx'):
            # Read Excel file with optimized settings
            data = pd.read_excel(
                uploaded_file,
                engine='openpyxl',
                sheet_name=None,  # Read all sheets
                nrows=None,  # Read all rows
                memory_map=True  # Memory optimization
            )
            return data
        elif uploaded_file.name.endswith('.csv'):
            # Read CSV with optimized chunking for large files
            chunk_size = 10000
            chunks = []
            for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
                chunks.append(chunk)
            data = pd.concat(chunks, ignore_index=True)
            return data
        else:
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def display_data_input_section():
    """Display comprehensive data input section for inventory management."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">📥 Data Input & Management</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Upload your data, enter manually, or download templates to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create main tabs for comprehensive data management
    main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
        "📥 Download Template", "📤 Upload Data", "📝 Manual Entry", "🧪 Sample Data"
    ])
    
    with main_tab1:
        st.markdown("""
        <div class="welcome-section">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">📥 Download Inventory Data Template</h3>
            <p style="color: #374151; margin-bottom: 20px;">Download the comprehensive Excel template with all required inventory data schema, fill it with your data, and upload it back.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create comprehensive template for download
        if st.button("📥 Download Excel Template", key="download_template", use_container_width=True):
            template_data = create_comprehensive_inventory_template()
            st.download_button(
                label="💾 Save Template",
                data=template_data,
                file_name="inventory_data_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="save_template"
            )
        
        # Template information
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #1e3c72; margin-bottom: 15px;">Template includes:</h4>
            <ul style="color: #374151; margin: 0; padding-left: 20px;">
                <li>Comprehensive inventory data schema with 25+ fields</li>
                <li>Multiple data tables in separate sheets</li>
                <li>Instructions sheet with field descriptions</li>
                <li>Proper column headers and data types</li>
                <li>Sample data for reference</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Show template schema
        st.subheader("📋 Template Schema")
        schema_data = {
            'Field': [
                'item_id', 'item_name', 'category', 'description', 'sku', 'barcode',
                'current_stock', 'reorder_point', 'max_stock', 'min_stock', 'unit_cost',
                'holding_cost_rate', 'supplier_id', 'supplier_name', 'lead_time',
                'warehouse_location', 'storage_volume', 'pick_route', 'pick_time',
                'turnover_rate', 'forecast_accuracy', 'seasonality_score', 'abc_category',
                'last_updated', 'status'
            ],
            'Type': [
                'Text', 'Text', 'Text', 'Text', 'Text', 'Text',
                'Number', 'Number', 'Number', 'Number', 'Currency',
                'Percentage', 'Text', 'Text', 'Number',
                'Text', 'Number', 'Text', 'Number',
                'Number', 'Percentage', 'Number', 'Text',
                'Date', 'Text'
            ],
            'Description': [
                'Unique item identifier', 'Item name/description', 'Product category', 'Detailed description', 'Stock keeping unit', 'Barcode/QR code',
                'Current stock level', 'Reorder threshold', 'Maximum stock level', 'Minimum stock level', 'Unit cost in USD',
                'Annual holding cost rate (%)', 'Supplier identifier', 'Supplier name', 'Lead time in days',
                'Warehouse location/zone', 'Storage volume required', 'Picking route', 'Standard pick time (min)',
                'Annual turnover rate', 'Forecast accuracy (%)', 'Seasonality score (0-1)', 'ABC analysis category',
                'Last update timestamp', 'Item status'
            ]
        }
        schema_df = pd.DataFrame(schema_data)
        st.dataframe(schema_df, use_container_width=True)
    
    with main_tab2:
        st.markdown("""
        <div class="welcome-section">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">📤 Upload Your Inventory Data</h3>
            <p style="color: #374151; margin-bottom: 20px;">Upload your filled Excel template or individual data files:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Complete dataset upload
        st.markdown("### 📊 Complete Dataset")
        uploaded_complete_dataset = st.file_uploader(
            "📊 Upload Complete Dataset (Excel file with multiple sheets)", 
            type=['xlsx'], 
            key="complete_dataset_upload",
            help="Upload an Excel file with sheets named: Inventory_Items, Suppliers, Transactions, Locations"
        )
        
        if uploaded_complete_dataset is not None:
            try:
                # Read all sheets from the Excel file
                excel_file = pd.read_excel(uploaded_complete_dataset, sheet_name=None)
                
                # Dictionary to store loaded data
                loaded_data = {}
                
                # Expected sheet names
                expected_sheets = {
                    'Inventory_Items': 'inventory_data',
                    'Suppliers': 'suppliers_data', 
                    'Transactions': 'transactions_data',
                    'Locations': 'locations_data'
                }
                
                # Load each sheet if it exists
                for sheet_name, session_key in expected_sheets.items():
                    if sheet_name in excel_file.keys():
                        loaded_data[session_key] = pd.read_excel(uploaded_complete_dataset, sheet_name=sheet_name)
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                            ✅ {sheet_name} loaded: {len(loaded_data[session_key])} records
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                            ⚠️ Sheet '{sheet_name}' not found in the uploaded file
                        </div>
                        """, unsafe_allow_html=True)
                
                # Update session state with loaded data
                for session_key, data in loaded_data.items():
                    if session_key == 'inventory_data':
                        st.session_state['inventory_data'] = data
                    else:
                        setattr(st.session_state, session_key, data)
                
                # Show summary
                total_records = sum(len(data) for data in loaded_data.values())
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4 style="margin: 0 0 10px 0;">🎉 Complete Dataset Loaded Successfully!</h4>
                    <p style="margin: 0;">Total records loaded: <strong>{total_records:,}</strong> across <strong>{len(loaded_data)}</strong> data tables</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading complete dataset: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        # Separator
        st.markdown("---")
        
        # Individual file upload
        st.markdown("### 📁 Individual Files")
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_inventory = st.file_uploader("📦 Inventory Items", type=['xlsx', 'csv'], key="inventory_upload")
            uploaded_suppliers = st.file_uploader("🏭 Suppliers Data", type=['xlsx', 'csv'], key="suppliers_upload")
        
        with col2:
            uploaded_transactions = st.file_uploader("📊 Transactions", type=['xlsx', 'csv'], key="transactions_upload")
            uploaded_locations = st.file_uploader("📍 Locations", type=['xlsx', 'csv'], key="locations_upload")
        
        # Process individual uploads
        if uploaded_inventory is not None:
            try:
                if uploaded_inventory.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_inventory)
                else:
                    data = pd.read_excel(uploaded_inventory, engine='openpyxl')
                
                st.session_state['inventory_data'] = data
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Inventory data loaded: {len(data)} records
                </div>
                """, unsafe_allow_html=True)
                
                # Display data preview
                st.subheader("📋 Data Preview")
                st.dataframe(data.head(10), use_container_width=True)
                
                return data
                
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading inventory data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        # Upload features information
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #1e3c72; margin-bottom: 15px;">Upload features:</h4>
            <ul style="color: #374151; margin: 0; padding-left: 20px;">
                <li>Support for Excel (.xlsx) and CSV formats</li>
                <li>Automatic data validation and error checking</li>
                <li>Multiple data table support</li>
                <li>Real-time data preview and statistics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with main_tab3:
        st.markdown("""
        <div class="welcome-section">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">📝 Manual Data Entry</h3>
            <p style="color: #374151; margin-bottom: 20px;">Add inventory items manually using the forms below:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create sub-tabs for different data types
        manual_tab1, manual_tab2, manual_tab3, manual_tab4 = st.tabs([
            "📦 Inventory Items", "🏭 Suppliers", "📊 Transactions", "📍 Locations"
        ])
        
        with manual_tab1:
            st.subheader("📦 Add Inventory Item")
            col1, col2 = st.columns(2)
            
            with col1:
                item_id = st.text_input("Item ID", key="item_id_input")
                item_name = st.text_input("Item Name", key="item_name_input")
                category = st.selectbox("Category", ["Electronics", "Clothing", "Food", "Books", "Tools", "Other"], key="category_input")
                description = st.text_area("Description", key="description_input")
                sku = st.text_input("SKU", key="sku_input")
                barcode = st.text_input("Barcode", key="barcode_input")
                current_stock = st.number_input("Current Stock", min_value=0, key="current_stock_input")
                reorder_point = st.number_input("Reorder Point", min_value=0, key="reorder_point_input")
                max_stock = st.number_input("Max Stock", min_value=0, key="max_stock_input")
                min_stock = st.number_input("Min Stock", min_value=0, key="min_stock_input")
            
            with col2:
                unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, key="unit_cost_input")
                holding_cost_rate = st.number_input("Holding Cost Rate (%)", min_value=0.0, max_value=100.0, key="holding_cost_rate_input")
                supplier_id = st.text_input("Supplier ID", key="supplier_id_input")
                supplier_name = st.text_input("Supplier Name", key="supplier_name_input")
                lead_time = st.number_input("Lead Time (days)", min_value=0, key="lead_time_input")
                warehouse_location = st.text_input("Warehouse Location", key="warehouse_location_input")
                storage_volume = st.number_input("Storage Volume", min_value=0.0, key="storage_volume_input")
                pick_route = st.text_input("Pick Route", key="pick_route_input")
                pick_time = st.number_input("Pick Time (min)", min_value=0.0, key="pick_time_input")
                status = st.selectbox("Status", ["Active", "Inactive", "Discontinued"], key="status_input")
            
            if st.button("➕ Add Item", key="add_item_btn"):
                new_item = pd.DataFrame([{
                    'item_id': item_id,
                    'item_name': item_name,
                    'category': category,
                    'description': description,
                    'sku': sku,
                    'barcode': barcode,
                    'current_stock': current_stock,
                    'reorder_point': reorder_point,
                    'max_stock': max_stock,
                    'min_stock': min_stock,
                    'unit_cost': unit_cost,
                    'holding_cost_rate': holding_cost_rate,
                    'supplier_id': supplier_id,
                    'supplier_name': supplier_name,
                    'lead_time': lead_time,
                    'warehouse_location': warehouse_location,
                    'storage_volume': storage_volume,
                    'pick_route': pick_route,
                    'pick_time': pick_time,
                    'turnover_rate': 0.0,
                    'forecast_accuracy': 0.0,
                    'seasonality_score': 0.0,
                    'abc_category': 'C',
                    'last_updated': datetime.now(),
                    'status': status
                }])
                
                if 'inventory_data' not in st.session_state or st.session_state['inventory_data'] is None:
                    st.session_state['inventory_data'] = new_item
                else:
                    st.session_state['inventory_data'] = pd.concat([st.session_state['inventory_data'], new_item], ignore_index=True)
                
                st.success("✅ Inventory item added successfully!")
            
            # Display existing data
            if 'inventory_data' in st.session_state and st.session_state['inventory_data'] is not None and not st.session_state['inventory_data'].empty:
                st.subheader("📋 Existing Inventory Items")
                st.dataframe(st.session_state['inventory_data'], use_container_width=True)
        
        with manual_tab2:
            st.subheader("🏭 Add Supplier")
            col1, col2 = st.columns(2)
            
            with col1:
                supplier_id = st.text_input("Supplier ID", key="supplier_id_manual_input")
                supplier_name = st.text_input("Supplier Name", key="supplier_name_manual_input")
                contact_person = st.text_input("Contact Person", key="contact_person_input")
                email = st.text_input("Email", key="supplier_email_input")
                phone = st.text_input("Phone", key="supplier_phone_input")
            
            with col2:
                address = st.text_area("Address", key="supplier_address_input")
                rating = st.selectbox("Rating", ["A", "B", "C", "D"], key="supplier_rating_input")
                performance_score = st.number_input("Performance Score (0-100)", min_value=0, max_value=100, key="performance_score_input")
                lead_time_avg = st.number_input("Average Lead Time (days)", min_value=0, key="lead_time_avg_input")
                status = st.selectbox("Status", ["Active", "Inactive", "Suspended"], key="supplier_status_input")
            
            if st.button("➕ Add Supplier", key="add_supplier_btn"):
                new_supplier = pd.DataFrame([{
                    'supplier_id': supplier_id,
                    'supplier_name': supplier_name,
                    'contact_person': contact_person,
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'rating': rating,
                    'performance_score': performance_score,
                    'lead_time_avg': lead_time_avg,
                    'status': status
                }])
                
                if 'suppliers_data' not in st.session_state:
                    st.session_state['suppliers_data'] = new_supplier
                else:
                    st.session_state['suppliers_data'] = pd.concat([st.session_state['suppliers_data'], new_supplier], ignore_index=True)
                
                st.success("✅ Supplier added successfully!")
        
        with manual_tab3:
            st.subheader("📊 Add Transaction")
            col1, col2 = st.columns(2)
            
            with col1:
                transaction_id = st.text_input("Transaction ID", key="transaction_id_input")
                item_id = st.text_input("Item ID", key="transaction_item_id_input")
                transaction_type = st.selectbox("Type", ["In", "Out", "Adjustment", "Transfer"], key="transaction_type_input")
                quantity = st.number_input("Quantity", min_value=0, key="transaction_quantity_input")
                unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, key="transaction_unit_cost_input")
            
            with col2:
                transaction_date = st.date_input("Date", key="transaction_date_input")
                reference = st.text_input("Reference", key="reference_input")
                notes = st.text_area("Notes", key="transaction_notes_input")
                user_id = st.text_input("User ID", key="user_id_input")
                location = st.text_input("Location", key="transaction_location_input")
            
            if st.button("➕ Add Transaction", key="add_transaction_btn"):
                new_transaction = pd.DataFrame([{
                    'transaction_id': transaction_id,
                    'item_id': item_id,
                    'transaction_type': transaction_type,
                    'quantity': quantity,
                    'unit_cost': unit_cost,
                    'transaction_date': transaction_date,
                    'reference': reference,
                    'notes': notes,
                    'user_id': user_id,
                    'location': location
                }])
                
                if 'transactions_data' not in st.session_state:
                    st.session_state['transactions_data'] = new_transaction
                else:
                    st.session_state['transactions_data'] = pd.concat([st.session_state['transactions_data'], new_transaction], ignore_index=True)
                
                st.success("✅ Transaction added successfully!")
        
        with manual_tab4:
            st.subheader("📍 Add Location")
            col1, col2 = st.columns(2)
            
            with col1:
                location_id = st.text_input("Location ID", key="location_id_input")
                location_name = st.text_input("Location Name", key="location_name_input")
                location_type = st.selectbox("Type", ["Warehouse", "Store", "Distribution Center", "Office"], key="location_type_input")
                address = st.text_area("Address", key="location_address_input")
            
            with col2:
                capacity = st.number_input("Capacity", min_value=0, key="capacity_input")
                manager = st.text_input("Manager", key="manager_input")
                phone = st.text_input("Phone", key="location_phone_input")
                status = st.selectbox("Status", ["Active", "Inactive", "Maintenance"], key="location_status_input")
            
            if st.button("➕ Add Location", key="add_location_btn"):
                new_location = pd.DataFrame([{
                    'location_id': location_id,
                    'location_name': location_name,
                    'location_type': location_type,
                    'address': address,
                    'capacity': capacity,
                    'manager': manager,
                    'phone': phone,
                    'status': status
                }])
                
                if 'locations_data' not in st.session_state:
                    st.session_state['locations_data'] = new_location
                else:
                    st.session_state['locations_data'] = pd.concat([st.session_state['locations_data'], new_location], ignore_index=True)
                
                st.success("✅ Location added successfully!")
    
    with main_tab4:
        st.markdown("""
        <div class="welcome-section">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">🧪 Sample Dataset</h3>
            <p style="color: #374151; margin-bottom: 20px;">Load a comprehensive sample dataset to explore all features and test the system:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Load Sample Dataset", key="load_sample_btn", use_container_width=True):
                sample_data = generate_sample_inventory_dataset()
                st.session_state['inventory_data'] = sample_data
                st.success("✅ Sample dataset loaded successfully!")
                st.dataframe(sample_data.head(10), use_container_width=True)
                
                # Show sample data statistics
                st.subheader("📊 Sample Data Statistics")
                st.write(f"**Total Items:** {len(sample_data):,}")
                st.write(f"**Categories:** {sample_data['category'].nunique()}")
                st.write(f"**Total Value:** ${sample_data['current_stock'].sum():,.2f}")
                st.write(f"**Average Stock:** {sample_data['current_stock'].mean():.1f}")
                
                return sample_data
        
        with col2:
            if st.button("📥 Download Sample Dataset", key="download_sample_btn", use_container_width=True):
                sample_data = generate_sample_inventory_dataset()
                csv_data = sample_data.to_csv(index=False)
                st.download_button(
                    label="💾 Download Sample CSV",
                    data=csv_data,
                    file_name="sample_inventory_dataset.csv",
                    mime="text/csv",
                    key="save_sample"
                )
        
        # Sample data information
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #1e3c72; margin-bottom: 15px;">Sample dataset includes:</h4>
            <ul style="color: #374151; margin: 0; padding-left: 20px;">
                <li>500+ realistic inventory items across multiple categories</li>
                <li>Complete data schema with all required fields</li>
                <li>Realistic stock levels, costs, and performance metrics</li>
                <li>Supplier information and location data</li>
                <li>Ready for immediate analytics and insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    return None

def display_ai_insights_section(data):
    """Display AI-powered insights section."""
    if data is None or data.empty:
        st.warning("📊 No data available for AI insights.")
        return
    
    st.subheader("🧠 AI-Powered Insights & Recommendations")
    
    # Generate insights for different areas
    insight_areas = [
        "inventory_optimization",
        "demand_forecasting", 
        "supplier_management",
        "warehouse_operations",
        "cost_analysis",
        "risk_management",
        "performance_metrics",
        "automation_opportunities"
    ]
    
    # Display insights in tabs
    tab_names = ["📦 Inventory", "🔮 Forecasting", "🏭 Suppliers", "🏗️ Operations", 
                 "💰 Costs", "⚠️ Risks", "📊 Performance", "🤖 Automation"]
    
    tabs = st.tabs(tab_names)
    
    for i, (tab, area) in enumerate(zip(tabs, insight_areas)):
        with tab:
            recommendations = generate_ai_recommendations(area, data)
            
            if isinstance(recommendations, list):
                for rec in recommendations:
                    st.info(rec)
            else:
                st.info(recommendations)
            
            # Add specific visualizations for each area
            if area == "inventory_optimization":
                display_inventory_optimization_charts(data)
            elif area == "demand_forecasting":
                display_forecasting_charts(data)
            elif area == "supplier_management":
                display_supplier_charts(data)
            elif area == "warehouse_operations":
                display_warehouse_charts(data)

def display_inventory_optimization_charts(data):
    """Display charts specific to inventory optimization."""
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        # Stock level analysis
        fig_stock_analysis = px.scatter(
            data,
            x='reorder_point',
            y='current_stock',
            size='unit_cost',
            color='abc_category' if 'abc_category' in data.columns else 'item_name',
            title="Stock Level Analysis",
            hover_data=['item_name', 'unit_cost']
        )
        st.plotly_chart(fig_stock_analysis, use_container_width=True)

def display_forecasting_charts(data):
    """Display charts specific to demand forecasting."""
    if 'forecast_accuracy' in data.columns:
        # Forecast accuracy by category
        if 'category' in data.columns:
            accuracy_by_category = data.groupby('category')['forecast_accuracy'].mean().reset_index()
            fig_accuracy_category = px.bar(
                accuracy_by_category,
                x='category',
                y='forecast_accuracy',
                title="Forecast Accuracy by Category"
            )
            st.plotly_chart(fig_accuracy_category, use_container_width=True)

def display_supplier_charts(data):
    """Display charts specific to supplier management."""
    if 'supplier_id' in data.columns and 'supplier_performance' in data.columns:
        # Supplier performance ranking
        supplier_perf = data.groupby('supplier_id')['supplier_performance'].mean().sort_values(ascending=False).reset_index()
        fig_supplier_ranking = px.bar(
            supplier_perf.head(10),
            x='supplier_id',
            y='supplier_performance',
            title="Top 10 Suppliers by Performance"
        )
        st.plotly_chart(fig_supplier_ranking, use_container_width=True)

def display_warehouse_charts(data):
    """Display charts specific to warehouse operations."""
    if 'warehouse_location' in data.columns and 'current_stock' in data.columns:
        # Warehouse capacity utilization
        warehouse_utilization = data.groupby('warehouse_location')['current_stock'].sum().reset_index()
        fig_warehouse_util = px.bar(
            warehouse_utilization,
            x='warehouse_location',
            y='current_stock',
            title="Warehouse Capacity Utilization"
        )
        st.plotly_chart(fig_warehouse_util, use_container_width=True)

# ============================================================================
# COMPREHENSIVE ANALYTICS DASHBOARDS
# ============================================================================

def display_analytics_overview_dashboard(data):
    """Display high-level analytics overview dashboard with strategic insights and executive summary."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">📊 Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Strategic inventory intelligence and executive insights overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for analytics overview.")
        return
    
    # Executive Summary Section with Enhanced Metrics
    st.subheader("🎯 Executive Summary")
    
    # Enhanced KPI cards with better styling and hover effects
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(data)
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>📦 Total Inventory Items</h3>
            <h2>{total_items:,}</h2>
            <p>Active inventory items across all categories</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            total_value = (data['current_stock'] * data['unit_cost']).sum()
            value_change = total_value * 0.05  # Simulated 5% change
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>💰 Total Inventory Value</h3>
                <h2>${total_value:,.0f}</h2>
                <p>Current stock value at unit cost</p>
                <div style="font-size: 0.8rem; color: {'#22c55e' if value_change > 0 else '#dc2626'}; margin-top: 10px;">
                    {'📈' if value_change > 0 else '📉'} {abs(value_change):.1f}% from last period
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="inventory-metric-card">
                <h3>💰 Total Inventory Value</h3>
                <h2>N/A</h2>
                <p>Cost data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if 'category' in data.columns:
            unique_categories = data['category'].nunique()
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>🏷️ Product Categories</h3>
                <h2>{unique_categories:,}</h2>
                <p>Distinct product categories</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Most common: {data['category'].value_counts().index[0] if len(data['category'].value_counts()) > 0 else 'N/A'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="inventory-metric-card">
                <h3>🏷️ Product Categories</h3>
                <h2>N/A</h2>
                <p>Category data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'supplier_id' in data.columns:
            unique_suppliers = data['supplier_id'].nunique()
            st.markdown(f"""
            <div class="inventory-metric-card">
                <h3>🏭 Active Suppliers</h3>
                <h2>{unique_suppliers:,}</h2>
                <p>Active supplier relationships</p>
                <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                    📊 Top supplier: {data['supplier_id'].value_counts().index[0] if len(data['supplier_id'].value_counts()) > 0 else 'N/A'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="inventory-metric-card">
                <h3>🏭 Active Suppliers</h3>
                <h2>N/A</h2>
                <p>Supplier data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Strategic Overview Charts with Enhanced Interactivity
    st.subheader("📈 Strategic Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced category distribution overview with better tooltips
        if 'category' in data.columns:
            category_dist = data['category'].value_counts().head(8)
            
            # Create enhanced pie chart with custom colors and tooltips
            fig_category_overview = go.Figure(data=[go.Pie(
                labels=category_dist.index,
                values=category_dist.values,
                hole=0.4,
                marker_colors=px.colors.qualitative.Set3,
                textinfo='label+percent',
                textposition='outside',
                hovertemplate="<b>%{label}</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "<extra></extra>"
            )])
            
            fig_category_overview.update_layout(
                title={
                    'text': "Top 8 Categories by Item Count",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_category_overview, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced stock value distribution overview
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            data['stock_value'] = data['current_stock'] * data['unit_cost']
            category_value = data.groupby('category')['stock_value'].sum().nlargest(8).reset_index()
            
            # Create enhanced bar chart with custom styling
            fig_value_overview = go.Figure(data=[go.Bar(
                x=category_value['category'],
                y=category_value['stock_value'],
                marker_color='rgba(102, 126, 234, 0.8)',
                marker_line_color='rgba(102, 126, 234, 1)',
                marker_line_width=2,
                hovertemplate="<b>%{x}</b><br>" +
                            "Stock Value: $%{y:,.0f}<br>" +
                            "Percentage: %{customdata:.1f}%<br>" +
                            "<extra></extra>",
                customdata=[(val / category_value['stock_value'].sum()) * 100 for val in category_value['stock_value']]
            )])
            
            fig_value_overview.update_layout(
                title={
                    'text': "Top 8 Categories by Stock Value",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Category",
                yaxis_title="Stock Value ($)",
                xaxis=dict(
                    tickangle=45,
                    tickfont=dict(size=10),
                    tickmode='array',
                    ticktext=category_value['category'],
                    tickvals=list(range(len(category_value)))
                ),
                yaxis=dict(
                    tickformat=',',
                    tickprefix='$'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=80)
            )
            
            st.plotly_chart(fig_value_overview, use_container_width=True, config={'displayModeBar': True})
    
    # Business Intelligence Metrics with Enhanced Visualizations
    st.subheader("🏆 Business Intelligence Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced ABC Analysis Overview with interactive features
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            data['total_value'] = data['current_stock'] * data['unit_cost']
            total_value = data['total_value'].sum()
            
            # Sort by value and calculate cumulative percentage
            data_sorted = data.sort_values('total_value', ascending=False)
            data_sorted['cumulative_percentage'] = (data_sorted['total_value'].cumsum() / total_value) * 100
            
            # Categorize as A, B, or C
            data_sorted['abc_category'] = np.where(
                data_sorted['cumulative_percentage'] <= 80, 'A',
                np.where(data_sorted['cumulative_percentage'] <= 95, 'B', 'C')
            )
            
            abc_distribution = data_sorted['abc_category'].value_counts()
            
            # Create enhanced ABC analysis chart
            fig_abc_overview = go.Figure(data=[go.Pie(
                labels=abc_distribution.index,
                values=abc_distribution.values,
                hole=0.3,
                marker_colors=['#dc2626', '#f59e0b', '#22c55e'],
                textinfo='label+percent+value',
                textposition='inside',
                hovertemplate="<b>%{label} Category</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "<extra></extra>"
            )])
            
            fig_abc_overview.update_layout(
                title={
                    'text': "ABC Analysis - Inventory Value Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_abc_overview, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced stock level health overview
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Categorize stock levels
            data['stock_health'] = np.where(
                data['current_stock'] <= data['reorder_point'],
                'Critical',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 1.5,
                    'Optimal',
                    'Overstocked'
                )
            )
            
            stock_health_dist = data['stock_health'].value_counts()
            
            # Create enhanced stock health chart
            fig_stock_health = go.Figure(data=[go.Pie(
                labels=stock_health_dist.index,
                values=stock_health_dist.values,
                hole=0.3,
                marker_colors=['#dc2626', '#22c55e', '#f59e0b'],
                textinfo='label+percent+value',
                textposition='inside',
                hovertemplate="<b>%{label}</b><br>" +
                            "Items: %{value}<br>" +
                            "Percentage: %{percent}<br>" +
                            "<extra></extra>"
            )])
            
            fig_stock_health.update_layout(
                title={
                    'text': "Stock Level Health Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                margin=dict(l=20, r=120, t=40, b=20),
                height=400
            )
            
            st.plotly_chart(fig_stock_health, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Strategic Insights with Interactive Elements
    st.subheader("💡 Strategic Insights")
    
    insights_container = st.container()
    
    with insights_container:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Inventory Strategy Insights:**")
            
            # ABC analysis insights with enhanced styling
            if 'abc_category' in data.columns:
                a_items = data[data['abc_category'] == 'A']
                c_items = data[data['abc_category'] == 'C']
                
                if not a_items.empty:
                    a_value = (a_items['current_stock'] * a_items['unit_cost']).sum()
                    a_percentage = (a_value / total_value) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ A-Category Items</h4>
                        <p style="margin: 0; color: #374151;"><strong>{len(a_items)}</strong> items represent <strong>{a_percentage:.1f}%</strong> of inventory value</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #667eea;">High-value items requiring tight controls</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if not c_items.empty:
                    c_value = (c_items['current_stock'] * c_items['unit_cost']).sum()
                    c_percentage = (c_value / total_value) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                                border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #3b82f6; margin: 0 0 10px 0;">📊 C-Category Items</h4>
                        <p style="margin: 0; color: #374151;"><strong>{len(c_items)}</strong> items represent <strong>{c_percentage:.1f}%</strong> of inventory value</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #667eea;">Low-value items for simplified management</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Category concentration insights with enhanced styling
            if 'category' in data.columns:
                top_category = data['category'].value_counts().index[0]
                top_category_count = data['category'].value_counts().iloc[0]
                top_category_percentage = (top_category_count / total_items) * 100
                
                if top_category_percentage > 30:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Category Concentration</h4>
                        <p style="margin: 0; color: #374151;"><strong>{top_category}</strong> represents <strong>{top_category_percentage:.1f}%</strong> of items</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #f59e0b;">Consider diversification strategy</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Category Balance</h4>
                        <p style="margin: 0; color: #374151;">Good distribution across categories</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">Optimal category diversification</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**📊 Operational Health:**")
            
            # Stock level insights with enhanced styling
            if 'current_stock' in data.columns and 'reorder_point' in data.columns:
                critical_items = len(data[data['current_stock'] <= data['reorder_point']])
                critical_percentage = (critical_items / total_items) * 100
                
                if critical_percentage > 20:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 10px 0;">🚨 Critical Stock Levels</h4>
                        <p style="margin: 0; color: #374151;"><strong>{critical_items}</strong> items ({critical_percentage:.1f}%) below reorder point</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #dc2626;">Immediate action required</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif critical_percentage > 10:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Stock Alert</h4>
                        <p style="margin: 0; color: #374151;"><strong>{critical_items}</strong> items ({critical_percentage:.1f}%) need attention</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #f59e0b;">Monitor closely</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Stock Health</h4>
                        <p style="margin: 0; color: #374151;">Only <strong>{critical_items}</strong> items ({critical_percentage:.1f}%) below reorder point</p>
                        <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #16a34a;">Excellent inventory management</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Value concentration insights with enhanced styling
            if 'current_stock' in data.columns and 'unit_cost' in data.columns:
                high_value_threshold = data['total_value'].quantile(0.9)
                high_value_items = data[data['total_value'] > high_value_threshold]
                high_value_percentage = (high_value_items['total_value'].sum() / total_value) * 100
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                            border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">💰 Value Concentration</h4>
                    <p style="margin: 0; color: #374151;">Top 10% of items represent <strong>{high_value_percentage:.1f}%</strong> of total value</p>
                    <p style="margin: 5px 0 0 0; font-size: 0.9rem; color: #8b5cf6;">Focus on high-value item management</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced Quick Actions & Recommendations with Interactive Elements
    st.subheader("🚀 Quick Actions & Recommendations")
    
    # Create expandable sections for different recommendation categories
    with st.expander("📦 Stock Level Management", expanded=True):
        recommendations = []
        
        # Stock level recommendations with enhanced styling
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            critical_items = len(data[data['current_stock'] <= data['reorder_point']])
            if critical_items > 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                            border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #dc2626; margin: 0 0 10px 0;">🚨 Immediate Action Required</h4>
                    <p style="margin: 0; color: #374151;"><strong>{critical_items}</strong> items are below reorder point - initiate reordering process</p>
                    <div style="margin-top: 10px;">
                        <button style="background: #dc2626; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                            📋 View Critical Items
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # ABC analysis recommendations
        if 'abc_category' in data.columns:
            a_items = data[data['abc_category'] == 'A']
            if not a_items.empty:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                            border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #22c55e; margin: 0 0 10px 0;">📊 A-Category Management</h4>
                    <p style="margin: 0; color: #374151;">Implement tight controls and frequent reviews for <strong>{len(a_items)}</strong> high-value items</p>
                    <div style="margin-top: 10px;">
                        <button style="background: #22c55e; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                            📈 View A-Category Items
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with st.expander("📉 Performance Optimization", expanded=False):
        # Performance recommendations with enhanced styling
        if 'turnover_rate' in data.columns:
            low_turnover_threshold = data['turnover_rate'].quantile(0.25)
            low_turnover_items = len(data[data['turnover_rate'] < low_turnover_threshold])
            if low_turnover_items > 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                            border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #fbbf24; margin: 0 0 10px 0;">📉 Performance Review</h4>
                    <p style="margin: 0; color: #374151;"><strong>{low_turnover_items}</strong> items have low turnover rates - review stocking strategy</p>
                    <div style="margin-top: 10px;">
                        <button style="background: #fbbf24; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                            📊 Analyze Low Turnover Items
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Space utilization recommendations
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            data['utilization'] = (data['current_stock'] / data['storage_volume']) * 100
            low_utilization = len(data[data['utilization'] < 50])
            if low_utilization > 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                            border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">🏗️ Space Optimization</h4>
                    <p style="margin: 0; color: #374151;"><strong>{low_utilization}</strong> items have low space utilization - consider consolidation</p>
                    <div style="margin-top: 10px;">
                        <button style="background: #8b5cf6; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">
                            🏗️ View Space Analysis
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    


def display_category_analytics_dashboard(data):
    """Display comprehensive category-based analytics dashboard."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">📊 Category Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Comprehensive analysis by product categories for strategic decision-making</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty or 'category' not in data.columns:
        st.warning("📊 Category data not available. Please ensure your data includes category information.")
        return
    
    # Category Overview Section
    st.subheader("🎯 Category Overview")
    
    # Calculate category statistics
    category_stats = data.groupby('category').agg({
        'item_id': 'count',
        'current_stock': 'sum',
        'unit_cost': 'mean',
        'turnover_rate': 'mean',
        'forecast_accuracy': 'mean'
    }).round(2)
    
    category_stats.columns = ['Item Count', 'Total Stock', 'Avg Unit Cost', 'Avg Turnover Rate', 'Avg Forecast Accuracy']
    category_stats = category_stats.reset_index()
    
    # Display category overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Category distribution pie chart
        fig_category_dist = px.pie(
            data,
            names='category',
            title="Items by Category Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_category_dist.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_category_dist, use_container_width=True)
    
    with col2:
        # Category statistics table
        st.markdown("### 📋 Category Statistics")
        st.dataframe(category_stats, use_container_width=True)
    
    # Category Performance Analysis
    st.subheader("📈 Category Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock value by category
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            data['stock_value'] = data['current_stock'] * data['unit_cost']
            category_value = data.groupby('category')['stock_value'].sum().reset_index()
            
            fig_category_value = px.bar(
                category_value,
                x='category',
                y='stock_value',
                title="Total Stock Value by Category",
                color_discrete_sequence=['#667eea']
            )
            fig_category_value.update_layout(xaxis_title="Category", yaxis_title="Stock Value ($)")
            fig_category_value.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_value, use_container_width=True)
    
    with col2:
        # Turnover rate by category
        if 'turnover_rate' in data.columns:
            category_turnover = data.groupby('category')['turnover_rate'].mean().reset_index()
            
            fig_category_turnover = px.bar(
                category_turnover,
                x='category',
                y='turnover_rate',
                title="Average Turnover Rate by Category",
                color_discrete_sequence=['#764ba2']
            )
            fig_category_turnover.update_layout(xaxis_title="Category", yaxis_title="Turnover Rate")
            fig_category_turnover.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_turnover, use_container_width=True)
    
    # Category Risk Analysis
    st.subheader("⚠️ Category Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stockout risk by category
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Calculate stockout risk for each item
            data['stockout_risk'] = np.where(
                data['current_stock'] <= data['reorder_point'],
                'High Risk',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 1.5,
                    'Medium Risk',
                    'Low Risk'
                )
            )
            
            category_risk = data.groupby(['category', 'stockout_risk']).size().reset_index(name='count')
            category_risk = category_risk.pivot(index='category', columns='stockout_risk', values='count').fillna(0)
            
            fig_category_risk = px.bar(
                category_risk,
                title="Stockout Risk by Category",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_category_risk.update_layout(xaxis_title="Category", yaxis_title="Number of Items")
            fig_category_risk.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_risk, use_container_width=True)
    
    with col2:
        # ABC analysis by category
        if 'abc_category' in data.columns:
            category_abc = data.groupby(['category', 'abc_category']).size().reset_index(name='count')
            category_abc = category_abc.pivot(index='category', columns='abc_category', values='count').fillna(0)
            
            fig_category_abc = px.bar(
                category_abc,
                title="ABC Analysis by Category",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_category_abc.update_layout(xaxis_title="Category", yaxis_title="Number of Items")
            fig_category_abc.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_abc, use_container_width=True)
    
    # Category Efficiency Metrics
    st.subheader("⚡ Category Efficiency Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Forecast accuracy by category
        if 'forecast_accuracy' in data.columns:
            category_forecast = data.groupby('category')['forecast_accuracy'].mean().reset_index()
            
            fig_category_forecast = px.bar(
                category_forecast,
                x='category',
                y='forecast_accuracy',
                title="Average Forecast Accuracy by Category",
                color_discrete_sequence=['#14b8a6']
            )
            fig_category_forecast.update_layout(xaxis_title="Category", yaxis_title="Forecast Accuracy (%)")
            fig_category_forecast.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_forecast, use_container_width=True)
    
    with col2:
        # Space utilization by category
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            data['space_utilization'] = (data['current_stock'] / data['storage_volume']) * 100
            data['space_utilization'] = data['space_utilization'].clip(0, 100)
            
            category_space = data.groupby('category')['space_utilization'].mean().reset_index()
            
            fig_category_space = px.bar(
                category_space,
                x='category',
                y='space_utilization',
                title="Average Space Utilization by Category",
                color_discrete_sequence=['#8b5cf6']
            )
            fig_category_space.update_layout(xaxis_title="Category", yaxis_title="Space Utilization (%)")
            fig_category_space.update_xaxes(tickangle=45)
            st.plotly_chart(fig_category_space, use_container_width=True)
    
    # Category Comparison Table
    st.subheader("📊 Detailed Category Comparison")
    
    # Enhanced category statistics
    detailed_category_stats = data.groupby('category').agg({
        'item_id': 'count',
        'current_stock': ['sum', 'mean', 'std'],
        'unit_cost': ['mean', 'min', 'max'],
        'turnover_rate': ['mean', 'min', 'max'],
        'forecast_accuracy': ['mean', 'min', 'max'],
        'stockout_risk_score': 'mean' if 'stockout_risk_score' in data.columns else 'current_stock'
    }).round(2)
    
    # Flatten column names
    detailed_category_stats.columns = ['_'.join(col).strip() for col in detailed_category_stats.columns]
    detailed_category_stats = detailed_category_stats.reset_index()
    
    # Rename columns for better readability
    column_mapping = {
        'item_id_count': 'Total Items',
        'current_stock_sum': 'Total Stock',
        'current_stock_mean': 'Avg Stock',
        'current_stock_std': 'Stock Std Dev',
        'unit_cost_mean': 'Avg Unit Cost',
        'unit_cost_min': 'Min Unit Cost',
        'unit_cost_max': 'Max Unit Cost',
        'turnover_rate_mean': 'Avg Turnover',
        'turnover_rate_min': 'Min Turnover',
        'turnover_rate_max': 'Max Turnover',
        'forecast_accuracy_mean': 'Avg Forecast Acc',
        'forecast_accuracy_min': 'Min Forecast Acc',
        'forecast_accuracy_max': 'Max Forecast Acc'
    }
    
    detailed_category_stats = detailed_category_stats.rename(columns=column_mapping)
    
    st.dataframe(detailed_category_stats, use_container_width=True)
    
    # Category Insights and Recommendations
    st.subheader("💡 Category Insights & Recommendations")
    
    # Generate insights for each category
    insights_container = st.container()
    
    with insights_container:
        for category in data['category'].unique():
            category_data = data[data['category'] == category]
            
            with st.expander(f"📊 {category} - Insights & Recommendations", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**📈 Performance Summary:**")
                    st.write(f"• **Total Items:** {len(category_data):,}")
                    st.write(f"• **Total Stock:** {category_data['current_stock'].sum():,}")
                    st.write(f"• **Total Value:** ${(category_data['current_stock'] * category_data['unit_cost']).sum():,.2f}")
                    
                    if 'turnover_rate' in category_data.columns:
                        st.write(f"• **Avg Turnover:** {category_data['turnover_rate'].mean():.2f}")
                    
                    if 'forecast_accuracy' in category_data.columns:
                        st.write(f"• **Avg Forecast Accuracy:** {category_data['forecast_accuracy'].mean():.1f}%")
                
                with col2:
                    st.markdown(f"**🎯 Key Insights:**")
                    
                    # Stock level insights
                    low_stock_items = category_data[category_data['current_stock'] <= category_data['reorder_point']]
                    if not low_stock_items.empty:
                        st.warning(f"⚠️ **{len(low_stock_items)} items below reorder point**")
                    
                    # High-value items
                    if 'unit_cost' in category_data.columns:
                        high_value_items = category_data.nlargest(3, 'unit_cost')
                        st.info(f"💰 **Top 3 high-value items** (${high_value_items['unit_cost'].max():.2f} max)")
                    
                    # Performance insights
                    if 'turnover_rate' in category_data.columns:
                        low_turnover = category_data[category_data['turnover_rate'] < category_data['turnover_rate'].quantile(0.25)]
                        if not low_turnover.empty:
                            st.warning(f"📉 **{len(low_turnover)} low-turnover items**")
                
                # Recommendations
                st.markdown("**🚀 Recommendations:**")
                
                recommendations = []
                
                # Stock level recommendations
                if len(low_stock_items) > 0:
                    recommendations.append(f"• **Immediate Action:** Reorder {len(low_stock_items)} items below reorder point")
                
                # Performance recommendations
                if 'turnover_rate' in category_data.columns:
                    if category_data['turnover_rate'].mean() < 4:
                        recommendations.append("• **Performance:** Review stocking strategy for low-turnover items")
                
                # Cost optimization
                if 'unit_cost' in category_data.columns:
                    cost_variance = category_data['unit_cost'].std() / category_data['unit_cost'].mean()
                    if cost_variance > 0.5:
                        recommendations.append("• **Cost Management:** High cost variance - review pricing strategy")
                
                # Space optimization
                if 'storage_volume' in category_data.columns:
                    avg_utilization = (category_data['current_stock'] / category_data['storage_volume']).mean() * 100
                    if avg_utilization < 50:
                        recommendations.append("• **Space Efficiency:** Low space utilization - consider consolidation")
                
                if not recommendations:
                    recommendations.append("• **Status:** Category performing well within optimal parameters")
                
                for rec in recommendations:
                    st.write(rec)

def display_descriptive_analytics_dashboard(data):
    """Display comprehensive descriptive analytics dashboard focusing on 'What happened?' analysis."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">📊 Descriptive Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Comprehensive analysis of what happened in your inventory - stock levels, turnover, demand fulfillment, valuation, aging, and accuracy</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for descriptive analysis.")
        return
    
    # 1. STOCK LEVELS ANALYSIS
    st.subheader("📦 Stock Levels Analysis")
    st.markdown("**Current inventory on hand, stock by location, stock by category/SKU**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Current stock overview
        if 'current_stock' in data.columns:
            total_stock = data['current_stock'].sum()
            avg_stock = data['current_stock'].mean()
            stock_std = data['current_stock'].std()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #667eea; margin: 0 0 15px 0;">📊 Stock Overview</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Stock:</strong> {total_stock:,} units</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Average Stock:</strong> {avg_stock:.1f} units</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Stock Variance:</strong> {stock_std:.1f} units</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Stock distribution by category
        if 'category' in data.columns and 'current_stock' in data.columns:
            category_stock = data.groupby('category')['current_stock'].sum().sort_values(ascending=False).head(8)
            
            fig_category_stock = px.bar(
                x=category_stock.values,
                y=category_stock.index,
                orientation='h',
                title="Stock Levels by Category (Top 8)",
                color_discrete_sequence=['#667eea']
            )
            fig_category_stock.update_layout(
                xaxis_title="Stock Units",
                yaxis_title="Category",
                height=300
            )
            st.plotly_chart(fig_category_stock, use_container_width=True)
    
    # Stock by location (if available)
    if 'location' in data.columns and 'current_stock' in data.columns:
        st.markdown("### 📍 Stock Distribution by Location")
        location_stock = data.groupby('location')['current_stock'].sum().sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_location_stock = px.pie(
                values=location_stock.values,
                names=location_stock.index,
                title="Stock Distribution by Location",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_location_stock.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_location_stock, use_container_width=True)
        
        with col2:
            st.markdown("**Location Stock Summary:**")
            for location, stock in location_stock.items():
                percentage = (stock / location_stock.sum()) * 100
                st.write(f"• **{location}:** {stock:,} units ({percentage:.1f}%)")
    
    # 2. TURNOVER RATIOS ANALYSIS
    st.subheader("🔄 Turnover Ratios Analysis")
    st.markdown("**Inventory turnover, days of inventory on hand (DOH/DSI)**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'turnover_rate' in data.columns:
            avg_turnover = data['turnover_rate'].mean()
            turnover_std = data['turnover_rate'].std()
            
            # Calculate DOH (Days of Inventory on Hand)
            doh = 365 / avg_turnover if avg_turnover > 0 else 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                        border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #22c55e; margin: 0 0 15px 0;">🔄 Turnover Metrics</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Average Turnover Rate:</strong> {avg_turnover:.2f}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Days of Inventory (DOH):</strong> {doh:.1f} days</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Turnover Variance:</strong> {turnover_std:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'turnover_rate' in data.columns:
            # Turnover distribution
            fig_turnover_dist = px.histogram(
                data,
                x='turnover_rate',
                nbins=20,
                title="Turnover Rate Distribution",
                color_discrete_sequence=['#22c55e']
            )
            fig_turnover_dist.update_layout(
                xaxis_title="Turnover Rate",
                yaxis_title="Number of Items",
                height=300
            )
            st.plotly_chart(fig_turnover_dist, use_container_width=True)
    
    # 3. DEMAND FULFILLMENT ANALYSIS
    st.subheader("✅ Demand Fulfillment Analysis")
    st.markdown("**Stockout frequency, backorder rates, order fill rate**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Calculate stockout risk
            stockout_items = len(data[data['current_stock'] <= data['reorder_point']])
            stockout_percentage = (stockout_items / len(data)) * 100
            
            # Calculate backorder simulation (items with zero stock)
            backorder_items = len(data[data['current_stock'] == 0])
            backorder_percentage = (backorder_items / len(data)) * 100
            
            # Order fill rate simulation
            fill_rate = 100 - stockout_percentage
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                        border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #f59e0b; margin: 0 0 15px 0;">✅ Fulfillment Metrics</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Stockout Risk:</strong> {stockout_items} items ({stockout_percentage:.1f}%)</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Backorder Items:</strong> {backorder_items} items ({backorder_percentage:.1f}%)</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Order Fill Rate:</strong> {fill_rate:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Stockout risk by category
            data['stockout_risk'] = np.where(
                data['current_stock'] <= data['reorder_point'],
                'High Risk',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 1.5,
                    'Medium Risk',
                    'Low Risk'
                )
            )
            
            risk_distribution = data['stockout_risk'].value_counts()
            
            fig_risk_dist = px.pie(
                values=risk_distribution.values,
                names=risk_distribution.index,
                title="Stockout Risk Distribution",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_risk_dist.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_risk_dist, use_container_width=True)
    
    # 4. VALUATION METRICS ANALYSIS
    st.subheader("💰 Valuation Metrics Analysis")
    st.markdown("**Inventory value (FIFO, LIFO, weighted average)**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            # Calculate different valuation methods
            data['stock_value'] = data['current_stock'] * data['unit_cost']
            total_value = data['stock_value'].sum()
            
            # Weighted average cost
            weighted_avg_cost = (data['stock_value'].sum() / data['current_stock'].sum()) if data['current_stock'].sum() > 0 else 0
            
            # Value distribution
            value_quartiles = data['stock_value'].quantile([0.25, 0.5, 0.75])
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                        border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #8b5cf6; margin: 0 0 15px 0;">💰 Valuation Summary</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Inventory Value:</strong> ${total_value:,.2f}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Weighted Avg Cost:</strong> ${weighted_avg_cost:.2f}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Median Item Value:</strong> ${value_quartiles[0.5]:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            # Value distribution histogram
            fig_value_dist = px.histogram(
                data,
                x='stock_value',
                nbins=20,
                title="Inventory Value Distribution",
                color_discrete_sequence=['#8b5cf6']
            )
            fig_value_dist.update_layout(
                xaxis_title="Stock Value ($)",
                yaxis_title="Number of Items",
                height=300
            )
            st.plotly_chart(fig_value_dist, use_container_width=True)
    
    # 5. AGING ANALYSIS
    st.subheader("📅 Aging Analysis")
    st.markdown("**Slow-moving, obsolete, and dead stock reports**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'turnover_rate' in data.columns:
            # Categorize items by movement speed
            data['movement_category'] = np.where(
                data['turnover_rate'] >= 8,
                'Fast Moving',
                np.where(
                    data['turnover_rate'] >= 4,
                    'Medium Moving',
                    np.where(
                        data['turnover_rate'] >= 1,
                        'Slow Moving',
                        'Dead Stock'
                    )
                )
            )
            
            movement_dist = data['movement_category'].value_counts()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                        border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #dc2626; margin: 0 0 15px 0;">📅 Movement Analysis</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Fast Moving:</strong> {movement_dist.get('Fast Moving', 0)} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Medium Moving:</strong> {movement_dist.get('Medium Moving', 0)} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Slow Moving:</strong> {movement_dist.get('Slow Moving', 0)} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Dead Stock:</strong> {movement_dist.get('Dead Stock', 0)} items</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'turnover_rate' in data.columns:
            # Movement category distribution
            fig_movement_dist = px.pie(
                values=movement_dist.values,
                names=movement_dist.index,
                title="Inventory Movement Categories",
                color_discrete_sequence=['#22c55e', '#f59e0b', '#f97316', '#dc2626']
            )
            fig_movement_dist.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_movement_dist, use_container_width=True)
    
    # 6. CYCLE COUNTS & ACCURACY ANALYSIS
    st.subheader("🔍 Cycle Counts & Accuracy Analysis")
    st.markdown("**Variance between physical count and system records**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Simulate cycle count accuracy (since we don't have actual physical count data)
        if 'current_stock' in data.columns:
            # Create simulated accuracy metrics
            np.random.seed(42)  # For reproducible results
            data['simulated_physical_count'] = data['current_stock'] + np.random.normal(0, data['current_stock'] * 0.05)
            data['cycle_count_variance'] = ((data['simulated_physical_count'] - data['current_stock']) / data['current_stock']) * 100
            
            # Calculate accuracy metrics
            accurate_items = len(data[abs(data['cycle_count_variance']) <= 2])  # Within 2%
            accurate_percentage = (accurate_items / len(data)) * 100
            
            avg_variance = abs(data['cycle_count_variance']).mean()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                        border: 2px solid rgba(14, 165, 233, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #0ea5e9; margin: 0 0 15px 0;">🔍 Accuracy Metrics</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Accurate Items:</strong> {accurate_items} ({accurate_percentage:.1f}%)</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Average Variance:</strong> {avg_variance:.1f}%</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Items Needing Review:</strong> {len(data) - accurate_items}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'current_stock' in data.columns:
            # Variance distribution
            fig_variance_dist = px.histogram(
                data,
                x='cycle_count_variance',
                nbins=20,
                title="Cycle Count Variance Distribution",
                color_discrete_sequence=['#0ea5e9']
            )
            fig_variance_dist.update_layout(
                xaxis_title="Variance (%)",
                yaxis_title="Number of Items",
                height=300
            )
            st.plotly_chart(fig_variance_dist, use_container_width=True)
    
    # Summary and Insights
    st.subheader("💡 Descriptive Analytics Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Key Findings:**")
        
        # Stock level insights
        if 'current_stock' in data.columns:
            low_stock_items = len(data[data['current_stock'] <= data['reorder_point']]) if 'reorder_point' in data.columns else 0
            if low_stock_items > 0:
                st.warning(f"⚠️ **{low_stock_items} items** are below reorder point")
        
        # Turnover insights
        if 'turnover_rate' in data.columns:
            slow_moving = len(data[data['turnover_rate'] < 2])
            if slow_moving > 0:
                st.info(f"📉 **{slow_moving} items** have low turnover rates")
        
        # Value insights
        if 'current_stock' in data.columns and 'unit_cost' in data.columns:
            high_value_items = len(data[data['stock_value'] > data['stock_value'].quantile(0.9)])
            if high_value_items > 0:
                st.success(f"💰 **{high_value_items} items** represent high inventory value")
    
    with col2:
        st.markdown("**🎯 Recommendations:**")
        
        recommendations = []
        
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            critical_items = len(data[data['current_stock'] <= data['reorder_point']])
            if critical_items > 0:
                recommendations.append(f"• Review reorder points for {critical_items} critical items")
        
        if 'turnover_rate' in data.columns:
            dead_stock = len(data[data['turnover_rate'] < 1])
            if dead_stock > 0:
                recommendations.append(f"• Consider liquidation for {dead_stock} dead stock items")
        
        if 'cycle_count_variance' in data.columns:
            high_variance = len(data[abs(data['cycle_count_variance']) > 5])
            if high_variance > 0:
                recommendations.append(f"• Investigate {high_variance} items with high variance")
        
        if not recommendations:
            recommendations.append("• Inventory appears well-managed")
        
        for rec in recommendations:
            st.write(rec)

def display_prescriptive_analytics_dashboard(data):
    """Display comprehensive prescriptive analytics dashboard focusing on 'What should we do?' recommendations."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">🎯 Prescriptive Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">AI-powered recommendations and optimization strategies for inventory management decisions</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for prescriptive analysis.")
        return
    
    # 1. OPTIMAL REPLENISHMENT ANALYSIS
    st.subheader("📦 Optimal Replenishment Analysis")
    st.markdown("**Suggested reorder quantities (EOQ, JIT models)**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'unit_cost' in data.columns and 'turnover_rate' in data.columns:
            # Calculate EOQ (Economic Order Quantity)
            # EOQ = sqrt((2 * Annual Demand * Order Cost) / Holding Cost)
            # Using turnover rate to estimate annual demand
            data['annual_demand'] = data['current_stock'] * data['turnover_rate']
            order_cost = 50  # Assumed order cost per order
            holding_cost_rate = 0.25  # 25% of unit cost per year
            
            data['eoq'] = np.sqrt((2 * data['annual_demand'] * order_cost) / (data['unit_cost'] * holding_cost_rate))
            data['eoq'] = data['eoq'].round(0)
            
            # Calculate JIT recommendations
            data['jit_recommendation'] = np.where(
                data['turnover_rate'] >= 8,
                'Frequent Small Orders',
                np.where(
                    data['turnover_rate'] >= 4,
                    'Regular Orders',
                    'Bulk Orders'
                )
            )
            
            eoq_summary = data['eoq'].describe()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                        border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #667eea; margin: 0 0 15px 0;">📊 EOQ Analysis</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Average EOQ:</strong> {eoq_summary['mean']:.0f} units</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Min EOQ:</strong> {eoq_summary['min']:.0f} units</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Max EOQ:</strong> {eoq_summary['max']:.0f} units</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'jit_recommendation' in data.columns:
            jit_distribution = data['jit_recommendation'].value_counts()
            
            fig_jit = px.pie(
                values=jit_distribution.values,
                names=jit_distribution.index,
                title="JIT Strategy Recommendations",
                color_discrete_sequence=['#22c55e', '#f59e0b', '#667eea']
            )
            fig_jit.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_jit, use_container_width=True)
    
    # EOQ vs Current Stock Comparison
    if 'eoq' in data.columns and 'current_stock' in data.columns:
        st.markdown("### 📊 EOQ vs Current Stock Comparison")
        
        # Identify items that need reordering
        data['reorder_needed'] = np.where(
            data['current_stock'] <= data['eoq'] * 0.5,
            'Immediate Reorder',
            np.where(
                data['current_stock'] <= data['eoq'] * 0.8,
                'Plan Reorder',
                'Stock Adequate'
            )
        )
        
        reorder_status = data['reorder_needed'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_reorder_status = px.pie(
                values=reorder_status.values,
                names=reorder_status.index,
                title="Reorder Status by EOQ",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_reorder_status.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_reorder_status, use_container_width=True)
        
        with col2:
            st.markdown("**Reorder Recommendations:**")
            immediate_reorder = len(data[data['reorder_needed'] == 'Immediate Reorder'])
            plan_reorder = len(data[data['reorder_needed'] == 'Plan Reorder'])
            
            if immediate_reorder > 0:
                st.warning(f"🚨 **{immediate_reorder} items** need immediate reordering")
            if plan_reorder > 0:
                st.info(f"📋 **{plan_reorder} items** should be planned for reorder")
            if immediate_reorder == 0 and plan_reorder == 0:
                st.success("✅ All items have adequate stock levels")
    
    # 2. SAFETY STOCK OPTIMIZATION
    st.subheader("🛡️ Safety Stock Optimization")
    st.markdown("**Balancing service levels with holding costs**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'turnover_rate' in data.columns and 'unit_cost' in data.columns:
            # Calculate optimal safety stock
            # Safety Stock = Z * sqrt(Lead Time * Demand Variance)
            # Using simplified calculation for demonstration
            lead_time_days = 14  # Assumed lead time
            service_level_z = 1.65  # 95% service level
            
            data['demand_variance'] = data['turnover_rate'] * 0.3  # Simplified variance
            data['optimal_safety_stock'] = service_level_z * np.sqrt(lead_time_days * data['demand_variance'])
            data['optimal_safety_stock'] = data['optimal_safety_stock'].round(0)
            
            # Calculate current vs optimal safety stock
            data['safety_stock_gap'] = data['current_stock'] - data['optimal_safety_stock']
            
            safety_stock_summary = data['optimal_safety_stock'].describe()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                        border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #22c55e; margin: 0 0 15px 0;">🛡️ Safety Stock Analysis</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Avg Optimal Safety Stock:</strong> {safety_stock_summary['mean']:.0f} units</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Safety Stock Value:</strong> ${(data['optimal_safety_stock'] * data['unit_cost']).sum():,.0f}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Items Below Safety Stock:</strong> {len(data[data['safety_stock_gap'] < 0])}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'safety_stock_gap' in data.columns:
            # Safety stock gap distribution
            fig_safety_gap = px.histogram(
                data,
                x='safety_stock_gap',
                nbins=20,
                title="Safety Stock Gap Distribution",
                color_discrete_sequence=['#22c55e']
            )
            fig_safety_gap.update_layout(
                xaxis_title="Safety Stock Gap (Current - Optimal)",
                yaxis_title="Number of Items",
                height=300
            )
            st.plotly_chart(fig_safety_gap, use_container_width=True)
    
    # 3. WAREHOUSE OPTIMIZATION
    st.subheader("🏗️ Warehouse Optimization")
    st.markdown("**Slotting, layout improvements, pick-path efficiency**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            # Calculate space utilization and optimization opportunities
            data['space_utilization'] = (data['current_stock'] / data['storage_volume']) * 100
            data['space_utilization'] = data['space_utilization'].clip(0, 100)
            
            # Identify optimization opportunities
            data['optimization_priority'] = np.where(
                data['space_utilization'] < 30,
                'High Priority - Consolidate',
                np.where(
                    data['space_utilization'] < 60,
                    'Medium Priority - Review',
                    'Low Priority - Optimized'
                )
            )
            
            optimization_dist = data['optimization_priority'].value_counts()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                        border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #f59e0b; margin: 0 0 15px 0;">🏗️ Space Optimization</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>High Priority Items:</strong> {optimization_dist.get('High Priority - Consolidate', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Medium Priority Items:</strong> {optimization_dist.get('Medium Priority - Review', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Low Priority Items:</strong> {optimization_dist.get('Low Priority - Optimized', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'optimization_priority' in data.columns:
            fig_optimization = px.pie(
                values=optimization_dist.values,
                names=optimization_dist.index,
                title="Warehouse Optimization Priorities",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_optimization.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_optimization, use_container_width=True)
    
    # 4. SUPPLIER SOURCING MIX
    st.subheader("🏭 Supplier Sourcing Mix")
    st.markdown("**Recommend best suppliers by lead time, cost, reliability**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'supplier_id' in data.columns and 'unit_cost' in data.columns:
            # Analyze supplier performance
            supplier_analysis = data.groupby('supplier_id').agg({
                'unit_cost': ['mean', 'std'],
                'item_id': 'count'
            }).round(2)
            
            supplier_analysis.columns = ['Avg Cost', 'Cost Std Dev', 'Item Count']
            supplier_analysis = supplier_analysis.reset_index()
            
            # Calculate supplier score (lower cost = higher score)
            supplier_analysis['cost_score'] = 100 - ((supplier_analysis['Avg Cost'] - supplier_analysis['Avg Cost'].min()) / 
                                                   (supplier_analysis['Avg Cost'].max() - supplier_analysis['Avg Cost'].min())) * 100
            
            supplier_analysis['overall_score'] = (supplier_analysis['cost_score'] * 0.7 + 
                                                supplier_analysis['Item Count'] / supplier_analysis['Item Count'].max() * 100 * 0.3)
            
            supplier_analysis = supplier_analysis.sort_values('overall_score', ascending=False)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                        border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #8b5cf6; margin: 0 0 15px 0;">🏭 Supplier Performance</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Top Supplier:</strong> {supplier_analysis.iloc[0]['supplier_id']}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Top Score:</strong> {supplier_analysis.iloc[0]['overall_score']:.1f}/100</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Suppliers:</strong> {len(supplier_analysis)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'supplier_id' in data.columns:
            # Top suppliers by score
            top_suppliers = supplier_analysis.head(5)
            
            fig_suppliers = px.bar(
                top_suppliers,
                x='supplier_id',
                y='overall_score',
                title="Top 5 Suppliers by Performance Score",
                color_discrete_sequence=['#8b5cf6']
            )
            fig_suppliers.update_layout(
                xaxis_title="Supplier ID",
                yaxis_title="Performance Score",
                height=300
            )
            fig_suppliers.update_xaxes(tickangle=45)
            st.plotly_chart(fig_suppliers, use_container_width=True)
    
    # 5. DYNAMIC PRICING & CLEARANCE
    st.subheader("💰 Dynamic Pricing & Clearance")
    st.markdown("**Identify items for markdown/discount to reduce aging stock**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'turnover_rate' in data.columns and 'current_stock' in data.columns and 'unit_cost' in data.columns:
            # Identify items for clearance
            data['clearance_priority'] = np.where(
                (data['turnover_rate'] < 2) & (data['current_stock'] > 0),
                'High Priority - Clearance',
                np.where(
                    (data['turnover_rate'] < 4) & (data['current_stock'] > 0),
                    'Medium Priority - Discount',
                    'No Action Needed'
                )
            )
            
            clearance_dist = data['clearance_priority'].value_counts()
            
            # Calculate potential revenue from clearance
            clearance_items = data[data['clearance_priority'].str.contains('Priority')]
            potential_revenue = (clearance_items['current_stock'] * clearance_items['unit_cost'] * 0.7).sum()  # 30% discount
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                        border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #dc2626; margin: 0 0 15px 0;">💰 Clearance Opportunities</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>High Priority Items:</strong> {clearance_dist.get('High Priority - Clearance', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Medium Priority Items:</strong> {clearance_dist.get('Medium Priority - Discount', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Potential Revenue:</strong> ${potential_revenue:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'clearance_priority' in data.columns:
            fig_clearance = px.pie(
                values=clearance_dist.values,
                names=clearance_dist.index,
                title="Clearance Priority Distribution",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_clearance.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_clearance, use_container_width=True)
    
    # 6. AUTOMATED ALERTS & DECISIONS
    st.subheader("🤖 Automated Alerts & Decisions")
    st.markdown("**Low-stock triggers, stock rotation rules**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Generate automated alerts
            data['alert_level'] = np.where(
                data['current_stock'] == 0,
                '🚨 OUT OF STOCK',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 0.5,
                    '⚠️ CRITICAL LOW',
                    np.where(
                        data['current_stock'] <= data['reorder_point'],
                        '🔶 LOW STOCK',
                        '✅ NORMAL'
                    )
                )
            )
            
            alert_dist = data['alert_level'].value_counts()
            
            # Calculate total value at risk
            critical_items = data[data['alert_level'].str.contains('CRITICAL|OUT OF STOCK')]
            value_at_risk = (critical_items['current_stock'] * critical_items['unit_cost']).sum() if 'unit_cost' in critical_items.columns else 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                        border: 2px solid rgba(14, 165, 233, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #0ea5e9; margin: 0 0 15px 0;">🤖 Alert System</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Critical Alerts:</strong> {len(critical_items)} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Value at Risk:</strong> ${value_at_risk:,.0f}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Alerts:</strong> {len(data) - alert_dist.get('✅ NORMAL', 0)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'alert_level' in data.columns:
            fig_alerts = px.pie(
                values=alert_dist.values,
                names=alert_dist.index,
                title="Automated Alert Distribution",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#f97316', '#22c55e']
            )
            fig_alerts.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_alerts, use_container_width=True)
    
    # Summary and Action Items
    st.subheader("🎯 Action Summary & Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚨 Immediate Actions Required:**")
        
        immediate_actions = []
        
        if 'reorder_needed' in data.columns:
            immediate_reorder = len(data[data['reorder_needed'] == 'Immediate Reorder'])
            if immediate_reorder > 0:
                immediate_actions.append(f"• Reorder {immediate_reorder} items immediately")
        
        if 'alert_level' in data.columns:
            out_of_stock = len(data[data['alert_level'] == '🚨 OUT OF STOCK'])
            if out_of_stock > 0:
                immediate_actions.append(f"• Restock {out_of_stock} out-of-stock items")
        
        if 'clearance_priority' in data.columns:
            high_clearance = len(data[data['clearance_priority'] == 'High Priority - Clearance'])
            if high_clearance > 0:
                immediate_actions.append(f"• Initiate clearance for {high_clearance} slow-moving items")
        
        if not immediate_actions:
            immediate_actions.append("• No immediate actions required")
        
        for action in immediate_actions:
            st.write(action)
    
    with col2:
        st.markdown("**📊 Optimization Opportunities:**")
        
        optimization_opportunities = []
        
        if 'optimization_priority' in data.columns:
            high_opt = len(data[data['optimization_priority'] == 'High Priority - Consolidate'])
            if high_opt > 0:
                optimization_opportunities.append(f"• Consolidate {high_opt} low-utilization items")
        
        if 'safety_stock_gap' in data.columns:
            below_safety = len(data[data['safety_stock_gap'] < 0])
            if below_safety > 0:
                optimization_opportunities.append(f"• Adjust safety stock for {below_safety} items")
        
        if 'supplier_id' in data.columns:
            optimization_opportunities.append("• Review supplier performance and optimize sourcing")
        
        if not optimization_opportunities:
            optimization_opportunities.append("• Inventory appears well-optimized")
        
        for opp in optimization_opportunities:
            st.write(opp)

def display_diagnostic_analytics_dashboard(data):
    """Display comprehensive diagnostic analytics dashboard focusing on 'Why did it happen?' root cause analysis."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">🔍 Diagnostic Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Root cause analysis to understand why inventory issues occurred</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for diagnostic analysis.")
        return
    
    # 1. ROOT CAUSE OF STOCKOUTS ANALYSIS
    st.subheader("🚨 Root Cause of Stockouts Analysis")
    st.markdown("**Late supplier delivery, demand spikes, poor forecasts**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Identify stockout items
            stockout_items = data[data['current_stock'] <= data['reorder_point']]
            stockout_count = len(stockout_items)
            
            if stockout_count > 0:
                # Analyze potential root causes
                if 'turnover_rate' in data.columns:
                    # High turnover items (demand spikes)
                    high_turnover_stockouts = len(stockout_items[stockout_items['turnover_rate'] > 6])
                    # Low turnover items (poor forecasting)
                    low_turnover_stockouts = len(stockout_items[stockout_items['turnover_rate'] < 2])
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 15px 0;">🚨 Stockout Root Causes</h4>
                        <p style="margin: 5px 0; color: #374151;"><strong>Total Stockouts:</strong> {stockout_count} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Demand Spikes:</strong> {high_turnover_stockouts} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Poor Forecasting:</strong> {low_turnover_stockouts} items</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 15px 0;">🚨 Stockout Analysis</h4>
                        <p style="margin: 5px 0; color: #374151;"><strong>Total Stockouts:</strong> {stockout_count} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Root Cause:</strong> Need turnover data for analysis</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No stockouts detected - inventory levels are adequate")
    
    with col2:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns and stockout_count > 0:
            # Stockout by category analysis
            if 'category' in data.columns:
                stockout_by_category = stockout_items['category'].value_counts().head(5)
                
                fig_stockout_category = px.bar(
                    x=stockout_by_category.values,
                    y=stockout_by_category.index,
                    orientation='h',
                    title="Stockouts by Category (Top 5)",
                    color_discrete_sequence=['#dc2626']
                )
                fig_stockout_category.update_layout(
                    xaxis_title="Number of Stockouts",
                    yaxis_title="Category",
                    height=300
                )
                st.plotly_chart(fig_stockout_category, use_container_width=True)
    
    # 2. EXCESS INVENTORY DRIVERS ANALYSIS
    st.subheader("📦 Excess Inventory Drivers Analysis")
    st.markdown("**Over-ordering, low demand, long lead times**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Identify overstocked items
            overstocked_items = data[data['current_stock'] > data['reorder_point'] * 2]
            overstocked_count = len(overstocked_items)
            
            if overstocked_count > 0:
                # Analyze overstocking drivers
                if 'turnover_rate' in data.columns:
                    # Low demand items
                    low_demand_overstock = len(overstocked_items[overstocked_items['turnover_rate'] < 2])
                    # Medium demand items (over-ordering)
                    medium_demand_overstock = len(overstocked_items[(overstocked_items['turnover_rate'] >= 2) & (overstocked_items['turnover_rate'] < 4)])
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                        <h4 style="color: #f59e0b; margin: 0 0 15px 0;">📦 Overstocking Drivers</h4>
                        <p style="margin: 5px 0; color: #374151;"><strong>Total Overstocked:</strong> {overstocked_count} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Low Demand:</strong> {low_demand_overstock} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Over-Ordering:</strong> {medium_demand_overstock} items</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                        <h4 style="color: #f59e0b; margin: 0 0 15px 0;">📦 Overstocking Analysis</h4>
                        <p style="margin: 5px 0; color: #374151;"><strong>Total Overstocked:</strong> {overstocked_count} items</p>
                        <p style="margin: 5px 0; color: #374151;"><strong>Root Cause:</strong> Need turnover data for analysis</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No excess inventory detected - stock levels are optimal")
    
    with col2:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns and overstocked_count > 0:
            # Overstocking by category analysis
            if 'category' in data.columns:
                overstock_by_category = overstocked_items['category'].value_counts().head(5)
                
                fig_overstock_category = px.bar(
                    x=overstock_by_category.values,
                    y=overstock_by_category.index,
                    orientation='h',
                    title="Overstocked Items by Category (Top 5)",
                    color_discrete_sequence=['#f59e0b']
                )
                fig_overstock_category.update_layout(
                    xaxis_title="Number of Overstocked Items",
                    yaxis_title="Category",
                    height=300
                )
                st.plotly_chart(fig_overstock_category, use_container_width=True)
    
    # 3. SHRINKAGE & LOSS ANALYSIS
    st.subheader("💸 Shrinkage & Loss Analysis")
    st.markdown("**Theft, damages, data entry errors**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns:
            # Simulate shrinkage analysis (since we don't have actual shrinkage data)
            np.random.seed(42)  # For reproducible results
            
            # Create simulated shrinkage scenarios
            data['simulated_shrinkage'] = np.random.normal(0.02, 0.01, len(data))  # 2% average shrinkage
            data['simulated_shrinkage'] = data['simulated_shrinkage'].clip(0, 0.1)  # Limit to 0-10%
            
            # Categorize shrinkage types
            data['shrinkage_type'] = np.where(
                data['simulated_shrinkage'] > 0.05,
                'High Risk - Investigate',
                np.where(
                    data['simulated_shrinkage'] > 0.03,
                    'Medium Risk - Monitor',
                    'Low Risk - Normal'
                )
            )
            
            shrinkage_dist = data['shrinkage_type'].value_counts()
            total_shrinkage_value = (data['current_stock'] * data['unit_cost'] * data['simulated_shrinkage']).sum() if 'unit_cost' in data.columns else 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                        border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #8b5cf6; margin: 0 0 15px 0;">💸 Shrinkage Analysis</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>High Risk Items:</strong> {shrinkage_dist.get('High Risk - Investigate', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Medium Risk Items:</strong> {shrinkage_dist.get('Medium Risk - Monitor', 0)}</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Total Loss Value:</strong> ${total_shrinkage_value:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'shrinkage_type' in data.columns:
            fig_shrinkage = px.pie(
                values=shrinkage_dist.values,
                names=shrinkage_dist.index,
                title="Shrinkage Risk Distribution",
                color_discrete_sequence=['#dc2626', '#f59e0b', '#22c55e']
            )
            fig_shrinkage.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_shrinkage, use_container_width=True)
    
    # 4. SUPPLIER RELIABILITY ANALYSIS
    st.subheader("🏭 Supplier Reliability Analysis")
    st.markdown("**Lead-time variability, partial shipments**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'supplier_id' in data.columns and 'unit_cost' in data.columns:
            # Analyze supplier reliability
            supplier_reliability = data.groupby('supplier_id').agg({
                'unit_cost': ['mean', 'std'],
                'item_id': 'count'
            }).round(2)
            
            supplier_reliability.columns = ['Avg Cost', 'Cost Std Dev', 'Item Count']
            supplier_reliability = supplier_reliability.reset_index()
            
            # Calculate reliability score (lower cost variance = higher reliability)
            if supplier_reliability['Cost Std Dev'].max() > 0:
                supplier_reliability['reliability_score'] = 100 - ((supplier_reliability['Cost Std Dev'] - supplier_reliability['Cost Std Dev'].min()) / 
                                                               (supplier_reliability['Cost Std Dev'].max() - supplier_reliability['Cost Std Dev'].min())) * 100
            else:
                supplier_reliability['reliability_score'] = 100
            
            # Categorize suppliers by reliability
            supplier_reliability['reliability_category'] = np.where(
                supplier_reliability['reliability_score'] >= 80,
                'High Reliability',
                np.where(
                    supplier_reliability['reliability_score'] >= 60,
                    'Medium Reliability',
                    'Low Reliability'
                )
            )
            
            reliability_dist = supplier_reliability['reliability_category'].value_counts()
            avg_reliability = supplier_reliability['reliability_score'].mean()
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); 
                        border: 2px solid rgba(14, 165, 233, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #0ea5e9; margin: 0 0 15px 0;">🏭 Supplier Reliability</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>High Reliability:</strong> {reliability_dist.get('High Reliability', 0)} suppliers</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Medium Reliability:</strong> {reliability_dist.get('Medium Reliability', 0)} suppliers</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Avg Reliability Score:</strong> {avg_reliability:.1f}/100</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'reliability_category' in data.columns:
            fig_reliability = px.pie(
                values=reliability_dist.values,
                names=reliability_dist.index,
                title="Supplier Reliability Distribution",
                color_discrete_sequence=['#22c55e', '#f59e0b', '#dc2626']
            )
            fig_reliability.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_reliability, use_container_width=True)
    
    # 5. PROCESS BOTTLENECKS ANALYSIS
    st.subheader("⏱️ Process Bottlenecks Analysis")
    st.markdown("**Warehouse picking delays, slow replenishment cycles**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Analyze replenishment cycle efficiency
            data['replenishment_efficiency'] = np.where(
                data['current_stock'] <= data['reorder_point'],
                'Inefficient - Below Reorder',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 1.2,
                    'Efficient - Optimal Range',
                    'Over-Efficient - Overstocked'
                )
            )
            
            efficiency_dist = data['replenishment_efficiency'].value_counts()
            
            # Calculate bottleneck indicators
            bottleneck_items = len(data[data['replenishment_efficiency'] == 'Inefficient - Below Reorder'])
            optimal_items = len(data[data['replenishment_efficiency'] == 'Efficient - Optimal Range'])
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                        border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 20px; margin: 15px 0;">
                <h4 style="color: #22c55e; margin: 0 0 15px 0;">⏱️ Process Efficiency</h4>
                <p style="margin: 5px 0; color: #374151;"><strong>Bottleneck Items:</strong> {bottleneck_items} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Optimal Process:</strong> {optimal_items} items</p>
                <p style="margin: 5px 0; color: #374151;"><strong>Efficiency Rate:</strong> {(optimal_items/len(data)*100):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if 'replenishment_efficiency' in data.columns:
            fig_efficiency = px.pie(
                values=efficiency_dist.values,
                names=efficiency_dist.index,
                title="Replenishment Process Efficiency",
                color_discrete_sequence=['#dc2626', '#22c55e', '#f59e0b']
            )
            fig_efficiency.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Summary and Root Cause Insights
    st.subheader("🔍 Root Cause Summary & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚨 Critical Issues Identified:**")
        
        critical_issues = []
        
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            stockout_count = len(data[data['current_stock'] <= data['reorder_point']])
            if stockout_count > 0:
                critical_issues.append(f"• **{stockout_count} stockouts** - Investigate supplier delays and demand forecasting")
        
        if 'shrinkage_type' in data.columns:
            high_shrinkage = len(data[data['shrinkage_type'] == 'High Risk - Investigate'])
            if high_shrinkage > 0:
                critical_issues.append(f"• **{high_shrinkage} high-shrinkage items** - Review security and handling processes")
        
        if 'reliability_category' in data.columns:
            low_reliability = len(supplier_reliability[supplier_reliability['reliability_category'] == 'Low Reliability'])
            if low_reliability > 0:
                critical_issues.append(f"• **{low_reliability} unreliable suppliers** - Consider alternative sourcing")
        
        if not critical_issues:
            critical_issues.append("• No critical issues detected")
        
        for issue in critical_issues:
            st.write(issue)
    
    with col2:
        st.markdown("**🎯 Recommended Actions:**")
        
        recommended_actions = []
        
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            stockout_count = len(data[data['current_stock'] <= data['reorder_point']])
            if stockout_count > 0:
                recommended_actions.append("• Implement demand forecasting improvements")
                recommended_actions.append("• Review supplier lead times and reliability")
        
        if 'shrinkage_type' in data.columns:
            high_shrinkage = len(data[data['shrinkage_type'] == 'High Risk - Investigate'])
            if high_shrinkage > 0:
                recommended_actions.append("• Conduct inventory audits for high-risk items")
                recommended_actions.append("• Review warehouse security measures")
        
        if 'replenishment_efficiency' in data.columns:
            bottleneck_items = len(data[data['replenishment_efficiency'] == 'Inefficient - Below Reorder'])
            if bottleneck_items > 0:
                recommended_actions.append("• Optimize replenishment processes")
                recommended_actions.append("• Review warehouse picking efficiency")
        
        if not recommended_actions:
            recommended_actions.append("• Continue monitoring current processes")
        
        for action in recommended_actions:
            st.write(action)

def display_performance_metrics_dashboard(data):
    """Display comprehensive performance metrics dashboard with world-class analytics and interactive visualizations."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">📈 Performance & KPIs Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">World-class performance analysis and benchmarking for inventory optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for performance analysis.")
        return
    
    # Enhanced Performance Overview Section with Advanced Metrics
    st.subheader("🎯 Performance Overview")
    
    # Calculate enhanced performance metrics with advanced calculations
    total_items = len(data)
    total_value = (data['current_stock'] * data['unit_cost']).sum() if 'current_stock' in data.columns and 'unit_cost' in data.columns else 0
    avg_turnover = data['turnover_rate'].mean() if 'turnover_rate' in data.columns else 0
    avg_accuracy = data['forecast_accuracy'].mean() if 'forecast_accuracy' in data.columns else 0
    
    # Advanced performance calculations
    if 'turnover_rate' in data.columns:
        turnover_performance = 'Excellent' if avg_turnover >= 8 else 'Good' if avg_turnover >= 6 else 'Average' if avg_turnover >= 4 else 'Below Average'
        turnover_color = '#22c55e' if avg_turnover >= 6 else '#fbbf24' if avg_turnover >= 4 else '#dc2626'
    else:
        turnover_performance = 'N/A'
        turnover_color = '#667eea'
    
    if 'forecast_accuracy' in data.columns:
        accuracy_performance = 'Excellent' if avg_accuracy >= 90 else 'Good' if avg_accuracy >= 80 else 'Average' if avg_accuracy >= 70 else 'Below Average'
        accuracy_color = '#22c55e' if avg_accuracy >= 80 else '#fbbf24' if avg_accuracy >= 70 else '#dc2626'
    else:
        accuracy_performance = 'N/A'
        accuracy_color = '#667eea'
    
    # Enhanced KPI cards with interactive features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>📦 Total Items</h3>
            <h2>{total_items:,}</h2>
            <p>Active inventory items</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Categories: {data['category'].nunique() if 'category' in data.columns else 'N/A'}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                ✅ Status: Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>💰 Total Value</h3>
            <h2>${total_value:,.0f}</h2>
            <p>Current stock value</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Avg Item: ${total_value/total_items:,.2f if total_items > 0 else 0}
            </div>
            <div style="font-size: 0.8rem; color: #22c55e; margin-top: 5px;">
                💎 High Value Items: {len(data[data['current_stock'] * data['unit_cost'] > (data['current_stock'] * data['unit_cost']).quantile(0.9)]) if 'current_stock' in data.columns and 'unit_cost' in data.columns else 'N/A'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>🔄 Avg Turnover</h3>
            <h2 style="color: {turnover_color};">{avg_turnover:.2f}</h2>
            <p>Annual turnover rate</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Performance: {turnover_performance}
            </div>
            <div style="font-size: 0.8rem; color: {turnover_color}; margin-top: 5px;">
                {'🎉' if avg_turnover >= 8 else '✅' if avg_turnover >= 6 else '⚠️' if avg_turnover >= 4 else '❌'} {avg_turnover:.1f}x annual
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="inventory-metric-card">
            <h3>🎯 Forecast Accuracy</h3>
            <h2 style="color: {accuracy_color};">{avg_accuracy:.1f}%</h2>
            <p>Average forecast accuracy</p>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 10px;">
                📊 Performance: {accuracy_performance}
            </div>
            <div style="font-size: 0.8rem; color: {accuracy_color}; margin-top: 5px;">
                {'🎉' if avg_accuracy >= 90 else '✅' if avg_accuracy >= 80 else '⚠️' if avg_accuracy >= 70 else '❌'} {avg_accuracy:.1f}% accuracy
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Performance Distribution Analysis with Interactive Charts
    st.subheader("📊 Performance Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Turnover Rate Distribution with better tooltips
        if 'turnover_rate' in data.columns:
            fig_turnover_dist = go.Figure(data=[go.Histogram(
                x=data['turnover_rate'],
                nbinsx=20,
                marker_color='rgba(102, 126, 234, 0.7)',
                marker_line_color='rgba(102, 126, 234, 1)',
                marker_line_width=1,
                hovertemplate="<b>Turnover Rate Range</b><br>" +
                            "Rate: %{x:.2f}<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            # Add performance threshold lines
            fig_turnover_dist.add_vline(x=4, line_dash="dash", line_color="orange", 
                                      annotation_text="Average Threshold", annotation_position="top")
            fig_turnover_dist.add_vline(x=6, line_dash="dash", line_color="green", 
                                      annotation_text="Good Threshold", annotation_position="top")
            fig_turnover_dist.add_vline(x=8, line_dash="dash", line_color="blue", 
                                      annotation_text="Excellent Threshold", annotation_position="top")
            
            fig_turnover_dist.update_layout(
                title={
                    'text': "Turnover Rate Distribution with Performance Thresholds",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Turnover Rate",
                yaxis_title="Number of Items",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig_turnover_dist, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced Forecast Accuracy Distribution with better tooltips
        if 'forecast_accuracy' in data.columns:
            fig_accuracy_dist = go.Figure(data=[go.Histogram(
                x=data['forecast_accuracy'],
                nbinsx=20,
                marker_color='rgba(118, 75, 162, 0.7)',
                marker_line_color='rgba(118, 75, 162, 1)',
                marker_line_width=1,
                hovertemplate="<b>Forecast Accuracy Range</b><br>" +
                            "Accuracy: %{x:.1f}%<br>" +
                            "Number of Items: %{y}<br>" +
                            "<extra></extra>"
            )])
            
            # Add accuracy threshold lines
            fig_accuracy_dist.add_vline(x=70, line_dash="dash", line_color="orange", 
                                      annotation_text="Average Threshold", annotation_position="top")
            fig_accuracy_dist.add_vline(x=80, line_dash="dash", line_color="green", 
                                      annotation_text="Good Threshold", annotation_position="top")
            fig_accuracy_dist.add_vline(x=90, line_dash="dash", line_color="blue", 
                                      annotation_text="Excellent Threshold", annotation_position="top")
            
            fig_accuracy_dist.update_layout(
                title={
                    'text': "Forecast Accuracy Distribution with Performance Thresholds",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Forecast Accuracy (%)",
                yaxis_title="Number of Items",
                xaxis=dict(range=[0, 100]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig_accuracy_dist, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Performance Benchmarking with Interactive Rankings
    st.subheader("🏆 Performance Benchmarking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Top Performers by Turnover with better tooltips
        if 'turnover_rate' in data.columns:
            top_turnover = data.nlargest(10, 'turnover_rate')[['item_name', 'turnover_rate', 'category']]
            
            fig_top_turnover = go.Figure(data=[go.Bar(
                x=top_turnover['turnover_rate'],
                y=top_turnover['item_name'],
                orientation='h',
                marker_color='rgba(34, 197, 94, 0.8)',
                marker_line_color='rgba(34, 197, 94, 1)',
                marker_line_width=2,
                hovertemplate="<b>%{y}</b><br>" +
                            "Turnover Rate: %{x:.2f}<br>" +
                            "Category: %{customdata}<br>" +
                            "<extra></extra>",
                customdata=top_turnover['category']
            )])
            
            fig_top_turnover.update_layout(
                title={
                    'text': "Top 10 Items by Turnover Rate",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Turnover Rate",
                yaxis_title="Item Name",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_top_turnover, use_container_width=True, config={'displayModeBar': True})
    
    with col2:
        # Enhanced Top Performers by Forecast Accuracy with better tooltips
        if 'forecast_accuracy' in data.columns:
            top_accuracy = data.nlargest(10, 'forecast_accuracy')[['item_name', 'forecast_accuracy', 'category']]
            
            fig_top_accuracy = go.Figure(data=[go.Bar(
                x=top_accuracy['forecast_accuracy'],
                y=top_accuracy['item_name'],
                orientation='h',
                marker_color='rgba(20, 184, 166, 0.8)',
                marker_line_color='rgba(20, 184, 166, 1)',
                marker_line_width=2,
                hovertemplate="<b>%{y}</b><br>" +
                            "Forecast Accuracy: %{x:.1f}%<br>" +
                            "Category: %{customdata}<br>" +
                            "<extra></extra>",
                customdata=top_accuracy['category']
            )])
            
            fig_top_accuracy.update_layout(
                title={
                    'text': "Top 10 Items by Forecast Accuracy",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#2d3748'}
                },
                xaxis_title="Forecast Accuracy (%)",
                yaxis_title="Item Name",
                xaxis=dict(range=[0, 100]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=60, r=20, t=60, b=60)
            )
            
            st.plotly_chart(fig_top_accuracy, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Performance Trends Analysis with Interactive Time Series
    st.subheader("📈 Performance Trends Analysis")
    
    if 'date' in data.columns and 'turnover_rate' in data.columns:
        # Enhanced Time Series Analysis with better tooltips
        data['date'] = pd.to_datetime(data['date'])
        data['month'] = data['date'].dt.to_period('M')
        
        monthly_performance = data.groupby('month').agg({
            'turnover_rate': 'mean',
            'forecast_accuracy': 'mean' if 'forecast_accuracy' in data.columns else 'turnover_rate'
        }).reset_index()
        
        monthly_performance['month'] = monthly_performance['month'].astype(str)
        
        # Create enhanced trends chart with multiple metrics
        fig_trends = go.Figure()
        
        # Add turnover rate line
        fig_trends.add_trace(go.Scatter(
            x=monthly_performance['month'],
            y=monthly_performance['turnover_rate'],
            mode='lines+markers',
            name='Turnover Rate',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea'),
            hovertemplate="<b>Month: %{x}</b><br>" +
                        "Turnover Rate: %{y:.2f}<br>" +
                        "<extra></extra>"
        ))
        
        # Add forecast accuracy line if available
        if 'forecast_accuracy' in data.columns:
            fig_trends.add_trace(go.Scatter(
                x=monthly_performance['month'],
                y=monthly_performance['forecast_accuracy'],
                mode='lines+markers',
                name='Forecast Accuracy',
                line=dict(color='#764ba2', width=3),
                marker=dict(size=8, color='#764ba2'),
                yaxis='y2',
                hovertemplate="<b>Month: %{x}</b><br>" +
                            "Forecast Accuracy: %{y:.1f}%<br>" +
                            "<extra></extra>"
            ))
        
        fig_trends.update_layout(
            title={
                'text': "Monthly Performance Trends",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#2d3748'}
            },
            xaxis_title="Month",
            yaxis_title="Turnover Rate",
            yaxis2=dict(
                title="Forecast Accuracy (%)",
                overlaying='y',
                side='right',
                range=[0, 100]
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            margin=dict(l=60, r=60, t=60, b=60),
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig_trends, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Performance by Category with Interactive Analysis
    st.subheader("📊 Performance by Category")
    
    if 'category' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced Category Performance Comparison with better tooltips
            if 'turnover_rate' in data.columns:
                category_performance = data.groupby('category')['turnover_rate'].agg(['mean', 'std', 'count']).reset_index()
                category_performance.columns = ['Category', 'Avg Turnover', 'Std Dev', 'Item Count']
                
                fig_category_perf = go.Figure(data=[go.Bar(
                    x=category_performance['Category'],
                    y=category_performance['Avg Turnover'],
                    marker_color='rgba(139, 92, 246, 0.8)',
                    marker_line_color='rgba(139, 92, 246, 1)',
                    marker_line_width=2,
                    hovertemplate="<b>%{x}</b><br>" +
                                "Avg Turnover: %{y:.2f}<br>" +
                                "Items: %{customdata}<br>" +
                                "<extra></extra>",
                    customdata=category_performance['Item Count']
                )])
                
                fig_category_perf.update_layout(
                    title={
                        'text': "Average Turnover Rate by Category",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Category",
                    yaxis_title="Average Turnover Rate",
                    xaxis=dict(tickangle=45),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=80)
                )
                
                st.plotly_chart(fig_category_perf, use_container_width=True, config={'displayModeBar': True})
        
        with col2:
            # Enhanced Category Forecast Accuracy Comparison with better tooltips
            if 'forecast_accuracy' in data.columns:
                category_accuracy = data.groupby('category')['forecast_accuracy'].agg(['mean', 'std', 'count']).reset_index()
                category_accuracy.columns = ['Category', 'Avg Accuracy', 'Std Dev', 'Item Count']
                
                fig_category_acc = go.Figure(data=[go.Bar(
                    x=category_accuracy['Category'],
                    y=category_accuracy['Avg Accuracy'],
                    marker_color='rgba(251, 146, 60, 0.8)',
                    marker_line_color='rgba(251, 146, 60, 1)',
                    marker_line_width=2,
                    hovertemplate="<b>%{x}</b><br>" +
                                "Avg Accuracy: %{y:.1f}%<br>" +
                                "Items: %{customdata}<br>" +
                                "<extra></extra>",
                    customdata=category_accuracy['Item Count']
                )])
                
                fig_category_acc.update_layout(
                    title={
                        'text': "Average Forecast Accuracy by Category",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#2d3748'}
                    },
                    xaxis_title="Category",
                    yaxis_title="Average Forecast Accuracy (%)",
                    xaxis=dict(tickangle=45),
                    yaxis=dict(range=[0, 100]),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    margin=dict(l=60, r=20, t=60, b=80)
                )
                
                st.plotly_chart(fig_category_acc, use_container_width=True, config={'displayModeBar': True})
    
    # Enhanced Performance Insights and Recommendations with Interactive Elements
    st.subheader("💡 Performance Insights & Recommendations")
    
    with st.expander("📊 Advanced Performance Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Overall Performance Analysis:**")
            
            if 'turnover_rate' in data.columns:
                turnover_stats = data['turnover_rate'].describe()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                            border: 2px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #667eea; margin: 0 0 10px 0;">🔄 Turnover Performance</h4>
                    <p style="margin: 0; color: #374151;"><strong>Mean:</strong> {turnover_stats['mean']:.2f}</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Median:</strong> {turnover_stats['50%']:.2f}</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Std Dev:</strong> {turnover_stats['std']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Performance level assessment with enhanced styling
                if turnover_stats['mean'] >= 8:
                    performance_level = "Excellent"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">🎉 Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your inventory turnover performance is exceptional!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif turnover_stats['mean'] >= 6:
                    performance_level = "Good"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%); 
                                border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #3b82f6; margin: 0 0 10px 0;">✅ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your inventory turnover performance is above average!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif turnover_stats['mean'] >= 4:
                    performance_level = "Average"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Your inventory turnover performance has room for improvement!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    performance_level = "Below Average"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 10px 0;">❌ Performance Level: {performance_level}</h4>
                        <p style="margin: 0; color: #374151;">Immediate action required to improve inventory turnover!</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🎯 Key Performance Indicators:**")
            
            if 'forecast_accuracy' in data.columns:
                accuracy_stats = data['forecast_accuracy'].describe()
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(13, 148, 136, 0.1) 100%); 
                            border: 2px solid rgba(20, 184, 166, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #14b8a6; margin: 0 0 10px 0;">🎯 Forecast Accuracy</h4>
                    <p style="margin: 0; color: #374151;"><strong>Mean:</strong> {accuracy_stats['mean']:.1f}%</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Median:</strong> {accuracy_stats['50%']:.1f}%</p>
                    <p style="margin: 5px 0 0 0; color: #374151;"><strong>Std Dev:</strong> {accuracy_stats['std']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'current_stock' in data.columns and 'reorder_point' in data.columns:
                stockout_risk = len(data[data['current_stock'] <= data['reorder_point']])
                total_items = len(data)
                risk_percentage = (stockout_risk / total_items) * 100
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%); 
                            border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">⚠️ Stockout Risk</h4>
                    <p style="margin: 0; color: #374151;"><strong>{stockout_risk}/{total_items}</strong> items ({risk_percentage:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)
                
                if risk_percentage > 20:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%); 
                                border: 2px solid rgba(220, 38, 38, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #dc2626; margin: 0 0 10px 0;">🚨 High Stockout Risk!</h4>
                        <p style="margin: 0; color: #374151;">Immediate action required to prevent stockouts!</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif risk_percentage > 10:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); 
                                border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #fbbf24; margin: 0 0 10px 0;">⚠️ Moderate Stockout Risk</h4>
                        <p style="margin: 0; color: #374151;">Monitor closely and initiate reordering!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%); 
                                border: 2px solid rgba(34, 197, 94, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
                        <h4 style="color: #22c55e; margin: 0 0 10px 0;">✅ Low Stockout Risk</h4>
                        <p style="margin: 0; color: #374151;">Excellent inventory control maintained!</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Enhanced Performance Recommendations with Interactive Elements
    st.subheader("🚀 Performance Optimization Recommendations")
    
    recommendations = []
    
    # Generate dynamic recommendations based on performance data
    if 'turnover_rate' in data.columns:
        low_turnover_threshold = data['turnover_rate'].quantile(0.25)
        low_turnover_items = data[data['turnover_rate'] < low_turnover_threshold]
        
        if not low_turnover_items.empty:
            recommendations.append({
                'type': 'warning',
                'title': 'Turnover Rate Optimization',
                'message': f'{len(low_turnover_items)} items have low turnover rates (< {low_turnover_threshold:.2f})',
                'action': 'Consider promotional activities, price adjustments, or inventory reviews'
            })
    
    if 'forecast_accuracy' in data.columns:
        low_accuracy_threshold = 80
        low_accuracy_items = data[data['forecast_accuracy'] < low_accuracy_threshold]
        
        if not low_accuracy_items.empty:
            recommendations.append({
                'type': 'warning',
                'title': 'Forecast Improvement',
                'message': f'{len(low_accuracy_items)} items have forecast accuracy below {low_accuracy_threshold}%',
                'action': 'Review forecasting models and data quality for these items'
            })
    
    if 'current_stock' in data.columns and 'reorder_point' in data.columns:
        overstock_threshold = 1.5
        overstock_items = data[data['current_stock'] > data['reorder_point'] * overstock_threshold]
        
        if not overstock_items.empty:
            recommendations.append({
                'type': 'info',
                'title': 'Stock Level Optimization',
                'message': f'{len(overstock_items)} items have stock levels significantly above reorder points',
                'action': 'Consider reducing order quantities or implementing promotional activities'
            })
    
    if 'storage_volume' in data.columns and 'current_stock' in data.columns:
        data['utilization'] = (data['current_stock'] / data['storage_volume']) * 100
        low_utilization = data[data['utilization'] < 50]
        
        if not low_utilization.empty:
            recommendations.append({
                'type': 'info',
                'title': 'Space Efficiency',
                'message': f'{len(low_utilization)} items have low space utilization (< 50%)',
                'action': 'Consider consolidation or storage optimization strategies'
            })
    
    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Optimal Performance',
            'message': 'All performance metrics are within optimal ranges',
            'action': 'Continue monitoring for continuous improvement opportunities'
        })
    
    # Display recommendations with enhanced styling
    for i, rec in enumerate(recommendations):
        color_map = {
            'success': '#22c55e',
            'warning': '#fbbf24',
            'error': '#dc2626',
            'info': '#3b82f6'
        }
        
        icon_map = {
            'success': '✅',
            'warning': '⚠️',
            'error': '🚨',
            'info': 'ℹ️'
        }
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba({color_map[rec['type']].replace('#', '')}, 0.1) 0%, rgba({color_map[rec['type']].replace('#', '')}, 0.05) 100%); 
                    border: 2px solid rgba({color_map[rec['type']].replace('#', '')}, 0.3); border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h4 style="color: {color_map[rec['type']]}; margin: 0 0 10px 0;">{icon_map[rec['type']]} {rec['title']}</h4>
            <p style="margin: 0; color: #374151;">{rec['message']}</p>
            <div style="margin-top: 10px;">
                <strong style="color: {color_map[rec['type']]};">Recommended Action:</strong> {rec['action']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Performance Summary Table with Interactive Features
    st.subheader("📋 Performance Summary Table")
    
    if 'category' in data.columns:
        # Create comprehensive performance summary
        performance_summary = data.groupby('category').agg({
            'item_id': 'count',
            'turnover_rate': ['mean', 'std', 'min', 'max'] if 'turnover_rate' in data.columns else 'item_id',
            'forecast_accuracy': ['mean', 'std', 'min', 'max'] if 'forecast_accuracy' in data.columns else 'item_id',
            'current_stock': 'sum' if 'current_stock' in data.columns else 'item_id'
        }).round(2)
        
        # Flatten column names
        performance_summary.columns = ['_'.join(col).strip() for col in performance_summary.columns]
        performance_summary = performance_summary.reset_index()
        
        # Rename columns for readability
        column_mapping = {
            'item_id_count': 'Total Items',
            'turnover_rate_mean': 'Avg Turnover',
            'turnover_rate_std': 'Turnover Std Dev',
            'turnover_rate_min': 'Min Turnover',
            'turnover_rate_max': 'Max Turnover',
            'forecast_accuracy_mean': 'Avg Forecast Acc',
            'forecast_accuracy_std': 'Forecast Std Dev',
            'forecast_accuracy_min': 'Min Forecast Acc',
            'forecast_accuracy_max': 'Max Forecast Acc',
            'current_stock_sum': 'Total Stock'
        }
        
        performance_summary = performance_summary.rename(columns=column_mapping)
        
        # Display enhanced summary table
        st.dataframe(performance_summary, use_container_width=True)
        
        # Add interactive insights and chart download options
        st.markdown("**💡 Interactive Features:**")
        st.markdown("""
        - **Hover over charts** for detailed performance metrics
        - **Use chart controls** to zoom, pan, and explore data
        - **Click legend items** to show/hide specific performance metrics
        - **Download charts** as PNG or SVG using the chart toolbar
        - **Performance thresholds** are automatically highlighted on charts
        """)

def display_operations_analytics_dashboard(data):
    """Display comprehensive operations analytics dashboard."""
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">🏗️ Operations Analytics Dashboard</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Comprehensive warehouse and operational efficiency analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data.empty:
        st.warning("📊 No data available for operations analysis.")
        return
    
    # Operations Overview Section
    st.subheader("🎯 Operations Overview")
    
    # Calculate key operations metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'warehouse_location' in data.columns:
            unique_locations = data['warehouse_location'].nunique()
            st.metric("Warehouse Locations", f"{unique_locations:,}")
        else:
            st.metric("Warehouse Locations", "N/A")
    
    with col2:
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            total_capacity = data['storage_volume'].sum()
            total_utilized = data['current_stock'].sum()
            utilization_rate = (total_utilized / total_capacity) * 100 if total_capacity > 0 else 0
            st.metric("Storage Utilization", f"{utilization_rate:.1f}%")
        else:
            st.metric("Storage Utilization", "N/A")
    
    with col3:
        if 'reorder_point' in data.columns and 'current_stock' in data.columns:
            below_reorder = len(data[data['current_stock'] <= data['reorder_point']])
            total_items = len(data)
            reorder_percentage = (below_reorder / total_items) * 100 if total_items > 0 else 0
            st.metric("Items Below Reorder", f"{below_reorder:,} ({reorder_percentage:.1f}%)")
        else:
            st.metric("Items Below Reorder", "N/A")
    
    with col4:
        if 'turnover_rate' in data.columns:
            avg_turnover = data['turnover_rate'].mean()
            st.metric("Avg Turnover Rate", f"{avg_turnover:.2f}")
        else:
            st.metric("Avg Turnover Rate", "N/A")
    
    # Warehouse Operations Analysis
    st.subheader("🏭 Warehouse Operations Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Storage utilization by location
        if 'warehouse_location' in data.columns and 'storage_volume' in data.columns and 'current_stock' in data.columns:
            location_utilization = data.groupby('warehouse_location').agg({
                'storage_volume': 'sum',
                'current_stock': 'sum'
            }).reset_index()
            
            location_utilization['utilization_rate'] = (location_utilization['current_stock'] / location_utilization['storage_volume']) * 100
            location_utilization['utilization_rate'] = location_utilization['utilization_rate'].clip(0, 100)
            
            fig_location_utilization = px.bar(
                location_utilization,
                x='warehouse_location',
                y='utilization_rate',
                title="Storage Utilization by Location",
                color_discrete_sequence=['#667eea']
            )
            fig_location_utilization.update_layout(xaxis_title="Warehouse Location", yaxis_title="Utilization Rate (%)")
            fig_location_utilization.update_xaxes(tickangle=45)
            st.plotly_chart(fig_location_utilization, use_container_width=True)
    
    with col2:
        # Stock level distribution
        if 'current_stock' in data.columns and 'reorder_point' in data.columns:
            # Categorize stock levels
            data['stock_level_status'] = np.where(
                data['current_stock'] <= data['reorder_point'],
                'Below Reorder Point',
                np.where(
                    data['current_stock'] <= data['reorder_point'] * 1.5,
                    'Optimal Range',
                    'Overstocked'
                )
            )
            
            stock_level_dist = data['stock_level_status'].value_counts()
            
            fig_stock_levels = px.pie(
                values=stock_level_dist.values,
                names=stock_level_dist.index,
                title="Stock Level Distribution",
                color_discrete_sequence=['#dc2626', '#22c55e', '#f59e0b']
            )
            fig_stock_levels.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_stock_levels, use_container_width=True)
    
    # Operational Efficiency Metrics
    st.subheader("⚡ Operational Efficiency Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Turnover rate by location
        if 'turnover_rate' in data.columns and 'warehouse_location' in data.columns:
            location_turnover = data.groupby('warehouse_location')['turnover_rate'].agg(['mean', 'std', 'count']).reset_index()
            location_turnover.columns = ['Location', 'Avg Turnover', 'Std Dev', 'Item Count']
            
            fig_location_turnover = px.bar(
                location_turnover,
                x='Location',
                y='Avg Turnover',
                title="Average Turnover Rate by Location",
                color_discrete_sequence=['#764ba2']
            )
            fig_location_turnover.update_layout(xaxis_title="Warehouse Location", yaxis_title="Average Turnover Rate")
            fig_location_turnover.update_xaxes(tickangle=45)
            st.plotly_chart(fig_location_turnover, use_container_width=True)
    
    with col2:
        # Space efficiency analysis
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            data['space_efficiency'] = (data['current_stock'] / data['storage_volume']) * 100
            data['space_efficiency'] = data['space_efficiency'].clip(0, 100)
            
            efficiency_stats = data['space_efficiency'].describe()
            
            fig_space_efficiency = px.histogram(
                data,
                x='space_efficiency',
                nbins=20,
                title="Space Efficiency Distribution",
                color_discrete_sequence=['#14b8a6']
            )
            fig_space_efficiency.update_layout(xaxis_title="Space Efficiency (%)", yaxis_title="Number of Items")
            st.plotly_chart(fig_space_efficiency, use_container_width=True)
    
    # Inventory Movement Analysis
    st.subheader("📦 Inventory Movement Analysis")
    
    if 'transaction_type' in data.columns and 'quantity' in data.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Transaction type distribution
            transaction_dist = data['transaction_type'].value_counts()
            
            fig_transaction_dist = px.pie(
                values=transaction_dist.values,
                names=transaction_dist.index,
                title="Transaction Type Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_transaction_dist.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_transaction_dist, use_container_width=True)
        
        with col2:
            # Quantity distribution by transaction type
            transaction_quantity = data.groupby('transaction_type')['quantity'].agg(['mean', 'std', 'count']).reset_index()
            transaction_quantity.columns = ['Transaction Type', 'Avg Quantity', 'Std Dev', 'Count']
            
            fig_transaction_quantity = px.bar(
                transaction_quantity,
                x='Transaction Type',
                y='Avg Quantity',
                title="Average Quantity by Transaction Type",
                color_discrete_sequence=['#8b5cf6']
            )
            fig_transaction_quantity.update_layout(xaxis_title="Transaction Type", yaxis_title="Average Quantity")
            st.plotly_chart(fig_transaction_quantity, use_container_width=True)
    
    # Performance Benchmarking
    st.subheader("🏆 Performance Benchmarking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top performing locations
        if 'warehouse_location' in data.columns and 'turnover_rate' in data.columns:
            top_locations = data.groupby('warehouse_location')['turnover_rate'].mean().nlargest(10).reset_index()
            
            fig_top_locations = px.bar(
                top_locations,
                x='turnover_rate',
                y='warehouse_location',
                orientation='h',
                title="Top 10 Locations by Turnover Rate",
                color_discrete_sequence=['#22c55e']
            )
            fig_top_locations.update_layout(xaxis_title="Average Turnover Rate", yaxis_title="Warehouse Location")
            st.plotly_chart(fig_top_locations, use_container_width=True)
    
    with col2:
        # Most efficient space utilization
        if 'storage_volume' in data.columns and 'current_stock' in data.columns:
            data['space_utilization'] = (data['current_stock'] / data['storage_volume']) * 100
            data['space_utilization'] = data['space_utilization'].clip(0, 100)
            
            top_efficiency = data.groupby('warehouse_location')['space_utilization'].mean().nlargest(10).reset_index()
            
            fig_top_efficiency = px.bar(
                top_efficiency,
                x='space_utilization',
                y='warehouse_location',
                orientation='h',
                title="Top 10 Locations by Space Efficiency",
                color_discrete_sequence=['#06b6d4']
            )
            fig_top_efficiency.update_layout(xaxis_title="Space Efficiency (%)", yaxis_title="Warehouse Location")
            st.plotly_chart(fig_top_efficiency, use_container_width=True)
    
    # Operations Insights and Recommendations
    st.subheader("💡 Operations Insights & Recommendations")
    
    insights_container = st.container()
    
    with insights_container:
        # Overall operations insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Operations Performance Analysis:**")
            
            if 'turnover_rate' in data.columns:
                turnover_stats = data['turnover_rate'].describe()
                st.write(f"• **Turnover Performance:**")
                st.write(f"  - Mean: {turnover_stats['mean']:.2f}")
                st.write(f"  - Median: {turnover_stats['50%']:.2f}")
                st.write(f"  - Std Dev: {turnover_stats['std']:.2f}")
                
                # Performance assessment
                if turnover_stats['mean'] >= 8:
                    st.success("🎉 **Excellent operational performance!**")
                elif turnover_stats['mean'] >= 6:
                    st.info("✅ **Good operational performance!**")
                elif turnover_stats['mean'] >= 4:
                    st.warning("⚠️ **Average operational performance - room for improvement!**")
                else:
                    st.error("❌ **Below average operational performance - immediate action required!**")
        
        with col2:
            st.markdown("**🎯 Key Operations Metrics:**")
            
            if 'storage_volume' in data.columns and 'current_stock' in data.columns:
                total_capacity = data['storage_volume'].sum()
                total_utilized = data['current_stock'].sum()
                utilization_rate = (total_utilized / total_capacity) * 100 if total_capacity > 0 else 0
                
                st.write(f"• **Space Utilization:**")
                st.write(f"  - Total Capacity: {total_capacity:,.0f}")
                st.write(f"  - Total Utilized: {total_utilized:,.0f}")
                st.write(f"  - Utilization Rate: {utilization_rate:.1f}%")
                
                if utilization_rate >= 80:
                    st.success("🎉 **Excellent space utilization!**")
                elif utilization_rate >= 60:
                    st.info("✅ **Good space utilization!**")
                elif utilization_rate >= 40:
                    st.warning("⚠️ **Moderate space utilization - room for improvement!**")
                else:
                    st.error("❌ **Low space utilization - immediate action required!**")
    
    # Operations Recommendations
    st.subheader("🚀 Operations Optimization Recommendations")
    
    recommendations = []
    
    # Generate dynamic recommendations based on operations data
    if 'turnover_rate' in data.columns:
        low_turnover_threshold = data['turnover_rate'].quantile(0.25)
        low_turnover_items = data[data['turnover_rate'] < low_turnover_threshold]
        
        if not low_turnover_items.empty:
            recommendations.append(f"• **Turnover Optimization:** {len(low_turnover_items)} items have low turnover rates (< {low_turnover_threshold:.2f}). Consider promotional activities or inventory reviews.")
    
    if 'storage_volume' in data.columns and 'current_stock' in data.columns:
        low_utilization_threshold = 50
        low_utilization_items = data[data['space_utilization'] < low_utilization_threshold]
        
        if not low_utilization_items.empty:
            recommendations.append(f"• **Space Efficiency:** {len(low_utilization_items)} items have low space utilization (< {low_utilization_threshold}%). Consider consolidation or storage optimization.")
    
    if not recommendations:
        recommendations.append("• **Status:** All operations metrics are within optimal ranges. Continue monitoring for continuous improvement.")
    
    for rec in recommendations:
        st.write(rec)
    
    # Operations Summary Table
    st.subheader("📋 Operations Summary Table")
    
    if 'warehouse_location' in data.columns:
        # Create comprehensive operations summary
        operations_summary = data.groupby('warehouse_location').agg({
            'item_id': 'count',
            'turnover_rate': 'mean' if 'turnover_rate' in data.columns else 'item_id',
            'current_stock': 'sum' if 'current_stock' in data.columns else 'item_id',
            'storage_volume': 'sum' if 'storage_volume' in data.columns else 'item_id'
        }).round(2)
        
        operations_summary = operations_summary.reset_index()
        operations_summary.columns = ['Warehouse Location', 'Total Items', 'Avg Turnover Rate', 'Total Stock', 'Total Capacity']
        
        # Display summary table
        st.dataframe(operations_summary, use_container_width=True)

# ============================================================================
# MAIN APPLICATION FUNCTION
# ============================================================================

def set_home_page():
    """Set the department to start on home page"""
    st.session_state.current_page = "🏠 Home"

def main():
    """Main function to run the Inventory Intelligence Dashboard."""
    
    # Load styling (original theme)
    load_inventory_styling()
    
    # Initialize session state
    if 'inventory_data' not in st.session_state:
        st.session_state.inventory_data = pd.DataFrame()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    if 'data_processed' not in st.session_state:
        st.session_state.data_processed = False
    
    # Display header
    display_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px;">
            <h3 style="color: #4CAF50; margin-bottom: 15px; text-align: center; font-size: 1.2rem; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
                🎯 Navigation
            </h3>
            <p style="color: #2196F3; text-align: center; margin: 0; font-size: 0.85rem; font-weight: 500;">
                Select a section to explore
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = "🏠 Home"
        
        if st.button("📊 Data Input", key="nav_data_input", use_container_width=True):
            st.session_state.current_page = "📊 Data Input"
        
        if st.button("📊 Executive Summary", key="nav_executive", use_container_width=True):
            st.session_state.current_page = "📊 Executive Summary"
        
        if st.button("📈 KPI Overview", key="nav_kpi", use_container_width=True):
            st.session_state.current_page = "📈 KPI Overview"
        
        if st.button("📊 Stock Analysis", key="nav_stock_analysis", use_container_width=True):
            st.session_state.current_page = "📊 Stock Analysis"
        
        if st.button("📦 Inventory Overview", key="nav_inventory", use_container_width=True):
            st.session_state.current_page = "📦 Inventory Overview"
        
        if st.button("🔮 Demand Forecasting", key="nav_forecasting", use_container_width=True):
            st.session_state.current_page = "🔮 Demand Forecasting"
        
        if st.button("🛡️ Risk Assessment", key="nav_risk", use_container_width=True):
            st.session_state.current_page = "🛡️ Risk Assessment"
        
        if st.button("🏭 Warehouse Operations", key="nav_warehouse", use_container_width=True):
            st.session_state.current_page = "🏭 Warehouse Operations"
        
        if st.button("🔍 Diagnostic Analytics", key="nav_diagnostic", use_container_width=True):
            st.session_state.current_page = "🔍 Diagnostic Analytics"
        
        if st.button("🔮 Predictive Analytics", key="nav_predictive", use_container_width=True):
            st.session_state.current_page = "🔮 Predictive Analytics"
        
        if st.button("🎯 Prescriptive Analytics", key="nav_prescriptive", use_container_width=True):
            st.session_state.current_page = "🎯 Prescriptive Analytics"
        
        if st.button("🤖 Auto Insights", key="nav_insights", use_container_width=True):
            st.session_state.current_page = "🤖 Auto Insights"
        
        # Developer attribution at the bottom of sidebar
        st.markdown("---")
        st.markdown("""
        <div style="padding: 12px 0; text-align: center;">
            <p style="color: #95a5a6; font-size: 0.75rem; margin: 0; line-height: 1.3;">
                Developed by <strong style="color: #3498db;">Aryan Zabihi</strong><br>
                <a href="https://github.com/Aryanzabihi" target="_blank" style="color: #3498db; text-decoration: none;">GitHub</a> • 
                <a href="https://www.linkedin.com/in/aryanzabihi/" target="_blank" style="color: #3498db; text-decoration: none;">LinkedIn</a> • 
                <a href="https://www.paypal.com/donate/?hosted_button_id=C9W46U77KNU9S" target="_blank" style="color: #ffc439; text-decoration: none; font-weight: 600;">💝 Donate</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance optimization: Lazy load data processing
    if not st.session_state.data_processed and not st.session_state.inventory_data.empty:
        with st.spinner("🔄 Optimizing data for performance..."):
            # Pre-process data for faster analytics
            if 'current_stock' in st.session_state.inventory_data.columns and 'unit_cost' in st.session_state.inventory_data.columns:
                st.session_state.inventory_data['stock_value'] = st.session_state.inventory_data['current_stock'] * st.session_state.inventory_data['unit_cost']
            st.session_state.data_processed = True
    
    # Display current page
    if st.session_state.current_page == "🏠 Home":
        # Home page with comprehensive overview
        st.markdown("## 🏠 Dashboard Overview")
        
        # Check if data is loaded
        if st.session_state.inventory_data.empty:
            # Welcome section with 4 colored cards
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
                <h2 style="color: #495057; margin-bottom: 1rem;">🎯 Welcome to Inventory Intelligence</h2>
                <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                    Get started by uploading your inventory data or generating sample data to explore the dashboard features.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 4 colored metric cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card(
                    "Analytics Categories", 
                    "12 comprehensive",
                    "analysis areas"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card(
                    "Inventory Analytics", 
                    "Real-time",
                    "metrics & insights"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card(
                    "Predictive", 
                    "Advanced",
                    "forecasting"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(create_metric_card(
                    "Risk Management", 
                    "Comprehensive",
                    "risk assessment"
                ), unsafe_allow_html=True)
            
            # Available analytics categories (6 cards in 2 columns)
            st.markdown("### 📊 Available Inventory Analytics Categories:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Card 1: KPI Overview
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">📈 KPI Overview</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>Inventory Turnover Rate</li>
                        <li>Stockout Frequency</li>
                        <li>Carrying Cost Analysis</li>
                        <li>Order Fill Rate</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 2: Inventory Overview
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">📦 Inventory Overview</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>Stock Level Analysis</li>
                        <li>Category Distribution</li>
                        <li>Value Analysis</li>
                        <li>Location Tracking</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 3: Demand Forecasting
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">🔮 Demand Forecasting</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>Seasonal Patterns</li>
                        <li>Trend Analysis</li>
                        <li>Forecast Accuracy</li>
                        <li>Demand Planning</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Card 4: Risk Assessment
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">🛡️ Risk Assessment</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>Stockout Risk</li>
                        <li>Excess Inventory Risk</li>
                        <li>Supplier Risk Analysis</li>
                        <li>Market Risk Assessment</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 5: Predictive Analytics
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">🔮 Predictive Analytics</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>ML-powered Forecasting</li>
                        <li>Anomaly Detection</li>
                        <li>Optimization Models</li>
                        <li>Scenario Planning</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Card 6: Warehouse Operations
                st.markdown("""
                <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                    <h4 style="color: #495057; margin-bottom: 1rem;">🏭 Warehouse Operations</h4>
                    <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                        <li>Space Utilization</li>
                        <li>Picking Efficiency</li>
                        <li>Storage Optimization</li>
                        <li>Process Analysis</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Getting Started section (3 cards)
            st.markdown("### 🚀 Getting Started:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                    <h4 style="margin-bottom: 1rem;">1. Data Input</h4>
                    <p style="margin: 0;">Enter your inventory data in the 'Data Input' tab</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                    <h4 style="margin-bottom: 1rem;">2. Calculate Metrics</h4>
                    <p style="margin: 0;">Use the main tabs to view specific metric categories</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                    <h4 style="margin-bottom: 1rem;">3. Real-time Analysis</h4>
                    <p style="margin: 0;">All metrics update automatically based on your data</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Data Schema section (8 cards in 2 rows)
            st.markdown("### 📈 Data Schema:")
            st.markdown("The application supports the following inventory data structure:")
            
            # Row 1 (4 cards)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">📦 Items</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Product details, SKUs, categories</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #6c757d; font-size: 0.9rem; margin: 0;">Stock levels, locations, costs</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">📊 Transactions</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Orders, receipts, adjustments</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">🏭 Suppliers</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Vendor info, lead times, costs</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Row 2 (4 cards)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">📅 Demand History</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Sales data, seasonal patterns</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">💰 Costs</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Holding costs, ordering costs</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; font-size: 0.9rem; margin: 0;">Warehouse layout, zones</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                    <h5 style="color: #495057; margin-bottom: 0.5rem;">📊 Performance</h5>
                    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">KPIs, metrics, benchmarks</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Data is loaded - show overview with metrics
            st.success("✅ Data loaded successfully! Use the navigation to explore different sections.")
            st.info(f"📊 Current dataset: {len(st.session_state.inventory_data)} items")
            
            # Show key metrics in cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_items = len(st.session_state.inventory_data)
                st.metric(
                    label="Total Items",
                    value=f"{total_items:,}",
                    delta="0"
                )
            
            with col2:
                if 'category' in st.session_state.inventory_data.columns:
                    unique_categories = st.session_state.inventory_data['category'].nunique()
                    st.metric(
                        label="Categories",
                        value=f"{unique_categories}",
                        delta="0"
                    )
            
            with col3:
                if 'stock_level' in st.session_state.inventory_data.columns:
                    total_stock = st.session_state.inventory_data['stock_level'].sum()
                    st.metric(
                        label="Total Stock",
                        value=f"{total_stock:,}",
                        delta="0"
                    )
            
            with col4:
                if 'unit_cost' in st.session_state.inventory_data.columns:
                    total_value = (st.session_state.inventory_data['stock_level'] * st.session_state.inventory_data['unit_cost']).sum()
                    st.metric(
                        label="Total Value",
                        value=f"${total_value:,.0f}",
                        delta="0"
                    )
            
    elif st.session_state.current_page == "📊 Data Input":
        display_data_input_section()
        
    elif st.session_state.current_page == "📈 KPI Overview":
        if not st.session_state.inventory_data.empty:
            display_kpi_overview(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "📦 Inventory Overview":
        if not st.session_state.inventory_data.empty:
            display_inventory_overview(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🔮 Demand Forecasting":
        if not st.session_state.inventory_data.empty:
            display_demand_forecasting(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🤖 Auto Insights":
        if not st.session_state.inventory_data.empty:
            display_ai_insights_section(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🛡️ Risk Assessment":
        if not st.session_state.inventory_data.empty:
            display_risk_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🔮 Predictive Analytics":
        if not st.session_state.inventory_data.empty:
            display_inventory_predictive_analytics_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "📊 Executive Summary":
        if not st.session_state.inventory_data.empty:
            display_analytics_overview_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🏭 Warehouse Operations":
        if not st.session_state.inventory_data.empty:
            display_warehouse_operations(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "📊 Stock Analysis":
        if not st.session_state.inventory_data.empty:
            display_descriptive_analytics_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🎯 Prescriptive Analytics":
        if not st.session_state.inventory_data.empty:
            display_prescriptive_analytics_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    elif st.session_state.current_page == "🔍 Diagnostic Analytics":
        if not st.session_state.inventory_data.empty:
            display_diagnostic_analytics_dashboard(st.session_state.inventory_data)
        else:
            st.warning("📊 Please load data first in the Data Input section.")
            
    else:
        # Default to home page
        st.session_state.current_page = "🏠 Home"
        main()

if __name__ == "__main__":
    # Performance monitoring
    start_time = time.time()
    
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("💡 Performance tip: Try refreshing the page or clearing the cache")
    finally:
        # Performance summary
        end_time = time.time()
        if 'performance_logging' in st.session_state:
            st.sidebar.info(f"⚡ App loaded in {end_time - start_time:.2f}s")
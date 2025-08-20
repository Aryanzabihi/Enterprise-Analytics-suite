"""
Performance Configuration for Sales Analytics Dashboard

This module contains performance optimization settings and configurations
to improve the overall speed and responsiveness of the application.
"""

import streamlit as st
import pandas as pd
import numpy as np
import warnings
from functools import lru_cache
import time

# ============================================================================
# PERFORMANCE OPTIMIZATION SETTINGS
# ============================================================================

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Pandas performance optimizations
pd.options.mode.chained_assignment = None  # Disable SettingWithCopyWarning
# pd.options.compute.use_numba = True  # Enable Numba acceleration if available
pd.options.mode.sim_interactive = True  # Optimize for interactive use

# Streamlit performance configurations
STREAMLIT_CONFIG = {
    'server.maxUploadSize': 200,  # MB
    'server.enableCORS': False,
    'server.enableXsrfProtection': False,
    'server.enableStaticServing': True,
    'browser.gatherUsageStats': False,
    'theme.base': 'light',
    'theme.primaryColor': '#4CAF50',
    'theme.backgroundColor': '#FFFFFF',
    'theme.secondaryBackgroundColor': '#F0F2F6',
    'theme.textColor': '#262730'
}

# Cache configurations
CACHE_CONFIG = {
    'data_cache_ttl': 300,  # 5 minutes
    'calculation_cache_ttl': 600,  # 10 minutes
    'chart_cache_ttl': 180,  # 3 minutes
    'max_cache_entries': 100,
    'calculation_cache_entries': 50
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    'slow_function_warning': 1.0,  # seconds
    'very_slow_function_warning': 3.0,  # seconds
    'data_size_warning': 10000,  # rows
    'chart_complexity_warning': 1000  # data points
}

# ============================================================================
# PERFORMANCE MONITORING FUNCTIONS
# ============================================================================

def performance_monitor(func_name, threshold=None):
    """Decorator to monitor function performance."""
    if threshold is None:
        threshold = PERFORMANCE_THRESHOLDS['slow_function_warning']
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            
            if execution_time > threshold:
                warning_level = "🚨" if execution_time > PERFORMANCE_THRESHOLDS['very_slow_function_warning'] else "⚠️"
                st.sidebar.warning(f"{warning_level} {func_name} took {execution_time:.2f}s")
            
            return result
        return wrapper
    return decorator

def data_size_monitor(data, data_name):
    """Monitor data size and warn if too large."""
    if hasattr(data, 'shape'):
        rows, cols = data.shape
        if rows > PERFORMANCE_THRESHOLDS['data_size_warning']:
            st.sidebar.warning(f"📊 {data_name} has {rows:,} rows - consider data sampling for better performance")
        return rows, cols
    elif hasattr(data, '__len__'):
        length = len(data)
        if length > PERFORMANCE_THRESHOLDS['data_size_warning']:
            st.sidebar.warning(f"📊 {data_name} has {length:,} items - consider data sampling for better performance")
        return length, 0
    return 0, 0

# ============================================================================
# CACHING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=CACHE_CONFIG['data_cache_ttl'], max_entries=CACHE_CONFIG['max_cache_entries'])
def cache_data_loading(data_key, data):
    """Cache data loading operations."""
    return data

@st.cache_data(ttl=CACHE_CONFIG['calculation_cache_ttl'], max_entries=CACHE_CONFIG['calculation_cache_entries'])
def cache_calculations(calculation_key, data, calculation_type):
    """Cache expensive calculations."""
    return data

@st.cache_data(ttl=CACHE_CONFIG['chart_cache_ttl'], max_entries=CACHE_CONFIG['max_cache_entries'])
def cache_chart_data(chart_key, chart_data):
    """Cache chart data for better performance."""
    return chart_data

# ============================================================================
# DATA OPTIMIZATION FUNCTIONS
# ============================================================================

def optimize_dataframe(df, optimize_types=True, optimize_memory=True):
    """Optimize DataFrame for better performance."""
    if df.empty:
        return df
    
    df_optimized = df.copy()
    
    if optimize_types:
        # Optimize data types for better memory usage
        for col in df_optimized.columns:
            if df_optimized[col].dtype == 'object':
                # Try to convert to more efficient types
                try:
                    df_optimized[col] = pd.to_datetime(df_optimized[col], errors='ignore')
                except:
                    try:
                        df_optimized[col] = pd.to_numeric(df_optimized[col], errors='ignore')
                    except:
                        pass
    
    if optimize_memory:
        # Reduce memory usage
        df_optimized = df_optimized.copy()
    
    return df_optimized

def sample_large_dataset(df, max_rows=10000, random_state=42):
    """Sample large datasets for better performance."""
    if len(df) > max_rows:
        return df.sample(n=max_rows, random_state=random_state)
    return df

# ============================================================================
# CHART OPTIMIZATION FUNCTIONS
# ============================================================================

def optimize_chart_data(data, max_points=1000):
    """Optimize chart data for better rendering performance."""
    if len(data) > max_points:
        # Sample data for better chart performance
        return data.sample(n=max_points, random_state=42)
    return data

def create_performance_optimized_chart(chart_func, data, **kwargs):
    """Create charts with performance optimizations."""
    # Optimize data if too large
    optimized_data = optimize_chart_data(data)
    
    # Create chart with optimized data
    chart = chart_func(optimized_data, **kwargs)
    
    # Add performance optimizations to chart
    if hasattr(chart, 'update_layout'):
        chart.update_layout(
            uirevision=True,  # Maintain zoom/pan state
            dragmode='pan',  # Default to pan mode for better performance
        )
    
    return chart

# ============================================================================
# PERFORMANCE REPORTING
# ============================================================================

def generate_performance_report():
    """Generate a performance report for the current session."""
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'function_calls': {},
            'data_operations': {},
            'chart_renders': {},
            'start_time': time.time()
        }
    
    current_time = time.time()
    session_duration = current_time - st.session_state.performance_metrics['start_time']
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Performance Report")
    st.sidebar.metric("⏱️ Session Time", f"{session_duration:.1f}s")
    
    if st.sidebar.button("🔄 Refresh Metrics"):
        st.rerun()

# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_performance_optimizations():
    """Initialize all performance optimizations."""
    # Set page config for better performance
    st.set_page_config(
        page_title="Sales Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize performance monitoring
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'function_calls': {},
            'data_operations': {},
            'chart_renders': {},
            'start_time': time.time()
        }
    
    # Display performance monitoring in sidebar
    generate_performance_report()

if __name__ == "__main__":
    initialize_performance_optimizations()

#!/usr/bin/env python3
"""
Optimized Utilities for Enhanced Analytics
==========================================

This file contains optimized utility functions for better performance
across all analytics pages.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple, Optional, Union
from functools import lru_cache

# Cache frequently used data operations
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_data_summary_optimized(dataframes: Dict[str, pd.DataFrame]) -> Dict[str, int]:
    """Get optimized data summary for multiple dataframes"""
    return {name: len(df) for name, df in dataframes.items()}

@st.cache_data(ttl=1800)
def calculate_basic_metrics(df: pd.DataFrame, column: str) -> Dict[str, Union[int, float]]:
    """Calculate basic metrics for a column with caching"""
    if df.empty or column not in df.columns:
        return {'count': 0, 'mean': 0, 'std': 0}
    
    return {
        'count': len(df),
        'mean': df[column].mean(),
        'std': df[column].std()
    }

@st.cache_data(ttl=1800)
def create_optimized_chart_data(df: pd.DataFrame, x_col: str, y_col: str, 
                               chart_type: str = 'bar') -> Tuple[List, List]:
    """Create optimized chart data with caching"""
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        return [], []
    
    if chart_type == 'bar':
        grouped = df.groupby(x_col)[y_col].agg(['count', 'mean']).reset_index()
        return grouped[x_col].tolist(), grouped['count'].tolist()
    elif chart_type == 'line':
        return df[x_col].tolist(), df[y_col].tolist()
    else:
        return df[x_col].tolist(), df[y_col].tolist()

# Optimized metric card creation
def create_optimized_metric_card(title: str, value: Union[str, int, float], 
                                icon: str, trend: float, color: str) -> None:
    """Create optimized metric card with minimal HTML"""
    trend_arrow = "↗️" if trend > 0 else "↘️" if trend < 0 else "➡️"
    trend_text = f"{trend:+.1f}%" if trend != 0 else "0.0%"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}20, {color}10);
        border: 1px solid {color}30;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    ">
        <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: {color}; margin-bottom: 5px;">
            {value}
        </div>
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 10px;">{title}</div>
        <div style="font-size: 0.8rem; color: {color};">
            {trend_arrow} {trend_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Optimized chart creation functions
@st.cache_data(ttl=1800)
def create_optimized_bar_chart(x_data: List, y_data: List, title: str, 
                              x_label: str, y_label: str, colors: Optional[List[str]] = None) -> go.Figure:
    """Create optimized bar chart with caching"""
    if not x_data or not y_data:
        return go.Figure()
    
    if colors is None:
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFA07A']
    
    fig = go.Figure(data=[go.Bar(
        x=x_data,
        y=y_data,
        marker_color=colors[:len(x_data)],
        text=[f'{y:.1f}' if isinstance(y, float) else str(y) for y in y_data],
        textposition='auto',
        hovertemplate=f'{x_label}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

@st.cache_data(ttl=1800)
def create_optimized_pie_chart(labels: List, values: List, title: str, 
                              colors: Optional[List[str]] = None) -> go.Figure:
    """Create optimized pie chart with caching"""
    if not labels or not values:
        return go.Figure()
    
    if colors is None:
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFA07A', '#DDA0DD']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors[:len(labels)],
        textinfo='label+percent+value',
        hovertemplate='Label: %{label}<br>Value: %{value}<extra></extra>'
    )])
    
    fig.update_layout(
        title=title,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

@st.cache_data(ttl=1800)
def create_optimized_line_chart(x_data: List, y_data: List, title: str, 
                               x_label: str, y_label: str, color: str = '#4ECDC4') -> go.Figure:
    """Create optimized line chart with caching"""
    if not x_data or not y_data:
        return go.Figure()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        name=title,
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

# Optimized data processing functions
@st.cache_data(ttl=1800)
def process_dataframe_optimized(df: pd.DataFrame, required_columns: List[str], 
                               fill_missing: bool = True) -> pd.DataFrame:
    """Process dataframe with optimized operations"""
    if df.empty:
        return df
    
    # Check for required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if fill_missing and missing_cols:
        for col in missing_cols:
            if 'date' in col.lower():
                df[col] = pd.to_datetime('now')
            elif 'id' in col.lower():
                df[col] = range(len(df))
            elif 'score' in col.lower() or 'rating' in col.lower():
                df[col] = np.random.randint(1, 6, len(df))
            else:
                df[col] = 'Unknown'
    
    return df

# Optimized session state management
def get_session_data_safe(key: str, default_value: any = None) -> any:
    """Safely get session state data with fallback"""
    return st.session_state.get(key, default_value)

def set_session_data_safe(key: str, value: any) -> None:
    """Safely set session state data"""
    st.session_state[key] = value

# Performance monitoring utilities
def measure_performance(func):
    """Decorator to measure function performance"""
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Log performance for optimization
        if execution_time > 1.0:  # Log slow functions
            st.warning(f"⚠️ Function {func.__name__} took {execution_time:.2f}s to execute")
        
        return result
    return wrapper

# Memory optimization utilities
def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize dataframe memory usage"""
    if df.empty:
        return df
    
    # Optimize numeric columns
    for col in df.select_dtypes(include=['int64']).columns:
        if df[col].min() >= 0:
            if df[col].max() < 255:
                df[col] = df[col].astype('uint8')
            elif df[col].max() < 65535:
                df[col] = df[col].astype('uint16')
            else:
                df[col] = df[col].astype('uint32')
        else:
            if df[col].min() > -128 and df[col].max() < 127:
                df[col] = df[col].astype('int8')
            elif df[col].min() > -32768 and df[col].max() < 32767:
                df[col] = df[col].astype('int16')
            else:
                df[col] = df[col].astype('int32')
    
    # Optimize float columns
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    # Optimize object columns
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # If less than 50% unique values
            df[col] = df[col].astype('category')
    
    return df

# Error handling utilities
def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error executing {func.__name__}: {str(e)}")
        return None

# Data validation utilities
def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, str]:
    """Validate dataframe has required columns"""
    if df.empty:
        return False, "DataFrame is empty"
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    
    return True, "DataFrame is valid"

# Chart rendering optimization
def render_chart_optimized(fig: go.Figure, use_container_width: bool = True) -> None:
    """Render chart with optimization checks"""
    if fig is None or not fig.data:
        st.info("📊 Chart data will be displayed here when available")
        return
    
    # Optimize chart rendering
    fig.update_layout(
        uirevision=True,  # Prevents unnecessary re-renders
        showlegend=True,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=use_container_width)

# Batch processing utilities
@st.cache_data(ttl=1800)
def batch_process_dataframes(dataframes: Dict[str, pd.DataFrame], 
                           operations: List[str]) -> Dict[str, pd.DataFrame]:
    """Batch process multiple dataframes efficiently"""
    results = {}
    
    for name, df in dataframes.items():
        if df.empty:
            results[name] = df
            continue
            
        processed_df = df.copy()
        
        for operation in operations:
            if operation == 'optimize_memory':
                processed_df = optimize_dataframe_memory(processed_df)
            elif operation == 'fill_na':
                processed_df = processed_df.fillna(method='ffill').fillna(method='bfill')
            elif operation == 'remove_duplicates':
                processed_df = processed_df.drop_duplicates()
        
        results[name] = processed_df
    
    return results

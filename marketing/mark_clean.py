import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import io
import base64
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Performance optimizations
import warnings
warnings.filterwarnings('ignore')

# Performance configuration
import os
os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '200'
os.environ['STREAMLIT_SERVER_ENABLE_STATIC_SERVING'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'

# Set Plotly template and optimize rendering
pio.templates.default = "plotly_white"
pio.renderers.default = "browser"

# Optimize pandas performance
pd.options.mode.chained_assignment = None

# Global constants for performance
CONTINUOUS_COLOR_SCALE = "Turbo"
CATEGORICAL_COLOR_SEQUENCE = px.colors.qualitative.Pastel

# Cache frequently used data
@st.cache_data(ttl=3600, max_entries=100)
def get_cached_data():
    """Cache frequently accessed data for performance"""
    return {}

# Performance: Optimize data processing functions
@st.cache_data(ttl=1800)
def optimize_dataframe(df):
    """Optimize DataFrame memory usage and performance"""
    if df.empty:
        return df
    
    # Convert object columns to category if they have low cardinality
    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')
    
    # Convert numeric columns to appropriate dtypes
    for col in df.select_dtypes(include=['int64']):
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
    
    return df

@st.cache_data(ttl=1800)
def fast_groupby_agg(df, group_cols, agg_dict):
    """Fast groupby aggregation with caching"""
    return df.groupby(group_cols).agg(agg_dict).reset_index()

# Performance monitoring
import time
@st.cache_data(ttl=3600)
def performance_monitor(func_name):
    """Monitor function performance with caching"""
    start_time = time.time()
    return lambda: time.time() - start_time

def log_performance(func_name, execution_time):
    """Log performance metrics"""
    if execution_time > 1.0:  # Log slow operations
        st.sidebar.info(f"⏱️ {func_name}: {execution_time:.2f}s")

# Import marketing metric calculation functions
from marketing_metrics_calculator import *

@st.cache_data(ttl=3600)
def apply_common_layout(fig):
    """Apply common layout settings to Plotly figures with caching for performance"""
    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=50, b=50),
        height=500
    )
    return fig

def display_dataframe_with_index_1(df, **kwargs):
    """Display dataframe with index starting from 1"""
    if not df.empty:
        df_display = df.reset_index(drop=True)
        df_display.index = df_display.index + 1
        return st.dataframe(df_display, **kwargs)
    else:
        return st.dataframe(df, **kwargs)

@st.cache_data(ttl=3600)
def create_template_for_download():
    """Create an Excel template with all required marketing data schema and make it downloadable"""
    
    # Pre-define column schemas for performance
    COLUMN_SCHEMAS = {
        'campaigns': ['campaign_id', 'campaign_name', 'start_date', 'end_date', 'budget', 
                     'channel', 'campaign_type', 'target_audience', 'status', 'objective'],
        'customers': ['customer_id', 'customer_name', 'email', 'phone', 'age', 'gender', 
                     'location', 'acquisition_source', 'acquisition_date', 'customer_segment',
                     'lifetime_value', 'last_purchase_date', 'total_purchases', 'status'],
        'website_traffic': ['session_id', 'customer_id', 'visit_date', 'page_url', 'time_on_page',
                           'bounce_rate', 'traffic_source', 'device_type', 'conversion_flag'],
        'social_media': ['post_id', 'platform', 'post_date', 'content_type', 'impressions',
                        'clicks', 'likes', 'shares', 'comments', 'reach', 'engagement_rate'],
        'email_campaigns': ['email_id', 'campaign_id', 'send_date', 'subject_line', 'recipients',
                           'opens', 'clicks', 'unsubscribes', 'bounces', 'conversions'],
        'content_marketing': ['content_id', 'content_type', 'publish_date', 'title', 'views',
                             'time_on_page', 'shares', 'comments', 'leads_generated', 'conversions'],
        'leads': ['lead_id', 'lead_name', 'email', 'company', 'source', 'created_date',
                 'status', 'assigned_to', 'value', 'conversion_date'],
        'conversions': ['conversion_id', 'customer_id', 'campaign_id', 'conversion_date',
                       'conversion_type', 'revenue', 'attribution_source', 'touchpoint_count']
    }
    
    # Create DataFrames efficiently
    templates = {name: pd.DataFrame(columns=cols) for name, cols in COLUMN_SCHEMAS.items()}
    
    # Create Excel file in memory with optimized writing
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write all templates efficiently
        for name, df in templates.items():
            df.to_excel(writer, sheet_name=name.replace('_', ' ').title(), index=False)
        
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
        
        # Apply formatting to each sheet
        for sheet_name in workbook.sheet_names:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_row(0, 20, header_format)
            worksheet.set_column('A:Z', 15)
    
    output.seek(0)
    return output

def show_home():
    """Display the home page with performance optimizations"""
    st.markdown("## 🏠 Welcome to Marketing Analytics Dashboard")
    st.markdown("This is a high-performance marketing analytics platform with advanced insights and predictive capabilities.")
    
    # Performance metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Performance", "Optimized", "Fast Loading")
    with col2:
        st.metric("⚡ Speed", "Enhanced", "Cached Operations")
    with col3:
        st.metric("🎯 Analytics", "Advanced", "AI-Powered")

def show_data_input():
    """Display data input page with performance optimizations"""
    st.markdown("## 📝 Data Input")
    
    # Performance: Cache template creation
    template = create_template_for_download()
    
    st.download_button(
        label="📥 Download Excel Template",
        data=template.getvalue(),
        file_name="marketing_data_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def main():
    # Performance optimizations
    st.set_page_config(
        page_title="Marketing Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Performance: Cache CSS to avoid re-rendering
    @st.cache_data(ttl=3600)
    def get_css():
        return """
        <style>
        /* Modern SaaS Dashboard Styling - Optimized for Performance */
        
        /* Main background gradient */
        .main .block-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
            max-width: 100%;
        }
        
        /* Sidebar styling - compact */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
            padding: 20px 12px;
            width: 250px;
            min-width: 250px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        /* Optimize sidebar width */
        .css-1lcbmhc {
            width: 250px;
            min-width: 250px;
        }
        
        /* Main content area - expanded width */
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
            width: 100%;
        }
        
        /* Expand main content width */
        .main {
            max-width: 100%;
            padding-left: 0;
            padding-right: 0;
        }
        
        /* Remove default Streamlit width constraints */
        .block-container {
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Expand chart containers */
        .chart-container {
            width: 100%;
            max-width: none;
        }
        
        /* Make plots wider */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Expand dataframe width */
        .dataframe {
            width: 100% !important;
            max-width: none;
        }
        
        /* Force full width for all content */
        .element-container {
            width: 100% !important;
            max-width: none !important;
        }
        
        /* Ensure plots use full width */
        .plotly-graph-div {
            width: 100% !important;
            max-width: none !important;
            height: auto !important;
        }
        
        /* Optimize chart height for wide layout */
        .js-plotly-plot {
            height: 500px !important;
        }
        
        /* Optimize column layouts for wider space */
        .row-widget.stHorizontal {
            width: 100%;
        }
        
        /* Remove any remaining width constraints */
        .stApp > div:first-child {
            max-width: 100%;
        }
        
        /* Ensure all Streamlit elements use full width */
        .stApp {
            max-width: 100%;
        }
        
        /* Optimize for wide screens */
        .stHorizontal {
            width: 100%;
        }
        
        /* Optimize for mobile */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 0.5rem;
            }
            
            .css-1d391kg {
                width: 200px;
                min-width: 200px;
            }
            
            .css-1lcbmhc {
                width: 200px;
                min-width: 200px;
            }
            
            .main-header h1 {
                font-size: 1.8rem;
            }
            
            .main-header p {
                font-size: 1rem;
            }
        }
        
        /* Marketing-specific styling */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .metric-card h2 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        
        .metric-card p {
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .insight-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .insight-card h3 {
            margin: 0 0 10px 0;
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .insight-card p {
            margin: 0;
            line-height: 1.5;
            opacity: 0.9;
        }
        
        .chart-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .chart-container h3 {
            margin: 0 0 15px 0;
            color: #333;
            font-size: 1.3rem;
            font-weight: 600;
        }
        
        .formula-box {
            background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
            padding: 0.5rem;
            border-left: 4px solid #2E86AB;
            margin: 0.5rem 0;
            border-radius: 0.25rem;
        }
        
        .summary-dashboard {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            color: white;
            text-align: center;
        }
        </style>
        """
    
    # Load cached CSS for performance
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # Modern header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">📊 Marketing Analytics Dashboard</h1>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">High-Performance Marketing Analytics & Insights Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance: Initialize session state efficiently
    @st.cache_data(ttl=3600)
    def initialize_session_state():
        """Initialize session state with empty DataFrames for performance"""
        return {
            'campaigns_data': pd.DataFrame(),
            'customers_data': pd.DataFrame(),
            'website_traffic_data': pd.DataFrame(),
            'social_media_data': pd.DataFrame(),
            'email_campaigns_data': pd.DataFrame(),
            'content_marketing_data': pd.DataFrame(),
            'leads_data': pd.DataFrame(),
            'conversions_data': pd.DataFrame()
        }
    
    # Initialize session state efficiently
    if 'campaigns_data' not in st.session_state:
        initial_data = initialize_session_state()
        for key, value in initial_data.items():
            st.session_state[key] = value
    
    # Sidebar navigation for main sections
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
        
        # Main navigation buttons
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = "🏠 Home"
        
        if st.button("📝 Data Input", key="nav_data_input", use_container_width=True):
            st.session_state.current_page = "📝 Data Input"
        
        # Performance monitoring section
        st.markdown("---")
        st.markdown("""
        <div style="padding: 12px 0; text-align: center;">
            <h4 style="color: #4CAF50; margin-bottom: 10px; font-size: 0.9rem;">⚡ Performance</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance metrics
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = {
                'total_pages_loaded': 0,
                'avg_load_time': 0.0,
                'cache_hits': 0
            }
        
        # Display performance summary
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Pages", st.session_state.performance_metrics['total_pages_loaded'])
        with col2:
            st.metric("⚡ Avg Time", f"{st.session_state.performance_metrics['avg_load_time']:.2f}s")
        
        # Developer attribution at the bottom of sidebar
        st.markdown("---")
        st.markdown("""
        <div style="padding: 12px 0; text-align: center;">
            <p style="color: #95a5a6; font-size: 0.75rem; margin: 0; line-height: 1.3;">
                Developed by <strong style="color: #3498db;">Aryan Zabihi</strong><br>
                <a href="https://github.com/Aryanzabihi" target="_blank" style="color: #3498db; text-decoration: none;">GitHub</a> • 
                <a href="https://www.linkedin.com/in/aryanzabihi/" target="_blank" style="color: #3498db; text-decoration: none;">LinkedIn</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize current page if not set
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Home"
        
        page = st.session_state.current_page
    
    # Performance: Main content area with lazy loading and monitoring
    @st.cache_data(ttl=1800)
    def get_page_function(page_name):
        """Cache page function mapping for performance"""
        page_functions = {
            "🏠 Home": show_home,
            "📝 Data Input": show_data_input
        }
        return page_functions.get(page_name, show_home)
    
    # Execute page with performance monitoring
    if page in ["🏠 Home", "📝 Data Input"]:
        
        page_func = get_page_function(page)
        start_time = time.time()
        
        try:
            page_func()
            
        except Exception as e:
            st.error(f"Error loading {page}: {str(e)}")
        finally:
            execution_time = time.time() - start_time
            
            # Update performance metrics
            st.session_state.performance_metrics['total_pages_loaded'] += 1
            current_avg = st.session_state.performance_metrics['avg_load_time']
            total_pages = st.session_state.performance_metrics['total_pages_loaded']
            new_avg = (current_avg * (total_pages - 1) + execution_time) / total_pages
            st.session_state.performance_metrics['avg_load_time'] = new_avg
            
            if execution_time > 0.5:  # Log slow page loads
                log_performance(f"Page Load: {page}", execution_time)

if __name__ == "__main__":
    main()

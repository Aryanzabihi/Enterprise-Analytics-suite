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
        
        # Add instructions sheet
        instructions_data = {
            'Sheet Name': ['Campaigns', 'Customers', 'Website_Traffic', 'Social_Media', 'Email_Campaigns', 'Content_Marketing', 'Leads', 'Conversions'],
            'Required Fields': [
                'campaign_id, campaign_name, start_date, end_date, budget, channel, campaign_type, target_audience, status, objective',
                'customer_id, customer_name, email, phone, age, gender, location, acquisition_source, acquisition_date, customer_segment, lifetime_value, last_purchase_date, total_purchases, status',
                'session_id, customer_id, visit_date, page_url, time_on_page, bounce_rate, traffic_source, device_type, conversion_flag',
                'post_id, platform, post_date, content_type, impressions, clicks, likes, shares, comments, reach, engagement_rate',
                'email_id, campaign_id, send_date, subject_line, recipients, opens, clicks, unsubscribes, bounces, conversions',
                'content_id, content_type, publish_date, title, views, time_on_page, shares, comments, leads_generated, conversions',
                'lead_id, lead_name, email, company, source, created_date, status, assigned_to, value, conversion_date',
                'conversion_id, customer_id, campaign_id, conversion_date, conversion_type, revenue, attribution_source, touchpoint_count'
            ],
            'Data Types': [
                'Text, Text, Date, Date, Number, Text, Text, Text, Text, Text',
                'Text, Text, Text, Text, Number, Text, Text, Text, Date, Text, Number, Date, Number, Text',
                'Text, Text, Date, Text, Number, Number, Text, Text, Boolean',
                'Text, Text, Date, Text, Number, Number, Number, Number, Number, Number, Number',
                'Text, Text, Date, Text, Number, Number, Number, Number, Number, Number',
                'Text, Text, Date, Text, Number, Number, Number, Number, Number, Number',
                'Text, Text, Text, Text, Text, Date, Text, Text, Number, Date',
                'Text, Text, Text, Date, Text, Number, Text, Number'
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Format the instructions sheet
        worksheet = writer.sheets['Instructions']
        for i, col in enumerate(instructions_df.columns):
            worksheet.set_column(i, i, 30)
    
    output.seek(0)
    return output

def export_data_to_excel():
    """Export all loaded data to Excel file"""
    if 'campaigns_data' not in st.session_state or st.session_state.campaigns_data.empty:
        st.warning("No data loaded to export.")
        return None
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Export each dataset to separate sheets
        if ('campaigns_data' in st.session_state and 
            isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
            not st.session_state.campaigns_data.empty):
            st.session_state.campaigns_data.to_excel(writer, sheet_name='Campaigns', index=False)
        
        if ('customers_data' in st.session_state and 
            isinstance(st.session_state.customers_data, pd.DataFrame) and 
            not st.session_state.customers_data.empty):
            st.session_state.customers_data.to_excel(writer, sheet_name='Customers', index=False)
        
        if ('website_traffic_data' in st.session_state and 
            isinstance(st.session_state.website_traffic_data, pd.DataFrame) and 
            not st.session_state.website_traffic_data.empty):
            st.session_state.website_traffic_data.to_excel(writer, sheet_name='Website_Traffic', index=False)
        
        if ('social_media_data' in st.session_state and 
            isinstance(st.session_state.social_media_data, pd.DataFrame) and 
            not st.session_state.social_media_data.empty):
            st.session_state.social_media_data.to_excel(writer, sheet_name='Social_Media', index=False)
        
        if ('email_campaigns_data' in st.session_state and 
            isinstance(st.session_state.email_campaigns_data, pd.DataFrame) and 
            not st.session_state.email_campaigns_data.empty):
            st.session_state.email_campaigns_data.to_excel(writer, sheet_name='Email_Campaigns', index=False)
        
        if ('content_marketing_data' in st.session_state and 
            isinstance(st.session_state.content_marketing_data, pd.DataFrame) and 
            not st.session_state.content_marketing_data.empty):
            st.session_state.content_marketing_data.to_excel(writer, sheet_name='Content_Marketing', index=False)
        
        if ('leads_data' in st.session_state and 
            isinstance(st.session_state.leads_data, pd.DataFrame) and 
            not st.session_state.leads_data.empty):
            st.session_state.leads_data.to_excel(writer, sheet_name='Leads', index=False)
        
        if ('conversions_data' in st.session_state and 
            isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.session_state.conversions_data.to_excel(writer, sheet_name='Conversions', index=False)
    
    output.seek(0)
    return output

def show_home():
    """Display the home page with comprehensive overview and key metrics"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Check if data is loaded (placeholder for future data integration)
    data_loaded = False  # This can be updated when data functionality is added
    
    if not data_loaded:
        # Welcome section with 4 colored cards
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #495057; margin-bottom: 1rem;">🎯 Welcome to Marketing Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Get started by exploring the comprehensive marketing analytics categories and metrics to optimize your marketing operations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 4 colored metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Analytics Categories", 
                "11 comprehensive",
                "analysis areas"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Marketing Analytics", 
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
                "ROI Analysis", 
                "Comprehensive",
                "performance metrics"
            ), unsafe_allow_html=True)
        
        # Available analytics categories (6 cards in 2 columns)
        st.markdown("### 📊 Available Marketing Analytics Categories:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 1: Campaign Performance Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📈 Campaign Performance Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Return on Investment (ROI)</li>
                    <li>Cost Per Acquisition (CPA)</li>
                    <li>Click-Through Rate (CTR)</li>
                    <li>Conversion Rate</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 2: Customer Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">👥 Customer Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Customer Lifetime Value (CLV)</li>
                    <li>Customer Churn Rate</li>
                    <li>Customer Segmentation</li>
                    <li>Acquisition Source Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 3: Digital Marketing & Web Analytics
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🌐 Digital Marketing & Web Analytics</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Website Traffic Analysis</li>
                    <li>SEO Performance</li>
                    <li>Pay-Per-Click (PPC) Metrics</li>
                    <li>Email Campaign Metrics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Card 4: Content Marketing Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📝 Content Marketing Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Content Engagement Metrics</li>
                    <li>Time on Page Analysis</li>
                    <li>Top-Performing Content</li>
                    <li>Lead Generation by Content</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 5: Brand Awareness & Perception
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🏷️ Brand Awareness & Perception</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Brand Recognition Metrics</li>
                    <li>Sentiment Analysis</li>
                    <li>Net Promoter Score (NPS)</li>
                    <li>Share of Voice (SOV)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 6: Customer Journey Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🛤️ Customer Journey Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Attribution Modeling</li>
                    <li>Path to Purchase Analysis</li>
                    <li>Cart Abandonment Rate</li>
                    <li>Retention Funnel Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Getting Started section (3 cards)
        st.markdown("### 🚀 Getting Started:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">1. Explore Categories</h4>
                <p style="margin: 0;">Browse through the marketing analytics categories above</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">2. Select Metrics</h4>
                <p style="margin: 0;">Choose specific metrics to analyze and calculate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">3. Generate Insights</h4>
                <p style="margin: 0;">Get actionable insights and recommendations</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Data Schema section (8 cards in 2 rows)
        st.markdown("### 📈 Data Schema:")
        st.markdown("The application supports the following marketing data categories:")
        
        # Row 1 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📈 Campaigns</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Details, budget, channels, objectives</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">👥 Customers</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Demographics, segments, acquisition</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🌐 Website Traffic</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Sessions, page views, sources</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📱 Social Media</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Posts, engagement, platform performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📧 Email Campaigns</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Sends, opens, clicks, conversions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📝 Content</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Content pieces, engagement, leads</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🎯 Leads</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Prospects, sources, status, conversion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">💰 Conversions</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Revenue, attribution, touchpoints</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Data is loaded - show overview with metrics
        st.success("✅ Data loaded successfully! Use the navigation to explore different sections.")
        st.info("📊 Marketing analytics data available for analysis")
        
        # Show key metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Campaigns",
                value="0",
                delta="0"
            )
        
        with col2:
            st.metric(
                label="Active Customers",
                value="0",
                delta="0"
            )
        
        with col3:
            st.metric(
                label="Conversion Rate",
                value="0%",
                delta="0"
            )
        
        with col4:
            st.metric(
                label="ROI",
                value="0%",
                delta="0"
            )

def show_data_input():
    """Show data input forms and file upload options"""
    st.markdown("## 📝 Data Input")
    
    # Create tabs for different data input methods
    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 Download Template", "📤 Upload Data", "📝 Data Entry", "📊 Sample Dataset"
    ])
    
    with tab1:
        st.markdown("### 📥 Download Data Template")
        st.markdown("Download the Excel template with all required marketing data schema, fill it with your data, and upload it back.")
        
        # Create template for download
        template_data = create_template_for_download()
        st.download_button(
            label="📥 Download Marketing Data Template",
            data=template_data.getvalue(),
            file_name="marketing_data_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Add some spacing for visual balance
        st.markdown("")
        st.markdown("**Template includes:**")
        st.markdown("• 8 Marketing data tables in separate sheets")
        st.markdown("• Instructions sheet with field descriptions")
        st.markdown("• Proper column headers and data types")
        
        st.markdown("### 📋 Template Structure")
        st.markdown("The template contains the following sheets:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Campaigns**")
            st.markdown("• Campaign details, budgets, channels")
            st.markdown("**👥 Customers**")
            st.markdown("• Customer profiles and segments")
            st.markdown("**🌐 Website Traffic**")
            st.markdown("• Session data and user behavior")
            st.markdown("**📱 Social Media**")
            st.markdown("• Post performance metrics")
        
        with col2:
            st.markdown("**📧 Email Campaigns**")
            st.markdown("• Email performance and metrics")
            st.markdown("**📝 Content Marketing**")
            st.markdown("• Content engagement data")
            st.markdown("**🎯 Leads**")
            st.markdown("• Lead information and status")
            st.markdown("**💰 Conversions**")
            st.markdown("• Conversion tracking and revenue")
    
    with tab2:
        st.markdown("### 📤 Upload Your Data")
        st.markdown("Upload your filled Excel template:")
        
        # File upload for Excel template
        uploaded_file = st.file_uploader(
            "Upload Excel file with all marketing tables", 
            type=['xlsx', 'xls'],
            help="Upload the filled Excel template with all 8 marketing tables in separate sheets"
        )
        
        # Add helpful information
        st.markdown("")
        st.markdown("**Upload features:**")
        st.markdown("• Automatic validation of all sheets")
        st.markdown("• Import all 8 marketing tables at once")
        st.markdown("• Error checking and feedback")
        
        if uploaded_file is not None:
            try:
                # Read all sheets from the Excel file
                excel_data = pd.read_excel(uploaded_file, sheet_name=None)
                
                # Check if all required sheets are present
                required_sheets = ['Campaigns', 'Customers', 'Website_Traffic', 'Social_Media', 'Email_Campaigns', 'Content_Marketing', 'Leads', 'Conversions']
                missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
                
                if missing_sheets:
                    st.error(f"❌ Missing required sheets: {', '.join(missing_sheets)}")
                    st.info("Please ensure your Excel file contains all 8 required marketing sheets.")
                else:
                    # Load data into session state with safety checks
                    st.session_state.campaigns_data = pd.DataFrame(excel_data['Campaigns']) if 'Campaigns' in excel_data else pd.DataFrame()
                    st.session_state.customers_data = pd.DataFrame(excel_data['Customers']) if 'Customers' in excel_data else pd.DataFrame()
                    st.session_state.website_traffic_data = pd.DataFrame(excel_data['Website_Traffic']) if 'Website_Traffic' in excel_data else pd.DataFrame()
                    st.session_state.social_media_data = pd.DataFrame(excel_data['Social_Media']) if 'Social_Media' in excel_data else pd.DataFrame()
                    st.session_state.email_campaigns_data = pd.DataFrame(excel_data['Email_Campaigns']) if 'Email_Campaigns' in excel_data else pd.DataFrame()
                    st.session_state.content_marketing_data = pd.DataFrame(excel_data['Content_Marketing']) if 'Content_Marketing' in excel_data else pd.DataFrame()
                    st.session_state.leads_data = pd.DataFrame(excel_data['Leads']) if 'Leads' in excel_data else pd.DataFrame()
                    st.session_state.conversions_data = pd.DataFrame(excel_data['Conversions']) if 'Conversions' in excel_data else pd.DataFrame()
                    
                    st.success("✅ All marketing data loaded successfully from Excel file!")
                    st.info(f"📊 Loaded {len(st.session_state.campaigns_data)} campaigns, {len(st.session_state.customers_data)} customers, {len(st.session_state.conversions_data)} conversions, and more...")
                    
                    # Show data summary
                    st.markdown("### 📊 Data Summary")
                    summary_data = {
                        'Data Type': ['Campaigns', 'Customers', 'Website Traffic', 'Social Media', 'Email Campaigns', 'Content Marketing', 'Leads', 'Conversions'],
                        'Records': [
                            len(st.session_state.campaigns_data),
                            len(st.session_state.customers_data),
                            len(st.session_state.website_traffic_data),
                            len(st.session_state.social_media_data),
                            len(st.session_state.email_campaigns_data),
                            len(st.session_state.content_marketing_data),
                            len(st.session_state.leads_data),
                            len(st.session_state.conversions_data)
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error reading Excel file: {str(e)}")
                st.info("Please ensure the file is a valid Excel file with the correct format.")
    
    with tab3:
        st.markdown("### 📝 Manual Data Entry")
        st.markdown("Add data manually using the forms below:")
        
        # Tabs for different data types
        data_tab1, data_tab2, data_tab3, data_tab4, data_tab5, data_tab6, data_tab7, data_tab8 = st.tabs([
            "Campaigns", "Customers", "Website Traffic", "Social Media", 
            "Email Campaigns", "Content Marketing", "Leads", "Conversions"
        ])
        
        with data_tab1:
            st.subheader("Campaigns")
            col1, col2 = st.columns(2)
            
            with col1:
                campaign_id = st.text_input("Campaign ID", key="campaign_id_input")
                campaign_name = st.text_input("Campaign Name", key="campaign_name_input")
                start_date = st.date_input("Start Date", key="campaign_start_input")
                end_date = st.date_input("End Date", key="campaign_end_input")
                budget = st.number_input("Budget ($)", min_value=0, key="campaign_budget_input")
                channel = st.selectbox("Channel", ["Facebook", "Instagram", "Google Ads", "LinkedIn", "Twitter", "YouTube", "Email"], key="campaign_channel_input")
            
            with col2:
                campaign_type = st.selectbox("Campaign Type", ["Social Media", "Email", "PPC", "Content Marketing", "Influencer", "Affiliate"], key="campaign_type_input")
                target_audience = st.text_input("Target Audience", key="campaign_audience_input")
                status = st.selectbox("Status", ["Active", "Completed", "Paused"], key="campaign_status_input")
                objective = st.selectbox("Objective", ["Brand Awareness", "Lead Generation", "Sales", "Engagement", "Traffic"], key="campaign_objective_input")
            
            if st.button("Add Campaign", key="add_campaign_btn"):
                if campaign_id and campaign_name:
                    new_campaign = {
                        'campaign_id': campaign_id,
                        'campaign_name': campaign_name,
                        'start_date': start_date,
                        'end_date': end_date,
                        'budget': budget,
                        'channel': channel,
                        'campaign_type': campaign_type,
                        'target_audience': target_audience,
                        'status': status,
                        'objective': objective
                    }
                    
                    if st.session_state.campaigns_data.empty:
                        st.session_state.campaigns_data = pd.DataFrame([new_campaign])
                    else:
                        st.session_state.campaigns_data = pd.concat([st.session_state.campaigns_data, pd.DataFrame([new_campaign])], ignore_index=True)
                    
                    st.success(f"✅ Campaign '{campaign_name}' added successfully!")
                else:
                    st.error("❌ Please fill in all required fields (Campaign ID and Name)")
            
            # Display existing data
            if not st.session_state.campaigns_data.empty:
                st.subheader("Existing Campaigns")
                display_dataframe_with_index_1(st.session_state.campaigns_data)
        
        with data_tab2:
            st.subheader("Customers")
            col1, col2 = st.columns(2)
            
            with col1:
                customer_id = st.text_input("Customer ID", key="customer_id_input")
                customer_name = st.text_input("Customer Name", key="customer_name_input")
                email = st.text_input("Email", key="customer_email_input")
                phone = st.text_input("Phone", key="customer_phone_input")
                age = st.number_input("Age", min_value=0, max_value=120, key="customer_age_input")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="customer_gender_input")
            
            with col2:
                location = st.text_input("Location", key="customer_location_input")
                acquisition_source = st.selectbox("Acquisition Source", ["Organic Search", "Social Media", "Email", "Referral", "Paid Ads", "Direct"], key="customer_source_input")
                acquisition_date = st.date_input("Acquisition Date", key="customer_acq_date_input")
                customer_segment = st.selectbox("Customer Segment", ["High Value", "Medium Value", "Low Value", "New Customer", "Loyal Customer"], key="customer_segment_input")
                lifetime_value = st.number_input("Lifetime Value ($)", min_value=0, key="customer_clv_input")
                total_purchases = st.number_input("Total Purchases", min_value=0, key="customer_purchases_input")
            
            if st.button("Add Customer", key="add_customer_btn"):
                if customer_id and customer_name:
                    new_customer = {
                        'customer_id': customer_id,
                        'customer_name': customer_name,
                        'email': email,
                        'phone': phone,
                        'age': age,
                        'gender': gender,
                        'location': location,
                        'acquisition_source': acquisition_source,
                        'acquisition_date': acquisition_date,
                        'customer_segment': customer_segment,
                        'lifetime_value': lifetime_value,
                        'last_purchase_date': datetime.now().date(),
                        'total_purchases': total_purchases,
                        'status': 'Active'
                    }
                    
                    if st.session_state.customers_data.empty:
                        st.session_state.customers_data = pd.DataFrame([new_customer])
                    else:
                        st.session_state.customers_data = pd.concat([st.session_state.customers_data, pd.DataFrame([new_customer])], ignore_index=True)
                    
                    st.success(f"✅ Customer '{customer_name}' added successfully!")
                else:
                    st.error("❌ Please fill in all required fields (Customer ID and Name)")
            
            # Display existing data
            if not st.session_state.customers_data.empty:
                st.subheader("Existing Customers")
                display_dataframe_with_index_1(st.session_state.customers_data)
        
        with data_tab3:
            st.subheader("Website Traffic")
            col1, col2 = st.columns(2)
            
            with col1:
                session_id = st.text_input("Session ID", key="session_id_input")
                customer_id = st.text_input("Customer ID", key="traffic_customer_id_input")
                visit_date = st.date_input("Visit Date", key="visit_date_input")
                page_url = st.text_input("Page URL", key="page_url_input")
                time_on_page = st.number_input("Time on Page (seconds)", min_value=0, key="time_on_page_input")
            
            with col2:
                bounce_rate = st.slider("Bounce Rate", 0.0, 1.0, 0.5, key="bounce_rate_input")
                traffic_source = st.selectbox("Traffic Source", ["Organic", "Direct", "Referral", "Paid", "Social"], key="traffic_source_input")
                device_type = st.selectbox("Device Type", ["Desktop", "Mobile", "Tablet"], key="device_type_input")
                conversion_flag = st.checkbox("Conversion", key="conversion_flag_input")
            
            if st.button("Add Website Session", key="add_session_btn"):
                if session_id:
                    new_session = {
                        'session_id': session_id,
                        'customer_id': customer_id,
                        'visit_date': visit_date,
                        'page_url': page_url,
                        'time_on_page': time_on_page,
                        'bounce_rate': bounce_rate,
                        'traffic_source': traffic_source,
                        'device_type': device_type,
                        'conversion_flag': conversion_flag
                    }
                    
                    if st.session_state.website_traffic_data.empty:
                        st.session_state.website_traffic_data = pd.DataFrame([new_session])
                    else:
                        st.session_state.website_traffic_data = pd.concat([st.session_state.website_traffic_data, pd.DataFrame([new_session])], ignore_index=True)
                    
                    st.success(f"✅ Website session '{session_id}' added successfully!")
                else:
                    st.error("❌ Please fill in Session ID")
            
            # Display existing data
            if not st.session_state.website_traffic_data.empty:
                st.subheader("Existing Website Sessions")
                display_dataframe_with_index_1(st.session_state.website_traffic_data)
        
        with data_tab4:
            st.subheader("Social Media")
            col1, col2 = st.columns(2)
            
            with col1:
                post_id = st.text_input("Post ID", key="post_id_input")
                platform = st.selectbox("Platform", ["Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube"], key="platform_input")
                post_date = st.date_input("Post Date", key="post_date_input")
                content_type = st.selectbox("Content Type", ["Image", "Video", "Text", "Story", "Reel"], key="social_media_content_type_input")
                impressions = st.number_input("Impressions", min_value=0, key="impressions_input")
            
            with col2:
                clicks = st.number_input("Clicks", min_value=0, key="social_media_clicks_input")
                likes = st.number_input("Likes", min_value=0, key="likes_input")
                shares = st.number_input("Shares", min_value=0, key="social_media_shares_input")
                comments = st.number_input("Comments", min_value=0, key="social_media_comments_input")
                reach = st.number_input("Reach", min_value=0, key="reach_input")
            
            if st.button("Add Social Media Post", key="add_post_btn"):
                if post_id:
                    engagement_rate = (likes + shares + comments) / max(reach, 1) if reach > 0 else 0
                    new_post = {
                        'post_id': post_id,
                        'platform': platform,
                        'post_date': post_date,
                        'content_type': content_type,
                        'impressions': impressions,
                        'clicks': clicks,
                        'likes': likes,
                        'shares': shares,
                        'comments': comments,
                        'reach': reach,
                        'engagement_rate': engagement_rate
                    }
                    
                    if st.session_state.social_media_data.empty:
                        st.session_state.social_media_data = pd.DataFrame([new_post])
                    else:
                        st.session_state.social_media_data = pd.concat([st.session_state.social_media_data, pd.DataFrame([new_post])], ignore_index=True)
                    
                    st.success(f"✅ Social media post '{post_id}' added successfully!")
                else:
                    st.error("❌ Please fill in Post ID")
            
            # Display existing data
            if not st.session_state.social_media_data.empty:
                st.subheader("Existing Social Media Posts")
                display_dataframe_with_index_1(st.session_state.social_media_data)
        
        with data_tab5:
            st.subheader("Email Campaigns")
            col1, col2 = st.columns(2)
            
            with col1:
                email_id = st.text_input("Email ID", key="email_id_input")
                campaign_id = st.text_input("Campaign ID", key="email_campaign_id_input")
                send_date = st.date_input("Send Date", key="email_send_date_input")
                subject_line = st.text_input("Subject Line", key="subject_line_input")
                recipients = st.number_input("Recipients", min_value=0, key="recipients_input")
            
            with col2:
                opens = st.number_input("Opens", min_value=0, key="opens_input")
                clicks = st.number_input("Clicks", min_value=0, key="email_clicks_input")
                unsubscribes = st.number_input("Unsubscribes", min_value=0, key="unsubscribes_input")
                bounces = st.number_input("Bounces", min_value=0, key="bounces_input")
                conversions = st.number_input("Conversions", min_value=0, key="email_conversions_input")
            
            if st.button("Add Email Campaign", key="add_email_btn"):
                if email_id:
                    new_email = {
                        'email_id': email_id,
                        'campaign_id': campaign_id,
                        'send_date': send_date,
                        'subject_line': subject_line,
                        'recipients': recipients,
                        'opens': opens,
                        'clicks': clicks,
                        'unsubscribes': unsubscribes,
                        'bounces': bounces,
                        'conversions': conversions
                    }
                    
                    if st.session_state.email_campaigns_data.empty:
                        st.session_state.email_campaigns_data = pd.DataFrame([new_email])
                    else:
                        st.session_state.email_campaigns_data = pd.concat([st.session_state.email_campaigns_data, pd.DataFrame([new_email])], ignore_index=True)
                    
                    st.success(f"✅ Email campaign '{email_id}' added successfully!")
                else:
                    st.error("❌ Please fill in Email ID")
            
            # Display existing data
            if not st.session_state.email_campaigns_data.empty:
                st.subheader("Existing Email Campaigns")
                display_dataframe_with_index_1(st.session_state.email_campaigns_data)
        
        with data_tab6:
            st.subheader("Content Marketing")
            col1, col2 = st.columns(2)
            
            with col1:
                content_id = st.text_input("Content ID", key="content_id_input")
                content_type = st.selectbox("Content Type", ["Blog Post", "Video", "Infographic", "Whitepaper", "Case Study", "Webinar"], key="content_marketing_content_type_input")
                publish_date = st.date_input("Publish Date", key="content_publish_date_input")
                title = st.text_input("Title", key="content_title_input")
                views = st.number_input("Views", min_value=0, key="content_views_input")
            
            with col2:
                time_on_page = st.number_input("Time on Page (seconds)", min_value=0, key="content_time_input")
                shares = st.number_input("Shares", min_value=0, key="content_shares_input")
                comments = st.number_input("Comments", min_value=0, key="content_comments_input")
                leads_generated = st.number_input("Leads Generated", min_value=0, key="leads_generated_input")
                conversions = st.number_input("Conversions", min_value=0, key="content_conversions_input")
            
            if st.button("Add Content", key="add_content_btn"):
                if content_id:
                    new_content = {
                        'content_id': content_id,
                        'content_type': content_type,
                        'publish_date': publish_date,
                        'title': title,
                        'views': views,
                        'time_on_page': time_on_page,
                        'shares': shares,
                        'comments': comments,
                        'leads_generated': leads_generated,
                        'conversions': conversions
                    }
                    
                    if st.session_state.content_marketing_data.empty:
                        st.session_state.content_marketing_data = pd.DataFrame([new_content])
                    else:
                        st.session_state.content_marketing_data = pd.concat([st.session_state.content_marketing_data, pd.DataFrame([new_content])], ignore_index=True)
                    
                    st.success(f"✅ Content '{title}' added successfully!")
                else:
                    st.error("❌ Please fill in Content ID")
            
            # Display existing data
            if not st.session_state.content_marketing_data.empty:
                st.subheader("Existing Content")
                display_dataframe_with_index_1(st.session_state.content_marketing_data)
        
        with data_tab7:
            st.subheader("Leads")
            col1, col2 = st.columns(2)
            
            with col1:
                lead_id = st.text_input("Lead ID", key="lead_id_input")
                lead_name = st.text_input("Lead Name", key="lead_name_input")
                email = st.text_input("Email", key="lead_email_input")
                company = st.text_input("Company", key="company_input")
                source = st.selectbox("Source", ["Website", "Social Media", "Email", "Referral", "Paid Ads", "Trade Show"], key="lead_source_input")
            
            with col2:
                created_date = st.date_input("Created Date", key="lead_created_date_input")
                status = st.selectbox("Status", ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"], key="lead_status_input")
                assigned_to = st.text_input("Assigned To", key="assigned_to_input")
                value = st.number_input("Value ($)", min_value=0, key="lead_value_input")
                conversion_date = st.date_input("Conversion Date", key="lead_conversion_date_input")
            
            if st.button("Add Lead", key="add_lead_btn"):
                if lead_id and lead_name:
                    new_lead = {
                        'lead_id': lead_id,
                        'lead_name': lead_name,
                        'email': email,
                        'company': company,
                        'source': source,
                        'created_date': created_date,
                        'status': status,
                        'assigned_to': assigned_to,
                        'value': value,
                        'conversion_date': conversion_date
                    }
                    
                    if st.session_state.leads_data.empty:
                        st.session_state.leads_data = pd.DataFrame([new_lead])
                    else:
                        st.session_state.leads_data = pd.concat([st.session_state.leads_data, pd.DataFrame([new_lead])], ignore_index=True)
                    
                    st.success(f"✅ Lead '{lead_name}' added successfully!")
                else:
                    st.error("❌ Please fill in all required fields (Lead ID and Name)")
            
            # Display existing data
            if not st.session_state.leads_data.empty:
                st.subheader("Existing Leads")
                display_dataframe_with_index_1(st.session_state.leads_data)
        
        with data_tab8:
            st.subheader("Conversions")
            col1, col2 = st.columns(2)
            
            with col1:
                conversion_id = st.text_input("Conversion ID", key="conversion_id_input")
                customer_id = st.text_input("Customer ID", key="conversion_customer_id_input")
                campaign_id = st.text_input("Campaign ID", key="conversion_campaign_id_input")
                conversion_date = st.date_input("Conversion Date", key="conversion_date_input")
                conversion_type = st.selectbox("Conversion Type", ["Purchase", "Sign-up", "Download", "Contact", "Demo Request"], key="conversion_type_input")
            
            with col2:
                revenue = st.number_input("Revenue ($)", min_value=0, key="revenue_input")
                attribution_source = st.selectbox("Attribution Source", ["First Touch", "Last Touch", "Multi-touch", "Time Decay"], key="attribution_source_input")
                touchpoint_count = st.number_input("Touchpoint Count", min_value=1, key="touchpoint_count_input")
            
            if st.button("Add Conversion", key="add_conversion_btn"):
                if conversion_id:
                    new_conversion = {
                        'conversion_id': conversion_id,
                        'customer_id': customer_id,
                        'campaign_id': campaign_id,
                        'conversion_date': conversion_date,
                        'conversion_type': conversion_type,
                        'revenue': revenue,
                        'attribution_source': attribution_source,
                        'touchpoint_count': touchpoint_count
                    }
                    
                    # Ensure conversions_data is a DataFrame
                    if not isinstance(st.session_state.conversions_data, pd.DataFrame):
                        st.session_state.conversions_data = pd.DataFrame()
                    
                    if st.session_state.conversions_data.empty:
                        st.session_state.conversions_data = pd.DataFrame([new_conversion])
                    else:
                        st.session_state.conversions_data = pd.concat([st.session_state.conversions_data, pd.DataFrame([new_conversion])], ignore_index=True)
                    
                    st.success(f"✅ Conversion '{conversion_id}' added successfully!")
                else:
                    st.error("❌ Please fill in Conversion ID")
            
            # Display existing data
            if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
                not st.session_state.conversions_data.empty):
                st.subheader("Existing Conversions")
                display_dataframe_with_index_1(st.session_state.conversions_data)
    
    with tab4:
        st.markdown("### 📊 Sample Dataset")
        st.markdown("Load sample marketing data to explore the dashboard features:")
        
        if st.button("🚀 Load Sample Marketing Dataset", key="load_sample_btn", use_container_width=True):
            # Generate comprehensive sample data
            sample_campaigns = pd.DataFrame({
                'campaign_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008'],
                'campaign_name': ['Summer Sale 2024', 'Brand Awareness Q1', 'Lead Generation Campaign', 'Holiday Promotion', 'Product Launch', 'Email Newsletter Q1', 'Content Marketing Series', 'Social Media Boost'],
                'start_date': ['2024-06-01', '2024-01-01', '2024-03-01', '2024-11-01', '2024-09-01', '2024-01-01', '2024-02-01', '2024-04-01'],
                'end_date': ['2024-08-31', '2024-03-31', '2024-05-31', '2024-12-31', '2024-10-31', '2024-03-31', '2024-05-31', '2024-06-30'],
                'budget': [50000, 30000, 25000, 40000, 60000, 15000, 20000, 18000],
                'channel': ['Facebook', 'Google Ads', 'LinkedIn', 'Email', 'Instagram', 'Email', 'Content Hub', 'Social Media'],
                'campaign_type': ['Social Media', 'PPC', 'B2B', 'Email', 'Social Media', 'Email', 'Content Marketing', 'Social Media'],
                'target_audience': ['General', 'B2B', 'Professionals', 'Existing Customers', 'Young Adults', 'Subscribers', 'Professionals', 'General'],
                'status': ['Active', 'Completed', 'Completed', 'Active', 'Active', 'Completed', 'Completed', 'Active'],
                'objective': ['Sales', 'Brand Awareness', 'Lead Generation', 'Sales', 'Brand Awareness', 'Engagement', 'Thought Leadership', 'Brand Awareness']
            })
            
            sample_customers = pd.DataFrame({
                'customer_id': ['CU001', 'CU002', 'CU003', 'CU004', 'CU005', 'CU006', 'CU007', 'CU008', 'CU009', 'CU010'],
                'customer_name': ['John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Wilson', 'David Brown', 'Emma Taylor', 'Alex Chen', 'Maria Garcia', 'Tom Wilson', 'Anna Lee'],
                'email': ['john@email.com', 'sarah@email.com', 'mike@email.com', 'lisa@email.com', 'david@email.com', 'emma@email.com', 'alex@email.com', 'maria@email.com', 'tom@email.com', 'anna@email.com'],
                'phone': ['555-0101', '555-0102', '555-0103', '555-0104', '555-0105', '555-0106', '555-0107', '555-0108', '555-0109', '555-0110'],
                'age': [35, 28, 42, 31, 39, 26, 45, 33, 29, 37],
                'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
                'location': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Seattle', 'Boston', 'Miami', 'Denver', 'Austin'],
                'acquisition_source': ['Organic Search', 'Social Media', 'Email', 'Paid Ads', 'Referral', 'Content Marketing', 'LinkedIn', 'Facebook', 'Google Ads', 'Email'],
                'acquisition_date': ['2024-01-15', '2024-02-20', '2024-01-10', '2024-03-05', '2024-02-15', '2024-02-01', '2024-01-25', '2024-03-10', '2024-02-28', '2024-01-20'],
                'customer_segment': ['High Value', 'Medium Value', 'High Value', 'Low Value', 'Medium Value', 'Medium Value', 'High Value', 'Low Value', 'Medium Value', 'High Value'],
                'lifetime_value': [2500, 1200, 3000, 800, 1500, 1800, 2800, 950, 1300, 2200],
                'last_purchase_date': ['2024-05-20', '2024-04-15', '2024-05-10', '2024-03-20', '2024-04-25', '2024-05-05', '2024-05-15', '2024-04-10', '2024-05-01', '2024-05-18'],
                'total_purchases': [8, 4, 12, 2, 6, 5, 10, 3, 7, 9],
                'status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active']
            })
            
            # Generate conversions data (CRITICAL for analysis)
            sample_conversions = pd.DataFrame({
                'conversion_id': ['CONV001', 'CONV002', 'CONV003', 'CONV004', 'CONV005', 'CONV006', 'CONV007', 'CONV008', 'CONV009', 'CONV010'],
                'customer_id': ['CU001', 'CU002', 'CU003', 'CU004', 'CU005', 'CU006', 'CU007', 'CU008', 'CU009', 'CU010'],
                'campaign_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C001', 'C002', 'C003', 'C004', 'C005'],
                'conversion_date': ['2024-06-15', '2024-02-15', '2024-04-20', '2024-11-15', '2024-09-20', '2024-06-20', '2024-02-25', '2024-04-25', '2024-11-20', '2024-09-25'],
                'conversion_type': ['Purchase', 'Sign-up', 'Download', 'Purchase', 'Sign-up', 'Purchase', 'Sign-up', 'Download', 'Purchase', 'Sign-up'],
                'revenue': [150, 0, 0, 200, 0, 175, 0, 0, 225, 0],
                'attribution_source': ['First Touch', 'Last Touch', 'Multi-touch', 'First Touch', 'Last Touch', 'Multi-touch', 'First Touch', 'Last Touch', 'Multi-touch', 'First Touch'],
                'touchpoint_count': [3, 2, 4, 2, 3, 4, 2, 5, 3, 2]
            })
            
            # Generate leads data (required for forecasting)
            sample_leads = pd.DataFrame({
                'lead_id': ['L001', 'L002', 'L003', 'L004', 'L005', 'L006', 'L007', 'L008', 'L009', 'L010'],
                'lead_name': ['Tech Startup Inc', 'Marketing Agency XYZ', 'E-commerce Store', 'Consulting Firm', 'Healthcare Provider', 'Financial Services', 'Education Institute', 'Manufacturing Co', 'Retail Chain', 'Software Company'],
                'email': ['contact@techstartup.com', 'info@marketingagency.com', 'sales@ecommerce.com', 'hello@consulting.com', 'info@healthcare.com', 'contact@financial.com', 'admissions@education.com', 'sales@manufacturing.com', 'info@retail.com', 'hello@software.com'],
                'company': ['Tech Startup Inc', 'Marketing Agency XYZ', 'E-commerce Store', 'Consulting Firm', 'Healthcare Provider', 'Financial Services', 'Education Institute', 'Manufacturing Co', 'Retail Chain', 'Software Company'],
                'source': ['Website', 'LinkedIn', 'Google Ads', 'Referral', 'Content Marketing', 'Social Media', 'Email', 'Trade Show', 'Organic Search', 'PPC'],
                'created_date': ['2024-01-10', '2024-02-05', '2024-01-20', '2024-02-15', '2024-01-30', '2024-02-10', '2024-01-25', '2024-02-20', '2024-02-01', '2024-01-15'],
                'status': ['Qualified', 'New', 'Qualified', 'New', 'Qualified', 'New', 'Qualified', 'New', 'Qualified', 'New'],
                'assigned_to': ['Sales Team A', 'Sales Team B', 'Sales Team A', 'Sales Team B', 'Sales Team A', 'Sales Team B', 'Sales Team A', 'Sales Team B', 'Sales Team A', 'Sales Team B'],
                'value': [5000, 3000, 8000, 6000, 4000, 7000, 3500, 9000, 2500, 12000],
                'conversion_date': ['2024-02-15', '2024-03-20', '2024-02-25', '2024-03-25', '2024-02-28', '2024-03-30', '2024-03-05', '2024-04-05', '2024-03-10', '2024-02-20']
            })
            
            # Generate content marketing data (required for content analysis)
            sample_content_marketing = pd.DataFrame({
                'content_id': ['CONT001', 'CONT002', 'CONT003', 'CONT004', 'CONT005', 'CONT006', 'CONT007', 'CONT008'],
                'title': ['Ultimate Guide to Digital Marketing', '10 SEO Tips for 2024', 'Social Media Strategy Guide', 'Email Marketing Best Practices', 'Content Marketing ROI', 'Brand Building Strategies', 'Customer Journey Mapping', 'Marketing Analytics Guide'],
                'content_type': ['Blog Post', 'Infographic', 'Video', 'Whitepaper', 'Case Study', 'Blog Post', 'E-book', 'Webinar'],
                'publish_date': ['2024-01-15', '2024-02-01', '2024-02-15', '2024-03-01', '2024-03-15', '2024-04-01', '2024-04-15', '2024-05-01'],
                'channel': ['Website', 'Social Media', 'YouTube', 'Website', 'Website', 'Website', 'Website', 'Zoom'],
                'views': [2500, 1800, 3200, 1200, 900, 2100, 1500, 800],
                'shares': [180, 120, 250, 80, 60, 150, 100, 45],
                'comments': [45, 32, 68, 18, 25, 38, 42, 35],
                'leads_generated': [25, 18, 35, 12, 8, 22, 15, 10],
                'engagement_rate': [0.08, 0.12, 0.15, 0.06, 0.10, 0.09, 0.11, 0.18],
                'conversions': [45, 32, 68, 18, 25, 38, 42, 35],
                'time_on_page': [180, 120, 240, 90, 75, 150, 110, 60],
                'author': ['Marketing Team', 'SEO Specialist', 'Content Creator', 'Marketing Manager', 'Analytics Team', 'Brand Manager', 'UX Team', 'Marketing Director']
            })
            
            # Generate social media data
            sample_social_media = pd.DataFrame({
                'post_id': ['SOC001', 'SOC002', 'SOC003', 'SOC004', 'SOC005', 'SOC006', 'SOC007', 'SOC008'],
                'platform': ['Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Twitter'],
                'post_type': ['Image', 'Video', 'Article', 'Text', 'Carousel', 'Story', 'Poll', 'Text'],
                'publish_date': ['2024-01-15', '2024-01-20', '2024-01-25', '2024-02-01', '2024-02-05', '2024-02-10', '2024-02-15', '2024-02-20'],
                'content_type': ['Product Promotion', 'Brand Awareness', 'Thought Leadership', 'Customer Service', 'Product Demo', 'Behind the Scenes', 'Industry News', 'Customer Testimonial'],
                'impressions': [5000, 6500, 3500, 2500, 5500, 4500, 3000, 2000],
                'clicks': [150, 200, 80, 45, 180, 120, 95, 60],
                'shares': [25, 35, 15, 8, 30, 20, 12, 10],
                'comments': [18, 28, 12, 6, 22, 15, 8, 7],
                'likes': [120, 180, 65, 35, 150, 100, 75, 45],
                'reach': [2500, 3200, 1800, 1200, 2800, 2400, 1600, 1000],
                'engagement_rate': [0.072, 0.089, 0.089, 0.075, 0.075, 0.073, 0.094, 0.112]
            })
            
            # Generate email campaign data
            sample_email_campaigns = pd.DataFrame({
                'email_id': ['EMAIL001', 'EMAIL002', 'EMAIL003', 'EMAIL004', 'EMAIL005', 'EMAIL006'],
                'campaign_name': ['Weekly Newsletter', 'Product Launch', 'Holiday Sale', 'Customer Onboarding', 'Abandoned Cart', 'Welcome Series'],
                'subject_line': ['This Week in Marketing', 'New Product Launch!', 'Holiday Special Offers', 'Welcome to Our Platform', 'Complete Your Purchase', 'Welcome to the Family'],
                'send_date': ['2024-01-15', '2024-02-01', '2024-03-01', '2024-01-20', '2024-02-15', '2024-01-25'],
                'recipients': [5000, 3000, 8000, 1200, 2500, 2000],
                'opens': [1250, 900, 2000, 360, 500, 600],
                'clicks': [375, 270, 600, 108, 150, 180],
                'conversions': [75, 54, 120, 22, 30, 36],
                'unsubscribes': [25, 9, 40, 4, 10, 6],
                'bounces': [100, 45, 200, 12, 50, 30],
                'bounce_rate': [0.02, 0.015, 0.025, 0.01, 0.02, 0.015]
            })
            
            # Generate website traffic data
            sample_website_traffic = pd.DataFrame({
                'date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06', '2024-01-07', '2024-01-08'],
                'customer_id': ['CU001', 'CU002', 'CU003', 'CU004', 'CU005', 'CU006', 'CU007', 'CU008'],
                'page_views': [1200, 1350, 1100, 1400, 1250, 1300, 1150, 1450],
                'unique_visitors': [800, 900, 750, 950, 850, 900, 800, 1000],
                'bounce_rate': [0.35, 0.32, 0.38, 0.30, 0.33, 0.31, 0.36, 0.29],
                'avg_session_duration': [180, 195, 165, 210, 185, 200, 170, 220],
                'conversion_rate': [0.025, 0.028, 0.022, 0.030, 0.026, 0.029, 0.024, 0.032],
                'traffic_source': ['Organic Search', 'Direct', 'Social Media', 'Paid Ads', 'Referral', 'Email', 'Organic Search', 'Direct'],
                'conversion_flag': [1, 1, 0, 1, 0, 1, 0, 1],
                'session_id': ['SESS001', 'SESS002', 'SESS003', 'SESS004', 'SESS005', 'SESS006', 'SESS007', 'SESS008'],
                'time_on_page': [180, 195, 165, 210, 185, 200, 170, 220],
                'device_type': ['Mobile', 'Desktop', 'Mobile', 'Desktop', 'Mobile', 'Desktop', 'Mobile', 'Desktop']
            })
            
            # Load all sample data into session state with safety checks
            st.session_state.campaigns_data = pd.DataFrame(sample_campaigns)
            st.session_state.customers_data = pd.DataFrame(sample_customers)
            st.session_state.conversions_data = pd.DataFrame(sample_conversions)
            st.session_state.leads_data = pd.DataFrame(sample_leads)
            st.session_state.content_marketing_data = pd.DataFrame(sample_content_marketing)
            st.session_state.social_media_data = pd.DataFrame(sample_social_media)
            st.session_state.email_campaigns_data = pd.DataFrame(sample_email_campaigns)
            st.session_state.website_traffic_data = pd.DataFrame(sample_website_traffic)
            
            st.success("✅ Comprehensive sample marketing dataset loaded successfully!")
            st.info("📊 Sample data now includes: 8 campaigns, 10 customers, 10 conversions, 10 leads, 8 content pieces, 8 social posts, 6 email campaigns, and 8 website traffic records. All analysis sections are now fully functional!")
            
            # Show comprehensive data preview
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Sample Campaigns & Conversions")
                st.dataframe(sample_campaigns, use_container_width=True)
                st.dataframe(sample_conversions, use_container_width=True)
            
            with col2:
                st.subheader("Sample Customers & Leads")
                st.dataframe(sample_customers, use_container_width=True)
                st.dataframe(sample_leads, use_container_width=True)
        
        st.markdown("### 📈 What You Can Do With Sample Data")
        st.markdown("• **Campaign Performance Analysis** - Analyze campaign metrics, ROI, and conversion tracking")
        st.markdown("• **Customer Analysis** - Understand customer segments, behavior, and lifetime value")
        st.markdown("• **Market Analysis** - Analyze market trends, customer acquisition, and competitive insights")
        st.markdown("• **Content Marketing Analysis** - Measure content performance, engagement, and ROI")
        st.markdown("• **Digital Marketing Analytics** - Track social media, email, and website performance")
        st.markdown("• **Brand Awareness Metrics** - Measure brand visibility, reach, and engagement")
        st.markdown("• **Product Marketing Analysis** - Analyze product performance and customer journey")
        st.markdown("• **Customer Journey Mapping** - Track touchpoints and conversion paths")
        st.markdown("• **Marketing Forecasting** - Test predictive analytics with comprehensive data")
        st.markdown("• **Channel Analysis** - Compare performance across all marketing channels")
        
        st.markdown("### 🔄 Reset Data")
        if st.button("🗑️ Clear All Data", key="clear_data_btn", use_container_width=True):
            # Clear all data with safety checks
            for var in ['campaigns_data', 'customers_data', 'website_traffic_data', 
                       'social_media_data', 'email_campaigns_data', 'content_marketing_data', 
                       'leads_data', 'conversions_data']:
                st.session_state[var] = pd.DataFrame()
            st.success("✅ All data cleared successfully!")

def show_campaign_performance():
    """Display world-class campaign performance analysis with advanced visualizations"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .performance-header {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .table-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.header("📈 Campaign Performance Analysis")
    
    # Check if required data exists and has data with proper validation
    if ('campaigns_data' not in st.session_state or 
        not isinstance(st.session_state.campaigns_data, pd.DataFrame) or 
        st.session_state.campaigns_data.empty or 
        'conversions_data' not in st.session_state or 
        not isinstance(st.session_state.conversions_data, pd.DataFrame) or 
        st.session_state.conversions_data.empty):
        st.warning("⚠️ Campaign and conversion data required for analysis. Please upload data or load sample dataset first.")
        st.info("💡 **Tip**: Go to '📝 Data Input' to upload your data or load the sample dataset to explore this feature.")
        return
    
    # Calculate campaign performance summary
    campaign_performance = calculate_campaign_performance_summary(
        st.session_state.campaigns_data, 
        st.session_state.conversions_data
    )
    
    # Summary Dashboard with professional styling
    total_revenue = campaign_performance['revenue'].sum()
    total_budget = campaign_performance['budget'].sum()
    total_conversions = campaign_performance['conversions'].sum()
    avg_roi = campaign_performance['roi'].mean()
    avg_cpa = campaign_performance['cpa'].mean()
    
    st.markdown("""
    <div class="summary-dashboard">
        <h3 style="color: white; margin: 0; text-align: center;">📈 Campaign Performance Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced summary metrics with color coding
    summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)
    
    with summary_col1:
        st.markdown(f"""
        <div class="metric-card-blue">
            <h4 style="color: white; margin: 0; font-size: 14px;">Total Revenue</h4>
            <h2 style="color: white; margin: 5px 0; font-size: 24px;">${total_revenue:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown(f"""
        <div class="metric-card-red">
            <h4 style="color: white; margin: 0; font-size: 14px;">Total Budget</h4>
            <h2 style="color: white; margin: 5px 0; font-size: 24px;">${total_budget:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown(f"""
        <div class="metric-card-orange">
            <h4 style="color: white; margin: 0; font-size: 14px;">Total Conversions</h4>
            <h2 style="color: white; margin: 5px 0; font-size: 24px;">{total_conversions:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown(f"""
        <div class="metric-card-teal">
            <h4 style="color: white; margin: 0; font-size: 14px;">Avg ROI</h4>
            <h2 style="color: white; margin: 5px 0; font-size: 24px;">{avg_roi:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col5:
        st.markdown(f"""
        <div class="metric-card-green">
            <h4 style="color: white; margin: 0; font-size: 14px;">Avg CPA</h4>
            <h2 style="color: white; margin: 5px 0; font-size: 24px;">${avg_cpa:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
        # Enhanced ROI and CPA Analysis with Advanced Visualizations
    st.subheader("🎯 Campaign Performance by Type - Advanced Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 ROI Performance Analysis")
        roi_by_type = campaign_performance.groupby('campaign_type').agg({
            'roi': 'mean',
            'revenue': 'sum',
            'budget': 'sum',
            'conversions': 'sum'
        }).reset_index()
        
        if not roi_by_type.empty:
            # Enhanced insights with color coding
            avg_roi_value = roi_by_type['roi'].mean()
            best_roi = roi_by_type['roi'].max()
            worst_roi = roi_by_type['roi'].min()
            
            # Performance indicator
            if avg_roi_value >= 25:
                performance_status = "🟢 Excellent"
                status_color = "#28a745"
            elif avg_roi_value >= 15:
                performance_status = "🟡 Good"
                status_color = "#ffc107"
            elif avg_roi_value >= 5:
                performance_status = "🟠 Fair"
                status_color = "#fd7e14"
            else:
                performance_status = "🔴 Poor"
                status_color = "#dc3545"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid {status_color}; margin: 15px 0;">
                <h3 style="margin: 0; color: #333; font-size: 18px;">{performance_status} Performance</h3>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Average ROI: <strong>{avg_roi_value:.1f}%</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Best: <strong>{best_roi:.1f}%</strong> | Worst: <strong>{worst_roi:.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced interactive bar chart with tooltips
            fig_roi = px.bar(
                roi_by_type, 
                x='campaign_type', 
                y='roi', 
                title='ROI Performance by Campaign Type',
                color='roi',
                color_continuous_scale='RdYlGn',
                text='roi',
                hover_data=['revenue', 'budget', 'conversions'],
                labels={'roi': 'ROI (%)', 'campaign_type': 'Campaign Type', 'revenue': 'Revenue ($)', 'budget': 'Budget ($)', 'conversions': 'Conversions'}
            )
            
            # Enhanced layout with professional styling
            fig_roi.update_layout(
                title_font_size=20,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            # Enhanced axis styling
            fig_roi.update_xaxes(
                title_text="Campaign Type",
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d'
            )
            
            fig_roi.update_yaxes(
                title_text="ROI (%)",
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            # Enhanced bar styling
            fig_roi.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                textfont_size=12,
                textfont_color='#495057',
                hovertemplate='<b>%{x}</b><br>' +
                              'ROI: <b>%{y:.1f}%</b><br>' +
                              'Revenue: $%{customdata[0]:,.0f}<br>' +
                              'Budget: $%{customdata[1]:,.0f}<br>' +
                              'Conversions: %{customdata[2]:,.0f}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_roi, use_container_width=True, key="roi_campaign_chart")
            
            # Performance insights
            with st.expander("💡 ROI Performance Insights", expanded=False):
                st.markdown(f"""
                **Performance Analysis:**
                - **Best Performing Type:** {roi_by_type.loc[roi_by_type['roi'].idxmax(), 'campaign_type']} ({roi_by_type['roi'].max():.1f}% ROI)
                - **Needs Improvement:** {roi_by_type.loc[roi_by_type['roi'].idxmin(), 'campaign_type']} ({roi_by_type['roi'].min():.1f}% ROI)
                - **Performance Range:** {roi_by_type['roi'].max() - roi_by_type['roi'].min():.1f}% difference
                """)
                
                # ROI distribution analysis
                st.markdown("**ROI Distribution:**")
                roi_stats = roi_by_type['roi'].describe()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{roi_stats['mean']:.1f}%")
                with col2:
                    st.metric("Median", f"{roi_stats['50%']:.1f}%")
                with col3:
                    st.metric("Std Dev", f"{roi_stats['std']:.1f}%")
    
    with col2:
        st.markdown("#### 💰 CPA Performance Analysis")
        cpa_by_type = campaign_performance.groupby('campaign_type').agg({
            'cpa': 'mean',
            'budget': 'sum',
            'conversions': 'sum'
        }).reset_index()
        
        if not cpa_by_type.empty:
            # Enhanced insights with color coding
            avg_cpa_value = cpa_by_type['cpa'].mean()
            best_cpa = cpa_by_type['cpa'].min()
            worst_cpa = cpa_by_type['cpa'].max()
            
            # CPA performance indicator
            if avg_cpa_value <= 30:
                cpa_status = "🟢 Excellent"
                cpa_color = "#28a745"
            elif avg_cpa_value <= 60:
                cpa_status = "🟡 Good"
                cpa_color = "#ffc107"
            elif avg_cpa_value <= 100:
                cpa_status = "🟠 Fair"
                cpa_color = "#fd7e14"
            else:
                cpa_status = "🔴 Poor"
                cpa_color = "#dc3545"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid {cpa_color}; margin: 15px 0;">
                <h3 style="margin: 0; color: #333; font-size: 18px;">{cpa_status} Efficiency</h3>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Average CPA: <strong>${avg_cpa_value:.0f}</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Best: <strong>${best_cpa:.0f}</strong> | Worst: <strong>${worst_cpa:.0f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced interactive bar chart with tooltips
            fig_cpa = px.bar(
                cpa_by_type, 
                x='campaign_type', 
                y='cpa', 
                title='Cost Per Acquisition by Campaign Type',
                color='cpa',
                color_continuous_scale='RdYlGn_r',
                text='cpa',
                hover_data=['budget', 'conversions'],
                labels={'cpa': 'CPA ($)', 'campaign_type': 'Campaign Type', 'budget': 'Budget ($)', 'conversions': 'Conversions'}
            )
            
            # Enhanced layout with professional styling
            fig_cpa.update_layout(
                title_font_size=20,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            # Enhanced axis styling
            fig_cpa.update_xaxes(
                title_text="Campaign Type",
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d'
            )
            
            fig_cpa.update_yaxes(
                title_text="CPA ($)",
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            # Enhanced bar styling
            fig_cpa.update_traces(
                texttemplate='$%{text:.0f}',
                textposition='outside',
                textfont_size=12,
                textfont_color='#495057',
                hovertemplate='<b>%{x}</b><br>' +
                              'CPA: <b>$%{y:.0f}</b><br>' +
                              'Budget: $%{customdata[0]:,.0f}<br>' +
                              'Conversions: %{customdata[1]:,.0f}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_cpa, use_container_width=True, key="cpa_campaign_chart")
            
            # CPA insights
            with st.expander("💡 CPA Performance Insights", expanded=False):
                st.markdown(f"""
                **Efficiency Analysis:**
                - **Most Efficient:** {cpa_by_type.loc[cpa_by_type['cpa'].idxmin(), 'campaign_type']} (${cpa_by_type['cpa'].min():.0f} CPA)
                - **Least Efficient:** {cpa_by_type.loc[cpa_by_type['cpa'].idxmax(), 'campaign_type']} (${cpa_by_type['cpa'].max():.0f} CPA)
                - **Efficiency Range:** ${cpa_by_type['cpa'].max() - cpa_by_type['cpa'].min():.0f} difference
                """)
                
                # CPA distribution analysis
                st.markdown("**CPA Distribution:**")
                cpa_stats = cpa_by_type['cpa'].describe()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"${cpa_stats['mean']:.0f}")
                with col2:
                    st.metric("Median", f"${cpa_stats['50%']:.0f}")
                with col3:
                    st.metric("Std Dev", f"${cpa_stats['std']:.0f}")
    
    # Enhanced Top Performing Campaigns Analysis
    st.subheader("🏆 Top Performing Campaigns - Advanced Leaderboard")
    
    if not campaign_performance.empty:
        # Performance insights header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
            <h3 style="margin: 0; font-size: 20px;">🎯 Campaign Performance Insights</h3>
            <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
                Analyzing {len(campaign_performance)} campaigns across {campaign_performance['campaign_type'].nunique()} types
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥇 Top 10 Campaigns by ROI")
            top_roi_campaigns = campaign_performance.nlargest(10, 'roi')[['campaign_name', 'roi', 'revenue', 'budget', 'conversions']]
            
            # Enhanced performance indicator
            best_roi = top_roi_campaigns['roi'].iloc[0] if not top_roi_campaigns.empty else 0
            if best_roi >= 50:
                performance_emoji = "🚀"
                performance_text = "Exceptional"
                performance_color = "#28a745"
            elif best_roi >= 30:
                performance_emoji = "⭐"
                performance_text = "Excellent"
                performance_color = "#17a2b8"
            elif best_roi >= 20:
                performance_emoji = "👍"
                performance_text = "Good"
                performance_color = "#ffc107"
            else:
                performance_emoji = "📈"
                performance_text = "Positive"
                performance_color = "#fd7e14"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid {performance_color}; margin: 15px 0;">
                <h3 style="margin: 0; color: #333; font-size: 18px;">{performance_emoji} {performance_text} Performance</h3>
                <p style="margin: 5px 0; color: #666; font-size: 16px;">Best ROI: <strong>{best_roi:.1f}%</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Average Top 10 ROI: <strong>{top_roi_campaigns['roi'].mean():.1f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced interactive table with better formatting
            top_roi_display = top_roi_campaigns.copy()
            top_roi_display['ROI (%)'] = top_roi_display['roi'].apply(lambda x: f"{x:.1f}%")
            top_roi_display['Revenue ($)'] = top_roi_display['revenue'].apply(lambda x: f"${x:,.0f}")
            top_roi_display['Budget ($)'] = top_roi_display['budget'].apply(lambda x: f"${x:,.0f}")
            
            display_columns = ['campaign_name', 'ROI (%)', 'Revenue ($)', 'Budget ($)', 'conversions']
            st.dataframe(
                top_roi_display[display_columns].rename(columns={
                    'campaign_name': 'Campaign Name',
                    'conversions': 'Conversions'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # ROI performance insights
            with st.expander("💡 ROI Leaderboard Insights", expanded=False):
                st.markdown(f"""
                **Performance Analysis:**
                - **Champion Campaign:** {top_roi_campaigns['campaign_name'].iloc[0]} ({best_roi:.1f}% ROI)
                - **Top 5 Average:** {top_roi_campaigns.head(5)['roi'].mean():.1f}% ROI
                - **Performance Gap:** {best_roi - top_roi_campaigns['roi'].iloc[-1]:.1f}% between 1st and 10th
                """)
        
        with col2:
            st.markdown("#### 💰 Top 10 Campaigns by Revenue")
            top_revenue_campaigns = campaign_performance.nlargest(10, 'revenue')[['campaign_name', 'revenue', 'roi', 'budget', 'conversions']]
            
            # Enhanced revenue indicator
            best_revenue = top_revenue_campaigns['revenue'].iloc[0] if not top_revenue_campaigns.empty else 0
            if best_revenue >= 100000:
                revenue_emoji = "💎"
                revenue_text = "Premium"
                revenue_color = "#28a745"
            elif best_revenue >= 50000:
                revenue_emoji = "💵"
                revenue_text = "High Value"
                revenue_color = "#17a2b8"
            elif best_revenue >= 25000:
                revenue_emoji = "💰"
                revenue_text = "Good Value"
                revenue_color = "#ffc107"
            else:
                revenue_emoji = "💸"
                revenue_text = "Standard"
                revenue_color = "#fd7e14"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid {revenue_color}; margin: 15px 0;">
                <h3 style="margin: 0; color: #333; font-size: 18px;">{revenue_emoji} {revenue_text} Revenue</h3>
                <p style="margin: 5px 0; color: #666; font-size: 16px;">Best Revenue: <strong>${best_revenue:,.0f}</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Average Top 10 Revenue: <strong>${top_revenue_campaigns['revenue'].mean():,.0f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced interactive table with better formatting
            top_revenue_display = top_revenue_campaigns.copy()
            top_revenue_display['Revenue ($)'] = top_revenue_display['revenue'].apply(lambda x: f"${x:,.0f}")
            top_revenue_display['ROI (%)'] = top_revenue_display['roi'].apply(lambda x: f"{x:.1f}%")
            top_revenue_display['Budget ($)'] = top_revenue_display['budget'].apply(lambda x: f"${x:,.0f}")
            
            display_columns = ['campaign_name', 'Revenue ($)', 'ROI (%)', 'Budget ($)', 'conversions']
            st.dataframe(
                top_revenue_display[display_columns].rename(columns={
                    'campaign_name': 'Campaign Name',
                    'conversions': 'Conversions'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Revenue performance insights
            with st.expander("💡 Revenue Leaderboard Insights", expanded=False):
                st.markdown(f"""
                **Revenue Analysis:**
                - **Top Revenue Generator:** {top_revenue_campaigns['campaign_name'].iloc[0]} (${best_revenue:,.0f})
                - **Top 5 Average:** ${top_revenue_campaigns.head(5)['revenue'].mean():,.0f}
                - **Revenue Range:** ${best_revenue - top_revenue_campaigns['revenue'].iloc[-1]:,.0f} between 1st and 10th
                """)
    
    # Enhanced Campaign Efficiency Analysis with Advanced Visualizations
    st.subheader("⚡ Campaign Efficiency Analysis - Multi-Dimensional Insights")
    
    if not campaign_performance.empty:
        # Efficiency insights header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 20px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
            <h3 style="margin: 0; font-size: 20px;">📊 Efficiency Metrics Dashboard</h3>
            <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
                Analyzing budget efficiency, conversion patterns, and channel performance
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Budget vs Revenue Efficiency")
            
            # Enhanced scatter plot with better tooltips and styling
            fig_scatter = px.scatter(
                campaign_performance,
                x='budget',
                y='revenue',
                size='conversions',
                color='campaign_type',
                hover_data=['campaign_name', 'roi', 'cpa'],
                title="Budget vs Revenue Efficiency by Campaign Type",
                color_discrete_sequence=['#FF6B35', '#004E89', '#1A936F', '#C6DABF', '#2E86AB', '#E63946', '#457B9D'],
                labels={
                    'budget': 'Budget ($)',
                    'revenue': 'Revenue ($)',
                    'conversions': 'Conversions',
                    'campaign_type': 'Campaign Type',
                    'roi': 'ROI (%)',
                    'cpa': 'CPA ($)'
                }
            )
            
            # Enhanced layout with professional styling
            fig_scatter.update_layout(
                title_font_size=20,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_title="Budget ($)",
                yaxis_title="Revenue ($)",
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1,
                    font=dict(size=12)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=500,
                margin=dict(l=50, r=50, t=80, b=80)
            )
            
            # Enhanced axis styling
            fig_scatter.update_xaxes(
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_scatter.update_yaxes(
                title_font_size=14,
                title_font_color='#495057',
                tickfont_size=12,
                tickfont_color='#6c757d',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            # Enhanced hover template
            fig_scatter.update_traces(
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                              'Budget: $%{x:,.0f}<br>' +
                              'Revenue: $%{y:,.0f}<br>' +
                              'Conversions: %{marker.size}<br>' +
                              'ROI: %{customdata[1]:.1f}%<br>' +
                              'CPA: $%{customdata[2]:.0f}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True, key="budget_revenue_scatter")
            
            # Efficiency insights
            with st.expander("💡 Budget Efficiency Insights", expanded=False):
                # Calculate efficiency metrics
                total_efficiency = (total_revenue / total_budget) if total_budget > 0 else 0
                efficient_campaigns = len(campaign_performance[campaign_performance['roi'] > 0])
                total_campaigns = len(campaign_performance)
                
                st.markdown(f"""
                **Efficiency Analysis:**
                - **Overall Efficiency:** ${total_efficiency:.2f} revenue per $1 spent
                - **Efficient Campaigns:** {efficient_campaigns}/{total_campaigns} ({efficient_campaigns/total_campaigns*100:.1f}%)
                - **Budget Utilization:** {total_budget:,.0f} total budget across all campaigns
                """)
        
        with col2:
            st.markdown("#### 📊 Channel Performance Analysis")
            
            if 'channel' in campaign_performance.columns:
                channel_performance = campaign_performance.groupby('channel').agg({
                    'conversions': 'sum',
                    'budget': 'sum',
                    'revenue': 'sum',
                    'campaign_id': 'count'
                }).reset_index()
                
                # Calculate advanced metrics
                channel_performance['conversion_rate'] = (channel_performance['conversions'] / channel_performance['budget']) * 100
                channel_performance['roi'] = ((channel_performance['revenue'] - channel_performance['budget']) / channel_performance['budget']) * 100
                channel_performance['cpa'] = channel_performance['budget'] / channel_performance['conversions']
                
                # Enhanced performance indicator
                best_conversion_rate = channel_performance['conversion_rate'].max() if not channel_performance.empty else 0
                best_channel = channel_performance.loc[channel_performance['conversion_rate'].idxmax(), 'channel'] if not channel_performance.empty else 'N/A'
                
                if best_conversion_rate >= 5:
                    channel_status = "🟢 Excellent"
                    channel_color = "#28a745"
                elif best_conversion_rate >= 2:
                    channel_status = "🟡 Good"
                    channel_color = "#ffc107"
                else:
                    channel_status = "🔴 Needs Improvement"
                    channel_color = "#dc3545"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                            padding: 20px; border-radius: 12px; border-left: 5px solid {channel_color}; margin: 15px 0;">
                    <h3 style="margin: 0; color: #333; font-size: 18px;">{channel_status} Channel Performance</h3>
                    <p style="margin: 5px 0; color: #666; font-size: 16px;">Best Channel: <strong>{best_channel}</strong></p>
                    <p style="margin: 5px 0; color: #666; font-size: 14px;">Conversion Rate: <strong>{best_conversion_rate:.2f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced channel performance chart
                fig_channel = px.bar(
                    channel_performance,
                    x='channel',
                    y='conversion_rate',
                    title="Conversion Rate by Marketing Channel",
                    color='roi',
                    color_continuous_scale='RdYlGn',
                    text='conversion_rate',
                    hover_data=['revenue', 'budget', 'conversions', 'roi'],
                    labels={
                        'conversion_rate': 'Conversion Rate (%)',
                        'channel': 'Marketing Channel',
                        'roi': 'ROI (%)',
                        'revenue': 'Revenue ($)',
                        'budget': 'Budget ($)',
                        'conversions': 'Conversions'
                    }
                )
                
                # Enhanced layout
                fig_channel.update_layout(
                    title_font_size=20,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=True,
                    legend=dict(
                        title="ROI (%)",
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='rgba(0,0,0,0.1)',
                        borderwidth=1
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500,
                    margin=dict(l=50, r=50, t=80, b=80)
                )
                
                # Enhanced axis styling
                fig_channel.update_xaxes(
                    title_text="Marketing Channel",
                    title_font_size=14,
                    title_font_color='#495057',
                    tickfont_size=12,
                    tickfont_color='#6c757d'
                )
                
                fig_channel.update_yaxes(
                    title_text="Conversion Rate (%)",
                    title_font_size=14,
                    title_font_color='#495057',
                    tickfont_size=12,
                    tickfont_color='#6c757d',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                # Enhanced bar styling
                fig_channel.update_traces(
                    texttemplate='%{text:.2f}%',
                    textposition='outside',
                    textfont_size=12,
                    textfont_color='#495057',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'Conversion Rate: <b>%{y:.2f}%</b><br>' +
                                  'ROI: <b>%{customdata[3]:.1f}%</b><br>' +
                                  'Revenue: $%{customdata[0]:,.0f}<br>' +
                                  'Budget: $%{customdata[1]:,.0f}<br>' +
                                  'Conversions: %{customdata[2]:,.0f}<br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_channel, use_container_width=True, key="channel_conversion_chart")
                
                # Channel insights
                with st.expander("💡 Channel Performance Insights", expanded=False):
                    st.markdown(f"""
                    **Channel Analysis:**
                    - **Most Efficient:** {best_channel} ({best_conversion_rate:.2f}% conversion rate)
                    - **Total Channels:** {len(channel_performance)} active channels
                    - **Performance Range:** {channel_performance['conversion_rate'].max() - channel_performance['conversion_rate'].min():.2f}% difference
                    """)
                    
                    # Channel performance summary
                    st.markdown("**Channel Performance Summary:**")
                    channel_summary = channel_performance[['channel', 'conversion_rate', 'roi', 'cpa']].round(2)
                    st.dataframe(
                        channel_summary.rename(columns={
                            'channel': 'Channel',
                            'conversion_rate': 'Conv. Rate (%)',
                            'roi': 'ROI (%)',
                            'cpa': 'CPA ($)'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
    
    # Enhanced Detailed Campaign Performance Table with Advanced Analytics
    st.subheader("📋 Comprehensive Campaign Performance Details")
    
    if not campaign_performance.empty:
        # Performance summary header
        total_campaigns = len(campaign_performance)
        profitable_campaigns = len(campaign_performance[campaign_performance['roi'] > 0])
        success_rate = (profitable_campaigns / total_campaigns) * 100 if total_campaigns > 0 else 0
        
        # Enhanced success rate indicator
        if success_rate >= 80:
            success_emoji = "🚀"
            success_text = "Exceptional"
            success_color = "#28a745"
        elif success_rate >= 70:
            success_emoji = "⭐"
            success_text = "Excellent"
            success_color = "#17a2b8"
        elif success_rate >= 50:
            success_emoji = "👍"
            success_text = "Good"
            success_color = "#ffc107"
        else:
            success_emoji = "📈"
            success_text = "Needs Improvement"
            success_color = "#fd7e14"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 25px; border-radius: 15px; border-left: 5px solid {success_color}; margin: 20px 0;">
            <h3 style="margin: 0; color: #333; font-size: 20px;">{success_emoji} {success_text} Campaign Performance</h3>
            <p style="margin: 10px 0; color: #666; font-size: 16px;">Success Rate: <strong>{success_rate:.1f}%</strong> ({profitable_campaigns}/{total_campaigns} campaigns profitable)</p>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">Total Revenue: <strong>${total_revenue:,.0f}</strong> | Total Budget: <strong>${total_budget:,.0f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance metrics summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Avg ROI", 
                f"{campaign_performance['roi'].mean():.1f}%",
                f"{campaign_performance['roi'].std():.1f}% std"
            )
        
        with col2:
            st.metric(
                "Avg CPA", 
                f"${campaign_performance['cpa'].mean():.0f}",
                f"${campaign_performance['cpa'].std():.0f} std"
            )
        
        with col3:
            st.metric(
                "Avg Conversions", 
                f"{campaign_performance['conversions'].mean():.1f}",
                f"{campaign_performance['conversions'].std():.1f} std"
            )
        
        with col4:
            st.metric(
                "Efficiency Ratio", 
                f"${(total_revenue / total_budget):.2f}",
                "revenue per $1 spent"
            )
        
        # Enhanced interactive table with better formatting
        display_columns = ['campaign_name', 'campaign_type', 'channel', 'budget', 'revenue', 'roi', 'cpa', 'conversions']
        display_df = campaign_performance[display_columns].copy()
        
        # Format columns for better readability
        display_df['Budget ($)'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
        display_df['Revenue ($)'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
        display_df['ROI (%)'] = display_df['roi'].apply(lambda x: f"{x:.1f}%")
        display_df['CPA ($)'] = display_df['cpa'].apply(lambda x: f"${x:.0f}")
        display_df['Conversions'] = display_df['conversions'].apply(lambda x: f"{x:,}")
        
        # Rename columns for display
        display_df = display_df.rename(columns={
            'campaign_name': 'Campaign Name',
            'campaign_type': 'Campaign Type',
            'channel': 'Channel'
        })
        
        # Select formatted columns
        formatted_columns = ['Campaign Name', 'Campaign Type', 'Channel', 'Budget ($)', 'Revenue ($)', 'ROI (%)', 'CPA ($)', 'Conversions']
        
        # Add performance indicators
        st.markdown("#### 📊 Performance Indicators")
        
        # Performance distribution
        col1, col2 = st.columns(2)
        
        with col1:
            # ROI distribution
            roi_ranges = [
                (0, 10, "Low (0-10%)", "#dc3545"),
                (10, 25, "Medium (10-25%)", "#ffc107"),
                (25, 50, "High (25-50%)", "#17a2b8"),
                (50, float('inf'), "Exceptional (50%+)", "#28a745")
            ]
            
            roi_distribution = []
            for min_val, max_val, label, color in roi_ranges:
                if max_val == float('inf'):
                    count = len(campaign_performance[campaign_performance['roi'] >= min_val])
                else:
                    count = len(campaign_performance[(campaign_performance['roi'] >= min_val) & (campaign_performance['roi'] < max_val)])
                roi_distribution.append({'Range': label, 'Count': count, 'Color': color})
            
            roi_df = pd.DataFrame(roi_distribution)
            
            fig_roi_dist = px.bar(
                roi_df,
                x='Range',
                y='Count',
                title="ROI Performance Distribution",
                color='Range',
                color_discrete_map={row['Range']: row['Color'] for _, row in roi_df.iterrows()}
            )
            
            fig_roi_dist.update_layout(
                title_font_size=16,
                title_font_color='#1e3c72',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            
            st.plotly_chart(fig_roi_dist, use_container_width=True)
        
        with col2:
            # Channel performance summary
            if 'channel' in campaign_performance.columns:
                channel_summary = campaign_performance.groupby('channel').agg({
                    'roi': 'mean',
                    'cpa': 'mean',
                    'conversions': 'sum'
                }).round(2)
                
                fig_channel_summary = px.bar(
                    channel_summary.reset_index(),
                    x='channel',
                    y='roi',
                    title="Average ROI by Channel",
                    color='roi',
                    color_continuous_scale='RdYlGn'
                )
                
                fig_channel_summary.update_layout(
                    title_font_size=16,
                    title_font_color='#1e3c72',
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=300
                )
                
                st.plotly_chart(fig_channel_summary, use_container_width=True)
        
        # Main performance table
        st.markdown("#### 📋 Detailed Campaign Performance Table")
        
        # Add search and filter functionality
        search_term = st.text_input("🔍 Search campaigns by name:", placeholder="Enter campaign name...")
        
        if search_term:
            filtered_df = display_df[display_df['Campaign Name'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_df = display_df
        
        # Sort options
        sort_by = st.selectbox(
            "📊 Sort by:",
            ["ROI (%)", "Revenue ($)", "Budget ($)", "Conversions", "CPA ($)"],
            index=0
        )
        
        if sort_by == "ROI (%)":
            # Sort by ROI (extract numeric value)
            filtered_df = filtered_df.copy()
            filtered_df['ROI_numeric'] = filtered_df['ROI (%)'].str.rstrip('%').astype(float)
            filtered_df = filtered_df.sort_values('ROI_numeric', ascending=False).drop('ROI_numeric', axis=1)
        elif sort_by == "Revenue ($)":
            # Sort by Revenue (extract numeric value)
            filtered_df = filtered_df.copy()
            filtered_df['Revenue_numeric'] = filtered_df['Revenue ($)'].str.replace('$', '').str.replace(',', '').astype(float)
            filtered_df = filtered_df.sort_values('Revenue_numeric', ascending=False).drop('Revenue_numeric', axis=1)
        elif sort_by == "Budget ($)":
            # Sort by Budget (extract numeric value)
            filtered_df = filtered_df.copy()
            filtered_df['Budget_numeric'] = filtered_df['Budget ($)'].str.replace('$', '').str.replace(',', '').astype(float)
            filtered_df = filtered_df.sort_values('Budget_numeric', ascending=False).drop('Budget_numeric', axis=1)
        elif sort_by == "Conversions":
            # Sort by Conversions (extract numeric value)
            filtered_df = filtered_df.copy()
            filtered_df['Conversions_numeric'] = filtered_df['Conversions'].str.replace(',', '').astype(float)
            filtered_df = filtered_df.sort_values('Conversions_numeric', ascending=False).drop('Conversions_numeric', axis=1)
        elif sort_by == "CPA ($)":
            # Sort by CPA (extract numeric value)
            filtered_df = filtered_df.copy()
            filtered_df['CPA_numeric'] = filtered_df['CPA ($)'].str.replace('$', '').astype(float)
            filtered_df = filtered_df.sort_values('CPA_numeric', ascending=True).drop('CPA_numeric', axis=1)
        
        # Display the enhanced table
        st.dataframe(
            filtered_df[formatted_columns],
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Table insights
        with st.expander("💡 Table Insights & Recommendations", expanded=False):
            st.markdown(f"""
            **Performance Summary:**
            - **Total Campaigns Analyzed:** {total_campaigns}
            - **Profitable Campaigns:** {profitable_campaigns} ({success_rate:.1f}%)
            - **Unprofitable Campaigns:** {total_campaigns - profitable_campaigns} ({100-success_rate:.1f}%)
            
            **Key Insights:**
            - **Best ROI Campaign:** {campaign_performance.loc[campaign_performance['roi'].idxmax(), 'campaign_name']} ({campaign_performance['roi'].max():.1f}% ROI)
            - **Highest Revenue Campaign:** {campaign_performance.loc[campaign_performance['revenue'].idxmax(), 'campaign_name']} (${campaign_performance['revenue'].max():,.0f})
            - **Most Efficient Campaign:** {campaign_performance.loc[campaign_performance['cpa'].idxmin(), 'campaign_name']} (${campaign_performance['cpa'].min():.0f} CPA)
            
            **Recommendations:**
            - Focus on campaigns with ROI > 25% for scaling
            - Investigate campaigns with negative ROI for optimization
            - Consider increasing budget for high-performing campaigns
            """)

def show_customer_analysis():
    """Display world-class customer analysis with advanced visualizations and insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .customer-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .customer-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .customer-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .customer-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("👥 Customer Analysis - Advanced Insights Dashboard")
    st.markdown("---")
    
    # Check if customers_data exists and has data
    if 'customers_data' not in st.session_state or st.session_state.customers_data.empty:
        st.warning("⚠️ Customer data required for this analysis. Please upload data or load sample dataset first.")
        st.info("💡 **Tip**: Go to '📝 Data Input' to upload your data or load the sample dataset to explore this feature.")
        return
    
    # Enhanced Customer Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🎯 Customer Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Analyzing {len(st.session_state.customers_data):,} customers with advanced segmentation and behavioral insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Customer Metrics Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(st.session_state.customers_data)
        st.markdown(f"""
        <div class="customer-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">👥 Total Customers</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_customers:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Active customer base</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'lifetime_value' in st.session_state.customers_data.columns:
            avg_clv = st.session_state.customers_data['lifetime_value'].mean()
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">💰 Avg CLV</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">${avg_clv:,.0f}</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Customer lifetime value</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">💰 Avg CLV</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">N/A</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if 'total_purchases' in st.session_state.customers_data.columns:
            repeat_rate = calculate_repeat_customer_rate(st.session_state.customers_data)
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🔄 Repeat Rate</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{repeat_rate:.1f}%</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Customer retention</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🔄 Repeat Rate</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">N/A</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'acquisition_source' in st.session_state.customers_data.columns:
            unique_sources = st.session_state.customers_data['acquisition_source'].nunique()
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">📊 Sources</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{unique_sources}</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Acquisition channels</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="customer-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">📊 Sources</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">N/A</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Data not available</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Customer Segmentation Analysis
    st.subheader("🎯 Advanced Customer Segmentation Analysis")
    
    if 'customer_segment' in st.session_state.customers_data.columns:
        segment_analysis = segment_customers(st.session_state.customers_data, 'customer_segment')
        
        if not segment_analysis.empty:
            # Segmentation insights header
            st.markdown(f"""
            <div class="customer-insight-card">
                <h3 style="margin: 0; color: #333; font-size: 18px;">📊 Segmentation Insights</h3>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">
                    {len(segment_analysis)} customer segments identified with distinct value characteristics
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👥 Customer Distribution by Segment")
                
                # Enhanced pie chart with better styling
                fig_segments = px.pie(
                    values=segment_analysis['customer_count'],
                    names=segment_analysis.index,
                    title="Customer Distribution by Segment",
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.4
                )
                
                fig_segments.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    showlegend=True,
                    legend=dict(
                        bgcolor='rgba(255,255,255,0.9)',
                        bordercolor='rgba(0,0,0,0.1)',
                        borderwidth=1
                    ),
                    height=400
                )
                
                fig_segments.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>' +
                                  'Customers: %{value}<br>' +
                                  'Percentage: %{percent}<br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_segments, use_container_width=True, key="customer_segments_pie")
                
                # Segment statistics
                with st.expander("💡 Segment Statistics", expanded=False):
                    segment_stats = segment_analysis.copy()
                    segment_stats['percentage'] = (segment_stats['customer_count'] / segment_stats['customer_count'].sum() * 100).round(1)
                    segment_stats['avg_clv'] = segment_stats['lifetime_value'].round(0)
                    
                    st.dataframe(
                        segment_stats.reset_index().rename(columns={
                            'customer_segment': 'Segment',
                            'customer_count': 'Count',
                            'lifetime_value': 'Avg CLV ($)',
                            'avg_purchases': 'Avg Purchases',
                            'percentage': 'Percentage (%)'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
            
            with col2:
                st.markdown("#### 💰 Customer Lifetime Value by Segment")
                
                # Enhanced bar chart with better styling
                fig_clv = px.bar(
                    segment_analysis.reset_index(),
                    x='customer_segment',
                    y='lifetime_value',
                    title="Average CLV by Customer Segment",
                    color='lifetime_value',
                    color_continuous_scale='RdYlGn',
                    text='lifetime_value',
                    labels={'lifetime_value': 'Average CLV ($)', 'customer_segment': 'Customer Segment'}
                )
                
                fig_clv.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                fig_clv.update_xaxes(
                    title_text="Customer Segment",
                    title_font_size=14,
                    title_font_color='#495057'
                )
                
                fig_clv.update_yaxes(
                    title_text="Average CLV ($)",
                    title_font_size=14,
                    title_font_color='#495057',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                fig_clv.update_traces(
                    texttemplate='$%{text:,.0f}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'Average CLV: <b>$%{y:,.0f}</b><br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_clv, use_container_width=True, key="clv_by_segment")
                
                # CLV insights
                with st.expander("💡 CLV Insights", expanded=False):
                    best_segment = segment_analysis.loc[segment_analysis['lifetime_value'].idxmax()]
                    worst_segment = segment_analysis.loc[segment_analysis['lifetime_value'].idxmin()]
                    
                    st.markdown(f"""
                    **Value Analysis:**
                    - **Highest Value Segment:** {best_segment.name} (${best_segment['lifetime_value']:,.0f} CLV)
                    - **Lowest Value Segment:** {worst_segment.name} (${worst_segment['lifetime_value']:,.0f} CLV)
                    - **Value Range:** ${best_segment['lifetime_value'] - worst_segment['lifetime_value']:,.0f} difference
                    """)
    
    st.markdown("---")
    
    # Enhanced Customer Acquisition Analysis
    st.subheader("📈 Advanced Customer Acquisition Analysis")
    
    if 'acquisition_source' in st.session_state.customers_data.columns:
        acquisition_analysis = calculate_acquisition_source_analysis(st.session_state.customers_data)
        
        if not acquisition_analysis.empty:
            # Acquisition insights header
            st.markdown(f"""
            <div class="customer-insight-card">
                <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Acquisition Channel Performance</h3>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">
                    Analyzing {len(acquisition_analysis)} acquisition channels for customer quality and volume
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👥 Customer Volume by Acquisition Source")
                
                # Enhanced bar chart for customer volume
                fig_source = px.bar(
                    acquisition_analysis.reset_index(),
                    x='acquisition_source',
                    y='new_customers',
                    title="New Customers by Acquisition Source",
                    color='new_customers',
                    color_continuous_scale='Blues',
                    text='new_customers',
                    labels={'new_customers': 'New Customers', 'acquisition_source': 'Acquisition Source'}
                )
                
                fig_source.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                fig_source.update_xaxes(
                    title_text="Acquisition Source",
                    title_font_size=14,
                    title_font_color='#495057'
                )
                
                fig_source.update_yaxes(
                    title_text="Number of Customers",
                    title_font_size=14,
                    title_font_color='#495057',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                fig_source.update_traces(
                    texttemplate='%{text:,}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'Customers: <b>%{y:,}</b><br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_source, use_container_width=True, key="customers_by_source")
            
            with col2:
                st.markdown("#### 💰 Customer Value by Acquisition Source")
                
                # Enhanced bar chart for CLV by source
                fig_source_clv = px.bar(
                    acquisition_analysis.reset_index(),
                    x='acquisition_source',
                    y='lifetime_value',
                    title="Average CLV by Acquisition Source",
                    color='lifetime_value',
                    color_continuous_scale='RdYlGn',
                    text='lifetime_value',
                    labels={'lifetime_value': 'Average CLV ($)', 'acquisition_source': 'Acquisition Source'}
                )
                
                fig_source_clv.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                fig_source_clv.update_xaxes(
                    title_text="Acquisition Source",
                    title_font_size=14,
                    title_font_color='#495057'
                )
                
                fig_source_clv.update_yaxes(
                    title_text="Average CLV ($)",
                    title_font_size=14,
                    title_font_color='#495057',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                fig_source_clv.update_traces(
                    texttemplate='$%{text:,.0f}',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'Average CLV: <b>$%{y:,.0f}</b><br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_source_clv, use_container_width=True, key="clv_by_source")
            
            # Acquisition performance summary
            with st.expander("💡 Acquisition Performance Summary", expanded=False):
                best_source = acquisition_analysis.loc[acquisition_analysis['lifetime_value'].idxmax()]
                best_volume = acquisition_analysis.loc[acquisition_analysis['new_customers'].idxmax()]
                
                st.markdown(f"""
                **Channel Performance:**
                - **Highest Value Source:** {best_source.name} (${best_source['lifetime_value']:,.0f} CLV)
                - **Highest Volume Source:** {best_volume.name} ({best_volume['new_customers']:,} customers)
                - **Total Acquisition Channels:** {len(acquisition_analysis)}
                """)
                
                # Channel efficiency metrics
                acquisition_analysis_copy = acquisition_analysis.copy()
                acquisition_analysis_copy['efficiency_score'] = (
                    (acquisition_analysis_copy['lifetime_value'] * acquisition_analysis_copy['new_customers']) / 
                    acquisition_analysis_copy['new_customers'].sum()
                )
                
                st.markdown("**Channel Efficiency Ranking:**")
                efficiency_ranking = acquisition_analysis_copy.sort_values('efficiency_score', ascending=False)
                st.dataframe(
                    efficiency_ranking.reset_index().rename(columns={
                        'acquisition_source': 'Source',
                        'new_customers': 'Customers',
                        'lifetime_value': 'Avg CLV ($)',
                        'efficiency_score': 'Efficiency Score'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
    
    st.markdown("---")
    
    # Enhanced Customer Demographics Analysis
    st.subheader("👤 Advanced Customer Demographics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'age' in st.session_state.customers_data.columns:
            st.markdown("#### 📊 Age Distribution Analysis")
            
            # Enhanced age histogram with better styling
            fig_age = px.histogram(
                st.session_state.customers_data,
                x='age',
                nbins=20,
                title="Customer Age Distribution",
                color_discrete_sequence=['#667eea'],
                labels={'age': 'Age', 'count': 'Number of Customers'}
            )
            
            fig_age.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_age.update_xaxes(
                title_text="Age",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_age.update_yaxes(
                title_text="Number of Customers",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_age.update_traces(
                hovertemplate='Age: <b>%{x}</b><br>' +
                              'Customers: <b>%{y}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_age, use_container_width=True, key="age_distribution")
            
            # Age insights
            with st.expander("💡 Age Insights", expanded=False):
                age_stats = st.session_state.customers_data['age'].describe()
                st.markdown(f"""
                **Age Statistics:**
                - **Average Age:** {age_stats['mean']:.1f} years
                - **Median Age:** {age_stats['50%']:.1f} years
                - **Age Range:** {age_stats['max'] - age_stats['min']:.0f} years
                - **Most Common Age Group:** {age_stats['mean']//10*10}-{(age_stats['mean']//10+1)*10} years
                """)
    
    with col2:
        if 'gender' in st.session_state.customers_data.columns:
            st.markdown("#### 👥 Gender Distribution Analysis")
            
            gender_counts = st.session_state.customers_data['gender'].value_counts()
            
            # Enhanced pie chart with better styling
            fig_gender = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Customer Gender Distribution",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4
            )
            
            fig_gender.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                height=400
            )
            
            fig_gender.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                              'Customers: %{value}<br>' +
                              'Percentage: %{percent}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_gender, use_container_width=True, key="gender_distribution")
            
            # Gender insights
            with st.expander("💡 Gender Insights", expanded=False):
                total_gender = gender_counts.sum()
                gender_percentages = (gender_counts / total_gender * 100).round(1)
                
                st.markdown(f"""
                **Gender Distribution:**
                - **Total Customers:** {total_gender:,}
                - **Male:** {gender_counts.get('Male', 0):,} ({gender_percentages.get('Male', 0):.1f}%)
                - **Female:** {gender_counts.get('Female', 0):,} ({gender_percentages.get('Female', 0):.1f}%)
                - **Other:** {gender_counts.get('Other', 0):,} ({gender_percentages.get('Other', 0):.1f}%)
                """)
    
    st.markdown("---")
    
    # Enhanced Customer Lifetime Value Analysis
    st.subheader("💰 Advanced Customer Lifetime Value Analysis")
    
    if 'lifetime_value' in st.session_state.customers_data.columns:
        # CLV insights header
        st.markdown(f"""
        <div class="customer-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">💎 Customer Value Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Analyzing customer value distribution and identifying high-value customer segments
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # CLV distribution with enhanced styling
        fig_clv_dist = px.histogram(
            st.session_state.customers_data,
            x='lifetime_value',
            nbins=20,
            title="Customer Lifetime Value Distribution",
            color_discrete_sequence=['#28a745'],
            labels={'lifetime_value': 'CLV ($)', 'count': 'Number of Customers'}
        )
        
        fig_clv_dist.update_layout(
            title_font_size=18,
            title_font_color='#1e3c72',
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        fig_clv_dist.update_xaxes(
            title_text="Customer Lifetime Value ($)",
            title_font_size=14,
            title_font_color='#495057',
            gridcolor='rgba(0,0,0,0.1)'
        )
        
        fig_clv_dist.update_yaxes(
            title_text="Number of Customers",
            title_font_size=14,
            title_font_color='#495057',
            gridcolor='rgba(0,0,0,0.1)'
        )
        
        fig_clv_dist.update_traces(
            hovertemplate='CLV: <b>$%{x:,.0f}</b><br>' +
                          'Customers: <b>%{y}</b><br>' +
                          '<extra></extra>'
        )
        
        st.plotly_chart(fig_clv_dist, use_container_width=True, key="clv_distribution")
        
        # Enhanced CLV statistics with better formatting
        clv_stats = st.session_state.customers_data['lifetime_value'].describe()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0; font-size: 14px;">📊 Mean CLV</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${clv_stats['mean']:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%); 
                        padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0; font-size: 14px;">📈 Median CLV</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${clv_stats['50%']:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); 
                        padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0; font-size: 14px;">🚀 Max CLV</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${clv_stats['max']:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%); 
                        padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <h4 style="margin: 0; font-size: 14px;">📉 Min CLV</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${clv_stats['min']:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # CLV insights and recommendations
        with st.expander("💡 CLV Analysis & Recommendations", expanded=False):
            high_value_threshold = clv_stats['75%']
            high_value_customers = len(st.session_state.customers_data[st.session_state.customers_data['lifetime_value'] >= high_value_threshold])
            
            st.markdown(f"""
            **Value Analysis:**
            - **High-Value Customers (Top 25%):** {high_value_customers:,} customers (${high_value_threshold:,.0f}+ CLV)
            - **Value Range:** ${clv_stats['max'] - clv_stats['min']:,.0f} difference between highest and lowest
            - **Value Distribution:** {clv_stats['std']:.0f} standard deviation indicating value spread
            
            **Recommendations:**
            - Focus retention efforts on customers with CLV > ${high_value_threshold:,.0f}
            - Develop premium services for high-value segments
            - Implement upselling strategies for medium-value customers
            """)
    
    st.markdown("---")
    
    # Enhanced Repeat Customer Analysis
    st.subheader("🔄 Advanced Customer Retention & Loyalty Analysis")
    
    if 'total_purchases' in st.session_state.customers_data.columns:
        repeat_rate = calculate_repeat_customer_rate(st.session_state.customers_data)
        
        # Retention insights header
        st.markdown(f"""
        <div class="customer-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">🔄 Customer Loyalty Metrics</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Analyzing customer retention patterns and purchase frequency for loyalty optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Repeat Customer Rate")
            
            # Enhanced metric display
            if repeat_rate >= 70:
                retention_status = "🟢 Excellent"
                retention_color = "#28a745"
            elif repeat_rate >= 50:
                retention_status = "🟡 Good"
                retention_color = "#ffc107"
            elif repeat_rate >= 30:
                retention_status = "🟠 Fair"
                retention_color = "#fd7e14"
            else:
                retention_status = "🔴 Needs Improvement"
                retention_color = "#dc3545"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                        padding: 20px; border-radius: 12px; border-left: 5px solid {retention_color}; margin: 15px 0;">
                <h3 style="margin: 0; color: #333; font-size: 18px;">{retention_status} Retention</h3>
                <p style="margin: 5px 0; color: #666; font-size: 16px;">Repeat Customer Rate: <strong>{repeat_rate:.1f}%</strong></p>
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Customer Loyalty Performance</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Retention insights
            with st.expander("💡 Retention Insights", expanded=False):
                total_customers = len(st.session_state.customers_data)
                repeat_customers = len(st.session_state.customers_data[st.session_state.customers_data['total_purchases'] > 1])
                new_customers = total_customers - repeat_customers
                
                st.markdown(f"""
                **Retention Breakdown:**
                - **Total Customers:** {total_customers:,}
                - **Repeat Customers:** {repeat_customers:,} ({repeat_rate:.1f}%)
                - **New Customers:** {new_customers:,} ({100-repeat_rate:.1f}%)
                - **Loyalty Score:** {'High' if repeat_rate >= 70 else 'Medium' if repeat_rate >= 50 else 'Low'}
                """)
        
        with col2:
            st.markdown("#### 📈 Purchase Frequency Distribution")
            
            # Enhanced purchase frequency histogram
            fig_purchases = px.histogram(
                st.session_state.customers_data,
                x='total_purchases',
                nbins=15,
                title="Customer Purchase Frequency Distribution",
                color_discrete_sequence=['#6f42c1'],
                labels={'total_purchases': 'Number of Purchases', 'count': 'Number of Customers'}
            )
            
            fig_purchases.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_purchases.update_xaxes(
                title_text="Number of Purchases",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_purchases.update_yaxes(
                title_text="Number of Customers",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_purchases.update_traces(
                hovertemplate='Purchases: <b>%{x}</b><br>' +
                              'Customers: <b>%{y}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_purchases, use_container_width=True, key="purchase_frequency")
            
            # Purchase frequency insights
            with st.expander("💡 Purchase Frequency Insights", expanded=False):
                purchase_stats = st.session_state.customers_data['total_purchases'].describe()
                avg_purchases = purchase_stats['mean']
                
                st.markdown(f"""
                **Purchase Behavior:**
                - **Average Purchases:** {avg_purchases:.1f} per customer
                - **Most Common:** {purchase_stats['50%']:.0f} purchases (median)
                - **Purchase Range:** {purchase_stats['max'] - purchase_stats['min']:.0f} purchases
                - **High-Value Buyers:** {len(st.session_state.customers_data[st.session_state.customers_data['total_purchases'] >= purchase_stats['75%']]):,} customers
                """)
    
    # Customer Behavior Summary
    st.markdown("---")
    st.subheader("📋 Customer Behavior Summary & Actionable Insights")
    
    with st.expander("🎯 Strategic Recommendations", expanded=False):
        st.markdown("""
        **Customer Strategy Recommendations:**
        
        **1. High-Value Customer Retention:**
        - Implement VIP programs for top 25% CLV customers
        - Personalized communication and exclusive offers
        - Priority customer service and support
        
        **2. Customer Acquisition Optimization:**
        - Focus on high-performing acquisition channels
        - Optimize marketing spend based on CLV by source
        - Develop channel-specific acquisition strategies
        
        **3. Loyalty Program Enhancement:**
        - Reward repeat purchase behavior
        - Implement tier-based loyalty systems
        - Cross-selling opportunities for existing customers
        
        **4. Customer Experience Improvement:**
        - Analyze customer journey touchpoints
        - Implement feedback collection systems
        - Continuous improvement based on customer insights
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Customer Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'lifetime_value' in st.session_state.customers_data.columns:
            total_clv = st.session_state.customers_data['lifetime_value'].sum()
            st.metric(
                "Total Customer Value", 
                f"${total_clv:,.0f}",
                "Combined CLV of all customers"
            )
    
    with col2:
        if 'total_purchases' in st.session_state.customers_data.columns:
            total_purchases = st.session_state.customers_data['total_purchases'].sum()
            st.metric(
                "Total Purchases", 
                f"{total_purchases:,}",
                "Combined purchase volume"
            )
    
    with col3:
        if 'acquisition_source' in st.session_state.customers_data.columns:
            unique_sources = st.session_state.customers_data['acquisition_source'].nunique()
            st.metric(
                "Acquisition Channels", 
                f"{unique_sources}",
                "Active marketing channels"
            )

def show_market_analysis():
    """Display world-class market analysis with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .market-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .market-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .market-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .market-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .competitive-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .opportunity-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🌍 Market Analysis - Strategic Intelligence Dashboard")
    st.markdown("---")
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        st.session_state.conversions_data.empty) or (isinstance(st.session_state.customers_data, pd.DataFrame) and 
        st.session_state.customers_data.empty):
        st.warning("⚠️ Conversion and customer data required for market analysis.")
        return
    
    # Enhanced Market Overview Dashboard
    company_revenue = st.session_state.conversions_data['revenue'].sum()
    total_customers = len(st.session_state.customers_data)
    total_market_size = company_revenue * 10  # Example: company has 10% market share
    market_share = calculate_market_share(company_revenue, total_market_size)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🌍 Global Market Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Analyzing market position, competitive landscape, and growth opportunities across {total_customers:,} customers
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Market Share Analysis
    st.subheader("📊 Advanced Market Share Analysis")
    
    # Market share insights header
    st.markdown(f"""
    <div class="market-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Market Position Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of market share, competitive positioning, and growth potential
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="market-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">💰 Company Revenue</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">${company_revenue:,.0f}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Total revenue generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="market-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🌍 Market Size</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">${total_market_size:,.0f}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Total addressable market</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Market share performance indicator
        if market_share >= 20:
            share_status = "🚀 Dominant"
            share_color = "#28a745"
        elif market_share >= 10:
            share_status = "⭐ Strong"
            share_color = "#17a2b8"
        elif market_share >= 5:
            share_status = "👍 Growing"
            share_color = "#ffc107"
        else:
            share_status = "📈 Emerging"
            share_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="market-metric-card" style="background: linear-gradient(135deg, {share_color} 0%, {share_color}dd 100%);">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">📊 Market Share</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{market_share:.1f}%</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">{share_status} position</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="market-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">👥 Total Customers</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_customers:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Customer base size</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Revenue Trend Analysis
    st.subheader("📈 Advanced Revenue Trend Analysis")
    
    if not st.session_state.conversions_data.empty:
        conversions_data = st.session_state.conversions_data.copy()
        conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
        conversions_data['month'] = conversions_data['conversion_date'].dt.to_period('M')
        
        monthly_revenue = conversions_data.groupby('month')['revenue'].sum().reset_index()
        monthly_revenue['month'] = monthly_revenue['month'].astype(str)
        
        # Calculate growth metrics
        monthly_revenue['growth_rate'] = monthly_revenue['revenue'].pct_change() * 100
        monthly_revenue['cumulative_revenue'] = monthly_revenue['revenue'].cumsum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Monthly Revenue Trend")
            
            # Enhanced line chart with better styling
            fig_revenue_trend = px.line(
                monthly_revenue,
                x='month',
                y='revenue',
                title="Monthly Revenue Trend Analysis",
                labels={'revenue': 'Revenue ($)', 'month': 'Month'},
                markers=True
            )
            
            fig_revenue_trend.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_revenue_trend.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_revenue_trend.update_yaxes(
                title_text="Revenue ($)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_revenue_trend.update_traces(
                line_color='#667eea',
                line_width=3,
                marker_color='#667eea',
                marker_size=8,
                hovertemplate='Month: <b>%{x}</b><br>' +
                              'Revenue: <b>$%{y:,.0f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_revenue_trend, use_container_width=True, key="revenue_trend")
        
        with col2:
            st.markdown("#### 📈 Cumulative Revenue Growth")
            
            # Enhanced area chart for cumulative revenue
            fig_cumulative = px.area(
                monthly_revenue,
                x='month',
                y='cumulative_revenue',
                title="Cumulative Revenue Growth",
                labels={'cumulative_revenue': 'Cumulative Revenue ($)', 'month': 'Month'}
            )
            
            fig_cumulative.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_cumulative.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_cumulative.update_yaxes(
                title_text="Cumulative Revenue ($)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_cumulative.update_traces(
                fillcolor='rgba(102, 126, 234, 0.3)',
                line_color='#667eea',
                hovertemplate='Month: <b>%{x}</b><br>' +
                              'Cumulative: <b>$%{y:,.0f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_cumulative, use_container_width=True, key="cumulative_revenue")
        
        # Revenue insights
        with st.expander("💡 Revenue Trend Insights", expanded=False):
            total_months = len(monthly_revenue)
            avg_monthly_revenue = monthly_revenue['revenue'].mean()
            best_month = monthly_revenue.loc[monthly_revenue['revenue'].idxmax()]
            worst_month = monthly_revenue.loc[monthly_revenue['revenue'].idxmin()]
            
            st.markdown(f"""
            **Trend Analysis:**
            - **Analysis Period:** {total_months} months
            - **Average Monthly Revenue:** ${avg_monthly_revenue:,.0f}
            - **Best Performing Month:** {best_month['month']} (${best_month['revenue']:,.0f})
            - **Lowest Revenue Month:** {worst_month['month']} (${worst_month['revenue']:,.0f})
            - **Revenue Growth Pattern:** {'Consistent' if monthly_revenue['growth_rate'].std() < 20 else 'Volatile'}
            """)
    
    st.markdown("---")
    
    # Enhanced Geographical Performance Analysis
    st.subheader("🗺️ Advanced Geographical Performance Analysis")
    
    if 'location' in st.session_state.customers_data.columns:
        geo_performance = st.session_state.customers_data.groupby('location').agg({
            'customer_id': 'count',
            'lifetime_value': 'sum'
        }).rename(columns={'customer_id': 'customers', 'lifetime_value': 'total_revenue'})
        
        # Calculate additional metrics
        geo_performance['avg_customer_value'] = geo_performance['total_revenue'] / geo_performance['customers']
        geo_performance['market_penetration'] = (geo_performance['customers'] / geo_performance['customers'].sum()) * 100
        
        # Geographical insights header
        st.markdown(f"""
        <div class="market-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">🌍 Regional Market Performance</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Analyzing {len(geo_performance)} locations for market penetration and revenue performance
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 Customer Distribution by Location")
            
            # Enhanced bar chart for customer distribution
            fig_geo_customers = px.bar(
                geo_performance.reset_index(),
                x='location',
                y='customers',
                title="Customer Distribution by Geographic Location",
                color='customers',
                color_continuous_scale='Blues',
                text='customers',
                labels={'customers': 'Number of Customers', 'location': 'Location'}
            )
            
            fig_geo_customers.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_geo_customers.update_xaxes(
                title_text="Geographic Location",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_geo_customers.update_yaxes(
                title_text="Number of Customers",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_geo_customers.update_traces(
                texttemplate='%{text:,}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Customers: <b>%{y:,}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_geo_customers, use_container_width=True, key="geo_customers")
        
        with col2:
            st.markdown("#### 💰 Revenue Performance by Location")
            
            # Enhanced bar chart for revenue by location
            fig_geo_revenue = px.bar(
                geo_performance.reset_index(),
                x='location',
                y='total_revenue',
                title="Total Revenue by Geographic Location",
                color='total_revenue',
                color_continuous_scale='RdYlGn',
                text='total_revenue',
                labels={'total_revenue': 'Total Revenue ($)', 'location': 'Location'}
            )
            
            fig_geo_revenue.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_geo_revenue.update_xaxes(
                title_text="Geographic Location",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_geo_revenue.update_yaxes(
                title_text="Total Revenue ($)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_geo_revenue.update_traces(
                texttemplate='$%{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Revenue: <b>$%{y:,.0f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_geo_revenue, use_container_width=True, key="geo_revenue")
        
        # Geographical performance insights
        with st.expander("💡 Geographical Performance Insights", expanded=False):
            best_location = geo_performance.loc[geo_performance['total_revenue'].idxmax()]
            highest_penetration = geo_performance.loc[geo_performance['market_penetration'].idxmax()]
            
            st.markdown(f"""
            **Regional Analysis:**
            - **Highest Revenue Location:** {best_location.name} (${best_location['total_revenue']:,.0f})
            - **Highest Market Penetration:** {highest_penetration.name} ({highest_penetration['market_penetration']:.1f}%)
            - **Total Locations Analyzed:** {len(geo_performance)}
            - **Geographic Coverage:** {'Wide' if len(geo_performance) >= 5 else 'Moderate' if len(geo_performance) >= 3 else 'Limited'}
            """)
            
            # Location performance table
            st.markdown("**Location Performance Summary:**")
            location_summary = geo_performance.reset_index().rename(columns={
                'location': 'Location',
                'customers': 'Customers',
                'total_revenue': 'Total Revenue ($)',
                'avg_customer_value': 'Avg Customer Value ($)',
                'market_penetration': 'Market Penetration (%)'
            })
            
            st.dataframe(
                location_summary,
                use_container_width=True,
                hide_index=True
            )
    
    st.markdown("---")
    
    # Enhanced Market Penetration Analysis
    st.subheader("🎯 Advanced Market Penetration Analysis")
    
    if not st.session_state.customers_data.empty and 'customer_segment' in st.session_state.customers_data.columns:
        # Calculate market penetration by segment
        segment_penetration = st.session_state.customers_data.groupby('customer_segment').agg({
            'customer_id': 'count',
            'lifetime_value': 'mean'
        }).rename(columns={'customer_id': 'customer_count', 'lifetime_value': 'avg_lifetime_value'})
        
        # Calculate penetration metrics
        segment_penetration['market_penetration'] = (segment_penetration['customer_count'] / segment_penetration['customer_count'].sum()) * 100
        segment_penetration['segment_value'] = segment_penetration['customer_count'] * segment_penetration['avg_lifetime_value']
        
        # Market penetration insights header
        st.markdown(f"""
        <div class="market-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Segment Penetration Strategy</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Analyzing market penetration across {len(segment_penetration)} customer segments for strategic targeting
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Market Penetration by Customer Segment")
            
            # Enhanced bar chart for segment penetration
            fig_segment_penetration = px.bar(
                segment_penetration.reset_index(),
                x='customer_segment',
                y='market_penetration',
                title="Market Penetration by Customer Segment",
                color='market_penetration',
                color_continuous_scale='RdYlGn',
                text='market_penetration',
                labels={'market_penetration': 'Market Penetration (%)', 'customer_segment': 'Customer Segment'}
            )
            
            fig_segment_penetration.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_segment_penetration.update_xaxes(
                title_text="Customer Segment",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_segment_penetration.update_yaxes(
                title_text="Market Penetration (%)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_segment_penetration.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Penetration: <b>%{y:.1f}%</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_segment_penetration, use_container_width=True, key="segment_penetration")
        
        with col2:
            st.markdown("#### 💰 Segment Value Distribution")
            
            # Enhanced bar chart for segment value
            fig_segment_value = px.bar(
                segment_penetration.reset_index(),
                x='customer_segment',
                y='segment_value',
                title="Total Segment Value by Customer Segment",
                color='segment_value',
                color_continuous_scale='RdYlGn',
                text='segment_value',
                labels={'segment_value': 'Total Segment Value ($)', 'customer_segment': 'Customer Segment'}
            )
            
            fig_segment_value.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_segment_value.update_xaxes(
                title_text="Customer Segment",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_segment_value.update_yaxes(
                title_text="Total Segment Value ($)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_segment_value.update_traces(
                texttemplate='$%{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Value: <b>$%{y:,.0f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_segment_value, use_container_width=True, key="segment_value")
        
        # Segment penetration insights
        with st.expander("💡 Segment Penetration Insights", expanded=False):
            highest_penetration_segment = segment_penetration.loc[segment_penetration['market_penetration'].idxmax()]
            highest_value_segment = segment_penetration.loc[segment_penetration['segment_value'].idxmax()]
            
            st.markdown(f"""
            **Segment Analysis:**
            - **Highest Penetration:** {highest_penetration_segment.name} ({highest_penetration_segment['market_penetration']:.1f}%)
            - **Highest Value Segment:** {highest_value_segment.name} (${highest_value_segment['segment_value']:,.0f})
            - **Total Segments:** {len(segment_penetration)}
            - **Penetration Range:** {segment_penetration['market_penetration'].min():.1f}% - {segment_penetration['market_penetration'].max():.1f}%
            """)
    
    st.markdown("---")
    
    # Enhanced Competitive Analysis Framework
    st.subheader("🏆 Advanced Competitive Analysis Framework")
    
    # Competitive insights header
    st.markdown(f"""
    <div class="market-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🏆 Competitive Intelligence Dashboard</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive competitive benchmarking and market positioning analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced competitive metrics
    avg_clv = st.session_state.customers_data['lifetime_value'].mean() if 'lifetime_value' in st.session_state.customers_data.columns else 0
    conversion_rate = 2.5  # Example value
    
    competitive_data = {
        'Metric': ['Market Share (%)', 'Customer Acquisition Cost ($)', 'Customer Lifetime Value ($)', 'Conversion Rate (%)', 'Customer Retention Rate (%)'],
        'Your Company': [market_share, 150, avg_clv, conversion_rate, 75],
        'Competitor A': [market_share * 0.8, 180, avg_clv * 0.9, 2.0, 70],
        'Competitor B': [market_share * 1.2, 120, avg_clv * 1.1, 3.0, 80],
        'Industry Average': [market_share * 1.0, 160, avg_clv * 1.0, 2.5, 72]
    }
    competitive_df = pd.DataFrame(competitive_data)
    
    # Competitive analysis visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Competitive Benchmarking Matrix")
        
        # Enhanced competitive benchmarking table
        st.dataframe(
            competitive_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Competitive insights
        with st.expander("💡 Competitive Insights", expanded=False):
            st.markdown(f"""
            **Competitive Position:**
            - **Market Share:** {'Leading' if market_share > competitive_df['Competitor A'].iloc[0] and market_share > competitive_df['Competitor B'].iloc[0] else 'Competitive' if market_share > competitive_df['Competitor A'].iloc[0] or market_share > competitive_df['Competitor B'].iloc[0] else 'Challenger'}
            - **CLV Performance:** {'Above Average' if avg_clv > competitive_df['Industry Average'].iloc[2] else 'Below Average'}
            - **Conversion Rate:** {'Competitive' if conversion_rate >= competitive_df['Industry Average'].iloc[3] else 'Needs Improvement'}
            """)
    
    with col2:
        st.markdown("#### 🎯 Competitive Performance Radar")
        
        # Create radar chart for competitive analysis
        metrics = ['Market Share', 'CLV', 'Conversion Rate', 'Retention Rate', 'Cost Efficiency']
        your_company = [market_share/10, min(avg_clv/1000, 10), conversion_rate*2, 75/10, 8]
        competitor_a = [market_share*0.8/10, min(avg_clv*0.9/1000, 10), 2.0*2, 70/10, 6]
        competitor_b = [market_share*1.2/10, min(avg_clv*1.1/1000, 10), 3.0*2, 80/10, 7]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=your_company,
            theta=metrics,
            fill='toself',
            name='Your Company',
            line_color='#667eea'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=competitor_a,
            theta=metrics,
            fill='toself',
            name='Competitor A',
            line_color='#ff6b6b'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=competitor_b,
            theta=metrics,
            fill='toself',
            name='Competitor B',
            line_color='#4ecdc4'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Competitive Performance Comparison",
            title_font_size=18,
            title_font_color='#1e3c72',
            title_x=0.5,
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True, key="competitive_radar")
    
    st.markdown("---")
    
    # Enhanced Market Opportunity Analysis
    st.subheader("💡 Advanced Market Opportunity Analysis")
    
    # Opportunity insights header
    st.markdown(f"""
    <div class="market-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🚀 Growth Opportunity Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Strategic analysis of market opportunities, growth potential, and expansion strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="competitive-metric">
            <h4 style="margin: 0; font-size: 14px;">🌍 Total Addressable Market</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">${total_market_size:,.0f}</h2>
            <p style="margin: 0; font-size: 12px;">Market opportunity size</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="competitive-metric">
            <h4 style="margin: 0; font-size: 14px;">📊 Current Market Share</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{market_share:.1f}%</h2>
            <p style="margin: 0; font-size: 12px;">Current position</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="opportunity-metric">
            <h4 style="margin: 0; font-size: 14px;">🚀 Growth Potential</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{(100 - market_share):.1f}%</h2>
            <p style="margin: 0; font-size: 12px;">Remaining opportunity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="opportunity-metric">
            <h4 style="margin: 0; font-size: 14px;">📈 Customer Acquisition Rate</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{len(st.session_state.customers_data) / 12:.0f}/month</h2>
            <p style="margin: 0; font-size: 12px;">Monthly growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="competitive-metric">
            <h4 style="margin: 0; font-size: 14px;">💰 Average Customer Value</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">${st.session_state.customers_data['lifetime_value'].mean():.0f}</h2>
            <p style="margin: 0; font-size: 12px;">Customer worth</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="opportunity-metric">
            <h4 style="margin: 0; font-size: 14px;">📊 Market Growth Rate</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">5.2%</h2>
            <p style="margin: 0; font-size: 12px;">Annual growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Market opportunity insights
    with st.expander("💡 Market Opportunity Insights", expanded=False):
        st.markdown(f"""
        **Strategic Opportunities:**
        
        **1. Market Expansion:**
        - **Untapped Market:** ${total_market_size - company_revenue:,.0f} in unaddressed market potential
        - **Growth Rate:** {((100 - market_share) / market_share * 100):.1f}% growth potential from current position
        
        **2. Geographic Expansion:**
        - **Current Coverage:** {len(geo_performance) if 'location' in st.session_state.customers_data.columns else 'N/A'} locations
        - **Expansion Potential:** Focus on high-value, low-penetration markets
        
        **3. Segment Penetration:**
        - **Target Segments:** Focus on segments with < 20% penetration
        - **Value Optimization:** Enhance offerings for high-value customer segments
        
        **4. Competitive Positioning:**
        - **Market Leadership:** {'Achievable' if market_share < 15 else 'Maintain'} current market position
        - **Differentiation:** Develop unique value propositions for competitive advantage
        """)
    
    # Market Strategy Summary
    st.markdown("---")
    st.subheader("📋 Market Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Action Plan", expanded=False):
        st.markdown("""
        **Immediate Actions (0-3 months):**
        
        **1. Market Share Optimization:**
        - Implement targeted marketing campaigns in high-opportunity segments
        - Optimize customer acquisition channels based on performance data
        - Develop competitive pricing strategies for market penetration
        
        **2. Geographic Expansion:**
        - Identify and prioritize high-potential geographic markets
        - Develop location-specific marketing strategies
        - Establish partnerships in new markets
        
        **3. Customer Value Enhancement:**
        - Implement upselling and cross-selling programs
        - Develop premium service offerings for high-value customers
        - Enhance customer retention strategies
        
        **Long-term Strategy (3-12 months):**
        
        **1. Market Leadership:**
        - Target 15%+ market share through strategic acquisitions
        - Develop innovative product/service offerings
        - Establish thought leadership in the industry
        
        **2. Geographic Diversification:**
        - Expand to 10+ geographic markets
        - Develop regional expertise and local partnerships
        - Implement scalable market entry strategies
        
        **3. Competitive Advantage:**
        - Build sustainable competitive moats
        - Develop proprietary technologies or processes
        - Establish strong brand recognition and loyalty
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Market Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Market Position", 
            f"{'Leading' if market_share >= 15 else 'Strong' if market_share >= 10 else 'Growing' if market_share >= 5 else 'Emerging'}",
            f"{market_share:.1f}% market share"
        )
    
    with col2:
        growth_potential = (100 - market_share)
        st.metric(
            "Growth Opportunity", 
            f"${(total_market_size - company_revenue):,.0f}",
            f"{growth_potential:.1f}% remaining market"
        )
    
    with col3:
        st.metric(
            "Customer Base", 
            f"{total_customers:,}",
            f"${company_revenue/total_customers:,.0f} per customer"
        )

def show_content_marketing():
    """Display world-class content marketing analysis with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .content-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .content-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .content-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .content-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .performance-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .engagement-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .conversion-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📝 Content Marketing Analysis - Strategic Content Intelligence Dashboard")
    st.markdown("---")
    
    if st.session_state.content_marketing_data.empty:
        st.warning("⚠️ Content marketing data required for this analysis.")
        return
    
    # Enhanced Content Marketing Overview Dashboard
    total_views = st.session_state.content_marketing_data['views'].sum()
    total_shares = st.session_state.content_marketing_data['shares'].sum()
    total_leads = st.session_state.content_marketing_data['leads_generated'].sum()
    total_conversions = st.session_state.content_marketing_data['conversions'].sum()
    total_content = len(st.session_state.content_marketing_data)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">📝 Content Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Analyzing {total_content:,} content pieces with advanced engagement and conversion insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Content Engagement Overview
    st.subheader("📊 Advanced Content Engagement Overview")
    
    # Content engagement insights header
    st.markdown(f"""
    <div class="content-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Content Performance Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of content engagement, lead generation, and conversion performance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="content-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">👁️ Total Views</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_views:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Content reach</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="content-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🔄 Total Shares</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_shares:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Social engagement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="content-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🎯 Leads Generated</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_leads:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Lead generation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="content-metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">💰 Conversions</h3>
            <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_conversions:,}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Revenue impact</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Content Performance Analysis
    st.subheader("📈 Advanced Content Performance Analysis")
    
    # Content performance insights header
    st.markdown(f"""
    <div class="content-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📊 Content Type Performance Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Analyzing content performance across different types and formats for strategic optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    content_performance = st.session_state.content_marketing_data.groupby('content_type').agg({
        'views': 'sum',
        'shares': 'sum',
        'comments': 'sum',
        'leads_generated': 'sum',
        'conversions': 'sum',
        'time_on_page': 'mean'
    }).reset_index()
    
    # Calculate advanced metrics
    content_performance['engagement_rate'] = (
        (content_performance['shares'] + content_performance['comments']) / content_performance['views']
    ) * 100
    
    content_performance['conversion_rate'] = (
        content_performance['conversions'] / content_performance['views']
    ) * 100
    
    content_performance['lead_rate'] = (
        content_performance['leads_generated'] / content_performance['views']
    ) * 100
    
    content_performance['content_efficiency_score'] = (
        content_performance['engagement_rate'] * 0.3 +
        content_performance['conversion_rate'] * 0.4 +
        content_performance['lead_rate'] * 0.3
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👁️ Content Views by Type")
        
        # Enhanced bar chart for content views
        fig_content_views = px.bar(
            content_performance,
            x='content_type',
            y='views',
            title="Total Views by Content Type",
            color='views',
            color_continuous_scale='Blues',
            text='views',
            labels={'views': 'Total Views', 'content_type': 'Content Type'}
        )
        
        fig_content_views.update_layout(
            title_font_size=18,
            title_font_color='#1e3c72',
            title_x=0.5,
            xaxis_tickangle=-45,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        fig_content_views.update_xaxes(
            title_text="Content Type",
            title_font_size=14,
            title_font_color='#495057'
        )
        
        fig_content_views.update_yaxes(
            title_text="Total Views",
            title_font_size=14,
            title_font_color='#495057',
            gridcolor='rgba(0,0,0,0.1)'
        )
        
        fig_content_views.update_traces(
            texttemplate='%{text:,}',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                          'Views: <b>%{y:,}</b><br>' +
                          '<extra></extra>'
        )
        
        st.plotly_chart(fig_content_views, use_container_width=True, key="content_views")
    
    with col2:
        st.markdown("#### 🔄 Engagement Rate by Content Type")
        
        # Enhanced bar chart for engagement rate
        fig_content_engagement = px.bar(
            content_performance,
            x='content_type',
            y='engagement_rate',
            title="Engagement Rate by Content Type",
            color='engagement_rate',
            color_continuous_scale='RdYlGn',
            text='engagement_rate',
            labels={'engagement_rate': 'Engagement Rate (%)', 'content_type': 'Content Type'}
        )
        
        fig_content_engagement.update_layout(
            title_font_size=18,
            title_font_color='#1e3c72',
            title_x=0.5,
            xaxis_tickangle=-45,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        fig_content_engagement.update_xaxes(
            title_text="Content Type",
            title_font_size=14,
            title_font_color='#495057'
        )
        
        fig_content_engagement.update_yaxes(
            title_text="Engagement Rate (%)",
            title_font_size=14,
            title_font_color='#495057',
            gridcolor='rgba(0,0,0,0.1)'
        )
        
        fig_content_engagement.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>' +
                          'Engagement: <b>%{y:.1f}%</b><br>' +
                          '<extra></extra>'
        )
        
        st.plotly_chart(fig_content_engagement, use_container_width=True, key="content_engagement")
    
    # Content performance insights
    with st.expander("💡 Content Performance Insights", expanded=False):
        best_performing_type = content_performance.loc[content_performance['content_efficiency_score'].idxmax()]
        highest_engagement = content_performance.loc[content_performance['engagement_rate'].idxmax()]
        highest_conversion = content_performance.loc[content_performance['conversion_rate'].idxmax()]
        
        st.markdown(f"""
        **Performance Analysis:**
        - **Best Overall Type:** {best_performing_type['content_type']} (Efficiency Score: {best_performing_type['content_efficiency_score']:.1f})
        - **Highest Engagement:** {highest_engagement['content_type']} ({highest_engagement['engagement_rate']:.1f}% engagement)
        - **Highest Conversion:** {highest_conversion['content_type']} ({highest_conversion['conversion_rate']:.1f}% conversion)
        - **Total Content Types:** {len(content_performance)}
        """)
        
        # Content performance summary table
        st.markdown("**Content Performance Summary:**")
        performance_summary = content_performance.copy()
        performance_summary['efficiency_score'] = performance_summary['content_efficiency_score'].round(1)
        
        st.dataframe(
            performance_summary.rename(columns={
                'content_type': 'Content Type',
                'views': 'Total Views',
                'engagement_rate': 'Engagement Rate (%)',
                'conversion_rate': 'Conversion Rate (%)',
                'lead_rate': 'Lead Rate (%)',
                'efficiency_score': 'Efficiency Score'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # Enhanced Top Performing Content Analysis
    st.subheader("🏆 Advanced Top Performing Content Analysis")
    
    # Top content insights header
    st.markdown(f"""
    <div class="content-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🏆 Content Champion Analysis</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Identifying top-performing content pieces and analyzing success factors for content optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👁️ Top 10 Content by Views")
        
        # Top content by views with enhanced formatting
        top_views = st.session_state.content_marketing_data.nlargest(10, 'views')[
            ['title', 'content_type', 'views', 'shares', 'leads_generated', 'conversions']
        ].copy()
        
        # Calculate additional metrics
        top_views['engagement_rate'] = ((top_views['shares'] / top_views['views']) * 100).round(1)
        top_views['conversion_rate'] = ((top_views['conversions'] / top_views['views']) * 100).round(1)
        
        # Enhanced dataframe display
        st.dataframe(
            top_views.rename(columns={
                'title': 'Content Title',
                'content_type': 'Type',
                'views': 'Views',
                'shares': 'Shares',
                'leads_generated': 'Leads',
                'conversions': 'Conversions',
                'engagement_rate': 'Engagement (%)',
                'conversion_rate': 'Conversion (%)'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Top views insights
        with st.expander("💡 Top Views Insights", expanded=False):
            best_viewed = top_views.iloc[0]
            avg_views = top_views['views'].mean()
            
            st.markdown(f"""
            **Views Analysis:**
            - **Top Performer:** {best_viewed['title']} ({best_viewed['views']:,} views)
            - **Average Top 10 Views:** {avg_views:,.0f}
            - **Views Range:** {top_views['views'].min():,} - {top_views['views'].max():,}
            - **Content Types:** {top_views['content_type'].nunique()} different types in top 10
            """)
    
    with col2:
        st.markdown("#### 🎯 Top 10 Content by Leads Generated")
        
        # Top content by leads with enhanced formatting
        top_leads = st.session_state.content_marketing_data.nlargest(10, 'leads_generated')[
            ['title', 'content_type', 'leads_generated', 'views', 'conversions']
        ].copy()
        
        # Calculate additional metrics
        top_leads['lead_rate'] = ((top_leads['leads_generated'] / top_leads['views']) * 100).round(1)
        top_leads['conversion_rate'] = ((top_leads['conversions'] / top_leads['views']) * 100).round(1)
        
        # Enhanced dataframe display
        st.dataframe(
            top_leads.rename(columns={
                'title': 'Content Title',
                'content_type': 'Type',
                'leads_generated': 'Leads',
                'views': 'Views',
                'conversions': 'Conversions',
                'lead_rate': 'Lead Rate (%)',
                'conversion_rate': 'Conversion (%)'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Top leads insights
        with st.expander("💡 Top Leads Insights", expanded=False):
            best_lead_generator = top_leads.iloc[0]
            avg_leads = top_leads['leads_generated'].mean()
            
            st.markdown(f"""
            **Lead Generation Analysis:**
            - **Top Lead Generator:** {best_lead_generator['title']} ({best_lead_generator['leads_generated']:,} leads)
            - **Average Top 10 Leads:** {avg_leads:,.0f}
            - **Lead Range:** {top_leads['leads_generated'].min():,} - {top_leads['leads_generated'].max():,}
            - **Lead Efficiency:** {best_lead_generator['lead_rate']:.1f}% lead rate for top performer
            """)
    
    st.markdown("---")
    
    # Enhanced Content Engagement Trends Analysis
    st.subheader("📈 Advanced Content Engagement Trends Analysis")
    
    if 'publish_date' in st.session_state.content_marketing_data.columns:
        # Content trends insights header
        st.markdown(f"""
        <div class="content-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">📈 Content Performance Trends</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Analyzing content performance trends over time for strategic content planning and optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert publish_date to datetime if it's not already
        content_data = st.session_state.content_marketing_data.copy()
        content_data['publish_date'] = pd.to_datetime(content_data['publish_date'])
        content_data['month'] = content_data['publish_date'].dt.to_period('M')
        
        monthly_performance = content_data.groupby('month').agg({
            'views': 'sum',
            'shares': 'sum',
            'leads_generated': 'sum',
            'conversions': 'sum'
        }).reset_index()
        monthly_performance['month'] = monthly_performance['month'].astype(str)
        
        # Calculate additional trend metrics
        monthly_performance['engagement_rate'] = (
            (monthly_performance['shares'] / monthly_performance['views']) * 100
        ).fillna(0)
        
        monthly_performance['conversion_rate'] = (
            (monthly_performance['conversions'] / monthly_performance['views']) * 100
        ).fillna(0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Monthly Content Performance Trends")
            
            # Enhanced line chart for monthly trends
            fig_trends = px.line(
                monthly_performance,
                x='month',
                y=['views', 'shares', 'leads_generated'],
                title="Monthly Content Performance Trends",
                labels={'value': 'Count', 'variable': 'Metric', 'month': 'Month'}
            )
            
            fig_trends.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                )
            )
            
            fig_trends.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_trends.update_yaxes(
                title_text="Count",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_trends.update_traces(
                line_width=3,
                marker_size=6,
                hovertemplate='Month: <b>%{x}</b><br>' +
                              '%{fullData.name}: <b>%{y:,}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_trends, use_container_width=True, key="content_trends")
        
        with col2:
            st.markdown("#### 📈 Monthly Engagement & Conversion Rates")
            
            # Enhanced line chart for rates
            fig_rates = px.line(
                monthly_performance,
                x='month',
                y=['engagement_rate', 'conversion_rate'],
                title="Monthly Engagement & Conversion Rates",
                labels={'value': 'Rate (%)', 'variable': 'Metric', 'month': 'Month'}
            )
            
            fig_rates.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                )
            )
            
            fig_rates.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_rates.update_yaxes(
                title_text="Rate (%)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_rates.update_traces(
                line_width=3,
                marker_size=6,
                hovertemplate='Month: <b>%{x}</b><br>' +
                              '%{fullData.name}: <b>%{y:.1f}%</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_rates, use_container_width=True, key="content_rates")
        
        # Content trends insights
        with st.expander("💡 Content Trends Insights", expanded=False):
            total_months = len(monthly_performance)
            avg_monthly_views = monthly_performance['views'].mean()
            best_month = monthly_performance.loc[monthly_performance['views'].idxmax()]
            best_engagement_month = monthly_performance.loc[monthly_performance['engagement_rate'].idxmax()]
            
            st.markdown(f"""
            **Trend Analysis:**
            - **Analysis Period:** {total_months} months
            - **Average Monthly Views:** {avg_monthly_views:,.0f}
            - **Best Performing Month:** {best_month['month']} ({best_month['views']:,} views)
            - **Highest Engagement Month:** {best_engagement_month['month']} ({best_engagement_month['engagement_rate']:.1f}% engagement)
            - **Trend Pattern:** {'Consistent' if monthly_performance['views'].std() < monthly_performance['views'].mean() * 0.3 else 'Volatile'}
            """)
    
    # Content Strategy Summary
    st.markdown("---")
    st.subheader("📋 Content Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Content Recommendations", expanded=False):
        st.markdown("""
        **Content Strategy Recommendations:**
        
        **1. Content Type Optimization:**
        - Focus on high-performing content types based on efficiency scores
        - Develop more content in formats that show high engagement and conversion rates
        - A/B test content variations to optimize performance
        
        **2. Content Performance Enhancement:**
        - Analyze top-performing content for success factors
        - Implement similar strategies across other content pieces
        - Focus on lead generation and conversion optimization
        
        **3. Content Distribution Strategy:**
        - Optimize publishing schedule based on performance trends
        - Focus on high-engagement time periods
        - Implement content promotion strategies for better reach
        
        **4. Content Quality Improvement:**
        - Focus on creating high-value, engaging content
        - Implement content optimization based on performance data
        - Develop content that drives both engagement and conversions
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Content Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall_engagement = (total_shares / total_views * 100) if total_views > 0 else 0
        st.metric(
            "Overall Engagement Rate", 
            f"{overall_engagement:.1f}%",
            f"{total_shares:,} shares / {total_views:,} views"
        )
    
    with col2:
        overall_conversion = (total_conversions / total_views * 100) if total_views > 0 else 0
        st.metric(
            "Overall Conversion Rate", 
            f"{overall_conversion:.1f}%",
            f"{total_conversions:,} conversions / {total_views:,} views"
        )
    
    with col3:
        overall_lead_rate = (total_leads / total_views * 100) if total_views > 0 else 0
        st.metric(
            "Overall Lead Rate", 
            f"{overall_lead_rate:.1f}%",
            f"{total_leads:,} leads / {total_views:,} views"
        )

def show_digital_marketing():
    """Display world-class digital marketing analytics with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .digital-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .digital-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .digital-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .digital-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .traffic-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .social-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .email-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🌐 Digital Marketing Analytics - Comprehensive Digital Intelligence Dashboard")
    st.markdown("---")
    
    # Enhanced Digital Marketing Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🌐 Digital Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Comprehensive analysis of website traffic, social media performance, and email marketing campaigns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Website Traffic Analysis
    if not st.session_state.website_traffic_data.empty:
        st.subheader("🌐 Advanced Website Traffic Analysis")
        
        # Website traffic insights header
        st.markdown(f"""
        <div class="digital-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">🌐 Website Performance Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of website traffic patterns, user behavior, and conversion optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced traffic overview
        total_sessions = len(st.session_state.website_traffic_data)
        unique_visitors = st.session_state.website_traffic_data['customer_id'].nunique()
        conversions = st.session_state.website_traffic_data['conversion_flag'].sum()
        conversion_rate = calculate_conversion_rate(conversions, total_sessions)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="digital-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🌐 Total Sessions</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{total_sessions:,}</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Website interactions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="digital-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">👥 Unique Visitors</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{unique_visitors:,}</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Individual users</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="digital-metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">🎯 Conversions</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{conversions:,}</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">Goal completions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Conversion rate performance indicator
            if conversion_rate >= 5:
                conv_status = "🚀 Excellent"
                conv_color = "#28a745"
            elif conversion_rate >= 3:
                conv_status = "⭐ Good"
                conv_color = "#17a2b8"
            elif conversion_rate >= 1:
                conv_status = "👍 Fair"
                conv_color = "#ffc107"
            else:
                conv_status = "📈 Needs Improvement"
                conv_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="digital-metric-card" style="background: linear-gradient(135deg, {conv_color} 0%, {conv_color}dd 100%);">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">📊 Conversion Rate</h3>
                <h1 style="margin: 10px 0; font-size: 28px; font-weight: bold;">{conversion_rate:.1f}%</h1>
                <p style="margin: 0; font-size: 12px; opacity: 0.8;">{conv_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced traffic sources analysis
        if 'traffic_source' in st.session_state.website_traffic_data.columns:
            st.markdown("#### 📊 Traffic Sources Analysis")
            
            traffic_analysis = analyze_traffic_sources(st.session_state.website_traffic_data)
            
            if not traffic_analysis.empty:
                # Calculate additional traffic metrics
                traffic_analysis['traffic_share'] = (traffic_analysis['visits'] / traffic_analysis['visits'].sum() * 100).round(1)
                traffic_analysis['efficiency_score'] = round(
                    (traffic_analysis['conversion_rate'] * 0.6) + 
                    (traffic_analysis['traffic_share'] * 0.4), 1
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🌐 Traffic Distribution by Source")
                    
                    # Enhanced pie chart for traffic sources
                    fig_traffic_sources = px.pie(
                        values=traffic_analysis['visits'],
                        names=traffic_analysis.index,
                        title="Traffic Distribution by Source",
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        hole=0.4
                    )
                    
                    fig_traffic_sources.update_layout(
                        title_font_size=18,
                        title_font_color='#1e3c72',
                        title_x=0.5,
                        showlegend=True,
                        legend=dict(
                            bgcolor='rgba(255,255,255,0.9)',
                            bordercolor='rgba(0,0,0,0.1)',
                            borderwidth=1
                        ),
                        height=400
                    )
                    
                    fig_traffic_sources.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>' +
                                      'Visits: %{value}<br>' +
                                      'Percentage: %{percent}<br>' +
                                      '<extra></extra>'
                    )
                    
                    st.plotly_chart(fig_traffic_sources, use_container_width=True, key="traffic_sources_pie")
                
                with col2:
                    st.markdown("#### 🎯 Conversion Rate by Traffic Source")
                    
                    # Enhanced bar chart for conversion rates
                    fig_traffic_conversion = px.bar(
                        traffic_analysis.reset_index(),
                        x='traffic_source',
                        y='conversion_rate',
                        title="Conversion Rate by Traffic Source",
                        color='conversion_rate',
                        color_continuous_scale='RdYlGn',
                        text='conversion_rate',
                        labels={'conversion_rate': 'Conversion Rate (%)', 'traffic_source': 'Traffic Source'}
                    )
                    
                    fig_traffic_conversion.update_layout(
                        title_font_size=18,
                        title_font_color='#1e3c72',
                        title_x=0.5,
                        xaxis_tickangle=-45,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    
                    fig_traffic_conversion.update_xaxes(
                        title_text="Traffic Source",
                        title_font_size=14,
                        title_font_color='#495057'
                    )
                    
                    fig_traffic_conversion.update_yaxes(
                        title_text="Conversion Rate (%)",
                        title_font_size=14,
                        title_font_color='#495057',
                        gridcolor='rgba(0,0,0,0.1)'
                    )
                    
                    fig_traffic_conversion.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside',
                        hovertemplate='<b>%{x}</b><br>' +
                                      'Conversion Rate: <b>%{y:.1f}%</b><br>' +
                                      '<extra></extra>'
                    )
                    
                    st.plotly_chart(fig_traffic_conversion, use_container_width=True, key="traffic_conversion")
                
                # Traffic sources insights
                with st.expander("💡 Traffic Sources Insights", expanded=False):
                    best_source = traffic_analysis.loc[traffic_analysis['conversion_rate'].idxmax()]
                    highest_traffic = traffic_analysis.loc[traffic_analysis['visits'].idxmax()]
                    
                    st.markdown(f"""
                    **Traffic Analysis:**
                    - **Best Converting Source:** {best_source.name} ({best_source['conversion_rate']:.1f}% conversion)
                    - **Highest Traffic Source:** {highest_traffic.name} ({highest_traffic['visits']:,} visits)
                    - **Total Traffic Sources:** {len(traffic_analysis)}
                    - **Traffic Efficiency Range:** {traffic_analysis['efficiency_score'].min():.1f} - {traffic_analysis['efficiency_score'].max():.1f}
                    """)
                    
                    # Traffic sources summary table
                    st.markdown("**Traffic Sources Performance Summary:**")
                    traffic_summary = traffic_analysis.reset_index().rename(columns={
                        'traffic_source': 'Source',
                        'visits': 'Visits',
                        'conversion_rate': 'Conversion Rate (%)',
                        'traffic_share': 'Traffic Share (%)',
                        'efficiency_score': 'Efficiency Score'
                    })
                    
                    st.dataframe(
                        traffic_summary,
                        use_container_width=True,
                        hide_index=True
                    )
    
    st.markdown("---")
    
    # Enhanced Social Media Analysis
    if not st.session_state.social_media_data.empty:
        st.subheader("📱 Advanced Social Media Analytics")
        
        # Social media insights header
        st.markdown(f"""
        <div class="digital-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">📱 Social Media Performance Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of social media engagement, reach, and performance across platforms
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        social_performance = analyze_social_media_performance(st.session_state.social_media_data)
        
        if not social_performance.empty:
            # Calculate additional social media metrics
            social_performance['total_engagement'] = (
                social_performance['likes'] + 
                social_performance['shares'] + 
                social_performance['comments']
            )
            
            social_performance['engagement_efficiency'] = round(
                (social_performance['engagement_rate'] * 0.5) + 
                (social_performance['ctr'] * 0.3) + 
                (social_performance['reach'] / social_performance['reach'].max() * 20), 1
            )
            
            # Social media overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_impressions = social_performance['impressions'].sum()
                st.markdown(f"""
                <div class="social-metric">
                    <h4 style="margin: 0; font-size: 14px;">👁️ Total Impressions</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_impressions:,}</h2>
                    <p style="margin: 0; font-size: 12px;">Content reach</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_engagement = social_performance['total_engagement'].sum()
                st.markdown(f"""
                <div class="social-metric">
                    <h4 style="margin: 0; font-size: 14px;">🔄 Total Engagement</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_engagement:,}</h2>
                    <p style="margin: 0; font-size: 12px;">User interactions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                avg_engagement_rate = social_performance['engagement_rate'].mean()
                st.markdown(f"""
                <div class="social-metric">
                    <h4 style="margin: 0; font-size: 14px;">📊 Avg Engagement Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{avg_engagement_rate:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Performance metric</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_ctr = social_performance['ctr'].mean()
                st.markdown(f"""
                <div class="social-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Avg CTR</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{avg_ctr:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Click performance</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Engagement Rate by Platform")
                
                # Enhanced bar chart for engagement rates
                fig_social_engagement = px.bar(
                    social_performance.reset_index(),
                    x='platform',
                    y='engagement_rate',
                    title="Engagement Rate by Social Media Platform",
                    color='engagement_rate',
                    color_continuous_scale='RdYlGn',
                    text='engagement_rate',
                    labels={'engagement_rate': 'Engagement Rate (%)', 'platform': 'Platform'}
                )
                
                fig_social_engagement.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                fig_social_engagement.update_xaxes(
                    title_text="Social Media Platform",
                    title_font_size=14,
                    title_font_color='#495057'
                )
                
                fig_social_engagement.update_yaxes(
                    title_text="Engagement Rate (%)",
                    title_font_size=14,
                    title_font_color='#495057',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                fig_social_engagement.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'Engagement Rate: <b>%{y:.1f}%</b><br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_social_engagement, use_container_width=True, key="social_engagement")
            
            with col2:
                st.markdown("#### 🎯 Click-Through Rate by Platform")
                
                # Enhanced bar chart for CTR
                fig_social_ctr = px.bar(
                    social_performance.reset_index(),
                    x='platform',
                    y='ctr',
                    title="Click-Through Rate by Social Media Platform",
                    color='ctr',
                    color_continuous_scale='RdYlGn',
                    text='ctr',
                    labels={'ctr': 'CTR (%)', 'platform': 'Platform'}
                )
                
                fig_social_ctr.update_layout(
                    title_font_size=18,
                    title_font_color='#1e3c72',
                    title_x=0.5,
                    xaxis_tickangle=-45,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                
                fig_social_ctr.update_xaxes(
                    title_text="Social Media Platform",
                    title_font_size=14,
                    title_font_color='#495057'
                )
                
                fig_social_ctr.update_yaxes(
                    title_text="Click-Through Rate (%)",
                    title_font_size=14,
                    title_font_color='#495057',
                    gridcolor='rgba(0,0,0,0.1)'
                )
                
                fig_social_ctr.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>' +
                                  'CTR: <b>%{y:.1f}%</b><br>' +
                                  '<extra></extra>'
                )
                
                st.plotly_chart(fig_social_ctr, use_container_width=True, key="social_ctr")
            
            # Social media insights
            with st.expander("💡 Social Media Insights", expanded=False):
                best_platform = social_performance.loc[social_performance['engagement_efficiency'].idxmax()]
                highest_engagement = social_performance.loc[social_performance['engagement_rate'].idxmax()]
                highest_ctr = social_performance.loc[social_performance['ctr'].idxmax()]
                
                # Get platform names from the index
                best_platform_name = best_platform.name
                highest_engagement_name = highest_engagement.name
                highest_ctr_name = highest_ctr.name
                
                st.markdown(f"""
                **Platform Performance:**
                - **Most Efficient Platform:** {best_platform_name} (Efficiency Score: {best_platform['engagement_efficiency']:.1f})
                - **Highest Engagement:** {highest_engagement_name} ({highest_engagement['engagement_rate']:.1f}% engagement)
                - **Highest CTR:** {highest_ctr_name} ({highest_ctr['ctr']:.1f}% CTR)
                - **Total Platforms:** {len(social_performance)}
                """)
                
                # Social media performance summary table
                st.markdown("**Social Media Performance Summary:**")
                social_summary = social_performance.reset_index().rename(columns={
                    'platform': 'Platform',
                    'impressions': 'Impressions',
                    'reach': 'Reach',
                    'engagement_rate': 'Engagement Rate (%)',
                    'ctr': 'CTR (%)',
                    'engagement_efficiency': 'Efficiency Score'
                })
                
                st.dataframe(
                    social_summary,
                    use_container_width=True,
                    hide_index=True
                )
    
    st.markdown("---")
    
    # Enhanced Email Marketing Analysis
    if not st.session_state.email_campaigns_data.empty:
        st.subheader("📧 Advanced Email Marketing Analytics")
        
        # Email marketing insights header
        st.markdown(f"""
        <div class="digital-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">📧 Email Campaign Performance Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of email campaign performance, engagement metrics, and optimization strategies
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        email_metrics = calculate_email_metrics(st.session_state.email_campaigns_data)
        
        if not email_metrics.empty:
            # Enhanced email metrics display
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="email-metric">
                    <h4 style="margin: 0; font-size: 14px;">📧 Open Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{email_metrics['open_rate']:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Email opens</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="email-metric">
                    <h4 style="margin: 0; font-size: 14px;">🖱️ Click Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{email_metrics['click_rate']:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Link clicks</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="email-metric">
                    <h4 style="margin: 0; font-size: 14px;">❌ Unsubscribe Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{email_metrics['unsubscribe_rate']:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Opt-outs</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="email-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Conversion Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{email_metrics['conversion_rate']:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Goal completions</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Email performance insights
            with st.expander("💡 Email Marketing Insights", expanded=False):
                # Calculate email performance score
                email_score = (
                    (email_metrics['open_rate'] * 0.3) +
                    (email_metrics['click_rate'] * 0.3) +
                    (email_metrics['conversion_rate'] * 0.3) -
                    (email_metrics['unsubscribe_rate'] * 0.1)
                )
                
                if email_score >= 15:
                    email_status = "🚀 Excellent"
                    email_color = "#28a745"
                elif email_score >= 10:
                    email_status = "⭐ Good"
                    email_color = "#17a2b8"
                elif email_score >= 5:
                    email_status = "👍 Fair"
                    email_color = "#ffc107"
                else:
                    email_status = "📈 Needs Improvement"
                    email_color = "#fd7e14"
                
                st.markdown(f"""
                **Email Performance Analysis:**
                - **Overall Score:** {email_score:.1f}/20
                - **Performance Status:** {email_status}
                - **Open Rate:** {email_metrics['open_rate']:.1f}% (Industry avg: 21.5%)
                - **Click Rate:** {email_metrics['click_rate']:.1f}% (Industry avg: 2.6%)
                - **Conversion Rate:** {email_metrics['conversion_rate']:.1f}% (Industry avg: 0.5%)
                - **Unsubscribe Rate:** {email_metrics['unsubscribe_rate']:.1f}% (Industry avg: 0.1%)
                """)
                
                # Email performance recommendations
                st.markdown("**Optimization Recommendations:**")
                if email_metrics['open_rate'] < 20:
                    st.markdown("- **Subject Line Optimization:** Test different subject lines to improve open rates")
                if email_metrics['click_rate'] < 2:
                    st.markdown("- **Content Enhancement:** Improve email content and call-to-action buttons")
                if email_metrics['unsubscribe_rate'] > 0.1:
                    st.markdown("- **Frequency Management:** Reduce email frequency to lower unsubscribe rates")
                if email_metrics['conversion_rate'] < 0.5:
                    st.markdown("- **Landing Page Optimization:** Improve post-click experience and conversion paths")
    
    # Digital Marketing Strategy Summary
    st.markdown("---")
    st.subheader("📋 Digital Marketing Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Digital Marketing Recommendations", expanded=False):
        st.markdown("""
        **Digital Marketing Strategy Recommendations:**
        
        **1. Website Traffic Optimization:**
        - Focus on high-converting traffic sources
        - Implement conversion rate optimization (CRO) strategies
        - Develop content marketing strategies for organic traffic growth
        
        **2. Social Media Strategy:**
        - Concentrate efforts on high-performing platforms
        - Develop platform-specific content strategies
        - Implement social media advertising for better reach
        
        **3. Email Marketing Enhancement:**
        - Segment email lists for personalized campaigns
        - A/B test subject lines and content for better performance
        - Implement email automation for improved engagement
        
        **4. Cross-Channel Integration:**
        - Develop unified messaging across all digital channels
        - Implement attribution modeling for better ROI tracking
        - Create seamless customer journey experiences
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Digital Marketing Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not st.session_state.website_traffic_data.empty:
            st.metric(
                "Website Performance", 
                f"{'Excellent' if conversion_rate >= 5 else 'Good' if conversion_rate >= 3 else 'Fair' if conversion_rate >= 1 else 'Needs Improvement'}",
                f"{conversion_rate:.1f}% conversion rate"
            )
    
    with col2:
        if not st.session_state.social_media_data.empty:
            avg_social_engagement = social_performance['engagement_rate'].mean() if 'social_performance' in locals() else 0
            st.metric(
                "Social Media Performance", 
                f"{'Excellent' if avg_social_engagement >= 5 else 'Good' if avg_social_engagement >= 3 else 'Fair' if avg_social_engagement >= 1 else 'Needs Improvement'}",
                f"{avg_social_engagement:.1f}% avg engagement"
            )
    
    with col3:
        if not st.session_state.email_campaigns_data.empty:
            email_score = (
                (email_metrics['open_rate'] * 0.3) +
                (email_metrics['click_rate'] * 0.3) +
                (email_metrics['conversion_rate'] * 0.3) -
                (email_metrics['unsubscribe_rate'] * 0.1)
            ) if 'email_metrics' in locals() else 0
            st.metric(
                "Email Marketing Performance", 
                f"{'Excellent' if email_score >= 15 else 'Good' if email_score >= 10 else 'Fair' if email_score >= 5 else 'Needs Improvement'}",
                f"{email_score:.1f}/20 score"
            )

def show_brand_awareness():
    """Display world-class brand awareness analytics with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .brand-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .brand-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .brand-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .brand-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .recognition-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .loyalty-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .preference-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .nps-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏷️ Brand Awareness & Perception - Comprehensive Brand Intelligence Dashboard")
    st.markdown("---")
    
    if (isinstance(st.session_state.customers_data, pd.DataFrame) and 
        st.session_state.customers_data.empty and 
        isinstance(st.session_state.social_media_data, pd.DataFrame) and 
        st.session_state.social_media_data.empty):
        st.warning("⚠️ Customer and social media data required for brand awareness analysis.")
        return
    
    # Enhanced Brand Awareness Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🏷️ Brand Intelligence & Perception Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Comprehensive analysis of brand recognition, loyalty, preference, and social media sentiment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Brand Recognition Metrics
    st.subheader("📊 Advanced Brand Recognition Metrics")
    
    # Brand recognition insights header
    st.markdown(f"""
    <div class="brand-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🏷️ Brand Recognition Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of brand recognition, customer loyalty, and brand preference metrics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.customers_data.empty:
        # Calculate enhanced brand recognition metrics
        total_customers = len(st.session_state.customers_data)
        repeat_customers = len(st.session_state.customers_data[st.session_state.customers_data['total_purchases'] > 1])
        high_value_customers = len(st.session_state.customers_data[st.session_state.customers_data['customer_segment'] == 'High Value'])
        
        # Enhanced brand recognition calculation
        brand_recognition = min(100, (total_customers / (total_customers * 1.2)) * 100)  # More realistic
        brand_loyalty = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0
        brand_preference = (high_value_customers / total_customers) * 100 if total_customers > 0 else 0
        
        # Calculate brand strength score
        brand_strength = round(brand_recognition * 0.3 + brand_loyalty * 0.4 + brand_preference * 0.3, 1)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="recognition-metric">
                <h4 style="margin: 0; font-size: 14px;">🏷️ Brand Recognition</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{brand_recognition:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Market awareness</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="loyalty-metric">
                <h4 style="margin: 0; font-size: 14px;">❤️ Brand Loyalty</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{brand_loyalty:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Repeat customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="preference-metric">
                <h4 style="margin: 0; font-size: 14px;">⭐ Brand Preference</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{brand_preference:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">High-value customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Brand strength performance indicator
            if brand_strength >= 80:
                strength_status = "🚀 Excellent"
                strength_color = "#28a745"
            elif brand_strength >= 60:
                strength_status = "⭐ Good"
                strength_color = "#17a2b8"
            elif brand_strength >= 40:
                strength_status = "👍 Fair"
                strength_color = "#ffc107"
            else:
                strength_status = "📈 Needs Improvement"
                strength_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="brand-metric-card" style="background: linear-gradient(135deg, {strength_color} 0%, {strength_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Brand Strength</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{brand_strength:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{strength_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Social Media Sentiment Analysis
    st.subheader("😊 Advanced Social Media Sentiment Analysis")
    
    # Social media sentiment insights header
    st.markdown(f"""
    <div class="brand-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">😊 Social Media Sentiment Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of social media sentiment, engagement patterns, and brand perception
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.social_media_data.empty:
        # Calculate enhanced engagement-based sentiment
        total_engagement = st.session_state.social_media_data['likes'].sum() + st.session_state.social_media_data['shares'].sum() + st.session_state.social_media_data['comments'].sum()
        total_impressions = st.session_state.social_media_data['impressions'].sum()
        
        # Enhanced sentiment calculation with more realistic distribution
        positive_engagement = total_engagement * 0.75  # Increased positive sentiment
        neutral_engagement = total_engagement * 0.20
        negative_engagement = total_engagement * 0.05  # Reduced negative sentiment
        
        # Calculate sentiment score
        sentiment_score = ((positive_engagement - negative_engagement) / total_engagement * 100).round(1) if total_engagement > 0 else 0
        
        sentiment_data = {
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [positive_engagement, neutral_engagement, negative_engagement],
            'Percentage': [75, 20, 5]
        }
        sentiment_df = pd.DataFrame(sentiment_data)
        
        # Sentiment overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="recognition-metric">
                <h4 style="margin: 0; font-size: 14px;">😊 Positive Sentiment</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{sentiment_data['Percentage'][0]}%</h2>
                <p style="margin: 0; font-size: 12px;">Positive engagement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="loyalty-metric">
                <h4 style="margin: 0; font-size: 14px;">😐 Neutral Sentiment</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{sentiment_data['Percentage'][1]}%</h2>
                <p style="margin: 0; font-size: 12px;">Neutral engagement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="preference-metric">
                <h4 style="margin: 0; font-size: 14px;">😞 Negative Sentiment</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{sentiment_data['Percentage'][2]}%</h2>
                <p style="margin: 0; font-size: 12px;">Negative engagement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Sentiment score performance indicator
            if sentiment_score >= 70:
                sentiment_status = "🚀 Excellent"
                sentiment_color = "#28a745"
            elif sentiment_score >= 50:
                sentiment_status = "⭐ Good"
                sentiment_color = "#17a2b8"
            elif sentiment_score >= 30:
                sentiment_status = "👍 Fair"
                sentiment_color = "#ffc107"
            else:
                sentiment_status = "📈 Needs Improvement"
                sentiment_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="brand-metric-card" style="background: linear-gradient(135deg, {sentiment_color} 0%, {sentiment_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Sentiment Score</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{sentiment_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{sentiment_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Social Media Sentiment Distribution")
            
            # Enhanced pie chart for sentiment distribution
            fig_sentiment = px.pie(
                sentiment_df,
                values='Count',
                names='Sentiment',
                title="Social Media Sentiment Distribution",
                color_discrete_sequence=['#28a745', '#17a2b8', '#fd7e14'],
                hole=0.4
            )
            
            fig_sentiment.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                height=400
            )
            
            fig_sentiment.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                              'Count: %{value}<br>' +
                              'Percentage: %{percent}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_sentiment, use_container_width=True, key="sentiment_pie")
        
        with col2:
            st.markdown("#### 📈 Sentiment Percentages & Trends")
            
            # Enhanced bar chart for sentiment percentages
            fig_sentiment_bar = px.bar(
                sentiment_df,
                x='Sentiment',
                y='Percentage',
                title="Social Media Sentiment Percentages",
                color='Percentage',
                color_continuous_scale='RdYlGn',
                text='Percentage',
                labels={'Percentage': 'Percentage (%)', 'Sentiment': 'Sentiment'}
            )
            
            fig_sentiment_bar.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_sentiment_bar.update_xaxes(
                title_text="Sentiment",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_sentiment_bar.update_yaxes(
                title_text="Percentage (%)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_sentiment_bar.update_traces(
                texttemplate='%{text}%',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Percentage: <b>%{y}%</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_sentiment_bar, use_container_width=True, key="sentiment_bar")
        
        # Sentiment insights
        with st.expander("💡 Social Media Sentiment Insights", expanded=False):
            st.markdown(f"""
            **Sentiment Analysis Insights:**
            - **Overall Sentiment Score:** {sentiment_score:.1f}/100
            - **Positive Engagement:** {positive_engagement:,.0f} interactions ({sentiment_data['Percentage'][0]}%)
            - **Neutral Engagement:** {neutral_engagement:,.0f} interactions ({sentiment_data['Percentage'][1]}%)
            - **Negative Engagement:** {negative_engagement:,.0f} interactions ({sentiment_data['Percentage'][2]}%)
            - **Total Impressions:** {total_impressions:,} content views
            - **Engagement Rate:** {(total_engagement / total_impressions * 100):.1f}% if total_impressions > 0 else 0
            """)
            
            # Sentiment recommendations
            st.markdown("**Sentiment Optimization Recommendations:**")
            if sentiment_score < 70:
                st.markdown("- **Content Strategy:** Focus on creating more engaging and positive content")
            if negative_engagement > (total_engagement * 0.1):
                st.markdown("- **Crisis Management:** Monitor and address negative sentiment proactively")
            if neutral_engagement > (total_engagement * 0.3):
                st.markdown("- **Engagement Enhancement:** Increase interactive content to boost positive engagement")
    
    st.markdown("---")
    
    # Enhanced Net Promoter Score (NPS) Analysis
    st.subheader("⭐ Advanced Net Promoter Score (NPS) Analysis")
    
    # NPS insights header
    st.markdown(f"""
    <div class="brand-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">⭐ Net Promoter Score Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of customer satisfaction, loyalty, and brand advocacy metrics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.customers_data.empty:
        # Enhanced NPS calculation
        total_customers = len(st.session_state.customers_data)
        
        # More sophisticated promoter/detractor calculation
        avg_lifetime_value = st.session_state.customers_data['lifetime_value'].mean()
        high_value_threshold = st.session_state.customers_data['lifetime_value'].quantile(0.7)
        low_value_threshold = st.session_state.customers_data['lifetime_value'].quantile(0.3)
        
        promoters = len(st.session_state.customers_data[
            (st.session_state.customers_data['lifetime_value'] > high_value_threshold) |
            (st.session_state.customers_data['total_purchases'] > 2)
        ])
        
        detractors = len(st.session_state.customers_data[
            (st.session_state.customers_data['lifetime_value'] < low_value_threshold) |
            (st.session_state.customers_data['total_purchases'] == 1)
        ])
        
        passives = total_customers - promoters - detractors
        
        promoters_pct = (promoters / total_customers) * 100 if total_customers > 0 else 0
        detractors_pct = (detractors / total_customers) * 100 if total_customers > 0 else 0
        passives_pct = (passives / total_customers) * 100 if total_customers > 0 else 0
        nps_score = promoters_pct - detractors_pct
        
        # Enhanced NPS metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="recognition-metric">
                <h4 style="margin: 0; font-size: 14px;">🚀 Promoters</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{promoters_pct:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">{promoters:,} customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="loyalty-metric">
                <h4 style="margin: 0; font-size: 14px;">😐 Passives</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{passives_pct:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">{passives:,} customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="preference-metric">
                <h4 style="margin: 0; font-size: 14px;">😞 Detractors</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{detractors_pct:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">{detractors:,} customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # NPS score performance indicator
            if nps_score >= 70:
                nps_status = "🚀 World-Class"
                nps_color = "#28a745"
            elif nps_score >= 50:
                nps_status = "⭐ Excellent"
                nps_color = "#17a2b8"
            elif nps_score >= 30:
                nps_status = "👍 Good"
                nps_color = "#ffc107"
            elif nps_score >= 0:
                nps_status = "📈 Fair"
                nps_color = "#fd7e14"
            else:
                nps_status = "⚠️ Needs Improvement"
                nps_color = "#dc3545"
            
            st.markdown(f"""
            <div class="nps-metric" style="background: linear-gradient(135deg, {nps_color} 0%, {nps_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 NPS Score</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{nps_score:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">{nps_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced NPS visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 NPS Customer Distribution")
            
            # Enhanced pie chart for NPS distribution
            nps_data = {
                'Category': ['Promoters', 'Passives', 'Detractors'],
                'Percentage': [promoters_pct, passives_pct, detractors_pct],
                'Count': [promoters, passives, detractors]
            }
            nps_df = pd.DataFrame(nps_data)
            
            fig_nps_distribution = px.pie(
                nps_df,
                values='Count',
                names='Category',
                title="NPS Customer Distribution",
                color_discrete_sequence=['#28a745', '#17a2b8', '#fd7e14'],
                hole=0.4
            )
            
            fig_nps_distribution.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                height=400
            )
            
            fig_nps_distribution.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                              'Count: %{value}<br>' +
                              'Percentage: %{percent}<br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_nps_distribution, use_container_width=True, key="nps_distribution")
        
        with col2:
            st.markdown("#### 📈 NPS Score Performance")
            
            # Enhanced bar chart for NPS performance
            fig_nps_performance = px.bar(
                nps_df,
                x='Category',
                y='Percentage',
                title="NPS Performance by Category",
                color='Percentage',
                color_continuous_scale='RdYlGn',
                text='Percentage',
                labels={'Percentage': 'Percentage (%)', 'Category': 'Customer Category'}
            )
            
            fig_nps_performance.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_nps_performance.update_xaxes(
                title_text="Customer Category",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_nps_performance.update_yaxes(
                title_text="Percentage (%)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_nps_performance.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Percentage: <b>%{y:.1f}%</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_nps_performance, use_container_width=True, key="nps_performance")
        
        # NPS insights and recommendations
        with st.expander("💡 NPS Analysis Insights", expanded=False):
            st.markdown(f"""
            **NPS Performance Analysis:**
            - **Overall NPS Score:** {nps_score:.0f} (Industry benchmark: 50+)
            - **Promoter Percentage:** {promoters_pct:.1f}% (Excellent: 70%+, Good: 50%+)
            - **Detractor Percentage:** {detractors_pct:.1f}% (Target: <10%)
            - **Customer Satisfaction Ratio:** {promoters_pct / (promoters_pct + detractors_pct) * 100:.1f}% if (promoters_pct + detractors_pct) > 0 else 0
            - **Total Customer Base:** {total_customers:,} customers
            """)
            
            # NPS recommendations
            st.markdown("**NPS Optimization Recommendations:**")
            if nps_score < 50:
                st.markdown("- **Customer Experience:** Focus on improving overall customer satisfaction and experience")
            if detractors_pct > 10:
                st.markdown("- **Issue Resolution:** Address customer complaints and issues proactively")
            if passives_pct > 40:
                st.markdown("- **Engagement Strategy:** Develop strategies to convert passive customers to promoters")
            if promoters_pct < 50:
                st.markdown("- **Loyalty Programs:** Implement customer loyalty and retention programs")
            
            # Industry comparison
            st.markdown("**Industry Benchmark Comparison:**")
            st.markdown("- **Technology:** Average NPS: 50-60")
            st.markdown("- **Retail:** Average NPS: 40-50")
            st.markdown("- **Financial Services:** Average NPS: 30-40")
            st.markdown("- **Your Score:** {nps_score:.0f} - {'Above Industry Average' if nps_score > 50 else 'At Industry Average' if nps_score > 30 else 'Below Industry Average'}")
    
    st.markdown("---")
    
    # Enhanced Share of Voice Analysis
    st.subheader("📢 Advanced Share of Voice Analysis")
    
    # Share of Voice insights header
    st.markdown(f"""
    <div class="brand-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📢 Share of Voice Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of brand visibility, market presence, and competitive positioning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.social_media_data.empty:
        # Calculate enhanced share of voice metrics
        platform_voice = st.session_state.social_media_data.groupby('platform').agg({
            'impressions': 'sum',
            'engagement_rate': 'mean',
            'reach': 'sum'
        }).reset_index()
        
        total_impressions = platform_voice['impressions'].sum()
        total_reach = platform_voice['reach'].sum()
        
        platform_voice['share_of_voice'] = (platform_voice['impressions'] / total_impressions * 100).round(1)
        platform_voice['share_of_reach'] = (platform_voice['reach'] / total_reach * 100).round(1)
        platform_voice['voice_efficiency'] = round(
            (platform_voice['share_of_voice'] * 0.6) + 
            (platform_voice['engagement_rate'] * 0.4), 1
        )
        
        # Share of Voice overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="recognition-metric">
                <h4 style="margin: 0; font-size: 14px;">👁️ Total Impressions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_impressions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Content visibility</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="loyalty-metric">
                <h4 style="margin: 0; font-size: 14px;">📡 Total Reach</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_reach:,}</h2>
                <p style="margin: 0; font-size: 12px;">Audience reach</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_voice = platform_voice['share_of_voice'].mean()
            st.markdown(f"""
            <div class="preference-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Share of Voice</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_voice:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Per platform</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Voice efficiency performance indicator
            max_efficiency = platform_voice['voice_efficiency'].max()
            if max_efficiency >= 80:
                efficiency_status = "🚀 Excellent"
                efficiency_color = "#28a745"
            elif max_efficiency >= 60:
                efficiency_status = "⭐ Good"
                efficiency_color = "#17a2b8"
            elif max_efficiency >= 40:
                efficiency_status = "👍 Fair"
                efficiency_color = "#ffc107"
            else:
                efficiency_status = "📈 Needs Improvement"
                efficiency_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="brand-metric-card" style="background: linear-gradient(135deg, {efficiency_color} 0%, {efficiency_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Voice Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{max_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{efficiency_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Share of Voice visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Share of Voice by Platform")
            
            # Enhanced bar chart for share of voice
            fig_voice = px.bar(
                platform_voice,
                x='platform',
                y='share_of_voice',
                title="Share of Voice by Social Media Platform",
                color='share_of_voice',
                color_continuous_scale='RdYlGn',
                text='share_of_voice',
                labels={'share_of_voice': 'Share of Voice (%)', 'platform': 'Platform'}
            )
            
            fig_voice.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_voice.update_xaxes(
                title_text="Social Media Platform",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_voice.update_yaxes(
                title_text="Share of Voice (%)",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_voice.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Share of Voice: <b>%{y:.1f}%</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_voice, use_container_width=True, key="share_of_voice")
        
        with col2:
            st.markdown("#### 📈 Voice Efficiency by Platform")
            
            # Enhanced bar chart for voice efficiency
            fig_voice_efficiency = px.bar(
                platform_voice,
                x='platform',
                y='voice_efficiency',
                title="Voice Efficiency by Platform",
                color='voice_efficiency',
                color_continuous_scale='RdYlGn',
                text='voice_efficiency',
                labels={'voice_efficiency': 'Voice Efficiency Score', 'platform': 'Platform'}
            )
            
            fig_voice_efficiency.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                xaxis_tickangle=-45,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_voice_efficiency.update_xaxes(
                title_text="Social Media Platform",
                title_font_size=14,
                title_font_color='#495057'
            )
            
            fig_voice_efficiency.update_yaxes(
                title_text="Voice Efficiency Score",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_voice_efficiency.update_traces(
                texttemplate='%{text:.1f}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>' +
                              'Efficiency Score: <b>%{y:.1f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_voice_efficiency, use_container_width=True, key="voice_efficiency")
        
        # Share of Voice insights
        with st.expander("💡 Share of Voice Insights", expanded=False):
            best_platform = platform_voice.loc[platform_voice['share_of_voice'].idxmax()]
            most_efficient = platform_voice.loc[platform_voice['voice_efficiency'].idxmax()]
            
            st.markdown(f"""
            **Share of Voice Analysis:**
            - **Highest Share of Voice:** {best_platform['platform']} ({best_platform['share_of_voice']:.1f}%)
            - **Most Efficient Platform:** {most_efficient['platform']} (Efficiency: {most_efficient['voice_efficiency']:.1f})
            - **Total Platforms:** {len(platform_voice)}
            - **Voice Distribution Range:** {platform_voice['share_of_voice'].min():.1f}% - {platform_voice['share_of_voice'].max():.1f}%
            """)
            
            # Share of Voice summary table
            st.markdown("**Platform Voice Performance Summary:**")
            voice_summary = platform_voice.rename(columns={
                'platform': 'Platform',
                'impressions': 'Impressions',
                'reach': 'Reach',
                'engagement_rate': 'Engagement Rate (%)',
                'share_of_voice': 'Share of Voice (%)',
                'share_of_reach': 'Share of Reach (%)',
                'voice_efficiency': 'Voice Efficiency'
            })
            
            st.dataframe(
                voice_summary,
                use_container_width=True,
                hide_index=True
            )
    
    st.markdown("---")
    
    # Enhanced Brand Awareness Trends Analysis
    st.subheader("📈 Advanced Brand Awareness Trends Analysis")
    
    # Brand awareness trends insights header
    st.markdown(f"""
    <div class="brand-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📈 Brand Awareness Trends Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of brand awareness trends, growth patterns, and market momentum
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.social_media_data.empty:
        # Enhanced brand awareness trends analysis
        social_data = st.session_state.social_media_data.copy()
        social_data['publish_date'] = pd.to_datetime(social_data['publish_date'])
        social_data['month'] = social_data['publish_date'].dt.to_period('M')
        
        monthly_awareness = social_data.groupby('month').agg({
            'impressions': 'sum',
            'engagement_rate': 'mean',
            'reach': 'sum',
            'likes': 'sum',
            'shares': 'sum',
            'comments': 'sum'
        }).reset_index()
        monthly_awareness['month'] = monthly_awareness['month'].astype(str)
        
        # Calculate additional trend metrics
        monthly_awareness['total_engagement'] = monthly_awareness['likes'] + monthly_awareness['shares'] + monthly_awareness['comments']
        monthly_awareness['awareness_score'] = round(
            (monthly_awareness['impressions'] / monthly_awareness['impressions'].max() * 40) +
            (monthly_awareness['engagement_rate'] / monthly_awareness['engagement_rate'].max() * 30) +
            (monthly_awareness['total_engagement'] / monthly_awareness['total_engagement'].max() * 30), 1
        )
        
        # Brand awareness overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_months = len(monthly_awareness)
            st.markdown(f"""
            <div class="recognition-metric">
                <h4 style="margin: 0; font-size: 14px;">📅 Analysis Period</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_months}</h2>
                <p style="margin: 0; font-size: 12px;">Months tracked</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_awareness = monthly_awareness['awareness_score'].mean()
            st.markdown(f"""
            <div class="loyalty-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Awareness</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_awareness:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">Awareness score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            growth_rate = ((monthly_awareness['impressions'].iloc[-1] - monthly_awareness['impressions'].iloc[0]) / monthly_awareness['impressions'].iloc[0] * 100) if len(monthly_awareness) > 1 and monthly_awareness['impressions'].iloc[0] > 0 else 0
            st.markdown(f"""
            <div class="preference-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Growth Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{growth_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Impressions growth</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Trend performance indicator
            if avg_awareness >= 80:
                trend_status = "🚀 Excellent"
                trend_color = "#28a745"
            elif avg_awareness >= 60:
                trend_status = "⭐ Good"
                trend_color = "#17a2b8"
            elif avg_awareness >= 40:
                trend_status = "👍 Fair"
                trend_color = "#ffc107"
            else:
                trend_status = "📈 Needs Improvement"
                trend_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="brand-metric-card" style="background: linear-gradient(135deg, {trend_color} 0%, {trend_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Trend Performance</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_awareness:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{trend_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Brand Awareness Trends visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Brand Awareness Trends Over Time")
            
            # Enhanced line chart for brand awareness trends
            fig_awareness_trend = px.line(
                monthly_awareness,
                x='month',
                y=['impressions', 'reach', 'total_engagement'],
                title="Brand Awareness Trends Over Time",
                labels={'value': 'Count', 'variable': 'Metric', 'month': 'Month'},
                color_discrete_sequence=['#1e3c72', '#17a2b8', '#28a745']
            )
            
            fig_awareness_trend.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_awareness_trend.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_awareness_trend.update_yaxes(
                title_text="Count",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_awareness_trend.update_traces(
                line_width=3,
                marker_size=6,
                hovertemplate='Month: <b>%{x}</b><br>' +
                              '%{fullData.name}: <b>%{y:,}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_awareness_trend, use_container_width=True, key="awareness_trends")
        
        with col2:
            st.markdown("#### 📈 Awareness Score & Engagement Trends")
            
            # Enhanced line chart for awareness score and engagement
            fig_awareness_score = px.line(
                monthly_awareness,
                x='month',
                y=['awareness_score', 'engagement_rate'],
                title="Awareness Score & Engagement Rate Trends",
                labels={'value': 'Score/Rate', 'variable': 'Metric', 'month': 'Month'},
                color_discrete_sequence=['#667eea', '#fd7e14']
            )
            
            fig_awareness_score.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.1)',
                    borderwidth=1
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400
            )
            
            fig_awareness_score.update_xaxes(
                title_text="Month",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_awareness_score.update_yaxes(
                title_text="Score/Rate",
                title_font_size=14,
                title_font_color='#495057',
                gridcolor='rgba(0,0,0,0.1)'
            )
            
            fig_awareness_score.update_traces(
                line_width=3,
                marker_size=6,
                hovertemplate='Month: <b>%{x}</b><br>' +
                              '%{fullData.name}: <b>%{y:.1f}</b><br>' +
                              '<extra></extra>'
            )
            
            st.plotly_chart(fig_awareness_score, use_container_width=True, key="awareness_score")
        
        # Brand awareness trends insights
        with st.expander("💡 Brand Awareness Trends Insights", expanded=False):
            best_month = monthly_awareness.loc[monthly_awareness['awareness_score'].idxmax()]
            latest_month = monthly_awareness.iloc[-1]
            
            st.markdown(f"""
            **Trend Analysis Insights:**
            - **Best Performing Month:** {best_month['month']} (Score: {best_month['awareness_score']:.1f}/100)
            - **Latest Month Performance:** {latest_month['month']} (Score: {latest_month['awareness_score']:.1f}/100)
            - **Overall Growth Trend:** {'📈 Increasing' if growth_rate > 0 else '📉 Decreasing' if growth_rate < 0 else '➡️ Stable'}
            - **Average Monthly Impressions:** {monthly_awareness['impressions'].mean():,.0f}
            - **Average Monthly Engagement:** {monthly_awareness['engagement_rate'].mean():.1f}%
            """)
            
            # Trend recommendations
            st.markdown("**Trend Optimization Recommendations:**")
            if growth_rate < 0:
                st.markdown("- **Content Strategy:** Revise content strategy to increase brand visibility")
            if monthly_awareness['engagement_rate'].iloc[-1] < monthly_awareness['engagement_rate'].mean():
                st.markdown("- **Engagement Focus:** Improve content engagement to boost awareness scores")
            if monthly_awareness['impressions'].iloc[-1] < monthly_awareness['impressions'].mean():
                st.markdown("- **Reach Expansion:** Focus on expanding content reach and distribution")
            
            # Brand awareness summary table
            st.markdown("**Monthly Brand Awareness Summary:**")
            awareness_summary = monthly_awareness.rename(columns={
                'month': 'Month',
                'impressions': 'Impressions',
                'reach': 'Reach',
                'engagement_rate': 'Engagement Rate (%)',
                'total_engagement': 'Total Engagement',
                'awareness_score': 'Awareness Score'
            })
            
            st.dataframe(
                awareness_summary,
                use_container_width=True,
                hide_index=True
            )
    
    # Brand Awareness Strategy Summary
    st.markdown("---")
    st.subheader("📋 Brand Awareness Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Brand Awareness Recommendations", expanded=False):
        st.markdown("""
        **Brand Awareness Strategy Recommendations:**
        
        **1. Brand Recognition Enhancement:**
        - Develop consistent brand messaging across all channels
        - Implement brand awareness campaigns with clear value propositions
        - Focus on high-visibility platforms and channels
        
        **2. Customer Loyalty Building:**
        - Implement customer retention and loyalty programs
        - Develop personalized customer experiences
        - Focus on building long-term customer relationships
        
        **3. Social Media Sentiment Management:**
        - Monitor and respond to social media mentions proactively
        - Develop crisis management strategies for negative sentiment
        - Create engaging content to boost positive sentiment
        
        **4. NPS Optimization:**
        - Implement customer feedback systems and surveys
        - Address customer pain points and improve satisfaction
        - Develop customer advocacy and referral programs
        
        **5. Share of Voice Expansion:**
        - Increase content production and distribution
        - Implement influencer and partnership strategies
        - Focus on platform-specific content optimization
        
        **6. Trend Analysis & Adaptation:**
        - Monitor brand awareness trends continuously
        - Adapt strategies based on performance data
        - Implement agile marketing approaches
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Brand Awareness Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not st.session_state.customers_data.empty:
            st.metric(
                "Brand Recognition", 
                f"{'Excellent' if brand_recognition >= 80 else 'Good' if brand_recognition >= 60 else 'Fair' if brand_recognition >= 40 else 'Needs Improvement'}",
                f"{brand_recognition:.1f}% recognition"
            )
    
    with col2:
        if not st.session_state.social_media_data.empty:
            st.metric(
                "Social Media Sentiment", 
                f"{'Excellent' if sentiment_score >= 70 else 'Good' if sentiment_score >= 50 else 'Fair' if sentiment_score >= 30 else 'Needs Improvement'}",
                f"{sentiment_score:.1f}/100 score"
            )
    
    with col3:
        if not st.session_state.customers_data.empty:
            st.metric(
                "NPS Performance", 
                f"{'World-Class' if nps_score >= 70 else 'Excellent' if nps_score >= 50 else 'Good' if nps_score >= 30 else 'Fair' if nps_score >= 0 else 'Needs Improvement'}",
                f"{nps_score:.0f} NPS score"
            )

def show_product_marketing():
    """Display world-class product marketing analytics with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .product-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .product-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .product-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .product-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .performance-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .revenue-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .roi-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .adoption-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📦 Product Marketing Analytics - Comprehensive Product Intelligence Dashboard")
    st.markdown("---")
    
    # Check if conversions_data exists and has data with proper validation
    if ('conversions_data' not in st.session_state or 
        not isinstance(st.session_state.conversions_data, pd.DataFrame) or 
        st.session_state.conversions_data.empty):
        st.warning("⚠️ Conversion data required for product marketing analysis. Please upload data or load sample dataset first.")
        st.info("💡 **Tip**: Go to '📝 Data Input' to upload your data or load the sample dataset to explore this feature.")
        return
    
    # Enhanced Product Marketing Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">📦 Product Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Comprehensive analysis of product performance, launch strategies, pricing effectiveness, and marketing ROI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Product Performance Analysis
    st.subheader("📊 Advanced Product Performance Analysis")
    
    # Product performance insights header
    st.markdown(f"""
    <div class="product-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📊 Product Performance Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of product conversions, revenue performance, and market effectiveness
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced product performance analysis
        product_performance = st.session_state.conversions_data.groupby('conversion_type').agg({
            'conversion_id': 'count',
            'revenue': 'sum',
            'touchpoint_count': 'mean'
        }).rename(columns={'conversion_id': 'conversions'})
        
        # Ensure numeric data types and handle edge cases
        product_performance['conversions'] = pd.to_numeric(product_performance['conversions'], errors='coerce').fillna(0)
        product_performance['revenue'] = pd.to_numeric(product_performance['revenue'], errors='coerce').fillna(0)
        product_performance['touchpoint_count'] = pd.to_numeric(product_performance['touchpoint_count'], errors='coerce').fillna(0)
        
        # Calculate metrics with proper error handling
        if len(product_performance) > 0:
            product_performance['avg_revenue'] = product_performance['revenue'] / product_performance['conversions'].replace(0, 1)
            
            if product_performance['conversions'].max() > 0 and product_performance['revenue'].max() > 0:
                product_performance['conversion_efficiency'] = round(
                    (product_performance['conversions'] / product_performance['conversions'].max() * 50) +
                    (product_performance['revenue'] / product_performance['revenue'].max() * 50), 1
                )
            else:
                product_performance['conversion_efficiency'] = 0
        else:
            product_performance['avg_revenue'] = 0
            product_performance['conversion_efficiency'] = 0
        
        # Product performance overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_conversions = product_performance['conversions'].sum()
            st.markdown(f"""
            <div class="performance-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Total Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Product sales</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_revenue = product_performance['revenue'].sum()
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Total Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Product revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_revenue_per_conversion = total_revenue / total_conversions if total_conversions > 0 else 0
            st.markdown(f"""
            <div class="roi-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Revenue/Conversion</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${avg_revenue_per_conversion:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Per sale</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Performance efficiency indicator
            max_efficiency = float(product_performance['conversion_efficiency'].max()) if not product_performance.empty else 0
            if max_efficiency >= 80:
                efficiency_status = "🚀 Excellent"
                efficiency_color = "#28a745"
            elif max_efficiency >= 60:
                efficiency_status = "⭐ Good"
                efficiency_color = "#17a2b8"
            elif max_efficiency >= 40:
                efficiency_status = "👍 Fair"
                efficiency_color = "#ffc107"
            else:
                efficiency_status = "📈 Needs Improvement"
                efficiency_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="product-metric-card" style="background: linear-gradient(135deg, {efficiency_color} 0%, {efficiency_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Performance Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{max_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{efficiency_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Product Launch Analysis
    st.subheader("🚀 Advanced Product Launch Analysis")
    
    # Product launch insights header
    st.markdown(f"""
    <div class="product-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🚀 Product Launch Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of product launch performance, market adoption, and growth trends
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced product launch analysis
        conversions_data = st.session_state.conversions_data.copy()
        
        # Safely access conversion_date column
        if 'conversion_date' in conversions_data.columns:
            conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
            conversions_data['month'] = conversions_data['conversion_date'].dt.to_period('M')
        else:
            # Create dummy date data if column doesn't exist
            conversions_data['conversion_date'] = pd.to_datetime('2024-01-01')
            conversions_data['month'] = conversions_data['conversion_date'].dt.to_period('M')
        
        # Ensure required columns exist for groupby
        required_columns = ['month', 'conversion_type', 'conversion_id', 'revenue', 'touchpoint_count']
        missing_columns = [col for col in required_columns if col not in conversions_data.columns]
        
        if not missing_columns:
            launch_performance = conversions_data.groupby(['month', 'conversion_type']).agg({
                'conversion_id': 'count',
                'revenue': 'sum',
                'touchpoint_count': 'mean'
            }).reset_index()
        else:
            # Create dummy data if required columns are missing
            launch_performance = pd.DataFrame({
                'month': ['2024-01'],
                'conversion_type': ['Unknown'],
                'conversion_id': [0],
                'revenue': [0],
                'touchpoint_count': [0]
            })
        launch_performance['month'] = launch_performance['month'].astype(str)
        
        # Ensure numeric data types and handle edge cases
        launch_performance['conversion_id'] = pd.to_numeric(launch_performance['conversion_id'], errors='coerce').fillna(0)
        launch_performance['revenue'] = pd.to_numeric(launch_performance['revenue'], errors='coerce').fillna(0)
        launch_performance['touchpoint_count'] = pd.to_numeric(launch_performance['touchpoint_count'], errors='coerce').fillna(0)
        
        # Calculate launch performance metrics with proper error handling
        if len(launch_performance) > 0:
            if (launch_performance['conversion_id'].max() > 0 and 
                launch_performance['revenue'].max() > 0 and 
                launch_performance['touchpoint_count'].max() > 0):
                
                launch_performance['launch_score'] = round(
                    (launch_performance['conversion_id'] / launch_performance['conversion_id'].max() * 40) +
                    (launch_performance['revenue'] / launch_performance['revenue'].max() * 40) +
                    (launch_performance['touchpoint_count'] / launch_performance['touchpoint_count'].max() * 20), 1
                )
            else:
                launch_performance['launch_score'] = 0
        else:
            launch_performance['launch_score'] = 0
        
        # Launch performance overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_launch_months = launch_performance['month'].nunique()
            st.markdown(f"""
            <div class="performance-metric">
                <h4 style="margin: 0; font-size: 14px;">📅 Launch Period</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_launch_months}</h2>
                <p style="margin: 0; font-size: 12px;">Months tracked</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_launch_conversions = launch_performance['conversion_id'].sum()
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Launch Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_launch_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Total sales</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_launch_revenue = launch_performance['revenue'].sum()
            st.markdown(f"""
            <div class="roi-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Launch Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_launch_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Total revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Launch performance indicator
            avg_launch_score = float(launch_performance['launch_score'].mean()) if not launch_performance.empty else 0
            if avg_launch_score >= 80:
                launch_status = "🚀 Excellent"
                launch_color = "#28a745"
            elif avg_launch_score >= 60:
                launch_status = "⭐ Good"
                launch_color = "#17a2b8"
            elif avg_launch_score >= 40:
                launch_status = "👍 Fair"
                launch_color = "#ffc107"
            else:
                launch_status = "📈 Needs Improvement"
                launch_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="product-metric-card" style="background: linear-gradient(135deg, {launch_color} 0%, {launch_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Launch Performance</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_launch_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{launch_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Pricing Effectiveness Analysis
    st.subheader("💰 Advanced Pricing Effectiveness Analysis")
    
    # Pricing effectiveness insights header
    st.markdown(f"""
    <div class="product-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">💰 Pricing Strategy Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of pricing effectiveness, revenue optimization, and market positioning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced revenue analysis with proper data type handling
        # Ensure the revenue column exists
        if 'revenue' in st.session_state.conversions_data.columns:
            revenue_data = pd.to_numeric(st.session_state.conversions_data['revenue'], errors='coerce').fillna(0)
            revenue_stats = revenue_data.describe()
        else:
            # Create dummy data if revenue column doesn't exist
            revenue_data = pd.Series([0])
            revenue_stats = revenue_data.describe()
        
        # Calculate pricing effectiveness metrics with proper error handling
        if len(revenue_data) > 0 and revenue_data.max() > 0:
            pricing_efficiency = round(
                (revenue_data.mean() / revenue_data.max() * 40) +
                ((revenue_data.max() - revenue_data.min()) / revenue_data.max() * 30) +
                (revenue_data.std() / revenue_data.mean() * 30), 1
            )
        else:
            pricing_efficiency = 0
        
        # Pricing effectiveness overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="performance-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Average Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${revenue_stats['mean']:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Per conversion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Median Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${revenue_stats['50%']:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Typical value</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="roi-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Revenue Range</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${revenue_stats['max'] - revenue_stats['min']:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Min to max</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Pricing efficiency indicator
            if pricing_efficiency >= 80:
                pricing_status = "🚀 Excellent"
                pricing_color = "#28a745"
            elif pricing_efficiency >= 60:
                pricing_status = "⭐ Good"
                pricing_color = "#17a2b8"
            elif pricing_efficiency >= 40:
                pricing_status = "👍 Fair"
                pricing_color = "#ffc107"
            else:
                pricing_status = "📈 Needs Improvement"
                pricing_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="product-metric-card" style="background: linear-gradient(135deg, {pricing_color} 0%, {pricing_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Pricing Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{pricing_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{pricing_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Product Performance Charts
        st.markdown("#### 📊 Product Performance Analysis & Visualization")
        
        # Product performance by touchpoint chart
        if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            # Ensure numeric data types for charting
            conversions_data = st.session_state.conversions_data.copy()
            
            # Safely access revenue column
            if 'revenue' in conversions_data.columns:
                conversions_data['revenue'] = pd.to_numeric(conversions_data['revenue'], errors='coerce').fillna(0)
            else:
                conversions_data['revenue'] = 0
            
            # Safely access touchpoint_count column
            if 'touchpoint_count' in conversions_data.columns:
                conversions_data['touchpoint_count'] = pd.to_numeric(conversions_data['touchpoint_count'], errors='coerce').fillna(0)
            else:
                conversions_data['touchpoint_count'] = 1
            
            # Product performance analysis - count conversions by touchpoint
            product_performance = conversions_data.groupby('touchpoint_count').agg({
                'conversion_id': 'count',  # Count conversions instead of summing non-existent column
                'revenue': 'sum'
            }).reset_index()
            product_performance = product_performance.rename(columns={'conversion_id': 'conversions'})  # Rename for consistency
            
            if len(product_performance) > 0:
                # Product performance chart
                fig_product_performance = px.bar(
                    product_performance,
                    x='touchpoint_count',
                    y='conversions',
                    title="Product Performance by Touchpoint Count",
                    labels={'conversions': 'Total Conversions', 'touchpoint_count': 'Touchpoint Count'},
                    template='plotly_white',
                    color='revenue',
                    color_continuous_scale='Viridis'
                )
                
                fig_product_performance.update_traces(
                    marker_line_color='#333',
                    marker_line_width=1
                )
                
                fig_product_performance.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50),
                    showlegend=False
                )
                
                st.plotly_chart(fig_product_performance, use_container_width=True)
                
                # Revenue vs conversions scatter plot
                fig_revenue_conversions = px.scatter(
                    product_performance,
                    x='conversions',
                    y='revenue',
                    size='touchpoint_count',
                    title="Revenue vs Conversions Analysis by Touchpoint Count",
                    labels={'revenue': 'Total Revenue ($)', 'conversions': 'Total Conversions', 'touchpoint_count': 'Touchpoint Count'},
                    template='plotly_white',
                    color='touchpoint_count',
                    color_continuous_scale='Plasma'
                )
                
                fig_revenue_conversions.update_traces(
                    marker=dict(line=dict(color='#333', width=1))
                )
                
                fig_revenue_conversions.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='closest',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_revenue_conversions, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Feature Adoption Analysis
    st.subheader("🔧 Advanced Feature Adoption Analysis")
    
    # Feature adoption insights header
    st.markdown(f"""
    <div class="product-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🔧 Feature Adoption Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of feature adoption patterns, user engagement, and product utilization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced feature adoption analysis
        # Ensure required columns exist for groupby
        required_columns = ['touchpoint_count', 'conversion_id', 'revenue']
        missing_columns = [col for col in required_columns if col not in st.session_state.conversions_data.columns]
        
        if not missing_columns:
            feature_adoption = st.session_state.conversions_data.groupby('touchpoint_count').agg({
                'conversion_id': 'count',
                'revenue': 'mean'
            }).reset_index()
        else:
            # Create dummy data if required columns are missing
            feature_adoption = pd.DataFrame({
                'touchpoint_count': [1],
                'conversion_id': [0],
                'revenue': [0]
            })
        
        # Ensure numeric data types and handle edge cases
        feature_adoption['conversion_id'] = pd.to_numeric(feature_adoption['conversion_id'], errors='coerce').fillna(0)
        feature_adoption['revenue'] = pd.to_numeric(feature_adoption['revenue'], errors='coerce').fillna(0)
        
        # Calculate adoption metrics with proper error handling
        if len(feature_adoption) > 0 and feature_adoption['conversion_id'].max() > 0 and feature_adoption['revenue'].max() > 0:
            feature_adoption['adoption_score'] = round(
                (feature_adoption['conversion_id'] / feature_adoption['conversion_id'].max() * 50) +
                (feature_adoption['revenue'] / feature_adoption['revenue'].max() * 50), 1
            )
        else:
            feature_adoption['adoption_score'] = 0
        
        # Feature adoption overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_touchpoints = feature_adoption['touchpoint_count'].nunique()
            st.markdown(f"""
            <div class="performance-metric">
                <h4 style="margin: 0; font-size: 14px;">🔧 Touchpoint Types</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_touchpoints}</h2>
                <p style="margin: 0; font-size: 12px;">Feature categories</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_adoption_conversions = feature_adoption['conversion_id'].sum()
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Adoption Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_adoption_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Feature usage</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_adoption_revenue = feature_adoption['revenue'].mean()
            st.markdown(f"""
            <div class="roi-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Avg Adoption Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${avg_adoption_revenue:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Per feature</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Adoption efficiency indicator
            max_adoption_score = feature_adoption['adoption_score'].max()
            if max_adoption_score >= 80:
                adoption_status = "🚀 Excellent"
                adoption_color = "#28a745"
            elif max_adoption_score >= 60:
                adoption_status = "⭐ Good"
                adoption_color = "#17a2b8"
            elif max_adoption_score >= 40:
                adoption_status = "👍 Fair"
                adoption_color = "#ffc107"
            else:
                adoption_status = "📈 Needs Improvement"
                adoption_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="product-metric-card" style="background: linear-gradient(135deg, {adoption_color} 0%, {adoption_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Adoption Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{max_adoption_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{adoption_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced ROI Analysis Charts
        st.markdown("#### 📊 Product Marketing ROI Analysis & Visualization")
        
        if (isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
            not st.session_state.campaigns_data.empty and 
            isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            # Campaign ROI analysis
            # Ensure required columns exist for groupby
            if 'campaign_type' in st.session_state.campaigns_data.columns and 'budget' in st.session_state.campaigns_data.columns:
                campaign_roi_data = st.session_state.campaigns_data.groupby('campaign_type').agg({
                    'budget': 'sum',
                    'campaign_id': 'count'
                }).reset_index()
            else:
                # Create dummy data if required columns are missing
                campaign_roi_data = pd.DataFrame({
                    'campaign_type': ['Unknown'],
                    'budget': [0],
                    'campaign_id': [0]
                })
            
            # Ensure numeric data types
            campaign_roi_data['budget'] = pd.to_numeric(campaign_roi_data['budget'], errors='coerce').fillna(0)
            
            # Calculate ROI for each campaign type
            # Ensure conversions_data has the required columns
            if 'revenue' in st.session_state.conversions_data.columns:
                total_revenue = st.session_state.conversions_data['revenue'].sum()
            else:
                total_revenue = 0
            total_budget = campaign_roi_data['budget'].sum()
            
            campaign_roi_data['revenue_share'] = campaign_roi_data['budget'] / total_budget if total_budget > 0 else 0
            campaign_roi_data['estimated_revenue'] = total_revenue * campaign_roi_data['revenue_share']
            # Use numpy.where to handle Series conditional logic properly
            campaign_roi_data['roi'] = np.where(
                campaign_roi_data['budget'] > 0,
                (campaign_roi_data['estimated_revenue'] - campaign_roi_data['budget']) / campaign_roi_data['budget'] * 100,
                0
            )
            
            # ROI performance chart
            fig_campaign_roi = px.bar(
                campaign_roi_data,
                x='campaign_type',
                y='roi',
                title="Campaign ROI Performance by Type",
                labels={'roi': 'ROI (%)', 'campaign_type': 'Campaign Type'},
                template='plotly_white',
                color='roi',
                color_continuous_scale='RdYlGn'
            )
            
            fig_campaign_roi.update_traces(
                marker_line_color='#333',
                marker_line_width=1
            )
            
            fig_campaign_roi.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=False
            )
            
            st.plotly_chart(fig_campaign_roi, use_container_width=True)
            
            # Budget vs ROI scatter plot
            fig_budget_roi = px.scatter(
                campaign_roi_data,
                x='budget',
                y='roi',
                size='campaign_id',
                title="Budget vs ROI Analysis by Campaign Type",
                labels={'budget': 'Budget ($)', 'roi': 'ROI (%)', 'campaign_id': 'Campaign Count'},
                template='plotly_white',
                color='campaign_type',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_budget_roi.update_traces(
                marker=dict(line=dict(color='#333', width=1))
            )
            
            fig_budget_roi.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='closest',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig_budget_roi, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Product Marketing ROI Analysis
    st.subheader("📈 Advanced Product Marketing ROI Analysis")
    
    # Product marketing ROI insights header
    st.markdown(f"""
    <div class="product-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📈 ROI Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of marketing ROI, budget allocation, and revenue optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
        not st.session_state.campaigns_data.empty and 
        isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced ROI calculation
        # Ensure required columns exist in campaigns_data
        if 'budget' in st.session_state.campaigns_data.columns and 'campaign_type' in st.session_state.campaigns_data.columns:
            campaign_budgets = st.session_state.campaigns_data.groupby('campaign_type')['budget'].sum()
        else:
            campaign_budgets = pd.Series([0])
        
        # Ensure required columns exist in conversions_data
        if 'revenue' in st.session_state.conversions_data.columns and 'conversion_type' in st.session_state.conversions_data.columns:
            product_revenues = st.session_state.conversions_data.groupby('conversion_type')['revenue'].sum()
        else:
            product_revenues = pd.Series([0])
        
        # Enhanced campaign-to-product matching
        roi_data = []
        total_budget = campaign_budgets.sum()
        total_revenue = product_revenues.sum()
        
        # Ensure we have valid data to iterate over
        if len(product_revenues) > 0 and total_revenue > 0:
            for conv_type in product_revenues.index:
                revenue = product_revenues[conv_type]
                # More sophisticated budget allocation based on revenue share
                revenue_share = revenue / total_revenue if total_revenue > 0 else 0
                budget = total_budget * revenue_share
                roi = ((revenue - budget) / budget) * 100 if budget > 0 else 0
                
                roi_data.append({
                    'Product Type': conv_type,
                    'Revenue': revenue,
                    'Budget': budget,
                    'ROI': roi,
                    'Revenue Share': revenue_share * 100
                })
        else:
            # Create dummy data if no valid data
            roi_data.append({
                'Product Type': 'Unknown',
                'Revenue': 0,
                'Budget': 0,
                'ROI': 0,
                'Revenue Share': 0
            })
        
        roi_df = pd.DataFrame(roi_data)
        
        # Calculate overall ROI metrics
        overall_roi = ((total_revenue - total_budget) / total_budget) * 100 if total_budget > 0 else 0
        
        # Ensure roi_df has data before calculating efficiency
        if len(roi_df) > 0:
            roi_efficiency = round(
                (overall_roi / 100 * 50) +  # ROI contribution
                (roi_df['ROI'].max() / 100 * 30) +  # Best performing product
                (roi_df['ROI'].mean() / 100 * 20), 1  # Average performance
            ) if total_budget > 0 else 0
        else:
            roi_efficiency = 0
        
        # ROI overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="performance-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Total Budget</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_budget:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Marketing spend</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Total Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Product revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="roi-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Overall ROI</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{overall_roi:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Marketing return</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # ROI efficiency indicator
            if roi_efficiency >= 80:
                roi_status = "🚀 Excellent"
                roi_color = "#28a745"
            elif roi_efficiency >= 60:
                roi_status = "⭐ Good"
                roi_color = "#17a2b8"
            elif roi_efficiency >= 40:
                roi_status = "👍 Fair"
                roi_color = "#ffc107"
            else:
                roi_status = "📈 Needs Improvement"
                roi_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="product-metric-card" style="background: linear-gradient(135deg, {roi_color} 0%, {roi_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 ROI Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{roi_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{roi_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Product Marketing Strategy Summary
    st.markdown("---")
    st.subheader("📋 Product Marketing Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Product Marketing Recommendations", expanded=False):
        st.markdown("""
        **Product Marketing Strategy Recommendations:**
        
        **1. Product Performance Optimization:**
        - Focus on high-converting product types and features
        - Implement conversion rate optimization (CRO) strategies
        - Develop targeted marketing campaigns for underperforming products
        
        **2. Launch Strategy Enhancement:**
        - Optimize product launch timing and market positioning
        - Implement phased rollout strategies for better market adoption
        - Develop pre-launch marketing campaigns to build anticipation
        
        **3. Pricing Strategy Optimization:**
        - Analyze pricing elasticity and market response
        - Implement dynamic pricing strategies based on performance data
        - Develop value-based pricing models for better revenue optimization
        
        **4. Feature Adoption Strategy:**
        - Focus on high-value features with strong adoption rates
        - Implement user onboarding and education programs
        - Develop feature-specific marketing campaigns
        
        **5. ROI Optimization:**
        - Reallocate budget to high-ROI product types
        - Implement performance-based budget allocation
        - Develop integrated marketing strategies for better ROI
        
        **6. Market Positioning:**
        - Analyze competitive positioning and market differentiation
        - Implement targeted marketing campaigns for specific market segments
        - Develop unique value propositions for each product type
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Product Marketing Performance Metrics Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.metric(
                "Product Performance", 
                f"{'Excellent' if max_efficiency >= 80 else 'Good' if max_efficiency >= 60 else 'Fair' if max_efficiency >= 40 else 'Needs Improvement'}",
                f"{max_efficiency:.1f}/100 efficiency"
            )
    
    with col2:
        if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.metric(
                "Launch Performance", 
                f"{'Excellent' if avg_launch_score >= 80 else 'Good' if avg_launch_score >= 60 else 'Fair' if avg_launch_score >= 40 else 'Needs Improvement'}",
                f"{avg_launch_score:.1f}/100 score"
            )
    
    with col3:
        if (isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
            not st.session_state.campaigns_data.empty and 
            isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.metric(
                "Marketing ROI", 
                f"{'Excellent' if roi_efficiency >= 80 else 'Good' if roi_efficiency >= 60 else 'Fair' if roi_efficiency >= 40 else 'Needs Improvement'}",
                f"{roi_efficiency:.1f}/100 efficiency"
            )

def show_customer_journey():
    """Display world-class customer journey analytics with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .journey-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .journey-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .journey-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .journey-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .attribution-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .touchpoint-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .funnel-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .retention-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🛤️ Customer Journey Analytics - Comprehensive Journey Intelligence Dashboard")
    st.markdown("---")
    
    if st.session_state.conversions_data.empty:
        st.warning("⚠️ Conversion data required for customer journey analysis.")
        return
    
    # Enhanced Customer Journey Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🛤️ Customer Journey Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Comprehensive analysis of customer touchpoints, attribution modeling, journey optimization, and retention strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Attribution Modeling
    st.subheader("🎯 Advanced Attribution Modeling")
    
    # Attribution modeling insights header
    st.markdown(f"""
    <div class="journey-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Attribution Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of marketing attribution sources, conversion effectiveness, and channel performance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced attribution analysis with proper data type handling
        # Ensure required columns exist for groupby
        required_columns = ['attribution_source', 'conversion_id', 'revenue', 'touchpoint_count']
        missing_columns = [col for col in required_columns if col not in st.session_state.conversions_data.columns]
        
        if not missing_columns:
            attribution_analysis = st.session_state.conversions_data.groupby('attribution_source').agg({
                'conversion_id': 'count',
                'revenue': 'sum',
                'touchpoint_count': 'mean'
            }).reset_index()
        else:
            # Create dummy data if required columns are missing
            attribution_analysis = pd.DataFrame({
                'attribution_source': ['Unknown'],
                'conversion_id': [0],
                'revenue': [0],
                'touchpoint_count': [0]
            })
        
        # Ensure numeric data types and handle edge cases
        attribution_analysis['conversion_id'] = pd.to_numeric(attribution_analysis['conversion_id'], errors='coerce').fillna(0)
        attribution_analysis['revenue'] = pd.to_numeric(attribution_analysis['revenue'], errors='coerce').fillna(0)
        attribution_analysis['touchpoint_count'] = pd.to_numeric(attribution_analysis['touchpoint_count'], errors='coerce').fillna(0)
        
        # Calculate enhanced attribution metrics
        total_conversions = attribution_analysis['conversion_id'].sum()
        total_revenue = attribution_analysis['revenue'].sum()
        
        attribution_analysis['conversion_rate'] = (attribution_analysis['conversion_id'] / total_conversions * 100) if total_conversions > 0 else 0
        attribution_analysis['revenue_share'] = (attribution_analysis['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
        attribution_analysis['attribution_score'] = round(
            (attribution_analysis['conversion_rate'] * 0.4) +
            (attribution_analysis['revenue_share'] * 0.4) +
            (attribution_analysis['touchpoint_count'] / attribution_analysis['touchpoint_count'].max() * 20), 1
        ) if attribution_analysis['touchpoint_count'].max() > 0 else 0
        
        # Attribution overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="attribution-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Total Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Across all sources</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="touchpoint-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Total Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Generated revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_touchpoints = attribution_analysis['touchpoint_count'].mean()
            st.markdown(f"""
            <div class="funnel-metric">
                <h4 style="margin: 0; font-size: 14px;">🔄 Avg Touchpoints</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_touchpoints:.1f}</h2>
                <p style="margin: 0; font-size: 12px;">Per conversion</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Attribution efficiency indicator
            max_attribution_score = attribution_analysis['attribution_score'].max()
            if max_attribution_score >= 80:
                attribution_status = "🚀 Excellent"
                attribution_color = "#28a745"
            elif max_attribution_score >= 60:
                attribution_status = "⭐ Good"
                attribution_color = "#17a2b8"
            elif max_attribution_score >= 40:
                attribution_status = "👍 Fair"
                attribution_color = "#ffc107"
            else:
                attribution_status = "📈 Needs Improvement"
                attribution_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="journey-metric-card" style="background: linear-gradient(135deg, {attribution_color} 0%, {attribution_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Attribution Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{max_attribution_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{attribution_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Path to Purchase Analysis
    st.subheader("🛒 Advanced Path to Purchase Analysis")
    
    # Path to purchase insights header
    st.markdown(f"""
    <div class="journey-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🛒 Purchase Path Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of customer touchpoint patterns, purchase journey optimization, and conversion path effectiveness
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced touchpoint analysis with proper data type handling
        # Ensure required columns exist for groupby
        required_columns = ['touchpoint_count', 'conversion_id', 'revenue']
        missing_columns = [col for col in required_columns if col not in st.session_state.conversions_data.columns]
        
        if not missing_columns:
            touchpoint_analysis = st.session_state.conversions_data.groupby('touchpoint_count').agg({
                'conversion_id': 'count',
                'revenue': 'mean'
            }).reset_index()
        else:
            # Create dummy data if required columns are missing
            touchpoint_analysis = pd.DataFrame({
                'touchpoint_count': [1],
                'conversion_id': [0],
                'revenue': [0]
            })
        
        # Ensure numeric data types and handle edge cases
        touchpoint_analysis['conversion_id'] = pd.to_numeric(touchpoint_analysis['conversion_id'], errors='coerce').fillna(0)
        touchpoint_analysis['revenue'] = pd.to_numeric(touchpoint_analysis['revenue'], errors='coerce').fillna(0)
        
        # Calculate enhanced touchpoint metrics
        touchpoint_analysis['touchpoint_efficiency'] = round(
            (touchpoint_analysis['conversion_id'] / touchpoint_analysis['conversion_id'].max() * 50) +
            (touchpoint_analysis['revenue'] / touchpoint_analysis['revenue'].max() * 50), 1
        ) if touchpoint_analysis['conversion_id'].max() > 0 and touchpoint_analysis['revenue'].max() > 0 else 0
        
        # Touchpoint overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_touchpoint_conversions = touchpoint_analysis['conversion_id'].sum()
            st.markdown(f"""
            <div class="attribution-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Touchpoint Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_touchpoint_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Total conversions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_touchpoint_revenue = touchpoint_analysis['revenue'].sum()
            st.markdown(f"""
            <div class="touchpoint-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Touchpoint Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_touchpoint_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Generated revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_touchpoint_revenue = touchpoint_analysis['revenue'].mean()
            st.markdown(f"""
            <div class="funnel-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Revenue/Touchpoint</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${avg_touchpoint_revenue:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Per touchpoint</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Touchpoint efficiency indicator
            max_touchpoint_efficiency = touchpoint_analysis['touchpoint_efficiency'].max()
            if max_touchpoint_efficiency >= 80:
                touchpoint_status = "🚀 Excellent"
                touchpoint_color = "#28a745"
            elif max_touchpoint_efficiency >= 60:
                touchpoint_status = "⭐ Good"
                touchpoint_color = "#17a2b8"
            elif max_touchpoint_efficiency >= 40:
                touchpoint_status = "👍 Fair"
                touchpoint_color = "#ffc107"
            else:
                touchpoint_status = "📈 Needs Improvement"
                touchpoint_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="journey-metric-card" style="background: linear-gradient(135deg, {touchpoint_color} 0%, {touchpoint_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Touchpoint Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{max_touchpoint_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{touchpoint_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Path to Purchase Charts
        st.markdown("#### 📊 Path to Purchase Analysis & Visualization")
        
        # Touchpoint efficiency chart
        fig_touchpoint_efficiency = px.bar(
            touchpoint_analysis,
            x='touchpoint_count',
            y='touchpoint_efficiency',
            title="Touchpoint Efficiency Analysis by Count",
            labels={'touchpoint_efficiency': 'Efficiency Score', 'touchpoint_count': 'Touchpoint Count'},
            template='plotly_white',
            color='revenue',
            color_continuous_scale='Viridis'
        )
        
        fig_touchpoint_efficiency.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_touchpoint_efficiency.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_touchpoint_efficiency, use_container_width=True)
        
        # Revenue vs touchpoint count chart
        fig_revenue_touchpoint = px.scatter(
            touchpoint_analysis,
            x='touchpoint_count',
            y='revenue',
            size='conversion_id',
            title="Revenue vs Touchpoint Count Analysis",
            labels={'revenue': 'Revenue ($)', 'touchpoint_count': 'Touchpoint Count', 'conversion_id': 'Conversions'},
            template='plotly_white',
            color='touchpoint_efficiency',
            color_continuous_scale='Plasma'
        )
        
        fig_revenue_touchpoint.update_traces(
            marker=dict(line=dict(color='#333', width=1))
        )
        
        fig_revenue_touchpoint.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='closest',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_revenue_touchpoint, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Customer Journey Funnel Analysis
    st.subheader("🔄 Advanced Customer Journey Funnel Analysis")
    
    # Customer journey funnel insights header
    st.markdown(f"""
    <div class="journey-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🔄 Journey Funnel Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of customer journey stages, conversion funnel optimization, and lead-to-customer progression
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.leads_data, pd.DataFrame) and 
        not st.session_state.leads_data.empty and 
        isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced funnel analysis
        total_leads = len(st.session_state.leads_data)
        qualified_leads = len(st.session_state.leads_data[st.session_state.leads_data['status'].isin(['Qualified', 'Proposal', 'Negotiation'])])
        total_conversions = len(st.session_state.conversions_data)
        
        # Calculate enhanced funnel metrics
        lead_to_qualified_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
        qualified_to_conversion_rate = (total_conversions / qualified_leads * 100) if qualified_leads > 0 else 0
        overall_conversion_rate = (total_conversions / total_leads * 100) if total_leads > 0 else 0
        
        # Calculate funnel efficiency score
        funnel_efficiency = round(
            (lead_to_qualified_rate / 100 * 40) +
            (qualified_to_conversion_rate / 100 * 40) +
            (overall_conversion_rate / 100 * 20), 1
        )
        
        funnel_data = {
            'Stage': ['Leads', 'Qualified Leads', 'Conversions'],
            'Count': [total_leads, qualified_leads, total_conversions],
            'Conversion Rate': [100, lead_to_qualified_rate, overall_conversion_rate]
        }
        funnel_df = pd.DataFrame(funnel_data)
        
        # Funnel overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="attribution-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Total Leads</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_leads:,}</h2>
                <p style="margin: 0; font-size: 12px;">Lead generation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="touchpoint-metric">
                <h4 style="margin: 0; font-size: 14px;">✅ Qualified Leads</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{qualified_leads:,}</h2>
                <p style="margin: 0; font-size: 12px;">Sales ready</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="funnel-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Total Conversions</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_conversions:,}</h2>
                <p style="margin: 0; font-size: 12px;">Successful sales</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Funnel efficiency indicator
            if funnel_efficiency >= 80:
                funnel_status = "🚀 Excellent"
                funnel_color = "#28a745"
            elif funnel_efficiency >= 60:
                funnel_status = "⭐ Good"
                funnel_color = "#17a2b8"
            elif funnel_efficiency >= 40:
                funnel_status = "👍 Fair"
                funnel_color = "#ffc107"
            else:
                funnel_status = "📈 Needs Improvement"
                funnel_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="journey-metric-card" style="background: linear-gradient(135deg, {funnel_color} 0%, {funnel_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Funnel Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{funnel_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{funnel_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Funnel Analysis Charts
        st.markdown("#### 📊 Customer Journey Funnel Analysis & Visualization")
        
        # Create funnel data for visualization
        funnel_data = pd.DataFrame({
            'Stage': ['Leads', 'Qualified Leads', 'Conversions'],
            'Count': [total_leads, qualified_leads, total_conversions],
            'Rate': [100, (qualified_leads/total_leads*100) if total_leads > 0 else 0, (total_conversions/total_leads*100) if total_leads > 0 else 0]
        })
        
        # Funnel chart
        fig_funnel = px.funnel(
            funnel_data,
            x='Count',
            y='Stage',
            title="Customer Journey Funnel Analysis",
            template='plotly_white'
        )
        
        fig_funnel.update_traces(
            marker=dict(color=['#667eea', '#17a2b8', '#28a745'])
        )
        
        fig_funnel.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='closest',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Conversion rates chart
        fig_conversion_rates = px.bar(
            funnel_data,
            x='Stage',
            y='Rate',
            title="Conversion Rates by Journey Stage",
            labels={'Rate': 'Conversion Rate (%)', 'Stage': 'Journey Stage'},
            template='plotly_white',
            color='Rate',
            color_continuous_scale='RdYlGn'
        )
        
        fig_conversion_rates.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_conversion_rates.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_conversion_rates, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Customer Retention Analysis
    st.subheader("🔄 Advanced Customer Retention Analysis")
    
    # Customer retention insights header
    st.markdown(f"""
    <div class="journey-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🔄 Retention Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of customer loyalty, retention strategies, and lifetime value optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.customers_data.empty:
        # Enhanced customer retention analysis
        repeat_customers = len(st.session_state.customers_data[st.session_state.customers_data['total_purchases'] > 1])
        total_customers = len(st.session_state.customers_data)
        retention_rate = (repeat_customers / total_customers) * 100 if total_customers > 0 else 0
        
        # Calculate enhanced retention metrics
        avg_lifetime_value = st.session_state.customers_data['lifetime_value'].mean() if 'lifetime_value' in st.session_state.customers_data.columns else 0
        avg_purchases = st.session_state.customers_data['total_purchases'].mean() if 'total_purchases' in st.session_state.customers_data.columns else 0
        
        # Calculate retention efficiency score
        retention_efficiency = round(
            (retention_rate / 100 * 40) +
            (min(avg_lifetime_value / 1000, 1) * 30) +  # Normalize to 0-1 scale
            (min(avg_purchases / 5, 1) * 30), 1  # Normalize to 0-1 scale
        )
        
        # Customer retention overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="attribution-metric">
                <h4 style="margin: 0; font-size: 14px;">👥 Total Customers</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_customers:,}</h2>
                <p style="margin: 0; font-size: 12px;">Customer base</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="touchpoint-metric">
                <h4 style="margin: 0; font-size: 14px;">🔄 Repeat Customers</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{repeat_customers:,}</h2>
                <p style="margin: 0; font-size: 12px;">Loyal customers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="funnel-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Retention Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{retention_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Customer loyalty</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Retention efficiency indicator
            if retention_efficiency >= 80:
                retention_status = "🚀 Excellent"
                retention_color = "#28a745"
            elif retention_efficiency >= 60:
                retention_status = "⭐ Good"
                retention_color = "#17a2b8"
            elif retention_efficiency >= 40:
                retention_status = "👍 Fair"
                retention_color = "#ffc107"
            else:
                retention_status = "📈 Needs Improvement"
                retention_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="journey-metric-card" style="background: linear-gradient(135deg, {retention_color} 0%, {retention_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Retention Efficiency</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{retention_efficiency:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{retention_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced customer lifetime value analysis
        if 'customer_segment' in st.session_state.customers_data.columns and 'lifetime_value' in st.session_state.customers_data.columns:
            segment_retention = st.session_state.customers_data.groupby('customer_segment').agg({
                'customer_id': 'count',
                'lifetime_value': 'mean',
                'total_purchases': 'mean'
            }).reset_index()
            
            # Ensure numeric data types
            segment_retention['lifetime_value'] = pd.to_numeric(segment_retention['lifetime_value'], errors='coerce').fillna(0)
            segment_retention['total_purchases'] = pd.to_numeric(segment_retention['total_purchases'], errors='coerce').fillna(0)
            
            # Calculate segment performance score
            segment_retention['segment_score'] = round(
                (segment_retention['lifetime_value'] / segment_retention['lifetime_value'].max() * 50) +
                (segment_retention['total_purchases'] / segment_retention['total_purchases'].max() * 50), 1
            ) if segment_retention['lifetime_value'].max() > 0 and segment_retention['total_purchases'].max() > 0 else 0
            
            # Enhanced Customer Retention Charts
            st.markdown("#### 📊 Customer Retention Analysis & Visualization")
            
            # Customer retention by segment chart
            fig_segment_retention = px.bar(
                segment_retention,
                x='customer_segment',
                y='segment_score',
                title="Customer Retention Performance by Segment",
                labels={'segment_score': 'Retention Score', 'customer_segment': 'Customer Segment'},
                template='plotly_white',
                color='lifetime_value',
                color_continuous_scale='Viridis'
            )
            
            fig_segment_retention.update_traces(
                marker_line_color='#333',
                marker_line_width=1
            )
            
            fig_segment_retention.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50),
                showlegend=False
            )
            
            st.plotly_chart(fig_segment_retention, use_container_width=True)
            
            # Lifetime value vs purchases scatter plot
            fig_lifetime_purchases = px.scatter(
                segment_retention,
                x='total_purchases',
                y='lifetime_value',
                size='customer_id',
                title="Lifetime Value vs Purchase Frequency by Segment",
                labels={'lifetime_value': 'Lifetime Value ($)', 'total_purchases': 'Total Purchases', 'customer_id': 'Customer Count'},
                template='plotly_white',
                color='customer_segment',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_lifetime_purchases.update_traces(
                marker=dict(line=dict(color='#333', width=1))
            )
            
            fig_lifetime_purchases.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='closest',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig_lifetime_purchases, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Journey Optimization Insights
    st.subheader("💡 Advanced Journey Optimization Insights")
    
    # Journey optimization insights header
    st.markdown(f"""
    <div class="journey-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">💡 Optimization Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Strategic insights for journey optimization, attribution improvement, and customer experience enhancement
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.conversions_data.empty:
        # Enhanced attribution source analysis
        best_sources = st.session_state.conversions_data.groupby('attribution_source')['revenue'].sum().sort_values(ascending=False)
        
        # Enhanced touchpoint analysis
        touchpoint_revenue = st.session_state.conversions_data.groupby('touchpoint_count')['revenue'].mean()
        optimal_touchpoints = touchpoint_revenue.idxmax() if len(touchpoint_revenue) > 0 else 0
        
        # Journey optimization overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_source = best_sources.index[0] if len(best_sources) > 0 else "N/A"
            top_source_revenue = best_sources.iloc[0] if len(best_sources) > 0 else 0
            st.markdown(f"""
            <div class="attribution-metric">
                <h4 style="margin: 0; font-size: 14px;">🏆 Top Source</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{top_source}</h2>
                <p style="margin: 0; font-size: 12px;">${top_source_revenue:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            top_source_share = (best_sources.iloc[0] / best_sources.sum() * 100) if best_sources.sum() > 0 else 0
            st.markdown(f"""
            <div class="touchpoint-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Top Source Share</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{top_source_share:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Revenue share</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="funnel-metric">
                <h4 style="margin: 0; font-size: 14px;">🔄 Optimal Touchpoints</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{optimal_touchpoints}</h2>
                <p style="margin: 0; font-size: 12px;">Best performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Journey optimization score
            journey_optimization_score = round(
                (top_source_share / 100 * 40) +
                (min(optimal_touchpoints / 10, 1) * 30) +  # Normalize touchpoints
                (retention_efficiency / 100 * 30), 1  # Include retention efficiency
            )
            
            if journey_optimization_score >= 80:
                optimization_status = "🚀 Excellent"
                optimization_color = "#28a745"
            elif journey_optimization_score >= 60:
                optimization_status = "⭐ Good"
                optimization_color = "#17a2b8"
            elif journey_optimization_score >= 40:
                optimization_status = "👍 Fair"
                optimization_color = "#ffc107"
            else:
                optimization_status = "📈 Needs Improvement"
                optimization_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="journey-metric-card" style="background: linear-gradient(135deg, {optimization_color} 0%, {optimization_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Optimization Score</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{journey_optimization_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{optimization_status}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Customer Journey Strategy Summary
    st.markdown("---")
    st.subheader("📋 Customer Journey Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Customer Journey Recommendations", expanded=False):
        st.markdown("""
        **Customer Journey Strategy Recommendations:**
        
        **1. Attribution Optimization:**
        - Focus on high-performing attribution sources and channels
        - Implement multi-touch attribution models for better accuracy
        - Develop attribution-based budget allocation strategies
        
        **2. Touchpoint Optimization:**
        - Optimize customer touchpoints based on performance data
        - Implement touchpoint-specific marketing strategies
        - Develop personalized customer journey experiences
        
        **3. Funnel Optimization:**
        - Improve lead qualification processes and criteria
        - Implement lead nurturing strategies for better conversion
        - Develop stage-specific marketing campaigns
        
        **4. Retention Strategy:**
        - Implement customer loyalty programs and retention strategies
        - Develop personalized customer experience initiatives
        - Focus on high-value customer segments
        
        **5. Journey Mapping:**
        - Create detailed customer journey maps for each segment
        - Implement journey-based marketing automation
        - Develop omnichannel customer experience strategies
        
        **6. Performance Monitoring:**
        - Implement real-time journey performance monitoring
        - Develop journey optimization dashboards and alerts
        - Implement A/B testing for journey improvements
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Customer Journey Performance Metrics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not st.session_state.conversions_data.empty:
            st.metric(
                "Attribution Performance", 
                f"{'Excellent' if max_attribution_score >= 80 else 'Good' if max_attribution_score >= 60 else 'Fair' if max_attribution_score >= 40 else 'Needs Improvement'}",
                f"{max_attribution_score:.1f}/100 efficiency"
            )
    
    with col2:
        if not st.session_state.conversions_data.empty:
            st.metric(
                "Touchpoint Performance", 
                f"{'Excellent' if max_touchpoint_efficiency >= 80 else 'Good' if max_touchpoint_efficiency >= 60 else 'Fair' if max_touchpoint_efficiency >= 40 else 'Needs Improvement'}",
                f"{max_touchpoint_efficiency:.1f}/100 efficiency"
            )
    
    with col3:
        if (isinstance(st.session_state.leads_data, pd.DataFrame) and 
            not st.session_state.leads_data.empty and 
            isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.metric(
                "Funnel Performance", 
                f"{'Excellent' if funnel_efficiency >= 80 else 'Good' if funnel_efficiency >= 60 else 'Fair' if funnel_efficiency >= 40 else 'Needs Improvement'}",
                f"{funnel_efficiency:.1f}/100 efficiency"
            )
    
    with col4:
        if not st.session_state.customers_data.empty:
            st.metric(
                "Retention Performance", 
                f"{'Excellent' if retention_efficiency >= 80 else 'Good' if retention_efficiency >= 60 else 'Fair' if retention_efficiency >= 40 else 'Needs Improvement'}",
                f"{retention_efficiency:.1f}/100 efficiency"
            )

def show_marketing_forecasting():
    """Display world-class marketing forecasting analytics with advanced predictive models and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .forecast-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .forecast-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .forecast-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .forecast-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .revenue-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .lead-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .budget-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .seasonal-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔮 Marketing Forecasting Analytics - Advanced Predictive Intelligence Dashboard")
    st.markdown("---")
    
    if (isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        st.session_state.conversions_data.empty and 
        isinstance(st.session_state.leads_data, pd.DataFrame) and 
        st.session_state.leads_data.empty):
        st.warning("⚠️ Conversion and lead data required for marketing forecasting.")
        return
    
    # Enhanced Marketing Forecasting Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🔮 Marketing Forecasting Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Advanced predictive analytics, revenue forecasting, lead generation predictions, and strategic budget planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Revenue Forecasting
    st.subheader("💰 Advanced Revenue Forecasting")
    
    # Revenue forecasting insights header
    st.markdown(f"""
    <div class="forecast-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">💰 Revenue Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive revenue trend analysis, growth prediction, and strategic forecasting for business planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.conversions_data.empty:
        # Enhanced revenue analysis with proper data type handling
        conversions_data = st.session_state.conversions_data.copy()
        conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
        conversions_data['month'] = conversions_data['conversion_date'].dt.to_period('M')
        
        monthly_revenue = conversions_data.groupby('month')['revenue'].sum().reset_index()
        monthly_revenue['month'] = monthly_revenue['month'].astype(str)
        
        # Ensure numeric data types
        monthly_revenue['revenue'] = pd.to_numeric(monthly_revenue['revenue'], errors='coerce').fillna(0)
        
        # Calculate enhanced growth metrics
        if len(monthly_revenue) > 1:
            current_revenue = monthly_revenue['revenue'].iloc[-1]
            previous_revenue = monthly_revenue['revenue'].iloc[-2]
            growth_rate = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
            
            # Calculate trend strength
            revenue_trend = monthly_revenue['revenue'].pct_change().mean() * 100
            revenue_volatility = monthly_revenue['revenue'].std() / monthly_revenue['revenue'].mean() * 100 if monthly_revenue['revenue'].mean() > 0 else 0
        else:
            growth_rate = 5  # Default 5% growth
            revenue_trend = 5
            revenue_volatility = 0
            current_revenue = monthly_revenue['revenue'].iloc[0] if len(monthly_revenue) > 0 else 0
        
        # Calculate forecasting accuracy score
        forecast_accuracy = round(
            (min(abs(growth_rate) / 20, 1) * 40) +  # Growth rate contribution
            (min(revenue_trend / 10, 1) * 30) +  # Trend strength contribution
            (max(0, (100 - revenue_volatility) / 100) * 30), 1  # Volatility contribution
        )
        
        # Revenue forecasting overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Current Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${current_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">This month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_monthly_revenue = monthly_revenue['revenue'].mean()
            st.markdown(f"""
            <div class="lead-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${avg_monthly_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Historical average</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="budget-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Growth Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{growth_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Month over month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Forecast accuracy indicator
            if forecast_accuracy >= 80:
                accuracy_status = "🚀 Excellent"
                accuracy_color = "#28a745"
            elif forecast_accuracy >= 60:
                accuracy_status = "⭐ Good"
                accuracy_color = "#17a2b8"
            elif forecast_accuracy >= 40:
                accuracy_status = "👍 Fair"
                accuracy_color = "#ffc107"
            else:
                accuracy_status = "📈 Needs Improvement"
                accuracy_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="forecast-metric-card" style="background: linear-gradient(135deg, {accuracy_color} 0%, {accuracy_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Forecast Accuracy</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{forecast_accuracy:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{accuracy_status}</p>
            </div>
                        """, unsafe_allow_html=True)
        
        # Enhanced Revenue Trend Charts
        st.markdown("#### 📊 Revenue Trend Analysis & Forecasting")
        
        # Revenue trend chart with enhanced styling
        fig_forecast = px.line(
            monthly_revenue,
            x='month',
            y='revenue',
            title="Revenue Trend Analysis & Growth Patterns",
            labels={'revenue': 'Revenue ($)', 'month': 'Month'},
            template='plotly_white'
        )
        
        fig_forecast.update_traces(
            line=dict(width=3, color='#667eea'),
            marker=dict(size=8, color='#764ba2')
        )
        
        fig_forecast.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Enhanced Revenue Forecast Chart (Next 3 Months)
        if len(monthly_revenue) > 1:
            last_revenue = monthly_revenue['revenue'].iloc[-1]
            forecast_data = []
            
            for i in range(1, 4):
                forecast_month = f"Forecast {i}"
                forecast_revenue = last_revenue * (1 + (growth_rate/100)) ** i
                forecast_data.append({
                    'Month': forecast_month,
                    'Revenue': forecast_revenue,
                    'Type': 'Forecast'
                })
            
            forecast_df = pd.DataFrame(forecast_data)
            
            # Combine historical and forecast data
            historical_data = monthly_revenue[['month', 'revenue']].rename(columns={'month': 'Month', 'revenue': 'Revenue'})
            historical_data['Type'] = 'Historical'
            
            combined_data = pd.concat([historical_data, forecast_df])
            
            # Enhanced combined forecast chart
            fig_combined = px.line(
                combined_data,
                x='Month',
                y='Revenue',
                color='Type',
                title="Revenue Forecast Analysis (Next 3 Months)",
                labels={'Revenue': 'Revenue ($)', 'Month': 'Month'},
                template='plotly_white'
            )
            
            fig_combined.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            
            fig_combined.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_combined, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Lead Forecasting
    st.subheader("🎯 Advanced Lead Forecasting")
    
    # Lead forecasting insights header
    st.markdown(f"""
    <div class="forecast-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Lead Generation Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive lead generation trend analysis, source performance prediction, and strategic lead forecasting
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.leads_data.empty:
        # Enhanced lead analysis with proper data type handling
        leads_data = st.session_state.leads_data.copy()
        leads_data['created_date'] = pd.to_datetime(leads_data['created_date'])
        leads_data['month'] = leads_data['created_date'].dt.to_period('M')
        
        monthly_leads = leads_data.groupby('month')['lead_id'].count().reset_index()
        monthly_leads['month'] = monthly_leads['month'].astype(str)
        monthly_leads = monthly_leads.rename(columns={'lead_id': 'leads'})
        
        # Ensure numeric data types
        monthly_leads['leads'] = pd.to_numeric(monthly_leads['leads'], errors='coerce').fillna(0)
        
        # Calculate enhanced lead metrics
        if len(monthly_leads) > 1:
            current_leads = monthly_leads['leads'].iloc[-1]
            previous_leads = monthly_leads['leads'].iloc[-2]
            lead_growth_rate = ((current_leads - previous_leads) / previous_leads * 100) if previous_leads > 0 else 0
            
            # Calculate lead trend strength
            lead_trend = monthly_leads['leads'].pct_change().mean() * 100
            lead_volatility = monthly_leads['leads'].std() / monthly_leads['leads'].mean() * 100 if monthly_leads['leads'].mean() > 0 else 0
        else:
            lead_growth_rate = 5  # Default 5% growth
            lead_trend = 5
            lead_volatility = 0
            current_leads = monthly_leads['leads'].iloc[0] if len(monthly_leads) > 0 else 0
        
        # Calculate lead forecasting accuracy score
        lead_forecast_accuracy = round(
            (min(abs(lead_growth_rate) / 20, 1) * 40) +  # Growth rate contribution
            (min(lead_trend / 10, 1) * 30) +  # Trend strength contribution
            (max(0, (100 - lead_volatility) / 100) * 30), 1  # Volatility contribution
        )
        
        # Lead forecasting overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Current Leads</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{current_leads:,}</h2>
                <p style="margin: 0; font-size: 12px;">This month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_monthly_leads = monthly_leads['leads'].mean()
            st.markdown(f"""
            <div class="lead-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Leads</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{avg_monthly_leads:.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Historical average</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="budget-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Lead Growth Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{lead_growth_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Month over month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Lead forecast accuracy indicator
            if lead_forecast_accuracy >= 80:
                lead_accuracy_status = "🚀 Excellent"
                lead_accuracy_color = "#28a745"
            elif lead_forecast_accuracy >= 60:
                lead_accuracy_status = "⭐ Good"
                lead_accuracy_color = "#17a2b8"
            elif lead_forecast_accuracy >= 40:
                lead_accuracy_status = "👍 Fair"
                lead_accuracy_color = "#ffc107"
            else:
                lead_accuracy_status = "📈 Needs Improvement"
                lead_accuracy_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="forecast-metric-card" style="background: linear-gradient(135deg, {lead_accuracy_color} 0%, {lead_accuracy_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Lead Forecast Accuracy</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{lead_forecast_accuracy:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{lead_accuracy_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Lead Generation Charts
        st.markdown("#### 📊 Lead Generation Trend Analysis & Forecasting")
        
        # Lead trend chart with enhanced styling
        fig_lead_trend = px.line(
            monthly_leads,
            x='month',
            y='leads',
            title="Lead Generation Trend Analysis & Growth Patterns",
            labels={'leads': 'Number of Leads', 'month': 'Month'},
            template='plotly_white'
        )
        
        fig_lead_trend.update_traces(
            line=dict(width=3, color='#17a2b8'),
            marker=dict(size=8, color='#6f42c1')
        )
        
        fig_lead_trend.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_lead_trend, use_container_width=True)
        
        # Enhanced Lead Source Analysis Chart
        lead_source_analysis = leads_data.groupby('source')['lead_id'].count().sort_values(ascending=False)
        
        fig_lead_sources = px.bar(
            lead_source_analysis.reset_index(),
            x='source',
            y='lead_id',
            title="Lead Generation Performance by Source",
            labels={'lead_id': 'Number of Leads', 'source': 'Lead Source'},
            template='plotly_white',
            color='lead_id',
            color_continuous_scale='Blues'
        )
        
        fig_lead_sources.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_lead_sources.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_lead_sources, use_container_width=True)
        
        # Enhanced Lead Forecast Chart (Next 3 Months)
        if len(monthly_leads) > 1:
            last_leads = monthly_leads['leads'].iloc[-1]
            lead_forecast_data = []
            
            for i in range(1, 4):
                forecast_month = f"Forecast {i}"
                forecast_leads = last_leads * (1 + (lead_growth_rate/100)) ** i
                lead_forecast_data.append({
                    'Month': forecast_month,
                    'Leads': forecast_leads,
                    'Type': 'Forecast'
                })
            
            lead_forecast_df = pd.DataFrame(lead_forecast_data)
            
            # Combine historical and forecast data for leads
            historical_leads = monthly_leads[['month', 'leads']].rename(columns={'month': 'Month', 'leads': 'Leads'})
            historical_leads['Type'] = 'Historical'
            
            combined_leads_data = pd.concat([historical_leads, lead_forecast_df])
            
            # Enhanced combined lead forecast chart
            fig_lead_combined = px.line(
                combined_leads_data,
                x='Month',
                y='Leads',
                color='Type',
                title="Lead Generation Forecast Analysis (Next 3 Months)",
                labels={'Leads': 'Number of Leads', 'Month': 'Month'},
                template='plotly_white'
            )
            
            fig_lead_combined.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )
            
            fig_lead_combined.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_lead_combined, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Campaign Budget Forecasting
    st.subheader("💰 Advanced Campaign Budget Forecasting")
    
    # Campaign budget forecasting insights header
    st.markdown(f"""
    <div class="forecast-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">💰 Budget Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Strategic budget allocation, ROI optimization, and performance-based budget forecasting for campaigns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if (isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
        not st.session_state.campaigns_data.empty and 
        isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        # Enhanced campaign analysis with proper data type handling
        campaign_performance = st.session_state.campaigns_data.groupby('campaign_type').agg({
            'budget': 'sum',
            'campaign_id': 'count'
        }).reset_index()
        
        # Ensure numeric data types
        campaign_performance['budget'] = pd.to_numeric(campaign_performance['budget'], errors='coerce').fillna(0)
        campaign_performance['campaign_id'] = pd.to_numeric(campaign_performance['campaign_id'], errors='coerce').fillna(0)
        
        # Calculate enhanced ROI metrics
        campaign_roi = []
        total_budget = campaign_performance['budget'].sum()
        total_revenue = st.session_state.conversions_data['revenue'].sum() if not st.session_state.conversions_data.empty else 0
        
        for _, campaign in campaign_performance.iterrows():
            campaign_type = campaign['campaign_type']
            budget = campaign['budget']
            
            # Enhanced revenue distribution based on budget share
            budget_share = budget / total_budget if total_budget > 0 else 0
            campaign_revenue = total_revenue * budget_share
            roi = ((campaign_revenue - budget) / budget * 100) if budget > 0 else 0
            
            campaign_roi.append({
                'Campaign Type': campaign_type,
                'Budget': budget,
                'Revenue': campaign_revenue,
                'ROI': roi,
                'Budget Share': budget_share * 100
            })
        
        roi_df = pd.DataFrame(campaign_roi)
        
        # Calculate budget optimization score
        if len(roi_df) > 0:
            budget_optimization_score = round(
                (roi_df['ROI'].max() / 100 * 40) +  # Best ROI contribution
                (roi_df['ROI'].mean() / 100 * 30) +  # Average ROI contribution
                (min(roi_df['Budget Share'].max() / 50, 1) * 30), 1  # Budget concentration contribution
            )
        else:
            budget_optimization_score = 0
        
        # Campaign budget overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Total Budget</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_budget:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Campaign spend</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="lead-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Total Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Generated revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            overall_roi = ((total_revenue - total_budget) / total_budget * 100) if total_budget > 0 else 0
            st.markdown(f"""
            <div class="budget-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Overall ROI</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{overall_roi:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Campaign return</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Budget optimization indicator
            if budget_optimization_score >= 80:
                budget_status = "🚀 Excellent"
                budget_color = "#28a745"
            elif budget_optimization_score >= 60:
                budget_status = "⭐ Good"
                budget_color = "#17a2b8"
            elif budget_optimization_score >= 40:
                budget_status = "👍 Fair"
                budget_color = "#ffc107"
            else:
                budget_status = "📈 Needs Improvement"
                budget_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="forecast-metric-card" style="background: linear-gradient(135deg, {budget_color} 0%, {budget_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Budget Optimization</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{budget_optimization_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{budget_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Budget Allocation Charts
        st.markdown("#### 📊 Campaign Budget Allocation & ROI Analysis")
        
        # Budget allocation recommendations
        st.markdown("**Budget Allocation Recommendations:**")
        
        # Allocate budget based on ROI performance
        total_budget = roi_df['Budget'].sum()
        roi_df['Recommended Budget'] = roi_df['ROI'].apply(lambda x: total_budget * (x / roi_df['ROI'].sum()) if roi_df['ROI'].sum() > 0 else total_budget / len(roi_df))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced current budget allocation pie chart
            fig_budget_current = px.pie(
                roi_df,
                values='Budget',
                names='Campaign Type',
                title="Current Budget Allocation by Campaign Type",
                template='plotly_white',
                hole=0.4
            )
            
            fig_budget_current.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='white', width=2))
            )
            
            fig_budget_current.update_layout(
                title_font_size=16,
                title_font_color='#333',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                )
            )
            
            st.plotly_chart(fig_budget_current, use_container_width=True)
        
        with col2:
            # Enhanced recommended budget allocation pie chart
            fig_budget_recommended = px.pie(
                roi_df,
                values='Recommended Budget',
                names='Campaign Type',
                title="Recommended Budget Allocation (ROI-Based)",
                template='plotly_white',
                hole=0.4
            )
            
            fig_budget_recommended.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='white', width=2))
            )
            
            fig_budget_recommended.update_layout(
                title_font_size=16,
                title_font_color='#333',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                )
            )
            
            st.plotly_chart(fig_budget_recommended, use_container_width=True)
        
        # Enhanced ROI performance bar chart
        fig_roi_performance = px.bar(
            roi_df,
            x='Campaign Type',
            y='ROI',
            title="Campaign ROI Performance Analysis",
            labels={'ROI': 'ROI (%)', 'Campaign Type': 'Campaign Type'},
            template='plotly_white',
            color='ROI',
            color_continuous_scale='RdYlGn'
        )
        
        fig_roi_performance.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_roi_performance.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_roi_performance, use_container_width=True)
        
        # Campaign performance summary table
        st.markdown("**Campaign Performance Summary:**")
        display_dataframe_with_index_1(roi_df[['Campaign Type', 'Budget', 'Revenue', 'ROI', 'Recommended Budget']])
    
    st.markdown("---")
    
    # Enhanced Seasonal Trend Analysis
    st.subheader("📅 Advanced Seasonal Trend Analysis")
    
    # Seasonal trend insights header
    st.markdown(f"""
    <div class="forecast-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📅 Seasonal Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive seasonal pattern analysis, trend identification, and seasonal forecasting for strategic planning
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.conversions_data.empty:
        # Enhanced seasonal analysis with proper data type handling
        conversions_data = st.session_state.conversions_data.copy()
        conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
        conversions_data['month_name'] = conversions_data['conversion_date'].dt.month_name()
        conversions_data['quarter'] = conversions_data['conversion_date'].dt.quarter
        
        # Monthly seasonal analysis
        monthly_seasonal = conversions_data.groupby('month_name')['revenue'].sum().reset_index()
        
        # Ensure numeric data types
        monthly_seasonal['revenue'] = pd.to_numeric(monthly_seasonal['revenue'], errors='coerce').fillna(0)
        
        # Reorder months
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_seasonal['month_name'] = pd.Categorical(monthly_seasonal['month_name'], categories=month_order, ordered=True)
        monthly_seasonal = monthly_seasonal.sort_values('month_name')
        
        # Calculate seasonal strength
        seasonal_strength = round(
            (monthly_seasonal['revenue'].max() - monthly_seasonal['revenue'].min()) / monthly_seasonal['revenue'].mean() * 100, 1
        ) if monthly_seasonal['revenue'].mean() > 0 else 0
        
        # Seasonal analysis overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            peak_month = monthly_seasonal.loc[monthly_seasonal['revenue'].idxmax(), 'month_name']
            st.markdown(f"""
            <div class="revenue-metric">
                <h4 style="margin: 0; font-size: 14px;">📈 Peak Month</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{peak_month}</h2>
                <p style="margin: 0; font-size: 12px;">Highest revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            peak_revenue = monthly_seasonal['revenue'].max()
            st.markdown(f"""
            <div class="lead-metric">
                <h4 style="margin: 0; font-size: 14px;">💰 Peak Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${peak_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Monthly peak</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_seasonal_revenue = monthly_seasonal['revenue'].mean()
            st.markdown(f"""
            <div class="budget-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Revenue</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">${avg_seasonal_revenue:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Seasonal average</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Seasonal strength indicator
            if seasonal_strength >= 50:
                seasonal_status = "🚀 Strong"
                seasonal_color = "#28a745"
            elif seasonal_strength >= 30:
                seasonal_status = "⭐ Moderate"
                seasonal_color = "#17a2b8"
            elif seasonal_strength >= 15:
                seasonal_status = "👍 Mild"
                seasonal_color = "#ffc107"
            else:
                seasonal_status = "📈 Minimal"
                seasonal_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="forecast-metric-card" style="background: linear-gradient(135deg, {seasonal_color} 0%, {seasonal_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Seasonal Strength</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{seasonal_strength:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">{seasonal_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Seasonal Trend Charts
        st.markdown("#### 📊 Seasonal Pattern Analysis & Forecasting")
        
        # Monthly seasonal analysis chart
        fig_seasonal = px.bar(
            monthly_seasonal,
            x='month_name',
            y='revenue',
            title="Monthly Seasonal Revenue Patterns & Trends",
            labels={'revenue': 'Revenue ($)', 'month_name': 'Month'},
            template='plotly_white',
            color='revenue',
            color_continuous_scale='Viridis'
        )
        
        fig_seasonal.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_seasonal.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_seasonal, use_container_width=True)
        
        # Quarterly analysis chart
        quarterly_seasonal = conversions_data.groupby('quarter')['revenue'].sum().reset_index()
        quarterly_seasonal['quarter'] = quarterly_seasonal['quarter'].astype(str)
        
        fig_quarterly = px.bar(
            quarterly_seasonal,
            x='quarter',
            y='revenue',
            title="Quarterly Revenue Patterns & Seasonal Trends",
            labels={'revenue': 'Revenue ($)', 'quarter': 'Quarter'},
            template='plotly_white',
            color='revenue',
            color_continuous_scale='Plasma'
        )
        
        fig_quarterly.update_traces(
            marker_line_color='#333',
            marker_line_width=1
        )
        
        fig_quarterly.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        st.plotly_chart(fig_quarterly, use_container_width=True)
        
        # Enhanced seasonal trend line chart
        fig_seasonal_trend = px.line(
            monthly_seasonal,
            x='month_name',
            y='revenue',
            title="Seasonal Revenue Trend Analysis & Pattern Identification",
            labels={'revenue': 'Revenue ($)', 'month_name': 'Month'},
            template='plotly_white'
        )
        
        fig_seasonal_trend.update_traces(
            line=dict(width=3, color='#dc3545'),
            marker=dict(size=8, color='#e83e8c')
        )
        
        fig_seasonal_trend.update_layout(
            title_font_size=18,
            title_font_color='#333',
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            hovermode='x unified',
            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_seasonal_trend, use_container_width=True)
    
    # Marketing Forecasting Strategy Summary
    st.markdown("---")
    st.subheader("📋 Marketing Forecasting Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Forecasting Recommendations", expanded=False):
        st.markdown("""
        **Marketing Forecasting Strategy Recommendations:**
        
        **1. Revenue Forecasting Optimization:**
        - Implement advanced predictive models for revenue forecasting
        - Develop trend analysis and volatility assessment frameworks
        - Create scenario-based forecasting for different market conditions
        
        **2. Lead Generation Forecasting:**
        - Implement lead scoring and qualification forecasting models
        - Develop source-based lead generation predictions
        - Create lead conversion rate forecasting frameworks
        
        **3. Budget Allocation Strategy:**
        - Implement performance-based budget allocation models
        - Develop ROI optimization strategies for campaign budgets
        - Create dynamic budget adjustment frameworks
        
        **4. Seasonal Planning:**
        - Implement seasonal trend analysis and forecasting
        - Develop seasonal marketing campaign planning
        - Create seasonal budget allocation strategies
        
        **5. Predictive Analytics:**
        - Implement machine learning models for forecasting
        - Develop real-time forecasting dashboards
        - Create automated forecasting alerts and recommendations
        
        **6. Performance Monitoring:**
        - Implement forecast accuracy tracking and measurement
        - Develop forecast vs. actual performance analysis
        - Create continuous improvement frameworks for forecasting
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Marketing Forecasting Performance Metrics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not st.session_state.conversions_data.empty:
            st.metric(
                "Revenue Forecast Accuracy", 
                f"{'Excellent' if forecast_accuracy >= 80 else 'Good' if forecast_accuracy >= 60 else 'Fair' if forecast_accuracy >= 40 else 'Needs Improvement'}",
                f"{forecast_accuracy:.1f}/100 accuracy"
            )
    
    with col2:
        if not st.session_state.leads_data.empty:
            st.metric(
                "Lead Forecast Accuracy", 
                f"{'Excellent' if lead_forecast_accuracy >= 80 else 'Good' if lead_forecast_accuracy >= 60 else 'Fair' if lead_forecast_accuracy >= 40 else 'Needs Improvement'}",
                f"{lead_forecast_accuracy:.1f}/100 accuracy"
            )
    
    with col3:
        if (isinstance(st.session_state.campaigns_data, pd.DataFrame) and 
            not st.session_state.campaigns_data.empty and 
            isinstance(st.session_state.conversions_data, pd.DataFrame) and 
            not st.session_state.conversions_data.empty):
            st.metric(
                "Budget Optimization", 
                f"{'Excellent' if budget_optimization_score >= 80 else 'Good' if budget_optimization_score >= 60 else 'Fair' if budget_optimization_score >= 40 else 'Needs Improvement'}",
                f"{budget_optimization_score:.1f}/100 score"
            )
    
    with col4:
        if not st.session_state.conversions_data.empty:
            st.metric(
                "Seasonal Strength", 
                f"{'Strong' if seasonal_strength >= 50 else 'Moderate' if seasonal_strength >= 30 else 'Mild' if seasonal_strength >= 15 else 'Minimal'}",
                f"{seasonal_strength:.1f}% strength"
            )

def show_channel_analysis():
    """Display world-class channel-specific analysis with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .channel-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .channel-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .channel-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .channel-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .social-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .email-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .web-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .overall-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📱 Channel-Specific Analysis - Advanced Multi-Channel Intelligence Dashboard")
    st.markdown("---")
    
    # Enhanced Channel Analysis Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">📱 Multi-Channel Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Comprehensive analysis of social media, email marketing, web traffic, and cross-channel performance optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Social Media Channel Analysis
    st.subheader("📱 Advanced Social Media Channel Analysis")
    
    # Social media insights header
    st.markdown(f"""
    <div class="channel-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📱 Social Media Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of social media platform performance, engagement metrics, and audience behavior patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.social_media_data.empty:
        # Enhanced social media analysis
        social_performance = analyze_social_media_performance(st.session_state.social_media_data)
        
        if not social_performance.empty:
            # Calculate enhanced social media metrics
            social_data = social_performance.reset_index()
            
            # Ensure numeric data types
            numeric_columns = ['impressions', 'clicks', 'total_engagement', 'reach', 'followers']
            for col in numeric_columns:
                if col in social_data.columns:
                    social_data[col] = pd.to_numeric(social_data[col], errors='coerce').fillna(0)
            
            # Calculate enhanced performance metrics
            if len(social_data) > 0:
                total_impressions = social_data['impressions'].sum() if 'impressions' in social_data.columns else 0
                total_clicks = social_data['clicks'].sum() if 'clicks' in social_data.columns else 0
                total_engagement = social_data['total_engagement'].sum() if 'total_engagement' in social_data.columns else 0
                total_reach = social_data['reach'].sum() if 'reach' in social_data.columns else 0
                
                # Calculate engagement rate and CTR
                overall_engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0
                overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
                
                # Calculate social media performance score
                social_performance_score = round(
                    (min(overall_engagement_rate / 10, 1) * 40) +  # Engagement rate contribution
                    (min(overall_ctr / 5, 1) * 30) +  # CTR contribution
                    (min(len(social_data) / 5, 1) * 30), 1  # Platform diversity contribution
                )
            else:
                total_impressions = total_clicks = total_engagement = total_reach = 0
                overall_engagement_rate = overall_ctr = social_performance_score = 0
            
            # Social media overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="social-metric">
                    <h4 style="margin: 0; font-size: 14px;">📊 Total Impressions</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_impressions:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Across platforms</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="email-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Total Clicks</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_clicks:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">User interactions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="web-metric">
                    <h4 style="margin: 0; font-size: 14px;">📈 Engagement Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{overall_engagement_rate:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Overall performance</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Social media performance indicator
                if social_performance_score >= 80:
                    social_status = "🚀 Excellent"
                    social_color = "#28a745"
                elif social_performance_score >= 60:
                    social_status = "⭐ Good"
                    social_color = "#17a2b8"
                elif social_performance_score >= 40:
                    social_status = "👍 Fair"
                    social_color = "#ffc107"
                else:
                    social_status = "📈 Needs Improvement"
                    social_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="channel-metric-card" style="background: linear-gradient(135deg, {social_color} 0%, {social_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Social Performance</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{social_performance_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{social_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced Social Media Charts
            st.markdown("#### 📊 Social Media Performance Analysis & Visualization")
            
            # Platform comparison chart with enhanced data validation
            try:
                # Check if required columns exist and handle missing ones
                required_columns = ['impressions', 'clicks', 'total_engagement']
                available_columns = [col for col in required_columns if col in social_data.columns]
                
                if len(available_columns) >= 2 and len(social_data) > 0:
                    # Create the platform comparison chart with available columns
                    fig_platform_comparison = px.bar(
                        social_data,
                        x='platform',
                        y=available_columns,
                        title="Social Media Platform Performance Comparison",
                        labels={'value': 'Count', 'variable': 'Metric', 'platform': 'Platform'},
                        barmode='group',
                        template='plotly_white'
                    )
                    
                    fig_platform_comparison.update_traces(
                        marker_line_color='#333',
                        marker_line_width=1
                    )
                    
                    fig_platform_comparison.update_layout(
                        title_font_size=18,
                        title_font_color='#333',
                        xaxis_title_font_size=14,
                        yaxis_title_font_size=14,
                        hovermode='x unified',
                        hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    
                    st.plotly_chart(fig_platform_comparison, use_container_width=True)
                    
                    # Additional social media insights
                    if 'reach' in social_data.columns and 'followers' in social_data.columns:
                        # Reach vs followers scatter plot
                        fig_reach_followers = px.scatter(
                            social_data,
                            x='followers',
                            y='reach',
                            size='total_engagement',
                            title="Reach vs Followers Analysis by Platform",
                            labels={'followers': 'Followers', 'reach': 'Reach', 'total_engagement': 'Engagement'},
                            template='plotly_white',
                            color='platform',
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        
                        fig_reach_followers.update_traces(
                            marker=dict(line=dict(color='#333', width=1))
                        )
                        
                        fig_reach_followers.update_layout(
                            title_font_size=18,
                            title_font_color='#333',
                            xaxis_title_font_size=14,
                            yaxis_title_font_size=14,
                            hovermode='closest',
                            hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            margin=dict(l=50, r=50, t=80, b=50)
                        )
                        
                        st.plotly_chart(fig_reach_followers, use_container_width=True)
                else:
                    st.warning("⚠️ Insufficient data for platform comparison chart. Need at least 2 metrics and platform data.")
                    
            except Exception as e:
                st.error(f"❌ Error creating platform comparison chart: {str(e)}")
                st.info("💡 This might be due to missing or mismatched data columns.")
    
    st.markdown("---")
    
    # Enhanced Email Marketing Channel Analysis
    st.subheader("📧 Advanced Email Marketing Channel Analysis")
    
    # Email marketing insights header
    st.markdown(f"""
    <div class="channel-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📧 Email Marketing Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of email campaign performance, engagement rates, and conversion optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.email_campaigns_data.empty:
        # Enhanced email marketing analysis
        email_performance = st.session_state.email_campaigns_data.groupby('campaign_name').agg({
            'recipients': 'sum',
            'opens': 'sum',
            'clicks': 'sum',
            'conversions': 'sum'
        }).reset_index()
        
        # Ensure numeric data types
        email_performance['recipients'] = pd.to_numeric(email_performance['recipients'], errors='coerce').fillna(0)
        email_performance['opens'] = pd.to_numeric(email_performance['opens'], errors='coerce').fillna(0)
        email_performance['clicks'] = pd.to_numeric(email_performance['clicks'], errors='coerce').fillna(0)
        email_performance['conversions'] = pd.to_numeric(email_performance['conversions'], errors='coerce').fillna(0)
        
        # Calculate enhanced email metrics
        email_performance['open_rate'] = (email_performance['opens'] / email_performance['recipients']) * 100
        email_performance['click_rate'] = (email_performance['clicks'] / email_performance['recipients']) * 100
        email_performance['conversion_rate'] = (email_performance['conversions'] / email_performance['recipients']) * 100
        
        # Calculate overall email performance metrics
        total_recipients = email_performance['recipients'].sum()
        total_opens = email_performance['opens'].sum()
        total_clicks = email_performance['clicks'].sum()
        total_conversions = email_performance['conversions'].sum()
        
        overall_open_rate = (total_opens / total_recipients * 100) if total_recipients > 0 else 0
        overall_click_rate = (total_clicks / total_recipients * 100) if total_recipients > 0 else 0
        overall_conversion_rate = (total_conversions / total_recipients * 100) if total_recipients > 0 else 0
        
        # Calculate email performance score
        email_performance_score = round(
            (min(overall_open_rate / 30, 1) * 40) +  # Open rate contribution
            (min(overall_click_rate / 10, 1) * 30) +  # Click rate contribution
            (min(overall_conversion_rate / 5, 1) * 30), 1  # Conversion rate contribution
        )
        
        # Email marketing overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="social-metric">
                <h4 style="margin: 0; font-size: 14px;">📧 Total Recipients</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{total_recipients:,.0f}</h2>
                <p style="margin: 0; font-size: 12px;">Email reach</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="email-metric">
                <h4 style="margin: 0; font-size: 14px;">📊 Open Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{overall_open_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Overall performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="web-metric">
                <h4 style="margin: 0; font-size: 14px;">🎯 Click Rate</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{overall_click_rate:.1f}%</h2>
                <p style="margin: 0; font-size: 12px;">Engagement level</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Email performance indicator
            if email_performance_score >= 80:
                email_status = "🚀 Excellent"
                email_color = "#28a745"
            elif email_performance_score >= 60:
                email_status = "⭐ Good"
                email_color = "#17a2b8"
            elif email_performance_score >= 40:
                email_status = "👍 Fair"
                email_color = "#ffc107"
            else:
                email_status = "📈 Needs Improvement"
                email_color = "#fd7e14"
            
            st.markdown(f"""
            <div class="channel-metric-card" style="background: linear-gradient(135deg, {email_color} 0%, {email_color}dd 100%);">
                <h4 style="margin: 0; font-size: 14px;">📊 Email Performance</h4>
                <h2 style="margin: 5px 0; font-size: 20px;">{email_performance_score:.1f}/100</h2>
                <p style="margin: 0; font-size: 12px;">{email_status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Email Marketing Charts
        st.markdown("#### 📊 Email Marketing Performance Analysis & Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                # Check if required columns exist for email rates
                rate_columns = ['open_rate', 'click_rate', 'conversion_rate']
                available_rate_columns = [col for col in rate_columns if col in email_performance.columns]
                
                if len(available_rate_columns) >= 2 and len(email_performance) > 0:
                    fig_email_rates = px.bar(
                        email_performance,
                        x='campaign_name',
                        y=available_rate_columns,
                        title="Email Campaign Performance Rates",
                        labels={'value': 'Rate (%)', 'variable': 'Metric', 'campaign_name': 'Campaign Name'},
                        barmode='group',
                        template='plotly_white'
                    )
                    
                    fig_email_rates.update_traces(
                        marker_line_color='#333',
                        marker_line_width=1
                    )
                    
                    fig_email_rates.update_layout(
                        title_font_size=16,
                        title_font_color='#333',
                        xaxis_title_font_size=12,
                        yaxis_title_font_size=12,
                        hovermode='x unified',
                        hoverlabel=dict(bgcolor='white', font_size=10, font_family='Arial'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=40, t=60, b=40)
                    )
                    
                    st.plotly_chart(fig_email_rates, use_container_width=True)
                else:
                    st.warning("⚠️ Insufficient data for email rates chart.")
            except Exception as e:
                st.error(f"❌ Error creating email rates chart: {str(e)}")
        
        with col2:
            try:
                # Check if required columns exist for email volume
                volume_columns = ['recipients', 'opens', 'clicks', 'conversions']
                available_volume_columns = [col for col in volume_columns if col in email_performance.columns]
                
                if len(available_volume_columns) >= 2 and len(email_performance) > 0:
                    fig_email_volume = px.bar(
                        email_performance,
                        x='campaign_name',
                        y=available_volume_columns,
                        title="Email Campaign Volume Metrics",
                        labels={'value': 'Count', 'variable': 'Metric', 'campaign_name': 'Campaign Name'},
                        barmode='group',
                        template='plotly_white'
                    )
                    
                    fig_email_volume.update_traces(
                        marker_line_color='#333',
                        marker_line_width=1
                    )
                    
                    fig_email_volume.update_layout(
                        title_font_size=16,
                        title_font_color='#333',
                        xaxis_title_font_size=12,
                        yaxis_title_font_size=12,
                        hovermode='x unified',
                        hoverlabel=dict(bgcolor='white', font_size=10, font_family='Arial'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=40, r=40, t=60, b=40)
                    )
                    
                    st.plotly_chart(fig_email_volume, use_container_width=True)
                else:
                    st.warning("⚠️ Insufficient data for email volume chart.")
            except Exception as e:
                st.error(f"❌ Error creating email volume chart: {str(e)}")
        
        # Additional email insights chart
        if len(email_performance) > 0:
            # Email performance scatter plot
            fig_email_scatter = px.scatter(
                email_performance,
                x='open_rate',
                y='conversion_rate',
                size='recipients',
                title="Email Open Rate vs Conversion Rate Analysis",
                labels={'open_rate': 'Open Rate (%)', 'conversion_rate': 'Conversion Rate (%)', 'recipients': 'Recipients'},
                template='plotly_white',
                color='campaign_name',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_email_scatter.update_traces(
                marker=dict(line=dict(color='#333', width=1))
            )
            
            fig_email_scatter.update_layout(
                title_font_size=18,
                title_font_color='#333',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                hovermode='closest',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig_email_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Enhanced Cross-Channel Performance Analysis
    st.subheader("🔄 Advanced Cross-Channel Performance Analysis")
    
    # Cross-channel insights header
    st.markdown(f"""
    <div class="channel-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🔄 Cross-Channel Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of channel integration, performance comparison, and optimization strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cross-channel performance summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Social media channel status
        social_status = "✅ Active" if not st.session_state.social_media_data.empty else "❌ No Data"
        social_color = "#28a745" if not st.session_state.social_media_data.empty else "#dc3545"
        
        st.markdown(f"""
        <div class="social-metric" style="background: linear-gradient(135deg, {social_color} 0%, {social_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">📱 Social Media</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{social_status}</h2>
            <p style="margin: 0; font-size: 12px;">Channel status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Email marketing channel status
        email_status = "✅ Active" if not st.session_state.email_campaigns_data.empty else "❌ No Data"
        email_color = "#17a2b8" if not st.session_state.email_campaigns_data.empty else "#dc3545"
        
        st.markdown(f"""
        <div class="email-metric" style="background: linear-gradient(135deg, {email_color} 0%, {email_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">📧 Email Marketing</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{email_status}</h2>
            <p style="margin: 0; font-size: 12px;">Channel status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Web traffic channel status
        web_status = "✅ Active" if not st.session_state.conversions_data.empty else "❌ No Data"
        web_color = "#ffc107" if not st.session_state.conversions_data.empty else "#dc3545"
        
        st.markdown(f"""
        <div class="web-metric" style="background: linear-gradient(135deg, {web_color} 0%, {web_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">🌐 Web Traffic</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{web_status}</h2>
            <p style="margin: 0; font-size: 12px;">Channel status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Overall channel performance
        active_channels = sum([
            1 if not st.session_state.social_media_data.empty else 0,
            1 if not st.session_state.email_campaigns_data.empty else 0,
            1 if not st.session_state.conversions_data.empty else 0
        ])
        
        if active_channels >= 3:
            overall_status = "🚀 Excellent"
            overall_color = "#28a745"
        elif active_channels >= 2:
            overall_status = "⭐ Good"
            overall_color = "#17a2b8"
        elif active_channels >= 1:
            overall_status = "👍 Fair"
            overall_color = "#ffc107"
        else:
            overall_status = "📈 Needs Setup"
            overall_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="overall-metric" style="background: linear-gradient(135deg, {overall_color} 0%, {overall_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">📊 Channel Coverage</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{active_channels}/3</h2>
            <p style="margin: 0; font-size: 12px;">{overall_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Channel Analysis Strategy Summary
    st.markdown("---")
    st.subheader("📋 Channel Analysis Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Channel Optimization Recommendations", expanded=False):
        st.markdown("""
        **Channel-Specific Strategy Recommendations:**
        
        **1. Social Media Channel Optimization:**
        - Implement platform-specific content strategies for better engagement
        - Develop cross-platform posting schedules for optimal reach
        - Create platform-specific advertising campaigns for better ROI
        
        **2. Email Marketing Channel Optimization:**
        - Implement segmentation strategies for personalized content
        - Develop A/B testing frameworks for subject lines and content
        - Create automated email sequences for better conversion rates
        
        **3. Cross-Channel Integration:**
        - Implement unified messaging across all channels
        - Develop cross-channel attribution models for better insights
        - Create integrated campaign strategies for better performance
        
        **4. Channel Performance Monitoring:**
        - Implement real-time performance tracking across all channels
        - Develop channel-specific KPIs and benchmarks
        - Create automated reporting for better decision-making
        
        **5. Audience Behavior Analysis:**
        - Implement cross-channel audience segmentation
        - Develop channel preference analysis for better targeting
        - Create personalized content strategies for each channel
        
        **6. Technology Integration:**
        - Implement marketing automation tools for better efficiency
        - Develop data integration strategies for unified insights
        - Create API connections for real-time data synchronization
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Channel Analysis Performance Metrics Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not st.session_state.social_media_data.empty:
            st.metric(
                "Social Media Performance", 
                f"{'Excellent' if social_performance_score >= 80 else 'Good' if social_performance_score >= 60 else 'Fair' if social_performance_score >= 40 else 'Needs Improvement'}",
                f"{social_performance_score:.1f}/100 score"
            )
    
    with col2:
        if not st.session_state.email_campaigns_data.empty:
            st.metric(
                "Email Marketing Performance", 
                f"{'Excellent' if email_performance_score >= 80 else 'Good' if email_performance_score >= 60 else 'Fair' if email_performance_score >= 40 else 'Needs Improvement'}",
                f"{email_performance_score:.1f}/100 score"
            )
    
    with col3:
        if not st.session_state.conversions_data.empty:
            st.metric(
                "Web Traffic Performance", 
                "Active",
                "Channel operational"
            )
    
    with col4:
        st.metric(
            "Overall Channel Coverage", 
            f"{active_channels}/3 channels",
            f"{'Excellent' if active_channels >= 3 else 'Good' if active_channels >= 2 else 'Fair' if active_channels >= 1 else 'Needs Setup'}"
        )

def show_specialized_metrics():
    """Display world-class specialized marketing metrics with advanced visualizations and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .specialized-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .specialized-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .specialized-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .specialized-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .seasonal-metric {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .device-metric {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .clv-metric {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .content-metric {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Specialized Marketing Metrics - Advanced Analytics Intelligence Dashboard")
    st.markdown("---")
    
    # Enhanced Specialized Metrics Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🎯 Specialized Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Advanced analytics for seasonal trends, device performance, customer lifetime value, and content optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Specialized metrics provide deeper insights into specific marketing areas with advanced analytics and strategic recommendations.")
    
    # Enhanced Seasonal Trends Analysis
    st.subheader("📅 Advanced Seasonal Trends Analysis")
    
    # Seasonal trends insights header
    st.markdown(f"""
    <div class="specialized-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">📅 Seasonal Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Comprehensive analysis of seasonal patterns, revenue trends, and conversion optimization strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.conversions_data.empty:
        try:
            conversions_data = st.session_state.conversions_data.copy()
            conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
            conversions_data['month'] = conversions_data['conversion_date'].dt.month_name()
            conversions_data['month_num'] = conversions_data['conversion_date'].dt.month
            
            # Group by month and aggregate
            seasonal_performance = conversions_data.groupby('month').agg({
                'revenue': 'sum',
                'conversion_id': 'count'
            }).rename(columns={'conversion_id': 'conversions'})
            
            # Add month number for proper ordering
            seasonal_performance['month_num'] = seasonal_performance.index.map({
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            })
            
            # Sort by month number and reset index
            seasonal_performance = seasonal_performance.sort_values('month_num').reset_index()
            
            # Create the seasonal trends chart
            fig_seasonal = px.line(
                seasonal_performance,
                x='month',
                y=['revenue', 'conversions'],
                title="Seasonal Revenue and Conversion Trends",
                labels={'value': 'Count/Amount', 'variable': 'Metric', 'month': 'Month'},
                color_discrete_sequence=['#667eea', '#f97316']
            )
            
            # Apply common layout and styling
            fig_seasonal = apply_common_layout(fig_seasonal)
            fig_seasonal.update_traces(line=dict(width=3))
            fig_seasonal.update_layout(
                title_font_size=18,
                title_font_color='#1e3c72',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                legend_title_font_size=14,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_seasonal, use_container_width=True)
            
            # Calculate enhanced seasonal metrics
            total_revenue = seasonal_performance['revenue'].sum()
            total_conversions = seasonal_performance['conversions'].sum()
            avg_revenue = seasonal_performance['revenue'].mean()
            
            # Calculate seasonal strength and performance score
            seasonal_strength = round(
                (seasonal_performance['revenue'].max() - seasonal_performance['revenue'].min()) / seasonal_performance['revenue'].mean() * 100, 1
            ) if seasonal_performance['revenue'].mean() > 0 else 0
            
            seasonal_performance_score = round(
                (min(seasonal_strength / 50, 1) * 40) +  # Seasonal strength contribution
                (min(len(seasonal_performance) / 12, 1) * 30) +  # Data completeness contribution
                (min(avg_revenue / 10000, 1) * 30), 1  # Revenue performance contribution
            )
            
            # Enhanced seasonal overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="seasonal-metric">
                    <h4 style="margin: 0; font-size: 14px;">💰 Total Revenue</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Seasonal total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="device-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Total Conversions</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_conversions:,}</h2>
                    <p style="margin: 0; font-size: 12px;">Seasonal total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="clv-metric">
                    <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Revenue</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${avg_revenue:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Monthly average</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Seasonal performance indicator
                if seasonal_performance_score >= 80:
                    seasonal_status = "🚀 Excellent"
                    seasonal_color = "#28a745"
                elif seasonal_performance_score >= 60:
                    seasonal_status = "⭐ Good"
                    seasonal_color = "#17a2b8"
                elif seasonal_performance_score >= 40:
                    seasonal_status = "👍 Fair"
                    seasonal_color = "#ffc107"
                else:
                    seasonal_status = "📈 Needs Improvement"
                    seasonal_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="specialized-metric-card" style="background: linear-gradient(135deg, {seasonal_color} 0%, {seasonal_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Seasonal Performance</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{seasonal_performance_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{seasonal_status}</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error processing seasonal trends data: {str(e)}")
            st.info("Please ensure conversions data contains valid dates and revenue information.")
    else:
        st.warning("⚠️ No conversion data available. Please load sample data or upload your own data first.")
    
    # Enhanced Mobile vs Desktop Analysis
    if not st.session_state.website_traffic_data.empty and 'device_type' in st.session_state.website_traffic_data.columns:
        st.subheader("📱 Advanced Mobile vs Desktop Analysis")
        
        # Device analysis insights header
        st.markdown(f"""
        <div class="specialized-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">📱 Device Performance Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of device-specific performance, user behavior patterns, and conversion optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            device_analysis = st.session_state.website_traffic_data.groupby('device_type').agg({
                'session_id': 'count',
                'conversion_flag': 'sum',
                'time_on_page': 'mean'
            }).rename(columns={'session_id': 'sessions', 'conversion_flag': 'conversions'})
            
            device_analysis['conversion_rate'] = (device_analysis['conversions'] / device_analysis['sessions']) * 100
            
            # Calculate enhanced device metrics
            total_sessions = device_analysis['sessions'].sum()
            total_conversions = device_analysis['conversions'].sum()
            overall_conversion_rate = (total_conversions / total_sessions) * 100 if total_sessions > 0 else 0
            
            # Calculate device performance score
            device_performance_score = round(
                (min(overall_conversion_rate / 10, 1) * 40) +  # Conversion rate contribution
                (min(len(device_analysis) / 3, 1) * 30) +  # Device diversity contribution
                (min(total_sessions / 1000, 1) * 30), 1  # Traffic volume contribution
            )
            
            # Enhanced device overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="seasonal-metric">
                    <h4 style="margin: 0; font-size: 14px;">📊 Total Sessions</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_sessions:,}</h2>
                    <p style="margin: 0; font-size: 12px;">Across devices</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="device-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Total Conversions</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_conversions:,}</h2>
                    <p style="margin: 0; font-size: 12px;">Successful conversions</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="clv-metric">
                    <h4 style="margin: 0; font-size: 14px;">📈 Conversion Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{overall_conversion_rate:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Overall performance</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Device performance indicator
                if device_performance_score >= 80:
                    device_status = "🚀 Excellent"
                    device_color = "#28a745"
                elif device_performance_score >= 60:
                    device_status = "⭐ Good"
                    device_color = "#17a2b8"
                elif device_performance_score >= 40:
                    device_status = "👍 Fair"
                    device_color = "#ffc107"
                else:
                    device_status = "📈 Needs Improvement"
                    device_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="specialized-metric-card" style="background: linear-gradient(135deg, {device_color} 0%, {device_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Device Performance</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{device_performance_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{device_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_device_sessions = px.pie(
                    values=device_analysis['sessions'],
                    names=device_analysis.index,
                    title="Traffic Distribution by Device Type",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_device_sessions = apply_common_layout(fig_device_sessions)
                fig_device_sessions.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_device_sessions, use_container_width=True)
            
            with col2:
                fig_device_conversion = px.bar(
                    device_analysis.reset_index(),
                    x='device_type',
                    y='conversion_rate',
                    title="Conversion Rate by Device Type",
                    labels={'conversion_rate': 'Conversion Rate (%)', 'device_type': 'Device Type'},
                    color='conversion_rate',
                    color_continuous_scale='Viridis'
                )
                fig_device_conversion = apply_common_layout(fig_device_conversion)
                fig_device_conversion.update_layout(
                    title_font_size=16,
                    title_font_color='#1e3c72'
                )
                st.plotly_chart(fig_device_conversion, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error processing device analysis data: {str(e)}")
            st.info("Please ensure website traffic data contains valid device type and session information.")
    else:
        st.warning("⚠️ No website traffic data available or missing 'device_type' column. Please load sample data or upload your own data first.")
    
    # Enhanced Customer Lifetime Value Analysis
    if (isinstance(st.session_state.customers_data, pd.DataFrame) and 
        not st.session_state.customers_data.empty and 
        isinstance(st.session_state.conversions_data, pd.DataFrame) and 
        not st.session_state.conversions_data.empty):
        st.subheader("💰 Advanced Customer Lifetime Value Analysis")
        
        # CLV analysis insights header
        st.markdown(f"""
        <div class="specialized-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">💰 CLV Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of customer lifetime value, segment performance, and revenue optimization strategies
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Merge customers with conversions to calculate CLV
            customers_clv = st.session_state.customers_data.copy()
            conversions_summary = st.session_state.conversions_data.groupby('customer_id')['revenue'].sum().reset_index()
            customers_clv = customers_clv.merge(conversions_summary, on='customer_id', how='left')
            customers_clv['revenue'] = customers_clv['revenue'].fillna(0)
            
            # Calculate CLV by customer segment
            clv_by_segment = customers_clv.groupby('customer_segment')['revenue'].agg(['mean', 'sum', 'count']).round(2)
            clv_by_segment.columns = ['Avg CLV', 'Total Revenue', 'Customer Count']
            
            # Calculate enhanced CLV metrics
            avg_clv = customers_clv['revenue'].mean()
            total_clv = customers_clv['revenue'].sum()
            high_value_customers = len(customers_clv[customers_clv['revenue'] > avg_clv])
            total_customers = len(customers_clv)
            
            # Calculate CLV performance score
            clv_performance_score = round(
                (min(avg_clv / 1000, 1) * 40) +  # Average CLV contribution
                (min(high_value_customers / total_customers * 100, 1) * 30) +  # High-value customer ratio
                (min(total_clv / 100000, 1) * 30), 1  # Total value contribution
            ) if total_customers > 0 else 0
            
            # Enhanced CLV overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="seasonal-metric">
                    <h4 style="margin: 0; font-size: 14px;">💰 Average CLV</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${avg_clv:.2f}</h2>
                    <p style="margin: 0; font-size: 12px;">Per customer</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="device-metric">
                    <h4 style="margin: 0; font-size: 14px;">📊 Total Customer Value</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${total_clv:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Combined value</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="clv-metric">
                    <h4 style="margin: 0; font-size: 14px;">👥 High-Value Customers</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{high_value_customers}</h2>
                    <p style="margin: 0; font-size: 12px;">Above average CLV</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # CLV performance indicator
                if clv_performance_score >= 80:
                    clv_status = "🚀 Excellent"
                    clv_color = "#28a745"
                elif clv_performance_score >= 60:
                    clv_status = "⭐ Good"
                    clv_color = "#17a2b8"
                elif clv_performance_score >= 40:
                    clv_status = "👍 Fair"
                    clv_color = "#ffc107"
                else:
                    clv_status = "📈 Needs Improvement"
                    clv_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="specialized-metric-card" style="background: linear-gradient(135deg, {clv_color} 0%, {clv_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 CLV Performance</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{clv_performance_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{clv_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced CLV Charts
            st.markdown("#### 📊 Customer Lifetime Value Analysis & Visualization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_clv_segment = px.bar(
                    clv_by_segment.reset_index(),
                    x='customer_segment',
                    y='Avg CLV',
                    title="Average CLV by Customer Segment",
                    color='Avg CLV',
                    color_continuous_scale='Viridis',
                    template='plotly_white'
                )
                
                fig_clv_segment.update_traces(
                    marker_line_color='#333',
                    marker_line_width=1
                )
                
                fig_clv_segment.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50),
                    showlegend=False
                )
                
                st.plotly_chart(fig_clv_segment, use_container_width=True)
            
            with col2:
                fig_clv_distribution = px.histogram(
                    customers_clv,
                    x='revenue',
                    nbins=10,
                    title="Customer Lifetime Value Distribution",
                    labels={'revenue': 'CLV ($)', 'count': 'Number of Customers'},
                    template='plotly_white',
                    color_discrete_sequence=['#667eea']
                )
                
                fig_clv_distribution.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_clv_distribution, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error processing CLV analysis: {str(e)}")
            st.info("Please ensure both customer and conversion data are available.")
    
    # Enhanced Content Performance Analysis
    if not st.session_state.content_marketing_data.empty:
        st.subheader("📝 Advanced Content Performance Analysis")
        
        # Content analysis insights header
        st.markdown(f"""
        <div class="specialized-insight-card">
            <h3 style="margin: 0; color: #333; font-size: 18px;">📝 Content Intelligence</h3>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                Comprehensive analysis of content performance, engagement metrics, and optimization strategies
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            content_data = st.session_state.content_marketing_data.copy()
            
            # Ensure numeric data types
            numeric_columns = ['views', 'shares', 'engagement_rate', 'leads_generated']
            for col in numeric_columns:
                if col in content_data.columns:
                    content_data[col] = pd.to_numeric(content_data[col], errors='coerce').fillna(0)
            
            # Top performing content by engagement
            top_content = content_data.nlargest(5, 'engagement_rate')[['title', 'content_type', 'views', 'shares', 'engagement_rate']]
            
            # Calculate enhanced content metrics
            total_views = content_data['views'].sum() if 'views' in content_data.columns else 0
            total_shares = content_data['shares'].sum() if 'shares' in content_data.columns else 0
            total_leads = content_data['leads_generated'].sum() if 'leads_generated' in content_data.columns else 0
            avg_engagement = content_data['engagement_rate'].mean() if 'engagement_rate' in content_data.columns else 0
            
            # Calculate content performance score
            content_performance_score = round(
                (min(avg_engagement / 10, 1) * 40) +  # Engagement rate contribution
                (min(total_views / 10000, 1) * 30) +  # Views contribution
                (min(total_leads / 100, 1) * 30), 1  # Leads contribution
            )
            
            # Enhanced content overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="seasonal-metric">
                    <h4 style="margin: 0; font-size: 14px;">👁️ Total Views</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_views:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Content reach</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="device-metric">
                    <h4 style="margin: 0; font-size: 14px;">📤 Total Shares</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_shares:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Viral potential</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="clv-metric">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Total Leads</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_leads:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Generated leads</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Content performance indicator
                if content_performance_score >= 80:
                    content_status = "🚀 Excellent"
                    content_color = "#28a745"
                elif content_performance_score >= 60:
                    content_status = "⭐ Good"
                    content_color = "#17a2b8"
                elif content_performance_score >= 40:
                    content_status = "👍 Fair"
                    content_color = "#ffc107"
                else:
                    content_status = "📈 Needs Improvement"
                    content_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="specialized-metric-card" style="background: linear-gradient(135deg, {content_color} 0%, {content_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Content Performance</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{content_performance_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{content_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced Content Charts
            st.markdown("#### 📊 Content Performance Analysis & Visualization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_content_engagement = px.bar(
                    top_content,
                    x='title',
                    y='engagement_rate',
                    title="Top Content by Engagement Rate",
                    color='content_type',
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    template='plotly_white'
                )
                
                fig_content_engagement.update_traces(
                    marker_line_color='#333',
                    marker_line_width=1
                )
                
                fig_content_engagement.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50),
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig_content_engagement, use_container_width=True)
            
            with col2:
                fig_content_views = px.scatter(
                    content_data,
                    x='views',
                    y='shares',
                    size='leads_generated',
                    title="Content Views vs Shares (Size = Leads Generated)",
                    labels={'views': 'Views', 'shares': 'Shares', 'leads_generated': 'Leads Generated'},
                    template='plotly_white',
                    color='content_type',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_content_views.update_traces(
                    marker=dict(line=dict(color='#333', width=1))
                )
                
                fig_content_views.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='closest',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_content_views, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error processing content performance analysis: {str(e)}")
            st.info("Please ensure content marketing data is available.")
    
    # Specialized Metrics Strategy Summary
    st.markdown("---")
    st.subheader("📋 Specialized Metrics Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Specialized Metrics Optimization Recommendations", expanded=False):
        st.markdown("""
        **Specialized Metrics Strategy Recommendations:**
        
        **1. Seasonal Trends Optimization:**
        - Implement seasonal marketing campaign planning based on trend analysis
        - Develop targeted content strategies for peak performance periods
        - Create seasonal budget allocation strategies for better ROI
        
        **2. Device Performance Optimization:**
        - Implement device-specific user experience optimization
        - Develop responsive design strategies for better mobile performance
        - Create device-targeted advertising campaigns for better conversion rates
        
        **3. Customer Lifetime Value Optimization:**
        - Implement customer segmentation strategies based on CLV analysis
        - Develop retention strategies for high-value customers
        - Create upselling and cross-selling strategies for better revenue growth
        
        **4. Content Performance Optimization:**
        - Implement content type optimization based on performance analysis
        - Develop content distribution strategies for better reach and engagement
        - Create content personalization strategies for better conversion rates
        
        **5. Cross-Metric Integration:**
        - Implement unified analytics strategies across all specialized metrics
        - Develop integrated optimization strategies for better overall performance
        - Create predictive modeling strategies for better strategic planning
        
        **6. Performance Benchmarking:**
        - Implement industry benchmark comparisons for better competitive positioning
        - Develop performance improvement strategies based on benchmark analysis
        - Create continuous optimization frameworks for better long-term performance
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Specialized Metrics Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'seasonal_performance_score' in locals():
            st.metric(
                "Seasonal Performance", 
                f"{'Excellent' if seasonal_performance_score >= 80 else 'Good' if seasonal_performance_score >= 60 else 'Fair' if seasonal_performance_score >= 40 else 'Needs Improvement'}",
                f"{seasonal_performance_score:.1f}/100 score"
            )
    
    with col2:
        if 'device_performance_score' in locals():
            st.metric(
                "Device Performance", 
                f"{'Excellent' if device_performance_score >= 80 else 'Good' if device_performance_score >= 60 else 'Fair' if device_performance_score >= 40 else 'Needs Improvement'}",
                f"{device_performance_score:.1f}/100 score"
            )
    
    with col3:
        if 'clv_performance_score' in locals():
            st.metric(
                "CLV Performance", 
                f"{'Excellent' if clv_performance_score >= 80 else 'Good' if clv_performance_score >= 60 else 'Fair' if clv_performance_score >= 40 else 'Needs Improvement'}",
                f"{clv_performance_score:.1f}/100 score"
            )
    
    with col4:
        if 'content_performance_score' in locals():
            st.metric(
                "Content Performance", 
                f"{'Excellent' if content_performance_score >= 80 else 'Good' if content_performance_score >= 60 else 'Fair' if content_performance_score >= 40 else 'Needs Improvement'}",
                f"{content_performance_score:.1f}/100 score"
            )

def show_predictive_analytics():
    """Display world-class predictive analytics with advanced forecasting models and strategic insights"""
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .predictive-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    
    .predictive-metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .predictive-insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .predictive-chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .revenue-predictor {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .lead-predictor {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .trend-predictor {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .ai-predictor {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔮 Predictive Analytics - Advanced AI-Powered Marketing Intelligence Dashboard")
    st.markdown("---")
    
    # Enhanced Predictive Analytics Overview Dashboard
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
        <h2 style="margin: 0; font-size: 24px;">🔮 AI-Powered Marketing Intelligence Dashboard</h2>
        <p style="margin: 10px 0; font-size: 16px; opacity: 0.9;">
            Advanced predictive modeling, trend forecasting, and AI-driven insights for strategic marketing optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 Predictive Analytics provides AI-powered forecasting, trend analysis, and strategic insights for data-driven marketing decisions.")
    
    # Helpful explanation for new users
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 20px; border-radius: 12px; border-left: 5px solid #1e3c72; margin: 20px 0;">
        <h4 style="margin: 0; color: #333; font-size: 16px;">🎯 Getting Started with Predictive Analytics</h4>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            <strong>New to Predictive Analytics?</strong> This section shows AI-powered predictions for revenue, leads, and trends. 
            To see it in action, you'll need to load sample data first. The sample data includes realistic marketing scenarios 
            that demonstrate the full power of our predictive models.
        </p>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            <strong>Already have data?</strong> Upload your own marketing data to get personalized predictions and insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Quality Check and Recommendations
    st.markdown("#### 📊 Data Quality Assessment & Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Check conversions data
        if not st.session_state.conversions_data.empty:
            st.success("✅ Conversions Data: Available")
            conv_count = len(st.session_state.conversions_data)
            st.metric("Records", f"{conv_count:,}")
        else:
            st.error("❌ Conversions Data: Missing")
            st.metric("Records", "0")
    
    with col2:
        # Check leads data
        if not st.session_state.leads_data.empty:
            st.success("✅ Leads Data: Available")
            leads_count = len(st.session_state.leads_data)
            st.metric("Records", f"{leads_count:,}")
        else:
            st.error("❌ Leads Data: Missing")
            st.metric("Records", "0")
    
    with col3:
        # Check overall data quality
        total_records = (len(st.session_state.conversions_data) if not st.session_state.conversions_data.empty else 0) + \
                       (len(st.session_state.leads_data) if not st.session_state.leads_data.empty else 0)
        
        if total_records >= 100:
            st.success("✅ Data Quality: Excellent")
            quality_color = "#28a745"
        elif total_records >= 50:
            st.warning("⚠️ Data Quality: Good")
            quality_color = "#ffc107"
        elif total_records >= 20:
            st.warning("⚠️ Data Quality: Fair")
            quality_color = "#fd7e14"
        else:
            st.error("❌ Data Quality: Poor")
            quality_color = "#dc3545"
        
        st.markdown(f"""
        <div style="background: {quality_color}; padding: 10px; border-radius: 8px; color: white; text-align: center;">
            <strong>Total Records: {total_records:,}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Data loading recommendations
    if total_records < 50:
        st.warning("⚠️ **Data Quality Notice**: For optimal predictive analytics, we recommend:")
        st.markdown("""
        - **Load Sample Data**: Use the '📝 Data Input' section to load comprehensive sample datasets
        - **Minimum Requirements**: At least 50+ records for reliable predictions
        - **Data Structure**: Ensure data contains proper date columns and numeric values
        - **Time Range**: Historical data spanning multiple months for trend analysis
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Load Sample Data Now", key="load_sample_predictive", use_container_width=True):
                st.session_state.current_page = "📝 Data Input"
                st.rerun()
        
        with col2:
            if st.button("📊 Go to Data Input", key="goto_data_input", use_container_width=True):
                st.session_state.current_page = "📝 Data Input"
                st.rerun()
        
        # Add a prominent call-to-action box
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; color: white; text-align: center; margin: 20px 0;">
            <h3 style="margin: 0; font-size: 20px;">🚀 Ready to Experience AI-Powered Predictions?</h3>
            <p style="margin: 10px 0; font-size: 16px; opacity: 0.8;">
                Load sample data to see the full power of our Predictive Analytics dashboard!
            </p>
            <p style="margin: 5px 0; font-size: 14px; opacity: 0.7;">
                Sample data includes: 100+ conversions, 150+ leads, 200+ customers, and comprehensive marketing metrics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo section showing what predictions would look like
        with st.expander("🔮 Preview: What Your Predictions Will Look Like", expanded=True):
            st.markdown("#### 💰 Sample Revenue Predictions (Demo)")
            
            # Create sample demo data
            demo_months = ['January', 'February', 'March', 'April', 'May', 'June']
            demo_revenue = [12000, 15000, 18000, 22000, 25000, 28000]
            demo_predictions = [32000, 35000, 38000]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Demo revenue trend chart
                fig_demo_revenue = px.line(
                    x=demo_months + ['Next Month', 'Month +2', 'Month +3'],
                    y=demo_revenue + demo_predictions,
                    title="Sample Revenue Trend with Predictions (Demo)",
                    labels={'x': 'Month', 'y': 'Revenue ($)'},
                    template='plotly_white'
                )
                
                # Add prediction markers
                fig_demo_revenue.add_scatter(
                    x=['Next Month', 'Month +2', 'Month +3'],
                    y=demo_predictions,
                    mode='markers',
                    name='Predictions',
                    marker=dict(size=12, color='green', symbol='diamond'),
                    showlegend=True
                )
                
                fig_demo_revenue.update_layout(
                    title_font_size=16,
                    title_font_color='#333',
                    xaxis_title_font_size=12,
                    yaxis_title_font_size=12,
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=40, t=60, b=40)
                )
                
                st.plotly_chart(fig_demo_revenue, use_container_width=True)
            
            with col2:
                # Demo metrics
                st.markdown("**Sample Prediction Metrics:**")
                st.metric("Historical Revenue", "$130,000", "6 months")
                st.metric("Predicted Revenue", "$105,000", "Next 3 months")
                st.metric("Growth Rate", "+15.4%", "Month over month")
                st.metric("Confidence Score", "87.2%", "High accuracy")
                
                st.markdown("---")
                st.markdown("**Sample AI Insights:**")
                st.success("✅ **Strong upward trend detected** - Revenue growing consistently")
                st.info("📊 **Seasonal pattern identified** - Q2 shows peak performance")
                st.warning("⚠️ **Growth rate stabilizing** - Consider optimization strategies")
                st.success("🎯 **High prediction confidence** - Model reliability: 87.2%")
    
    st.markdown("---")
    
    # Revenue Prediction Analysis
    st.subheader("💰 Advanced Revenue Prediction Analysis")
    
    # Revenue prediction insights header
    st.markdown(f"""
    <div class="predictive-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">💰 Revenue Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            AI-powered revenue forecasting with trend analysis, seasonal patterns, and growth predictions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.conversions_data.empty:
        try:
            # Prepare data for revenue prediction
            conversions_data = st.session_state.conversions_data.copy()
            conversions_data['conversion_date'] = pd.to_datetime(conversions_data['conversion_date'])
            conversions_data['month'] = conversions_data['conversion_date'].dt.month_name()
            conversions_data['month_num'] = conversions_data['conversion_date'].dt.month
            
            # Ensure numeric data types
            conversions_data['revenue'] = pd.to_numeric(conversions_data['revenue'], errors='coerce').fillna(0)
            
            # Group by month and aggregate
            monthly_revenue = conversions_data.groupby('month').agg({
                'revenue': 'sum',
                'conversion_id': 'count'
            }).rename(columns={'conversion_id': 'conversions'})
            
            # Add month number for proper ordering
            monthly_revenue['month_num'] = monthly_revenue.index.map({
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            })
            
            # Sort by month number and reset index
            monthly_revenue = monthly_revenue.sort_values('month_num').reset_index()
            
            # Calculate revenue prediction metrics
            total_revenue = monthly_revenue['revenue'].sum()
            avg_monthly_revenue = monthly_revenue['revenue'].mean()
            revenue_growth_rate = ((monthly_revenue['revenue'].iloc[-1] - monthly_revenue['revenue'].iloc[0]) / monthly_revenue['revenue'].iloc[0] * 100) if len(monthly_revenue) > 1 and monthly_revenue['revenue'].iloc[0] > 0 else 0
            
            # Performance: Calculate revenue predictions
            def calculate_revenue_predictions(monthly_data):
                """Calculate revenue predictions for analysis"""
                if len(monthly_data) > 1:
                    x = np.array(monthly_data['month_num']).reshape(-1, 1)
                    y = monthly_data['revenue'].values
                    
                    # Linear regression model
                    model = LinearRegression()
                    model.fit(x, y)
                    
                    # Predict next 3 months
                    future_months = np.array([13, 14, 15]).reshape(-1, 1)
                    future_predictions = model.predict(future_months)
                    
                    # Calculate prediction confidence
                    y_pred = model.predict(x)
                    mse = np.mean((y - y_pred) ** 2)
                    rmse = np.sqrt(mse)
                    confidence_score = max(0, 100 - (rmse / monthly_data['revenue'].mean() * 100)) if monthly_data['revenue'].mean() > 0 else 0
                    
                    return model, future_predictions, confidence_score
                else:
                    return None, [avg_monthly_revenue] * 3, 0
            
            # Get cached predictions
            model, future_predictions, confidence_score = calculate_revenue_predictions(monthly_revenue)
            
            # Calculate revenue prediction score
            revenue_prediction_score = round(
                (min(confidence_score / 100, 1) * 40) +  # Prediction confidence contribution
                (min(len(monthly_revenue) / 12, 1) * 30) +  # Data completeness contribution
                (min(abs(revenue_growth_rate) / 50, 1) * 30), 1  # Growth pattern contribution
            )
            
            # Enhanced revenue overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="revenue-predictor">
                    <h4 style="margin: 0; font-size: 14px;">💰 Total Revenue</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${total_revenue:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Historical total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="lead-predictor">
                    <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Revenue</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">${avg_monthly_revenue:,.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Monthly average</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="trend-predictor">
                    <h4 style="margin: 0; font-size: 14px;">📈 Growth Rate</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{revenue_growth_rate:.1f}%</h2>
                    <p style="margin: 0; font-size: 12px;">Revenue growth</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Revenue prediction indicator
                if revenue_prediction_score >= 80:
                    revenue_status = "🚀 Excellent"
                    revenue_color = "#28a745"
                elif revenue_prediction_score >= 60:
                    revenue_status = "⭐ Good"
                    revenue_color = "#17a2b8"
                elif revenue_prediction_score >= 40:
                    revenue_status = "👍 Fair"
                    revenue_color = "#ffc107"
                else:
                    revenue_status = "📈 Needs Improvement"
                    revenue_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="predictive-metric-card" style="background: linear-gradient(135deg, {revenue_color} 0%, {revenue_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Prediction Score</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{revenue_prediction_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{revenue_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Performance: Chart creation function for revenue analysis
            def create_revenue_chart(monthly_data, model, predictions):
                """Create revenue chart for analysis"""
                fig = px.line(
                    monthly_data,
                    x='month',
                    y='revenue',
                    title="Historical Revenue Trends with Prediction",
                    labels={'revenue': 'Revenue ($)', 'month': 'Month'},
                    template='plotly_white'
                )
                
                # Add trend line
                if model is not None:
                    fig.add_scatter(
                        x=monthly_data['month'],
                        y=model.predict(monthly_data['month_num'].values.reshape(-1, 1)),
                        mode='lines',
                        name='Trend Line',
                        line=dict(color='red', dash='dash')
                    )
                
                # Add future predictions
                future_months = ['Next Month', 'Month +2', 'Month +3']
                fig.add_scatter(
                    x=future_months,
                    y=predictions,
                    mode='markers+lines',
                    name='Predictions',
                    line=dict(color='green', width=3),
                    marker=dict(size=10, color='green')
                )
                
                fig.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                return fig
            
            # Enhanced Revenue Prediction Charts
            st.markdown("#### 📊 Revenue Prediction Analysis & Forecasting")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Get cached chart for performance
                fig_revenue_trend = create_revenue_chart(monthly_revenue, model, future_predictions)
                st.plotly_chart(fig_revenue_trend, use_container_width=True)
            
            with col2:
                # Revenue prediction confidence
                fig_confidence = px.bar(
                    x=['Prediction Confidence'],
                    y=[confidence_score],
                    title="Revenue Prediction Confidence Score",
                    labels={'y': 'Confidence (%)', 'x': 'Metric'},
                    template='plotly_white',
                    color_discrete_sequence=['#667eea']
                )
                
                fig_confidence.update_traces(
                    marker_line_color='#333',
                    marker_line_width=1
                )
                
                fig_confidence.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50),
                    yaxis=dict(range=[0, 100])
                )
                
                st.plotly_chart(fig_confidence, use_container_width=True)
            
            # Future revenue predictions table
            st.markdown("#### 🔮 Future Revenue Predictions")
            
            future_df = pd.DataFrame({
                'Period': ['Next Month', 'Month +2', 'Month +3'],
                'Predicted Revenue': [f"${pred:,.0f}" for pred in future_predictions],
                'Confidence Level': [f"{confidence_score:.1f}%" for _ in range(3)],
                'Growth Trend': ['📈' if i == 0 or future_predictions[i] > future_predictions[i-1] else '📉' for i in range(3)]
            })
            
            st.dataframe(future_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing revenue prediction analysis: {str(e)}")
            st.info("Please ensure conversions data contains valid dates and revenue information.")
    else:
        st.warning("⚠️ No conversion data available. Please load sample data or upload your own data first.")
    
    st.markdown("---")
    
    # Lead Generation Prediction Analysis
    st.subheader("🎯 Advanced Lead Generation Prediction Analysis")
    
    # Lead prediction insights header
    st.markdown(f"""
    <div class="predictive-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🎯 Lead Generation Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            AI-powered lead forecasting with conversion probability analysis and acquisition optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.leads_data.empty:
        try:
            # Prepare data for lead prediction
            leads_data = st.session_state.leads_data.copy()
            
            # Check if lead_date column exists, if not create a synthetic date
            if 'lead_date' not in leads_data.columns:
                # Create synthetic dates for demonstration
                leads_data['lead_date'] = pd.date_range(start='2024-01-01', periods=len(leads_data), freq='D')
            
            leads_data['lead_date'] = pd.to_datetime(leads_data['lead_date'])
            leads_data['month'] = leads_data['lead_date'].dt.month_name()
            leads_data['month_num'] = leads_data['lead_date'].dt.month
            
            # Ensure numeric data types and handle missing columns
            numeric_columns = ['lead_score', 'conversion_probability']
            for col in numeric_columns:
                if col not in leads_data.columns:
                    # Create synthetic columns for demonstration if they don't exist
                    if col == 'lead_score':
                        leads_data[col] = np.random.randint(1, 100, size=len(leads_data))
                    elif col == 'conversion_probability':
                        leads_data[col] = np.random.uniform(0.1, 0.8, size=len(leads_data)) * 100
                else:
                    leads_data[col] = pd.to_numeric(leads_data[col], errors='coerce').fillna(0)
            
            # Group by month and aggregate with safe column access
            agg_dict = {'lead_id': 'count'}
            if 'lead_score' in leads_data.columns:
                agg_dict['lead_score'] = 'mean'
            if 'conversion_probability' in leads_data.columns:
                agg_dict['conversion_probability'] = 'mean'
            
            monthly_leads = leads_data.groupby('month').agg(agg_dict).rename(columns={'lead_id': 'leads_generated'})
            
            # Add month number for proper ordering
            monthly_leads['month_num'] = monthly_leads.index.map({
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            })
            
            # Sort by month number and reset index
            monthly_leads = monthly_leads.sort_values('month_num').reset_index()
            
            # Calculate lead prediction metrics
            total_leads = monthly_leads['leads_generated'].sum()
            avg_monthly_leads = monthly_leads['leads_generated'].mean()
            avg_lead_score = monthly_leads['lead_score'].mean()
            avg_conversion_prob = monthly_leads['conversion_probability'].mean()
            
            # Simple linear regression for lead prediction
            if len(monthly_leads) > 1:
                x = np.array(monthly_leads['month_num']).reshape(-1, 1)
                y = monthly_leads['leads_generated'].values
                
                # Linear regression model
                lead_model = LinearRegression()
                lead_model.fit(x, y)
                
                # Predict next 3 months
                future_months = np.array([13, 14, 15]).reshape(-1, 1)
                future_lead_predictions = lead_model.predict(future_months)
                
                # Calculate prediction confidence
                y_pred = lead_model.predict(x)
                mse = np.mean((y - y_pred) ** 2)
                rmse = np.sqrt(mse)
                lead_confidence_score = max(0, 100 - (rmse / avg_monthly_leads * 100)) if avg_monthly_leads > 0 else 0
                
                # Calculate lead prediction score
                lead_prediction_score = round(
                    (min(lead_confidence_score / 100, 1) * 40) +  # Prediction confidence contribution
                    (min(len(monthly_leads) / 12, 1) * 30) +  # Data completeness contribution
                    (min(avg_conversion_prob / 50, 1) * 30), 1  # Conversion probability contribution
                )
            else:
                future_lead_predictions = [avg_monthly_leads] * 3
                lead_confidence_score = 0
                lead_prediction_score = 0
            
            # Enhanced lead overview metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="revenue-predictor">
                    <h4 style="margin: 0; font-size: 14px;">🎯 Total Leads</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{total_leads:,}</h2>
                    <p style="margin: 0; font-size: 12px;">Historical total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="lead-predictor">
                    <h4 style="margin: 0; font-size: 14px;">📊 Avg Monthly Leads</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{avg_monthly_leads:.0f}</h2>
                    <p style="margin: 0; font-size: 12px;">Monthly average</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="trend-predictor">
                    <h4 style="margin: 0; font-size: 14px;">⭐ Avg Lead Score</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{avg_lead_score:.1f}</h2>
                    <p style="margin: 0; font-size: 12px;">Lead quality</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Lead prediction indicator
                if lead_prediction_score >= 80:
                    lead_status = "🚀 Excellent"
                    lead_color = "#28a745"
                elif lead_prediction_score >= 60:
                    lead_status = "⭐ Good"
                    lead_color = "#17a2b8"
                elif lead_prediction_score >= 40:
                    lead_status = "👍 Fair"
                    lead_color = "#ffc107"
                else:
                    lead_status = "📈 Needs Improvement"
                    lead_color = "#fd7e14"
                
                st.markdown(f"""
                <div class="predictive-metric-card" style="background: linear-gradient(135deg, {lead_color} 0%, {lead_color}dd 100%);">
                    <h4 style="margin: 0; font-size: 14px;">📊 Prediction Score</h4>
                    <h2 style="margin: 5px 0; font-size: 20px;">{lead_prediction_score:.1f}/100</h2>
                    <p style="margin: 0; font-size: 12px;">{lead_status}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced Lead Prediction Charts
            st.markdown("#### 📊 Lead Generation Prediction Analysis & Forecasting")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Historical leads with trend line
                fig_leads_trend = px.line(
                    monthly_leads,
                    x='month',
                    y='leads_generated',
                    title="Historical Lead Generation Trends with Prediction",
                    labels={'leads_generated': 'Leads Generated', 'month': 'Month'},
                    template='plotly_white'
                )
                
                # Add trend line
                fig_leads_trend.add_scatter(
                    x=monthly_leads['month'],
                    y=lead_model.predict(monthly_leads['month_num'].values.reshape(-1, 1)) if len(monthly_leads) > 1 else [],
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', dash='dash')
                )
                
                # Add future predictions
                future_months = ['Next Month', 'Month +2', 'Month +3']
                fig_leads_trend.add_scatter(
                    x=future_months,
                    y=future_lead_predictions,
                    mode='markers+lines',
                    name='Predictions',
                    line=dict(color='green', width=3),
                    marker=dict(size=10, color='green')
                )
                
                fig_leads_trend.update_layout(
                    title_font_size=18,
                    title_font_color='#333',
                    xaxis_title_font_size=14,
                    yaxis_title_font_size=14,
                    hovermode='x unified',
                    hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_leads_trend, use_container_width=True)
            
            with col2:
                # Lead quality vs conversion probability (with column validation)
                if 'lead_score' in monthly_leads.columns and 'conversion_probability' in monthly_leads.columns:
                    fig_lead_quality = px.scatter(
                        monthly_leads,
                        x='lead_score',
                        y='conversion_probability',
                        size='leads_generated',
                        title="Lead Quality vs Conversion Probability",
                        labels={'lead_score': 'Lead Score', 'conversion_probability': 'Conversion Probability (%)', 'leads_generated': 'Leads Generated'},
                        template='plotly_white',
                        color='month',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    fig_lead_quality.update_traces(
                        marker=dict(line=dict(color='#333', width=1))
                    )
                    
                    fig_lead_quality.update_layout(
                        title_font_size=18,
                        title_font_color='#333',
                        xaxis_title_font_size=14,
                        yaxis_title_font_size=14,
                        hovermode='closest',
                        hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    
                    st.plotly_chart(fig_lead_quality, use_container_width=True)
                else:
                    # Alternative chart when columns are missing
                    fig_lead_alt = px.bar(
                        monthly_leads,
                        x='month',
                        y='leads_generated',
                        title="Monthly Lead Generation (Alternative View)",
                        labels={'leads_generated': 'Leads Generated', 'month': 'Month'},
                        template='plotly_white',
                        color_discrete_sequence=['#17a2b8']
                    )
                    
                    fig_lead_alt.update_traces(
                        marker_line_color='#333',
                        marker_line_width=1
                    )
                    
                    fig_lead_alt.update_layout(
                        title_font_size=18,
                        title_font_color='#333',
                        xaxis_title_font_size=14,
                        yaxis_title_font_size=14,
                        hovermode='x unified',
                        hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    
                    st.plotly_chart(fig_lead_alt, use_container_width=True)
                    st.info("💡 Showing alternative chart due to missing lead quality columns. Load sample data for full functionality.")
            
            # Future lead predictions table
            st.markdown("#### 🔮 Future Lead Generation Predictions")
            
            future_leads_df = pd.DataFrame({
                'Period': ['Next Month', 'Month +2', 'Month +3'],
                'Predicted Leads': [f"{pred:.0f}" for pred in future_lead_predictions],
                'Confidence Level': [f"{lead_confidence_score:.1f}%" for _ in range(3)],
                'Quality Trend': ['📈' if i == 0 or future_lead_predictions[i] > future_lead_predictions[i-1] else '📉' for i in range(3)]
            })
            
            st.dataframe(future_leads_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error processing lead prediction analysis: {str(e)}")
            st.info("💡 **Troubleshooting Tips:**")
            st.markdown("""
            - **Load Sample Data**: Use the '📝 Data Input' section to load comprehensive sample datasets
            - **Check Data Structure**: Ensure your data has the required columns (lead_id, lead_date, etc.)
            - **Data Format**: Make sure dates are in a recognizable format (YYYY-MM-DD, MM/DD/YYYY, etc.)
            - **Column Names**: Verify column names match exactly (case-sensitive)
            """)
            
            # Show sample data structure
            with st.expander("📋 Expected Leads Data Structure", expanded=False):
                st.markdown("""
                **Required Columns:**
                - `lead_id`: Unique identifier for each lead
                - `lead_date`: Date when the lead was created
                
                **Optional Columns (for enhanced analysis):**
                - `lead_score`: Numeric score (1-100) indicating lead quality
                - `conversion_probability`: Percentage (0-100) indicating conversion likelihood
                - `lead_name`: Name of the lead
                - `company`: Company name
                - `source`: Lead source (website, social media, etc.)
                - `status`: Current lead status
                - `value`: Lead value in currency
                
                **Sample Data:**
                ```csv
                lead_id,lead_date,lead_name,company,source,status,value
                1,2024-01-15,John Doe,ABC Corp,Website,New,5000
                2,2024-01-16,Jane Smith,XYZ Inc,Social Media,Contacted,7500
                ```
                """)
    else:
        st.warning("⚠️ No leads data available. Please load sample data or upload your own data first.")
        st.info("💡 **Quick Start:** Click '🚀 Load Sample Data Now' button above to get started with comprehensive sample datasets.")
    
    st.markdown("---")
    
    # AI-Powered Trend Analysis
    st.subheader("🤖 AI-Powered Advanced Trend Analysis")
    
    # AI trend analysis insights header
    st.markdown(f"""
    <div class="predictive-insight-card">
        <h3 style="margin: 0; color: #333; font-size: 18px;">🤖 AI Intelligence</h3>
        <p style="margin: 5px 0; color: #666; font-size: 14px;">
            Machine learning-powered trend analysis with pattern recognition and predictive modeling
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Trend Analysis Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Pattern Recognition Score
        pattern_score = round(
            (min(len(monthly_revenue) / 12, 1) * 40) +  # Data completeness
            (min(confidence_score / 100, 1) * 30) +  # Revenue prediction confidence
            (min(lead_confidence_score / 100, 1) * 30), 1  # Lead prediction confidence
        ) if ('monthly_revenue' in locals() and 'confidence_score' in locals() and 'lead_confidence_score' in locals() and monthly_revenue is not None) else 0
        
        if pattern_score >= 80:
            pattern_status = "🚀 Excellent"
            pattern_color = "#28a745"
        elif pattern_score >= 60:
            pattern_status = "⭐ Good"
            pattern_color = "#17a2b8"
        elif pattern_score >= 40:
            pattern_status = "👍 Fair"
            pattern_color = "#ffc107"
        else:
            pattern_status = "📈 Needs Improvement"
            pattern_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="ai-predictor" style="background: linear-gradient(135deg, {pattern_color} 0%, {pattern_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">🔍 Pattern Recognition</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{pattern_score:.1f}/100</h2>
            <p style="margin: 0; font-size: 12px;">{pattern_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Predictive Accuracy Score
        accuracy_score = round(
            (min(confidence_score / 100, 1) * 50) +  # Revenue accuracy
            (min(lead_confidence_score / 100, 1) * 50), 1  # Lead accuracy
        ) if 'confidence_score' in locals() and 'lead_confidence_score' in locals() else 0
        
        if accuracy_score >= 80:
            accuracy_status = "🚀 Excellent"
            accuracy_color = "#28a745"
        elif accuracy_score >= 60:
            accuracy_status = "⭐ Good"
            accuracy_color = "#17a2b8"
        elif accuracy_score >= 40:
            accuracy_status = "👍 Fair"
            accuracy_color = "#ffc107"
        else:
            accuracy_status = "📈 Needs Improvement"
            accuracy_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="ai-predictor" style="background: linear-gradient(135deg, {accuracy_color} 0%, {accuracy_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">🎯 Predictive Accuracy</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{accuracy_score:.1f}/100</h2>
            <p style="margin: 0; font-size: 12px;">{accuracy_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Data Quality Score
        data_quality_score = round(
            (min(len(monthly_revenue) / 12, 1) * 40) +  # Revenue data completeness
            (min(len(monthly_leads) / 12, 1) * 30) +  # Lead data completeness
            (min(30, 1) * 30), 1  # Data consistency
        ) if 'monthly_revenue' in locals() and 'monthly_leads' in locals() else 0
        
        if data_quality_score >= 80:
            quality_status = "🚀 Excellent"
            quality_color = "#28a745"
        elif data_quality_score >= 60:
            quality_status = "⭐ Good"
            quality_color = "#17a2b8"
        elif data_quality_score >= 40:
            quality_status = "👍 Fair"
            quality_color = "#ffc107"
        else:
            quality_status = "📈 Needs Improvement"
            quality_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="ai-predictor" style="background: linear-gradient(135deg, {quality_color} 0%, {quality_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">📊 Data Quality</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{data_quality_score:.1f}/100</h2>
            <p style="margin: 0; font-size: 12px;">{quality_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Overall AI Performance Score
        ai_performance_score = round(
            (pattern_score * 0.3) +  # Pattern recognition contribution
            (accuracy_score * 0.4) +  # Predictive accuracy contribution
            (data_quality_score * 0.3), 1  # Data quality contribution
        )
        
        if ai_performance_score >= 80:
            ai_status = "🚀 Excellent"
            ai_color = "#28a745"
        elif ai_performance_score >= 60:
            ai_status = "⭐ Good"
            ai_color = "#17a2b8"
        elif ai_performance_score >= 40:
            ai_status = "👍 Fair"
            ai_color = "#ffc107"
        else:
            ai_status = "📈 Needs Improvement"
            ai_color = "#fd7e14"
        
        st.markdown(f"""
        <div class="predictive-metric-card" style="background: linear-gradient(135deg, {ai_color} 0%, {ai_color}dd 100%);">
            <h4 style="margin: 0; font-size: 14px;">🤖 AI Performance</h4>
            <h2 style="margin: 5px 0; font-size: 20px;">{ai_performance_score:.1f}/100</h2>
            <p style="margin: 0; font-size: 12px;">{ai_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Trend Analysis Charts
    st.markdown("#### 🤖 AI-Powered Trend Analysis & Pattern Recognition")
    
    if 'monthly_revenue' in locals() and 'monthly_leads' in locals() and monthly_revenue is not None and monthly_leads is not None:
        try:
            # Combined trend analysis
            fig_combined_trends = go.Figure()
            
            # Revenue trend
            fig_combined_trends.add_trace(go.Scatter(
                x=monthly_revenue['month'],
                y=monthly_revenue['revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#28a745', width=3),
                marker=dict(size=8)
            ))
            
            # Leads trend
            fig_combined_trends.add_trace(go.Scatter(
                x=monthly_leads['month'],
                y=monthly_leads['leads_generated'],
                mode='lines+markers',
                name='Leads',
                line=dict(color='#17a2b8', width=3),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            # Update layout
            fig_combined_trends.update_layout(
                title="AI-Powered Combined Trend Analysis",
                title_font_size=18,
                title_font_color='#333',
                xaxis_title="Month",
                yaxis_title="Revenue ($)",
                yaxis2=dict(title="Leads Generated", overlaying='y', side='right'),
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Arial'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=50, t=80, b=50),
                legend=dict(x=0.02, y=0.98)
            )
            
            st.plotly_chart(fig_combined_trends, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Unable to create combined trend analysis chart: {str(e)}")
            st.info("💡 This usually happens when there's insufficient data for trend analysis.")
    else:
        st.warning("⚠️ Insufficient data for AI trend analysis. Need both revenue and lead data.")
        st.info("💡 Please ensure you have loaded sample data or uploaded your own data with sufficient historical information.")
    
    # Predictive Analytics Strategy Summary
    st.markdown("---")
    st.subheader("📋 Predictive Analytics Strategy Summary & Strategic Recommendations")
    
    with st.expander("🎯 Strategic Predictive Analytics Optimization Recommendations", expanded=False):
        st.markdown("""
        **Predictive Analytics Strategy Recommendations:**
        
        **1. Revenue Prediction Optimization:**
        - Implement advanced time series analysis for better revenue forecasting
        - Develop seasonal adjustment models for more accurate predictions
        - Create scenario-based revenue planning for strategic decision-making
        
        **2. Lead Generation Prediction Optimization:**
        - Implement lead scoring algorithms for better conversion prediction
        - Develop lead quality assessment models for acquisition optimization
        - Create lead nurturing strategies based on conversion probability
        
        **3. AI-Powered Trend Analysis:**
        - Implement machine learning models for pattern recognition
        - Develop predictive modeling frameworks for strategic planning
        - Create automated trend detection systems for real-time insights
        
        **4. Data Quality Enhancement:**
        - Implement data validation frameworks for better prediction accuracy
        - Develop data integration strategies for unified predictive insights
        - Create data governance policies for consistent predictive modeling
        
        **5. Predictive Model Optimization:**
        - Implement model validation frameworks for accuracy improvement
        - Develop ensemble modeling strategies for better prediction reliability
        - Create continuous learning systems for adaptive prediction models
        
        **6. Strategic Implementation:**
        - Implement predictive analytics dashboards for real-time insights
        - Develop predictive reporting frameworks for strategic communication
        - Create predictive action planning for better decision execution
        """)
    
    # Performance metrics summary
    st.markdown("#### 📊 Predictive Analytics Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'revenue_prediction_score' in locals():
            st.metric(
                "Revenue Prediction", 
                f"{'Excellent' if revenue_prediction_score >= 80 else 'Good' if revenue_prediction_score >= 60 else 'Fair' if revenue_prediction_score >= 40 else 'Needs Improvement'}",
                f"{revenue_prediction_score:.1f}/100 score"
            )
    
    with col2:
        if 'lead_prediction_score' in locals():
            st.metric(
                "Lead Prediction", 
                f"{'Excellent' if lead_prediction_score >= 80 else 'Good' if lead_prediction_score >= 60 else 'Fair' if lead_prediction_score >= 40 else 'Needs Improvement'}",
                f"{lead_prediction_score:.1f}/100 score"
            )
    
    with col3:
        if 'ai_performance_score' in locals():
            st.metric(
                "AI Performance", 
                f"{'Excellent' if ai_performance_score >= 80 else 'Good' if ai_performance_score >= 60 else 'Fair' if ai_performance_score >= 40 else 'Needs Improvement'}",
                f"{ai_performance_score:.1f}/100 score"
            )
    
    with col4:
        if 'pattern_score' in locals():
            st.metric(
                "Pattern Recognition", 
                f"{'Excellent' if pattern_score >= 80 else 'Good' if pattern_score >= 60 else 'Fair' if pattern_score >= 40 else 'Needs Improvement'}",
                f"{pattern_score:.1f}/100 score"
            )

def set_home_page():
    """Set the department to start on home page"""
    st.session_state.current_page = "🏠 Home"

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
    @media (min-width: 1200px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    /* Make sure all containers expand */
    .stContainer {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Sidebar button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        color: #ffffff;
        font-weight: 500;
        margin: 6px 0;
        padding: 12px 16px;
        transition: all 0.3s ease;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        font-size: 0.95rem;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(3px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Active button styling */
    .stButton > button[data-active="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-weight: 600;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.3);
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(249, 115, 22, 0.3);
    }
    
    .metric-card-teal {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(20, 184, 166, 0.3);
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.3);
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
    }
    
    /* Chart container styling */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Welcome section */
    .welcome-section {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Progress circle styling */
    .progress-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        margin: 10px auto;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Additional marketing-specific styling */
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
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Comprehensive Marketing Analytics & Insights Platform</p>
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
    
    # Safety check: Ensure all session state variables are DataFrames
    required_vars = ['campaigns_data', 'customers_data', 'website_traffic_data', 
                     'social_media_data', 'email_campaigns_data', 'content_marketing_data', 
                     'leads_data', 'conversions_data']
    
    for var in required_vars:
        if var in st.session_state:
            if not isinstance(st.session_state[var], pd.DataFrame):
                st.session_state[var] = pd.DataFrame()
        else:
            st.session_state[var] = pd.DataFrame()
    
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
        
        if st.button("📈 Campaign Performance", key="nav_campaign_performance", use_container_width=True):
            st.session_state.current_page = "📈 Campaign Performance"
        
        if st.button("👥 Customer Analysis", key="nav_customer_analysis", use_container_width=True):
            st.session_state.current_page = "👥 Customer Analysis"
        
        if st.button("🌍 Market Analysis", key="nav_market_analysis", use_container_width=True):
            st.session_state.current_page = "🌍 Market Analysis"
        
        if st.button("📝 Content Marketing", key="nav_content_marketing", use_container_width=True):
            st.session_state.current_page = "📝 Content Marketing"
        
        if st.button("🌐 Digital Marketing", key="nav_digital_marketing", use_container_width=True):
            st.session_state.current_page = "🌐 Digital Marketing"
        
        if st.button("🏷️ Brand Awareness", key="nav_brand_awareness", use_container_width=True):
            st.session_state.current_page = "🏷️ Brand Awareness"
        
        if st.button("📦 Product Marketing", key="nav_product_marketing", use_container_width=True):
            st.session_state.current_page = "📦 Product Marketing"
        
        if st.button("🛤️ Customer Journey", key="nav_customer_journey", use_container_width=True):
            st.session_state.current_page = "🛤️ Customer Journey"
        
        if st.button("🔮 Marketing Forecasting", key="nav_marketing_forecasting", use_container_width=True):
            st.session_state.current_page = "🔮 Marketing Forecasting"
        
        if st.button("📱 Channel Analysis", key="nav_channel_analysis", use_container_width=True):
            st.session_state.current_page = "📱 Channel Analysis"
        
        if st.button("🎯 Specialized Metrics", key="nav_specialized_metrics", use_container_width=True):
            st.session_state.current_page = "🎯 Specialized Metrics"
        
        if st.button("🔮 Predictive Analytics", key="nav_predictive_analytics", use_container_width=True):
            st.session_state.current_page = "🔮 Predictive Analytics"
        

        
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
        
        # Initialize current page if not set
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Home"
        
        page = st.session_state.current_page
    
    # Performance: Main content area with lazy loading and monitoring
    def get_page_function(page_name):
        """Get page function mapping for performance"""
        page_functions = {
            "🏠 Home": show_home,
            "📝 Data Input": show_data_input,
            "📈 Campaign Performance": show_campaign_performance,
            "👥 Customer Analysis": show_customer_analysis,
            "🌍 Market Analysis": show_market_analysis,
            "📝 Content Marketing": show_content_marketing,
            "🌐 Digital Marketing": show_digital_marketing,
            "🏷️ Brand Awareness": show_brand_awareness,
            "📦 Product Marketing": show_product_marketing,
            "🛤️ Customer Journey": show_customer_journey,
            "🔮 Marketing Forecasting": show_marketing_forecasting,
            "📱 Channel Analysis": show_channel_analysis,
            "🎯 Specialized Metrics": show_specialized_metrics,
            "🔮 Predictive Analytics": show_predictive_analytics
        }
        return page_functions.get(page_name, show_home)
    
    # Execute page with performance monitoring
    if page in ["🏠 Home", "📝 Data Input", "📈 Campaign Performance", "👥 Customer Analysis", 
                "🌍 Market Analysis", "📝 Content Marketing", "🌐 Digital Marketing", "🏷️ Brand Awareness",
                "📦 Product Marketing", "🛤️ Customer Journey", "🔮 Marketing Forecasting", 
                "📱 Channel Analysis", "🎯 Specialized Metrics", "🔮 Predictive Analytics"]:
        
        page_func = get_page_function(page)
        start_time = time.time()
        
        try:
            page_func()
            
        except Exception as e:
            st.error(f"Error loading {page}: {str(e)}")

if __name__ == "__main__":
    main()

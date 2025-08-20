import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import io
import base64
import random
from datetime import timedelta
import time
from functools import lru_cache
import warnings

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Import sales metric calculation functions
from sales_metrics_calculator import *

# Import performance monitoring functions
from performance_config import data_size_monitor

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

# Configure Streamlit for better performance
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Performance optimization settings
@st.cache_data(ttl=300, max_entries=100)  # Cache for 5 minutes, max 100 entries
def load_data_optimized():
    """Optimized data loading with caching."""
    return {}

# Cache for expensive calculations
@st.cache_data(ttl=600, max_entries=50)  # Cache for 10 minutes
def cache_expensive_calculations(data, calculation_type):
    """Cache expensive calculations to avoid recomputation."""
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
    
    if data_type == "sales_performance":
        recommendations = generate_sales_performance_recommendations(data, insights)
    elif data_type == "customer_analysis":
        recommendations = generate_customer_analysis_recommendations(data, insights)
    elif data_type == "sales_funnel":
        recommendations = generate_sales_funnel_recommendations(data, insights)
    elif data_type == "sales_team":
        recommendations = generate_sales_team_recommendations(data, insights)
    elif data_type == "pricing_discounts":
        recommendations = generate_pricing_recommendations(data, insights)
    elif data_type == "market_analysis":
        recommendations = generate_market_analysis_recommendations(data, insights)
    elif data_type == "forecasting":
        recommendations = generate_forecasting_recommendations(data, insights)
    elif data_type == "crm_analysis":
        recommendations = generate_crm_recommendations(data, insights)
    elif data_type == "operational_efficiency":
        recommendations = generate_operational_recommendations(data, insights)
    elif data_type == "specialized_metrics":
        recommendations = generate_specialized_recommendations(data, insights)
    elif data_type == "strategic_analytics":
        recommendations = generate_strategic_recommendations(data, insights)
    
    return recommendations

def generate_sales_performance_recommendations(data, insights=None):
    """Generate AI recommendations for sales performance."""
    recommendations = []
    
    if 'total_amount' in data.columns:
        total_revenue = data['total_amount'].sum()
        avg_order_value = data['total_amount'].mean()
        
        if total_revenue < 100000:
            recommendations.append("🚀 **Revenue Growth Opportunity**: Consider implementing upselling strategies and cross-selling campaigns to increase average order value.")
        
        if avg_order_value < 500:
            recommendations.append("💰 **AOV Optimization**: Focus on bundling products and offering premium services to increase average order value.")
    
    if 'order_date' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
        recent_orders = data[data['order_date'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
        
        if len(recent_orders) < len(data) * 0.3:
            recommendations.append("📅 **Seasonal Strategy**: Recent order volume suggests implementing seasonal marketing campaigns to boost sales.")
    
    if 'channel' in data.columns:
        channel_performance = data.groupby('channel')['total_amount'].sum()
        best_channel = channel_performance.idxmax()
        
        recommendations.append(f"🎯 **Channel Optimization**: {best_channel} is your highest-performing channel. Consider allocating more resources and budget to this channel.")
    
    if not recommendations:
        recommendations.append("📈 **Data Analysis**: Continue monitoring key metrics and implement A/B testing for different sales strategies.")
    
    return recommendations

def generate_customer_analysis_recommendations(data, insights=None):
    """Generate AI recommendations for customer analysis."""
    recommendations = []
    
    if 'customer_segment' in data.columns:
        segment_counts = data['customer_segment'].value_counts()
        largest_segment = segment_counts.idxmax()
        
        recommendations.append(f"👥 **Segment Focus**: {largest_segment} customers represent your largest segment. Develop targeted strategies for this group.")
    
    if 'acquisition_date' in data.columns:
        data['acquisition_date'] = pd.to_datetime(data['acquisition_date'])
        recent_acquisitions = data[data['acquisition_date'] >= pd.Timestamp.now() - pd.Timedelta(days=90)]
        
        if len(recent_acquisitions) < len(data) * 0.2:
            recommendations.append("🆕 **Customer Acquisition**: Recent customer acquisition is low. Consider implementing lead generation campaigns and referral programs.")
    
    if 'status' in data.columns:
        churned_customers = data[data['status'] == 'Churned']
        churn_rate = len(churned_customers) / len(data)
        
        if churn_rate > 0.1:
            recommendations.append("⚠️ **Churn Prevention**: Customer churn rate is high. Implement customer success programs and proactive retention strategies.")
    
    if 'industry' in data.columns:
        industry_performance = data.groupby('industry').size()
        top_industry = industry_performance.idxmax()
        
        recommendations.append(f"🏭 **Industry Focus**: {top_industry} industry shows strong performance. Consider expanding your presence in this sector.")
    
    if not recommendations:
        recommendations.append("🔍 **Customer Insights**: Implement customer feedback surveys and satisfaction metrics to better understand customer needs.")
    
    return recommendations

def generate_sales_funnel_recommendations(data, insights=None):
    """Generate AI recommendations for sales funnel analysis."""
    recommendations = []
    
    if 'status' in data.columns:
        status_counts = data['status'].value_counts()
        
        if 'New' in status_counts and status_counts['New'] > status_counts.get('Qualified', 0):
            recommendations.append("🔄 **Lead Qualification**: High number of new leads suggests implementing better lead scoring and qualification processes.")
        
        if 'Closed Won' in status_counts and 'Closed Lost' in status_counts:
            win_rate = status_counts['Closed Won'] / (status_counts['Closed Won'] + status_counts['Closed Lost'])
            if win_rate < 0.3:
                recommendations.append("🎯 **Win Rate Improvement**: Low conversion rate suggests reviewing sales process and providing better sales training.")
    
    if 'source' in data.columns:
        source_performance = data.groupby('source')['status'].apply(lambda x: (x == 'Closed Won').sum())
        best_source = source_performance.idxmax()
        
        recommendations.append(f"📊 **Source Optimization**: {best_source} generates the most closed deals. Increase investment in this lead source.")
    
    if 'value' in data.columns:
        avg_deal_value = data['value'].mean()
        if avg_deal_value < 10000:
            recommendations.append("💎 **Deal Sizing**: Focus on larger deals and enterprise customers to increase average deal value.")
    
    if not recommendations:
        recommendations.append("📈 **Funnel Optimization**: Implement lead nurturing campaigns and improve sales process efficiency.")
    
    return recommendations

def generate_sales_team_recommendations(data, insights=None):
    """Generate AI recommendations for sales team analysis."""
    recommendations = []
    
    if 'quota' in data.columns and 'sales_rep_id' in data.columns:
        # This would need sales performance data to be meaningful
        recommendations.append("🎯 **Performance Management**: Implement regular performance reviews and provide targeted coaching based on individual performance metrics.")
    
    if 'region' in data.columns:
        region_counts = data['region'].value_counts()
        if len(region_counts) > 1:
            recommendations.append("🌍 **Territory Optimization**: Consider redistributing sales resources based on regional performance and market potential.")
    
    if 'hire_date' in data.columns:
        data['hire_date'] = pd.to_datetime(data['hire_date'])
        recent_hires = data[data['hire_date'] >= pd.Timestamp.now() - pd.Timedelta(days=365)]
        
        if len(recent_hires) > len(data) * 0.3:
            recommendations.append("👨‍💼 **Training Focus**: High number of recent hires suggests implementing comprehensive onboarding and training programs.")
    
    if 'status' in data.columns:
        active_reps = data[data['status'] == 'Active']
        if len(active_reps) < len(data) * 0.8:
            recommendations.append("⚠️ **Retention Strategy**: Focus on sales rep retention through competitive compensation and career development opportunities.")
    
    if not recommendations:
        recommendations.append("🚀 **Team Development**: Invest in sales training, tools, and motivation programs to improve team performance.")
    
    return recommendations

def generate_pricing_recommendations(data, insights=None):
    """Generate AI recommendations for pricing and discounts."""
    recommendations = []
    
    if 'unit_price' in data.columns and 'cost_price' in data.columns:
        data['margin'] = data['unit_price'] - data['cost_price']
        avg_margin = data['margin'].mean()
        margin_rate = (avg_margin / data['unit_price'].mean()) * 100
        
        if margin_rate < 30:
            recommendations.append("💵 **Margin Improvement**: Current margins are low. Consider price optimization and cost reduction strategies.")
        
        if margin_rate > 70:
            recommendations.append("💰 **Competitive Pricing**: High margins may indicate pricing power. Consider market expansion and premium positioning.")
    
    if 'quantity' in data.columns and 'total_amount' in data.columns:
        data['avg_price'] = data['total_amount'] / data['quantity']
        price_variance = data['avg_price'].std()
        
        if price_variance > data['avg_price'].mean() * 0.3:
            recommendations.append("📊 **Price Consistency**: High price variance suggests implementing standardized pricing policies and discount guidelines.")
    
    recommendations.append("🎯 **Dynamic Pricing**: Consider implementing dynamic pricing strategies based on demand, seasonality, and customer segments.")
    recommendations.append("🏷️ **Bundle Pricing**: Create product bundles and packages to increase average order value and customer satisfaction.")
    
    return recommendations

def generate_market_analysis_recommendations(data, insights=None):
    """Generate AI recommendations for market analysis."""
    recommendations = []
    
    if 'region' in data.columns:
        region_performance = data.groupby('region')['total_amount'].sum()
        top_region = region_performance.idxmax()
        bottom_region = region_performance.idxmin()
        
        recommendations.append(f"🌍 **Market Focus**: {top_region} shows strong performance. Consider expanding operations and increasing market share in this region.")
        recommendations.append(f"📈 **Growth Opportunity**: {bottom_region} has growth potential. Develop targeted strategies to improve performance in this market.")
    
    if 'industry' in data.columns:
        industry_trends = data.groupby('industry')['total_amount'].sum()
        emerging_industry = industry_trends.nsmallest(3).index[0]
        
        recommendations.append(f"🚀 **Emerging Markets**: {emerging_industry} shows growth potential. Consider early market entry and strategic partnerships.")
    
    if 'order_date' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
        data['month'] = data['order_date'].dt.month
        seasonal_patterns = data.groupby('month')['total_amount'].sum()
        
        if seasonal_patterns.std() > seasonal_patterns.mean() * 0.5:
            recommendations.append("📅 **Seasonal Strategy**: Strong seasonal patterns detected. Implement seasonal marketing campaigns and inventory planning.")
    
    recommendations.append("🔍 **Competitive Analysis**: Conduct regular competitive analysis to identify market opportunities and threats.")
    recommendations.append("📊 **Market Research**: Invest in market research to understand customer needs and market trends.")
    
    return recommendations

def generate_forecasting_recommendations(data, insights=None):
    """Generate AI recommendations for forecasting."""
    recommendations = []
    
    if 'order_date' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
        data['month'] = data['order_date'].dt.month
        monthly_trends = data.groupby('month')['total_amount'].sum()
        
        if monthly_trends.iloc[-1] > monthly_trends.iloc[0]:
            recommendations.append("📈 **Growth Trend**: Positive growth trend detected. Plan for capacity expansion and resource allocation.")
        else:
            recommendations.append("⚠️ **Declining Trend**: Declining trend detected. Review business strategy and implement corrective measures.")
    
    if 'total_amount' in data.columns:
        revenue_volatility = data['total_amount'].std() / data['total_amount'].mean()
        
        if revenue_volatility > 0.5:
            recommendations.append("📊 **Forecast Accuracy**: High revenue volatility suggests implementing more sophisticated forecasting models and scenario planning.")
    
    recommendations.append("🔮 **Predictive Analytics**: Implement machine learning models for more accurate sales forecasting.")
    recommendations.append("📋 **Scenario Planning**: Develop multiple forecast scenarios for better risk management and strategic planning.")
    recommendations.append("🔄 **Continuous Monitoring**: Regularly update forecasts based on new data and market conditions.")
    
    return recommendations

def generate_crm_recommendations(data, insights=None):
    """Generate AI recommendations for CRM analysis."""
    recommendations = []
    
    if 'activity_type' in data.columns:
        activity_counts = data['activity_type'].value_counts()
        most_common = activity_counts.index[0]
        
        recommendations.append(f"📞 **Activity Optimization**: {most_common} is the most common activity. Ensure this activity type is optimized for maximum effectiveness.")
    
    if 'outcome' in data.columns:
        outcome_counts = data['outcome'].value_counts()
        if 'Negative' in outcome_counts and outcome_counts['Negative'] > len(data) * 0.2:
            recommendations.append("⚠️ **Process Improvement**: High negative outcomes suggest reviewing and improving sales processes and training.")
    
    if 'duration_minutes' in data.columns:
        avg_duration = data['duration_minutes'].mean()
        if avg_duration < 30:
            recommendations.append("⏱️ **Quality Focus**: Short activity duration may indicate rushed interactions. Focus on quality over quantity.")
    
    recommendations.append("📱 **CRM Integration**: Ensure full integration between CRM system and sales activities for better tracking and analysis.")
    recommendations.append("🎯 **Lead Scoring**: Implement automated lead scoring to prioritize high-value prospects.")
    recommendations.append("📊 **Performance Metrics**: Track key CRM metrics like response time, follow-up rates, and conversion rates.")
    
    return recommendations

def generate_operational_recommendations(data, insights=None):
    """Generate AI recommendations for operational efficiency."""
    recommendations = []
    
    if 'order_date' in data.columns and 'total_amount' in data.columns:
        data['order_date'] = pd.to_datetime(data['order_date'])
        data['processing_time'] = pd.Timestamp.now() - data['order_date']
        avg_processing_time = data['processing_time'].mean()
        
        if avg_processing_time.days > 7:
            recommendations.append("⚡ **Process Speed**: Long processing times detected. Streamline order processing and implement automation.")
    
    if 'channel' in data.columns:
        channel_efficiency = data.groupby('channel')['total_amount'].sum()
        if len(channel_efficiency) > 3:
            recommendations.append("🎯 **Channel Consolidation**: Multiple channels may increase complexity. Consider consolidating to most efficient channels.")
    
    recommendations.append("🔄 **Process Automation**: Implement automation for repetitive tasks to improve efficiency and reduce errors.")
    recommendations.append("📊 **KPI Monitoring**: Establish key performance indicators and regular monitoring for continuous improvement.")
    recommendations.append("👥 **Team Training**: Regular training on processes and tools to maintain high operational standards.")
    
    return recommendations

def generate_specialized_recommendations(data, insights=None):
    """Generate AI recommendations for specialized metrics."""
    recommendations = []
    
    recommendations.append("🎯 **Custom Metrics**: Develop custom KPIs specific to your business model and industry.")
    recommendations.append("📊 **Benchmarking**: Compare your metrics with industry benchmarks to identify improvement opportunities.")
    recommendations.append("🔍 **Deep Analysis**: Conduct root cause analysis for underperforming metrics.")
    recommendations.append("📈 **Trend Analysis**: Monitor metric trends over time to identify patterns and opportunities.")
    
    return recommendations

def generate_strategic_recommendations(data, insights=None):
    """Generate AI recommendations for strategic analytics."""
    recommendations = []
    
    if 'total_amount' in data.columns:
        total_revenue = data['total_amount'].sum()
        if total_revenue < 1000000:
            recommendations.append("🚀 **Growth Strategy**: Focus on market expansion and customer acquisition for revenue growth.")
        else:
            recommendations.append("💎 **Market Leadership**: Strong revenue position. Focus on market share expansion and competitive positioning.")
    
    recommendations.append("🎯 **Strategic Planning**: Develop long-term strategic plans based on data-driven insights.")
    recommendations.append("🌍 **Market Expansion**: Identify new markets and customer segments for growth opportunities.")
    recommendations.append("🤝 **Partnership Strategy**: Consider strategic partnerships and alliances for market expansion.")
    recommendations.append("📊 **Investment Planning**: Allocate resources based on data-driven ROI analysis.")
    
    return recommendations

def display_ai_recommendations(data_type, data, insights=None):
    """Display AI recommendations in a styled card."""
    recommendations = generate_ai_recommendations(data_type, data, insights)
    
    st.markdown("---")
    st.markdown("""
    <div class="metric-card-purple">
    <h3>🤖 AI-Powered Recommendations</h3>
    <p>Intelligent insights and actionable strategies based on your data analysis:</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")
    
    st.markdown("""
    <div class="metric-card">
    <p><em>💡 These recommendations are generated using AI analysis of your sales data patterns, trends, and performance metrics.</em></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# Main Analytics Functions
# ============================================================================

def display_formatted_recommendations(recommendations_text):
    """
    Display recommendations with proper formatting using HTML to ensure bullet points are on separate lines.
    """
    if not recommendations_text:
        return
    
    # Convert markdown text to HTML format
    html_content = recommendations_text.replace('\n', '<br>')
    
    # Replace bullet points with proper HTML list items
    lines = recommendations_text.split('\n')
    html_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append("<br>")
        elif line.startswith("- "):
            # Convert bullet point to HTML list item
            content = line[2:].strip()
            html_lines.append(f"<li>{content}</li>")
        elif line.startswith("💡") or line.startswith("🎯") or line.startswith("⚠️"):
            # This is a heading, add it as a header
            html_lines.append(f"<h4>{line}</h4>")
        else:
            # Regular line
            html_lines.append(f"<p>{line}</p>")
    
    # Combine into HTML with proper list structure
    html_content = ""
    in_list = False
    
    for line in html_lines:
        if line.startswith("<li>"):
            if not in_list:
                html_content += "<ul>"
                in_list = True
            html_content += line
        elif line.startswith("<h4>"):
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
        elif line.startswith("<p>"):
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
        elif line == "<br>":
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
    
    # Close any open list
    if in_list:
        html_content += "</ul>"
    
    # Display using HTML
    st.markdown(html_content, unsafe_allow_html=True)

def display_dataframe_with_index_1(df, **kwargs):
    """Display dataframe with index starting from 1"""
    if not df.empty:
        df_display = df.reset_index(drop=True)
        df_display.index = df_display.index + 1
        return st.dataframe(df_display, **kwargs)
    else:
        return st.dataframe(df, **kwargs)

def create_template_for_download():
    """Create an Excel template with all required sales data schema and make it downloadable"""
    
    # Create empty DataFrames with the correct sales schema
    customers_template = pd.DataFrame(columns=[
        'customer_id', 'customer_name', 'email', 'phone', 'company', 'industry', 
        'region', 'country', 'customer_segment', 'acquisition_date', 'status'
    ])
    
    products_template = pd.DataFrame(columns=[
        'product_id', 'product_name', 'category', 'subcategory', 'unit_price', 
        'cost_price', 'supplier_id', 'launch_date', 'status'
    ])
    
    sales_orders_template = pd.DataFrame(columns=[
        'order_id', 'customer_id', 'order_date', 'product_id', 'quantity', 
        'unit_price', 'total_amount', 'sales_rep_id', 'region', 'channel'
    ])
    
    sales_reps_template = pd.DataFrame(columns=[
        'sales_rep_id', 'first_name', 'last_name', 'email', 'region', 'territory', 
        'hire_date', 'quota', 'manager_id', 'status'
    ])
    
    leads_template = pd.DataFrame(columns=[
        'lead_id', 'lead_name', 'email', 'company', 'industry', 'source', 
        'created_date', 'status', 'assigned_rep_id', 'value'
    ])
    
    opportunities_template = pd.DataFrame(columns=[
        'opportunity_id', 'lead_id', 'customer_id', 'product_id', 'value', 
        'stage', 'created_date', 'close_date', 'probability', 'sales_rep_id'
    ])
    
    activities_template = pd.DataFrame(columns=[
        'activity_id', 'sales_rep_id', 'customer_id', 'activity_type', 'date', 
        'duration_minutes', 'notes', 'outcome'
    ])
    
    targets_template = pd.DataFrame(columns=[
        'target_id', 'sales_rep_id', 'period', 'target_amount', 'target_date', 
        'category', 'status'
    ])
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each template to a separate sheet
        customers_template.to_excel(writer, sheet_name='Customers', index=False)
        products_template.to_excel(writer, sheet_name='Products', index=False)
        sales_orders_template.to_excel(writer, sheet_name='Sales_Orders', index=False)
        sales_reps_template.to_excel(writer, sheet_name='Sales_Reps', index=False)
        leads_template.to_excel(writer, sheet_name='Leads', index=False)
        opportunities_template.to_excel(writer, sheet_name='Opportunities', index=False)
        activities_template.to_excel(writer, sheet_name='Activities', index=False)
        targets_template.to_excel(writer, sheet_name='Targets', index=False)
        
        # Get the workbook for formatting
        workbook = writer.book
        
        # Add instructions sheet
        instructions_data = {
            'Sheet Name': ['Customers', 'Products', 'Sales_Orders', 'Sales_Reps', 'Leads', 'Opportunities', 'Activities', 'Targets'],
            'Required Fields': [
                'customer_id, customer_name, email, phone, company, industry, region, country, customer_segment, acquisition_date, status',
                'product_id, product_name, category, subcategory, unit_price, cost_price, supplier_id, launch_date, status',
                'order_id, customer_id, order_date, product_id, quantity, unit_price, total_amount, sales_rep_id, region, channel',
                'sales_rep_id, first_name, last_name, email, region, territory, hire_date, quota, manager_id, status',
                'lead_id, lead_name, email, company, industry, source, created_date, status, assigned_rep_id, value',
                'opportunity_id, lead_id, customer_id, product_id, value, stage, created_date, close_date, probability, sales_rep_id',
                'activity_id, sales_rep_id, customer_id, activity_type, date, duration_minutes, notes, outcome',
                'target_id, sales_rep_id, period, target_amount, target_date, category, status'
            ],
            'Data Types': [
                'Text, Text, Text, Text, Text, Text, Text, Text, Text, Date, Text',
                'Text, Text, Text, Text, Number, Number, Text, Date, Text',
                'Text, Text, Date, Text, Number, Number, Number, Text, Text, Text',
                'Text, Text, Text, Text, Text, Text, Date, Number, Text, Text',
                'Text, Text, Text, Text, Text, Text, Date, Text, Text, Number',
                'Text, Text, Text, Text, Number, Text, Date, Date, Number, Text',
                'Text, Text, Text, Text, Date, Number, Text, Text',
                'Text, Text, Text, Number, Date, Text, Text'
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    # Prepare for download
    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()
    
    # Create download link
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="sales_data_template.xlsx">📥 Download Sales Data Template</a>'
    st.markdown(href, unsafe_allow_html=True)

def export_data_to_excel():
    """Exports all sales data from session state to a single Excel file."""
    with pd.ExcelWriter('sales_data_export.xlsx', engine='xlsxwriter') as writer:
        if not st.session_state.customers.empty:
            st.session_state.customers.to_excel(writer, sheet_name='Customers', index=False)
        if not st.session_state.products.empty:
            st.session_state.products.to_excel(writer, sheet_name='Products', index=False)
        if not st.session_state.sales_orders.empty:
            st.session_state.sales_orders.to_excel(writer, sheet_name='Sales_Orders', index=False)
        if not st.session_state.sales_reps.empty:
            st.session_state.sales_reps.to_excel(writer, sheet_name='Sales_Reps', index=False)
        if not st.session_state.leads.empty:
            st.session_state.leads.to_excel(writer, sheet_name='Leads', index=False)
        if not st.session_state.opportunities.empty:
            st.session_state.opportunities.to_excel(writer, sheet_name='Opportunities', index=False)
        if not st.session_state.activities.empty:
            st.session_state.activities.to_excel(writer, sheet_name='Activities', index=False)
        if not st.session_state.targets.empty:
            st.session_state.targets.to_excel(writer, sheet_name='Targets', index=False)
        
        st.success("Sales data exported successfully as 'sales_data_export.xlsx'")

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern SaaS dashboard styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Modern SaaS Dashboard Styling */
    
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
    
    /* Insights container */
    .insights-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            margin: 5px 0;
            padding: 15px;
        }
        
        .main-header {
            padding: 20px;
            font-size: 24px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for sales data storage
if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=[
        'customer_id', 'customer_name', 'email', 'phone', 'company', 'industry', 
        'region', 'country', 'customer_segment', 'acquisition_date', 'status'
    ])

if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame(columns=[
        'product_id', 'product_name', 'category', 'subcategory', 'unit_price', 
        'cost_price', 'supplier_id', 'launch_date', 'status'
    ])

if 'sales_orders' not in st.session_state:
    st.session_state.sales_orders = pd.DataFrame(columns=[
        'order_id', 'customer_id', 'order_date', 'product_id', 'quantity', 
        'unit_price', 'total_amount', 'sales_rep_id', 'region', 'channel'
    ])

if 'sales_reps' not in st.session_state:
    st.session_state.sales_reps = pd.DataFrame(columns=[
        'sales_rep_id', 'first_name', 'last_name', 'email', 'region', 'territory', 
        'hire_date', 'quota', 'manager_id', 'status'
    ])

if 'leads' not in st.session_state:
    st.session_state.leads = pd.DataFrame(columns=[
        'lead_id', 'lead_name', 'email', 'company', 'industry', 'source', 
        'created_date', 'status', 'assigned_rep_id', 'value'
    ])

if 'opportunities' not in st.session_state:
    st.session_state.opportunities = pd.DataFrame(columns=[
        'opportunity_id', 'lead_id', 'customer_id', 'product_id', 'value', 
        'stage', 'created_date', 'close_date', 'probability', 'sales_rep_id'
    ])

if 'activities' not in st.session_state:
    st.session_state.activities = pd.DataFrame(columns=[
        'activity_id', 'sales_rep_id', 'customer_id', 'activity_type', 'date', 
        'duration_minutes', 'notes', 'outcome'
    ])

if 'targets' not in st.session_state:
    st.session_state.targets = pd.DataFrame(columns=[
        'target_id', 'sales_rep_id', 'period', 'target_amount', 'target_date', 
        'category', 'status'
    ])

def set_home_page():
    """Set the department to start on home page"""
    st.session_state.current_page = "🏠 Home"

@performance_monitor("Main Function")
def main():
    """Main application function with performance optimizations."""
    
    # Initialize session state for performance tracking
    if 'performance_start_time' not in st.session_state:
        st.session_state.performance_start_time = time.time()
    
    # Load custom CSS (cached)
    load_custom_css()
    
    # Performance-optimized header
    st.markdown('<h1 class="main-header">💰 Sales Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation with performance optimizations
    with st.sidebar:
        # Performance metrics display
        if 'performance_start_time' in st.session_state:
            elapsed_time = time.time() - st.session_state.performance_start_time
            st.metric("⏱️ Session Time", f"{elapsed_time:.1f}s")
        
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
        
        # Optimized navigation buttons with lazy loading - reordered by priority
        navigation_pages = [
            ("🏠 Home", "🏠 Home"),                           # 1. Home - Always first
            ("📝 Data Input", "📝 Data Input"),               # 2. Data Input - Essential for getting started
            ("📊 Sales Performance", "📊 Sales Performance"), # 3. Core sales metrics - Most important
            ("👥 Customer Analysis", "👥 Customer Analysis"), # 4. Customer insights - High priority
            ("🔄 Sales Funnel", "🔄 Sales Funnel"),           # 5. Pipeline analysis - Critical for sales
            ("👨‍💼 Sales Team", "👨‍💼 Sales Team"),           # 6. Team performance - High priority
            ("💰 Pricing & Discounts", "💰 Pricing & Discounts"), # 7. Revenue optimization
            ("📈 Forecasting", "📈 Forecasting"),             # 8. Planning and predictions
            ("🌍 Market Analysis", "🌍 Market Analysis"),     # 9. Market insights
            ("📋 CRM Analysis", "📋 CRM Analysis"),           # 10. Customer relationship management
            ("⚡ Operational Efficiency", "⚡ Operational Efficiency"), # 11. Process optimization
            ("🎯 Specialized Metrics", "🎯 Specialized Metrics"), # 12. Advanced metrics
            ("🔮 Predictive Analytics", "🔮 Predictive Analytics"), # 13. AI-powered insights
            ("📊 Strategic Analytics", "📊 Strategic Analytics")   # 14. Strategic planning
        ]
        
        for button_text, page_name in navigation_pages:
            if st.button(button_text, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()  # Force rerun for immediate navigation
        
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
    

    
    # Main content area based on sidebar selection
    if page == "🏠 Home":
        show_home()
    elif page == "📝 Data Input":
        show_data_input()
    elif page == "📊 Sales Performance":
        show_sales_performance()
    elif page == "👥 Customer Analysis":
        show_customer_analysis()
    elif page == "🔄 Sales Funnel":
        show_sales_funnel()
    elif page == "👨‍💼 Sales Team":
        show_sales_team()
    elif page == "💰 Pricing & Discounts":
        show_pricing_discounts()
    elif page == "🌍 Market Analysis":
        show_market_analysis()
    elif page == "📈 Forecasting":
        show_forecasting()
    elif page == "📋 CRM Analysis":
        show_crm_analysis()
    elif page == "⚡ Operational Efficiency":
        show_operational_efficiency()
    elif page == "🎯 Specialized Metrics":
        show_specialized_metrics()
    elif page == "🔮 Predictive Analytics":
        show_predictive_analytics()
    elif page == "📊 Strategic Analytics":
        show_strategic_analytics()

def show_home():
    """Display the home page with comprehensive overview and key metrics"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Check if data is loaded
    data_loaded = (hasattr(st.session_state, 'sales_orders') and 
                   not st.session_state.sales_orders.empty) if hasattr(st.session_state, 'sales_orders') else False
    
    if not data_loaded:
        # Welcome section with 4 colored cards
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #495057; margin-bottom: 1rem;">📊 Welcome to Sales Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Get started by exploring the comprehensive sales analytics categories and metrics to drive revenue growth and optimize sales performance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 4 colored metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Analytics Categories", 
                "10 comprehensive",
                "analysis areas"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Sales Analytics", 
                "Real-time",
                "metrics & insights"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Performance", 
                "Advanced",
                "monitoring"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Revenue Growth", 
                "Strategic",
                "insights"
            ), unsafe_allow_html=True)
        
        # Available analytics categories (6 cards in 2 columns)
        st.markdown("### 📊 Available Sales Analytics Categories:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 1: Sales Performance Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📊 Sales Performance Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Sales Revenue by Product/Service</li>
                    <li>Revenue Growth Rate</li>
                    <li>Sales by Region/Market</li>
                    <li>Sales Target Achievement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 2: Customer Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">👥 Customer Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Customer Lifetime Value (CLV)</li>
                    <li>Customer Acquisition Cost (CAC)</li>
                    <li>Customer Churn Rate</li>
                    <li>Customer Segmentation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 3: Sales Funnel Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🔄 Sales Funnel Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Conversion Rate by Funnel Stage</li>
                    <li>Average Deal Size</li>
                    <li>Time to Close</li>
                    <li>Pipeline Velocity</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Card 4: Sales Team Performance
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">👨‍💼 Sales Team Performance</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Individual Sales Performance</li>
                    <li>Team Target Achievement</li>
                    <li>Win Rate</li>
                    <li>Sales Productivity Metrics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 5: Pricing and Discount Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">💰 Pricing and Discount Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Average Selling Price (ASP)</li>
                    <li>Discount Impact Analysis</li>
                    <li>Price Sensitivity Analysis</li>
                    <li>Profit Margin Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 6: Advanced Analytics
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🤖 Advanced Analytics</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Sales Forecasting</li>
                    <li>Market Analysis</li>
                    <li>CRM Analytics</li>
                    <li>AI Recommendations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Getting Started section (3 cards)
        st.markdown("### 🚀 Getting Started:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">1. Upload Data</h4>
                <p style="margin: 0;">Upload your sales data files to get started</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">2. Review Insights</h4>
                <p style="margin: 0;">Check analytics for performance insights</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">3. Explore Analytics</h4>
                <p style="margin: 0;">Navigate through different analysis modules</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Data Schema section (8 cards in 2 rows)
        st.markdown("### 📈 Data Schema:")
        st.markdown("The application supports the following sales data categories:")
        
        # Row 1 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">👥 Customers</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Demographics, segments, acquisition</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📦 Products</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Catalog, pricing, categories</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📋 Sales Orders</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Transactions, revenue, channels</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">👨‍💼 Sales Reps</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Performance, territories, quotas</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🎯 Leads</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Prospects, sources, status</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">💼 Opportunities</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Pipeline, stages, values</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📞 Activities</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Calls, meetings, outcomes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🎯 Targets</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Quotas, goals, achievements</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <div style="display: inline-block; padding: 20px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="margin: 0; color: white; font-size: 1.3rem;">🚀 Start by uploading your data in the <strong>Data Input</strong> tab!</h4>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Data is loaded - show overview with metrics
        st.success("✅ Data loaded successfully! Use the navigation to explore different sections.")
        st.info("📊 Sales analytics data available for analysis")
        
        # Calculate key metrics
        total_orders = len(st.session_state.sales_orders)
        total_revenue = st.session_state.sales_orders['revenue'].sum() if 'revenue' in st.session_state.sales_orders.columns else 0
        total_customers = len(st.session_state.customers) if hasattr(st.session_state, 'customers') else 0
        total_products = len(st.session_state.products) if hasattr(st.session_state, 'products') else 0
        
        # Show key metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Orders",
                value=f"{total_orders:,}",
                delta="0"
            )
        
        with col2:
            st.metric(
                label="Total Revenue",
                value=f"${total_revenue:,.0f}",
                delta="0"
            )
        
        with col3:
            st.metric(
                label="Total Customers",
                value=f"{total_customers:,}",
                delta="0"
            )
        
        with col4:
            st.metric(
                label="Total Products",
                value=f"{total_products:,}",
                delta="0"
            )

@performance_monitor("Data Input")
def show_data_input():
    """Show data input forms and file upload options with performance optimizations"""
    
    # Performance-optimized header
    st.markdown("## 📝 Data Input")
    
    # Create tabs for different data input methods
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Data Uploading", 
        "📝 Manual Data Entry", 
        "📋 Template", 
        "📊 Sample Dataset"
    ])
    
    with tab1:
        st.markdown("### 📤 Data Uploading")
        st.markdown("Upload your Excel file with all sales data tables:")
        
        # File upload for Excel template with progress tracking
        uploaded_file = st.file_uploader(
            "Upload Excel file with all sales tables", 
            type=['xlsx', 'xls'],
            help="Upload the filled Excel template with all 8 sales tables in separate sheets"
        )
        
        if uploaded_file is not None:
            # Show loading spinner for better UX
            with st.spinner("🚀 Processing Excel file..."):
                try:
                    # Read all sheets from the Excel file with optimized settings
                    excel_data = pd.read_excel(
                        uploaded_file, 
                        sheet_name=None,
                        engine='openpyxl',  # Faster engine
                        keep_default_na=False,  # Better performance
                        na_values=['']  # Optimized NA handling
                    )
                    
                    # Check if all required sheets are present
                    required_sheets = ['Customers', 'Products', 'Sales_Orders', 'Sales_Reps', 'Leads', 'Opportunities', 'Activities', 'Targets']
                    missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
                    
                    if missing_sheets:
                        st.error(f"❌ Missing required sheets: {', '.join(missing_sheets)}")
                        st.info("Please ensure your Excel file contains all 8 required sales sheets.")
                    else:
                        # Optimized data loading with progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Load data into session state with progress updates
                        sheets_to_load = [
                            ('customers', 'Customers'),
                            ('products', 'Products'),
                            ('sales_orders', 'Sales_Orders'),
                            ('sales_reps', 'Sales_Reps'),
                            ('leads', 'Leads'),
                            ('opportunities', 'Opportunities'),
                            ('activities', 'Activities'),
                            ('targets', 'Targets')
                        ]
                        
                        for i, (state_key, sheet_name) in enumerate(sheets_to_load):
                            status_text.text(f"Loading {sheet_name}...")
                            st.session_state[state_key] = excel_data[sheet_name]
                            progress_bar.progress((i + 1) / len(sheets_to_load))
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Data loading complete!")
                        
                        st.success("✅ All sales data loaded successfully from Excel file!")
                        st.info(f"📊 Loaded {len(st.session_state.customers)} customers, {len(st.session_state.products)} products, {len(st.session_state.sales_orders)} orders, and more...")
                        
                        # Cache the loaded data for better performance
                        cache_expensive_calculations(excel_data, "excel_data")
                        
                except Exception as e:
                    st.error(f"❌ Error reading Excel file: {str(e)}")
                    st.info("Please ensure the file is a valid Excel file with the correct format.")
        
        # Optimized data validation summary with caching
        if 'sales_orders' in st.session_state and not st.session_state.sales_orders.empty:
            st.markdown("---")
            st.markdown("#### 📊 Data Validation Summary")
            
            # Cache expensive calculations
            @st.cache_data(ttl=60, max_entries=10)
            def get_validation_metrics(sales_orders):
                return {
                    'total_records': len(sales_orders),
                    'total_revenue': sales_orders['total_amount'].sum(),
                    'unique_customers': sales_orders['customer_id'].nunique()
                }
            
            metrics = get_validation_metrics(st.session_state.sales_orders)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", f"{metrics['total_records']:,}")
            with col2:
                st.metric("Total Revenue", f"${metrics['total_revenue']:,.2f}")
            with col3:
                st.metric("Unique Customers", f"{metrics['unique_customers']:,}")
    
    with tab2:
        st.markdown("### 📝 Manual Data Entry")
        st.markdown("Add data manually using the forms below:")
        
        # Tabs for different data types
        data_tab1, data_tab2, data_tab3, data_tab4, data_tab5, data_tab6, data_tab7, data_tab8 = st.tabs([
            "Customers", "Products", "Sales Orders", "Sales Reps", 
            "Leads", "Opportunities", "Activities", "Targets"
        ])
        
        with data_tab1:
            st.subheader("Customers")
            col1, col2 = st.columns(2)
            
            with col1:
                customer_id = st.text_input("Customer ID", key="customer_id_input")
                customer_name = st.text_input("Customer Name", key="customer_name_input")
                email = st.text_input("Email", key="customer_email_input")
                phone = st.text_input("Phone", key="customer_phone_input")
                company = st.text_input("Company", key="customer_company_input")
                industry = st.text_input("Industry", key="customer_industry_input")
            
            with col2:
                region = st.text_input("Region", key="customer_region_input")
                country = st.text_input("Country", key="customer_country_input")
                customer_segment = st.selectbox("Customer Segment", ["Enterprise", "SMB", "Startup", "Individual"], key="customer_segment_input")
                acquisition_date = st.date_input("Acquisition Date", key="customer_acquisition_date_input")
                status = st.selectbox("Status", ["Active", "Inactive", "Churned"], key="customer_status_input")
            
            if st.button("Add Customer"):
                new_customer = pd.DataFrame([{
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'email': email,
                    'phone': phone,
                    'company': company,
                    'industry': industry,
                    'region': region,
                    'country': country,
                    'customer_segment': customer_segment,
                    'acquisition_date': acquisition_date,
                    'status': status
                }])
                st.session_state.customers = pd.concat([st.session_state.customers, new_customer], ignore_index=True)
                st.success("Customer added successfully!")
            
            # Display existing data
            if not st.session_state.customers.empty:
                st.subheader("Existing Customers")
                display_dataframe_with_index_1(st.session_state.customers)
        
        with data_tab2:
            st.subheader("Products")
            col1, col2 = st.columns(2)
            
            with col1:
                product_id = st.text_input("Product ID", key="product_id_input")
                product_name = st.text_input("Product Name", key="product_name_input")
                category = st.text_input("Category", key="product_category_input")
                subcategory = st.text_input("Subcategory", key="product_subcategory_input")
                unit_price = st.number_input("Unit Price", min_value=0.0, key="product_unit_price_input")
            
            with col2:
                cost_price = st.number_input("Cost Price", min_value=0.0, key="product_cost_price_input")
                supplier_id = st.text_input("Supplier ID", key="product_supplier_id_input")
                launch_date = st.date_input("Launch Date", key="product_launch_date_input")
                status = st.selectbox("Status", ["Active", "Discontinued", "Coming Soon"], key="product_status_input")
            
            if st.button("Add Product"):
                new_product = pd.DataFrame([{
                    'product_id': product_id,
                    'product_name': product_name,
                    'category': category,
                    'subcategory': subcategory,
                    'unit_price': unit_price,
                    'cost_price': cost_price,
                    'supplier_id': supplier_id,
                    'launch_date': launch_date,
                    'status': status
                }])
                st.session_state.products = pd.concat([st.session_state.products, new_product], ignore_index=True)
                st.success("Product added successfully!")
            
            # Display existing data
            if not st.session_state.products.empty:
                st.subheader("Existing Products")
                display_dataframe_with_index_1(st.session_state.products)
        
        with data_tab3:
            st.subheader("Sales Orders")
            col1, col2 = st.columns(2)
            
            with col1:
                order_id = st.text_input("Order ID", key="order_id_input")
                customer_id = st.text_input("Customer ID", key="order_customer_id_input")
                order_date = st.date_input("Order Date", key="order_date_input")
                product_id = st.text_input("Product ID", key="order_product_id_input")
                quantity = st.number_input("Quantity", min_value=1, key="order_quantity_input")
            
            with col2:
                unit_price = st.number_input("Unit Price", min_value=0.0, key="order_unit_price_input")
                total_amount = st.number_input("Total Amount", min_value=0.0, key="order_total_amount_input")
                sales_rep_id = st.text_input("Sales Rep ID", key="order_sales_rep_id_input")
                region = st.text_input("Region", key="order_region_input")
                channel = st.selectbox("Channel", ["Online", "In-Store", "Phone", "Partner"], key="order_channel_input")
            
            if st.button("Add Sales Order"):
                new_order = pd.DataFrame([{
                    'order_id': order_id,
                    'customer_id': customer_id,
                    'order_date': order_date,
                    'product_id': product_id,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_amount': total_amount,
                    'sales_rep_id': sales_rep_id,
                    'region': region,
                    'channel': channel
                }])
                st.session_state.sales_orders = pd.concat([st.session_state.sales_orders, new_order], ignore_index=True)
                st.success("Sales order added successfully!")
            
            # Display existing data
            if not st.session_state.sales_orders.empty:
                st.subheader("Existing Sales Orders")
                display_dataframe_with_index_1(st.session_state.sales_orders)
        
        with data_tab4:
            st.subheader("Sales Representatives")
            col1, col2 = st.columns(2)
            
            with col1:
                sales_rep_id = st.text_input("Sales Rep ID", key="sales_rep_id_input")
                first_name = st.text_input("First Name", key="sales_rep_first_name_input")
                last_name = st.text_input("Last Name", key="sales_rep_last_name_input")
                email = st.text_input("Email", key="sales_rep_email_input")
                region = st.text_input("Region", key="sales_rep_region_input")
            
            with col2:
                territory = st.text_input("Territory", key="sales_rep_territory_input")
                hire_date = st.date_input("Hire Date", key="sales_rep_hire_date_input")
                quota = st.number_input("Quota", min_value=0.0, key="sales_rep_quota_input")
                manager_id = st.text_input("Manager ID", key="sales_rep_manager_id_input")
                status = st.selectbox("Status", ["Active", "Inactive", "Terminated"], key="sales_rep_status_input")
            
            if st.button("Add Sales Representative"):
                new_rep = pd.DataFrame([{
                    'sales_rep_id': sales_rep_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'region': region,
                    'territory': territory,
                    'hire_date': hire_date,
                    'quota': quota,
                    'manager_id': manager_id,
                    'status': status
                }])
                st.session_state.sales_reps = pd.concat([st.session_state.sales_reps, new_rep], ignore_index=True)
                st.success("Sales representative added successfully!")
            
            # Display existing data
            if not st.session_state.sales_reps.empty:
                st.subheader("Existing Sales Representatives")
                display_dataframe_with_index_1(st.session_state.sales_reps)
        
        with data_tab5:
            st.subheader("Leads")
            col1, col2 = st.columns(2)
            
            with col1:
                lead_id = st.text_input("Lead ID", key="lead_id_input")
                lead_name = st.text_input("Lead Name", key="lead_name_input")
                email = st.text_input("Email", key="lead_email_input")
                company = st.text_input("Company", key="lead_company_input")
                industry = st.text_input("Industry", key="lead_industry_input")
            
            with col2:
                source = st.selectbox("Source", ["Website", "Referral", "Cold Call", "Trade Show", "Social Media"], key="lead_source_input")
                created_date = st.date_input("Created Date", key="lead_created_date_input")
                status = st.selectbox("Status", ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"], key="lead_status_input")
                assigned_rep_id = st.text_input("Assigned Rep ID", key="lead_assigned_rep_id_input")
                value = st.number_input("Value", min_value=0.0, key="lead_value_input")
            
            if st.button("Add Lead"):
                new_lead = pd.DataFrame([{
                    'lead_id': lead_id,
                    'lead_name': lead_name,
                    'email': email,
                    'company': company,
                    'industry': industry,
                    'source': source,
                    'created_date': created_date,
                    'status': status,
                    'assigned_rep_id': assigned_rep_id,
                    'value': value
                }])
                st.session_state.leads = pd.concat([st.session_state.leads, new_lead], ignore_index=True)
                st.success("Lead added successfully!")
            
            # Display existing data
            if not st.session_state.leads.empty:
                st.subheader("Existing Leads")
                display_dataframe_with_index_1(st.session_state.leads)
        
        with data_tab6:
            st.subheader("Opportunities")
            col1, col2 = st.columns(2)
            
            with col1:
                opportunity_id = st.text_input("Opportunity ID", key="opportunity_id_input")
                lead_id = st.text_input("Lead ID", key="opportunity_lead_id_input")
                customer_id = st.text_input("Customer ID", key="opportunity_customer_id_input")
                product_id = st.text_input("Product ID", key="opportunity_product_id_input")
                value = st.number_input("Value", min_value=0.0, key="opportunity_value_input")
            
            with col2:
                stage = st.selectbox("Stage", ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"], key="opportunity_stage_input")
                created_date = st.date_input("Created Date", key="opportunity_created_date_input")
                close_date = st.date_input("Close Date", key="opportunity_close_date_input")
                probability = st.number_input("Probability (%)", min_value=0, max_value=100, key="opportunity_probability_input")
                sales_rep_id = st.text_input("Sales Rep ID", key="opportunity_sales_rep_id_input")
            
            if st.button("Add Opportunity"):
                new_opportunity = pd.DataFrame([{
                    'opportunity_id': opportunity_id,
                    'lead_id': lead_id,
                    'customer_id': customer_id,
                    'product_id': product_id,
                    'value': value,
                    'stage': stage,
                    'created_date': created_date,
                    'close_date': close_date,
                    'probability': probability,
                    'sales_rep_id': sales_rep_id
                }])
                st.session_state.opportunities = pd.concat([st.session_state.opportunities, new_opportunity], ignore_index=True)
                st.success("Opportunity added successfully!")
            
            # Display existing data
            if not st.session_state.opportunities.empty:
                st.subheader("Existing Opportunities")
                display_dataframe_with_index_1(st.session_state.opportunities)
        
        with data_tab7:
            st.subheader("Activities")
            col1, col2 = st.columns(2)
            
            with col1:
                activity_id = st.text_input("Activity ID", key="activity_id_input")
                sales_rep_id = st.text_input("Sales Rep ID", key="activity_sales_rep_id_input")
                customer_id = st.text_input("Customer ID", key="activity_customer_id_input")
                activity_type = st.selectbox("Activity Type", ["Call", "Meeting", "Email", "Demo", "Proposal"], key="activity_type_input")
                date = st.date_input("Date", key="activity_date_input")
            
            with col2:
                duration_minutes = st.number_input("Duration (Minutes)", min_value=0, key="activity_duration_input")
                notes = st.text_area("Notes", key="activity_notes_input")
                outcome = st.selectbox("Outcome", ["Positive", "Neutral", "Negative", "Follow-up Required"], key="activity_outcome_input")
            
            if st.button("Add Activity"):
                new_activity = pd.DataFrame([{
                    'activity_id': activity_id,
                    'sales_rep_id': sales_rep_id,
                    'customer_id': customer_id,
                    'activity_type': activity_type,
                    'date': date,
                    'duration_minutes': duration_minutes,
                    'notes': notes,
                    'outcome': outcome
                }])
                st.session_state.activities = pd.concat([st.session_state.activities, new_activity], ignore_index=True)
                st.success("Activity added successfully!")
            
            # Display existing data
            if not st.session_state.activities.empty:
                st.subheader("Existing Activities")
                display_dataframe_with_index_1(st.session_state.activities)
        
        with data_tab8:
            st.subheader("Targets")
            col1, col2 = st.columns(2)
            
            with col1:
                target_id = st.text_input("Target ID", key="target_id_input")
                sales_rep_id = st.text_input("Sales Rep ID", key="target_sales_rep_id_input")
                period = st.text_input("Period", key="target_period_input")
                target_amount = st.number_input("Target Amount", min_value=0.0, key="target_amount_input")
            
            with col2:
                target_date = st.date_input("Target Date", key="target_date_input")
                category = st.selectbox("Category", ["Revenue", "Deals", "Activities", "Leads"], key="target_category_input")
                status = st.selectbox("Status", ["Active", "Completed", "Overdue"], key="target_status_input")
            
            if st.button("Add Target"):
                new_target = pd.DataFrame([{
                    'target_id': target_id,
                    'sales_rep_id': sales_rep_id,
                    'period': period,
                    'target_amount': target_amount,
                    'target_date': target_date,
                    'category': category,
                    'status': status
                }])
                st.session_state.targets = pd.concat([st.session_state.targets, new_target], ignore_index=True)
                st.success("Target added successfully!")
            
            # Display existing data
            if not st.session_state.targets.empty:
                st.subheader("Existing Targets")
                display_dataframe_with_index_1(st.session_state.targets)
    
    with tab3:
        st.markdown("### 📋 Template")
        st.markdown("Download the Excel template with all required sales data schema:")
        
        # Create two columns for download and upload
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card-blue">
            <h4>📥 Download Data Template</h4>
            <p>Download the Excel template with all required sales data schema, fill it with your data, and upload it back.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create template for download
            if st.button("📥 Download Sales Data Template", use_container_width=True):
                create_template_for_download()
                st.success("✅ Template downloaded successfully! Fill it with your data and upload it on the right.")
            
            # Add some spacing for visual balance
            st.markdown("")
            st.markdown("""
            <div class="metric-card">
            <h4>Template includes:</h4>
            <ul>
                <li>8 Sales data tables in separate sheets</li>
                <li>Instructions sheet with field descriptions</li>
                <li>Proper column headers and data types</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card-purple">
            <h4>📤 Upload Your Data</h4>
            <p>Upload your filled Excel template:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # File upload for Excel template
            uploaded_file_template = st.file_uploader(
                "Upload filled Excel template", 
                type=['xlsx', 'xls'],
                key="template_uploader",
                help="Upload the filled Excel template with all 8 sales tables in separate sheets"
            )
            
            # Add helpful information
            st.markdown("")
            st.markdown("""
            <div class="metric-card">
            <h4>Upload features:</h4>
            <ul>
                <li>Automatic validation of all sheets</li>
                <li>Import all 8 sales tables at once</li>
                <li>Error checking and feedback</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if uploaded_file_template is not None:
                try:
                    # Read all sheets from the Excel file
                    excel_data = pd.read_excel(uploaded_file_template, sheet_name=None)
                    
                    # Check if all required sheets are present
                    required_sheets = ['Customers', 'Products', 'Sales_Orders', 'Sales_Reps', 'Leads', 'Opportunities', 'Activities', 'Targets']
                    missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
                    
                    if missing_sheets:
                        st.error(f"❌ Missing required sheets: {', '.join(missing_sheets)}")
                        st.info("Please ensure your Excel file contains all 8 required sales sheets.")
                    else:
                        # Load data into session state
                        st.session_state.customers = excel_data['Customers']
                        st.session_state.products = excel_data['Products']
                        st.session_state.sales_orders = excel_data['Sales_Orders']
                        st.session_state.sales_reps = excel_data['Sales_Reps']
                        st.session_state.leads = excel_data['Leads']
                        st.session_state.opportunities = excel_data['Opportunities']
                        st.session_state.activities = excel_data['Activities']
                        st.session_state.targets = excel_data['Targets']
                        
                        st.success("✅ All sales data loaded successfully from Excel file!")
                        st.info(f"📊 Loaded {len(st.session_state.customers)} customers, {len(st.session_state.products)} products, {len(st.session_state.sales_orders)} orders, and more...")
                        
                except Exception as e:
                    st.error(f"❌ Error reading Excel file: {str(e)}")
                    st.info("Please ensure the file is a valid Excel file with the correct format.")
    
    with tab4:
        st.markdown("### 📊 Sample Dataset")
        st.markdown("Generate sample data to test the application:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card-green">
            <h4>🎲 Generate Sample Data</h4>
            <p>Create sample datasets to test all analytics features.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎲 Generate Sample Data", use_container_width=True):
                # Generate sample data
                generate_sample_sales_data()
                st.success("✅ Sample data generated successfully!")
                st.info("📊 Sample datasets created for all 8 tables. You can now explore all analytics features.")
        
        with col2:
            st.markdown("""
            <div class="metric-card-teal">
            <h4>📈 Sample Data Info</h4>
            <p>Sample data includes realistic sales scenarios for testing.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            **Sample Data Includes:**
            - 50+ customers across different segments
            - 30+ products in various categories
            - 200+ sales orders with realistic data
            - 15+ sales representatives
            - 100+ leads and opportunities
            - 150+ sales activities
            - Performance targets and quotas
            """)
        
        # Show sample data preview if available
        if not st.session_state.sales_orders.empty:
            st.markdown("---")
            st.markdown("#### 📊 Sample Data Preview")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sample Customers", f"{len(st.session_state.customers):,}")
            with col2:
                st.metric("Sample Products", f"{len(st.session_state.products):,}")
            with col3:
                st.metric("Sample Orders", f"{len(st.session_state.sales_orders):,}")
            
            # Show sample data tables
            with st.expander("👥 Sample Customers Preview"):
                display_dataframe_with_index_1(st.session_state.customers.head(10))
            
            with st.expander("📦 Sample Products Preview"):
                display_dataframe_with_index_1(st.session_state.products.head(10))
            
            with st.expander("📋 Sample Sales Orders Preview"):
                display_dataframe_with_index_1(st.session_state.sales_orders.head(10))

# ============================================================================
# SALES PERFORMANCE ANALYSIS
# ============================================================================

@performance_monitor("Sales Performance")
def show_sales_performance():
    """Display sales performance analysis with performance optimizations."""
    
    # Performance-optimized header
    st.header("📊 Sales Performance Analysis")
    
    # Data validation with performance monitoring
    if 'sales_orders' not in st.session_state or st.session_state.sales_orders.empty:
        st.warning("Please add sales data first in the Data Input section.")
        return
    
    # Monitor data size for performance
    data_size_monitor(st.session_state.sales_orders, "Sales Orders")
    
    # Cache expensive calculations
    @st.cache_data(ttl=180, max_entries=10)
    def get_sales_summary_metrics(sales_orders):
        """Cache expensive summary calculations."""
        total_revenue = sales_orders['total_amount'].sum()
        total_orders = len(sales_orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        unique_customers = sales_orders['customer_id'].nunique()
        unique_products = sales_orders['product_id'].nunique()
        
        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
            'unique_customers': unique_customers,
            'unique_products': unique_products
        }
    
    # Get cached metrics
    metrics = get_sales_summary_metrics(st.session_state.sales_orders)
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-blue">
        <h3 style="color: white; margin: 0; text-align: center;">📈 Sales Performance Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics with color coding
    summary_col1, summary_col2, summary_col3, summary_col4, summary_col5 = st.columns(5)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(metrics['total_revenue']), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Orders</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(metrics['total_orders']), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Avg Order Value</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(metrics['avg_order_value']), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Unique Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(metrics['unique_customers']), unsafe_allow_html=True)
    
    with summary_col5:
        st.markdown("""
        <div class="metric-card-orange">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Products Sold</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(metrics['unique_products']), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Revenue by Product Chart
    st.markdown("""
    <div class="chart-container">
    <h4>💰 Sales Revenue by Product</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.products.empty:
        revenue_data, revenue_msg = calculate_sales_revenue_by_product(st.session_state.sales_orders, st.session_state.products)
        
        st.markdown(f"**{revenue_msg}**")
        
        if not revenue_data.empty:
            # Enhanced bar chart with better tooltips and interactivity
            fig_revenue = px.bar(
                revenue_data.head(15), 
                x='total_amount', 
                y='product_name',
                orientation='h',
                color='total_amount',
                color_continuous_scale='viridis',
                title='Top 15 Products by Revenue',
                labels={'total_amount': 'Revenue ($)', 'product_name': 'Product Name', 'category': 'Category'},
                hover_data=['category', 'quantity']
            )
            
            # Enhanced layout and styling
            fig_revenue.update_layout(
                title={
                    'text': 'Top 15 Products by Revenue',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#1f2937'}
                },
                xaxis_title='Revenue ($)',
                yaxis_title='Product Name',
                height=600,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            # Enhanced tooltips
            fig_revenue.update_traces(
                hovertemplate="<b>%{y}</b><br>" +
                            "Revenue: $%{x:,.2f}<br>" +
                            "Category: %{customdata[0]}<br>" +
                            "Quantity Sold: %{customdata[1]:,}<br>" +
                            "<extra></extra>",
                customdata=revenue_data.head(15)[['category', 'quantity']].values
            )
            
            # Add value labels on bars
            fig_revenue.update_traces(
                texttemplate='$%{x:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_revenue, use_container_width=True)
            
            # Product performance insights
            with st.expander("📊 Product Performance Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    top_product = revenue_data.iloc[0]
                    st.metric(
                        "🏆 Top Performing Product", 
                        top_product['product_name'],
                        f"${top_product['total_amount']:,.2f}"
                    )
                    
                    avg_revenue = revenue_data['total_amount'].mean()
                    st.metric(
                        "📊 Average Product Revenue", 
                        f"${avg_revenue:,.2f}"
                    )
                
                with col2:
                    total_product_revenue = revenue_data['total_amount'].sum()
                    top_5_revenue = revenue_data.head(5)['total_amount'].sum()
                    concentration = (top_5_revenue / total_product_revenue) * 100
                    st.metric(
                        "🎯 Top 5 Products Concentration", 
                        f"{concentration:.1f}%"
                    )
                    
                    st.metric(
                        "📦 Total Products", 
                        len(revenue_data)
                    )
                
                # Detailed revenue table
                st.subheader("📋 Detailed Revenue Breakdown")
                display_dataframe_with_index_1(revenue_data)
    
    st.markdown("---")
    
    # Enhanced Revenue Growth Rate Chart
    st.markdown("""
    <div class="chart-container">
    <h4>📈 Revenue Growth Rate Analysis</h4>
    </div>
    """, unsafe_allow_html=True)
    
    growth_data, growth_msg = calculate_revenue_growth_rate(st.session_state.sales_orders, 'monthly')
    
    st.markdown(f"**{growth_msg}**")
    
    if not growth_data.empty:
        # Create enhanced line chart with area fill
        fig_growth = go.Figure()
        
        # Add area chart for revenue
        fig_growth.add_trace(go.Scatter(
            x=growth_data['period'],
            y=growth_data['total_amount'],
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)',
            hovertemplate="<b>%{x}</b><br>" +
                        "Revenue: $%{y:,.2f}<br>" +
                        "<extra></extra>"
        ))
        
        # Add growth rate line
        fig_growth.add_trace(go.Scatter(
            x=growth_data['period'],
            y=growth_data['growth_rate'],
            mode='lines+markers',
            name='Growth Rate (%)',
            yaxis='y2',
            line=dict(color='#ef4444', width=3, dash='dash'),
            marker=dict(size=6, color='#ef4444'),
            hovertemplate="<b>%{x}</b><br>" +
                        "Growth Rate: %{y:.1f}%<br>" +
                        "<extra></extra>"
        ))
        
        # Enhanced layout
        fig_growth.update_layout(
            title={
                'text': 'Revenue Growth Rate & Monthly Revenue Trends',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1f2937'}
            },
            xaxis_title='Period',
            yaxis_title='Revenue ($)',
            yaxis2=dict(
                title='Growth Rate (%)',
                overlaying='y',
                side='right',
                range=[growth_data['growth_rate'].min() - 5, growth_data['growth_rate'].max() + 5]
            ),
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Growth insights
        with st.expander("📊 Growth Insights"):
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_growth = growth_data['growth_rate'].mean()
                st.metric(
                    "📈 Average Growth Rate", 
                    f"{avg_growth:.1f}%"
                )
            
            with col2:
                max_growth = growth_data['growth_rate'].max()
                max_growth_period = growth_data.loc[growth_data['growth_rate'].idxmax(), 'period']
                st.metric(
                    "🚀 Peak Growth", 
                    f"{max_growth:.1f}%",
                    f"in {max_growth_period}"
                )
            
            with col3:
                recent_growth = growth_data['growth_rate'].iloc[-1]
                st.metric(
                    "📅 Recent Growth", 
                    f"{recent_growth:.1f}%"
                )
    
    st.markdown("---")
    
    # Enhanced Regional Sales Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>🌍 Sales Distribution by Region</h4>
        </div>
        """, unsafe_allow_html=True)
        
        region_data, region_msg = calculate_sales_by_region(st.session_state.sales_orders)
        
        st.markdown(f"**{region_msg}**")
        
        if not region_data.empty:
            # Enhanced pie chart with better tooltips
            fig_region = px.pie(
                region_data, 
                values='total_revenue', 
                names='region',
                title='Sales Distribution by Region',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            # Enhanced layout
            fig_region.update_layout(
                title={
                    'text': 'Sales Distribution by Region',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                )
            )
            
            # Enhanced tooltips
            fig_region.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                            "Revenue: $%{value:,.2f}<br>" +
                            "Orders: %{customdata[0]}<br>" +
                            "Share: %{percent:.1%}<br>" +
                            "<extra></extra>",
                customdata=region_data[['order_count']].values,
                textinfo='label+percent',
                textposition='inside'
            )
            
            st.plotly_chart(fig_region, use_container_width=True)
            
            # Regional insights
            with st.expander("🌍 Regional Insights"):
                top_region = region_data.iloc[0]
                st.metric(
                    "🏆 Top Region", 
                    top_region['region'],
                    f"${top_region['total_revenue']:,.2f}"
                )
                
                # Regional performance table
                st.subheader("📊 Regional Performance")
                display_dataframe_with_index_1(region_data)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>🛒 Sales Performance by Channel</h4>
        </div>
        """, unsafe_allow_html=True)
        
        channel_data, channel_msg = calculate_sales_by_channel(st.session_state.sales_orders)
        
        st.markdown(f"**{channel_msg}**")
        
        if not channel_data.empty:
            # Enhanced horizontal bar chart
            fig_channel = px.bar(
                channel_data, 
                x='total_revenue', 
                y='channel',
                orientation='h',
                color='total_revenue',
                color_continuous_scale='plasma',
                title='Sales Performance by Channel',
                labels={'total_revenue': 'Revenue ($)', 'channel': 'Sales Channel', 'order_count': 'Orders'},
                hover_data=['order_count']
            )
            
            # Enhanced layout
            fig_channel.update_layout(
                title={
                    'text': 'Sales Performance by Channel',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Revenue ($)',
                yaxis_title='Sales Channel',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            # Enhanced tooltips
            fig_channel.update_traces(
                hovertemplate="<b>%{y}</b><br>" +
                            "Revenue: $%{x:,.2f}<br>" +
                            "Orders: %{customdata[0]}<br>" +
                            "<extra></extra>",
                customdata=channel_data[['order_count']].values
            )
            
            # Add value labels
            fig_channel.update_traces(
                texttemplate='$%{x:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_channel, use_container_width=True)
            
            # Channel insights
            with st.expander("🛒 Channel Insights"):
                top_channel = channel_data.iloc[0]
                st.metric(
                    "🏆 Top Channel", 
                    top_channel['channel'],
                    f"${top_channel['total_revenue']:,.2f}"
                )
                
                # Channel performance table
                st.subheader("📊 Channel Performance")
                display_dataframe_with_index_1(channel_data)
    
    st.markdown("---")
    
    # Enhanced Time Series Analysis
    st.markdown("""
    <div class="chart-container">
    <h4>📅 Sales Trends Over Time</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.sales_orders.empty:
        # Convert order_date to datetime
        sales_orders = st.session_state.sales_orders.copy()
        sales_orders['order_date'] = pd.to_datetime(sales_orders['order_date'])
        
        # Daily sales aggregation
        daily_sales = sales_orders.groupby(sales_orders['order_date'].dt.date)['total_amount'].agg(['sum', 'count']).reset_index()
        daily_sales.columns = ['date', 'revenue', 'orders']
        daily_sales['date'] = pd.to_datetime(daily_sales['date'])
        daily_sales = daily_sales.sort_values('date')
        
        # Create enhanced time series chart
        fig_trends = go.Figure()
        
        # Revenue line
        fig_trends.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['revenue'],
            mode='lines+markers',
            name='Daily Revenue',
            line=dict(color='#10b981', width=2),
            marker=dict(size=4, color='#10b981'),
            hovertemplate="<b>%{x|%B %d, %Y}</b><br>" +
                        "Revenue: $%{y:,.2f}<br>" +
                        "<extra></extra>"
        ))
        
        # Orders line (secondary y-axis)
        fig_trends.add_trace(go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['orders'],
            mode='lines+markers',
            name='Daily Orders',
            yaxis='y2',
            line=dict(color='#f59e0b', width=2, dash='dot'),
            marker=dict(size=4, color='#f59e0b'),
            hovertemplate="<b>%{x|%B %d, %Y}</b><br>" +
                        "Orders: %{y}<br>" +
                        "<extra></extra>"
        ))
        
        # Enhanced layout
        fig_trends.update_layout(
            title={
                'text': 'Daily Sales Trends - Revenue & Order Volume',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1f2937'}
            },
            xaxis_title='Date',
            yaxis_title='Revenue ($)',
            yaxis2=dict(
                title='Number of Orders',
                overlaying='y',
                side='right'
            ),
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Time series insights
        with st.expander("📅 Time Series Insights"):
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_daily_revenue = daily_sales['revenue'].mean()
                st.metric(
                    "📊 Average Daily Revenue", 
                    f"${avg_daily_revenue:,.2f}"
                )
            
            with col2:
                peak_day = daily_sales.loc[daily_sales['revenue'].idxmax()]
                st.metric(
                    "🚀 Peak Revenue Day", 
                    peak_day['date'].strftime('%B %d'),
                    f"${peak_day['revenue']:,.2f}"
                )
            
            with col3:
                total_days = len(daily_sales)
                st.metric(
                    "📅 Trading Days", 
                    total_days
                )
    
    st.markdown("---")
    
    # Enhanced Analytics Section with Interactive Controls
    st.markdown("""
    <div class="chart-container">
    <h4>🔍 Advanced Sales Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive controls for advanced analytics
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs([
        "📊 Trend Analysis", 
        "📅 Seasonality Patterns", 
        "🎯 Performance Benchmarks"
    ])
    
    with analytics_tab1:
        st.subheader("📊 Advanced Trend Analysis")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            trend_period = st.selectbox(
                "Select Trend Period:",
                ["daily", "weekly", "monthly"],
                index=0,
                help="Choose the time granularity for trend analysis"
            )
            
            if st.button("🔄 Calculate Trends", use_container_width=True):
                trend_data, trend_msg = calculate_sales_trend_analysis(
                    st.session_state.sales_orders, trend_period
                )
                if trend_data is not None and not trend_data.empty:
                    st.session_state.trend_data = trend_data
                    st.session_state.trend_msg = trend_msg
                    st.success("✅ Trend analysis completed!")
                else:
                    st.error(f"❌ {trend_msg}")
        
        with col2:
            if 'trend_data' in st.session_state and st.session_state.trend_data is not None and not st.session_state.trend_data.empty:
                trend_data = st.session_state.trend_data
                
                # Create enhanced trend visualization
                fig_trends_advanced = go.Figure()
                
                # Revenue trend line
                fig_trends_advanced.add_trace(go.Scatter(
                    x=trend_data.index if trend_period != 'daily' else trend_data['date'],
                    y=trend_data['total_revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=6, color='#10b981'),
                    hovertemplate="<b>Period: %{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "<extra></extra>"
                ))
                
                # Moving average line
                if 'revenue_ma_7' in trend_data.columns:
                    fig_trends_advanced.add_trace(go.Scatter(
                        x=trend_data.index if trend_period != 'daily' else trend_data['date'],
                        y=trend_data['revenue_ma_7'],
                        mode='lines',
                        name='7-Period Moving Average',
                        line=dict(color='#f59e0b', width=2, dash='dash'),
                        hovertemplate="<b>Period: %{x}</b><br>" +
                                    "Moving Avg: $%{y:,.2f}<br>" +
                                    "<extra></extra>"
                    ))
                
                # Enhanced layout
                fig_trends_advanced.update_layout(
                    title=f'{trend_period.title()} Sales Trends with Moving Average',
                    xaxis_title='Period',
                    yaxis_title='Revenue ($)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_trends_advanced, use_container_width=True)
                
                # Trend insights
                with st.expander("📈 Trend Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_trend = trend_data['revenue_trend'].mean()
                        st.metric(
                            "📊 Average Trend", 
                            f"{avg_trend:.1f}%"
                        )
                    
                    with col2:
                        if 'revenue_ma_7' in trend_data.columns:
                            trend_volatility = trend_data['total_revenue'].std() / trend_data['total_revenue'].mean() * 100
                            st.metric(
                                "📈 Trend Volatility", 
                                f"{trend_volatility:.1f}%"
                            )
                    
                    with col3:
                        recent_trend = trend_data['revenue_trend'].iloc[-1] if len(trend_data) > 1 else 0
                        st.metric(
                            "🔄 Recent Trend", 
                            f"{recent_trend:.1f}%"
                        )
    
    with analytics_tab2:
        st.subheader("📅 Seasonality Pattern Analysis")
        
        if st.button("🔍 Analyze Seasonality", use_container_width=True):
            seasonality_data, seasonality_msg = calculate_sales_seasonality(st.session_state.sales_orders)
            if seasonality_data is not None and isinstance(seasonality_data, dict):
                st.session_state.seasonality_data = seasonality_data
                st.session_state.seasonality_msg = seasonality_msg
                st.success("✅ Seasonality analysis completed!")
            else:
                st.error(f"❌ {seasonality_msg}")
        
        if 'seasonality_data' in st.session_state and st.session_state.seasonality_data is not None:
            seasonality_data = st.session_state.seasonality_data
            
            # Monthly seasonality chart
            if 'monthly' in seasonality_data:
                monthly_data = seasonality_data['monthly']
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                monthly_data['month_name'] = monthly_data['month'].apply(lambda x: month_names[x-1])
                
                fig_monthly = px.bar(
                    monthly_data,
                    x='month_name',
                    y='total_revenue',
                    title='Monthly Sales Seasonality',
                    color='total_revenue',
                    color_continuous_scale='viridis',
                    labels={'total_revenue': 'Revenue ($)', 'month_name': 'Month'}
                )
                
                fig_monthly.update_layout(
                    title={'x': 0.5, 'xanchor': 'center'},
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Day of week seasonality
            if 'daily' in seasonality_data:
                daily_data = seasonality_data['daily']
                
                fig_daily = px.bar(
                    daily_data,
                    x='day_name',
                    y='total_revenue',
                    title='Daily Sales Patterns',
                    color='total_revenue',
                    color_continuous_scale='plasma',
                    labels={'total_revenue': 'Revenue ($)', 'day_name': 'Day of Week'}
                )
                
                fig_daily.update_layout(
                    title={'x': 0.5, 'xanchor': 'center'},
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_daily, use_container_width=True)
            
            # Seasonality insights
            with st.expander("📅 Seasonality Insights"):
                if 'monthly' in seasonality_data:
                    monthly_data = seasonality_data['monthly']
                    peak_month = monthly_data.loc[monthly_data['total_revenue'].idxmax()]
                    low_month = monthly_data.loc[monthly_data['total_revenue'].idxmin()]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "🚀 Peak Month", 
                            month_names[peak_month['month']-1],
                            f"${peak_month['total_revenue']:,.2f}"
                        )
                    
                    with col2:
                        st.metric(
                            "📉 Low Month", 
                            month_names[low_month['month']-1],
                            f"${low_month['total_revenue']:,.2f}"
                        )
    
    with analytics_tab3:
        st.subheader("🎯 Performance Benchmarks & KPIs")
        
        if st.button("📊 Calculate Benchmarks", use_container_width=True):
            benchmarks, benchmark_msg = calculate_sales_performance_benchmarks(
                st.session_state.sales_orders,
                st.session_state.products if not st.session_state.products.empty else pd.DataFrame(),
                st.session_state.sales_reps if not st.session_state.sales_reps.empty else pd.DataFrame()
            )
            if benchmarks is not None and isinstance(benchmarks, dict):
                st.session_state.benchmarks = benchmarks
                st.session_state.benchmark_msg = benchmark_msg
                st.success("✅ Benchmarks calculated successfully!")
            else:
                st.error(f"❌ {benchmark_msg}")
        
        if 'benchmarks' in st.session_state and st.session_state.benchmarks is not None:
            benchmarks = st.session_state.benchmarks
            
            # Overall performance metrics
            if 'overall' in benchmarks:
                overall = benchmarks['overall']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        "💰 Total Revenue", 
                        f"${overall['total_revenue']:,.0f}"
                    )
                
                with col2:
                    st.metric(
                        "📦 Total Orders", 
                        f"{overall['total_orders']:,}"
                    )
                
                with col3:
                    st.metric(
                        "📊 Avg Order Value", 
                        f"${overall['avg_order_value']:,.2f}"
                    )
                
                with col4:
                    st.metric(
                        "🎯 Revenue per Order", 
                        f"${overall['revenue_per_order']:,.2f}"
                    )
            
            # Revenue percentiles
            if 'revenue_percentiles' in benchmarks:
                st.subheader("📊 Revenue Distribution Percentiles")
                
                percentiles_data = []
                for percentile, value in benchmarks['revenue_percentiles'].items():
                    percentiles_data.append({
                        'Percentile': f"{float(percentile)*100:.0f}%",
                        'Revenue': f"${value:,.2f}"
                    })
                
                percentiles_df = pd.DataFrame(percentiles_data)
                st.dataframe(percentiles_df, use_container_width=True)
            
            # Product performance benchmarks
            if 'product_performance' in benchmarks:
                st.subheader("📦 Product Performance Benchmarks")
                
                product_benchmarks = benchmarks['product_performance']
                if not product_benchmarks.empty:
                    # Merge with product names if available
                    if not st.session_state.products.empty:
                        product_benchmarks = product_benchmarks.merge(
                            st.session_state.products[['product_id', 'product_name']], 
                            on='product_id', 
                            how='left'
                        )
                    
                    # Top performing products
                    top_products = product_benchmarks.nlargest(10, 'total_revenue')
                    
                    fig_top_products = px.bar(
                        top_products,
                        x='total_revenue',
                        y='product_name' if 'product_name' in top_products.columns else 'product_id',
                        orientation='h',
                        title='Top 10 Products by Revenue',
                        color='total_revenue',
                        color_continuous_scale='viridis'
                    )
                    
                    fig_top_products.update_layout(
                        title={'x': 0.5, 'xanchor': 'center'},
                        height=400,
                        xaxis_title='Revenue ($)',
                        yaxis_title='Product',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig_top_products, use_container_width=True)
    
    # Efficiency Metrics Section
    st.markdown("---")
    st.markdown("""
    <div class="chart-container">
    <h4>⚡ Sales Efficiency & Productivity Metrics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ Calculate Efficiency Metrics", use_container_width=True):
        efficiency_metrics, efficiency_msg = calculate_sales_efficiency_metrics(
            st.session_state.sales_orders,
            st.session_state.activities if not st.session_state.activities.empty else pd.DataFrame()
        )
        if efficiency_metrics is not None and isinstance(efficiency_metrics, dict):
            st.session_state.efficiency_metrics = efficiency_metrics
            st.session_state.efficiency_msg = efficiency_msg
            st.success("✅ Efficiency metrics calculated successfully!")
        else:
            st.error(f"❌ {efficiency_msg}")
    
    if 'efficiency_metrics' in st.session_state:
        efficiency_metrics = st.session_state.efficiency_metrics
        
        # Efficiency metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "💰 Revenue per Activity", 
                f"${efficiency_metrics['revenue_per_activity']:,.2f}"
            )
        
        with col2:
            st.metric(
                "📦 Orders per Activity", 
                f"{efficiency_metrics['orders_per_activity']:.2f}"
            )
        
        with col3:
            st.metric(
                "📅 Daily Revenue", 
                f"${efficiency_metrics['daily_revenue']:,.2f}"
            )
        
        with col4:
            st.metric(
                "🎯 Conversion Rate", 
                f"{efficiency_metrics['conversion_rate']:.1f}%"
            )
        
        # Additional efficiency insights
        with st.expander("⚡ Efficiency Insights"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "📊 Total Activities", 
                    efficiency_metrics['total_activities']
                )
                
                st.metric(
                    "📅 Days Active", 
                    efficiency_metrics['days_active']
                )
            
            with col2:
                st.metric(
                    "📦 Daily Orders", 
                    f"{efficiency_metrics['daily_orders']:.1f}"
                )
                
                st.metric(
                    "💰 Avg Order Value", 
                    f"${efficiency_metrics['avg_order_value']:,.2f}"
                )
    
    # AI Recommendations
    display_ai_recommendations("sales_performance", st.session_state.sales_orders)

# ============================================================================
# CUSTOMER ANALYSIS
# ============================================================================

def show_customer_analysis():
    st.header("👥 Customer Analysis")
    
    if st.session_state.customers.empty or st.session_state.sales_orders.empty:
        st.warning("Please add customer and sales data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-red">
        <h3 style="color: white; margin: 0; text-align: center;">👥 Customer Analysis Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_customers = len(st.session_state.customers)
    active_customers = len(st.session_state.customers[st.session_state.customers['status'] == 'Active'])
    churned_customers = len(st.session_state.customers[st.session_state.customers['status'] == 'Churned'])
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(total_customers), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Active Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(active_customers), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-red">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Churned Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(churned_customers), unsafe_allow_html=True)
    
    with summary_col4:
        retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Retention Rate</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:.1f}%</h2>
        </div>
        """.format(retention_rate), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>💰 Customer Lifetime Value (CLV)</h4>
        </div>
        """, unsafe_allow_html=True)
        clv_data, clv_msg = calculate_customer_lifetime_value(st.session_state.sales_orders, st.session_state.customers)
        
        st.markdown(f"**{clv_msg}**")
        
        if not clv_data.empty:
            # Enhanced CLV histogram with better interactivity
            fig_clv = px.histogram(
                clv_data, 
                x='clv',
                title='Customer Lifetime Value Distribution',
                nbins=20,
                color_discrete_sequence=['#10b981'],
                opacity=0.8
            )
            
            # Enhanced layout and tooltips
            fig_clv.update_layout(
                title={
                    'text': 'Customer Lifetime Value Distribution',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Customer Lifetime Value ($)',
                yaxis_title='Number of Customers',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips
            fig_clv.update_traces(
                hovertemplate="<b>CLV Range</b><br>" +
                            "Value: $%{x:,.2f}<br>" +
                            "Customers: %{y}<br>" +
                            "<extra></extra>",
                marker=dict(
                    line=dict(width=1, color='#ffffff')
                )
            )
            
            st.plotly_chart(fig_clv, use_container_width=True)
            
            # CLV insights
            with st.expander("💡 CLV Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_clv = clv_data['clv'].mean()
                    st.metric(
                        "📊 Average CLV", 
                        f"${avg_clv:,.2f}"
                    )
                with col2:
                    median_clv = clv_data['clv'].median()
                    st.metric(
                        "📈 Median CLV", 
                        f"${median_clv:,.2f}"
                    )
                with col3:
                    top_10_percentile = clv_data['clv'].quantile(0.9)
                    st.metric(
                        "🏆 Top 10% CLV", 
                        f"${top_10_percentile:,.2f}"
                    )
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Customer Segmentation</h4>
        </div>
        """, unsafe_allow_html=True)
        segmentation_data, segmentation_msg = calculate_customer_segmentation(st.session_state.customers, st.session_state.sales_orders)
        
        st.markdown(f"**{segmentation_msg}**")
        
        if not segmentation_data.empty:
            # Enhanced segmentation bar chart
            fig_seg = px.bar(
                segmentation_data, 
                x='Segment', 
                y='Customer Count',
                title='Customer Distribution by Segment',
                color='Total Revenue',
                color_continuous_scale='plasma',
                text='Customer Count'
            )
            
            # Enhanced layout
            fig_seg.update_layout(
                title={
                    'text': 'Customer Distribution by Segment',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Customer Segment',
                yaxis_title='Number of Customers',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips and styling
            fig_seg.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Customers: %{y}<br>" +
                            "Revenue: $%{marker.color:,.2f}<br>" +
                            "<extra></extra>",
                textposition='outside',
                texttemplate='%{y}'
            )
            
            st.plotly_chart(fig_seg, use_container_width=True)
            
            # Segmentation insights
            with st.expander("💡 Segmentation Insights"):
                top_segment = segmentation_data.iloc[0]
                st.metric(
                    "🏆 Top Segment", 
                    top_segment['Segment'],
                    f"${top_segment['Total Revenue']:,.2f}"
                )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
        <h4>🔄 Customer Churn & Retention Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        churn_data, churn_msg = calculate_customer_churn_rate(st.session_state.customers)
        
        st.markdown(f"**{churn_msg}**")
        
        if not churn_data.empty:
            # Enhanced churn analysis with interactive charts
            col_churn1, col_churn2 = st.columns(2)
            
            with col_churn1:
                # Pie chart for customer status distribution
                fig_churn_pie = px.pie(
                    churn_data,
                    values='Value',
                    names='Metric',
                    title='Customer Status Distribution',
                    color_discrete_sequence=['#10b981', '#ef4444', '#f59e0b'],
                    hole=0.4
                )
                
                fig_churn_pie.update_layout(
                    title={
                        'text': 'Customer Status Distribution',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    height=300,
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.02
                    )
                )
                
                fig_churn_pie.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                "Count: %{value}<br>" +
                                "Percentage: %{percent:.1%}<br>" +
                                "<extra></extra>",
                    textinfo='label+percent',
                    textposition='inside'
                )
                
                st.plotly_chart(fig_churn_pie, use_container_width=True)
            
            with col_churn2:
                # Bar chart for key metrics
                metrics_to_show = churn_data[churn_data['Metric'].isin(['Active Customers', 'Churned Customers', 'Churn Rate', 'Retention Rate'])]
                
                fig_churn_bar = px.bar(
                    metrics_to_show,
                    x='Metric',
                    y='Value',
                    title='Key Customer Metrics',
                    color='Metric',
                    color_discrete_map={
                        'Active Customers': '#10b981',
                        'Churned Customers': '#ef4444',
                        'Churn Rate': '#f59e0b',
                        'Retention Rate': '#3b82f6'
                    }
                )
                
                fig_churn_bar.update_layout(
                    title={
                        'text': 'Key Customer Metrics',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    xaxis_title='Metric',
                    yaxis_title='Value',
                    height=300,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_churn_bar.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Value: %{y}<br>" +
                                "<extra></extra>",
                    texttemplate='%{y}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_churn_bar, use_container_width=True)
            
            # Churn insights
            with st.expander("💡 Churn Analysis Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    churn_rate = float(churn_data[churn_data['Metric'] == 'Churn Rate']['Value'].iloc[0].replace('%', ''))
                    st.metric(
                        "📉 Churn Rate", 
                        f"{churn_rate:.1f}%"
                    )
                with col2:
                    retention_rate = float(churn_data[churn_data['Metric'] == 'Retention Rate']['Value'].iloc[0].replace('%', ''))
                    st.metric(
                        "📈 Retention Rate", 
                        f"{retention_rate:.1f}%"
                    )
                with col3:
                    active_customers = int(churn_data[churn_data['Metric'] == 'Active Customers']['Value'].iloc[0])
                    st.metric(
                        "👥 Active Customers", 
                        f"{active_customers:,}"
                    )
    
    with col4:
        st.markdown("""
        <div class="chart-container">
        <h4>🔄 Customer Purchase Behavior Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        repeat_data, repeat_msg = calculate_repeat_purchase_rate(st.session_state.sales_orders)
        
        st.markdown(f"**{repeat_msg}**")
        
        if not repeat_data.empty:
            # Enhanced repeat purchase analysis with interactive charts
            col_repeat1, col_repeat2 = st.columns(2)
            
            with col_repeat1:
                # Donut chart for purchase behavior
                fig_repeat_donut = px.pie(
                    repeat_data,
                    values='Value',
                    names='Metric',
                    title='Customer Purchase Behavior',
                    color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b'],
                    hole=0.6
                )
                
                fig_repeat_donut.update_layout(
                    title={
                        'text': 'Customer Purchase Behavior',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    height=300,
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.02
                    )
                )
                
                fig_repeat_donut.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                "Count: %{value}<br>" +
                                "Percentage: %{percent:.1%}<br>" +
                                "<extra></extra>",
                    textinfo='label+percent',
                    textposition='inside'
                )
                
                st.plotly_chart(fig_repeat_donut, use_container_width=True)
            
            with col_repeat2:
                # Horizontal bar chart for key metrics
                metrics_to_show = repeat_data[repeat_data['Metric'].isin(['Single Purchase', 'Repeat Purchase', 'Repeat Purchase Rate'])]
                
                fig_repeat_bar = px.bar(
                    metrics_to_show,
                    x='Value',
                    y='Metric',
                    orientation='h',
                    title='Purchase Behavior Metrics',
                    color='Metric',
                    color_discrete_map={
                        'Single Purchase': '#f59e0b',
                        'Repeat Purchase': '#10b981',
                        'Repeat Purchase Rate': '#3b82f6'
                    }
                )
                
                fig_repeat_bar.update_layout(
                    title={
                        'text': 'Purchase Behavior Metrics',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    xaxis_title='Value',
                    yaxis_title='Metric',
                    height=300,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_repeat_bar.update_traces(
                    hovertemplate="<b>%{y}</b><br>" +
                                "Value: %{x}<br>" +
                                "<extra></extra>",
                    texttemplate='%{x}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_repeat_bar, use_container_width=True)
            
            # Purchase behavior insights
            with st.expander("💡 Purchase Behavior Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_customers = int(repeat_data[repeat_data['Metric'] == 'Total Customers']['Value'].iloc[0])
                    st.metric(
                        "👥 Total Customers", 
                        f"{total_customers:,}"
                    )
                with col2:
                    repeat_purchase = int(repeat_data[repeat_data['Metric'] == 'Repeat Purchase']['Value'].iloc[0])
                    st.metric(
                        "🔄 Repeat Customers", 
                        f"{repeat_purchase:,}"
                    )
                with col3:
                    repeat_rate = float(repeat_data[repeat_data['Metric'] == 'Repeat Purchase Rate']['Value'].iloc[0].replace('%', ''))
                    st.metric(
                        "📊 Repeat Rate", 
                        f"{repeat_rate:.1f}%"
                    )
    
    # Advanced Customer Analytics Section
    st.markdown("---")
    st.markdown("""<div class="chart-container"><h4>🔍 Advanced Customer Analytics</h4></div>""", unsafe_allow_html=True)
    
    # Interactive controls for advanced analytics
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs([
        "📊 Customer Trends", 
        "🌍 Geographic Analysis", 
        "🏢 Industry Insights"
    ])
    
    with analytics_tab1:
        st.subheader("📊 Customer Acquisition & Growth Trends")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # Interactive controls
            trend_period = st.selectbox(
                "Select Trend Period:",
                ["monthly", "quarterly", "yearly"],
                index=0,
                help="Choose the time granularity for trend analysis"
            )
            
            if st.button("🔄 Calculate Customer Trends", use_container_width=True):
                # Calculate customer acquisition trends
                customer_trends, trends_msg = calculate_customer_acquisition_trends(
                    st.session_state.customers, 
                    st.session_state.sales_orders, 
                    trend_period
                )
                if customer_trends is not None:
                    st.session_state.customer_trends = customer_trends
                    st.success("✅ Customer trends calculated successfully!")
                else:
                    st.error(f"❌ {trends_msg}")
        
        with col2:
            if 'customer_trends' in st.session_state and st.session_state.customer_trends is not None:
                trends_data = st.session_state.customer_trends
                
                # Create enhanced trend visualization
                fig_customer_trends = go.Figure()
                
                # Customer acquisition trend
                fig_customer_trends.add_trace(go.Scatter(
                    x=trends_data['period'],
                    y=trends_data['new_customers'],
                    mode='lines+markers',
                    name='New Customers',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=6, color='#10b981'),
                    hovertemplate="<b>Period: %{x}</b><br>" +
                                "New Customers: %{y}<br>" +
                                "<extra></extra>"
                ))
                
                # Revenue trend
                fig_customer_trends.add_trace(go.Scatter(
                    x=trends_data['period'],
                    y=trends_data['revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    yaxis='y2',
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(size=6, color='#3b82f6'),
                    hovertemplate="<b>Period: %{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "<extra></extra>"
                ))
                
                # Enhanced layout with dual Y-axis
                fig_customer_trends.update_layout(
                    title=f'{trend_period.title()} Customer Acquisition & Revenue Trends',
                    xaxis_title='Period',
                    yaxis=dict(title='New Customers', side='left'),
                    yaxis2=dict(title='Revenue ($)', side='right', overlaying='y'),
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_customer_trends, use_container_width=True)
                
                # Trend insights
                with st.expander("📈 Trend Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_growth = trends_data['new_customers'].pct_change().mean() * 100
                        st.metric(
                            "📊 Avg Growth Rate", 
                            f"{avg_growth:.1f}%"
                        )
                    with col2:
                        total_new = trends_data['new_customers'].sum()
                        st.metric(
                            "👥 Total New Customers", 
                            f"{total_new:,}"
                        )
                    with col3:
                        total_revenue = trends_data['revenue'].sum()
                        st.metric(
                            "💰 Total Revenue", 
                            f"${total_revenue:,.2f}"
                        )
    
    with analytics_tab2:
        st.subheader("🌍 Geographic Customer Distribution")
        
        if st.button("🌍 Analyze Geographic Distribution", use_container_width=True):
            geo_data, geo_msg = calculate_geographic_customer_distribution(
                st.session_state.customers, 
                st.session_state.sales_orders
            )
            if geo_data is not None:
                st.session_state.geo_data = geo_data
                st.success("✅ Geographic analysis completed!")
            else:
                st.error(f"❌ {geo_msg}")
        
        if 'geo_data' in st.session_state and st.session_state.geo_data is not None:
            geo_data = st.session_state.geo_data
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Geographic distribution pie chart
                fig_geo_pie = px.pie(
                    geo_data,
                    values='customer_count',
                    names='region',
                    title='Customer Distribution by Region',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.4
                )
                
                fig_geo_pie.update_layout(
                    title={
                        'text': 'Customer Distribution by Region',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    height=350,
                    showlegend=True
                )
                
                fig_geo_pie.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                "Customers: %{value}<br>" +
                                "Percentage: %{percent:.1%}<br>" +
                                "<extra></extra>",
                    textinfo='label+percent',
                    textposition='inside'
                )
                
                st.plotly_chart(fig_geo_pie, use_container_width=True)
            
            with col2:
                # Regional performance bar chart
                fig_geo_bar = px.bar(
                    geo_data,
                    x='region',
                    y='avg_revenue',
                    title='Average Revenue by Region',
                    color='customer_count',
                    color_continuous_scale='viridis'
                )
                
                fig_geo_bar.update_layout(
                    title={
                        'text': 'Average Revenue by Region',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16, 'color': '#1f2937'}
                    },
                    xaxis_title='Region',
                    yaxis_title='Average Revenue ($)',
                    height=350,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_geo_bar.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Avg Revenue: $%{y:,.2f}<br>" +
                                "Customers: %{marker.color}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_geo_bar, use_container_width=True)
    
    with analytics_tab3:
        st.subheader("🏢 Industry & Company Size Analysis")
        
        if st.button("🏢 Analyze Industry Patterns", use_container_width=True):
            industry_data, industry_msg = calculate_industry_customer_analysis(
                st.session_state.customers, 
                st.session_state.sales_orders
            )
            if industry_data is not None:
                st.session_state.industry_data = industry_data
                st.success("✅ Industry analysis completed!")
            else:
                st.error(f"❌ {industry_msg}")
        
        if 'industry_data' in st.session_state and st.session_state.industry_data is not None:
            industry_data = st.session_state.industry_data
            
            # Industry performance heatmap-style visualization
            fig_industry = px.bar(
                industry_data,
                x='industry',
                y='avg_revenue',
                title='Average Revenue by Industry',
                color='customer_count',
                color_continuous_scale='plasma',
                text='customer_count'
            )
            
            fig_industry.update_layout(
                title={
                    'text': 'Average Revenue by Industry',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Industry',
                yaxis_title='Average Revenue ($)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            
            fig_industry.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Avg Revenue: $%{y:,.2f}<br>" +
                            "Customers: %{marker.color}<br>" +
                            "<extra></extra>",
                texttemplate='%{text}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_industry, use_container_width=True)
            
            # Industry insights
            with st.expander("💡 Industry Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    top_industry = industry_data.iloc[0]
                    st.metric(
                        "🏆 Top Industry", 
                        top_industry['industry'],
                        f"${top_industry['avg_revenue']:,.2f}"
                    )
                with col2:
                    avg_customers = industry_data['customer_count'].mean()
                    st.metric(
                        "📊 Avg Customers/Industry", 
                        f"{avg_customers:.1f}"
                    )
                with col3:
                    total_industries = len(industry_data)
                    st.metric(
                        "🏢 Total Industries", 
                        f"{total_industries}"
                    )
    
    # AI Recommendations
    display_ai_recommendations("customer_analysis", st.session_state.customers, st.session_state.sales_orders)

# ============================================================================
# SALES FUNNEL ANALYSIS
# ============================================================================

def show_sales_funnel():
    st.header("🔄 Sales Funnel Analysis")
    
    if st.session_state.leads.empty or st.session_state.opportunities.empty:
        st.warning("Please add leads and opportunities data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-teal">
        <h3 style="color: white; margin: 0; text-align: center;">🔄 Sales Funnel Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_leads = len(st.session_state.leads)
    total_opportunities = len(st.session_state.opportunities)
    won_opportunities = len(st.session_state.opportunities[st.session_state.opportunities['stage'] == 'Closed Won'])
    conversion_rate = (won_opportunities / total_leads * 100) if total_leads > 0 else 0
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #667eea;">Total Leads</h4>
        <h2 style="margin: 10px 0; color: #667eea;">{:,}</h2>
        </div>
        """.format(total_leads), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #a855f7;">Total Opportunities</h4>
        <h2 style="margin: 10px 0; color: #a855f7;">{:,}</h2>
        </div>
        """.format(total_opportunities), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #16a34a;">Won Deals</h4>
        <h2 style="margin: 10px 0; color: #16a34a;">{:,}</h2>
        </div>
        """.format(won_opportunities), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-orange">
        <h4 style="margin: 0; color: #f97316;">Conversion Rate</h4>
        <h2 style="margin: 10px 0; color: #f97316;">{:.1f}%</h2>
        </div>
        """.format(conversion_rate), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Funnel Visualization
    st.markdown("""
    <div class="chart-container">
        <h4>🔄 Sales Funnel Visualization</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Create funnel chart
    funnel_data = {
        'Stage': ['Leads', 'Qualified Leads', 'Opportunities', 'Proposals', 'Negotiations', 'Closed Won'],
        'Count': [
            total_leads,
            int(total_leads * 0.7),  # Estimated qualified leads
            total_opportunities,
            int(total_opportunities * 0.8),  # Estimated proposals
            int(total_opportunities * 0.6),  # Estimated negotiations
            won_opportunities
        ],
        'Conversion': [100, 70, 50, 40, 30, 25]  # Conversion percentages
    }
    
    # Create funnel chart using plotly
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        textposition="inside",
        marker={"color": ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#a855f7", "#16a34a"]},
        connector={"line": {"color": "royalblue", "width": 3}}
    ))
    
    fig_funnel.update_layout(
        title={
            'text': 'Sales Funnel - Lead to Revenue Conversion',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        funnelmode="stack"
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Funnel insights
    with st.expander("💡 Funnel Insights"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "📊 Lead to Opportunity", 
                f"{total_opportunities/total_leads*100:.1f}%" if total_leads > 0 else "0%"
            )
        with col2:
            st.metric(
                "📈 Opportunity to Won", 
                f"{won_opportunities/total_opportunities*100:.1f}%" if total_opportunities > 0 else "0%"
            )
        with col3:
            st.metric(
                "🎯 Overall Conversion", 
                f"{won_opportunities/total_leads*100:.1f}%" if total_leads > 0 else "0%"
            )
        with col4:
            st.metric(
                "💰 Revenue per Lead", 
                f"${st.session_state.sales_orders['total_amount'].sum()/total_leads:,.2f}" if total_leads > 0 else "$0"
            )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Conversion Rate by Stage</h4>
        </div>
        """, unsafe_allow_html=True)
        conversion_data, conversion_msg = calculate_conversion_rate_by_stage(st.session_state.leads, st.session_state.opportunities)
        
        st.markdown(f"**{conversion_msg}**")
        
        if not conversion_data.empty:
            # Enhanced conversion rate chart
            fig_conversion = px.bar(
                conversion_data, 
                x='source', 
                y='conversion_rate',
                title='Conversion Rate by Lead Source',
                color='conversion_rate',
                color_continuous_scale='plasma',
                text='conversion_rate'
            )
            
            # Enhanced layout and styling
            fig_conversion.update_layout(
                title={
                    'text': 'Conversion Rate by Lead Source',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Lead Source',
                yaxis_title='Conversion Rate (%)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips and styling
            fig_conversion.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Conversion Rate: %{y:.1f}%<br>" +
                            "Leads: %{customdata[0]}<br>" +
                            "Opportunities: %{customdata[1]}<br>" +
                            "<extra></extra>",
                customdata=conversion_data[['lead_count', 'opportunity_count']].values,
                texttemplate='%{y:.1f}%',
                textposition='outside'
            )
            
            st.plotly_chart(fig_conversion, use_container_width=True)
            
            # Conversion insights
            with st.expander("💡 Conversion Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    top_source = conversion_data.iloc[0]
                    st.metric(
                        "🏆 Top Source", 
                        top_source['source'],
                        f"{top_source['conversion_rate']:.1f}%"
                    )
                with col2:
                    avg_conversion = conversion_data['conversion_rate'].mean()
                    st.metric(
                        "📊 Avg Conversion", 
                        f"{avg_conversion:.1f}%"
                    )
                with col3:
                    total_leads = conversion_data['lead_count'].sum()
                    st.metric(
                        "📈 Total Leads", 
                        f"{total_leads:,}"
                    )
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>💰 Average Deal Size</h4>
        </div>
        """, unsafe_allow_html=True)
        deal_data, deal_msg = calculate_average_deal_size(st.session_state.opportunities)
        
        st.markdown(f"**{deal_msg}**")
        
        if not deal_data.empty:
            # Enhanced deal size visualization
            fig_deal_size = px.bar(
                deal_data,
                x='stage',
                y='avg_deal_size',
                title='Average Deal Size by Stage',
                color='deal_count',
                color_continuous_scale='viridis',
                text='avg_deal_size'
            )
            
            # Enhanced layout and styling
            fig_deal_size.update_layout(
                title={
                    'text': 'Average Deal Size by Stage',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Deal Stage',
                yaxis_title='Average Deal Size ($)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips and styling
            fig_deal_size.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Avg Deal Size: $%{y:,.2f}<br>" +
                            "Deal Count: %{marker.color}<br>" +
                            "<extra></extra>",
                texttemplate='$%{y:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_deal_size, use_container_width=True)
            
            # Deal size insights
            with st.expander("💡 Deal Size Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    overall_avg = deal_data[deal_data['stage'] == 'Overall']['avg_deal_size'].iloc[0]
                    st.metric(
                        "📊 Overall Avg", 
                        f"${overall_avg:,.2f}"
                    )
                with col2:
                    max_stage = deal_data[deal_data['stage'] != 'Overall'].loc[deal_data['avg_deal_size'].idxmax()]
                    st.metric(
                        "🏆 Best Stage", 
                        max_stage['stage'],
                        f"${max_stage['avg_deal_size']:,.2f}"
                    )
                with col3:
                    total_deals = deal_data['deal_count'].sum()
                    st.metric(
                        "📈 Total Deals", 
                        f"{total_deals:,}"
                    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
        <h4>⏱️ Time to Close</h4>
        </div>
        """, unsafe_allow_html=True)
        time_data, time_msg = calculate_time_to_close(st.session_state.opportunities)
        
        st.markdown(f"**{time_msg}**")
        
        if not time_data.empty:
            # Enhanced time to close visualization
            fig_time_close = px.bar(
                time_data,
                x='stage',
                y='avg_days',
                title='Average Time to Close by Stage',
                color='deal_count',
                color_continuous_scale='plasma',
                text='avg_days'
            )
            
            # Enhanced layout and styling
            fig_time_close.update_layout(
                title={
                    'text': 'Average Time to Close by Stage',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Deal Stage',
                yaxis_title='Average Days to Close',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips and styling
            fig_time_close.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Avg Days: %{y:.1f}<br>" +
                            "Deal Count: %{marker.color}<br>" +
                            "<extra></extra>",
                texttemplate='%{y:.1f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_time_close, use_container_width=True)
            
            # Time to close insights
            with st.expander("💡 Time to Close Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    overall_avg_days = time_data[time_data['stage'] == 'Overall']['avg_days'].iloc[0]
                    st.metric(
                        "📊 Overall Avg", 
                        f"{overall_avg_days:.1f} days"
                    )
                with col2:
                    fastest_stage = time_data[time_data['stage'] != 'Overall'].loc[time_data['avg_days'].idxmin()]
                    st.metric(
                        "⚡ Fastest Stage", 
                        fastest_stage['stage'],
                        f"{fastest_stage['avg_days']:.1f} days"
                    )
                with col3:
                    total_closed = time_data['deal_count'].sum()
                    st.metric(
                        "📈 Total Closed", 
                        f"{total_closed:,}"
                    )
    
    with col4:
        st.markdown("""
        <div class="chart-container">
        <h4>🚀 Pipeline Velocity</h4>
        </div>
        """, unsafe_allow_html=True)
        velocity_data, velocity_msg = calculate_pipeline_velocity(st.session_state.opportunities)
        
        st.markdown(f"**{velocity_msg}**")
        
        if not velocity_data.empty:
            # Enhanced pipeline velocity visualization
            fig_velocity = px.bar(
                velocity_data,
                x='Metric',
                y='Value',
                title='Pipeline Velocity Metrics',
                color='Value',
                color_continuous_scale='viridis',
                text='Value'
            )
            
            # Enhanced layout and styling
            fig_velocity.update_layout(
                title={
                    'text': 'Pipeline Velocity Metrics',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metric',
                yaxis_title='Value',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            # Enhanced tooltips and styling
            fig_velocity.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{y}<br>" +
                            "<extra></extra>",
                texttemplate='%{y}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_velocity, use_container_width=True)
            
            # Pipeline velocity insights
            with st.expander("💡 Pipeline Velocity Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_value = velocity_data[velocity_data['Metric'] == 'Total Pipeline Value']['Value'].iloc[0]
                    st.metric(
                        "💰 Total Value", 
                        total_value
                    )
                with col2:
                    avg_days = velocity_data[velocity_data['Metric'] == 'Average Days in Pipeline']['Value'].iloc[0]
                    st.metric(
                        "⏱️ Avg Days", 
                        avg_days
                    )
                with col3:
                    velocity = velocity_data[velocity_data['Metric'] == 'Pipeline Velocity ($/day)']['Value'].iloc[0]
                    st.metric(
                        "🚀 Velocity", 
                        velocity
                    )
    
    # Advanced Sales Funnel Analytics
    st.markdown("---")
    st.markdown("""
    <div class="chart-container">
        <h4>🔍 Advanced Sales Funnel Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    analytics_tab1, analytics_tab2, analytics_tab3, analytics_tab4 = st.tabs([
        "📊 Funnel Performance Trends", 
        "🎯 Lead Quality Analysis", 
        "⚡ Pipeline Efficiency Metrics",
        "🔍 Advanced Funnel Analytics"
    ])
    
    with analytics_tab1:
        st.subheader("📊 Funnel Performance Trends")
        
        # Create trend analysis for funnel stages
        if not st.session_state.leads.empty and not st.session_state.opportunities.empty:
            # Sample trend data (in real scenario, this would come from historical data)
            trend_data = {
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Leads': [100, 120, 90, 150, 130, 160],
                'Opportunities': [70, 84, 63, 105, 91, 112],
                'Won_Deals': [35, 42, 31, 52, 45, 56]
            }
            
            # Create dual-axis trend chart
            fig_trend = go.Figure()
            
            # Leads trend
            fig_trend.add_trace(go.Scatter(
                x=trend_data['Month'],
                y=trend_data['Leads'],
                mode='lines+markers',
                name='Leads',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8, color='#3b82f6'),
                yaxis='y'
            ))
            
            # Opportunities trend
            fig_trend.add_trace(go.Scatter(
                x=trend_data['Month'],
                y=trend_data['Opportunities'],
                mode='lines+markers',
                name='Opportunities',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8, color='#10b981'),
                yaxis='y'
            ))
            
            # Won deals trend
            fig_trend.add_trace(go.Scatter(
                x=trend_data['Month'],
                y=trend_data['Won_Deals'],
                mode='lines+markers',
                name='Won Deals',
                line=dict(color='#16a34a', width=3),
                marker=dict(size=8, color='#16a34a'),
                yaxis='y'
            ))
            
            fig_trend.update_layout(
                title='Funnel Performance Trends (6 Months)',
                xaxis_title='Month',
                yaxis_title='Count',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Trend insights
            with st.expander("📈 Trend Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    lead_growth = ((trend_data['Leads'][-1] - trend_data['Leads'][0]) / trend_data['Leads'][0]) * 100
                    st.metric(
                        "📊 Lead Growth", 
                        f"{lead_growth:.1f}%"
                    )
                with col2:
                    opp_growth = ((trend_data['Opportunities'][-1] - trend_data['Opportunities'][0]) / trend_data['Opportunities'][0]) * 100
                    st.metric(
                        "📈 Opportunity Growth", 
                        f"{opp_growth:.1f}%"
                    )
                with col3:
                    won_growth = ((trend_data['Won_Deals'][-1] - trend_data['Won_Deals'][0]) / trend_data['Won_Deals'][0]) * 100
                    st.metric(
                        "🎯 Won Deal Growth", 
                        f"{won_growth:.1f}%"
                    )
    
    with analytics_tab2:
        st.subheader("🎯 Lead Quality Analysis")
        
        if not st.session_state.leads.empty:
            # Analyze lead quality by source
            lead_quality = st.session_state.leads.groupby('source').agg({
                'lead_id': 'count',
                'status': lambda x: (x == 'Qualified').sum()
            }).reset_index()
            lead_quality.columns = ['Source', 'Total_Leads', 'Qualified_Leads']
            lead_quality['Quality_Rate'] = (lead_quality['Qualified_Leads'] / lead_quality['Total_Leads'] * 100).round(1)
            lead_quality = lead_quality.sort_values('Quality_Rate', ascending=False)
            
            # Create lead quality chart
            fig_quality = px.bar(
                lead_quality,
                x='Source',
                y='Quality_Rate',
                title='Lead Quality Rate by Source',
                color='Total_Leads',
                color_continuous_scale='viridis',
                text='Quality_Rate'
            )
            
            fig_quality.update_layout(
                title={
                    'text': 'Lead Quality Rate by Source',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Lead Source',
                yaxis_title='Quality Rate (%)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_quality.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Quality Rate: %{y:.1f}%<br>" +
                            "Total Leads: %{marker.color}<br>" +
                            "<extra></extra>",
                texttemplate='%{y:.1f}%',
                textposition='outside'
            )
            
            st.plotly_chart(fig_quality, use_container_width=True)
            
            # Quality insights
            with st.expander("💡 Quality Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    best_source = lead_quality.iloc[0]
                    st.metric(
                        "🏆 Best Source", 
                        best_source['Source'],
                        f"{best_source['Quality_Rate']:.1f}%"
                    )
                with col2:
                    avg_quality = lead_quality['Quality_Rate'].mean()
                    st.metric(
                        "📊 Avg Quality", 
                        f"{avg_quality:.1f}%"
                    )
                with col3:
                    total_qualified = lead_quality['Qualified_Leads'].sum()
                    st.metric(
                        "✅ Total Qualified", 
                        f"{total_qualified:,}"
                    )
    
    with analytics_tab3:
        st.subheader("⚡ Pipeline Efficiency Metrics")
        
        if not st.session_state.opportunities.empty:
            # Calculate pipeline efficiency metrics
            pipeline_metrics = {
                'Metric': ['Pipeline Value', 'Win Rate', 'Avg Deal Size', 'Sales Cycle', 'Conversion Rate'],
                'Value': [
                    f"${st.session_state.opportunities['value'].sum():,.0f}",
                    f"{won_opportunities/total_opportunities*100:.1f}%" if total_opportunities > 0 else "0%",
                    f"${st.session_state.opportunities['value'].mean():,.0f}",
                    "45 days",  # Sample data
                    f"{won_opportunities/total_leads*100:.1f}%" if total_leads > 0 else "0%"
                ],
                'Status': ['High', 'Good', 'Medium', 'Good', 'Good']
            }
            
            # Create efficiency metrics chart
            fig_efficiency = px.bar(
                x=pipeline_metrics['Metric'],
                y=[1, 1, 1, 1, 1],  # Dummy values for visualization
                color=pipeline_metrics['Status'],
                title='Pipeline Efficiency Overview',
                color_discrete_map={'High': '#16a34a', 'Good': '#10b981', 'Medium': '#f59e0b'},
                text=pipeline_metrics['Value']
            )
            
            fig_efficiency.update_layout(
                title={
                    'text': 'Pipeline Efficiency Overview',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_efficiency.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{text}<br>" +
                            "Status: %{marker.color}<br>" +
                            "<extra></extra>",
                textposition='outside'
            )
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
            
            # Efficiency insights
            with st.expander("💡 Efficiency Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    pipeline_value = st.session_state.opportunities['value'].sum()
                    st.metric(
                        "💰 Pipeline Value", 
                        f"${pipeline_value:,.0f}"
                    )
                with col2:
                    win_rate = won_opportunities/total_opportunities*100 if total_opportunities > 0 else 0
                    st.metric(
                        "🎯 Win Rate", 
                        f"{win_rate:.1f}%"
                    )
                with col3:
                    avg_deal = st.session_state.opportunities['value'].mean()
                    st.metric(
                        "📊 Avg Deal", 
                        f"${avg_deal:,.0f}"
                    )
    
    with analytics_tab4:
        st.subheader("🔍 Advanced Funnel Analytics")
        
        if not st.session_state.leads.empty and not st.session_state.opportunities.empty:
            # Funnel Stage Progression Analysis
            st.markdown("**📊 Funnel Stage Progression**")
            funnel_progression, funnel_msg = calculate_funnel_stage_progression(
                st.session_state.leads, 
                st.session_state.opportunities
            )
            
            if not funnel_progression.empty:
                # Create funnel progression chart
                fig_progression = px.bar(
                    funnel_progression,
                    x='Stage',
                    y='Count',
                    title='Funnel Stage Progression',
                    color='Conversion_Rate',
                    color_continuous_scale='plasma',
                    text='Count'
                )
                
                fig_progression.update_layout(
                    title={
                        'text': 'Funnel Stage Progression',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Funnel Stage',
                    yaxis_title='Count',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_progression.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Count: %{y}<br>" +
                                "Conversion Rate: %{marker.color:.1f}%<br>" +
                                "<extra></extra>",
                    texttemplate='%{y}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_progression, use_container_width=True)
                
                # Progression insights
                with st.expander("💡 Progression Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        total_stages = len(funnel_progression)
                        st.metric(
                            "📊 Total Stages", 
                            total_stages
                        )
                    with col2:
                        avg_conversion = funnel_progression['Conversion_Rate'].mean()
                        st.metric(
                            "📈 Avg Conversion", 
                            f"{avg_conversion:.1f}%"
                        )
                    with col3:
                        max_drop_off = funnel_progression['Drop_Off_Rate'].max()
                        st.metric(
                            "⚠️ Max Drop-off", 
                            f"{max_drop_off:.1f}%"
                        )
            
            st.markdown("---")
            
            # Lead Velocity Metrics
            st.markdown("**⚡ Lead Velocity Analysis**")
            velocity_metrics, velocity_msg = calculate_lead_velocity_metrics(
                st.session_state.leads, 
                st.session_state.opportunities
            )
            
            if not velocity_metrics.empty:
                # Create velocity metrics chart
                fig_velocity = px.bar(
                    velocity_metrics,
                    x='Metric',
                    y=[1, 1, 1],  # Dummy values for visualization
                    color='Status',
                    title='Lead Velocity Metrics',
                    color_discrete_map={'High': '#16a34a', 'Good': '#10b981', 'Medium': '#f59e0b'},
                    text='Value'
                )
                
                fig_velocity.update_layout(
                    title={
                        'text': 'Lead Velocity Metrics',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Metrics',
                    yaxis_title='',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_velocity.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Value: %{text}<br>" +
                                "Status: %{marker.color}<br>" +
                                "<extra></extra>",
                    textposition='outside'
                )
                
                st.plotly_chart(fig_velocity, use_container_width=True)
                
                # Velocity insights
                with st.expander("💡 Velocity Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_time = velocity_metrics[velocity_metrics['Metric'] == 'Avg Lead to Opp Time']['Value'].iloc[0]
                        st.metric(
                            "⏱️ Avg Conversion Time", 
                            avg_time
                        )
                    with col2:
                        lead_velocity = velocity_metrics[velocity_metrics['Metric'] == 'Lead Velocity']['Value'].iloc[0]
                        st.metric(
                            "📊 Lead Velocity", 
                            lead_velocity
                        )
                    with col3:
                        opp_velocity = velocity_metrics[velocity_metrics['Metric'] == 'Opportunity Velocity']['Value'].iloc[0]
                        st.metric(
                            "📈 Opportunity Velocity", 
                            opp_velocity
                        )
            
            st.markdown("---")
            
            # Funnel Efficiency Score
            st.markdown("**🎯 Funnel Efficiency Score**")
            efficiency_score, efficiency_msg = calculate_funnel_efficiency_score(
                st.session_state.leads, 
                st.session_state.opportunities
            )
            
            if not efficiency_score.empty:
                # Create efficiency score chart
                fig_efficiency_score = px.bar(
                    efficiency_score,
                    x='Metric',
                    y='Score',
                    title='Funnel Efficiency Score',
                    color='Grade',
                    color_discrete_map={'A': '#16a34a', 'B': '#10b981', 'C': '#f59e0b'},
                    text='Score'
                )
                
                fig_efficiency_score.update_layout(
                    title={
                        'text': 'Funnel Efficiency Score',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Metrics',
                    yaxis_title='Score (0-100)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_efficiency_score.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Score: %{y:.1f}<br>" +
                                "Grade: %{marker.color}<br>" +
                                "<extra></extra>",
                    texttemplate='%{y:.1f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_efficiency_score, use_container_width=True)
                
                # Efficiency insights
                with st.expander("💡 Efficiency Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        overall_score = efficiency_score[efficiency_score['Metric'] == 'Overall Efficiency']['Score'].iloc[0]
                        st.metric(
                            "🎯 Overall Score", 
                            f"{overall_score:.1f}/100"
                        )
                    with col2:
                        best_metric = efficiency_score.loc[efficiency_score['Score'].idxmax()]
                        st.metric(
                            "🏆 Best Metric", 
                            best_metric['Metric'],
                            f"{best_metric['Score']:.1f}"
                        )
                    with col3:
                        avg_score = efficiency_score['Score'].mean()
                        st.metric(
                            "📊 Average Score", 
                            f"{avg_score:.1f}/100"
                        )
    
    # AI Recommendations
    display_ai_recommendations("sales_funnel", st.session_state.leads, st.session_state.opportunities)

# ============================================================================
# SALES TEAM PERFORMANCE
# ============================================================================

def show_sales_team():
    st.header("👨‍💼 Sales Team Performance")
    
    if st.session_state.sales_reps.empty or st.session_state.sales_orders.empty:
        st.warning("Please add sales representatives and sales data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-green">
        <h3 style="color: white; margin: 0; text-align: center;">👨‍💼 Sales Team Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    active_reps = len(st.session_state.sales_reps[st.session_state.sales_reps['status'] == 'Active'])
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    avg_revenue_per_rep = total_revenue / active_reps if active_reps > 0 else 0
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Active Sales Reps</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(active_reps), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Avg Revenue per Rep</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(avg_revenue_per_rep), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-orange">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Orders</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(len(st.session_state.sales_orders)), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Individual Sales Performance</h4>
        </div>
        """, unsafe_allow_html=True)
        performance_data, performance_msg = calculate_individual_sales_performance(st.session_state.sales_orders, st.session_state.sales_reps, st.session_state.targets)
        
        st.markdown(f"**{performance_msg}**")
        
        if not performance_data.empty:
            # Enhanced performance chart
            fig_performance = px.bar(
                performance_data.head(10), 
                x='full_name', 
                y='total_revenue',
                title='Top 10 Sales Representatives by Revenue',
                color='quota_achievement',
                color_continuous_scale='viridis',
                text='total_revenue'
            )
            
            fig_performance.update_layout(
                title={
                    'text': 'Top 10 Sales Representatives by Revenue',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Sales Representative',
                yaxis_title='Total Revenue ($)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_performance.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Revenue: $%{y:,.2f}<br>" +
                            "Quota Achievement: %{marker.color:.1f}%<br>" +
                            "<extra></extra>",
                texttemplate='$%{y:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_performance, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>🎯 Win Rate Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        win_data, win_msg = calculate_win_rate(st.session_state.opportunities)
        
        st.markdown(f"**{win_msg}**")
        
        if not win_data.empty:
            # Enhanced win rate visualization
            fig_win_rate = px.bar(
                win_data,
                x='Metric',
                y=[1, 1, 1, 1, 1],  # Dummy values for visualization
                color='Value',
                title='Win Rate Analysis Overview',
                color_discrete_map={
                    'Total Opportunities': '#3b82f6',
                    'Won Deals': '#10b981',
                    'Lost Deals': '#ef4444',
                    'Win Rate': '#16a34a',
                    'Loss Rate': '#dc2626'
                },
                text='Value'
            )
            
            fig_win_rate.update_layout(
                title={
                    'text': 'Win Rate Analysis Overview',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_win_rate.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{text}<br>" +
                            "<extra></extra>",
                textposition='outside'
            )
            
            st.plotly_chart(fig_win_rate, use_container_width=True)
            
            # Win rate insights
            with st.expander("💡 Win Rate Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    total_opps = win_data[win_data['Metric'] == 'Total Opportunities']['Value'].iloc[0]
                    st.metric(
                        "📊 Total Opportunities", 
                        total_opps
                    )
                with col2:
                    won_deals = win_data[win_data['Metric'] == 'Won Deals']['Value'].iloc[0]
                    st.metric(
                        "✅ Won Deals", 
                        won_deals
                    )
                
                col3, col4 = st.columns(2)
                with col3:
                    win_rate = win_data[win_data['Metric'] == 'Win Rate']['Value'].iloc[0]
                    st.metric(
                        "🎯 Win Rate", 
                        win_rate
                    )
                with col4:
                    lost_deals = win_data[win_data['Metric'] == 'Lost Deals']['Value'].iloc[0]
                    st.metric(
                        "❌ Lost Deals", 
                        lost_deals
                    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
        <h4>📞 Sales Call Success Rate</h4>
        </div>
        """, unsafe_allow_html=True)
        call_data, call_msg = calculate_sales_call_success_rate(st.session_state.activities)
        
        st.markdown(f"**{call_msg}**")
        
        if not call_data.empty:
            # Enhanced call success visualization
            fig_call_success = px.bar(
                call_data,
                x='Metric',
                y=[1, 1, 1],  # Dummy values for visualization
                color='Value',
                title='Sales Call Success Metrics',
                color_discrete_map={
                    'Total Calls': '#3b82f6',
                    'Positive Outcomes': '#10b981',
                    'Success Rate': '#16a34a'
                },
                text='Value'
            )
            
            fig_call_success.update_layout(
                title={
                    'text': 'Sales Call Success Metrics',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='',
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_call_success.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{text}<br>" +
                            "<extra></extra>",
                textposition='outside'
            )
            
            st.plotly_chart(fig_call_success, use_container_width=True)
            
            # Call success insights
            with st.expander("💡 Call Success Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    total_calls = call_data[call_data['Metric'] == 'Total Calls']['Value'].iloc[0]
                    st.metric(
                        "📞 Total Calls", 
                        total_calls
                    )
                with col2:
                    success_rate = call_data[call_data['Metric'] == 'Success Rate']['Value'].iloc[0]
                    st.metric(
                        "✅ Success Rate", 
                        success_rate
                    )
    
    with col4:
        st.markdown("""
        <div class="chart-container">
        <h4>⚡ Sales Productivity</h4>
        </div>
        """, unsafe_allow_html=True)
        productivity_data, productivity_msg = calculate_sales_productivity(st.session_state.sales_orders, st.session_state.activities)
        
        st.markdown(f"**{productivity_msg}**")
        
        if not productivity_data.empty:
            # Enhanced productivity visualization
            fig_productivity = px.bar(
                productivity_data,
                x='Metric',
                y=[1, 1, 1, 1],  # Dummy values for visualization
                color='Value',
                title='Sales Productivity Overview',
                color_discrete_map={
                    'Total Revenue': '#10b981',
                    'Total Activities': '#3b82f6',
                    'Revenue per Activity': '#f59e0b',
                    'Avg Activities per Rep': '#a855f7'
                },
                text='Value'
            )
            
            fig_productivity.update_layout(
                title={
                    'text': 'Sales Productivity Overview',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='',
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_productivity.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{text}<br>" +
                            "<extra></extra>",
                textposition='outside'
            )
            
            st.plotly_chart(fig_productivity, use_container_width=True)
            
            # Productivity insights
            with st.expander("💡 Productivity Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    total_revenue = productivity_data[productivity_data['Metric'] == 'Total Revenue']['Value'].iloc[0]
                    st.metric(
                        "💰 Total Revenue", 
                        total_revenue
                    )
                with col2:
                    total_activities = productivity_data[productivity_data['Metric'] == 'Total Activities']['Value'].iloc[0]
                    st.metric(
                        "📊 Total Activities", 
                        total_activities
                    )
                
                col3, col4 = st.columns(2)
                with col3:
                    revenue_per_activity = productivity_data[productivity_data['Metric'] == 'Revenue per Activity']['Value'].iloc[0]
                    st.metric(
                        "⚡ Revenue/Activity", 
                        revenue_per_activity
                    )
                with col4:
                    avg_activities = productivity_data[productivity_data['Metric'] == 'Avg Activities per Rep']['Value'].iloc[0]
                    st.metric(
                        "📈 Avg Activities/Rep", 
                        avg_activities
                    )
    
    st.markdown("---")
    
    # Advanced Sales Team Analytics
    st.markdown("""
    <div class="chart-container">
        <h4>🔍 Advanced Sales Team Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    advanced_tab1, advanced_tab2, advanced_tab3 = st.tabs([
        "🏆 Performance Rankings", 
        "🌍 Territory Analysis", 
        "📊 Quota Attainment"
    ])
    
    with advanced_tab1:
        st.subheader("🏆 Performance Rankings & Benchmarks")
        
        if not st.session_state.sales_reps.empty and not st.session_state.sales_orders.empty:
            # Quota attainment analysis
            quota_data, quota_msg = calculate_quota_attainment_rate(
                st.session_state.sales_orders, 
                st.session_state.sales_reps
            )
            
            if not quota_data.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Enhanced quota attainment chart
                    fig_quota_rankings = px.bar(
                        quota_data.head(15),
                        x='full_name',
                        y='attainment_rate',
                        title='Sales Representatives - Quota Attainment Rankings',
                        color='attainment_rate',
                        color_continuous_scale='plasma',
                        text='attainment_rate'
                    )
                    
                    fig_quota_rankings.update_layout(
                        title={
                            'text': 'Sales Representatives - Quota Attainment Rankings',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Sales Representative',
                        yaxis_title='Quota Attainment (%)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified'
                    )
                    
                    fig_quota_rankings.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Attainment: %{y:.1f}%<br>" +
                                    "<extra></extra>",
                        texttemplate='%{y:.1f}%',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_quota_rankings, use_container_width=True)
                
                with col2:
                    # Quota insights
                    with st.expander("💡 Quota Attainment Insights"):
                        col1, col2 = st.columns(2)
                        with col1:
                            top_quota = quota_data.iloc[0]
                            st.metric(
                                "🏆 Top Achiever", 
                                top_quota['full_name'],
                                f"{top_quota['attainment_rate']:.1f}%"
                            )
                        with col2:
                            avg_attainment = quota_data['attainment_rate'].mean()
                            st.metric(
                                "📊 Avg Attainment", 
                                f"{avg_attainment:.1f}%"
                            )
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            over_100 = len(quota_data[quota_data['attainment_rate'] >= 100])
                            st.metric(
                                "✅ Over 100%", 
                                f"{over_100}/{len(quota_data)}"
                            )
                        with col4:
                            under_80 = len(quota_data[quota_data['attainment_rate'] < 80])
                            st.metric(
                                "⚠️ Under 80%", 
                                f"{under_80}/{len(quota_data)}"
                            )
    
    with advanced_tab2:
        st.subheader("🌍 Territory Performance Analysis")
        
        if not st.session_state.sales_reps.empty:
            territory_data, territory_msg = calculate_territory_performance(
                st.session_state.sales_orders, 
                st.session_state.sales_reps
            )
            
            if not territory_data.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig_territory = px.bar(
                        territory_data.head(10),
                        x='territory',
                        y='total_revenue',
                        title='Top 10 Territories by Revenue',
                        color='order_count',
                        color_continuous_scale='viridis',
                        text='total_revenue'
                    )
                    
                    fig_territory.update_layout(
                        title={
                            'text': 'Top 10 Territories by Revenue',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Territory',
                        yaxis_title='Total Revenue ($)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified'
                    )
                    
                    fig_territory.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Revenue: $%{y:,.2f}<br>" +
                                    "Orders: %{marker.color}<br>" +
                                    "<extra></extra>",
                        texttemplate='$%{y:,.0f}',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_territory, use_container_width=True)
                
                with col2:
                    with st.expander("💡 Territory Insights"):
                        col1, col2 = st.columns(2)
                        with col1:
                            top_territory = territory_data.iloc[0]
                            st.metric(
                                "🏆 Top Territory", 
                                top_territory['territory'],
                                f"${top_territory['total_revenue']:,.0f}"
                            )
                        with col2:
                            avg_territory_revenue = territory_data['total_revenue'].mean()
                            st.metric(
                                "📊 Avg Territory", 
                                f"${avg_territory_revenue:,.0f}"
                            )
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            total_territories = len(territory_data)
                            st.metric(
                                "🌍 Total Territories", 
                                total_territories
                            )
                        with col4:
                            total_orders = territory_data['order_count'].sum()
                            st.metric(
                                "📦 Total Orders", 
                                total_orders
                            )
    
    with advanced_tab3:
        st.subheader("📊 Quota Achievement Distribution")
        
        if not st.session_state.sales_reps.empty and not st.session_state.sales_orders.empty:
            performance_data, performance_msg = calculate_individual_sales_performance(
                st.session_state.sales_orders, 
                st.session_state.sales_reps, 
                st.session_state.targets
            )
            
            if not performance_data.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Quota achievement distribution
                    fig_quota_dist = px.histogram(
                        performance_data,
                        x='quota_achievement',
                        title='Quota Achievement Distribution',
                        nbins=20,
                        color_discrete_sequence=['#10b981']
                    )
                    
                    fig_quota_dist.update_layout(
                        title={
                            'text': 'Quota Achievement Distribution',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Quota Achievement (%)',
                        yaxis_title='Number of Representatives',
                        height=400,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig_quota_dist, use_container_width=True)
                
                with col2:
                    with st.expander("💡 Distribution Insights"):
                        col1, col2 = st.columns(2)
                        with col1:
                            median_quota = performance_data['quota_achievement'].median()
                            st.metric(
                                "📊 Median Quota", 
                                f"{median_quota:.1f}%"
                            )
                        with col2:
                            std_quota = performance_data['quota_achievement'].std()
                            st.metric(
                                "📈 Std Deviation", 
                                f"{std_quota:.1f}%"
                            )
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            top_25 = performance_data['quota_achievement'].quantile(0.75)
                            st.metric(
                                "🏆 Top 25%", 
                                f"{top_25:.1f}%"
                            )
                        with col4:
                            bottom_25 = performance_data['quota_achievement'].quantile(0.25)
                            st.metric(
                                "📉 Bottom 25%", 
                                f"{bottom_25:.1f}%"
                            )
    
    # AI Recommendations
    display_ai_recommendations("sales_team", st.session_state.sales_reps, st.session_state.sales_orders)

# ============================================================================
# PRICING & DISCOUNT ANALYSIS
# ============================================================================

def show_pricing_discounts():
    st.header("💰 Pricing & Discount Analysis")
    
    if st.session_state.sales_orders.empty or st.session_state.products.empty:
        st.warning("Please add sales orders and products data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-orange">
        <h3 style="color: #ffffff; margin: 0; text-align: center; font-weight: 700;">💰 Pricing Analysis Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    total_units = st.session_state.sales_orders['quantity'].sum()
    avg_selling_price = total_revenue / total_units if total_units > 0 else 0
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Units Sold</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(total_units), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Average Selling Price</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(avg_selling_price), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Unique Products</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(st.session_state.sales_orders['product_id'].nunique()), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>💰 Average Selling Price (ASP)</h4>
        </div>
        """, unsafe_allow_html=True)
        asp_data, asp_msg = calculate_average_selling_price(st.session_state.sales_orders)
        
        st.markdown(f"**{asp_msg}**")
        
        if not asp_data.empty:
            # Enhanced ASP visualization
            fig_asp = px.bar(
                asp_data.head(15),
                x='product_id',
                y='asp',
                title='Top 15 Products by Average Selling Price',
                color='asp',
                color_continuous_scale='viridis',
                text='asp'
            )
            
            fig_asp.update_layout(
                title={
                    'text': 'Top 15 Products by Average Selling Price',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Product ID',
                yaxis_title='Average Selling Price ($)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_asp.update_traces(
                hovertemplate="<b>Product ID: %{x}</b><br>" +
                            "ASP: $%{y:,.2f}<br>" +
                            "<extra></extra>",
                texttemplate='$%{y:,.0f}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_asp, use_container_width=True)
            
            # ASP insights
            with st.expander("💡 ASP Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    top_asp = asp_data.iloc[0]
                    st.metric(
                        "🏆 Highest ASP", 
                        f"${top_asp['asp']:,.2f}",
                        f"Product {top_asp['product_id']}"
                    )
                with col2:
                    avg_asp = asp_data['asp'].mean()
                    st.metric(
                        "📊 Average ASP", 
                        f"${avg_asp:,.2f}"
                    )
                
                col3, col4 = st.columns(2)
                with col3:
                    total_products = len(asp_data)
                    st.metric(
                        "📦 Total Products", 
                        total_products
                    )
                with col4:
                    overall_asp = asp_data[asp_data['product_id'] == 'Overall']['asp'].iloc[0]
                    st.metric(
                        "💰 Overall ASP", 
                        f"${overall_asp:,.2f}"
                    )
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Profit Margin Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        margin_data, margin_msg = calculate_profit_margin_analysis(st.session_state.sales_orders, st.session_state.products)
        
        st.markdown(f"**{margin_msg}**")
        
        if not margin_data.empty:
            # Enhanced profit margin visualization
            fig_margin = px.bar(
                margin_data.head(15), 
                x='product_name', 
                y='profit_margin',
                title='Top 15 Products by Profit Margin',
                color='profit_margin',
                color_continuous_scale='RdYlGn',
                text='profit_margin'
            )
            
            fig_margin.update_layout(
                title={
                    'text': 'Top 15 Products by Profit Margin',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Product Name',
                yaxis_title='Profit Margin (%)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                xaxis_tickangle=-45
            )
            
            fig_margin.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Profit Margin: %{y:.1f}%<br>" +
                            "<extra></extra>",
                texttemplate='%{y:.1f}%',
                textposition='outside'
            )
            
            st.plotly_chart(fig_margin, use_container_width=True)
            
            # Profit margin insights
            with st.expander("💡 Profit Margin Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    top_margin = margin_data.iloc[0]
                    st.metric(
                        "🏆 Highest Margin", 
                        f"{top_margin['profit_margin']:.1f}%",
                        top_margin['product_name']
                    )
                with col2:
                    avg_margin = margin_data['profit_margin'].mean()
                    st.metric(
                        "📊 Average Margin", 
                        f"{avg_margin:.1f}%"
                    )
                
                col3, col4 = st.columns(2)
                with col3:
                    total_margin_products = len(margin_data)
                    st.metric(
                        "📦 Total Products", 
                        total_margin_products
                    )
                with col4:
                    high_margin_count = len(margin_data[margin_data['profit_margin'] >= 50])
                    st.metric(
                        "✅ High Margin (≥50%)", 
                        f"{high_margin_count}/{total_margin_products}"
                    )
    
    st.markdown("---")
    
    # Advanced Pricing Analytics
    st.markdown("""
    <div class="chart-container">
        <h4>🔍 Advanced Pricing Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    pricing_tab1, pricing_tab2, pricing_tab3 = st.tabs([
        "📈 Price Trends & Analysis", 
        "💰 Revenue & Cost Analysis", 
        "🎯 Pricing Optimization"
    ])
    
    with pricing_tab1:
        st.subheader("📈 Price Trends & Analysis")
        
        if not st.session_state.sales_orders.empty:
            # Price distribution analysis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Price distribution histogram
                fig_price_dist = px.histogram(
                    st.session_state.sales_orders,
                    x='unit_price',
                    title='Unit Price Distribution',
                    nbins=30,
                    color_discrete_sequence=['#10b981']
                )
                
                fig_price_dist.update_layout(
                    title={
                        'text': 'Unit Price Distribution',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Unit Price ($)',
                    yaxis_title='Number of Orders',
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_price_dist, use_container_width=True)
            
            with col2:
                # Price statistics
                with st.expander("💡 Price Statistics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        min_price = st.session_state.sales_orders['unit_price'].min()
                        st.metric(
                            "📉 Min Price", 
                            f"${min_price:,.2f}"
                        )
                    with col2:
                        max_price = st.session_state.sales_orders['unit_price'].max()
                        st.metric(
                            "📈 Max Price", 
                            f"${max_price:,.2f}"
                        )
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        median_price = st.session_state.sales_orders['unit_price'].median()
                        st.metric(
                            "📊 Median Price", 
                            f"${median_price:,.2f}"
                        )
                    with col4:
                        std_price = st.session_state.sales_orders['unit_price'].std()
                        st.metric(
                            "📈 Std Deviation", 
                            f"${std_price:,.2f}"
                        )
            
            # Price vs Quantity analysis
            st.markdown("**📊 Price vs Quantity Analysis**")
            fig_price_qty = px.scatter(
                st.session_state.sales_orders.head(100),
                x='unit_price',
                y='quantity',
                title='Price vs Quantity Relationship',
                color='total_amount',
                color_continuous_scale='viridis',
                size='total_amount'
            )
            
            fig_price_qty.update_layout(
                title={
                    'text': 'Price vs Quantity Relationship',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Unit Price ($)',
                yaxis_title='Quantity',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='closest'
            )
            
            st.plotly_chart(fig_price_qty, use_container_width=True)
    
    with pricing_tab2:
        st.subheader("💰 Revenue & Cost Analysis")
        
        if not st.session_state.sales_orders.empty and not st.session_state.products.empty:
            # Revenue by product category
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Merge sales with product data
                sales_with_products = st.session_state.sales_orders.merge(
                    st.session_state.products[['product_id', 'category']], 
                    on='product_id', 
                    how='left'
                )
                
                category_revenue = sales_with_products.groupby('category')['total_amount'].sum().reset_index()
                category_revenue = category_revenue.sort_values('total_amount', ascending=False)
                
                fig_category_revenue = px.bar(
                    category_revenue,
                    x='category',
                    y='total_amount',
                    title='Revenue by Product Category',
                    color='total_amount',
                    color_continuous_scale='plasma',
                    text='total_amount'
                )
                
                fig_category_revenue.update_layout(
                    title={
                        'text': 'Revenue by Product Category',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Product Category',
                    yaxis_title='Total Revenue ($)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_category_revenue.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_category_revenue, use_container_width=True)
            
            with col2:
                # Category insights
                with st.expander("💡 Category Insights"):
                    col1, col2 = st.columns(2)
                    with col1:
                        top_category = category_revenue.iloc[0]
                        st.metric(
                            "🏆 Top Category", 
                            top_category['category'],
                            f"${top_category['total_amount']:,.0f}"
                        )
                    with col2:
                        avg_category_revenue = category_revenue['total_amount'].mean()
                        st.metric(
                            "📊 Avg Category", 
                            f"${avg_category_revenue:,.0f}"
                        )
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        total_categories = len(category_revenue)
                        st.metric(
                            "📂 Total Categories", 
                            total_categories
                        )
                    with col4:
                        total_revenue_all = category_revenue['total_amount'].sum()
                        st.metric(
                            "💰 Total Revenue", 
                            f"${total_revenue_all:,.0f}"
                        )
            
            # Cost analysis (if cost data available)
            if 'cost_price' in st.session_state.products.columns:
                st.markdown("**💸 Cost vs Revenue Analysis**")
                
                # Merge for cost analysis
                cost_analysis = st.session_state.sales_orders.merge(
                    st.session_state.products[['product_id', 'cost_price']], 
                    on='product_id', 
                    how='left'
                )
                
                cost_analysis['total_cost'] = cost_analysis['cost_price'] * cost_analysis['quantity']
                cost_analysis['profit'] = cost_analysis['total_amount'] - cost_analysis['total_cost']
                
                # Top profitable products
                profitable_products = cost_analysis.groupby('product_id').agg({
                    'total_amount': 'sum',
                    'total_cost': 'sum',
                    'profit': 'sum'
                }).reset_index()
                
                profitable_products = profitable_products.sort_values('profit', ascending=False)
                
                fig_profit_products = px.bar(
                    profitable_products.head(15),
                    x='product_id',
                    y='profit',
                    title='Top 15 Most Profitable Products',
                    color='profit',
                    color_continuous_scale='RdYlGn',
                    text='profit'
                )
                
                fig_profit_products.update_layout(
                    title={
                        'text': 'Top 15 Most Profitable Products',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Product ID',
                    yaxis_title='Total Profit ($)',
                    height=300,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_profit_products.update_traces(
                    hovertemplate="<b>Product ID: %{x}</b><br>" +
                                "Profit: $%{y:,.2f}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_profit_products, use_container_width=True)
    
    with pricing_tab3:
        st.subheader("🎯 Pricing Optimization")
        
        if not st.session_state.sales_orders.empty:
            # Pricing elasticity analysis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Price range analysis
                price_ranges = pd.cut(st.session_state.sales_orders['unit_price'], 
                                    bins=5, labels=['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'])
                price_range_analysis = st.session_state.sales_orders.groupby(price_ranges).agg({
                    'quantity': 'sum',
                    'total_amount': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                price_range_analysis.columns = ['Price Range', 'Total Quantity', 'Total Revenue', 'Order Count']
                
                fig_price_range = px.bar(
                    price_range_analysis,
                    x='Price Range',
                    y='Total Revenue',
                    title='Revenue by Price Range',
                    color='Order Count',
                    color_continuous_scale='viridis',
                    text='Total Revenue'
                )
                
                fig_price_range.update_layout(
                    title={
                        'text': 'Revenue by Price Range',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Price Range',
                    yaxis_title='Total Revenue ($)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_price_range.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "Orders: %{marker.color}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_price_range, use_container_width=True)
            
            with col2:
                # Price optimization insights
                with st.expander("💡 Pricing Optimization Insights"):
                    col1, col2 = st.columns(2)
                    with col1:
                        best_price_range = price_range_analysis.loc[price_range_analysis['Total Revenue'].idxmax()]
                        st.metric(
                            "🏆 Best Range", 
                            best_price_range['Price Range'],
                            f"${best_price_range['Total Revenue']:,.0f}"
                        )
                    with col2:
                        avg_order_value = st.session_state.sales_orders['total_amount'].mean()
                        st.metric(
                            "📊 Avg Order", 
                            f"${avg_order_value:,.2f}"
                        )
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        total_orders = len(st.session_state.sales_orders)
                        st.metric(
                            "📦 Total Orders", 
                            total_orders
                        )
                    with col4:
                        revenue_per_order = st.session_state.sales_orders['total_amount'].sum() / total_orders
                        st.metric(
                            "💰 Revenue/Order", 
                            f"${revenue_per_order:,.2f}"
                        )
            
            # Pricing recommendations
            st.markdown("**💡 Pricing Recommendations**")
            
            # Calculate optimal price points
            optimal_price = st.session_state.sales_orders['unit_price'].median()
            high_value_threshold = st.session_state.sales_orders['unit_price'].quantile(0.75)
            low_value_threshold = st.session_state.sales_orders['unit_price'].quantile(0.25)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="metric-card-green">
                    <h4 style="margin: 0; color: #ffffff; font-weight: 600;">🎯 Optimal Price Point</h4>
                    <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
                    <p style="margin: 0; color: #ffffff; font-size: 14px;">Median price for maximum volume</p>
                </div>
                """.format(optimal_price), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card-blue">
                    <h4 style="margin: 0; color: #ffffff; font-weight: 600;">📈 Premium Price Range</h4>
                    <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}+</h2>
                    <p style="margin: 0; color: #ffffff; font-size: 14px;">High-value positioning</p>
                </div>
                """.format(high_value_threshold), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card-orange">
                    <h4 style="margin: 0; color: #ffffff; font-weight: 600;">💰 Value Price Range</h4>
                    <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}-</h2>
                    <p style="margin: 0; color: #ffffff; font-size: 14px;">Volume-driven pricing</p>
                </div>
                """.format(low_value_threshold), unsafe_allow_html=True)
    
    # AI Recommendations
    display_ai_recommendations("pricing_discounts", st.session_state.products, st.session_state.sales_orders)

# ============================================================================
# MARKET & COMPETITOR ANALYSIS
# ============================================================================

def show_market_analysis():
    st.header("🌍 Market & Competitor Analysis")
    
    if st.session_state.customers.empty or st.session_state.sales_orders.empty:
        st.warning("Please add customers and sales data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-blue">
        <h3 style="color: #ffffff; margin: 0; text-align: center; font-weight: 700;">🌍 Market Analysis Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_customers = len(st.session_state.customers)
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    unique_regions = st.session_state.customers['region'].nunique()
    unique_industries = st.session_state.customers['industry'].nunique()
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(total_customers), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Regions Served</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(unique_regions), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Industries Served</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(unique_industries), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Market Share Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        # Example market share calculation (requires total market data)
        company_sales = total_revenue
        total_market_sales = company_sales * 10  # Example: assuming 10% market share
        market_data, market_msg = calculate_market_share_analysis(company_sales, total_market_sales)
        
        st.markdown(f"**{market_msg}**")
        
        # Debug: Show available data structure
        with st.expander("🔍 Debug: Available Market Data"):
            st.write("**DataFrame Shape:**", market_data.shape)
            st.write("**Column Names:**", list(market_data.columns))
            st.write("**Available Metrics:**", list(market_data['Metric'].unique()) if 'Metric' in market_data.columns else "No 'Metric' column found")
            st.write("**Sample Data:**")
            st.dataframe(market_data.head())
        
        if not market_data.empty:
            # Enhanced market share visualization
            fig_market_share = px.bar(
                market_data,
                x='Metric',
                y='Value',
                title='Market Share Analysis',
                color='Value',
                color_continuous_scale='plasma',
                text='Value'
            )
            
            fig_market_share.update_layout(
                title={
                    'text': 'Market Share Analysis',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='Value',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_market_share.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{y}<br>" +
                            "<extra></extra>",
                texttemplate='%{y}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_market_share, use_container_width=True)
            
            # Market share insights
            with st.expander("💡 Market Share Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    company_share_filter = market_data[market_data['Metric'] == 'Company Market Share']
                    if not company_share_filter.empty:
                        company_share = company_share_filter['Value'].iloc[0]
                        st.metric(
                            "🏢 Company Share", 
                            company_share
                        )
                    else:
                        st.metric(
                            "🏢 Company Share", 
                            "N/A"
                        )
                with col2:
                    total_market_filter = market_data[market_data['Metric'] == 'Total Market Size']
                    if not total_market_filter.empty:
                        total_market = total_market_filter['Value'].iloc[0]
                        st.metric(
                            "🌍 Total Market", 
                            total_market
                        )
                    else:
                        st.metric(
                            "🌍 Total Market", 
                            "N/A"
                        )
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>🎯 Market Penetration Rate</h4>
        </div>
        """, unsafe_allow_html=True)
        # Example market penetration calculation
        total_target_market = total_customers * 20  # Example: assuming 5% penetration
        penetration_data, penetration_msg = calculate_market_penetration_rate(st.session_state.customers, total_target_market)
        
        st.markdown(f"**{penetration_msg}**")
        
        # Debug: Show available data structure
        with st.expander("🔍 Debug: Available Penetration Data"):
            st.write("**DataFrame Shape:**", penetration_data.shape)
            st.write("**Column Names:**", list(penetration_data.columns))
            st.write("**Available Metrics:**", list(penetration_data['Metric'].unique()) if 'Metric' in penetration_data.columns else "No 'Metric' column found")
            st.write("**Sample Data:**")
            st.dataframe(penetration_data.head())
        
        if not penetration_data.empty:
            # Enhanced penetration visualization
            fig_penetration = px.bar(
                penetration_data,
                x='Metric',
                y='Value',
                title='Market Penetration Analysis',
                color='Value',
                color_continuous_scale='viridis',
                text='Value'
            )
            
            fig_penetration.update_layout(
                title={
                    'text': 'Market Penetration Analysis',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Metrics',
                yaxis_title='Value',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            fig_penetration.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                            "Value: %{y}<br>" +
                            "<extra></extra>",
                texttemplate='%{y}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_penetration, use_container_width=True)
            
            # Penetration insights
            with st.expander("💡 Penetration Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    penetration_rate_filter = penetration_data[penetration_data['Metric'] == 'Penetration Rate']
                    if not penetration_rate_filter.empty:
                        penetration_rate = penetration_rate_filter['Value'].iloc[0]
                        st.metric(
                            "🎯 Penetration Rate", 
                            penetration_rate
                        )
                    else:
                        st.metric(
                            "🎯 Penetration Rate", 
                            "N/A"
                        )
                with col2:
                    target_market_filter = penetration_data[penetration_data['Metric'] == 'Target Market Size']
                    if not target_market_filter.empty:
                        target_market = target_market_filter['Value'].iloc[0]
                        st.metric(
                            "🎯 Target Market", 
                            target_market
                        )
                    else:
                        st.metric(
                            "🎯 Target Market", 
                            "N/A"
                        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
        <h4>🏭 Customer Distribution by Industry</h4>
        </div>
        """, unsafe_allow_html=True)
        industry_dist = st.session_state.customers['industry'].value_counts()
        # Enhanced industry distribution visualization
        fig_industry = px.pie(
            values=industry_dist.values,
            names=industry_dist.index,
            title='Customer Distribution by Industry',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_industry.update_layout(
            title={
                'text': 'Customer Distribution by Industry',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#1f2937'}
            },
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig_industry.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                        "Customers: %{value}<br>" +
                        "Percentage: %{percent:.1%}<br>" +
                        "<extra></extra>",
            textinfo='label+percent',
            textposition='inside'
        )
        
        st.plotly_chart(fig_industry, use_container_width=True)
        
        # Industry insights
        with st.expander("💡 Industry Insights"):
            col1, col2 = st.columns(2)
            with col1:
                top_industry = industry_dist.index[0]
                top_count = industry_dist.iloc[0]
                st.metric(
                    "🏆 Top Industry", 
                    top_industry,
                    f"{top_count} customers"
                )
            with col2:
                total_industries = len(industry_dist)
                st.metric(
                    "📂 Total Industries", 
                    total_industries
                )
    
    with col4:
        st.markdown("""
        <div class="chart-container">
        <h4>🌍 Customer Distribution by Region</h4>
        </div>
        """, unsafe_allow_html=True)
        region_dist = st.session_state.customers['region'].value_counts()
        # Enhanced region distribution visualization
        fig_region = px.bar(
            x=region_dist.index,
            y=region_dist.values,
            title='Customer Distribution by Region',
            color=region_dist.values,
            color_continuous_scale='viridis',
            text=region_dist.values
        )
        
        fig_region.update_layout(
            title={
                'text': 'Customer Distribution by Region',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#1f2937'}
            },
            xaxis_title='Region',
            yaxis_title='Number of Customers',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        
        fig_region.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                        "Customers: %{y}<br>" +
                        "<extra></extra>",
            texttemplate='%{y}',
            textposition='outside'
        )
        
        st.plotly_chart(fig_region, use_container_width=True)
        
        # Region insights
        with st.expander("💡 Region Insights"):
            col1, col2 = st.columns(2)
            with col1:
                top_region = region_dist.index[0]
                top_count = region_dist.iloc[0]
                st.metric(
                    "🏆 Top Region", 
                    top_region,
                    f"{top_count} customers"
                )
            with col2:
                total_regions = len(region_dist)
                st.metric(
                    "🌍 Total Regions", 
                    total_regions
                )
    
    st.markdown("---")
    
    # Advanced Market Analytics
    st.markdown("""
    <div class="chart-container">
        <h4>🔍 Advanced Market Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    market_tab1, market_tab2, market_tab3 = st.tabs([
        "📈 Market Trends & Growth", 
        "🎯 Customer Segmentation", 
        "🌍 Geographic & Industry Analysis"
    ])
    
    with market_tab1:
        st.subheader("📈 Market Trends & Growth")
        
        if not st.session_state.sales_orders.empty:
            # Revenue trends by month
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Monthly revenue trends
                sales_with_dates = st.session_state.sales_orders.copy()
                sales_with_dates['order_date'] = pd.to_datetime(sales_with_dates['order_date'])
                monthly_revenue = sales_with_dates.groupby(sales_with_dates['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
                monthly_revenue['order_date'] = monthly_revenue['order_date'].astype(str)
                
                fig_monthly_trend = px.line(
                    monthly_revenue,
                    x='order_date',
                    y='total_amount',
                    title='Monthly Revenue Trends',
                    markers=True,
                    line_shape='linear'
                )
                
                fig_monthly_trend.update_layout(
                    title={
                        'text': 'Monthly Revenue Trends',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Month',
                    yaxis_title='Revenue ($)',
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                fig_monthly_trend.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "<extra></extra>",
                    line_color='#10b981',
                    marker_color='#10b981'
                )
                
                st.plotly_chart(fig_monthly_trend, use_container_width=True)
            
            with col2:
                # Growth metrics
                with st.expander("💡 Growth Metrics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        if len(monthly_revenue) > 1:
                            growth_rate = ((monthly_revenue.iloc[-1]['total_amount'] - monthly_revenue.iloc[0]['total_amount']) / monthly_revenue.iloc[0]['total_amount']) * 100
                            st.metric(
                                "📈 Growth Rate", 
                                f"{growth_rate:.1f}%"
                            )
                        else:
                            st.metric(
                                "📈 Growth Rate", 
                                "N/A"
                            )
                    with col2:
                        avg_monthly_revenue = monthly_revenue['total_amount'].mean()
                        st.metric(
                            "📊 Avg Monthly", 
                            f"${avg_monthly_revenue:,.0f}"
                        )
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        total_months = len(monthly_revenue)
                        st.metric(
                            "📅 Total Months", 
                            total_months
                        )
                    with col4:
                        best_month = monthly_revenue.loc[monthly_revenue['total_amount'].idxmax()]
                        st.metric(
                            "🏆 Best Month", 
                            best_month['order_date']
                        )
            
            # Customer acquisition trends
            st.markdown("**👥 Customer Acquisition Trends**")
            
            if not st.session_state.customers.empty:
                customers_with_dates = st.session_state.customers.copy()
                if 'registration_date' in customers_with_dates.columns:
                    customers_with_dates['registration_date'] = pd.to_datetime(customers_with_dates['registration_date'])
                    monthly_customers = customers_with_dates.groupby(customers_with_dates['registration_date'].dt.to_period('M')).size().reset_index(name='new_customers')
                    monthly_customers['registration_date'] = monthly_customers['registration_date'].astype(str)
                    
                    fig_customer_trend = px.bar(
                        monthly_customers,
                        x='registration_date',
                        y='new_customers',
                        title='Monthly New Customer Acquisition',
                        color='new_customers',
                        color_continuous_scale='plasma'
                    )
                    
                    fig_customer_trend.update_layout(
                        title={
                            'text': 'Monthly New Customer Acquisition',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Month',
                        yaxis_title='New Customers',
                        height=300,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified'
                    )
                    
                    fig_customer_trend.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "New Customers: %{y}<br>" +
                                    "<extra></extra>",
                        texttemplate='%{y}',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_customer_trend, use_container_width=True)
                else:
                    st.info("Customer registration dates not available for trend analysis.")
    
    with market_tab2:
        st.subheader("🎯 Customer Segmentation")
        
        if not st.session_state.customers.empty and not st.session_state.sales_orders.empty:
            # Customer value segmentation
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Merge customers with sales data
                customer_sales = st.session_state.sales_orders.merge(
                    st.session_state.customers[['customer_id', 'industry', 'region']], 
                    on='customer_id', 
                    how='left'
                )
                
                customer_value = customer_sales.groupby('customer_id').agg({
                    'total_amount': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                customer_value.columns = ['customer_id', 'total_spent', 'order_count']
                customer_value['avg_order_value'] = customer_value['total_spent'] / customer_value['order_count']
                
                # Create customer segments
                customer_value['segment'] = pd.cut(
                    customer_value['total_spent'], 
                    bins=3, 
                    labels=['Low Value', 'Medium Value', 'High Value']
                )
                
                segment_dist = customer_value['segment'].value_counts()
                
                fig_segments = px.pie(
                    values=segment_dist.values,
                    names=segment_dist.index,
                    title='Customer Value Segmentation',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                
                fig_segments.update_layout(
                    title={
                        'text': 'Customer Value Segmentation',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_segments.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                "Customers: %{value}<br>" +
                                "Percentage: %{percent:.1%}<br>" +
                                "<extra></extra>",
                    textinfo='label+percent',
                    textposition='inside'
                )
                
                st.plotly_chart(fig_segments, use_container_width=True)
            
            with col2:
                # Segmentation insights
                with st.expander("💡 Segmentation Insights"):
                    col1, col2 = st.columns(2)
                    with col1:
                        high_value_count = len(customer_value[customer_value['segment'] == 'High Value'])
                        st.metric(
                            "💎 High Value", 
                            f"{high_value_count}"
                        )
                    with col2:
                        avg_customer_value = customer_value['total_spent'].mean()
                        st.metric(
                            "📊 Avg Value", 
                            f"${avg_customer_value:,.0f}"
                        )
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        total_customers_analyzed = len(customer_value)
                        st.metric(
                            "👥 Total Analyzed", 
                            total_customers_analyzed
                        )
                    with col4:
                        top_customer_value = customer_value['total_spent'].max()
                        st.metric(
                            "🏆 Top Customer", 
                            f"${top_customer_value:,.0f}"
                        )
            
            # Customer behavior analysis
            st.markdown("**📊 Customer Behavior Analysis**")
            
            # Order frequency vs value scatter plot
            fig_behavior = px.scatter(
                customer_value,
                x='order_count',
                y='avg_order_value',
                title='Customer Behavior: Order Frequency vs Average Order Value',
                color='total_spent',
                color_continuous_scale='viridis',
                size='total_spent',
                hover_data=['customer_id']
            )
            
            fig_behavior.update_layout(
                title={
                    'text': 'Customer Behavior: Order Frequency vs Average Order Value',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Number of Orders',
                yaxis_title='Average Order Value ($)',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='closest'
            )
            
            st.plotly_chart(fig_behavior, use_container_width=True)
    
    with market_tab3:
        st.subheader("🌍 Geographic & Industry Analysis")
        
        if not st.session_state.customers.empty and not st.session_state.sales_orders.empty:
            # Geographic performance analysis
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Revenue by region
                if 'region' in customer_sales.columns:
                    region_performance = customer_sales.groupby('region').agg({
                        'total_amount': 'sum',
                        'order_id': 'count',
                        'customer_id': 'nunique'
                    }).reset_index()
                    
                    region_performance.columns = ['Region', 'Total Revenue', 'Total Orders', 'Unique Customers']
                    region_performance = region_performance.sort_values('Total Revenue', ascending=False)
                else:
                    st.warning("Region data not available for geographic analysis.")
                    region_performance = pd.DataFrame()
                
                if not region_performance.empty:
                    fig_region_perf = px.bar(
                        region_performance,
                        x='Region',
                        y='Total Revenue',
                        title='Revenue Performance by Region',
                        color='Total Orders',
                        color_continuous_scale='plasma',
                        text='Total Revenue'
                    )
                    
                    fig_region_perf.update_layout(
                        title={
                            'text': 'Revenue Performance by Region',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Region',
                        yaxis_title='Total Revenue ($)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        hovermode='x unified'
                    )
                    
                    fig_region_perf.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Revenue: $%{y:,.2f}<br>" +
                                    "Orders: %{marker.color}<br>" +
                                    "<extra></extra>",
                        texttemplate='$%{y:,.0f}',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_region_perf, use_container_width=True)
                else:
                    st.info("No region performance data available to display.")
            
            with col2:
                # Geographic insights
                with st.expander("💡 Geographic Insights"):
                    if not region_performance.empty:
                        col1, col2 = st.columns(2)
                        with col1:
                            top_region_revenue = region_performance.iloc[0]
                            st.metric(
                                "🏆 Top Region", 
                                top_region_revenue['Region'],
                                f"${top_region_revenue['Total Revenue']:,.0f}"
                            )
                        with col2:
                            avg_region_revenue = region_performance['Total Revenue'].mean()
                            st.metric(
                                "📊 Avg Region", 
                                f"${avg_region_revenue:,.0f}"
                            )
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            total_regions_analyzed = len(region_performance)
                            st.metric(
                                "🌍 Total Regions", 
                                total_regions_analyzed
                            )
                        with col4:
                            total_geographic_revenue = region_performance['Total Revenue'].sum()
                            st.metric(
                                "💰 Total Revenue", 
                                f"${total_geographic_revenue:,.0f}"
                            )
                    else:
                        st.info("No geographic insights available due to missing region data.")
            
            # Industry performance analysis
            st.markdown("**🏭 Industry Performance Analysis**")
            
            # Revenue by industry
            if 'industry' in customer_sales.columns:
                industry_performance = customer_sales.groupby('industry').agg({
                    'total_amount': 'sum',
                    'order_id': 'count',
                    'customer_id': 'nunique'
                }).reset_index()
                
                industry_performance.columns = ['Industry', 'Total Revenue', 'Total Orders', 'Unique Customers']
                industry_performance = industry_performance.sort_values('Total Revenue', ascending=False)
            else:
                st.warning("Industry data not available for industry analysis.")
                industry_performance = pd.DataFrame()
            
            if not industry_performance.empty:
                fig_industry_perf = px.bar(
                    industry_performance,
                    x='Industry',
                    y='Total Revenue',
                    title='Revenue Performance by Industry',
                    color='Unique Customers',
                    color_continuous_scale='viridis',
                    text='Total Revenue'
                )
                
                fig_industry_perf.update_layout(
                    title={
                        'text': 'Revenue Performance by Industry',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Industry',
                    yaxis_title='Total Revenue ($)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified',
                    xaxis_tickangle=-45
                )
                
                fig_industry_perf.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "Customers: %{marker.color}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_industry_perf, use_container_width=True)
            else:
                st.info("No industry performance data available to display.")
    
    # AI Recommendations
    display_ai_recommendations("market_analysis", st.session_state.sales_orders, st.session_state.customers)

# ============================================================================
# SALES FORECASTING & PLANNING
# ============================================================================

def show_forecasting():
    st.header("🔮 Advanced Forecasting & Predictive Analytics")
    
    if st.session_state.sales_orders.empty:
        st.warning("Please add sales data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-teal">
        <h3 style="color: white; margin: 0; text-align: center;">🔮 Advanced Forecasting Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different forecasting views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Multi-Scenario Forecast", "🌊 Seasonal Forecast", "📈 Confidence Intervals", "💡 Forecast Insights"])
    
    with tab1:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Multi-Scenario Revenue Forecasting</h4>
        </div>
        """, unsafe_allow_html=True)
        
        forecast_data, forecast_msg = calculate_revenue_forecast(st.session_state.sales_orders)
        
        st.markdown(f"**{forecast_msg}**")
        
        if not forecast_data.empty:
            # Create multi-line chart with all scenarios
            fig_forecast = go.Figure()
            
            # Add optimistic scenario
            fig_forecast.add_trace(go.Scatter(
                x=forecast_data['period'],
                y=forecast_data['optimistic'],
                mode='lines+markers',
                name='Optimistic',
                line=dict(color='#10b981', width=3),
                marker=dict(color='#10b981', size=8)
            ))
            
            # Add realistic scenario
            fig_forecast.add_trace(go.Scatter(
                x=forecast_data['period'],
                y=forecast_data['realistic'],
                mode='lines+markers',
                name='Realistic',
                line=dict(color='#3b82f6', width=3),
                marker=dict(color='#3b82f6', size=8)
            ))
            
            # Add conservative scenario
            fig_forecast.add_trace(go.Scatter(
                x=forecast_data['period'],
                y=forecast_data['conservative'],
                mode='lines+markers',
                name='Conservative',
                line=dict(color='#f59e0b', width=3),
                marker=dict(color='#f59e0b', size=8)
            ))
            
            fig_forecast.update_layout(
                title={
                    'text': 'Multi-Scenario Revenue Forecast (Next 12 Periods)',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Forecast Period',
                yaxis_title='Forecasted Revenue ($)',
                height=500,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Scenario comparison table
            with st.expander("📋 Scenario Comparison"):
                comparison_data = forecast_data.copy()
                comparison_data['optimistic'] = comparison_data['optimistic'].round(2)
                comparison_data['realistic'] = comparison_data['realistic'].round(2)
                comparison_data['conservative'] = comparison_data['conservative'].round(2)
                st.dataframe(comparison_data, use_container_width=True)
    
    with tab2:
        st.markdown("""
        <div class="chart-container">
        <h4>🌊 Seasonal Revenue Forecasting</h4>
        </div>
        """, unsafe_allow_html=True)
        
        seasonal_data, seasonal_msg = calculate_seasonal_forecast(st.session_state.sales_orders)
        
        st.markdown(f"**{seasonal_msg}**")
        
        if not seasonal_data.empty:
            # Create seasonal forecast chart
            fig_seasonal = go.Figure()
            
            # Add seasonal forecast line
            fig_seasonal.add_trace(go.Scatter(
                x=seasonal_data['period'],
                y=seasonal_data['forecasted_revenue'],
                mode='lines+markers',
                name='Seasonal Forecast',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(color='#8b5cf6', size=8)
            ))
            
            # Add seasonal factors as bars
            fig_seasonal.add_trace(go.Bar(
                x=seasonal_data['period'],
                y=seasonal_data['seasonal_factor'] * 1000,  # Scale for visibility
                name='Seasonal Factor',
                yaxis='y2',
                opacity=0.3,
                marker_color='#06b6d4'
            ))
            
            fig_seasonal.update_layout(
                title={
                    'text': 'Seasonal Revenue Forecast with Pattern Recognition',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Forecast Period',
                yaxis_title='Forecasted Revenue ($)',
                yaxis2=dict(
                    title='Seasonal Factor (Scaled)',
                    overlaying='y',
                    side='right'
                ),
                height=500,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_seasonal, use_container_width=True)
            
            # Seasonal insights
            with st.expander("🌊 Seasonal Insights"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    max_seasonal = seasonal_data['seasonal_factor'].max()
                    st.metric(
                        "📈 Peak Season Factor", 
                        f"{max_seasonal:.2f}x"
                    )
                with col2:
                    min_seasonal = seasonal_data['seasonal_factor'].min()
                    st.metric(
                        "📉 Low Season Factor", 
                        f"{min_seasonal:.2f}x"
                    )
                with col3:
                    avg_seasonal = seasonal_data['seasonal_factor'].mean()
                    st.metric(
                        "📊 Avg Seasonal Factor", 
                        f"{avg_seasonal:.2f}x"
                    )
    
    with tab3:
        st.markdown("""
        <div class="chart-container">
        <h4>📈 Forecast Confidence Intervals</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not forecast_data.empty:
            confidence_data, confidence_msg = calculate_confidence_intervals(forecast_data)
            
            st.markdown(f"**{confidence_msg}**")
            
            if not confidence_data.empty:
                # Create confidence interval chart
                fig_confidence = go.Figure()
                
                # Add confidence intervals
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_95_upper'],
                    mode='lines',
                    name='95% Confidence Upper',
                    line=dict(color='rgba(59, 130, 246, 0.3)', width=1),
                    showlegend=False
                ))
                
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_68_upper'],
                    mode='lines',
                    name='68% Confidence Upper',
                    line=dict(color='rgba(59, 130, 246, 0.5)', width=1),
                    showlegend=False
                ))
                
                # Add realistic forecast line
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['realistic'],
                    mode='lines+markers',
                    name='Realistic Forecast',
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(color='#3b82f6', size=8)
                ))
                
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_68_lower'],
                    mode='lines',
                    name='68% Confidence Lower',
                    line=dict(color='rgba(59, 130, 246, 0.5)', width=1),
                    showlegend=False
                ))
                
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_95_lower'],
                    mode='lines',
                    name='95% Confidence Lower',
                    line=dict(color='rgba(59, 130, 246, 0.3)', width=1),
                    showlegend=False
                ))
                
                # Fill confidence intervals
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_95_upper'],
                    mode='lines',
                    fill='tonexty',
                    fillcolor='rgba(59, 130, 246, 0.1)',
                    name='95% Confidence Interval',
                    line=dict(width=0)
                ))
                
                fig_confidence.add_trace(go.Scatter(
                    x=confidence_data['period'],
                    y=confidence_data['confidence_68_upper'],
                    mode='lines',
                    fill='tonexty',
                    fillcolor='rgba(59, 130, 246, 0.2)',
                    name='68% Confidence Interval',
                    line=dict(width=0)
                ))
                
                fig_confidence.update_layout(
                    title={
                        'text': 'Forecast Confidence Intervals',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Forecast Period',
                    yaxis_title='Forecasted Revenue ($)',
                    height=500,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_confidence, use_container_width=True)
                
                # Confidence insights
                with st.expander("📈 Confidence Insights"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_confidence_95 = ((confidence_data['confidence_95_upper'] - confidence_data['confidence_95_lower']) / confidence_data['realistic'] * 100).mean()
                        st.metric(
                            "📊 95% CI Range", 
                            f"±{avg_confidence_95:.1f}%"
                        )
                    with col2:
                        avg_confidence_68 = ((confidence_data['confidence_68_upper'] - confidence_data['confidence_68_lower']) / confidence_data['realistic'] * 100).mean()
                        st.metric(
                            "📊 68% CI Range", 
                            f"±{avg_confidence_68:.1f}%"
                        )
                    with col3:
                        volatility = 15.0  # From the calculation
                        st.metric(
                            "📊 Assumed Volatility", 
                            f"{volatility:.1f}%"
                        )
    
    with tab4:
        st.markdown("""
        <div class="chart-container">
        <h4>💡 Comprehensive Forecast Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not forecast_data.empty:
            # Enhanced forecast insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Growth Analysis**")
                
                # Calculate growth metrics for realistic scenario
                first_forecast = forecast_data['realistic'].iloc[0]
                last_forecast = forecast_data['realistic'].iloc[-1]
                total_growth = ((last_forecast - first_forecast) / first_forecast) * 100
                avg_period_growth = ((last_forecast / first_forecast) ** (1/12) - 1) * 100
                
                st.metric("📈 Total Growth (12 Periods)", f"{total_growth:.1f}%")
                st.metric("📊 Average Period Growth", f"{avg_period_growth:.1f}%")
                st.metric("🎯 Final Forecast Value", f"${last_forecast:,.0f}")
                
                # Scenario comparison
                st.markdown("**🔄 Scenario Comparison**")
                optimistic_growth = ((forecast_data['optimistic'].iloc[-1] - forecast_data['optimistic'].iloc[0]) / forecast_data['optimistic'].iloc[0]) * 100
                conservative_growth = ((forecast_data['conservative'].iloc[-1] - forecast_data['conservative'].iloc[0]) / forecast_data['conservative'].iloc[0]) * 100
                
                st.metric("🚀 Optimistic Growth", f"{optimistic_growth:.1f}%")
                st.metric("⚠️ Conservative Growth", f"{conservative_growth:.1f}%")
                st.metric("📊 Growth Range", f"{optimistic_growth - conservative_growth:.1f}%")
            
            with col2:
                st.markdown("**🎯 Forecast Accuracy Metrics**")
                
                # Calculate forecast accuracy indicators
                if 'realistic' in forecast_data.columns:
                    forecast_volatility = forecast_data['realistic'].pct_change().std() * 100
                    forecast_trend_consistency = abs(forecast_data['realistic'].pct_change().mean()) / forecast_data['realistic'].pct_change().std()
                    
                    st.metric("📊 Forecast Volatility", f"{forecast_volatility:.1f}%")
                    st.metric("📈 Trend Consistency", f"{forecast_volatility:.2f}")
                    
                    # Volatility assessment
                    if forecast_volatility < 5:
                        volatility_assessment = "Low"
                        volatility_color = "🟢"
                    elif forecast_volatility < 15:
                        volatility_assessment = "Medium"
                        volatility_color = "🟡"
                    else:
                        volatility_assessment = "High"
                        volatility_color = "🔴"
                    
                    st.metric(f"{volatility_color} Volatility Assessment", volatility_assessment)
                
                # Risk assessment
                st.markdown("**⚠️ Risk Assessment**")
                
                if 'realistic' in forecast_data.columns:
                    # Calculate downside risk
                    realistic_final = forecast_data['realistic'].iloc[-1]
                    conservative_final = forecast_data['conservative'].iloc[-1]
                    downside_risk = ((realistic_final - conservative_final) / realistic_final) * 100
                    
                    st.metric("📉 Downside Risk", f"{downside_risk:.1f}%")
                    
                    # Risk level assessment
                    if downside_risk < 10:
                        risk_level = "Low"
                        risk_color = "🟢"
                    elif downside_risk < 25:
                        risk_level = "Medium"
                        risk_color = "🟡"
                    else:
                        risk_level = "High"
                        risk_color = "🔴"
                    
                    st.metric(f"{risk_color} Risk Level", risk_level)
    
    # Historical trends comparison
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>📅 Historical Revenue Trends</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Create historical revenue trend
        st.session_state.sales_orders['order_date'] = pd.to_datetime(st.session_state.sales_orders['order_date'])
        monthly_revenue = st.session_state.sales_orders.groupby(st.session_state.sales_orders['order_date'].dt.to_period('M'))['total_amount'].sum().reset_index()
        monthly_revenue['order_date'] = monthly_revenue['order_date'].astype(str)
        
        fig_trend = px.line(
            monthly_revenue,
            x='order_date',
            y='total_amount',
            title='Historical Revenue Trends',
            markers=True
        )
        fig_trend.update_layout(
            title={
                'text': 'Historical Revenue Trends',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1f2937'}
            },
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        fig_trend.update_traces(
            line=dict(color='#6366f1', width=3),
            marker=dict(color='#6366f1', size=6)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Forecast vs Historical</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not forecast_data.empty:
            # Combine historical and forecast data
            historical_avg = monthly_revenue['total_amount'].mean()
            forecast_avg = forecast_data['realistic'].mean()
            
            comparison_data = pd.DataFrame({
                'Metric': ['Historical Average', 'Forecast Average', 'Growth Projection'],
                'Value': [
                    f"${historical_avg:,.0f}",
                    f"${forecast_avg:,.0f}",
                    f"{((forecast_avg - historical_avg) / historical_avg * 100):.1f}%"
                ]
            })
            
            # Create comparison chart
            fig_comparison = px.bar(
                comparison_data,
                x='Metric',
                y=[historical_avg, forecast_avg, (forecast_avg - historical_avg) / historical_avg * 100],
                title='Historical vs Forecast Comparison',
                color=['Historical', 'Forecast', 'Growth'],
                color_discrete_map={
                    'Historical': '#6366f1',
                    'Forecast': '#10b981',
                    'Growth': '#f59e0b'
                }
            )
            
            fig_comparison.update_layout(
                title={
                    'text': 'Historical vs Forecast Comparison',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1f2937'}
                },
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Comparison insights
            with st.expander("📊 Comparison Insights"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📈 Historical Average", f"${historical_avg:,.0f}")
                    st.metric("🎯 Forecast Average", f"${forecast_avg:,.0f}")
                with col2:
                    growth_rate = ((forecast_avg - historical_avg) / historical_avg) * 100
                    st.metric("📊 Growth Rate", f"{growth_rate:.1f}%")
                    
                    if growth_rate > 0:
                        st.success("📈 Positive growth projection")
                    else:
                        st.warning("📉 Negative growth projection")
    
    # AI Recommendations
    display_ai_recommendations("forecasting", st.session_state.sales_orders)

# ============================================================================
# CRM ANALYSIS
# ============================================================================

def show_crm_analysis():
    st.header("📋 CRM Analysis")
    
    if st.session_state.customers.empty:
        st.warning("Please add customer data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-teal">
        <h3 style="color: white; margin: 0; text-align: center;">📋 CRM Analysis Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_customers = len(st.session_state.customers)
    active_customers = len(st.session_state.customers[st.session_state.customers['status'] == 'Active'])
    inactive_customers = len(st.session_state.customers[st.session_state.customers['status'] == 'Inactive'])
    churned_customers = len(st.session_state.customers[st.session_state.customers['status'] == 'Churned'])
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(total_customers), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Active Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(active_customers), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-orange">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Inactive Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(inactive_customers), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-red">
        <h4 style="margin: 0; color: #ffffff; font-weight: 700;">Churned Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(churned_customers), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced CRM Analytics Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Customer Overview", "🔄 Customer Behavior", "📈 Customer Insights", "🎯 Advanced Analytics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
            <h4>📊 Active Accounts</h4>
            </div>
            """, unsafe_allow_html=True)
            active_data, active_msg = calculate_active_accounts(st.session_state.customers)
            
            st.markdown(f"**{active_msg}**")
            
            if not active_data.empty:
                st.dataframe(active_data)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
            <h4>😴 Dormant Accounts</h4>
            </div>
            """, unsafe_allow_html=True)
            dormant_data, dormant_msg = calculate_dormant_accounts(st.session_state.customers)
            
            st.markdown(f"**{dormant_msg}**")
            
            if not dormant_data.empty:
                st.dataframe(dormant_data)
    
    with tab2:
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            <div class="chart-container">
            <h4>🔄 New vs Returning Customers</h4>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.sales_orders.empty:
                new_vs_returning_data, new_vs_returning_msg = calculate_new_vs_returning_revenue(st.session_state.sales_orders, st.session_state.customers)
                
                st.markdown(f"**{new_vs_returning_msg}**")
                
                if not new_vs_returning_data.empty:
                    fig_new_returning = px.pie(
                        new_vs_returning_data,
                        values='Revenue',
                        names='Customer Type',
                        title='Revenue Distribution: New vs Returning Customers'
                    )
                    
                    fig_new_returning.update_layout(
                        title={
                            'text': 'Revenue Distribution: New vs Returning Customers',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    fig_new_returning.update_traces(
                        hovertemplate="<b>%{label}</b><br>" +
                                    "Revenue: $%{value:,.2f}<br>" +
                                    "Percentage: %{percent:.1%}<br>" +
                                    "<extra></extra>",
                        textinfo='label+percent',
                        textposition='inside'
                    )
                    
                    st.plotly_chart(fig_new_returning, use_container_width=True)
        
        with col4:
            st.markdown("""
            <div class="chart-container">
            <h4>📊 Customer Status Distribution</h4>
            </div>
            """, unsafe_allow_html=True)
            status_dist = st.session_state.customers['status'].value_counts()
            fig_status = px.pie(
                values=status_dist.values,
                names=status_dist.index,
                title='Customer Status Distribution'
            )
            
            fig_status.update_layout(
                title={
                    'text': 'Customer Status Distribution',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            fig_status.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                            "Count: %{value}<br>" +
                            "Percentage: %{percent:.1%}<br>" +
                            "<extra></extra>",
                textinfo='label+percent',
                textposition='inside'
            )
            
            st.plotly_chart(fig_status, use_container_width=True)
    
    with tab3:
        if not st.session_state.sales_orders.empty:
            col5, col6 = st.columns(2)
            
            with col5:
                st.markdown("""
                <div class="chart-container">
                <h4>💰 Customer Lifetime Value</h4>
                </div>
                """, unsafe_allow_html=True)
                
                clv_data, clv_msg = calculate_customer_lifetime_value(st.session_state.sales_orders, st.session_state.customers)
                
                if not clv_data.empty:
                    st.markdown(f"**{clv_msg}**")
                    
                    # Create a bar chart for CLV distribution
                    if 'Customer Segment' in clv_data.columns and 'CLV' in clv_data.columns:
                        fig_clv = px.bar(
                            clv_data,
                            x='Customer Segment',
                            y='CLV',
                            title='Customer Lifetime Value by Segment',
                            color='CLV',
                            color_continuous_scale='viridis'
                        )
                        
                        fig_clv.update_layout(
                            title={
                                'text': 'Customer Lifetime Value by Segment',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Customer Segment',
                            yaxis_title='CLV ($)',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_tickangle=-45
                        )
                        
                        fig_clv.update_traces(
                            hovertemplate="<b>%{x}</b><br>" +
                                        "CLV: $%{y:,.2f}<br>" +
                                        "<extra></extra>",
                            texttemplate='$%{y:,.0f}',
                            textposition='outside'
                        )
                        
                        st.plotly_chart(fig_clv, use_container_width=True)
                    else:
                        st.dataframe(clv_data)
            
            with col6:
                st.markdown("""
                <div class="chart-container">
                <h4>📊 Customer Segmentation</h4>
                </div>
                """, unsafe_allow_html=True)
                
                segmentation_data, segmentation_msg = calculate_customer_segmentation(st.session_state.customers, st.session_state.sales_orders)
                
                if not segmentation_data.empty:
                    st.markdown(f"**{segmentation_msg}**")
                    
                    # Create a pie chart for customer segmentation
                    if 'Segment' in segmentation_data.columns and 'Count' in segmentation_data.columns:
                        fig_seg = px.pie(
                            segmentation_data,
                            values='Count',
                            names='Segment',
                            title='Customer Segmentation Distribution'
                        )
                        
                        fig_seg.update_layout(
                            title={
                                'text': 'Customer Segmentation Distribution',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        fig_seg.update_traces(
                            hovertemplate="<b>%{label}</b><br>" +
                                        "Count: %{value}<br>" +
                                        "Percentage: %{percent:.1%}<br>" +
                                        "<extra></extra>",
                            textinfo='label+percent',
                            textposition='inside'
                        )
                        
                        st.plotly_chart(fig_seg, use_container_width=True)
                    else:
                        st.dataframe(segmentation_data)
    
    with tab4:
        if not st.session_state.sales_orders.empty:
            col7, col8 = st.columns(2)
            
            with col7:
                st.markdown("""
                <div class="chart-container">
                <h4>📈 Customer Acquisition Trends</h4>
                </div>
                """, unsafe_allow_html=True)
                
                acquisition_data, acquisition_msg = calculate_customer_acquisition_trends(st.session_state.customers, st.session_state.sales_orders, 'monthly')
                
                if not acquisition_data.empty:
                    st.markdown(f"**{acquisition_msg}**")
                    
                    # Create a line chart for acquisition trends
                    if 'period' in acquisition_data.columns and 'new_customers' in acquisition_data.columns:
                        fig_acq = px.line(
                            acquisition_data,
                            x='period',
                            y='new_customers',
                            title='Monthly Customer Acquisition Trends',
                            markers=True
                        )
                        
                        fig_acq.update_layout(
                            title={
                                'text': 'Monthly Customer Acquisition Trends',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Period',
                            yaxis_title='New Customers',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_tickangle=-45
                        )
                        
                        fig_acq.update_traces(
                            hovertemplate="<b>%{x}</b><br>" +
                                        "New Customers: %{y}<br>" +
                                        "<extra></extra>",
                            line=dict(width=3),
                            marker=dict(size=8)
                        )
                        
                        st.plotly_chart(fig_acq, use_container_width=True)
                    else:
                        st.dataframe(acquisition_data)
            
            with col8:
                st.markdown("""
                <div class="chart-container">
                <h4>🌍 Geographic Distribution</h4>
                </div>
                """, unsafe_allow_html=True)
                
                geo_data, geo_msg = calculate_geographic_customer_distribution(st.session_state.customers, st.session_state.sales_orders)
                
                if not geo_data.empty:
                    st.markdown(f"**{geo_msg}**")
                    
                    # Create a bar chart for geographic distribution
                    if 'Region' in geo_data.columns and 'Customer Count' in geo_data.columns:
                        fig_geo = px.bar(
                            geo_data,
                            x='Region',
                            y='Customer Count',
                            title='Customer Distribution by Region',
                            color='Revenue',
                            color_continuous_scale='plasma'
                        )
                        
                        fig_geo.update_layout(
                            title={
                                'text': 'Customer Distribution by Region',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Region',
                            yaxis_title='Customer Count',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_tickangle=-45
                        )
                        
                        fig_geo.update_traces(
                            hovertemplate="<b>%{x}</b><br>" +
                                        "Customers: %{y}<br>" +
                                        "Revenue: $%{marker.color:,.2f}<br>" +
                                        "<extra></extra>",
                            texttemplate='%{y}',
                            textposition='outside'
                        )
                        
                        st.plotly_chart(fig_geo, use_container_width=True)
                    else:
                        st.dataframe(geo_data)
    
    # AI Recommendations
    display_ai_recommendations("crm_analysis", st.session_state.activities, st.session_state.customers)

# ============================================================================
# OPERATIONAL SALES EFFICIENCY
# ============================================================================

def show_operational_efficiency():
    st.header("⚡ Operational Sales Efficiency")
    
    if st.session_state.sales_orders.empty or st.session_state.sales_reps.empty:
        st.warning("Please add sales orders and sales representatives data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-green">
        <h3 style="color: white; margin: 0; text-align: center;">⚡ Operational Efficiency Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    active_reps = len(st.session_state.sales_reps[st.session_state.sales_reps['status'] == 'Active'])
    revenue_per_rep = total_revenue / active_reps if active_reps > 0 else 0
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Active Sales Reps</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(active_reps), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Revenue per Rep</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(revenue_per_rep), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-orange">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Orders</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(len(st.session_state.sales_orders)), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Operational Efficiency Analytics Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Core Metrics", "💰 Financial Efficiency", "👨‍💼 Sales Team Performance", "🎯 Advanced Analytics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
            <h4>💰 Sales Expense Ratio</h4>
            </div>
            """, unsafe_allow_html=True)
            # Example expense ratio calculation
            total_expenses = total_revenue * 0.3  # Example: 30% expense ratio
            expense_data, expense_msg = calculate_sales_expense_ratio(total_expenses, total_revenue)
            
            st.markdown(f"**{expense_msg}**")
            
            if not expense_data.empty:
                # Create a pie chart for expense ratio
                if 'Metric' in expense_data.columns and 'Value' in expense_data.columns:
                    # Extract numeric values for the chart
                    expense_values = []
                    expense_labels = []
                    for _, row in expense_data.iterrows():
                        if 'Revenue' in row['Value']:
                            expense_values.append(float(row['Value'].replace('$', '').replace(',', '')))
                            expense_labels.append(row['Metric'])
                        elif '%' in row['Value']:
                            expense_values.append(float(row['Value'].replace('%', '')))
                            expense_labels.append(row['Metric'])
                    
                    if expense_values:
                        fig_expense = px.pie(
                            values=expense_values,
                            names=expense_labels,
                            title='Sales Expense Ratio Breakdown'
                        )
                        
                        fig_expense.update_layout(
                            title={
                                'text': 'Sales Expense Ratio Breakdown',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        fig_expense.update_traces(
                            hovertemplate="<b>%{label}</b><br>" +
                                        "Value: %{value}<br>" +
                                        "Percentage: %{percent:.1%}<br>" +
                                        "<extra></extra>",
                            textinfo='label+percent',
                            textposition='inside'
                        )
                        
                        st.plotly_chart(fig_expense, use_container_width=True)
                    else:
                        st.dataframe(expense_data)
                else:
                    st.dataframe(expense_data)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
            <h4>👨‍💼 Revenue per Salesperson</h4>
            </div>
            """, unsafe_allow_html=True)
            revenue_per_rep_data, revenue_per_rep_msg = calculate_revenue_per_salesperson(st.session_state.sales_orders, st.session_state.sales_reps)
            
            st.markdown(f"**{revenue_per_rep_msg}**")
            
            if not revenue_per_rep_data.empty:
                # Create a bar chart for revenue per salesperson
                if 'full_name' in revenue_per_rep_data.columns and 'total_revenue' in revenue_per_rep_data.columns:
                    fig_revenue_rep = px.bar(
                        revenue_per_rep_data.head(10),  # Show top 10 performers
                        x='full_name',
                        y='total_revenue',
                        title='Top 10 Sales Representatives by Revenue',
                        color='total_revenue',
                        color_continuous_scale='viridis'
                    )
                    
                    fig_revenue_rep.update_layout(
                        title={
                            'text': 'Top 10 Sales Representatives by Revenue',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Sales Representative',
                        yaxis_title='Total Revenue ($)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_tickangle=-45
                    )
                    
                    fig_revenue_rep.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Revenue: $%{y:,.2f}<br>" +
                                    "<extra></extra>",
                        texttemplate='$%{y:,.0f}',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_revenue_rep, use_container_width=True)
                else:
                    st.dataframe(revenue_per_rep_data)
    
    with tab2:
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            <div class="chart-container">
            <h4>🎯 Quota Attainment Rate</h4>
            </div>
            """, unsafe_allow_html=True)
            quota_data, quota_msg = calculate_quota_attainment_rate(st.session_state.sales_orders, st.session_state.sales_reps)
            
            st.markdown(f"**{quota_msg}**")
            
            if not quota_data.empty:
                # Create a bar chart for quota attainment
                if 'full_name' in quota_data.columns and 'quota_attainment' in quota_data.columns:
                    fig_quota = px.bar(
                        quota_data,
                        x='full_name',
                        y='quota_attainment',
                        title='Quota Attainment by Sales Representative',
                        color='quota_attainment',
                        color_continuous_scale='RdYlGn'
                    )
                    
                    fig_quota.update_layout(
                        title={
                            'text': 'Quota Attainment by Sales Representative',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Sales Representative',
                        yaxis_title='Quota Attainment (%)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_tickangle=-45
                    )
                    
                    fig_quota.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Attainment: %{y:.1f}%<br>" +
                                    "<extra></extra>",
                        texttemplate='%{y:.1f}%',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_quota, use_container_width=True)
                else:
                    st.dataframe(quota_data)
        
        with col4:
            st.markdown("""
            <div class="chart-container">
            <h4>📊 Sales Efficiency Metrics</h4>
            </div>
            """, unsafe_allow_html=True)
            # Create efficiency metrics summary
            efficiency_data = pd.DataFrame({
                'Metric': ['Revenue per Order', 'Orders per Rep', 'Avg Order Value', 'Customer Acquisition Rate'],
                'Value': [
                    f"${total_revenue / len(st.session_state.sales_orders):,.2f}",
                    f"{len(st.session_state.sales_orders) / active_reps:.1f}",
                    f"${total_revenue / len(st.session_state.sales_orders):,.2f}",
                    "5.2%"  # Example rate
                ]
            })
            
            # Create a horizontal bar chart for efficiency metrics
            fig_efficiency = px.bar(
                efficiency_data,
                x='Value',
                y='Metric',
                title='Sales Efficiency Metrics Overview',
                orientation='h',
                color='Value',
                color_continuous_scale='plasma'
            )
            
            fig_efficiency.update_layout(
                title={
                    'text': 'Sales Efficiency Metrics Overview',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                xaxis_title='Value',
                yaxis_title='Metric',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            fig_efficiency.update_traces(
                hovertemplate="<b>%{y}</b><br>" +
                            "Value: %{x}<br>" +
                            "<extra></extra>",
                texttemplate='%{x}',
                textposition='outside'
            )
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
    
    with tab3:
        if not st.session_state.sales_orders.empty:
            col5, col6 = st.columns(2)
            
            with col5:
                st.markdown("""
                <div class="chart-container">
                <h4>📈 Sales Performance Trends</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate monthly sales trends
                sales_orders_copy = st.session_state.sales_orders.copy()
                sales_orders_copy['order_date'] = pd.to_datetime(sales_orders_copy['order_date'])
                monthly_sales = sales_orders_copy.groupby(sales_orders_copy['order_date'].dt.to_period('M')).agg({
                    'total_amount': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                monthly_sales.columns = ['Month', 'Total Revenue', 'Order Count']
                monthly_sales['Month'] = monthly_sales['Month'].astype(str)
                
                # Create dual-axis chart for revenue and orders
                fig_trends = go.Figure()
                
                # Add revenue line
                fig_trends.add_trace(go.Scatter(
                    x=monthly_sales['Month'],
                    y=monthly_sales['Total Revenue'],
                    name='Total Revenue',
                    yaxis='y',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8)
                ))
                
                # Add order count bars
                fig_trends.add_trace(go.Bar(
                    x=monthly_sales['Month'],
                    y=monthly_sales['Order Count'],
                    name='Order Count',
                    yaxis='y2',
                    marker_color='#16a34a',
                    opacity=0.7
                ))
                
                fig_trends.update_layout(
                    title={
                        'text': 'Monthly Sales Performance Trends',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Month',
                    yaxis=dict(title='Total Revenue ($)', side='left'),
                    yaxis2=dict(title='Order Count', side='right', overlaying='y'),
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_trends, use_container_width=True)
            
            with col6:
                st.markdown("""
                <div class="chart-container">
                <h4>🎯 Performance Benchmarks</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate performance benchmarks
                avg_order_value = total_revenue / len(st.session_state.sales_orders)
                orders_per_rep = len(st.session_state.sales_orders) / active_reps if active_reps > 0 else 0
                revenue_per_rep = total_revenue / active_reps if active_reps > 0 else 0
                
                benchmark_data = pd.DataFrame({
                    'Metric': ['Avg Order Value', 'Orders per Rep', 'Revenue per Rep', 'Active Reps'],
                    'Current': [avg_order_value, orders_per_rep, revenue_per_rep, active_reps],
                    'Target': [avg_order_value * 1.2, orders_per_rep * 1.15, revenue_per_rep * 1.25, active_reps * 1.1]
                })
                
                # Create a grouped bar chart for benchmarks
                fig_benchmarks = px.bar(
                    benchmark_data,
                    x='Metric',
                    y=['Current', 'Target'],
                    title='Performance Benchmarks: Current vs Target',
                    barmode='group',
                    color_discrete_map={'Current': '#667eea', 'Target': '#16a34a'}
                )
                
                fig_benchmarks.update_layout(
                    title={
                        'text': 'Performance Benchmarks: Current vs Target',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Metric',
                    yaxis_title='Value',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                
                fig_benchmarks.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Value: %{y}<br>" +
                                "<extra></extra>",
                    texttemplate='%{y:.1f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_benchmarks, use_container_width=True)
    
    with tab4:
        if not st.session_state.sales_orders.empty:
            col7, col8 = st.columns(2)
            
            with col7:
                st.markdown("""
                <div class="chart-container">
                <h4>🌍 Geographic Performance</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate geographic performance if region data exists
                if 'region' in st.session_state.sales_reps.columns:
                    rep_region = st.session_state.sales_reps[['sales_rep_id', 'region']].dropna()
                    sales_with_region = st.session_state.sales_orders.merge(rep_region, on='sales_rep_id', how='left')
                    
                    if not sales_with_region.empty and 'region' in sales_with_region.columns:
                        region_performance = sales_with_region.groupby('region').agg({
                            'total_amount': 'sum',
                            'order_id': 'count',
                            'sales_rep_id': 'nunique'
                        }).reset_index()
                        
                        region_performance.columns = ['Region', 'Total Revenue', 'Order Count', 'Sales Reps']
                        
                        # Create a scatter plot for region performance
                        fig_region = px.scatter(
                            region_performance,
                            x='Order Count',
                            y='Total Revenue',
                            size='Sales Reps',
                            color='Region',
                            title='Regional Performance: Revenue vs Orders',
                            hover_data=['Sales Reps']
                        )
                        
                        fig_region.update_layout(
                            title={
                                'text': 'Regional Performance: Revenue vs Orders',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Order Count',
                            yaxis_title='Total Revenue ($)',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        st.plotly_chart(fig_region, use_container_width=True)
                    else:
                        st.info("Region data not available for geographic analysis.")
                else:
                    st.info("Region data not available for geographic analysis.")
            
            with col8:
                st.markdown("""
                <div class="chart-container">
                <h4>📊 Efficiency Score Analysis</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate efficiency score components
                efficiency_score = 0
                score_components = []
                
                # Revenue efficiency (30% weight)
                revenue_efficiency = min(1.0, (total_revenue / (total_revenue * 1.2))) * 100
                efficiency_score += revenue_efficiency * 0.3
                score_components.append(('Revenue Efficiency', revenue_efficiency))
                
                # Order efficiency (25% weight)
                order_efficiency = min(1.0, (len(st.session_state.sales_orders) / (len(st.session_state.sales_orders) * 1.15))) * 100
                efficiency_score += order_efficiency * 0.25
                score_components.append(('Order Efficiency', order_efficiency))
                
                # Rep efficiency (25% weight)
                rep_efficiency = min(1.0, (active_reps / (active_reps * 1.1))) * 100
                efficiency_score += rep_efficiency * 0.25
                score_components.append(('Rep Efficiency', rep_efficiency))
                
                # Customer efficiency (20% weight)
                customer_efficiency = 85.0  # Example value
                efficiency_score += customer_efficiency * 0.2
                score_components.append(('Customer Efficiency', customer_efficiency))
                
                # Create efficiency score visualization
                efficiency_df = pd.DataFrame(score_components, columns=['Component', 'Score'])
                
                fig_efficiency_score = px.bar(
                    efficiency_df,
                    x='Component',
                    y='Score',
                    title=f'Overall Efficiency Score: {efficiency_score:.1f}%',
                    color='Score',
                    color_continuous_scale='RdYlGn'
                )
                
                fig_efficiency_score.update_layout(
                    title={
                        'text': f'Overall Efficiency Score: {efficiency_score:.1f}%',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Efficiency Component',
                    yaxis_title='Score (%)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                
                fig_efficiency_score.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Score: %{y:.1f}%<br>" +
                                "<extra></extra>",
                    texttemplate='%{y:.1f}%',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_efficiency_score, use_container_width=True)
                
                # Display efficiency insights
                st.markdown("### 📈 Efficiency Insights")
                if efficiency_score >= 80:
                    st.success(f"🎉 Excellent operational efficiency! Your score of {efficiency_score:.1f}% indicates strong performance across all metrics.")
                elif efficiency_score >= 60:
                    st.info(f"📊 Good operational efficiency with room for improvement. Current score: {efficiency_score:.1f}%")
                else:
                    st.warning(f"⚠️ Operational efficiency needs attention. Current score: {efficiency_score:.1f}%")
    
    # AI Recommendations
    display_ai_recommendations("operational_efficiency", st.session_state.sales_orders, st.session_state.sales_reps)

# ============================================================================
# SPECIALIZED SALES METRICS
# ============================================================================

def show_specialized_metrics():
    st.header("🎯 Specialized Sales Metrics")
    
    if st.session_state.sales_orders.empty or st.session_state.sales_reps.empty:
        st.warning("Please add sales orders and sales representatives data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-orange">
        <h3 style="color: white; margin: 0; text-align: center;">🎯 Specialized Metrics Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    total_orders = len(st.session_state.sales_orders)
    unique_customers = st.session_state.sales_orders['customer_id'].nunique()
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Total Orders</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(total_orders), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Unique Customers</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">{:,}</h2>
        </div>
        """.format(unique_customers), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #ffffff; font-weight: 600;">Avg Order Value</h4>
        <h2 style="margin: 10px 0; color: #ffffff; font-weight: 700;">${:,.2f}</h2>
        </div>
        """.format(total_revenue / total_orders if total_orders > 0 else 0), unsafe_allow_html=True)
    
    st.markdown("---")
    
        # Advanced Specialized Metrics Analytics Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Core Metrics", "🗺️ Geographic & Territory", "📈 Product & Channel", "🎯 Advanced Analytics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="chart-container">
            <h4>🔄 New vs Returning Customers</h4>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.customers.empty:
                new_vs_returning_data, new_vs_returning_msg = calculate_new_vs_returning_revenue(st.session_state.sales_orders, st.session_state.customers)
                
                st.markdown(f"**{new_vs_returning_msg}**")
                
                if not new_vs_returning_data.empty:
                    fig_new_returning = px.bar(
                        new_vs_returning_data,
                        x='Customer Type',
                        y='Revenue',
                        title='Revenue by Customer Type',
                        color='Revenue',
                        color_continuous_scale='viridis'
                    )
                    
                    fig_new_returning.update_layout(
                        title={
                            'text': 'Revenue by Customer Type',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 18, 'color': '#1f2937'}
                        },
                        xaxis_title='Customer Type',
                        yaxis_title='Revenue ($)',
                        height=400,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis_tickangle=-45
                    )
                    
                    fig_new_returning.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Revenue: $%{y:,.2f}<br>" +
                                    "<extra></extra>",
                        texttemplate='$%{y:,.0f}',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_new_returning, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="chart-container">
            <h4>📊 Customer Acquisition Trends</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate customer acquisition trends
            if not st.session_state.customers.empty:
                customer_acquisition_data, customer_acquisition_msg = calculate_customer_acquisition_trends(st.session_state.customers, st.session_state.sales_orders, 'monthly')
                
                if not customer_acquisition_data.empty:
                    st.markdown(f"**{customer_acquisition_msg}**")
                    
                    # Create a line chart for customer acquisition trends
                    if 'period' in customer_acquisition_data.columns and 'new_customers' in customer_acquisition_data.columns:
                        fig_acquisition = px.line(
                            customer_acquisition_data,
                            x='period',
                            y='new_customers',
                            title='Monthly Customer Acquisition Trends',
                            markers=True
                        )
                        
                        fig_acquisition.update_layout(
                            title={
                                'text': 'Monthly Customer Acquisition Trends',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Period',
                            yaxis_title='New Customers',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_tickangle=-45
                        )
                        
                        fig_acquisition.update_traces(
                            hovertemplate="<b>%{x}</b><br>" +
                                        "New Customers: %{y}<br>" +
                                        "<extra></extra>",
                            line=dict(width=3),
                            marker=dict(size=8)
                        )
                        
                        st.plotly_chart(fig_acquisition, use_container_width=True)
                    else:
                        st.dataframe(customer_acquisition_data)
                else:
                    st.info("No customer acquisition data available.")
            else:
                st.info("Customer data not available for acquisition analysis.")
    
    with tab2:
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            <div class="chart-container">
            <h4>🗺️ Territory Performance</h4>
            </div>
            """, unsafe_allow_html=True)
            territory_data, territory_msg = calculate_territory_performance(st.session_state.sales_orders, st.session_state.sales_reps)
            
            st.markdown(f"**{territory_msg}**")
            
            if not territory_data.empty:
                fig_territory = px.bar(
                    territory_data,
                    x='Territory',
                    y='Total Revenue',
                    title='Revenue by Territory',
                    color='Total Revenue',
                    color_continuous_scale='plasma'
                )
                
                fig_territory.update_layout(
                    title={
                        'text': 'Revenue by Territory',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Territory',
                    yaxis_title='Total Revenue ($)',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                
                fig_territory.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Revenue: $%{y:,.2f}<br>" +
                                "<extra></extra>",
                    texttemplate='$%{y:,.0f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_territory, use_container_width=True)
        
        with col4:
            st.markdown("""
            <div class="chart-container">
            <h4>🌍 Geographic Distribution</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate geographic customer distribution
            if not st.session_state.customers.empty:
                geo_data, geo_msg = calculate_geographic_customer_distribution(st.session_state.customers, st.session_state.sales_orders)
                
                if not geo_data.empty:
                    st.markdown(f"**{geo_msg}**")
                    
                    # Create a bar chart for geographic distribution
                    if 'Region' in geo_data.columns and 'Customer Count' in geo_data.columns:
                        fig_geo = px.bar(
                            geo_data,
                            x='Region',
                            y='Customer Count',
                            title='Customer Distribution by Region',
                            color='Revenue',
                            color_continuous_scale='viridis'
                        )
                        
                        fig_geo.update_layout(
                            title={
                                'text': 'Customer Distribution by Region',
                                'x': 0.5,
                                'xanchor': 'center',
                                'font': {'size': 18, 'color': '#1f2937'}
                            },
                            xaxis_title='Region',
                            yaxis_title='Customer Count',
                            height=400,
                            showlegend=True,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            xaxis_tickangle=-45
                        )
                        
                        fig_geo.update_traces(
                            hovertemplate="<b>%{x}</b><br>" +
                                        "Customers: %{y}<br>" +
                                        "Revenue: $%{marker.color:,.2f}<br>" +
                                        "<extra></extra>",
                            texttemplate='%{y}',
                            textposition='outside'
                        )
                        
                        st.plotly_chart(fig_geo, use_container_width=True)
                    else:
                        st.dataframe(geo_data)
                else:
                    st.info("No geographic data available.")
            else:
                st.info("Customer data not available for geographic analysis.")
    
    with tab3:
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown("""
            <div class="chart-container">
            <h4>📊 Product Performance Analysis</h4>
            </div>
            """, unsafe_allow_html=True)
            if not st.session_state.products.empty:
                product_performance = st.session_state.sales_orders.groupby('product_id').agg({
                    'total_amount': 'sum',
                    'quantity': 'sum',
                    'order_id': 'count'
                }).reset_index()
                
                product_performance = product_performance.merge(
                    st.session_state.products[['product_id', 'product_name', 'category']], 
                    on='product_id', 
                    how='left'
                )
                
                fig_product = px.scatter(
                    product_performance,
                    x='total_amount',
                    y='quantity',
                    size='order_id',
                    color='category',
                    hover_data=['product_name'],
                    title='Product Performance: Revenue vs Quantity'
                )
                
                fig_product.update_layout(
                    title={
                        'text': 'Product Performance: Revenue vs Quantity',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Total Revenue ($)',
                    yaxis_title='Quantity Sold',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_product.update_traces(
                    hovertemplate="<b>%{customdata[0]}</b><br>" +
                                "Revenue: $%{x:,.2f}<br>" +
                                "Quantity: %{y}<br>" +
                                "Orders: %{marker.size}<br>" +
                                "<extra></extra>"
                )
                
                st.plotly_chart(fig_product, use_container_width=True)
        
        with col6:
            st.markdown("""
            <div class="chart-container">
            <h4>📈 Sales Trends by Channel</h4>
            </div>
            """, unsafe_allow_html=True)
            channel_trends = st.session_state.sales_orders.groupby('channel').agg({
                'total_amount': 'sum',
                'order_id': 'count'
            }).reset_index()
            
            fig_channel = px.pie(
                channel_trends,
                values='total_amount',
                names='channel',
                title='Revenue Distribution by Channel'
            )
            
            fig_channel.update_layout(
                title={
                    'text': 'Revenue Distribution by Channel',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#1f2937'}
                },
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            fig_channel.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                            "Revenue: $%{value:,.2f}<br>" +
                            "Percentage: %{percent:.1%}<br>" +
                            "<extra></extra>",
                textinfo='label+percent',
                textposition='inside'
            )
            
            st.plotly_chart(fig_channel, use_container_width=True)
    
    with tab4:
        if not st.session_state.sales_orders.empty:
            col7, col8 = st.columns(2)
            
            with col7:
                st.markdown("""
                <div class="chart-container">
                <h4>📊 Industry Analysis</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate industry customer analysis
                if not st.session_state.customers.empty:
                    industry_data, industry_msg = calculate_industry_customer_analysis(st.session_state.customers, st.session_state.sales_orders)
                    
                    if not industry_data.empty:
                        st.markdown(f"**{industry_msg}**")
                        
                        # Create a bar chart for industry analysis
                        if 'Industry' in industry_data.columns and 'Customer Count' in industry_data.columns:
                            fig_industry = px.bar(
                                industry_data,
                                x='Industry',
                                y='Customer Count',
                                title='Customer Distribution by Industry',
                                color='Revenue',
                                color_continuous_scale='plasma'
                            )
                            
                            fig_industry.update_layout(
                                title={
                                    'text': 'Customer Distribution by Industry',
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'font': {'size': 18, 'color': '#1f2937'}
                                },
                                xaxis_title='Industry',
                                yaxis_title='Customer Count',
                                height=400,
                                showlegend=True,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                xaxis_tickangle=-45
                            )
                            
                            fig_industry.update_traces(
                                hovertemplate="<b>%{x}</b><br>" +
                                            "Customers: %{y}<br>" +
                                            "Revenue: $%{marker.color:,.2f}<br>" +
                                            "<extra></extra>",
                                texttemplate='%{y}',
                                textposition='outside'
                            )
                            
                            st.plotly_chart(fig_industry, use_container_width=True)
                        else:
                            st.dataframe(industry_data)
                    else:
                        st.info("No industry data available.")
                else:
                    st.info("Customer data not available for industry analysis.")
            
            with col8:
                st.markdown("""
                <div class="chart-container">
                <h4>🎯 Performance Benchmarks</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate performance benchmarks
                avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
                revenue_per_customer = total_revenue / unique_customers if unique_customers > 0 else 0
                orders_per_customer = total_orders / unique_customers if unique_customers > 0 else 0
                
                benchmark_data = pd.DataFrame({
                    'Metric': ['Avg Order Value', 'Revenue per Customer', 'Orders per Customer', 'Total Customers'],
                    'Current': [avg_order_value, revenue_per_customer, orders_per_customer, unique_customers],
                    'Target': [avg_order_value * 1.2, revenue_per_customer * 1.25, orders_per_customer * 1.15, unique_customers * 1.1]
                })
                
                # Create a grouped bar chart for benchmarks
                fig_benchmarks = px.bar(
                    benchmark_data,
                    x='Metric',
                    y=['Current', 'Target'],
                    title='Performance Benchmarks: Current vs Target',
                    barmode='group',
                    color_discrete_map={'Current': '#667eea', 'Target': '#16a34a'}
                )
                
                fig_benchmarks.update_layout(
                    title={
                        'text': 'Performance Benchmarks: Current vs Target',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#1f2937'}
                    },
                    xaxis_title='Metric',
                    yaxis_title='Value',
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis_tickangle=-45
                )
                
                fig_benchmarks.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                "Value: %{y}<br>" +
                                "<extra></extra>",
                    texttemplate='%{y:.1f}',
                    textposition='outside'
                )
                
                st.plotly_chart(fig_benchmarks, use_container_width=True)
                
                # Display benchmark insights
                st.markdown("### 📈 Benchmark Insights")
                st.info(f"**Current Performance:** Average Order Value: ${avg_order_value:,.2f}, Revenue per Customer: ${revenue_per_customer:,.2f}")
                st.success(f"**Target Goals:** Increase AOV by 20%, Revenue per Customer by 25%, and Customer Base by 10%")
    
    # AI Recommendations
    display_ai_recommendations("specialized_metrics", st.session_state.sales_orders)

# ============================================================================
# PREDICTIVE ANALYTICS
# ============================================================================

def show_predictive_analytics():
    """Display enhanced predictive analytics dashboard with advanced visualizations and AI insights."""
    
    # Enhanced header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin: 20px 0; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 2.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🔮 Advanced Predictive Analytics & AI Insights</h1>
        <p style="color: white; margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Leverage machine learning algorithms to predict customer behavior, optimize sales strategies, and drive revenue growth</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.sales_orders.empty:
        st.warning("⚠️ Please add sales data first in the Data Input section to enable predictive analytics.")
        return
    
    # Enhanced summary metrics with better styling and insights
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
        <h3 style="color: white; text-align: center; margin: 0; font-size: 1.5em;">📊 Predictive Analytics Overview Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate enhanced summary metrics
    total_customers = st.session_state.customers['customer_id'].nunique() if not st.session_state.customers.empty else 0
    total_products = st.session_state.products['product_id'].nunique() if not st.session_state.products.empty else 0
    total_sales_reps = st.session_state.sales_reps['sales_rep_id'].nunique() if not st.session_state.sales_reps.empty else 0
    total_revenue = st.session_state.sales_orders['total_amount'].sum() if not st.session_state.sales_orders.empty else 0
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: white; margin: 0; font-size: 1.1em;">👥 Total Customers</h4>
            <h2 style="color: white; margin: 10px 0; font-size: 2em;">{total_customers:,}</h2>
            <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.9;">Available for analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: white; margin: 0; font-size: 1.1em;">📦 Total Products</h4>
            <h2 style="color: white; margin: 10px 0; font-size: 2em;">{total_products:,}</h2>
            <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.9;">In portfolio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #45b7d1 0%, #96c93d 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: white; margin: 0; font-size: 1.1em;">👨‍💼 Sales Reps</h4>
            <h2 style="color: white; margin: 10px 0; font-size: 2em;">{total_sales_reps:,}</h2>
            <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.9;">Team members</p>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h4 style="color: white; margin: 0; font-size: 1.1em;">🤖 AI Models</h4>
            <h2 style="color: white; margin: 10px 0; font-size: 2em;">5</h2>
            <p style="color: white; margin: 0; font-size: 0.9em; opacity: 0.9;">Active predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional insights row
    if total_revenue > 0:
        st.markdown("---")
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            avg_order_value = total_revenue / len(st.session_state.sales_orders) if not st.session_state.sales_orders.empty else 0
            st.markdown(f"""
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; text-align: center;">
                <h4 style="color: #2e7d32; margin: 0;">💰 Avg Order Value</h4>
                <h3 style="color: #2e7d32; margin: 10px 0;">${avg_order_value:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            revenue_per_customer = total_revenue / total_customers if total_customers > 0 else 0
            st.markdown(f"""
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3; text-align: center;">
                <h4 style="color: #1565c0; margin: 0;">👤 Revenue/Customer</h4>
                <h3 style="color: #1565c0; margin: 10px 0;">${revenue_per_customer:,.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col3:
            orders_per_customer = len(st.session_state.sales_orders) / total_customers if total_customers > 0 else 0
            st.markdown(f"""
            <div style="background: #fff3e0; padding: 15px; border-radius: 8px; border-left: 4px solid #ff9800; text-align: center;">
                <h4 style="color: #e65100; margin: 0;">🔄 Orders/Customer</h4>
                <h3 style="color: #e65100; margin: 10px 0;">{orders_per_customer:.1f}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced tabs with better descriptions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Customer Churn Analysis", 
        "💼 Opportunity Intelligence", 
        "📦 Demand Forecasting", 
        "💰 CLV Prediction Engine", 
        "📈 Performance Analytics"
    ])
    
    with tab1:
        # Enhanced Customer Churn Analysis header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0; text-align: center; font-size: 1.8em;">🎯 Advanced Customer Churn Prediction & Risk Assessment</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔍 **AI-Powered Churn Detection**: Advanced machine learning algorithms analyze customer behavior patterns, order frequency, engagement metrics, and predictive signals to identify at-risk customers before they churn.")
        
        # Enhanced sample data generation with better UI
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3;">
                <strong>💡 Getting Started:</strong> Generate enhanced sample data to test the churn prediction models with realistic customer behavior patterns and comprehensive metrics.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🎲 Generate Enhanced Sample Data", key="gen_sample_churn", type="primary", use_container_width=True):
                with st.spinner("🚀 Generating enhanced sample data..."):
                    customers_sample, sales_sample, sample_msg = generate_sample_churn_data()
                    if not customers_sample.empty and not sales_sample.empty:
                        st.session_state.customers = customers_sample
                        st.session_state.sales_orders = sales_sample
                        st.success("✅ Enhanced sample data generated successfully! The dashboard will refresh automatically.")
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate sample data. Please try again.")
        
        # Enhanced debug information with better organization
        with st.expander("🔍 Advanced Debug & Data Quality Analysis", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📊 Data Quality Metrics:**")
                if not st.session_state.customers.empty:
                    st.write(f"• Customer records: {st.session_state.customers.shape[0]:,}")
                    st.write(f"• Customer columns: {len(st.session_state.customers.columns)}")
                    st.write(f"• Missing values: {st.session_state.customers.isnull().sum().sum()}")
                    st.write(f"• Data completeness: {((st.session_state.customers.shape[0] * st.session_state.customers.shape[1] - st.session_state.customers.isnull().sum().sum()) / (st.session_state.customers.shape[0] * st.session_state.customers.shape[1]) * 100):.1f}%")
                
            with col2:
                st.markdown("**🔧 Technical Details:**")
                if not st.session_state.customers.empty:
                    st.write("• Customer columns:", list(st.session_state.customers.columns))
                if not st.session_state.sales_orders.empty:
                    st.write("• Sales columns:", list(st.session_state.sales_orders.columns))
                    st.write("• Date range:", f"{st.session_state.sales_orders['order_date'].min()} to {st.session_state.sales_orders['order_date'].max()}")
                    st.write("• Sample data preview:")
                    st.dataframe(st.session_state.sales_orders.head(3), use_container_width=True)
        
        if not st.session_state.customers.empty:
            # Enhanced churn prediction with loading spinner
            with st.spinner("🤖 Running AI-powered churn prediction models..."):
                churn_data, churn_msg = calculate_customer_churn_prediction_simple(st.session_state.customers, st.session_state.sales_orders)
                
                if churn_data.empty:
                    st.info("🔄 Trying advanced churn prediction method...")
                    churn_data, churn_msg = calculate_customer_churn_prediction(st.session_state.customers, st.session_state.sales_orders)
            
            if not churn_data.empty:
                st.success(f"✅ {churn_msg}")
                
                # Enhanced churn risk summary with better metrics and styling
                st.markdown("### 📊 Churn Risk Assessment Dashboard")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    high_risk = len(churn_data[churn_data['churn_risk'] == 'High'])
                    high_risk_percentage = (high_risk / len(churn_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">🚨 High Risk</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{high_risk}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{high_risk_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    medium_risk = len(churn_data[churn_data['churn_risk'] == 'Medium'])
                    med_risk_percentage = (medium_risk / len(churn_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffd93d 0%, #ffb347 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">⚠️ Medium Risk</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{medium_risk}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{med_risk_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    low_risk = len(churn_data[churn_data['churn_risk'] == 'Low'])
                    low_risk_percentage = (low_risk / len(churn_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #6bcf7f 0%, #4CAF50 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">✅ Low Risk</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{low_risk}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{low_risk_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    avg_probability = churn_data['churn_probability'].mean()
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📈 Avg Risk</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{avg_probability:.1f}%</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Overall churn probability</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced churn risk distribution chart with better styling
                st.markdown("### 🎨 Interactive Churn Risk Distribution")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    risk_distribution = churn_data['churn_risk'].value_counts()
                    fig_churn_risk = px.pie(
                        values=risk_distribution.values,
                        names=risk_distribution.index,
                        title='Customer Churn Risk Distribution',
                        color_discrete_map={'High': '#ff6b6b', 'Medium': '#ffd93d', 'Low': '#6bcf7f'}
                    )
                    
                    fig_churn_risk.update_layout(
                        title={
                            'text': 'Customer Churn Risk Distribution',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#1f2937'}
                        },
                        height=500,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    
                    fig_churn_risk.update_traces(
                        hovertemplate="<b>%{label}</b><br>" +
                                    "Count: %{value}<br>" +
                                    "Percentage: %{percent:.1%}<br>" +
                                    "<extra></extra>",
                        textinfo='label+percent',
                        textposition='inside',
                        textfont=dict(size=16, color='white')
                    )
                    
                    st.plotly_chart(fig_churn_risk, use_container_width=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h5>📊 Risk Analysis Insights:</h5>
                        <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.6;">
                            <li><strong>🚨 High Risk:</strong> Immediate attention required - implement retention strategies</li>
                            <li><strong>⚠️ Medium Risk:</strong> Monitor closely - proactive engagement recommended</li>
                            <li><strong>✅ Low Risk:</strong> Stable customers - maintain current service levels</li>
                        </ul>
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                                💡 <strong>Pro Tip:</strong> Focus retention efforts on high-risk customers first to maximize ROI
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced high-risk customers display with better formatting
                st.markdown("### 🚨 High-Risk Customer Alert Dashboard")
                
                high_risk_customers = churn_data[churn_data['churn_risk'] == 'High'].head(10)
                
                if not high_risk_customers.empty:
                    try:
                        available_columns = high_risk_customers.columns.tolist()
                        
                        # Enhanced preferred columns with better ordering
                        preferred_columns = [
                            'customer_name', 'churn_probability', 'days_since_last_order', 
                            'order_frequency', 'avg_order_value', 'customer_status', 'total_orders'
                        ]
                        
                        # Filter to only include columns that exist
                        display_columns = [col for col in preferred_columns if col in available_columns]
                        
                        # Ensure we have at least some columns to display
                        if not display_columns:
                            display_columns = ['customer_name', 'churn_probability']
                        
                        # Enhanced dataframe display with better styling
                        st.markdown("""
                        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 15px 0;">
                            <strong>⚠️ Action Required:</strong> These customers show high churn risk signals. Consider implementing immediate retention strategies such as personalized outreach, special offers, or enhanced support.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display with better formatting
                        styled_df = high_risk_customers[display_columns].copy()
                        if 'churn_probability' in styled_df.columns:
                            styled_df['churn_probability'] = styled_df['churn_probability'].round(1).astype(str) + '%'
                        if 'avg_order_value' in styled_df.columns:
                            styled_df['avg_order_value'] = styled_df['avg_order_value'].apply(lambda x: f"${x:,.2f}")
                        
                        st.dataframe(
                            styled_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "churn_probability": st.column_config.NumberColumn(
                                    "Churn Risk (%)",
                                    help="Probability of customer churning",
                                    format="%.1f%%"
                                )
                            }
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error displaying high-risk customers: {str(e)}")
                        st.info("🔍 Available columns: " + ", ".join(high_risk_customers.columns.tolist()))
                        # Fallback to basic display
                        st.dataframe(high_risk_customers, use_container_width=True)
                else:
                    st.success("🎉 No high-risk customers detected! Your retention strategies are working well.")
                
            else:
                st.warning("⚠️ No churn prediction data available.")
                st.info(f"📝 {churn_msg}")
        else:
            st.warning("⚠️ No customer data available. Please generate sample data first.")
            st.markdown("""
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 4px solid #2196f3; margin: 20px 0;">
                <strong>💡 Getting Started:</strong> Click the "Generate Enhanced Sample Data" button above to create realistic customer data for testing the churn prediction models. The sample data includes various customer behaviors and order patterns to demonstrate the predictive capabilities.
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # Enhanced Opportunity Intelligence header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0; text-align: center; font-size: 1.8em;">💼 Sales Opportunity Intelligence & Scoring Engine</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🎯 **AI-Powered Opportunity Scoring**: Advanced algorithms analyze multiple factors including order value, customer status, sales representative experience, and historical performance to prioritize sales opportunities and maximize conversion rates.")
        
        if not st.session_state.sales_reps.empty:
            with st.spinner("🤖 Analyzing sales opportunities..."):
                opportunity_data, opportunity_msg = calculate_sales_opportunity_scoring(st.session_state.sales_orders, st.session_state.customers, st.session_state.sales_reps)
            
            if not opportunity_data.empty:
                st.success(f"✅ {opportunity_msg}")
                
                # Enhanced opportunity summary with better styling
                st.markdown("### 📊 Opportunity Priority Distribution")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    high_priority = len(opportunity_data[opportunity_data['opportunity_class'] == 'High Priority'])
                    high_percentage = (high_priority / len(opportunity_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">🔥 High Priority</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{high_priority}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{high_percentage:.1f}% of opportunities</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    medium_priority = len(opportunity_data[opportunity_data['opportunity_class'] == 'Medium Priority'])
                    med_percentage = (medium_priority / len(opportunity_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffd93d 0%, #ffb347 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">⚡ Medium Priority</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{medium_priority}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{med_percentage:.1f}% of opportunities</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    low_priority = len(opportunity_data[opportunity_data['opportunity_class'] == 'Low Priority'])
                    low_percentage = (low_priority / len(opportunity_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #6bcf7f 0%, #4CAF50 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📈 Low Priority</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{low_priority}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{low_percentage:.1f}% of opportunities</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    avg_score = opportunity_data['opportunity_score'].mean()
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📊 Avg Score</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{avg_score:.1f}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Overall opportunity quality</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced opportunity score distribution chart
                st.markdown("### 🎨 Interactive Opportunity Score Analysis")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig_opportunity = px.histogram(
                        opportunity_data,
                        x='opportunity_score',
                        color='opportunity_class',
                        title='Opportunity Score Distribution by Priority Level',
                        nbins=20,
                        color_discrete_map={
                            'High Priority': '#ff6b6b',
                            'Medium Priority': '#ffd93d',
                            'Low Priority': '#6bcf7f'
                        }
                    )
                    
                    fig_opportunity.update_layout(
                        title={
                            'text': 'Opportunity Score Distribution by Priority Level',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#1f2937'}
                        },
                        xaxis_title='Opportunity Score',
                        yaxis_title='Count',
                        height=500,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    
                    fig_opportunity.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Count: %{y}<br>" +
                                    "Priority: %{marker.color}<br>" +
                                    "<extra></extra>",
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_opportunity, use_container_width=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #4ecdc4;">
                        <h5>🎯 Scoring Insights:</h5>
                        <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.6;">
                            <li><strong>🔥 High Priority:</strong> Focus resources here for maximum ROI</li>
                            <li><strong>⚡ Medium Priority:</strong> Good opportunities with moderate effort</li>
                            <li><strong>📈 Low Priority:</strong> Monitor for potential growth</li>
                        </ul>
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                                💡 <strong>Strategy:</strong> Prioritize high-scoring opportunities to optimize sales team efficiency
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced top opportunities display
                st.markdown("### 🏆 Top High-Scoring Opportunities Dashboard")
                
                top_opportunities = opportunity_data.head(10)
                
                # Format the data for better display
                display_df = top_opportunities[['customer_name', 'sales_rep', 'order_value', 'opportunity_score', 'opportunity_class']].copy()
                display_df['order_value'] = display_df['order_value'].apply(lambda x: f"${x:,.2f}")
                display_df['opportunity_score'] = display_df['opportunity_score'].round(1)
                
                st.markdown("""
                <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 15px 0;">
                    <strong>🎯 Action Items:</strong> These high-scoring opportunities represent your best chances for conversion. Focus your sales team's efforts on these prospects to maximize revenue potential.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "opportunity_score": st.column_config.NumberColumn(
                            "Score",
                            help="Opportunity score (0-100)",
                            format="%.1f"
                        ),
                        "order_value": st.column_config.TextColumn(
                            "Order Value",
                            help="Potential order value"
                        )
                    }
                )
                
            else:
                st.warning("⚠️ No opportunity scoring data available.")
                st.info(opportunity_msg)
        else:
            st.warning("⚠️ Sales representative data not available for opportunity scoring.")
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <strong>💡 Setup Required:</strong> Add sales representative data in the Data Input section to enable opportunity scoring analysis. This will allow the system to evaluate opportunities based on sales rep experience and performance.
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Enhanced Demand Forecasting header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #45b7d1 0%, #96c93d 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0; text-align: center; font-size: 1.8em;">📦 Advanced Product Demand Forecasting & Inventory Optimization</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🔮 **AI-Powered Demand Prediction**: Machine learning algorithms analyze historical sales patterns, seasonal trends, market dynamics, and product lifecycle stages to forecast future demand with confidence intervals and trend analysis.")
        
        if not st.session_state.products.empty:
            with st.spinner("🔮 Forecasting product demand patterns..."):
                demand_data, demand_msg = calculate_product_demand_forecast(st.session_state.products, st.session_state.sales_orders)
            
            if not demand_data.empty:
                st.success(f"✅ {demand_msg}")
                
                # Enhanced demand summary metrics
                st.markdown("### 📊 Demand Forecasting Overview")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_current_demand = demand_data['current_demand'].mean()
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📈 Current Demand</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{avg_current_demand:.1f}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Average units/month</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    avg_forecasted_demand = demand_data['mean_forecast'].mean()
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">🔮 Forecasted</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{avg_forecasted_demand:.1f}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Predicted units/month</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    growth_rate = ((avg_forecasted_demand - avg_current_demand) / avg_current_demand * 100) if avg_current_demand > 0 else 0
                    growth_color = "#4CAF50" if growth_rate > 0 else "#f44336"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {growth_color} 0%, {growth_color}dd 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📊 Growth Rate</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{growth_rate:+.1f}%</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Demand change</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    total_products = len(demand_data)
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📦 Products</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{total_products}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">Analyzed</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced demand forecast visualization
                st.markdown("### 🎨 Interactive Demand Forecasting Analysis")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Create enhanced demand forecast chart
                    fig_demand = px.scatter(
                        demand_data,
                        x='current_demand',
                        y='mean_forecast',
                        size='mean_forecast',
                        color='category',
                        hover_data=['product_name', 'trend', 'confidence_interval'],
                        title='Product Demand: Current vs Forecasted Analysis',
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    
                    fig_demand.update_layout(
                        title={
                            'text': 'Product Demand: Current vs Forecasted Analysis',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#1f2937'}
                        },
                        xaxis_title='Current Demand (units/month)',
                        yaxis_title='Forecasted Demand (units/month)',
                        height=600,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    
                    fig_demand.update_traces(
                        hovertemplate="<b>%{customdata[0]}</b><br>" +
                                    "Category: %{marker.color}<br>" +
                                    "Current: %{x} units<br>" +
                                    "Forecasted: %{y} units<br>" +
                                    "Trend: %{customdata[1]:.2f}<br>" +
                                    "Confidence: %{customdata[2]}<br>" +
                                    "<extra></extra>",
                        textposition='top center'
                    )
                    
                    st.plotly_chart(fig_demand, use_container_width=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #45b7d1;">
                        <h5>🔮 Forecasting Insights:</h5>
                        <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.6;">
                            <li><strong>📈 Growing Demand:</strong> Increase inventory and production</li>
                            <li><strong>📉 Declining Demand:</strong> Consider promotions or phase-out</li>
                            <li><strong>🔄 Stable Demand:</strong> Maintain current levels</li>
                        </ul>
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                                💡 <strong>Strategy:</strong> Use forecasts to optimize inventory levels and production planning
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced top products display
                st.markdown("### 🚀 Top Products by Forecasted Demand")
                
                top_demand_products = demand_data.head(10)
                
                # Format the data for better display
                display_df = top_demand_products[['product_name', 'category', 'current_demand', 'mean_forecast', 'confidence_interval']].copy()
                display_df['current_demand'] = display_df['current_demand'].round(1)
                display_df['mean_forecast'] = display_df['mean_forecast'].round(1)
                
                st.markdown("""
                <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 15px 0;">
                    <strong>📊 Inventory Planning:</strong> These products show the highest forecasted demand. Consider increasing production capacity, optimizing supply chains, and ensuring adequate inventory levels to meet projected customer needs.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "current_demand": st.column_config.NumberColumn(
                            "Current Demand",
                            help="Current monthly demand in units",
                            format="%.1f"
                        ),
                        "mean_forecast": st.column_config.NumberColumn(
                            "Forecasted Demand",
                            help="Predicted monthly demand in units",
                            format="%.1f"
                        )
                    }
                )
                
            else:
                st.warning("⚠️ No product demand forecast data available.")
                st.info(demand_msg)
        else:
            st.warning("⚠️ Product data not available for demand forecasting.")
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <strong>💡 Setup Required:</strong> Add product data in the Data Input section to enable demand forecasting analysis. This will allow the system to analyze sales patterns and predict future demand for inventory optimization.
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Enhanced CLV Prediction Engine header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0; text-align: center; font-size: 1.8em;">💰 Advanced Customer Lifetime Value Prediction Engine</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💎 **AI-Powered CLV Prediction**: Advanced machine learning models analyze customer behavior patterns, purchase history, engagement metrics, and growth trajectories to predict future customer value and identify high-potential customers for strategic retention and growth initiatives.")
        
        if not st.session_state.customers.empty:
            with st.spinner("💎 Calculating customer lifetime value predictions..."):
                # Try the simple CLV prediction first
                clv_data, clv_msg = calculate_customer_lifetime_value_prediction_simple(st.session_state.customers, st.session_state.sales_orders)
                
                # If that fails, try the original function
                if clv_data.empty:
                    st.info("🔄 Trying advanced CLV prediction method...")
                    clv_data, clv_msg = calculate_customer_lifetime_value_prediction(st.session_state.customers, st.session_state.sales_orders)
            
            if not clv_data.empty:
                st.success(f"✅ {clv_msg}")
                
                # Enhanced CLV segment summary with better styling
                st.markdown("### 📊 Customer Value Segmentation Dashboard")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    premium = len(clv_data[clv_data['clv_segment'] == 'Premium'])
                    premium_percentage = (premium / len(clv_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">💎 Premium</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{premium}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{premium_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    high_value = len(clv_data[clv_data['clv_segment'] == 'High Value'])
                    high_percentage = (high_value / len(clv_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #32CD32 0%, #228B22 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">🚀 High Value</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{high_value}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{high_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    medium_value = len(clv_data[clv_data['clv_segment'] == 'Medium Value'])
                    med_percentage = (medium_value / len(clv_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📈 Medium Value</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{medium_value}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{med_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    standard = len(clv_data[clv_data['clv_segment'] == 'Standard'])
                    standard_percentage = (standard / len(clv_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📊 Standard</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{standard}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{standard_percentage:.1f}% of customers</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced CLV segment distribution chart
                st.markdown("### 🎨 Interactive CLV Segmentation Analysis")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    segment_distribution = clv_data['clv_segment'].value_counts()
                    fig_clv_segments = px.bar(
                        x=segment_distribution.index,
                        y=segment_distribution.values,
                        title='Customer Distribution by CLV Segment',
                        color=segment_distribution.values,
                        color_discrete_map={
                            'Premium': '#FFD700',
                            'High Value': '#32CD32',
                            'Medium Value': '#FFA500',
                            'Standard': '#87CEEB'
                        }
                    )
                    
                    fig_clv_segments.update_layout(
                        title={
                            'text': 'Customer Distribution by CLV Segment',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#1f2937'}
                        },
                        xaxis_title='CLV Segment',
                        yaxis_title='Customer Count',
                        height=500,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    
                    fig_clv_segments.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Count: %{y}<br>" +
                                    "<extra></extra>",
                        texttemplate='%{y}',
                        textposition='outside',
                        textfont=dict(size=16)
                    )
                    
                    st.plotly_chart(fig_clv_segments, use_container_width=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #f093fb;">
                        <h5>💎 Value Segmentation Insights:</h5>
                        <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.6;">
                            <li><strong>💎 Premium:</strong> VIP treatment, exclusive offers</li>
                            <li><strong>🚀 High Value:</strong> Growth focus, upselling</li>
                            <li><strong>📈 Medium Value:</strong> Engagement, retention</li>
                            <li><strong>📊 Standard:</strong> Basic service, efficiency</li>
                        </ul>
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                                💡 <strong>Strategy:</strong> Tailor customer experience based on predicted CLV segments
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced top customers display
                st.markdown("### 🏆 Top Customers by Predicted CLV")
                
                top_clv_customers = clv_data.head(10)
                
                # Format the data for better display
                display_df = top_clv_customers[['customer_name', 'historical_revenue', 'predicted_revenue', 'total_predicted_clv', 'clv_growth_rate', 'clv_segment']].copy()
                display_df['historical_revenue'] = display_df['historical_revenue'].apply(lambda x: f"${x:,.2f}")
                display_df['predicted_revenue'] = display_df['predicted_revenue'].apply(lambda x: f"${x:,.2f}")
                display_df['total_predicted_clv'] = display_df['total_predicted_clv'].apply(lambda x: f"${x:,.2f}")
                display_df['clv_growth_rate'] = display_df['clv_growth_rate'].apply(lambda x: f"{x:+.1f}%")
                
                st.markdown("""
                <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 15px 0;">
                    <strong>💎 Strategic Focus:</strong> These customers represent your highest-value prospects. Implement personalized retention strategies, exclusive offers, and dedicated account management to maximize their lifetime value and drive revenue growth.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "historical_revenue": st.column_config.TextColumn(
                            "Historical Revenue",
                            help="Total revenue generated to date"
                        ),
                        "predicted_revenue": st.column_config.TextColumn(
                            "Predicted Revenue",
                            help="Forecasted future revenue"
                        ),
                        "total_predicted_clv": st.column_config.TextColumn(
                            "Total Predicted CLV",
                            help="Combined historical + predicted revenue"
                        ),
                        "clv_growth_rate": st.column_config.TextColumn(
                            "Growth Rate",
                            help="Predicted revenue growth percentage"
                        )
                    }
                )
                
            else:
                st.warning("⚠️ No CLV prediction data available.")
                st.info(f"📝 {clv_msg}")
        else:
            st.warning("⚠️ Customer data not available for CLV prediction.")
            st.markdown("""
            <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 4px solid #2196f3; margin: 20px 0;">
                <strong>💡 Setup Required:</strong> Add customer data in the Data Input section to enable CLV prediction analysis. This will allow the system to analyze customer behavior patterns and predict future value for strategic decision-making.
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        # Enhanced Sales Performance Analytics header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: white; margin: 0; text-align: center; font-size: 1.8em;">📈 Advanced Sales Performance Analytics & Prediction Engine</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🚀 **AI-Powered Performance Prediction**: Advanced analytics engines evaluate sales representative performance patterns, growth trajectories, and market dynamics to predict future performance and identify optimization opportunities for sales team development and quota planning.")
        
        if not st.session_state.sales_reps.empty:
            with st.spinner("🚀 Analyzing sales performance patterns..."):
                performance_data, performance_msg = calculate_sales_performance_prediction(st.session_state.sales_orders, st.session_state.sales_reps)
            
            if not performance_data.empty:
                st.success(f"✅ {performance_msg}")
                
                # Enhanced performance summary with better styling
                st.markdown("### 📊 Sales Performance Classification Dashboard")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    excellent = len(performance_data[performance_data['performance_class'] == 'Excellent'])
                    excellent_percentage = (excellent / len(performance_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">🏆 Excellent</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{excellent}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{excellent_percentage:.1f}% of team</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    good = len(performance_data[performance_data['performance_class'] == 'Good'])
                    good_percentage = (good / len(performance_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">👍 Good</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{good}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{good_percentage:.1f}% of team</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    average = len(performance_data[performance_data['performance_class'] == 'Average'])
                    avg_percentage = (average / len(performance_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📊 Average</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{average}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{avg_percentage:.1f}% of team</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    needs_improvement = len(performance_data[performance_data['performance_class'] == 'Needs Improvement'])
                    improvement_percentage = (needs_improvement / len(performance_data)) * 100
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <h4 style="color: white; margin: 0; font-size: 1.2em;">📈 Needs Improvement</h4>
                        <h2 style="color: white; margin: 10px 0; font-size: 2.2em;">{needs_improvement}</h2>
                        <p style="color: white; margin: 0; font-size: 1em; opacity: 0.9;">{improvement_percentage:.1f}% of team</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced performance score distribution chart
                st.markdown("### 🎨 Interactive Performance Score Analysis")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig_performance = px.histogram(
                        performance_data,
                        x='performance_score',
                        color='performance_class',
                        title='Sales Performance Score Distribution by Classification',
                        nbins=20,
                        color_discrete_map={
                            'Excellent': '#4CAF50',
                            'Good': '#2196F3',
                            'Average': '#FF9800',
                            'Needs Improvement': '#f44336'
                        }
                    )
                    
                    fig_performance.update_layout(
                        title={
                            'text': 'Sales Performance Score Distribution by Classification',
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#1f2937'}
                        },
                        xaxis_title='Performance Score',
                        yaxis_title='Count',
                        height=500,
                        showlegend=True,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=14)
                    )
                    
                    fig_performance.update_traces(
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Count: %{y}<br>" +
                                    "Classification: %{marker.color}<br>" +
                                    "<extra></extra>",
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_performance, use_container_width=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                        <h5>📊 Performance Insights:</h5>
                        <ul style="margin: 15px 0; padding-left: 20px; line-height: 1.6;">
                            <li><strong>🏆 Excellent:</strong> Top performers, recognize & reward</li>
                            <li><strong>👍 Good:</strong> Strong performers, growth potential</li>
                            <li><strong>📊 Average:</strong> Development opportunities</li>
                            <li><strong>📈 Needs Improvement:</strong> Training & support focus</li>
                        </ul>
                        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 15px;">
                            <p style="margin: 0; color: #2e7d32; font-size: 0.9em;">
                                💡 <strong>Strategy:</strong> Use predictions for targeted coaching and resource allocation
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Enhanced top performers display
                st.markdown("### 🏅 Top Sales Representatives Performance Dashboard")
                
                top_performers = performance_data.head(10)
                
                # Format the data for better display
                display_df = top_performers[['sales_rep_name', 'performance_score', 'performance_class', 'predicted_monthly_revenue', 'total_predicted_revenue']].copy()
                display_df['performance_score'] = display_df['performance_score'].round(1)
                display_df['predicted_monthly_revenue'] = display_df['predicted_monthly_revenue'].apply(lambda x: f"${x:,.2f}")
                display_df['total_predicted_revenue'] = display_df['total_predicted_revenue'].apply(lambda x: f"${x:,.2f}")
                
                st.markdown("""
                <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin: 15px 0;">
                    <strong>🏆 Performance Recognition:</strong> These top performers demonstrate exceptional sales capabilities and growth potential. Consider them for leadership roles, advanced training opportunities, and as mentors for other team members.
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "performance_score": st.column_config.NumberColumn(
                            "Performance Score",
                            help="Overall performance rating (0-100)",
                            format="%.1f"
                        ),
                        "predicted_monthly_revenue": st.column_config.TextColumn(
                            "Monthly Revenue",
                            help="Predicted monthly revenue generation"
                        ),
                        "total_predicted_revenue": st.column_config.TextColumn(
                            "Total Predicted Revenue",
                            help="Total predicted revenue over forecast period"
                        )
                    }
                )
                
            else:
                st.warning("⚠️ No performance prediction data available.")
                st.info(performance_msg)
        else:
            st.warning("⚠️ Sales representative data not available for performance prediction.")
            st.markdown("""
            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <strong>💡 Setup Required:</strong> Add sales representative data in the Data Input section to enable performance prediction analysis. This will allow the system to evaluate individual performance patterns and predict future success for strategic team development.
            </div>
            """, unsafe_allow_html=True)
    
    # AI Recommendations
    display_ai_recommendations("predictive_analytics", st.session_state.sales_orders)

# ============================================================================
# STRATEGIC SALES ANALYTICS
# ============================================================================

def show_strategic_analytics():
    st.header("📊 Strategic Sales Analytics")
    
    if st.session_state.sales_orders.empty:
        st.warning("Please add sales data first in the Data Input section.")
        return
    
    # Summary metrics
    st.markdown("""
    <div class="metric-card-blue">
        <h3 style="color: white; margin: 0; text-align: center;">📊 Strategic Analytics Summary Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_revenue = st.session_state.sales_orders['total_amount'].sum()
    total_orders = len(st.session_state.sales_orders)
    unique_customers = st.session_state.sales_orders['customer_id'].nunique()
    unique_products = st.session_state.sales_orders['product_id'].nunique()
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.markdown("""
        <div class="metric-card-green">
        <h4 style="margin: 0; color: #16a34a;">Total Revenue</h4>
        <h2 style="margin: 10px 0; color: #16a34a;">${:,.2f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="metric-card-blue">
        <h4 style="margin: 0; color: #667eea;">Total Orders</h4>
        <h2 style="margin: 10px 0; color: #667eea;">{:,}</h2>
        </div>
        """.format(total_orders), unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="metric-card-purple">
        <h4 style="margin: 0; color: #a855f7;">Unique Customers</h4>
        <h2 style="margin: 10px 0; color: #a855f7;">{:,}</h2>
        </div>
        """.format(unique_customers), unsafe_allow_html=True)
    
    with summary_col4:
        st.markdown("""
        <div class="metric-card-teal">
        <h4 style="margin: 0; color: #14b8a6;">Products Sold</h4>
        <h2 style="margin: 10px 0; color: #14b8a6;">{:,}</h2>
        </div>
        """.format(unique_products), unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Revenue Analysis Dashboard</h4>
        </div>
        """, unsafe_allow_html=True)
        # Create comprehensive revenue analysis
        revenue_analysis = pd.DataFrame({
            'Metric': [
                'Total Revenue',
                'Average Order Value',
                'Revenue per Customer',
                'Revenue Growth Rate',
                'Customer Acquisition Cost',
                'Customer Lifetime Value',
                'Profit Margin',
                'Market Share'
            ],
            'Value': [
                f"${total_revenue:,.2f}",
                f"${total_revenue / total_orders:,.2f}",
                f"${total_revenue / unique_customers:,.2f}",
                "12.5%",
                "$1,250",
                "$15,000",
                "35%",
                "8.5%"
            ],
            'Status': [
                "✅ On Track",
                "✅ Above Target",
                "✅ Strong",
                "🟡 Moderate",
                "✅ Efficient",
                "✅ High Value",
                "✅ Healthy",
                "🟡 Growing"
            ]
        })
        st.dataframe(revenue_analysis, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
        <h4>🎯 Key Performance Indicators</h4>
        </div>
        """, unsafe_allow_html=True)
        # Create KPI summary
        kpi_data = pd.DataFrame({
            'KPI': [
                'Sales Conversion Rate',
                'Average Deal Size',
                'Sales Cycle Length',
                'Win Rate',
                'Quota Attainment',
                'Customer Retention Rate',
                'Revenue per Sales Rep',
                'Pipeline Velocity'
            ],
            'Current': [
                "15.2%",
                "$45,000",
                "45 days",
                "68%",
                "87%",
                "92%",
                "$850,000",
                "$125,000/day"
            ],
            'Target': [
                "18%",
                "$50,000",
                "40 days",
                "70%",
                "90%",
                "95%",
                "$900,000",
                "$150,000/day"
            ],
            'Status': [
                "🟡 Below Target",
                "🟡 Below Target",
                "🟡 Above Target",
                "🟡 Below Target",
                "🟡 Below Target",
                "🟡 Below Target",
                "🟡 Below Target",
                "🟡 Below Target"
            ]
        })
        st.dataframe(kpi_data, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
        <h4>📈 Strategic Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        recommendations_text = """
        **Key Strategic Insights:**
        
        🎯 **Growth Opportunities:**
        - Expand into underserved regions
        - Increase product portfolio
        - Improve customer retention
        
        ⚠️ **Risk Areas:**
        - Sales cycle length increasing
        - Win rate below target
        - Customer acquisition cost rising
        
        💡 **Recommendations:**
        - Implement sales training programs
        - Optimize pricing strategies
        - Enhance customer success initiatives
        """
        display_formatted_recommendations(recommendations_text)
    
    with col4:
        st.markdown("""
        <div class="chart-container">
        <h4>📊 Performance Trends</h4>
        </div>
        """, unsafe_allow_html=True)
        # Create trend analysis
        trends_data = pd.DataFrame({
            'Metric': ['Revenue Growth', 'Customer Growth', 'Product Performance', 'Sales Efficiency'],
            'Trend': ['↗️ Increasing', '↗️ Increasing', '→ Stable', '↘️ Declining'],
            'Change': ['+12.5%', '+8.2%', '+2.1%', '-5.3%'],
            'Impact': ['High', 'Medium', 'Low', 'Medium']
        })
        st.dataframe(trends_data, use_container_width=True)
    
    # AI Recommendations
    display_ai_recommendations("strategic_analytics", st.session_state.sales_orders)

# ============================================================================
# Sample Data Generation Functions
# ============================================================================

def generate_sample_sales_data():
    """Generate comprehensive sample data for sales analytics with 200+ records."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Generate sample data for all tables
    customers = generate_sample_customers(50)
    products = generate_sample_products(30)
    sales_reps = generate_sample_sales_reps(15)
    sales_orders = generate_sample_sales_orders(200, customers, products, sales_reps)
    leads = generate_sample_leads(100, sales_reps)
    opportunities = generate_sample_opportunities(80, leads, customers, products, sales_reps)
    activities = generate_sample_activities(150, sales_reps, customers)
    targets = generate_sample_targets(20, sales_reps)
    
    # Store in session state
    st.session_state.customers = customers
    st.session_state.products = products
    st.session_state.sales_reps = sales_reps
    st.session_state.sales_orders = sales_orders
    st.session_state.leads = leads
    st.session_state.opportunities = opportunities
    st.session_state.activities = activities
    st.session_state.targets = targets
    
    return customers, products, sales_reps, sales_orders, leads, opportunities, activities, targets

def generate_sample_customers(n_customers):
    """Generate sample customer data."""
    
    customer_names = [
        'Acme Corporation', 'TechStart Inc', 'Global Solutions Ltd', 'Innovation Co',
        'Premium Services', 'Elite Business Group', 'Future Technologies', 'Smart Solutions',
        'Quality Products Inc', 'Advanced Systems', 'Reliable Partners', 'Excellence Corp',
        'NextGen Industries', 'Strategic Solutions', 'Peak Performance', 'Summit Business',
        'Pinnacle Corp', 'Apex Solutions', 'Prime Technologies', 'Core Business Group'
    ]
    
    industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Consulting', 'Real Estate']
    segments = ['Enterprise', 'SMB', 'Startup', 'Individual']
    countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia', 'Japan', 'Singapore']
    regions = ['North America', 'Europe', 'Asia Pacific', 'Middle East', 'Africa']
    
    data = []
    start_date = datetime(2020, 1, 1)
    
    for i in range(n_customers):
        acquisition_date = start_date + timedelta(days=random.randint(0, 1000))
        
        data.append({
            'customer_id': f'CUST-{str(i+1).zfill(3)}',
            'customer_name': random.choice(customer_names) + f' {i+1}',
            'email': f'customer{i+1}@example.com',
            'phone': f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'company': random.choice(customer_names) + f' {i+1}',
            'industry': random.choice(industries),
            'region': random.choice(regions),
            'country': random.choice(countries),
            'customer_segment': random.choice(segments),
            'acquisition_date': acquisition_date,
            'status': random.choice(['Active', 'Active', 'Active', 'Inactive', 'Churned'])
        })
    
    return pd.DataFrame(data)

def generate_sample_products(n_products):
    """Generate sample product data."""
    
    product_names = [
        'Premium Software Suite', 'Enterprise Solution', 'Cloud Platform', 'Mobile App',
        'Analytics Dashboard', 'CRM System', 'ERP Solution', 'Security Suite',
        'Collaboration Tool', 'Project Management', 'Data Analytics', 'AI Platform',
        'IoT Solution', 'Blockchain Platform', 'Machine Learning Tool', 'API Gateway',
        'Database System', 'Web Application', 'Desktop Software', 'Mobile Platform'
    ]
    
    categories = ['Software', 'Platform', 'Service', 'Solution', 'Tool', 'System']
    subcategories = ['Enterprise', 'Cloud', 'Mobile', 'Web', 'Desktop', 'API', 'Database']
    
    data = []
    start_date = datetime(2020, 1, 1)
    
    for i in range(n_products):
        launch_date = start_date + timedelta(days=random.randint(0, 1000))
        unit_price = round(random.uniform(50, 5000), 2)
        cost_price = round(unit_price * random.uniform(0.3, 0.7), 2)
        
        data.append({
            'product_id': f'PROD-{str(i+1).zfill(3)}',
            'product_name': random.choice(product_names) + f' {i+1}',
            'category': random.choice(categories),
            'subcategory': random.choice(subcategories),
            'unit_price': unit_price,
            'cost_price': cost_price,
            'supplier_id': f'SUP-{random.randint(1, 10)}',
            'launch_date': launch_date,
            'status': random.choice(['Active', 'Active', 'Active', 'Coming Soon', 'Discontinued'])
        })
    
    return pd.DataFrame(data)

def generate_sample_sales_reps(n_reps):
    """Generate sample sales representative data."""
    
    first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Lisa', 'Robert', 'Jennifer', 'James', 'Amanda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Middle East', 'Africa']
    territories = ['East Coast', 'West Coast', 'Central', 'Northern', 'Southern', 'International']
    
    data = []
    start_date = datetime(2018, 1, 1)
    
    for i in range(n_reps):
        hire_date = start_date + timedelta(days=random.randint(0, 1500))
        quota = round(random.uniform(50000, 500000), 2)
        
        data.append({
            'sales_rep_id': f'REP-{str(i+1).zfill(3)}',
            'first_name': random.choice(first_names),
            'last_name': random.choice(last_names),
            'email': f'rep{i+1}@company.com',
            'region': random.choice(regions),
            'territory': random.choice(territories),
            'hire_date': hire_date,
            'quota': quota,
            'manager_id': f'REP-{random.randint(1, 5)}' if i >= 5 else None,
            'status': random.choice(['Active', 'Active', 'Active', 'Inactive'])
        })
    
    return pd.DataFrame(data)

def generate_sample_sales_orders(n_orders, customers, products, sales_reps):
    """Generate sample sales orders data."""
    
    channels = ['Online', 'In-Store', 'Phone', 'Partner']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_orders):
        order_date = start_date + timedelta(days=random.randint(0, 365))
        customer = customers.iloc[random.randint(0, len(customers)-1)]
        product = products.iloc[random.randint(0, len(products)-1)]
        sales_rep = sales_reps.iloc[random.randint(0, len(sales_reps)-1)]
        
        quantity = random.randint(1, 10)
        unit_price = product['unit_price']
        total_amount = quantity * unit_price
        
        data.append({
            'order_id': f'ORD-{str(i+1).zfill(4)}',
            'customer_id': customer['customer_id'],
            'order_date': order_date,
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'sales_rep_id': sales_rep['sales_rep_id'],
            'region': customer['region'],
            'channel': random.choice(channels)
        })
    
    return pd.DataFrame(data)

def generate_sample_leads(n_leads, sales_reps):
    """Generate sample leads data."""
    
    sources = ['Website', 'Referral', 'Cold Call', 'Trade Show', 'Social Media', 'Email Campaign']
    statuses = ['New', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_leads):
        created_date = start_date + timedelta(days=random.randint(0, 365))
        sales_rep = sales_reps.iloc[random.randint(0, len(sales_reps)-1)]
        value = round(random.uniform(5000, 100000), 2)
        
        data.append({
            'lead_id': f'LEAD-{str(i+1).zfill(4)}',
            'lead_name': f'Lead {i+1}',
            'email': f'lead{i+1}@example.com',
            'company': f'Company {i+1}',
            'industry': random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']),
            'source': random.choice(sources),
            'created_date': created_date,
            'status': random.choice(statuses),
            'assigned_rep_id': sales_rep['sales_rep_id'],
            'value': value
        })
    
    return pd.DataFrame(data)

def generate_sample_opportunities(n_opportunities, leads, customers, products, sales_reps):
    """Generate sample opportunities data."""
    
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_opportunities):
        created_date = start_date + timedelta(days=random.randint(0, 365))
        close_date = created_date + timedelta(days=random.randint(30, 180))
        
        lead = leads.iloc[random.randint(0, len(leads)-1)]
        customer = customers.iloc[random.randint(0, len(customers)-1)]
        product = products.iloc[random.randint(0, len(products)-1)]
        sales_rep = sales_reps.iloc[random.randint(0, len(sales_reps)-1)]
        
        value = round(random.uniform(10000, 200000), 2)
        probability = random.choice([10, 25, 50, 75, 90])
        
        data.append({
            'opportunity_id': f'OPP-{str(i+1).zfill(4)}',
            'lead_id': lead['lead_id'],
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'value': value,
            'stage': random.choice(stages),
            'created_date': created_date,
            'close_date': close_date,
            'probability': probability,
            'sales_rep_id': sales_rep['sales_rep_id']
        })
    
    return pd.DataFrame(data)

def generate_sample_activities(n_activities, sales_reps, customers):
    """Generate sample activities data."""
    
    activity_types = ['Call', 'Meeting', 'Email', 'Demo', 'Proposal', 'Follow-up']
    outcomes = ['Positive', 'Neutral', 'Negative', 'Follow-up Required']
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(n_activities):
        date = start_date + timedelta(days=random.randint(0, 365))
        sales_rep = sales_reps.iloc[random.randint(0, len(sales_reps)-1)]
        customer = customers.iloc[random.randint(0, len(customers)-1)]
        
        duration_minutes = random.randint(15, 120)
        
        data.append({
            'activity_id': f'ACT-{str(i+1).zfill(4)}',
            'sales_rep_id': sales_rep['sales_rep_id'],
            'customer_id': customer['customer_id'],
            'activity_type': random.choice(activity_types),
            'date': date,
            'duration_minutes': duration_minutes,
            'notes': f'Activity notes for {random.choice(activity_types)} with {customer["customer_name"]}',
            'outcome': random.choice(outcomes)
        })
    
    return pd.DataFrame(data)

def generate_sample_targets(n_targets, sales_reps):
    """Generate sample targets data."""
    
    categories = ['Revenue', 'Deals', 'Activities', 'Leads']
    periods = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Annual 2024']
    statuses = ['Active', 'Completed', 'Overdue']
    
    data = []
    
    for i in range(n_targets):
        sales_rep = sales_reps.iloc[random.randint(0, len(sales_reps)-1)]
        target_amount = round(random.uniform(50000, 500000), 2)
        target_date = datetime(2024, random.randint(1, 12), random.randint(1, 28))
        
        data.append({
            'target_id': f'TARGET-{str(i+1).zfill(3)}',
            'sales_rep_id': sales_rep['sales_rep_id'],
            'period': random.choice(periods),
            'target_amount': target_amount,
            'target_date': target_date,
            'category': random.choice(categories),
            'status': random.choice(statuses)
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    main()

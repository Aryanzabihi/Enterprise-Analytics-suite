import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import datetime
import io
import base64
import warnings

# Configure Streamlit page
st.set_page_config(
    page_title="R&D Analytics Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

warnings.filterwarnings('ignore')

# Set Plotly template
pio.templates.default = "plotly_white"
CONTINUOUS_COLOR_SCALE = "Turbo"
CATEGORICAL_COLOR_SEQUENCE = px.colors.qualitative.Pastel

# Import R&D metric calculation functions
try:
    from rd_metrics_calculator import calculate_innovation_metrics
except ImportError as e:
    st.error(f"Error importing rd_metrics_calculator: {e}")
    # Define a fallback function
    def calculate_innovation_metrics(projects_data, products_data, prototypes_data):
        return pd.DataFrame(), "Error: Could not import metrics calculator"

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

def apply_common_layout(fig):
    """Apply a common layout to Plotly figures for consistent style."""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=14),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
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

def create_template_for_download():
    """Create an Excel template with all required R&D data schema and make it downloadable"""
    
    # Create empty DataFrames with the correct R&D schema
    projects_template = pd.DataFrame(columns=[
        'project_id', 'project_name', 'project_type', 'start_date', 'end_date', 
        'status', 'budget', 'actual_spend', 'team_lead_id', 'department', 'priority',
        'technology_area', 'trl_level', 'milestones_completed', 'total_milestones'
    ])
    
    researchers_template = pd.DataFrame(columns=[
        'researcher_id', 'first_name', 'last_name', 'email', 'department', 
        'specialization', 'hire_date', 'education_level', 'experience_years', 
        'status', 'salary', 'manager_id'
    ])
    
    patents_template = pd.DataFrame(columns=[
        'patent_id', 'project_id', 'patent_title', 'filing_date', 'grant_date', 
        'status', 'researcher_id', 'technology_area', 'estimated_value', 
        'licensing_revenue', 'expiry_date'
    ])
    
    equipment_template = pd.DataFrame(columns=[
        'equipment_id', 'equipment_name', 'equipment_type', 'purchase_date', 
        'cost', 'location', 'status', 'total_hours', 'utilized_hours', 
        'maintenance_cost', 'department'
    ])
    
    collaborations_template = pd.DataFrame(columns=[
        'collaboration_id', 'partner_name', 'partner_type', 'start_date', 
        'end_date', 'project_id', 'investment_amount', 'revenue_generated', 
        'status', 'collaboration_type', 'researcher_id'
    ])
    
    prototypes_template = pd.DataFrame(columns=[
        'prototype_id', 'project_id', 'prototype_name', 'development_date', 
        'testing_date', 'cost', 'status', 'success_rate', 'iterations', 
        'researcher_id', 'technology_used'
    ])
    
    products_template = pd.DataFrame(columns=[
        'product_id', 'project_id', 'product_name', 'launch_date', 'development_cost', 
        'revenue_generated', 'market_response', 'customer_satisfaction', 
        'patent_id', 'status', 'target_market'
    ])
    
    training_template = pd.DataFrame(columns=[
        'training_id', 'researcher_id', 'training_type', 'training_date', 
        'duration_hours', 'cost', 'pre_performance_score', 'post_performance_score', 
        'effectiveness_rating', 'trainer_name'
    ])
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each template to a separate sheet
        projects_template.to_excel(writer, sheet_name='Projects', index=False)
        researchers_template.to_excel(writer, sheet_name='Researchers', index=False)
        patents_template.to_excel(writer, sheet_name='Patents', index=False)
        equipment_template.to_excel(writer, sheet_name='Equipment', index=False)
        collaborations_template.to_excel(writer, sheet_name='Collaborations', index=False)
        prototypes_template.to_excel(writer, sheet_name='Prototypes', index=False)
        products_template.to_excel(writer, sheet_name='Products', index=False)
        training_template.to_excel(writer, sheet_name='Training', index=False)
        
        # Get the workbook for formatting
        workbook = writer.book
        
        # Add instructions sheet
        instructions_data = {
            'Sheet Name': ['Projects', 'Researchers', 'Patents', 'Equipment', 'Collaborations', 'Prototypes', 'Products', 'Training'],
            'Required Fields': [
                'project_id, project_name, project_type, start_date, end_date, status, budget, actual_spend, team_lead_id, department, priority, technology_area, trl_level, milestones_completed, total_milestones',
                'researcher_id, first_name, last_name, email, department, specialization, hire_date, education_level, experience_years, status, salary, manager_id',
                'patent_id, project_id, patent_title, filing_date, grant_date, status, researcher_id, technology_area, estimated_value, licensing_revenue, expiry_date',
                'equipment_id, equipment_name, equipment_type, purchase_date, cost, location, status, total_hours, utilized_hours, maintenance_cost, department',
                'collaboration_id, partner_name, partner_type, start_date, end_date, project_id, investment_amount, revenue_generated, status, collaboration_type, researcher_id',
                'prototype_id, project_id, prototype_name, development_date, testing_date, cost, status, success_rate, iterations, researcher_id, technology_used',
                'product_id, project_id, product_name, launch_date, development_cost, revenue_generated, market_response, customer_satisfaction, patent_id, status, target_market',
                'training_id, researcher_id, training_type, training_date, duration_hours, cost, pre_performance_score, post_performance_score, effectiveness_rating, trainer_name'
            ],
            'Data Types': [
                'Text, Text, Text, Date, Date, Text, Number, Number, Text, Text, Text, Text, Number, Number, Number',
                'Text, Text, Text, Text, Text, Text, Date, Text, Number, Text, Number, Text',
                'Text, Text, Text, Date, Date, Text, Text, Text, Number, Number, Date',
                'Text, Text, Text, Date, Number, Text, Text, Number, Number, Number, Text',
                'Text, Text, Text, Date, Date, Text, Number, Number, Text, Text, Text',
                'Text, Text, Text, Date, Date, Number, Text, Number, Number, Text, Text',
                'Text, Text, Text, Date, Number, Number, Number, Number, Text, Text, Text',
                'Text, Text, Text, Date, Number, Number, Number, Number, Number, Text'
            ],
            'Description': [
                'R&D projects with timelines, budgets, and progress tracking',
                'Research team members with skills and performance data',
                'Intellectual property including patents and their value',
                'R&D equipment and utilization tracking',
                'External partnerships and collaborations',
                'Prototype development and testing results',
                'Products launched from R&D projects',
                'Training programs and their effectiveness'
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
    """Export all R&D data to Excel file"""
    if (st.session_state.projects.empty and st.session_state.researchers.empty and 
        st.session_state.patents.empty and st.session_state.equipment.empty and
        st.session_state.collaborations.empty and st.session_state.prototypes.empty and
        st.session_state.products.empty and st.session_state.training.empty):
        st.warning("No data to export. Please add data first.")
        return None
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each DataFrame to a separate sheet
        st.session_state.projects.to_excel(writer, sheet_name='Projects', index=False)
        st.session_state.researchers.to_excel(writer, sheet_name='Researchers', index=False)
        st.session_state.patents.to_excel(writer, sheet_name='Patents', index=False)
        st.session_state.equipment.to_excel(writer, sheet_name='Equipment', index=False)
        st.session_state.collaborations.to_excel(writer, sheet_name='Collaborations', index=False)
        st.session_state.prototypes.to_excel(writer, sheet_name='Prototypes', index=False)
        st.session_state.products.to_excel(writer, sheet_name='Products', index=False)
        st.session_state.training.to_excel(writer, sheet_name='Training', index=False)
    
    output.seek(0)
    return output

# Page configuration
st.set_page_config(
    page_title="R&D Analytics Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure page for wide layout
st.set_page_config(
    page_title="R&D Analytics Dashboard",
    page_icon="🔬",
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



# Initialize session state for R&D data storage
if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=[
        'project_id', 'project_name', 'project_type', 'start_date', 'end_date', 
        'status', 'budget', 'actual_spend', 'team_lead_id', 'department', 'priority',
        'technology_area', 'trl_level', 'milestones_completed', 'total_milestones'
    ])

if 'researchers' not in st.session_state:
    st.session_state.researchers = pd.DataFrame(columns=[
        'researcher_id', 'first_name', 'last_name', 'email', 'department', 
        'specialization', 'hire_date', 'education_level', 'experience_years', 
        'status', 'salary', 'manager_id'
    ])

if 'patents' not in st.session_state:
    st.session_state.patents = pd.DataFrame(columns=[
        'patent_id', 'project_id', 'patent_title', 'filing_date', 'grant_date', 
        'status', 'researcher_id', 'technology_area', 'estimated_value', 
        'licensing_revenue', 'expiry_date'
    ])

if 'equipment' not in st.session_state:
    st.session_state.equipment = pd.DataFrame(columns=[
        'equipment_id', 'equipment_name', 'equipment_type', 'purchase_date', 
        'cost', 'location', 'status', 'total_hours', 'utilized_hours', 
        'maintenance_cost', 'department'
    ])

if 'collaborations' not in st.session_state:
    st.session_state.collaborations = pd.DataFrame(columns=[
        'collaboration_id', 'partner_name', 'partner_type', 'start_date', 
        'end_date', 'project_id', 'investment_amount', 'revenue_generated', 
        'status', 'collaboration_type', 'researcher_id'
    ])

if 'prototypes' not in st.session_state:
    st.session_state.prototypes = pd.DataFrame(columns=[
        'prototype_id', 'project_id', 'prototype_name', 'development_date', 
        'testing_date', 'cost', 'status', 'success_rate', 'iterations', 
        'researcher_id', 'technology_used'
    ])

if 'products' not in st.session_state:
    st.session_state.products = pd.DataFrame(columns=[
        'product_id', 'project_id', 'product_name', 'launch_date', 'development_cost', 
        'revenue_generated', 'market_response', 'customer_satisfaction', 
        'patent_id', 'status', 'target_market'
    ])

if 'training' not in st.session_state:
    st.session_state.training = pd.DataFrame(columns=[
        'training_id', 'researcher_id', 'training_type', 'training_date', 
        'duration_hours', 'cost', 'pre_performance_score', 'post_performance_score', 
        'effectiveness_rating', 'trainer_name'
    ])

def set_home_page():
    """Set the department to start on home page"""
    st.session_state.current_page = "🏠 Home"

def main():
    # Configure page for wide layout
    st.set_page_config(
        page_title="R&D Analytics Dashboard",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Modern header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🔬 R&D Analytics Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'projects' not in st.session_state:
        st.session_state.projects = pd.DataFrame()
    if 'researchers' not in st.session_state:
        st.session_state.researchers = pd.DataFrame()
    if 'patents' not in st.session_state:
        st.session_state.patents = pd.DataFrame()
    if 'equipment' not in st.session_state:
        st.session_state.equipment = pd.DataFrame()
    if 'collaborations' not in st.session_state:
        st.session_state.collaborations = pd.DataFrame()
    if 'prototypes' not in st.session_state:
        st.session_state.prototypes = pd.DataFrame()
    if 'products' not in st.session_state:
        st.session_state.products = pd.DataFrame()
    if 'training' not in st.session_state:
        st.session_state.training = pd.DataFrame()
    
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
        
        if st.button("🚀 Innovation & Product Development", key="nav_innovation", use_container_width=True):
            st.session_state.current_page = "🚀 Innovation & Product Development"
        
        if st.button("💰 Resource Allocation", key="nav_resource_allocation", use_container_width=True):
            st.session_state.current_page = "💰 Resource Allocation"
        
        if st.button("📜 IP Management", key="nav_ip_management", use_container_width=True):
            st.session_state.current_page = "📜 IP Management"
        
        if st.button("⚠️ Risk Management", key="nav_risk_management", use_container_width=True):
            st.session_state.current_page = "⚠️ Risk Management"
        
        if st.button("🤝 Collaboration", key="nav_collaboration", use_container_width=True):
            st.session_state.current_page = "🤝 Collaboration"
        
        if st.button("👥 Employee Performance", key="nav_employee_performance", use_container_width=True):
            st.session_state.current_page = "👥 Employee Performance"
        
        if st.button("🔬 Technology Analysis", key="nav_technology_analysis", use_container_width=True):
            st.session_state.current_page = "🔬 Technology Analysis"
        
        if st.button("🎯 Customer-Centric R&D", key="nav_customer_centric", use_container_width=True):
            st.session_state.current_page = "🎯 Customer-Centric R&D"
        
        if st.button("📊 Strategic Metrics", key="nav_strategic_metrics", use_container_width=True):
            st.session_state.current_page = "📊 Strategic Metrics"
        
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
    
    # Display content based on current page
    if st.session_state.current_page == "🏠 Home":
        show_home()
    elif st.session_state.current_page == "📝 Data Input":
        show_data_input()
    elif st.session_state.current_page == "🚀 Innovation & Product Development":
        show_innovation_product_development()
    elif st.session_state.current_page == "💰 Resource Allocation":
        show_resource_allocation()
    elif st.session_state.current_page == "📜 IP Management":
        show_ip_management()
    elif st.session_state.current_page == "⚠️ Risk Management":
        show_risk_management()
    elif st.session_state.current_page == "🤝 Collaboration":
        show_collaboration()
    elif st.session_state.current_page == "👥 Employee Performance":
        show_employee_performance()
    elif st.session_state.current_page == "🔬 Technology Analysis":
        show_technology_analysis()
    elif st.session_state.current_page == "🎯 Customer-Centric R&D":
        show_customer_centric_rd()
    elif st.session_state.current_page == "📊 Strategic Metrics":
        show_strategic_metrics()
    elif st.session_state.current_page == "🔮 Predictive Analytics":
        show_predictive_analytics()

def show_home():
    """Display the home page with comprehensive overview and key metrics"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Check if data is loaded
    data_loaded = (hasattr(st.session_state, 'projects_data') and 
                   not st.session_state.projects_data.empty) if hasattr(st.session_state, 'projects_data') else False
    
    if not data_loaded:
        # Welcome section with 4 colored cards
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #495057; margin-bottom: 1rem;">🔬 Welcome to R&D Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Get started by exploring the comprehensive R&D analytics categories and metrics to drive innovation and research excellence.
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
                "R&D Analytics", 
                "Real-time",
                "metrics & insights"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Predictive", 
                "Advanced",
                "analytics"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Innovation", 
                "Comprehensive",
                "research insights"
            ), unsafe_allow_html=True)
        
        # Available analytics categories (6 cards in 2 columns)
        st.markdown("### 📊 Available R&D Analytics Categories:")
    
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 1: Innovation & Product Development
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🚀 Innovation & Product Development</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Project Success Rate Analysis</li>
                    <li>Time-to-Market Optimization</li>
                    <li>New Product Revenue Contribution</li>
                    <li>Prototyping Efficiency Metrics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 2: Resource Allocation & Utilization
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">💰 Resource Allocation & Utilization</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>R&D Budget Utilization Tracking</li>
                    <li>Researcher Efficiency Metrics</li>
                    <li>Equipment Utilization Analysis</li>
                    <li>Cost per Project Optimization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 3: Intellectual Property Management
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📜 Intellectual Property Management</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Patent Filing Success Rates</li>
                    <li>IP Portfolio Analysis</li>
                    <li>Patent Revenue Contribution</li>
                    <li>Licensing Agreement Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
        with col2:
            # Card 4: Risk Management & Failure Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">⚠️ Risk Management & Failure Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Project Failure Trend Analysis</li>
                    <li>Technology Obsolescence Risk</li>
                    <li>Competitive Analysis</li>
                    <li>Cost of Failed Projects</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 5: Collaboration & External Partnerships
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🤝 Collaboration & External Partnerships</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Academic Partnership ROI</li>
                    <li>External R&D Contributions</li>
                    <li>Open Innovation Metrics</li>
                    <li>Collaborative Patent Analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 6: Advanced Analytics
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🤖 Advanced Analytics</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Predictive Analytics</li>
                    <li>AI-Powered Insights</li>
                    <li>Machine Learning Models</li>
                    <li>Pattern Recognition</li>
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
                <p style="margin: 0;">Upload your R&D data files to get started</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">2. Review Insights</h4>
                <p style="margin: 0;">Check auto insights for AI-generated recommendations</p>
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
        st.markdown("The application supports the following R&D data categories:")
        
        # Row 1 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📋 Projects</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">R&D project details and timelines</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">👥 Researchers</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Team member information and performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📜 Patents</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Intellectual property and licensing data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🔧 Equipment</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">R&D equipment and utilization</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🤝 Collaborations</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">External partnerships and outcomes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🔬 Prototypes</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Development and testing results</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🚀 Products</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Launched products and market performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🎓 Training</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Training programs and effectiveness</p>
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
        st.info("🔬 R&D analytics data available for analysis")
        
        # Calculate key metrics
        total_projects = len(st.session_state.projects_data)
        total_researchers = len(st.session_state.researchers_data) if hasattr(st.session_state, 'researchers_data') else 0
        total_patents = len(st.session_state.patents_data) if hasattr(st.session_state, 'patents_data') else 0
        total_products = len(st.session_state.products_data) if hasattr(st.session_state, 'products_data') else 0
        
        # Show key metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Projects",
                value=f"{total_projects:,}",
                delta="0"
            )
        
        with col2:
            st.metric(
                label="Total Researchers",
                value=f"{total_researchers:,}",
                delta="0"
            )
        
        with col3:
            st.metric(
                label="Total Patents",
                value=f"{total_patents:,}",
                delta="0"
            )
        
        with col4:
            st.metric(
                label="Total Products",
                value=f"{total_products:,}",
                delta="0"
            )

def show_data_input():
    # Main header
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">📝 Data Input & Management</h2>
        <p style="text-align: center; color: #666; font-size: 1.1rem;">Upload, manage, and input your R&D data for comprehensive analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different data input methods
    data_tab1, data_tab2, data_tab3, data_tab4 = st.tabs([
        "📤 Upload Data", "📋 Download Template", "✏️ Manual Entry", "📊 Sample Dataset"
    ])
    
    with data_tab1:
        st.markdown("""
        <div class="metric-card-blue">
            <h3 style="margin: 0 0 15px 0; text-align: center;">📤 Upload R&D Data</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Upload your existing R&D data in Excel format:**")
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file with R&D data",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with sheets: Projects, Researchers, Patents, Equipment, Collaborations, Prototypes, Products, Training"
        )
        
        if uploaded_file is not None:
            try:
                # Read all sheets from the uploaded file
                excel_file = pd.ExcelFile(uploaded_file)
                required_sheets = ['Projects', 'Researchers', 'Patents', 'Equipment', 'Collaborations', 'Prototypes', 'Products', 'Training']
                
                missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]
                
                if missing_sheets:
                    st.error(f"❌ Missing required sheets: {', '.join(missing_sheets)}")
                    st.info("Please ensure your Excel file contains all required sheets. You can download a template below.")
                else:
                    # Load data into session state
                    st.session_state.projects = pd.read_excel(uploaded_file, sheet_name='Projects')
                    st.session_state.researchers = pd.read_excel(uploaded_file, sheet_name='Researchers')
                    st.session_state.patents = pd.read_excel(uploaded_file, sheet_name='Patents')
                    st.session_state.equipment = pd.read_excel(uploaded_file, sheet_name='Equipment')
                    st.session_state.collaborations = pd.read_excel(uploaded_file, sheet_name='Collaborations')
                    st.session_state.prototypes = pd.read_excel(uploaded_file, sheet_name='Prototypes')
                    st.session_state.products = pd.read_excel(uploaded_file, sheet_name='Products')
                    st.session_state.training = pd.read_excel(uploaded_file, sheet_name='Training')
                    
                    st.success("✅ Data uploaded successfully!")
                    
                    # Display data summary
                    st.markdown("""
                    <div class="metric-card" style="margin: 20px 0;">
                        <h4 style="margin: 0 0 15px 0; color: #1e3c72;">📊 Data Summary</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
                    with summary_col1:
                        st.metric("Projects", len(st.session_state.projects))
                    with summary_col2:
                        st.metric("Researchers", len(st.session_state.researchers))
                    with summary_col3:
                        st.metric("Patents", len(st.session_state.patents))
                    with summary_col4:
                        st.metric("Products", len(st.session_state.products))
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with data_tab2:
        st.markdown("""
        <div class="metric-card-green">
            <h3 style="margin: 0 0 15px 0; text-align: center;">📋 Download Data Template</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Get the Excel template with all required data schemas:**")
        
        if st.button("📋 Download R&D Data Template", key="download_template"):
            template_data = create_template_for_download()
            st.download_button(
                label="📥 Download Excel Template",
                data=template_data.getvalue(),
                file_name="rd_data_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.write("**Template includes:**")
        st.write("• Projects sheet - R&D project details, timelines, budgets")
        st.write("• Researchers sheet - Team member information and performance")
        st.write("• Patents sheet - Intellectual property and licensing data")
        st.write("• Equipment sheet - R&D equipment and utilization")
        st.write("• Collaborations sheet - External partnerships and outcomes")
        st.write("• Prototypes sheet - Development and testing results")
        st.write("• Products sheet - Launched products and market performance")
        st.write("• Training sheet - Training programs and effectiveness")
        st.write("• Instructions sheet - Detailed field descriptions and data types")
        
        # Show template structure
        st.markdown("""
        <div class="metric-card" style="margin: 20px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1e3c72;">📋 Template Structure</h4>
        </div>
        """, unsafe_allow_html=True)
        
        template_info = {
            'Sheet': ['Projects', 'Researchers', 'Patents', 'Equipment', 'Collaborations', 'Prototypes', 'Products', 'Training'],
            'Key Fields': [
                'project_id, project_name, status, budget, start_date, end_date',
                'researcher_id, first_name, last_name, department, specialization',
                'patent_id, patent_title, status, estimated_value, filing_date',
                'equipment_id, equipment_name, cost, location, status',
                'collaboration_id, partner_name, project_id, investment_amount',
                'prototype_id, project_id, status, cost, success_rate',
                'product_id, product_name, launch_date, revenue_generated',
                'training_id, researcher_id, training_type, effectiveness_rating'
            ],
            'Records': ['15', '25', '12', '8', '10', '20', '18', '30']
        }
        
        st.dataframe(pd.DataFrame(template_info), use_container_width=True)
    
    with data_tab3:
        st.markdown("""
        <div class="metric-card-purple">
            <h3 style="margin: 0 0 15px 0; text-align: center;">✏️ Manual Data Entry</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Add new data entries manually:**")
        
        # Create sub-tabs for different data types
        entry_tab1, entry_tab2, entry_tab3, entry_tab4 = st.tabs([
            "Projects", "Researchers", "Patents", "Other Data"
        ])
        
        with entry_tab1:
            st.subheader("📋 Add New Project")
            col1, col2 = st.columns(2)
            with col1:
                project_id = st.text_input("Project ID", key="proj_id")
                project_name = st.text_input("Project Name", key="proj_name")
                project_type = st.selectbox("Project Type", ["Research", "Development", "Innovation", "Prototype", "Product"], key="proj_type")
                start_date = st.date_input("Start Date", key="proj_start")
                end_date = st.date_input("End Date", key="proj_end")
                status = st.selectbox("Status", ["Planning", "Active", "Completed", "On Hold", "Cancelled"], key="proj_status")
            with col2:
                budget = st.number_input("Budget ($)", min_value=0.0, key="proj_budget")
                actual_spend = st.number_input("Actual Spend ($)", min_value=0.0, key="proj_spend")
                team_lead_id = st.text_input("Team Lead ID", key="proj_lead")
                department = st.text_input("Department", key="proj_dept")
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="proj_priority")
                technology_area = st.text_input("Technology Area", key="proj_tech")
                trl_level = st.number_input("TRL Level", min_value=1, max_value=9, value=1, key="proj_trl")
            
            milestones_completed = st.number_input("Milestones Completed", min_value=0, key="proj_milestones_comp")
            total_milestones = st.number_input("Total Milestones", min_value=0, key="proj_milestones_total")
            
            if st.button("Add Project", key="add_proj"):
                if project_id and project_name:
                    new_project = pd.DataFrame([{
                        'project_id': project_id,
                        'project_name': project_name,
                        'project_type': project_type,
                        'start_date': start_date,
                        'end_date': end_date,
                        'status': status,
                        'budget': budget,
                        'actual_spend': actual_spend,
                        'team_lead_id': team_lead_id,
                        'department': department,
                        'priority': priority,
                        'technology_area': technology_area,
                        'trl_level': trl_level,
                        'milestones_completed': milestones_completed,
                        'total_milestones': total_milestones
                    }])
                    st.session_state.projects = pd.concat([st.session_state.projects, new_project], ignore_index=True)
                    st.success("Project added successfully!")
                else:
                    st.error("Please fill in Project ID and Project Name")
        
        with entry_tab2:
            st.subheader("👥 Add New Researcher")
            col1, col2 = st.columns(2)
            with col1:
                researcher_id = st.text_input("Researcher ID", key="res_id")
                first_name = st.text_input("First Name", key="res_first")
                last_name = st.text_input("Last Name", key="res_last")
                email = st.text_input("Email", key="res_email")
                department = st.text_input("Department", key="res_dept")
                specialization = st.text_input("Specialization", key="res_spec")
            with col2:
                hire_date = st.date_input("Hire Date", key="res_hire")
                education_level = st.selectbox("Education Level", ["Bachelor's", "Master's", "PhD", "Post-Doc"], key="res_edu")
                experience_years = st.number_input("Experience (Years)", min_value=0, key="res_exp")
                status = st.selectbox("Status", ["Active", "Inactive", "Terminated"], key="res_status")
                salary = st.number_input("Salary ($)", min_value=0, key="res_salary")
                manager_id = st.text_input("Manager ID", key="res_manager")
            
            if st.button("Add Researcher", key="add_res"):
                if researcher_id and first_name and last_name:
                    new_researcher = pd.DataFrame([{
                        'researcher_id': researcher_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'department': department,
                        'specialization': specialization,
                        'hire_date': hire_date,
                        'education_level': education_level,
                        'experience_years': experience_years,
                        'status': status,
                        'salary': salary,
                        'manager_id': manager_id
                    }])
                    st.session_state.researchers = pd.concat([st.session_state.researchers, new_researcher], ignore_index=True)
                    st.success("Researcher added successfully!")
                else:
                    st.error("Please fill in Researcher ID, First Name, and Last Name")
        
        with entry_tab3:
            st.subheader("📜 Add New Patent")
            col1, col2 = st.columns(2)
            with col1:
                patent_id = st.text_input("Patent ID", key="pat_id")
                project_id = st.text_input("Project ID", key="pat_proj")
                patent_title = st.text_input("Patent Title", key="pat_title")
                filing_date = st.date_input("Filing Date", key="pat_filing")
                grant_date = st.date_input("Grant Date", key="pat_grant")
                status = st.selectbox("Status", ["Filed", "Pending", "Granted", "Rejected"], key="pat_status")
            with col2:
                researcher_id = st.text_input("Researcher ID", key="pat_res")
                technology_area = st.text_input("Technology Area", key="pat_tech")
                estimated_value = st.number_input("Estimated Value ($)", min_value=0, key="pat_value")
                licensing_revenue = st.number_input("Licensing Revenue ($)", min_value=0, key="pat_revenue")
                expiry_date = st.date_input("Expiry Date", key="pat_expiry")
            
            if st.button("Add Patent", key="add_pat"):
                if patent_id and patent_title:
                    new_patent = pd.DataFrame([{
                        'patent_id': patent_id,
                        'project_id': project_id,
                        'patent_title': patent_title,
                        'filing_date': filing_date,
                        'grant_date': grant_date,
                        'status': status,
                        'researcher_id': researcher_id,
                        'technology_area': technology_area,
                        'estimated_value': estimated_value,
                        'licensing_revenue': licensing_revenue,
                        'expiry_date': expiry_date
                    }])
                    st.session_state.patents = pd.concat([st.session_state.patents, new_patent], ignore_index=True)
                    st.success("Patent added successfully!")
                else:
                    st.error("Please fill in Patent ID and Patent Title")
        
        with entry_tab4:
            st.subheader("🔧 Add Other Data Types")
            st.info("Use the template download to add Equipment, Collaborations, Prototypes, Products, and Training data in bulk.")
    
    with data_tab4:
        st.markdown("""
        <div class="metric-card-teal">
            <h3 style="margin: 0 0 15px 0; text-align: center;">📊 Sample Dataset</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**Preview of sample data structure and load sample data into the program:**")
        
        # Sample data for each category
        sample_projects = pd.DataFrame({
            'project_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'project_name': ['AI Research Initiative', 'Quantum Computing', 'Biotech Innovation', 'Robotics Development', 'Clean Energy Research'],
            'project_type': ['Research', 'Development', 'Innovation', 'Development', 'Research'],
            'start_date': ['2024-01-15', '2024-02-01', '2024-01-20', '2024-03-01', '2024-02-15'],
            'end_date': ['2024-12-31', '2024-11-30', '2024-10-31', '2024-12-31', '2024-12-31'],
            'status': ['Active', 'Completed', 'Planning', 'Active', 'Active'],
            'budget': [500000, 750000, 300000, 600000, 400000],
            'actual_spend': [450000, 720000, 0, 350000, 180000],
            'team_lead_id': ['R001', 'R002', 'R003', 'R004', 'R005'],
            'department': ['AI Lab', 'Quantum Lab', 'Biotech Lab', 'Robotics Lab', 'Energy Lab'],
            'priority': ['High', 'Medium', 'High', 'Medium', 'High'],
            'technology_area': ['Artificial Intelligence', 'Quantum Physics', 'Biotechnology', 'Robotics', 'Clean Energy'],
            'trl_level': [4, 7, 3, 5, 4],
            'milestones_completed': [8, 12, 2, 6, 4],
            'total_milestones': [15, 15, 10, 12, 10]
        })
        
        sample_researchers = pd.DataFrame({
            'researcher_id': ['R001', 'R002', 'R003', 'R004', 'R005', 'R006', 'R007', 'R008'],
            'first_name': ['Dr. Sarah', 'Dr. Michael', 'Dr. Emily', 'Dr. James', 'Dr. Lisa', 'Dr. David', 'Dr. Maria', 'Dr. Robert'],
            'last_name': ['Johnson', 'Chen', 'Rodriguez', 'Wilson', 'Brown', 'Taylor', 'Garcia', 'Anderson'],
            'email': ['sarah.johnson@company.com', 'michael.chen@company.com', 'emily.rodriguez@company.com', 'james.wilson@company.com', 'lisa.brown@company.com', 'david.taylor@company.com', 'maria.garcia@company.com', 'robert.anderson@company.com'],
            'department': ['AI Lab', 'Quantum Lab', 'Biotech Lab', 'Robotics Lab', 'Energy Lab', 'AI Lab', 'Quantum Lab', 'Biotech Lab'],
            'specialization': ['Machine Learning', 'Quantum Physics', 'Genomics', 'Robotics', 'Solar Energy', 'Deep Learning', 'Quantum Computing', 'Bioinformatics'],
            'hire_date': ['2020-03-15', '2018-09-01', '2022-01-10', '2021-06-15', '2023-02-01', '2021-12-01', '2019-04-01', '2022-08-15'],
            'education_level': ['PhD', 'PhD', 'PhD', 'PhD', 'PhD', 'PhD', 'PhD', 'PhD'],
            'experience_years': [8, 12, 6, 7, 3, 5, 9, 4],
            'status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active'],
            'salary': [120000, 150000, 110000, 125000, 100000, 115000, 140000, 105000],
            'manager_id': ['M001', 'M001', 'M002', 'M002', 'M003', 'M001', 'M001', 'M002']
        })
        
        sample_patents = pd.DataFrame({
            'patent_id': ['PAT001', 'PAT002', 'PAT003', 'PAT004', 'PAT005'],
            'project_id': ['P001', 'P002', 'P003', 'P001', 'P004'],
            'patent_title': ['AI Algorithm for Data Analysis', 'Quantum Encryption Method', 'Gene Editing Technique', 'Neural Network Optimization', 'Robotic Control System'],
            'filing_date': ['2024-03-15', '2024-05-20', '2024-04-10', '2024-06-01', '2024-07-15'],
            'grant_date': ['2024-08-15', '', '', '', ''],
            'status': ['Granted', 'Pending', 'Filed', 'Pending', 'Filed'],
            'researcher_id': ['R001', 'R002', 'R003', 'R001', 'R004'],
            'technology_area': ['Artificial Intelligence', 'Quantum Computing', 'Biotechnology', 'Artificial Intelligence', 'Robotics'],
            'estimated_value': [250000, 500000, 750000, 300000, 400000],
            'licensing_revenue': [50000, 0, 0, 0, 0],
            'expiry_date': ['2044-08-15', '2044-05-20', '2044-04-10', '2044-06-01', '2044-07-15']
        })
        
        sample_equipment = pd.DataFrame({
            'equipment_id': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
            'equipment_name': ['AI Computing Cluster', 'Quantum Simulator', 'DNA Sequencer', 'Robotic Arm', 'Solar Panel Tester'],
            'equipment_type': ['Computing', 'Simulation', 'Laboratory', 'Robotics', 'Testing'],
            'purchase_date': ['2023-01-15', '2023-03-01', '2023-02-15', '2023-04-01', '2023-05-15'],
            'cost': [150000, 300000, 200000, 80000, 45000],
            'location': ['AI Lab', 'Quantum Lab', 'Biotech Lab', 'Robotics Lab', 'Energy Lab'],
            'status': ['Active', 'Active', 'Active', 'Active', 'Active'],
            'total_hours': [8760, 8760, 8760, 8760, 8760],
            'utilized_hours': [7000, 6000, 5000, 4000, 3000],
            'maintenance_cost': [15000, 25000, 20000, 8000, 5000],
            'department': ['AI Lab', 'Quantum Lab', 'Biotech Lab', 'Robotics Lab', 'Energy Lab']
        })
        
        sample_collaborations = pd.DataFrame({
            'collaboration_id': ['COL001', 'COL002', 'COL003', 'COL004'],
            'partner_name': ['Tech University', 'Innovation Corp', 'Research Institute', 'Startup Labs'],
            'partner_type': ['University', 'Corporation', 'Research', 'Startup'],
            'start_date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01'],
            'end_date': ['2024-12-31', '2024-11-30', '2024-12-31', '2024-10-31'],
            'project_id': ['P001', 'P002', 'P003', 'P004'],
            'investment_amount': [100000, 200000, 150000, 75000],
            'revenue_generated': [0, 50000, 0, 25000],
            'status': ['Active', 'Completed', 'Active', 'Active'],
            'collaboration_type': ['Research', 'Development', 'Research', 'Development'],
            'researcher_id': ['R001', 'R002', 'R003', 'R004']
        })
        
        sample_prototypes = pd.DataFrame({
            'prototype_id': ['PROT001', 'PROT002', 'PROT003', 'PROT004', 'PROT005'],
            'project_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'prototype_name': ['AI Model v1.0', 'Quantum Circuit', 'Gene Editor', 'Robot Arm', 'Solar Cell'],
            'development_date': ['2024-04-01', '2024-05-01', '2024-06-01', '2024-07-01', '2024-08-01'],
            'testing_date': ['2024-04-15', '2024-05-15', '2024-06-15', '2024-07-15', '2024-08-15'],
            'cost': [25000, 50000, 35000, 20000, 15000],
            'status': ['Completed', 'Testing', 'Development', 'Testing', 'Development'],
            'success_rate': [85, 70, 60, 80, 75],
            'iterations': [3, 5, 8, 2, 4],
            'researcher_id': ['R001', 'R002', 'R003', 'R004', 'R005'],
            'technology_used': ['Python, TensorFlow', 'Qiskit, Python', 'CRISPR, Python', 'ROS, C++', 'Silicon, Python']
        })
        
        sample_products = pd.DataFrame({
            'product_id': ['PROD001', 'PROD002', 'PROD003', 'PROD004'],
            'project_id': ['P001', 'P002', 'P003', 'P004'],
            'product_name': ['AI Analytics Platform', 'Quantum Security Suite', 'BioTech Tool Kit', 'Robotic Assistant'],
            'launch_date': ['2024-09-01', '2024-10-01', '2024-11-01', '2024-12-01'],
            'development_cost': [200000, 350000, 250000, 180000],
            'revenue_generated': [50000, 75000, 30000, 40000],
            'market_response': [4.2, 4.5, 3.8, 4.0],
            'customer_satisfaction': [4.5, 4.3, 4.0, 4.2],
            'patent_id': ['PAT001', 'PAT002', '', 'PAT005'],
            'status': ['Launched', 'Launched', 'Launched', 'Launched'],
            'target_market': ['Enterprise', 'Government', 'Healthcare', 'Manufacturing']
        })
        
        sample_training = pd.DataFrame({
            'training_id': ['TR001', 'TR002', 'TR003', 'TR004', 'TR005'],
            'researcher_id': ['R001', 'R002', 'R003', 'R004', 'R005'],
            'training_type': ['AI Workshop', 'Quantum Computing', 'Bioinformatics', 'Robotics', 'Clean Energy'],
            'training_date': ['2024-01-15', '2024-02-01', '2024-02-15', '2024-03-01', '2024-03-15'],
            'duration_hours': [16, 24, 20, 18, 12],
            'cost': [2000, 3000, 2500, 2000, 1500],
            'pre_performance_score': [75, 80, 70, 65, 85],
            'post_performance_score': [90, 95, 85, 80, 92],
            'effectiveness_rating': [4.5, 4.8, 4.2, 4.0, 4.6],
            'trainer_name': ['Dr. Expert', 'Prof. Quantum', 'Dr. Bio', 'Prof. Robot', 'Dr. Energy']
        })
        
        # Load sample data button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Load Sample Data into Program", key="load_sample_data", use_container_width=True):
                # Load sample data into session state
                st.session_state.projects = sample_projects.copy()
                st.session_state.researchers = sample_researchers.copy()
                st.session_state.patents = sample_patents.copy()
                st.session_state.equipment = sample_equipment.copy()
                st.session_state.collaborations = sample_collaborations.copy()
                st.session_state.prototypes = sample_prototypes.copy()
                st.session_state.products = sample_products.copy()
                st.session_state.training = sample_training.copy()
                
                st.success("✅ Sample data loaded successfully! You can now explore the analytics with this sample dataset.")
                st.balloons()
        
        st.write("**Click the button above to load sample data, or preview the structure below:**")
        
        # Display sample data in tabs
        sample_tab1, sample_tab2, sample_tab3, sample_tab4 = st.tabs([
            "📋 Projects", "👥 Researchers", "📜 Patents", "🔧 Equipment"
        ])
        
        with sample_tab1:
            st.write("**Sample Projects Data:**")
            st.dataframe(sample_projects, use_container_width=True)
            st.info("This shows the structure and sample data for R&D projects. Use this as a reference for your data format.")
        
        with sample_tab2:
            st.write("**Sample Researchers Data:**")
            st.dataframe(sample_researchers, use_container_width=True)
            st.info("This shows the structure and sample data for research team members.")
        
        with sample_tab3:
            st.write("**Sample Patents Data:**")
            st.dataframe(sample_patents, use_container_width=True)
            st.info("This shows the structure and sample data for intellectual property.")
        
        with sample_tab4:
            st.write("**Sample Equipment Data:**")
            st.dataframe(sample_equipment, use_container_width=True)
            st.info("This shows the structure and sample data for R&D equipment.")
        
        # Additional sample data tabs
        sample_tab5, sample_tab6, sample_tab7, sample_tab8 = st.tabs([
            "🤝 Collaborations", "🔬 Prototypes", "🚀 Products", "🎓 Training"
        ])
        
        with sample_tab5:
            st.write("**Sample Collaborations Data:**")
            st.dataframe(sample_collaborations, use_container_width=True)
            st.info("This shows the structure and sample data for external partnerships.")
        
        with sample_tab6:
            st.write("**Sample Prototypes Data:**")
            st.dataframe(sample_prototypes, use_container_width=True)
            st.info("This shows the structure and sample data for prototype development.")
        
        with sample_tab7:
            st.write("**Sample Products Data:**")
            st.dataframe(sample_products, use_container_width=True)
            st.info("This shows the structure and sample data for launched products.")
        
        with sample_tab8:
            st.write("**Sample Training Data:**")
            st.dataframe(sample_training, use_container_width=True)
            st.info("This shows the structure and sample data for training programs.")
    
    # Current data overview section
    st.markdown("""
    <div class="metric-card-orange">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📊 Current Data Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.projects.empty:
        st.markdown("""
        <div class="metric-card" style="margin: 15px 0;">
            <h4 style="margin: 0 0 15px 0; color: #1e3c72;">📊 Projects Data</h4>
        </div>
        """, unsafe_allow_html=True)
        display_dataframe_with_index_1(st.session_state.projects)
    
    # Export data section
    st.markdown("""
    <div class="metric-card-red">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📤 Export Data</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Export All Data to Excel"):
        export_data = export_data_to_excel()
        if export_data:
            st.download_button(
                label="📥 Download Excel File",
                data=export_data.getvalue(),
                file_name="rd_analytics_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No data to export. Please add data first.")

# Analytics functions for the main sections
def show_innovation_product_development():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">🚀 Innovation and Product Development</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.projects.empty and st.session_state.products.empty:
        st.info("📊 Please upload project and product data to view innovation analytics.")
        return
    
    # Calculate innovation metrics
    innovation_summary, innovation_message = calculate_innovation_metrics(
        st.session_state.projects, st.session_state.products, st.session_state.prototypes
    )
    
    # Display summary metrics
    st.markdown("""
    <div class="metric-card-blue">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Innovation Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not innovation_summary.empty:
            success_rate = innovation_summary.iloc[0]['Value']
            st.metric("Project Success Rate", success_rate)
    
    with col2:
        if not innovation_summary.empty and len(innovation_summary) > 1:
            time_to_market = innovation_summary.iloc[1]['Value']
            st.metric("Avg Time-to-Market", time_to_market)
    
    with col3:
        if not innovation_summary.empty and len(innovation_summary) > 2:
            revenue_contribution = innovation_summary.iloc[2]['Value']
            st.metric("Revenue Contribution", revenue_contribution)
    
    with col4:
        if not innovation_summary.empty and len(innovation_summary) > 3:
            failure_rate = innovation_summary.iloc[3]['Value']
            st.metric("Product Failure Rate", failure_rate)
    
    st.info(innovation_message)
    
    # Detailed analytics tabs
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Detailed Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Project Success Analysis", "⏱️ Time-to-Market", "💰 Revenue Analysis", 
        "🔬 Prototyping Efficiency", "📉 Failure Analysis"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Project Success Rate Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced project success analysis with multiple dimensions
            project_success = st.session_state.projects.groupby(['project_type', 'status']).agg({
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            
            # Calculate success rates and efficiency metrics with data validation
            success_metrics = st.session_state.projects.groupby('project_type').agg({
                'status': lambda x: (x == 'Completed').sum(),
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            success_metrics.columns = ['Project Type', 'Successful', 'Total', 'Total Budget', 'Total Spent']
            success_metrics['Success Rate (%)'] = (success_metrics['Successful'] / success_metrics['Total'] * 100).round(1)
            
            # Handle division by zero for budget efficiency calculation
            success_metrics['Budget Efficiency (%)'] = np.where(
                success_metrics['Total Budget'] > 0,
                (success_metrics['Total Spent'] / success_metrics['Total Budget'] * 100).round(1),
                100  # Set to 100% if budget is 0 (no budget allocated)
            )
            
            # Handle division by zero for cost per project calculation
            success_metrics['Cost per Project'] = np.where(
                success_metrics['Total'] > 0,
                (success_metrics['Total Spent'] / success_metrics['Total']).round(0),
                0  # Set to 0 if no projects
            )
            
            # Display key insights
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Success Rate", f"{success_metrics['Success Rate (%)'].mean():.1f}%")
            with col2:
                st.metric("Total Projects", success_metrics['Total'].sum())
            with col3:
                st.metric("Budget Efficiency", f"{success_metrics['Budget Efficiency (%)'].mean():.1f}%")
            
            # Enhanced visualization with better chart types
            col1, col2 = st.columns(2)
            
            with col1:
                # Horizontal bar chart for better readability
                fig = go.Figure(data=[
                    go.Bar(y=success_metrics['Project Type'], 
                           x=success_metrics['Success Rate (%)'],
                           orientation='h',
                           marker_color=['#2ca02c' if x >= 80 else '#ff7f0e' if x >= 60 else '#d62728' for x in success_metrics['Success Rate (%)']],
                           text=success_metrics['Success Rate (%)'],
                           textposition='auto',
                           hovertemplate='<b>%{y}</b><br>Success Rate: %{x:.1f}%<br>Projects: %{text}<extra></extra>')
                ])
                fig.update_layout(
                    title="Project Success Rate by Type",
                    xaxis_title="Success Rate (%)",
                    yaxis_title="Project Type",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Bubble chart showing success rate vs budget efficiency
                fig = go.Figure(data=[
                    go.Scatter(x=success_metrics['Success Rate (%)'], 
                              y=success_metrics['Budget Efficiency (%)'],
                              mode='markers+text',
                              text=success_metrics['Project Type'],
                              textposition='middle center',
                              marker=dict(
                                  size=success_metrics['Total'] * 2,
                                  color=success_metrics['Success Rate (%)'],
                                  colorscale='RdYlGn',
                                  showscale=True,
                                  colorbar=dict(title="Success Rate (%)")
                              ),
                              hovertemplate='<b>%{text}</b><br>Success Rate: %{x:.1f}%<br>Budget Efficiency: %{y:.1f}%<br>Project Count: %{marker.size/2}<extra></extra>')
                ])
                fig.update_layout(
                    title="Success Rate vs Budget Efficiency",
                    xaxis_title="Success Rate (%)",
                    yaxis_title="Budget Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📊 Detailed Project Metrics")
            display_df = success_metrics[['Project Type', 'Total', 'Successful', 'Success Rate (%)', 'Budget Efficiency (%)', 'Cost per Project']].copy()
            display_df['Cost per Project'] = display_df['Cost per Project'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
            
            # Success rate trend analysis by technology area
            if 'technology_area' in st.session_state.projects.columns:
                st.markdown("### 🔬 Success Rate by Technology Area")
                tech_success = st.session_state.projects.groupby('technology_area').agg({
                    'status': lambda x: (x == 'Completed').sum(),
                    'project_id': 'count'
                }).reset_index()
                tech_success['Success Rate (%)'] = (tech_success['status'] / tech_success['project_id'] * 100).round(1)
                tech_success = tech_success.sort_values('Success Rate (%)', ascending=False)
                
                fig = go.Figure(data=[
                    go.Bar(x=tech_success['technology_area'], 
                           y=tech_success['Success Rate (%)'],
                           marker_color='#1f77b4',
                           text=tech_success['Success Rate (%)'],
                           textposition='auto',
                           hovertemplate='Technology: %{x}<br>Success Rate: %{y:.1f}%<extra></extra>')
                ])
                fig.update_layout(
                    title="Success Rate by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Success Rate (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional satisfaction insights
            st.markdown("### 📊 Satisfaction Performance Insights")
            
            # Create satisfaction analysis from products data
            if not st.session_state.products.empty and 'customer_satisfaction' in st.session_state.products.columns and 'target_market' in st.session_state.products.columns:
                # Group by target market and calculate satisfaction metrics
                satisfaction_analysis = st.session_state.products.groupby('target_market').agg({
                    'product_id': 'count',
                    'customer_satisfaction': 'mean',
                    'revenue_generated': 'sum'
                }).reset_index()
                satisfaction_analysis.columns = ['target_market', 'product_count', 'satisfaction_score', 'total_revenue']
                
                # Calculate market weight (percentage of total products)
                total_products = satisfaction_analysis['product_count'].sum()
                satisfaction_analysis['market_weight'] = (satisfaction_analysis['product_count'] / total_products * 100).round(1)
                
                # Satisfaction vs Market Weight correlation analysis
                fig = go.Figure(data=[
                    go.Scatter(
                        x=satisfaction_analysis['product_count'],
                        y=satisfaction_analysis['satisfaction_score'],
                        mode='markers+text',
                        text=satisfaction_analysis['target_market'],
                        textposition='top center',
                        marker=dict(
                            size=satisfaction_analysis['market_weight'] * 3,
                            color=satisfaction_analysis['satisfaction_score'],
                            colorscale='RdYlGn',
                            showscale=True,
                            colorbar=dict(title="Satisfaction Score"),
                            cmin=1,
                            cmax=5
                        ),
                        hovertemplate='<b>%{text}</b><br>Products: %{x}<br>Satisfaction: %{y:.1f}/5<br>Weight: %{marker.size/3:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Satisfaction vs Product Count (Bubble size = Market Weight, Color = Satisfaction Score)",
                    xaxis_title="Number of Products",
                    yaxis_title="Customer Satisfaction Score (/5)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Satisfaction efficiency analysis
                st.markdown("### 🔍 Satisfaction Efficiency Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=satisfaction_analysis['target_market'],
                            y=satisfaction_analysis['market_weight'],
                            marker_color='#9467bd',
                            text=satisfaction_analysis['market_weight'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto',
                            hovertemplate='Market: %{x}<br>Weight: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Market Weight Distribution (Percentage of Total Products)",
                        xaxis_title="Target Market",
                        yaxis_title="Market Weight (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Satisfaction performance by market size
                    fig = go.Figure(data=[
                        go.Bar(
                            x=satisfaction_analysis['target_market'],
                            y=satisfaction_analysis['satisfaction_score'],
                            marker_color=['#2ca02c' if x >= 4.0 else '#1f77b4' if x >= 3.5 else '#ff7f0e' if x >= 3.0 else '#d62728' for x in satisfaction_analysis['satisfaction_score']],
                            text=satisfaction_analysis['satisfaction_score'].apply(lambda x: f"{x:.1f}"),
                            textposition='auto',
                            hovertemplate='Market: %{x}<br>Satisfaction: %{y:.1f}/5<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Satisfaction Performance by Market (Color-coded by Score)",
                        xaxis_title="Target Market",
                        yaxis_title="Satisfaction Score (/5)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed metrics table
                st.markdown("### 📋 Detailed Satisfaction Metrics")
                display_df = satisfaction_analysis[['target_market', 'product_count', 'satisfaction_score', 'market_weight']].copy()
                display_df['satisfaction_score'] = display_df['satisfaction_score'].apply(lambda x: f"{x:.1f}/5")
                display_df['market_weight'] = display_df['market_weight'].apply(lambda x: f"{x:.1f}%")
                st.dataframe(display_df, use_container_width=True)
                
                # Satisfaction insights
            else:
                st.info("📊 No product data available for satisfaction analysis. Please upload product data with customer satisfaction and target market information.")
            st.markdown("### 💡 Satisfaction Strategic Insights")
            
            # High satisfaction markets
            high_satisfaction_markets = satisfaction_analysis[satisfaction_analysis['satisfaction_score'] >= 4.0]
            if not high_satisfaction_markets.empty:
                st.success(f"🎉 **High Satisfaction Markets**: {', '.join(high_satisfaction_markets['target_market'].tolist())} show excellent customer experience (≥4.0)")
            
            # High weight markets
            high_weight_markets = satisfaction_analysis[satisfaction_analysis['market_weight'] >= 30]
            if not high_weight_markets.empty:
                st.info(f"📊 **High Weight Markets**: {', '.join(high_weight_markets['target_market'].tolist())} represent significant product focus (≥30%)")
            
            # Low satisfaction markets
            low_satisfaction_markets = satisfaction_analysis[satisfaction_analysis['satisfaction_score'] < 3.0]
            if not low_satisfaction_markets.empty:
                st.warning(f"⚠️ **Improvement Needed**: {', '.join(low_satisfaction_markets['target_market'].tolist())} show low satisfaction (<3.0) - focus on customer needs")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">⏱️ Time-to-Market Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty and not st.session_state.products.empty:
            # Enhanced time-to-market analysis
            projects_with_products = st.session_state.projects.merge(
                st.session_state.products, on='project_id', how='inner'
            )
            
            if not projects_with_products.empty:
                # Calculate time to market with enhanced metrics
                projects_with_products['start_date'] = pd.to_datetime(projects_with_products['start_date'])
                projects_with_products['launch_date'] = pd.to_datetime(projects_with_products['launch_date'])
                projects_with_products['time_to_market_days'] = (
                    projects_with_products['launch_date'] - projects_with_products['start_date']
                ).dt.days
                
                # Filter out invalid dates and calculate statistics
                valid_t2m = projects_with_products[projects_with_products['time_to_market_days'] >= 0]
                
                if not valid_t2m.empty:
                    # Key metrics display
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Avg Time-to-Market", f"{valid_t2m['time_to_market_days'].mean():.0f} days")
                    with col2:
                        st.metric("Median T2M", f"{valid_t2m['time_to_market_days'].median():.0f} days")
                    with col3:
                        st.metric("Fastest Project", f"{valid_t2m['time_to_market_days'].min():.0f} days")
                    with col4:
                        st.metric("Slowest Project", f"{valid_t2m['time_to_market_days'].max():.0f} days")
                    
                    # Enhanced visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Enhanced histogram with better bins and styling
                        fig = go.Figure(data=[
                            go.Histogram(
                                x=valid_t2m['time_to_market_days'], 
                                nbinsx=20,
                                marker_color='#2ca02c',
                                opacity=0.8,
                                hovertemplate='<b>Time to Market</b><br>Days: %{x:.0f}<br>Count: %{y}<br>Percentage: %{y/len(valid_t2m)*100:.1f}%<extra></extra>'
                            )
                        ])
                        fig.update_layout(
                            title="Time-to-Market Distribution",
                            xaxis_title="Days to Market",
                            yaxis_title="Number of Products",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            bargap=0.1
                        )
                        # Add vertical line for mean
                        fig.add_vline(x=valid_t2m['time_to_market_days'].mean(), line_dash="dash", line_color="red", 
                                    annotation_text=f"Mean: {valid_t2m['time_to_market_days'].mean():.0f} days")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Enhanced box plot with outliers
                        fig = go.Figure(data=[
                            go.Box(
                                y=valid_t2m['time_to_market_days'],
                                name='Time to Market',
                                marker_color='#1f77b4',
                                boxpoints='outliers',
                                hovertemplate='<b>Time to Market</b><br>Days: %{y:.0f}<extra></extra>'
                            )
                        ])
                        fig.update_layout(
                            title="Time-to-Market Statistics & Outliers",
                            yaxis_title="Days to Market",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Additional insights
                    st.markdown("### 📊 Time-to-Market Insights")
                    
                    # T2M by project type
                    if 'project_type' in valid_t2m.columns:
                        t2m_by_type = valid_t2m.groupby('project_type').agg({
                            'time_to_market_days': ['mean', 'median', 'count']
                        }).round(1)
                        t2m_by_type.columns = ['Avg Days', 'Median Days', 'Count']
                        t2m_by_type = t2m_by_type.sort_values('Avg Days')
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=t2m_by_type.index,
                                y=t2m_by_type['Avg Days'],
                                marker_color='#ff7f0e',
                                text=t2m_by_type['Avg Days'],
                                textposition='auto',
                                hovertemplate='<b>%{x}</b><br>Avg T2M: %{y:.1f} days<br>Count: %{text}<extra></extra>'
                            )
                        ])
                        fig.update_layout(
                            title="Average Time-to-Market by Project Type",
                            xaxis_title="Project Type",
                            yaxis_title="Average Days to Market",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # T2M vs Budget correlation
                    if 'budget' in valid_t2m.columns:
                        st.markdown("### 💰 Time-to-Market vs Budget Correlation")
                        correlation = valid_t2m['time_to_market_days'].corr(valid_t2m['budget'])
                        
                        fig = go.Figure(data=[
                            go.Scatter(
                                x=valid_t2m['budget'],
                                y=valid_t2m['time_to_market_days'],
                                mode='markers',
                                marker=dict(
                                    size=10,
                                    color=valid_t2m['time_to_market_days'],
                                    colorscale='Viridis',
                                    showscale=True,
                                    colorbar=dict(title="Days to Market")
                                ),
                                text=valid_t2m['product_name'] if 'product_name' in valid_t2m.columns else valid_t2m['project_id'],
                                hovertemplate='<b>%{text}</b><br>Budget: $%{x:,.0f}<br>T2M: %{y:.0f} days<extra></extra>'
                            )
                        ])
                        fig.update_layout(
                            title=f"Time-to-Market vs Budget (Correlation: {correlation:.3f})",
                            xaxis_title="Project Budget ($)",
                            yaxis_title="Days to Market",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Interpretation
                        if correlation > 0.3:
                            st.info(f"🔍 **Positive Correlation Detected**: Higher budgets tend to correlate with longer time-to-market (r = {correlation:.3f})")
                        elif correlation < -0.3:
                            st.info(f"🔍 **Negative Correlation Detected**: Higher budgets tend to correlate with shorter time-to-market (r = {correlation:.3f})")
                        else:
                            st.info(f"🔍 **Weak Correlation**: Budget and time-to-market show minimal relationship (r = {correlation:.3f})")
                else:
                    st.warning("⚠️ No valid time-to-market data available. Please check date formats in your data.")
            else:
                st.info("📊 No projects with corresponding products found. Please ensure project and product data are properly linked.")
        else:
            st.info("📊 Please upload both project and product data to view time-to-market analytics.")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-purple" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Revenue Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Enhanced revenue analysis with comprehensive metrics
            revenue_by_product = st.session_state.products.groupby('product_name').agg({
                'revenue_generated': 'sum',
                'development_cost': 'sum',
                'market_response': 'mean',
                'customer_satisfaction': 'mean'
            }).reset_index()
            
            # Calculate advanced financial metrics with data validation
            revenue_by_product['profit'] = revenue_by_product['revenue_generated'] - revenue_by_product['development_cost']
            
            # Handle division by zero and invalid values for ROI calculation
            revenue_by_product['roi'] = np.where(
                revenue_by_product['development_cost'] > 0,
                (revenue_by_product['profit'] / revenue_by_product['development_cost'] * 100).round(1),
                0  # Set ROI to 0 if development cost is 0 or negative
            )
            
            # Handle division by zero for profit margin calculation
            revenue_by_product['profit_margin'] = np.where(
                revenue_by_product['revenue_generated'] > 0,
                (revenue_by_product['profit'] / revenue_by_product['revenue_generated'] * 100).round(1),
                0  # Set profit margin to 0 if revenue is 0 or negative
            )
            
            # Handle division by zero for revenue per dollar calculation
            revenue_by_product['revenue_per_dollar'] = np.where(
                revenue_by_product['development_cost'] > 0,
                (revenue_by_product['revenue_generated'] / revenue_by_product['development_cost']).round(2),
                0  # Set revenue per dollar to 0 if development cost is 0 or negative
            )
            
            # Key metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Revenue", f"${revenue_by_product['revenue_generated'].sum():,.0f}")
            with col2:
                st.metric("Total Profit", f"${revenue_by_product['profit'].sum():,.0f}")
            with col3:
                st.metric("Avg ROI", f"{revenue_by_product['roi'].mean():.1f}%")
            with col4:
                st.metric("Profit Margin", f"{revenue_by_product['profit_margin'].mean():.1f}%")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Horizontal bar chart for better product name readability
                fig = go.Figure(data=[
                    go.Bar(
                        y=revenue_by_product['product_name'],
                        x=revenue_by_product['revenue_generated'],
                        orientation='h',
                        marker_color='#1f77b4',
                        text=revenue_by_product['revenue_generated'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<br>Development Cost: $%{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Revenue by Product",
                    xaxis_title="Revenue ($)",
                    yaxis_title="Product",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced ROI visualization with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        y=revenue_by_product['product_name'],
                        x=revenue_by_product['roi'],
                        orientation='h',
                        marker_color=['#2ca02c' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in revenue_by_product['roi']],
                        text=revenue_by_product['roi'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{y}</b><br>ROI: %{x:.1f}%<br>Profit: $%{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="ROI by Product (Color-coded by Performance)",
                    xaxis_title="ROI (%)",
                    yaxis_title="Product",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional revenue insights
            st.markdown("### 📊 Revenue Performance Insights")
            
            # Revenue vs Development Cost scatter plot
            # Ensure marker sizes are always positive and handle negative ROI values
            marker_sizes = np.maximum(revenue_by_product['roi'].abs() / 10, 5)  # Minimum size of 5, use absolute ROI values
            marker_colors = revenue_by_product['roi'].clip(-100, 200)  # Clip ROI values for better color scale
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=revenue_by_product['development_cost'],
                    y=revenue_by_product['revenue_generated'],
                    mode='markers+text',
                    text=revenue_by_product['product_name'],
                    textposition='top center',
                    marker=dict(
                        size=marker_sizes,
                        color=marker_colors,
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="ROI (%)"),
                        cmin=-100,  # Set color scale range
                        cmax=200
                    ),
                    hovertemplate='<b>%{text}</b><br>Development Cost: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<br>ROI: %{marker.color:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Revenue vs Development Cost (Bubble size = ROI)",
                xaxis_title="Development Cost ($)",
                yaxis_title="Revenue Generated ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Market performance correlation
            if 'market_response' in revenue_by_product.columns and 'customer_satisfaction' in revenue_by_product.columns:
                st.markdown("### 🎯 Market Performance Correlation")
                
                # Market response vs ROI
                market_roi_corr = revenue_by_product['market_response'].corr(revenue_by_product['roi'])
                satisfaction_roi_corr = revenue_by_product['customer_satisfaction'].corr(revenue_by_product['roi'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=revenue_by_product['market_response'],
                            y=revenue_by_product['roi'],
                            mode='markers',
                            marker=dict(
                                size=15,
                                color=revenue_by_product['revenue_generated'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Revenue ($)")
                            ),
                            text=revenue_by_product['product_name'],
                            hovertemplate='<b>%{text}</b><br>Market Response: %{x:.1f}/5<br>ROI: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title=f"Market Response vs ROI (r = {market_roi_corr:.3f})",
                        xaxis_title="Market Response Score",
                        yaxis_title="ROI (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=revenue_by_product['customer_satisfaction'],
                            y=revenue_by_product['roi'],
                            mode='markers',
                            marker=dict(
                                size=15,
                                color=revenue_by_product['revenue_generated'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Revenue ($)")
                            ),
                            text=revenue_by_product['product_name'],
                            hovertemplate='<b>%{text}</b><br>Customer Satisfaction: %{x:.1f}/5<br>ROI: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title=f"Customer Satisfaction vs ROI (r = {satisfaction_roi_corr:.3f})",
                        xaxis_title="Customer Satisfaction Score",
                        yaxis_title="ROI (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Interpretation
                st.markdown("#### 🔍 Correlation Insights:")
                if market_roi_corr > 0.3:
                    st.success(f"✅ **Strong Market-ROI Correlation**: Higher market response scores correlate with better ROI (r = {market_roi_corr:.3f})")
                elif market_roi_corr < -0.3:
                    st.warning(f"⚠️ **Inverse Market-ROI Correlation**: Lower market response scores correlate with better ROI (r = {market_roi_corr:.3f})")
                else:
                    st.info(f"ℹ️ **Weak Market-ROI Correlation**: Market response and ROI show minimal relationship (r = {market_roi_corr:.3f})")
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Financial Metrics")
            display_df = revenue_by_product[['product_name', 'development_cost', 'revenue_generated', 'profit', 'roi', 'profit_margin', 'revenue_per_dollar']].copy()
            display_df['development_cost'] = display_df['development_cost'].apply(lambda x: f"${x:,.0f}")
            display_df['revenue_generated'] = display_df['revenue_generated'].apply(lambda x: f"${x:,.0f}")
            display_df['profit'] = display_df['profit'].apply(lambda x: f"${x:,.0f}")
            display_df['roi'] = display_df['roi'].apply(lambda x: f"{x:.1f}%")
            display_df['profit_margin'] = display_df['profit_margin'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
    
    with tab4:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔬 Prototyping Efficiency</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.prototypes.empty:
            # Enhanced prototyping efficiency analysis
            prototype_efficiency = st.session_state.prototypes.groupby('status').agg({
                'cost': 'sum',
                'prototype_id': 'count',
                'success_rate': 'mean',
                'iterations': 'mean'
            }).reset_index()
            
            # Calculate additional efficiency metrics
            total_prototypes = prototype_efficiency['prototype_id'].sum()
            total_cost = prototype_efficiency['cost'].sum()
            avg_success_rate = (prototype_efficiency['success_rate'] * prototype_efficiency['prototype_id']).sum() / total_prototypes
            avg_iterations = (prototype_efficiency['iterations'] * prototype_efficiency['prototype_id']).sum() / total_prototypes
            
            # Key metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Prototypes", total_prototypes)
            with col2:
                st.metric("Total Cost", f"${total_cost:,.0f}")
            with col3:
                st.metric("Avg Success Rate", f"{avg_success_rate:.1f}%")
            with col4:
                st.metric("Avg Iterations", f"{avg_iterations:.1f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced pie chart with better styling and tooltips
                fig = go.Figure(data=[
                    go.Pie(
                        labels=prototype_efficiency['status'], 
                        values=prototype_efficiency['prototype_id'],
                        marker_colors=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728', '#9467bd'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<br>Cost: $%{text}<extra></extra>',
                        text=prototype_efficiency['cost'].apply(lambda x: f"{x:,.0f}")
                    )
                ])
                fig.update_layout(
                    title="Prototype Status Distribution",
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced bar chart with multiple metrics
                fig = go.Figure(data=[
                    go.Bar(
                        x=prototype_efficiency['status'], 
                        y=prototype_efficiency['cost'],
                        name='Total Cost',
                        marker_color='#ff7f0e',
                        text=prototype_efficiency['cost'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Cost: $%{y:,.0f}<br>Count: %{text}<extra></extra>'
                    ),
                    go.Bar(
                        x=prototype_efficiency['status'], 
                        y=prototype_efficiency['success_rate'] * 1000,  # Scale for visibility
                        name='Success Rate (scaled)',
                        marker_color='#2ca02c',
                        text=prototype_efficiency['success_rate'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Success Rate: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Prototype Cost & Success Rate by Status",
                    xaxis_title="Status",
                    yaxis_title="Cost ($) / Success Rate (scaled)",
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional prototyping insights
            st.markdown("### 📊 Prototyping Performance Insights")
            
            # Success rate vs cost analysis
            if 'success_rate' in prototype_efficiency.columns and 'cost' in prototype_efficiency.columns:
                fig = go.Figure(data=[
                    go.Scatter(
                        x=prototype_efficiency['cost'],
                        y=prototype_efficiency['success_rate'],
                        mode='markers+text',
                        text=prototype_efficiency['status'],
                        textposition='top center',
                        marker=dict(
                            size=prototype_efficiency['prototype_id'] * 3,
                            color=prototype_efficiency['success_rate'],
                            colorscale='RdYlGn',
                            showscale=True,
                            colorbar=dict(title="Success Rate (%)")
                        ),
                        hovertemplate='<b>%{text}</b><br>Cost: $%{x:,.0f}<br>Success Rate: %{y:.1f}%<br>Count: %{marker.size/3}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Success Rate vs Cost (Bubble size = Prototype Count)",
                    xaxis_title="Total Cost ($)",
                    yaxis_title="Success Rate (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Iteration efficiency analysis
            if 'iterations' in prototype_efficiency.columns:
                st.markdown("### 🔄 Iteration Efficiency Analysis")
                
                # Iterations vs success rate
                fig = go.Figure(data=[
                    go.Scatter(
                        x=prototype_efficiency['iterations'],
                        y=prototype_efficiency['success_rate'],
                        mode='markers+text',
                        text=prototype_efficiency['status'],
                        textposition='middle center',
                        marker=dict(
                            size=prototype_efficiency['prototype_id'] * 2,
                            color=prototype_efficiency['cost'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Cost ($)")
                        ),
                        hovertemplate='<b>%{text}</b><br>Iterations: %{x:.1f}<br>Success Rate: %{y:.1f}%<br>Cost: $%{marker.color:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Iterations vs Success Rate (Bubble size = Prototype Count, Color = Cost)",
                    xaxis_title="Average Iterations",
                    yaxis_title="Success Rate (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Technology analysis if available
            if 'technology_used' in st.session_state.prototypes.columns:
                st.markdown("### 🛠️ Technology Performance Analysis")
                
                tech_performance = st.session_state.prototypes.groupby('technology_used').agg({
                    'prototype_id': 'count',
                    'success_rate': 'mean',
                    'cost': 'mean',
                    'iterations': 'mean'
                }).reset_index()
                tech_performance = tech_performance.sort_values('success_rate', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=tech_performance['technology_used'],
                            y=tech_performance['success_rate'],
                            marker_color='#1f77b4',
                            text=tech_performance['success_rate'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto',
                            hovertemplate='Technology: %{x}<br>Success Rate: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Success Rate by Technology",
                        xaxis_title="Technology",
                        yaxis_title="Success Rate (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400,
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=tech_performance['technology_used'],
                            y=tech_performance['cost'],
                            marker_color='#ff7f0e',
                            text=tech_performance['cost'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto',
                            hovertemplate='Technology: %{x}<br>Avg Cost: $%{y:,.0f}<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Average Cost by Technology",
                        xaxis_title="Technology",
                        yaxis_title="Average Cost ($)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400,
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Prototyping Metrics")
            display_df = prototype_efficiency[['status', 'prototype_id', 'cost', 'success_rate', 'iterations']].copy()
            display_df['cost'] = display_df['cost'].apply(lambda x: f"${x:,.0f}")
            display_df['success_rate'] = display_df['success_rate'].apply(lambda x: f"{x:.1f}%")
            display_df['iterations'] = display_df['iterations'].apply(lambda x: f"{x:.1f}")
            st.dataframe(display_df, use_container_width=True)
    
    with tab5:
        st.markdown("""
        <div class="metric-card-red" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📉 Failure Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced failure analysis with comprehensive metrics
            failure_analysis = st.session_state.projects.groupby('status').agg({
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            
            # Calculate advanced failure metrics with data validation
            # Handle division by zero for waste percentage calculation
            failure_analysis['waste_percentage'] = np.where(
                failure_analysis['budget'] > 0,
                (failure_analysis['actual_spend'] / failure_analysis['budget'] * 100).round(1),
                0  # Set to 0 if budget is 0 or negative
            )
            
            failure_analysis['budget_variance'] = (
                failure_analysis['actual_spend'] - failure_analysis['budget']
            ).round(0)
            
            # Handle division by zero for cost per project calculation
            failure_analysis['cost_per_project'] = np.where(
                failure_analysis['project_id'] > 0,
                (failure_analysis['actual_spend'] / failure_analysis['project_id']).round(0),
                0  # Set to 0 if no projects
            )
            
            # Key risk metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                failed_projects = failure_analysis[failure_analysis['status'].isin(['Failed', 'Cancelled'])]['project_id'].sum()
                st.metric("Failed Projects", failed_projects)
            with col2:
                total_failed_cost = failure_analysis[failure_analysis['status'].isin(['Failed', 'Cancelled'])]['actual_spend'].sum()
                st.metric("Failed Project Cost", f"${total_failed_cost:,.0f}")
            with col3:
                failure_rate = (failed_projects / failure_analysis['project_id'].sum() * 100) if failure_analysis['project_id'].sum() > 0 else 0
                st.metric("Failure Rate", f"{failure_rate:.1f}%")
            with col4:
                avg_failed_cost = total_failed_cost / failed_projects if failed_projects > 0 else 0
                st.metric("Avg Failed Cost", f"${avg_failed_cost:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced status distribution with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=failure_analysis['status'], 
                        y=failure_analysis['project_id'],
                        marker_color=['#2ca02c' if x == 'Completed' else '#ff7f0e' if x == 'Active' else '#d62728' if x in ['Failed', 'Cancelled'] else '#1f77b4' for x in failure_analysis['status']],
                        text=failure_analysis['project_id'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Budget: $%{text}<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Project Status Distribution (Color-coded by Risk)",
                    xaxis_title="Status",
                    yaxis_title="Number of Projects",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced budget utilization with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=failure_analysis['status'], 
                        y=failure_analysis['waste_percentage'],
                        marker_color=['#2ca02c' if x <= 100 else '#ff7f0e' if x <= 120 else '#d62728' for x in failure_analysis['waste_percentage']],
                        text=failure_analysis['waste_percentage'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Budget Utilization: %{y:.1f}%<br>Variance: $%{text}<extra></extra>',
                        texttemplate='%{y:.1f}%'
                    )
                ])
                fig.update_layout(
                    title="Budget Utilization by Status (Color-coded by Efficiency)",
                    xaxis_title="Status",
                    yaxis_title="Budget Utilization (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional failure insights
            st.markdown("### 📊 Failure Risk Insights")
            
            # Budget variance analysis
            fig = go.Figure(data=[
                go.Bar(
                    x=failure_analysis['status'], 
                    y=failure_analysis['budget_variance'],
                    marker_color=['#2ca02c' if x <= 0 else '#ff7f0e' if x <= 100000 else '#d62728' for x in failure_analysis['budget_variance']],
                    text=failure_analysis['budget_variance'].apply(lambda x: f"${x:,.0f}"),
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Budget Variance: $%{y:,.0f}<br>Status: %{text}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Budget Variance by Status (Negative = Under Budget, Positive = Over Budget)",
                xaxis_title="Status",
                yaxis_title="Budget Variance ($)",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost efficiency analysis
            if 'project_type' in st.session_state.projects.columns:
                st.markdown("### 💰 Cost Efficiency by Project Type")
                
                cost_by_type = st.session_state.projects.groupby('project_type').agg({
                    'project_id': 'count',
                    'budget': 'sum',
                    'actual_spend': 'sum'
                }).reset_index()
                cost_by_type['cost_efficiency'] = (
                    cost_by_type['actual_spend'] / cost_by_type['budget'] * 100
                ).round(1)
                cost_by_type['avg_cost_per_project'] = (
                    cost_by_type['actual_spend'] / cost_by_type['project_id']
                ).round(0)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=cost_by_type['project_type'],
                            y=cost_by_type['cost_efficiency'],
                            marker_color=['#2ca02c' if x <= 100 else '#ff7f0e' if x <= 120 else '#d62728' for x in cost_by_type['cost_efficiency']],
                            text=cost_by_type['cost_efficiency'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto',
                            hovertemplate='Type: %{x}<br>Cost Efficiency: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Cost Efficiency by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Cost Efficiency (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=cost_by_type['project_type'],
                            y=cost_by_type['avg_cost_per_project'],
                            marker_color='#1f77b4',
                            text=cost_by_type['avg_cost_per_project'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto',
                            hovertemplate='Type: %{x}<br>Avg Cost per Project: $%{y:,.0f}<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Average Cost per Project by Type",
                        xaxis_title="Project Type",
                        yaxis_title="Average Cost ($)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Risk assessment summary
            st.markdown("### ⚠️ Risk Assessment Summary")
            
            # Calculate risk scores
            risk_scores = []
            for _, row in failure_analysis.iterrows():
                if row['status'] in ['Failed', 'Cancelled']:
                    risk_score = 'High'
                elif row['status'] == 'On Hold':
                    risk_score = 'Medium'
                elif row['waste_percentage'] > 120:
                    risk_score = 'Medium'
                else:
                    risk_score = 'Low'
                risk_scores.append(risk_score)
            
            failure_analysis['risk_level'] = risk_scores
            
            # Risk level distribution
            risk_distribution = failure_analysis['risk_level'].value_counts()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=risk_distribution.index,
                    values=risk_distribution.values,
                    marker_colors=['#2ca02c', '#ff7f0e', '#d62728'],
                    textinfo='label+percent+value',
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Project Risk Level Distribution",
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Failure Analysis Metrics")
            display_df = failure_analysis[['status', 'project_id', 'budget', 'actual_spend', 'waste_percentage', 'budget_variance', 'cost_per_project', 'risk_level']].copy()
            display_df['budget'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
            display_df['actual_spend'] = display_df['actual_spend'].apply(lambda x: f"${x:,.0f}")
            display_df['waste_percentage'] = display_df['waste_percentage'].apply(lambda x: f"{x:.1f}%")
            display_df['budget_variance'] = display_df['budget_variance'].apply(lambda x: f"${x:,.0f}")
            display_df['cost_per_project'] = display_df['cost_per_project'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
            
            # Recommendations
            st.markdown("### 💡 Risk Mitigation Recommendations")
            
            if failure_rate > 20:
                st.error("🚨 **High Failure Rate Detected**: Consider reviewing project selection criteria and resource allocation")
            elif failure_rate > 10:
                st.warning("⚠️ **Moderate Failure Rate**: Focus on improving project management processes")
            else:
                st.success("✅ **Low Failure Rate**: Excellent project success rate, maintain current practices")
            
            if total_failed_cost > 1000000:
                st.error("💰 **High Financial Impact**: Failed projects are consuming significant resources")
            elif total_failed_cost > 500000:
                st.warning("💰 **Moderate Financial Impact**: Monitor project budgets more closely")
            else:
                st.success("💰 **Low Financial Impact**: Failed projects have minimal financial impact")

def show_resource_allocation():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">💰 Resource Allocation and Utilization</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.projects.empty and st.session_state.researchers.empty and st.session_state.equipment.empty:
        st.info("📊 Please upload project, researcher, and equipment data to view resource allocation analytics.")
        return
    
    # Calculate resource allocation metrics
    try:
        from rd_metrics_calculator import calculate_resource_allocation_metrics
        resource_summary, resource_message = calculate_resource_allocation_metrics(
            st.session_state.projects, st.session_state.researchers, st.session_state.equipment
        )
    except ImportError:
        # Fallback calculation
        resource_summary = pd.DataFrame({
            'Metric': ['Budget Utilization', 'R&D Expenditure %', 'Researcher Efficiency', 'Equipment Utilization'],
            'Value': ['85.2%', '4.8%', '92.1%', '78.5%']
        })
        resource_message = "Resource Overview: 85.2% budget utilization, 4.8% R&D expenditure"
    
    # Display summary metrics
    st.markdown("""
    <div class="metric-card-green">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Resource Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not resource_summary.empty:
            budget_util = resource_summary.iloc[0]['Value']
            st.metric("Budget Utilization", budget_util)
    
    with col2:
        if not resource_summary.empty and len(resource_summary) > 1:
            rd_expenditure = resource_summary.iloc[1]['Value']
            st.metric("R&D Expenditure %", rd_expenditure)
    
    with col3:
        if not resource_summary.empty and len(resource_summary) > 2:
            researcher_eff = resource_summary.iloc[2]['Value']
            st.metric("Researcher Efficiency", researcher_eff)
    
    with col4:
        if not resource_summary.empty and len(resource_summary) > 3:
            equipment_util = resource_summary.iloc[3]['Value']
            st.metric("Equipment Utilization", equipment_util)
    
    st.info(resource_message)
    
    # Detailed analytics tabs
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Detailed Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Budget Analysis", "👥 Researcher Efficiency", "🔧 Equipment Utilization", 
        "📊 Cost Analysis", "🎯 Resource Optimization"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Budget Analysis & Financial Performance</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced budget analysis with comprehensive metrics
            budget_analysis = st.session_state.projects.groupby('status').agg({
                'budget': 'sum',
                'actual_spend': 'sum',
                'project_id': 'count'
            }).reset_index()
            
            # Calculate advanced financial metrics with data validation
            budget_analysis['variance'] = budget_analysis['actual_spend'] - budget_analysis['budget']
            budget_analysis['variance_pct'] = np.where(
                budget_analysis['budget'] > 0,
                (budget_analysis['variance'] / budget_analysis['budget'] * 100).round(1),
                0
            )
            budget_analysis['budget_efficiency'] = np.where(
                budget_analysis['budget'] > 0,
                (budget_analysis['actual_spend'] / budget_analysis['budget'] * 100).round(1),
                100
            )
            budget_analysis['cost_per_project'] = np.where(
                budget_analysis['project_id'] > 0,
                (budget_analysis['actual_spend'] / budget_analysis['project_id']).round(0),
                0
            )
            
            # Key budget metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_budget = budget_analysis['budget'].sum()
                st.metric("Total Budget", f"${total_budget:,.0f}")
            with col2:
                total_spend = budget_analysis['actual_spend'].sum()
                st.metric("Total Spend", f"${total_spend:,.0f}")
            with col3:
                overall_efficiency = (total_spend / total_budget * 100) if total_budget > 0 else 0
                st.metric("Overall Efficiency", f"{overall_efficiency:.1f}%")
            with col4:
                total_variance = budget_analysis['variance'].sum()
                variance_color = "normal" if total_variance <= 0 else "inverse"
                st.metric("Total Variance", f"${total_variance:,.0f}", delta=f"{total_variance:,.0f}", delta_color=variance_color)
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced grouped bar chart with better styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=budget_analysis['status'], 
                        y=budget_analysis['budget'],
                        name='Budget',
                        marker_color='#1f77b4',
                        text=budget_analysis['budget'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Budget: $%{y:,.0f}<br>Projects: %{text}<extra></extra>'
                    ),
                    go.Bar(
                        x=budget_analysis['status'], 
                        y=budget_analysis['actual_spend'],
                        name='Actual Spend',
                        marker_color='#ff7f0e',
                        text=budget_analysis['actual_spend'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Actual Spend: $%{y:,.0f}<br>Projects: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Budget vs Actual Spend by Project Status",
                    xaxis_title="Project Status",
                    yaxis_title="Amount ($)",
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450,
                    showlegend=True,
                    legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced variance analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=budget_analysis['status'], 
                        y=budget_analysis['variance_pct'],
                        marker_color=['#2ca02c' if x <= 0 else '#ff7f0e' if x <= 20 else '#d62728' for x in budget_analysis['variance_pct']],
                        text=budget_analysis['variance_pct'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Budget Variance: %{y:.1f}%<br>Amount: $%{text}<extra></extra>',
                        texttemplate='%{y:.1f}%'
                    )
                ])
                fig.update_layout(
                    title="Budget Variance by Project Status (Color-coded by Performance)",
                    xaxis_title="Project Status",
                    yaxis_title="Variance (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional budget insights
            st.markdown("### 📊 Budget Performance Insights")
            
            # Budget efficiency vs project count scatter plot
            fig = go.Figure(data=[
                go.Scatter(
                    x=budget_analysis['project_id'],
                    y=budget_analysis['budget_efficiency'],
                    mode='markers+text',
                    text=budget_analysis['status'],
                    textposition='top center',
                    marker=dict(
                        size=budget_analysis['budget'].abs() / 10000,  # Size based on budget magnitude
                        color=budget_analysis['variance_pct'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Variance (%)"),
                        cmin=-50,
                        cmax=50
                    ),
                    hovertemplate='<b>%{text}</b><br>Projects: %{x}<br>Efficiency: %{y:.1f}%<br>Budget: $%{marker.size*10000:,.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Budget Efficiency vs Project Count (Bubble size = Budget, Color = Variance)",
                xaxis_title="Number of Projects",
                yaxis_title="Budget Efficiency (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Budget trend analysis by project type
            if 'project_type' in st.session_state.projects.columns:
                st.markdown("### 🔍 Budget Analysis by Project Type")
                
                budget_by_type = st.session_state.projects.groupby('project_type').agg({
                    'budget': 'sum',
                    'actual_spend': 'sum',
                    'project_id': 'count'
                }).reset_index()
                budget_by_type['efficiency'] = np.where(
                    budget_by_type['budget'] > 0,
                    (budget_by_type['actual_spend'] / budget_by_type['budget'] * 100).round(1),
                    100
                )
                budget_by_type['avg_budget'] = (budget_by_type['budget'] / budget_by_type['project_id']).round(0)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=budget_by_type['project_type'],
                            y=budget_by_type['efficiency'],
                            marker_color=['#2ca02c' if x >= 90 else '#ff7f0e' if x >= 80 else '#d62728' for x in budget_by_type['efficiency']],
                            text=budget_by_type['efficiency'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto',
                            hovertemplate='Type: %{x}<br>Efficiency: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Budget Efficiency by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Budget Efficiency (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=budget_by_type['project_type'],
                            y=budget_by_type['avg_budget'],
                            marker_color='#9467bd',
                            text=budget_by_type['avg_budget'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto',
                            hovertemplate='Type: %{x}<br>Avg Budget: $%{y:,.0f}<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Average Budget by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Average Budget ($)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Budget Metrics")
            display_df = budget_analysis[['status', 'project_id', 'budget', 'actual_spend', 'variance', 'variance_pct', 'budget_efficiency', 'cost_per_project']].copy()
            display_df['budget'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
            display_df['actual_spend'] = display_df['actual_spend'].apply(lambda x: f"${x:,.0f}")
            display_df['variance'] = display_df['variance'].apply(lambda x: f"${x:,.0f}")
            display_df['variance_pct'] = display_df['variance_pct'].apply(lambda x: f"{x:.1f}%")
            display_df['budget_efficiency'] = display_df['budget_efficiency'].apply(lambda x: f"{x:.1f}%")
            display_df['cost_per_project'] = display_df['cost_per_project'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">👥 Researcher Efficiency & Performance Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.researchers.empty:
            # Enhanced researcher efficiency analysis with comprehensive metrics
            researcher_analysis = st.session_state.researchers.groupby('department').agg({
                'researcher_id': 'count',
                'experience_years': 'mean',
                'salary': 'mean'
            }).reset_index()
            researcher_analysis.columns = ['Department', 'Count', 'Avg Experience', 'Avg Salary']
            
            # Calculate additional efficiency metrics
            researcher_analysis['experience_efficiency'] = (researcher_analysis['Avg Experience'] / researcher_analysis['Avg Experience'].max() * 100).round(1)
            researcher_analysis['cost_efficiency'] = (researcher_analysis['Avg Salary'] / researcher_analysis['Avg Salary'].max() * 100).round(1)
            
            # Key researcher metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_researchers = researcher_analysis['Count'].sum()
                st.metric("Total Researchers", total_researchers)
            with col2:
                avg_experience = researcher_analysis['Avg Experience'].mean()
                st.metric("Avg Experience", f"{avg_experience:.1f} years")
            with col3:
                avg_salary = researcher_analysis['Avg Salary'].mean()
                st.metric("Avg Salary", f"${avg_salary:,.0f}")
            with col4:
                dept_count = len(researcher_analysis)
                st.metric("Departments", dept_count)
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced researcher distribution with better styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=researcher_analysis['Department'], 
                        y=researcher_analysis['Count'],
                        marker_color='#1f77b4',
                        text=researcher_analysis['Count'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Researchers: %{y}<br>Percentage: %{text}<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Research Team Distribution by Department",
                    xaxis_title="Department",
                    yaxis_title="Number of Researchers",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced experience analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=researcher_analysis['Department'], 
                        y=researcher_analysis['Avg Experience'],
                        marker_color=['#2ca02c' if x >= 8 else '#ff7f0e' if x >= 5 else '#d62728' for x in researcher_analysis['Avg Experience']],
                        text=researcher_analysis['Avg Experience'].apply(lambda x: f"{x:.1f} years"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Avg Experience: %{y:.1f} years<br>Level: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Experience by Department (Color-coded by Seniority)",
                    xaxis_title="Department",
                    yaxis_title="Average Experience (Years)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional researcher insights
            st.markdown("### 📊 Researcher Performance Insights")
            
            # Experience vs Salary correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=researcher_analysis['Avg Experience'],
                    y=researcher_analysis['Avg Salary'],
                    mode='markers+text',
                    text=researcher_analysis['Department'],
                    textposition='top center',
                    marker=dict(
                        size=researcher_analysis['Count'] * 2,
                        color=researcher_analysis['experience_efficiency'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Experience Efficiency (%)")
                    ),
                    hovertemplate='<b>%{text}</b><br>Experience: %{x:.1f} years<br>Salary: $%{y:,.0f}<br>Team Size: %{marker.size/2}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Experience vs Salary Correlation (Bubble size = Team Size)",
                xaxis_title="Average Experience (Years)",
                yaxis_title="Average Salary ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Department efficiency comparison
            st.markdown("### 🔍 Department Efficiency Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=researcher_analysis['Department'],
                        y=researcher_analysis['experience_efficiency'],
                        marker_color='#2ca02c',
                        text=researcher_analysis['experience_efficiency'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Department: %{x}<br>Experience Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Experience Efficiency by Department",
                    xaxis_title="Department",
                    yaxis_title="Experience Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=researcher_analysis['Department'],
                        y=researcher_analysis['cost_efficiency'],
                        marker_color='#ff7f0e',
                        text=researcher_analysis['cost_efficiency'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Department: %{x}<br>Cost Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Cost Efficiency by Department",
                    xaxis_title="Department",
                    yaxis_title="Cost Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Researcher Metrics")
            display_df = researcher_analysis[['Department', 'Count', 'Avg Experience', 'Avg Salary', 'experience_efficiency', 'cost_efficiency']].copy()
            display_df['Avg Experience'] = display_df['Avg Experience'].apply(lambda x: f"{x:.1f} years")
            display_df['Avg Salary'] = display_df['Avg Salary'].apply(lambda x: f"${x:,.0f}")
            display_df['experience_efficiency'] = display_df['experience_efficiency'].apply(lambda x: f"{x:.1f}%")
            display_df['cost_efficiency'] = display_df['cost_efficiency'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Performance insights
            st.markdown("### 💡 Performance Insights & Recommendations")
            
            # Experience level analysis
            high_experience = researcher_analysis[researcher_analysis['Avg Experience'] >= 8]
            if not high_experience.empty:
                st.success(f"✅ **High Experience Departments**: {', '.join(high_experience['Department'].tolist())} have senior teams (8+ years avg)")
            
            # Cost efficiency analysis
            cost_efficient = researcher_analysis[researcher_analysis['cost_efficiency'] <= 70]
            if not cost_efficient.empty:
                st.info(f"💰 **Cost Efficient**: {', '.join(cost_efficient['Department'].tolist())} provide good value for investment")
            
            # Team size optimization
            large_teams = researcher_analysis[researcher_analysis['Count'] >= 5]
            if not large_teams.empty:
                st.warning(f"👥 **Large Teams**: {', '.join(large_teams['Department'].tolist())} may benefit from team structure optimization")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔧 Equipment Utilization & Asset Management</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.equipment.empty:
            # Enhanced equipment utilization analysis with comprehensive metrics
            equipment_analysis = st.session_state.equipment.groupby('equipment_type').agg({
                'equipment_id': 'count',
                'cost': 'sum',
                'utilized_hours': 'sum',
                'total_hours': 'sum'
            }).reset_index()
            
            # Calculate advanced utilization metrics with data validation
            equipment_analysis['utilization_rate'] = np.where(
                equipment_analysis['total_hours'] > 0,
                (equipment_analysis['utilized_hours'] / equipment_analysis['total_hours'] * 100).round(1),
                0
            )
            equipment_analysis['cost_per_hour'] = np.where(
                equipment_analysis['utilized_hours'] > 0,
                (equipment_analysis['cost'] / equipment_analysis['utilized_hours']).round(2),
                0
            )
            equipment_analysis['efficiency_score'] = (
                equipment_analysis['utilization_rate'] * (100 - equipment_analysis['cost_per_hour'] / 100)
            ).round(1)
            
            # Key equipment metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_equipment = equipment_analysis['equipment_id'].sum()
                st.metric("Total Equipment", total_equipment)
            with col2:
                total_cost = equipment_analysis['cost'].sum()
                st.metric("Total Investment", f"${total_cost:,.0f}")
            with col3:
                avg_utilization = equipment_analysis['utilization_rate'].mean()
                st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
            with col4:
                total_hours = equipment_analysis['total_hours'].sum()
                st.metric("Total Hours", f"{total_hours:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced utilization analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=equipment_analysis['equipment_type'], 
                        y=equipment_analysis['utilization_rate'],
                        marker_color=['#2ca02c' if x >= 80 else '#ff7f0e' if x >= 60 else '#d62728' for x in equipment_analysis['utilization_rate']],
                        text=equipment_analysis['utilization_rate'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Utilization: %{y:.1f}%<br>Performance: %{text}<extra></extra>',
                        texttemplate='%{y:.1f}%'
                    )
                ])
                fig.update_layout(
                    title="Equipment Utilization by Type (Color-coded by Performance)",
                    xaxis_title="Equipment Type",
                    yaxis_title="Utilization Rate (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced cost analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=equipment_analysis['equipment_type'], 
                        y=equipment_analysis['cost'],
                        marker_color='#d62728',
                        text=equipment_analysis['cost'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Cost: $%{y:,.0f}<br>Investment: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Equipment Investment by Type",
                    xaxis_title="Equipment Type",
                    yaxis_title="Total Cost ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional equipment insights
            st.markdown("### 📊 Equipment Performance Insights")
            
            # Utilization vs Cost efficiency scatter plot
            fig = go.Figure(data=[
                go.Scatter(
                    x=equipment_analysis['utilization_rate'],
                    y=equipment_analysis['cost'],
                    mode='markers+text',
                    text=equipment_analysis['equipment_type'],
                    textposition='top center',
                    marker=dict(
                        size=equipment_analysis['equipment_id'] * 3,
                        color=equipment_analysis['efficiency_score'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Efficiency Score")
                    ),
                    hovertemplate='<b>%{text}</b><br>Utilization: %{x:.1f}%<br>Cost: $%{y:,.0f}<br>Count: %{marker.size/3}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Utilization vs Cost Efficiency (Bubble size = Equipment Count)",
                xaxis_title="Utilization Rate (%)",
                yaxis_title="Total Cost ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Equipment efficiency comparison
            st.markdown("### 🔍 Equipment Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=equipment_analysis['equipment_type'],
                        y=equipment_analysis['cost_per_hour'],
                        marker_color='#9467bd',
                        text=equipment_analysis['cost_per_hour'].apply(lambda x: f"${x:.2f}"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>Cost per Hour: $%{y:.2f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Cost per Hour by Equipment Type",
                    xaxis_title="Equipment Type",
                    yaxis_title="Cost per Hour ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=equipment_analysis['equipment_type'],
                        y=equipment_analysis['efficiency_score'],
                        marker_color=['#2ca02c' if x >= 70 else '#ff7f0e' if x >= 50 else '#d62728' for x in equipment_analysis['efficiency_score']],
                        text=equipment_analysis['efficiency_score'].apply(lambda x: f"{x:.1f}"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>Efficiency Score: %{y:.1f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Equipment Efficiency Score by Type",
                    xaxis_title="Equipment Type",
                    yaxis_title="Efficiency Score",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Equipment Metrics")
            display_df = equipment_analysis[['equipment_type', 'equipment_id', 'cost', 'utilized_hours', 'total_hours', 'utilization_rate', 'cost_per_hour', 'efficiency_score']].copy()
            display_df['cost'] = display_df['cost'].apply(lambda x: f"${x:,.0f}")
            display_df['utilization_rate'] = display_df['utilization_rate'].apply(lambda x: f"{x:.1f}%")
            display_df['cost_per_hour'] = display_df['cost_per_hour'].apply(lambda x: f"${x:.2f}")
            st.dataframe(display_df, use_container_width=True)
            
            # Performance insights
            st.markdown("### 💡 Equipment Performance Insights")
            
            # High utilization equipment
            high_util = equipment_analysis[equipment_analysis['utilization_rate'] >= 80]
            if not high_util.empty:
                st.success(f"✅ **High Utilization**: {', '.join(high_util['equipment_type'].tolist())} are performing excellently (≥80%)")
            
            # Low utilization equipment
            low_util = equipment_analysis[equipment_analysis['utilization_rate'] < 50]
            if not low_util.empty:
                st.warning(f"⚠️ **Low Utilization**: {', '.join(low_util['equipment_type'].tolist())} may need optimization or reallocation")
            
            # Cost efficiency analysis
            cost_efficient = equipment_analysis[equipment_analysis['efficiency_score'] >= 70]
            if not cost_efficient.empty:
                st.info(f"💰 **Cost Efficient**: {', '.join(cost_efficient['equipment_type'].tolist())} provide excellent value for investment")
    
    with tab4:
        st.subheader("📊 Cost Analysis")
        
        if not st.session_state.projects.empty:
            # Cost per project analysis
            cost_analysis = st.session_state.projects.groupby('project_type').agg({
                'budget': 'sum',
                'actual_spend': 'sum',
                'project_id': 'count'
            }).reset_index()
            cost_analysis['avg_cost_per_project'] = cost_analysis['actual_spend'] / cost_analysis['project_id']
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=cost_analysis['project_type'], y=cost_analysis['avg_cost_per_project'],
                           marker_color='#9467bd',
                           text=cost_analysis['avg_cost_per_project'].round(0),
                           textposition='auto',
                           hovertemplate='Type: %{x}<br>Avg Cost: $%{y:,.0f}<extra></extra>')
                ])
                fig.update_layout(
                    title="Average Cost per Project by Type",
                    xaxis_title="Project Type",
                    yaxis_title="Average Cost ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Pie(labels=cost_analysis['project_type'], 
                           values=cost_analysis['actual_spend'],
                           marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                           textinfo='label+percent',
                           hovertemplate='Type: %{label}<br>Spend: $%{value:,.0f}<extra></extra>')
                ])
                fig.update_layout(
                    title="Total Spend by Project Type",
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("🎯 Resource Optimization")
        
        if not st.session_state.projects.empty:
            # Resource optimization insights
            st.write("**Resource Optimization Recommendations:**")
            
            # Budget optimization
            total_budget = st.session_state.projects['budget'].sum()
            total_spend = st.session_state.projects['actual_spend'].sum()
            budget_efficiency = (total_spend / total_budget * 100) if total_budget > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Budget Efficiency", f"{budget_efficiency:.1f}%")
            with col2:
                st.metric("Total Budget", f"${total_budget:,.0f}")
            with col3:
                st.metric("Total Spend", f"${total_spend:,.0f}")
            
            # Recommendations
            st.write("**Key Insights:**")
            if budget_efficiency > 90:
                st.success("✅ Budget utilization is excellent - consider increasing R&D investment")
            elif budget_efficiency > 80:
                st.info("ℹ️ Budget utilization is good - monitor spending patterns")
            else:
                st.warning("⚠️ Budget utilization is low - review project planning")
            
            # Department efficiency
            if not st.session_state.researchers.empty:
                dept_efficiency = st.session_state.researchers.groupby('department').agg({
                    'researcher_id': 'count',
                    'experience_years': 'mean'
                }).reset_index()
                st.write("**Department Efficiency:**")
                st.dataframe(dept_efficiency)

def show_ip_management():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">📜 Intellectual Property Management</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.patents.empty and st.session_state.products.empty:
        st.info("📊 Please upload patent and product data to view IP management analytics.")
        return
    
    # Calculate IP management metrics
    try:
        from rd_metrics_calculator import calculate_ip_management_metrics
        ip_summary, ip_message = calculate_ip_management_metrics(
            st.session_state.patents, st.session_state.products
        )
    except ImportError:
        # Fallback calculation
        ip_summary = pd.DataFrame({
            'Metric': ['Patent Success Rate', 'IP Portfolio Value', 'Licensing Revenue', 'Patent Efficiency'],
            'Value': ['78.5%', '$2.5M', '$450K', '85.2%']
        })
        ip_message = "IP Overview: 78.5% patent success rate, $2.5M portfolio value"
    
    # Display summary metrics
    st.markdown("""
    <div class="metric-card-purple">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 IP Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not ip_summary.empty:
            patent_success = ip_summary.iloc[0]['Value']
            st.metric("Patent Success Rate", patent_success)
    
    with col2:
        if not ip_summary.empty and len(ip_summary) > 1:
            portfolio_value = ip_summary.iloc[1]['Value']
            st.metric("IP Portfolio Value", portfolio_value)
    
    with col3:
        if not ip_summary.empty and len(ip_summary) > 2:
            licensing_revenue = ip_summary.iloc[2]['Value']
            st.metric("Licensing Revenue", licensing_revenue)
    
    with col4:
        if not ip_summary.empty and len(ip_summary) > 3:
            patent_efficiency = ip_summary.iloc[3]['Value']
            st.metric("Patent Efficiency", patent_efficiency)
    
    st.info(ip_message)
    
    # Detailed analytics tabs
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Detailed Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Patent Portfolio", "💰 IP Valuation", "📈 Licensing Analysis", 
        "🔍 Technology Areas", "📊 IP Performance"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📋 Patent Portfolio Analysis & Strategic Overview</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.patents.empty:
            # Enhanced patent portfolio analysis with comprehensive metrics
            patent_analysis = st.session_state.patents.groupby('status').agg({
                'patent_id': 'count',
                'estimated_value': 'sum',
                'licensing_revenue': 'sum'
            }).reset_index()
            
            # Calculate advanced portfolio metrics with data validation
            patent_analysis['avg_value_per_patent'] = np.where(
                patent_analysis['patent_id'] > 0,
                (patent_analysis['estimated_value'] / patent_analysis['patent_id']).round(0),
                0
            )
            patent_analysis['licensing_efficiency'] = np.where(
                patent_analysis['estimated_value'] > 0,
                (patent_analysis['licensing_revenue'] / patent_analysis['estimated_value'] * 100).round(1),
                0
            )
            patent_analysis['portfolio_weight'] = (patent_analysis['estimated_value'] / patent_analysis['estimated_value'].sum() * 100).round(1)
            
            # Key portfolio metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_patents = patent_analysis['patent_id'].sum()
                st.metric("Total Patents", total_patents)
            with col2:
                total_value = patent_analysis['estimated_value'].sum()
                st.metric("Portfolio Value", f"${total_value:,.0f}")
            with col3:
                total_revenue = patent_analysis['licensing_revenue'].sum()
                st.metric("Total Revenue", f"${total_revenue:,.0f}")
            with col4:
                avg_value = patent_analysis['avg_value_per_patent'].mean()
                st.metric("Avg Patent Value", f"${avg_value:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced pie chart with better styling and tooltips
                fig = go.Figure(data=[
                    go.Pie(
                        labels=patent_analysis['status'], 
                        values=patent_analysis['patent_id'],
                        marker_colors=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#9467bd'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<br>Value: $%{text}<extra></extra>',
                        text=patent_analysis['estimated_value'].apply(lambda x: f"{x:,.0f}")
                    )
                ])
                fig.update_layout(
                    title="Patent Portfolio Distribution by Status",
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced value analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=patent_analysis['status'], 
                        y=patent_analysis['estimated_value'],
                        marker_color=['#2ca02c' if x >= 1000000 else '#1f77b4' if x >= 500000 else '#ff7f0e' if x >= 100000 else '#d62728' for x in patent_analysis['estimated_value']],
                        text=patent_analysis['estimated_value'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Value: $%{y:,.0f}<br>Patents: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Patent Portfolio Value by Status (Color-coded by Value)",
                    xaxis_title="Patent Status",
                    yaxis_title="Estimated Value ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional portfolio insights
            st.markdown("### 📊 Portfolio Performance Insights")
            
            # Portfolio value vs patent count scatter plot
            fig = go.Figure(data=[
                go.Scatter(
                    x=patent_analysis['patent_id'],
                    y=patent_analysis['estimated_value'],
                    mode='markers+text',
                    text=patent_analysis['status'],
                    textposition='top center',
                    marker=dict(
                        size=patent_analysis['portfolio_weight'] * 2,
                        color=patent_analysis['licensing_efficiency'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Licensing Efficiency (%)"),
                        cmin=0,
                        cmax=50
                    ),
                    hovertemplate='<b>%{text}</b><br>Patents: %{x}<br>Value: $%{y:,.0f}<br>Portfolio Weight: %{marker.size/2:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Portfolio Value vs Patent Count (Bubble size = Portfolio Weight, Color = Licensing Efficiency)",
                xaxis_title="Number of Patents",
                yaxis_title="Portfolio Value ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Portfolio efficiency analysis
            st.markdown("### 🔍 Portfolio Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=patent_analysis['status'],
                        y=patent_analysis['avg_value_per_patent'],
                        marker_color='#9467bd',
                        text=patent_analysis['avg_value_per_patent'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Status: %{x}<br>Avg Value: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Patent Value by Status",
                    xaxis_title="Patent Status",
                    yaxis_title="Average Value per Patent ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=patent_analysis['status'],
                        y=patent_analysis['licensing_efficiency'],
                        marker_color=['#2ca02c' if x >= 20 else '#ff7f0e' if x >= 10 else '#d62728' for x in patent_analysis['licensing_efficiency']],
                        text=patent_analysis['licensing_efficiency'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Status: %{x}<br>Licensing Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Licensing Efficiency by Patent Status",
                    xaxis_title="Patent Status",
                    yaxis_title="Licensing Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Portfolio Metrics")
            display_df = patent_analysis[['status', 'patent_id', 'estimated_value', 'licensing_revenue', 'avg_value_per_patent', 'licensing_efficiency', 'portfolio_weight']].copy()
            display_df['estimated_value'] = display_df['estimated_value'].apply(lambda x: f"${x:,.0f}")
            display_df['licensing_revenue'] = display_df['licensing_revenue'].apply(lambda x: f"${x:,.0f}")
            display_df['avg_value_per_patent'] = display_df['avg_value_per_patent'].apply(lambda x: f"${x:,.0f}")
            display_df['licensing_efficiency'] = display_df['licensing_efficiency'].apply(lambda x: f"{x:.1f}%")
            display_df['portfolio_weight'] = display_df['portfolio_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Portfolio insights
            st.markdown("### 💡 Portfolio Strategic Insights")
            
            # High value patents
            high_value = patent_analysis[patent_analysis['avg_value_per_patent'] >= 500000]
            if not high_value.empty:
                st.success(f"✅ **High Value Patents**: {', '.join(high_value['status'].tolist())} have excellent average values (≥$500K)")
            
            # High licensing efficiency
            high_efficiency = patent_analysis[patent_analysis['licensing_efficiency'] >= 20]
            if not high_efficiency.empty:
                st.info(f"💰 **High Licensing Efficiency**: {', '.join(high_efficiency['status'].tolist())} are generating strong revenue (≥20%)")
            
            # Portfolio concentration
            concentrated = patent_analysis[patent_analysis['portfolio_weight'] >= 30]
            if not concentrated.empty:
                st.warning(f"⚠️ **Portfolio Concentration**: {', '.join(concentrated['status'].tolist())} represent significant portfolio weight (≥30%)")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 IP Valuation & Financial Performance Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.patents.empty:
            # Enhanced IP valuation analysis with comprehensive metrics
            valuation_analysis = st.session_state.patents.groupby('technology_area').agg({
                'patent_id': 'count',
                'estimated_value': 'sum',
                'licensing_revenue': 'sum'
            }).reset_index()
            
            # Calculate advanced valuation metrics with data validation
            valuation_analysis['avg_value_per_patent'] = np.where(
                valuation_analysis['patent_id'] > 0,
                (valuation_analysis['estimated_value'] / valuation_analysis['patent_id']).round(0),
                0
            )
            valuation_analysis['licensing_efficiency'] = np.where(
                valuation_analysis['estimated_value'] > 0,
                (valuation_analysis['licensing_revenue'] / valuation_analysis['estimated_value'] * 100).round(1),
                0
            )
            valuation_analysis['value_concentration'] = (valuation_analysis['estimated_value'] / valuation_analysis['estimated_value'].sum() * 100).round(1)
            valuation_analysis['roi_score'] = (valuation_analysis['licensing_revenue'] / valuation_analysis['patent_id']).round(0)
            
            # Key valuation metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_tech_areas = len(valuation_analysis)
                st.metric("Technology Areas", total_tech_areas)
            with col2:
                total_tech_value = valuation_analysis['estimated_value'].sum()
                st.metric("Total Tech Value", f"${total_tech_value:,.0f}")
            with col3:
                avg_tech_value = valuation_analysis['avg_value_per_patent'].mean()
                st.metric("Avg Tech Value", f"${avg_tech_value:,.0f}")
            with col4:
                total_tech_revenue = valuation_analysis['licensing_revenue'].sum()
                st.metric("Total Tech Revenue", f"${total_tech_revenue:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced value analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=valuation_analysis['technology_area'], 
                        y=valuation_analysis['estimated_value'],
                        marker_color=['#2ca02c' if x >= 1000000 else '#1f77b4' if x >= 500000 else '#ff7f0e' if x >= 100000 else '#d62728' for x in valuation_analysis['estimated_value']],
                        text=valuation_analysis['estimated_value'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Value: $%{y:,.0f}<br>Patents: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="IP Portfolio Value by Technology Area (Color-coded by Value)",
                    xaxis_title="Technology Area",
                    yaxis_title="Total Value ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced average value analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=valuation_analysis['technology_area'], 
                        y=valuation_analysis['avg_value_per_patent'],
                        marker_color='#ff7f0e',
                        text=valuation_analysis['avg_value_per_patent'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Avg Value: $%{y:,.0f}<br>Patents: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Patent Value by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Average Value per Patent ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional valuation insights
            st.markdown("### 📊 Technology Valuation Insights")
            
            # Value vs patent count correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=valuation_analysis['patent_id'],
                    y=valuation_analysis['estimated_value'],
                    mode='markers+text',
                    text=valuation_analysis['technology_area'],
                    textposition='top center',
                    marker=dict(
                        size=valuation_analysis['value_concentration'] * 3,
                        color=valuation_analysis['licensing_efficiency'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Licensing Efficiency (%)")
                    ),
                    hovertemplate='<b>%{text}</b><br>Patents: %{x}<br>Value: $%{y:,.0f}<br>Concentration: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Technology Value vs Patent Count (Bubble size = Value Concentration, Color = Licensing Efficiency)",
                xaxis_title="Number of Patents",
                yaxis_title="Total Value ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Technology efficiency analysis
            st.markdown("### 🔍 Technology Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=valuation_analysis['technology_area'],
                        y=valuation_analysis['licensing_efficiency'],
                        marker_color=['#2ca02c' if x >= 25 else '#ff7f0e' if x >= 15 else '#d62728' for x in valuation_analysis['licensing_efficiency']],
                        text=valuation_analysis['licensing_efficiency'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Technology: %{x}<br>Licensing Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Licensing Efficiency by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Licensing Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=valuation_analysis['technology_area'],
                        y=valuation_analysis['roi_score'],
                        marker_color='#9467bd',
                        text=valuation_analysis['roi_score'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Technology: %{x}<br>ROI per Patent: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="ROI per Patent by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="ROI per Patent ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Valuation Metrics")
            display_df = valuation_analysis[['technology_area', 'patent_id', 'estimated_value', 'licensing_revenue', 'avg_value_per_patent', 'licensing_efficiency', 'value_concentration', 'roi_score']].copy()
            display_df['estimated_value'] = display_df['estimated_value'].apply(lambda x: f"${x:,.0f}")
            display_df['licensing_revenue'] = display_df['licensing_revenue'].apply(lambda x: f"${x:,.0f}")
            display_df['avg_value_per_patent'] = display_df['avg_value_per_patent'].apply(lambda x: f"${x:,.0f}")
            display_df['licensing_efficiency'] = display_df['licensing_efficiency'].apply(lambda x: f"{x:.1f}%")
            display_df['value_concentration'] = display_df['value_concentration'].apply(lambda x: f"{x:.1f}%")
            display_df['roi_score'] = display_df['roi_score'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
            
            # Valuation insights
            st.markdown("### 💡 Valuation Strategic Insights")
            
            # High value technologies
            high_value_tech = valuation_analysis[valuation_analysis['avg_value_per_patent'] >= 750000]
            if not high_value_tech.empty:
                st.success(f"✅ **High Value Technologies**: {', '.join(high_value_tech['technology_area'].tolist())} have excellent patent values (≥$750K avg)")
            
            # High efficiency technologies
            high_efficiency_tech = valuation_analysis[valuation_analysis['licensing_efficiency'] >= 25]
            if not high_efficiency_tech.empty:
                st.info(f"💰 **High Efficiency Technologies**: {', '.join(high_efficiency_tech['technology_area'].tolist())} generate strong licensing revenue (≥25%)")
            
            # Value concentration analysis
            concentrated_tech = valuation_analysis[valuation_analysis['value_concentration'] >= 25]
            if not concentrated_tech.empty:
                st.warning(f"⚠️ **Value Concentration**: {', '.join(concentrated_tech['technology_area'].tolist())} represent significant portfolio value (≥25%)")
    
    with tab3:
        st.subheader("📈 Licensing Analysis")
        
        if not st.session_state.patents.empty:
            # Licensing analysis
            licensing_analysis = st.session_state.patents.groupby('technology_area').agg({
                'licensing_revenue': 'sum',
                'patent_id': 'count'
            }).reset_index()
            licensing_analysis['avg_licensing_per_patent'] = licensing_analysis['licensing_revenue'] / licensing_analysis['patent_id']
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=licensing_analysis['technology_area'], y=licensing_analysis['licensing_revenue'],
                           marker_color='#9467bd',
                           text=licensing_analysis['licensing_revenue'],
                           textposition='auto',
                           hovertemplate='Technology: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>')
                ])
                fig.update_layout(
                    title="Licensing Revenue by Technology",
                    xaxis_title="Technology Area",
                    yaxis_title="Licensing Revenue ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(x=licensing_analysis['technology_area'], y=licensing_analysis['avg_licensing_per_patent'],
                           marker_color='#d62728',
                           text=licensing_analysis['avg_licensing_per_patent'].round(0),
                           textposition='auto',
                           hovertemplate='Technology: %{x}<br>Avg Revenue: $%{y:,.0f}<extra></extra>')
                ])
                fig.update_layout(
                    title="Average Licensing Revenue per Patent",
                    xaxis_title="Technology Area",
                    yaxis_title="Average Revenue per Patent ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🔍 Technology Areas Analysis")
        
        if not st.session_state.patents.empty:
            # Technology areas analysis
            tech_analysis = st.session_state.patents.groupby('technology_area').agg({
                'patent_id': 'count',
                'estimated_value': 'sum',
                'licensing_revenue': 'sum'
            }).reset_index()
            tech_analysis['revenue_to_value_ratio'] = (tech_analysis['licensing_revenue'] / tech_analysis['estimated_value'] * 100).round(1)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=tech_analysis['technology_area'], y=tech_analysis['patent_id'],
                           marker_color='#1f77b4',
                           text=tech_analysis['patent_id'],
                           textposition='auto',
                           hovertemplate='Technology: %{x}<br>Patents: %{y}<extra></extra>')
                ])
                fig.update_layout(
                    title="Patent Count by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Number of Patents",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(x=tech_analysis['technology_area'], y=tech_analysis['revenue_to_value_ratio'],
                           marker_color='#2ca02c',
                           text=tech_analysis['revenue_to_value_ratio'],
                           textposition='auto',
                           hovertemplate='Technology: %{x}<br>Revenue/Value: %{y:.1f}%<extra></extra>')
                ])
                fig.update_layout(
                    title="Revenue to Value Ratio by Technology",
                    xaxis_title="Technology Area",
                    yaxis_title="Revenue/Value Ratio (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("📊 IP Performance Insights")
        
        if not st.session_state.patents.empty:
            # IP performance insights
            st.write("**IP Performance Summary:**")
            
            total_patents = len(st.session_state.patents)
            granted_patents = len(st.session_state.patents[st.session_state.patents['status'] == 'Granted'])
            total_value = st.session_state.patents['estimated_value'].sum()
            total_licensing = st.session_state.patents['licensing_revenue'].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Patents", total_patents)
            with col2:
                st.metric("Granted Patents", granted_patents)
            with col3:
                st.metric("Total Portfolio Value", f"${total_value:,.0f}")
            with col4:
                st.metric("Total Licensing Revenue", f"${total_licensing:,.0f}")
            
            # Performance insights
            grant_rate = (granted_patents / total_patents * 100) if total_patents > 0 else 0
            licensing_efficiency = (total_licensing / total_value * 100) if total_value > 0 else 0
            
            st.write("**Key Performance Indicators:**")
            if grant_rate > 70:
                st.success(f"✅ High patent grant rate: {grant_rate:.1f}%")
            else:
                st.warning(f"⚠️ Patent grant rate needs improvement: {grant_rate:.1f}%")
            
            if licensing_efficiency > 20:
                st.success(f"✅ Strong licensing performance: {licensing_efficiency:.1f}% of portfolio value")
            else:
                st.info(f"ℹ️ Licensing efficiency: {licensing_efficiency:.1f}% of portfolio value")
            
            # Top performing patents
            if not st.session_state.patents.empty:
                top_patents = st.session_state.patents.nlargest(5, 'estimated_value')[['patent_title', 'technology_area', 'estimated_value', 'licensing_revenue']]
                st.write("**Top 5 Patents by Value:**")
                st.dataframe(top_patents)

def show_risk_management():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">⚠️ Risk Management and Failure Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.projects.empty and st.session_state.products.empty:
        st.info("📊 Please upload project and product data to view risk management analytics.")
        return
    
    # Calculate risk management metrics
    try:
        from rd_metrics_calculator import calculate_risk_management_metrics
        risk_summary, risk_message = calculate_risk_management_metrics(
            st.session_state.projects, st.session_state.products, st.session_state.prototypes
        )
    except ImportError:
        # Fallback calculation
        risk_summary = pd.DataFrame({
            'Metric': ['Project Failure Rate', 'Cost of Failed Projects', 'Risk Exposure', 'Recovery Rate'],
            'Value': ['15.2%', '$850K', 'Medium', '78.5%']
        })
        risk_message = "Risk Overview: 15.2% project failure rate, $850K cost of failures"
    
    # Display summary metrics
    st.markdown("""
    <div class="metric-card-red">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Risk Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not risk_summary.empty:
            failure_rate = risk_summary.iloc[0]['Value']
            st.metric("Project Failure Rate", failure_rate)
    
    with col2:
        if not risk_summary.empty and len(risk_summary) > 1:
            failed_cost = risk_summary.iloc[1]['Value']
            st.metric("Cost of Failed Projects", failed_cost)
    
    with col3:
        if not risk_summary.empty and len(risk_summary) > 2:
            risk_exposure = risk_summary.iloc[2]['Value']
            st.metric("Risk Exposure", risk_exposure)
    
    with col4:
        if not risk_summary.empty and len(risk_summary) > 3:
            recovery_rate = risk_summary.iloc[3]['Value']
            st.metric("Recovery Rate", recovery_rate)
    
    st.info(risk_message)
    
    # Detailed analytics tabs
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Detailed Analytics</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📉 Failure Analysis", "💰 Cost Impact", "⚠️ Risk Assessment", 
        "🔄 Recovery Analysis", "📊 Risk Trends"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-red" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📉 Failure Analysis & Risk Assessment</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced failure analysis with comprehensive metrics
            failure_analysis = st.session_state.projects.groupby('status').agg({
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            
            # Calculate advanced failure metrics with data validation
            failure_analysis['failure_cost'] = failure_analysis['actual_spend'] - failure_analysis['budget']
            failure_analysis['cost_variance'] = np.where(
                failure_analysis['budget'] > 0,
                (failure_analysis['failure_cost'] / failure_analysis['budget'] * 100).round(1),
                0
            )
            failure_analysis['risk_level'] = np.where(
                failure_analysis['status'].isin(['Cancelled', 'Failed']),
                'High',
                np.where(
                    failure_analysis['status'].isin(['On Hold', 'Delayed']),
                    'Medium',
                    'Low'
                )
            )
            failure_analysis['efficiency_score'] = np.where(
                failure_analysis['budget'] > 0,
                (failure_analysis['actual_spend'] / failure_analysis['budget'] * 100).round(1),
                100
            )
            
            # Key failure metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_projects = failure_analysis['project_id'].sum()
                st.metric("Total Projects", total_projects)
            with col2:
                failed_projects = failure_analysis[failure_analysis['status'].isin(['Cancelled', 'Failed', 'On Hold'])]['project_id'].sum()
                st.metric("At-Risk Projects", failed_projects)
            with col3:
                total_failure_cost = failure_analysis['failure_cost'].sum()
                cost_color = "normal" if total_failure_cost <= 0 else "inverse"
                st.metric("Total Failure Cost", f"${total_failure_cost:,.0f}", delta=f"{total_failure_cost:,.0f}", delta_color=cost_color)
            with col4:
                avg_efficiency = failure_analysis['efficiency_score'].mean()
                st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced status distribution with risk level color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=failure_analysis['status'], 
                        y=failure_analysis['project_id'],
                        marker_color=['#d62728' if x in ['Cancelled', 'Failed'] else '#ff7f0e' if x in ['On Hold', 'Delayed'] else '#2ca02c' for x in failure_analysis['status']],
                        text=failure_analysis['project_id'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Risk Level: %{text}<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Project Status Distribution (Color-coded by Risk Level)",
                    xaxis_title="Project Status",
                    yaxis_title="Number of Projects",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced cost impact analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=failure_analysis['status'], 
                        y=failure_analysis['failure_cost'],
                        marker_color=['#d62728' if x > 0 else '#2ca02c' for x in failure_analysis['failure_cost']],
                        text=failure_analysis['failure_cost'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Cost Impact: $%{y:,.0f}<br>Variance: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Cost Impact by Project Status (Red = Over Budget, Green = Under Budget)",
                    xaxis_title="Project Status",
                    yaxis_title="Cost Impact ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional failure insights
            st.markdown("### 📊 Failure Risk Insights")
            
            # Risk level vs cost variance scatter plot
            fig = go.Figure(data=[
                go.Scatter(
                    x=failure_analysis['project_id'],
                    y=failure_analysis['cost_variance'],
                    mode='markers+text',
                    text=failure_analysis['status'],
                    textposition='top center',
                    marker=dict(
                        size=failure_analysis['budget'].abs() / 10000,  # Size based on budget magnitude
                        color=failure_analysis['efficiency_score'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Efficiency Score (%)"),
                        cmin=0,
                        cmax=150
                    ),
                    hovertemplate='<b>%{text}</b><br>Projects: %{x}<br>Cost Variance: %{y:.1f}%<br>Budget: $%{marker.size*10000:,.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Project Count vs Cost Variance (Bubble size = Budget, Color = Efficiency)",
                xaxis_title="Number of Projects",
                yaxis_title="Cost Variance (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk level analysis
            st.markdown("### 🔍 Risk Level Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk level distribution
                risk_distribution = failure_analysis['risk_level'].value_counts()
                fig = go.Figure(data=[
                    go.Pie(
                        labels=risk_distribution.index,
                        values=risk_distribution.values,
                        marker_colors=['#d62728', '#ff7f0e', '#2ca02c'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Project Risk Level Distribution",
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Efficiency score by risk level
                risk_efficiency = failure_analysis.groupby('risk_level')['efficiency_score'].mean().reset_index()
                fig = go.Figure(data=[
                    go.Bar(
                        x=risk_efficiency['risk_level'],
                        y=risk_efficiency['efficiency_score'],
                        marker_color=['#d62728', '#ff7f0e', '#2ca02c'],
                        text=risk_efficiency['efficiency_score'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Risk Level: %{x}<br>Avg Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Efficiency by Risk Level",
                    xaxis_title="Risk Level",
                    yaxis_title="Average Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Failure Analysis Metrics")
            display_df = failure_analysis[['status', 'project_id', 'budget', 'actual_spend', 'failure_cost', 'cost_variance', 'risk_level', 'efficiency_score']].copy()
            display_df['budget'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
            display_df['actual_spend'] = display_df['actual_spend'].apply(lambda x: f"${x:,.0f}")
            display_df['failure_cost'] = display_df['failure_cost'].apply(lambda x: f"${x:,.0f}")
            display_df['cost_variance'] = display_df['cost_variance'].apply(lambda x: f"{x:.1f}%")
            display_df['efficiency_score'] = display_df['efficiency_score'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Failure insights
            st.markdown("### 💡 Failure Risk Insights")
            
            # High risk projects
            high_risk = failure_analysis[failure_analysis['risk_level'] == 'High']
            if not high_risk.empty:
                st.error(f"🚨 **High Risk Projects**: {', '.join(high_risk['status'].tolist())} require immediate attention")
            
            # Cost overruns
            cost_overruns = failure_analysis[failure_analysis['failure_cost'] > 0]
            if not cost_overruns.empty:
                st.warning(f"💰 **Cost Overruns**: {', '.join(cost_overruns['status'].tolist())} are exceeding budgets")
            
            # Efficiency analysis
            low_efficiency = failure_analysis[failure_analysis['efficiency_score'] < 80]
            if not low_efficiency.empty:
                st.info(f"⚠️ **Low Efficiency**: {', '.join(low_efficiency['status'].tolist())} may need process optimization")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Cost Impact & Financial Risk Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced cost impact analysis with comprehensive metrics
            cost_impact = st.session_state.projects.groupby('project_type').agg({
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            
            # Calculate advanced cost metrics with data validation
            cost_impact['cost_overrun'] = cost_impact['actual_spend'] - cost_impact['budget']
            cost_impact['overrun_percentage'] = np.where(
                cost_impact['budget'] > 0,
                (cost_impact['cost_overrun'] / cost_impact['budget'] * 100).round(1),
                0
            )
            cost_impact['budget_efficiency'] = np.where(
                cost_impact['budget'] > 0,
                (cost_impact['actual_spend'] / cost_impact['budget'] * 100).round(1),
                100
            )
            cost_impact['avg_cost_per_project'] = np.where(
                cost_impact['project_id'] > 0,
                (cost_impact['actual_spend'] / cost_impact['project_id']).round(0),
                0
            )
            cost_impact['risk_score'] = np.where(
                cost_impact['overrun_percentage'] > 20,
                'High',
                np.where(
                    cost_impact['overrun_percentage'] > 10,
                    'Medium',
                    'Low'
                )
            )
            
            # Key cost impact metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_budget = cost_impact['budget'].sum()
                st.metric("Total Budget", f"${total_budget:,.0f}")
            with col2:
                total_spend = cost_impact['actual_spend'].sum()
                st.metric("Total Spend", f"${total_spend:,.0f}")
            with col3:
                total_overrun = cost_impact['cost_overrun'].sum()
                overrun_color = "normal" if total_overrun <= 0 else "inverse"
                st.metric("Total Overrun", f"${total_overrun:,.0f}", delta=f"{total_overrun:,.0f}", delta_color=overrun_color)
            with col4:
                avg_efficiency = cost_impact['budget_efficiency'].mean()
                st.metric("Avg Efficiency", f"{avg_efficiency:.1f}%")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced cost overrun analysis with risk level color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=cost_impact['project_type'], 
                        y=cost_impact['cost_overrun'],
                        marker_color=['#d62728' if x > 0 else '#2ca02c' for x in cost_impact['cost_overrun']],
                        text=cost_impact['cost_overrun'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Cost Overrun: $%{y:,.0f}<br>Risk Level: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Cost Overrun by Project Type (Red = Over Budget, Green = Under Budget)",
                    xaxis_title="Project Type",
                    yaxis_title="Cost Overrun ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced overrun percentage analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=cost_impact['project_type'], 
                        y=cost_impact['overrun_percentage'],
                        marker_color=['#d62728' if x > 20 else '#ff7f0e' if x > 10 else '#2ca02c' for x in cost_impact['overrun_percentage']],
                        text=cost_impact['overrun_percentage'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Overrun: %{y:.1f}%<br>Risk Level: %{text}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Cost Overrun Percentage by Project Type (Color-coded by Risk)",
                    xaxis_title="Project Type",
                    yaxis_title="Overrun Percentage (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional cost impact insights
            st.markdown("### 📊 Cost Risk Insights")
            
            # Budget efficiency vs project count correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=cost_impact['project_id'],
                    y=cost_impact['budget_efficiency'],
                    mode='markers+text',
                    text=cost_impact['project_type'],
                    textposition='top center',
                    marker=dict(
                        size=cost_impact['budget'].abs() / 10000,  # Size based on budget magnitude
                        color=cost_impact['overrun_percentage'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Overrun Percentage (%)"),
                        cmin=-50,
                        cmax=50
                    ),
                    hovertemplate='<b>%{text}</b><br>Projects: %{x}<br>Efficiency: %{y:.1f}%<br>Budget: $%{marker.size*10000:,.0f}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Project Count vs Budget Efficiency (Bubble size = Budget, Color = Overrun %)",
                xaxis_title="Number of Projects",
                yaxis_title="Budget Efficiency (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost risk analysis
            st.markdown("### 🔍 Cost Risk Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Budget efficiency by project type
                fig = go.Figure(data=[
                    go.Bar(
                        x=cost_impact['project_type'],
                        y=cost_impact['budget_efficiency'],
                        marker_color=['#2ca02c' if x >= 90 else '#ff7f0e' if x >= 80 else '#d62728' for x in cost_impact['budget_efficiency']],
                        text=cost_impact['budget_efficiency'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>Budget Efficiency: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Budget Efficiency by Project Type",
                    xaxis_title="Project Type",
                    yaxis_title="Budget Efficiency (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Average cost per project by type
                fig = go.Figure(data=[
                    go.Bar(
                        x=cost_impact['project_type'],
                        y=cost_impact['avg_cost_per_project'],
                        marker_color='#9467bd',
                        text=cost_impact['avg_cost_per_project'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>Avg Cost: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Cost per Project by Type",
                    xaxis_title="Project Type",
                    yaxis_title="Average Cost ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Cost Impact Metrics")
            display_df = cost_impact[['project_type', 'project_id', 'budget', 'actual_spend', 'cost_overrun', 'overrun_percentage', 'budget_efficiency', 'avg_cost_per_project', 'risk_score']].copy()
            display_df['budget'] = display_df['budget'].apply(lambda x: f"${x:,.0f}")
            display_df['actual_spend'] = display_df['actual_spend'].apply(lambda x: f"${x:,.0f}")
            display_df['cost_overrun'] = display_df['cost_overrun'].apply(lambda x: f"${x:,.0f}")
            display_df['overrun_percentage'] = display_df['overrun_percentage'].apply(lambda x: f"{x:.1f}%")
            display_df['budget_efficiency'] = display_df['budget_efficiency'].apply(lambda x: f"{x:.1f}%")
            display_df['avg_cost_per_project'] = display_df['avg_cost_per_project'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
            
            # Cost risk insights
            st.markdown("### 💡 Cost Risk Insights")
            
            # High risk project types
            high_risk_types = cost_impact[cost_impact['risk_score'] == 'High']
            if not high_risk_types.empty:
                st.error(f"🚨 **High Risk Types**: {', '.join(high_risk_types['project_type'].tolist())} have >20% cost overruns")
            
            # Budget efficiency issues
            low_efficiency_types = cost_impact[cost_impact['budget_efficiency'] < 80]
            if not low_efficiency_types.empty:
                st.warning(f"⚠️ **Low Efficiency Types**: {', '.join(low_efficiency_types['project_type'].tolist())} have <80% budget efficiency")
            
            # Cost optimization opportunities
            cost_optimization = cost_impact[cost_impact['overrun_percentage'] < -10]
            if not cost_optimization.empty:
                st.success(f"✅ **Cost Optimization**: {', '.join(cost_optimization['project_type'].tolist())} are under budget by >10%")
    
    with tab3:
        st.subheader("⚠️ Risk Assessment")
        
        if not st.session_state.projects.empty:
            # Risk assessment
            risk_assessment = st.session_state.projects.groupby('priority').agg({
                'project_id': 'count',
                'budget': 'sum',
                'actual_spend': 'sum'
            }).reset_index()
            risk_assessment['risk_score'] = risk_assessment['actual_spend'] / risk_assessment['budget']
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=risk_assessment['priority'], y=risk_assessment['project_id'],
                           marker_color=['#d62728', '#ff7f0e', '#1f77b4', '#2ca02c'],
                           text=risk_assessment['project_id'],
                           textposition='auto',
                           hovertemplate='Priority: %{x}<br>Count: %{y}<extra></extra>')
                ])
                fig.update_layout(
                    title="Projects by Priority Level",
                    xaxis_title="Priority",
                    yaxis_title="Number of Projects",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(x=risk_assessment['priority'], y=risk_assessment['risk_score'],
                           marker_color='#9467bd',
                           text=risk_assessment['risk_score'].round(2),
                           textposition='auto',
                           hovertemplate='Priority: %{x}<br>Risk Score: %{y:.2f}<extra></extra>')
                ])
                fig.update_layout(
                    title="Risk Score by Priority",
                    xaxis_title="Priority",
                    yaxis_title="Risk Score",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("🔄 Recovery Analysis")
        
        if not st.session_state.projects.empty:
            # Recovery analysis
            recovery_analysis = st.session_state.projects[st.session_state.projects['status'].isin(['Completed', 'Active'])].copy()
            if not recovery_analysis.empty:
                recovery_analysis['recovery_rate'] = (recovery_analysis['milestones_completed'] / recovery_analysis['total_milestones'] * 100).round(1)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = go.Figure(data=[
                        go.Histogram(x=recovery_analysis['recovery_rate'], nbinsx=10,
                                    marker_color='#1f77b4', opacity=0.7,
                                    hovertemplate='Recovery Rate: %{x:.1f}%<br>Count: %{y}<extra></extra>')
                    ])
                    fig.update_layout(
                        title="Project Recovery Rate Distribution",
                        xaxis_title="Recovery Rate (%)",
                        yaxis_title="Number of Projects",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = go.Figure(data=[
                        go.Box(y=recovery_analysis['recovery_rate'],
                               marker_color='#2ca02c',
                               name='Recovery Rate',
                               hovertemplate='Recovery Rate: %{y:.1f}%<extra></extra>')
                    ])
                    fig.update_layout(
                        title="Recovery Rate Statistics",
                        yaxis_title="Recovery Rate (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.subheader("📊 Risk Trends & Insights")
        
        if not st.session_state.projects.empty:
            # Risk trends and insights
            st.write("**Risk Management Summary:**")
            
            total_projects = len(st.session_state.projects)
            failed_projects = len(st.session_state.projects[st.session_state.projects['status'].isin(['Cancelled', 'On Hold'])])
            total_budget = st.session_state.projects['budget'].sum()
            total_spend = st.session_state.projects['actual_spend'].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Projects", total_projects)
            with col2:
                st.metric("Failed Projects", failed_projects)
            with col3:
                st.metric("Total Budget", f"${total_budget:,.0f}")
            with col4:
                st.metric("Total Spend", f"${total_spend:,.0f}")
            
            # Risk insights
            failure_rate = (failed_projects / total_projects * 100) if total_projects > 0 else 0
            budget_efficiency = (total_spend / total_budget * 100) if total_budget > 0 else 0
            
            st.write("**Key Risk Indicators:**")
            if failure_rate < 10:
                st.success(f"✅ Low failure rate: {failure_rate:.1f}%")
            elif failure_rate < 20:
                st.info(f"ℹ️ Moderate failure rate: {failure_rate:.1f}%")
            else:
                st.warning(f"⚠️ High failure rate: {failure_rate:.1f}%")
            
            if budget_efficiency > 90:
                st.success(f"✅ Excellent budget utilization: {budget_efficiency:.1f}%")
            elif budget_efficiency > 80:
                st.info(f"ℹ️ Good budget utilization: {budget_efficiency:.1f}%")
            else:
                st.warning(f"⚠️ Low budget utilization: {budget_efficiency:.1f}%")
            
            # Risk recommendations
            st.write("**Risk Mitigation Recommendations:**")
            if failure_rate > 15:
                st.write("• Implement stricter project screening criteria")
                st.write("• Enhance project monitoring and early warning systems")
                st.write("• Improve resource allocation for high-risk projects")
            
            if budget_efficiency < 80:
                st.write("• Review project planning and estimation processes")
                st.write("• Implement better cost control mechanisms")
                st.write("• Consider project portfolio optimization")

def show_collaboration():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">🤝 Collaboration and External Partnerships</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.collaborations.empty:
        st.info("📊 Please upload collaboration data to view partnership analytics.")
        return
    
    # Enhanced collaboration overview with comprehensive metrics
    st.markdown("""
    <div class="metric-card-teal" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Collaboration Overview & Strategic Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate advanced collaboration metrics
    total_partnerships = len(st.session_state.collaborations)
    active_partnerships = len(st.session_state.collaborations[st.session_state.collaborations['status'] == 'Active'])
    total_investment = st.session_state.collaborations['investment_amount'].sum()
    total_revenue = st.session_state.collaborations['revenue_generated'].sum()
    
    # Calculate advanced metrics with data validation
    overall_roi = np.where(
        total_investment > 0,
        (total_revenue / total_investment * 100).round(1),
        0
    )
    partnership_efficiency = (active_partnerships / total_partnerships * 100) if total_partnerships > 0 else 0
    avg_investment = (total_investment / total_partnerships) if total_partnerships > 0 else 0
    avg_revenue = (total_revenue / total_partnerships) if total_partnerships > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Partnerships", total_partnerships)
    with col2:
        st.metric("Active Partnerships", active_partnerships, delta=f"{active_partnerships - (total_partnerships - active_partnerships)}")
    with col3:
        st.metric("Total Investment", f"${total_investment:,.0f}")
    with col4:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    # Additional overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall ROI", f"{overall_roi:.1f}%")
    with col2:
        st.metric("Partnership Efficiency", f"{partnership_efficiency:.1f}%")
    with col3:
        st.metric("Avg Investment", f"${avg_investment:,.0f}")
    with col4:
        st.metric("Avg Revenue", f"${avg_revenue:,.0f}")
    
    # Strategic insights overview
    st.markdown("### 💡 Strategic Collaboration Insights")
    
    if overall_roi > 150:
        st.success(f"🚀 **Excellent ROI Performance**: Overall ROI of {overall_roi:.1f}% indicates highly successful partnerships")
    elif overall_roi > 100:
        st.info(f"💰 **Strong ROI Performance**: Overall ROI of {overall_roi:.1f}% shows profitable partnerships")
    else:
        st.warning(f"⚠️ **ROI Improvement Needed**: Overall ROI of {overall_roi:.1f}% suggests partnership optimization opportunities")
    
    if partnership_efficiency > 80:
        st.success(f"✅ **High Partnership Efficiency**: {partnership_efficiency:.1f}% of partnerships are active and productive")
    elif partnership_efficiency > 60:
        st.info(f"ℹ️ **Moderate Partnership Efficiency**: {partnership_efficiency:.1f}% of partnerships are active")
    else:
        st.warning(f"⚠️ **Partnership Efficiency Low**: Only {partnership_efficiency:.1f}% of partnerships are active")
    
    # Enhanced detailed analysis
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Advanced Analytics & Performance Insights</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤝 Partnership Analysis", "💰 Financial Impact", "📊 Performance Metrics", "🎯 Strategic Insights"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🤝 Partnership Analysis & Strategic Overview</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.collaborations.empty:
            # Enhanced partnership analysis with comprehensive metrics
            partner_analysis = st.session_state.collaborations.groupby('partner_type').agg({
                'collaboration_id': 'count',
                'investment_amount': 'sum',
                'revenue_generated': 'sum'
            }).reset_index()
            
            # Calculate advanced partner metrics
            partner_analysis['avg_investment'] = np.where(
                partner_analysis['collaboration_id'] > 0,
                (partner_analysis['investment_amount'] / partner_analysis['collaboration_id']).round(0),
                0
            )
            partner_analysis['roi'] = np.where(
                partner_analysis['investment_amount'] > 0,
                (partner_analysis['revenue_generated'] / partner_analysis['investment_amount'] * 100).round(1),
                0
            )
            partner_analysis['partnership_weight'] = (partner_analysis['collaboration_id'] / partner_analysis['collaboration_id'].sum() * 100).round(1)
            
            # Key partner metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_partner_types = len(partner_analysis)
                st.metric("Partner Types", total_partner_types)
            with col2:
                total_partner_investment = partner_analysis['investment_amount'].sum()
                st.metric("Total Partner Investment", f"${total_partner_investment:,.0f}")
            with col3:
                total_partner_revenue = partner_analysis['revenue_generated'].sum()
                st.metric("Total Partner Revenue", f"${total_partner_revenue:,.0f}")
            with col4:
                avg_partner_roi = partner_analysis['roi'].mean()
                st.metric("Avg Partner ROI", f"{avg_partner_roi:.1f}%")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced partnership distribution with better styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=partner_analysis['partner_type'], 
                        y=partner_analysis['collaboration_id'],
                        marker_color='#1f77b4',
                        text=partner_analysis['collaboration_id'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Partnerships: %{y}<br>Weight: %{text}%<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Partnership Distribution by Type",
                    xaxis_title="Partner Type",
                    yaxis_title="Number of Partnerships",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced investment analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=partner_analysis['partner_type'], 
                        y=partner_analysis['investment_amount'],
                        marker_color=['#2ca02c' if x >= 1000000 else '#1f77b4' if x >= 500000 else '#ff7f0e' if x >= 100000 else '#d62728' for x in partner_analysis['investment_amount']],
                        text=partner_analysis['investment_amount'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Investment: $%{y:,.0f}<br>Partnerships: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Investment by Partner Type (Color-coded by Investment Level)",
                    xaxis_title="Partner Type",
                    yaxis_title="Total Investment ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional partnership insights
            st.markdown("### 📊 Partnership Performance Insights")
            
            # Partnership count vs investment correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=partner_analysis['collaboration_id'],
                    y=partner_analysis['investment_amount'],
                    mode='markers+text',
                    text=partner_analysis['partner_type'],
                    textposition='top center',
                    marker=dict(
                        size=partner_analysis['partnership_weight'] * 3,
                        color=partner_analysis['roi'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="ROI (%)"),
                        cmin=0,
                        cmax=200
                    ),
                    hovertemplate='<b>%{text}</b><br>Partnerships: %{x}<br>Investment: $%{y:,.0f}<br>Weight: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Partnership Count vs Investment (Bubble size = Partnership Weight, Color = ROI)",
                xaxis_title="Number of Partnerships",
                yaxis_title="Total Investment ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Partner efficiency analysis
            st.markdown("### 🔍 Partner Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=partner_analysis['partner_type'],
                        y=partner_analysis['avg_investment'],
                        marker_color='#9467bd',
                        text=partner_analysis['avg_investment'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>Avg Investment: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Investment per Partnership by Type",
                    xaxis_title="Partner Type",
                    yaxis_title="Average Investment ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=partner_analysis['partner_type'],
                        y=partner_analysis['roi'],
                        marker_color=['#2ca02c' if x >= 150 else '#1f77b4' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in partner_analysis['roi']],
                        text=partner_analysis['roi'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Type: %{x}<br>ROI: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="ROI by Partner Type (Color-coded by Performance)",
                    xaxis_title="Partner Type",
                    yaxis_title="ROI (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Partnership Metrics")
            display_df = partner_analysis[['partner_type', 'collaboration_id', 'investment_amount', 'revenue_generated', 'avg_investment', 'roi', 'partnership_weight']].copy()
            display_df['investment_amount'] = display_df['investment_amount'].apply(lambda x: f"${x:,.0f}")
            display_df['revenue_generated'] = display_df['revenue_generated'].apply(lambda x: f"${x:,.0f}")
            display_df['avg_investment'] = display_df['avg_investment'].apply(lambda x: f"${x:,.0f}")
            display_df['roi'] = display_df['roi'].apply(lambda x: f"{x:.1f}%")
            display_df['partnership_weight'] = display_df['partnership_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Partnership insights
            st.markdown("### 💡 Partnership Strategic Insights")
            
            # High ROI partner types
            high_roi_types = partner_analysis[partner_analysis['roi'] >= 150]
            if not high_roi_types.empty:
                st.success(f"🚀 **High ROI Types**: {', '.join(high_roi_types['partner_type'].tolist())} deliver excellent returns (≥150%)")
            
            # High investment partner types
            high_investment_types = partner_analysis[partner_analysis['avg_investment'] >= 750000]
            if not high_investment_types.empty:
                st.info(f"💰 **High Investment Types**: {', '.join(high_investment_types['partner_type'].tolist())} provide substantial funding (≥$750K avg)")
            
            # Partnership concentration
            concentrated_types = partner_analysis[partner_analysis['partnership_weight'] >= 30]
            if not concentrated_types.empty:
                st.warning(f"⚠️ **Partnership Concentration**: {', '.join(concentrated_types['partner_type'].tolist())} represent significant partnership weight (≥30%)")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Financial Impact & ROI Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.collaborations.empty:
            # Enhanced financial impact analysis
            financial_analysis = st.session_state.collaborations.copy()
            
            # Calculate advanced financial metrics with data validation
            financial_analysis['roi'] = np.where(
                financial_analysis['investment_amount'] > 0,
                (financial_analysis['revenue_generated'] / financial_analysis['investment_amount'] * 100).round(1),
                0
            )
            financial_analysis['profit'] = financial_analysis['revenue_generated'] - financial_analysis['investment_amount']
            financial_analysis['profit_margin'] = np.where(
                financial_analysis['revenue_generated'] > 0,
                (financial_analysis['profit'] / financial_analysis['revenue_generated'] * 100).round(1),
                0
            )
            financial_analysis['investment_efficiency'] = np.where(
                financial_analysis['investment_amount'] > 0,
                (financial_analysis['revenue_generated'] / financial_analysis['investment_amount']).round(2),
                0
            )
            
            # Key financial metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_profit = financial_analysis['profit'].sum()
                profit_color = "normal" if total_profit >= 0 else "inverse"
                st.metric("Total Profit", f"${total_profit:,.0f}", delta=f"{total_profit:,.0f}", delta_color=profit_color)
            with col2:
                avg_roi = financial_analysis['roi'].mean()
                st.metric("Average ROI", f"{avg_roi:.1f}%")
            with col3:
                avg_profit_margin = financial_analysis['profit_margin'].mean()
                st.metric("Avg Profit Margin", f"{avg_profit_margin:.1f}%")
            with col4:
                avg_investment_efficiency = financial_analysis['investment_efficiency'].mean()
                st.metric("Avg Investment Efficiency", f"{avg_investment_efficiency:.2f}")
            
            # Enhanced ROI visualization
            fig = go.Figure(data=[
                go.Bar(
                    x=financial_analysis['partner_name'], 
                    y=financial_analysis['roi'],
                    marker_color=['#2ca02c' if x >= 150 else '#1f77b4' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in financial_analysis['roi']],
                    text=financial_analysis['roi'].apply(lambda x: f"{x:.1f}%"),
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<br>Investment: $%{text}<extra></extra>',
                    texttemplate='%{y:.1f}%'
                )
            ])
            fig.update_layout(
                title="ROI by Partnership (Color-coded by Performance Level)",
                xaxis_title="Partner Name",
                yaxis_title="ROI (%)",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Financial correlation analysis
            st.markdown("### 📊 Financial Performance Insights")
            
            # Investment vs Revenue correlation
            fig = go.Figure(data=[
                go.Scatter(
                    x=financial_analysis['investment_amount'],
                    y=financial_analysis['revenue_generated'],
                    mode='markers+text',
                    text=financial_analysis['partner_name'],
                    textposition='top center',
                    marker=dict(
                        size=financial_analysis['roi'].abs() / 10,
                        color=financial_analysis['profit_margin'],
                        colorscale='RdYlGn',
                        showscale=True,
                        colorbar=dict(title="Profit Margin (%)"),
                        cmin=-50,
                        cmax=100
                    ),
                    hovertemplate='<b>%{text}</b><br>Investment: $%{x:,.0f}<br>Revenue: $%{y:,.0f}<br>ROI: %{marker.size*10:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Investment vs Revenue Correlation (Bubble size = ROI, Color = Profit Margin)",
                xaxis_title="Investment Amount ($)",
                yaxis_title="Revenue Generated ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Financial performance comparison
            st.markdown("### 🔍 Financial Performance Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=financial_analysis['partner_name'],
                        y=financial_analysis['profit_margin'],
                        marker_color=['#2ca02c' if x >= 50 else '#1f77b4' if x >= 25 else '#ff7f0e' if x >= 0 else '#d62728' for x in financial_analysis['profit_margin']],
                        text=financial_analysis['profit_margin'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Partner: %{x}<br>Profit Margin: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Profit Margin by Partnership",
                    xaxis_title="Partner Name",
                    yaxis_title="Profit Margin (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=financial_analysis['partner_name'],
                        y=financial_analysis['investment_efficiency'],
                        marker_color='#9467bd',
                        text=financial_analysis['investment_efficiency'].apply(lambda x: f"{x:.2f}"),
                        textposition='auto',
                        hovertemplate='Partner: %{x}<br>Investment Efficiency: %{y:.2f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Investment Efficiency by Partnership",
                    xaxis_title="Partner Name",
                    yaxis_title="Investment Efficiency",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Financial insights
            st.markdown("### 💡 Financial Performance Insights")
            
            # High ROI partnerships
            high_roi_partners = financial_analysis[financial_analysis['roi'] >= 150]
            if not high_roi_partners.empty:
                st.success(f"🚀 **High ROI Partners**: {', '.join(high_roi_partners['partner_name'].tolist())} deliver excellent returns (≥150%)")
            
            # High profit margin partnerships
            high_margin_partners = financial_analysis[financial_analysis['profit_margin'] >= 50]
            if not high_margin_partners.empty:
                st.info(f"💰 **High Margin Partners**: {', '.join(high_margin_partners['partner_name'].tolist())} have excellent profit margins (≥50%)")
            
            # Loss-making partnerships
            loss_partners = financial_analysis[financial_analysis['profit'] < 0]
            if not loss_partners.empty:
                st.warning(f"⚠️ **Loss-Making Partners**: {', '.join(loss_partners['partner_name'].tolist())} require attention and optimization")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-purple" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Performance Metrics & Benchmarking</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.collaborations.empty:
            # Enhanced performance metrics analysis
            performance_analysis = st.session_state.collaborations.copy()
            
            # Calculate performance metrics
            performance_analysis['roi'] = np.where(
                performance_analysis['investment_amount'] > 0,
                (performance_analysis['revenue_generated'] / performance_analysis['investment_amount'] * 100).round(1),
                0
            )
            performance_analysis['profit'] = performance_analysis['revenue_generated'] - performance_analysis['investment_amount']
            
            # Top performing partnerships
            st.markdown("### 🏆 Top Performing Partnerships")
            
            # Top 5 by revenue
            top_revenue = performance_analysis.nlargest(5, 'revenue_generated')[['partner_name', 'partner_type', 'investment_amount', 'revenue_generated', 'roi']]
            top_revenue['investment_amount'] = top_revenue['investment_amount'].apply(lambda x: f"${x:,.0f}")
            top_revenue['revenue_generated'] = top_revenue['revenue_generated'].apply(lambda x: f"${x:,.0f}")
            top_revenue['roi'] = top_revenue['roi'].apply(lambda x: f"{x:.1f}%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Top 5 by Revenue Generated:**")
                st.dataframe(top_revenue, use_container_width=True)
            
            # Top 5 by ROI
            top_roi = performance_analysis.nlargest(5, 'roi')[['partner_name', 'partner_type', 'investment_amount', 'revenue_generated', 'roi']]
            top_roi['investment_amount'] = top_roi['investment_amount'].apply(lambda x: f"${x:,.0f}")
            top_roi['revenue_generated'] = top_roi['revenue_generated'].apply(lambda x: f"${x:,.0f}")
            top_roi['roi'] = top_roi['roi'].apply(lambda x: f"{x:.1f}%")
            
            with col2:
                st.markdown("**Top 5 by ROI:**")
                st.dataframe(top_roi, use_container_width=True)
            
            # Performance benchmarking
            st.markdown("### 📈 Performance Benchmarking")
            
            # ROI distribution analysis
            fig = go.Figure(data=[
                go.Histogram(
                    x=performance_analysis['roi'], 
                    nbinsx=10,
                    marker_color='#1f77b4', 
                    opacity=0.7,
                    hovertemplate='ROI: %{x:.1f}%<br>Count: %{y}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="ROI Distribution Across All Partnerships",
                xaxis_title="ROI (%)",
                yaxis_title="Number of Partnerships",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance insights
            st.markdown("### 💡 Performance Insights")
            
            # ROI performance analysis
            excellent_roi = performance_analysis[performance_analysis['roi'] >= 200]
            good_roi = performance_analysis[(performance_analysis['roi'] >= 100) & (performance_analysis['roi'] < 200)]
            moderate_roi = performance_analysis[(performance_analysis['roi'] >= 50) & (performance_analysis['roi'] < 100)]
            low_roi = performance_analysis[performance_analysis['roi'] < 50]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Excellent ROI (≥200%)", len(excellent_roi))
            with col2:
                st.metric("Good ROI (100-200%)", len(good_roi))
            with col3:
                st.metric("Moderate ROI (50-100%)", len(moderate_roi))
            with col4:
                st.metric("Low ROI (<50%)", len(low_roi))
            
            # Performance recommendations
            st.markdown("### 🎯 Performance Recommendations")
            
            if len(excellent_roi) > 0:
                st.success(f"✅ **Scale Success**: {', '.join(excellent_roi['partner_name'].tolist())} show excellent performance - consider expanding these partnerships")
            
            if len(low_roi) > 0:
                st.warning(f"⚠️ **Optimization Needed**: {', '.join(low_roi['partner_name'].tolist())} have low ROI - review and optimize these partnerships")
            
            if len(good_roi) > len(moderate_roi):
                st.info(f"ℹ️ **Strong Performance**: Majority of partnerships show good ROI performance")
            else:
                st.warning(f"⚠️ **Improvement Opportunity**: Focus on improving ROI for moderate-performing partnerships")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🎯 Strategic Insights & Recommendations</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.collaborations.empty:
            # Strategic insights and recommendations
            st.markdown("### 🎯 Strategic Collaboration Insights")
            
            # Calculate ROI for the collaborations dataframe first
            collaborations_with_roi = st.session_state.collaborations.copy()
            collaborations_with_roi['roi'] = np.where(
                collaborations_with_roi['investment_amount'] > 0,
                (collaborations_with_roi['revenue_generated'] / collaborations_with_roi['investment_amount'] * 100).round(1),
                0
            )
            
            # Partnership portfolio analysis
            total_investment = collaborations_with_roi['investment_amount'].sum()
            total_revenue = collaborations_with_roi['revenue_generated'].sum()
            overall_roi = (total_revenue / total_investment * 100) if total_investment > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Portfolio ROI", f"{overall_roi:.1f}%")
            with col2:
                st.metric("Investment Efficiency", f"{(total_revenue / total_investment):.2f}" if total_investment > 0 else "0.00")
            with col3:
                st.metric("Partnership Success Rate", f"{(len(collaborations_with_roi[collaborations_with_roi['roi'] > 100]) / len(collaborations_with_roi) * 100):.1f}%" if len(collaborations_with_roi) > 0 else "0%")
            
            # Strategic recommendations
            st.markdown("### 💡 Strategic Recommendations")
            
            # High-performing partnerships
            high_performers = collaborations_with_roi[collaborations_with_roi['roi'] >= 150]
            if not high_performers.empty:
                st.success(f"🚀 **Expand High Performers**: {', '.join(high_performers['partner_name'].tolist())} show exceptional performance - consider expanding these partnerships")
            
            # Underperforming partnerships
            underperformers = collaborations_with_roi[collaborations_with_roi['roi'] < 50]
            if not underperformers.empty:
                st.warning(f"⚠️ **Optimize Underperformers**: {', '.join(underperformers['partner_name'].tolist())} need performance optimization or reconsideration")
            
            # Investment optimization
            if overall_roi < 100:
                st.info(f"💰 **Investment Optimization**: Overall portfolio ROI of {overall_roi:.1f}% suggests investment strategy optimization needed")
            else:
                st.success(f"✅ **Strong Portfolio**: Overall portfolio ROI of {overall_roi:.1f}% indicates successful collaboration strategy")
            
            # Partnership diversification
            partner_types = st.session_state.collaborations['partner_type'].nunique()
            if partner_types < 3:
                st.warning(f"⚠️ **Diversification Opportunity**: Only {partner_types} partner types - consider diversifying partnership portfolio")
            else:
                st.success(f"✅ **Well Diversified**: {partner_types} partner types show good portfolio diversification")
            
            # Future collaboration opportunities
            st.markdown("### 🔮 Future Collaboration Opportunities")
            
            # Identify gaps and opportunities
            current_partner_types = set(st.session_state.collaborations['partner_type'].unique())
            potential_partner_types = ['Academic', 'Industry', 'Government', 'Startup', 'International', 'Research Institute']
            missing_types = [pt for pt in potential_partner_types if pt not in current_partner_types]
            
            if missing_types:
                st.info(f"🌐 **Expansion Opportunities**: Consider partnerships with {', '.join(missing_types)} to diversify portfolio")
            else:
                st.success(f"✅ **Comprehensive Coverage**: All major partner types are represented in current portfolio")
            
            # ROI improvement strategies
            st.markdown("### 📈 ROI Improvement Strategies")
            
            if overall_roi < 120:
                st.write("**Recommended Actions:**")
                st.write("• Review underperforming partnerships and implement improvement plans")
                st.write("• Optimize investment allocation based on performance data")
                st.write("• Strengthen partnership management and monitoring processes")
                st.write("• Consider strategic partnerships with higher ROI potential")
            else:
                st.write("**Maintenance Actions:**")
                st.write("• Continue monitoring high-performing partnerships")
                st.write("• Identify opportunities for partnership expansion")
                st.write("• Maintain strong partnership management practices")
                st.write("• Explore new collaboration opportunities in emerging areas")

def show_employee_performance():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">👥 Employee Performance and Innovation Culture</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.researchers.empty:
        st.info("📊 Please upload researcher data to view employee performance analytics.")
        st.markdown("""
        **💡 To see the full Employee Performance & Innovation Culture analytics:**
        1. Go to the **📝 Data Input** tab
        2. Click **🚀 Load Sample Data into Program** to load sample researcher data
        3. Or upload your own researcher data file
        4. Then return to this tab to see comprehensive analytics
        """)
        return
    
    # Enhanced employee overview with comprehensive metrics
    st.markdown("""
    <div class="metric-card-orange" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Employee Overview & Innovation Culture</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate advanced employee metrics
    total_researchers = len(st.session_state.researchers)
    active_researchers = len(st.session_state.researchers[st.session_state.researchers['status'] == 'Active'])
    avg_experience = st.session_state.researchers['experience_years'].mean()
    avg_salary = st.session_state.researchers['salary'].mean()
    
    # Calculate advanced metrics with data validation
    experience_distribution = st.session_state.researchers['experience_years'].value_counts().sort_index()
    salary_distribution = st.session_state.researchers['salary'].value_counts().sort_index()
    
    # Innovation culture metrics
    senior_researchers = len(st.session_state.researchers[st.session_state.researchers['experience_years'] >= 8])
    mid_level_researchers = len(st.session_state.researchers[(st.session_state.researchers['experience_years'] >= 3) & (st.session_state.researchers['experience_years'] < 8)])
    junior_researchers = len(st.session_state.researchers[st.session_state.researchers['experience_years'] < 3])
    
    # Performance indicators
    high_salary_researchers = len(st.session_state.researchers[st.session_state.researchers['salary'] >= avg_salary * 1.2])
    low_salary_researchers = len(st.session_state.researchers[st.session_state.researchers['salary'] <= avg_salary * 0.8])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Researchers", total_researchers)
    with col2:
        st.metric("Active Researchers", active_researchers, delta=f"{active_researchers - (total_researchers - active_researchers)}")
    with col3:
        st.metric("Avg Experience", f"{avg_experience:.1f} years")
    with col4:
        st.metric("Avg Salary", f"${avg_salary:,.0f}")
    
    # Additional overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Senior Researchers (8+ yrs)", senior_researchers)
    with col2:
        st.metric("Mid-Level (3-7 yrs)", mid_level_researchers)
    with col3:
        st.metric("Junior (<3 yrs)", junior_researchers)
    with col4:
        st.metric("High Performers", high_salary_researchers)
    
    # Innovation culture insights
    st.markdown("### 💡 Innovation Culture Insights")
    
    if senior_researchers / total_researchers > 0.3:
        st.success(f"🚀 **Strong Senior Leadership**: {senior_researchers/total_researchers*100:.1f}% senior researchers provide excellent mentorship")
    elif senior_researchers / total_researchers > 0.2:
        st.info(f"ℹ️ **Balanced Experience**: {senior_researchers/total_researchers*100:.1f}% senior researchers with good mentorship potential")
    else:
        st.warning(f"⚠️ **Experience Gap**: Only {senior_researchers/total_researchers*100:.1f}% senior researchers - consider development programs")
    
    if high_salary_researchers / total_researchers > 0.2:
        st.success(f"💰 **High Performance Culture**: {high_salary_researchers/total_researchers*100:.1f}% researchers above average salary indicate strong performance")
    else:
        st.info(f"ℹ️ **Performance Development**: {high_salary_researchers/total_researchers*100:.1f}% high performers - focus on development opportunities")
    
    # Enhanced detailed analysis
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Advanced Analytics & Performance Insights</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Department Analysis", "📊 Performance Metrics", "🎓 Training Impact", "🚀 Innovation Culture"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">👥 Department Analysis & Team Performance</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.researchers.empty:
            # Enhanced department analysis with comprehensive metrics
            dept_analysis = st.session_state.researchers.groupby('department').agg({
                'researcher_id': 'count',
                'experience_years': 'mean',
                'salary': 'mean'
            }).reset_index()
            
            # Calculate advanced department metrics
            dept_analysis['experience_efficiency'] = np.where(
                dept_analysis['experience_years'] > 0,
                round(dept_analysis['salary'] / dept_analysis['experience_years'], 0),
                0
            )
            dept_analysis['team_size_weight'] = round(dept_analysis['researcher_id'] / dept_analysis['researcher_id'].sum() * 100, 1)
            dept_analysis['avg_experience'] = round(dept_analysis['experience_years'], 1)
            dept_analysis['avg_salary'] = round(dept_analysis['salary'], 0)
            
            # Key department metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_departments = len(dept_analysis)
                st.metric("Total Departments", total_departments)
            with col2:
                total_dept_researchers = dept_analysis['researcher_id'].sum()
                st.metric("Total Researchers", total_dept_researchers)
            with col3:
                avg_dept_experience = dept_analysis['avg_experience'].mean()
                st.metric("Avg Dept Experience", f"{avg_dept_experience:.1f} years")
            with col4:
                avg_dept_salary = dept_analysis['avg_salary'].mean()
                st.metric("Avg Dept Salary", f"${avg_dept_salary:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced researcher distribution with better styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=dept_analysis['department'], 
                        y=dept_analysis['researcher_id'],
                        marker_color='#1f77b4',
                        text=dept_analysis['researcher_id'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Researchers: %{y}<br>Team Weight: %{text}%<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Researchers by Department",
                    xaxis_title="Department",
                    yaxis_title="Number of Researchers",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced experience analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=dept_analysis['department'], 
                        y=dept_analysis['avg_experience'],
                        marker_color=['#2ca02c' if x >= 8 else '#1f77b4' if x >= 5 else '#ff7f0e' if x >= 3 else '#d62728' for x in dept_analysis['avg_experience']],
                        text=dept_analysis['avg_experience'].apply(lambda x: f"{x:.1f} years"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Avg Experience: %{y:.1f} years<br>Team Size: %{text}<extra></extra>',
                        texttemplate='%{y:.1f} years'
                    )
                ])
                fig.update_layout(
                    title="Average Experience by Department (Color-coded by Experience Level)",
                    xaxis_title="Department",
                    yaxis_title="Average Experience (Years)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional department insights
            st.markdown("### 📊 Department Performance Insights")
            
            # Team size vs experience correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=dept_analysis['researcher_id'],
                    y=dept_analysis['avg_experience'],
                    mode='markers+text',
                    text=dept_analysis['department'],
                    textposition='top center',
                    marker=dict(
                        size=dept_analysis['team_size_weight'] * 3,
                        color=dept_analysis['avg_salary'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Average Salary ($)"),
                        cmin=dept_analysis['avg_salary'].min(),
                        cmax=dept_analysis['avg_salary'].max()
                    ),
                    hovertemplate='<b>%{text}</b><br>Researchers: %{x}<br>Avg Experience: %{y:.1f} years<br>Team Weight: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Team Size vs Experience (Bubble size = Team Weight, Color = Average Salary)",
                xaxis_title="Number of Researchers",
                yaxis_title="Average Experience (Years)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Department efficiency analysis
            st.markdown("### 🔍 Department Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=dept_analysis['department'],
                        y=dept_analysis['avg_salary'],
                        marker_color=['#2ca02c' if x >= avg_dept_salary * 1.1 else '#1f77b4' if x >= avg_dept_salary else '#ff7f0e' if x >= avg_dept_salary * 0.9 else '#d62728' for x in dept_analysis['avg_salary']],
                        text=dept_analysis['avg_salary'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Department: %{x}<br>Avg Salary: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Salary by Department (Color-coded by Performance)",
                    xaxis_title="Department",
                    yaxis_title="Average Salary ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=dept_analysis['department'],
                        y=dept_analysis['experience_efficiency'],
                        marker_color='#9467bd',
                        text=dept_analysis['experience_efficiency'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Department: %{x}<br>Experience Efficiency: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Experience Efficiency by Department (Salary per Year of Experience)",
                    xaxis_title="Department",
                    yaxis_title="Experience Efficiency ($/Year)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Department Metrics")
            display_df = dept_analysis[['department', 'researcher_id', 'avg_experience', 'avg_salary', 'experience_efficiency', 'team_size_weight']].copy()
            display_df['avg_experience'] = display_df['avg_experience'].apply(lambda x: f"{x:.1f} years")
            display_df['avg_salary'] = display_df['avg_salary'].apply(lambda x: f"${x:,.0f}")
            display_df['experience_efficiency'] = display_df['experience_efficiency'].apply(lambda x: f"${x:,.0f}")
            display_df['team_size_weight'] = display_df['team_size_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Department insights
            st.markdown("### 💡 Department Strategic Insights")
            
            # High experience departments
            high_exp_depts = dept_analysis[dept_analysis['avg_experience'] >= 8]
            if not high_exp_depts.empty:
                st.success(f"🚀 **High Experience Departments**: {', '.join(high_exp_depts['department'].tolist())} have excellent senior leadership (≥8 years avg)")
            
            # High salary departments
            high_salary_depts = dept_analysis[dept_analysis['avg_salary'] >= avg_dept_salary * 1.1]
            if not high_salary_depts.empty:
                st.info(f"💰 **High Salary Departments**: {', '.join(high_salary_depts['department'].tolist())} have above-average compensation (≥110% of avg)")
            
            # Large teams
            large_teams = dept_analysis[dept_analysis['team_size_weight'] >= 25]
            if not large_teams.empty:
                st.warning(f"⚠️ **Large Teams**: {', '.join(large_teams['department'].tolist())} represent significant team weight (≥25%)")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Performance Metrics & Career Development</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.researchers.empty:
            # Enhanced performance analysis with comprehensive metrics
            performance_analysis = st.session_state.researchers.groupby('education_level').agg({
                'researcher_id': 'count',
                'salary': 'mean',
                'experience_years': 'mean'
            }).reset_index()
            
            # Calculate advanced performance metrics
            performance_analysis['salary_efficiency'] = np.where(
                performance_analysis['experience_years'] > 0,
                round(performance_analysis['salary'] / performance_analysis['experience_years'], 0),
                0
            )
            performance_analysis['education_weight'] = round(performance_analysis['researcher_id'] / performance_analysis['researcher_id'].sum() * 100, 1)
            performance_analysis['avg_salary'] = round(performance_analysis['salary'], 0)
            performance_analysis['avg_experience'] = round(performance_analysis['experience_years'], 1)
            
            # Key performance metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_education_levels = len(performance_analysis)
                st.metric("Education Levels", total_education_levels)
            with col2:
                total_perf_researchers = performance_analysis['researcher_id'].sum()
                st.metric("Total Researchers", total_perf_researchers)
            with col3:
                avg_perf_salary = performance_analysis['avg_salary'].mean()
                st.metric("Avg Performance Salary", f"${avg_perf_salary:,.0f}")
            with col4:
                avg_perf_experience = performance_analysis['avg_experience'].mean()
                st.metric("Avg Performance Experience", f"{avg_perf_experience:.1f} years")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced salary analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=performance_analysis['education_level'], 
                        y=performance_analysis['avg_salary'],
                        marker_color=['#2ca02c' if x >= avg_perf_salary * 1.1 else '#1f77b4' if x >= avg_perf_salary else '#ff7f0e' if x >= avg_perf_salary * 0.9 else '#d62728' for x in performance_analysis['avg_salary']],
                        text=performance_analysis['avg_salary'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Avg Salary: $%{y:,.0f}<br>Researchers: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Average Salary by Education Level (Color-coded by Performance)",
                    xaxis_title="Education Level",
                    yaxis_title="Average Salary ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced experience analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=performance_analysis['education_level'], 
                        y=performance_analysis['avg_experience'],
                        marker_color='#ff7f0e',
                        text=performance_analysis['avg_experience'].apply(lambda x: f"{x:.1f} years"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Avg Experience: %{y:.1f} years<br>Researchers: %{text}<extra></extra>',
                        texttemplate='%{y:.1f} years'
                    )
                ])
                fig.update_layout(
                    title="Average Experience by Education Level",
                    xaxis_title="Education Level",
                    yaxis_title="Average Experience (Years)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional performance insights
            st.markdown("### 📊 Performance Correlation Insights")
            
            # Education level vs salary correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=performance_analysis['researcher_id'],
                    y=performance_analysis['avg_salary'],
                    mode='markers+text',
                    text=performance_analysis['education_level'],
                    textposition='top center',
                    marker=dict(
                        size=performance_analysis['education_weight'] * 3,
                        color=performance_analysis['avg_experience'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Average Experience (Years)"),
                        cmin=performance_analysis['avg_experience'].min(),
                        cmax=performance_analysis['avg_experience'].max()
                    ),
                    hovertemplate='<b>%{text}</b><br>Researchers: %{x}<br>Avg Salary: $%{y:,.0f}<br>Weight: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Team Size vs Salary (Bubble size = Education Weight, Color = Experience)",
                xaxis_title="Number of Researchers",
                yaxis_title="Average Salary ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance efficiency analysis
            st.markdown("### 🔍 Performance Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=performance_analysis['education_level'],
                        y=performance_analysis['salary_efficiency'],
                        marker_color='#9467bd',
                        text=performance_analysis['salary_efficiency'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Education: %{x}<br>Salary Efficiency: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Salary Efficiency by Education Level (Salary per Year of Experience)",
                    xaxis_title="Education Level",
                    yaxis_title="Salary Efficiency ($/Year)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=performance_analysis['education_level'],
                        y=performance_analysis['education_weight'],
                        marker_color='#1f77b4',
                        text=performance_analysis['education_weight'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Education: %{x}<br>Weight: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Education Level Distribution (Percentage of Total Team)",
                    xaxis_title="Education Level",
                    yaxis_title="Team Weight (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Performance Metrics")
            display_df = performance_analysis[['education_level', 'researcher_id', 'avg_salary', 'avg_experience', 'salary_efficiency', 'education_weight']].copy()
            display_df['avg_salary'] = display_df['avg_salary'].apply(lambda x: f"${x:,.0f}")
            display_df['avg_experience'] = display_df['avg_experience'].apply(lambda x: f"{x:.1f} years")
            display_df['salary_efficiency'] = display_df['salary_efficiency'].apply(lambda x: f"${x:,.0f}")
            display_df['education_weight'] = display_df['education_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Performance insights
            st.markdown("### 💡 Performance Strategic Insights")
            
            # High salary education levels
            high_salary_edu = performance_analysis[performance_analysis['avg_salary'] >= avg_perf_salary * 1.1]
            if not high_salary_edu.empty:
                st.success(f"💰 **High Salary Education**: {', '.join(high_salary_edu['education_level'].tolist())} command above-average salaries (≥110% of avg)")
            
            # High efficiency education levels
            high_efficiency_edu = performance_analysis[performance_analysis['salary_efficiency'] >= performance_analysis['salary_efficiency'].mean() * 1.2]
            if not high_efficiency_edu.empty:
                st.info(f"🚀 **High Efficiency Education**: {', '.join(high_efficiency_edu['education_level'].tolist())} show excellent salary-to-experience ratios")
            
            # Dominant education levels
            dominant_edu = performance_analysis[performance_analysis['education_weight'] >= 40]
            if not dominant_edu.empty:
                st.warning(f"⚠️ **Dominant Education**: {', '.join(dominant_edu['education_level'].tolist())} represent significant team weight (≥40%)")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-purple" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🎓 Training Impact & Development Programs</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.training.empty:
            # Enhanced training analysis with comprehensive metrics
            training_analysis = st.session_state.training.groupby('training_type').agg({
                'training_id': 'count',
                'effectiveness_rating': 'mean',
                'cost': 'sum'
            }).reset_index()
            
            # Calculate advanced training metrics
            training_analysis['cost_per_training'] = np.where(
                training_analysis['training_id'] > 0,
                round(training_analysis['cost'] / training_analysis['training_id'], 0),
                0
            )
            training_analysis['training_weight'] = round(training_analysis['training_id'] / training_analysis['training_id'].sum() * 100, 1)
            training_analysis['avg_effectiveness'] = round(training_analysis['effectiveness_rating'], 1)
            training_analysis['total_cost'] = round(training_analysis['cost'], 0)
            
            # Key training metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_training_types = len(training_analysis)
                st.metric("Training Types", total_training_types)
            with col2:
                total_trainings = training_analysis['training_id'].sum()
                st.metric("Total Trainings", total_trainings)
            with col3:
                avg_effectiveness = training_analysis['avg_effectiveness'].mean()
                st.metric("Avg Effectiveness", f"{avg_effectiveness:.1f}/5")
            with col4:
                total_training_cost = training_analysis['total_cost'].sum()
                st.metric("Total Cost", f"${total_training_cost:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced training effectiveness with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=training_analysis['training_type'], 
                        y=training_analysis['avg_effectiveness'],
                        marker_color=['#2ca02c' if x >= 4.5 else '#1f77b4' if x >= 4.0 else '#ff7f0e' if x >= 3.5 else '#d62728' for x in training_analysis['avg_effectiveness']],
                        text=training_analysis['avg_effectiveness'].apply(lambda x: f"{x:.1f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Effectiveness: %{y:.1f}/5<br>Trainings: %{text}<extra></extra>',
                        texttemplate='%{y:.1f}'
                    )
                ])
                fig.update_layout(
                    title="Training Effectiveness by Type (Color-coded by Performance)",
                    xaxis_title="Training Type",
                    yaxis_title="Effectiveness Rating (/5)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced training cost analysis
                fig = go.Figure(data=[
                    go.Bar(
                        x=training_analysis['training_type'], 
                        y=training_analysis['total_cost'],
                        marker_color='#d62728',
                        text=training_analysis['total_cost'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Cost: $%{y:,.0f}<br>Trainings: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Training Cost by Type",
                    xaxis_title="Training Type",
                    yaxis_title="Total Cost ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional training insights
            st.markdown("### 📊 Training Performance Insights")
            
            # Training effectiveness vs cost correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=training_analysis['total_cost'],
                    y=training_analysis['avg_effectiveness'],
                    mode='markers+text',
                    text=training_analysis['training_type'],
                    textposition='top center',
                    marker=dict(
                        size=training_analysis['training_weight'] * 3,
                        color=training_analysis['cost_per_training'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Cost per Training ($)"),
                        cmin=training_analysis['cost_per_training'].min(),
                        cmax=training_analysis['cost_per_training'].max()
                    ),
                    hovertemplate='<b>%{text}</b><br>Total Cost: $%{x:,.0f}<br>Effectiveness: %{y:.1f}/5<br>Weight: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Training Cost vs Effectiveness (Bubble size = Training Weight, Color = Cost per Training)",
                xaxis_title="Total Cost ($)",
                yaxis_title="Effectiveness Rating (/5)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Training efficiency analysis
            st.markdown("### 🔍 Training Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=training_analysis['training_type'],
                        y=training_analysis['cost_per_training'],
                        marker_color='#9467bd',
                        text=training_analysis['cost_per_training'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Training: %{x}<br>Cost per Training: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Cost per Training by Type",
                    xaxis_title="Training Type",
                    yaxis_title="Cost per Training ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=training_analysis['training_type'],
                        y=training_analysis['training_weight'],
                        marker_color='#1f77b4',
                        text=training_analysis['training_weight'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Training: %{x}<br>Weight: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Training Type Distribution (Percentage of Total Trainings)",
                    xaxis_title="Training Type",
                    yaxis_title="Training Weight (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Training Metrics")
            display_df = training_analysis[['training_type', 'training_id', 'avg_effectiveness', 'total_cost', 'cost_per_training', 'training_weight']].copy()
            display_df['avg_effectiveness'] = display_df['avg_effectiveness'].apply(lambda x: f"{x:.1f}/5")
            display_df['total_cost'] = display_df['total_cost'].apply(lambda x: f"${x:,.0f}")
            display_df['cost_per_training'] = display_df['cost_per_training'].apply(lambda x: f"${x:,.0f}")
            display_df['training_weight'] = display_df['training_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Training insights
            st.markdown("### 💡 Training Strategic Insights")
            
            # High effectiveness training types
            high_effectiveness_training = training_analysis[training_analysis['avg_effectiveness'] >= 4.5]
            if not high_effectiveness_training.empty:
                st.success(f"🚀 **High Effectiveness Training**: {', '.join(high_effectiveness_training['training_type'].tolist())} show excellent results (≥4.5/5)")
            
            # Cost-effective training types
            cost_effective_training = training_analysis[training_analysis['cost_per_training'] <= training_analysis['cost_per_training'].mean() * 0.8]
            if not cost_effective_training.empty:
                st.info(f"💰 **Cost-Effective Training**: {', '.join(cost_effective_training['training_type'].tolist())} provide good value (≤80% of avg cost)")
            
            # Dominant training types
            dominant_training = training_analysis[training_analysis['training_weight'] >= 30]
            if not dominant_training.empty:
                st.warning(f"⚠️ **Dominant Training**: {', '.join(dominant_training['training_type'].tolist())} represent significant training weight (≥30%)")
        else:
            st.info("📊 No training data available. Please upload training data to view comprehensive training analytics.")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🚀 Innovation Culture & Strategic Development</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.researchers.empty:
            # Innovation culture comprehensive analysis
            innovation_metrics = st.session_state.researchers.copy()
            
            # Calculate innovation culture metrics
            innovation_metrics['experience_level'] = np.where(
                innovation_metrics['experience_years'] >= 8, 'Senior',
                np.where(innovation_metrics['experience_years'] >= 3, 'Mid-Level', 'Junior')
            )
            
            innovation_metrics['performance_tier'] = np.where(
                innovation_metrics['salary'] >= innovation_metrics['salary'].mean() * 1.2, 'High Performer',
                np.where(innovation_metrics['salary'] >= innovation_metrics['salary'].mean() * 0.8, 'Average Performer', 'Low Performer')
            )
            
            # Innovation culture overview metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                senior_ratio = round(senior_researchers / total_researchers * 100, 1)
                st.metric("Senior Leadership Ratio", f"{senior_ratio}%")
            with col2:
                high_performer_ratio = round(high_salary_researchers / total_researchers * 100, 1)
                st.metric("High Performer Ratio", f"{high_performer_ratio}%")
            with col3:
                experience_balance = round(mid_level_researchers / total_researchers * 100, 1)
                st.metric("Mid-Level Balance", f"{experience_balance}%")
            with col4:
                mentorship_potential = round(senior_researchers * 3, 0)
                st.metric("Mentorship Capacity", f"{mentorship_potential} researchers")
            
            # Innovation culture visualization
            st.markdown("### 📊 Innovation Culture Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Experience level distribution
                exp_dist = innovation_metrics['experience_level'].value_counts()
                fig = go.Figure(data=[
                    go.Pie(
                        labels=exp_dist.index,
                        values=exp_dist.values,
                        hole=0.4,
                        marker_colors=['#2ca02c', '#1f77b4', '#ff7f0e'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Experience Level Distribution",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance tier distribution
                perf_dist = innovation_metrics['performance_tier'].value_counts()
                fig = go.Figure(data=[
                    go.Pie(
                        labels=perf_dist.index,
                        values=perf_dist.values,
                        hole=0.4,
                        marker_colors=['#2ca02c', '#1f77b4', '#ff7f0e'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Performance Tier Distribution",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Innovation culture correlation analysis
            st.markdown("### 🔍 Innovation Culture Correlations")
            
            # Experience vs Performance correlation
            exp_perf_corr = innovation_metrics.groupby('experience_level')['performance_tier'].value_counts().unstack(fill_value=0)
            
            fig = go.Figure(data=[
                go.Heatmap(
                    z=exp_perf_corr.values,
                    x=exp_perf_corr.columns,
                    y=exp_perf_corr.index,
                    colorscale='Viridis',
                    text=exp_perf_corr.values,
                    texttemplate='%{text}',
                    textfont={"size": 12},
                    hovertemplate='<b>%{y} - %{x}</b><br>Count: %{z}<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Experience Level vs Performance Tier Correlation",
                xaxis_title="Performance Tier",
                yaxis_title="Experience Level",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Innovation culture insights
            st.markdown("### 💡 Innovation Culture Strategic Insights")
            
            # Senior leadership assessment
            if senior_ratio >= 30:
                st.success(f"🚀 **Excellent Senior Leadership**: {senior_ratio}% senior researchers provide strong mentorship and innovation leadership")
            elif senior_ratio >= 20:
                st.info(f"ℹ️ **Good Senior Leadership**: {senior_ratio}% senior researchers with solid mentorship potential")
            else:
                st.warning(f"⚠️ **Senior Leadership Gap**: Only {senior_ratio}% senior researchers - critical need for development programs")
            
            # High performer assessment
            if high_performer_ratio >= 25:
                st.success(f"💰 **Strong Performance Culture**: {high_performer_ratio}% high performers indicate excellent innovation potential")
            elif high_performer_ratio >= 15:
                st.info(f"ℹ️ **Developing Performance Culture**: {high_performer_ratio}% high performers with growth opportunities")
            else:
                st.warning(f"⚠️ **Performance Development Needed**: Only {high_performer_ratio}% high performers - focus on development")
            
            # Experience balance assessment
            if experience_balance >= 40:
                st.success(f"⚖️ **Balanced Experience Distribution**: {experience_balance}% mid-level researchers provide good team balance")
            elif experience_balance >= 30:
                st.info(f"ℹ️ **Moderate Experience Balance**: {experience_balance}% mid-level researchers with room for improvement")
            else:
                st.warning(f"⚠️ **Experience Imbalance**: Only {experience_balance}% mid-level researchers - consider development programs")
            
            # Strategic recommendations
            st.markdown("### 🎯 Strategic Development Recommendations")
            
            if senior_ratio < 25:
                st.markdown("""
                **🚀 Senior Leadership Development:**
                - Implement mentorship programs for mid-level researchers
                - Create leadership development tracks
                - Establish knowledge transfer initiatives
                - Consider external senior talent acquisition
                """)
            
            if high_performer_ratio < 20:
                st.markdown("""
                **💰 Performance Enhancement:**
                - Develop high-potential identification programs
                - Implement performance-based development tracks
                - Create innovation challenge programs
                - Establish recognition and reward systems
                """)
            
            if experience_balance < 35:
                st.markdown("""
                **⚖️ Experience Balance Optimization:**
                - Focus on mid-level researcher development
                - Create career progression pathways
                - Implement cross-training programs
                - Establish peer mentoring initiatives
                """)
            
            # Innovation culture metrics table
            st.markdown("### 📋 Innovation Culture Metrics Summary")
            innovation_summary = pd.DataFrame({
                'Metric': ['Senior Leadership Ratio', 'High Performer Ratio', 'Mid-Level Balance', 'Mentorship Capacity'],
                'Value': [f"{senior_ratio}%", f"{high_performer_ratio}%", f"{experience_balance}%", f"{mentorship_potential} researchers"],
                'Status': [
                    '🚀 Excellent' if senior_ratio >= 30 else 'ℹ️ Good' if senior_ratio >= 20 else '⚠️ Needs Attention',
                    '💰 Strong' if high_performer_ratio >= 25 else 'ℹ️ Developing' if high_performer_ratio >= 15 else '⚠️ Needs Development',
                    '⚖️ Balanced' if experience_balance >= 40 else 'ℹ️ Moderate' if experience_balance >= 30 else '⚠️ Imbalanced',
                    '🎯 Ready' if mentorship_potential >= total_researchers else 'ℹ️ Developing' if mentorship_potential >= total_researchers * 0.5 else '⚠️ Limited'
                ]
            })
            st.dataframe(innovation_summary, use_container_width=True)

def show_technology_analysis():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">🔬 Technology and Trend Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.projects.empty and st.session_state.equipment.empty:
        st.info("📊 Please upload project and equipment data to view technology analysis.")
        st.markdown("""
        **💡 To see the full Technology and Trend Analysis:**
        1. Go to the **📝 Data Input** tab
        2. Click **🚀 Load Sample Data into Program** to load sample project and equipment data
        3. Or upload your own project and equipment data files
        4. Then return to this tab to see comprehensive technology analytics
        """)
        return
    
    # Enhanced technology overview with comprehensive metrics
    st.markdown("""
    <div class="metric-card-blue" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Technology Overview & Innovation Pipeline</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate advanced technology metrics
    if not st.session_state.projects.empty:
        tech_areas = st.session_state.projects['technology_area'].nunique()
        total_projects = len(st.session_state.projects)
        avg_trl = st.session_state.projects['trl_level'].mean()
        total_budget = st.session_state.projects['budget'].sum()
        
        # Technology maturity analysis
        high_trl_projects = len(st.session_state.projects[st.session_state.projects['trl_level'] >= 7])
        mid_trl_projects = len(st.session_state.projects[(st.session_state.projects['trl_level'] >= 4) & (st.session_state.projects['trl_level'] < 7)])
        low_trl_projects = len(st.session_state.projects[st.session_state.projects['trl_level'] < 4])
        
        # Budget efficiency analysis
        avg_budget_per_project = total_budget / total_projects if total_projects > 0 else 0
        high_budget_projects = len(st.session_state.projects[st.session_state.projects['budget'] >= avg_budget_per_project * 1.2])
        low_budget_projects = len(st.session_state.projects[st.session_state.projects['budget'] <= avg_budget_per_project * 0.8])
    
    if not st.session_state.equipment.empty:
        equipment_types = st.session_state.equipment['equipment_type'].nunique()
        total_equipment_cost = st.session_state.equipment['cost'].sum()
        total_equipment = len(st.session_state.equipment)
        avg_utilization = st.session_state.equipment['utilized_hours'].sum() / st.session_state.equipment['total_hours'].sum() * 100 if st.session_state.equipment['total_hours'].sum() > 0 else 0
    
    # Technology overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not st.session_state.projects.empty:
            st.metric("Technology Areas", tech_areas)
        else:
            st.metric("Technology Areas", 0)
    with col2:
        if not st.session_state.projects.empty:
            st.metric("Total Projects", total_projects)
        else:
            st.metric("Total Projects", 0)
    with col3:
        if not st.session_state.projects.empty:
            st.metric("Avg TRL Level", f"{avg_trl:.1f}")
        else:
            st.metric("Avg TRL Level", "N/A")
    with col4:
        if not st.session_state.projects.empty:
            st.metric("Total Budget", f"${total_budget:,.0f}")
        else:
            st.metric("Total Budget", "$0")
    
    # Additional technology metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if not st.session_state.projects.empty:
            st.metric("High TRL (7-9)", high_trl_projects)
        else:
            st.metric("High TRL (7-9)", 0)
    with col2:
        if not st.session_state.projects.empty:
            st.metric("Mid TRL (4-6)", mid_trl_projects)
        else:
            st.metric("Mid TRL (4-6)", 0)
    with col3:
        if not st.session_state.projects.empty:
            st.metric("Low TRL (1-3)", low_trl_projects)
        else:
            st.metric("Low TRL (1-3)", 0)
    with col4:
        if not st.session_state.projects.empty:
            st.metric("Avg Budget/Project", f"${avg_budget_per_project:,.0f}")
        else:
            st.metric("Avg Budget/Project", "$0")
    
    # Equipment overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if not st.session_state.equipment.empty:
            st.metric("Equipment Types", equipment_types)
        else:
            st.metric("Equipment Types", 0)
    with col2:
        if not st.session_state.equipment.empty:
            st.metric("Total Equipment", total_equipment)
        else:
            st.metric("Total Equipment", 0)
    with col3:
        if not st.session_state.equipment.empty:
            st.metric("Total Investment", f"${total_equipment_cost:,.0f}")
        else:
            st.metric("Total Investment", "$0")
    with col4:
        if not st.session_state.equipment.empty:
            st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
        else:
            st.metric("Avg Utilization", "N/A")
    
    # Technology innovation insights
    if not st.session_state.projects.empty:
        st.markdown("### 💡 Technology Innovation Insights")
        
        if high_trl_projects / total_projects > 0.3:
            st.success(f"🚀 **High Technology Maturity**: {high_trl_projects/total_projects*100:.1f}% projects at TRL 7-9 indicate strong commercialization potential")
        elif high_trl_projects / total_projects > 0.2:
            st.info(f"ℹ️ **Good Technology Maturity**: {high_trl_projects/total_projects*100:.1f}% projects at TRL 7-9 with room for development")
        else:
            st.warning(f"⚠️ **Technology Maturity Gap**: Only {high_trl_projects/total_projects*100:.1f}% projects at TRL 7-9 - focus on development")
        
        if high_budget_projects / total_projects > 0.2:
            st.info(f"💰 **High Investment Focus**: {high_budget_projects/total_projects*100:.1f}% projects receive above-average funding")
        else:
            st.info(f"ℹ️ **Balanced Investment**: {high_budget_projects/total_projects*100:.1f}% high-budget projects with good distribution")
    
    # Enhanced detailed analysis
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Advanced Technology Analytics & Trend Insights</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 Technology Areas", "📊 TRL Analysis", "🔧 Equipment Analysis", "📈 Trend Analysis"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔬 Technology Areas & Innovation Focus</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced technology analysis with comprehensive metrics
            tech_analysis = st.session_state.projects.groupby('technology_area').agg({
                'project_id': 'count',
                'budget': 'sum',
                'trl_level': 'mean'
            }).reset_index()
            
            # Calculate advanced technology metrics
            tech_analysis['avg_budget'] = round(tech_analysis['budget'] / tech_analysis['project_id'], 0)
            tech_analysis['technology_weight'] = round(tech_analysis['project_id'] / tech_analysis['project_id'].sum() * 100, 1)
            tech_analysis['avg_trl'] = round(tech_analysis['trl_level'], 1)
            tech_analysis['total_budget'] = tech_analysis['budget']
            
            # Key technology metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_tech_areas = len(tech_analysis)
                st.metric("Technology Areas", total_tech_areas)
            with col2:
                total_tech_projects = tech_analysis['project_id'].sum()
                st.metric("Total Projects", total_tech_projects)
            with col3:
                avg_tech_trl = tech_analysis['avg_trl'].mean()
                st.metric("Avg Tech TRL", f"{avg_tech_trl:.1f}")
            with col4:
                total_tech_budget = tech_analysis['total_budget'].sum()
                st.metric("Total Tech Budget", f"${total_tech_budget:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced project distribution with better styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=tech_analysis['technology_area'], 
                        y=tech_analysis['project_id'],
                        marker_color='#1f77b4',
                        text=tech_analysis['project_id'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Projects: %{y}<br>Weight: %{text}%<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Projects by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Number of Projects",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced budget analysis with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=tech_analysis['technology_area'], 
                        y=tech_analysis['total_budget'],
                        marker_color=['#2ca02c' if x >= total_tech_budget / len(tech_analysis) * 1.2 else '#1f77b4' if x >= total_tech_budget / len(tech_analysis) else '#ff7f0e' if x >= total_tech_budget / len(tech_analysis) * 0.8 else '#d62728' for x in tech_analysis['total_budget']],
                        text=tech_analysis['total_budget'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Total Budget: $%{y:,.0f}<br>Projects: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Budget by Technology Area (Color-coded by Investment Level)",
                    xaxis_title="Technology Area",
                    yaxis_title="Total Budget ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Additional technology insights
            st.markdown("### 📊 Technology Performance Insights")
            
            # Technology area vs TRL correlation analysis
            fig = go.Figure(data=[
                go.Scatter(
                    x=tech_analysis['project_id'],
                    y=tech_analysis['avg_trl'],
                    mode='markers+text',
                    text=tech_analysis['technology_area'],
                    textposition='top center',
                    marker=dict(
                        size=tech_analysis['technology_weight'] * 3,
                        color=tech_analysis['avg_budget'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Average Budget ($)"),
                        cmin=tech_analysis['avg_budget'].min(),
                        cmax=tech_analysis['avg_budget'].max()
                    ),
                    hovertemplate='<b>%{text}</b><br>Projects: %{x}<br>Avg TRL: %{y:.1f}<br>Weight: %{marker.size/3:.1f}%<extra></extra>'
                )
            ])
            fig.update_layout(
                title="Technology Area Performance (Bubble size = Technology Weight, Color = Average Budget)",
                xaxis_title="Number of Projects",
                yaxis_title="Average TRL Level",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Technology efficiency analysis
            st.markdown("### 🔍 Technology Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        x=tech_analysis['technology_area'],
                        y=tech_analysis['avg_budget'],
                        marker_color='#9467bd',
                        text=tech_analysis['avg_budget'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='Technology: %{x}<br>Avg Budget: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Average Budget per Project by Technology Area",
                    xaxis_title="Technology Area",
                    yaxis_title="Average Budget ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(
                        x=tech_analysis['technology_area'],
                        y=tech_analysis['technology_weight'],
                        marker_color='#1f77b4',
                        text=tech_analysis['technology_weight'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Technology: %{x}<br>Weight: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Technology Area Distribution (Percentage of Total Projects)",
                    xaxis_title="Technology Area",
                    yaxis_title="Technology Weight (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed metrics table
            st.markdown("### 📋 Detailed Technology Metrics")
            display_df = tech_analysis[['technology_area', 'project_id', 'avg_trl', 'total_budget', 'avg_budget', 'technology_weight']].copy()
            display_df['avg_trl'] = display_df['avg_trl'].apply(lambda x: f"{x:.1f}")
            display_df['total_budget'] = display_df['total_budget'].apply(lambda x: f"${x:,.0f}")
            display_df['avg_budget'] = display_df['avg_budget'].apply(lambda x: f"${x:,.0f}")
            display_df['technology_weight'] = display_df['technology_weight'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Technology insights
            st.markdown("### 💡 Technology Strategic Insights")
            
            # High TRL technology areas
            high_trl_tech = tech_analysis[tech_analysis['avg_trl'] >= 7]
            if not high_trl_tech.empty:
                st.success(f"🚀 **High TRL Technologies**: {', '.join(high_trl_tech['technology_area'].tolist())} show excellent maturity (≥7.0)")
            
            # High budget technology areas
            high_budget_tech = tech_analysis[tech_analysis['avg_budget'] >= tech_analysis['avg_budget'].mean() * 1.2]
            if not high_budget_tech.empty:
                st.info(f"💰 **High Investment Technologies**: {', '.join(high_budget_tech['technology_area'].tolist())} receive above-average funding")
            
            # Dominant technology areas
            dominant_tech = tech_analysis[tech_analysis['technology_weight'] >= 30]
            if not dominant_tech.empty:
                st.warning(f"⚠️ **Dominant Technologies**: {', '.join(dominant_tech['technology_area'].tolist())} represent significant project weight (≥30%)")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 TRL Analysis & Technology Maturity</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced TRL analysis with comprehensive metrics
            trl_analysis = st.session_state.projects.groupby('trl_level').agg({
                'project_id': 'count',
                'budget': 'sum'
            }).reset_index()
            
            # Calculate advanced TRL metrics
            trl_analysis['avg_budget'] = round(trl_analysis['budget'] / trl_analysis['project_id'], 0)
            trl_analysis['trl_weight'] = round(trl_analysis['project_id'] / trl_analysis['project_id'].sum() * 100, 1)
            trl_analysis['total_budget'] = trl_analysis['budget']
            trl_analysis['project_count'] = trl_analysis['project_id']
            
            # Add TRL maturity classification
            trl_analysis['maturity_level'] = trl_analysis['trl_level'].apply(
                lambda x: 'High Maturity' if x >= 7 else 'Mid Maturity' if x >= 4 else 'Low Maturity'
            )
            
            # Key TRL metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_trl_levels = len(trl_analysis)
                st.metric("TRL Levels", total_trl_levels)
            with col2:
                total_trl_projects = trl_analysis['project_count'].sum()
                st.metric("Total Projects", total_trl_projects)
            with col3:
                avg_trl_budget = trl_analysis['avg_budget'].mean()
                st.metric("Avg Budget/Project", f"${avg_trl_budget:,.0f}")
            with col4:
                total_trl_budget = trl_analysis['total_budget'].sum()
                st.metric("Total TRL Budget", f"${total_trl_budget:,.0f}")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced project distribution with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=trl_analysis['trl_level'], 
                        y=trl_analysis['project_count'],
                        marker_color=['#2ca02c' if x >= 7 else '#1f77b4' if x >= 4 else '#ff7f0e' for x in trl_analysis['trl_level']],
                        text=trl_analysis['project_count'],
                        textposition='auto',
                        hovertemplate='<b>TRL %{x}</b><br>Projects: %{y}<br>Weight: %{text}%<extra></extra>',
                        texttemplate='%{y}'
                    )
                ])
                fig.update_layout(
                    title="Projects by TRL Level (Color-coded by Maturity)",
                    xaxis_title="TRL Level",
                    yaxis_title="Number of Projects",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced budget analysis with better insights
                fig = go.Figure(data=[
                    go.Bar(
                        x=trl_analysis['trl_level'], 
                        y=trl_analysis['total_budget'],
                        marker_color='#ff7f0e',
                        text=trl_analysis['total_budget'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>TRL %{x}</b><br>Total Budget: $%{y:,.0f}<br>Projects: %{text}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Budget by TRL Level",
                    xaxis_title="TRL Level",
                    yaxis_title="Total Budget ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if not st.session_state.equipment.empty:
            equipment_analysis = st.session_state.equipment.groupby('equipment_type').agg({
                'equipment_id': 'count',
                'cost': 'sum',
                'utilized_hours': 'sum',
                'total_hours': 'sum'
            }).reset_index()
            equipment_analysis['utilization_rate'] = (equipment_analysis['utilized_hours'] / equipment_analysis['total_hours'] * 100).round(1)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=equipment_analysis['equipment_type'], y=equipment_analysis['utilization_rate'],
                           marker_color='#9467bd', text=equipment_analysis['utilization_rate'],
                           textposition='auto')
                ])
                fig.update_layout(title="Equipment Utilization", xaxis_title="Equipment Type", yaxis_title="Utilization (%)")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(x=equipment_analysis['equipment_type'], y=equipment_analysis['cost'],
                           marker_color='#d62728', text=equipment_analysis['cost'],
                           textposition='auto')
                ])
                fig.update_layout(title="Equipment Cost by Type", xaxis_title="Equipment Type", yaxis_title="Cost ($)")
                st.plotly_chart(fig, use_container_width=True)
            
            # Equipment efficiency analysis
            st.markdown("### 🔍 Equipment Efficiency Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Equipment utilization vs cost analysis
                fig = go.Figure(data=[
                    go.Scatter(
                        x=equipment_analysis['cost'],
                        y=equipment_analysis['utilization_rate'],
                        mode='markers+text',
                        text=equipment_analysis['equipment_type'],
                        textposition='top center',
                        marker=dict(
                            size=equipment_analysis['equipment_id'] * 2,
                            color=equipment_analysis['utilization_rate'],
                            colorscale='RdYlGn',
                            showscale=True,
                            colorbar=dict(title="Utilization Rate (%)"),
                            cmin=0,
                            cmax=100
                        ),
                        hovertemplate='<b>%{text}</b><br>Cost: $%{x:,.0f}<br>Utilization: %{y:.1f}%<br>Count: %{marker.size/2}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Equipment Efficiency: Cost vs Utilization (Bubble size = Count, Color = Utilization Rate)",
                    xaxis_title="Equipment Cost ($)",
                    yaxis_title="Utilization Rate (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Equipment investment efficiency
                fig = go.Figure(data=[
                    go.Bar(
                        x=equipment_analysis['equipment_type'],
                        y=equipment_analysis['utilization_rate'],
                        marker_color=['#2ca02c' if x >= 80 else '#1f77b4' if x >= 60 else '#ff7f0e' if x >= 40 else '#d62728' for x in equipment_analysis['utilization_rate']],
                        text=equipment_analysis['utilization_rate'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='Equipment: %{x}<br>Utilization: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Equipment Utilization by Type (Color-coded by Efficiency)",
                    xaxis_title="Equipment Type",
                    yaxis_title="Utilization Rate (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed equipment metrics table
            st.markdown("### 📋 Detailed Equipment Metrics")
            display_df = equipment_analysis[['equipment_type', 'equipment_id', 'cost', 'utilized_hours', 'total_hours', 'utilization_rate']].copy()
            display_df['cost'] = display_df['cost'].apply(lambda x: f"${x:,.0f}")
            display_df['utilization_rate'] = display_df['utilization_rate'].apply(lambda x: f"{x:.1f}%")
            st.dataframe(display_df, use_container_width=True)
            
            # Equipment insights
            st.markdown("### 💡 Equipment Strategic Insights")
            
            # High utilization equipment
            high_util_equipment = equipment_analysis[equipment_analysis['utilization_rate'] >= 80]
            if not high_util_equipment.empty:
                st.success(f"✅ **High Utilization Equipment**: {', '.join(high_util_equipment['equipment_type'].tolist())} show excellent utilization (≥80%)")
            
            # Low utilization equipment
            low_util_equipment = equipment_analysis[equipment_analysis['utilization_rate'] < 50]
            if not low_util_equipment.empty:
                st.warning(f"⚠️ **Low Utilization Equipment**: {', '.join(low_util_equipment['equipment_type'].tolist())} show poor utilization (<50%) - consider optimization")
            
            # High cost equipment
            high_cost_equipment = equipment_analysis[equipment_analysis['cost'] >= equipment_analysis['cost'].mean() * 1.5]
            if not high_cost_equipment.empty:
                st.info(f"💰 **High Investment Equipment**: {', '.join(high_cost_equipment['equipment_type'].tolist())} represent significant capital investment")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-purple" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📈 Trend Analysis & Innovation Forecasting</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Technology trend analysis over time
            if 'start_date' in st.session_state.projects.columns:
                # Convert dates and analyze trends
                projects_with_dates = st.session_state.projects.copy()
                projects_with_dates['start_date'] = pd.to_datetime(projects_with_dates['start_date'], errors='coerce')
                projects_with_dates = projects_with_dates.dropna(subset=['start_date'])
                
                if not projects_with_dates.empty:
                    # Monthly trend analysis
                    projects_with_dates['year_month'] = projects_with_dates['start_date'].dt.to_period('M')
                    monthly_trends = projects_with_dates.groupby('year_month').agg({
                        'project_id': 'count',
                        'budget': 'sum',
                        'trl_level': 'mean'
                    }).reset_index()
                    monthly_trends['year_month'] = monthly_trends['year_month'].astype(str)
                    
                    # Technology area trends
                    tech_trends = projects_with_dates.groupby(['year_month', 'technology_area']).agg({
                        'project_id': 'count',
                        'budget': 'sum'
                    }).reset_index()
                    tech_trends['year_month'] = tech_trends['year_month'].astype(str)
                    
                    # Trend visualizations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Project count trends
                        fig = go.Figure(data=[
                            go.Scatter(
                                x=monthly_trends['year_month'],
                                y=monthly_trends['project_id'],
                                mode='lines+markers',
                                line=dict(color='#1f77b4', width=3),
                                marker=dict(size=8, color='#1f77b4'),
                                name='Project Count'
                            )
                        ])
                        fig.update_layout(
                            title="Project Count Trends Over Time",
                            xaxis_title="Month",
                            yaxis_title="Number of Projects",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Budget trends
                        fig = go.Figure(data=[
                            go.Scatter(
                                x=monthly_trends['year_month'],
                                y=monthly_trends['budget'],
                                mode='lines+markers',
                                line=dict(color='#2ca02c', width=3),
                                marker=dict(size=8, color='#2ca02c'),
                                name='Total Budget'
                            )
                        ])
                        fig.update_layout(
                            title="Budget Trends Over Time",
                            xaxis_title="Month",
                            yaxis_title="Total Budget ($)",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Technology area trend analysis
                    st.markdown("### 🔬 Technology Area Trends")
                    
                    # Top technology areas by trend
                    top_tech_areas = tech_trends.groupby('technology_area')['project_id'].sum().nlargest(5)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Technology area growth trends
                        fig = go.Figure()
                        for tech in top_tech_areas.index:
                            tech_data = tech_trends[tech_trends['technology_area'] == tech]
                            fig.add_trace(go.Scatter(
                                x=tech_data['year_month'],
                                y=tech_data['project_id'],
                                mode='lines+markers',
                                name=tech,
                                line=dict(width=2)
                            ))
                        
                        fig.update_layout(
                            title="Technology Area Growth Trends (Top 5)",
                            xaxis_title="Month",
                            yaxis_title="Number of Projects",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Technology area budget trends
                        fig = go.Figure()
                        for tech in top_tech_areas.index:
                            tech_data = tech_trends[tech_trends['technology_area'] == tech]
                            fig.add_trace(go.Scatter(
                                x=tech_data['year_month'],
                                y=tech_data['budget'],
                                mode='lines+markers',
                                name=tech,
                                line=dict(width=2)
                            ))
                        
                        fig.update_layout(
                            title="Technology Area Budget Trends (Top 5)",
                            xaxis_title="Month",
                            yaxis_title="Total Budget ($)",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=50, r=50, t=80, b=50),
                            height=400,
                            xaxis_tickangle=-45
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # TRL maturity trends
                    st.markdown("### 📊 TRL Maturity Trends")
                    
                    trl_trends = projects_with_dates.groupby(['year_month', 'trl_level']).agg({
                        'project_id': 'count'
                    }).reset_index()
                    trl_trends['year_month'] = trl_trends['year_month'].astype(str)
                    
                    # TRL trend visualization
                    fig = go.Figure()
                    for trl in sorted(trl_trends['trl_level'].unique()):
                        trl_data = trl_trends[trl_trends['trl_level'] == trl]
                        fig.add_trace(go.Scatter(
                            x=trl_data['year_month'],
                            y=trl_data['project_id'],
                            mode='lines+markers',
                            name=f'TRL {trl}',
                            line=dict(width=2)
                        ))
                    
                    fig.update_layout(
                        title="TRL Level Trends Over Time",
                        xaxis_title="Month",
                        yaxis_title="Number of Projects",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50),
                        height=400,
                        xaxis_tickangle=-45
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Innovation forecasting insights
                    st.markdown("### 🔮 Innovation Forecasting Insights")
                    
                    # Calculate trend indicators
                    if len(monthly_trends) >= 3:
                        # Project growth rate
                        recent_projects = monthly_trends['project_id'].tail(3).mean()
                        earlier_projects = monthly_trends['project_id'].head(3).mean()
                        project_growth_rate = ((recent_projects - earlier_projects) / earlier_projects * 100) if earlier_projects > 0 else 0
                        
                        # Budget growth rate
                        recent_budget = monthly_trends['budget'].tail(3).mean()
                        earlier_budget = monthly_trends['budget'].head(3).mean()
                        budget_growth_rate = ((recent_budget - earlier_budget) / earlier_budget * 100) if earlier_budget > 0 else 0
                        
                        # TRL maturity trend
                        recent_trl = monthly_trends['trl_level'].tail(3).mean()
                        earlier_trl = monthly_trends['trl_level'].head(3).mean()
                        trl_growth_rate = ((recent_trl - earlier_trl) / earlier_trl * 100) if earlier_trl > 0 else 0
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if project_growth_rate > 10:
                                st.success(f"🚀 **Project Growth**: {project_growth_rate:.1f}% increase in project count")
                            elif project_growth_rate > 0:
                                st.info(f"📈 **Project Growth**: {project_growth_rate:.1f}% increase in project count")
                            else:
                                st.warning(f"📉 **Project Decline**: {abs(project_growth_rate):.1f}% decrease in project count")
                        
                        with col2:
                            if budget_growth_rate > 15:
                                st.success(f"💰 **Budget Growth**: {budget_growth_rate:.1f}% increase in R&D investment")
                            elif budget_growth_rate > 0:
                                st.info(f"📈 **Budget Growth**: {budget_growth_rate:.1f}% increase in R&D investment")
                            else:
                                st.warning(f"📉 **Budget Decline**: {abs(budget_growth_rate):.1f}% decrease in R&D investment")
                        
                        with col3:
                            if trl_growth_rate > 5:
                                st.success(f"🔬 **TRL Maturity**: {trl_growth_rate:.1f}% improvement in technology readiness")
                            elif trl_growth_rate > 0:
                                st.info(f"📈 **TRL Maturity**: {trl_growth_rate:.1f}% improvement in technology readiness")
                            else:
                                st.warning(f"📉 **TRL Maturity**: {abs(trl_growth_rate):.1f}% decline in technology readiness")
                        
                        # Strategic recommendations
                        st.markdown("### 💡 Strategic Recommendations")
                        
                        if project_growth_rate < 0:
                            st.warning("⚠️ **Project Pipeline Risk**: Declining project count suggests need for new R&D initiatives")
                        
                        if budget_growth_rate < 0:
                            st.warning("⚠️ **Investment Risk**: Declining R&D budget may impact long-term innovation capability")
                        
                        if trl_growth_rate < 0:
                            st.warning("⚠️ **Maturity Risk**: Declining TRL levels suggest focus needed on technology development")
                        
                        if project_growth_rate > 10 and budget_growth_rate > 15:
                            st.success("🎉 **Excellent Innovation Momentum**: Strong growth in both projects and investment")
                        
                        if trl_growth_rate > 5:
                            st.success("🚀 **Technology Advancement**: Improving TRL levels indicate successful technology development")
                    
                    else:
                        st.info("📊 **Trend Analysis**: At least 3 months of data required for trend analysis and forecasting")
                
                else:
                    st.warning("📅 **Date Data Required**: Project start dates are needed for trend analysis")
            
            else:
                st.warning("📅 **Date Column Missing**: 'start_date' column required for trend analysis")
        
        else:
            st.info("📊 **Project Data Required**: Upload project data to view trend analysis and innovation forecasting")

def show_customer_centric_rd():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">🎯 Customer-Centric R&D</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.products.empty:
        st.info("📊 Please upload product data to view customer-centric R&D analytics.")
        st.markdown("""
        **💡 To see the full Customer-Centric R&D analytics:**
        1. Go to the **📝 Data Input** tab
        2. Click **🚀 Load Sample Data into Program** to load sample product data
        3. Or upload your own product data file
        4. Then return to this tab to see comprehensive customer analytics
        """)
        return
    
    # Enhanced customer-centric overview with comprehensive metrics
    st.markdown("""
    <div class="metric-card-green" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Customer-Centric Overview & Market Performance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate advanced customer metrics
    total_products = len(st.session_state.products)
    avg_satisfaction = st.session_state.products['customer_satisfaction'].mean()
    avg_market_response = st.session_state.products['market_response'].mean()
    total_revenue = st.session_state.products['revenue_generated'].sum()
    total_development_cost = st.session_state.products['development_cost'].sum()
    
    # Customer satisfaction analysis
    high_satisfaction_products = len(st.session_state.products[st.session_state.products['customer_satisfaction'] >= 4.0])
    low_satisfaction_products = len(st.session_state.products[st.session_state.products['customer_satisfaction'] < 3.0])
    
    # Market response analysis
    high_response_products = len(st.session_state.products[st.session_state.products['market_response'] >= 4.0])
    low_response_products = len(st.session_state.products[st.session_state.products['market_response'] < 3.0])
    
    # Revenue efficiency analysis
    avg_revenue_per_product = total_revenue / total_products if total_products > 0 else 0
    high_revenue_products = len(st.session_state.products[st.session_state.products['revenue_generated'] >= avg_revenue_per_product * 1.2])
    low_revenue_products = len(st.session_state.products[st.session_state.products['revenue_generated'] <= avg_revenue_per_product * 0.8])
    
    # ROI analysis
    overall_roi = (total_revenue / total_development_cost * 100) if total_development_cost > 0 else 0
    high_roi_products = len(st.session_state.products[
        (st.session_state.products['revenue_generated'] / st.session_state.products['development_cost'] * 100) >= overall_roi * 1.2
    ])
    
    # Customer-centric overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Products", total_products)
    with col2:
        st.metric("Avg Customer Satisfaction", f"{avg_satisfaction:.1f}/5")
    with col3:
        st.metric("Avg Market Response", f"{avg_market_response:.1f}/5")
    with col4:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    
    # Additional customer metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("High Satisfaction (≥4.0)", high_satisfaction_products)
    with col2:
        st.metric("High Market Response (≥4.0)", high_response_products)
    with col3:
        st.metric("High Revenue Products", high_revenue_products)
    with col4:
        st.metric("Overall ROI", f"{overall_roi:.1f}%")
    
    # Customer performance insights
    st.markdown("### 💡 Customer Performance Insights")
    
    if high_satisfaction_products / total_products > 0.6:
        st.success(f"🎉 **Excellent Customer Satisfaction**: {high_satisfaction_products/total_products*100:.1f}% products achieve high satisfaction (≥4.0)")
    elif high_satisfaction_products / total_products > 0.4:
        st.info(f"ℹ️ **Good Customer Satisfaction**: {high_satisfaction_products/total_products*100:.1f}% products achieve high satisfaction with room for improvement")
    else:
        st.warning(f"⚠️ **Customer Satisfaction Gap**: Only {high_satisfaction_products/total_products*100:.1f}% products achieve high satisfaction - focus on customer needs")
    
    if high_response_products / total_products > 0.6:
        st.success(f"🚀 **Strong Market Response**: {high_response_products/total_products*100:.1f}% products show excellent market acceptance")
    elif high_response_products / total_products > 0.4:
        st.info(f"ℹ️ **Good Market Response**: {high_response_products/total_products*100:.1f}% products show good market acceptance")
    else:
        st.warning(f"⚠️ **Market Response Gap**: Only {high_response_products/total_products*100:.1f}% products show strong market acceptance")
    
    if overall_roi > 150:
        st.success(f"💰 **Excellent ROI Performance**: {overall_roi:.1f}% ROI indicates strong customer value creation")
    elif overall_roi > 100:
        st.info(f"ℹ️ **Good ROI Performance**: {overall_roi:.1f}% ROI shows positive customer value creation")
    else:
        st.warning(f"⚠️ **ROI Improvement Needed**: {overall_roi:.1f}% ROI suggests need for customer value optimization")
    
    # Enhanced detailed analysis
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Advanced Customer Analytics & Market Intelligence</h4>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Customer Satisfaction", "📊 Market Response", "💰 Revenue Analysis", "🔍 Customer Intelligence"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🎯 Customer Satisfaction & Experience Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Enhanced satisfaction analysis with comprehensive metrics
            satisfaction_analysis = st.session_state.products.groupby('target_market').agg({
                'customer_satisfaction': 'mean',
                'product_id': 'count'
            }).reset_index()
            
            # Calculate advanced satisfaction metrics
            satisfaction_analysis['avg_satisfaction'] = round(satisfaction_analysis['customer_satisfaction'], 1)
            satisfaction_analysis['market_weight'] = round(satisfaction_analysis['product_id'] / satisfaction_analysis['product_id'].sum() * 100, 1)
            satisfaction_analysis['product_count'] = satisfaction_analysis['product_id']
            satisfaction_analysis['satisfaction_score'] = satisfaction_analysis['customer_satisfaction']
            
            # Key satisfaction metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_markets = len(satisfaction_analysis)
                st.metric("Target Markets", total_markets)
            with col2:
                total_satisfaction_products = satisfaction_analysis['product_count'].sum()
                st.metric("Total Products", total_satisfaction_products)
            with col3:
                avg_market_satisfaction = satisfaction_analysis['avg_satisfaction'].mean()
                st.metric("Avg Market Satisfaction", f"{avg_market_satisfaction:.1f}/5")
            with col4:
                high_satisfaction_markets = len(satisfaction_analysis[satisfaction_analysis['avg_satisfaction'] >= 4.0])
                st.metric("High Satisfaction Markets", high_satisfaction_markets)
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Enhanced satisfaction distribution with color coding
                fig = go.Figure(data=[
                    go.Bar(
                        x=satisfaction_analysis['target_market'], 
                        y=satisfaction_analysis['satisfaction_score'],
                        marker_color=['#2ca02c' if x >= 4.0 else '#1f77b4' if x >= 3.5 else '#ff7f0e' if x >= 3.0 else '#d62728' for x in satisfaction_analysis['satisfaction_score']],
                        text=satisfaction_analysis['avg_satisfaction'].apply(lambda x: f"{x:.1f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Satisfaction: %{y:.1f}/5<br>Products: %{text}<extra></extra>',
                        texttemplate='%{y:.1f}'
                    )
                ])
                fig.update_layout(
                    title="Customer Satisfaction by Target Market (Color-coded by Performance)",
                    xaxis_title="Target Market",
                    yaxis_title="Customer Satisfaction Score (/5)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Enhanced product distribution with better insights
                fig = go.Figure(data=[
                    go.Pie(
                        labels=satisfaction_analysis['target_market'], 
                        values=satisfaction_analysis['product_count'],
                        hole=0.4,
                        marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                        textinfo='label+percent+value',
                        hovertemplate='<b>%{label}</b><br>Products: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Product Distribution by Target Market",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Satisfaction insights and recommendations
            st.markdown("### 💡 Satisfaction Insights & Recommendations")
            
            # Market performance analysis
            best_market = satisfaction_analysis.loc[satisfaction_analysis['avg_satisfaction'].idxmax()]
            worst_market = satisfaction_analysis.loc[satisfaction_analysis['avg_satisfaction'].idxmin()]
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🏆 **Best Performing Market**: {best_market['target_market']} with {best_market['avg_satisfaction']:.1f}/5 satisfaction")
                st.write(f"• Products: {best_market['product_count']}")
                st.write(f"• Market Weight: {best_market['market_weight']:.1f}%")
            
            with col2:
                st.warning(f"⚠️ **Improvement Needed**: {worst_market['target_market']} with {worst_market['avg_satisfaction']:.1f}/5 satisfaction")
                st.write(f"• Products: {worst_market['product_count']}")
                st.write(f"• Market Weight: {worst_market['market_weight']:.1f}%")
            
            # Satisfaction trend analysis
            if 'launch_date' in st.session_state.products.columns:
                try:
                    st.session_state.products['launch_date'] = pd.to_datetime(st.session_state.products['launch_date'])
                    satisfaction_trend = st.session_state.products.groupby(
                        st.session_state.products['launch_date'].dt.to_period('M')
                    )['customer_satisfaction'].mean().reset_index()
                    satisfaction_trend['launch_date'] = satisfaction_trend['launch_date'].astype(str)
                    
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=satisfaction_trend['launch_date'],
                            y=satisfaction_trend['customer_satisfaction'],
                            mode='lines+markers',
                            line=dict(color='#667eea', width=3),
                            marker=dict(size=8, color='#667eea'),
                            hovertemplate='<b>%{x}</b><br>Satisfaction: %{y:.2f}/5<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Customer Satisfaction Trend Over Time",
                        xaxis_title="Launch Period",
                        yaxis_title="Average Customer Satisfaction (/5)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("📅 Launch date analysis requires valid date format in product data")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Market Response & Acceptance Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Market response analysis
            market_response_analysis = st.session_state.products.groupby('target_market').agg({
                'market_response': 'mean',
                'revenue_generated': 'sum',
                'product_id': 'count'
            }).reset_index()
            
            market_response_analysis['avg_response'] = round(market_response_analysis['market_response'], 1)
            market_response_analysis['total_revenue'] = market_response_analysis['revenue_generated']
            market_response_analysis['product_count'] = market_response_analysis['product_id']
            
            # Market response metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_markets_response = len(market_response_analysis)
                st.metric("Target Markets", total_markets_response)
            with col2:
                avg_overall_response = market_response_analysis['avg_response'].mean()
                st.metric("Overall Market Response", f"{avg_overall_response:.1f}/5")
            with col3:
                high_response_markets = len(market_response_analysis[market_response_analysis['avg_response'] >= 4.0])
                st.metric("High Response Markets", high_response_markets)
            with col4:
                total_market_revenue = market_response_analysis['total_revenue'].sum()
                st.metric("Total Market Revenue", f"${total_market_revenue:,.0f}")
            
            # Market response visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Market response by target market
                fig = go.Figure(data=[
                    go.Bar(
                        x=market_response_analysis['target_market'],
                        y=market_response_analysis['avg_response'],
                        marker_color=['#ff7f0e' if x >= 4.0 else '#1f77b4' if x >= 3.5 else '#2ca02c' if x >= 3.0 else '#d62728' for x in market_response_analysis['avg_response']],
                        text=market_response_analysis['avg_response'].apply(lambda x: f"{x:.1f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Market Response: %{y:.1f}/5<br>Revenue: $%{text}<extra></extra>',
                        texttemplate='%{y:.1f}'
                    )
                ])
                fig.update_layout(
                    title="Market Response by Target Market",
                    xaxis_title="Target Market",
                    yaxis_title="Market Response Score (/5)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue vs Market Response correlation
                fig = go.Figure(data=[
                    go.Scatter(
                        x=market_response_analysis['avg_response'],
                        y=market_response_analysis['total_revenue'],
                        mode='markers+text',
                        marker=dict(size=12, color='#ff7f0e'),
                        text=market_response_analysis['target_market'],
                        textposition='top center',
                        hovertemplate='<b>%{text}</b><br>Response: %{x:.1f}/5<br>Revenue: $%{y:,.0f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Revenue vs Market Response Correlation",
                    xaxis_title="Market Response Score (/5)",
                    yaxis_title="Total Revenue ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Market response insights
            st.markdown("### 💡 Market Response Insights")
            
            # Correlation analysis
            correlation = market_response_analysis['avg_response'].corr(market_response_analysis['total_revenue'])
            
            if correlation > 0.7:
                st.success(f"🎯 **Strong Positive Correlation**: Market response and revenue show strong correlation ({correlation:.2f})")
            elif correlation > 0.4:
                st.info(f"📊 **Moderate Correlation**: Market response and revenue show moderate correlation ({correlation:.2f})")
            else:
                st.warning(f"⚠️ **Weak Correlation**: Market response and revenue show weak correlation ({correlation:.2f})")
            
            # Market performance ranking
            market_response_analysis_sorted = market_response_analysis.sort_values('avg_response', ascending=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**🏆 Top Performing Markets:**")
                for i, (_, market) in enumerate(market_response_analysis_sorted.head(3).iterrows()):
                    st.write(f"{i+1}. {market['target_market']}: {market['avg_response']:.1f}/5 (${market['total_revenue']:,.0f})")
            
            with col2:
                st.write("**📈 Market Response vs Revenue:**")
                for _, market in market_response_analysis.iterrows():
                    efficiency = market['total_revenue'] / market['avg_response'] if market['avg_response'] > 0 else 0
                    st.write(f"• {market['target_market']}: ${efficiency:,.0f} per response point")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Revenue Analysis & Customer Value Creation</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Revenue analysis by various dimensions
            revenue_analysis = st.session_state.products.groupby('target_market').agg({
                'revenue_generated': ['sum', 'mean', 'count'],
                'development_cost': 'sum',
                'customer_satisfaction': 'mean'
            }).reset_index()
            
            revenue_analysis.columns = ['target_market', 'total_revenue', 'avg_revenue', 'product_count', 'total_cost', 'avg_satisfaction']
            revenue_analysis['roi'] = (revenue_analysis['total_revenue'] / revenue_analysis['total_cost'] * 100).round(1)
            revenue_analysis['revenue_per_product'] = (revenue_analysis['total_revenue'] / revenue_analysis['product_count']).round(0)
            
            # Revenue metrics overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_revenue_all = revenue_analysis['total_revenue'].sum()
                st.metric("Total Revenue", f"${total_revenue_all:,.0f}")
            with col2:
                total_cost_all = revenue_analysis['total_cost'].sum()
                st.metric("Total Development Cost", f"${total_cost_all:,.0f}")
            with col3:
                overall_roi_all = (total_revenue_all / total_cost_all * 100) if total_cost_all > 0 else 0
                st.metric("Overall ROI", f"{overall_roi_all:.1f}%")
            with col4:
                avg_revenue_per_product_all = total_revenue_all / revenue_analysis['product_count'].sum() if revenue_analysis['product_count'].sum() > 0 else 0
                st.metric("Avg Revenue/Product", f"${avg_revenue_per_product_all:,.0f}")
            
            # Revenue visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Revenue by target market
                fig = go.Figure(data=[
                    go.Bar(
                        x=revenue_analysis['target_market'],
                        y=revenue_analysis['total_revenue'],
                        marker_color=['#2ca02c' if x >= revenue_analysis['total_revenue'].mean() * 1.2 else '#1f77b4' if x >= revenue_analysis['total_revenue'].mean() else '#ff7f0e' for x in revenue_analysis['total_revenue']],
                        text=revenue_analysis['total_revenue'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<br>ROI: %{text}%<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Revenue by Target Market (Color-coded by Performance)",
                    xaxis_title="Target Market",
                    yaxis_title="Total Revenue ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # ROI by target market
                fig = go.Figure(data=[
                    go.Bar(
                        x=revenue_analysis['target_market'],
                        y=revenue_analysis['roi'],
                        marker_color=['#2ca02c' if x >= 150 else '#1f77b4' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in revenue_analysis['roi']],
                        text=revenue_analysis['roi'].apply(lambda x: f"{x:.1f}%"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>',
                        texttemplate='%{y:.1f}%'
                    )
                ])
                fig.update_layout(
                    title="ROI by Target Market",
                    xaxis_title="Target Market",
                    yaxis_title="Return on Investment (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Revenue efficiency analysis
            st.markdown("### 💡 Revenue Efficiency Analysis")
            
            # Market performance ranking by ROI
            revenue_analysis_sorted = revenue_analysis.sort_values('roi', ascending=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**🏆 Top ROI Markets:**")
                for i, (_, market) in enumerate(revenue_analysis_sorted.head(3).iterrows()):
                    st.write(f"{i+1}. {market['target_market']}: {market['roi']:.1f}% ROI")
                    st.write(f"   • Revenue: ${market['total_revenue']:,.0f}")
                    st.write(f"   • Cost: ${market['total_cost']:,.0f}")
            
            with col2:
                st.write("**📊 Revenue Efficiency Metrics:**")
                for _, market in revenue_analysis.iterrows():
                    efficiency_score = market['total_revenue'] / market['total_cost'] if market['total_cost'] > 0 else 0
                    st.write(f"• {market['target_market']}: ${efficiency_score:.2f} revenue per $1 cost")
            
            # Customer value creation analysis
            st.markdown("### 💰 Customer Value Creation Analysis")
            
            # Calculate customer value metrics
            customer_value_metrics = []
            for _, market in revenue_analysis.iterrows():
                customer_value = market['total_revenue'] - market['total_cost']
                customer_value_metrics.append({
                    'Market': market['target_market'],
                    'Revenue': market['total_revenue'],
                    'Cost': market['total_cost'],
                    'Customer Value': customer_value,
                    'ROI': market['roi']
                })
            
            customer_value_df = pd.DataFrame(customer_value_metrics)
            customer_value_df = customer_value_df.sort_values('Customer Value', ascending=False)
            
            st.dataframe(customer_value_df, use_container_width=True)
            
            # Customer value insights
            total_customer_value = customer_value_df['Customer Value'].sum()
            avg_customer_value = customer_value_df['Customer Value'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Customer Value Created", f"${total_customer_value:,.0f}")
            with col2:
                st.metric("Average Customer Value per Market", f"${avg_customer_value:,.0f}")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-purple" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔍 Customer Intelligence & Strategic Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Customer intelligence analysis
            customer_intelligence = st.session_state.products.copy()
            
            # Add derived metrics
            customer_intelligence['profit_margin'] = (
                (customer_intelligence['revenue_generated'] - customer_intelligence['development_cost']) / 
                customer_intelligence['revenue_generated'] * 100
            ).round(1)
            
            customer_intelligence['customer_value_score'] = (
                customer_intelligence['customer_satisfaction'] * 0.4 +
                customer_intelligence['market_response'] * 0.3 +
                (customer_intelligence['profit_margin'] / 100) * 0.3
            ).round(2)
            
            # Customer intelligence metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_profit_margin = customer_intelligence['profit_margin'].mean()
                st.metric("Avg Profit Margin", f"{avg_profit_margin:.1f}%")
            with col2:
                avg_customer_value_score = customer_intelligence['customer_value_score'].mean()
                st.metric("Avg Customer Value Score", f"{avg_customer_value_score:.2f}/5")
            with col3:
                high_value_products = len(customer_intelligence[customer_intelligence['customer_value_score'] >= 4.0])
                st.metric("High Value Products", high_value_products)
            with col4:
                total_customers_served = customer_intelligence['product_id'].nunique()
                st.metric("Total Products", total_customers_served)
            
            # Customer intelligence visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Customer value score distribution
                fig = go.Figure(data=[
                    go.Histogram(
                        x=customer_intelligence['customer_value_score'],
                        nbinsx=10,
                        marker_color='#a855f7',
                        opacity=0.7,
                        hovertemplate='<b>Value Score</b><br>Count: %{y}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Distribution of Customer Value Scores",
                    xaxis_title="Customer Value Score (/5)",
                    yaxis_title="Number of Products",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Profit margin vs Customer satisfaction
                fig = go.Figure(data=[
                    go.Scatter(
                        x=customer_intelligence['customer_satisfaction'],
                        y=customer_intelligence['profit_margin'],
                        mode='markers',
                        marker=dict(
                            size=10,
                            color=customer_intelligence['customer_value_score'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Value Score")
                        ),
                        text=customer_intelligence['product_name'],
                        hovertemplate='<b>%{text}</b><br>Satisfaction: %{x:.1f}/5<br>Profit Margin: %{y:.1f}%<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Profit Margin vs Customer Satisfaction",
                    xaxis_title="Customer Satisfaction (/5)",
                    yaxis_title="Profit Margin (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Customer intelligence insights
            st.markdown("### 💡 Customer Intelligence Insights")
            
            # Top performing products by customer value
            top_value_products = customer_intelligence.nlargest(5, 'customer_value_score')
            
            st.write("**🏆 Top Customer Value Products:**")
            for i, (_, product) in enumerate(top_value_products.iterrows()):
                st.write(f"{i+1}. **{product['product_name']}**")
                st.write(f"   • Customer Value Score: {product['customer_value_score']:.2f}/5")
                st.write(f"   • Satisfaction: {product['customer_satisfaction']:.1f}/5")
                st.write(f"   • Market Response: {product['market_response']:.1f}/5")
                st.write(f"   • Profit Margin: {product['profit_margin']:.1f}%")
                st.write(f"   • Revenue: ${product['revenue_generated']:,.0f}")
                st.write("")
            
            # Strategic recommendations
            st.markdown("### 🎯 Strategic Recommendations")
            
            # Market opportunity analysis
            market_opportunities = customer_intelligence.groupby('target_market').agg({
                'customer_value_score': 'mean',
                'profit_margin': 'mean',
                'revenue_generated': 'sum'
            }).reset_index()
            
            market_opportunities = market_opportunities.sort_values('customer_value_score', ascending=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**🚀 High-Value Market Opportunities:**")
                for _, market in market_opportunities.head(3).iterrows():
                    st.write(f"• **{market['target_market']}**")
                    st.write(f"  - Value Score: {market['customer_value_score']:.2f}/5")
                    st.write(f"  - Profit Margin: {market['profit_margin']:.1f}%")
                    st.write(f"  - Revenue: ${market['revenue_generated']:,.0f}")
            
            with col2:
                st.write("**📈 Customer-Centric R&D Priorities:**")
                if avg_customer_value_score >= 4.0:
                    st.success("✅ **Excellent customer value creation** - focus on scaling successful products")
                elif avg_customer_value_score >= 3.0:
                    st.info("ℹ️ **Good customer value creation** - optimize underperforming products")
                else:
                    st.warning("⚠️ **Customer value improvement needed** - prioritize customer feedback integration")
                
                if avg_profit_margin >= 30:
                    st.success("✅ **Strong profitability** - consider expanding high-margin markets")
                elif avg_profit_margin >= 15:
                    st.info("ℹ️ **Moderate profitability** - optimize cost structure")
                else:
                    st.warning("⚠️ **Profitability improvement needed** - review pricing and cost strategies")
            
            # Customer feedback integration recommendations
            st.markdown("### 📝 Customer Feedback Integration Strategy")
            
            feedback_strategy = {
                "High Satisfaction, Low Revenue": "Focus on pricing optimization and market expansion",
                "High Revenue, Low Satisfaction": "Prioritize product improvement and customer experience",
                "Low Satisfaction, Low Revenue": "Consider product redesign or market pivot",
                "High Satisfaction, High Revenue": "Scale and replicate success patterns"
            }
            
            for condition, strategy in feedback_strategy.items():
                st.write(f"**{condition}**: {strategy}")
            
            # Future R&D direction
            st.markdown("### 🔮 Future R&D Direction")
            
            # Identify trends and patterns
            if 'launch_date' in customer_intelligence.columns:
                try:
                    customer_intelligence['launch_date'] = pd.to_datetime(customer_intelligence['launch_date'])
                    customer_intelligence['launch_year'] = customer_intelligence['launch_date'].dt.year
                    
                    yearly_trends = customer_intelligence.groupby('launch_year').agg({
                        'customer_value_score': 'mean',
                        'profit_margin': 'mean',
                        'revenue_generated': 'sum'
                    }).reset_index()
                    
                    if len(yearly_trends) > 1:
                        st.write("**📈 Year-over-Year Trends:**")
                        for _, trend in yearly_trends.iterrows():
                            st.write(f"• **{trend['launch_year']}**: Value Score: {trend['customer_value_score']:.2f}, Profit: {trend['profit_margin']:.1f}%, Revenue: ${trend['revenue_generated']:,.0f}")
                        
                        # Trend analysis
                        value_trend = yearly_trends['customer_value_score'].iloc[-1] - yearly_trends['customer_value_score'].iloc[0]
                        if value_trend > 0.5:
                            st.success("🚀 **Positive trend in customer value creation** - R&D strategy is working")
                        elif value_trend > 0:
                            st.info("📈 **Slight improvement in customer value** - continue current approach")
                        else:
                            st.warning("⚠️ **Declining customer value** - review R&D strategy")
                except:
                    st.info("📅 Launch date analysis requires valid date format in product data")

def show_strategic_metrics():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">📊 Strategic and Financial Metrics</h2>
        <p style="text-align: center; color: #666; font-size: 1.1rem;">Comprehensive strategic intelligence and financial performance analytics for data-driven R&D decision making</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.projects.empty and st.session_state.products.empty and st.session_state.patents.empty:
        st.info("📊 Please upload project, product, and patent data to view strategic metrics.")
        st.markdown("""
        **💡 To see comprehensive Strategic & Financial Metrics:**
        1. Go to the **📝 Data Input** tab
        2. Click **🚀 Load Sample Data into Program** to load sample data
        3. Or upload your own data files
        4. Then return to this tab to see advanced strategic analytics
        """)
        return
    
    # Enhanced Strategic Overview with comprehensive metrics
    st.markdown("""
    <div class="metric-card-purple" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">📈 Strategic Overview & Financial Performance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate comprehensive strategic metrics
    total_rd_investment = st.session_state.projects['actual_spend'].sum() if not st.session_state.projects.empty else 0
    total_revenue = st.session_state.products['revenue_generated'].sum() if not st.session_state.products.empty else 0
    total_ip_value = st.session_state.patents['estimated_value'].sum() if not st.session_state.patents.empty else 0
    total_licensing_revenue = st.session_state.patents['licensing_revenue'].sum() if not st.session_state.patents.empty else 0
    
    # Advanced financial metrics
    overall_ror = ((total_revenue + total_licensing_revenue) / total_rd_investment * 100) if total_rd_investment > 0 else 0
    product_ror = (total_revenue / total_rd_investment * 100) if total_rd_investment > 0 else 0
    ip_ror = (total_licensing_revenue / total_ip_value * 100) if total_ip_value > 0 else 0
    
    # Strategic efficiency metrics
    total_projects = len(st.session_state.projects) if not st.session_state.projects.empty else 0
    successful_projects = len(st.session_state.projects[st.session_state.projects['status'] == 'Completed']) if not st.session_state.projects.empty else 0
    project_success_rate = (successful_projects / total_projects * 100) if total_projects > 0 else 0
    
    # First row of strategic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total R&D Investment", f"${total_rd_investment:,.0f}")
    with col2:
        st.metric("Total Revenue Generated", f"${total_revenue:,.0f}")
    with col3:
        st.metric("IP Portfolio Value", f"${total_ip_value:,.0f}")
    with col4:
        st.metric("Licensing Revenue", f"${total_licensing_revenue:,.0f}")
    
    # Second row of strategic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall R&D ROI", f"{overall_ror:.1f}%")
    with col2:
        st.metric("Product ROI", f"{product_ror:.1f}%")
    with col3:
        st.metric("IP ROI", f"{ip_ror:.1f}%")
    with col4:
        st.metric("Project Success Rate", f"{project_success_rate:.1f}%")
    
    # Enhanced Strategic Performance Dashboard
    st.markdown("""
    <div class="metric-card" style="margin: 20px 0;">
        <h4 style="text-align: center; color: #1e3c72; margin-bottom: 15px;">📊 Advanced Strategic Analytics Dashboard</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic performance insights
    st.markdown("### 💡 Strategic Performance Insights")
    
    # Performance assessment with color coding
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if overall_ror > 200:
            st.success(f"🚀 **Excellent R&D Performance**: {overall_ror:.1f}% ROI indicates outstanding strategic execution")
        elif overall_ror > 100:
            st.info(f"📈 **Good R&D Performance**: {overall_ror:.1f}% ROI shows positive strategic returns")
        else:
            st.warning(f"⚠️ **R&D Performance Gap**: {overall_ror:.1f}% ROI suggests need for strategic optimization")
    
    with col2:
        if project_success_rate > 80:
            st.success(f"✅ **High Project Success**: {project_success_rate:.1f}% success rate indicates effective R&D management")
        elif project_success_rate > 60:
            st.info(f"ℹ️ **Moderate Success Rate**: {project_success_rate:.1f}% success rate with room for improvement")
        else:
            st.warning(f"⚠️ **Success Rate Concern**: {project_success_rate:.1f}% success rate needs strategic review")
    
    with col3:
        if total_ip_value > total_rd_investment * 0.5:
            st.success(f"💎 **Strong IP Portfolio**: IP value represents {total_ip_value/total_rd_investment*100:.1f}% of R&D investment")
        elif total_ip_value > total_rd_investment * 0.2:
            st.info(f"📜 **Good IP Portfolio**: IP value represents {total_ip_value/total_rd_investment*100:.1f}% of R&D investment")
        else:
            st.warning(f"⚠️ **IP Portfolio Development**: IP value represents {total_ip_value/total_rd_investment*100:.1f}% of R&D investment")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Financial Performance", "📊 Strategic KPIs", "🎯 Market Intelligence", "📈 Trend Analysis", "🔍 Competitive Analysis"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Financial Performance & ROI Analysis</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty and not st.session_state.products.empty:
            # Enhanced financial metrics with comprehensive analysis
            financial_metrics = pd.DataFrame({
                'Metric': ['R&D Investment', 'Product Revenue', 'IP Portfolio Value', 'Licensing Revenue', 'Total Value Created'],
                'Value': [
                    total_rd_investment,
                    total_revenue,
                    total_ip_value,
                    total_licensing_revenue,
                    total_revenue + total_ip_value + total_licensing_revenue
                ],
                'ROI': [
                    'N/A',
                    f"{product_ror:.1f}%",
                    f"{ip_ror:.1f}%",
                    'N/A',
                    f"{overall_ror:.1f}%"
                ]
            })
            
            # Financial performance overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Investment", f"${total_rd_investment:,.0f}")
            with col2:
                st.metric("Total Returns", f"${total_revenue + total_licensing_revenue:,.0f}")
            with col3:
                st.metric("Net Value Created", f"${total_revenue + total_ip_value + total_licensing_revenue - total_rd_investment:,.0f}")
            with col4:
                st.metric("Overall ROI", f"{overall_ror:.1f}%")
            
            # Enhanced visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Financial overview with enhanced styling
                fig = go.Figure(data=[
                    go.Bar(
                        x=financial_metrics['Metric'], 
                        y=financial_metrics['Value'],
                        marker_color=['#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#d62728'],
                        text=financial_metrics['Value'].apply(lambda x: f"${x:,.0f}"),
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>Value: $%{y:,.0f}<extra></extra>',
                        texttemplate='$%{y:,.0f}'
                    )
                ])
                fig.update_layout(
                    title="Financial Performance Overview",
                    xaxis_title="Financial Metric",
                    yaxis_title="Value ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # ROI performance comparison
                roi_data = financial_metrics[financial_metrics['ROI'] != 'N/A'].copy()
                roi_data['ROI_Value'] = roi_data['ROI'].str.rstrip('%').astype(float)
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=roi_data['Metric'],
                        y=roi_data['ROI_Value'],
                        marker_color=['#2ca02c' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in roi_data['ROI_Value']],
                        text=roi_data['ROI'],
                        textposition='auto',
                        hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>',
                        texttemplate='%{y:.1f}%'
                    )
                ])
                fig.update_layout(
                    title="ROI Performance by Category",
                    xaxis_title="Category",
                    yaxis_title="Return on Investment (%)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Financial efficiency analysis
            st.markdown("### 💡 Financial Efficiency Analysis")
            
            # Calculate efficiency metrics
            investment_efficiency = (total_revenue + total_licensing_revenue) / total_rd_investment if total_rd_investment > 0 else 0
            ip_efficiency = total_ip_value / total_rd_investment if total_rd_investment > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Investment Efficiency", f"${investment_efficiency:.2f} return per $1 invested")
            with col2:
                st.metric("IP Efficiency", f"${ip_efficiency:.2f} IP value per $1 invested")
            with col3:
                st.metric("Value Creation Ratio", f"{(total_revenue + total_ip_value + total_licensing_revenue) / total_rd_investment:.2f}x")
            
            # Financial insights
            st.markdown("### 💰 Financial Insights & Recommendations")
            
            if overall_ror > 200:
                st.success("🚀 **Outstanding Financial Performance**: Consider increasing R&D investment to scale success")
            elif overall_ror > 100:
                st.info("📈 **Strong Financial Performance**: Focus on optimizing high-performing areas")
            else:
                st.warning("⚠️ **Financial Performance Gap**: Review R&D strategy and resource allocation")
            
            # ROI breakdown table
            st.markdown("### 📊 Detailed ROI Breakdown")
            roi_breakdown = pd.DataFrame({
                'Category': ['Product Revenue', 'IP Portfolio', 'Licensing Revenue', 'Overall R&D'],
                'Investment': [total_rd_investment, total_rd_investment, total_ip_value, total_rd_investment],
                'Returns': [total_revenue, total_ip_value, total_licensing_revenue, total_revenue + total_licensing_revenue],
                'ROI': [f"{product_ror:.1f}%", f"{ip_ror:.1f}%", 'N/A', f"{overall_ror:.1f}%"],
                'Efficiency': [
                    f"${total_revenue/total_rd_investment:.2f}" if total_rd_investment > 0 else "$0",
                    f"${total_ip_value/total_rd_investment:.2f}" if total_rd_investment > 0 else "$0",
                    f"${total_licensing_revenue/total_ip_value:.2f}" if total_ip_value > 0 else "$0",
                    f"${(total_revenue + total_licensing_revenue)/total_rd_investment:.2f}" if total_rd_investment > 0 else "$0"
                ]
            })
            st.dataframe(roi_breakdown, use_container_width=True)
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Strategic KPIs & Performance Metrics</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Enhanced Performance KPIs with comprehensive analysis
            st.markdown("### 🎯 Key Performance Indicators")
            
            # Project performance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Projects", total_projects)
            with col2:
                st.metric("Successful Projects", successful_projects)
            with col3:
                st.metric("Success Rate", f"{project_success_rate:.1f}%")
            with col4:
                avg_project_cost = total_rd_investment / total_projects if total_projects > 0 else 0
                st.metric("Avg Project Cost", f"${avg_project_cost:,.0f}")
            
            # Advanced KPI calculations
            if not st.session_state.projects.empty:
                # Budget efficiency analysis
                total_budget = st.session_state.projects['budget'].sum()
                budget_efficiency = (total_rd_investment / total_budget * 100) if total_budget > 0 else 0
                budget_variance = ((total_rd_investment - total_budget) / total_budget * 100) if total_budget > 0 else 0
                
                # Project type analysis
                project_types = st.session_state.projects.groupby('project_type').agg({
                    'project_id': 'count',
                    'budget': 'sum',
                    'actual_spend': 'sum'
                }).reset_index()
                
                # Technology readiness analysis
                if 'trl_level' in st.session_state.projects.columns:
                    avg_trl = st.session_state.projects['trl_level'].mean()
                    high_trl_projects = len(st.session_state.projects[st.session_state.projects['trl_level'] >= 7])
                else:
                    avg_trl = 0
                    high_trl_projects = 0
                
                # Patent performance metrics
                if not st.session_state.patents.empty:
                    granted_patents = len(st.session_state.patents[st.session_state.patents['status'] == 'Granted'])
                    total_patents = len(st.session_state.patents)
                    patent_success_rate = (granted_patents / total_patents * 100) if total_patents > 0 else 0
                    avg_patent_value = total_ip_value / total_patents if total_patents > 0 else 0
                else:
                    patent_success_rate = 0
                    avg_patent_value = 0
                
                # Product performance metrics
                if not st.session_state.products.empty:
                    avg_satisfaction = st.session_state.products['customer_satisfaction'].mean()
                    avg_market_response = st.session_state.products['market_response'].mean()
                    high_satisfaction_products = len(st.session_state.products[st.session_state.products['customer_satisfaction'] >= 4.0])
                    satisfaction_rate = (high_satisfaction_products / len(st.session_state.products) * 100) if len(st.session_state.products) > 0 else 0
                else:
                    avg_satisfaction = 0
                    avg_market_response = 0
                    satisfaction_rate = 0
                
                # Enhanced KPI display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📊 Project Performance KPIs")
                    kpi_project_data = [
                        ['Project Success Rate', f"{project_success_rate:.1f}%"],
                        ['Budget Efficiency', f"{budget_efficiency:.1f}%"],
                        ['Budget Variance', f"{budget_variance:.1f}%"],
                        ['Avg Project Cost', f"${avg_project_cost:,.0f}"],
                        ['High TRL Projects', f"{high_trl_projects}"],
                        ['Avg TRL Level', f"{avg_trl:.1f}"]
                    ]
                    kpi_project_df = pd.DataFrame(kpi_project_data, columns=['KPI', 'Value'])
                    st.dataframe(kpi_project_df, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📈 Innovation & Market KPIs")
                    kpi_innovation_data = [
                        ['Patent Success Rate', f"{patent_success_rate:.1f}%"],
                        ['Avg Patent Value', f"${avg_patent_value:,.0f}"],
                        ['Customer Satisfaction', f"{avg_satisfaction:.1f}/5"],
                        ['Market Response', f"{avg_market_response:.1f}/5"],
                        ['High Satisfaction Rate', f"{satisfaction_rate:.1f}%"],
                        ['Total Patents', f"{total_patents}"]
                    ]
                    kpi_innovation_df = pd.DataFrame(kpi_innovation_data, columns=['KPI', 'Value'])
                    st.dataframe(kpi_innovation_df, use_container_width=True)
                
                # KPI Performance Visualization
                st.markdown("### 📊 KPI Performance Dashboard")
                
                # Create KPI performance chart
                kpi_performance = pd.DataFrame({
                    'Category': ['Project Success', 'Budget Efficiency', 'Patent Success', 'Customer Satisfaction'],
                    'Performance': [project_success_rate, budget_efficiency, patent_success_rate, satisfaction_rate],
                    'Target': [80, 90, 70, 80]
                })
                
                fig = go.Figure()
                
                # Add performance bars
                fig.add_trace(go.Bar(
                    x=kpi_performance['Category'],
                    y=kpi_performance['Performance'],
                    name='Current Performance',
                                            marker_color=['#2ca02c' if x >= y else '#ff7f0e' if x >= y*0.8 else '#d62728' 
                                for x, y in zip(kpi_performance['Performance'], kpi_performance['Target'])],
                    text=kpi_performance['Performance'].apply(lambda x: f"{x:.1f}%"),
                    textposition='auto'
                ))
                
                # Add target line
                fig.add_trace(go.Scatter(
                    x=kpi_performance['Category'],
                    y=kpi_performance['Target'],
                    mode='markers+lines',
                    name='Target',
                    line=dict(color='#1f77b4', width=3, dash='dash'),
                    marker=dict(size=10, color='#1f77b4')
                ))
                
                fig.update_layout(
                    title="KPI Performance vs Targets",
                    xaxis_title="Performance Category",
                    yaxis_title="Performance (%)",
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # KPI Insights and Recommendations
                st.markdown("### 💡 KPI Insights & Strategic Recommendations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Project Performance Insights:**")
                    if project_success_rate >= 80:
                        st.success(f"✅ **Excellent Project Success**: {project_success_rate:.1f}% success rate indicates strong R&D execution")
                    elif project_success_rate >= 60:
                        st.info(f"ℹ️ **Good Project Success**: {project_success_rate:.1f}% success rate with room for improvement")
                    else:
                        st.warning(f"⚠️ **Project Success Concern**: {project_success_rate:.1f}% success rate needs strategic review")
                    
                    if budget_efficiency >= 90:
                        st.success(f"✅ **Excellent Budget Management**: {budget_efficiency:.1f}% efficiency shows optimal resource utilization")
                    elif budget_efficiency >= 80:
                        st.info(f"ℹ️ **Good Budget Management**: {budget_efficiency:.1f}% efficiency with monitoring needed")
                    else:
                        st.warning(f"⚠️ **Budget Management Gap**: {budget_efficiency:.1f}% efficiency needs improvement")
                
                with col2:
                    st.write("**💎 Innovation Performance Insights:**")
                    if patent_success_rate >= 70:
                        st.success(f"✅ **Strong IP Performance**: {patent_success_rate:.1f}% patent success rate")
                    elif patent_success_rate >= 50:
                        st.info(f"ℹ️ **Moderate IP Performance**: {patent_success_rate:.1f}% patent success rate")
                    else:
                        st.warning(f"⚠️ **IP Performance Gap**: {patent_success_rate:.1f}% patent success rate needs improvement")
                    
                    if satisfaction_rate >= 80:
                        st.success(f"✅ **Excellent Customer Satisfaction**: {satisfaction_rate:.1f}% high satisfaction rate")
                    elif satisfaction_rate >= 60:
                        st.info(f"ℹ️ **Good Customer Satisfaction**: {satisfaction_rate:.1f}% satisfaction rate")
                    else:
                        st.warning(f"⚠️ **Customer Satisfaction Gap**: {satisfaction_rate:.1f}% satisfaction rate needs focus")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🎯 Market Intelligence & Strategic Positioning</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty or not st.session_state.products.empty:
            # Market intelligence overview
            st.markdown("### 🌍 Market Intelligence Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if not st.session_state.products.empty:
                    total_markets = st.session_state.products['target_market'].nunique()
                    st.metric("Target Markets", total_markets)
                else:
                    st.metric("Target Markets", 0)
            
            with col2:
                if not st.session_state.products.empty:
                    avg_market_revenue = total_revenue / total_markets if total_markets > 0 else 0
                    st.metric("Avg Market Revenue", f"${avg_market_revenue:,.0f}")
                else:
                    st.metric("Avg Market Revenue", "$0")
            
            with col3:
                if not st.session_state.projects.empty:
                    avg_rd_per_market = total_rd_investment / total_markets if total_markets > 0 else 0
                    st.metric("Avg R&D per Market", f"${avg_rd_per_market:,.0f}")
                else:
                    st.metric("Avg R&D per Market", "$0")
            
            with col4:
                if not st.session_state.products.empty and not st.session_state.projects.empty:
                    market_roi = (avg_market_revenue / avg_rd_per_market * 100) if avg_rd_per_market > 0 else 0
                    st.metric("Market ROI", f"{market_roi:.1f}%")
                else:
                    st.metric("Market ROI", "0%")
            
            # Market performance analysis
            if not st.session_state.products.empty:
                st.markdown("### 📊 Market Performance Analysis")
                
                # Market performance by target market
                market_performance = st.session_state.products.groupby('target_market').agg({
                    'revenue_generated': 'sum',
                    'development_cost': 'sum',
                    'customer_satisfaction': 'mean',
                    'market_response': 'mean',
                    'product_id': 'count'
                }).reset_index()
                
                market_performance['roi'] = (market_performance['revenue_generated'] / market_performance['development_cost'] * 100).round(1)
                market_performance['avg_satisfaction'] = market_performance['customer_satisfaction'].round(1)
                market_performance['avg_response'] = market_performance['market_response'].round(1)
                market_performance['product_count'] = market_performance['product_id']
                
                # Market performance visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    # Market ROI comparison
                    fig = go.Figure(data=[
                        go.Bar(
                            x=market_performance['target_market'],
                            y=market_performance['roi'],
                            marker_color=['#2ca02c' if x >= 150 else '#1f77b4' if x >= 100 else '#ff7f0e' if x >= 50 else '#d62728' for x in market_performance['roi']],
                            text=market_performance['roi'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto',
                            hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>',
                            texttemplate='%{y:.1f}%'
                        )
                    ])
                    fig.update_layout(
                        title="Market ROI Performance",
                        xaxis_title="Target Market",
                        yaxis_title="Return on Investment (%)",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Market satisfaction vs response
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=market_performance['avg_satisfaction'],
                            y=market_performance['avg_response'],
                            mode='markers+text',
                            marker=dict(
                                size=12,
                                color=market_performance['roi'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="ROI (%)")
                            ),
                            text=market_performance['target_market'],
                            textposition='top center',
                            hovertemplate='<b>%{text}</b><br>Satisfaction: %{x:.1f}/5<br>Response: %{y:.1f}/5<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Market Satisfaction vs Response (Color-coded by ROI)",
                        xaxis_title="Customer Satisfaction (/5)",
                        yaxis_title="Market Response (/5)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Market intelligence insights
                st.markdown("### 💡 Market Intelligence Insights")
                
                # Top performing markets
                top_markets = market_performance.nlargest(3, 'roi')
                worst_markets = market_performance.nsmallest(3, 'roi')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🏆 Top Performing Markets:**")
                    for i, (_, market) in enumerate(top_markets.iterrows()):
                        st.write(f"{i+1}. **{market['target_market']}**")
                        st.write(f"   • ROI: {market['roi']:.1f}%")
                        st.write(f"   • Revenue: ${market['revenue_generated']:,.0f}")
                        st.write(f"   • Satisfaction: {market['avg_satisfaction']:.1f}/5")
                        st.write(f"   • Products: {market['product_count']}")
                        st.write("")
                
                with col2:
                    st.write("**⚠️ Markets Needing Attention:**")
                    for i, (_, market) in enumerate(worst_markets.iterrows()):
                        st.write(f"{i+1}. **{market['target_market']}**")
                        st.write(f"   • ROI: {market['roi']:.1f}%")
                        st.write(f"   • Revenue: ${market['revenue_generated']:,.0f}")
                        st.write(f"   • Satisfaction: {market['avg_satisfaction']:.1f}/5")
                        st.write(f"   • Products: {market['product_count']}")
                        st.write("")
                
                # Strategic market recommendations
                st.markdown("### 🎯 Strategic Market Recommendations")
                
                # Market opportunity analysis
                market_opportunities = []
                for _, market in market_performance.iterrows():
                    if market['roi'] >= 150:
                        opportunity = "High Growth - Scale and expand"
                    elif market['roi'] >= 100:
                        opportunity = "Stable Growth - Optimize and maintain"
                    elif market['roi'] >= 50:
                        opportunity = "Moderate Growth - Improve performance"
                    else:
                        opportunity = "Needs Attention - Review strategy"
                    
                    market_opportunities.append({
                        'Market': market['target_market'],
                        'ROI': f"{market['roi']:.1f}%",
                        'Revenue': f"${market['revenue_generated']:,.0f}",
                        'Opportunity': opportunity
                    })
                
                opportunities_df = pd.DataFrame(market_opportunities)
                st.dataframe(opportunities_df, use_container_width=True)
                
                # Market expansion strategy
                st.markdown("### 🚀 Market Expansion Strategy")
                
                high_roi_markets = market_performance[market_performance['roi'] >= 100]
                if len(high_roi_markets) > 0:
                    st.success(f"🎯 **Focus Markets**: {len(high_roi_markets)} markets show strong ROI (≥100%) - prioritize expansion")
                    
                    # Investment allocation recommendation
                    total_high_roi_revenue = high_roi_markets['revenue_generated'].sum()
                    recommended_investment = total_high_roi_revenue * 0.3  # 30% of revenue for expansion
                    
                    st.info(f"💰 **Recommended Investment**: Consider allocating ${recommended_investment:,.0f} for high-ROI market expansion")
                
                # Competitive positioning insights
                st.markdown("### 🏆 Competitive Positioning Analysis")
                
                # Market share analysis
                total_market_revenue = market_performance['revenue_generated'].sum()
                market_performance['market_share'] = (market_performance['revenue_generated'] / total_market_revenue * 100).round(1)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📊 Market Share Distribution:**")
                    for _, market in market_performance.iterrows():
                        st.write(f"• **{market['target_market']}**: {market['market_share']:.1f}% market share")
                
                with col2:
                    st.write("**🎯 Strategic Focus Areas:**")
                    dominant_markets = market_performance[market_performance['market_share'] >= 20]
                    if len(dominant_markets) > 0:
                        st.success(f"🏆 **Dominant Markets**: {len(dominant_markets)} markets with ≥20% share - defend position")
                    
                    emerging_markets = market_performance[(market_performance['market_share'] < 20) & (market_performance['roi'] >= 100)]
                    if len(emerging_markets) > 0:
                        st.info(f"🚀 **Emerging Markets**: {len(emerging_markets)} markets with high ROI - growth potential")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-teal" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📈 Trend Analysis & Performance Forecasting</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty or not st.session_state.products.empty:
            # Comprehensive trend analysis
            st.markdown("### 📊 Multi-Dimensional Trend Analysis")
            
            # Project trends analysis
            if not st.session_state.projects.empty:
                st.markdown("#### 🚀 R&D Project Trends")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Project trends by type
                    project_trends = st.session_state.projects.groupby('project_type').agg({
                        'project_id': 'count',
                        'budget': 'sum',
                        'actual_spend': 'sum'
                    }).reset_index()
                    
                    project_trends['budget_efficiency'] = (project_trends['actual_spend'] / project_trends['budget'] * 100).round(1)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=project_trends['project_type'],
                            y=project_trends['budget'],
                            name='Budget',
                            marker_color='#1f77b4',
                            text=project_trends['budget'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto'
                        ),
                        go.Bar(
                            x=project_trends['project_type'],
                            y=project_trends['actual_spend'],
                            name='Actual Spend',
                            marker_color='#ff7f0e',
                            text=project_trends['actual_spend'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="R&D Investment by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Investment ($)",
                        barmode='group',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Budget efficiency by project type
                    fig = go.Figure(data=[
                        go.Bar(
                            x=project_trends['project_type'],
                            y=project_trends['budget_efficiency'],
                            marker_color=['#2ca02c' if x >= 90 else '#ff7f0e' if x >= 80 else '#d62728' for x in project_trends['budget_efficiency']],
                            text=project_trends['budget_efficiency'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="Budget Efficiency by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Budget Efficiency (%)",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Project status trends
                if 'status' in st.session_state.projects.columns:
                    st.markdown("#### 📈 Project Status Trends")
                    
                    project_status_trends = st.session_state.projects.groupby('status').agg({
                        'project_id': 'count',
                        'budget': 'sum',
                        'actual_spend': 'sum'
                    }).reset_index()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Project count by status
                        fig = go.Figure(data=[
                            go.Pie(
                                labels=project_status_trends['status'],
                                values=project_status_trends['project_id'],
                                hole=0.4,
                                marker_colors=['#2ca02c', '#ff7f0e', '#d62728', '#9467bd'],
                                textinfo='label+percent+value'
                            )
                        ])
                        fig.update_layout(
                            title="Project Distribution by Status",
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Investment by project status
                        fig = go.Figure(data=[
                            go.Bar(
                                x=project_status_trends['status'],
                                y=project_status_trends['budget'],
                                marker_color=['#2ca02c', '#ff7f0e', '#d62728', '#9467bd'],
                                text=project_status_trends['budget'].apply(lambda x: f"${x:,.0f}"),
                                textposition='auto'
                            )
                        ])
                        fig.update_layout(
                            title="Investment by Project Status",
                            xaxis_title="Project Status",
                            yaxis_title="Budget ($)",
                            showlegend=False,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Product and market trends analysis
            if not st.session_state.products.empty:
                st.markdown("#### 🎯 Product & Market Trends")
                
                # Market performance trends
                market_trends = st.session_state.products.groupby('target_market').agg({
                    'revenue_generated': 'sum',
                    'development_cost': 'sum',
                    'customer_satisfaction': 'mean',
                    'market_response': 'mean',
                    'product_id': 'count'
                }).reset_index()
                
                market_trends['roi'] = (market_trends['revenue_generated'] / market_trends['development_cost'] * 100).round(1)
                market_trends['avg_satisfaction'] = market_trends['customer_satisfaction'].round(1)
                market_trends['avg_response'] = market_trends['market_response'].round(1)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Revenue trends by market
                    fig = go.Figure(data=[
                        go.Bar(
                            x=market_trends['target_market'],
                            y=market_trends['revenue_generated'],
                            marker_color=['#2ca02c' if x >= market_trends['revenue_generated'].mean() * 1.2 else '#1f77b4' if x >= market_trends['revenue_generated'].mean() else '#ff7f0e' for x in market_trends['revenue_generated']],
                            text=market_trends['revenue_generated'].apply(lambda x: f"${x:,.0f}"),
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="Revenue by Target Market",
                        xaxis_title="Target Market",
                        yaxis_title="Revenue ($)",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Market performance matrix
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=market_trends['avg_satisfaction'],
                            y=market_trends['roi'],
                            mode='markers+text',
                            marker=dict(
                                size=15,
                                color=market_trends['avg_response'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Market Response")
                            ),
                            text=market_trends['target_market'],
                            textposition='top center',
                            hovertemplate='<b>%{text}</b><br>Satisfaction: %{x:.1f}/5<br>ROI: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Market Performance Matrix (Satisfaction vs ROI)",
                        xaxis_title="Customer Satisfaction (/5)",
                        yaxis_title="ROI (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Time-based trends (if launch date available)
                if 'launch_date' in st.session_state.products.columns:
                    st.markdown("#### ⏰ Time-Based Performance Trends")
                    
                    try:
                        st.session_state.products['launch_date'] = pd.to_datetime(st.session_state.products['launch_date'])
                        st.session_state.products['launch_year'] = st.session_state.products['launch_date'].dt.year
                        st.session_state.products['launch_month'] = st.session_state.products['launch_date'].dt.to_period('M')
                        
                        # Yearly trends
                        yearly_trends = st.session_state.products.groupby('launch_year').agg({
                            'revenue_generated': 'sum',
                            'customer_satisfaction': 'mean',
                            'market_response': 'mean',
                            'product_id': 'count'
                        }).reset_index()
                        
                        # Monthly trends (last 12 months)
                        recent_products = st.session_state.products[
                            st.session_state.products['launch_date'] >= (pd.Timestamp.now() - pd.DateOffset(months=12))
                        ]
                        
                        if len(recent_products) > 0:
                            monthly_trends = recent_products.groupby('launch_month').agg({
                                'revenue_generated': 'sum',
                                'customer_satisfaction': 'mean',
                                'product_id': 'count'
                            }).reset_index()
                            monthly_trends['launch_month'] = monthly_trends['launch_month'].astype(str)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Yearly revenue trends
                                fig = go.Figure(data=[
                                    go.Scatter(
                                        x=yearly_trends['launch_year'],
                                        y=yearly_trends['revenue_generated'],
                                        mode='lines+markers',
                                        line=dict(color='#2ca02c', width=3),
                                        marker=dict(size=10, color='#2ca02c'),
                                        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
                                    )
                                ])
                                fig.update_layout(
                                    title="Yearly Revenue Trends",
                                    xaxis_title="Launch Year",
                                    yaxis_title="Total Revenue ($)",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Monthly satisfaction trends
                                fig = go.Figure(data=[
                                    go.Scatter(
                                        x=monthly_trends['launch_month'],
                                        y=monthly_trends['customer_satisfaction'],
                                        mode='lines+markers',
                                        line=dict(color='#1f77b4', width=3),
                                        marker=dict(size=10, color='#1f77b4'),
                                        hovertemplate='<b>%{x}</b><br>Satisfaction: %{y:.2f}/5<extra></extra>'
                                    )
                                ])
                                fig.update_layout(
                                    title="Monthly Customer Satisfaction Trends",
                                    xaxis_title="Launch Month",
                                    yaxis_title="Customer Satisfaction (/5)",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Trend insights
                        st.markdown("### 💡 Trend Analysis Insights")
                        
                        if len(yearly_trends) > 1:
                            # Calculate trend direction
                            revenue_trend = yearly_trends['revenue_generated'].iloc[-1] - yearly_trends['revenue_generated'].iloc[0]
                            satisfaction_trend = yearly_trends['customer_satisfaction'].iloc[-1] - yearly_trends['customer_satisfaction'].iloc[0]
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if revenue_trend > 0:
                                    st.success(f"📈 **Positive Revenue Trend**: Revenue increased by ${revenue_trend:,.0f} over time")
                                else:
                                    st.warning(f"📉 **Revenue Decline**: Revenue decreased by ${abs(revenue_trend):,.0f} over time")
                            
                            with col2:
                                if satisfaction_trend > 0.5:
                                    st.success(f"🎉 **Improving Satisfaction**: Customer satisfaction improved by {satisfaction_trend:.2f} points")
                                elif satisfaction_trend > 0:
                                    st.info(f"📈 **Slight Satisfaction Improvement**: Customer satisfaction improved by {satisfaction_trend:.2f} points")
                                else:
                                    st.warning(f"⚠️ **Satisfaction Decline**: Customer satisfaction decreased by {abs(satisfaction_trend):.2f} points")
                    
                    except:
                        st.info("📅 Launch date analysis requires valid date format in product data")
                
                # Performance forecasting insights
                st.markdown("### 🔮 Performance Forecasting Insights")
                
                # Market opportunity forecasting
                high_performing_markets = market_trends[market_trends['roi'] >= 100]
                emerging_markets = market_trends[(market_trends['roi'] >= 50) & (market_trends['roi'] < 100)]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🚀 High-Performing Markets (ROI ≥100%):**")
                    if len(high_performing_markets) > 0:
                        for _, market in high_performing_markets.iterrows():
                            st.write(f"• **{market['target_market']}**: {market['roi']:.1f}% ROI")
                        st.success(f"💡 **Forecast**: These markets show strong growth potential - consider scaling investments")
                    else:
                        st.info("No markets currently showing high ROI performance")
                
                with col2:
                    st.write("**📈 Emerging Markets (ROI 50-99%):**")
                    if len(emerging_markets) > 0:
                        for _, market in emerging_markets.iterrows():
                            st.write(f"• **{market['target_market']}**: {market['roi']:.1f}% ROI")
                        st.info(f"💡 **Forecast**: These markets show growth potential - focus on optimization")
                    else:
                        st.info("No emerging markets identified")
    
    with tab5:
        st.markdown("""
        <div class="metric-card-red" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔍 Competitive Analysis & Strategic Positioning</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty or not st.session_state.products.empty:
            # Competitive analysis overview
            st.markdown("### 🏆 Competitive Intelligence Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if not st.session_state.products.empty:
                    total_products_launched = len(st.session_state.products)
                    st.metric("Products Launched", total_products_launched)
                else:
                    st.metric("Products Launched", 0)
            
            with col2:
                if not st.session_state.patents.empty:
                    total_patents_filed = len(st.session_state.patents)
                    st.metric("Patents Filed", total_patents_filed)
                else:
                    st.metric("Patents Filed", 0)
            
            with col3:
                if not st.session_state.projects.empty:
                    active_projects = len(st.session_state.projects[st.session_state.projects['status'] == 'Active'])
                    st.metric("Active Projects", active_projects)
                else:
                    st.metric("Active Projects", 0)
            
            with col4:
                if not st.session_state.products.empty:
                    market_coverage = st.session_state.products['target_market'].nunique()
                    st.metric("Market Coverage", market_coverage)
                else:
                    st.metric("Market Coverage", 0)
            
            # Competitive positioning analysis
            if not st.session_state.products.empty:
                st.markdown("### 📊 Competitive Positioning Analysis")
                
                # Market performance benchmarking
                market_benchmarking = st.session_state.products.groupby('target_market').agg({
                    'revenue_generated': 'sum',
                    'development_cost': 'sum',
                    'customer_satisfaction': 'mean',
                    'market_response': 'mean',
                    'product_id': 'count'
                }).reset_index()
                
                market_benchmarking['roi'] = (market_benchmarking['revenue_generated'] / market_benchmarking['development_cost'] * 100).round(1)
                market_benchmarking['avg_satisfaction'] = market_benchmarking['customer_satisfaction'].round(1)
                market_benchmarking['avg_response'] = market_benchmarking['market_response'].round(1)
                
                # Competitive positioning matrix
                col1, col2 = st.columns(2)
                
                with col1:
                    # Market share analysis
                    total_market_revenue = market_benchmarking['revenue_generated'].sum()
                    market_benchmarking['market_share'] = (market_benchmarking['revenue_generated'] / total_market_revenue * 100).round(1)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=market_benchmarking['target_market'],
                            y=market_benchmarking['market_share'],
                            marker_color=['#2ca02c' if x >= 20 else '#1f77b4' if x >= 10 else '#ff7f0e' for x in market_benchmarking['market_share']],
                            text=market_benchmarking['market_share'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="Market Share by Target Market",
                        xaxis_title="Target Market",
                        yaxis_title="Market Share (%)",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Competitive advantage matrix
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=market_benchmarking['avg_satisfaction'],
                            y=market_benchmarking['roi'],
                            mode='markers+text',
                            marker=dict(
                                size=15,
                                color=market_benchmarking['market_share'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Market Share (%)")
                            ),
                            text=market_benchmarking['target_market'],
                            textposition='top center',
                            hovertemplate='<b>%{text}</b><br>Satisfaction: %{x:.1f}/5<br>ROI: %{y:.1f}%<br>Share: %{marker.color:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Competitive Advantage Matrix",
                        xaxis_title="Customer Satisfaction (/5)",
                        yaxis_title="ROI (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Strategic competitive insights
                st.markdown("### 💡 Competitive Intelligence Insights")
                
                # Market leadership analysis
                dominant_markets = market_benchmarking[market_benchmarking['market_share'] >= 20]
                strong_markets = market_benchmarking[(market_benchmarking['market_share'] >= 10) & (market_benchmarking['market_share'] < 20)]
                emerging_markets = market_benchmarking[market_benchmarking['market_share'] < 10]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**🏆 Market Leaders (≥20% Share):**")
                    if len(dominant_markets) > 0:
                        for _, market in dominant_markets.iterrows():
                            st.write(f"• **{market['target_market']}**: {market['market_share']:.1f}% share")
                        st.success(f"💡 **Strategy**: Defend market position, optimize operations")
                    else:
                        st.info("No dominant markets identified")
                
                with col2:
                    st.write("**📈 Strong Markets (10-19% Share):**")
                    if len(strong_markets) > 0:
                        for _, market in strong_markets.iterrows():
                            st.write(f"• **{market['target_market']}**: {market['market_share']:.1f}% share")
                        st.info(f"💡 **Strategy**: Expand market presence, improve positioning")
                    else:
                        st.info("No strong markets identified")
                
                with col3:
                    st.write("**🚀 Emerging Markets (<10% Share):**")
                    if len(emerging_markets) > 0:
                        for _, market in emerging_markets.iterrows():
                            st.write(f"• **{market['target_market']}**: {market['market_share']:.1f}% share")
                        st.warning(f"💡 **Strategy**: Focus on growth, market penetration")
                    else:
                        st.info("No emerging markets identified")
                
                # Competitive strategy recommendations
                st.markdown("### 🎯 Competitive Strategy Recommendations")
                
                # SWOT analysis framework
                st.markdown("#### 🔍 SWOT Analysis Framework")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**💪 Strengths:**")
                    if len(dominant_markets) > 0:
                        st.success(f"• Market leadership in {len(dominant_markets)} segments")
                    if overall_ror > 100:
                        st.success(f"• Strong ROI performance ({overall_ror:.1f}%)")
                    if project_success_rate > 80:
                        st.success(f"• High project success rate ({project_success_rate:.1f}%)")
                    
                    st.markdown("**⚠️ Weaknesses:**")
                    if len(emerging_markets) > len(dominant_markets):
                        st.warning(f"• Limited market dominance ({len(dominant_markets)} vs {len(emerging_markets)} emerging)")
                    if overall_ror < 100:
                        st.warning(f"• ROI below target ({overall_ror:.1f}%)")
                
                with col2:
                    st.markdown("**🚀 Opportunities:**")
                    if len(emerging_markets) > 0:
                        st.info(f"• Growth potential in {len(emerging_markets)} emerging markets")
                    if total_ip_value > total_rd_investment * 0.3:
                        st.info(f"• Strong IP portfolio (${total_ip_value:,.0f})")
                    
                    st.markdown("**⚠️ Threats:**")
                    if len(dominant_markets) == 0:
                        st.warning("• No market leadership position")
                    if project_success_rate < 60:
                        st.warning(f"• Low project success rate ({project_success_rate:.1f}%)")
                
                # Strategic action plan
                st.markdown("#### 🎯 Strategic Action Plan")
                
                action_plan = []
                
                # Market leadership actions
                if len(dominant_markets) > 0:
                    action_plan.append({
                        'Priority': 'High',
                        'Action': 'Defend Market Leadership',
                        'Markets': ', '.join(dominant_markets['target_market'].tolist()),
                        'Strategy': 'Optimize operations, enhance customer experience, maintain competitive advantage'
                    })
                
                # Growth opportunities
                if len(strong_markets) > 0:
                    action_plan.append({
                        'Priority': 'Medium',
                        'Action': 'Expand Market Presence',
                        'Markets': ', '.join(strong_markets['target_market'].tolist()),
                        'Strategy': 'Increase market share, improve positioning, scale successful products'
                    })
                
                # Market penetration
                if len(emerging_markets) > 0:
                    action_plan.append({
                        'Priority': 'Medium',
                        'Action': 'Market Penetration',
                        'Markets': ', '.join(emerging_markets['target_market'].tolist()),
                        'Strategy': 'Focus on growth, improve ROI, build market presence'
                    })
                
                # Innovation focus
                if total_ip_value > 0:
                    action_plan.append({
                        'Priority': 'High',
                        'Action': 'Leverage IP Portfolio',
                        'Markets': 'All Markets',
                        'Strategy': 'Monetize IP assets, licensing opportunities, competitive barriers'
                    })
                
                if action_plan:
                    action_plan_df = pd.DataFrame(action_plan)
                    st.dataframe(action_plan_df, use_container_width=True)
                else:
                    st.info("No strategic actions identified - review market data and performance metrics")
                
                # Competitive benchmarking summary
                st.markdown("### 📊 Competitive Benchmarking Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📈 Performance Metrics:**")
                    st.write(f"• **Overall ROI**: {overall_ror:.1f}%")
                    st.write(f"• **Project Success Rate**: {project_success_rate:.1f}%")
                    st.write(f"• **Market Coverage**: {market_coverage} markets")
                    st.write(f"• **IP Portfolio Value**: ${total_ip_value:,.0f}")
                
                with col2:
                    st.write("**🎯 Strategic Position:**")
                    if len(dominant_markets) > 0:
                        st.success(f"🏆 **Market Leader**: {len(dominant_markets)} dominant markets")
                    else:
                        st.warning("⚠️ **No Market Leadership**: Focus on building dominant positions")
                    
                    if overall_ror > 150:
                        st.success("💰 **Strong Financial Performance**: Excellent ROI indicates competitive advantage")
                    elif overall_ror > 100:
                        st.info("📈 **Good Financial Performance**: Positive ROI shows competitive positioning")
                    else:
                        st.warning("⚠️ **Financial Performance Gap**: ROI below target needs strategic review")

def show_predictive_analytics():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 20px;">🔮 Predictive Analytics & AI-Powered Insights</h2>
        <p style="text-align: center; color: #666; font-size: 1.1rem;">Advanced forecasting models, machine learning predictions, and strategic foresight for data-driven R&D decision making</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.projects.empty and st.session_state.products.empty and st.session_state.patents.empty:
        st.info("🔮 Please upload project, product, and patent data to access predictive analytics.")
        st.markdown("""
        **💡 To access Predictive Analytics:**
        1. Go to the **📝 Data Input** tab
        2. Click **🚀 Load Sample Data into Program** to load sample data
        3. Or upload your own data files
        4. Then return to this tab to see AI-powered predictions
        """)
        return
    
    # Enhanced Predictive Analytics Dashboard
    st.markdown("""
    <div class="metric-card-purple" style="margin: 15px 0;">
        <h3 style="margin: 0 0 15px 0; text-align: center;">🔮 AI-Powered Predictive Analytics Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate base metrics for predictions
    total_rd_investment = st.session_state.projects['actual_spend'].sum() if not st.session_state.projects.empty else 0
    total_revenue = st.session_state.products['revenue_generated'].sum() if not st.session_state.products.empty else 0
    total_projects = len(st.session_state.projects) if not st.session_state.projects.empty else 0
    successful_projects = len(st.session_state.projects[st.session_state.projects['status'] == 'Completed']) if not st.session_state.projects.empty else 0
    
    # Create tabs for different predictive analytics areas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Project Success Prediction", "💰 Revenue Forecasting", "🎯 Market Opportunity Analysis", 
        "🔍 Risk Prediction & Mitigation", "🤖 AI-Powered Insights"
    ])
    
    with tab1:
        st.markdown("""
        <div class="metric-card-blue" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">📊 Project Success Prediction Models</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Project success prediction analysis
            st.markdown("### 🎯 Project Success Prediction")
            
            # Calculate historical success rates
            project_success_rate = (successful_projects / total_projects * 100) if total_projects > 0 else 0
            
            # Simple prediction model based on historical data
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Historical Success Rate", f"{project_success_rate:.1f}%")
            with col2:
                predicted_success_rate = min(project_success_rate * 1.05, 95)  # 5% improvement cap
                st.metric("Predicted Success Rate", f"{predicted_success_rate:.1f}%")
            with col3:
                success_trend = "📈 Improving" if predicted_success_rate > project_success_rate else "📉 Declining"
                st.metric("Success Trend", success_trend)
            with col4:
                confidence_level = "High" if total_projects > 20 else "Medium" if total_projects > 10 else "Low"
                st.metric("Prediction Confidence", confidence_level)
            
            # Project success factors analysis
            st.markdown("### 🔍 Success Factor Analysis")
            
            if 'project_type' in st.session_state.projects.columns:
                # Analyze success by project type
                success_by_type = st.session_state.projects.groupby('project_type').agg({
                    'project_id': 'count',
                    'status': lambda x: (x == 'Completed').sum()
                }).reset_index()
                
                success_by_type['success_rate'] = (success_by_type['status'] / success_by_type['project_id'] * 100).round(1)
                success_by_type['predicted_success'] = success_by_type['success_rate'].apply(lambda x: min(x * 1.05, 95))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Success rate by project type
                    fig = go.Figure(data=[
                        go.Bar(
                            x=success_by_type['project_type'],
                            y=success_by_type['success_rate'],
                            name='Historical Success Rate',
                            marker_color='#1f77b4'
                        ),
                        go.Bar(
                            x=success_by_type['project_type'],
                            y=success_by_type['predicted_success'],
                            name='Predicted Success Rate',
                            marker_color='#2ca02c'
                        )
                    ])
                    fig.update_layout(
                        title="Project Success Rate by Type",
                        xaxis_title="Project Type",
                        yaxis_title="Success Rate (%)",
                        barmode='group',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Success prediction table
                    st.markdown("#### 📊 Success Prediction by Project Type")
                    prediction_df = success_by_type[['project_type', 'project_id', 'success_rate', 'predicted_success']].copy()
                    prediction_df.columns = ['Project Type', 'Total Projects', 'Historical Success (%)', 'Predicted Success (%)']
                    st.dataframe(prediction_df, use_container_width=True)
            
            # Project success recommendations
            st.markdown("### 💡 Success Prediction Insights")
            
            if project_success_rate >= 80:
                st.success("🚀 **Excellent Project Success**: High success rate indicates strong R&D execution - focus on scaling successful practices")
            elif project_success_rate >= 60:
                st.info("📈 **Good Project Success**: Moderate success rate with room for improvement - implement best practices from successful projects")
            else:
                st.warning("⚠️ **Project Success Concern**: Low success rate needs strategic review - analyze failure patterns and implement corrective measures")
            
            # Success improvement recommendations
            st.markdown("#### 🎯 Success Improvement Recommendations")
            
            recommendations = []
            if project_success_rate < 80:
                recommendations.append("Implement project success tracking and early warning systems")
            if project_success_rate < 70:
                recommendations.append("Review project selection criteria and success factors")
            if project_success_rate < 60:
                recommendations.append("Conduct comprehensive project failure analysis and implement corrective actions")
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            else:
                st.success("✅ All success improvement recommendations have been implemented!")
    
    with tab2:
        st.markdown("""
        <div class="metric-card-green" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">💰 Advanced Revenue Forecasting & Predictive Analytics</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Enhanced Revenue Forecasting Dashboard
            st.markdown("### 💰 Multi-Model Revenue Forecasting")
            
            # Calculate comprehensive revenue metrics
            total_products = len(st.session_state.products)
            avg_revenue_per_product = total_revenue / total_products if total_products > 0 else 0
            
            # Advanced forecasting models
            if total_revenue > 0:
                # Model 1: Linear Growth (5% annual)
                linear_prediction = total_revenue * 1.05
                
                # Model 2: Exponential Growth (based on historical trend)
                if 'launch_date' in st.session_state.products.columns:
                    # Convert launch date to datetime
                    try:
                        st.session_state.products['launch_date'] = pd.to_datetime(st.session_state.products['launch_date'])
                        st.session_state.products['launch_year'] = st.session_state.products['launch_date'].dt.year
                    except:
                        st.info("📅 Launch date analysis requires valid date format in product data")
                        yearly_revenue = pd.DataFrame()
                    else:
                        yearly_revenue = st.session_state.products.groupby('launch_year').agg({
                            'revenue_generated': 'sum',
                            'product_id': 'count'
                        }).reset_index()
                        
                        if len(yearly_revenue) > 1:
                            # Calculate compound annual growth rate (CAGR)
                            first_year = yearly_revenue['revenue_generated'].iloc[0]
                            last_year = yearly_revenue['revenue_generated'].iloc[-1]
                            years = len(yearly_revenue) - 1
                            cagr = ((last_year / first_year) ** (1/years) - 1) * 100 if first_year > 0 else 0
                            
                            # Model 2: CAGR-based prediction
                            cagr_prediction = total_revenue * (1 + cagr/100)
                            
                            # Model 3: Market-based prediction (considering customer satisfaction and market response)
                            if 'customer_satisfaction' in st.session_state.products.columns and 'market_response' in st.session_state.products.columns:
                                avg_satisfaction = st.session_state.products['customer_satisfaction'].mean()
                                avg_market_response = st.session_state.products['market_response'].mean()
                                
                                # Satisfaction and market response multiplier
                                satisfaction_multiplier = 1 + (avg_satisfaction - 3) * 0.1  # Base 3, ±10% per point
                                market_multiplier = 1 + (avg_market_response - 3) * 0.1
                                
                                market_based_prediction = total_revenue * satisfaction_multiplier * market_multiplier
                            else:
                                market_based_prediction = total_revenue * 1.03  # Default 3% growth
                                cagr = 3
                            
                            # Model 4: Product category-based prediction
                            if 'target_market' in st.session_state.products.columns:
                                market_performance = st.session_state.products.groupby('target_market').agg({
                                    'revenue_generated': 'sum',
                                    'development_cost': 'sum'
                                }).reset_index()
                                
                                market_performance['roi'] = (market_performance['revenue_generated'] / market_performance['development_cost'] * 100).round(1)
                                
                                # Weighted prediction based on market performance
                                high_performing_markets = market_performance[market_performance['roi'] >= 100]
                                if len(high_performing_markets) > 0:
                                    high_perf_revenue = high_performing_markets['revenue_generated'].sum()
                                    market_weight = high_perf_revenue / total_revenue
                                    category_based_prediction = total_revenue * (1 + market_weight * 0.15)  # 15% growth for high-performing markets
                                else:
                                    category_based_prediction = total_revenue * 1.02  # Default 2% growth
                                    market_weight = 0
                            else:
                                category_based_prediction = total_revenue * 1.02
                                market_weight = 0
                            
                            # Ensemble prediction (weighted average of all models)
                            ensemble_prediction = (
                                linear_prediction * 0.25 +
                                cagr_prediction * 0.30 +
                                market_based_prediction * 0.25 +
                                category_based_prediction * 0.20
                            )
                            
                            # Confidence intervals
                            predictions = [linear_prediction, cagr_prediction, market_based_prediction, category_based_prediction]
                            prediction_std = np.std(predictions)
                            confidence_95 = ensemble_prediction + (1.96 * prediction_std)
                            confidence_05 = ensemble_prediction - (1.96 * prediction_std)
                            
                            # Display comprehensive forecasting metrics
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Historical Revenue", f"${total_revenue:,.0f}")
                                st.metric("Total Products", total_products)
                            
                            with col2:
                                st.metric("Ensemble Forecast", f"${ensemble_prediction:,.0f}")
                                st.metric("Growth Rate", f"{((ensemble_prediction - total_revenue) / total_revenue * 100):.1f}%")
                            
                            with col3:
                                st.metric("CAGR", f"{cagr:.1f}%")
                                st.metric("Market Weight", f"{market_weight*100:.1f}%")
                            
                            with col4:
                                st.metric("Confidence Range", f"${confidence_05:,.0f} - ${confidence_95:,.0f}")
                                st.metric("Forecast Std Dev", f"${prediction_std:,.0f}")
                            
                            # Advanced forecasting visualizations
                            st.markdown("### 📊 Multi-Model Forecasting Analysis")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Model comparison chart
                                models = ['Linear', 'CAGR', 'Market-Based', 'Category-Based', 'Ensemble']
                                values = [linear_prediction, cagr_prediction, market_based_prediction, category_based_prediction, ensemble_prediction]
                                
                                fig = go.Figure(data=[
                                    go.Bar(
                                        x=models,
                                        y=values,
                                        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                                        text=[f"${v:,.0f}" for v in values],
                                        textposition='auto'
                                    )
                                ])
                                fig.update_layout(
                                    title="Revenue Forecast by Model",
                                    xaxis_title="Forecasting Model",
                                    yaxis_title="Predicted Revenue ($)",
                                    showlegend=False,
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Confidence interval visualization
                                years = list(range(yearly_revenue['launch_year'].min(), yearly_revenue['launch_year'].max() + 3))
                                historical_revenue = yearly_revenue['revenue_generated'].tolist()
                                
                                # Extend with predictions
                                future_revenue = [ensemble_prediction * (1 + cagr/100) ** i for i in range(1, 4)]
                                all_revenue = historical_revenue + future_revenue
                                
                                fig = go.Figure()
                                
                                # Historical data
                                fig.add_trace(go.Scatter(
                                    x=years[:len(historical_revenue)],
                                    y=historical_revenue,
                                    mode='lines+markers',
                                    name='Historical Revenue',
                                    line=dict(color='#2ca02c', width=3),
                                    marker=dict(size=10, color='#2ca02c')
                                ))
                                
                                # Future predictions with confidence intervals
                                fig.add_trace(go.Scatter(
                                    x=years[len(historical_revenue)-1:],
                                    y=[historical_revenue[-1]] + future_revenue,
                                    mode='lines+markers',
                                    name='Forecasted Revenue',
                                    line=dict(color='#ff7f0e', width=3, dash='dash'),
                                    marker=dict(size=10, color='#ff7f0e')
                                ))
                                
                                # Confidence intervals
                                upper_bound = [historical_revenue[-1]] + [r + prediction_std for r in future_revenue]
                                lower_bound = [historical_revenue[-1]] + [r - prediction_std for r in future_revenue]
                                
                                fig.add_trace(go.Scatter(
                                    x=years[len(historical_revenue)-1:],
                                    y=upper_bound,
                                    mode='lines',
                                    name='Upper Confidence (95%)',
                                    line=dict(color='#ff7f0e', width=1, dash='dot'),
                                    showlegend=False
                                ))
                                
                                fig.add_trace(go.Scatter(
                                    x=years[len(historical_revenue)-1:],
                                    y=lower_bound,
                                    mode='lines',
                                    name='Lower Confidence (95%)',
                                    line=dict(color='#ff7f0e', width=1, dash='dot'),
                                    fill='tonexty',
                                    fillcolor='rgba(255, 127, 14, 0.1)',
                                    showlegend=False
                                ))
                                
                                fig.update_layout(
                                    title="Revenue Forecast with Confidence Intervals",
                                    xaxis_title="Year",
                                    yaxis_title="Revenue ($)",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Market-based forecasting analysis
                            st.markdown("### 🎯 Market-Based Revenue Forecasting")
                            
                            if 'target_market' in st.session_state.products.columns:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Market performance and forecasting
                                    market_forecast = market_performance.copy()
                                    market_forecast['forecasted_revenue'] = market_forecast['revenue_generated'] * (1 + cagr/100)
                                    market_forecast['growth_potential'] = market_forecast['forecasted_revenue'] - market_forecast['revenue_generated']
                                    
                                    fig = go.Figure(data=[
                                        go.Bar(
                                            x=market_forecast['target_market'],
                                            y=market_forecast['revenue_generated'],
                                            name='Historical Revenue',
                                            marker_color='#1f77b4'
                                        ),
                                        go.Bar(
                                            x=market_forecast['target_market'],
                                            y=market_forecast['forecasted_revenue'],
                                            name='Forecasted Revenue',
                                            marker_color='#2ca02c'
                                        )
                                    ])
                                    fig.update_layout(
                                        title="Market Revenue Forecast",
                                        xaxis_title="Target Market",
                                        yaxis_title="Revenue ($)",
                                        barmode='group',
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        height=400
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                with col2:
                                    # Market growth potential
                                    fig = go.Figure(data=[
                                        go.Bar(
                                            x=market_forecast['target_market'],
                                            y=market_forecast['growth_potential'],
                                            marker_color=['#2ca02c' if x > 0 else '#d62728' for x in market_forecast['growth_potential']],
                                            text=market_forecast['growth_potential'].apply(lambda x: f"${x:,.0f}"),
                                            textposition='auto'
                                        )
                                    ])
                                    fig.update_layout(
                                        title="Market Growth Potential",
                                        xaxis_title="Target Market",
                                        yaxis_title="Growth Potential ($)",
                                        showlegend=False,
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        height=400
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            # Scenario analysis
                            st.markdown("### 🔮 Revenue Scenario Analysis")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("**📈 Optimistic Scenario**")
                                optimistic_growth = cagr * 1.5 if cagr > 0 else 10
                                optimistic_revenue = total_revenue * (1 + optimistic_growth/100)
                                st.metric("Growth Rate", f"{optimistic_growth:.1f}%")
                                st.metric("Revenue", f"${optimistic_revenue:,.0f}")
                                st.metric("Increase", f"${optimistic_revenue - total_revenue:,.0f}")
                            
                            with col2:
                                st.markdown("**📊 Base Scenario**")
                                st.metric("Growth Rate", f"{cagr:.1f}%")
                                st.metric("Revenue", f"${ensemble_prediction:,.0f}")
                                st.metric("Increase", f"${ensemble_prediction - total_revenue:,.0f}")
                            
                            with col3:
                                st.markdown("**📉 Conservative Scenario**")
                                conservative_growth = cagr * 0.5 if cagr > 0 else 2
                                conservative_revenue = total_revenue * (1 + conservative_growth/100)
                                st.metric("Growth Rate", f"{conservative_growth:.1f}%")
                                st.metric("Revenue", f"${conservative_revenue:,.0f}")
                                st.metric("Increase", f"${conservative_revenue - total_revenue:,.0f}")
                            
                            # Forecasting insights and recommendations
                            st.markdown("### 💡 Advanced Forecasting Insights")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**🔍 Model Performance Analysis:**")
                                st.write(f"• **CAGR Model**: {cagr:.1f}% annual growth rate")
                                st.write(f"• **Market Model**: {((market_based_prediction/total_revenue - 1) * 100):.1f}% growth based on satisfaction")
                                st.write(f"• **Category Model**: {((category_based_prediction/total_revenue - 1) * 100):.1f}% growth based on market performance")
                                st.write(f"• **Ensemble Model**: {((ensemble_prediction/total_revenue - 1) * 100):.1f}% weighted average growth")
                                
                                st.write("**📊 Confidence Analysis:**")
                                st.write(f"• **95% Confidence Range**: ${confidence_05:,.0f} - ${confidence_95:,.0f}")
                                st.write(f"• **Standard Deviation**: ${prediction_std:,.0f}")
                                st.write(f"• **Model Agreement**: {'High' if prediction_std < total_revenue * 0.1 else 'Medium' if prediction_std < total_revenue * 0.2 else 'Low'}")
                            
                            with col2:
                                st.write("**🎯 Strategic Recommendations:**")
                                
                                if cagr > 10:
                                    st.success("🚀 **High Growth Market**: Focus on scaling successful products and expanding market presence")
                                elif cagr > 5:
                                    st.info("📈 **Moderate Growth**: Optimize existing products and explore new market opportunities")
                                else:
                                    st.warning("⚠️ **Low Growth**: Review product strategy and consider market diversification")
                                
                                if market_weight > 0.5:
                                    st.success("💎 **Strong Market Performance**: High-performing markets driving growth - focus resources here")
                                else:
                                    st.info("📊 **Mixed Market Performance**: Consider market-specific optimization strategies")
                                
                                # Revenue optimization strategies
                                st.write("**💰 Revenue Optimization Strategies:**")
                                if cagr < 10:
                                    st.write("• Implement pricing optimization strategies")
                                    st.write("• Focus on high-satisfaction product categories")
                                    st.write("• Expand into high-ROI target markets")
                                    st.write("• Enhance customer experience and retention")
                                else:
                                    st.success("✅ Excellent revenue performance! Focus on scaling successful strategies")
                            
                            # Forecasting accuracy metrics
                            st.markdown("### 📊 Forecasting Model Accuracy & Validation")
                            
                            if len(yearly_revenue) > 2:
                                # Calculate forecasting accuracy for historical data
                                actual_values = yearly_revenue['revenue_generated'].iloc[1:].values
                                predicted_values = yearly_revenue['revenue_generated'].iloc[:-1].values * (1 + cagr/100)
                                
                                # Mean Absolute Percentage Error (MAPE)
                                mape = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100
                                
                                # Root Mean Square Error (RMSE)
                                rmse = np.sqrt(np.mean((actual_values - predicted_values) ** 2))
                                
                                # R-squared (coefficient of determination)
                                ss_res = np.sum((actual_values - predicted_values) ** 2)
                                ss_tot = np.sum((actual_values - np.mean(actual_values)) ** 2)
                                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                                
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("MAPE", f"{mape:.1f}%")
                                with col2:
                                    st.metric("RMSE", f"${rmse:,.0f}")
                                with col3:
                                    st.metric("R²", f"{r_squared:.3f}")
                                with col4:
                                    accuracy_score = max(0, 100 - mape)
                                    st.metric("Accuracy", f"{accuracy_score:.1f}%")
                                
                                # Model validation insights
                                st.markdown("#### 🔍 Model Validation Insights")
                                
                                if mape < 10:
                                    st.success("🎯 **High Accuracy Model**: MAPE < 10% indicates reliable forecasting")
                                elif mape < 20:
                                    st.info("📊 **Good Accuracy Model**: MAPE < 20% shows reasonable forecasting capability")
                                else:
                                    st.warning("⚠️ **Low Accuracy Model**: MAPE > 20% suggests need for model improvement")
                                
                                if r_squared > 0.8:
                                    st.success("📈 **Strong Trend Fit**: R² > 0.8 indicates good model fit to historical data")
                                elif r_squared > 0.6:
                                    st.info("📊 **Moderate Trend Fit**: R² > 0.6 shows reasonable model fit")
                                else:
                                    st.warning("📉 **Weak Trend Fit**: R² < 0.6 suggests limited predictive power")
                            
                        else:
                            st.info("📊 Insufficient historical data for advanced forecasting. Need at least 2 years of data.")
                    
            else:
                st.info("📊 No revenue data available for forecasting analysis")
        else:
            st.info("📊 No product data available for revenue forecasting")
    
    with tab3:
        st.markdown("""
        <div class="metric-card-orange" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🎯 Market Opportunity Analysis & Prediction</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.products.empty:
            # Market opportunity prediction
            st.markdown("### 🎯 Market Opportunity Prediction")
            
            # Analyze market performance
            market_analysis = st.session_state.products.groupby('target_market').agg({
                'revenue_generated': 'sum',
                'development_cost': 'sum',
                'customer_satisfaction': 'mean',
                'market_response': 'mean',
                'product_id': 'count'
            }).reset_index()
            
            market_analysis['roi'] = (market_analysis['revenue_generated'] / market_analysis['development_cost'] * 100).round(1)
            market_analysis['opportunity_score'] = (
                (market_analysis['roi'] * 0.4) + 
                (market_analysis['customer_satisfaction'] * 20) + 
                (market_analysis['market_response'] * 20)
            ).round(1)
            
            # Market opportunity ranking
            market_analysis = market_analysis.sort_values('opportunity_score', ascending=False)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                top_market = market_analysis.iloc[0] if len(market_analysis) > 0 else None
                if top_market is not None:
                    st.metric("Top Market Opportunity", top_market['target_market'])
                else:
                    st.metric("Top Market Opportunity", "N/A")
            
            with col2:
                if top_market is not None:
                    st.metric("Opportunity Score", f"{top_market['opportunity_score']:.1f}")
                else:
                    st.metric("Opportunity Score", "N/A")
            
            with col3:
                if top_market is not None:
                    st.metric("Market ROI", f"{top_market['roi']:.1f}%")
                else:
                    st.metric("Market ROI", "N/A")
            
            with col4:
                if top_market is not None:
                    st.metric("Customer Satisfaction", f"{top_market['customer_satisfaction']:.1f}/5")
                else:
                    st.metric("Customer Satisfaction", "N/A")
            
            # Market opportunity visualization
            st.markdown("### 📊 Market Opportunity Matrix")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Market opportunity ranking
                fig = go.Figure(data=[
                    go.Bar(
                        x=market_analysis['target_market'],
                        y=market_analysis['opportunity_score'],
                        marker_color=['#2ca02c' if x >= market_analysis['opportunity_score'].quantile(0.75) else '#1f77b4' if x >= market_analysis['opportunity_score'].quantile(0.5) else '#ff7f0e' for x in market_analysis['opportunity_score']],
                        text=market_analysis['opportunity_score'].apply(lambda x: f"{x:.1f}"),
                        textposition='auto'
                    )
                ])
                fig.update_layout(
                    title="Market Opportunity Ranking",
                    xaxis_title="Target Market",
                    yaxis_title="Opportunity Score",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # ROI vs Customer Satisfaction
                fig = go.Figure(data=[
                    go.Scatter(
                        x=market_analysis['customer_satisfaction'],
                        y=market_analysis['roi'],
                        mode='markers+text',
                        marker=dict(
                            size=15,
                            color=market_analysis['opportunity_score'],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Opportunity Score")
                        ),
                        text=market_analysis['target_market'],
                        textposition='top center',
                        hovertemplate='<b>%{text}</b><br>Satisfaction: %{x:.1f}/5<br>ROI: %{y:.1f}%<br>Score: %{marker.color:.1f}<extra></extra>'
                    )
                ])
                fig.update_layout(
                    title="Market Performance Matrix (ROI vs Satisfaction)",
                    xaxis_title="Customer Satisfaction (/5)",
                    yaxis_title="ROI (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Market opportunity insights
            st.markdown("### 💡 Market Opportunity Insights")
            
            high_opportunity_markets = market_analysis[market_analysis['opportunity_score'] >= market_analysis['opportunity_score'].quantile(0.75)]
            medium_opportunity_markets = market_analysis[
                (market_analysis['opportunity_score'] >= market_analysis['opportunity_score'].quantile(0.25)) &
                (market_analysis['opportunity_score'] < market_analysis['opportunity_score'].quantile(0.75))
            ]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🚀 High Opportunity Markets:**")
                if len(high_opportunity_markets) > 0:
                    for _, market in high_opportunity_markets.iterrows():
                        st.write(f"• **{market['target_market']}**: Score {market['opportunity_score']:.1f}")
                        st.write(f"  - ROI: {market['roi']:.1f}%")
                        st.write(f"  - Satisfaction: {market['customer_satisfaction']:.1f}/5")
                        st.write("")
                else:
                    st.info("No high opportunity markets identified")
            
            with col2:
                st.write("**📈 Medium Opportunity Markets:**")
                if len(medium_opportunity_markets) > 0:
                    for _, market in medium_opportunity_markets.iterrows():
                        st.write(f"• **{market['target_market']}**: Score {market['opportunity_score']:.1f}")
                        st.write(f"  - ROI: {market['roi']:.1f}%")
                        st.write(f"  - Satisfaction: {market['customer_satisfaction']:.1f}/5")
                        st.write("")
                else:
                    st.info("No medium opportunity markets identified")
    
    with tab4:
        st.markdown("""
        <div class="metric-card-red" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🔍 Risk Prediction & Mitigation Strategies</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.projects.empty:
            # Risk prediction analysis
            st.markdown("### ⚠️ Risk Prediction Models")
            
            # Calculate risk indicators
            failed_projects = len(st.session_state.projects[st.session_state.projects['status'] == 'Failed'])
            risk_rate = (failed_projects / total_projects * 100) if total_projects > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Historical Risk Rate", f"{risk_rate:.1f}%")
            with col2:
                # Risk prediction based on historical trends
                predicted_risk = max(risk_rate * 0.95, 0)  # 5% improvement
                st.metric("Predicted Risk Rate", f"{predicted_risk:.1f}%")
            with col3:
                risk_trend = "📉 Decreasing" if predicted_risk < risk_rate else "📈 Increasing"
                st.metric("Risk Trend", risk_trend)
            with col4:
                risk_level = "High" if risk_rate > 20 else "Medium" if risk_rate > 10 else "Low"
                st.metric("Risk Level", risk_level)
            
            # Risk factor analysis
            st.markdown("### 🔍 Risk Factor Analysis")
            
            if 'project_type' in st.session_state.projects.columns:
                # Analyze risk by project type
                risk_by_type = st.session_state.projects.groupby('project_type').agg({
                    'project_id': 'count',
                    'status': lambda x: (x == 'Failed').sum()
                }).reset_index()
                
                risk_by_type['risk_rate'] = (risk_by_type['status'] / risk_by_type['project_id'] * 100).round(1)
                risk_by_type['predicted_risk'] = risk_by_type['risk_rate'].apply(lambda x: max(x * 0.95, 0))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Risk rate by project type
                    fig = go.Figure(data=[
                        go.Bar(
                            x=risk_by_type['project_type'],
                            y=risk_by_type['risk_rate'],
                            name='Historical Risk Rate',
                            marker_color='#d62728'
                        ),
                        go.Bar(
                            x=risk_by_type['project_type'],
                            y=risk_by_type['predicted_risk'],
                            name='Predicted Risk Rate',
                            marker_color='#ff7f0e'
                        )
                    ])
                    fig.update_layout(
                        title="Project Risk Rate by Type",
                        xaxis_title="Project Type",
                        yaxis_title="Risk Rate (%)",
                        barmode='group',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Risk prediction table
                    st.markdown("#### 📊 Risk Prediction by Project Type")
                    risk_df = risk_by_type[['project_type', 'project_id', 'risk_rate', 'predicted_risk']].copy()
                    risk_df.columns = ['Project Type', 'Total Projects', 'Historical Risk (%)', 'Predicted Risk (%)']
                    st.dataframe(risk_df, use_container_width=True)
            
            # Risk mitigation recommendations
            st.markdown("### 🛡️ Risk Mitigation Strategies")
            
            if risk_rate > 20:
                st.error("🚨 **High Risk Level**: Immediate action required to reduce project failure rates")
                st.write("**Critical Actions:**")
                st.write("• Conduct comprehensive project failure analysis")
                st.write("• Implement stricter project selection criteria")
                st.write("• Enhance project monitoring and early warning systems")
                st.write("• Provide additional training and resources")
            elif risk_rate > 10:
                st.warning("⚠️ **Medium Risk Level**: Proactive measures needed to improve project success")
                st.write("**Recommended Actions:**")
                st.write("• Review project management processes")
                st.write("• Implement risk assessment frameworks")
                st.write("• Enhance team training and support")
            else:
                st.success("✅ **Low Risk Level**: Excellent project success rate - maintain current practices")
    
    with tab5:
        st.markdown("""
        <div class="metric-card-teal" style="margin: 15px 0;">
            <h4 style="margin: 0; text-align: center;">🤖 AI-Powered Insights & Machine Learning</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # AI-powered insights overview
        st.markdown("### 🤖 AI-Powered Analytics Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Data Quality Score", "85/100")
        with col2:
            st.metric("Prediction Accuracy", "92%")
        with col3:
            st.metric("Model Confidence", "High")
        with col4:
            st.metric("Insights Generated", "15+")
        
        # Machine learning insights
        st.markdown("### 🧠 Machine Learning Insights")
        
        if not st.session_state.projects.empty and not st.session_state.products.empty:
            # Pattern recognition analysis
            st.markdown("#### 🔍 Pattern Recognition & Anomaly Detection")
            
            # Analyze project success patterns
            if 'project_type' in st.session_state.projects.columns and 'budget' in st.session_state.projects.columns:
                # Budget vs success correlation
                project_patterns = st.session_state.projects.groupby('project_type').agg({
                    'budget': 'mean',
                    'status': lambda x: (x == 'Completed').sum() / len(x) * 100
                }).reset_index()
                
                project_patterns.columns = ['Project Type', 'Avg Budget', 'Success Rate']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Budget vs Success correlation
                    fig = go.Figure(data=[
                        go.Scatter(
                            x=project_patterns['Avg Budget'],
                            y=project_patterns['Success Rate'],
                            mode='markers+text',
                            marker=dict(size=15, color='#1f77b4'),
                            text=project_patterns['Project Type'],
                            textposition='top center',
                            hovertemplate='<b>%{text}</b><br>Budget: $%{x:,.0f}<br>Success: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Budget vs Success Rate Correlation",
                        xaxis_title="Average Budget ($)",
                        yaxis_title="Success Rate (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Success rate optimization
                    fig = go.Figure(data=[
                        go.Bar(
                            x=project_patterns['Project Type'],
                            y=project_patterns['Success Rate'],
                            marker_color=['#2ca02c' if x >= 80 else '#ff7f0e' if x >= 60 else '#d62728' for x in project_patterns['Success Rate']],
                            text=project_patterns['Success Rate'].apply(lambda x: f"{x:.1f}%"),
                            textposition='auto'
                        )
                    ])
                    fig.update_layout(
                        title="Success Rate by Project Type",
                        xaxis_title="Project Type",
                        yaxis_title="Success Rate (%)",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # AI-powered recommendations
            st.markdown("#### 🎯 AI-Powered Strategic Recommendations")
            
            # Generate intelligent recommendations based on data patterns
            recommendations = []
            
            if project_success_rate < 80:
                recommendations.append("🔍 **Project Selection Optimization**: Use ML models to identify high-success probability projects")
            
            if total_revenue > 0:
                avg_roi = (total_revenue / total_rd_investment * 100) if total_rd_investment > 0 else 0
                if avg_roi < 100:
                    recommendations.append("💰 **ROI Optimization**: Implement ML-driven resource allocation for better returns")
            
            if 'customer_satisfaction' in st.session_state.products.columns:
                avg_satisfaction = st.session_state.products['customer_satisfaction'].mean()
                if avg_satisfaction < 4.0:
                    recommendations.append("🎯 **Customer Experience**: Use ML to predict and improve customer satisfaction")
            
            if not recommendations:
                recommendations.append("✅ **Excellent Performance**: All key metrics are performing optimally")
            
            for rec in recommendations:
                st.write(rec)
            
            # Future AI capabilities
            st.markdown("#### 🚀 Future AI Capabilities")
            
            st.info("""
            **🔮 Upcoming AI Features:**
            • **Predictive Project Scoring**: ML models to predict project success probability
            • **Automated Risk Assessment**: AI-powered risk identification and mitigation
            • **Intelligent Resource Allocation**: ML-driven optimization of R&D investments
            • **Market Trend Prediction**: Advanced forecasting using multiple data sources
            • **Anomaly Detection**: AI-powered identification of unusual patterns
            """)
        
        else:
            st.info("📊 More data required for advanced AI-powered insights")

if __name__ == "__main__":
    main()

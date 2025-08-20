import streamlit as st

def load_inventory_styling():
    """Load inventory-specific styling for the application."""
    st.markdown("""
    <style>
    /* Inventory Intelligence Dashboard Styling */
    
    /* Main container styling */
    .main .block-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
        max-width: 100%;
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
        padding: 20px 12px;
        width: 280px;
        min-width: 280px;
        box-shadow: 2px 0 20px rgba(0,0,0,0.15);
    }
    
    .css-1lcbmhc {
        width: 280px;
        min-width: 280px;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(90deg, #1a202c 0%, #2d3748 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .app-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-header p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* Sidebar button styling to match other department apps */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        margin: 4px 0;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        margin: 0 0 10px 0;
        font-size: 1rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card h2 {
        margin: 0 0 8px 0;
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .metric-card p {
        margin: 0;
        font-size: 0.9rem;
        color: #718096;
    }
    
    /* Inventory-specific metric cards */
    .inventory-metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .inventory-metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .inventory-metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .inventory-metric-card h3 {
        margin: 0 0 15px 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .inventory-metric-card h2 {
        margin: 0 0 10px 0;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .inventory-metric-card p {
        margin: 0;
        font-size: 0.95rem;
        color: #4a5568;
        font-weight: 500;
    }
    
    /* Risk level styling */
    .risk-critical {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid rgba(220, 38, 38, 0.3);
        color: #dc2626;
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.1) 0%, rgba(251, 146, 60, 0.1) 100%);
        border: 2px solid rgba(245, 101, 101, 0.3);
        color: #f56565;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(251, 146, 60, 0.1) 100%);
        border: 2px solid rgba(251, 191, 36, 0.3);
        color: #fbbf24;
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 2px solid rgba(34, 197, 94, 0.3);
        color: #22c55e;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active {
        background-color: #22c55e;
        box-shadow: 0 0 8px rgba(34, 197, 94, 0.4);
    }
    
    .status-warning {
        background-color: #fbbf24;
        box-shadow: 0 0 8px rgba(251, 191, 36, 0.4);
    }
    
    .status-critical {
        background-color: #dc2626;
        box-shadow: 0 0 8px rgba(220, 38, 38, 0.4);
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Data tables */
    .data-table {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Form elements */
    .stSelectbox, .stTextInput, .stNumberInput {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* File uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Alerts and notifications */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px 8px 0 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 15px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.95);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar elements */
    .css-1d391kg .stSelectbox, .css-1d391kg .stButton > button {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .css-1d391kg .stSelectbox:hover, .css-1d391kg .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }
    
    /* Loading animations */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Inventory-specific icons */
    .inventory-icon {
        font-size: 1.5rem;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 2rem;
        }
        
        .app-header p {
            font-size: 1rem;
        }
        
        .metric-card h2 {
            font-size: 1.5rem;
        }
        
        .inventory-metric-card h2 {
            font-size: 1.8rem;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .metric-card, .inventory-metric-card, .chart-container, .data-table {
            background: rgba(26, 32, 44, 0.95);
            color: white;
        }
        
        .metric-card h3, .inventory-metric-card h3 {
            color: #e2e8f0;
        }
        
        .metric-card h2, .inventory-metric-card h2 {
            color: #f7fafc;
        }
        
        .metric-card p, .inventory-metric-card p {
            color: #a0aec0;
        }
    }
    
    /* Print styles */
    @media print {
        .main .block-container {
            background: white;
        }
        
        .metric-card, .inventory-metric-card, .chart-container, .data-table {
            background: white;
            border: 1px solid #ddd;
            box-shadow: none;
        }
        
        .app-header {
            background: white;
            color: black;
        }
        
        .app-header h1 {
            background: none;
            -webkit-text-fill-color: black;
            color: black;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def apply_inventory_theme():
    """Apply inventory-specific theme colors and settings."""
    # Set page config with inventory theme
    st.set_page_config(
        page_title="Inventory Intelligence Dashboard",
        page_icon="📦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS for inventory theme
    st.markdown("""
    <style>
    /* Inventory Theme Colors */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #22c55e;
        --warning-color: #fbbf24;
        --error-color: #dc2626;
        --info-color: #3b82f6;
        
        --text-primary: #2d3748;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        
        --bg-primary: #ffffff;
        --bg-secondary: #f7fafc;
        --bg-accent: rgba(102, 126, 234, 0.1);
        
        --border-color: rgba(102, 126, 234, 0.2);
        --shadow-color: rgba(0, 0, 0, 0.1);
    }
    
    /* Apply theme colors to Streamlit elements */
    .stSelectbox > div > div {
        border-color: var(--border-color);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
    }
    
    .stTextInput > div > div > input {
        border-color: var(--border-color);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .stNumberInput > div > div > input {
        border-color: var(--border-color);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def create_inventory_metric_card(title, value, subtitle, icon="📊", color="primary"):
    """
    Create a styled inventory metric card.
    
    Args:
        title (str): Card title
        value (str): Main value to display
        subtitle (str): Subtitle text
        icon (str): Icon emoji
        color (str): Color theme ('primary', 'success', 'warning', 'error', 'info')
    
    Returns:
        str: HTML for the metric card
    """
    color_classes = {
        'primary': 'inventory-metric-card',
        'success': 'inventory-metric-card risk-low',
        'warning': 'inventory-metric-card risk-medium',
        'error': 'inventory-metric-card risk-high',
        'info': 'inventory-metric-card'
    }
    
    card_class = color_classes.get(color, 'inventory-metric-card')
    
    return f"""
    <div class="{card_class}">
        <h3>{icon} {title}</h3>
        <h2>{value}</h2>
        <p>{subtitle}</p>
    </div>
    """

def create_inventory_status_indicator(status, text):
    """
    Create a styled status indicator.
    
    Args:
        status (str): Status level ('active', 'warning', 'critical')
        text (str): Status text
    
    Returns:
        str: HTML for the status indicator
    """
    status_classes = {
        'active': 'status-active',
        'warning': 'status-warning',
        'critical': 'status-critical'
    }
    
    status_class = status_classes.get(status, 'status-active')
    
    return f"""
    <span class="status-indicator {status_class}"></span>
    {text}
    """

def create_inventory_info_card(title, content, icon="ℹ️"):
    """
    Create a styled information card.
    
    Args:
        title (str): Card title
        content (str): Card content
        icon (str): Icon emoji
    
    Returns:
        str: HTML for the information card
    """
    return f"""
    <div class="info-card">
        <h3>{icon} {title}</h3>
        <p>{content}</p>
    </div>
    """

def create_inventory_chart_container(title, chart_content):
    """
    Create a styled chart container.
    
    Args:
        title (str): Chart title
        chart_content (str): Chart HTML content
    
    Returns:
        str: HTML for the chart container
    """
    return f"""
    <div class="chart-container">
        <h3>{title}</h3>
        {chart_content}
    </div>
    """

def create_inventory_data_table(title, table_content):
    """
    Create a styled data table container.
    
    Args:
        title (str): Table title
        table_content (str): Table HTML content
    
    Returns:
        str: HTML for the data table container
    """
    return f"""
    <div class="data-table">
        <h3>{title}</h3>
        {table_content}
    </div>
    """

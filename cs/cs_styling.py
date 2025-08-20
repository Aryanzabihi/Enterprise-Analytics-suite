import streamlit as st

def load_custom_css():
    """Load custom CSS styling for the customer service dashboard with unified typography"""
    st.markdown("""
    <style>
    /* ===== UNIFIED TYPOGRAPHY SYSTEM ===== */
    
    /* Base font settings for consistency */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Streamlit default text elements */
    .stMarkdown, .stText, .stDataFrame, .stPlotlyChart {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* ===== HEADER TYPOGRAPHY ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    .main-header h2 {
        margin: 0;
        font-size: 2rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    .main-header p {
        margin: 10px 0 0 0;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    /* ===== SUBHEADER TYPOGRAPHY ===== */
    .stSubheader, h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #2c3e50 !important;
        margin: 1.5rem 0 1rem 0 !important;
        line-height: 1.3;
    }
    
    /* ===== TAB TYPOGRAPHY ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #2c3e50 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* ===== METRIC CARDS TYPOGRAPHY ===== */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem !important;
        font-weight: 500 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        opacity: 0.9;
        line-height: 1.2;
    }
    
    .metric-card h2 {
        margin: 0;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        line-height: 1.2;
    }
    
    .metric-card p {
        margin: 5px 0 0 0;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        opacity: 0.8;
        line-height: 1.3;
    }
    
    /* ===== INSIGHT BOXES TYPOGRAPHY ===== */
    .insight-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .insight-box h3 {
        margin: 0 0 1rem 0;
        color: #495057;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.3;
    }
    
    .insight-box p {
        margin: 0.5rem 0;
        color: #6c757d;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.4;
    }
    
    .insight-box ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .insight-box li {
        color: #6c757d;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.4;
        margin: 0.25rem 0;
    }
    
    /* ===== STATUS INDICATORS TYPOGRAPHY ===== */
    .status-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    
    .status-resolved {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    
    .status-pending {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
    }
    
    .status-escalated {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
    }
    
    .status-open {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        color: white;
    }
    
    /* ===== PRIORITY INDICATORS TYPOGRAPHY ===== */
    .priority-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    
    /* ===== CHART CONTAINERS TYPOGRAPHY ===== */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    .chart-container h4 {
        margin: 0 0 1rem 0;
        color: #2c3e50;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.3;
    }
    
    /* ===== DATA TABLE TYPOGRAPHY ===== */
    .data-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .data-table th {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #2c3e50 !important;
    }
    
    .data-table td {
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #495057 !important;
    }
    
    /* ===== BUTTON TYPOGRAPHY ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        transition: all 0.3s ease;
        line-height: 1.2;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* ===== SIDEBAR TYPOGRAPHY ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .css-1d391kg .stMarkdown {
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* ===== METRIC DISPLAY TYPOGRAPHY ===== */
    .metric-display {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    
    .metric-display h4 {
        margin: 0 0 0.5rem 0;
        color: #495057;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.2;
    }
    
    .metric-display p {
        margin: 0;
        color: #6c757d;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.3;
    }
    
    /* ===== ALERT TYPOGRAPHY ===== */
    .alert-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* ===== PROGRESS BARS TYPOGRAPHY ===== */
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* ===== TOOLTIP TYPOGRAPHY ===== */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.3;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem !important;
        }
        
        .main-header h2 {
            font-size: 1.5rem !important;
        }
        
        .main-header p {
            font-size: 1rem !important;
        }
        
        .metric-card h2 {
            font-size: 1.5rem !important;
        }
        
        .stSubheader, h3 {
            font-size: 1.3rem !important;
        }
    }
    
    /* ===== ANIMATION CLASSES ===== */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* ===== STREAMLIT SPECIFIC OVERRIDES ===== */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #2c3e50 !important;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown div {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        line-height: 1.4;
    }
    
    /* ===== PLOTLY CHART TYPOGRAPHY ===== */
    .js-plotly-plot .plotly .main-svg {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* ===== DATAFRAME TYPOGRAPHY ===== */
    .dataframe {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* ===== UNIFIED COLOR SCHEME ===== */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --info-color: #17a2b8;
        --light-color: #f8f9fa;
        --dark-color: #2c3e50;
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --text-muted: #adb5bd;
    }
    </style>
    """, unsafe_allow_html=True)

def create_status_badge(status, status_type="status"):
    """Create a styled status or priority badge with consistent typography"""
    if status_type == "status":
        if status.lower() in ["resolved", "closed", "completed"]:
            return f'<span class="status-indicator status-resolved">{status}</span>'
        elif status.lower() in ["pending", "in progress", "open"]:
            return f'<span class="status-indicator status-pending">{status}</span>'
        elif status.lower() in ["escalated", "urgent"]:
            return f'<span class="status-indicator status-escalated">{status}</span>'
        else:
            return f'<span class="status-indicator status-open">{status}</span>'
    elif status_type == "priority":
        if status.lower() in ["high", "critical", "urgent"]:
            return f'<span class="priority-indicator priority-high">{status}</span>'
        elif status.lower() in ["medium", "normal"]:
            return f'<span class="priority-indicator priority-medium">{status}</span>'
        else:
            return f'<span class="priority-indicator priority-low">{status}</span>'
    else:
        return f'<span class="status-indicator status-info">{status}</span>'

def create_metric_card(title, value, subtitle="", color="#667eea", icon="📊"):
    """Create a metric card with consistent typography"""
    return f"""
    <div class="metric-card" style="background: {color};">
        <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
        <h2 style="margin: 0; font-size: 1.8rem; font-weight: 600; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{value}</h2>
        <h3 style="margin: 5px 0 0 0; font-size: 1rem; font-weight: 500; opacity: 0.9;">{title}</h3>
        {f'<p style="margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;">{subtitle}</p>' if subtitle else ''}
    </div>
    """

def create_insight_box(title, content, icon="💡"):
    """Create a styled insight box"""
    return f"""
    <div class="insight-box slide-in">
        <h3>{icon} {title}</h3>
        <p>{content}</p>
    </div>
    """

def create_alert_box(message, alert_type="info"):
    """Create an alert box with consistent typography"""
    alert_classes = {
        "success": "alert-success",
        "warning": "alert-warning", 
        "error": "alert-error",
        "info": "alert-info"
    }
    
    alert_class = alert_classes.get(alert_type, "alert-info")
    
    return f"""
    <div class="{alert_class}">
        <p style="margin: 0; font-size: 0.95rem; font-weight: 400; line-height: 1.4;">{message}</p>
    </div>
    """

def create_progress_bar(percentage, label=""):
    """Create a styled progress bar"""
    return f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%"></div>
    </div>
    {f'<p style="text-align: center; margin: 0.25rem 0; font-size: 0.9rem; color: #6c757d;">{label}</p>' if label else ''}
    """

def create_tooltip(text, tooltip_text):
    """Create a tooltip element"""
    return f"""
    <div class="tooltip">
        {text}
        <span class="tooltiptext">{tooltip_text}</span>
    </div>
    """

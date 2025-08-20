#!/usr/bin/env python3
"""
Customer Service Analytics Dashboard - Main Application
=====================================================

This is the main entry point for the Customer Service Analytics Dashboard.
It provides navigation and integrates all analytics modules with unified typography.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import page modules - lazy loading for better performance
from cs_data_utils import initialize_session_state, get_data_summary
from cs_styling import load_custom_css, create_metric_card, create_alert_box
from typography_config import apply_typography_to_streamlit

# Page configuration
st.set_page_config(
    page_title="Customer Service Analytics Dashboard",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load unified styling and typography
load_custom_css()
apply_typography_to_streamlit()

# Cache the main navigation to avoid re-rendering
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_navigation_buttons():
    """Get navigation buttons with consistent styling"""
    return [
        ("🏠 Home Dashboard", "🏠 Home Dashboard"),
        ("📝 Data Input & Management", "📝 Data Input & Management"),
        ("😊 Customer Satisfaction", "😊 Customer Satisfaction"),
        ("⚡ Response & Resolution", "⚡ Response & Resolution"),
        ("🔧 Service Efficiency", "🔧 Service Efficiency"),
        ("👥 Agent Performance", "👥 Agent Performance"),
        ("📊 Customer Retention", "📊 Customer Retention"),
        ("💼 Business Impact", "💼 Business Impact"),
        ("💬 Interaction Analysis", "💬 Interaction Analysis"),
        ("🌐 Omnichannel Experience", "🌐 Omnichannel Experience"),
        ("🔮 Predictive Analytics", "🔮 Predictive Analytics")
    ]

def create_sidebar():
    """Create optimized sidebar with navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h2 style="margin: 0; color: white; font-size: 1.5rem; font-weight: 600;">🎧 Customer Service Analytics</h2>
            <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9rem;">Select a section to explore</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create navigation buttons efficiently
        nav_buttons = get_navigation_buttons()
        for button_text, page_name in nav_buttons:
            if st.button(button_text, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
        
        # Developer attribution at the bottom of sidebar
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px 0; opacity: 0.7;">
            <p style="margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);">
                Developed by <strong>Aryan Zabihi</strong>
            </p>
            <div style="margin-top: 10px;">
                <a href="https://github.com/aryanzabihi" target="_blank" style="color: rgba(255,255,255,0.8); text-decoration: none; margin: 0 10px;">
                    GitHub
                </a>
                <span style="color: rgba(255,255,255,0.5);">•</span>
                <a href="https://linkedin.com/in/aryanzabihi" target="_blank" style="color: rgba(255,255,255,0.8); text-decoration: none; margin: 0 10px;">
                    LinkedIn
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_page_content():
    """Get page content based on current selection - optimized for performance"""
    page = st.session_state.get('current_page', "🏠 Home Dashboard")
    
    # Use lazy loading for page modules to improve startup time
    if page == "🏠 Home Dashboard":
        from cs_pages.home_page import show_home
        return show_home()
    
    elif page == "📝 Data Input & Management":
        from cs_pages.data_input_page import show_data_input
        return show_data_input()
    
    elif page == "😊 Customer Satisfaction":
        from cs_pages.customer_satisfaction_page import show_customer_satisfaction
        return show_customer_satisfaction()
    
    elif page == "⚡ Response & Resolution":
        from cs_pages.response_resolution_page import show_response_resolution
        return show_response_resolution()
    
    elif page == "🔧 Service Efficiency":
        return show_service_efficiency()
    
    elif page == "👥 Agent Performance":
        return show_agent_performance()
    
    elif page == "📊 Customer Retention":
        return show_customer_retention()
    
    elif page == "💼 Business Impact":
        return show_business_impact()
    
    elif page == "💬 Interaction Analysis":
        return show_interaction_analysis()
    
    elif page == "🌐 Omnichannel Experience":
        return show_omnichannel_experience()
    
    elif page == "🔮 Predictive Analytics":
        return show_predictive_analytics()

def show_service_efficiency():
    """Display service efficiency analytics - optimized"""
    # Check if we have data efficiently
    if st.session_state.get('tickets', pd.DataFrame()).empty:
        st.warning("⚠️ No ticket data available. Please add ticket data in the Data Input tab.")
        return
    
    # Import and use the redesigned service efficiency page
    from cs_pages.service_efficiency_page import show_service_efficiency as show_redesigned_efficiency
    show_redesigned_efficiency()

def show_agent_performance():
    """Display enhanced agent performance analytics - optimized"""
    from cs_pages.agent_performance_page import show_agent_performance as show_enhanced_agent_performance
    show_enhanced_agent_performance()

def show_customer_retention():
    """Display enhanced customer retention analytics - optimized"""
    from cs_pages.customer_retention_page import show_customer_retention as show_enhanced_customer_retention
    show_enhanced_customer_retention()

def show_business_impact():
    """Display enhanced business impact analytics - optimized"""
    from cs_pages.business_impact_page import show_business_impact as show_enhanced_business_impact
    show_enhanced_business_impact()

def show_interaction_analysis():
    """Display enhanced interaction analysis - optimized"""
    from cs_pages.interaction_analysis_page import show_interaction_analysis as show_enhanced_interaction_analysis
    show_enhanced_interaction_analysis()

def show_omnichannel_experience():
    """Display enhanced omnichannel experience analytics - optimized"""
    from cs_pages.omnichannel_experience_page import show_omnichannel_experience as show_enhanced_omnichannel_experience
    show_enhanced_omnichannel_experience()

def show_predictive_analytics():
    """Display enhanced predictive analytics - optimized"""
    from cs_pages.predictive_analytics_page import show_predictive_analytics as show_enhanced_predictive_analytics
    show_enhanced_predictive_analytics()

def create_footer():
    """Create optimized footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; opacity: 0.7;">
        <p style="margin: 0; font-size: 0.9rem; font-weight: 400; color: #6c757d;">🎧 Customer Service Analytics Dashboard | Built with Streamlit</p>
        <p style="margin: 5px 0 0 0; font-size: 0.8rem; font-weight: 400; color: #adb5bd;">Comprehensive analytics for customer service excellence</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function - optimized for performance with unified typography"""
    
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar
    create_sidebar()
    
    # Initialize current page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home Dashboard"
    
    # Get page content
    get_page_content()
    
    # Create footer
    create_footer()

if __name__ == "__main__":
    main()

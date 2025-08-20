#!/usr/bin/env python3
"""
Enhanced Business Impact Analytics Page
=======================================

This page implements advanced business impact analytics with:
- Dynamic, interactive visualizations
- Real-time business metrics
- Advanced analytics and insights
- Interactive charts and graphs
- Revenue impact analysis
- Customer value analysis
- Business performance tracking
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import calendar

def show_business_impact():
    """Display enhanced business impact analytics"""
    
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">💼 Business Impact Analytics</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Measure and analyze the business impact of customer service operations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.customers.empty or st.session_state.tickets.empty:
        st.warning("⚠️ No customer or ticket data available. Please add data in the Data Input tab.")
        return
    
    # Create enhanced business impact dashboard
    create_enhanced_business_dashboard()

def create_enhanced_business_dashboard():
    """Create enhanced business impact dashboard"""
    
    # Create main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Business Overview", 
        "💰 Revenue Impact", 
        "👥 Customer Value", 
        "📈 Performance Trends", 
        "🎯 Strategic Insights", 
        "🚀 Growth Analytics"
    ])
    
    with tab1:
        create_business_overview_dashboard()
    
    with tab2:
        create_revenue_impact_dashboard()
    
    with tab3:
        create_customer_value_dashboard()
    
    with tab4:
        create_performance_trends_dashboard()
    
    with tab5:
        create_strategic_insights_dashboard()
    
    with tab6:
        create_growth_analytics_dashboard()

def create_business_overview_dashboard():
    """Create business overview dashboard"""
    
    st.subheader("📊 Business Impact Overview")
    
    # Calculate business metrics
    business_metrics = calculate_business_metrics()
    
    # Display KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_animated_metric_card(
            "Total Revenue Impact",
            f"${business_metrics.get('total_revenue', 0):,.0f}",
            "💰",
            business_metrics.get('revenue_trend', 0),
            "green" if business_metrics.get('revenue_trend', 0) > 0 else "red"
        )
    
    with col2:
        create_animated_metric_card(
            "Customer Lifetime Value",
            f"${business_metrics.get('avg_clv', 0):,.0f}",
            "👤",
            business_metrics.get('clv_trend', 0),
            "green" if business_metrics.get('clv_trend', 0) > 0 else "red"
        )
    
    with col3:
        create_animated_metric_card(
            "Service ROI",
            f"{business_metrics.get('service_roi', 0):.1f}%",
            "📈",
            business_metrics.get('roi_trend', 0),
            "green" if business_metrics.get('roi_trend', 0) > 0 else "red"
        )
    
    with col4:
        create_animated_metric_card(
            "Customer Acquisition Cost",
            f"${business_metrics.get('cac', 0):,.0f}",
            "🎯",
            business_metrics.get('cac_trend', 0),
            "red" if business_metrics.get('cac_trend', 0) > 0 else "green"
        )
    
    st.markdown("---")
    
    # Business impact distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Revenue Distribution by Segment")
        create_revenue_distribution_chart()
    
    with col2:
        st.subheader("🎯 Customer Value Distribution")
        create_customer_value_distribution_chart()
    
    # Business performance summary
    st.subheader("📋 Business Performance Summary")
    create_business_performance_summary()

def create_revenue_impact_dashboard():
    """Create revenue impact dashboard"""
    
    st.subheader("💰 Revenue Impact Analysis")
    
    # Revenue trends over time
    st.subheader("📈 Revenue Trends")
    create_revenue_trends_chart()
    
    st.markdown("---")
    
    # Revenue breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Revenue by Customer Segment")
        create_revenue_by_segment_chart()
    
    with col2:
        st.subheader("🔄 Revenue by Service Type")
        create_revenue_by_service_chart()
    
    # Revenue optimization insights
    st.subheader("🚀 Revenue Optimization Insights")
    create_revenue_optimization_insights()

def create_customer_value_dashboard():
    """Create customer value dashboard"""
    
    st.subheader("👥 Customer Value Analysis")
    
    # Customer value metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_animated_metric_card(
            "High-Value Customers",
            f"{calculate_high_value_customers()}",
            "⭐",
            0,
            "green"
        )
    
    with col2:
        create_animated_metric_card(
            "Average Order Value",
            f"${calculate_avg_order_value():,.0f}",
            "🛒",
            0,
            "blue"
        )
    
    with col3:
        create_animated_metric_card(
            "Customer Retention Rate",
            f"{calculate_customer_retention_rate():.1f}%",
            "🔄",
            0,
            "green"
        )
    
    st.markdown("---")
    
    # Customer value analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Customer Value Segmentation")
        create_customer_value_segmentation_chart()
    
    with col2:
        st.subheader("🎯 Value vs Retention Correlation")
        create_value_retention_correlation_chart()
    
    # Customer value insights
    st.subheader("💡 Customer Value Insights")
    create_customer_value_insights()

def create_performance_trends_dashboard():
    """Create performance trends dashboard"""
    
    st.subheader("📈 Performance Trends Analysis")
    
    # Performance trends over time
    st.subheader("🔄 Monthly Performance Trends")
    create_monthly_performance_trends_chart()
    
    st.markdown("---")
    
    # Performance breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Performance by Channel")
        create_performance_by_channel_chart()
    
    with col2:
        st.subheader("🎯 Performance by Agent")
        create_performance_by_agent_chart()
    
    # Performance insights
    st.subheader("🔍 Performance Insights")
    create_performance_insights()

def create_strategic_insights_dashboard():
    """Create strategic insights dashboard"""
    
    st.subheader("🎯 Strategic Business Insights")
    
    # Strategic recommendations
    st.subheader("💡 Strategic Recommendations")
    create_strategic_recommendations()
    
    st.markdown("---")
    
    # Business impact analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Business Impact Factors")
        create_business_impact_factors_chart()
    
    with col2:
        st.subheader("🎯 Opportunity Analysis")
        create_opportunity_analysis_chart()
    
    # Strategic planning
    st.subheader("📋 Strategic Planning Insights")
    create_strategic_planning_insights()

def create_growth_analytics_dashboard():
    """Create growth analytics dashboard"""
    
    st.subheader("🚀 Growth Analytics")
    
    # Growth metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_animated_metric_card(
            "Growth Rate",
            f"{calculate_growth_rate():.1f}%",
            "📈",
            0,
            "green"
        )
    
    with col2:
        create_animated_metric_card(
            "Market Share",
            f"{calculate_market_share():.1f}%",
            "🌍",
            0,
            "blue"
        )
    
    with col3:
        create_animated_metric_card(
            "Expansion Rate",
            f"{calculate_expansion_rate():.1f}%",
            "🚀",
            0,
            "green"
        )
    
    with col4:
        create_animated_metric_card(
            "Innovation Index",
            f"{calculate_innovation_index():.1f}",
            "💡",
            0,
            "purple"
        )
    
    st.markdown("---")
    
    # Growth analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Growth Trajectory")
        create_growth_trajectory_chart()
    
    with col2:
        st.subheader("🎯 Growth Opportunities")
        create_growth_opportunities_chart()
    
    # Growth insights
    st.subheader("🔮 Growth Insights & Predictions")
    create_growth_insights()

# Helper functions for creating visualizations and components

def create_animated_metric_card(title, value, icon, trend, color):
    """Create animated metric card"""
    
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

def create_revenue_distribution_chart():
    """Create revenue distribution chart"""
    
    try:
        # Sample data - replace with actual data processing
        segments = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
        revenue = [45000, 32000, 18000, 8000]
        
        fig = go.Figure(data=[go.Pie(
            labels=segments,
            values=revenue,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            textinfo='label+percent+value',
            hovertemplate='Segment: %{label}<br>Revenue: $%{value:,.0f}<extra></extra>'
        )])
        
        fig.update_layout(
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Revenue distribution data will be displayed here when available")

def create_customer_value_distribution_chart():
    """Create customer value distribution chart"""
    
    try:
        # Sample data - replace with actual data processing
        value_ranges = ['$0-1K', '$1K-5K', '$5K-10K', '$10K+']
        customer_counts = [120, 85, 45, 30]
        
        fig = go.Figure(data=[go.Bar(
            x=value_ranges,
            y=customer_counts,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=customer_counts,
            textposition='auto',
            hovertemplate='Value Range: %{x}<br>Customers: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Customer Value Distribution",
            xaxis_title="Customer Value Range",
            yaxis_title="Number of Customers",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Customer value distribution data will be displayed here when available")

def create_business_performance_summary():
    """Create business performance summary"""
    
    try:
        # Sample data - replace with actual data processing
        summary_data = {
            'Metric': [
                'Total Customers',
                'Active Customers',
                'Revenue per Customer',
                'Customer Satisfaction',
                'Service Efficiency',
                'Business Growth Rate'
            ],
            'Value': [
                '280',
                '245',
                '$1,250',
                '4.2/5.0',
                '87.5%',
                '+12.3%'
            ],
            'Status': [
                '✅',
                '✅',
                '✅',
                '⚠️',
                '✅',
                '✅'
            ]
        }
        
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.info("📋 Business performance summary will be displayed here when available")

def create_revenue_trends_chart():
    """Create revenue trends chart"""
    
    try:
        # Sample data - replace with actual data processing
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [85000, 92000, 88000, 95000, 102000, 98000]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8, color='#4ECDC4')
        ))
        
        fig.update_layout(
            title="Monthly Revenue Trends",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📈 Revenue trends data will be displayed here when available")

def create_revenue_by_segment_chart():
    """Create revenue by segment chart"""
    
    try:
        # Sample data - replace with actual data processing
        segments = ['Enterprise', 'Mid-Market', 'SMB', 'Startup']
        revenue = [45000, 32000, 18000, 8000]
        
        fig = go.Figure(data=[go.Bar(
            x=segments,
            y=revenue,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'${r:,.0f}' for r in revenue],
            textposition='auto',
            hovertemplate='Segment: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Revenue by Customer Segment",
            xaxis_title="Customer Segment",
            yaxis_title="Revenue ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("💵 Revenue by segment data will be displayed here when available")

def create_revenue_by_service_chart():
    """Create revenue by service chart"""
    
    try:
        # Sample data - replace with actual data processing
        services = ['Support', 'Consulting', 'Training', 'Implementation']
        revenue = [35000, 28000, 22000, 15000]
        
        fig = go.Figure(data=[go.Bar(
            x=services,
            y=revenue,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'${r:,.0f}' for r in revenue],
            textposition='auto',
            hovertemplate='Service: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Revenue by Service Type",
            xaxis_title="Service Type",
            yaxis_title="Revenue ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("🔄 Revenue by service data will be displayed here when available")

def create_revenue_optimization_insights():
    """Create revenue optimization insights"""
    
    st.markdown("""
    ### 💡 Revenue Optimization Insights
    
    **High-Value Opportunities:**
    - Enterprise customers show 3.2x higher revenue potential
    - Consulting services have 25% higher margins
    - Q2 shows strongest seasonal revenue patterns
    
    **Optimization Strategies:**
    - Focus on upselling to existing enterprise customers
    - Expand consulting service offerings
    - Implement seasonal pricing strategies
    - Develop customer success programs for SMB segment
    """)

def create_customer_value_segmentation_chart():
    """Create customer value segmentation chart"""
    
    try:
        # Sample data - replace with actual data processing
        segments = ['Platinum', 'Gold', 'Silver', 'Bronze']
        customers = [25, 45, 120, 90]
        
        fig = go.Figure(data=[go.Bar(
            x=segments,
            y=customers,
            marker_color=['#FFD700', '#C0C0C0', '#CD7F32', '#8B4513'],
            text=customers,
            textposition='auto',
            hovertemplate='Segment: %{x}<br>Customers: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Customer Value Segmentation",
            xaxis_title="Value Tier",
            yaxis_title="Number of Customers",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Customer value segmentation data will be displayed here when available")

def create_value_retention_correlation_chart():
    """Create value vs retention correlation chart"""
    
    try:
        # Sample data - replace with actual data processing
        value_tiers = ['Platinum', 'Gold', 'Silver', 'Bronze']
        retention_rates = [95, 88, 75, 62]
        
        fig = go.Figure(data=[go.Scatter(
            x=value_tiers,
            y=retention_rates,
            mode='lines+markers',
            name='Retention Rate',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=10, color='#4ECDC4')
        )])
        
        fig.update_layout(
            title="Customer Value vs Retention Correlation",
            xaxis_title="Customer Value Tier",
            yaxis_title="Retention Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("🎯 Value vs retention correlation data will be displayed here when available")

def create_customer_value_insights():
    """Create customer value insights"""
    
    st.markdown("""
    ### 💡 Customer Value Insights
    
    **High-Value Customer Characteristics:**
    - Platinum customers have 95% retention rate
    - Gold customers show 3.5x higher lifetime value
    - Enterprise customers prefer consulting services
    
    **Value Optimization Strategies:**
    - Implement tiered customer success programs
    - Develop personalized upselling strategies
    - Focus on customer education and training
    - Create exclusive benefits for high-value segments
    """)

def create_monthly_performance_trends_chart():
    """Create monthly performance trends chart"""
    
    try:
        # Sample data - replace with actual data processing
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        satisfaction = [4.1, 4.2, 4.0, 4.3, 4.4, 4.2]
        efficiency = [82, 85, 83, 87, 89, 87]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=satisfaction,
            mode='lines+markers',
            name='Customer Satisfaction',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8, color='#4ECDC4')
        ))
        fig.add_trace(go.Scatter(
            x=months,
            y=[e/10 for e in efficiency],  # Scale efficiency to 0-5 range
            mode='lines+markers',
            name='Service Efficiency',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8, color='#FF6B6B')
        ))
        
        fig.update_layout(
            title="Monthly Performance Trends",
            xaxis_title="Month",
            yaxis_title="Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📈 Performance trends data will be displayed here when available")

def create_performance_by_channel_chart():
    """Create performance by channel chart"""
    
    try:
        # Sample data - replace with actual data processing
        channels = ['Phone', 'Email', 'Chat', 'Portal']
        satisfaction = [4.3, 4.1, 4.4, 4.2]
        
        fig = go.Figure(data=[go.Bar(
            x=channels,
            y=satisfaction,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'{s:.1f}' for s in satisfaction],
            textposition='auto',
            hovertemplate='Channel: %{x}<br>Satisfaction: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Performance by Channel",
            xaxis_title="Communication Channel",
            yaxis_title="Customer Satisfaction Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Performance by channel data will be displayed here when available")

def create_performance_by_agent_chart():
    """Create performance by agent chart"""
    
    try:
        # Sample data - replace with actual data processing
        agents = ['Agent A', 'Agent B', 'Agent C', 'Agent D', 'Agent E']
        performance = [92, 88, 95, 87, 91]
        
        fig = go.Figure(data=[go.Bar(
            x=agents,
            y=performance,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFA07A'],
            text=[f'{p}%' for p in performance],
            textposition='auto',
            hovertemplate='Agent: %{x}<br>Performance: %{y}%<extra></extra>'
        )])
        
        fig.update_layout(
            title="Agent Performance Comparison",
            xaxis_title="Agent",
            yaxis_title="Performance Score (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("🎯 Performance by agent data will be displayed here when available")

def create_performance_insights():
    """Create performance insights"""
    
    st.markdown("""
    ### 🔍 Performance Insights
    
    **Key Performance Trends:**
    - Customer satisfaction improved 7.3% over 6 months
    - Service efficiency shows consistent upward trend
    - Chat channel performs best for customer satisfaction
    - Agent performance varies by 8% across team
    
    **Performance Optimization:**
    - Implement chat-first strategy for high-priority issues
    - Share best practices from top-performing agents
    - Focus on email response quality improvement
    - Develop agent training programs based on performance gaps
    """)

def create_strategic_recommendations():
    """Create strategic recommendations"""
    
    st.markdown("""
    ### 💡 Strategic Business Recommendations
    
    **Immediate Actions (0-3 months):**
    1. **Customer Segmentation Strategy**: Implement tiered service levels for different customer segments
    2. **Revenue Optimization**: Focus on upselling consulting services to enterprise customers
    3. **Performance Improvement**: Develop agent training programs based on performance analysis
    
    **Medium-term Initiatives (3-6 months):**
    1. **Channel Optimization**: Invest in chat and portal capabilities for better customer experience
    2. **Customer Success Programs**: Develop comprehensive customer success initiatives
    3. **Data Analytics**: Implement advanced analytics for predictive insights
    
    **Long-term Strategy (6-12 months):**
    1. **Market Expansion**: Explore new customer segments and geographic markets
    2. **Service Innovation**: Develop new service offerings based on customer needs
    3. **Technology Integration**: Implement AI-powered customer service solutions
    """)

def create_business_impact_factors_chart():
    """Create business impact factors chart"""
    
    try:
        # Sample data - replace with actual data processing
        factors = ['Customer Satisfaction', 'Response Time', 'Resolution Rate', 'Agent Performance']
        impact_score = [85, 78, 92, 88]
        
        fig = go.Figure(data=[go.Bar(
            x=factors,
            y=impact_score,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'{s}%' for s in impact_score],
            textposition='auto',
            hovertemplate='Factor: %{x}<br>Impact Score: %{y}%<extra></extra>'
        )])
        
        fig.update_layout(
            title="Business Impact Factors",
            xaxis_title="Impact Factor",
            yaxis_title="Impact Score (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Business impact factors data will be displayed here when available")

def create_opportunity_analysis_chart():
    """Create opportunity analysis chart"""
    
    try:
        # Sample data - replace with actual data processing
        opportunities = ['Upselling', 'Cross-selling', 'Customer Expansion', 'New Markets']
        potential_value = [45000, 32000, 28000, 35000]
        
        fig = go.Figure(data=[go.Bar(
            x=opportunities,
            y=potential_value,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'${v:,.0f}' for v in potential_value],
            textposition='auto',
            hovertemplate='Opportunity: %{x}<br>Potential Value: $%{y:,.0f}<extra></extra>'
        )])
        
        fig.update_layout(
            title="Business Opportunity Analysis",
            xaxis_title="Opportunity Type",
            yaxis_title="Potential Value ($)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("🎯 Opportunity analysis data will be displayed here when available")

def create_strategic_planning_insights():
    """Create strategic planning insights"""
    
    st.markdown("""
    ### 📋 Strategic Planning Insights
    
    **Market Position Analysis:**
    - Strong position in enterprise segment with 45% market share
    - Growing presence in mid-market with 28% growth rate
    - Opportunity to expand in SMB segment with targeted offerings
    
    **Competitive Advantages:**
    - High customer satisfaction scores (4.2/5.0)
    - Strong customer retention rates (87.5%)
    - Efficient service delivery (87.5% efficiency)
    - Diverse service portfolio covering multiple customer needs
    
    **Strategic Priorities:**
    1. **Customer Experience**: Maintain high satisfaction while scaling operations
    2. **Revenue Growth**: Focus on high-value customer segments and services
    3. **Operational Excellence**: Continue improving efficiency and performance
    4. **Market Expansion**: Explore new customer segments and geographic markets
    """)

def create_growth_trajectory_chart():
    """Create growth trajectory chart"""
    
    try:
        # Sample data - replace with actual data processing
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        growth_rate = [8.5, 12.3, 15.7, 18.2]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quarters,
            y=growth_rate,
            mode='lines+markers',
            name='Growth Rate',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=10, color='#4ECDC4')
        ))
        
        fig.update_layout(
            title="Business Growth Trajectory",
            xaxis_title="Quarter",
            yaxis_title="Growth Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("📊 Growth trajectory data will be displayed here when available")

def create_growth_opportunities_chart():
    """Create growth opportunities chart"""
    
    try:
        # Sample data - replace with actual data processing
        opportunities = ['Market Expansion', 'Product Development', 'Customer Acquisition', 'Service Innovation']
        growth_potential = [85, 72, 68, 78]
        
        fig = go.Figure(data=[go.Bar(
            x=opportunities,
            y=growth_potential,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
            text=[f'{p}%' for p in growth_potential],
            textposition='auto',
            hovertemplate='Opportunity: %{x}<br>Growth Potential: %{y}%<extra></extra>'
        )])
        
        fig.update_layout(
            title="Growth Opportunities Analysis",
            xaxis_title="Growth Opportunity",
            yaxis_title="Growth Potential (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.info("🎯 Growth opportunities data will be displayed here when available")

def create_growth_insights():
    """Create growth insights"""
    
    st.markdown("""
    ### 🔮 Growth Insights & Predictions
    
    **Current Growth Drivers:**
    - Strong customer retention driving recurring revenue
    - High customer satisfaction leading to referrals
    - Efficient service delivery enabling scale
    - Diverse service portfolio meeting various customer needs
    
    **Growth Predictions:**
    - **Q3 2024**: Expected 15-18% growth based on current pipeline
    - **Q4 2024**: Potential 18-22% growth with new service launches
    - **2025**: Projected 25-30% annual growth rate
    
    **Growth Strategies:**
    1. **Market Penetration**: Increase market share in existing segments
    2. **Market Development**: Expand into new geographic markets
    3. **Product Development**: Launch new service offerings
    4. **Diversification**: Enter new customer segments and markets
    """)

# Data calculation functions

def calculate_business_metrics():
    """Calculate business metrics"""
    
    try:
        # Sample metrics - replace with actual calculations
        return {
            'total_revenue': 103000,
            'revenue_trend': 12.3,
            'avg_clv': 1250,
            'clv_trend': 8.5,
            'service_roi': 87.5,
            'roi_trend': 5.2,
            'cac': 450,
            'cac_trend': -3.1
        }
    except Exception as e:
        return {
            'total_revenue': 0,
            'revenue_trend': 0,
            'avg_clv': 0,
            'clv_trend': 0,
            'service_roi': 0,
            'roi_trend': 0,
            'cac': 0,
            'cac_trend': 0
        }

def calculate_high_value_customers():
    """Calculate high-value customers count"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 70
    except Exception as e:
        return 0

def calculate_avg_order_value():
    """Calculate average order value"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 1250
    except Exception as e:
        return 0

def calculate_customer_retention_rate():
    """Calculate customer retention rate"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 87.5
    except Exception as e:
        return 0

def calculate_growth_rate():
    """Calculate business growth rate"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 12.3
    except Exception as e:
        return 0

def calculate_market_share():
    """Calculate market share"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 15.7
    except Exception as e:
        return 0

def calculate_expansion_rate():
    """Calculate expansion rate"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 18.2
    except Exception as e:
        return 0

def calculate_innovation_index():
    """Calculate innovation index"""
    
    try:
        # Sample calculation - replace with actual data processing
        return 7.8
    except Exception as e:
        return 0

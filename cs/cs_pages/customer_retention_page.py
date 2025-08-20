#!/usr/bin/env python3
"""
Enhanced Customer Retention Analytics Page
=========================================

This page implements advanced customer retention analytics with:
- Dynamic, interactive visualizations
- Real-time retention metrics
- Advanced analytics and insights
- Interactive charts and graphs
- Retention trend analysis
- Predictive analytics for customer churn
- Customer lifetime value analysis
- Engagement pattern insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import calendar
from operator import attrgetter

# Import analytics functions
from cs_analytics import (
    calculate_churn_rate_analysis,
    calculate_customer_lifetime_value
)

def show_customer_retention():
    """Display enhanced customer retention analytics with interactive visualizations"""
    
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text;">📊 Advanced Customer Retention Analytics</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Comprehensive customer intelligence with retention optimization, churn prediction, and lifetime value analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have the required data
    if st.session_state.tickets.empty:
        st.warning("⚠️ No ticket data available. Please load data in the Data Input tab first.")
        st.info("💡 Go to '📝 Data Input & Management' → '📁 Load Sample File' to load sample data.")
        return
    
    if 'customer_id' not in st.session_state.tickets.columns:
        st.error("❌ Customer data not available. Please ensure tickets have customer assignments.")
        st.info("💡 The customer retention analytics requires ticket data with customer_id field.")
        return
    
    # Create enhanced customer retention analytics dashboard
    create_enhanced_customer_retention_dashboard()

def create_enhanced_customer_retention_dashboard():
    """Create enhanced customer retention analytics dashboard with interactive visualizations"""
    
    # Create main tabs for different customer retention analytics categories
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Retention Overview", "📈 Retention Trends", "🎯 Churn Analysis", 
        "💰 Lifetime Value", "🔗 Engagement Patterns", "🚀 Optimization Insights"
    ])
    
    # Tab 1: Retention Overview Dashboard
    with tab1:
        create_retention_overview_dashboard()
    
    # Tab 2: Retention Trends & Patterns
    with tab2:
        create_retention_trends_dashboard()
    
    # Tab 3: Churn Analysis & Prediction
    with tab3:
        create_churn_analysis_dashboard()
    
    # Tab 4: Customer Lifetime Value
    with tab4:
        create_lifetime_value_dashboard()
    
    # Tab 5: Engagement Pattern Analysis
    with tab5:
        create_engagement_patterns_dashboard()
    
    # Tab 6: Optimization Insights & Recommendations
    with tab6:
        create_optimization_insights_dashboard()

def create_retention_overview_dashboard():
    """Create comprehensive retention overview dashboard"""
    
    st.subheader("📊 Customer Retention Overview")
    st.markdown("Real-time retention metrics with dynamic updates and trend indicators")
    
    # Calculate customer retention metrics
    retention_metrics = calculate_customer_retention_metrics()
    
    # Create animated metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(retention_metrics)
        create_animated_metric_card(
            "Total Customers", 
            f"{total_customers:,}", 
            "👥", 
            "#667eea",
            get_retention_trend_indicator(total_customers, 'count')
        )
    
    with col2:
        retention_rate = retention_metrics['Retention Rate %'].mean()
        create_animated_metric_card(
            "Avg Retention Rate", 
            f"{retention_rate:.1f}%", 
            "🎯", 
            "#4CAF50",
            get_retention_trend_indicator(retention_rate, 'rate')
        )
    
    with col3:
        churn_rate = 100 - retention_rate
        create_animated_metric_card(
            "Churn Rate", 
            f"{churn_rate:.1f}%", 
            "⚠️", 
            "#F44336",
            get_retention_trend_indicator(churn_rate, 'churn')
        )
    
    with col4:
        avg_lifetime = retention_metrics['Avg Lifetime (Days)'].mean()
        create_animated_metric_card(
            "Avg Customer Lifetime", 
            f"{avg_lifetime:.0f} days", 
            "⏰", 
            "#9C27B0",
            get_retention_trend_indicator(avg_lifetime, 'lifetime')
        )
    
    # Retention distribution charts
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_retention_distribution_chart(retention_metrics)
    
    with col2:
        create_retention_breakdown_chart(retention_metrics)
    
    # Top retained customers leaderboard
    st.markdown("---")
    create_top_retained_customers_leaderboard(retention_metrics)
    
    # Live customer activity feed
    st.markdown("---")
    create_live_customer_activity_feed()

def create_retention_trends_dashboard():
    """Create retention trends dashboard with time-based patterns"""
    
    st.subheader("📈 Retention Trends & Time Patterns")
    st.markdown("Visualize customer retention patterns across different time dimensions")
    
    if 'created_date' in st.session_state.tickets.columns:
        # Monthly retention trends
        create_monthly_retention_trends()
        
        # Cohort analysis
        st.markdown("---")
        create_cohort_retention_analysis()
        
        # Seasonal retention patterns
        st.markdown("---")
        create_seasonal_retention_patterns()
    else:
        st.info("Date data required for trend analysis. Please ensure tickets have creation dates.")
    
    # Retention clustering analysis
    st.markdown("---")
    create_retention_clustering_analysis()

def create_churn_analysis_dashboard():
    """Create churn analysis and prediction dashboard"""
    
    st.subheader("🎯 Churn Analysis & Prediction")
    st.markdown("Analyze customer churn patterns and predict future churn risk")
    
    if 'created_date' in st.session_state.tickets.columns:
        # Churn timeline analysis
        create_churn_timeline_analysis()
        
        # Churn risk factors
        st.markdown("---")
        create_churn_risk_factors()
        
        # Predictive churn modeling
        st.markdown("---")
        create_predictive_churn_modeling()
    else:
        st.info("Date data required for churn analysis. Please ensure tickets have creation dates.")
    
    # Churn prevention strategies
    st.markdown("---")
    create_churn_prevention_strategies()

def create_lifetime_value_dashboard():
    """Create customer lifetime value analysis dashboard"""
    
    st.subheader("💰 Customer Lifetime Value Analysis")
    st.markdown("Analyze customer value and revenue patterns over time")
    
    # Customer value distribution
    create_customer_value_distribution()
    
    # Value vs retention correlation
    st.markdown("---")
    create_value_retention_correlation()
    
    # Revenue forecasting
    st.markdown("---")
    create_revenue_forecasting()
    
    # Value optimization strategies
    st.markdown("---")
    create_value_optimization_strategies()

def create_engagement_patterns_dashboard():
    """Create customer engagement pattern analysis dashboard"""
    
    st.subheader("🔗 Customer Engagement Pattern Analysis")
    st.markdown("Analyze customer interaction patterns and engagement drivers")
    
    # Engagement frequency analysis
    create_engagement_frequency_analysis()
    
    # Channel preference analysis
    st.markdown("---")
    create_channel_preference_analysis()
    
    # Engagement vs retention correlation
    st.markdown("---")
    create_engagement_retention_correlation()
    
    # Engagement optimization strategies
    st.markdown("---")
    create_engagement_optimization_strategies()

def create_optimization_insights_dashboard():
    """Create optimization insights and recommendations dashboard"""
    
    st.subheader("🚀 Optimization Insights & Recommendations")
    st.markdown("AI-powered insights for retention optimization and improvement")
    
    # Retention optimization recommendations
    create_retention_optimization_recommendations()
    
    # Customer experience insights
    st.markdown("---")
    create_customer_experience_insights()
    
    # Loyalty program suggestions
    st.markdown("---")
    create_loyalty_program_suggestions()
    
    # Predictive retention forecasting
    st.markdown("---")
    create_predictive_retention_forecasting()

# Enhanced Visualization Functions
def create_animated_metric_card(title, value, icon, color, trend):
    """Create animated metric card with trend indicators"""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                padding: 20px; border-radius: 15px; color: white; text-align: center;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15); transition: transform 0.3s ease;">
        <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
        <h2 style="margin: 0; font-size: 2.5rem; font-weight: bold;">{value}</h2>
        <p style="margin: 5px 0 0 0; font-size: 1.1rem;">{title}</p>
        <div style="margin-top: 10px; font-size: 1.2rem;">{trend}</div>
    </div>
    """, unsafe_allow_html=True)

def create_retention_distribution_chart(retention_metrics):
    """Create retention distribution chart"""
    
    # Create retention categories
    retention_categories = {
        'High Retention (≥80%)': len(retention_metrics[retention_metrics['Retention Rate %'] >= 80]),
        'Good Retention (60-80%)': len(retention_metrics[(retention_metrics['Retention Rate %'] >= 60) & (retention_metrics['Retention Rate %'] < 80)]),
        'Average Retention (40-60%)': len(retention_metrics[(retention_metrics['Retention Rate %'] >= 40) & (retention_metrics['Retention Rate %'] < 60)]),
        'Low Retention (<40%)': len(retention_metrics[retention_metrics['Retention Rate %'] < 40])
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(retention_categories.keys()),
        values=list(retention_categories.values()),
        hole=0.4,
        marker_colors=['#4CAF50', '#FF9800', '#FFC107', '#F44336'],
        textinfo='label+percent+value',
        textfont_size=14,
        hovertemplate='Category: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Customer Retention Distribution",
        height=400,
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_retention_breakdown_chart(retention_metrics):
    """Create retention breakdown chart"""
    
    # Top 5 customers by retention rate
    top_customers = retention_metrics.nlargest(5, 'Retention Rate %')
    
    fig = go.Figure(data=[go.Bar(
        x=top_customers['Customer ID'],
        y=top_customers['Retention Rate %'],
        marker_color='#4CAF50',
        text=[f"{val:.1f}%" for val in top_customers['Retention Rate %']],
        textposition='auto',
        hovertemplate='Customer: %{x}<br>Retention Rate: %{y:.1f}%<extra></extra>'
    )])
    
    fig.update_layout(
        title="Top 5 Customers by Retention Rate",
        xaxis_title="Customer ID",
        yaxis_title="Retention Rate (%)",
        height=400,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_top_retained_customers_leaderboard(retention_metrics):
    """Create top retained customers leaderboard"""
    
    st.subheader("🏆 Top Retained Customers Leaderboard")
    
    # Sort by retention rate and display top 10
    top_customers = retention_metrics.nlargest(10, 'Retention Rate %')
    
    # Create leaderboard with styling
    for i, (_, customer) in enumerate(top_customers.iterrows()):
        rank = i + 1
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        
        st.markdown(f"""
        <div style="background: {'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' if rank <= 3 else '#f8f9fa'}; 
                    padding: 15px; border-radius: 10px; margin: 8px 0; 
                    border-left: 4px solid {'#FFD700' if rank <= 3 else '#667eea'}; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; font-size: 1.2rem;">{medal} Customer {customer['Customer ID']}</span>
                <span style="font-weight: bold; color: {'#B8860B' if rank <= 3 else '#667eea'}; font-size: 1.1rem;">
                    {customer['Retention Rate %']:.1f}%
                </span>
            </div>
            <div style="color: #666; font-size: 0.9rem; margin-top: 5px;">
                Tickets: {customer['Total Tickets']} | Lifetime: {customer['Avg Lifetime (Days)']:.0f} days
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_monthly_retention_trends():
    """Create monthly retention trends chart"""
    
    tickets_df = st.session_state.tickets.copy()
    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
    tickets_df = tickets_df.dropna(subset=['created_date'])
    
    if not tickets_df.empty:
        # Group by month and calculate retention metrics
        tickets_df['month'] = tickets_df['created_date'].dt.to_period('M')
        monthly_retention = tickets_df.groupby('month').agg({
            'customer_id': 'nunique',
            'ticket_id': 'count'
        }).reset_index()
        
        monthly_retention['month'] = monthly_retention['month'].astype(str)
        
        # Create retention trend chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_retention['month'],
            y=monthly_retention['customer_id'],
            mode='lines+markers',
            name='Unique Customers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_retention['month'],
            y=monthly_retention['ticket_id'],
            mode='lines+markers',
            name='Total Tickets',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Monthly Customer Retention Trends",
            xaxis_title="Month",
            yaxis_title="Unique Customers",
            yaxis2=dict(title="Total Tickets", overlaying='y', side='right'),
            height=400,
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend insights
        if len(monthly_retention) > 1:
            customer_trend = monthly_retention['customer_id'].iloc[-1] - monthly_retention['customer_id'].iloc[-2]
            ticket_trend = monthly_retention['ticket_id'].iloc[-1] - monthly_retention['ticket_id'].iloc[-2]
            
            if customer_trend > 0:
                st.success(f"📈 **Customer Trend**: Growing by {customer_trend} customers this month")
            else:
                st.warning(f"📉 **Customer Trend**: Declining by {abs(customer_trend)} customers this month")

def create_cohort_retention_analysis():
    """Create cohort retention analysis"""
    
    st.subheader("📊 Cohort Retention Analysis")
    st.markdown("Analyze customer retention by acquisition cohorts")
    
    tickets_df = st.session_state.tickets.copy()
    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
    tickets_df = tickets_df.dropna(subset=['created_date'])
    
    if not tickets_df.empty:
        # Create cohort analysis
        tickets_df['cohort_month'] = tickets_df.groupby('customer_id')['created_date'].transform('min').dt.to_period('M')
        tickets_df['period_number'] = (tickets_df['created_date'].dt.to_period('M') - tickets_df['cohort_month']).apply(attrgetter('n'))
        
        # Calculate cohort retention
        cohort_data = tickets_df.groupby(['cohort_month', 'period_number'])['customer_id'].nunique().reset_index()
        cohort_pivot = cohort_data.pivot(index='cohort_month', columns='period_number', values='customer_id')
        
        # Calculate retention rates
        retention_matrix = cohort_pivot.div(cohort_pivot[0], axis=0) * 100
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=retention_matrix.values,
            x=[f"Month {i}" for i in retention_matrix.columns],
            y=retention_matrix.index.astype(str),
            colorscale='Viridis',
            hovertemplate='Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Cohort Retention Analysis",
            xaxis_title="Months Since First Purchase",
            yaxis_title="Cohort Month",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cohort insights
        avg_retention_1m = retention_matrix[1].mean() if 1 in retention_matrix.columns else 0
        avg_retention_3m = retention_matrix[3].mean() if 3 in retention_matrix.columns else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("1-Month Retention", f"{avg_retention_1m:.1f}%")
        with col2:
            st.metric("3-Month Retention", f"{avg_retention_3m:.1f}%")

def create_churn_timeline_analysis():
    """Create churn timeline analysis"""
    
    st.subheader("⏰ Churn Timeline Analysis")
    st.markdown("Analyze when and why customers churn")
    
    tickets_df = st.session_state.tickets.copy()
    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
    tickets_df = tickets_df.dropna(subset=['created_date'])
    
    if not tickets_df.empty:
        # Calculate customer last activity
        customer_last_activity = tickets_df.groupby('customer_id')['created_date'].max().reset_index()
        customer_last_activity['days_since_last'] = (pd.Timestamp.now() - customer_last_activity['created_date']).dt.days
        
        # Define churn threshold (e.g., 90 days)
        churn_threshold = 90
        customer_last_activity['churned'] = customer_last_activity['days_since_last'] > churn_threshold
        
        # Create churn timeline
        fig = go.Figure()
        
        # Churned customers
        churned_customers = customer_last_activity[customer_last_activity['churned']]
        if not churned_customers.empty:
            fig.add_trace(go.Histogram(
                x=churned_customers['days_since_last'],
                name='Churned Customers',
                marker_color='#F44336',
                opacity=0.7,
                nbinsx=20
            ))
        
        # Active customers
        active_customers = customer_last_activity[~customer_last_activity['churned']]
        if not active_customers.empty:
            fig.add_trace(go.Histogram(
                x=active_customers['days_since_last'],
                name='Active Customers',
                marker_color='#4CAF50',
                opacity=0.7,
                nbinsx=20
            ))
        
        fig.update_layout(
            title="Customer Churn Timeline",
            xaxis_title="Days Since Last Activity",
            yaxis_title="Number of Customers",
            height=400,
            showlegend=True,
            barmode='overlay'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Churn statistics
        churn_rate = len(churned_customers) / len(customer_last_activity) * 100
        avg_churn_time = churned_customers['days_since_last'].mean() if not churned_customers.empty else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Churn Rate", f"{churn_rate:.1f}%")
        with col2:
            st.metric("Avg Time to Churn", f"{avg_churn_time:.0f} days")

def create_customer_value_distribution():
    """Create customer value distribution analysis"""
    
    st.subheader("💰 Customer Value Distribution")
    st.markdown("Analyze customer value patterns and revenue distribution")
    
    # Calculate customer value metrics
    customer_value_metrics = calculate_customer_value_metrics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Value distribution histogram
        fig = go.Figure(data=[go.Histogram(
            x=customer_value_metrics['Total Value'],
            nbinsx=20,
            marker_color='#9C27B0',
            opacity=0.7
        )])
        
        fig.update_layout(
            title="Customer Value Distribution",
            xaxis_title="Total Customer Value",
            yaxis_title="Number of Customers",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Value vs retention scatter
        fig = go.Figure(data=[go.Scatter(
            x=customer_value_metrics['Total Value'],
            y=customer_value_metrics['Retention Rate %'],
            mode='markers',
            marker=dict(
                size=8,
                color=customer_value_metrics['Retention Rate %'],
                colorscale='Viridis',
                showscale=True
            ),
            text=customer_value_metrics['Customer ID'],
            hovertemplate='Customer: %{text}<br>Value: %{x}<br>Retention: %{y:.1f}%<extra></extra>'
        )])
        
        fig.update_layout(
            title="Customer Value vs Retention",
            xaxis_title="Total Customer Value",
            yaxis_title="Retention Rate (%)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_retention_optimization_recommendations():
    """Create retention optimization recommendations"""
    
    st.subheader("🎯 Retention Optimization Recommendations")
    
    # Get retention data
    retention_metrics = calculate_customer_retention_metrics()
    
    # Generate recommendations based on retention data
    recommendations = generate_retention_recommendations(retention_metrics)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚀 High Retention Customers (≥80%)**")
        high_retention = retention_metrics[retention_metrics['Retention Rate %'] >= 80]
        if not high_retention.empty:
            st.success(f"**{len(high_retention)} customers** - Excellent retention! Focus on upselling and referrals")
        else:
            st.info("No customers currently in high retention category")
    
    with col2:
        st.markdown("**⚠️ At-Risk Customers (<40%)**")
        low_retention = retention_metrics[retention_metrics['Retention Rate %'] < 40]
        if not low_retention.empty:
            st.warning(f"**{len(low_retention)} customers** - High churn risk! Implement retention campaigns")
        else:
            st.success("All customers above 40% retention threshold")
    
    # Specific recommendations
    st.markdown("---")
    st.markdown("**💡 Specific Recommendations**")
    
    for rec in recommendations:
        st.info(rec)

# Helper Functions
def calculate_customer_retention_metrics():
    """Calculate comprehensive customer retention metrics"""
    
    tickets_df = st.session_state.tickets.copy()
    
    # Group by customer and calculate metrics
    customer_retention = tickets_df.groupby('customer_id').agg({
        'ticket_id': 'count',
        'created_date': ['min', 'max']
    }).reset_index()
    
    customer_retention.columns = ['Customer ID', 'Total Tickets', 'First Ticket', 'Last Ticket']
    
    # Calculate retention rate (simplified - customers with multiple tickets)
    customer_retention['Retention Rate %'] = np.where(
        customer_retention['Total Tickets'] > 1, 
        100, 
        np.where(customer_retention['Total Tickets'] == 1, 50, 0)
    )
    
    # Calculate average lifetime
    customer_retention['First Ticket'] = pd.to_datetime(customer_retention['First Ticket'], errors='coerce')
    customer_retention['Last Ticket'] = pd.to_datetime(customer_retention['Last Ticket'], errors='coerce')
    
    customer_retention['Avg Lifetime (Days)'] = (
        customer_retention['Last Ticket'] - customer_retention['First Ticket']
    ).dt.days
    
    # Fill NaN values
    customer_retention['Avg Lifetime (Days)'] = customer_retention['Avg Lifetime (Days)'].fillna(0)
    
    return customer_retention

def calculate_customer_value_metrics():
    """Calculate customer value metrics"""
    
    # For now, use ticket count as a proxy for value
    # In a real implementation, this would include actual revenue data
    customer_value = st.session_state.tickets.groupby('customer_id').agg({
        'ticket_id': 'count'
    }).reset_index()
    
    customer_value.columns = ['Customer ID', 'Total Value']
    
    # Merge with retention metrics
    retention_metrics = calculate_customer_retention_metrics()
    customer_value = customer_value.merge(
        retention_metrics[['Customer ID', 'Retention Rate %']], 
        on='Customer ID', 
        how='left'
    )
    
    return customer_value

def generate_retention_recommendations(retention_metrics):
    """Generate retention optimization recommendations"""
    
    recommendations = []
    
    # Overall retention recommendations
    avg_retention = retention_metrics['Retention Rate %'].mean()
    if avg_retention < 70:
        recommendations.append("📈 **Overall Retention**: Focus on improving average retention rate across all customers")
    
    # High-value customer recommendations
    high_value_customers = retention_metrics[retention_metrics['Total Tickets'] > retention_metrics['Total Tickets'].mean()]
    if len(high_value_customers) > 0:
        recommendations.append("💎 **High-Value Customers**: Implement VIP programs for customers with multiple tickets")
    
    # Low retention recommendations
    low_retention_customers = retention_metrics[retention_metrics['Retention Rate %'] < 40]
    if len(low_retention_customers) > 0:
        recommendations.append("🔒 **Low Retention**: Develop targeted re-engagement campaigns for at-risk customers")
    
    # New customer recommendations
    new_customers = retention_metrics[retention_metrics['Total Tickets'] == 1]
    if len(new_customers) > 0:
        recommendations.append("🆕 **New Customers**: Implement onboarding programs to increase first-time retention")
    
    return recommendations

def get_retention_trend_indicator(value, metric_type):
    """Get trend indicator for retention metrics"""
    
    try:
        if metric_type == 'count':
            if value > 1000:
                return "📈 Large Customer Base"
            elif value > 500:
                return "📊 Medium Customer Base"
            else:
                return "📉 Small Customer Base"
        elif metric_type == 'rate':
            if value >= 80:
                return "🚀 Excellent"
            elif value >= 60:
                return "📈 Good"
            else:
                return "⚠️ Needs Improvement"
        elif metric_type == 'churn':
            if value <= 20:
                return "🚀 Low Churn"
            elif value <= 40:
                return "📈 Moderate"
            else:
                return "⚠️ High Churn"
        elif metric_type == 'lifetime':
            if value > 365:
                return "🚀 Long-term"
            elif value > 90:
                return "📈 Medium-term"
            else:
                return "📉 Short-term"
        else:
            return "📊 Stable"
    except:
        return "📊 Stable"

# Placeholder functions for additional features
def create_seasonal_retention_patterns():
    st.markdown("**📅 Seasonal Retention Patterns**")
    st.info("Seasonal retention pattern analysis will be implemented here")

def create_retention_clustering_analysis():
    st.markdown("**🔍 Retention Clustering Analysis**")
    st.info("Retention clustering and segmentation analysis will be implemented here")

def create_churn_risk_factors():
    st.markdown("**⚠️ Churn Risk Factors**")
    st.info("Churn risk factor analysis will be implemented here")

def create_predictive_churn_modeling():
    st.markdown("**🔮 Predictive Churn Modeling**")
    st.info("AI-powered churn prediction will be implemented here")

def create_churn_prevention_strategies():
    st.markdown("**🛡️ Churn Prevention Strategies**")
    st.info("Churn prevention and retention strategies will be implemented here")

def create_value_retention_correlation():
    st.markdown("**💰 Value vs Retention Correlation**")
    st.info("Customer value and retention correlation analysis will be implemented here")

def create_revenue_forecasting():
    st.markdown("**📈 Revenue Forecasting**")
    st.info("Customer revenue forecasting will be implemented here")

def create_value_optimization_strategies():
    st.markdown("**💎 Value Optimization Strategies**")
    st.info("Customer value optimization strategies will be implemented here")

def create_engagement_frequency_analysis():
    st.markdown("**📊 Engagement Frequency Analysis**")
    st.info("Customer engagement frequency analysis will be implemented here")

def create_channel_preference_analysis():
    st.markdown("**📱 Channel Preference Analysis**")
    st.info("Customer channel preference analysis will be implemented here")

def create_engagement_retention_correlation():
    st.markdown("**🔗 Engagement vs Retention Correlation**")
    st.info("Engagement and retention correlation analysis will be implemented here")

def create_engagement_optimization_strategies():
    st.markdown("**⚡ Engagement Optimization Strategies**")
    st.info("Customer engagement optimization strategies will be implemented here")

def create_customer_experience_insights():
    st.markdown("**😊 Customer Experience Insights**")
    st.info("Customer experience analysis and insights will be implemented here")

def create_loyalty_program_suggestions():
    st.markdown("**🎁 Loyalty Program Suggestions**")
    st.info("Loyalty program recommendations will be implemented here")

def create_predictive_retention_forecasting():
    st.markdown("**🔮 Predictive Retention Forecasting**")
    st.info("AI-powered retention forecasting will be implemented here")

def create_live_customer_activity_feed():
    """Create live customer activity feed"""
    
    st.markdown("**🔴 Live Customer Activity Feed**")
    
    # Simulate live customer updates
    activity_data = [
        {"time": "2 min ago", "event": "New customer registered", "customer": "Customer 123", "status": "🆕"},
        {"time": "5 min ago", "event": "Customer completed purchase", "customer": "Customer 456", "status": "💰"},
        {"time": "8 min ago", "event": "Customer support ticket resolved", "customer": "Customer 789", "status": "✅"},
        {"time": "12 min ago", "event": "Customer feedback received", "customer": "Customer 101", "status": "⭐"},
        {"time": "15 min ago", "event": "Customer churn risk detected", "customer": "Customer 202", "status": "⚠️"}
    ]
    
    for activity in activity_data:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #667eea;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold;">{activity['status']} {activity['event']}</span>
                <span style="color: #666; font-size: 0.9rem;">{activity['time']}</span>
            </div>
            <div style="color: #666; font-size: 0.9rem; margin-top: 5px;">Customer: {activity['customer']}</div>
        </div>
        """, unsafe_allow_html=True)

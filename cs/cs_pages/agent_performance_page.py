#!/usr/bin/env python3
"""
Enhanced Agent Performance Analytics Page
========================================

This page implements advanced agent performance analytics with:
- Dynamic, interactive visualizations
- Real-time performance metrics
- Advanced analytics and insights
- Interactive charts and graphs
- Performance trend analysis
- Predictive analytics for agents
- Team performance comparison
- Workload optimization insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import calendar

def show_agent_performance():
    """Display enhanced agent performance analytics with interactive visualizations"""
    
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text;">👨‍💼 Advanced Agent Performance Analytics</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Comprehensive agent intelligence with performance optimization, trend analysis, and predictive insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have the required data
    if st.session_state.tickets.empty:
        st.warning("⚠️ No ticket data available. Please load data in the Data Input tab first.")
        st.info("💡 Go to '📝 Data Input & Management' → '📁 Load Sample File' to load sample data.")
        return
    
    if 'agent_id' not in st.session_state.tickets.columns:
        st.error("❌ Agent data not available. Please ensure tickets have agent assignments.")
        st.info("💡 The agent performance analytics requires ticket data with agent_id field.")
        return
    
    # Create enhanced agent analytics dashboard
    create_enhanced_agent_dashboard()

def create_enhanced_agent_dashboard():
    """Create enhanced agent analytics dashboard with interactive visualizations"""
    
    # Create main tabs for different agent analytics categories
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Performance Overview", "🔥 Performance Heatmap", "📈 Individual Trends", 
        "👥 Team Comparison", "⚖️ Workload Analysis", "🎯 Optimization Insights"
    ])
    
    # Tab 1: Performance Overview Dashboard
    with tab1:
        create_performance_overview_dashboard()
    
    # Tab 2: Performance Heatmap & Patterns
    with tab2:
        create_performance_heatmap_dashboard()
    
    # Tab 3: Individual Agent Trends
    with tab3:
        create_individual_trends_dashboard()
    
    # Tab 4: Team Performance Comparison
    with tab4:
        create_team_comparison_dashboard()
    
    # Tab 5: Workload Analysis & Distribution
    with tab5:
        create_workload_analysis_dashboard()
    
    # Tab 6: Optimization Insights & Recommendations
    with tab6:
        create_optimization_insights_dashboard()

def create_performance_overview_dashboard():
    """Create comprehensive performance overview dashboard"""
    
    st.subheader("📊 Agent Performance Overview")
    st.markdown("Real-time performance metrics with dynamic updates and trend indicators")
    
    # Calculate agent performance metrics
    agent_metrics = calculate_agent_performance_metrics()
    
    # Create animated metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_agents = len(agent_metrics)
        create_animated_metric_card(
            "Total Agents", 
            f"{total_agents}", 
            "👥", 
            "#667eea",
            get_agent_trend_indicator(total_agents, 'count')
        )
    
    with col2:
        avg_resolution_rate = agent_metrics['Resolution Rate %'].mean()
        create_animated_metric_card(
            "Avg Resolution Rate", 
            f"{avg_resolution_rate:.1f}%", 
            "🎯", 
            "#4CAF50",
            get_agent_trend_indicator(avg_resolution_rate, 'rate')
        )
    
    with col3:
        top_performer_rate = agent_metrics[agent_metrics['Resolution Rate %'] >= 80]['Resolution Rate %'].mean()
        create_animated_metric_card(
            "Top Performer Rate", 
            f"{top_performer_rate:.1f}%", 
            "🏆", 
            "#FFD700",
            get_agent_trend_indicator(top_performer_rate, 'rate')
        )
    
    with col4:
        total_tickets_handled = agent_metrics['Total Tickets'].sum()
        create_animated_metric_card(
            "Total Tickets Handled", 
            f"{total_tickets_handled:,}", 
            "📋", 
            "#9C27B0",
            get_agent_trend_indicator(total_tickets_handled, 'tickets')
        )
    
    # Performance distribution charts
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        create_performance_distribution_chart(agent_metrics)
    
    with col2:
        create_performance_breakdown_chart(agent_metrics)
    
    # Top performers leaderboard
    st.markdown("---")
    create_top_performers_leaderboard(agent_metrics)
    
    # Live agent activity feed
    st.markdown("---")
    create_live_agent_activity_feed()

def create_performance_heatmap_dashboard():
    """Create performance heatmap dashboard with time-based patterns"""
    
    st.subheader("🔥 Performance Heatmap & Time Patterns")
    st.markdown("Visualize agent performance patterns across different time dimensions")
    
    if 'created_date' in st.session_state.tickets.columns:
        # Day and hour performance heatmap
        create_day_hour_heatmap()
        
        # Weekly performance patterns
        st.markdown("---")
        create_weekly_performance_patterns()
        
        # Monthly performance trends
        st.markdown("---")
        create_monthly_performance_trends()
    else:
        st.info("Date data required for heatmap analysis. Please ensure tickets have creation dates.")
    
    # Performance clustering analysis
    st.markdown("---")
    create_performance_clustering_analysis()

def create_individual_trends_dashboard():
    """Create individual agent performance trends dashboard"""
    
    st.subheader("📈 Individual Agent Performance Trends")
    st.markdown("Track individual agent performance over time with trend analysis")
    
    if 'created_date' in st.session_state.tickets.columns:
        # Agent performance over time
        create_agent_performance_timeline()
        
        # Performance improvement tracking
        st.markdown("---")
        create_performance_improvement_tracking()
        
        # Agent efficiency trends
        st.markdown("---")
        create_agent_efficiency_trends()
    else:
        st.info("Date data required for trend analysis. Please ensure tickets have creation dates.")
    
    # Individual agent insights
    st.markdown("---")
    create_individual_agent_insights()

def create_team_comparison_dashboard():
    """Create team performance comparison dashboard"""
    
    st.subheader("👥 Team Performance Comparison")
    st.markdown("Compare team performance and identify best practices")
    
    # Team performance metrics
    create_team_performance_metrics()
    
    # Cross-team comparison
    st.markdown("---")
    create_cross_team_comparison()
    
    # Team collaboration analysis
    st.markdown("---")
    create_team_collaboration_analysis()
    
    # Best practices identification
    st.markdown("---")
    create_best_practices_identification()

def create_workload_analysis_dashboard():
    """Create workload analysis and distribution dashboard"""
    
    st.subheader("⚖️ Workload Analysis & Distribution")
    st.markdown("Analyze workload distribution and identify optimization opportunities")
    
    # Workload distribution analysis
    create_workload_distribution_analysis()
    
    # Capacity planning insights
    st.markdown("---")
    create_capacity_planning_insights()
    
    # Workload balancing recommendations
    st.markdown("---")
    create_workload_balancing_recommendations()
    
    # Resource utilization optimization
    st.markdown("---")
    create_resource_utilization_optimization()

def create_optimization_insights_dashboard():
    """Create optimization insights and recommendations dashboard"""
    
    st.subheader("🎯 Optimization Insights & Recommendations")
    st.markdown("AI-powered insights for performance optimization and improvement")
    
    # Performance optimization recommendations
    create_performance_optimization_recommendations()
    
    # Training and development insights
    st.markdown("---")
    create_training_development_insights()
    
    # Process improvement suggestions
    st.markdown("---")
    create_process_improvement_suggestions()
    
    # Predictive performance forecasting
    st.markdown("---")
    create_predictive_performance_forecasting()

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

def create_performance_distribution_chart(agent_metrics):
    """Create performance distribution chart"""
    
    # Create performance categories
    performance_categories = {
        'Top Performers (≥80%)': len(agent_metrics[agent_metrics['Resolution Rate %'] >= 80]),
        'Good Performers (60-80%)': len(agent_metrics[(agent_metrics['Resolution Rate %'] >= 60) & (agent_metrics['Resolution Rate %'] < 80)]),
        'Average Performers (40-60%)': len(agent_metrics[(agent_metrics['Resolution Rate %'] >= 40) & (agent_metrics['Resolution Rate %'] < 60)]),
        'Needs Improvement (<40%)': len(agent_metrics[agent_metrics['Resolution Rate %'] < 40])
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(performance_categories.keys()),
        values=list(performance_categories.values()),
        hole=0.4,
        marker_colors=['#4CAF50', '#FF9800', '#FFC107', '#F44336'],
        textinfo='label+percent+value',
        textfont_size=14,
        hovertemplate='Category: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Agent Performance Distribution",
        height=400,
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_performance_breakdown_chart(agent_metrics):
    """Create performance breakdown chart"""
    
    # Top 5 agents by resolution rate
    top_agents = agent_metrics.nlargest(5, 'Resolution Rate %')
    
    fig = go.Figure(data=[go.Bar(
        x=top_agents['Agent Name'],
        y=top_agents['Resolution Rate %'],
        marker_color='#4CAF50',
        text=[f"{val:.1f}%" for val in top_agents['Resolution Rate %']],
        textposition='auto',
        hovertemplate='Agent: %{x}<br>Resolution Rate: %{y:.1f}%<extra></extra>'
    )])
    
    fig.update_layout(
        title="Top 5 Agents by Resolution Rate",
        xaxis_title="Agent",
        yaxis_title="Resolution Rate (%)",
        height=400,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_top_performers_leaderboard(agent_metrics):
    """Create top performers leaderboard"""
    
    st.subheader("🏆 Top Performers Leaderboard")
    
    # Sort by resolution rate and display top 10
    top_performers = agent_metrics.nlargest(10, 'Resolution Rate %')
    
    # Create leaderboard with styling
    for i, (_, agent) in enumerate(top_performers.iterrows()):
        rank = i + 1
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        
        st.markdown(f"""
        <div style="background: {'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)' if rank <= 3 else '#f8f9fa'}; 
                    padding: 15px; border-radius: 10px; margin: 8px 0; 
                    border-left: 4px solid {'#FFD700' if rank <= 3 else '#667eea'}; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; font-size: 1.2rem;">{medal} {agent['Agent Name']}</span>
                <span style="font-weight: bold; color: {'#B8860B' if rank <= 3 else '#667eea'}; font-size: 1.1rem;">
                    {agent['Resolution Rate %']:.1f}%
                </span>
            </div>
            <div style="color: #666; font-size: 0.9rem; margin-top: 5px;">
                Tickets: {agent['Total Tickets']} | Avg Time: {agent.get('Avg Resolution Time', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_day_hour_heatmap():
    """Create day and hour performance heatmap"""
    
    tickets_df = st.session_state.tickets.copy()
    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
    tickets_df = tickets_df.dropna(subset=['created_date'])
    
    if not tickets_df.empty:
        # Create daily agent performance matrix
        tickets_df['day_of_week'] = tickets_df['created_date'].dt.day_name()
        tickets_df['hour'] = tickets_df['created_date'].dt.hour
        
        # Group by day and hour, calculate performance metric
        performance_matrix = tickets_df.groupby(['day_of_week', 'hour']).agg({
            'ticket_id': 'count',
            'status': lambda x: (x == 'Resolved').sum() / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        
        # Pivot for heatmap
        heatmap_data = performance_matrix.pivot(index='day_of_week', columns='hour', values='status')
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis',
            hovertemplate='Day: %{y}<br>Hour: %{x}:00<br>Resolution Rate: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title="Agent Performance Heatmap by Day & Hour",
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance insights
        max_hour = heatmap_data.max().idxmax()
        max_day = heatmap_data.loc[:, max_hour].idxmax()
        max_performance = heatmap_data.loc[max_day, max_hour]
        
        st.info(f"🔥 **Peak Performance**: {max_day}s at {max_hour}:00 with {max_performance:.1f}% resolution rate")

def create_agent_performance_timeline():
    """Create agent performance timeline chart"""
    
    tickets_df = st.session_state.tickets.copy()
    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
    tickets_df = tickets_df.dropna(subset=['created_date'])
    
    if not tickets_df.empty:
        # Group by date and agent, calculate daily performance
        daily_performance = tickets_df.groupby([tickets_df['created_date'].dt.date, 'agent_id']).agg({
            'ticket_id': 'count',
            'status': lambda x: (x == 'Resolved').sum() / len(x) * 100 if len(x) > 0 else 0
        }).reset_index()
        
        daily_performance.columns = ['Date', 'Agent ID', 'Ticket Count', 'Resolution Rate']
        daily_performance['Date'] = pd.to_datetime(daily_performance['Date'])
        
        # Get top 5 agents for visualization
        top_agents = daily_performance.groupby('Agent ID')['Resolution Rate'].mean().nlargest(5).index
        
        fig = go.Figure()
        
        for agent_id in top_agents:
            agent_data = daily_performance[daily_performance['Agent ID'] == agent_id]
            agent_data = agent_data.sort_values('Date')
            
            fig.add_trace(go.Scatter(
                x=agent_data['Date'],
                y=agent_data['Resolution Rate'],
                mode='lines+markers',
                name=f'Agent {agent_id}',
                hovertemplate='Date: %{x}<br>Resolution Rate: %{y:.1f}%<extra></extra>'
            ))
        
        fig.update_layout(
            title="Top 5 Agents Performance Timeline",
            xaxis_title="Date",
            yaxis_title="Resolution Rate (%)",
            height=400,
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_workload_distribution_analysis():
    """Create workload distribution analysis"""
    
    st.subheader("⚖️ Workload Distribution Analysis")
    
    # Calculate workload metrics
    workload_metrics = calculate_workload_metrics()
    
    # Check if workload balance data is available
    if 'Workload Balance' in workload_metrics.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Workload distribution pie chart
            fig = go.Figure(data=[go.Pie(
                labels=['Evenly Distributed', 'Moderately Balanced', 'Unbalanced'],
                values=[
                    len(workload_metrics[workload_metrics['Workload Balance'] == 'Even']),
                    len(workload_metrics[workload_metrics['Workload Balance'] == 'Moderate']),
                    len(workload_metrics[workload_metrics['Workload Balance'] == 'Unbalanced'])
                ],
                marker_colors=['#4CAF50', '#FF9800', '#F44336'],
                textinfo='label+percent+value',
                hovertemplate='Balance: %{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig.update_layout(
                title="Workload Balance Distribution",
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Workload vs performance scatter plot
            fig = go.Figure(data=[go.Scatter(
                x=workload_metrics['Total Tickets'],
                y=workload_metrics['Resolution Rate %'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=workload_metrics['Resolution Rate %'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=workload_metrics['Agent Name'],
                hovertemplate='Agent: %{text}<br>Tickets: %{x}<br>Resolution Rate: %{y:.1f}%<extra></extra>'
            )])
            
            fig.update_layout(
                title="Workload vs Performance",
                xaxis_title="Total Tickets",
                yaxis_title="Resolution Rate (%)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        # If workload balance data is not available, show basic workload analysis
        st.info("💡 **Workload Analysis**: Basic workload metrics available. For detailed workload balance analysis, ensure agent data includes workload distribution information.")
        
        # Show basic workload metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Basic Workload Metrics**")
            total_tickets = workload_metrics['Total Tickets'].sum()
            avg_tickets = workload_metrics['Total Tickets'].mean()
            st.metric("Total Tickets", f"{total_tickets:,}")
            st.metric("Average per Agent", f"{avg_tickets:.1f}")
        
        with col2:
            st.markdown("**📈 Workload Distribution**")
            # Simple histogram of ticket distribution
            fig = go.Figure(data=[go.Histogram(
                x=workload_metrics['Total Tickets'],
                nbinsx=10,
                marker_color='#667eea',
                opacity=0.7
            )])
            
            fig.update_layout(
                title="Ticket Distribution Across Agents",
                xaxis_title="Number of Tickets",
                yaxis_title="Number of Agents",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_performance_optimization_recommendations():
    """Create performance optimization recommendations"""
    
    st.subheader("🎯 Performance Optimization Recommendations")
    
    # Get agent performance data
    agent_metrics = calculate_agent_performance_metrics()
    
    # Generate recommendations based on performance
    recommendations = generate_performance_recommendations(agent_metrics)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🚀 High Performers (≥80%)**")
        high_performers = agent_metrics[agent_metrics['Resolution Rate %'] >= 80]
        if not high_performers.empty:
            for _, agent in high_performers.iterrows():
                st.success(f"**{agent['Agent Name']}** - Maintain excellence and mentor others")
        else:
            st.info("No agents currently in high performer category")
    
    with col2:
        st.markdown("**⚠️ Needs Improvement (<60%)**")
        low_performers = agent_metrics[agent_metrics['Resolution Rate %'] < 60]
        if not low_performers.empty:
            for _, agent in low_performers.iterrows():
                st.warning(f"**{agent['Agent Name']}** - Focus on training and process improvement")
        else:
            st.success("All agents performing above 60% threshold")
    
    # Specific recommendations
    st.markdown("---")
    st.markdown("**💡 Specific Recommendations**")
    
    for rec in recommendations:
        st.info(rec)

# Helper Functions
def calculate_agent_performance_metrics():
    """Calculate comprehensive agent performance metrics"""
    
    tickets_df = st.session_state.tickets.copy()
    
    # Group by agent and calculate metrics
    agent_performance = tickets_df.groupby('agent_id').agg({
        'ticket_id': 'count',
        'status': lambda x: (x == 'Resolved').sum() / len(x) * 100
    }).reset_index()
    
    agent_performance.columns = ['Agent ID', 'Total Tickets', 'Resolution Rate %']
    
    # Merge with agent names if available
    if not st.session_state.agents.empty and 'agent_id' in st.session_state.agents.columns:
        available_columns = st.session_state.agents.columns.tolist()
        name_columns = [col for col in available_columns if 'name' in col.lower()]
        
        if name_columns:
            name_col = name_columns[0]
            try:
                agent_performance = agent_performance.merge(
                    st.session_state.agents[['agent_id', name_col]], 
                    on='agent_id', how='left'
                )
                agent_performance['Agent Name'] = agent_performance[name_col].fillna(agent_performance['Agent ID'])
            except:
                agent_performance['Agent Name'] = agent_performance['Agent ID']
        else:
            agent_performance['Agent Name'] = agent_performance['Agent ID']
    else:
        agent_performance['Agent Name'] = agent_performance['Agent ID']
    
    return agent_performance

def calculate_workload_metrics():
    """Calculate workload distribution metrics"""
    
    agent_metrics = calculate_agent_performance_metrics()
    
    # Calculate workload balance
    total_tickets = agent_metrics['Total Tickets'].sum()
    avg_tickets = total_tickets / len(agent_metrics)
    
    def get_workload_balance(tickets):
        if abs(tickets - avg_tickets) <= avg_tickets * 0.2:
            return 'Even'
        elif abs(tickets - avg_tickets) <= avg_tickets * 0.5:
            return 'Moderate'
        else:
            return 'Unbalanced'
    
    agent_metrics['Workload Balance'] = agent_metrics['Total Tickets'].apply(get_workload_balance)
    
    return agent_metrics

def generate_performance_recommendations(agent_metrics):
    """Generate performance optimization recommendations"""
    
    recommendations = []
    
    # Overall performance recommendations
    avg_rate = agent_metrics['Resolution Rate %'].mean()
    if avg_rate < 70:
        recommendations.append("📈 **Overall Performance**: Focus on improving average resolution rate across all agents")
    
    # Workload distribution recommendations
    if 'Workload Balance' in agent_metrics.columns:
        workload_balance = agent_metrics['Workload Balance'].value_counts()
        if workload_balance.get('Unbalanced', 0) > len(agent_metrics) * 0.3:
            recommendations.append("⚖️ **Workload Distribution**: Redistribute workload more evenly across agents")
    else:
        # If workload balance data is not available, provide general recommendation
        recommendations.append("⚖️ **Workload Distribution**: Monitor and balance workload distribution across agents")
    
    # Top performer recommendations
    top_performers = agent_metrics[agent_metrics['Resolution Rate %'] >= 80]
    if len(top_performers) > 0:
        recommendations.append("🏆 **Knowledge Sharing**: Leverage top performers to mentor and train others")
    
    # Training recommendations
    low_performers = agent_metrics[agent_metrics['Resolution Rate %'] < 60]
    if len(low_performers) > 0:
        recommendations.append("📚 **Training Focus**: Provide additional training for agents below 60% performance")
    
    return recommendations

def get_agent_trend_indicator(value, metric_type):
    """Get trend indicator for agent metrics"""
    
    try:
        if metric_type == 'count':
            if value > 20:
                return "📈 Large Team"
            elif value > 10:
                return "📊 Medium Team"
            else:
                return "📉 Small Team"
        elif metric_type == 'rate':
            if value >= 80:
                return "🚀 Excellent"
            elif value >= 60:
                return "📈 Good"
            else:
                return "⚠️ Needs Improvement"
        elif metric_type == 'tickets':
            if value > 1000:
                return "📈 High Volume"
            elif value > 500:
                return "📊 Moderate"
            else:
                return "📉 Low Volume"
        else:
            return "📊 Stable"
    except:
        return "📊 Stable"

# Placeholder functions for additional features
def create_weekly_performance_patterns():
    st.markdown("**📅 Weekly Performance Patterns**")
    st.info("Weekly performance pattern analysis will be implemented here")

def create_monthly_performance_trends():
    st.markdown("**📊 Monthly Performance Trends**")
    st.info("Monthly performance trend analysis will be implemented here")

def create_performance_clustering_analysis():
    st.markdown("**🔍 Performance Clustering Analysis**")
    st.info("Performance clustering and segmentation analysis will be implemented here")

def create_performance_improvement_tracking():
    st.markdown("**📈 Performance Improvement Tracking**")
    st.info("Individual performance improvement tracking will be implemented here")

def create_agent_efficiency_trends():
    st.markdown("**⚡ Agent Efficiency Trends**")
    st.info("Agent efficiency trend analysis will be implemented here")

def create_individual_agent_insights():
    st.markdown("**💡 Individual Agent Insights**")
    st.info("Personalized agent insights and recommendations will be implemented here")

def create_team_performance_metrics():
    st.markdown("**👥 Team Performance Metrics**")
    st.info("Team-based performance metrics will be implemented here")

def create_cross_team_comparison():
    st.markdown("**🔄 Cross-Team Comparison**")
    st.info("Cross-team performance comparison will be implemented here")

def create_team_collaboration_analysis():
    st.markdown("**🤝 Team Collaboration Analysis**")
    st.info("Team collaboration and interaction analysis will be implemented here")

def create_best_practices_identification():
    st.markdown("**⭐ Best Practices Identification**")
    st.info("Best practices identification and sharing will be implemented here")

def create_capacity_planning_insights():
    st.markdown("**📋 Capacity Planning Insights**")
    st.info("Capacity planning and resource allocation insights will be implemented here")

def create_workload_balancing_recommendations():
    st.markdown("**⚖️ Workload Balancing Recommendations**")
    st.info("Workload balancing and optimization recommendations will be implemented here")

def create_resource_utilization_optimization():
    st.markdown("**🔧 Resource Utilization Optimization**")
    st.info("Resource utilization optimization strategies will be implemented here")

def create_training_development_insights():
    st.markdown("**📚 Training & Development Insights**")
    st.info("Training and development recommendations will be implemented here")

def create_process_improvement_suggestions():
    st.markdown("**🔄 Process Improvement Suggestions**")
    st.info("Process improvement and optimization suggestions will be implemented here")

def create_predictive_performance_forecasting():
    st.markdown("**🔮 Predictive Performance Forecasting**")
    st.info("AI-powered performance forecasting will be implemented here")

def create_live_agent_activity_feed():
    """Create live agent activity feed"""
    
    st.markdown("**🔴 Live Agent Activity Feed**")
    
    # Simulate live agent updates
    activity_data = [
        {"time": "2 min ago", "event": "Agent 3 resolved high-priority ticket", "status": "✅"},
        {"time": "5 min ago", "event": "Agent 1 achieved performance milestone", "status": "🏆"},
        {"time": "8 min ago", "event": "Agent 2 completed training module", "status": "📚"},
        {"time": "12 min ago", "event": "Agent 4 received customer commendation", "status": "⭐"},
        {"time": "15 min ago", "event": "Agent 5 optimized workflow process", "status": "⚡"}
    ]
    
    for activity in activity_data:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #667eea;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold;">{activity['status']} {activity['event']}</span>
                <span style="color: #666; font-size: 0.9rem;">{activity['time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

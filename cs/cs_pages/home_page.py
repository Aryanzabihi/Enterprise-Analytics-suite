import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from cs_metrics_calculator import *
from cs_data_utils import get_data_summary, validate_data_integrity
from cs_styling import create_metric_card, create_insight_box, create_alert_box
from datetime import datetime

def show_home():
    """Display the home page with overview and key metrics"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Check if data is loaded
    if (st.session_state.customers.empty and st.session_state.tickets.empty and 
        st.session_state.agents.empty and st.session_state.interactions.empty):
        
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #495057; margin-bottom: 1rem;">🎯 Welcome to Customer Service Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Get started by uploading your customer service data or generating sample data to explore the dashboard features.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); min-width: 200px;">
                    <h4 style="color: #495057; margin-bottom: 0.5rem;">📊 Upload Data</h4>
                    <p style="color: #6c757d; font-size: 0.9rem;">Upload Excel files with customer service data</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); min-width: 200px;">
                    <h4 style="color: #495057; margin-bottom: 0.5rem;">📝 Manual Entry</h4>
                    <p style="color: #6c757d; font-size: 0.9rem;">Add data manually for testing</p>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); min-width: 200px;">
                    <h4 style="color: #495057; margin-bottom: 0.5rem;">📋 Download Template</h4>
                    <p style="color: #6c757d; font-size: 0.9rem;">Get Excel template for data structure</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Upload Data", use_container_width=True):
                st.session_state.current_page = "📝 Data Input"
                st.rerun()
        
        with col2:
            if st.button("📝 Manual Entry", use_container_width=True):
                st.session_state.current_page = "📝 Data Input & Management"
                st.rerun()
        
        with col3:
            if st.button("📋 Download Template", use_container_width=True):
                from cs_data_utils import create_template_for_download
                template_data = create_template_for_download()
                st.download_button(
                    label="📥 Download Excel Template",
                    data=template_data,
                    file_name="customer_service_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        return
    
    # Data is loaded, show overview
    st.success("✅ Customer service data loaded successfully!")
    
    # Data summary
    data_summary = get_data_summary()
    
    # Key metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total Customers", 
            f"{data_summary.get('Customers', 0):,}",
            "Active customer base"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Total Tickets", 
            f"{data_summary.get('Tickets', 0):,}",
            "Support requests"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Active Agents", 
            f"{data_summary.get('Agents', 0):,}",
            "Support team size"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Interactions", 
            f"{data_summary.get('Interactions', 0):,}",
            "Customer touchpoints"
        ), unsafe_allow_html=True)
    
    # Data validation
    st.markdown("### 🔍 Data Quality Check")
    validation_results = validate_data_integrity()
    
    for result in validation_results:
        if "✅" in result:
            st.success(result)
        elif "⚠️" in result:
            st.warning(result)
        else:
            st.error(result)
    
    # Quick insights
    st.markdown("### 💡 Quick Insights")
    
    if not st.session_state.tickets.empty:
        # Ticket status distribution
        if 'status' in st.session_state.tickets.columns:
            status_counts = st.session_state.tickets['status'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Status pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=status_counts.index,
                    values=status_counts.values,
                    hole=0.4,
                    marker_colors=['#28a745', '#ffc107', '#dc3545', '#17a2b8']
                )])
                
                fig.update_layout(
                    title="Ticket Status Distribution",
                    height=300,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Status metrics
                total_tickets = len(st.session_state.tickets)
                resolved_tickets = len(st.session_state.tickets[st.session_state.tickets['status'].str.lower() == 'resolved'])
                resolution_rate = (resolved_tickets / total_tickets) * 100 if total_tickets > 0 else 0
                
                st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
                st.metric("Open Tickets", f"{total_tickets - resolved_tickets:,}")
                st.metric("Total Tickets", f"{total_tickets:,}")
    
    # Customer satisfaction overview
    if not st.session_state.feedback.empty and not st.session_state.customers.empty:
        st.markdown("### 😊 Customer Satisfaction Overview")
        
        # Calculate satisfaction metrics
        satisfaction_data, satisfaction_msg = calculate_customer_satisfaction_metrics(
            st.session_state.customers, 
            st.session_state.feedback, 
            st.session_state.tickets
        )
        
        if not satisfaction_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Satisfaction metrics table
                st.markdown("**Satisfaction Metrics**")
                st.dataframe(satisfaction_data, use_container_width=True, hide_index=True)
            
            with col2:
                # Rating distribution
                if 'rating' in st.session_state.feedback.columns:
                    rating_counts = st.session_state.feedback['rating'].value_counts().sort_index()
                    
                    fig = go.Figure(data=[go.Bar(
                        x=rating_counts.index,
                        y=rating_counts.values,
                        marker_color='#667eea'
                    )])
                    
                    fig.update_layout(
                        title="Customer Rating Distribution",
                        xaxis_title="Rating (1-5)",
                        yaxis_title="Number of Responses",
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # Agent performance overview
    if not st.session_state.agents.empty and not st.session_state.tickets.empty:
        st.markdown("### 👨‍💼 Agent Performance Overview")
        
        # Calculate agent performance metrics
        agent_performance, agent_msg = calculate_agent_performance_metrics(
            st.session_state.agents,
            st.session_state.tickets,
            st.session_state.feedback
        )
        
        if not agent_performance.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Agent performance table
                st.markdown("**Agent Performance Metrics**")
                st.dataframe(agent_performance, use_container_width=True, hide_index=True)
            
            with col2:
                # Top performers
                if 'agent_name' in agent_performance.columns and 'resolution_rate' in agent_performance.columns:
                    top_performers = agent_performance.head(5)
                    
                    fig = go.Figure(data=[go.Bar(
                        x=top_performers['agent_name'],
                        y=top_performers['resolution_rate'],
                        marker_color='#28a745'
                    )])
                    
                    fig.update_layout(
                        title="Top 5 Agents by Resolution Rate",
                        xaxis_title="Agent",
                        yaxis_title="Resolution Rate (%)",
                        height=300,
                        xaxis_tickangle=-45
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    
    if not st.session_state.tickets.empty and 'created_date' in st.session_state.tickets.columns:
        # Convert dates
        tickets_with_date = st.session_state.tickets.copy()
        tickets_with_date['created_date'] = pd.to_datetime(tickets_with_date['created_date'], errors='coerce')
        tickets_with_date = tickets_with_date.dropna(subset=['created_date'])
        
        if not tickets_with_date.empty:
            # Daily ticket volume
            daily_tickets = tickets_with_date.groupby(
                tickets_with_date['created_date'].dt.date
            ).size().reset_index(name='ticket_count')
            
            daily_tickets.columns = ['Date', 'Ticket Count']
            daily_tickets = daily_tickets.sort_values('Date').tail(30)  # Last 30 days
            
            fig = go.Figure(data=[go.Scatter(
                x=daily_tickets['Date'],
                y=daily_tickets['Ticket Count'],
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            )])
            
            fig.update_layout(
                title="Daily Ticket Volume (Last 30 Days)",
                xaxis_title="Date",
                yaxis_title="Number of Tickets",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Detailed Analytics", use_container_width=True):
            st.session_state.current_page = "😊 Customer Satisfaction"
            st.rerun()
    
    with col2:
        if st.button("📝 Manage Data", use_container_width=True):
            st.session_state.current_page = "📝 Data Input"
            st.rerun()
    
    with col3:
        if st.button("🔮 Predictive Analytics", use_container_width=True):
            st.session_state.current_page = "🔮 Predictive Analytics"
            st.rerun()
    
    # System information
    st.markdown("---")
    st.markdown("### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Data Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info(f"**Total Records**: {sum(data_summary.values()):,}")
    
    with col2:
        st.info(f"**Dashboard Version**: 2.0.0")
        st.info(f"**Data Sources**: {len([k for k, v in data_summary.items() if v > 0])} active datasets")

#!/usr/bin/env python3
"""
Response & Resolution Analytics Page
====================================

This page implements comprehensive response and resolution analytics including:
- Response time metrics
- Resolution time analysis
- SLA compliance tracking
- Escalation analysis
- Performance trends
- Interactive visualizations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Import analytics functions
from cs_analytics import (
    calculate_response_metrics,
    calculate_sla_compliance
)

def safe_column_access(df, columns, default_value=None):
    """Safely access DataFrame columns, returning default if not available"""
    if df is None or df.empty:
        return default_value
    
    available_columns = [col for col in columns if col in df.columns]
    if not available_columns:
        return default_value
    
    return df[available_columns]

def safe_merge(left_df, right_df, on_column, how='left'):
    """Safely merge DataFrames with error handling"""
    try:
        if (left_df is None or left_df.empty or 
            right_df is None or right_df.empty or
            on_column not in left_df.columns or
            on_column not in right_df.columns):
            return None
        
        return left_df.merge(right_df, on=on_column, how=how)
    except Exception as e:
        st.error(f"❌ Merge operation failed: {str(e)}")
        return None

def show_response_resolution():
    """Display comprehensive response and resolution analytics"""
    
    st.markdown("""
    <div class="main-header" style="margin-bottom: 30px;">
        <h2 style="margin: 0;">⚡ Response & Resolution Analytics</h2>
        <p style="margin: 10px 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Analyze response times, resolution efficiency, and SLA compliance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # COMPLETE DATA VALIDATION - Check all required data and columns
    required_data = {
        'tickets': st.session_state.tickets,
        'agents': st.session_state.agents,
        'sla': st.session_state.sla
    }
    
    required_columns = {
        'tickets': ['created_date', 'status', 'priority'],
        'agents': ['agent_id', 'first_name', 'last_name'],
        'sla': ['ticket_type', 'priority', 'first_response_target_hours', 'resolution_target_hours']
    }
    
    # Check if data exists and has required columns
    missing_data = []
    missing_columns = {}
    
    for data_name, data_df in required_data.items():
        if data_df.empty:
            missing_data.append(data_name)
        else:
            missing_cols = [col for col in required_columns[data_name] if col not in data_df.columns]
            if missing_cols:
                missing_columns[data_name] = missing_cols
    
    # Display comprehensive error message if validation fails
    if missing_data or missing_columns:
        st.error("🚨 **Data Validation Failed**")
        
        if missing_data:
            st.error(f"**Missing Data:** {', '.join(missing_data)}")
        
        if missing_columns:
            st.error("**Missing Columns:**")
            for data_name, cols in missing_columns.items():
                st.error(f"  - {data_name}: {', '.join(cols)}")
        
        st.info("""
        **To fix this issue:**
        1. Go to '📝 Data Input & Management' 
        2. Click '📁 Load Sample File' tab
        3. Click '📁 Load Sample Dataset' button
        4. Or use '📝 Manual Entry' to add data manually
        
        **Required Data Structure:**
        - **Tickets**: Must have 'created_date', 'status', 'priority' columns
        - **Agents**: Must have 'agent_id', 'first_name', 'last_name' columns  
        - **SLA**: Must have 'ticket_type', 'priority', 'first_response_target_hours', 'resolution_target_hours' columns
        """)
        return
    
    # Additional validation for optional columns that enhance functionality
    optional_columns = {
        'tickets': ['first_response_date', 'resolved_date', 'agent_id', 'category', 'customer_id'],
        'agents': ['department', 'team', 'experience_level'],
        'sla': ['sla_status', 'business_hours']
    }
    
    available_columns = {}
    for data_name, data_df in required_data.items():
        available_columns[data_name] = [col for col in optional_columns[data_name] if col in data_df.columns]
    
    # Success message with available features
    st.success(f"✅ **Data Validation Successful!** All required data loaded.")
    
    if any(available_columns.values()):
        st.info("**Enhanced Features Available:** " + 
                ", ".join([f"{data_name}: {', '.join(cols)}" for data_name, cols in available_columns.items() if cols]))
    
    # Create tabs for different analytics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⏱️ Response Metrics", "🔧 Resolution Metrics", "📋 SLA Compliance", "📈 Performance Trends", "📊 Detailed Analysis"
    ])
    
    with tab1:
        st.subheader("⏱️ Response Time Metrics")
        st.markdown("""
        **Response Time Analysis** measures how quickly your team responds to customer inquiries.
        
        Faster response times typically lead to higher customer satisfaction.
        """)
        
        # Calculate response metrics with error handling
        try:
            response_summary, response_message = calculate_response_metrics(st.session_state.tickets)
            
            if response_summary is not None and not response_summary.empty:
                # Display key metrics
                col1, col2, col3, col4 = st.columns(4)
                
                for i, (metric, value) in enumerate(zip(response_summary['Metric'], response_summary['Value'])):
                    with [col1, col2, col3, col4][i % 4]:
                        st.metric(metric, value)
                
                # Display detailed table
                st.subheader("📋 Response Metrics Details")
                st.dataframe(response_summary, use_container_width=True)
                
                # Create response time visualizations with safe column access
                required_date_columns = ['created_date', 'first_response_date']
                if all(col in st.session_state.tickets.columns for col in required_date_columns):
                    try:
                        tickets_analysis = st.session_state.tickets.copy()
                        
                        # Convert dates safely
                        tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
                        tickets_analysis['first_response_date'] = pd.to_datetime(tickets_analysis['first_response_date'], errors='coerce')
                        
                        # Calculate response times
                        tickets_analysis['response_time_hours'] = (
                            tickets_analysis['first_response_date'] - tickets_analysis['created_date']
                        ).dt.total_seconds() / 3600
                        
                        # Remove invalid response times
                        valid_response_times = tickets_analysis[
                            (tickets_analysis['response_time_hours'] >= 0) & 
                            (tickets_analysis['response_time_hours'] <= 168)  # Max 1 week
                        ]
                        
                        if not valid_response_times.empty:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Response time distribution
                                fig = go.Figure(data=[
                                    go.Histogram(
                                        x=valid_response_times['response_time_hours'],
                                        nbinsx=20,
                                        marker_color='#2196f3',
                                        opacity=0.8
                                    )
                                ])
                                fig.update_layout(
                                    title="Response Time Distribution",
                                    xaxis_title="Response Time (Hours)",
                                    yaxis_title="Number of Tickets",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)'
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Response time by priority
                                if 'priority' in st.session_state.tickets.columns:
                                    priority_response = valid_response_times.groupby('priority')['response_time_hours'].mean().reset_index()
                                    fig = go.Figure(data=[
                                        go.Bar(
                                            x=priority_response['priority'],
                                            y=priority_response['response_time_hours'],
                                            marker_color='#ff9800',
                                            text=[f"{val:.1f}h" for val in priority_response['response_time_hours']],
                                            textposition='auto'
                                        )
                                    ])
                                    fig.update_layout(
                                        title="Average Response Time by Priority",
                                        xaxis_title="Priority",
                                        yaxis_title="Average Response Time (Hours)",
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        paper_bgcolor='rgba(0,0,0,0)'
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("⚠️ No valid response time data available for visualization")
                    except Exception as e:
                        st.error(f"❌ Error creating response time visualizations: {str(e)}")
                        st.info("💡 This may be due to data format issues or missing columns")
                else:
                    st.info("ℹ️ Response time visualizations require 'created_date' and 'first_response_date' columns")
            else:
                st.warning("⚠️ No response metrics data available")
        except Exception as e:
            st.error(f"❌ Error calculating response metrics: {str(e)}")
            st.info("💡 Please check that your ticket data has the required columns and format")
    
    # Display success message if available
    if 'response_message' in locals() and response_message:
        st.success(response_message)
    
    with tab2:
        st.subheader("🔧 Resolution Metrics")
        st.markdown("""
        **Resolution Metrics** track how efficiently tickets are resolved and identify bottlenecks.
        
        Faster resolution times improve customer satisfaction and team productivity.
        """)
        
        # Calculate resolution metrics
        if 'created_date' in st.session_state.tickets.columns and 'resolved_date' in st.session_state.tickets.columns:
            tickets_analysis = st.session_state.tickets.copy()
            
            # Convert dates
            tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
            tickets_analysis['resolved_date'] = pd.to_datetime(tickets_analysis['resolved_date'], errors='coerce')
            
            # Calculate resolution times
            tickets_analysis['resolution_time_hours'] = (
                tickets_analysis['resolved_date'] - tickets_analysis['created_date']
            ).dt.total_seconds() / 3600
            
            # Filter resolved tickets
            resolved_tickets = tickets_analysis[
                (tickets_analysis['resolution_time_hours'] >= 0) & 
                (tickets_analysis['resolution_time_hours'] <= 720)  # Max 30 days
            ]
            
            if not resolved_tickets.empty:
                # Calculate resolution metrics
                total_resolved = len(resolved_tickets)
                avg_resolution_time = resolved_tickets['resolution_time_hours'].mean()
                median_resolution_time = resolved_tickets['resolution_time_hours'].median()
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Resolved", total_resolved)
                
                with col2:
                    st.metric("Avg Resolution Time", f"{avg_resolution_time:.1f} hours")
                
                with col3:
                    st.metric("Median Resolution Time", f"{median_resolution_time:.1f} hours")
                
                with col4:
                    resolution_rate = (total_resolved / len(st.session_state.tickets)) * 100
                    st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
                
                # Create resolution visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    # Resolution time distribution
                    fig = go.Figure(data=[
                        go.Histogram(
                            x=resolved_tickets['resolution_time_hours'],
                            nbinsx=20,
                            marker_color='#4caf50',
                            hovertemplate='Resolution Time: %{x:.1f} hours<br>Count: %{y}<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="Resolution Time Distribution",
                        xaxis_title="Resolution Time (Hours)",
                        yaxis_title="Number of Tickets",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Resolution time by priority
                    if 'priority' in resolved_tickets.columns:
                        priority_resolution = resolved_tickets.groupby('priority')['resolution_time_hours'].mean().reset_index()
                        priority_resolution = priority_resolution.dropna()
                        
                        if not priority_resolution.empty:
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=priority_resolution['priority'],
                                    y=priority_resolution['resolution_time_hours'],
                                    marker_color=['#ff5722', '#ff9800', '#4caf50', '#2196f3'],
                                    text=[f"{val:.1f}h" for val in priority_resolution['resolution_time_hours']],
                                    textposition='auto',
                                    hovertemplate='Priority: %{x}<br>Avg Resolution Time: %{y:.1f} hours<extra></extra>'
                                )
                            ])
                            fig.update_layout(
                                title="Average Resolution Time by Priority",
                                xaxis_title="Priority",
                                yaxis_title="Average Resolution Time (Hours)",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(size=12),
                                margin=dict(l=50, r=50, t=80, b=50)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                # Resolution efficiency by agent
                if ('agent_id' in resolved_tickets.columns and 
                    not st.session_state.agents.empty and
                    'agent_id' in st.session_state.agents.columns and
                    'first_name' in st.session_state.agents.columns and
                    'last_name' in st.session_state.agents.columns):
                    
                    st.subheader("👥 Resolution Efficiency by Agent")
                    
                    try:
                        agent_resolution = resolved_tickets.groupby('agent_id')['resolution_time_hours'].agg([
                            'count', 'mean', 'median'
                        ]).reset_index()
                        agent_resolution.columns = ['Agent ID', 'Tickets Resolved', 'Avg Resolution Time', 'Median Resolution Time']
                        
                        # Safe merge with agent names - only if all required columns exist
                        if (len(st.session_state.agents) > 0 and 
                            'agent_id' in st.session_state.agents.columns and
                            'first_name' in st.session_state.agents.columns and
                            'last_name' in st.session_state.agents.columns):
                            
                            agent_resolution = agent_resolution.merge(
                                st.session_state.agents[['agent_id', 'first_name', 'last_name']], 
                                on='agent_id', how='left'
                            )
                            
                            # Handle missing agent names gracefully
                            agent_resolution['Agent Name'] = agent_resolution.apply(
                                lambda row: f"{row['first_name']} {row['last_name']}" 
                                if pd.notna(row['first_name']) and pd.notna(row['last_name'])
                                else f"Agent {row['Agent ID']}", axis=1
                            )
                            
                            # Display agent performance table
                            st.dataframe(agent_resolution[['Agent Name', 'Tickets Resolved', 'Avg Resolution Time', 'Median Resolution Time']], 
                                       use_container_width=True)
                            
                            # Agent performance chart
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=agent_resolution['Agent Name'],
                                    y=agent_resolution['Avg Resolution Time'],
                                    marker_color='#9c27b0',
                                    text=[f"{val:.1f}h" for val in agent_resolution['Avg Resolution Time']],
                                    textposition='auto',
                                    hovertemplate='Agent: %{x}<br>Avg Resolution Time: %{y:.1f} hours<extra></extra>'
                                )
                            ])
                            fig.update_layout(
                                title="Agent Resolution Performance",
                                xaxis_title="Agent",
                                yaxis_title="Average Resolution Time (Hours)",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(size=12),
                                margin=dict(l=50, r=50, t=80, b=50),
                                xaxis_tickangle=-45
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("⚠️ Agent data missing required columns (agent_id, first_name, last_name)")
                            
                    except Exception as e:
                        st.error(f"❌ Error analyzing agent resolution efficiency: {str(e)}")
                        st.info("💡 This may be due to missing or corrupted data columns")
                else:
                    st.info("ℹ️ Agent resolution analysis requires 'agent_id' column in tickets and complete agent data")
                
                st.success(f"Resolution analysis completed. {total_resolved} tickets analyzed.")
            else:
                st.warning("No resolved tickets found for analysis.")
        else:
            st.error("Resolution analysis requires 'created_date' and 'resolved_date' columns in ticket data.")
    
    with tab3:
        st.subheader("📋 SLA Compliance")
        st.markdown("""
        **Service Level Agreement (SLA) Compliance** tracks how well your team meets response and resolution targets.
        
        Higher compliance rates indicate better service quality and customer satisfaction.
        """)
        
        # Calculate SLA compliance
        if not st.session_state.sla.empty:
            sla_compliance_rate = calculate_sla_compliance(st.session_state.tickets, st.session_state.sla)
            
            # Display SLA metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("SLA Compliance Rate", f"{sla_compliance_rate:.1f}%")
            
            with col2:
                st.metric("SLA Targets", len(st.session_state.sla))
            
            with col3:
                if 'priority' in st.session_state.tickets.columns:
                    high_priority_tickets = len(st.session_state.tickets[st.session_state.tickets['priority'] == 'High'])
                    st.metric("High Priority Tickets", high_priority_tickets)
            
            with col4:
                if 'status' in st.session_state.tickets.columns:
                    escalated_tickets = len(st.session_state.tickets[st.session_state.tickets['status'] == 'Escalated'])
                    st.metric("Escalated Tickets", escalated_tickets)
            
            # SLA details table
            st.subheader("📋 SLA Configuration")
            st.dataframe(st.session_state.sla, use_container_width=True)
            
            # SLA compliance visualization
            if 'priority' in st.session_state.tickets.columns and 'created_date' in st.session_state.tickets.columns:
                tickets_analysis = st.session_state.tickets.copy()
                tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
                tickets_analysis['first_response_date'] = pd.to_datetime(tickets_analysis['first_response_date'], errors='coerce')
                
                # Calculate response times by priority
                priority_response_times = []
                for priority in ['Critical', 'High', 'Medium', 'Low']:
                    priority_tickets = tickets_analysis[tickets_analysis['priority'] == priority]
                    if not priority_tickets.empty:
                        response_times = (priority_tickets['first_response_date'] - priority_tickets['created_date']).dt.total_seconds() / 3600
                        valid_times = response_times[(response_times >= 0) & (response_times <= 168)]
                        if not valid_times.empty:
                            priority_response_times.append({
                                'Priority': priority,
                                'Avg Response Time': valid_times.mean(),
                                'SLA Target': 4 if priority in ['Critical', 'High'] else 8,
                                'Compliance Rate': (valid_times <= (4 if priority in ['Critical', 'High'] else 8)).mean() * 100
                            })
                
                if priority_response_times:
                    sla_df = pd.DataFrame(priority_response_times)
                    
                    # SLA compliance chart
                    fig = go.Figure(data=[
                        go.Bar(
                            x=sla_df['Priority'],
                            y=sla_df['Compliance Rate'],
                            marker_color=['#ff5722', '#ff9800', '#4caf50', '#2196f3'],
                            text=[f"{val:.1f}%" for val in sla_df['Compliance Rate']],
                            textposition='auto',
                            hovertemplate='Priority: %{x}<br>Compliance Rate: %{y:.1f}%<extra></extra>'
                        )
                    ])
                    fig.update_layout(
                        title="SLA Compliance by Priority",
                        xaxis_title="Priority",
                        yaxis_title="Compliance Rate (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # SLA performance table
                    st.subheader("📊 SLA Performance Summary")
                    st.dataframe(sla_df, use_container_width=True)
            
            st.success(f"SLA compliance analysis completed. Overall compliance: {sla_compliance_rate:.1f}%")
        else:
            st.warning("SLA analysis requires SLA configuration data.")
    
    with tab4:
        st.subheader("📈 Performance Trends")
        st.markdown("""
        **Performance Trends** show how response and resolution metrics change over time.
        
        Identify patterns, seasonal variations, and improvement areas.
        """)
        
        # Analyze trends over time
        if 'created_date' in st.session_state.tickets.columns:
            tickets_analysis = st.session_state.tickets.copy()
            tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
            tickets_analysis['month'] = tickets_analysis['created_date'].dt.strftime('%Y-%m')
            
            # Remove invalid dates
            tickets_analysis = tickets_analysis.dropna(subset=['created_date'])
            
            if not tickets_analysis.empty:
                # Monthly ticket volume
                monthly_volume = tickets_analysis.groupby('month').size().reset_index(name='ticket_count')
                
                # Monthly response times
                if 'first_response_date' in tickets_analysis.columns:
                    tickets_analysis['first_response_date'] = pd.to_datetime(tickets_analysis['first_response_date'], errors='coerce')
                    tickets_analysis['response_time_hours'] = (
                        tickets_analysis['first_response_date'] - tickets_analysis['created_date']
                    ).dt.total_seconds() / 3600
                    
                    valid_response_times = tickets_analysis[
                        (tickets_analysis['response_time_hours'] >= 0) & 
                        (tickets_analysis['response_time_hours'] <= 168)
                    ]
                    
                    if not valid_response_times.empty:
                        monthly_response = valid_response_times.groupby('month')['response_time_hours'].mean().reset_index()
                        
                        # Create trend visualization
                        fig = make_subplots(
                            rows=2, cols=1,
                            subplot_titles=('Monthly Ticket Volume', 'Average Response Time Trend'),
                            vertical_spacing=0.1
                        )
                        
                        # Ticket volume
                        fig.add_trace(
                            go.Scatter(
                                x=monthly_volume['month'],
                                y=monthly_volume['ticket_count'],
                                mode='lines+markers',
                                name='Ticket Volume',
                                line=dict(color='#2196f3', width=3)
                            ),
                            row=1, col=1
                        )
                        
                        # Response time trend
                        fig.add_trace(
                            go.Scatter(
                                x=monthly_response['month'],
                                y=monthly_response['response_time_hours'],
                                mode='lines+markers',
                                name='Response Time',
                                line=dict(color='#ff5722', width=3)
                            ),
                            row=2, col=1
                        )
                        
                        fig.update_layout(
                            title="Performance Trends Over Time",
                            height=600,
                            showlegend=False,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12)
                        )
                        
                        fig.update_xaxes(title_text="Month", row=2, col=1)
                        fig.update_yaxes(title_text="Ticket Count", row=1, col=1)
                        fig.update_yaxes(title_text="Response Time (Hours)", row=2, col=1)
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Trend insights
                        st.subheader("💡 Trend Insights")
                        
                        if len(monthly_volume) > 1:
                            volume_change = ((monthly_volume.iloc[-1]['ticket_count'] - monthly_volume.iloc[0]['ticket_count']) / 
                                           monthly_volume.iloc[0]['ticket_count'] * 100)
                            
                            if volume_change > 0:
                                st.info(f"📈 Ticket volume increased by {volume_change:.1f}% over the period")
                            else:
                                st.info(f"📉 Ticket volume decreased by {abs(volume_change):.1f}% over the period")
                        
                        if len(monthly_response) > 1:
                            response_change = monthly_response.iloc[-1]['response_time_hours'] - monthly_response.iloc[0]['response_time_hours']
                            
                            if response_change < 0:
                                st.success(f"⚡ Response time improved by {abs(response_change):.1f} hours over the period")
                            else:
                                st.warning(f"⚠️ Response time increased by {response_change:.1f} hours over the period")
                
                st.success("Performance trend analysis completed successfully.")
            else:
                st.warning("No valid date data available for trend analysis.")
        else:
            st.error("Trend analysis requires 'created_date' column in ticket data.")
    
    with tab5:
        st.subheader("📊 Detailed Analysis")
        st.markdown("""
        **Detailed Analysis** provides comprehensive insights into response and resolution performance.
        
        Use filters to analyze specific time periods, priorities, or agents.
        """)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Date range filter
            if 'created_date' in st.session_state.tickets.columns:
                min_date = pd.to_datetime(st.session_state.tickets['created_date']).min()
                max_date = pd.to_datetime(st.session_state.tickets['created_date']).max()
                
                date_range = st.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
        
        with col2:
            # Priority filter
            if 'priority' in st.session_state.tickets.columns:
                priorities = ['All'] + list(st.session_state.tickets['priority'].unique())
                selected_priority = st.selectbox("Select Priority", priorities)
        
        with col3:
            # Status filter
            if 'status' in st.session_state.tickets.columns:
                statuses = ['All'] + list(st.session_state.tickets['status'].unique())
                selected_status = st.selectbox("Select Status", statuses)
        
        # Apply filters
        filtered_tickets = st.session_state.tickets.copy()
        
        if 'created_date' in filtered_tickets.columns and len(date_range) == 2:
            filtered_tickets['created_date'] = pd.to_datetime(filtered_tickets['created_date'])
            filtered_tickets = filtered_tickets[
                (filtered_tickets['created_date'].dt.date >= date_range[0]) &
                (filtered_tickets['created_date'].dt.date <= date_range[1])
            ]
        
        if selected_priority != 'All':
            filtered_tickets = filtered_tickets[filtered_tickets['priority'] == selected_priority]
        
        if selected_status != 'All':
            filtered_tickets = filtered_tickets[filtered_tickets['status'] == selected_status]
        
        # Display filtered results
        st.subheader(f"📊 Filtered Results ({len(filtered_tickets)} tickets)")
        
        if not filtered_tickets.empty:
            # Summary metrics for filtered data
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Filtered Tickets", len(filtered_tickets))
            
            with col2:
                if 'priority' in filtered_tickets.columns:
                    high_priority = len(filtered_tickets[filtered_tickets['priority'] == 'High'])
                    st.metric("High Priority", high_priority)
            
            with col3:
                if 'status' in filtered_tickets.columns:
                    resolved = len(filtered_tickets[filtered_tickets['status'] == 'Resolved'])
                    st.metric("Resolved", resolved)
            
            with col4:
                if 'created_date' in filtered_tickets.columns and 'first_response_date' in filtered_tickets.columns:
                    filtered_tickets['created_date'] = pd.to_datetime(filtered_tickets['created_date'])
                    filtered_tickets['first_response_date'] = pd.to_datetime(filtered_tickets['first_response_date'])
                    
                    response_times = (filtered_tickets['first_response_date'] - filtered_tickets['created_date']).dt.total_seconds() / 3600
                    valid_times = response_times[(response_times >= 0) & (response_times <= 168)]
                    
                    if not valid_times.empty:
                        avg_response = valid_times.mean()
                        st.metric("Avg Response", f"{avg_response:.1f}h")
            
            # Detailed table
            st.subheader("📋 Filtered Ticket Details")
            display_columns = ['ticket_id', 'customer_id', 'priority', 'status', 'created_date']
            available_columns = [col for col in display_columns if col in filtered_tickets.columns]
            
            if available_columns:
                st.dataframe(filtered_tickets[available_columns], use_container_width=True)
            else:
                st.dataframe(filtered_tickets.head(10), use_container_width=True)
        else:
            st.warning("No tickets match the selected filters.")
    
    # Summary insights
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    # Generate insights based on available data
    insights = []
    
    if not st.session_state.tickets.empty:
        if 'created_date' in st.session_state.tickets.columns and 'first_response_date' in st.session_state.tickets.columns:
            tickets_analysis = st.session_state.tickets.copy()
            tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
            tickets_analysis['first_response_date'] = pd.to_datetime(tickets_analysis['first_response_date'], errors='coerce')
            
            response_times = (tickets_analysis['first_response_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            valid_times = response_times[(response_times >= 0) & (response_times <= 168)]
            
            if not valid_times.empty:
                avg_response_time = valid_times.mean()
                if avg_response_time <= 4:
                    insights.append("⚡ **Excellent Response Time:** Average response time is 4 hours or less")
                elif avg_response_time <= 8:
                    insights.append("✅ **Good Response Time:** Average response time is 8 hours or less")
                else:
                    insights.append("⚠️ **Needs Improvement:** Average response time exceeds 8 hours")
        
        if 'status' in st.session_state.tickets.columns:
            status_counts = st.session_state.tickets['status'].value_counts()
            if 'Resolved' in status_counts.index:
                resolution_rate = (status_counts['Resolved'] / len(st.session_state.tickets)) * 100
                if resolution_rate >= 80:
                    insights.append("🎯 **High Resolution Rate:** Over 80% of tickets are resolved")
                elif resolution_rate >= 60:
                    insights.append("✅ **Good Resolution Rate:** Over 60% of tickets are resolved")
                else:
                    insights.append("⚠️ **Low Resolution Rate:** Less than 60% of tickets are resolved")
    
    if not insights:
        insights.append("📊 **Data Analysis:** Use the tabs above to explore response and resolution metrics")
    
    for insight in insights:
        st.info(insight)

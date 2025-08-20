#!/usr/bin/env python3
"""
Customer Service Analytics Module
================================

This module contains all the analytics functions from the original cs.py file,
implementing comprehensive customer service analytics including:
- CSAT (Customer Satisfaction) scoring
- NPS (Net Promoter Score) analysis
- CES (Customer Effort Score) metrics
- Sentiment analysis
- Resolution satisfaction
- Response and resolution metrics
- Service efficiency metrics
- Agent performance analytics
- Customer retention analysis
- Business impact metrics
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CUSTOMER SATISFACTION ANALYTICS
# ============================================================================

def calculate_csat_score(feedback_df):
    """Calculate Customer Satisfaction Score (CSAT)"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available"
        
        # Filter for CSAT feedback (assuming rating column exists)
        if 'rating' not in feedback_df.columns:
            return pd.DataFrame(), "Rating column not found in feedback data"
        
        # Calculate CSAT metrics
        total_responses = len(feedback_df)
        positive_responses = len(feedback_df[feedback_df['rating'] >= 4])  # 4-5 rating
        csat_score = (positive_responses / total_responses * 100) if total_responses > 0 else 0
        
        # Create summary DataFrame
        csat_summary = pd.DataFrame({
            'Metric': ['CSAT Score', 'Positive Responses', 'Total Responses', 'Positive Rate'],
            'Value': [f"{csat_score:.1f}%", positive_responses, total_responses, f"{csat_score:.1f}%"]
        })
        
        message = f"CSAT Score: {csat_score:.1f}% ({positive_responses}/{total_responses} positive responses)"
        
        return csat_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating CSAT score: {str(e)}"

def calculate_nps_score(feedback_df):
    """Calculate Net Promoter Score (NPS)"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available"
        
        # Filter for NPS feedback (assuming nps_score column exists)
        if 'nps_score' not in feedback_df.columns:
            return pd.DataFrame(), "NPS score column not found in feedback data"
        
        # Calculate NPS metrics
        promoters = len(feedback_df[feedback_df['nps_score'] >= 9])  # 9-10
        detractors = len(feedback_df[feedback_df['nps_score'] <= 6])  # 0-6
        total_responses = len(feedback_df)
        
        nps_score = ((promoters - detractors) / total_responses * 100) if total_responses > 0 else 0
        
        # Create summary DataFrame
        nps_summary = pd.DataFrame({
            'Metric': ['NPS Score', 'Promoters (9-10)', 'Passives (7-8)', 'Detractors (0-6)', 'Total Responses'],
            'Value': [
                f"{nps_score:.1f}%",
                promoters,
                len(feedback_df[(feedback_df['nps_score'] >= 7) & (feedback_df['nps_score'] <= 8)]),
                detractors,
                total_responses
            ]
        })
        
        message = f"NPS Score: {nps_score:.1f}% ({promoters} promoters, {detractors} detractors)"
        
        return nps_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating NPS score: {str(e)}"

def calculate_ces_score(feedback_df):
    """Calculate Customer Effort Score (CES)"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available"
        
        # Filter for CES feedback (assuming customer_effort_score column exists)
        if 'customer_effort_score' not in feedback_df.columns:
            return pd.DataFrame(), "Customer effort score column not found in feedback data"
        
        # Calculate CES metrics
        total_responses = len(feedback_df)
        low_effort = len(feedback_df[feedback_df['customer_effort_score'] <= 2])  # 1-2 (low effort)
        high_effort = len(feedback_df[feedback_df['customer_effort_score'] >= 5])  # 5-6 (high effort)
        avg_ces = feedback_df['customer_effort_score'].mean()
        
        # Create summary DataFrame
        ces_summary = pd.DataFrame({
            'Metric': ['Average CES', 'Low Effort (1-2)', 'High Effort (5-6)', 'Total Responses'],
            'Value': [f"{avg_ces:.2f}", low_effort, high_effort, total_responses]
        })
        
        message = f"Average CES: {avg_ces:.2f} (Lower is better)"
        
        return ces_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating CES score: {str(e)}"

def analyze_sentiment(feedback_df):
    """Analyze customer sentiment from feedback"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available"
        
        # Check if sentiment column exists, otherwise infer from rating
        if 'sentiment' in feedback_df.columns:
            sentiment_data = feedback_df['sentiment']
        elif 'rating' in feedback_df.columns:
            # Infer sentiment from rating
            sentiment_data = pd.cut(feedback_df['rating'], 
                                  bins=[0, 2, 3, 5], 
                                  labels=['Negative', 'Neutral', 'Positive'],
                                  include_lowest=True)
        else:
            return pd.DataFrame(), "Neither sentiment nor rating column found"
        
        # Calculate sentiment distribution
        sentiment_counts = sentiment_data.value_counts()
        total_feedback = len(feedback_df)
        
        # Create summary DataFrame
        sentiment_summary = pd.DataFrame({
            'Sentiment': sentiment_counts.index,
            'Count': sentiment_counts.values,
            'Percentage': (sentiment_counts.values / total_feedback * 100).round(1)
        })
        
        message = f"Sentiment analysis: {sentiment_counts.get('Positive', 0)} positive, {sentiment_counts.get('Negative', 0)} negative"
        
        return sentiment_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing sentiment: {str(e)}"

def calculate_resolution_satisfaction(feedback_df, tickets_df):
    """Calculate resolution satisfaction metrics"""
    try:
        if feedback_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for resolution satisfaction analysis"
        
        # Merge feedback with tickets
        resolution_data = feedback_df.merge(
            tickets_df[['ticket_id', 'status', 'priority']], 
            on='ticket_id', how='left'
        )
        
        # Calculate satisfaction by resolution status
        resolved_satisfaction = resolution_data[resolution_data['status'] == 'Resolved']['rating'].mean()
        open_satisfaction = resolution_data[resolution_data['status'] == 'Open']['rating'].mean()
        
        # Calculate satisfaction by priority
        priority_satisfaction = resolution_data.groupby('priority')['rating'].mean()
        
        # Create summary DataFrame
        metrics = []
        if not pd.isna(resolved_satisfaction):
            metrics.append(['Resolved Tickets Satisfaction', f"{resolved_satisfaction:.2f}/5"])
        if not pd.isna(open_satisfaction):
            metrics.append(['Open Tickets Satisfaction', f"{open_satisfaction:.2f}/5"])
        
        for priority, satisfaction in priority_satisfaction.items():
            if not pd.isna(satisfaction):
                metrics.append([f'{priority} Priority Satisfaction', f"{satisfaction:.2f}/5"])
        
        resolution_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Resolution satisfaction analysis completed"
        
        return resolution_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating resolution satisfaction: {str(e)}"

# ============================================================================
# RESPONSE & RESOLUTION ANALYTICS
# ============================================================================

def calculate_response_metrics(tickets_df):
    """Calculate response time and resolution metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Convert dates to datetime
        tickets_analysis = tickets_df.copy()
        date_columns = ['created_date', 'first_response_date', 'resolved_date']
        
        for col in date_columns:
            if col in tickets_analysis.columns:
                tickets_analysis[col] = pd.to_datetime(tickets_analysis[col], errors='coerce')
        
        # Calculate response and resolution times
        metrics = []
        
        if 'first_response_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            response_time = (tickets_analysis['first_response_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            avg_response_time = response_time.mean()
            if not pd.isna(avg_response_time):
                metrics.append(['Average First Response Time', f"{avg_response_time:.2f} hours"])
        
        if 'resolved_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            resolution_time = (tickets_analysis['resolved_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            avg_resolution_time = resolution_time.mean()
            if not pd.isna(avg_resolution_time):
                metrics.append(['Average Resolution Time', f"{avg_resolution_time:.2f} hours"])
        
        if 'escalated_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            escalation_rate = (tickets_analysis['escalated_date'].notna()).mean() * 100
            metrics.append(['Escalation Rate', f"{escalation_rate:.1f}%"])
        
        # Calculate SLA compliance (simplified)
        if 'priority' in tickets_analysis.columns:
            high_priority = tickets_analysis[tickets_analysis['priority'] == 'High']
            if not high_priority.empty:
                high_priority_response = (high_priority['first_response_date'] - high_priority['created_date']).dt.total_seconds() / 3600
                sla_compliance = (high_priority_response <= 4).mean() * 100  # 4-hour SLA for high priority
                metrics.append(['High Priority SLA Compliance', f"{sla_compliance:.1f}%"])
        
        response_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Response and resolution metrics calculated successfully"
        
        return response_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating response metrics: {str(e)}"

def calculate_sla_compliance(tickets_df, sla_df):
    """Calculate SLA compliance rates"""
    try:
        if tickets_df.empty:
            return 0.0
        
        # Simplified SLA compliance calculation
        # In a real implementation, this would compare against actual SLA targets
        if 'priority' in tickets_df.columns and 'first_response_date' in tickets_df.columns:
            high_priority = tickets_df[tickets_df['priority'] == 'High']
            if not high_priority.empty:
                high_priority['created_date'] = pd.to_datetime(high_priority['created_date'], errors='coerce')
                high_priority['first_response_date'] = pd.to_datetime(high_priority['first_response_date'], errors='coerce')
                
                response_time = (high_priority['first_response_date'] - high_priority['created_date']).dt.total_seconds() / 3600
                sla_compliance = (response_time <= 4).mean() * 100  # 4-hour SLA for high priority
                return sla_compliance
        
        return 0.0
        
    except Exception as e:
        return 0.0

# ============================================================================
# SERVICE EFFICIENCY ANALYTICS
# ============================================================================

def calculate_service_efficiency(tickets_df, agents_df):
    """Calculate service efficiency metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Calculate efficiency metrics
        metrics = []
        
        # Ticket volume metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        if 'status' in tickets_df.columns:
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['Resolution Rate', f"{resolution_rate:.1f}%"])
        
        if 'priority' in tickets_df.columns:
            high_priority = len(tickets_df[tickets_df['priority'] == 'High'])
            high_priority_rate = (high_priority / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['High Priority Rate', f"{high_priority_rate:.1f}%"])
        
        # Agent efficiency (if agent data available)
        if not agents_df.empty and 'agent_id' in tickets_df.columns:
            agent_ticket_counts = tickets_df['agent_id'].value_counts()
            avg_tickets_per_agent = agent_ticket_counts.mean()
            metrics.append(['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"])
        
        efficiency_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Service efficiency metrics calculated successfully"
        
        return efficiency_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating service efficiency: {str(e)}"

# ============================================================================
# AGENT PERFORMANCE ANALYTICS
# ============================================================================

def calculate_agent_performance(tickets_df, agents_df, feedback_df):
    """Calculate agent performance metrics"""
    try:
        if tickets_df.empty or agents_df.empty:
            return pd.DataFrame(), "Insufficient data for agent performance analysis"
        
        # Merge data for analysis
        agent_performance = tickets_df.merge(
            agents_df[['agent_id', 'first_name', 'last_name', 'department']], 
            on='agent_id', how='left'
        )
        
        # Calculate agent metrics
        agent_metrics = []
        
        # Tickets per agent
        tickets_per_agent = agent_performance.groupby(['agent_id', 'first_name', 'last_name']).size().reset_index(name='ticket_count')
        agent_metrics.append(['Total Agents', len(tickets_per_agent)])
        agent_metrics.append(['Average Tickets per Agent', f"{tickets_per_agent['ticket_count'].mean():.1f}"])
        
        # Resolution rate by agent
        if 'status' in agent_performance.columns:
            agent_resolution = agent_performance.groupby(['agent_id', 'first_name', 'last_name'])['status'].apply(
                lambda x: (x == 'Resolved').mean() * 100
            ).reset_index(name='resolution_rate')
            
            avg_resolution_rate = agent_resolution['resolution_rate'].mean()
            agent_metrics.append(['Average Agent Resolution Rate', f"{avg_resolution_rate:.1f}%"])
        
        # Customer satisfaction by agent (if feedback available)
        if not feedback_df.empty and 'agent_id' in feedback_df.columns:
            agent_satisfaction = feedback_df.groupby('agent_id')['rating'].mean().reset_index(name='avg_rating')
            avg_agent_satisfaction = agent_satisfaction['avg_rating'].mean()
            agent_metrics.append(['Average Agent Satisfaction', f"{avg_agent_satisfaction:.2f}/5"])
        
        agent_summary = pd.DataFrame(agent_metrics, columns=['Metric', 'Value'])
        
        message = "Agent performance metrics calculated successfully"
        
        return agent_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating agent performance: {str(e)}"

# ============================================================================
# CUSTOMER RETENTION ANALYTICS
# ============================================================================

def calculate_customer_retention(customers_df, tickets_df):
    """Calculate customer retention metrics"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for customer retention analysis"
        
        # Calculate retention metrics
        metrics = []
        
        total_customers = len(customers_df)
        customers_with_tickets = len(tickets_df['customer_id'].unique())
        
        metrics.append(['Total Customers', total_customers])
        metrics.append(['Customers with Tickets', customers_with_tickets])
        
        if total_customers > 0:
            engagement_rate = (customers_with_tickets / total_customers * 100)
            metrics.append(['Customer Engagement Rate', f"{engagement_rate:.1f}%"])
        
        # Repeat customer analysis
        customer_ticket_counts = tickets_df['customer_id'].value_counts()
        repeat_customers = len(customer_ticket_counts[customer_ticket_counts > 1])
        
        if customers_with_tickets > 0:
            repeat_customer_rate = (repeat_customers / customers_with_tickets * 100)
            metrics.append(['Repeat Customer Rate', f"{repeat_customer_rate:.1f}%"])
        
        # Average tickets per customer
        if customers_with_tickets > 0:
            avg_tickets_per_customer = len(tickets_df) / customers_with_tickets
            metrics.append(['Average Tickets per Customer', f"{avg_tickets_per_customer:.1f}"])
        
        retention_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Customer retention metrics calculated successfully"
        
        return retention_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating customer retention: {str(e)}"

# ============================================================================
# BUSINESS IMPACT ANALYTICS
# ============================================================================

def calculate_business_impact(customers_df, tickets_df, feedback_df):
    """Calculate business impact metrics"""
    try:
        if customers_df.empty:
            return pd.DataFrame(), "No customer data available"
        
        # Calculate business impact metrics
        metrics = []
        
        # Customer base metrics
        total_customers = len(customers_df)
        metrics.append(['Total Customer Base', total_customers])
        
        if 'customer_segment' in customers_df.columns:
            enterprise_customers = len(customers_df[customers_df['customer_segment'] == 'Enterprise'])
            if total_customers > 0:
                enterprise_rate = (enterprise_customers / total_customers * 100)
                metrics.append(['Enterprise Customer Rate', f"{enterprise_rate:.1f}%"])
        
        # Customer lifetime value (simplified)
        if 'lifetime_value' in customers_df.columns:
            avg_lifetime_value = customers_df['lifetime_value'].mean()
            if not pd.isna(avg_lifetime_value):
                metrics.append(['Average Customer Lifetime Value', f"${avg_lifetime_value:,.0f}"])
        
        # Customer satisfaction impact
        if not feedback_df.empty and 'rating' in feedback_df.columns:
            avg_satisfaction = feedback_df['rating'].mean()
            if not pd.isna(avg_satisfaction):
                metrics.append(['Average Customer Satisfaction', f"{avg_satisfaction:.2f}/5"])
        
        # Support efficiency
        if not tickets_df.empty:
            total_tickets = len(tickets_df)
            if total_customers > 0:
                support_intensity = total_tickets / total_customers
                metrics.append(['Support Intensity (Tickets/Customer)', f"{support_intensity:.2f}"])
        
        business_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Business impact metrics calculated successfully"
        
        return business_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating business impact: {str(e)}"

# ============================================================================
# INTERACTION ANALYSIS
# ============================================================================

def analyze_customer_interactions(interactions_df, tickets_df):
    """Analyze customer interaction patterns"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available"
        
        # Calculate interaction metrics
        metrics = []
        
        total_interactions = len(interactions_df)
        metrics.append(['Total Interactions', total_interactions])
        
        if 'interaction_type' in interactions_df.columns:
            interaction_types = interactions_df['interaction_type'].value_counts()
            for interaction_type, count in interaction_types.head(3).items():
                percentage = (count / total_interactions * 100)
                metrics.append([f'{interaction_type} Interactions', f"{count} ({percentage:.1f}%)"])
        
        if 'channel' in interactions_df.columns:
            channel_distribution = interactions_df['channel'].value_counts()
            primary_channel = channel_distribution.index[0]
            primary_channel_count = channel_distribution.iloc[0]
            primary_channel_percentage = (primary_channel_count / total_interactions * 100)
            metrics.append(['Primary Channel', f"{primary_channel} ({primary_channel_percentage:.1f}%)"])
        
        # Interaction per ticket
        if not tickets_df.empty and 'ticket_id' in interactions_df.columns:
            interactions_per_ticket = interactions_df.groupby('ticket_id').size()
            avg_interactions_per_ticket = interactions_per_ticket.mean()
            metrics.append(['Average Interactions per Ticket', f"{avg_interactions_per_ticket:.1f}"])
        
        interaction_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Customer interaction analysis completed successfully"
        
        return interaction_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing customer interactions: {str(e)}"

# ============================================================================
# OMNICHANNEL EXPERIENCE ANALYTICS
# ============================================================================

def analyze_omnichannel_experience(interactions_df, tickets_df):
    """Analyze omnichannel customer experience"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available"
        
        # Calculate omnichannel metrics
        metrics = []
        
        # Channel diversity
        if 'channel' in interactions_df.columns:
            unique_channels = interactions_df['channel'].nunique()
            metrics.append(['Channels Used', unique_channels])
            
            # Channel distribution
            channel_counts = interactions_df['channel'].value_counts()
            for channel, count in channel_counts.head(3).items():
                percentage = (count / len(interactions_df) * 100)
                metrics.append([f'{channel} Usage', f"{count} ({percentage:.1f}%)"])
        
        # Cross-channel ticket analysis
        if not tickets_df.empty and 'ticket_id' in interactions_df.columns:
            ticket_channels = interactions_df.groupby('ticket_id')['channel'].nunique()
            multi_channel_tickets = (ticket_channels > 1).sum()
            total_tickets = len(ticket_channels)
            
            if total_tickets > 0:
                multi_channel_rate = (multi_channel_tickets / total_tickets * 100)
                metrics.append(['Multi-Channel Tickets', f"{multi_channel_rate:.1f}%"])
        
        omnichannel_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Omnichannel experience analysis completed successfully"
        
        return omnichannel_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing omnichannel experience: {str(e)}"

# ============================================================================
# PREDICTIVE ANALYTICS
# ============================================================================

def predict_customer_churn(customers_df, tickets_df, feedback_df):
    """Predict customer churn risk"""
    try:
        if customers_df.empty:
            return pd.DataFrame(), "No customer data available"
        
        # Simplified churn prediction based on activity patterns
        churn_risk_data = []
        
        for _, customer in customers_df.iterrows():
            customer_id = customer['customer_id']
            
            # Get customer activity
            customer_tickets = tickets_df[tickets_df['customer_id'] == customer_id]
            customer_feedback = feedback_df[feedback_df['customer_id'] == customer_id]
            
            # Calculate churn risk factors
            ticket_count = len(customer_tickets)
            last_ticket_date = customer_tickets['created_date'].max() if not customer_tickets.empty else None
            avg_satisfaction = customer_feedback['rating'].mean() if not customer_feedback.empty else 0
            
            # Simple churn risk scoring
            churn_risk = 0
            
            if ticket_count == 0:
                churn_risk += 30  # No activity
            elif ticket_count < 3:
                churn_risk += 20  # Low activity
            
            if pd.notna(last_ticket_date):
                days_since_last_ticket = (pd.Timestamp.now() - pd.to_datetime(last_ticket_date)).days
                if days_since_last_ticket > 90:
                    churn_risk += 25  # Inactive for 3+ months
                elif days_since_last_ticket > 30:
                    churn_risk += 15  # Inactive for 1+ month
            
            if avg_satisfaction < 3:
                churn_risk += 25  # Low satisfaction
            
            # Categorize risk
            if churn_risk >= 50:
                risk_level = "High"
            elif churn_risk >= 30:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            churn_risk_data.append({
                'customer_id': customer_id,
                'customer_name': customer.get('customer_name', 'Unknown'),
                'ticket_count': ticket_count,
                'last_activity_days': days_since_last_ticket if pd.notna(last_ticket_date) else None,
                'avg_satisfaction': avg_satisfaction,
                'churn_risk_score': churn_risk,
                'risk_level': risk_level
            })
        
        churn_analysis = pd.DataFrame(churn_risk_data)
        
        # Summary statistics
        high_risk_customers = len(churn_analysis[churn_analysis['risk_level'] == 'High'])
        medium_risk_customers = len(churn_analysis[churn_analysis['risk_level'] == 'Medium'])
        low_risk_customers = len(churn_analysis[churn_analysis['risk_level'] == 'Low'])
        
        summary_data = [
            ['Total Customers', len(churn_analysis)],
            ['High Risk Customers', f"{high_risk_customers} ({high_risk_customers/len(churn_analysis)*100:.1f}%)"],
            ['Medium Risk Customers', f"{medium_risk_customers} ({medium_risk_customers/len(churn_analysis)*100:.1f}%)"],
            ['Low Risk Customers', f"{low_risk_customers} ({low_risk_customers/len(churn_analysis)*100:.1f}%)"],
            ['Average Churn Risk Score', f"{churn_analysis['churn_risk_score'].mean():.1f}"]
        ]
        
        churn_summary = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
        
        message = f"Churn prediction analysis completed. {high_risk_customers} customers identified as high risk."
        
        return churn_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error predicting customer churn: {str(e)}"

# ============================================================================
# TRENDS AND PATTERNS ANALYSIS
# ============================================================================

def analyze_trends_and_patterns(tickets_df, feedback_df):
    """Analyze trends and patterns in customer service data"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Convert dates for trend analysis
        tickets_analysis = tickets_df.copy()
        if 'created_date' in tickets_analysis.columns:
            tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
            tickets_analysis['month'] = tickets_analysis['created_date'].dt.strftime('%Y-%m')
        
        # Calculate trend metrics
        metrics = []
        
        # Monthly ticket volume
        if 'month' in tickets_analysis.columns:
            monthly_tickets = tickets_analysis.groupby('month').size()
            if len(monthly_tickets) > 1:
                # Calculate growth rate
                first_month = monthly_tickets.iloc[0]
                last_month = monthly_tickets.iloc[-1]
                growth_rate = ((last_month - first_month) / first_month * 100) if first_month > 0 else 0
                metrics.append(['Monthly Ticket Growth Rate', f"{growth_rate:.1f}%"])
        
        # Priority trends
        if 'priority' in tickets_analysis.columns:
            priority_trends = tickets_analysis.groupby(['month', 'priority']).size().unstack(fill_value=0)
            if 'High' in priority_trends.columns:
                high_priority_trend = priority_trends['High'].iloc[-1] - priority_trends['High'].iloc[0]
                metrics.append(['High Priority Ticket Trend', f"{high_priority_trend:+d}"])
        
        # Resolution time trends
        if 'resolved_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            tickets_analysis['resolution_time'] = (
                pd.to_datetime(tickets_analysis['resolved_date'], errors='coerce') - 
                tickets_analysis['created_date']
            ).dt.total_seconds() / 3600
            
            monthly_resolution_time = tickets_analysis.groupby('month')['resolution_time'].mean()
            if len(monthly_resolution_time) > 1:
                resolution_time_change = monthly_resolution_time.iloc[-1] - monthly_resolution_time.iloc[0]
                metrics.append(['Resolution Time Trend', f"{resolution_time_change:+.1f} hours"])
        
        # Customer satisfaction trends
        if not feedback_df.empty and 'submitted_date' in feedback_df.columns:
            feedback_analysis = feedback_df.copy()
            feedback_analysis['submitted_date'] = pd.to_datetime(feedback_analysis['submitted_date'], errors='coerce')
            feedback_analysis['month'] = feedback_analysis['submitted_date'].dt.strftime('%Y-%m')
            
            monthly_satisfaction = feedback_analysis.groupby('month')['rating'].mean()
            if len(monthly_satisfaction) > 1:
                satisfaction_change = monthly_satisfaction.iloc[-1] - monthly_satisfaction.iloc[0]
                metrics.append(['Satisfaction Trend', f"{satisfaction_change:+.2f}"])
        
        trends_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Trends and patterns analysis completed successfully"
        
        return trends_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing trends and patterns: {str(e)}"

# ============================================================================
# PRODUCTIVITY METRICS
# ============================================================================

def calculate_productivity_metrics(tickets_df, agents_df, interactions_df):
    """Calculate productivity and efficiency metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Calculate productivity metrics
        metrics = []
        
        # Ticket processing metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        if 'status' in tickets_df.columns:
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['Ticket Resolution Rate', f"{resolution_rate:.1f}%"])
        
        # Agent productivity
        if not agents_df.empty and 'agent_id' in tickets_df.columns:
            agent_ticket_counts = tickets_df.groupby('agent_id').size()
            avg_tickets_per_agent = agent_ticket_counts.mean()
            max_tickets_per_agent = agent_ticket_counts.max()
            metrics.append(['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"])
            metrics.append(['Max Tickets per Agent', f"{max_tickets_per_agent}"])
        
        # Interaction efficiency
        if not interactions_df.empty and 'ticket_id' in interactions_df.columns:
            interactions_per_ticket = interactions_df.groupby('ticket_id').size()
            avg_interactions_per_ticket = interactions_per_ticket.mean()
            metrics.append(['Average Interactions per Ticket', f"{avg_interactions_per_ticket:.1f}"])
        
        # Time-based productivity
        if 'created_date' in tickets_df.columns and 'resolved_date' in tickets_df.columns:
            tickets_analysis = tickets_df.copy()
            tickets_analysis['created_date'] = pd.to_datetime(tickets_analysis['created_date'], errors='coerce')
            tickets_analysis['resolved_date'] = pd.to_datetime(tickets_analysis['resolved_date'], errors='coerce')
            
            resolution_time = (tickets_analysis['resolved_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            avg_resolution_time = resolution_time.mean()
            if not pd.isna(avg_resolution_time):
                metrics.append(['Average Resolution Time', f"{avg_resolution_time:.1f} hours"])
        
        productivity_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Productivity metrics calculated successfully"
        
        return productivity_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating productivity metrics: {str(e)}"

# ============================================================================
# CUSTOMER JOURNEY ANALYSIS
# ============================================================================

def analyze_customer_journey(tickets_df, interactions_df, feedback_df):
    """Analyze customer journey and touchpoints"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Calculate customer journey metrics
        metrics = []
        
        # Journey length metrics
        if 'ticket_id' in interactions_df.columns:
            interactions_per_ticket = interactions_df.groupby('ticket_id').size()
            avg_journey_length = interactions_per_ticket.mean()
            max_journey_length = interactions_per_ticket.max()
            metrics.append(['Average Journey Length', f"{avg_journey_length:.1f} interactions"])
            metrics.append(['Max Journey Length', f"{max_journey_length} interactions"])
        
        # Journey complexity
        if 'priority' in tickets_df.columns and 'status' in tickets_df.columns:
            complex_journeys = tickets_df[
                (tickets_df['priority'] == 'High') & 
                (tickets_df['status'].isin(['Escalated', 'In Progress']))
            ]
            complex_journey_rate = (len(complex_journeys) / len(tickets_df) * 100) if len(tickets_df) > 0 else 0
            metrics.append(['Complex Journey Rate', f"{complex_journey_rate:.1f}%"])
        
        # Journey outcomes
        if 'status' in tickets_df.columns:
            successful_journeys = len(tickets_df[tickets_df['status'] == 'Resolved'])
            total_journeys = len(tickets_df)
            success_rate = (successful_journeys / total_journeys * 100) if total_journeys > 0 else 0
            metrics.append(['Journey Success Rate', f"{success_rate:.1f}%"])
        
        # Customer satisfaction by journey length
        if not feedback_df.empty and 'ticket_id' in feedback_df.columns:
            journey_satisfaction = interactions_df.groupby('ticket_id').size().reset_index(name='interaction_count')
            journey_satisfaction = journey_satisfaction.merge(
                feedback_df[['ticket_id', 'rating']], on='ticket_id', how='left'
            )
            
            if not journey_satisfaction.empty:
                # Correlation between journey length and satisfaction
                correlation = journey_satisfaction['interaction_count'].corr(journey_satisfaction['rating'])
                if not pd.isna(correlation):
                    metrics.append(['Journey Length vs Satisfaction Correlation', f"{correlation:.3f}"])
        
        journey_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Customer journey analysis completed successfully"
        
        return journey_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing customer journey: {str(e)}"

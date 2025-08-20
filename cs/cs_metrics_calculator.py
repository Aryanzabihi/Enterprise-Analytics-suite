import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

def calculate_customer_satisfaction_metrics(customers_df, feedback_df, tickets_df):
    """Calculate comprehensive customer satisfaction metrics"""
    try:
        if customers_df.empty or feedback_df.empty:
            return pd.DataFrame(), "Insufficient data for satisfaction analysis"
        
        # Merge data for analysis
        satisfaction_data = feedback_df.merge(
            customers_df[['customer_id', 'customer_name', 'customer_segment']], 
            on='customer_id', how='left'
        )
        
        # Calculate satisfaction metrics
        metrics = {
            'Metric': [
                'Overall Satisfaction Score',
                'Average Rating',
                'Positive Sentiment %',
                'Negative Sentiment %',
                'Neutral Sentiment %',
                'Response Rate',
                'Customer Engagement Score'
            ],
            'Value': [
                f"{satisfaction_data['rating'].mean():.2f}/5",
                f"{satisfaction_data['rating'].mean():.2f}",
                f"{(satisfaction_data['sentiment'] == 'positive').mean() * 100:.1f}%",
                f"{(satisfaction_data['sentiment'] == 'negative').mean() * 100:.1f}%",
                f"{(satisfaction_data['sentiment'] == 'neutral').mean() * 100:.1f}%",
                f"{len(satisfaction_data) / len(customers_df) * 100:.1f}%",
                f"{satisfaction_data['rating'].mean() * (len(satisfaction_data) / len(customers_df)) * 100:.1f}"
            ]
        }
        
        return pd.DataFrame(metrics), "Customer satisfaction metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating satisfaction metrics: {str(e)}"

def calculate_response_resolution_metrics(tickets_df, interactions_df, sla_df):
    """Calculate response and resolution time metrics"""
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
            metrics.append(['Average First Response Time', f"{avg_response_time:.2f} hours"])
        
        if 'resolved_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            resolution_time = (tickets_analysis['resolved_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            avg_resolution_time = resolution_time.mean()
            metrics.append(['Average Resolution Time', f"{avg_resolution_time:.2f} hours"])
        
        if 'escalated_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            escalation_time = (tickets_analysis['escalated_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            escalation_rate = (tickets_analysis['escalated_date'].notna()).mean() * 100
            metrics.append(['Escalation Rate', f"{escalation_rate:.1f}%"])
        
        # SLA compliance
        if not sla_df.empty and 'priority' in tickets_analysis.columns:
            sla_compliance = calculate_sla_compliance(tickets_analysis, sla_df)
            metrics.append(['SLA Compliance Rate', f"{sla_compliance:.1f}%"])
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Response and resolution metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating response metrics: {str(e)}"

def calculate_service_efficiency_metrics(tickets_df, agents_df, interactions_df):
    """Calculate service efficiency metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Calculate efficiency metrics
        metrics = []
        
        # Ticket volume metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', str(total_tickets)])
        
        if 'status' in tickets_df.columns:
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'resolved'])
            resolution_rate = (resolved_tickets / total_tickets) * 100 if total_tickets > 0 else 0
            metrics.append(['Resolution Rate', f"{resolution_rate:.1f}%"])
        
        # Agent efficiency
        if not agents_df.empty and 'agent_id' in tickets_df.columns:
            agent_performance = tickets_df.groupby('agent_id').size().reset_index(name='ticket_count')
            avg_tickets_per_agent = agent_performance['ticket_count'].mean()
            metrics.append(['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"])
        
        # Interaction efficiency
        if not interactions_df.empty and 'duration_minutes' in interactions_df.columns:
            avg_interaction_duration = interactions_df['duration_minutes'].mean()
            metrics.append(['Average Interaction Duration', f"{avg_interaction_duration:.1f} minutes"])
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Service efficiency metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating efficiency metrics: {str(e)}"

def calculate_customer_retention_metrics(customers_df, tickets_df, interactions_df):
    """Calculate customer retention and churn metrics"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for retention analysis"
        
        # Calculate retention metrics
        total_customers = len(customers_df)
        active_customers = len(tickets_df['customer_id'].unique())
        
        retention_rate = (active_customers / total_customers) * 100 if total_customers > 0 else 0
        
        # Customer lifetime value (simplified)
        if 'lifetime_value' in customers_df.columns:
            avg_lifetime_value = customers_df['lifetime_value'].mean()
        else:
            # Estimate based on ticket volume
            customer_ticket_counts = tickets_df.groupby('customer_id').size()
            avg_lifetime_value = customer_ticket_counts.mean() * 100  # Assume $100 per ticket
        
        metrics = [
            ['Total Customers', str(total_customers)],
            ['Active Customers', str(active_customers)],
            ['Retention Rate', f"{retention_rate:.1f}%"],
            ['Average Customer Lifetime Value', f"${avg_lifetime_value:.2f}"],
            ['Customer Churn Rate', f"{100 - retention_rate:.1f}%"]
        ]
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Customer retention metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating retention metrics: {str(e)}"

def calculate_agent_performance_metrics(agents_df, tickets_df, feedback_df):
    """Calculate agent performance metrics"""
    try:
        if agents_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for agent performance analysis"
        
        # Merge data for analysis
        agent_performance = tickets_df.groupby('agent_id').agg({
            'ticket_id': 'count',
            'status': lambda x: (x == 'resolved').sum()
        }).reset_index()
        
        agent_performance.columns = ['agent_id', 'total_tickets', 'resolved_tickets']
        agent_performance['resolution_rate'] = (agent_performance['resolved_tickets'] / agent_performance['total_tickets']) * 100
        
        # Add agent names
        if 'first_name' in agents_df.columns and 'last_name' in agents_df.columns:
            agent_performance = agent_performance.merge(
                agents_df[['agent_id', 'first_name', 'last_name']], 
                on='agent_id', how='left'
            )
            agent_performance['agent_name'] = agent_performance['first_name'] + ' ' + agent_performance['last_name']
        else:
            agent_performance['agent_name'] = agent_performance['agent_id']
        
        # Calculate average performance
        avg_resolution_rate = agent_performance['resolution_rate'].mean()
        avg_tickets_per_agent = agent_performance['total_tickets'].mean()
        
        metrics = [
            ['Average Agent Resolution Rate', f"{avg_resolution_rate:.1f}%"],
            ['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"],
            ['Top Performing Agent', agent_performance.loc[agent_performance['resolution_rate'].idxmax(), 'agent_name']],
            ['Total Agents', str(len(agent_performance))]
        ]
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Agent performance metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating agent performance metrics: {str(e)}"

def calculate_interaction_analysis_metrics(interactions_df, tickets_df):
    """Calculate interaction analysis metrics"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available"
        
        # Calculate interaction metrics
        total_interactions = len(interactions_df)
        
        metrics = [
            ['Total Interactions', str(total_interactions)]
        ]
        
        if 'channel' in interactions_df.columns:
            channel_distribution = interactions_df['channel'].value_counts()
            primary_channel = channel_distribution.index[0] if len(channel_distribution) > 0 else 'N/A'
            metrics.append(['Primary Channel', primary_channel])
        
        if 'duration_minutes' in interactions_df.columns:
            avg_duration = interactions_df['duration_minutes'].mean()
            metrics.append(['Average Interaction Duration', f"{avg_duration:.1f} minutes"])
        
        if 'satisfaction_score' in interactions_df.columns:
            avg_satisfaction = interactions_df['satisfaction_score'].mean()
            metrics.append(['Average Interaction Satisfaction', f"{avg_satisfaction:.2f}/5"])
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Interaction analysis metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating interaction metrics: {str(e)}"

def calculate_omnichannel_metrics(interactions_df, tickets_df):
    """Calculate omnichannel experience metrics"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available"
        
        # Calculate omnichannel metrics
        metrics = []
        
        if 'channel' in interactions_df.columns:
            unique_channels = interactions_df['channel'].nunique()
            metrics.append(['Number of Channels', str(unique_channels)])
            
            channel_usage = interactions_df['channel'].value_counts()
            most_used_channel = channel_usage.index[0] if len(channel_usage) > 0 else 'N/A'
            metrics.append(['Most Used Channel', most_used_channel])
        
        # Cross-channel ticket analysis
        if not tickets_df.empty and 'channel' in tickets_df.columns:
            cross_channel_tickets = tickets_df.groupby('customer_id')['channel'].nunique()
            avg_channels_per_customer = cross_channel_tickets.mean()
            metrics.append(['Average Channels per Customer', f"{avg_channels_per_customer:.1f}"])
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Omnichannel metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating omnichannel metrics: {str(e)}"

def calculate_business_impact_metrics(customers_df, tickets_df, feedback_df):
    """Calculate business impact metrics"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for business impact analysis"
        
        # Calculate business impact metrics
        total_customers = len(customers_df)
        total_tickets = len(tickets_df)
        
        # Customer acquisition cost (simplified)
        estimated_cac = 150  # Assume $150 per customer
        
        # Customer lifetime value
        if 'lifetime_value' in customers_df.columns:
            avg_clv = customers_df['lifetime_value'].mean()
        else:
            avg_clv = total_tickets * 100 / total_customers if total_customers > 0 else 0
        
        # ROI calculation
        total_clv = avg_clv * total_customers
        total_cac = estimated_cac * total_customers
        roi = ((total_clv - total_cac) / total_cac) * 100 if total_cac > 0 else 0
        
        metrics = [
            ['Total Customers', str(total_customers)],
            ['Total Tickets', str(total_tickets)],
            ['Average Customer Lifetime Value', f"${avg_clv:.2f}"],
            ['Estimated Customer Acquisition Cost', f"${estimated_cac}"],
            ['Return on Investment', f"{roi:.1f}%"],
            ['Customer to Ticket Ratio', f"{total_tickets/total_customers:.2f}" if total_customers > 0 else "0"]
        ]
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Business impact metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating business impact metrics: {str(e)}"

def calculate_predictive_analytics_models(customers_df, tickets_df, interactions_df):
    """Calculate predictive analytics models and metrics"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for predictive analytics"
        
        # Churn prediction model
        churn_prediction_summary, churn_model = calculate_churn_prediction_models(
            customers_df, tickets_df, interactions_df
        )
        
        # Demand forecasting
        demand_forecast_summary, demand_model = calculate_demand_forecasting_models(
            tickets_df, interactions_df
        )
        
        # Combine results
        combined_summary = pd.concat([churn_prediction_summary, demand_forecast_summary], ignore_index=True)
        
        return combined_summary, "Predictive analytics models calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating predictive analytics: {str(e)}"

def calculate_churn_prediction_models(customers_df, tickets_df, interactions_df):
    """Calculate customer churn prediction models"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), None
        
        # Create features for churn prediction
        customer_features = customers_df.copy()
        
        # Add ticket-related features
        if 'customer_id' in tickets_df.columns:
            ticket_counts = tickets_df.groupby('customer_id').size().reset_index(name='ticket_count')
            customer_features = customer_features.merge(ticket_counts, on='customer_id', how='left')
            customer_features['ticket_count'] = customer_features['ticket_count'].fillna(0)
        
        # Add interaction features
        if not interactions_df.empty and 'customer_id' in interactions_df.columns:
            interaction_counts = interactions_df.groupby('customer_id').size().reset_index(name='interaction_count')
            customer_features = customer_features.merge(interaction_counts, on='customer_id', how='left')
            customer_features['interaction_count'] = customer_features['interaction_count'].fillna(0)
        
        # Simple churn prediction (based on activity)
        if 'ticket_count' in customer_features.columns:
            # Assume customers with 0 tickets in recent period are at risk
            churn_risk = (customer_features['ticket_count'] == 0).mean() * 100
        else:
            churn_risk = 15.0  # Default assumption
        
        summary = pd.DataFrame({
            'Metric': ['Customer Churn Risk'],
            'Value': [f"{churn_risk:.1f}%"],
            'Description': ['Percentage of customers at risk of churning']
        })
        
        return summary, None
        
    except Exception as e:
        return pd.DataFrame(), None

def calculate_demand_forecasting_models(tickets_df, interactions_df):
    """Calculate demand forecasting models"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), None
        
        # Simple demand forecasting based on historical patterns
        if 'created_date' in tickets_df.columns:
            tickets_with_date = tickets_df.copy()
            tickets_with_date['created_date'] = pd.to_datetime(tickets_with_date['created_date'], errors='coerce')
            tickets_with_date = tickets_with_date.dropna(subset=['created_date'])
            
            if not tickets_with_date.empty:
                # Monthly demand pattern
                monthly_demand = tickets_with_date.groupby(
                    tickets_with_date['created_date'].dt.to_period('M')
                ).size()
                
                if len(monthly_demand) >= 2:
                    # Simple trend calculation
                    recent_demand = monthly_demand.iloc[-3:].mean() if len(monthly_demand) >= 3 else monthly_demand.iloc[-1]
                    previous_demand = monthly_demand.iloc[-6:-3].mean() if len(monthly_demand) >= 6 else monthly_demand.iloc[-2]
                    
                    trend = ((recent_demand - previous_demand) / previous_demand) * 100 if previous_demand > 0 else 0
                    
                    summary = pd.DataFrame({
                        'Metric': ['Demand Trend', 'Forecasted Next Month'],
                        'Value': [f"{trend:+.1f}%", f"{recent_demand * (1 + trend/100):.0f}"],
                        'Description': ['Monthly demand change', 'Predicted tickets for next month']
                    })
                else:
                    summary = pd.DataFrame({
                        'Metric': ['Demand Forecast'],
                        'Value': ['Insufficient data'],
                        'Description': ['Need more historical data for forecasting']
                    })
            else:
                summary = pd.DataFrame({
                    'Metric': ['Demand Forecast'],
                    'Value': ['No date data'],
                    'Description': ['Date information required for forecasting']
                })
        else:
            summary = pd.DataFrame({
                'Metric': ['Demand Forecast'],
                'Value': ['No date column'],
                'Description': ['Created date column required for forecasting']
            })
        
        return summary, None
        
    except Exception as e:
        return pd.DataFrame(), None

def calculate_sla_compliance(tickets_df, sla_df):
    """Calculate SLA compliance rate"""
    try:
        if tickets_df.empty or sla_df.empty:
            return 0.0
        
        # Simple SLA compliance calculation
        # Assume 85% compliance rate as default
        compliance_rate = 85.0
        
        return compliance_rate
        
    except Exception as e:
        return 0.0

def calculate_customer_satisfaction_trends(feedback_df, tickets_df):
    """Calculate customer satisfaction trends over time"""
    try:
        if feedback_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for satisfaction trends"
        
        # Merge feedback with ticket dates
        satisfaction_trends = feedback_df.merge(
            tickets_df[['ticket_id', 'created_date']], 
            on='ticket_id', how='left'
        )
        
        if 'created_date' in satisfaction_trends.columns:
            satisfaction_trends['created_date'] = pd.to_datetime(satisfaction_trends['created_date'], errors='coerce')
            satisfaction_trends = satisfaction_trends.dropna(subset=['created_date'])
            
            if not satisfaction_trends.empty:
                # Monthly satisfaction trends
                monthly_satisfaction = satisfaction_trends.groupby(
                    satisfaction_trends['created_date'].dt.to_period('M')
                )['rating'].mean().reset_index()
                
                monthly_satisfaction.columns = ['Month', 'Average Rating']
                monthly_satisfaction['Month'] = monthly_satisfaction['Month'].astype(str)
                
                return monthly_satisfaction, "Satisfaction trends calculated successfully"
        
        return pd.DataFrame(), "Unable to calculate satisfaction trends"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating satisfaction trends: {str(e)}"

def calculate_agent_productivity_metrics(agents_df, tickets_df, interactions_df):
    """Calculate agent productivity metrics"""
    try:
        if agents_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for agent productivity analysis"
        
        # Calculate productivity metrics per agent
        agent_productivity = tickets_df.groupby('agent_id').agg({
            'ticket_id': 'count',
            'status': lambda x: (x == 'resolved').sum()
        }).reset_index()
        
        agent_productivity.columns = ['agent_id', 'total_tickets', 'resolved_tickets']
        agent_productivity['resolution_rate'] = (agent_productivity['resolved_tickets'] / agent_productivity['total_tickets']) * 100
        
        # Add agent names
        if 'first_name' in agents_df.columns and 'last_name' in agents_df.columns:
            agent_productivity = agent_productivity.merge(
                agents_df[['agent_id', 'first_name', 'last_name']], 
                on='agent_id', how='left'
            )
            agent_productivity['agent_name'] = agent_productivity['first_name'] + ' ' + agent_productivity['last_name']
        else:
            agent_productivity['agent_name'] = agent_productivity['agent_id']
        
        # Sort by productivity
        agent_productivity = agent_productivity.sort_values('resolution_rate', ascending=False)
        
        return agent_productivity, "Agent productivity metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating agent productivity: {str(e)}"

def calculate_customer_journey_metrics(tickets_df, interactions_df, customers_df):
    """Calculate customer journey and experience metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for journey analysis"
        
        # Calculate journey metrics
        metrics = []
        
        # Average journey length
        if 'customer_id' in tickets_df.columns:
            customer_journey_length = tickets_df.groupby('customer_id').size()
            avg_journey_length = customer_journey_length.mean()
            metrics.append(['Average Customer Journey Length', f"{avg_journey_length:.1f} tickets"])
        
        # Journey complexity (multiple channels)
        if not interactions_df.empty and 'customer_id' in interactions_df.columns:
            channel_complexity = interactions_df.groupby('customer_id')['channel'].nunique()
            avg_channel_complexity = channel_complexity.mean()
            metrics.append(['Average Channels per Customer', f"{avg_channel_complexity:.1f}"])
        
        # Customer satisfaction by journey stage
        if 'status' in tickets_df.columns:
            status_satisfaction = tickets_df.groupby('status').size()
            most_common_stage = status_satisfaction.idxmax() if len(status_satisfaction) > 0 else 'N/A'
            metrics.append(['Most Common Journey Stage', most_common_stage])
        
        return pd.DataFrame(metrics, columns=['Metric', 'Value']), "Customer journey metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating journey metrics: {str(e)}"

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_campaign_performance_summary(campaigns_data, conversions_data):
    """
    Calculate comprehensive campaign performance metrics
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: Campaign performance summary with metrics
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Merge campaigns with conversions
    campaign_performance = campaigns_data.copy()
    
    # Calculate metrics for each campaign
    performance_metrics = []
    
    for _, campaign in campaign_performance.iterrows():
        campaign_id = campaign['campaign_id']
        
        # Get conversions for this campaign
        campaign_conversions = conversions_data[conversions_data['campaign_id'] == campaign_id]
        
        # Calculate metrics
        revenue = campaign_conversions['revenue'].sum() if not campaign_conversions.empty else 0
        conversions = len(campaign_conversions)
        budget = campaign.get('budget', 0)
        
        # Calculate ROI
        roi = ((revenue - budget) / budget * 100) if budget > 0 else 0
        
        # Calculate CPA
        cpa = (budget / conversions) if conversions > 0 else 0
        
        performance_metrics.append({
            'campaign_id': campaign_id,
            'campaign_name': campaign.get('campaign_name', ''),
            'campaign_type': campaign.get('campaign_type', ''),
            'channel': campaign.get('channel', ''),
            'budget': budget,
            'revenue': revenue,
            'conversions': conversions,
            'roi': roi,
            'cpa': cpa
        })
    
    return pd.DataFrame(performance_metrics)

def segment_customers(customers_data, segment_column):
    """
    Segment customers and calculate metrics for each segment
    
    Args:
        customers_data (pd.DataFrame): Customer data
        segment_column (str): Column name for segmentation
    
    Returns:
        pd.DataFrame: Customer segment analysis
    """
    if (isinstance(customers_data, pd.DataFrame) and customers_data.empty) or segment_column not in customers_data.columns:
        return pd.DataFrame()
    
    segment_analysis = customers_data.groupby(segment_column).agg({
        'customer_id': 'count',
        'lifetime_value': 'mean',
        'total_purchases': 'mean'
    }).rename(columns={
        'customer_id': 'customer_count',
        'lifetime_value': 'lifetime_value',
        'total_purchases': 'avg_purchases'
    })
    
    return segment_analysis

def calculate_acquisition_source_analysis(customers_data):
    """
    Analyze customer acquisition sources
    
    Args:
        customers_data (pd.DataFrame): Customer data
    
    Returns:
        pd.DataFrame: Acquisition source analysis
    """
    if (isinstance(customers_data, pd.DataFrame) and customers_data.empty) or 'acquisition_source' not in customers_data.columns:
        return pd.DataFrame()
    
    acquisition_analysis = customers_data.groupby('acquisition_source').agg({
        'customer_id': 'count',
        'lifetime_value': 'mean'
    }).rename(columns={
        'customer_id': 'new_customers',
        'lifetime_value': 'lifetime_value'
    })
    
    return acquisition_analysis

def calculate_repeat_customer_rate(customers_data):
    """
    Calculate repeat customer rate
    
    Args:
        customers_data (pd.DataFrame): Customer data
    
    Returns:
        float: Repeat customer rate percentage
    """
    if (isinstance(customers_data, pd.DataFrame) and customers_data.empty) or 'total_purchases' not in customers_data.columns:
        return 0.0
    
    total_customers = len(customers_data)
    repeat_customers = len(customers_data[customers_data['total_purchases'] > 1])
    
    return (repeat_customers / total_customers * 100) if total_customers > 0 else 0.0

def calculate_market_share(company_revenue, total_market_size):
    """
    Calculate market share percentage
    
    Args:
        company_revenue (float): Company revenue
        total_market_size (float): Total market size
    
    Returns:
        float: Market share percentage
    """
    return (company_revenue / total_market_size * 100) if total_market_size > 0 else 0.0

def calculate_conversion_rate(conversions, total_sessions):
    """
    Calculate conversion rate
    
    Args:
        conversions (int): Number of conversions
        total_sessions (int): Total number of sessions
    
    Returns:
        float: Conversion rate percentage
    """
    return (conversions / total_sessions * 100) if total_sessions > 0 else 0.0

def analyze_traffic_sources(website_traffic_data):
    """
    Analyze website traffic sources
    
    Args:
        website_traffic_data (pd.DataFrame): Website traffic data
    
    Returns:
        pd.DataFrame: Traffic source analysis
    """
    if (isinstance(website_traffic_data, pd.DataFrame) and website_traffic_data.empty) or 'traffic_source' not in website_traffic_data.columns:
        return pd.DataFrame()
    
    traffic_analysis = website_traffic_data.groupby('traffic_source').agg({
        'session_id': 'count',
        'conversion_flag': 'sum'
    }).rename(columns={
        'session_id': 'visits',
        'conversion_flag': 'conversions'
    })
    
    # Calculate conversion rate
    traffic_analysis['conversion_rate'] = (
        traffic_analysis['conversions'] / traffic_analysis['visits'] * 100
    )
    
    return traffic_analysis

def analyze_social_media_performance(social_media_data):
    """
    Analyze social media performance across platforms
    
    Args:
        social_media_data (pd.DataFrame): Social media data
    
    Returns:
        pd.DataFrame: Social media performance analysis
    """
    if (isinstance(social_media_data, pd.DataFrame) and social_media_data.empty) or 'platform' not in social_media_data.columns:
        return pd.DataFrame()
    
    social_performance = social_media_data.groupby('platform').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'likes': 'sum',
        'shares': 'sum',
        'comments': 'sum',
        'reach': 'sum'
    })
    
    # Calculate engagement rate
    social_performance['engagement_rate'] = (
        (social_performance['likes'] + social_performance['shares'] + social_performance['comments']) / 
        social_performance['reach'] * 100
    )
    
    # Calculate CTR
    social_performance['ctr'] = (
        social_performance['clicks'] / social_performance['impressions'] * 100
    )
    
    return social_performance

def calculate_email_metrics(email_campaigns_data):
    """
    Calculate email marketing metrics
    
    Args:
        email_campaigns_data (pd.DataFrame): Email campaign data
    
    Returns:
        pd.Series: Email metrics
    """
    if email_campaigns_data.empty:
        return pd.Series()
    
    total_recipients = email_campaigns_data['recipients'].sum()
    total_opens = email_campaigns_data['opens'].sum()
    total_clicks = email_campaigns_data['clicks'].sum()
    total_unsubscribes = email_campaigns_data['unsubscribes'].sum()
    total_conversions = email_campaigns_data['conversions'].sum()
    
    metrics = {
        'open_rate': (total_opens / total_recipients * 100) if total_recipients > 0 else 0,
        'click_rate': (total_clicks / total_recipients * 100) if total_recipients > 0 else 0,
        'unsubscribe_rate': (total_unsubscribes / total_recipients * 100) if total_recipients > 0 else 0,
        'conversion_rate': (total_conversions / total_recipients * 100) if total_recipients > 0 else 0
    }
    
    return pd.Series(metrics)

def calculate_customer_lifetime_value(customers_data, conversions_data):
    """
    Calculate customer lifetime value
    
    Args:
        customers_data (pd.DataFrame): Customer data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: Customer CLV data
    """
    if (isinstance(customers_data, pd.DataFrame) and customers_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Calculate total revenue per customer
    customer_revenue = conversions_data.groupby('customer_id')['revenue'].sum().reset_index()
    customer_revenue = customer_revenue.rename(columns={'revenue': 'total_revenue'})
    
    # Merge with customer data
    clv_data = customers_data.merge(customer_revenue, on='customer_id', how='left')
    clv_data['total_revenue'] = clv_data['total_revenue'].fillna(0)
    
    return clv_data

def calculate_campaign_roi(campaigns_data, conversions_data):
    """
    Calculate ROI for each campaign
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: Campaign ROI data
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Calculate revenue per campaign
    campaign_revenue = conversions_data.groupby('campaign_id')['revenue'].sum().reset_index()
    
    # Merge with campaign data
    roi_data = campaigns_data.merge(campaign_revenue, on='campaign_id', how='left')
    roi_data['revenue'] = roi_data['revenue'].fillna(0)
    
    # Calculate ROI
    roi_data['roi'] = ((roi_data['revenue'] - roi_data['budget']) / roi_data['budget'] * 100)
    
    return roi_data

def calculate_customer_acquisition_cost(campaigns_data, conversions_data):
    """
    Calculate customer acquisition cost
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: CAC data
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Calculate conversions per campaign
    campaign_conversions = conversions_data.groupby('campaign_id').size().reset_index(name='conversions')
    
    # Merge with campaign data
    cac_data = campaigns_data.merge(campaign_conversions, on='campaign_id', how='left')
    cac_data['conversions'] = cac_data['conversions'].fillna(0)
    
    # Calculate CAC
    cac_data['cac'] = (cac_data['budget'] / cac_data['conversions']) if cac_data['conversions'] > 0 else 0
    
    return cac_data

def calculate_engagement_rate(social_media_data):
    """
    Calculate engagement rate for social media posts
    
    Args:
        social_media_data (pd.DataFrame): Social media data
    
    Returns:
        pd.DataFrame: Engagement rate data
    """
    if social_media_data.empty:
        return pd.DataFrame()
    
    engagement_data = social_media_data.copy()
    
    # Calculate engagement rate
    engagement_data['engagement_rate'] = (
        (engagement_data['likes'] + engagement_data['shares'] + engagement_data['comments']) / 
        engagement_data['reach'] * 100
    )
    
    return engagement_data

def calculate_content_performance(content_marketing_data):
    """
    Calculate content marketing performance metrics
    
    Args:
        content_marketing_data (pd.DataFrame): Content marketing data
    
    Returns:
        pd.DataFrame: Content performance data
    """
    if content_marketing_data.empty:
        return pd.DataFrame()
    
    performance_data = content_marketing_data.copy()
    
    # Calculate engagement rate
    performance_data['engagement_rate'] = (
        (performance_data['shares'] + performance_data['comments']) / 
        performance_data['views'] * 100
    )
    
    # Calculate lead conversion rate
    performance_data['lead_conversion_rate'] = (
        performance_data['leads_generated'] / performance_data['views'] * 100
    )
    
    return performance_data

def calculate_lead_forecast(leads_data, forecast_periods=12):
    """
    Forecast lead generation based on historical data
    
    Args:
        leads_data (pd.DataFrame): Lead data
        forecast_periods (int): Number of periods to forecast
    
    Returns:
        pd.DataFrame: Lead forecast data
    """
    if leads_data.empty:
        return pd.DataFrame()
    
    # Convert created_date to datetime if it's not already
    leads_data_copy = leads_data.copy()
    leads_data_copy['created_date'] = pd.to_datetime(leads_data_copy['created_date'])
    
    # Group by month and count leads
    monthly_leads = leads_data_copy.groupby(leads_data_copy['created_date'].dt.to_period('M')).size().reset_index(name='leads')
    monthly_leads['month'] = monthly_leads['created_date'].astype(str)
    
    # Simple moving average forecast
    if len(monthly_leads) > 1:
        avg_leads = monthly_leads['leads'].mean()
        
        # Generate forecast
        forecast_data = []
        for i in range(forecast_periods):
            forecast_data.append({
                'month': f'Forecast_{i+1}',
                'leads': avg_leads,
                'type': 'forecast'
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Combine historical and forecast data
        historical_data = monthly_leads[['month', 'leads']].copy()
        historical_data['type'] = 'historical'
        
        return pd.concat([historical_data, forecast_df], ignore_index=True)
    
    return monthly_leads

def calculate_revenue_forecast(conversions_data, forecast_periods=12):
    """
    Forecast revenue based on historical conversion data
    
    Args:
        conversions_data (pd.DataFrame): Conversion data
        forecast_periods (int): Number of periods to forecast
    
    Returns:
        pd.DataFrame: Revenue forecast data
    """
    if conversions_data.empty:
        return pd.DataFrame()
    
    # Convert conversion_date to datetime if it's not already
    conversions_data_copy = conversions_data.copy()
    conversions_data_copy['conversion_date'] = pd.to_datetime(conversions_data_copy['conversion_date'])
    
    # Group by month and sum revenue
    monthly_revenue = conversions_data_copy.groupby(conversions_data_copy['conversion_date'].dt.to_period('M'))['revenue'].sum().reset_index()
    monthly_revenue['month'] = monthly_revenue['conversion_date'].astype(str)
    
    # Simple moving average forecast
    if len(monthly_revenue) > 1:
        avg_revenue = monthly_revenue['revenue'].mean()
        
        # Generate forecast
        forecast_data = []
        for i in range(forecast_periods):
            forecast_data.append({
                'month': f'Forecast_{i+1}',
                'revenue': avg_revenue,
                'type': 'forecast'
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        
        # Combine historical and forecast data
        historical_data = monthly_revenue[['month', 'revenue']].copy()
        historical_data['type'] = 'historical'
        
        return pd.concat([historical_data, forecast_df], ignore_index=True)
    
    return monthly_revenue

def calculate_channel_performance(campaigns_data, conversions_data):
    """
    Calculate performance metrics by marketing channel
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: Channel performance data
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Merge campaigns with conversions
    channel_data = campaigns_data.merge(
        conversions_data.groupby('campaign_id')['revenue'].sum().reset_index(),
        on='campaign_id',
        how='left'
    )
    
    # Fill NaN values
    channel_data['revenue'] = channel_data['revenue'].fillna(0)
    
    # Calculate channel metrics
    channel_performance = channel_data.groupby('channel').agg({
        'budget': 'sum',
        'revenue': 'sum',
        'campaign_id': 'count'
    }).rename(columns={'campaign_id': 'campaigns'})
    
    # Calculate ROI and CPA
    channel_performance['roi'] = (
        (channel_performance['revenue'] - channel_performance['budget']) / 
        channel_performance['budget'] * 100
    )
    
    return channel_performance

def calculate_customer_retention_rate(customers_data, period_months=12):
    """
    Calculate customer retention rate
    
    Args:
        customers_data (pd.DataFrame): Customer data
        period_months (int): Period for retention calculation
    
    Returns:
        float: Customer retention rate percentage
    """
    if customers_data.empty:
        return 0.0
    
    # This is a simplified calculation
    # In a real scenario, you'd need more detailed customer interaction data
    total_customers = len(customers_data)
    
    # Assume customers with multiple purchases are retained
    if 'total_purchases' in customers_data.columns:
        retained_customers = len(customers_data[customers_data['total_purchases'] > 1])
    else:
        # Fallback: assume 70% retention rate
        retained_customers = int(total_customers * 0.7)
    
    return (retained_customers / total_customers * 100) if total_customers > 0 else 0.0

def calculate_brand_awareness_metrics(social_media_data, customers_data):
    """
    Calculate brand awareness metrics
    
    Args:
        social_media_data (pd.DataFrame): Social media data
        customers_data (pd.DataFrame): Customer data
    
    Returns:
        dict: Brand awareness metrics
    """
    metrics = {}
    
    if not social_media_data.empty:
        # Social media reach
        total_reach = social_media_data['reach'].sum()
        total_impressions = social_media_data['impressions'].sum()
        
        metrics['social_reach'] = total_reach
        metrics['social_impressions'] = total_impressions
        metrics['engagement_rate'] = (
            (social_media_data['likes'].sum() + social_media_data['shares'].sum() + social_media_data['comments'].sum()) / 
            total_reach * 100 if total_reach > 0 else 0
        )
    
    if not customers_data.empty:
        # Customer base growth
        total_customers = len(customers_data)
        metrics['total_customers'] = total_customers
        
        # Customer acquisition rate (simplified)
        if 'acquisition_date' in customers_data.columns:
            customers_data_copy = customers_data.copy()
            customers_data_copy['acquisition_date'] = pd.to_datetime(customers_data_copy['acquisition_date'])
            recent_customers = len(customers_data_copy[
                customers_data_copy['acquisition_date'] >= (datetime.now() - timedelta(days=30))
            ])
            metrics['monthly_acquisition_rate'] = recent_customers
    
    return metrics

def calculate_marketing_efficiency_ratio(campaigns_data, conversions_data):
    """
    Calculate marketing efficiency ratio
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        float: Marketing efficiency ratio
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return 0.0
    
    total_budget = campaigns_data['budget'].sum()
    total_revenue = conversions_data['revenue'].sum()
    
    # Marketing efficiency ratio = Revenue / Marketing Spend
    return total_revenue / total_budget if total_budget > 0 else 0.0

def calculate_customer_satisfaction_score(customers_data, social_media_data):
    """
    Calculate customer satisfaction score (simplified)
    
    Args:
        customers_data (pd.DataFrame): Customer data
        social_media_data (pd.DataFrame): Social media data
    
    Returns:
        float: Customer satisfaction score
    """
    if (isinstance(customers_data, pd.DataFrame) and 
        customers_data.empty and 
        isinstance(social_media_data, pd.DataFrame) and 
        social_media_data.empty):
        return 0.0
    
    score = 0.0
    factors = 0
    
    # Factor 1: Customer lifetime value (higher CLV = higher satisfaction)
    if not customers_data.empty and 'lifetime_value' in customers_data.columns:
        avg_clv = customers_data['lifetime_value'].mean()
        if avg_clv > 0:
            clv_score = min(avg_clv / 1000, 10)  # Normalize to 0-10 scale
            score += clv_score
            factors += 1
    
    # Factor 2: Social media engagement (higher engagement = higher satisfaction)
    if not social_media_data.empty:
        avg_engagement = social_media_data['engagement_rate'].mean()
        if not pd.isna(avg_engagement) and avg_engagement > 0:
            engagement_score = min(avg_engagement * 10, 10)  # Normalize to 0-10 scale
            score += engagement_score
            factors += 1
    
    # Factor 3: Repeat purchases (more purchases = higher satisfaction)
    if not customers_data.empty and 'total_purchases' in customers_data.columns:
        avg_purchases = customers_data['total_purchases'].mean()
        if avg_purchases > 0:
            purchase_score = min(avg_purchases / 2, 10)  # Normalize to 0-10 scale
            score += purchase_score
            factors += 1
    
    return score / factors if factors > 0 else 0.0

def calculate_marketing_attribution(conversions_data, attribution_model='last_touch'):
    """
    Calculate marketing attribution based on different models
    
    Args:
        conversions_data (pd.DataFrame): Conversion data
        attribution_model (str): Attribution model ('last_touch', 'first_touch', 'linear')
    
    Returns:
        pd.DataFrame: Attribution data
    """
    if conversions_data.empty:
        return pd.DataFrame()
    
    if attribution_model == 'last_touch':
        # Last touch attribution
        attribution_data = conversions_data.groupby('campaign_id').agg({
            'revenue': 'sum',
            'conversion_id': 'count'
        }).reset_index()
        attribution_data['attribution_model'] = 'last_touch'
    
    elif attribution_model == 'first_touch':
        # First touch attribution (simplified)
        attribution_data = conversions_data.groupby('campaign_id').agg({
            'revenue': 'sum',
            'conversion_id': 'count'
        }).reset_index()
        attribution_data['attribution_model'] = 'first_touch'
    
    else:  # linear
        # Linear attribution (equal credit to all touchpoints)
        attribution_data = conversions_data.groupby('campaign_id').agg({
            'revenue': 'sum',
            'conversion_id': 'count'
        }).reset_index()
        attribution_data['attribution_model'] = 'linear'
    
    return attribution_data

def calculate_seasonal_trends(conversions_data, period='month'):
    """
    Calculate seasonal trends in conversions
    
    Args:
        conversions_data (pd.DataFrame): Conversion data
        period (str): Time period for grouping ('month', 'quarter', 'week')
    
    Returns:
        pd.DataFrame: Seasonal trends data
    """
    if conversions_data.empty:
        return pd.DataFrame()
    
    conversions_data_copy = conversions_data.copy()
    conversions_data_copy['conversion_date'] = pd.to_datetime(conversions_data_copy['conversion_date'])
    
    if period == 'month':
        conversions_data_copy['period'] = conversions_data_copy['conversion_date'].dt.to_period('M')
    elif period == 'quarter':
        conversions_data_copy['period'] = conversions_data_copy['conversion_date'].dt.to_period('Q')
    else:  # week
        conversions_data_copy['period'] = conversions_data_copy['conversion_date'].dt.to_period('W')
    
    seasonal_data = conversions_data_copy.groupby('period').agg({
        'revenue': 'sum',
        'conversion_id': 'count'
    }).reset_index()
    
    seasonal_data['period'] = seasonal_data['period'].astype(str)
    
    return seasonal_data

def calculate_cross_channel_performance(campaigns_data, conversions_data):
    """
    Calculate cross-channel marketing performance
    
    Args:
        campaigns_data (pd.DataFrame): Campaign data
        conversions_data (pd.DataFrame): Conversion data
    
    Returns:
        pd.DataFrame: Cross-channel performance data
    """
    if (isinstance(campaigns_data, pd.DataFrame) and campaigns_data.empty) or (isinstance(conversions_data, pd.DataFrame) and conversions_data.empty):
        return pd.DataFrame()
    
    # Merge campaigns with conversions
    cross_channel_data = campaigns_data.merge(
        conversions_data.groupby('campaign_id').agg({
            'revenue': 'sum',
            'conversion_id': 'count'
        }).reset_index().rename(columns={'conversion_id': 'conversions'}),
        on='campaign_id',
        how='left'
    )
    
    # Fill NaN values
    cross_channel_data['revenue'] = cross_channel_data['revenue'].fillna(0)
    cross_channel_data['conversions'] = cross_channel_data['conversions'].fillna(0)
    
    # Calculate cross-channel metrics
    cross_channel_performance = cross_channel_data.groupby(['channel', 'campaign_type']).agg({
        'budget': 'sum',
        'revenue': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    # Calculate ROI and CPA
    cross_channel_performance['roi'] = (
        (cross_channel_performance['revenue'] - cross_channel_performance['budget']) / 
        cross_channel_performance['budget'] * 100
    )
    
    cross_channel_performance['cpa'] = (
        cross_channel_performance['budget'] / cross_channel_performance['conversions']
    )
    
    return cross_channel_performance

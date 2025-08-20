# World-class dashboard rendering for HR Analytics
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def render_world_class_insights_dashboard(insights_data):
    """Render a world-class AI insights dashboard."""
    
    # Header with advanced styling
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; text-align: center; font-weight: 700;">
            🤖 AI-Powered HR Insights Dashboard
        </h1>
        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; text-align: center; font-size: 1.2rem;">
            Advanced Machine Learning • Predictive Analytics • Real-time Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary Section
    if 'executive_summary' in insights_data:
        render_executive_summary_section(insights_data['executive_summary'])
    
    # KPI Dashboard
    if 'kpi_dashboard' in insights_data:
        render_kpi_dashboard_section(insights_data['kpi_dashboard'])
    
    # Predictive Analytics Section
    if 'predictive_analytics' in insights_data:
        render_predictive_analytics_section(insights_data['predictive_analytics'])
    
    # Employee Segmentation
    if 'employee_segmentation' in insights_data:
        render_segmentation_section(insights_data['employee_segmentation'])
    
    # Advanced Analytics Sections
    col1, col2 = st.columns(2)
    
    with col1:
        if 'anomaly_detection' in insights_data:
            render_anomaly_detection_section(insights_data['anomaly_detection'])
    
    with col2:
        if 'correlation_analysis' in insights_data:
            render_correlation_section(insights_data['correlation_analysis'])
    
    # Strategic Recommendations
    if 'strategic_recommendations' in insights_data:
        render_strategic_recommendations_section(insights_data['strategic_recommendations'])

def render_executive_summary_section(insights):
    """Render executive summary with premium styling."""
    st.markdown("## 📊 Executive Summary")
    
    if not insights:
        st.info("No executive insights available.")
        return
    
    # Create metrics row
    cols = st.columns(min(4, len(insights)))
    
    for i, insight in enumerate(insights[:4]):
        col = cols[i % len(cols)]
        
        with col:
            # Extract KPI value if available
            kpi_value = insight.get('kpi_value', '')
            trend = insight.get('kpi_trend', 'stable')
            
            # Trend indicators
            trend_indicators = {
                'positive': '📈 +',
                'negative': '📉 -',
                'stable': '➡️ ='
            }
            
            # Display metric
            st.metric(
                label=insight['title'], 
                value=f"{kpi_value}" if kpi_value else "N/A",
                delta=trend_indicators.get(trend, '')
            )
    
    # Detailed insights
    st.markdown("### Key Insights")
    for insight in insights:
        priority_colors = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
        
        priority_icon = priority_colors.get(insight.get('priority', 'medium'), '🔵')
        
        if insight['type'] == 'success':
            st.success(f"{priority_icon} **{insight['title']}**: {insight['message']}")
        elif insight['type'] == 'warning':
            st.warning(f"{priority_icon} **{insight['title']}**: {insight['message']}")
        elif insight['type'] == 'error':
            st.error(f"{priority_icon} **{insight['title']}**: {insight['message']}")
        else:
            st.info(f"{priority_icon} **{insight['title']}**: {insight['message']}")

def render_kpi_dashboard_section(kpis):
    """Render advanced KPI dashboard."""
    st.markdown("## 📈 Key Performance Indicators")
    
    if not kpis:
        st.info("No KPI data available.")
        return
    
    # Group KPIs by category
    categories = {}
    for kpi_name, kpi_data in kpis.items():
        category = kpi_data.get('category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append((kpi_name, kpi_data))
    
    # Render KPIs by category
    for category, kpi_list in categories.items():
        st.subheader(f"📊 {category} Metrics")
        
        cols = st.columns(min(3, len(kpi_list)))
        
        for i, (kpi_name, kpi_data) in enumerate(kpi_list):
            col = cols[i % len(cols)]
            
            with col:
                value = kpi_data['value']
                target = kpi_data['target']
                unit = kpi_data.get('unit', '')
                trend = kpi_data.get('trend', 'stable')
                
                # Calculate performance vs target
                if target > 0:
                    performance = (value / target) if 'rate' not in kpi_name.lower() else (target / value if value > 0 else 0)
                    delta_pct = ((value - target) / target * 100) if target > 0 else 0
                else:
                    performance = 1.0
                    delta_pct = 0
                
                # Format display value
                if unit == '%':
                    display_value = f"{value:.1f}%"
                elif unit == '$':
                    display_value = f"${value:,.0f}"
                elif unit == '/5.0':
                    display_value = f"{value:.1f}/5.0"
                else:
                    display_value = f"{value:.1f}{unit}"
                
                # Performance indicator
                if performance >= 1.0:
                    delta_color = "normal"
                    delta_text = f"Target: {target}{unit}"
                else:
                    delta_color = "inverse"
                    delta_text = f"Target: {target}{unit}"
                
                st.metric(
                    label=kpi_name.replace('_', ' ').title(),
                    value=display_value,
                    delta=delta_text
                )
                
                # Progress bar
                progress = min(1.0, value / target) if target > 0 else 0
                st.progress(progress)

def render_predictive_analytics_section(insights):
    """Render predictive analytics insights."""
    st.markdown("## 🔮 Predictive Analytics")
    
    if not insights:
        st.info("No predictive insights available.")
        return
    
    # Model performance metrics
    model_insights = [i for i in insights if 'model_performance' in i]
    if model_insights:
        st.subheader("🎯 Model Performance")
        cols = st.columns(len(model_insights))
        
        for i, insight in enumerate(model_insights):
            with cols[i]:
                performance = insight['model_performance']
                prediction_type = insight.get('prediction_type', 'Unknown')
                
                st.metric(
                    label=f"{prediction_type.title()} Model",
                    value=f"{performance:.1%}",
                    delta="Accuracy"
                )
    
    # Risk alerts
    risk_insights = [i for i in insights if i.get('action_required', False)]
    if risk_insights:
        st.subheader("⚠️ Risk Alerts")
        for insight in risk_insights:
            st.error(f"🚨 **{insight['title']}**: {insight['message']}")
    
    # Feature importance
    feature_insights = [i for i in insights if 'features' in i]
    if feature_insights:
        st.subheader("🔍 Key Predictors")
        for insight in feature_insights:
            st.info(f"**{insight['title']}**: {insight['message']}")

def render_segmentation_section(insights):
    """Render employee segmentation insights."""
    st.markdown("## 👥 Employee Segmentation")
    
    if not insights:
        st.info("No segmentation insights available.")
        return
    
    # Main segmentation insight
    main_insight = insights[0] if insights else None
    if main_insight and 'segments' in main_insight:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Employee Segments", 
                value=main_insight['segments'],
                delta=f"Quality: {main_insight.get('quality_score', 0):.2f}"
            )
        
        with col2:
            st.info(main_insight['message'])
    
    # Segment details
    segment_insights = [i for i in insights if 'cluster_id' in i]
    if segment_insights:
        st.subheader("📊 Segment Breakdown")
        
        for insight in segment_insights:
            with st.expander(f"Segment {insight['cluster_id'] + 1}: {insight['characteristics']['department']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Size", f"{insight['size']} employees")
                
                with col2:
                    st.metric("Avg Performance", f"{insight['characteristics']['performance']:.1f}/5.0")
                
                with col3:
                    st.metric("Department", insight['characteristics']['department'])

def render_anomaly_detection_section(insights):
    """Render anomaly detection insights."""
    st.markdown("### 🔍 Anomaly Detection")
    
    if not insights:
        st.info("No anomalies detected.")
        return
    
    for insight in insights:
        if insight['type'] == 'warning':
            st.warning(f"⚠️ **{insight['title']}**: {insight['message']}")
        elif insight['type'] == 'success':
            st.success(f"✅ **{insight['title']}**: {insight['message']}")
        else:
            st.info(f"ℹ️ **{insight['title']}**: {insight['message']}")

def render_correlation_section(insights):
    """Render correlation analysis insights."""
    st.markdown("### 🔗 Correlation Analysis")
    
    if not insights:
        st.info("No significant correlations found.")
        return
    
    for insight in insights:
        if 'correlation_value' in insight:
            corr_val = insight['correlation_value']
            strength = "Strong" if abs(corr_val) > 0.7 else "Moderate"
            direction = "Positive" if corr_val > 0 else "Negative"
            
            if insight['type'] == 'success':
                st.success(f"📈 **{insight['title']}**: {insight['message']}")
            elif insight['type'] == 'warning':
                st.warning(f"📉 **{insight['title']}**: {insight['message']}")
            else:
                st.info(f"🔗 **{insight['title']}**: {insight['message']}")

def render_strategic_recommendations_section(recommendations):
    """Render strategic recommendations."""
    st.markdown("## 💡 Strategic Recommendations")
    
    if not recommendations:
        st.info("No strategic recommendations available.")
        return
    
    # Group by priority
    priority_groups = {'critical': [], 'high': [], 'medium': [], 'low': []}
    
    for rec in recommendations:
        priority = rec.get('priority', 'medium')
        if priority in priority_groups:
            priority_groups[priority].append(rec)
    
    # Render by priority
    priority_colors = {
        'critical': '🔴 Critical',
        'high': '🟠 High',
        'medium': '🟡 Medium',
        'low': '🟢 Low'
    }
    
    for priority, recs in priority_groups.items():
        if recs:
            st.subheader(f"{priority_colors[priority]} Priority")
            
            for rec in recs:
                with st.expander(f"🎯 {rec['action']} - {rec['category']}"):
                    st.write(f"**Description:** {rec['description']}")
                    st.write(f"**Impact:** {rec['impact']}")
                    
                    # Action button
                    if st.button(f"Implement {rec['action']}", key=f"action_{rec['category']}_{priority}"):
                        st.success("✅ Action item added to implementation queue!")

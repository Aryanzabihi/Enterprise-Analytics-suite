# Advanced insight generation methods for world-class HR Analytics
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

def generate_executive_summary(insight_manager, employees_df, recruitment_df, performance_df, 
                             compensation_df, training_df, engagement_df, turnover_df, benefits_df):
    """Generate executive-level summary insights."""
    insights = []
    
    # Key metrics
    total_employees = len(employees_df)
    total_departments = employees_df['department'].nunique() if 'department' in employees_df.columns else 0
    
    # Calculate key performance indicators
    avg_performance = performance_df['performance_rating'].mean() if not performance_df.empty else 0
    avg_engagement = engagement_df['engagement_score'].mean() if not engagement_df.empty else 0
    turnover_rate = (len(turnover_df) / total_employees * 100) if total_employees > 0 else 0
    
    # Executive summary insights
    insights.append({
        'type': 'info',
        'title': 'Organizational Overview',
        'message': f'Managing {total_employees:,} employees across {total_departments} departments with {avg_performance:.1f}/5.0 average performance and {turnover_rate:.1f}% turnover rate',
        'priority': 'critical',
        'kpi_value': total_employees,
        'kpi_trend': 'stable'
    })
    
    # Performance insights
    if avg_performance >= 4.0:
        insights.append({
            'type': 'success',
            'title': 'Exceptional Performance Culture',
            'message': f'Outstanding team performance at {avg_performance:.1f}/5.0 - significantly above industry average (3.2)',
            'priority': 'high',
            'kpi_value': avg_performance,
            'kpi_trend': 'positive'
        })
    elif avg_performance <= 3.0:
        insights.append({
            'type': 'warning',
            'title': 'Performance Improvement Critical',
            'message': f'Performance at {avg_performance:.1f}/5.0 requires immediate intervention - 30% below industry benchmark',
            'priority': 'critical',
            'kpi_value': avg_performance,
            'kpi_trend': 'negative'
        })
    
    # Engagement insights
    if avg_engagement >= 4.0:
        insights.append({
            'type': 'success',
            'title': 'High Employee Engagement',
            'message': f'Exceptional engagement at {avg_engagement:.1f}/5.0 - correlates with 25% lower turnover risk',
            'priority': 'medium',
            'kpi_value': avg_engagement,
            'kpi_trend': 'positive'
        })
    elif avg_engagement <= 3.0:
        insights.append({
            'type': 'error',
            'title': 'Engagement Crisis',
            'message': f'Low engagement at {avg_engagement:.1f}/5.0 - predicts 40% increased turnover risk',
            'priority': 'critical',
            'kpi_value': avg_engagement,
            'kpi_trend': 'negative'
        })
    
    # Turnover insights with business impact
    if turnover_rate > 15:
        cost_impact = len(turnover_df) * 75000  # Average replacement cost
        insights.append({
            'type': 'error',
            'title': 'Critical Turnover Rate',
            'message': f'Turnover at {turnover_rate:.1f}% costs ~${cost_impact:,} annually - 3x industry average',
            'priority': 'critical',
            'kpi_value': turnover_rate,
            'kpi_trend': 'negative'
        })
    elif turnover_rate < 5:
        insights.append({
            'type': 'success',
            'title': 'Excellent Retention',
            'message': f'Superior retention at {turnover_rate:.1f}% - saving ~$2M annually vs industry average',
            'priority': 'medium',
            'kpi_value': turnover_rate,
            'kpi_trend': 'positive'
        })
    
    return insights

def generate_predictive_insights(insight_manager, employees_df, performance_df, engagement_df, turnover_df):
    """Generate predictive analytics insights."""
    insights = []
    
    # Turnover prediction insights
    if 'turnover_prediction' in insight_manager.ml_models:
        model = insight_manager.ml_models['turnover_prediction']
        accuracy = insight_manager.prediction_accuracy.get('turnover', 0)
        
        insights.append({
            'type': 'info',
            'title': 'Turnover Prediction Model',
            'message': f'AI model predicts turnover with {accuracy:.1%} accuracy - identifying high-risk employees proactively',
            'priority': 'high',
            'model_performance': accuracy,
            'prediction_type': 'turnover'
        })
        
        # Feature importance insights
        if 'turnover' in insight_manager.feature_importance:
            top_features = sorted(insight_manager.feature_importance['turnover'].items(), 
                                key=lambda x: x[1], reverse=True)[:3]
            
            feature_names = [f.replace('_', ' ').title() for f, _ in top_features]
            insights.append({
                'type': 'info',
                'title': 'Key Turnover Predictors',
                'message': f'Top predictors: {", ".join(feature_names)} - focus retention efforts here',
                'priority': 'medium',
                'features': top_features
            })
    
    # Performance prediction insights
    if 'performance_prediction' in insight_manager.ml_models:
        accuracy = insight_manager.prediction_accuracy.get('performance', 0)
        
        insights.append({
            'type': 'info',
            'title': 'Performance Prediction Model',
            'message': f'AI forecasts future performance with {accuracy:.1%} accuracy - enabling proactive development',
            'priority': 'high',
            'model_performance': accuracy,
            'prediction_type': 'performance'
        })
    
    # Risk scoring insights
    if not employees_df.empty:
        # Calculate composite risk scores
        risk_employees = []
        for _, emp in employees_df.iterrows():
            risk_score = 0
            
            # Performance risk
            if emp.get('performance_rating', 3.5) < 3.0:
                risk_score += 30
            
            # Tenure risk
            if emp.get('tenure_days', 365) < 365:
                risk_score += 20
                
            # Add to high-risk list if score > 40
            if risk_score > 40:
                risk_employees.append(emp['employee_id'])
        
        if len(risk_employees) > 0:
            insights.append({
                'type': 'warning',
                'title': 'High-Risk Employee Alert',
                'message': f'{len(risk_employees)} employees flagged as high-risk - immediate intervention required',
                'priority': 'critical',
                'risk_count': len(risk_employees),
                'action_required': True
            })
    
    return insights

def generate_segmentation_insights(insight_manager, employees_df, performance_df, engagement_df):
    """Generate employee segmentation insights."""
    insights = []
    
    if insight_manager.clustering_results:
        results = insight_manager.clustering_results
        n_clusters = results['n_clusters']
        silhouette = results['silhouette_score']
        
        insights.append({
            'type': 'info',
            'title': 'Employee Segmentation Analysis',
            'message': f'Identified {n_clusters} distinct employee segments (quality: {silhouette:.2f}) for targeted strategies',
            'priority': 'medium',
            'segments': n_clusters,
            'quality_score': silhouette
        })
        
        # Analyze cluster characteristics
        if not employees_df.empty:
            cluster_labels = results['labels']
            
            # Find dominant characteristics per cluster
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_size = np.sum(cluster_mask)
                cluster_pct = cluster_size / len(employees_df) * 100
                
                # Analyze cluster demographics
                cluster_employees = employees_df[cluster_mask]
                
                if len(cluster_employees) > 0:
                    # Dominant department
                    dept_mode = cluster_employees['department'].mode().iloc[0] if 'department' in cluster_employees.columns else 'Unknown'
                    
                    # Average performance
                    avg_perf = cluster_employees['performance_rating'].mean() if 'performance_rating' in cluster_employees.columns else 0
                    
                    insights.append({
                        'type': 'info',
                        'title': f'Segment {cluster_id + 1}: {dept_mode} Focus',
                        'message': f'{cluster_size} employees ({cluster_pct:.1f}%) - avg performance {avg_perf:.1f}/5.0',
                        'priority': 'low',
                        'cluster_id': cluster_id,
                        'size': cluster_size,
                        'characteristics': {'department': dept_mode, 'performance': avg_perf}
                    })
    
    return insights

def generate_correlation_insights(insight_manager, employees_df, performance_df, engagement_df, compensation_df):
    """Generate correlation analysis insights."""
    insights = []
    
    try:
        # Prepare correlation matrix
        if not employees_df.empty:
            # Collect metrics for correlation analysis
            metrics = {}
            
            # Performance metrics
            if not performance_df.empty:
                perf_by_emp = performance_df.groupby('employee_id')['performance_rating'].mean()
                metrics['performance'] = perf_by_emp
            
            # Engagement metrics
            if not engagement_df.empty:
                eng_by_emp = engagement_df.groupby('employee_id')['engagement_score'].mean()
                metrics['engagement'] = eng_by_emp
            
            # Compensation metrics
            if not compensation_df.empty:
                comp_by_emp = compensation_df.groupby('employee_id')['total_compensation'].mean()
                metrics['compensation'] = comp_by_emp
            
            # Tenure metrics
            if 'tenure_days' in employees_df.columns:
                tenure_by_emp = employees_df.set_index('employee_id')['tenure_days']
                metrics['tenure'] = tenure_by_emp
            
            # Calculate correlations
            if len(metrics) >= 2:
                correlation_matrix = pd.DataFrame(metrics).corr()
                
                # Find strong correlations
                strong_correlations = []
                for i in range(len(correlation_matrix.columns)):
                    for j in range(i+1, len(correlation_matrix.columns)):
                        corr_value = correlation_matrix.iloc[i, j]
                        if abs(corr_value) > 0.5:
                            strong_correlations.append({
                                'var1': correlation_matrix.columns[i],
                                'var2': correlation_matrix.columns[j],
                                'correlation': corr_value
                            })
                
                # Generate insights from correlations
                for corr in strong_correlations:
                    var1, var2, corr_val = corr['var1'], corr['var2'], corr['correlation']
                    
                    if corr_val > 0.7:
                        insights.append({
                            'type': 'success',
                            'title': f'Strong Positive Correlation: {var1.title()} ↔ {var2.title()}',
                            'message': f'Strong relationship (r={corr_val:.2f}) - improving {var1} likely increases {var2}',
                            'priority': 'medium',
                            'correlation_value': corr_val,
                            'variables': [var1, var2]
                        })
                    elif corr_val < -0.7:
                        insights.append({
                            'type': 'warning',
                            'title': f'Strong Negative Correlation: {var1.title()} ↔ {var2.title()}',
                            'message': f'Inverse relationship (r={corr_val:.2f}) - high {var1} associated with low {var2}',
                            'priority': 'medium',
                            'correlation_value': corr_val,
                            'variables': [var1, var2]
                        })
    
    except Exception as e:
        insights.append({
            'type': 'info',
            'title': 'Correlation Analysis',
            'message': 'Advanced correlation analysis requires more data points',
            'priority': 'low'
        })
    
    return insights

def generate_kpi_insights(insight_manager, employees_df, recruitment_df, performance_df, 
                        compensation_df, training_df, engagement_df, turnover_df, benefits_df):
    """Generate KPI dashboard insights."""
    kpis = {}
    
    # Calculate comprehensive KPIs
    total_employees = len(employees_df)
    
    # Performance KPIs
    if not performance_df.empty:
        kpis['avg_performance'] = {
            'value': performance_df['performance_rating'].mean(),
            'target': 4.0,
            'unit': '/5.0',
            'trend': 'stable',
            'category': 'Performance'
        }
        
        kpis['high_performers'] = {
            'value': len(performance_df[performance_df['performance_rating'] >= 4.5]),
            'target': total_employees * 0.2,  # 20% target
            'unit': 'employees',
            'trend': 'positive',
            'category': 'Performance'
        }
    
    # Engagement KPIs
    if not engagement_df.empty:
        kpis['avg_engagement'] = {
            'value': engagement_df['engagement_score'].mean(),
            'target': 4.0,
            'unit': '/5.0',
            'trend': 'stable',
            'category': 'Engagement'
        }
        
        kpis['highly_engaged'] = {
            'value': len(engagement_df[engagement_df['engagement_score'] >= 4.0]),
            'target': total_employees * 0.7,  # 70% target
            'unit': 'employees',
            'trend': 'positive',
            'category': 'Engagement'
        }
    
    # Retention KPIs
    if not turnover_df.empty:
        turnover_rate = len(turnover_df) / total_employees * 100 if total_employees > 0 else 0
        kpis['turnover_rate'] = {
            'value': turnover_rate,
            'target': 10.0,  # 10% target
            'unit': '%',
            'trend': 'negative' if turnover_rate > 15 else 'positive',
            'category': 'Retention'
        }
        
        kpis['retention_rate'] = {
            'value': 100 - turnover_rate,
            'target': 90.0,
            'unit': '%',
            'trend': 'positive' if turnover_rate < 10 else 'negative',
            'category': 'Retention'
        }
    
    # Training KPIs
    if not training_df.empty:
        avg_training_cost = training_df['training_cost'].mean()
        training_roi = training_df['performance_impact'].mean() * 100
        
        kpis['training_roi'] = {
            'value': training_roi,
            'target': 25.0,  # 25% ROI target
            'unit': '%',
            'trend': 'positive' if training_roi > 20 else 'stable',
            'category': 'Development'
        }
        
        kpis['avg_training_cost'] = {
            'value': avg_training_cost,
            'target': 3000,
            'unit': '$',
            'trend': 'negative' if avg_training_cost > 4000 else 'positive',
            'category': 'Development'
        }
    
    # Compensation KPIs
    if not compensation_df.empty:
        pay_equity = compensation_df['total_compensation'].std() / compensation_df['total_compensation'].mean()
        
        kpis['pay_equity_ratio'] = {
            'value': pay_equity,
            'target': 0.3,  # Lower is better
            'unit': 'ratio',
            'trend': 'positive' if pay_equity < 0.4 else 'negative',
            'category': 'Compensation'
        }
    
    return kpis

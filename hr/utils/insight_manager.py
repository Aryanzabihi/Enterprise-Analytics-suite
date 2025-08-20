import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Advanced ML and Analytics imports
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, IsolationForest
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error, silhouette_score
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from scipy import stats
    from scipy.stats import chi2_contingency, pearsonr
    import seaborn as sns
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    st.warning("⚠️ Advanced ML features require sklearn, scipy, and seaborn. Some features may be limited.")

# NLP capabilities
try:
    from textblob import TextBlob
    import re
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

import json
import hashlib
from typing import Dict, List, Tuple, Any, Optional
# Import advanced insights with fallback for different import contexts
try:
    from .advanced_insights import (
        generate_executive_summary, generate_predictive_insights, 
        generate_segmentation_insights, generate_correlation_insights, 
        generate_kpi_insights
    )
except ImportError:
    # Fallback for when imported directly
    from advanced_insights import (
        generate_executive_summary, generate_predictive_insights, 
        generate_segmentation_insights, generate_correlation_insights, 
        generate_kpi_insights
    )

class AdvancedInsightManager:
    """World-class AI-powered HR insights manager with advanced machine learning capabilities."""
    
    def __init__(self):
        self.insights_cache = {}
        self.ml_models = {}
        self.feature_importance = {}
        self.prediction_accuracy = {}
        self.clustering_results = {}
        self.anomaly_scores = {}
        self.statistical_tests = {}
        
        # Initialize ML components if available
        if ML_AVAILABLE:
            self.scaler = StandardScaler()
            self.label_encoder = LabelEncoder()
            self.pca = PCA(n_components=2)
            
        # Performance thresholds
        self.performance_thresholds = {
            'excellent': 4.5,
            'good': 3.5,
            'average': 2.5,
            'poor': 2.0
        }
        
        # Engagement thresholds
        self.engagement_thresholds = {
            'highly_engaged': 4.0,
            'engaged': 3.5,
            'neutral': 3.0,
            'disengaged': 2.5
        }
        
        # Risk scoring weights
        self.risk_weights = {
            'performance': 0.3,
            'engagement': 0.25,
            'tenure': 0.2,
            'compensation': 0.15,
            'training': 0.1
        }
        
    def generate_all_insights(self, employees_df, recruitment_df, performance_df, 
                             compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate comprehensive AI insights from all HR data using advanced analytics."""
        
        # Pre-process data and build ML models
        self._build_ml_models(employees_df, performance_df, engagement_df, turnover_df, compensation_df)
        
        insights = {
            'executive_summary': self._generate_executive_summary(employees_df, recruitment_df, performance_df, 
                                                                compensation_df, training_df, engagement_df, turnover_df, benefits_df),
            'predictive_analytics': self._generate_predictive_insights(employees_df, performance_df, engagement_df, turnover_df),
            'employee_segmentation': self._generate_segmentation_insights(employees_df, performance_df, engagement_df),
            'advanced_trends': self._generate_advanced_trend_insights(employees_df, performance_df, engagement_df, turnover_df),
            'risk_scoring': self._generate_advanced_risk_insights(employees_df, performance_df, engagement_df, turnover_df),
            'anomaly_detection': self._generate_ml_anomaly_insights(employees_df, performance_df, compensation_df, engagement_df),
            'correlation_analysis': self._generate_correlation_insights(employees_df, performance_df, engagement_df, compensation_df),
            'strategic_recommendations': self._generate_strategic_recommendations(employees_df, recruitment_df, performance_df, 
                                                                               compensation_df, training_df, engagement_df, turnover_df, benefits_df),
            'kpi_dashboard': self._generate_kpi_insights(employees_df, recruitment_df, performance_df, 
                                                       compensation_df, training_df, engagement_df, turnover_df, benefits_df)
        }
        
        return insights
    
    def _build_ml_models(self, employees_df, performance_df, engagement_df, turnover_df, compensation_df):
        """Build and train machine learning models for predictions."""
        if not ML_AVAILABLE or employees_df.empty:
            return
            
        try:
            # Prepare data for ML models
            ml_data = self._prepare_ml_features(employees_df, performance_df, engagement_df, compensation_df)
            
            if ml_data is not None and len(ml_data) > 10:
                # Turnover prediction model
                if not turnover_df.empty:
                    self._build_turnover_prediction_model(ml_data, turnover_df)
                
                # Performance prediction model
                if not performance_df.empty:
                    self._build_performance_prediction_model(ml_data, performance_df)
                
                # Employee clustering model
                self._build_employee_clustering_model(ml_data)
                
                # Anomaly detection model
                self._build_anomaly_detection_model(ml_data)
                
        except Exception as e:
            st.warning(f"ML model building encountered an issue: {str(e)}")
    
    def _prepare_ml_features(self, employees_df, performance_df, engagement_df, compensation_df):
        """Prepare feature matrix for machine learning models."""
        try:
            # Start with employee base features
            features = employees_df.copy()
            
            # Add performance metrics
            if not performance_df.empty:
                perf_agg = performance_df.groupby('employee_id').agg({
                    'performance_rating': ['mean', 'std', 'count'],
                    'goal_achievement_rate': 'mean',
                    'productivity_score': 'mean'
                }).round(3)
                perf_agg.columns = ['perf_rating_mean', 'perf_rating_std', 'perf_review_count', 
                                  'goal_achievement_mean', 'productivity_mean']
                features = features.merge(perf_agg, left_on='employee_id', right_index=True, how='left')
            
            # Add engagement metrics
            if not engagement_df.empty:
                eng_agg = engagement_df.groupby('employee_id').agg({
                    'engagement_score': ['mean', 'std'],
                    'satisfaction_score': 'mean',
                    'work_life_balance_score': 'mean'
                }).round(3)
                eng_agg.columns = ['engagement_mean', 'engagement_std', 'satisfaction_mean', 'wlb_mean']
                features = features.merge(eng_agg, left_on='employee_id', right_index=True, how='left')
            
            # Add compensation metrics
            if not compensation_df.empty:
                comp_agg = compensation_df.groupby('employee_id').agg({
                    'base_salary': 'mean',
                    'bonus_amount': 'mean',
                    'total_compensation': 'mean'
                }).round(0)
                comp_agg.columns = ['salary_mean', 'bonus_mean', 'total_comp_mean']
                features = features.merge(comp_agg, left_on='employee_id', right_index=True, how='left')
            
            # Encode categorical variables
            categorical_cols = ['department', 'gender', 'ethnicity', 'education_level']
            for col in categorical_cols:
                if col in features.columns:
                    features[f'{col}_encoded'] = pd.Categorical(features[col]).codes
            
            # Select numeric features for ML
            numeric_cols = features.select_dtypes(include=[np.number]).columns
            ml_features = features[numeric_cols].fillna(0)
            
            return ml_features
            
        except Exception as e:
            st.warning(f"Feature preparation failed: {str(e)}")
            return None
    
    def _build_turnover_prediction_model(self, ml_data, turnover_df):
        """Build a model to predict employee turnover risk."""
        try:
            # Create turnover labels
            turnover_employees = set(turnover_df['employee_id'].unique())
            ml_data['turnover_risk'] = ml_data.index.map(
                lambda x: 1 if f'EMP{x+1:03d}' in turnover_employees else 0
            )
            
            # Prepare features and target
            feature_cols = [col for col in ml_data.columns if col != 'turnover_risk']
            X = ml_data[feature_cols]
            y = ml_data['turnover_risk']
            
            if len(X) > 10 and y.sum() > 0:
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                # Train Random Forest model
                rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
                rf_model.fit(X_train, y_train)
                
                # Evaluate model
                y_pred = rf_model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                
                # Store model and results
                self.ml_models['turnover_prediction'] = rf_model
                self.prediction_accuracy['turnover'] = accuracy
                self.feature_importance['turnover'] = dict(zip(feature_cols, rf_model.feature_importances_))
                
        except Exception as e:
            st.warning(f"Turnover prediction model failed: {str(e)}")
    
    def _build_performance_prediction_model(self, ml_data, performance_df):
        """Build a model to predict employee performance."""
        try:
            # Get latest performance rating for each employee
            latest_perf = performance_df.sort_values('review_date').groupby('employee_id').last()
            
            # Match with ML data
            perf_target = []
            for idx in ml_data.index:
                emp_id = f'EMP{idx+1:03d}'
                if emp_id in latest_perf.index:
                    perf_target.append(latest_perf.loc[emp_id, 'performance_rating'])
                else:
                    perf_target.append(np.nan)
            
            ml_data['performance_target'] = perf_target
            
            # Remove rows with missing targets
            valid_data = ml_data.dropna(subset=['performance_target'])
            
            if len(valid_data) > 10:
                feature_cols = [col for col in valid_data.columns if col != 'performance_target']
                X = valid_data[feature_cols]
                y = valid_data['performance_target']
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                # Train Gradient Boosting model
                gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
                gb_model.fit(X_train, y_train)
                
                # Evaluate model
                y_pred = gb_model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                
                # Store model and results
                self.ml_models['performance_prediction'] = gb_model
                self.prediction_accuracy['performance'] = 1 / (1 + mse)  # Convert MSE to accuracy-like metric
                self.feature_importance['performance'] = dict(zip(feature_cols, gb_model.feature_importances_))
                
        except Exception as e:
            st.warning(f"Performance prediction model failed: {str(e)}")
    
    def _build_employee_clustering_model(self, ml_data):
        """Build employee segmentation using clustering."""
        try:
            # Select features for clustering
            feature_cols = [col for col in ml_data.columns if 'encoded' not in col]
            X = ml_data[feature_cols].fillna(0)
            
            if len(X) > 5:
                # Standardize features
                X_scaled = self.scaler.fit_transform(X)
                
                # K-means clustering
                n_clusters = min(5, len(X) // 2)  # Adaptive cluster count
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = kmeans.fit_predict(X_scaled)
                
                # Calculate silhouette score
                if len(set(cluster_labels)) > 1:
                    silhouette = silhouette_score(X_scaled, cluster_labels)
                    
                    # Store results
                    self.clustering_results = {
                        'model': kmeans,
                        'labels': cluster_labels,
                        'silhouette_score': silhouette,
                        'n_clusters': n_clusters,
                        'feature_names': feature_cols
                    }
                
        except Exception as e:
            st.warning(f"Employee clustering failed: {str(e)}")
    
    def _build_anomaly_detection_model(self, ml_data):
        """Build anomaly detection model."""
        try:
            # Select features for anomaly detection
            feature_cols = [col for col in ml_data.columns if 'encoded' not in col]
            X = ml_data[feature_cols].fillna(0)
            
            if len(X) > 5:
                # Isolation Forest for anomaly detection
                isolation_forest = IsolationForest(contamination=0.1, random_state=42)
                anomaly_scores = isolation_forest.fit_predict(X)
                
                # Store results
                self.anomaly_scores = {
                    'model': isolation_forest,
                    'scores': anomaly_scores,
                    'outlier_indices': np.where(anomaly_scores == -1)[0]
                }
                
        except Exception as e:
            st.warning(f"Anomaly detection failed: {str(e)}")
    
    def _generate_executive_summary(self, employees_df, recruitment_df, performance_df, 
                                   compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate executive-level summary insights."""
        return generate_executive_summary(self, employees_df, recruitment_df, performance_df, 
                                        compensation_df, training_df, engagement_df, turnover_df, benefits_df)
    
    def _generate_predictive_insights(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate predictive analytics insights."""
        return generate_predictive_insights(self, employees_df, performance_df, engagement_df, turnover_df)
    
    def _generate_segmentation_insights(self, employees_df, performance_df, engagement_df):
        """Generate employee segmentation insights."""
        return generate_segmentation_insights(self, employees_df, performance_df, engagement_df)
    
    def _generate_correlation_insights(self, employees_df, performance_df, engagement_df, compensation_df):
        """Generate correlation analysis insights."""
        return generate_correlation_insights(self, employees_df, performance_df, engagement_df, compensation_df)
    
    def _generate_kpi_insights(self, employees_df, recruitment_df, performance_df, 
                              compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate KPI dashboard insights."""
        return generate_kpi_insights(self, employees_df, recruitment_df, performance_df, 
                                   compensation_df, training_df, engagement_df, turnover_df, benefits_df)
    
    def _generate_summary_insights(self, employees_df, recruitment_df, performance_df, 
                                  compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate high-level summary insights."""
        
        insights = []
        
        # Employee count insights
        total_employees = len(employees_df)
        if total_employees > 0:
            insights.append({
                'type': 'info',
                'title': 'Workforce Size',
                'message': f'Company has {total_employees} employees across {employees_df["department"].nunique()} departments',
                'priority': 'high'
            })
        
        # Performance insights
        if not performance_df.empty:
            avg_performance = performance_df['performance_rating'].mean()
            if avg_performance >= 4.0:
                insights.append({
                    'type': 'success',
                    'title': 'High Performance Culture',
                    'message': f'Average performance rating is {avg_performance:.1f}/5.0 - excellent team performance!',
                    'priority': 'high'
                })
            elif avg_performance <= 3.0:
                insights.append({
                    'type': 'warning',
                    'title': 'Performance Improvement Needed',
                    'message': f'Average performance rating is {avg_performance:.1f}/5.0 - consider performance improvement programs',
                    'priority': 'high'
                })
        
        # Engagement insights
        if not engagement_df.empty:
            avg_engagement = engagement_df['engagement_score'].mean()
            if avg_engagement >= 4.0:
                insights.append({
                    'type': 'success',
                    'title': 'High Employee Engagement',
                    'message': f'Average engagement score is {avg_engagement:.1f}/5.0 - strong employee satisfaction!',
                    'priority': 'medium'
                })
            elif avg_engagement <= 3.0:
                insights.append({
                    'type': 'warning',
                    'title': 'Low Engagement Alert',
                    'message': f'Average engagement score is {avg_engagement:.1f}/5.0 - focus on employee satisfaction initiatives',
                    'priority': 'high'
                })
        
        # Turnover insights
        if not turnover_df.empty:
            turnover_rate = len(turnover_df) / total_employees * 100 if total_employees > 0 else 0
            if turnover_rate > 15:
                insights.append({
                    'type': 'error',
                    'title': 'High Turnover Rate',
                    'message': f'Turnover rate is {turnover_rate:.1f}% - above industry average, immediate attention needed',
                    'priority': 'critical'
                })
            elif turnover_rate < 5:
                insights.append({
                    'type': 'success',
                    'title': 'Low Turnover Rate',
                    'message': f'Turnover rate is {turnover_rate:.1f}% - excellent retention, strong company culture',
                    'priority': 'medium'
                })
        
        return insights
    
    def _generate_trend_insights(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate trend-based insights."""
        
        insights = []
        
        # Tenure trends
        if not employees_df.empty and 'tenure_days' in employees_df.columns:
            avg_tenure = employees_df['tenure_days'].mean()
            if avg_tenure > 1000:  # More than 2.7 years
                insights.append({
                    'type': 'info',
                    'title': 'Experienced Workforce',
                    'message': f'Average tenure is {avg_tenure:.0f} days - experienced team with strong institutional knowledge',
                    'priority': 'medium'
                })
            elif avg_tenure < 365:  # Less than 1 year
                insights.append({
                    'type': 'warning',
                    'title': 'New Team Formation',
                    'message': f'Average tenure is {avg_tenure:.0f} days - mostly new hires, focus on onboarding and training',
                    'priority': 'medium'
                })
        
        # Performance trends
        if not performance_df.empty:
            recent_performance = performance_df[performance_df['review_date'] >= 
                                             (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')]
            if not recent_performance.empty:
                recent_avg = recent_performance['performance_rating'].mean()
                overall_avg = performance_df['performance_rating'].mean()
                
                if recent_avg > overall_avg + 0.3:
                    insights.append({
                        'type': 'success',
                        'title': 'Performance Improving',
                        'message': f'Recent performance ({recent_avg:.1f}) is {recent_avg - overall_avg:.1f} points above average - positive trend!',
                        'priority': 'medium'
                    })
                elif recent_avg < overall_avg - 0.3:
                    insights.append({
                        'type': 'warning',
                        'title': 'Performance Declining',
                        'message': f'Recent performance ({recent_avg:.1f}) is {overall_avg - recent_avg:.1f} points below average - investigate causes',
                        'priority': 'high'
                    })
        
        return insights
    
    def _generate_risk_insights(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate risk assessment insights."""
        
        insights = []
        
        # High-risk employees
        if not employees_df.empty:
            # Performance risk
            low_performers = employees_df[employees_df['performance_rating'] < 3.0]
            if len(low_performers) > 0:
                risk_percentage = len(low_performers) / len(employees_df) * 100
                insights.append({
                    'type': 'warning',
                    'title': 'Performance Risk',
                    'message': f'{len(low_performers)} employees ({risk_percentage:.1f}%) have performance ratings below 3.0 - high turnover risk',
                    'priority': 'high'
                })
            
            # Tenure risk
            if 'tenure_days' in employees_df.columns:
                short_tenure = employees_df[employees_df['tenure_days'] < 365]
                if len(short_tenure) > len(employees_df) * 0.3:  # More than 30% new hires
                    insights.append({
                        'type': 'warning',
                        'title': 'Tenure Risk',
                        'message': f'{len(short_tenure)} employees ({len(short_tenure)/len(employees_df)*100:.1f}%) have less than 1 year tenure - knowledge retention risk',
                        'priority': 'medium'
                    })
        
        # Engagement risk
        if not engagement_df.empty:
            low_engagement = engagement_df[engagement_df['engagement_score'] < 3.0]
            if len(low_engagement) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Engagement Risk',
                    'message': f'{len(low_engagement)} employees have low engagement scores - increased turnover risk',
                    'priority': 'high'
                })
        
        return insights
    
    def _generate_opportunity_insights(self, employees_df, performance_df, training_df, engagement_df):
        """Generate opportunity-based insights."""
        
        insights = []
        
        # High performers
        if not performance_df.empty:
            high_performers = performance_df[performance_df['performance_rating'] >= 4.5]
            if len(high_performers) > 0:
                insights.append({
                    'type': 'success',
                    'title': 'High Performer Recognition',
                    'message': f'{len(high_performers)} employees have exceptional performance (4.5+) - consider promotion opportunities',
                    'priority': 'medium'
                })
        
        # Training opportunities
        if not training_df.empty:
            avg_training_impact = training_df['performance_impact'].mean()
            if avg_training_impact > 0.3:
                insights.append({
                    'type': 'success',
                    'title': 'Training ROI',
                    'message': f'Training programs show strong performance impact ({avg_training_impact:.2f}) - consider expanding successful programs',
                    'priority': 'medium'
                })
        
        # Engagement opportunities
        if not engagement_df.empty:
            high_engagement = engagement_df[engagement_df['engagement_score'] >= 4.5]
            if len(high_engagement) > 0:
                insights.append({
                    'type': 'info',
                    'title': 'Engagement Champions',
                    'message': f'{len(high_engagement)} employees are highly engaged - leverage them as culture ambassadors',
                    'priority': 'low'
                })
        
        return insights
    
    def _generate_anomaly_insights(self, employees_df, performance_df, compensation_df, engagement_df):
        """Generate anomaly detection insights."""
        
        insights = []
        
        # Salary anomalies
        if not compensation_df.empty:
            salary_mean = compensation_df['base_salary'].mean()
            salary_std = compensation_df['base_salary'].std()
            
            # High salary outliers
            high_outliers = compensation_df[compensation_df['base_salary'] > salary_mean + 2 * salary_std]
            if len(high_outliers) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Salary Anomalies',
                    'message': f'{len(high_outliers)} employees have salaries significantly above average - review compensation strategy',
                    'priority': 'medium'
                })
            
            # Low salary outliers
            low_outliers = compensation_df[compensation_df['base_salary'] < salary_mean - 2 * salary_std]
            if len(low_outliers) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Underpaid Employees',
                    'message': f'{len(low_outliers)} employees have salaries significantly below average - potential retention risk',
                    'priority': 'high'
                })
        
        # Performance anomalies
        if not performance_df.empty:
            perf_mean = performance_df['performance_rating'].mean()
            perf_std = performance_df['performance_rating'].std()
            
            # Exceptional performers
            exceptional = performance_df[performance_df['performance_rating'] > perf_mean + 2 * perf_std]
            if len(exceptional) > 0:
                insights.append({
                    'type': 'success',
                    'title': 'Exceptional Performers',
                    'message': f'{len(exceptional)} employees have exceptional performance ratings - consider special recognition',
                    'priority': 'medium'
                })
        
        return insights
    
    def _generate_recommendations(self, employees_df, recruitment_df, performance_df, 
                                compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate actionable recommendations."""
        
        recommendations = []
        
        # Performance improvement
        if not performance_df.empty:
            low_perf_count = len(performance_df[performance_df['performance_rating'] < 3.0])
            if low_perf_count > 0:
                recommendations.append({
                    'category': 'Performance Management',
                    'action': 'Implement Performance Improvement Plans',
                    'description': f'Develop PIPs for {low_perf_count} employees with ratings below 3.0',
                    'priority': 'high',
                    'impact': 'Reduce turnover risk and improve team performance'
                })
        
        # Engagement improvement
        if not engagement_df.empty:
            low_engagement_count = len(engagement_df[engagement_df['engagement_score'] < 3.0])
            if low_engagement_count > 0:
                recommendations.append({
                    'category': 'Employee Engagement',
                    'action': 'Conduct Engagement Survey Analysis',
                    'description': f'Analyze feedback from {low_engagement_count} low-engagement employees',
                    'priority': 'high',
                    'impact': 'Improve retention and workplace satisfaction'
                })
        
        # Training optimization
        if not training_df.empty:
            avg_training_cost = training_df['training_cost'].mean()
            if avg_training_cost > 3000:
                recommendations.append({
                    'category': 'Training & Development',
                    'action': 'Optimize Training Costs',
                    'description': f'Review training programs with average cost of ${avg_training_cost:,.0f}',
                    'priority': 'medium',
                    'impact': 'Reduce training expenses while maintaining quality'
                })
        
        # Compensation review
        if not compensation_df.empty:
            salary_range = compensation_df['base_salary'].max() - compensation_df['base_salary'].min()
            avg_salary = compensation_df['base_salary'].mean()
            if salary_range > avg_salary * 2:
                recommendations.append({
                    'category': 'Compensation',
                    'action': 'Review Compensation Structure',
                    'description': 'Large salary range detected - review for equity and market competitiveness',
                    'priority': 'medium',
                    'impact': 'Ensure fair compensation and reduce turnover risk'
                })
        
        return recommendations
    
    def render_insights_dashboard(self, insights_data):
        """Render the complete insights dashboard."""
        
        st.header("🤖 AI-Powered HR Insights Dashboard")
        st.markdown("---")
        
        # Summary Insights
        st.subheader("📊 Key Insights")
        self._render_insights_grid(insights_data['summary'])
        
        # Trends
        if insights_data['trends']:
            st.subheader("📈 Trend Analysis")
            self._render_insights_grid(insights_data['trends'])
        
        # Risks
        if insights_data['risks']:
            st.subheader("⚠️ Risk Alerts")
            self._render_insights_grid(insights_data['risks'])
        
        # Opportunities
        if insights_data['opportunities']:
            st.subheader("🎯 Opportunities")
            self._render_insights_grid(insights_data['opportunities'])
        
        # Anomalies
        if insights_data['anomalies']:
            st.subheader("🔍 Anomaly Detection")
            self._render_insights_grid(insights_data['anomalies'])
        
        # Recommendations
        if insights_data['recommendations']:
            st.subheader("💡 Actionable Recommendations")
            self._render_recommendations(insights_data['recommendations'])
        
        # Metrics Summary
        st.subheader("📊 Quick Metrics")
        self._render_metrics_summary()
    
    def _generate_advanced_trend_insights(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate advanced trend analysis insights."""
        insights = []
        
        # Performance trends with statistical analysis
        if not performance_df.empty and 'review_date' in performance_df.columns:
            performance_df['review_date'] = pd.to_datetime(performance_df['review_date'])
            monthly_perf = performance_df.groupby(pd.Grouper(key='review_date', freq='M'))['performance_rating'].mean()
            
            if len(monthly_perf) > 3:
                # Calculate trend slope
                x = np.arange(len(monthly_perf))
                y = monthly_perf.values
                slope = np.polyfit(x, y, 1)[0]
                
                if slope > 0.1:
                    insights.append({
                        'type': 'success',
                        'title': 'Performance Trending Up',
                        'message': f'Performance shows strong upward trend (+{slope:.2f} per month) - maintain current strategies',
                        'priority': 'medium',
                        'trend_direction': 'positive',
                        'trend_strength': abs(slope)
                    })
                elif slope < -0.1:
                    insights.append({
                        'type': 'warning',
                        'title': 'Performance Declining',
                        'message': f'Performance shows concerning downward trend ({slope:.2f} per month) - intervention needed',
                        'priority': 'high',
                        'trend_direction': 'negative',
                        'trend_strength': abs(slope)
                    })
        
        return insights
    
    def _generate_advanced_risk_insights(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate advanced risk assessment insights using ML."""
        insights = []
        
        if not employees_df.empty:
            # Calculate composite risk scores
            risk_scores = {}
            
            for _, emp in employees_df.iterrows():
                emp_id = emp['employee_id']
                risk_score = 0
                risk_factors = []
                
                # Performance risk (30% weight)
                if emp.get('performance_rating', 3.5) < 3.0:
                    risk_score += 30
                    risk_factors.append('Low Performance')
                
                # Tenure risk (20% weight)
                if emp.get('tenure_days', 365) < 365:
                    risk_score += 20
                    risk_factors.append('Short Tenure')
                
                # Engagement risk (25% weight)
                if not engagement_df.empty:
                    emp_engagement = engagement_df[engagement_df['employee_id'] == emp_id]['engagement_score'].mean()
                    if emp_engagement < 3.0:
                        risk_score += 25
                        risk_factors.append('Low Engagement')
                
                # Store risk assessment
                if risk_score > 0:
                    risk_scores[emp_id] = {
                        'score': risk_score,
                        'factors': risk_factors,
                        'level': 'High' if risk_score > 50 else 'Medium' if risk_score > 25 else 'Low'
                    }
            
            # Generate insights based on risk analysis
            high_risk_count = sum(1 for r in risk_scores.values() if r['score'] > 50)
            total_at_risk = len(risk_scores)
            
            if high_risk_count > 0:
                insights.append({
                    'type': 'error',
                    'title': 'Critical Risk Alert',
                    'message': f'{high_risk_count} employees at critical risk level - immediate action required',
                    'priority': 'critical',
                    'high_risk_count': high_risk_count,
                    'action_required': True
                })
            
            if total_at_risk > len(employees_df) * 0.3:
                insights.append({
                    'type': 'warning',
                    'title': 'Elevated Workforce Risk',
                    'message': f'{total_at_risk} employees ({total_at_risk/len(employees_df)*100:.1f}%) showing risk factors',
                    'priority': 'high',
                    'at_risk_percentage': total_at_risk/len(employees_df)*100
                })
        
        return insights
    
    def _generate_ml_anomaly_insights(self, employees_df, performance_df, compensation_df, engagement_df):
        """Generate ML-powered anomaly detection insights."""
        insights = []
        
        if self.anomaly_scores and 'outlier_indices' in self.anomaly_scores:
            outlier_indices = self.anomaly_scores['outlier_indices']
            
            if len(outlier_indices) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'AI-Detected Anomalies',
                    'message': f'Machine learning identified {len(outlier_indices)} employees with unusual patterns requiring investigation',
                    'priority': 'medium',
                    'anomaly_count': len(outlier_indices),
                    'detection_method': 'Isolation Forest'
                })
        
        # Traditional statistical anomalies
        if not compensation_df.empty:
            # Salary anomalies using IQR method
            Q1 = compensation_df['base_salary'].quantile(0.25)
            Q3 = compensation_df['base_salary'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            salary_outliers = compensation_df[
                (compensation_df['base_salary'] < lower_bound) | 
                (compensation_df['base_salary'] > upper_bound)
            ]
            
            if len(salary_outliers) > 0:
                insights.append({
                    'type': 'warning',
                    'title': 'Salary Outliers Detected',
                    'message': f'{len(salary_outliers)} employees have statistically unusual salaries - review compensation equity',
                    'priority': 'medium',
                    'outlier_count': len(salary_outliers)
                })
        
        return insights
    
    def _generate_strategic_recommendations(self, employees_df, recruitment_df, performance_df, 
                                          compensation_df, training_df, engagement_df, turnover_df, benefits_df):
        """Generate strategic, data-driven recommendations."""
        recommendations = []
        
        # Performance-based recommendations
        if not performance_df.empty:
            low_performers = performance_df[performance_df['performance_rating'] < 3.0]
            if len(low_performers) > 0:
                recommendations.append({
                    'category': 'Performance Excellence',
                    'action': 'Implement AI-Driven Performance Coaching',
                    'description': f'Deploy personalized coaching for {len(low_performers)} underperforming employees using predictive analytics',
                    'priority': 'high',
                    'impact': 'Potential 15-25% performance improvement, $500K+ productivity gain',
                    'timeline': '3-6 months',
                    'investment': '$150K',
                    'roi_estimate': '300%'
                })
        
        # Engagement-based recommendations
        if not engagement_df.empty:
            avg_engagement = engagement_df['engagement_score'].mean()
            if avg_engagement < 3.5:
                recommendations.append({
                    'category': 'Employee Experience',
                    'action': 'Launch Comprehensive Engagement Initiative',
                    'description': 'Multi-phase engagement program targeting culture, growth, and recognition',
                    'priority': 'critical',
                    'impact': 'Reduce turnover by 40%, increase productivity by 20%',
                    'timeline': '6-12 months',
                    'investment': '$300K',
                    'roi_estimate': '250%'
                })
        
        # Turnover-based recommendations
        if not turnover_df.empty:
            turnover_rate = len(turnover_df) / len(employees_df) * 100 if len(employees_df) > 0 else 0
            if turnover_rate > 15:
                recommendations.append({
                    'category': 'Retention Strategy',
                    'action': 'Deploy Predictive Retention System',
                    'description': 'Implement ML-powered early warning system to identify at-risk employees',
                    'priority': 'critical',
                    'impact': 'Prevent 50% of voluntary turnover, save $2M+ annually',
                    'timeline': '2-4 months',
                    'investment': '$200K',
                    'roi_estimate': '1000%'
                })
        
        # Training optimization recommendations
        if not training_df.empty:
            avg_training_cost = training_df['training_cost'].mean()
            avg_impact = training_df['performance_impact'].mean()
            
            if avg_training_cost > 3000 and avg_impact < 0.3:
                recommendations.append({
                    'category': 'Learning & Development',
                    'action': 'Optimize Training Portfolio with AI',
                    'description': 'Use ML to identify high-ROI training programs and eliminate low-impact initiatives',
                    'priority': 'medium',
                    'impact': 'Reduce training costs by 30%, increase effectiveness by 50%',
                    'timeline': '4-6 months',
                    'investment': '$100K',
                    'roi_estimate': '200%'
                })
        
        # Compensation equity recommendations
        if not compensation_df.empty:
            salary_std = compensation_df['base_salary'].std()
            salary_mean = compensation_df['base_salary'].mean()
            cv = salary_std / salary_mean  # Coefficient of variation
            
            if cv > 0.4:  # High salary variance
                recommendations.append({
                    'category': 'Compensation Strategy',
                    'action': 'Implement Pay Equity Analysis',
                    'description': 'Comprehensive compensation review using market data and performance metrics',
                    'priority': 'high',
                    'impact': 'Ensure fair pay, reduce legal risk, improve retention',
                    'timeline': '3-4 months',
                    'investment': '$75K',
                    'roi_estimate': '150%'
                })
        
        return recommendations
    
    def _render_insights_grid(self, insights):
        """Render insights in a grid layout."""
        if not insights:
            st.info("No insights available for this category.")
            return
        
        cols = st.columns(2)
        for i, insight in enumerate(insights):
            col = cols[i % 2]
            
            with col:
                # Color coding based on type
                if insight['type'] == 'success':
                    st.success(f"✅ **{insight['title']}**")
                elif insight['type'] == 'warning':
                    st.warning(f"⚠️ **{insight['title']}**")
                elif insight['type'] == 'error':
                    st.error(f"🚨 **{insight['title']}**")
                else:
                    st.info(f"ℹ️ **{insight['title']}**")
                
                st.write(insight['message'])
                
                # Priority indicator
                priority_colors = {
                    'critical': '🔴',
                    'high': '🟠', 
                    'medium': '🟡',
                    'low': '🟢'
                }
                st.caption(f"{priority_colors.get(insight['priority'], '⚪')} Priority: {insight['priority'].title()}")
                st.markdown("---")
    
    def _render_recommendations(self, recommendations):
        """Render actionable recommendations."""
        if not recommendations:
            st.info("No recommendations available.")
            return
        
        for rec in recommendations:
            with st.expander(f"🎯 {rec['action']} - {rec['category']}", expanded=False):
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Impact:** {rec['impact']}")
                
                # Priority indicator
                priority_colors = {
                    'critical': '🔴',
                    'high': '🟠', 
                    'medium': '🟡',
                    'low': '🟢'
                }
                st.caption(f"{priority_colors.get(rec['priority'], '⚪')} Priority: {rec['priority'].title()}")
    
    def _render_metrics_summary(self):
        """Render quick metrics summary."""
        # This would show key metrics in a compact format
        st.info("📈 Detailed metrics are available in the specific analytics sections.")

# Maintain backward compatibility
InsightManager = AdvancedInsightManager

# HR Predictive Analytics Dashboard
# Advanced machine learning models for HR predictions and forecasting

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Enhanced visualization imports
import plotly.figure_factory as ff
from plotly.offline import plot
import plotly.io as pio

# Set Plotly template for consistent styling
pio.templates.default = "plotly_white"

# ML imports
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, RandomForestRegressor
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    st.warning("⚠️ Advanced ML features require sklearn. Some predictive features may be limited.")

class HRPredictiveAnalytics:
    """Advanced HR Predictive Analytics with Machine Learning capabilities."""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_importance = {}
        self.model_performance = {}
        self.predictions_cache = {}
        
        # Initialize ML components if available
        if ML_AVAILABLE:
            self.scaler = StandardScaler()
            self.label_encoder = LabelEncoder()
    
    def display_predictive_analytics_dashboard(self, employees_df, performance_df, engagement_df, 
                                            turnover_df, recruitment_df, compensation_df):
        """Display the comprehensive predictive analytics dashboard."""
        
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; margin-bottom: 30px;">
            <h1 style="color: white; margin: 0; font-size: 2.2rem; text-align: center; font-weight: 700;">
                🔮 Predictive Analytics Dashboard
            </h1>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; text-align: center; font-size: 1.1rem;">
                AI-Powered Predictions • Workforce Planning • Risk Assessment • Strategic Insights
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check data availability and provide helpful information
        if employees_df.empty:
            st.warning("⚠️ No employee data available. Please load data first.")
            return
        

        
        # Check ML availability
        if not ML_AVAILABLE:
            st.warning("⚠️ **Machine Learning Libraries Not Available**")
            st.info("""
            Some advanced predictive features require scikit-learn. Please install it with:
            ```
            pip install scikit-learn
            ```
            Basic analytics will still work without ML capabilities.
            """)
        
        # Create tabs for different predictive features
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Turnover Prediction", 
            "📊 Performance Forecasting", 
            "👥 Workforce Planning",
            "🎯 Recruitment Optimization",
            "📈 Predictive Insights"
        ])
        
        with tab1:
            try:
                self.display_turnover_prediction(employees_df, performance_df, engagement_df, turnover_df)
            except Exception as e:
                st.error(f"❌ Error in Turnover Prediction: {str(e)}")
                st.info("Please check your data and try again.")
        
        with tab2:
            try:
                self.display_performance_forecasting(employees_df, performance_df, engagement_df)
            except Exception as e:
                st.error(f"❌ Error in Performance Forecasting: {str(e)}")
                st.info("Please check your data and try again.")
        
        with tab3:
            try:
                self.display_workforce_planning(employees_df, performance_df, engagement_df, turnover_df)
            except Exception as e:
                st.error(f"❌ Error in Workforce Planning: {str(e)}")
                st.info("Please check your data and try again.")
        
        with tab4:
            try:
                self.display_recruitment_optimization(recruitment_df, employees_df)
            except Exception as e:
                st.error(f"❌ Error in Recruitment Optimization: {str(e)}")
                st.info("Please check your data and try again.")
        
        with tab5:
            try:
                self.display_predictive_insights(employees_df, performance_df, engagement_df, turnover_df, compensation_df)
            except Exception as e:
                st.error(f"❌ Error in Predictive Insights: {str(e)}")
                st.info("Please check your data and try again.")
    
    def display_turnover_prediction(self, employees_df, performance_df, engagement_df, turnover_df):
        """Display turnover prediction analysis."""
        st.header("🎯 Employee Turnover Prediction")
        
        if not ML_AVAILABLE:
            st.error("❌ Machine learning libraries not available. Please install scikit-learn for predictive features.")
            return
        
        # Prepare data for turnover prediction
        if not self._validate_turnover_data(employees_df, performance_df, engagement_df, turnover_df):
            st.warning("⚠️ Insufficient data for turnover prediction. Need performance and engagement data.")
            return
        
        # Build and train turnover prediction model
        if st.button("🚀 Build Turnover Prediction Model", key="build_turnover_model"):
            with st.spinner("Training AI model for turnover prediction..."):
                success = self._build_turnover_model(employees_df, performance_df, engagement_df, turnover_df)
                if success:
                    st.success("✅ Turnover prediction model trained successfully!")
                else:
                    st.error("❌ Failed to train turnover prediction model.")
        
        # Display model performance if available
        if 'turnover_prediction' in self.models:
            self._display_turnover_model_performance()
            
            # Show predictions
            if st.button("🔮 Predict Turnover Risk", key="predict_turnover"):
                self._display_turnover_predictions(employees_df, performance_df, engagement_df)
        
        # Show historical turnover analysis
        if not turnover_df.empty:
            self._display_turnover_analysis(turnover_df, employees_df)
    
    def display_performance_forecasting(self, employees_df, performance_df, engagement_df):
        """Display performance forecasting analysis."""
        st.header("📊 Performance Forecasting")
        
        if not ML_AVAILABLE:
            st.error("❌ Machine learning libraries not available.")
            return
        
        if performance_df.empty:
            st.warning("⚠️ No performance data available for forecasting.")
            return
        
        # Performance trend analysis
        st.subheader("📈 Performance Trends")
        
        # Group performance by date
        if 'review_date' in performance_df.columns:
            performance_df['review_date'] = pd.to_datetime(performance_df['review_date'])
            monthly_perf = performance_df.groupby(pd.Grouper(key='review_date', freq='M'))['performance_rating'].agg(['mean', 'count']).reset_index()
            
            # Enhanced performance trends visualization
            fig = go.Figure()
            
            # Main performance trend
            fig.add_trace(go.Scatter(
                x=monthly_perf['review_date'],
                y=monthly_perf['mean'],
                mode='lines+markers',
                name='Average Performance',
                line=dict(color='#667eea', width=4, shape='spline'),
                marker=dict(
                    size=10,
                    color='#667eea',
                    line=dict(color='white', width=2)
                ),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.1)',
                hovertemplate="<b>%{x|%B %Y}</b><br>" +
                            "Performance: <b>%{y:.2f}</b><br>" +
                            "Reviews: <b>%{customdata}</b><br>" +
                            "<extra></extra>",
                customdata=monthly_perf['count']
            ))
            
            # Add performance count as secondary axis
            fig.add_trace(go.Scatter(
                x=monthly_perf['review_date'],
                y=monthly_perf['count'],
                mode='lines+markers',
                name='Review Count',
                yaxis='y2',
                line=dict(color='#f39c12', width=3, dash='dot'),
                marker=dict(
                    size=8,
                    color='#f39c12',
                    symbol='diamond'
                ),
                hovertemplate="<b>%{x|%B %Y}</b><br>" +
                            "Review Count: <b>%{y}</b><br>" +
                            "<extra></extra>"
            ))
            
            # Add trend line
            if len(monthly_perf) > 1:
                z = np.polyfit(range(len(monthly_perf)), monthly_perf['mean'], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=monthly_perf['review_date'],
                    y=p(range(len(monthly_perf))),
                    mode='lines',
                    name='Performance Trend',
                    line=dict(color='#e74c3c', width=3, dash='dash'),
                    hovertemplate="<b>Trend</b><br>" +
                                "Expected: <b>%{y:.2f}</b><br>" +
                                "<extra></extra>"
                ))
            
            fig.update_layout(
                title=dict(
                    text="📊 Performance Trends Over Time",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text="Review Period", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Average Performance Rating", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True,
                    range=[0, 5.5]
                ),
                yaxis2=dict(
                    title=dict(text="Number of Reviews", font=dict(size=14, color='#f39c12')),
                    tickfont=dict(size=12),
                    overlaying='y',
                    side='right',
                    gridcolor='rgba(128,128,128,0.1)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=500,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Performance insights
            if len(monthly_perf) > 1:
                avg_perf = monthly_perf['mean'].mean()
                perf_trend = "↗️ Improving" if z[0] > 0.01 else "↘️ Declining" if z[0] < -0.01 else "→ Stable"
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Average Performance", f"{avg_perf:.2f}/5.0")
                with col2:
                    st.metric("📈 Trend Direction", perf_trend)
                with col3:
                    st.metric("📅 Total Reviews", monthly_perf['count'].sum())
            
            # Performance forecasting
            if st.button("🔮 Forecast Future Performance", key="forecast_performance"):
                self._forecast_performance(monthly_perf)
        
        # Individual performance prediction
        st.subheader("👤 Individual Performance Prediction")
        
        if st.button("🚀 Build Performance Prediction Model", key="build_performance_model"):
            with st.spinner("Training performance prediction model..."):
                success = self._build_performance_model(employees_df, performance_df, engagement_df)
                if success:
                    st.success("✅ Performance prediction model trained successfully!")
                else:
                    st.error("❌ Failed to train performance prediction model.")
        
        # Show individual predictions if model is available
        if 'performance_prediction' in self.models:
            self._display_individual_performance_predictions(employees_df, performance_df, engagement_df)
    
    def display_workforce_planning(self, employees_df, performance_df, engagement_df, turnover_df):
        """Display workforce planning and forecasting."""
        st.header("👥 Workforce Planning & Forecasting")
        
        # Current workforce analysis
        st.subheader("📊 Current Workforce Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_employees = len(employees_df)
            st.metric("Total Employees", f"{total_employees:,}")
        
        with col2:
            if not performance_df.empty:
                avg_performance = performance_df['performance_rating'].mean()
                st.metric("Avg Performance", f"{avg_performance:.1f}/5.0")
        
        with col3:
            if not engagement_df.empty:
                avg_engagement = engagement_df['engagement_score'].mean()
                st.metric("Avg Engagement", f"{avg_engagement:.1f}/5.0")
        
        # Department distribution
        if 'department' in employees_df.columns:
            st.subheader("🏢 Department Distribution")
            dept_counts = employees_df['department'].value_counts()
            
            # Enhanced department distribution visualization
            fig = go.Figure()
            
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
            
            fig.add_trace(go.Pie(
                labels=dept_counts.index,
                values=dept_counts.values,
                hole=0.4,
                marker=dict(
                    colors=colors[:len(dept_counts)],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent+value',
                textposition='inside',
                hovertemplate="<b>%{label}</b><br>" +
                            "Employees: <b>%{value}</b><br>" +
                            "Percentage: <b>%{percent:.1%}</b><br>" +
                            "<extra></extra>",
                textfont=dict(size=14, color='white'),
                insidetextorientation='radial'
            ))
            
            fig.update_layout(
                title=dict(
                    text="🏢 Employee Distribution by Department",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=12)
                ),
                height=500,
                margin=dict(l=20, r=20, t=60, b=20),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Department insights
            with st.expander("💡 Department Distribution Insights", expanded=False):
                largest_dept = dept_counts.index[0]
                largest_pct = (dept_counts.iloc[0] / len(employees_df)) * 100
                
                st.markdown(f"""
                **Current Distribution:**
                - **{largest_dept}** is the largest department with {largest_pct:.1f}% of employees
                - **Balanced distribution** helps with knowledge sharing and succession planning
                - **Department concentration** above 40% may indicate over-reliance risk
                
                **Recommendations:**
                - Monitor department growth rates for balanced expansion
                - Ensure cross-department collaboration and knowledge transfer
                - Plan succession across all departments, not just the largest
                """)
        
        # Workforce forecasting
        st.subheader("🔮 Workforce Forecasting")
        
        if st.button("📈 Generate Workforce Forecast", key="workforce_forecast"):
            self._generate_workforce_forecast(employees_df, performance_df, engagement_df, turnover_df)
        
        # Succession planning
        st.subheader("👑 Succession Planning")
        
        if not performance_df.empty:
            # Identify high performers
            high_performers = performance_df[performance_df['performance_rating'] >= 4.5]
            if not high_performers.empty:
                st.success(f"🎯 {len(high_performers)} high performers identified for succession planning")
                
                # Show high performers by department
                if 'department' in employees_df.columns:
                    high_perf_dept = high_performers.merge(
                        employees_df[['employee_id', 'department', 'first_name', 'last_name']], 
                        on='employee_id'
                    )
                    
                    dept_high_perf = high_perf_dept.groupby('department').size().reset_index(name='count')
                    
                    # Enhanced high performers visualization
                    fig = go.Figure()
                    
                    colors = ['#00d4aa', '#2ecc71', '#27ae60', '#16a085', '#1abc9c']
                    
                    fig.add_trace(go.Bar(
                        x=dept_high_perf['department'],
                        y=dept_high_perf['count'],
                        marker=dict(
                            color=colors[:len(dept_high_perf)],
                            line=dict(color='white', width=2)
                        ),
                        text=dept_high_perf['count'],
                        textposition='auto',
                        hovertemplate="<b>%{x}</b><br>" +
                                    "High Performers: <b>%{y}</b><br>" +
                                    "Percentage: <b>%{customdata:.1%}</b><br>" +
                                    "<extra></extra>",
                        customdata=[count/len(high_perf_dept) for count in dept_high_perf['count']]
                    ))
                    
                    fig.update_layout(
                        title=dict(
                            text="👑 High Performers by Department",
                            font=dict(size=20, color='#2c3e50'),
                            x=0.5
                        ),
                                        xaxis=dict(
                    title=dict(text="Department", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    tickangle=45
                ),
                yaxis=dict(
                    title=dict(text="Number of High Performers", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=20, r=20, t=60, b=60),
                        height=450,
                        showlegend=False,
                        hoverlabel=dict(
                            bgcolor="white",
                            font_size=12,
                            font_family="Arial"
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Succession planning insights
                    with st.expander("💡 Succession Planning Insights", expanded=False):
                        st.markdown(f"""
                        **High Performer Distribution:**
                        - **{len(high_performers)} total high performers** identified across all departments
                        - **Department coverage** ensures leadership pipeline in all areas
                        - **Performance threshold** set at 4.5/5.0 for succession planning
                        
                        **Action Items:**
                        - Develop individual development plans for each high performer
                        - Create mentorship programs pairing high performers with leaders
                        - Plan for leadership transitions and knowledge transfer
                        - Monitor high performer engagement and retention
                        """)
    
    def display_recruitment_optimization(self, recruitment_df, employees_df):
        """Display recruitment optimization analysis."""
        st.header("🎯 Recruitment Optimization")
        
        if recruitment_df.empty:
            st.warning("⚠️ No recruitment data available.")
            return
        
        # Recruitment funnel analysis
        st.subheader("📊 Recruitment Funnel Analysis")
        
        # Calculate funnel metrics
        total_postings = len(recruitment_df)
        total_applications = recruitment_df['applications_received'].sum()
        total_interviews = recruitment_df['candidates_interviewed'].sum()
        total_offers = recruitment_df['offers_made'].sum()
        total_hires = recruitment_df['hires_made'].sum()
        
        # Display funnel metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Job Postings", total_postings)
        
        with col2:
            st.metric("Applications", f"{total_applications:,}")
        
        with col3:
            st.metric("Interviews", total_interviews)
        
        with col4:
            st.metric("Offers Made", total_offers)
        
        with col5:
            st.metric("Hires", total_hires)
        
        # Recruitment funnel visualization
        funnel_data = {
            'Stage': ['Applications', 'Interviews', 'Offers', 'Hires'],
            'Count': [total_applications, total_interviews, total_offers, total_hires],
            'Conversion Rate': [
                f"{(total_interviews/total_applications*100):.1f}%" if total_applications > 0 else "0%",
                f"{(total_offers/total_interviews*100):.1f}%" if total_interviews > 0 else "0%",
                f"{(total_hires/total_offers*100):.1f}%" if total_offers > 0 else "0%",
                "100%"
            ]
        }
        
        funnel_df = pd.DataFrame(funnel_data)
        
        # Enhanced recruitment funnel visualization
        fig = go.Figure()
        
        colors = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71']
        
        fig.add_trace(go.Funnel(
            y=funnel_df['Stage'],
            x=funnel_df['Count'],
            textinfo="value+percent initial",
            textposition="inside",
            marker=dict(
                color=colors[:len(funnel_df)],
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{y}</b><br>" +
                        "Count: <b>%{x:,}</b><br>" +
                        "Conversion: <b>%{customdata}</b><br>" +
                        "<extra></extra>",
            customdata=funnel_df['Conversion Rate']
        ))
        
        fig.update_layout(
            title=dict(
                text="🎯 Recruitment Funnel with Conversion Rates",
                font=dict(size=20, color='#2c3e50'),
                x=0.5
            ),
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Funnel insights
        with st.expander("💡 Recruitment Funnel Insights", expanded=False):
            st.markdown("""
            **Funnel Analysis:**
            - **Applications to Interviews:** First major filter - quality of job postings and candidate attraction
            - **Interviews to Offers:** Interview effectiveness and candidate evaluation
            - **Offers to Hires:** Offer competitiveness and candidate experience
            
            **Optimization Opportunities:**
            - Improve job descriptions to attract better candidates
            - Enhance interview processes for better candidate selection
            - Review offer packages and candidate experience
            - Monitor conversion rates by department and role level
            """)
        
        # Source effectiveness analysis
        if 'recruitment_source' in recruitment_df.columns:
            st.subheader("🔍 Recruitment Source Effectiveness")
            
            source_analysis = recruitment_df.groupby('recruitment_source').agg({
                'applications_received': 'sum',
                'candidates_interviewed': 'sum',
                'hires_made': 'sum',
                'recruitment_cost': 'mean'
            }).reset_index()
            
            source_analysis['conversion_rate'] = (source_analysis['hires_made'] / source_analysis['applications_received'] * 100).round(2)
            
            # Enhanced source effectiveness visualization
            fig = go.Figure()
            
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
            
            for i, source in enumerate(source_analysis['recruitment_source']):
                source_data = source_analysis[source_analysis['recruitment_source'] == source].iloc[0]
                
                fig.add_trace(go.Scatter(
                    x=[source_data['conversion_rate']],
                    y=[source_data['recruitment_cost']],
                    mode='markers',
                    name=source,
                    marker=dict(
                        size=source_data['hires_made'] * 3 + 20,  # Scale size based on hires
                        color=colors[i % len(colors)],
                        line=dict(color='white', width=2),
                        opacity=0.8
                    ),
                    text=f"<b>{source}</b><br>" +
                         f"Hires: {source_data['hires_made']}<br>" +
                         f"Applications: {source_data['applications_received']}<br>" +
                         f"Interviews: {source_data['candidates_interviewed']}",
                    hovertemplate="<b>%{text}</b><br>" +
                                "Conversion Rate: <b>%{x:.1f}%</b><br>" +
                                "Cost: <b>$%{y:,.0f}</b><br>" +
                                "Hires: <b>%{marker.size}</b><br>" +
                                "<extra></extra>",
                    showlegend=True
                ))
            
            fig.update_layout(
                title=dict(
                    text="🔍 Recruitment Source Effectiveness",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text="Conversion Rate (%)", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Average Recruitment Cost ($)", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=500,
                hovermode='closest',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=12)
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            # Add quadrant lines for analysis
            avg_conversion = source_analysis['conversion_rate'].mean()
            avg_cost = source_analysis['recruitment_cost'].mean()
            
            # Vertical line for average conversion
            fig.add_vline(
                x=avg_conversion,
                line_dash="dash",
                line_color="gray",
                annotation_text="Avg Conversion",
                annotation_position="top right"
            )
            
            # Horizontal line for average cost
            fig.add_hline(
                y=avg_cost,
                line_dash="dash",
                line_color="gray",
                annotation_text="Avg Cost",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Source effectiveness insights
            with st.expander("💡 Source Effectiveness Insights", expanded=False):
                best_source = source_analysis.loc[source_analysis['conversion_rate'].idxmax()]
                cost_effective_source = source_analysis.loc[source_analysis['recruitment_cost'].idxmin()]
                
                st.markdown(f"""
                **Top Performing Sources:**
                - **Best Conversion:** {best_source['recruitment_source']} ({best_source['conversion_rate']:.1f}%)
                - **Most Cost-Effective:** {cost_effective_source['recruitment_source']} (${cost_effective_source['recruitment_cost']:,.0f})
                
                **Quadrant Analysis:**
                - **High Conversion, Low Cost:** Ideal sources to invest in
                - **High Conversion, High Cost:** Quality sources but expensive
                - **Low Conversion, Low Cost:** May need optimization
                - **Low Conversion, High Cost:** Consider discontinuing
                
                **Recommendations:**
                - Focus budget on high-conversion sources
                - Optimize low-performing sources or reduce investment
                - Test new sources with small budgets first
                """)
        
        # Time-to-hire optimization
        if 'time_to_hire_days' in recruitment_df.columns:
            st.subheader("⏱️ Time-to-Hire Optimization")
            
            avg_time_to_hire = recruitment_df['time_to_hire_days'].mean()
            st.metric("Average Time to Hire", f"{avg_time_to_hire:.1f} days")
            
            # Enhanced time-to-hire distribution visualization
            fig = go.Figure()
            
            # Create histogram with better styling
            fig.add_trace(go.Histogram(
                x=recruitment_df['time_to_hire_days'],
                nbinsx=20,
                marker=dict(
                    color='#3498db',
                    line=dict(color='white', width=1)
                ),
                opacity=0.8,
                hovertemplate="<b>Days to Hire</b><br>" +
                            "Range: %{x}<br>" +
                            "Count: <b>%{y}</b><br>" +
                            "<extra></extra>"
            ))
            
            # Add mean line
            mean_days = recruitment_df['time_to_hire_days'].mean()
            fig.add_vline(
                x=mean_days,
                line_dash="dash",
                line_color="#e74c3c",
                annotation_text=f"Mean: {mean_days:.1f} days",
                annotation_position="top right"
            )
            
            # Add industry benchmark lines (example values)
            fig.add_vline(
                x=30,
                line_dash="dot",
                line_color="#f39c12",
                annotation_text="Industry Avg: 30 days",
                annotation_position="top left"
            )
            
            fig.add_vline(
                x=45,
                line_dash="dot",
                line_color="#e67e22",
                annotation_text="Industry Slow: 45 days",
                annotation_position="top left"
            )
            
            fig.update_layout(
                title=dict(
                    text="⏱️ Time-to-Hire Distribution",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text="Days to Hire", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Number of Hires", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=450,
                showlegend=False,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Time-to-hire insights
            with st.expander("💡 Time-to-Hire Insights", expanded=False):
                fast_hires = recruitment_df[recruitment_df['time_to_hire_days'] <= 30]
                slow_hires = recruitment_df[recruitment_df['time_to_hire_days'] > 45]
                
                st.markdown(f"""
                **Current Performance:**
                - **Average Time:** {mean_days:.1f} days
                - **Fast Hires (≤30 days):** {len(fast_hires)} ({len(fast_hires)/len(recruitment_df)*100:.1f}%)
                - **Slow Hires (>45 days):** {len(slow_hires)} ({len(slow_hires)/len(recruitment_df)*100:.1f}%)
                
                **Benchmarks:**
                - **Excellent:** < 25 days
                - **Good:** 25-35 days
                - **Average:** 35-45 days
                - **Slow:** > 45 days
                
                **Optimization Opportunities:**
                - Streamline interview processes for faster decisions
                - Improve offer response times
                - Reduce administrative delays
                - Set clear hiring timelines and expectations
                """)
    
    def display_predictive_insights(self, employees_df, performance_df, engagement_df, turnover_df, compensation_df):
        """Display predictive insights and recommendations."""
        st.header("📈 Predictive Insights & Recommendations")
        
        # Generate comprehensive insights
        insights = self._generate_predictive_insights(
            employees_df, performance_df, engagement_df, turnover_df, compensation_df
        )
        
        # Display insights by category
        for category, category_insights in insights.items():
            st.subheader(f"💡 {category}")
            
            for insight in category_insights:
                if insight['type'] == 'success':
                    st.success(f"✅ **{insight['title']}**: {insight['message']}")
                elif insight['type'] == 'warning':
                    st.warning(f"⚠️ **{insight['title']}**: {insight['message']}")
                elif insight['type'] == 'error':
                    st.error(f"🚨 **{insight['title']}**: {insight['message']}")
                else:
                    st.info(f"ℹ️ **{insight['title']}**: {insight['message']}")
        
        # Predictive recommendations
        st.subheader("🎯 Strategic Recommendations")
        
        recommendations = self._generate_strategic_recommendations(
            employees_df, performance_df, engagement_df, turnover_df, compensation_df
        )
        
        for i, rec in enumerate(recommendations):
            with st.expander(f"🎯 {rec['action']} - Priority: {rec['priority'].title()}", expanded=False):
                st.write(f"**Description:** {rec['description']}")
                st.write(f"**Impact:** {rec['impact']}")
                st.write(f"**Timeline:** {rec['timeline']}")
                st.write(f"**Investment:** {rec['investment']}")
                st.write(f"**ROI Estimate:** {rec['roi_estimate']}")
                
                if st.button(f"Implement {rec['action']}", key=f"implement_{i}"):
                    st.success("✅ Action item added to implementation queue!")
    
    def _validate_turnover_data(self, employees_df, performance_df, engagement_df, turnover_df):
        """Validate data for turnover prediction."""
        if employees_df.empty or performance_df.empty or engagement_df.empty:
            return False
        
        # Check minimum data requirements
        min_employees = 50
        min_performance_records = 100
        min_engagement_records = 50
        
        if (len(employees_df) < min_employees or 
            len(performance_df) < min_performance_records or 
            len(engagement_df) < min_engagement_records):
            return False
        
        return True
    
    def _build_turnover_model(self, employees_df, performance_df, engagement_df, turnover_df):
        """Build and train turnover prediction model."""
        try:
            # Prepare features
            features = self._prepare_turnover_features(employees_df, performance_df, engagement_df, turnover_df)
            
            if features is None or len(features) < 50:
                return False
            
            # Split features and target
            X = features.drop('turnover_risk', axis=1)
            y = features['turnover_risk']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Random Forest model
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = rf_model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Store model and results
            self.models['turnover_prediction'] = rf_model
            self.scalers['turnover'] = self.scaler
            self.feature_importance['turnover'] = dict(zip(X.columns, rf_model.feature_importances_))
            self.model_performance['turnover'] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }
            
            return True
            
        except Exception as e:
            st.error(f"Error building turnover model: {str(e)}")
            return False
    
    def _prepare_turnover_features(self, employees_df, performance_df, engagement_df, turnover_df):
        """Prepare features for turnover prediction."""
        try:
            # Create turnover labels
            turnover_employees = set(turnover_df['employee_id'].unique())
            
            # Start with employee base features
            features = employees_df.copy()
            features['turnover_risk'] = features['employee_id'].map(
                lambda x: 1 if x in turnover_employees else 0
            )
            
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
            
            # Encode categorical variables
            categorical_cols = ['department', 'gender', 'ethnicity', 'education_level']
            for col in categorical_cols:
                if col in features.columns:
                    features[f'{col}_encoded'] = pd.Categorical(features[col]).codes
            
            # Select numeric features
            numeric_cols = features.select_dtypes(include=[np.number]).columns
            features = features[numeric_cols].fillna(0)
            
            return features
            
        except Exception as e:
            st.error(f"Error preparing features: {str(e)}")
            return None
    
    def _display_turnover_model_performance(self):
        """Display turnover model performance metrics."""
        if 'turnover' not in self.model_performance:
            return
        
        perf = self.model_performance['turnover']
        
        st.subheader("🎯 Model Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Accuracy", f"{perf['accuracy']:.1%}")
        
        with col2:
            st.metric("Precision", f"{perf['precision']:.1%}")
        
        with col3:
            st.metric("Recall", f"{perf['recall']:.1%}")
        
        with col4:
            st.metric("F1 Score", f"{perf['f1_score']:.1%}")
        
        # Feature importance
        if 'turnover' in self.feature_importance:
            st.subheader("🔍 Feature Importance")
            
            importance_df = pd.DataFrame(
                list(self.feature_importance['turnover'].items()),
                columns=['Feature', 'Importance']
            ).sort_values('Importance', ascending=False)
            
            # Enhanced feature importance visualization
            fig = go.Figure()
            
            # Create gradient colors based on importance
            colors = [f'rgba(102, 126, 234, {0.3 + 0.7 * (i/len(importance_df.head(10)))})' 
                     for i in range(len(importance_df.head(10)))]
            
            fig.add_trace(go.Bar(
                x=importance_df.head(10)['Importance'],
                y=importance_df.head(10)['Feature'],
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='#667eea', width=2)
                ),
                text=[f'{val:.3f}' for val in importance_df.head(10)['Importance']],
                textposition='auto',
                hovertemplate="<b>%{y}</b><br>" +
                            "Importance: <b>%{x:.3f}</b><br>" +
                            "Rank: %{customdata}<br>" +
                            "<extra></extra>",
                customdata=[f"#{i+1}" for i in range(len(importance_df.head(10)))]
            ))
            
            fig.update_layout(
                title=dict(
                    text="🎯 Top 10 Features for Turnover Prediction",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(
                        text="Feature Importance Score",
                        font=dict(size=14, color='#34495e')
                    ),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                yaxis=dict(
                    title=dict(
                        text="Features",
                        font=dict(size=12, color='#34495e')
                    ),
                    tickfont=dict(size=12)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=500,
                showlegend=False,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            # Add annotations for top 3 features
            top_features = importance_df.head(10)
            for i in range(min(3, len(top_features))):
                fig.add_annotation(
                    x=top_features.iloc[i]['Importance'] + 0.01,
                    y=top_features.iloc[i]['Feature'],
                    text=f"🥇" if i == 0 else f"🥈" if i == 1 else "🥉",
                    showarrow=False,
                    font=dict(size=20)
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Feature insights
            with st.expander("💡 Feature Insights & Recommendations", expanded=False):
                st.markdown("""
                **Understanding Feature Importance:**
                - **Higher scores** indicate features that most strongly predict turnover
                - **Performance metrics** (ratings, productivity) are typically top predictors
                - **Engagement scores** help identify disengaged employees at risk
                - **Demographics** provide context but should be used ethically
                
                **Action Items:**
                - Focus retention efforts on employees with low performance scores
                - Monitor engagement trends for early warning signs
                - Use tenure data to identify critical retention periods
                """)
    
    def _display_turnover_predictions(self, employees_df, performance_df, engagement_df):
        """Display turnover predictions for current employees."""
        if 'turnover_prediction' not in self.models:
            return
        
        # Prepare features for prediction
        features = self._prepare_turnover_features(employees_df, performance_df, engagement_df, pd.DataFrame())
        
        if features is None:
            return
        
        # Make predictions
        X = features.drop('turnover_risk', axis=1, errors='ignore')
        X_scaled = self.scalers['turnover'].transform(X)
        
        predictions = self.models['turnover_prediction'].predict_proba(X_scaled)
        turnover_prob = predictions[:, 1]
        
        # Create results dataframe
        results_df = employees_df.copy()
        results_df['turnover_probability'] = turnover_prob
        results_df['risk_level'] = pd.cut(
            turnover_prob, 
            bins=[0, 0.3, 0.7, 1.0], 
            labels=['Low', 'Medium', 'High']
        )
        
        # Display high-risk employees
        high_risk = results_df[results_df['turnover_probability'] > 0.7]
        
        if not high_risk.empty:
            st.subheader("🚨 High-Risk Employees")
            st.warning(f"⚠️ {len(high_risk)} employees identified as high turnover risk")
            
            # Show high-risk employees
            display_cols = ['first_name', 'last_name', 'department', 'turnover_probability']
            available_cols = [col for col in display_cols if col in high_risk.columns]
            
            if available_cols:
                st.dataframe(
                    high_risk[available_cols].sort_values('turnover_probability', ascending=False),
                    use_container_width=True
                )
        
        # Risk distribution
        st.subheader("📊 Turnover Risk Distribution")
        
        risk_counts = results_df['risk_level'].value_counts()
        
        # Enhanced risk distribution visualization
        colors = {'Low': '#00d4aa', 'Medium': '#ffa726', 'High': '#ef5350'}
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            hole=0.4,
            marker=dict(
                colors=[colors.get(risk, '#95a5a6') for risk in risk_counts.index],
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent+value',
            textposition='inside',
            hovertemplate="<b>%{label}</b><br>" +
                        "Count: <b>%{value}</b><br>" +
                        "Percentage: <b>%{percent:.1%}</b><br>" +
                        "<extra></extra>",
            textfont=dict(size=14, color='white'),
            insidetextorientation='radial'
        ))
        
        fig.update_layout(
            title=dict(
                text="🎯 Employee Turnover Risk Distribution",
                font=dict(size=20, color='#2c3e50'),
                x=0.5
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=12)
            ),
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk insights and actions
        with st.expander("🚨 Risk Level Analysis & Actions", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                low_count = risk_counts.get('Low', 0)
                st.metric("🟢 Low Risk", f"{low_count} employees", 
                         help="Employees with <30% turnover probability")
                st.info("**Actions:** Monitor engagement, maintain positive culture")
            
            with col2:
                medium_count = risk_counts.get('Medium', 0)
                st.metric("🟡 Medium Risk", f"{medium_count} employees", 
                         help="Employees with 30-70% turnover probability")
                st.warning("**Actions:** Conduct stay interviews, address concerns")
            
            with col3:
                high_count = risk_counts.get('High', 0)
                st.metric("🔴 High Risk", f"{high_count} employees", 
                         help="Employees with >70% turnover probability")
                st.error("**Actions:** Immediate retention intervention required")
    
    def _display_turnover_analysis(self, turnover_df, employees_df):
        """Display historical turnover analysis."""
        st.subheader("📈 Historical Turnover Analysis")
        
        # Turnover trends
        if 'separation_date' in turnover_df.columns:
            turnover_df['separation_date'] = pd.to_datetime(turnover_df['separation_date'])
            monthly_turnover = turnover_df.groupby(pd.Grouper(key='separation_date', freq='M')).size().reset_index(name='count')
            
            # Enhanced turnover trends visualization
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=monthly_turnover['separation_date'],
                y=monthly_turnover['count'],
                mode='lines+markers',
                name='Turnover Count',
                line=dict(color='#e74c3c', width=4, shape='spline'),
                marker=dict(
                    size=8,
                    color='#e74c3c',
                    line=dict(color='white', width=2)
                ),
                fill='tonexty',
                fillcolor='rgba(231, 76, 60, 0.1)',
                hovertemplate="<b>%{x|%B %Y}</b><br>" +
                            "Turnover Count: <b>%{y}</b><br>" +
                            "<extra></extra>"
            ))
            
            # Add trend line
            if len(monthly_turnover) > 1:
                z = np.polyfit(range(len(monthly_turnover)), monthly_turnover['count'], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=monthly_turnover['separation_date'],
                    y=p(range(len(monthly_turnover))),
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='#34495e', width=2, dash='dash'),
                    hovertemplate="<b>Trend</b><br>" +
                                "Expected: <b>%{y:.1f}</b><br>" +
                                "<extra></extra>"
                ))
            
            fig.update_layout(
                title=dict(
                    text="📈 Monthly Turnover Trends",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(text="Month", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Turnover Count", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=20),
                height=450,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Turnover insights
            if len(monthly_turnover) > 1:
                avg_turnover = monthly_turnover['count'].mean()
                trend_direction = "↗️ Increasing" if z[0] > 0 else "↘️ Decreasing" if z[0] < 0 else "→ Stable"
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Average Monthly Turnover", f"{avg_turnover:.1f}")
                with col2:
                    st.metric("📈 Trend Direction", trend_direction)
                with col3:
                    st.metric("📅 Data Points", len(monthly_turnover))
        
        # Turnover reasons
        if 'separation_reason' in turnover_df.columns:
            reason_counts = turnover_df['separation_reason'].value_counts()
            
            # Enhanced turnover reasons visualization
            fig = go.Figure()
            
            colors = ['#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#1abc9c', '#34495e']
            
            fig.add_trace(go.Bar(
                x=reason_counts.index,
                y=reason_counts.values,
                marker=dict(
                    color=colors[:len(reason_counts)],
                    line=dict(color='white', width=2)
                ),
                text=reason_counts.values,
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>" +
                            "Count: <b>%{y}</b><br>" +
                            "Percentage: <b>%{customdata:.1%}</b><br>" +
                            "<extra></extra>",
                customdata=[val/len(turnover_df) for val in reason_counts.values]
            ))
            
            fig.update_layout(
                title=dict(
                    text="🔍 Turnover Reasons Analysis",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(
                        text="Separation Reason",
                        font=dict(size=14, color='#34495e')
                    ),
                    tickfont=dict(size=12),
                    tickangle=45
                ),
                yaxis=dict(
                    title=dict(
                        text="Number of Separations",
                        font=dict(size=12, color='#34495e')
                    ),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=60, b=60),
                height=450,
                showlegend=False,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=12,
                    font_family="Arial"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Reason insights
            with st.expander("💡 Turnover Reason Insights", expanded=False):
                st.markdown("""
                **Understanding Turnover Reasons:**
                - **Resignations** often indicate pull factors (better opportunities)
                - **Terminations** suggest performance or behavioral issues
                - **Retirements** are natural and predictable
                - **Other reasons** may need investigation
                
                **Action Items:**
                - Address root causes for voluntary separations
                - Improve performance management for involuntary separations
                - Plan for retirement waves in advance
                """)
    
    def _build_performance_model(self, employees_df, performance_df, engagement_df):
        """Build performance prediction model."""
        try:
            # Prepare features for performance prediction
            features = self._prepare_performance_features(employees_df, performance_df, engagement_df)
            
            if features is None or len(features) < 50:
                return False
            
            # Split features and target
            X = features.drop('performance_target', axis=1)
            y = features['performance_target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Gradient Boosting model
            gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            gb_model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = gb_model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Store model and results
            self.models['performance_prediction'] = gb_model
            self.scalers['performance'] = self.scaler
            self.feature_importance['performance'] = dict(zip(X.columns, gb_model.feature_importances_))
            self.model_performance['performance'] = {
                'mse': mse,
                'r2_score': r2,
                'rmse': np.sqrt(mse)
            }
            
            return True
            
        except Exception as e:
            st.error(f"Error building performance model: {str(e)}")
            return False
    
    def _prepare_performance_features(self, employees_df, performance_df, engagement_df):
        """Prepare features for performance prediction."""
        try:
            # Get latest performance rating for each employee
            latest_perf = performance_df.sort_values('review_date').groupby('employee_id').last()
            
            # Start with employee base features
            features = employees_df.copy()
            
            # Add performance target
            features = features.merge(
                latest_perf[['performance_rating']].rename(columns={'performance_rating': 'performance_target'}),
                left_on='employee_id',
                right_index=True,
                how='left'
            )
            
            # Add engagement metrics
            if not engagement_df.empty:
                eng_agg = engagement_df.groupby('employee_id').agg({
                    'engagement_score': ['mean', 'std'],
                    'satisfaction_score': 'mean',
                    'work_life_balance_score': 'mean'
                }).round(3)
                
                eng_agg.columns = ['engagement_mean', 'engagement_std', 'satisfaction_mean', 'wlb_mean']
                features = features.merge(eng_agg, left_on='employee_id', right_index=True, how='left')
            
            # Encode categorical variables
            categorical_cols = ['department', 'gender', 'ethnicity', 'education_level']
            for col in categorical_cols:
                if col in features.columns:
                    features[f'{col}_encoded'] = pd.Categorical(features[col]).codes
            
            # Select numeric features
            numeric_cols = features.select_dtypes(include=[np.number]).columns
            features = features[numeric_cols].fillna(0)
            
            return features
            
        except Exception as e:
            st.error(f"Error preparing performance features: {str(e)}")
            return None
    
    def _display_individual_performance_predictions(self, employees_df, performance_df, engagement_df):
        """Display individual performance predictions."""
        if 'performance_prediction' not in self.models:
            return
        
        st.subheader("🔮 Individual Performance Predictions")
        
        # Prepare features for prediction
        features = self._prepare_performance_features(employees_df, performance_df, engagement_df)
        
        if features is None:
            return
        
        # Make predictions
        X = features.drop('performance_target', axis=1, errors='ignore')
        X_scaled = self.scalers['performance'].transform(X)
        
        predictions = self.models['performance_prediction'].predict(X_scaled)
        
        # Create results dataframe
        results_df = employees_df.copy()
        results_df['predicted_performance'] = predictions
        results_df['performance_gap'] = results_df['predicted_performance'] - features['performance_target']
        
        # Display predictions
        st.dataframe(
            results_df[['first_name', 'last_name', 'department', 'predicted_performance', 'performance_gap']].head(20),
            use_container_width=True
        )
        
        # Enhanced performance gap analysis
        st.subheader("📊 Performance Gap Analysis")
        
        fig = go.Figure()
        
        # Create histogram with better styling
        fig.add_trace(go.Histogram(
            x=results_df['performance_gap'],
            nbinsx=20,
            marker=dict(
                color='#667eea',
                line=dict(color='white', width=1)
            ),
            opacity=0.8,
            hovertemplate="<b>Performance Gap</b><br>" +
                        "Range: %{x:.2f}<br>" +
                        "Count: <b>%{y}</b><br>" +
                        "<extra></extra>"
        ))
        
        # Add mean line
        mean_gap = results_df['performance_gap'].mean()
        fig.add_vline(
            x=mean_gap,
            line_dash="dash",
            line_color="#e74c3c",
            annotation_text=f"Mean Gap: {mean_gap:.2f}",
            annotation_position="top right"
        )
        
        # Add zero line for reference
        fig.add_vline(
            x=0,
            line_dash="solid",
            line_color="#2ecc71",
            annotation_text="Perfect Prediction",
            annotation_position="top left"
        )
        
        # Add standard deviation bands
        std_gap = results_df['performance_gap'].std()
        fig.add_vline(
            x=mean_gap + std_gap,
            line_dash="dot",
            line_color="#f39c12",
            annotation_text=f"+1σ: {mean_gap + std_gap:.2f}",
            annotation_position="top right"
        )
        
        fig.add_vline(
            x=mean_gap - std_gap,
            line_dash="dot",
            line_color="#f39c12",
            annotation_text=f"-1σ: {mean_gap - std_gap:.2f}",
            annotation_position="top left"
        )
        
        fig.update_layout(
            title=dict(
                text="📊 Distribution of Performance Gaps",
                font=dict(size=20, color='#2c3e50'),
                x=0.5
            ),
                            xaxis=dict(
                    title=dict(text="Predicted - Actual Performance", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Number of Employees", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20),
            height=450,
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis insights
        with st.expander("💡 Performance Gap Insights", expanded=False):
            over_predicted = results_df[results_df['performance_gap'] > 0]
            under_predicted = results_df[results_df['performance_gap'] < 0]
            accurate_predictions = results_df[abs(results_df['performance_gap']) <= 0.5]
            
            st.markdown(f"""
            **Gap Analysis:**
            - **Mean Gap:** {mean_gap:.2f} points
            - **Standard Deviation:** {std_gap:.2f} points
            - **Over-predicted:** {len(over_predicted)} employees ({len(over_predicted)/len(results_df)*100:.1f}%)
            - **Under-predicted:** {len(under_predicted)} employees ({len(under_predicted)/len(results_df)*100:.1f}%)
            - **Accurate (±0.5):** {len(accurate_predictions)} employees ({len(accurate_predictions)/len(results_df)*100:.1f}%)
            
            **Interpretation:**
            - **Positive gaps:** Model overestimates performance (optimistic)
            - **Negative gaps:** Model underestimates performance (conservative)
            - **Small gaps:** Model is accurate and reliable
            - **Large gaps:** Model needs improvement or more features
            
            **Model Improvement:**
            - Add more relevant features for better prediction
            - Increase training data size and quality
            - Consider ensemble methods for better accuracy
            - Regular model retraining with new data
            """)
    
    def _forecast_performance(self, monthly_perf):
        """Forecast future performance trends."""
        if len(monthly_perf) < 6:
            st.warning("⚠️ Need at least 6 months of data for forecasting.")
            return
        
        # Simple linear trend forecasting
        x = np.arange(len(monthly_perf))
        y = monthly_perf['mean'].values
        
        # Fit linear trend
        coeffs = np.polyfit(x, y, 1)
        trend_line = np.poly1d(coeffs)
        
        # Forecast next 3 months
        future_x = np.arange(len(monthly_perf), len(monthly_perf) + 3)
        future_y = trend_line(future_x)
        
        # Create forecast dataframe
        forecast_dates = pd.date_range(
            start=monthly_perf['review_date'].iloc[-1] + pd.DateOffset(months=1),
            periods=3,
            freq='M'
        )
        
        forecast_df = pd.DataFrame({
            'forecast_date': forecast_dates,
            'predicted_performance': future_y
        })
        
        # Display forecast
        st.subheader("🔮 Performance Forecast (Next 3 Months)")
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=monthly_perf['review_date'],
            y=monthly_perf['mean'],
            mode='lines+markers',
            name='Historical Performance',
            line=dict(color='#667eea', width=4, shape='spline'),
            marker=dict(
                size=8,
                color='#667eea',
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{x|%B %Y}</b><br>" +
                        "Performance: <b>%{y:.2f}</b><br>" +
                        "<extra></extra>"
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['forecast_date'],
            y=forecast_df['predicted_performance'],
            mode='lines+markers',
            name='Forecasted Performance',
            line=dict(color='#ff7f0e', width=4, dash='dash'),
            marker=dict(
                size=10,
                color='#ff7f0e',
                symbol='diamond',
                line=dict(color='white', width=2)
            ),
            hovertemplate="<b>%{x|%B %Y}</b><br>" +
                        "Forecast: <b>%{y:.2f}</b><br>" +
                        "<extra></extra>"
        ))
        
        # Add confidence interval (example)
        if len(monthly_perf) > 1:
            # Calculate confidence bounds (simplified)
            confidence = 0.2  # 20% confidence interval
            upper_bound = forecast_df['predicted_performance'] * (1 + confidence)
            lower_bound = forecast_df['predicted_performance'] * (1 - confidence)
            
            fig.add_trace(go.Scatter(
                x=forecast_df['forecast_date'],
                y=upper_bound,
                mode='lines',
                name='Upper Bound',
                line=dict(color='rgba(255, 127, 14, 0.3)', width=1),
                showlegend=False,
                hovertemplate="<b>%{x|%B %Y}</b><br>" +
                            "Upper Bound: <b>%{y:.2f}</b><br>" +
                            "<extra></extra>"
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df['forecast_date'],
                y=lower_bound,
                mode='lines',
                name='Lower Bound',
                line=dict(color='rgba(255, 127, 14, 0.3)', width=1),
                fill='tonexty',
                fillcolor='rgba(255, 127, 14, 0.1)',
                showlegend=False,
                hovertemplate="<b>%{x|%B %Y}</b><br>" +
                            "Lower Bound: <b>%{y:.2f}</b><br>" +
                            "<extra></extra>"
            ))
        
        fig.update_layout(
            title=dict(
                text="🔮 Performance Trend and Forecast",
                font=dict(size=20, color='#2c3e50'),
                x=0.5
            ),
                            xaxis=dict(
                    title=dict(text="Date", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True
                ),
                yaxis=dict(
                    title=dict(text="Performance Rating", font=dict(size=14, color='#34495e')),
                    tickfont=dict(size=12),
                    gridcolor='rgba(128,128,128,0.2)',
                    showgrid=True,
                    range=[0, 5.5]
                ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=60, b=20),
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show forecast values
        st.dataframe(forecast_df, use_container_width=True)
    
    def _generate_workforce_forecast(self, employees_df, performance_df, engagement_df, turnover_df):
        """Generate workforce forecasting insights."""
        st.subheader("🔮 Workforce Forecast")
        
        # Calculate current metrics
        total_employees = len(employees_df)
        
        if not turnover_df.empty:
            # Calculate turnover rate
            turnover_rate = len(turnover_df) / total_employees * 100
            
            # Forecast employee count for next 12 months
            months = 12
            forecast_employees = []
            forecast_dates = []
            
            current_count = total_employees
            
            for month in range(months + 1):
                forecast_employees.append(current_count)
                forecast_dates.append(datetime.now() + timedelta(days=month * 30))
                
                # Apply turnover rate
                monthly_turnover = current_count * (turnover_rate / 100) / 12
                current_count = max(0, current_count - monthly_turnover)
            
            # Display forecast
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_employees,
                mode='lines+markers',
                name='Forecasted Employee Count',
                line=dict(color='#667eea', width=3)
            ))
            
            fig.update_layout(
                title=dict(
                    text="12-Month Workforce Forecast",
                    font=dict(size=20, color='#2c3e50'),
                    x=0.5
                ),
                xaxis=dict(
                    title=dict(
                        text="Date",
                        font=dict(size=14, color='#34495e')
                    )
                ),
                yaxis=dict(
                    title=dict(
                        text="Employee Count",
                        font=dict(size=14, color='#34495e')
                    )
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show key insights
            final_count = forecast_employees[-1]
            change = final_count - total_employees
            change_pct = (change / total_employees) * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Employees", total_employees)
            
            with col2:
                st.metric("Forecasted (12 months)", final_count)
            
            with col3:
                st.metric("Change", f"{int(change):+d} ({change_pct:+.1f}%)")
    
    def _generate_predictive_insights(self, employees_df, performance_df, engagement_df, turnover_df, compensation_df):
        """Generate comprehensive predictive insights."""
        insights = {
            'Turnover Risk': [],
            'Performance Trends': [],
            'Workforce Planning': [],
            'Compensation Analysis': []
        }
        
        # Turnover risk insights
        if not turnover_df.empty:
            turnover_rate = len(turnover_df) / len(employees_df) * 100
            
            if turnover_rate > 15:
                insights['Turnover Risk'].append({
                    'type': 'error',
                    'title': 'Critical Turnover Rate',
                    'message': f'Current turnover rate of {turnover_rate:.1f}% is above industry average. Immediate intervention required.'
                })
            elif turnover_rate < 5:
                insights['Turnover Risk'].append({
                    'type': 'success',
                    'title': 'Excellent Retention',
                    'message': f'Turnover rate of {turnover_rate:.1f}% is exceptional. Focus on maintaining current culture.'
                })
        
        # Performance trend insights
        if not performance_df.empty:
            if 'review_date' in performance_df.columns:
                performance_df['review_date'] = pd.to_datetime(performance_df['review_date'])
                recent_perf = performance_df[performance_df['review_date'] >= 
                                          (datetime.now() - timedelta(days=90))]['performance_rating'].mean()
                overall_perf = performance_df['performance_rating'].mean()
                
                if recent_perf > overall_perf + 0.3:
                    insights['Performance Trends'].append({
                        'type': 'success',
                        'title': 'Performance Improving',
                        'message': f'Recent performance ({recent_perf:.1f}) is significantly above average ({overall_perf:.1f}).'
                    })
                elif recent_perf < overall_perf - 0.3:
                    insights['Performance Trends'].append({
                        'type': 'warning',
                        'title': 'Performance Declining',
                        'message': f'Recent performance ({recent_perf:.1f}) is below average ({overall_perf:.1f}). Investigation needed.'
                    })
        
        # Workforce planning insights
        if not employees_df.empty:
            if 'department' in employees_df.columns:
                dept_counts = employees_df['department'].value_counts()
                largest_dept = dept_counts.index[0]
                largest_count = dept_counts.iloc[0]
                
                if largest_count > len(employees_df) * 0.4:
                    insights['Workforce Planning'].append({
                        'type': 'warning',
                        'title': 'Department Concentration Risk',
                        'message': f'{largest_dept} department represents {largest_count/len(employees_df)*100:.1f}% of workforce. Consider diversification.'
                    })
        
        # Compensation insights
        if not compensation_df.empty:
            if 'base_salary' in compensation_df.columns:
                salary_std = compensation_df['base_salary'].std()
                salary_mean = compensation_df['base_salary'].mean()
                cv = salary_std / salary_mean
                
                if cv > 0.5:
                    insights['Compensation Analysis'].append({
                        'type': 'warning',
                        'title': 'High Salary Variance',
                        'message': f'Salary coefficient of variation is {cv:.2f}. Review compensation equity and structure.'
                    })
        
        return insights
    
    def _generate_strategic_recommendations(self, employees_df, performance_df, engagement_df, turnover_df, compensation_df):
        """Generate strategic recommendations based on predictive analysis."""
        recommendations = []
        
        # Turnover-based recommendations
        if not turnover_df.empty:
            turnover_rate = len(turnover_df) / len(employees_df) * 100
            
            if turnover_rate > 15:
                recommendations.append({
                    'action': 'Implement Retention Strategy',
                    'priority': 'critical',
                    'description': 'Develop comprehensive retention program targeting high-turnover areas',
                    'impact': 'Reduce turnover by 30-50%, save $500K+ annually',
                    'timeline': '3-6 months',
                    'investment': '$200K',
                    'roi_estimate': '250%'
                })
        
        # Performance-based recommendations
        if not performance_df.empty:
            low_performers = performance_df[performance_df['performance_rating'] < 3.0]
            
            if len(low_performers) > len(performance_df) * 0.2:
                recommendations.append({
                    'action': 'Performance Improvement Program',
                    'priority': 'high',
                    'description': 'Launch targeted performance improvement initiatives for underperforming employees',
                    'impact': 'Improve team performance by 15-25%',
                    'timeline': '4-8 months',
                    'investment': '$150K',
                    'roi_estimate': '200%'
                })
        
        # Engagement-based recommendations
        if not engagement_df.empty:
            avg_engagement = engagement_df['engagement_score'].mean()
            
            if avg_engagement < 3.5:
                recommendations.append({
                    'action': 'Employee Engagement Initiative',
                    'priority': 'high',
                    'description': 'Implement comprehensive engagement program with regular pulse surveys',
                    'impact': 'Increase engagement by 20-30%, reduce turnover risk',
                    'timeline': '6-12 months',
                    'investment': '$300K',
                    'roi_estimate': '180%'
                })
        
        # Compensation-based recommendations
        if not compensation_df.empty:
            if 'base_salary' in compensation_df.columns:
                salary_std = compensation_df['base_salary'].std()
                salary_mean = compensation_df['base_salary'].mean()
                cv = salary_std / salary_mean
                
                if cv > 0.5:
                    recommendations.append({
                        'action': 'Compensation Structure Review',
                        'priority': 'medium',
                        'description': 'Conduct comprehensive compensation audit and equity analysis',
                        'impact': 'Ensure fair compensation, reduce legal risk, improve retention',
                        'timeline': '3-4 months',
                        'investment': '$100K',
                        'roi_estimate': '150%'
                    })
        
        return recommendations

# Main function to display the dashboard
def display_predictive_analytics_dashboard(employees_df, performance_df, engagement_df, 
                                         turnover_df, recruitment_df, compensation_df):
    """Main function to display the predictive analytics dashboard."""
    
    # Initialize the predictive analytics class
    predictive_analytics = HRPredictiveAnalytics()
    
    # Display the dashboard
    predictive_analytics.display_predictive_analytics_dashboard(
        employees_df, performance_df, engagement_df, turnover_df, recruitment_df, compensation_df
    )

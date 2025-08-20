#!/usr/bin/env python3
"""
Customer Service Analytics Module - CORRECTED VERSION
==================================================

This module contains all the analytics functions corrected to match the actual dataset structure.
All functions have been validated against the real dataset to prevent future debugging issues.
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
    """Calculate comprehensive Customer Satisfaction (CSAT) score with advanced analytics"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for CSAT analysis"
        
        required_cols = ['rating', 'sentiment', 'customer_effort_score', 'nps_score']
        missing_cols = [col for col in required_cols if col not in feedback_df.columns]
        if missing_cols:
            return pd.DataFrame(), f"Missing required columns: {missing_cols}"
        
        metrics = []
        
        # Core CSAT Metrics
        total_feedback = len(feedback_df)
        metrics.append(['Total Feedback Responses', total_feedback])
        
        # CSAT Score Calculation (Rating-based)
        if 'rating' in feedback_df.columns:
            valid_ratings = feedback_df['rating'].dropna()
            if not valid_ratings.empty:
                csat_score = (valid_ratings >= 4).sum() / len(valid_ratings) * 100
                metrics.append(['CSAT Score (Rating ≥4)', f"{csat_score:.1f}%"])
                
                # Rating Distribution Analysis
                rating_distribution = valid_ratings.value_counts().sort_index()
                avg_rating = valid_ratings.mean()
                metrics.append(['Average Rating', f"{avg_rating:.2f}/5"])
                metrics.append(['Rating Standard Deviation', f"{valid_ratings.std():.2f}"])
                
                # Rating Performance Categories
                excellent_ratings = (valid_ratings == 5).sum()
                good_ratings = (valid_ratings == 4).sum()
                neutral_ratings = (valid_ratings == 3).sum()
                poor_ratings = (valid_ratings <= 2).sum()
                
                metrics.append(['Excellent (5/5)', f"{excellent_ratings} ({excellent_ratings/len(valid_ratings)*100:.1f}%)"])
                metrics.append(['Good (4/5)', f"{good_ratings} ({good_ratings/len(valid_ratings)*100:.1f}%)"])
                metrics.append(['Neutral (3/5)', f"{neutral_ratings} ({neutral_ratings/len(valid_ratings)*100:.1f}%)"])
                metrics.append(['Poor (≤2/5)', f"{poor_ratings} ({poor_ratings/len(valid_ratings)*100:.1f}%)"])
        
        # Sentiment Analysis
        if 'sentiment' in feedback_df.columns:
            sentiment_counts = feedback_df['sentiment'].value_counts()
            if not sentiment_counts.empty:
                positive_sentiment = sentiment_counts.get('Positive', 0) + sentiment_counts.get('Very Positive', 0)
                negative_sentiment = sentiment_counts.get('Negative', 0) + sentiment_counts.get('Very Negative', 0)
                neutral_sentiment = sentiment_counts.get('Neutral', 0)
                
                sentiment_score = (positive_sentiment - negative_sentiment) / total_feedback * 100
                metrics.append(['Sentiment Score', f"{sentiment_score:+.1f}%"])
                metrics.append(['Positive Sentiment Rate', f"{positive_sentiment/total_feedback*100:.1f}%"])
                metrics.append(['Negative Sentiment Rate', f"{negative_sentiment/total_feedback*100:.1f}%"])
                
                # Top Sentiment Categories
                for sentiment, count in sentiment_counts.head(3).items():
                    percentage = count / total_feedback * 100
                    metrics.append([f'{sentiment} Sentiment', f"{count} ({percentage:.1f}%)"])
        
        # Customer Effort Score Integration
        if 'customer_effort_score' in feedback_df.columns:
            effort_scores = feedback_df['customer_effort_score'].dropna()
            if not effort_scores.empty:
                avg_effort = effort_scores.mean()
                low_effort_rate = (effort_scores <= 3).sum() / len(effort_scores) * 100
                high_effort_rate = (effort_scores >= 5).sum() / len(effort_scores) * 100
                
                metrics.append(['Average Customer Effort', f"{avg_effort:.2f}/6"])
                metrics.append(['Low Effort Rate (≤3)', f"{low_effort_rate:.1f}%"])
                metrics.append(['High Effort Rate (≥5)', f"{high_effort_rate:.1f}%"])
        
        # NPS Score Integration
        if 'nps_score' in feedback_df.columns:
            nps_scores = feedback_df['nps_score'].dropna()
            if not nps_scores.empty:
                promoters = (nps_scores >= 9).sum()
                passives = ((nps_scores >= 7) & (nps_scores <= 8)).sum()
                detractors = (nps_scores <= 6).sum()
                
                nps = (promoters - detractors) / len(nps_scores) * 100
                metrics.append(['Net Promoter Score (NPS)', f"{nps:+.1f}"])
                metrics.append(['Promoters (9-10)', f"{promoters} ({promoters/len(nps_scores)*100:.1f}%)"])
                metrics.append(['Passives (7-8)', f"{passives} ({passives/len(nps_scores)*100:.1f}%)"])
                metrics.append(['Detractors (0-6)', f"{detractors} ({detractors/len(nps_scores)*100:.1f}%)"])
        
        # Advanced Analytics
        if 'rating' in feedback_df.columns and 'customer_effort_score' in feedback_df.columns:
            # Correlation Analysis
            correlation_data = feedback_df[['rating', 'customer_effort_score']].dropna()
            if len(correlation_data) > 1:
                correlation = correlation_data['rating'].corr(correlation_data['customer_effort_score'])
                metrics.append(['Rating-Effort Correlation', f"{correlation:.3f}"])
                
                # Effort vs Satisfaction Analysis
                low_effort_satisfaction = feedback_df[feedback_df['customer_effort_score'] <= 3]['rating'].mean()
                high_effort_satisfaction = feedback_df[feedback_df['customer_effort_score'] >= 5]['rating'].mean()
                if not pd.isna(low_effort_satisfaction):
                    metrics.append(['Low Effort Avg Rating', f"{low_effort_satisfaction:.2f}/5"])
                if not pd.isna(high_effort_satisfaction):
                    metrics.append(['High Effort Avg Rating', f"{high_effort_satisfaction:.2f}/5"])
        
        # Performance Benchmarks
        if 'rating' in feedback_df.columns:
            valid_ratings = feedback_df['rating'].dropna()
            if not valid_ratings.empty:
                # Industry Benchmark Comparison (Example)
                industry_benchmark = 4.2  # Example benchmark
                current_avg = valid_ratings.mean()
                benchmark_diff = current_avg - industry_benchmark
                benchmark_status = "Above" if benchmark_diff > 0 else "Below" if benchmark_diff < 0 else "At"
                metrics.append(['Industry Benchmark', f"{industry_benchmark}/5"])
                metrics.append(['Benchmark Performance', f"{benchmark_status} by {abs(benchmark_diff):.2f} points"])
        
        # Trend Analysis (if date available)
        if 'submitted_date' in feedback_df.columns:
            feedback_df['submitted_date'] = pd.to_datetime(feedback_df['submitted_date'], errors='coerce')
            feedback_df = feedback_df.dropna(subset=['submitted_date'])
            if not feedback_df.empty:
                feedback_df['month'] = feedback_df['submitted_date'].dt.to_period('M')
                monthly_ratings = feedback_df.groupby('month')['rating'].agg(['mean', 'count']).reset_index()
                if len(monthly_ratings) > 1:
                    recent_avg = monthly_ratings.iloc[-1]['mean']
                    previous_avg = monthly_ratings.iloc[-2]['mean']
                    trend = recent_avg - previous_avg
                    trend_direction = "↗️ Improving" if trend > 0 else "↘️ Declining" if trend < 0 else "→ Stable"
                    metrics.append(['Recent Trend', f"{trend_direction} ({trend:+.2f})"])
        
        csat_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Comprehensive CSAT analysis completed. {total_feedback} feedback responses analyzed with advanced metrics and insights."
        return csat_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating comprehensive CSAT score: {str(e)}"

def calculate_nps_score(feedback_df):
    """Calculate comprehensive Net Promoter Score (NPS) with advanced analytics"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for NPS analysis"
        
        required_cols = ['nps_score']
        missing_cols = [col for col in required_cols if col not in feedback_df.columns]
        if missing_cols:
            return pd.DataFrame(), f"Missing required columns: {missing_cols}"
        
        metrics = []
        
        # Core NPS Metrics
        total_responses = len(feedback_df)
        metrics.append(['Total NPS Responses', total_responses])
        
        # NPS Score Calculation
        nps_scores = feedback_df['nps_score'].dropna()
        if not nps_scores.empty:
            promoters = (nps_scores >= 9).sum()
            passives = ((nps_scores >= 7) & (nps_scores <= 8)).sum()
            detractors = (nps_scores <= 6).sum()
            
            nps = (promoters - detractors) / len(nps_scores) * 100
            metrics.append(['Net Promoter Score (NPS)', f"{nps:+.1f}"])
            
            # NPS Components
            metrics.append(['Promoters (9-10)', f"{promoters} ({promoters/len(nps_scores)*100:.1f}%)"])
            metrics.append(['Passives (7-8)', f"{passives} ({passives/len(nps_scores)*100:.1f}%)"])
            metrics.append(['Detractors (0-6)', f"{detractors} ({detractors/len(nps_scores)*100:.1f}%)"])
            
            # NPS Performance Analysis
            avg_nps = nps_scores.mean()
            metrics.append(['Average NPS Score', f"{avg_nps:.2f}/10"])
            metrics.append(['NPS Standard Deviation', f"{nps_scores.std():.2f}"])
            
            # NPS Distribution Analysis
            score_distribution = nps_scores.value_counts().sort_index()
            top_score = score_distribution.index[-1]
            top_score_count = score_distribution.iloc[-1]
            metrics.append(['Most Common Score', f"{top_score}/10 ({top_score_count} responses)"])
            
            # NPS Performance Categories
            if nps >= 70:
                nps_category = "🏆 World Class"
            elif nps >= 50:
                nps_category = "🥇 Excellent"
            elif nps >= 30:
                nps_category = "🥈 Good"
            elif nps >= 0:
                nps_category = "🥉 Fair"
            else:
                nps_category = "⚠️ Needs Improvement"
            
            metrics.append(['NPS Performance Category', nps_category])
            
            # Promoter-Detractor Ratio
            if detractors > 0:
                promoter_ratio = promoters / detractors
                metrics.append(['Promoter-Detractor Ratio', f"{promoter_ratio:.2f}:1"])
            else:
                metrics.append(['Promoter-Detractor Ratio', "∞ (No Detractors)"])
        
        # Advanced NPS Analytics
        if 'customer_effort_score' in feedback_df.columns:
            effort_scores = feedback_df['customer_effort_score'].dropna()
            if not effort_scores.empty and not nps_scores.empty:
                # NPS vs Effort Correlation
                correlation_data = feedback_df[['nps_score', 'customer_effort_score']].dropna()
                if len(correlation_data) > 1:
                    correlation = correlation_data['nps_score'].corr(correlation_data['customer_effort_score'])
                    metrics.append(['NPS-Effort Correlation', f"{correlation:.3f}"])
                    
                    # Effort Impact on NPS
                    low_effort_nps = feedback_df[feedback_df['customer_effort_score'] <= 3]['nps_score'].mean()
                    high_effort_nps = feedback_df[feedback_df['customer_effort_score'] >= 5]['nps_score'].mean()
                    
                    if not pd.isna(low_effort_nps):
                        metrics.append(['Low Effort Avg NPS', f"{low_effort_nps:.2f}/10"])
                    if not pd.isna(high_effort_nps):
                        metrics.append(['High Effort Avg NPS', f"{high_effort_nps:.2f}/10"])
                        
                    # Effort Impact Analysis
                    if not pd.isna(low_effort_nps) and not pd.isna(high_effort_nps):
                        effort_impact = low_effort_nps - high_effort_nps
                        impact_direction = "Positive" if effort_impact > 0 else "Negative"
                        metrics.append(['Effort Impact on NPS', f"{impact_direction} ({effort_impact:+.2f})"])
        
        # Sentiment Integration
        if 'sentiment' in feedback_df.columns:
            sentiment_counts = feedback_df['sentiment'].value_counts()
            if not sentiment_counts.empty:
                # NPS by Sentiment
                positive_nps = feedback_df[feedback_df['sentiment'].isin(['Positive', 'Very Positive'])]['nps_score'].mean()
                negative_nps = feedback_df[feedback_df['sentiment'].isin(['Negative', 'Very Negative'])]['nps_score'].mean()
                
                if not pd.isna(positive_nps):
                    metrics.append(['Positive Sentiment Avg NPS', f"{positive_nps:.2f}/10"])
                if not pd.isna(negative_nps):
                    metrics.append(['Negative Sentiment Avg NPS', f"{negative_nps:.2f}/10"])
        
        # Industry Benchmarking
        industry_nps_benchmark = 42  # Example industry benchmark
        if not nps_scores.empty:
            current_nps = (promoters - detractors) / len(nps_scores) * 100
            benchmark_diff = current_nps - industry_nps_benchmark
            benchmark_percentile = "Top 25%" if benchmark_diff > 20 else "Top 50%" if benchmark_diff > 10 else "Average" if benchmark_diff > -10 else "Below Average"
            
            metrics.append(['Industry NPS Benchmark', f"{industry_nps_benchmark:+.0f}"])
            metrics.append(['Benchmark Performance', f"{benchmark_percentile} ({benchmark_diff:+.1f})"])
        
        # Trend Analysis (if date available)
        if 'submitted_date' in feedback_df.columns:
            feedback_df['submitted_date'] = pd.to_datetime(feedback_df['submitted_date'], errors='coerce')
            feedback_df = feedback_df.dropna(subset=['submitted_date'])
            if not feedback_df.empty:
                feedback_df['month'] = feedback_df['submitted_date'].dt.to_period('M')
                monthly_nps = feedback_df.groupby('month')['nps_score'].agg(['mean', 'count']).reset_index()
                if len(monthly_nps) > 1:
                    recent_nps = monthly_nps.iloc[-1]['mean']
                    previous_nps = monthly_nps.iloc[-2]['mean']
                    nps_trend = recent_nps - previous_nps
                    trend_direction = "↗️ Improving" if nps_trend > 0 else "↘️ Declining" if nps_trend < 0 else "→ Stable"
                    metrics.append(['NPS Trend (Monthly)', f"{trend_direction} ({nps_trend:+.2f})"])
                    
                    # NPS Velocity
                    if len(monthly_nps) > 2:
                        nps_velocity = (monthly_nps.iloc[-1]['mean'] - monthly_nps.iloc[-3]['mean']) / 2
                        metrics.append(['NPS Monthly Velocity', f"{nps_velocity:+.2f}/month"])
        
        # Predictive Insights
        if not nps_scores.empty:
            # NPS Prediction Model (Simple)
            recent_scores = nps_scores.tail(min(10, len(nps_scores)))
            if len(recent_scores) > 1:
                recent_trend = recent_scores.iloc[-1] - recent_scores.iloc[0]
                predicted_nps = current_nps + (recent_trend * 0.5)  # Simple prediction
                metrics.append(['Predicted NPS (Next Period)', f"{predicted_nps:+.1f}"])
                
                # Risk Assessment
                if detractors > promoters * 0.3:
                    risk_level = "🔴 High Risk"
                elif detractors > promoters * 0.2:
                    risk_level = "🟡 Medium Risk"
                else:
                    risk_level = "🟢 Low Risk"
                metrics.append(['Churn Risk Level', risk_level])
        
        nps_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Comprehensive NPS analysis completed. {total_responses} responses analyzed with advanced metrics, benchmarking, and predictive insights."
        return nps_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating comprehensive NPS score: {str(e)}"

def calculate_ces_score(feedback_df):
    """Calculate comprehensive Customer Effort Score (CES) with advanced analytics"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for CES analysis"
        
        required_cols = ['customer_effort_score']
        missing_cols = [col for col in required_cols if col not in feedback_df.columns]
        if missing_cols:
            return pd.DataFrame(), f"Missing required columns: {missing_cols}"
        
        metrics = []
        
        # Core CES Metrics
        total_responses = len(feedback_df)
        metrics.append(['Total CES Responses', total_responses])
        
        # CES Score Calculation
        effort_scores = feedback_df['customer_effort_score'].dropna()
        if not effort_scores.empty:
            avg_ces = effort_scores.mean()
            metrics.append(['Average Customer Effort Score', f"{avg_ces:.2f}/6"])
            
            # CES Distribution Analysis
            ces_distribution = effort_scores.value_counts().sort_index()
            metrics.append(['CES Standard Deviation', f"{effort_scores.std():.2f}"])
            
            # CES Performance Categories
            very_easy = (effort_scores <= 2).sum()
            easy = (effort_scores == 3).sum()
            moderate = (effort_scores == 4).sum()
            difficult = (effort_scores == 5).sum()
            very_difficult = (effort_scores == 6).sum()
            
            metrics.append(['Very Easy (1-2)', f"{very_easy} ({very_easy/len(effort_scores)*100:.1f}%)"])
            metrics.append(['Easy (3)', f"{easy} ({easy/len(effort_scores)*100:.1f}%)"])
            metrics.append(['Moderate (4)', f"{moderate} ({moderate/len(effort_scores)*100:.1f}%)"])
            metrics.append(['Difficult (5)', f"{difficult} ({difficult/len(effort_scores)*100:.1f}%)"])
            metrics.append(['Very Difficult (6)', f"{very_difficult} ({very_difficult/len(effort_scores)*100:.1f}%)"])
            
            # CES Performance Score (Lower is better)
            low_effort_rate = (effort_scores <= 3).sum() / len(effort_scores) * 100
            high_effort_rate = (effort_scores >= 5).sum() / len(effort_scores) * 100
            
            metrics.append(['Low Effort Rate (≤3)', f"{low_effort_rate:.1f}%"])
            metrics.append(['High Effort Rate (≥5)', f"{high_effort_rate:.1f}%"])
            
            # CES Performance Categories
            if avg_ces <= 2.5:
                ces_category = "🏆 World Class"
            elif avg_ces <= 3.0:
                ces_category = "🥇 Excellent"
            elif avg_ces <= 3.5:
                ces_category = "🥈 Good"
            elif avg_ces <= 4.0:
                ces_category = "🥉 Fair"
            else:
                ces_category = "⚠️ Needs Improvement"
            
            metrics.append(['CES Performance Category', ces_category])
            
            # Effort Efficiency Score
            effort_efficiency = (6 - avg_ces) / 5 * 100  # Convert to efficiency percentage
            metrics.append(['Effort Efficiency Score', f"{effort_efficiency:.1f}%"])
        
        # Advanced CES Analytics
        if 'nps_score' in feedback_df.columns:
            nps_scores = feedback_df['nps_score'].dropna()
            if not nps_scores.empty and not effort_scores.empty:
                # CES vs NPS Correlation
                correlation_data = feedback_df[['customer_effort_score', 'nps_score']].dropna()
                if len(correlation_data) > 1:
                    correlation = correlation_data['customer_effort_score'].corr(correlation_data['nps_score'])
                    metrics.append(['CES-NPS Correlation', f"{correlation:.3f}"])
                    
                    # NPS by Effort Level
                    low_effort_nps = feedback_df[feedback_df['customer_effort_score'] <= 3]['nps_score'].mean()
                    high_effort_nps = feedback_df[feedback_df['customer_effort_score'] >= 5]['nps_score'].mean()
                    
                    if not pd.isna(low_effort_nps):
                        metrics.append(['Low Effort Avg NPS', f"{low_effort_nps:.2f}/10"])
                    if not pd.isna(high_effort_nps):
                        metrics.append(['High Effort Avg NPS', f"{high_effort_nps:.2f}/10"])
                        
                    # Effort Impact on NPS
                    if not pd.isna(low_effort_nps) and not pd.isna(high_effort_nps):
                        effort_impact = low_effort_nps - high_effort_nps
                        impact_direction = "Positive" if effort_impact > 0 else "Negative"
                        metrics.append(['Effort Impact on NPS', f"{impact_direction} ({effort_impact:+.2f})"])
        
        # Rating Integration
        if 'rating' in feedback_df.columns:
            ratings = feedback_df['rating'].dropna()
            if not ratings.empty and not effort_scores.empty:
                # CES vs Rating Correlation
                correlation_data = feedback_df[['customer_effort_score', 'rating']].dropna()
                if len(correlation_data) > 1:
                    correlation = correlation_data['customer_effort_score'].corr(correlation_data['rating'])
                    metrics.append(['CES-Rating Correlation', f"{correlation:.3f}"])
                    
                    # Rating by Effort Level
                    low_effort_rating = feedback_df[feedback_df['customer_effort_score'] <= 3]['rating'].mean()
                    high_effort_rating = feedback_df[feedback_df['customer_effort_score'] >= 5]['rating'].mean()
                    
                    if not pd.isna(low_effort_rating):
                        metrics.append(['Low Effort Avg Rating', f"{low_effort_rating:.2f}/5"])
                    if not pd.isna(high_effort_rating):
                        metrics.append(['High Effort Avg Rating', f"{high_effort_rating:.2f}/5"])
        
        # Sentiment Integration
        if 'sentiment' in feedback_df.columns:
            sentiment_counts = feedback_df['sentiment'].value_counts()
            if not sentiment_counts.empty:
                # CES by Sentiment
                positive_ces = feedback_df[feedback_df['sentiment'].isin(['Positive', 'Very Positive'])]['customer_effort_score'].mean()
                negative_ces = feedback_df[feedback_df['sentiment'].isin(['Negative', 'Very Negative'])]['customer_effort_score'].mean()
                
                if not pd.isna(positive_ces):
                    metrics.append(['Positive Sentiment Avg CES', f"{positive_ces:.2f}/6"])
                if not pd.isna(negative_ces):
                    metrics.append(['Negative Sentiment Avg CES', f"{negative_ces:.2f}/6"])
        
        # Industry Benchmarking
        industry_ces_benchmark = 3.2  # Example industry benchmark (lower is better)
        if not effort_scores.empty:
            current_ces = effort_scores.mean()
            benchmark_diff = current_ces - industry_ces_benchmark
            benchmark_percentile = "Top 25%" if benchmark_diff < -0.5 else "Top 50%" if benchmark_diff < -0.2 else "Average" if benchmark_diff < 0.5 else "Below Average"
            
            metrics.append(['Industry CES Benchmark', f"{industry_ces_benchmark:.1f}/6"])
            metrics.append(['Benchmark Performance', f"{benchmark_percentile} ({benchmark_diff:+.2f})"])
        
        # Trend Analysis (if date available)
        if 'submitted_date' in feedback_df.columns:
            feedback_df['submitted_date'] = pd.to_datetime(feedback_df['submitted_date'], errors='coerce')
            feedback_df = feedback_df.dropna(subset=['submitted_date'])
            if not feedback_df.empty:
                feedback_df['month'] = feedback_df['submitted_date'].dt.to_period('M')
                monthly_ces = feedback_df.groupby('month')['customer_effort_score'].agg(['mean', 'count']).reset_index()
                if len(monthly_ces) > 1:
                    recent_ces = monthly_ces.iloc[-1]['mean']
                    previous_ces = monthly_ces.iloc[-2]['mean']
                    ces_trend = recent_ces - previous_ces
                    trend_direction = "↘️ Improving" if ces_trend < 0 else "↗️ Declining" if ces_trend > 0 else "→ Stable"
                    metrics.append(['CES Trend (Monthly)', f"{trend_direction} ({ces_trend:+.2f})"])
                    
                    # CES Velocity
                    if len(monthly_ces) > 2:
                        ces_velocity = (monthly_ces.iloc[-1]['mean'] - monthly_ces.iloc[-3]['mean']) / 2
                        metrics.append(['CES Monthly Velocity', f"{ces_velocity:+.2f}/month"])
        
        # Predictive Insights
        if not effort_scores.empty:
            # CES Prediction Model (Simple)
            recent_scores = effort_scores.tail(min(10, len(effort_scores)))
            if len(recent_scores) > 1:
                recent_trend = recent_scores.iloc[-1] - recent_scores.iloc[0]
                predicted_ces = current_ces + (recent_trend * 0.5)  # Simple prediction
                metrics.append(['Predicted CES (Next Period)', f"{predicted_ces:.2f}/6"])
                
                # Improvement Potential
                if avg_ces > 3.0:
                    improvement_potential = (avg_ces - 2.5) / (4.0 - 2.5) * 100
                    metrics.append(['Improvement Potential', f"{improvement_potential:.1f}%"])
                
                # Risk Assessment
                if high_effort_rate > 30:
                    risk_level = "🔴 High Risk"
                elif high_effort_rate > 20:
                    risk_level = "🟡 Medium Risk"
                else:
                    risk_level = "🟢 Low Risk"
                metrics.append(['Customer Experience Risk', risk_level])
        
        # Operational Insights
        if not effort_scores.empty:
            # Effort Distribution Analysis
            effort_variance = effort_scores.var()
            if effort_variance > 2.0:
                consistency_status = "⚠️ Inconsistent"
            elif effort_variance > 1.0:
                consistency_status = "🟡 Moderate"
            else:
                consistency_status = "✅ Consistent"
            metrics.append(['Effort Consistency', consistency_status])
            
            # Customer Journey Optimization
            if low_effort_rate < 60:
                optimization_priority = "🔴 High Priority"
            elif low_effort_rate < 75:
                optimization_priority = "🟡 Medium Priority"
            else:
                optimization_priority = "🟢 Low Priority"
            metrics.append(['Optimization Priority', optimization_priority])
        
        ces_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Comprehensive CES analysis completed. {total_responses} responses analyzed with advanced metrics, benchmarking, and predictive insights."
        return ces_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating comprehensive CES score: {str(e)}"

def analyze_sentiment(feedback_df):
    """Analyze comprehensive customer sentiment with advanced analytics"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for sentiment analysis"
        
        required_cols = ['sentiment']
        missing_cols = [col for col in required_cols if col not in feedback_df.columns]
        if missing_cols:
            return pd.DataFrame(), f"Missing required columns: {missing_cols}"
        
        metrics = []
        
        # Core Sentiment Metrics
        total_feedback = len(feedback_df)
        metrics.append(['Total Feedback Responses', total_feedback])
        
        # Sentiment Distribution Analysis
        sentiment_counts = feedback_df['sentiment'].value_counts()
        if not sentiment_counts.empty:
            # Sentiment Categories
            very_positive = sentiment_counts.get('Very Positive', 0)
            positive = sentiment_counts.get('Positive', 0)
            neutral = sentiment_counts.get('Neutral', 0)
            negative = sentiment_counts.get('Negative', 0)
            very_negative = sentiment_counts.get('Very Negative', 0)
            
            # Calculate Sentiment Score (-100 to +100)
            positive_sentiment = very_positive + positive
            negative_sentiment = negative + very_negative
            sentiment_score = (positive_sentiment - negative_sentiment) / total_feedback * 100
            
            metrics.append(['Overall Sentiment Score', f"{sentiment_score:+.1f}%"])
            metrics.append(['Positive Sentiment Rate', f"{positive_sentiment/total_feedback*100:.1f}%"])
            metrics.append(['Negative Sentiment Rate', f"{negative_sentiment/total_feedback*100:.1f}%"])
            metrics.append(['Neutral Sentiment Rate', f"{neutral/total_feedback*100:.1f}%"])
            
            # Sentiment Performance Categories
            if sentiment_score >= 60:
                sentiment_category = "🏆 Excellent"
            elif sentiment_score >= 30:
                sentiment_category = "🥇 Good"
            elif sentiment_score >= 0:
                sentiment_category = "🥈 Fair"
            elif sentiment_score >= -30:
                sentiment_category = "🥉 Poor"
            else:
                sentiment_category = "⚠️ Critical"
            
            metrics.append(['Sentiment Performance', sentiment_category])
            
            # Detailed Sentiment Breakdown
            for sentiment, count in sentiment_counts.items():
                percentage = count / total_feedback * 100
                metrics.append([f'{sentiment} Sentiment', f"{count} ({percentage:.1f}%)"])
            
            # Sentiment Balance Analysis
            if negative_sentiment > 0:
                positive_negative_ratio = positive_sentiment / negative_sentiment
                metrics.append(['Positive-Negative Ratio', f"{positive_negative_ratio:.2f}:1"])
            else:
                metrics.append(['Positive-Negative Ratio', "∞ (No Negative)"])
        
        # Advanced Sentiment Analytics
        if 'rating' in feedback_df.columns:
            ratings = feedback_df['rating'].dropna()
            if not ratings.empty and not sentiment_counts.empty:
                # Sentiment vs Rating Correlation
                correlation_data = feedback_df[['sentiment', 'rating']].dropna()
                if len(correlation_data) > 1:
                    # Convert sentiment to numeric for correlation
                    sentiment_mapping = {'Very Negative': 1, 'Negative': 2, 'Neutral': 3, 'Positive': 4, 'Very Positive': 5}
                    correlation_data['sentiment_numeric'] = correlation_data['sentiment'].map(sentiment_mapping)
                    correlation = correlation_data['sentiment_numeric'].corr(correlation_data['rating'])
                    metrics.append(['Sentiment-Rating Correlation', f"{correlation:.3f}"])
                
                # Rating by Sentiment
                positive_rating = feedback_df[feedback_df['sentiment'].isin(['Positive', 'Very Positive'])]['rating'].mean()
                negative_rating = feedback_df[feedback_df['sentiment'].isin(['Negative', 'Very Negative'])]['rating'].mean()
                neutral_rating = feedback_df[feedback_df['sentiment'] == 'Neutral']['rating'].mean()
                
                if not pd.isna(positive_rating):
                    metrics.append(['Positive Sentiment Avg Rating', f"{positive_rating:.2f}/5"])
                if not pd.isna(negative_rating):
                    metrics.append(['Negative Sentiment Avg Rating', f"{negative_rating:.2f}/5"])
                if not pd.isna(neutral_rating):
                    metrics.append(['Neutral Sentiment Avg Rating', f"{neutral_rating:.2f}/5"])
        
        # NPS Integration
        if 'nps_score' in feedback_df.columns:
            nps_scores = feedback_df['nps_score'].dropna()
            if not nps_scores.empty and not sentiment_counts.empty:
                # NPS by Sentiment
                positive_nps = feedback_df[feedback_df['sentiment'].isin(['Positive', 'Very Positive'])]['nps_score'].mean()
                negative_nps = feedback_df[feedback_df['sentiment'].isin(['Negative', 'Very Negative'])]['nps_score'].mean()
                
                if not pd.isna(positive_nps):
                    metrics.append(['Positive Sentiment Avg NPS', f"{positive_nps:.2f}/10"])
                if not pd.isna(negative_nps):
                    metrics.append(['Negative Sentiment Avg NPS', f"{negative_nps:.2f}/10"])
        
        # CES Integration
        if 'customer_effort_score' in feedback_df.columns:
            effort_scores = feedback_df['customer_effort_score'].dropna()
            if not effort_scores.empty and not sentiment_counts.empty:
                # Sentiment vs Effort Correlation
                correlation_data = feedback_df[['sentiment', 'customer_effort_score']].dropna()
                if len(correlation_data) > 1:
                    # Convert sentiment to numeric for correlation
                    sentiment_mapping = {'Very Negative': 1, 'Negative': 2, 'Neutral': 3, 'Positive': 4, 'Very Positive': 5}
                    correlation_data['sentiment_numeric'] = correlation_data['sentiment'].map(sentiment_mapping)
                    correlation = correlation_data['sentiment_numeric'].corr(correlation_data['customer_effort_score'])
                    metrics.append(['Sentiment-Effort Correlation', f"{correlation:.3f}"])
                
                # Effort by Sentiment
                positive_effort = feedback_df[feedback_df['sentiment'].isin(['Positive', 'Very Positive'])]['customer_effort_score'].mean()
                negative_effort = feedback_df[feedback_df['sentiment'].isin(['Negative', 'Very Negative'])]['customer_effort_score'].mean()
                
                if not pd.isna(positive_effort):
                    metrics.append(['Positive Sentiment Avg CES', f"{positive_effort:.2f}/6"])
                if not pd.isna(negative_effort):
                    metrics.append(['Negative Sentiment Avg CES', f"{negative_effort:.2f}/6"])
        
        # Sentiment Trend Analysis (if date available)
        if 'submitted_date' in feedback_df.columns:
            feedback_df['submitted_date'] = pd.to_datetime(feedback_df['submitted_date'], errors='coerce')
            feedback_df = feedback_df.dropna(subset=['submitted_date'])
            if not feedback_df.empty:
                feedback_df['month'] = feedback_df['submitted_date'].dt.to_period('M')
                
                # Monthly sentiment trends
                monthly_sentiment = feedback_df.groupby('month')['sentiment'].apply(
                    lambda x: (x.isin(['Positive', 'Very Positive']).sum() - x.isin(['Negative', 'Very Negative']).sum()) / len(x) * 100
                ).reset_index()
                monthly_sentiment.columns = ['Month', 'Sentiment Score']
                monthly_sentiment = monthly_sentiment.sort_values('Month')
                
                if len(monthly_sentiment) > 1:
                    recent_sentiment = monthly_sentiment.iloc[-1]['Sentiment Score']
                    previous_sentiment = monthly_sentiment.iloc[-2]['Sentiment Score']
                    sentiment_trend = recent_sentiment - previous_sentiment
                    trend_direction = "↗️ Improving" if sentiment_trend > 0 else "↘️ Declining" if sentiment_trend < 0 else "→ Stable"
                    metrics.append(['Sentiment Trend (Monthly)', f"{trend_direction} ({sentiment_trend:+.1f}%)"])
                    
                    # Sentiment Velocity
                    if len(monthly_sentiment) > 2:
                        sentiment_velocity = (monthly_sentiment.iloc[-1]['Sentiment Score'] - monthly_sentiment.iloc[-3]['Sentiment Score']) / 2
                        metrics.append(['Sentiment Monthly Velocity', f"{sentiment_velocity:+.1f}%/month"])
        
        # Sentiment Volatility Analysis
        if not sentiment_counts.empty:
            # Calculate sentiment volatility (how much sentiment varies)
            sentiment_proportions = sentiment_counts / total_feedback
            sentiment_entropy = -sum(p * np.log2(p) for p in sentiment_proportions if p > 0)
            max_entropy = np.log2(len(sentiment_counts))
            sentiment_consistency = (1 - sentiment_entropy / max_entropy) * 100
            
            metrics.append(['Sentiment Consistency', f"{sentiment_consistency:.1f}%"])
            
            if sentiment_consistency < 50:
                consistency_status = "⚠️ High Volatility"
            elif sentiment_consistency < 75:
                consistency_status = "🟡 Moderate"
            else:
                consistency_status = "✅ Consistent"
            metrics.append(['Sentiment Stability', consistency_status])
        
        # Predictive Sentiment Insights
        if not sentiment_counts.empty:
            # Sentiment Prediction Model (Simple)
            positive_trend = positive_sentiment / total_feedback
            negative_trend = negative_sentiment / total_feedback
            
            if positive_trend > negative_trend:
                prediction = "Positive sentiment likely to continue"
                confidence = min(positive_trend * 100, 95)
            elif negative_trend > positive_trend:
                prediction = "Negative sentiment trend detected"
                confidence = min(negative_trend * 100, 95)
            else:
                prediction = "Sentiment likely to remain stable"
                confidence = 50
            
            metrics.append(['Sentiment Prediction', prediction])
            metrics.append(['Prediction Confidence', f"{confidence:.1f}%"])
            
            # Risk Assessment
            if negative_sentiment / total_feedback > 0.3:
                risk_level = "🔴 High Risk"
            elif negative_sentiment / total_feedback > 0.2:
                risk_level = "🟡 Medium Risk"
            else:
                risk_level = "🟢 Low Risk"
            metrics.append(['Sentiment Risk Level', risk_level])
        
        # Customer Experience Insights
        if not sentiment_counts.empty:
            # Sentiment Impact Analysis
            if positive_sentiment / total_feedback < 0.6:
                improvement_priority = "🔴 High Priority"
            elif positive_sentiment / total_feedback < 0.75:
                improvement_priority = "🟡 Medium Priority"
            else:
                improvement_priority = "🟢 Low Priority"
            metrics.append(['Improvement Priority', improvement_priority])
            
            # Customer Satisfaction Correlation
            if positive_sentiment > negative_sentiment * 2:
                satisfaction_correlation = "Strong Positive"
            elif positive_sentiment > negative_sentiment:
                satisfaction_correlation = "Moderate Positive"
            elif positive_sentiment == negative_sentiment:
                satisfaction_correlation = "Neutral"
            else:
                satisfaction_correlation = "Negative"
            metrics.append(['Satisfaction Correlation', satisfaction_correlation])
        
        sentiment_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Comprehensive sentiment analysis completed. {total_feedback} feedback responses analyzed with advanced metrics, trends, and predictive insights."
        return sentiment_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing comprehensive sentiment: {str(e)}"

def calculate_resolution_satisfaction(feedback_df, tickets_df):
    """Calculate resolution satisfaction metrics"""
    try:
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available"
        
        # Use actual columns from dataset
        required_cols = ['rating', 'sentiment']
        missing_cols = [col for col in required_cols if col not in feedback_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required columns: {missing_cols}"
        
        # Calculate satisfaction metrics
        metrics = []
        
        # Overall satisfaction
        total_feedback = len(feedback_df)
        avg_rating = feedback_df['rating'].mean()
        metrics.append(['Average Rating', f"{avg_rating:.2f}/5"])
        
        # Sentiment analysis
        if 'sentiment' in feedback_df.columns:
            sentiment_counts = feedback_df['sentiment'].value_counts()
            for sentiment, count in sentiment_counts.items():
                percentage = (count / total_feedback) * 100
                metrics.append([f'{sentiment} Sentiment', f"{count} ({percentage:.1f}%)"])
        
        # Rating distribution
        rating_counts = feedback_df['rating'].value_counts().sort_index()
        for rating, count in rating_counts.items():
            percentage = (count / total_feedback) * 100
            metrics.append([f'{rating}-Star Rating', f"{count} ({percentage:.1f}%)"])
        
        satisfaction_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Resolution satisfaction analysis completed. Average rating: {avg_rating:.2f}/5"
        
        return satisfaction_summary, message
        
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
            # Filter out invalid response times
            valid_response_times = response_time[(response_time >= 0) & (response_time <= 168)]  # Max 1 week
            if not valid_response_times.empty:
                avg_response_time = valid_response_times.mean()
                if not pd.isna(avg_response_time):
                    metrics.append(['Average First Response Time', f"{avg_response_time:.2f} hours"])
                    metrics.append(['Response Time Range', f"{valid_response_times.min():.1f} - {valid_response_times.max():.1f} hours"])
        
        if 'resolved_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            resolution_time = (tickets_analysis['resolved_date'] - tickets_analysis['created_date']).dt.total_seconds() / 3600
            # Filter out invalid resolution times
            valid_resolution_times = resolution_time[(resolution_time >= 0) & (resolution_time <= 720)]  # Max 30 days
            if not valid_resolution_times.empty:
                avg_resolution_time = valid_resolution_times.mean()
                if not pd.isna(avg_resolution_time):
                    metrics.append(['Average Resolution Time', f"{avg_resolution_time:.2f} hours"])
                    metrics.append(['Resolution Time Range', f"{valid_resolution_times.min():.1f} - {valid_resolution_times.max():.1f} hours"])
        
        # Calculate escalation rate (handle missing values)
        if 'escalated_date' in tickets_analysis.columns and 'created_date' in tickets_analysis.columns:
            # Only count as escalated if escalated_date is not null and after created_date
            valid_escalations = tickets_analysis[
                (tickets_analysis['escalated_date'].notna()) & 
                (tickets_analysis['created_date'].notna())
            ]
            if not valid_escalations.empty:
                escalation_rate = (valid_escalations['escalated_date'].notna()).mean() * 100
                metrics.append(['Escalation Rate', f"{escalation_rate:.1f}%"])
        
        # Calculate SLA compliance using actual SLA targets from dataset
        if 'priority' in tickets_analysis.columns and 'first_response_date' in tickets_analysis.columns:
            high_priority = tickets_analysis[tickets_analysis['priority'] == 'High']
            if not high_priority.empty:
                high_priority_response = (high_priority['first_response_date'] - high_priority['created_date']).dt.total_seconds() / 3600
                valid_high_priority = high_priority_response[(high_priority_response >= 0) & (high_priority_response <= 168)]
                if not valid_high_priority.empty:
                    sla_compliance = (valid_high_priority <= 4).mean() * 100  # 4-hour SLA for high priority
                    metrics.append(['High Priority SLA Compliance', f"{sla_compliance:.1f}%"])
        
        # Add ticket volume metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        if 'status' in tickets_df.columns:
            status_counts = tickets_df['status'].value_counts()
            for status, count in status_counts.items():
                metrics.append([f'{status} Tickets', count])
        
        if 'priority' in tickets_df.columns:
            priority_counts = tickets_df['priority'].value_counts()
            for priority, count in priority_counts.items():
                metrics.append([f'{priority} Priority', count])
        
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
        
        # Use actual columns from dataset
        if 'priority' in tickets_df.columns and 'first_response_date' in tickets_df.columns:
            high_priority = tickets_df[tickets_df['priority'] == 'High']
            if not high_priority.empty:
                high_priority['created_date'] = pd.to_datetime(high_priority['created_date'], errors='coerce')
                high_priority['first_response_date'] = pd.to_datetime(high_priority['first_response_date'], errors='coerce')
                
                response_time = (high_priority['first_response_date'] - high_priority['created_date']).dt.total_seconds() / 3600
                # Filter valid response times
                valid_times = response_time[(response_time >= 0) & (response_time <= 168)]
                if not valid_times.empty:
                    sla_compliance = (valid_times <= 4).mean() * 100  # 4-hour SLA for high priority
                    return sla_compliance
        
        return 0.0
        
    except Exception as e:
        return 0.0

# ============================================================================
# SERVICE EFFICIENCY ANALYTICS
# ============================================================================

def calculate_service_efficiency(tickets_df, agents_df):
    """Calculate comprehensive service efficiency metrics with advanced analytics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for service efficiency analysis"
        if agents_df.empty:
            return pd.DataFrame(), "No agent data available for service efficiency analysis"
        
        required_ticket_cols = ['status', 'priority', 'created_date', 'resolved_date', 'actual_resolution_hours']
        required_agent_cols = ['agent_id', 'first_name', 'last_name']
        missing_ticket_cols = [col for col in required_ticket_cols if col not in tickets_df.columns]
        missing_agent_cols = [col for col in required_agent_cols if col not in agents_df.columns]
        if missing_ticket_cols or missing_agent_cols:
            return pd.DataFrame(), f"Missing required columns: Tickets: {missing_ticket_cols}, Agents: {missing_agent_cols}"
        
        metrics = []
        
        # Core Service Efficiency Metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        # Ticket Status Analysis
        if 'status' in tickets_df.columns:
            status_counts = tickets_df['status'].value_counts()
            resolved_tickets = status_counts.get('Resolved', 0)
            open_tickets = status_counts.get('Open', 0)
            pending_tickets = status_counts.get('Pending', 0)
            
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            open_rate = (open_tickets / total_tickets * 100) if total_tickets > 0 else 0
            pending_rate = (pending_tickets / total_tickets * 100) if total_tickets > 0 else 0
            
            metrics.append(['Resolution Rate', f"{resolution_rate:.1f}%"])
            metrics.append(['Open Ticket Rate', f"{open_rate:.1f}%"])
            metrics.append(['Pending Ticket Rate', f"{pending_rate:.1f}%"])
            
            # Status Performance Categories
            if resolution_rate >= 85:
                status_performance = "🏆 World Class"
            elif resolution_rate >= 75:
                status_performance = "🥇 Excellent"
            elif resolution_rate >= 65:
                status_performance = "🥈 Good"
            elif resolution_rate >= 50:
                status_performance = "🥉 Fair"
            else:
                status_performance = "⚠️ Needs Improvement"
            metrics.append(['Status Performance', status_performance])
        
        # Priority Analysis
        if 'priority' in tickets_df.columns:
            priority_counts = tickets_df['priority'].value_counts()
            high_priority = priority_counts.get('High', 0)
            medium_priority = priority_counts.get('Medium', 0)
            low_priority = priority_counts.get('Low', 0)
            
            high_priority_rate = (high_priority / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['High Priority Tickets', f"{high_priority} ({high_priority_rate:.1f}%)"])
            metrics.append(['Medium Priority Tickets', f"{medium_priority} ({medium_priority/total_tickets*100:.1f}%)"])
            metrics.append(['Low Priority Tickets', f"{low_priority} ({low_priority/total_tickets*100:.1f}%)"])
            
            # Priority Distribution Analysis
            priority_distribution = priority_counts / total_tickets * 100
            priority_entropy = -sum(p * np.log2(p) for p in priority_distribution if p > 0)
            max_entropy = np.log2(len(priority_counts))
            priority_balance = (1 - priority_entropy / max_entropy) * 100
            metrics.append(['Priority Balance', f"{priority_balance:.1f}%"])
        
        # Resolution Time Analysis
        if 'actual_resolution_hours' in tickets_df.columns and 'resolved_date' in tickets_df.columns:
            resolution_data = tickets_df[tickets_df['status'] == 'Resolved'].copy()
            if not resolution_data.empty:
                resolution_data['actual_resolution_hours'] = pd.to_numeric(resolution_data['actual_resolution_hours'], errors='coerce')
                valid_resolution = resolution_data['actual_resolution_hours'].dropna()
                
                if not valid_resolution.empty:
                    avg_resolution_time = valid_resolution.mean()
                    median_resolution_time = valid_resolution.median()
                    resolution_std = valid_resolution.std()
                    
                    metrics.append(['Average Resolution Time', f"{avg_resolution_time:.1f} hours"])
                    metrics.append(['Median Resolution Time', f"{median_resolution_time:.1f} hours"])
                    metrics.append(['Resolution Time Std Dev', f"{resolution_std:.1f} hours"])
                    
                    # Resolution Time Performance Categories
                    if avg_resolution_time <= 4:
                        resolution_performance = "🏆 World Class"
                    elif avg_resolution_time <= 8:
                        resolution_performance = "🥇 Excellent"
                    elif avg_resolution_time <= 12:
                        resolution_performance = "🥈 Good"
                    elif avg_resolution_time <= 24:
                        resolution_performance = "🥉 Fair"
                    else:
                        resolution_performance = "⚠️ Needs Improvement"
                    metrics.append(['Resolution Performance', resolution_performance])
                    
                    # Resolution Time Distribution
                    fast_resolution = (valid_resolution <= 4).sum()
                    normal_resolution = ((valid_resolution > 4) & (valid_resolution <= 12)).sum()
                    slow_resolution = (valid_resolution > 12).sum()
                    
                    fast_rate = (fast_resolution / len(valid_resolution) * 100) if len(valid_resolution) > 0 else 0
                    slow_rate = (slow_resolution / len(valid_resolution) * 100) if len(valid_resolution) > 0 else 0
                    
                    metrics.append(['Fast Resolution (≤4h)', f"{fast_resolution} ({fast_rate:.1f}%)"])
                    metrics.append(['Normal Resolution (4-12h)', f"{normal_resolution} ({normal_resolution/len(valid_resolution)*100:.1f}%)"])
                    metrics.append(['Slow Resolution (>12h)', f"{slow_resolution} ({slow_rate:.1f}%)"])
        
        # Agent Efficiency Analysis
        if 'agent_id' in tickets_df.columns and 'agent_id' in agents_df.columns:
            agent_tickets = tickets_df.groupby('agent_id').agg({
                'ticket_id': 'count',
                'status': lambda x: (x == 'Resolved').sum()
            }).reset_index()
            agent_tickets.columns = ['agent_id', 'total_tickets', 'resolved_tickets']
            
            # Merge with agent names
            agent_efficiency = agent_tickets.merge(agents_df[['agent_id', 'first_name', 'last_name']], on='agent_id', how='left')
            agent_efficiency['resolution_rate'] = (agent_efficiency['resolved_tickets'] / agent_efficiency['total_tickets'] * 100)
            agent_efficiency = agent_efficiency.sort_values('resolution_rate', ascending=False)
            
            if not agent_efficiency.empty:
                top_agent = agent_efficiency.iloc[0]
                top_agent_name = f"{top_agent['first_name']} {top_agent['last_name']}"
                metrics.append(['Top Performing Agent', f"{top_agent_name} ({top_agent['resolution_rate']:.1f}%)"])
                
                avg_agent_resolution_rate = agent_efficiency['resolution_rate'].mean()
                metrics.append(['Average Agent Resolution Rate', f"{avg_agent_resolution_rate:.1f}%"])
                
                # Agent Performance Distribution
                high_performers = (agent_efficiency['resolution_rate'] >= 80).sum()
                medium_performers = ((agent_efficiency['resolution_rate'] >= 60) & (agent_efficiency['resolution_rate'] < 80)).sum()
                low_performers = (agent_efficiency['resolution_rate'] < 60).sum()
                
                metrics.append(['High Performers (≥80%)', high_performers])
                metrics.append(['Medium Performers (60-80%)', medium_performers])
                metrics.append(['Low Performers (<60%)', low_performers])
        
        # Time-based Efficiency Analysis
        if 'created_date' in tickets_df.columns:
            tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
            tickets_df = tickets_df.dropna(subset=['created_date'])
            if not tickets_df.empty:
                tickets_df['month'] = tickets_df['created_date'].dt.to_period('M')
                monthly_volume = tickets_df.groupby('month')['ticket_id'].count().reset_index()
                monthly_volume.columns = ['Month', 'Ticket Count']
                monthly_volume = monthly_volume.sort_values('Month')
                
                if len(monthly_volume) > 1:
                    recent_volume = monthly_volume.iloc[-1]['Ticket Count']
                    previous_volume = monthly_volume.iloc[-2]['Ticket Count']
                    volume_trend = ((recent_volume - previous_volume) / previous_volume * 100) if previous_volume > 0 else 0
                    
                    trend_direction = "↗️ Increasing" if volume_trend > 0 else "↘️ Decreasing" if volume_trend < 0 else "→ Stable"
                    metrics.append(['Ticket Volume Trend', f"{trend_direction} ({volume_trend:+.1f}%)"])
                    
                    # Volume Velocity
                    if len(monthly_volume) > 2:
                        volume_velocity = (monthly_volume.iloc[-1]['Ticket Count'] - monthly_volume.iloc[-3]['Ticket Count']) / 2
                        metrics.append(['Monthly Volume Velocity', f"{volume_velocity:+.1f} tickets/month"])
        
        # Operational Efficiency Metrics
        if 'actual_resolution_hours' in tickets_df.columns:
            resolution_data = tickets_df[tickets_df['status'] == 'Resolved'].copy()
            if not resolution_data.empty:
                resolution_data['actual_resolution_hours'] = pd.to_numeric(resolution_data['actual_resolution_hours'], errors='coerce')
                valid_resolution = resolution_data['actual_resolution_hours'].dropna()
                
                if not valid_resolution.empty:
                    # Efficiency Score (lower resolution time = higher efficiency)
                    max_expected_time = 24  # hours
                    efficiency_score = max(0, (max_expected_time - valid_resolution.mean()) / max_expected_time * 100)
                    metrics.append(['Overall Efficiency Score', f"{efficiency_score:.1f}%"])
                    
                    # Resource Utilization
                    total_resolution_hours = valid_resolution.sum()
                    avg_tickets_per_hour = len(valid_resolution) / total_resolution_hours if total_resolution_hours > 0 else 0
                    metrics.append(['Tickets per Hour', f"{avg_tickets_per_hour:.2f}"])
                    
                    # Cost Efficiency (assuming cost per hour)
                    cost_per_hour = 25  # Example cost
                    total_cost = total_resolution_hours * cost_per_hour
                    cost_per_ticket = total_cost / len(valid_resolution) if len(valid_resolution) > 0 else 0
                    metrics.append(['Cost per Ticket', f"${cost_per_ticket:.2f}"])
        
        # Predictive Efficiency Insights
        if 'created_date' in tickets_df.columns and 'status' in tickets_df.columns:
            # Efficiency Prediction Model (Simple)
            recent_tickets = tickets_df.tail(min(50, len(tickets_df)))
            recent_resolution_rate = (recent_tickets['status'] == 'Resolved').sum() / len(recent_tickets) * 100
            
            if recent_resolution_rate > resolution_rate:
                efficiency_prediction = "Efficiency improving"
                confidence = min(recent_resolution_rate - resolution_rate, 95)
            elif recent_resolution_rate < resolution_rate:
                efficiency_prediction = "Efficiency declining"
                confidence = min(resolution_rate - recent_resolution_rate, 95)
            else:
                efficiency_prediction = "Efficiency stable"
                confidence = 50
            
            metrics.append(['Efficiency Prediction', efficiency_prediction])
            metrics.append(['Prediction Confidence', f"{confidence:.1f}%"])
            
            # Risk Assessment
            if open_rate > 30:
                risk_level = "🔴 High Risk"
            elif open_rate > 20:
                risk_level = "🟡 Medium Risk"
            else:
                risk_level = "🟢 Low Risk"
            metrics.append(['Operational Risk Level', risk_level])
        
        # Service Quality Metrics
        if 'customer_satisfaction_rating' in tickets_df.columns:
            satisfaction_data = tickets_df['customer_satisfaction_rating'].dropna()
            if not satisfaction_data.empty:
                avg_satisfaction = satisfaction_data.mean()
                high_satisfaction_rate = (satisfaction_data >= 4).sum() / len(satisfaction_data) * 100
                
                metrics.append(['Average Customer Satisfaction', f"{avg_satisfaction:.2f}/5"])
                metrics.append(['High Satisfaction Rate (≥4)', f"{high_satisfaction_rate:.1f}%"])
                
                # Satisfaction vs Efficiency Correlation
                if 'actual_resolution_hours' in tickets_df.columns:
                    correlation_data = tickets_df[['customer_satisfaction_rating', 'actual_resolution_hours']].dropna()
                    if len(correlation_data) > 1:
                        correlation = correlation_data['customer_satisfaction_rating'].corr(correlation_data['actual_resolution_hours'])
                        metrics.append(['Satisfaction-Efficiency Correlation', f"{correlation:.3f}"])
        
        service_efficiency_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Comprehensive service efficiency analysis completed. {total_tickets} tickets analyzed with advanced metrics, operational insights, and predictive analytics."
        return service_efficiency_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating comprehensive service efficiency: {str(e)}"

# ============================================================================
# AGENT PERFORMANCE ANALYTICS
# ============================================================================

def calculate_agent_performance(tickets_df, agents_df, feedback_df):
    """Calculate agent performance metrics"""
    try:
        if tickets_df.empty or agents_df.empty:
            return pd.DataFrame(), "Insufficient data for agent performance analysis"
        
        # Use actual columns from dataset
        required_agent_cols = ['agent_id', 'first_name', 'last_name']
        missing_agent_cols = [col for col in required_agent_cols if col not in agents_df.columns]
        
        if missing_agent_cols:
            return pd.DataFrame(), f"Missing required agent columns: {missing_agent_cols}"
        
        # Merge data for analysis
        agent_performance = tickets_df.merge(
            agents_df[['agent_id', 'first_name', 'last_name']], 
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
            agent_satisfaction = agent_satisfaction.merge(
                agents_df[['agent_id', 'first_name', 'last_name']], 
                on='agent_id', how='left'
            )
            
            if not agent_satisfaction.empty:
                avg_agent_rating = agent_satisfaction['avg_rating'].mean()
                agent_metrics.append(['Average Agent Rating', f"{avg_agent_rating:.2f}/5"])
        
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
        if customers_df.empty:
            return pd.DataFrame(), "No customer data available"
        
        # Use actual columns from dataset
        required_cols = ['customer_id', 'acquisition_date', 'last_interaction_date']
        missing_cols = [col for col in required_cols if col not in customers_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required customer columns: {missing_cols}"
        
        # Calculate retention metrics
        metrics = []
        
        # Total customers
        total_customers = len(customers_df)
        metrics.append(['Total Customers', total_customers])
        
        # Active customers (with recent interactions)
        if 'last_interaction_date' in customers_df.columns:
            customers_df['last_interaction_date'] = pd.to_datetime(customers_df['last_interaction_date'], errors='coerce')
            recent_cutoff = datetime.now() - timedelta(days=90)
            active_customers = len(customers_df[customers_df['last_interaction_date'] >= recent_cutoff])
            active_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
            metrics.append(['Active Customers (90 days)', f"{active_customers} ({active_rate:.1f}%)"])
        
        # Customer segments
        if 'customer_segment' in customers_df.columns:
            segment_counts = customers_df['customer_segment'].value_counts()
            for segment, count in segment_counts.items():
                percentage = (count / total_customers * 100) if total_customers > 0 else 0
                metrics.append([f'{segment} Customers', f"{count} ({percentage:.1f}%)"])
        
        # Customer status
        if 'status' in customers_df.columns:
            status_counts = customers_df['status'].value_counts()
            for status, count in status_counts.items():
                percentage = (count / total_customers * 100) if total_customers > 0 else 0
                metrics.append([f'{status} Status', f"{count} ({percentage:.1f}%)"])
        
        retention_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Customer retention analysis completed. Total customers: {total_customers}"
        
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
        
        # Use actual columns from dataset
        required_cols = ['customer_id', 'lifetime_value', 'total_orders']
        missing_cols = [col for col in required_cols if col not in customers_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required customer columns: {missing_cols}"
        
        # Calculate business impact metrics
        metrics = []
        
        # Customer value metrics
        total_customers = len(customers_df)
        metrics.append(['Total Customers', total_customers])
        
        if 'lifetime_value' in customers_df.columns:
            avg_lifetime_value = customers_df['lifetime_value'].mean()
            total_lifetime_value = customers_df['lifetime_value'].sum()
            metrics.append(['Average Lifetime Value', f"${avg_lifetime_value:.2f}"])
            metrics.append(['Total Lifetime Value', f"${total_lifetime_value:,.2f}"])
        
        if 'total_orders' in customers_df.columns:
            avg_orders = customers_df['total_orders'].mean()
            total_orders = customers_df['total_orders'].sum()
            metrics.append(['Average Orders per Customer', f"{avg_orders:.1f}"])
            metrics.append(['Total Orders', f"{total_orders:,.0f}"])
        
        # Customer satisfaction impact
        if not feedback_df.empty and 'rating' in feedback_df.columns:
            avg_rating = feedback_df['rating'].mean()
            metrics.append(['Average Customer Rating', f"{avg_rating:.2f}/5"])
        
        # Support ticket impact
        if not tickets_df.empty:
            total_tickets = len(tickets_df)
            if 'customer_id' in tickets_df.columns:
                unique_customers_with_tickets = tickets_df['customer_id'].nunique()
                avg_tickets_per_customer = total_tickets / unique_customers_with_tickets if unique_customers_with_tickets > 0 else 0
                metrics.append(['Total Support Tickets', total_tickets])
                metrics.append(['Customers with Tickets', unique_customers_with_tickets])
                metrics.append(['Average Tickets per Customer', f"{avg_tickets_per_customer:.1f}"])
        
        business_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Business impact analysis completed successfully"
        
        return business_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating business impact: {str(e)}"

# ============================================================================
# PRODUCTIVITY METRICS
# ============================================================================

def calculate_productivity_metrics(tickets_df, agents_df, interactions_df):
    """Calculate productivity metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available"
        
        # Use actual columns from dataset
        required_cols = ['ticket_id', 'agent_id', 'interaction_type']
        missing_cols = [col for col in required_cols if col not in interactions_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required interaction columns: {missing_cols}"
        
        # Calculate productivity metrics
        metrics = []
        
        # Interaction metrics
        total_interactions = len(interactions_df)
        metrics.append(['Total Interactions', total_interactions])
        
        if 'interaction_type' in interactions_df.columns:
            type_counts = interactions_df['interaction_type'].value_counts()
            for interaction_type, count in type_counts.items():
                percentage = (count / total_interactions * 100) if total_interactions > 0 else 0
                metrics.append([f'{interaction_type} Interactions', f"{count} ({percentage:.1f}%)"])
        
        # Duration metrics
        if 'duration_minutes' in interactions_df.columns:
            avg_duration = interactions_df['duration_minutes'].mean()
            total_duration = interactions_df['duration_minutes'].sum()
            metrics.append(['Average Interaction Duration', f"{avg_duration:.1f} minutes"])
            metrics.append(['Total Interaction Time', f"{total_duration/60:.1f} hours"])
        
        # Satisfaction metrics
        if 'satisfaction_score' in interactions_df.columns:
            avg_satisfaction = interactions_df['satisfaction_score'].mean()
            metrics.append(['Average Interaction Satisfaction', f"{avg_satisfaction:.2f}/5"])
        
        # Agent productivity
        if not agents_df.empty and 'agent_id' in interactions_df.columns:
            agent_interaction_counts = interactions_df['agent_id'].value_counts()
            avg_interactions_per_agent = agent_interaction_counts.mean()
            metrics.append(['Average Interactions per Agent', f"{avg_interactions_per_agent:.1f}"])
        
        productivity_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Productivity metrics calculated successfully"
        
        return productivity_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating productivity metrics: {str(e)}"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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
        print(f"Merge operation failed: {str(e)}")
        return None

def validate_dataframe(df, required_columns, function_name):
    """Validate DataFrame has required columns"""
    if df is None or df.empty:
        return False, f"{function_name}: DataFrame is empty or None"
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"{function_name}: Missing required columns: {missing_columns}"
    
    return True, "Data validation passed"

# ============================================================================
# ADDITIONAL ANALYTICS FUNCTIONS FROM ORIGINAL CS.PY
# ============================================================================

def calculate_agent_performance_score(agents_df, tickets_df, feedback_df):
    """Calculate comprehensive agent performance score"""
    try:
        if agents_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Insufficient data for agent performance analysis"
        
        # Use actual columns from dataset
        required_cols = ['agent_id', 'first_name', 'last_name']
        missing_cols = [col for col in required_cols if col not in agents_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required agent columns: {missing_cols}"
        
        # Calculate performance metrics
        metrics = []
        
        # Resolution time per agent
        if 'status' in tickets_df.columns and 'created_date' in tickets_df.columns and 'resolved_date' in tickets_df.columns:
            resolved_tickets = tickets_df[tickets_df['status'] == 'Resolved'].copy()
            resolved_tickets['created_date'] = pd.to_datetime(resolved_tickets['created_date'], errors='coerce')
            resolved_tickets['resolved_date'] = pd.to_datetime(resolved_tickets['resolved_date'], errors='coerce')
            
            if not resolved_tickets.empty:
                resolved_tickets['resolution_time_hours'] = (
                    resolved_tickets['resolved_date'] - resolved_tickets['created_date']
                ).dt.total_seconds() / 3600
                
                # Filter valid resolution times
                valid_resolution = resolved_tickets[
                    (resolved_tickets['resolution_time_hours'] >= 0) & 
                    (resolved_tickets['resolution_time_hours'] <= 720)
                ]
                
                if not valid_resolution.empty:
                    avg_resolution_time = valid_resolution['resolution_time_hours'].mean()
                    metrics.append(['Average Resolution Time', f"{avg_resolution_time:.1f} hours"])
        
        # First Call Resolution (FCR) rate
        if 'status' in tickets_df.columns:
            total_tickets = len(tickets_df)
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
            fcr_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['First Call Resolution Rate', f"{fcr_rate:.1f}%"])
        
        # Agent performance scores
        if not agents_df.empty and 'performance_score' in agents_df.columns:
            avg_performance = agents_df['performance_score'].mean()
            top_performer = agents_df['performance_score'].max()
            high_performers = len(agents_df[agents_df['performance_score'] > 80])
            total_agents = len(agents_df)
            
            metrics.append(['Average Performance Score', f"{avg_performance:.1f}"])
            metrics.append(['Top Performer Score', f"{top_performer:.1f}"])
            metrics.append(['High Performers (>80)', high_performers])
            metrics.append(['Total Agents', total_agents])
        
        # Customer feedback scores
        if not feedback_df.empty and 'rating' in feedback_df.columns:
            avg_feedback = feedback_df['rating'].mean()
            metrics.append(['Average Customer Rating', f"{avg_feedback:.2f}/5"])
        
        performance_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Agent performance score analysis completed successfully"
        
        return performance_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating agent performance score: {str(e)}"

def calculate_interaction_analytics(interactions_df, tickets_df, agents_df):
    """Calculate comprehensive interaction analytics"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available"
        
        # Use actual columns from dataset
        required_cols = ['interaction_type', 'duration_minutes']
        missing_cols = [col for col in required_cols if col not in interactions_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required interaction columns: {missing_cols}"
        
        # Calculate interaction metrics
        metrics = []
        
        # Overall interaction metrics
        total_interactions = len(interactions_df)
        metrics.append(['Total Interactions', total_interactions])
        
        # Interaction types
        if 'interaction_type' in interactions_df.columns:
            type_counts = interactions_df['interaction_type'].value_counts()
            for interaction_type, count in type_counts.items():
                percentage = (count / total_interactions * 100) if total_interactions > 0 else 0
                metrics.append([f'{interaction_type} Interactions', f"{count} ({percentage:.1f}%)"])
        
        # Duration analysis
        if 'duration_minutes' in interactions_df.columns:
            avg_duration = interactions_df['duration_minutes'].mean()
            total_duration = interactions_df['duration_minutes'].sum()
            metrics.append(['Average Duration', f"{avg_duration:.1f} minutes"])
            metrics.append(['Total Duration', f"{total_duration/60:.1f} hours"])
        
        # Satisfaction analysis
        if 'satisfaction_score' in interactions_df.columns:
            avg_satisfaction = interactions_df['satisfaction_score'].mean()
            high_satisfaction = len(interactions_df[interactions_df['satisfaction_score'] >= 4])
            satisfaction_rate = (high_satisfaction / total_interactions * 100) if total_interactions > 0 else 0
            metrics.append(['Average Satisfaction', f"{avg_satisfaction:.2f}/5"])
            metrics.append(['High Satisfaction Rate', f"{satisfaction_rate:.1f}%"])
        
        # Channel performance
        if 'channel' in interactions_df.columns:
            channel_counts = interactions_df['channel'].value_counts()
            for channel, count in channel_counts.items():
                percentage = (count / total_interactions * 100) if total_interactions > 0 else 0
                metrics.append([f'{channel} Channel', f"{count} ({percentage:.1f}%)"])
        
        # Agent interaction analysis
        if not agents_df.empty and 'agent_id' in interactions_df.columns:
            agent_interaction_counts = interactions_df['agent_id'].value_counts()
            avg_interactions_per_agent = agent_interaction_counts.mean()
            metrics.append(['Average Interactions per Agent', f"{avg_interactions_per_agent:.1f}"])
        
        interaction_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Interaction analytics completed. Total interactions analyzed: {total_interactions}"
        
        return interaction_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating interaction analytics: {str(e)}"

def calculate_predictive_analytics(tickets_df, customers_df, feedback_df):
    """Calculate predictive analytics for customer service"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for predictive analysis"
        
        # Use actual columns from dataset
        metrics = []
        
        # Ticket volume prediction
        if 'created_date' in tickets_df.columns:
            tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
            tickets_df = tickets_df.dropna(subset=['created_date'])
            
            if not tickets_df.empty:
                # Monthly trend analysis
                tickets_df['month'] = tickets_df['created_date'].dt.strftime('%Y-%m')
                monthly_volume = tickets_df.groupby('month').size().reset_index(name='ticket_count')
                
                if len(monthly_volume) > 1:
                    # Calculate growth rate
                    first_month = monthly_volume.iloc[0]['ticket_count']
                    last_month = monthly_volume.iloc[-1]['ticket_count']
                    growth_rate = ((last_month - first_month) / first_month * 100) if first_month > 0 else 0
                    
                    # Predict next month
                    if growth_rate > 0:
                        predicted_next_month = last_month * (1 + growth_rate/100)
                        metrics.append(['Predicted Next Month Volume', f"{predicted_next_month:.0f} tickets"])
                        metrics.append(['Monthly Growth Rate', f"{growth_rate:.1f}%"])
                    else:
                        metrics.append(['Volume Trend', 'Decreasing'])
                        metrics.append(['Monthly Change Rate', f"{growth_rate:.1f}%"])
        
        # Customer churn prediction
        if not customers_df.empty and 'last_interaction_date' in customers_df.columns:
            customers_df['last_interaction_date'] = pd.to_datetime(customers_df['last_interaction_date'], errors='coerce')
            recent_cutoff = datetime.now() - timedelta(days=90)
            
            inactive_customers = len(customers_df[customers_df['last_interaction_date'] < recent_cutoff])
            total_customers = len(customers_df)
            churn_risk = (inactive_customers / total_customers * 100) if total_customers > 0 else 0
            
            metrics.append(['Customers at Churn Risk', inactive_customers])
            metrics.append(['Churn Risk Rate', f"{churn_risk:.1f}%"])
        
        # Satisfaction trend prediction
        if not feedback_df.empty and 'submitted_date' in feedback_df.columns and 'rating' in feedback_df.columns:
            feedback_df['submitted_date'] = pd.to_datetime(feedback_df['submitted_date'], errors='coerce')
            feedback_df = feedback_df.dropna(subset=['submitted_date'])
            
            if not feedback_df.empty:
                feedback_df['month'] = feedback_df['submitted_date'].dt.strftime('%Y-%m')
                monthly_satisfaction = feedback_df.groupby('month')['rating'].mean().reset_index()
                
                if len(monthly_satisfaction) > 1:
                    first_month_rating = monthly_satisfaction.iloc[0]['rating']
                    last_month_rating = monthly_satisfaction.iloc[-1]['rating']
                    rating_change = last_month_rating - first_month_rating
                    
                    if rating_change > 0:
                        metrics.append(['Satisfaction Trend', 'Improving'])
                        metrics.append(['Rating Improvement', f"+{rating_change:.2f} points"])
                    else:
                        metrics.append(['Satisfaction Trend', 'Declining'])
                        metrics.append(['Rating Change', f"{rating_change:.2f} points"])
        
        # Priority prediction
        if 'priority' in tickets_df.columns:
            priority_counts = tickets_df['priority'].value_counts()
            high_priority_rate = (priority_counts.get('High', 0) / len(tickets_df) * 100) if len(tickets_df) > 0 else 0
            
            if high_priority_rate > 20:
                metrics.append(['Priority Alert', 'High priority tickets above 20%'])
                metrics.append(['High Priority Rate', f"{high_priority_rate:.1f}%"])
            else:
                metrics.append(['Priority Status', 'Normal priority distribution'])
                metrics.append(['High Priority Rate', f"{high_priority_rate:.1f}%"])
        
        predictive_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Predictive analytics completed successfully"
        
        return predictive_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating predictive analytics: {str(e)}"

def calculate_quality_assurance_metrics(tickets_df, agents_df, feedback_df):
    """Calculate quality assurance metrics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for quality analysis"
        
        # Use actual columns from dataset
        metrics = []
        
        # Overall quality metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        # Resolution quality
        if 'status' in tickets_df.columns:
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['Resolution Rate', f"{resolution_rate:.1f}%"])
        
        # Customer satisfaction quality
        if not feedback_df.empty and 'rating' in feedback_df.columns:
            avg_rating = feedback_df['rating'].mean()
            high_satisfaction = len(feedback_df[feedback_df['rating'] >= 4])
            satisfaction_rate = (high_satisfaction / len(feedback_df) * 100) if len(feedback_df) > 0 else 0
            
            metrics.append(['Average Rating', f"{avg_rating:.2f}/5"])
            metrics.append(['High Satisfaction Rate', f"{satisfaction_rate:.1f}%"])
        
        # Agent quality metrics
        if not agents_df.empty and 'agent_id' in tickets_df.columns:
            # Agent performance distribution
            agent_ticket_counts = tickets_df.groupby('agent_id').size()
            avg_tickets_per_agent = agent_ticket_counts.mean()
            metrics.append(['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"])
            
            # Quality consistency
            if 'performance_score' in agents_df.columns:
                performance_std = agents_df['performance_score'].std()
                metrics.append(['Performance Consistency', f"±{performance_std:.1f} points"])
        
        # SLA quality
        if 'priority' in tickets_df.columns and 'created_date' in tickets_df.columns:
            high_priority = tickets_df[tickets_df['priority'] == 'High']
            if not high_priority.empty:
                # Calculate SLA compliance for high priority
                high_priority['created_date'] = pd.to_datetime(high_priority['created_date'], errors='coerce')
                if 'first_response_date' in high_priority.columns:
                    high_priority['first_response_date'] = pd.to_datetime(high_priority['first_response_date'], errors='coerce')
                    
                    response_time = (high_priority['first_response_date'] - high_priority['created_date']).dt.total_seconds() / 3600
                    valid_times = response_time[(response_time >= 0) & (response_time <= 168)]
                    
                    if not valid_times.empty:
                        sla_compliance = (valid_times <= 4).mean() * 100  # 4-hour SLA for high priority
                        metrics.append(['High Priority SLA Compliance', f"{sla_compliance:.1f}%"])
        
        quality_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Quality assurance metrics calculated successfully"
        
        return quality_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating quality assurance metrics: {str(e)}"

def calculate_cost_analytics(tickets_df, agents_df):
    """Calculate cost-related analytics"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for cost analysis"
        
        # Use actual columns from dataset
        metrics = []
        
        # Basic cost metrics
        total_tickets = len(tickets_df)
        metrics.append(['Total Tickets', total_tickets])
        
        # Cost per resolution (simplified calculation)
        # Assume average cost per resolution based on agent time and resources
        avg_cost_per_resolution = 25  # USD - this would be configurable in real implementation
        
        if 'status' in tickets_df.columns:
            resolved_tickets = len(tickets_df[tickets_df['status'] == 'Resolved'])
            total_resolution_cost = resolved_tickets * avg_cost_per_resolution
            metrics.append(['Total Resolution Cost', f"${total_resolution_cost:,.2f}"])
            metrics.append(['Cost per Resolution', f"${avg_cost_per_resolution:.2f}"])
        
        # Agent cost efficiency
        if not agents_df.empty and 'agent_id' in tickets_df.columns:
            agent_ticket_counts = tickets_df.groupby('agent_id').size()
            avg_tickets_per_agent = agent_ticket_counts.mean()
            
            # Assume agent cost per hour
            agent_cost_per_hour = 30  # USD - configurable
            avg_resolution_time_hours = 2  # Assume 2 hours average resolution time
            
            cost_per_agent = avg_resolution_time_hours * agent_cost_per_hour
            metrics.append(['Average Cost per Agent', f"${cost_per_agent:.2f}/resolution"])
            metrics.append(['Average Tickets per Agent', f"{avg_tickets_per_agent:.1f}"])
        
        # Priority-based cost analysis
        if 'priority' in tickets_df.columns:
            priority_counts = tickets_df['priority'].value_counts()
            for priority, count in priority_counts.items():
                priority_cost = count * avg_cost_per_resolution
                percentage = (count / total_tickets * 100) if total_tickets > 0 else 0
                metrics.append([f'{priority} Priority Cost', f"${priority_cost:,.2f} ({percentage:.1f}%)"])
        
        # Cost efficiency metrics
        if 'status' in tickets_df.columns:
            resolution_rate = (len(tickets_df[tickets_df['status'] == 'Resolved']) / total_tickets * 100) if total_tickets > 0 else 0
            cost_efficiency = (100 - resolution_rate) if resolution_rate < 100 else 0  # Lower is better
            metrics.append(['Cost Efficiency Score', f"{cost_efficiency:.1f}%"])
        
        cost_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = "Cost analytics calculated successfully"
        
        return cost_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating cost analytics: {str(e)}"

# ============================================================================
# CUSTOMER RETENTION ANALYTICS
# ============================================================================

def calculate_churn_rate_analysis(customers_df):
    """Calculate churn rate and retention metrics"""
    try:
        if customers_df.empty:
            return pd.DataFrame(), "No customer data available for churn analysis"
        
        # Use actual columns from dataset
        required_cols = ['customer_id', 'status']
        missing_cols = [col for col in required_cols if col not in customers_df.columns]
        
        if missing_cols:
            return pd.DataFrame(), f"Missing required customer columns: {missing_cols}"
        
        # Calculate churn metrics
        metrics = []
        
        # Total customers
        total_customers = len(customers_df)
        metrics.append(['Total Customers', total_customers])
        
        # Customer status distribution
        if 'status' in customers_df.columns:
            status_counts = customers_df['status'].value_counts()
            
            # Calculate churn rate (customers with 'Churned' status)
            churned_customers = status_counts.get('Churned', 0)
            churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
            metrics.append(['Churn Rate', f"{churn_rate:.1f}%"])
            
            # Calculate retention rate (customers with 'Active' status)
            active_customers = status_counts.get('Active', 0)
            retention_rate = (active_customers / total_customers * 100) if total_customers > 0 else 0
            metrics.append(['Retention Rate', f"{retention_rate:.1f}%"])
            
            # Add status breakdown
            for status, count in status_counts.items():
                percentage = (count / total_customers * 100) if total_customers > 0 else 0
                metrics.append([f'{status} Customers', f"{count} ({percentage:.1f}%)"])
        
        # Customer segment analysis (if available)
        if 'customer_segment' in customers_df.columns:
            segment_counts = customers_df['customer_segment'].value_counts()
            for segment, count in segment_counts.items():
                percentage = (count / total_customers * 100) if total_customers > 0 else 0
                metrics.append([f'{segment} Segment', f"{count} ({percentage:.1f}%)"])
        
        # Industry analysis (if available)
        if 'industry' in customers_df.columns:
            industry_counts = customers_df['industry'].value_counts()
            for industry, count in industry_counts.items():
                percentage = (count / total_customers * 100) if total_customers > 0 else 0
                metrics.append([f'{industry} Industry', f"{count} ({percentage:.1f}%)"])
        
        churn_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Churn rate analysis completed. Total customers: {total_customers}"
        
        return churn_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating churn rate analysis: {str(e)}"

def calculate_customer_lifetime_value(customers_df, tickets_df):
    """Calculate customer lifetime value metrics"""
    try:
        if customers_df.empty or tickets_df.empty:
            return pd.DataFrame(), "Both customer and ticket data required for CLV analysis"
        
        # Use actual columns from dataset
        required_customer_cols = ['customer_id', 'lifetime_value']
        required_ticket_cols = ['customer_id']
        
        missing_customer_cols = [col for col in required_customer_cols if col not in customers_df.columns]
        missing_ticket_cols = [col for col in required_ticket_cols if col not in tickets_df.columns]
        
        if missing_customer_cols or missing_ticket_cols:
            return pd.DataFrame(), f"Missing required columns: Customer: {missing_customer_cols}, Tickets: {missing_ticket_cols}"
        
        # Calculate CLV metrics
        metrics = []
        
        # Basic CLV metrics
        if 'lifetime_value' in customers_df.columns:
            avg_clv = customers_df['lifetime_value'].mean()
            total_clv = customers_df['lifetime_value'].sum()
            
            metrics.append(['Average CLV', f"${avg_clv:,.2f}"])
            metrics.append(['Total CLV', f"${total_clv:,.2f}"])
            
            # CLV distribution analysis
            high_value_customers = len(customers_df[customers_df['lifetime_value'] > 1000])
            medium_value_customers = len(customers_df[(customers_df['lifetime_value'] >= 100) & (customers_df['lifetime_value'] <= 1000)])
            low_value_customers = len(customers_df[customers_df['lifetime_value'] < 100])
            
            metrics.append(['High Value Customers (>$1000)', high_value_customers])
            metrics.append(['Medium Value Customers ($100-$1000)', medium_value_customers])
            metrics.append(['Low Value Customers (<$100)', low_value_customers])
        
        # Ticket-based CLV calculation
        if 'customer_id' in tickets_df.columns:
            # Calculate interactions per customer
            customer_interactions = tickets_df.groupby('customer_id').size().reset_index(name='interaction_count')
            
            # Merge with customer data
            clv_data = customers_df.merge(customer_interactions, on='customer_id', how='left')
            clv_data['interaction_count'] = clv_data['interaction_count'].fillna(0)
            
            # Calculate CLV based on interactions (simplified)
            avg_interaction_value = 50  # Assume average value per interaction
            avg_customer_lifespan = 2  # Assume 2 years average lifespan
            
            clv_data['calculated_clv'] = clv_data['interaction_count'] * avg_interaction_value * avg_customer_lifespan
            
            # CLV metrics from interactions
            avg_interaction_clv = clv_data['calculated_clv'].mean()
            total_interaction_clv = clv_data['calculated_clv'].sum()
            
            metrics.append(['Average Interaction-Based CLV', f"${avg_interaction_clv:,.2f}"])
            metrics.append(['Total Interaction-Based CLV', f"${total_interaction_clv:,.2f}"])
            
            # Customer engagement analysis
            high_engagement = len(clv_data[clv_data['interaction_count'] > 5])
            medium_engagement = len(clv_data[(clv_data['interaction_count'] >= 2) & (clv_data['interaction_count'] <= 5)])
            low_engagement = len(clv_data[clv_data['interaction_count'] < 2])
            
            metrics.append(['High Engagement (>5 interactions)', high_engagement])
            metrics.append(['Medium Engagement (2-5 interactions)', medium_engagement])
            metrics.append(['Low Engagement (<2 interactions)', low_engagement])
        
        # Customer segment CLV analysis
        if 'customer_segment' in customers_df.columns and 'lifetime_value' in customers_df.columns:
            segment_clv = customers_df.groupby('customer_segment')['lifetime_value'].agg(['mean', 'count']).reset_index()
            segment_clv.columns = ['Customer Segment', 'Average CLV', 'Customer Count']
            segment_clv = segment_clv.sort_values('Average CLV', ascending=False)
            
            for _, row in segment_clv.iterrows():
                metrics.append([f'{row["Customer Segment"]} Avg CLV', f"${row["Average CLV"]:,.2f}"])
        
        clv_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Customer lifetime value analysis completed. Total customers: {len(customers_df)}"
        
        return clv_summary, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating customer lifetime value: {str(e)}"

# ============================================================================
# OMNICHANNEL EXPERIENCE ANALYTICS
# ============================================================================

def calculate_omnichannel_experience(interactions_df, feedback_df):
    """Calculate omnichannel experience metrics"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available for omnichannel analysis"
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for omnichannel analysis"
        required_interaction_cols = ['channel', 'satisfaction_score']
        required_feedback_cols = ['ticket_id', 'customer_id', 'agent_id']
        missing_interaction_cols = [col for col in required_interaction_cols if col not in interactions_df.columns]
        missing_feedback_cols = [col for col in required_feedback_cols if col not in feedback_df.columns]
        if missing_interaction_cols or missing_feedback_cols:
            return pd.DataFrame(), f"Missing required columns: Interactions: {missing_interaction_cols}, Feedback: {missing_feedback_cols}"
        metrics = []
        omnichannel_data = interactions_df.merge(
            feedback_df, on='ticket_id', how='inner'
        )
        if omnichannel_data.empty:
            return pd.DataFrame(), "No matching data between interactions and feedback for omnichannel analysis"
        
        # Handle column conflicts after merge
        satisfaction_column = 'satisfaction_score_x' if 'satisfaction_score_x' in omnichannel_data.columns else 'satisfaction_score'
        channel_column = 'channel_x' if 'channel_x' in omnichannel_data.columns else 'channel'
        
        overall_satisfaction = omnichannel_data[satisfaction_column].mean()
        metrics.append(['Overall Omnichannel Satisfaction', f"{overall_satisfaction:.1f}/10"])
        total_interactions = len(omnichannel_data)
        metrics.append(['Total Interactions', total_interactions])
        unique_channels = omnichannel_data[channel_column].nunique()
        metrics.append(['Channels Analyzed', unique_channels])
        high_satisfaction_channels = len(omnichannel_data[omnichannel_data[satisfaction_column] > 8])
        metrics.append(['High Satisfaction Interactions (>8)', high_satisfaction_channels])
        channel_satisfaction = omnichannel_data.groupby(channel_column)[satisfaction_column].agg(['mean', 'count']).reset_index()
        channel_satisfaction.columns = ['Channel', 'Average Satisfaction', 'Interaction Count']
        channel_satisfaction = channel_satisfaction.sort_values('Average Satisfaction', ascending=False)
        if not channel_satisfaction.empty:
            top_channel = channel_satisfaction.iloc[0]
            metrics.append(['Top Performing Channel', f"{top_channel['Channel']} ({top_channel['Average Satisfaction']:.1f}/10)"])
            satisfaction_std = channel_satisfaction['Average Satisfaction'].std()
            metrics.append(['Channel Consistency', f"±{satisfaction_std:.1f} points"])
        if len(channel_satisfaction) > 1:
            satisfaction_range = channel_satisfaction['Average Satisfaction'].max() - channel_satisfaction['Average Satisfaction'].min()
            if satisfaction_range <= 2:
                consistency_status = "High"
            elif satisfaction_range <= 4:
                consistency_status = "Medium"
            else:
                consistency_status = "Low"
            metrics.append(['Cross-Channel Consistency', consistency_status])
        if 'start_time' in omnichannel_data.columns:
            omnichannel_data['start_time'] = pd.to_datetime(omnichannel_data['start_time'], errors='coerce')
            omnichannel_data = omnichannel_data.dropna(subset=['start_time'])
            if not omnichannel_data.empty:
                omnichannel_data['hour'] = omnichannel_data['start_time'].dt.hour
                hourly_satisfaction = omnichannel_data.groupby('hour')[satisfaction_column].mean()
                if not hourly_satisfaction.empty:
                    peak_hour = hourly_satisfaction.idxmax()
                    peak_satisfaction = hourly_satisfaction.max()
                    metrics.append(['Peak Satisfaction Hour', f"{peak_hour}:00 ({peak_satisfaction:.1f}/10)"])
        omnichannel_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Omnichannel experience analysis completed. {unique_channels} channels analyzed across {total_interactions} interactions."
        return omnichannel_summary, message
    except Exception as e:
        return pd.DataFrame(), f"Error calculating omnichannel experience: {str(e)}"


def analyze_customer_interactions(interactions_df, tickets_df):
    """Analyze customer interaction patterns and trends"""
    try:
        if interactions_df.empty:
            return pd.DataFrame(), "No interaction data available for analysis"
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for analysis"
        required_interaction_cols = ['channel', 'duration_minutes', 'satisfaction_score']
        required_ticket_cols = ['ticket_id', 'priority', 'status']
        missing_interaction_cols = [col for col in required_interaction_cols if col not in interactions_df.columns]
        missing_ticket_cols = [col for col in required_ticket_cols if col not in tickets_df.columns]
        if missing_interaction_cols or missing_ticket_cols:
            return pd.DataFrame(), f"Missing required columns: Interactions: {missing_interaction_cols}, Tickets: {missing_ticket_cols}"
        metrics = []
        # Handle column conflicts when merging (both DataFrames have 'channel' column)
        interaction_data = interactions_df.merge(tickets_df, on='ticket_id', how='inner', suffixes=('_interaction', '_ticket'))
        if interaction_data.empty:
            return pd.DataFrame(), "No matching data between interactions and tickets for analysis"
        
        # Use the interaction channel column (from interactions_df)
        channel_column = 'channel_interaction' if 'channel_interaction' in interaction_data.columns else 'channel'
        
        total_interactions = len(interaction_data)
        metrics.append(['Total Interactions', total_interactions])
        unique_channels = interaction_data[channel_column].nunique()
        metrics.append(['Channels Used', unique_channels])
        avg_duration = interaction_data['duration_minutes'].mean()
        metrics.append(['Average Duration', f"{avg_duration:.1f} minutes"])
        avg_satisfaction = interaction_data['satisfaction_score'].mean()
        metrics.append(['Average Satisfaction', f"{avg_satisfaction:.1f}/10"])
        high_priority_interactions = len(interaction_data[interaction_data['priority'] == 'High'])
        metrics.append(['High Priority Interactions', high_priority_interactions])
        resolved_interactions = len(interaction_data[interaction_data['status'] == 'Resolved'])
        metrics.append(['Resolved Interactions', resolved_interactions])
        channel_performance = interaction_data.groupby(channel_column).agg({
            'duration_minutes': 'mean',
            'satisfaction_score': 'mean',
            'ticket_id': 'count'
        }).reset_index()
        channel_performance.columns = ['Channel', 'Avg Duration (min)', 'Avg Satisfaction', 'Interaction Count']
        channel_performance = channel_performance.sort_values('Avg Satisfaction', ascending=False)
        if not channel_performance.empty:
            top_channel = channel_performance.iloc[0]
            metrics.append(['Top Channel', f"{top_channel['Channel']} ({top_channel['Avg Satisfaction']:.1f}/10)"])
        priority_analysis = interaction_data.groupby('priority').agg({
            'duration_minutes': 'mean',
            'satisfaction_score': 'mean',
            'ticket_id': 'count'
        }).reset_index()
        priority_analysis.columns = ['Priority', 'Avg Duration (min)', 'Avg Satisfaction', 'Interaction Count']
        priority_analysis = priority_analysis.sort_values('Avg Satisfaction', ascending=False)
        if not priority_analysis.empty:
            top_priority = priority_analysis.iloc[0]
            metrics.append(['Best Performing Priority', f"{top_priority['Priority']} ({top_priority['Avg Satisfaction']:.1f}/10)"])
        interaction_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Customer interaction analysis completed. {total_interactions} interactions analyzed across {unique_channels} channels."
        return interaction_summary, message
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing customer interactions: {str(e)}"


def predict_customer_churn(customers_df, tickets_df, feedback_df):
    """Predict customer churn based on historical data"""
    try:
        if customers_df.empty:
            return pd.DataFrame(), "No customer data available for churn prediction"
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for churn prediction"
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for churn prediction"
        required_customer_cols = ['customer_id', 'status', 'customer_segment']
        required_ticket_cols = ['customer_id', 'created_date', 'status', 'priority']
        required_feedback_cols = ['customer_id', 'nps_score', 'customer_effort_score']
        missing_customer_cols = [col for col in required_customer_cols if col not in customers_df.columns]
        missing_ticket_cols = [col for col in required_ticket_cols if col not in tickets_df.columns]
        missing_feedback_cols = [col for col in required_feedback_cols if col not in feedback_df.columns]
        if missing_customer_cols or missing_ticket_cols or missing_feedback_cols:
            return pd.DataFrame(), f"Missing required columns: Customer: {missing_customer_cols}, Tickets: {missing_ticket_cols}, Feedback: {missing_feedback_cols}"
        metrics = []
        # Handle column conflicts when merging (both DataFrames have 'status' column)
        churn_data = customers_df.merge(tickets_df, on='customer_id', how='left', suffixes=('_customer', '_ticket'))
        churn_data = churn_data.merge(feedback_df, on='customer_id', how='left', suffixes=('', '_feedback'))
        if churn_data.empty:
            return pd.DataFrame(), "No matching data between customers, tickets, and feedback for churn prediction"
        total_customers = len(customers_df)
        metrics.append(['Total Customers', total_customers])
        churned_customers = len(customers_df[customers_df['status'] == 'Churned'])
        churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
        metrics.append(['Current Churn Rate', f"{churn_rate:.1f}%"])
        high_risk_customers = len(churn_data[
            (churn_data['nps_score'] < 6) & 
            (churn_data['customer_effort_score'] > 4)
        ])
        metrics.append(['High Risk Customers', high_risk_customers])
        low_risk_customers = len(churn_data[
            (churn_data['nps_score'] >= 8) & 
            (churn_data['customer_effort_score'] <= 3)
        ])
        metrics.append(['Low Risk Customers', low_risk_customers])
        if 'customer_segment' in churn_data.columns:
            # Use the customer status column (from customers_df)
            customer_status_column = 'status_customer' if 'status_customer' in churn_data.columns else 'status'
            segment_churn = churn_data.groupby('customer_segment')[customer_status_column].apply(
                lambda x: (x == 'Churned').sum() / len(x) * 100
            ).reset_index()
            segment_churn.columns = ['Customer Segment', 'Churn Rate (%)']
            segment_churn = segment_churn.sort_values('Churn Rate (%)', ascending=False)
            if not segment_churn.empty:
                highest_churn_segment = segment_churn.iloc[0]
                metrics.append(['Highest Churn Segment', f"{highest_churn_segment['Customer Segment']} ({highest_churn_segment['Churn Rate (%)']:.1f}%)"])
        if 'priority' in churn_data.columns:
            # Use the customer status column (from customers_df)
            customer_status_column = 'status_customer' if 'status_customer' in churn_data.columns else 'status'
            priority_churn = churn_data.groupby('priority')[customer_status_column].apply(
                lambda x: (x == 'Churned').sum() / len(x) * 100
            ).reset_index()
            priority_churn.columns = ['Ticket Priority', 'Churn Rate (%)']
            priority_churn = priority_churn.sort_values('Churn Rate (%)', ascending=False)
            if not priority_churn.empty:
                highest_churn_priority = priority_churn.iloc[0]
                metrics.append(['Highest Churn Priority', f"{highest_churn_priority['Ticket Priority']} ({highest_churn_priority['Churn Rate (%)']:.1f}%)"])
        predicted_churn_rate = min(100, churn_rate * 1.2)
        metrics.append(['Predicted Churn Rate (Next Period)', f"{predicted_churn_rate:.1f}%"])
        churn_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Customer churn prediction completed. {total_customers} customers analyzed with {churn_rate:.1f}% current churn rate."
        return churn_summary, message
    except Exception as e:
        return pd.DataFrame(), f"Error predicting customer churn: {str(e)}"


def analyze_trends_and_patterns(tickets_df, feedback_df):
    """Analyze trends and patterns in ticket data and feedback"""
    try:
        if tickets_df.empty:
            return pd.DataFrame(), "No ticket data available for trend analysis"
        if feedback_df.empty:
            return pd.DataFrame(), "No feedback data available for trend analysis"
        required_ticket_cols = ['created_date', 'status', 'priority', 'ticket_type']
        required_feedback_cols = ['ticket_id', 'nps_score', 'customer_effort_score']
        missing_ticket_cols = [col for col in required_ticket_cols if col not in tickets_df.columns]
        missing_feedback_cols = [col for col in required_feedback_cols if col not in feedback_df.columns]
        if missing_ticket_cols or missing_feedback_cols:
            return pd.DataFrame(), f"Missing required columns: Tickets: {missing_ticket_cols}, Feedback: {missing_feedback_cols}"
        metrics = []
        trend_data = tickets_df.merge(feedback_df, on='ticket_id', how='inner')
        if trend_data.empty:
            return pd.DataFrame(), "No matching data between tickets and feedback for trend analysis"
        total_tickets = len(trend_data)
        metrics.append(['Total Tickets Analyzed', total_tickets])
        if 'created_date' in trend_data.columns:
            trend_data['created_date'] = pd.to_datetime(trend_data['created_date'], errors='coerce')
            trend_data = trend_data.dropna(subset=['created_date'])
            if not trend_data.empty:
                trend_data['month'] = trend_data['created_date'].dt.to_period('M')
                monthly_trends = trend_data.groupby('month').agg({
                    'ticket_id': 'count',
                    'nps_score': 'mean',
                    'customer_effort_score': 'mean'
                }).reset_index()
                monthly_trends.columns = ['Month', 'Ticket Count', 'Avg NPS', 'Avg CES']
                monthly_trends = monthly_trends.sort_values('Month')
                if len(monthly_trends) > 1:
                    ticket_growth = ((monthly_trends.iloc[-1]['Ticket Count'] - monthly_trends.iloc[0]['Ticket Count']) / 
                                   monthly_trends.iloc[0]['Ticket Count'] * 100)
                    metrics.append(['Ticket Volume Growth', f"{ticket_growth:.1f}%"])
                    nps_trend = monthly_trends.iloc[-1]['Avg NPS'] - monthly_trends.iloc[0]['Avg NPS']
                    metrics.append(['NPS Trend', f"{nps_trend:+.1f} points"])
                    ces_trend = monthly_trends.iloc[-1]['Avg CES'] - monthly_trends.iloc[0]['Avg CES']
                    metrics.append(['CES Trend', f"{ces_trend:+.1f} points"])
        if 'priority' in trend_data.columns:
            priority_distribution = trend_data['priority'].value_counts()
            top_priority = priority_distribution.index[0]
            top_priority_count = priority_distribution.iloc[0]
            metrics.append(['Most Common Priority', f"{top_priority} ({top_priority_count} tickets)"])
        if 'ticket_type' in trend_data.columns:
            type_distribution = trend_data['ticket_type'].value_counts()
            top_type = type_distribution.index[0]
            top_type_count = type_distribution.iloc[0]
            metrics.append(['Most Common Ticket Type', f"{top_type} ({top_type_count} tickets)"])
        if 'status' in trend_data.columns:
            status_distribution = trend_data['status'].value_counts()
            resolved_tickets = status_distribution.get('Resolved', 0)
            resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['Resolution Rate', f"{resolution_rate:.1f}%"])
        if 'nps_score' in trend_data.columns:
            high_satisfaction = len(trend_data[trend_data['nps_score'] >= 8])
            satisfaction_rate = (high_satisfaction / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['High Satisfaction Rate', f"{satisfaction_rate:.1f}%"])
        if 'customer_effort_score' in trend_data.columns:
            low_effort = len(trend_data[trend_data['customer_effort_score'] <= 3])
            low_effort_rate = (low_effort / total_tickets * 100) if total_tickets > 0 else 0
            metrics.append(['Low Effort Rate', f"{low_effort_rate:.1f}%"])
        trends_summary = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        message = f"Trends and patterns analysis completed. {total_tickets} tickets analyzed for patterns and trends."
        return trends_summary, message
    except Exception as e:
        return pd.DataFrame(), f"Error analyzing trends and patterns: {str(e)}"

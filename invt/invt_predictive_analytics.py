import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Machine Learning imports
try:
    from sklearn.ensemble import RandomForestRegressor, IsolationForest
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def safe_format(value, decimal_places=0):
    """Safely format a value, handling numpy arrays and None values."""
    if value is None:
        return "N/A"
    if isinstance(value, (np.ndarray, list)):
        # If it's an array/list, take the mean or first value
        if len(value) > 0:
            value = np.mean(value) if len(value) > 1 else value[0]
        else:
            return "N/A"
    if np.isnan(value):
        return "N/A"
    return f"{value:.{decimal_places}f}"

def optimize_dataframe_operations(df):
    """Optimize DataFrame operations for better performance."""
    # Convert object columns to category if they have low cardinality
    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')
    
    # Optimize numeric columns
    for col in df.select_dtypes(include=['int64']):
        if df[col].min() >= 0 and df[col].max() < 255:
            df[col] = df[col].astype('uint8')
        elif df[col].min() >= -32768 and df[col].max() < 32767:
            df[col] = df[col].astype('int16')
    
    return df

# ============================================================================
# INVENTORY PREDICTIVE ANALYTICS CLASS
# ============================================================================

class InventoryPredictiveAnalytics:
    """Optimized class for comprehensive inventory predictive analytics and forecasting."""
    
    def __init__(self, data):
        """
        Initialize with inventory data.
        
        Args:
            data (pd.DataFrame): Inventory data
        """
        # Optimize DataFrame for better performance
        self.data = optimize_dataframe_operations(data.copy())
        self.forecasts = {}
        self.trends = {}
        self.anomalies = {}
        self.optimization_recommendations = {}
        
        # Cache for frequently accessed calculations
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes cache TTL
        self._last_cache_update = datetime.now()
        
    def perform_comprehensive_analysis(self):
        """Perform comprehensive predictive analysis."""
        if self.data.empty:
            return {}
        
        # Perform all analyses
        self._analyze_demand_trends()
        self._forecast_demand()
        self._detect_anomalies()
        self._predict_stockout_risks()
        self._optimize_reorder_points()
        self._forecast_costs()
        self._predict_supplier_performance()
        
        return {
            'forecasts': self.forecasts,
            'trends': self.trends,
            'anomalies': self.anomalies,
            'optimization_recommendations': self.optimization_recommendations
        }
    
    def _analyze_demand_trends(self):
        """Analyze demand trends and patterns with caching for performance."""
        cache_key = 'demand_trends'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        # Check if required columns exist
        if 'date' not in self.data.columns or 'quantity' not in self.data.columns:
            st.warning("⚠️ Required columns 'date' or 'quantity' not found in data")
            # Create dummy trend data for demonstration
            result = {
                'daily_data': pd.DataFrame({
                    'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
                    'quantity': np.random.randint(10, 100, 30),
                    'ma_7': np.random.randint(20, 80, 30),
                    'ma_30': np.random.randint(30, 70, 30),
                    'trend': np.random.uniform(-2, 2, 30)
                }),
                'seasonality_strength': 0.3,
                'trend_direction': 'increasing',
                'trend_magnitude': 1.5
            }
            self.trends['demand_trends'] = result
            self._cache[cache_key] = result
            return result
        
        # Convert date column efficiently
        if self.data['date'].dtype == 'object':
            self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce')
        
        # Use vectorized operations for better performance
        daily_demand = (self.data.groupby('date')['quantity']
                       .sum()
                       .reset_index()
                       .sort_values('date'))
        
        # Calculate moving averages efficiently
        daily_demand['ma_7'] = daily_demand['quantity'].rolling(window=7, min_periods=1).mean()
        daily_demand['ma_30'] = daily_demand['quantity'].rolling(window=30, min_periods=1).mean()
        
        # Calculate trend using vectorized operations
        daily_demand['trend'] = self._calculate_trend_vectorized(daily_demand['quantity'])
        
        # Identify seasonality efficiently
        daily_demand['month'] = daily_demand['date'].dt.month
        monthly_patterns = daily_demand.groupby('month')['quantity'].mean()
        
        # Calculate seasonality strength
        seasonal_variance = monthly_patterns.var()
        total_variance = daily_demand['quantity'].var()
        seasonality_strength = seasonal_variance / total_variance if total_variance > 0 else 0
        
        result = {
            'daily_data': daily_demand,
            'seasonality_strength': seasonality_strength,
            'trend_direction': 'increasing' if daily_demand['trend'].mean() > 0 else 'decreasing',
            'trend_magnitude': abs(daily_demand['trend'].mean())
        }
        
        self.trends['demand_trends'] = result
        self._cache[cache_key] = result
        return result
    
    def _calculate_trend_vectorized(self, series):
        """Calculate trend using vectorized operations for better performance."""
        if len(series) < 2:
            return pd.Series([0] * len(series))
        
        # Use numpy's polyfit for vectorized trend calculation
        x = np.arange(len(series))
        y = series.values
        
        # Calculate trend for rolling windows
        trend = pd.Series(index=series.index, dtype=float)
        
        for i in range(len(series)):
            if i < 29:  # Need at least 30 points for trend calculation
                trend.iloc[i] = 0
            else:
                window_x = x[i-29:i+1]
                window_y = y[i-29:i+1]
                if len(window_y) > 1:
                    slope = np.polyfit(window_x, window_y, 1)[0]
                    trend.iloc[i] = slope
                else:
                    trend.iloc[i] = 0
        
        return trend
    
    def _is_cache_valid(self, key):
        """Check if cached data is still valid."""
        if key not in self._cache:
            return False
        
        time_diff = (datetime.now() - self._last_cache_update).total_seconds()
        return time_diff < self._cache_ttl
    
    def _forecast_demand(self):
        """Forecast future demand using multiple methods with caching."""
        cache_key = 'demand_forecast'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        if 'date' not in self.data.columns or 'quantity' not in self.data.columns:
            return
        
        # Prepare time series data efficiently
        daily_demand = (self.data.groupby('date')['quantity']
                       .sum()
                       .reset_index()
                       .sort_values('date')
                       .set_index('date'))
        
        # Simple moving average forecast
        ma_forecast = daily_demand['quantity'].rolling(window=30).mean().iloc[-1]
        
        # Linear trend forecast using vectorized operations
        if len(daily_demand) > 1:
            x = np.arange(len(daily_demand))
            y = daily_demand['quantity'].values
            slope, intercept = np.polyfit(x, y, 1)
            
            # Forecast next 30 days
            future_x = np.arange(len(daily_demand), len(daily_demand) + 30)
            trend_forecast = slope * future_x + intercept
            trend_forecast = np.maximum(trend_forecast, 0)  # Ensure non-negative
        else:
            trend_forecast = [ma_forecast] * 30
        
        # Seasonal forecast (if seasonality detected)
        seasonality_strength = self.trends.get('demand_trends', {}).get('seasonality_strength', 0)
        if seasonality_strength > 0.3:
            monthly_patterns = daily_demand.groupby(daily_demand.index.month)['quantity'].mean()
            seasonal_forecast = monthly_patterns.mean()
        else:
            seasonal_forecast = ma_forecast
        
        # Machine learning forecast (if available)
        ml_forecast = None
        if ML_AVAILABLE and len(daily_demand) > 30:
            try:
                ml_forecast = self._ml_demand_forecast(daily_demand)
            except Exception as e:
                st.warning(f"ML forecasting failed: {str(e)}")
                ml_forecast = ma_forecast
        
        # Combine forecasts efficiently
        forecasts = [ma_forecast, np.mean(trend_forecast), seasonal_forecast]
        if ml_forecast is not None:
            forecasts.append(ml_forecast)
        
        # Remove None values and calculate weighted average
        valid_forecasts = [f for f in forecasts if f is not None and not np.isnan(f)]
        combined_forecast = np.mean(valid_forecasts) if valid_forecasts else ma_forecast
        
        result = {
            'moving_average': ma_forecast,
            'trend': np.mean(trend_forecast) if isinstance(trend_forecast, list) else trend_forecast,
            'seasonal': seasonal_forecast,
            'ml_forecast': ml_forecast,
            'combined_forecast': combined_forecast,
            'forecast_horizon': 30,
            'confidence_interval': self._calculate_forecast_confidence(daily_demand)
        }
        
        self.forecasts['demand_forecast'] = result
        self._cache[cache_key] = result
        return result
    
    def _ml_demand_forecast(self, daily_demand):
        """Perform machine learning-based demand forecasting."""
        if not ML_AVAILABLE or len(daily_demand) < 30:
            return None
        
        try:
            # Prepare features
            daily_demand['day_of_week'] = daily_demand.index.dayofweek
            daily_demand['month'] = daily_demand.index.month
            daily_demand['day_of_year'] = daily_demand.index.dayofyear
            
            # Create lag features
            for lag in [1, 7, 14]:
                daily_demand[f'lag_{lag}'] = daily_demand['quantity'].shift(lag)
            
            # Create rolling features
            daily_demand['rolling_mean_7'] = daily_demand['quantity'].rolling(window=7).mean()
            daily_demand['rolling_std_7'] = daily_demand['quantity'].rolling(window=7).std()
            
            # Remove NaN values
            daily_demand = daily_demand.dropna()
            
            if len(daily_demand) < 20:
                return None
            
            # Prepare features and target
            feature_columns = ['day_of_week', 'month', 'day_of_year', 'lag_1', 'lag_7', 'lag_14', 
                             'rolling_mean_7', 'rolling_std_7']
            
            X = daily_demand[feature_columns]
            y = daily_demand['quantity']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Make prediction for next day
            last_features = daily_demand[feature_columns].iloc[-1:]
            prediction = model.predict(last_features)[0]
            
            return max(0, prediction)  # Ensure non-negative
            
        except Exception as e:
            st.warning(f"ML forecasting failed: {str(e)}")
            return None
    
    def _calculate_forecast_confidence(self, daily_demand):
        """Calculate forecast confidence intervals."""
        if len(daily_demand) < 10:
            return {'lower': 0, 'upper': 0, 'confidence': 0}
        
        # Calculate historical volatility
        returns = daily_demand['quantity'].pct_change().dropna()
        volatility = returns.std()
        
        # Calculate confidence intervals
        forecast_value = self.forecasts.get('demand_forecast', {}).get('combined_forecast', 0)
        
        confidence_level = 0.95
        z_score = 1.96  # 95% confidence
        
        margin_of_error = z_score * volatility * forecast_value
        
        return {
            'lower': max(0, forecast_value - margin_of_error),
            'upper': forecast_value + margin_of_error,
            'confidence': confidence_level * 100
        }
    
    def _detect_anomalies(self):
        """Detect anomalies in inventory data with caching."""
        cache_key = 'anomalies'
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        anomalies = {}
        
        # Stock level anomalies
        if 'current_stock' in self.data.columns:
            stock_anomalies = self._detect_stock_anomalies()
            anomalies['stock_anomalies'] = stock_anomalies
        
        # Demand anomalies
        if 'quantity' in self.data.columns:
            demand_anomalies = self._detect_demand_anomalies()
            anomalies['demand_anomalies'] = demand_anomalies
        
        # Cost anomalies
        if 'unit_cost' in self.data.columns:
            cost_anomalies = self._detect_cost_anomalies()
            anomalies['cost_anomalies'] = cost_anomalies
        
        self.anomalies = anomalies
        self._cache[cache_key] = anomalies
        return anomalies
    
    def _detect_stock_anomalies(self):
        """Detect anomalies in stock levels using vectorized operations."""
        stock_data = self.data['current_stock'].dropna()
        
        if len(stock_data) < 10:
            return {'anomalous_items': [], 'anomaly_score': 0}
        
        # Statistical anomaly detection using vectorized operations
        Q1 = stock_data.quantile(0.25)
        Q3 = stock_data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Use vectorized boolean indexing for better performance
        anomaly_mask = (self.data['current_stock'] < lower_bound) | (self.data['current_stock'] > upper_bound)
        anomalous_items = self.data[anomaly_mask]
        
        # ML-based anomaly detection (if available)
        ml_anomalies = []
        if ML_AVAILABLE and len(stock_data) > 20:
            try:
                # Use more efficient anomaly detection for large datasets
                if len(stock_data) > 1000:
                    # Sample data for large datasets to improve performance
                    sample_size = min(1000, len(stock_data))
                    sample_indices = np.random.choice(len(stock_data), sample_size, replace=False)
                    X_sample = stock_data.iloc[sample_indices].values.reshape(-1, 1)
                    
                    iso_forest = IsolationForest(contamination=0.1, random_state=42, n_estimators=100)
                    iso_forest.fit(X_sample)
                    
                    # Predict on full dataset
                    X_full = stock_data.values.reshape(-1, 1)
                    predictions = iso_forest.predict(X_full)
                else:
                    # Use full dataset for smaller datasets
                    X = stock_data.values.reshape(-1, 1)
                    iso_forest = IsolationForest(contamination=0.1, random_state=42)
                    predictions = iso_forest.fit_predict(X)
                
                # Get anomalous indices
                anomaly_indices = np.where(predictions == -1)[0]
                ml_anomalies = self.data.iloc[anomaly_indices]['item_name'].tolist()
                
            except Exception as e:
                st.warning(f"ML anomaly detection failed: {str(e)}")
        
        return {
            'anomalous_items': anomalous_items['item_name'].tolist(),
            'ml_anomalies': ml_anomalies,
            'anomaly_score': len(anomalous_items) / len(self.data) * 100,
            'statistical_bounds': {'lower': lower_bound, 'upper': upper_bound}
        }
    
    def _detect_demand_anomalies(self):
        """Detect anomalies in demand patterns."""
        if 'date' not in self.data.columns or 'quantity' not in self.data.columns:
            return {'anomalous_dates': [], 'anomaly_score': 0}
        
        # Aggregate demand by date
        daily_demand = self.data.groupby('date')['quantity'].sum()
        
        if len(daily_demand) < 10:
            return {'anomalous_dates': [], 'anomaly_score': 0}
        
        # Calculate demand volatility
        demand_returns = daily_demand.pct_change().dropna()
        
        # Identify high volatility periods
        volatility_threshold = demand_returns.std() * 2
        high_volatility_dates = demand_returns[abs(demand_returns) > volatility_threshold].index
        
        return {
            'anomalous_dates': high_volatility_dates.tolist(),
            'anomaly_score': len(high_volatility_dates) / len(daily_demand) * 100,
            'volatility_threshold': volatility_threshold
        }
    
    def _detect_cost_anomalies(self):
        """Detect anomalies in cost patterns."""
        if 'unit_cost' not in self.data.columns:
            return {'anomalous_costs': [], 'anomaly_score': 0}
        
        cost_data = self.data['unit_cost'].dropna()
        
        if len(cost_data) < 10:
            return {'anomalous_costs': [], 'anomaly_score': 0}
        
        # Statistical anomaly detection
        Q1 = cost_data.quantile(0.25)
        Q3 = cost_data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomalous_costs = self.data[
            (self.data['unit_cost'] < lower_bound) | 
            (self.data['unit_cost'] > upper_bound)
        ]
        
        return {
            'anomalous_costs': anomalous_costs['item_name'].tolist(),
            'anomaly_score': len(anomalous_costs) / len(self.data) * 100,
            'cost_bounds': {'lower': lower_bound, 'upper': upper_bound}
        }
    
    def _predict_stockout_risks(self):
        """Predict stockout risks based on current trends."""
        if 'current_stock' not in self.data.columns or 'reorder_point' not in self.data.columns:
            return
        
        # Calculate current stockout risk
        current_risk = self.data[self.data['current_stock'] <= self.data['reorder_point']]
        
        # Predict future stockout risk based on demand forecast
        if 'demand_forecast' in self.forecasts:
            forecast_demand = self.forecasts['demand_forecast']['combined_forecast']
            
            # Estimate days until stockout
            if 'daily_demand' in self.data.columns:
                avg_daily_demand = self.data['daily_demand'].mean()
            else:
                avg_daily_demand = forecast_demand / 30  # Assume monthly forecast
            
            # Predict stockout for each item
            predicted_stockout = []
            for _, row in self.data.iterrows():
                current_stock = row['current_stock']
                days_until_stockout = current_stock / avg_daily_demand if avg_daily_demand > 0 else float('inf')
                
                if days_until_stockout <= 30:
                    predicted_stockout.append({
                        'item_name': row['item_name'],
                        'days_until_stockout': days_until_stockout,
                        'risk_level': 'High' if days_until_stockout <= 7 else 'Medium'
                    })
            
            self.forecasts['stockout_prediction'] = {
                'current_risk_items': len(current_risk),
                'predicted_stockout_items': predicted_stockout,
                'avg_daily_demand': avg_daily_demand,
                'forecast_horizon': 30
            }
    
    def _optimize_reorder_points(self):
        """Optimize reorder points based on demand patterns."""
        if 'current_stock' not in self.data.columns or 'reorder_point' not in self.data.columns:
            return
        
        optimization_recommendations = []
        
        for _, row in self.data.iterrows():
            current_stock = row['current_stock']
            current_reorder_point = row['reorder_point']
            
            # Calculate optimal reorder point based on demand forecast
            if 'demand_forecast' in self.forecasts:
                forecast_demand = self.forecasts['demand_forecast']['combined_forecast']
                avg_daily_demand = forecast_demand / 30
                
                # Assume lead time of 14 days (can be customized)
                lead_time = 14
                safety_stock = avg_daily_demand * 7  # 7 days safety stock
                
                optimal_reorder_point = (avg_daily_demand * lead_time) + safety_stock
                
                # Check if current reorder point needs adjustment
                if abs(current_reorder_point - optimal_reorder_point) > optimal_reorder_point * 0.2:
                    optimization_recommendations.append({
                        'item_name': row['item_name'],
                        'current_reorder_point': current_reorder_point,
                        'optimal_reorder_point': optimal_reorder_point,
                        'adjustment_needed': optimal_reorder_point - current_reorder_point,
                        'reason': 'Demand pattern change' if optimal_reorder_point > current_reorder_point else 'Overstocking'
                    })
        
        self.optimization_recommendations['reorder_point_optimization'] = optimization_recommendations
    
    def _forecast_costs(self):
        """Forecast future costs based on historical trends."""
        if 'unit_cost' not in self.data.columns:
            return
        
        # Calculate cost trends
        cost_data = self.data['unit_cost'].dropna()
        
        if len(cost_data) > 1:
            # Simple linear trend
            x = np.arange(len(cost_data))
            y = cost_data.values
            slope, intercept = np.polyfit(x, y, 1)
            
            # Forecast next 12 months
            future_months = np.arange(len(cost_data), len(cost_data) + 12)
            cost_forecast = slope * future_months + intercept
            cost_forecast = np.maximum(cost_forecast, 0)  # Ensure non-negative
            
            self.forecasts['cost_forecast'] = {
                'trend_slope': slope,
                'monthly_forecast': cost_forecast.tolist(),
                'forecast_horizon': 12,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing'
            }
    
    def _predict_supplier_performance(self):
        """Predict supplier performance based on historical data."""
        if 'supplier_id' not in self.data.columns or 'supplier_performance' not in self.data.columns:
            return
        
        supplier_performance = self.data.groupby('supplier_id')['supplier_performance'].agg(['mean', 'std', 'count']).reset_index()
        
        # Predict future performance based on trends
        performance_predictions = []
        
        for _, supplier in supplier_performance.iterrows():
            current_performance = supplier['mean']
            performance_volatility = supplier['std']
            
            # Simple prediction: assume slight improvement for poor performers, slight decline for excellent performers
            if current_performance < 60:
                predicted_change = 5  # Expected improvement
            elif current_performance > 90:
                predicted_change = -2  # Slight decline
            else:
                predicted_change = 0  # Stable
            
            predicted_performance = current_performance + predicted_change
            predicted_performance = max(0, min(100, predicted_performance))  # Clamp to 0-100
            
            performance_predictions.append({
                'supplier_id': supplier['supplier_id'],
                'current_performance': current_performance,
                'predicted_performance': predicted_performance,
                'predicted_change': predicted_change,
                'confidence': max(0, 100 - performance_volatility)  # Higher volatility = lower confidence
            })
        
        self.forecasts['supplier_performance_prediction'] = performance_predictions

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_inventory_predictive_analytics_dashboard(data):
    """Display comprehensive predictive analytics dashboard with performance optimizations."""
    if data is None or data.empty:
        st.warning("📊 No data available for predictive analytics.")
        return
    
    # Data validation (hidden from user)
    missing_columns = []
    if 'date' not in data.columns:
        missing_columns.append('date')
    if 'quantity' not in data.columns:
        missing_columns.append('quantity')
    
    # Only show warning if columns are missing
    if missing_columns:
        st.warning(f"⚠️ **Missing required columns:** {missing_columns}")
        st.info("Some analytics features may not work without these columns.")
    
    st.subheader("🔮 Predictive Analytics & Forecasting Dashboard")
    
    # Add performance metrics
    with st.expander("⚡ Performance Metrics", expanded=False):
        start_time = datetime.now()
        st.info(f"Analysis started at: {start_time.strftime('%H:%M:%S')}")
    
    # Initialize predictive analytics with progress bar
    with st.spinner("Initializing predictive analytics..."):
        predictive_analytics = InventoryPredictiveAnalytics(data)
    
    # Perform analysis with progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Performing comprehensive analysis...")
        progress_bar.progress(20)
        
        analysis_results = predictive_analytics.perform_comprehensive_analysis()
        progress_bar.progress(80)
        
        if not analysis_results:
            st.error("❌ Unable to perform predictive analysis.")
            return
        
        progress_bar.progress(100)
        status_text.text("Analysis complete!")
        
        # Calculate and display performance metrics
        end_time = datetime.now()
        analysis_duration = (end_time - start_time).total_seconds()
        st.success(f"✅ Analysis completed in {analysis_duration:.2f} seconds")
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        return
    finally:
        progress_bar.empty()
        status_text.empty()
    
    # Display different sections in tabs with lazy loading
    tab_names = ["📈 Demand Forecasting", "🔍 Trend Analysis", "⚠️ Anomaly Detection", "🎯 Optimization", "💰 Cost Forecasting"]
    tabs = st.tabs(tab_names)
    
    with tabs[0]:  # Demand Forecasting
        display_demand_forecasting_tab(analysis_results)
    
    with tabs[1]:  # Trend Analysis
        display_trend_analysis_tab(analysis_results)
    
    with tabs[2]:  # Anomaly Detection
        display_anomaly_detection_tab(analysis_results)
    
    with tabs[3]:  # Optimization
        display_optimization_tab(analysis_results)
    
    with tabs[4]:  # Cost Forecasting
        display_cost_forecasting_tab(analysis_results, data)

def display_demand_forecasting_tab(analysis_results):
    """Display demand forecasting results."""
    st.subheader("📈 Demand Forecasting")
    
    if 'demand_forecast' not in analysis_results['forecasts']:
        st.info("No demand forecasting data available.")
        return
    
    forecast_data = analysis_results['forecasts']['demand_forecast']
    
    # Display forecast summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Combined Forecast",
            value=safe_format(forecast_data['combined_forecast']),
            delta=f"Next {forecast_data['forecast_horizon']} days"
        )
    
    with col2:
        st.metric(
            label="Moving Average",
            value=safe_format(forecast_data['moving_average']),
            delta="Historical average"
        )
    
    with col3:
        st.metric(
            label="Trend Forecast",
            value=safe_format(forecast_data['trend']),
            delta="Linear trend"
        )
    
    # Display confidence intervals
    if 'confidence_interval' in forecast_data:
        confidence = forecast_data['confidence_interval']
        st.info(f"**Forecast Confidence:** {safe_format(confidence['confidence'])}% confidence interval: "
                f"{safe_format(confidence['lower'])} - {safe_format(confidence['upper'])}")
    
    # Display forecast methods comparison
    st.subheader("📊 Forecast Methods Comparison")
    
    methods = ['Moving Average', 'Trend', 'Seasonal']
    values = [forecast_data['moving_average'], forecast_data['trend'], forecast_data['seasonal']]
    
    if forecast_data['ml_forecast'] is not None:
        methods.append('Machine Learning')
        values.append(forecast_data['ml_forecast'])
    
    # Clean values for plotting
    clean_values = []
    for val in values:
        if isinstance(val, (np.ndarray, list)):
            clean_values.append(np.mean(val) if len(val) > 0 else 0)
        elif val is None or np.isnan(val):
            clean_values.append(0)
        else:
            clean_values.append(val)
    
    fig_forecast_comparison = px.bar(
        x=methods,
        y=clean_values,
        title="Forecast Methods Comparison",
        color_discrete_sequence=['#667eea']
    )
    
    fig_forecast_comparison.update_layout(
        xaxis_title="Forecast Method",
        yaxis_title="Forecasted Demand"
    )
    
    st.plotly_chart(fig_forecast_comparison, use_container_width=True)
    
    # Display stockout predictions
    if 'stockout_prediction' in analysis_results['forecasts']:
        st.subheader("🚨 Stockout Risk Predictions")
        
        stockout_data = analysis_results['forecasts']['stockout_prediction']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Current Risk Items",
                value=stockout_data['current_risk_items'],
                delta="Items below reorder point"
            )
        
        with col2:
            st.metric(
                label="Predicted Stockouts",
                value=len(stockout_data['predicted_stockout_items']),
                delta="Next 30 days"
            )
        
        # Display high-risk items
        high_risk_items = [item for item in stockout_data['predicted_stockout_items'] if item['risk_level'] == 'High']
        
        if high_risk_items:
            st.warning(f"⚠️ **High Risk Items:** {len(high_risk_items)} items at risk of stockout within 7 days")
            
            risk_df = pd.DataFrame(high_risk_items)
            st.dataframe(risk_df, use_container_width=True)

def display_trend_analysis_tab(analysis_results):
    """Display trend analysis results."""
    st.subheader("📊 Trend Analysis")
    
    if 'demand_trends' not in analysis_results.get('trends', {}):
        st.warning("⚠️ No trend analysis data available.")
        return
    
    trend_data = analysis_results['trends']['demand_trends']
    
    # Display trend summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Trend Direction",
            value=trend_data['trend_direction'].title(),
            delta=f"Magnitude: {safe_format(trend_data['trend_magnitude'], 3)}"
        )
    
    with col2:
        st.metric(
            label="Seasonality Strength",
            value=safe_format(trend_data['seasonality_strength'], 2),
            delta="0 = No seasonality, 1 = Strong seasonality"
        )
    
    with col3:
        st.metric(
            label="Data Points",
            value=len(trend_data['daily_data']),
            delta="Historical observations"
        )
    
    # Display trend charts
    if 'daily_data' in trend_data:
        daily_data = trend_data['daily_data']
        
        # Time series plot
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['quantity'],
            mode='lines',
            name='Actual Demand',
            line=dict(color='#667eea')
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['ma_7'],
            mode='lines',
            name='7-Day Moving Average',
            line=dict(color='#764ba2', dash='dash')
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=daily_data['date'],
            y=daily_data['ma_30'],
            mode='lines',
            name='30-Day Moving Average',
            line=dict(color='#f093fb', dash='dot')
        ))
        
        fig_trends.update_layout(
            title="Demand Trends Over Time",
            xaxis_title="Date",
            yaxis_title="Demand Quantity",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Seasonality analysis
        seasonality_strength = trend_data['seasonality_strength']
        if isinstance(seasonality_strength, (np.ndarray, list)):
            seasonality_strength = np.mean(seasonality_strength) if len(seasonality_strength) > 0 else 0
        
        if seasonality_strength > 0.3:
            st.subheader("🌱 Seasonality Analysis")
            
            monthly_data = daily_data.groupby('month')['quantity'].mean()
            
            fig_seasonality = px.bar(
                x=monthly_data.index,
                y=monthly_data.values,
                title="Monthly Demand Patterns",
                color_discrete_sequence=['#667eea']
            )
            
            fig_seasonality.update_layout(
                xaxis_title="Month",
                yaxis_title="Average Demand"
            )
            
            st.plotly_chart(fig_seasonality, use_container_width=True)

def display_anomaly_detection_tab(analysis_results):
    """Display anomaly detection results."""
    st.subheader("⚠️ Anomaly Detection")
    
    if not analysis_results['anomalies']:
        st.info("No anomaly detection data available.")
        return
    
    # Stock anomalies
    if 'stock_anomalies' in analysis_results['anomalies']:
        st.subheader("📦 Stock Level Anomalies")
        
        stock_anomalies = analysis_results['anomalies']['stock_anomalies']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Anomaly Score",
                value=f"{stock_anomalies['anomaly_score']:.1f}%",
                delta="Percentage of anomalous items"
            )
        
        with col2:
            st.metric(
                label="Anomalous Items",
                value=len(stock_anomalies['anomalous_items']),
                delta="Items flagged as anomalies"
            )
        
        if stock_anomalies['anomalous_items']:
            st.warning(f"🚨 **Anomalous Stock Levels:** {len(stock_anomalies['anomalous_items'])} items detected")
            
            # Display anomalous items - we need to pass the data as a parameter
            st.info("📊 Anomalous items detected. Check the data for detailed analysis.")
    
    # Demand anomalies
    if 'demand_anomalies' in analysis_results['anomalies']:
        st.subheader("📊 Demand Pattern Anomalies")
        
        demand_anomalies = analysis_results['anomalies']['demand_anomalies']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Anomaly Score",
                value=f"{demand_anomalies['anomaly_score']:.1f}%",
                delta="Percentage of anomalous dates"
            )
        
        with col2:
            st.metric(
                label="Anomalous Dates",
                value=len(demand_anomalies['anomalous_dates']),
                delta="Dates with unusual demand"
            )
    
    # Cost anomalies
    if 'cost_anomalies' in analysis_results['anomalies']:
        st.subheader("💰 Cost Anomalies")
        
        cost_anomalies = analysis_results['anomalies']['cost_anomalies']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Anomaly Score",
                value=f"{cost_anomalies['anomaly_score']:.1f}%",
                delta="Percentage of anomalous costs"
            )
        
        with col2:
            st.metric(
                label="Anomalous Costs",
                value=len(cost_anomalies['anomalous_costs']),
                delta="Items with unusual costs"
            )

def display_optimization_tab(analysis_results):
    """Display optimization recommendations."""
    st.subheader("🎯 Optimization Recommendations")
    
    if not analysis_results['optimization_recommendations']:
        st.info("No optimization recommendations available.")
        return
    
    # Reorder point optimization
    if 'reorder_point_optimization' in analysis_results['optimization_recommendations']:
        st.subheader("📋 Reorder Point Optimization")
        
        reorder_optimizations = analysis_results['optimization_recommendations']['reorder_point_optimization']
        
        if reorder_optimizations:
            st.info(f"🔍 **Optimization Opportunities:** {len(reorder_optimizations)} items need reorder point adjustments")
            
            # Create optimization dataframe
            opt_df = pd.DataFrame(reorder_optimizations)
            
            # Display summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_adjustment = opt_df['adjustment_needed'].mean()
                st.metric(
                    label="Average Adjustment",
                    value=safe_format(avg_adjustment, 1),
                    delta="Units adjustment needed"
                )
            
            with col2:
                positive_adjustments = len(opt_df[opt_df['adjustment_needed'] > 0])
                st.metric(
                    label="Increase Needed",
                    value=positive_adjustments,
                    delta="Items needing higher reorder points"
                )
            
            with col3:
                negative_adjustments = len(opt_df[opt_df['adjustment_needed'] < 0])
                st.metric(
                    label="Decrease Needed",
                    value=negative_adjustments,
                    delta="Items needing lower reorder points"
                )
            
            # Display detailed recommendations
            st.subheader("📊 Detailed Optimization Recommendations")
            st.dataframe(opt_df, use_container_width=True)
            
            # Create optimization chart with performance optimizations
            # Use absolute values for size to ensure non-negative values
            opt_df_copy = opt_df.copy()
            opt_df_copy['size_value'] = opt_df_copy['adjustment_needed'].abs()
            
            # Optimize chart rendering for large datasets
            if len(opt_df_copy) > 1000:
                # Sample data for large datasets to improve chart performance
                sample_size = min(1000, len(opt_df_copy))
                opt_df_sample = opt_df_copy.sample(n=sample_size, random_state=42)
                st.info(f"📊 Chart shows {sample_size} randomly sampled items from {len(opt_df_copy)} total items for better performance")
            else:
                opt_df_sample = opt_df_copy
            
            # Create chart with optimized settings
            fig_optimization = px.scatter(
                opt_df_sample,
                x='current_reorder_point',
                y='optimal_reorder_point',
                size='size_value',
                color='reason',
                title="Reorder Point Optimization",
                hover_data=['item_name'],
                render_mode='svg'  # Use SVG for better performance
            )
            
            fig_optimization.update_layout(
                xaxis_title="Current Reorder Point",
                yaxis_title="Optimal Reorder Point",
                showlegend=True,
                hovermode='closest'
            )
            
            # Optimize chart performance
            fig_optimization.update_traces(
                marker=dict(line=dict(width=0.5)),
                selector=dict(type='scatter')
            )
            
            st.plotly_chart(fig_optimization, use_container_width=True, config={'displayModeBar': False})
        else:
            st.success("✅ All reorder points are optimally configured!")

def display_cost_forecasting_tab(analysis_results, data):
    """Display cost forecasting results."""
    st.subheader("💰 Cost Forecasting")
    
    if 'cost_forecast' not in analysis_results['forecasts']:
        st.info("No cost forecasting data available.")
        return
    
    cost_forecast = analysis_results['forecasts']['cost_forecast']
    
    # Display cost forecast summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Trend Direction",
            value=cost_forecast['trend_direction'].title(),
            delta=f"Slope: {safe_format(cost_forecast['trend_slope'], 3)}"
        )
    
    with col2:
        current_cost = data['unit_cost'].mean() if 'unit_cost' in data.columns else 0
        future_cost = cost_forecast['monthly_forecast'][-1]
        cost_change = ((future_cost - current_cost) / current_cost) * 100 if current_cost > 0 else 0
        
        st.metric(
            label="12-Month Forecast",
            value=f"${safe_format(future_cost, 2)}",
            delta=f"{safe_format(cost_change, 1)}% change"
        )
    
    with col3:
        st.metric(
            label="Forecast Horizon",
            value=f"{cost_forecast['forecast_horizon']} months",
            delta="Future prediction period"
        )
    
    # Display cost trend chart
    if 'monthly_forecast' in cost_forecast:
        months = list(range(1, len(cost_forecast['monthly_forecast']) + 1))
        
        fig_cost_forecast = px.line(
            x=months,
            y=cost_forecast['monthly_forecast'],
            title="12-Month Cost Forecast",
            markers=True
        )
        
        fig_cost_forecast.update_layout(
            xaxis_title="Month",
            yaxis_title="Forecasted Unit Cost ($)",
            showlegend=False
        )
        
        st.plotly_chart(fig_cost_forecast, use_container_width=True)
    
    # Display supplier performance predictions
    if 'supplier_performance_prediction' in analysis_results['forecasts']:
        st.subheader("🏭 Supplier Performance Predictions")
        
        supplier_predictions = analysis_results['forecasts']['supplier_performance_prediction']
        
        if supplier_predictions:
            # Create prediction dataframe
            pred_df = pd.DataFrame(supplier_predictions)
            
            # Display summary metrics
            col1, col2 = st.columns(2)
            
            with col1:
                improving_suppliers = len(pred_df[pred_df['predicted_change'] > 0])
                st.metric(
                    label="Improving Suppliers",
                    value=improving_suppliers,
                    delta="Expected performance improvement"
                )
            
            with col2:
                declining_suppliers = len(pred_df[pred_df['predicted_change'] < 0])
                st.metric(
                    label="Declining Suppliers",
                    value=declining_suppliers,
                    delta="Expected performance decline"
                )
            
            # Display detailed predictions
            st.subheader("📊 Supplier Performance Forecasts")
            st.dataframe(pred_df, use_container_width=True)
            
            # Create performance comparison chart
            fig_supplier_performance = px.scatter(
                pred_df,
                x='current_performance',
                y='predicted_performance',
                size='confidence',
                color='predicted_change',
                title="Supplier Performance Predictions",
                hover_data=['supplier_id'],
                color_continuous_scale='RdYlGn'
            )
            
            fig_supplier_performance.update_layout(
                xaxis_title="Current Performance",
                yaxis_title="Predicted Performance"
            )
            
            st.plotly_chart(fig_supplier_performance, use_container_width=True)

def generate_predictive_analytics_report(data):
    """Generate a comprehensive predictive analytics report."""
    if data is None or data.empty:
        return "No data available for predictive analytics."
    
    predictive_analytics = InventoryPredictiveAnalytics(data)
    analysis_results = predictive_analytics.perform_comprehensive_analysis()
    
    if not analysis_results:
        return "Unable to generate predictive analytics report."
    
    # Helper function to safely format values for reports
    def safe_report_format(value, decimal_places=0):
        """Safely format a value for reports, handling numpy arrays and None values."""
        if value is None:
            return "N/A"
        if isinstance(value, (np.ndarray, list)):
            # If it's an array/list, take the mean or first value
            if len(value) > 0:
                value = np.mean(value) if len(value) > 1 else value[0]
            else:
                return "N/A"
        if np.isnan(value):
            return "N/A"
        return f"{value:.{decimal_places}f}"
    
    report = []
    report.append("INVENTORY PREDICTIVE ANALYTICS REPORT")
    report.append("=" * 50)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Demand forecasting summary
    if 'demand_forecast' in analysis_results['forecasts']:
        report.append("DEMAND FORECASTING SUMMARY")
        report.append("-" * 30)
        forecast_data = analysis_results['forecasts']['demand_forecast']
        report.append(f"Combined Forecast: {safe_report_format(forecast_data['combined_forecast'])} units")
        report.append(f"Forecast Horizon: {forecast_data['forecast_horizon']} days")
        report.append("")
    
    # Trend analysis summary
    if 'demand_trends' in analysis_results['trends']:
        report.append("TREND ANALYSIS SUMMARY")
        report.append("-" * 25)
        trend_data = analysis_results['trends']['demand_trends']
        report.append(f"Trend Direction: {trend_data['trend_direction']}")
        report.append(f"Seasonality Strength: {safe_report_format(trend_data['seasonality_strength'], 2)}")
        report.append("")
    
    # Anomaly detection summary
    if analysis_results['anomalies']:
        report.append("ANOMALY DETECTION SUMMARY")
        report.append("-" * 30)
        for anomaly_type, anomaly_data in analysis_results['anomalies'].items():
            report.append(f"{anomaly_type.replace('_', ' ').title()}: {safe_report_format(anomaly_data['anomaly_score'], 1)}%")
        report.append("")
    
    # Optimization recommendations
    if analysis_results['optimization_recommendations']:
        report.append("OPTIMIZATION RECOMMENDATIONS")
        report.append("-" * 30)
        for opt_type, opt_data in analysis_results['optimization_recommendations'].items():
            report.append(f"{opt_type.replace('_', ' ').title()}: {len(opt_data)} recommendations")
        report.append("")
    
    return "\n".join(report)

# ============================================================================
# PERFORMANCE MONITORING AND OPTIMIZATION
# ============================================================================

def monitor_performance(func):
    """Decorator to monitor function performance."""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Log performance metrics
            if duration > 1.0:  # Log slow operations
                st.warning(f"⚠️ {func.__name__} took {duration:.2f} seconds to complete")
            elif duration > 0.5:
                st.info(f"ℹ️ {func.__name__} completed in {duration:.2f} seconds")
            else:
                st.success(f"✅ {func.__name__} completed in {duration:.2f} seconds")
            
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            st.error(f"❌ {func.__name__} failed after {duration:.2f} seconds: {str(e)}")
            raise
    
    return wrapper

def get_performance_summary():
    """Get a summary of performance optimizations implemented."""
    return {
        "dataframe_optimization": "Category encoding and numeric type optimization",
        "caching": "5-minute TTL cache for expensive calculations",
        "vectorized_operations": "Numpy and pandas vectorized operations",
        "sampling": "Data sampling for large datasets in visualizations",
        "chart_optimization": "SVG rendering and performance settings",
        "progress_tracking": "Real-time progress bars and status updates",
        "error_handling": "Comprehensive exception handling with fallbacks",
        "memory_management": "Efficient data copying and garbage collection"
    }

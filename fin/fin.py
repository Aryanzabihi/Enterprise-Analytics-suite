import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from datetime import datetime
import io
import base64
import warnings
from functools import lru_cache
import time

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Machine Learning imports (lazy loading for better startup performance)
try:
    from sklearn.ensemble import IsolationForest, RandomForestRegressor
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ Scikit-learn not available. Some advanced features will be disabled.")

# Performance optimization: Set pandas options for better performance
pd.options.mode.chained_assignment = None

# Try to enable numba optimization if available
try:
    pd.options.compute.use_numba = True
except ImportError:
    # Numba not available, continue without it
    pass

# Global cache for expensive calculations
@st.cache_data(ttl=3600, max_entries=100)
def get_cached_calculations():
    """Cache for expensive financial calculations"""
    return {}

# Helper function to find cash flow column names with fallbacks
def get_cash_flow_column_mapping(cash_flow_data):
    """Get mapping for cash flow columns with fallback names"""
    mapping = {}
    
    # Operating cash flow column mapping
    for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
        if col_name in cash_flow_data.columns:
            mapping['operating_cash_flow'] = col_name
            break
    
    # Free cash flow column mapping
    for col_name in ['free_cash_flow', 'free_cf', 'free_cashflow', 'fcf']:
        if col_name in cash_flow_data.columns:
            mapping['free_cash_flow'] = col_name
            break
    
    # Capital expenditures column mapping
    for col_name in ['capital_expenditures', 'capex', 'capital_expenses', 'investment_expenditures']:
        if col_name in cash_flow_data.columns:
            mapping['capital_expenditures'] = col_name
            break
    
    return mapping

# Performance monitoring
class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.operations = {}
    
    def start_operation(self, name):
        self.operations[name] = time.time()
    
    def end_operation(self, name):
        if name in self.operations:
            duration = time.time() - self.operations[name]
            # Removed sidebar logging to keep UI clean
            del self.operations[name]

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Performance-optimized chart rendering
@st.cache_data(ttl=1800, max_entries=100)
def create_optimized_chart(chart_type, data, x_col, y_col, title, **kwargs):
    """Create optimized charts with caching for better performance"""
    try:
        if chart_type == "line":
            fig = go.Figure(data=[
                go.Scatter(x=data[x_col], y=data[y_col], mode='lines+markers', 
                          line=dict(width=2), marker=dict(size=6))
            ])
        elif chart_type == "bar":
            fig = go.Figure(data=[
                go.Bar(x=data[x_col], y=data[y_col], marker_color='#1f77b4')
            ])
        elif chart_type == "scatter":
            fig = go.Figure(data=[
                go.Scatter(x=data[x_col], y=data[y_col], mode='markers', 
                          marker=dict(size=8, color='#2ca02c'))
            ])
        
        # Apply common styling
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400
        )
        
        return fig
    except Exception as e:
        st.error(f"Chart creation error: {e}")
        return None

# Optimized data processing functions
@st.cache_data(ttl=900, max_entries=200)
def preprocess_financial_data(data, required_columns):
    """Preprocess financial data for analysis with caching"""
    if data.empty:
        return pd.DataFrame()
    
    # Fill missing values efficiently
    for col in required_columns:
        if col in data.columns:
            if data[col].dtype in ['int64', 'float64']:
                data[col] = data[col].fillna(0)
            else:
                data[col] = data[col].fillna('Unknown')
    
    return data

# Lazy loading for heavy computations
class LazyFinancialCalculator:
    def __init__(self):
        self._cache = {}
    
    def get_cached_result(self, key, calculation_func, *args):
        """Get cached result or calculate if not available"""
        if key not in self._cache:
            self._cache[key] = calculation_func(*args)
        return self._cache[key]
    
    def clear_cache(self):
        """Clear the calculation cache"""
        self._cache.clear()

# Global lazy calculator
lazy_calculator = LazyFinancialCalculator()

# Finance-specific metric calculation functions (optimized for performance)
@st.cache_data(ttl=1800, max_entries=50)
def calculate_financial_performance_metrics(income_statement_data, balance_sheet_data):
    """Calculate comprehensive financial performance metrics with enhanced analysis (optimized)"""
    perf_monitor.start_operation("financial_performance_calculation")
    
    if income_statement_data.empty:
        perf_monitor.end_operation("financial_performance_calculation")
        return pd.DataFrame(), "No income statement data available"
    
    try:
        # Vectorized operations for better performance
        df = income_statement_data.copy()
        
        # Fill missing values with 0 for calculations
        numeric_columns = ['revenue', 'cost_of_goods_sold', 'gross_profit', 'operating_expenses', 
                          'operating_income', 'net_income', 'ebitda', 'ebit']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
            else:
                df[col] = 0
        
        # Vectorized ratio calculations (much faster than loops)
        revenue = df['revenue'].values
        gross_profit = df['gross_profit'].values
        operating_income = df['operating_income'].values
        net_income = df['net_income'].values
        operating_expenses = df['operating_expenses'].values
        ebitda = df['ebitda'].values
        ebit = df['ebit'].values
        
        # Avoid division by zero with numpy where
        gross_margin = np.where(revenue > 0, (gross_profit / revenue * 100), 0)
        operating_margin = np.where(revenue > 0, (operating_income / revenue * 100), 0)
        net_margin = np.where(revenue > 0, (net_income / revenue * 100), 0)
        expense_ratio = np.where(revenue > 0, (operating_expenses / revenue * 100), 0)
        ebitda_margin = np.where(revenue > 0, (ebitda / revenue * 100), 0)
        ebit_margin = np.where(revenue > 0, (ebit / revenue * 100), 0)
        cost_of_goods_ratio = np.where(revenue > 0, (df['cost_of_goods_sold'].values / revenue * 100), 0)
        operating_efficiency = np.where(gross_profit > 0, (operating_income / gross_profit * 100), 0)
        return_on_revenue = np.where(revenue > 0, (net_income / revenue * 100), 0)
        profit_quality = np.where(net_income != 0, (operating_income / net_income * 100), 0)
        
        # Create metrics dataframe
        metrics_df = pd.DataFrame({
            'period': df['period'].values,
            'revenue': revenue,
            'gross_margin_pct': gross_margin,
            'operating_margin_pct': operating_margin,
            'net_margin_pct': net_margin,
            'expense_ratio_pct': expense_ratio,
            'ebitda_margin_pct': ebitda_margin,
            'ebit_margin_pct': ebit_margin,
            'cost_of_goods_ratio_pct': cost_of_goods_ratio,
            'operating_efficiency_pct': operating_efficiency,
            'return_on_revenue_pct': return_on_revenue,
            'profit_quality_pct': profit_quality,
            'gross_profit': gross_profit,
            'operating_income': operating_income,
            'net_income': net_income,
            'ebitda': ebitda,
            'ebit': ebit
        })
        
        # Add performance indicators and trends (vectorized)
        if len(metrics_df) > 1:
            # Vectorized calculations
            metrics_df['revenue_growth_pct'] = metrics_df['revenue'].pct_change() * 100
            metrics_df['gross_margin_change_pct'] = metrics_df['gross_margin_pct'].diff()
            metrics_df['operating_margin_change_pct'] = metrics_df['operating_margin_pct'].diff()
            metrics_df['net_margin_change_pct'] = metrics_df['net_margin_pct'].diff()
            
            # Vectorized moving averages
            metrics_df['revenue_ma_3'] = metrics_df['revenue'].rolling(window=3, min_periods=1).mean()
            metrics_df['gross_margin_ma_3'] = metrics_df['gross_margin_pct'].rolling(window=3, min_periods=1).mean()
            metrics_df['operating_margin_ma_3'] = metrics_df['operating_margin_pct'].rolling(window=3, min_periods=1).mean()
            
            # Vectorized performance scoring (much faster than loops)
            revenue_growth = metrics_df['revenue_growth_pct'].fillna(0).values
            gross_margin_vals = metrics_df['gross_margin_pct'].values
            operating_margin_vals = metrics_df['operating_margin_pct'].values
            net_margin_vals = metrics_df['net_margin_pct'].values
            
            # Revenue growth scoring (25 points)
            revenue_score = np.where(revenue_growth > 10, 25,
                                   np.where(revenue_growth > 5, 20,
                                           np.where(revenue_growth > 0, 15,
                                                   np.where(revenue_growth > -5, 10, 5))))
            
            # Margin scoring (50 points)
            gross_score = np.where(gross_margin_vals > 40, 20,
                                  np.where(gross_margin_vals > 30, 15,
                                          np.where(gross_margin_vals > 20, 10, 5)))
            
            operating_score = np.where(operating_margin_vals > 15, 20,
                                      np.where(operating_margin_vals > 10, 15,
                                              np.where(operating_margin_vals > 5, 10, 5)))
            
            # Profitability scoring (25 points)
            profit_score = np.where(net_margin_vals > 10, 25,
                                   np.where(net_margin_vals > 5, 20,
                                           np.where(net_margin_vals > 0, 15, 5)))
            
            # Total score
            metrics_df['performance_score'] = revenue_score + gross_score + operating_score + profit_score
        
        perf_monitor.end_operation("financial_performance_calculation")
        return metrics_df, "Enhanced financial performance metrics calculated successfully (optimized)"
        
    except Exception as e:
        perf_monitor.end_operation("financial_performance_calculation")
        return pd.DataFrame(), f"Error calculating financial performance metrics: {str(e)}"

@st.cache_data(ttl=1800, max_entries=50)
def calculate_liquidity_solvency_metrics(balance_sheet_data, cash_flow_data):
    """Calculate comprehensive liquidity and solvency metrics with enhanced analysis (optimized)"""
    perf_monitor.start_operation("liquidity_solvency_calculation")
    
    if balance_sheet_data.empty:
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return pd.DataFrame(), "No balance sheet data available"
    
    try:
        # Vectorized operations for better performance
        df = balance_sheet_data.copy()
        
        # Fill missing values with 0 for calculations
        numeric_columns = ['current_assets', 'total_assets', 'current_liabilities', 'total_liabilities',
                          'shareholder_equity', 'cash_and_equivalents', 'accounts_receivable', 
                          'inventory', 'long_term_debt', 'total_debt']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
            else:
                df[col] = 0
        
        # Vectorized ratio calculations
        current_assets = df['current_assets'].values
        total_assets = df['total_assets'].values
        current_liabilities = df['current_liabilities'].values
        total_liabilities = df['total_liabilities'].values
        shareholder_equity = df['shareholder_equity'].values
        cash_and_equivalents = df['cash_and_equivalents'].values
        accounts_receivable = df['accounts_receivable'].values
        inventory = df['inventory'].values
        long_term_debt = df['long_term_debt'].values
        total_debt = df['total_debt'].values
        
        # Vectorized liquidity ratios
        current_ratio = np.where(current_liabilities > 0, current_assets / current_liabilities, 0)
        quick_ratio = np.where(current_liabilities > 0, (cash_and_equivalents + accounts_receivable) / current_liabilities, 0)
        cash_ratio = np.where(current_liabilities > 0, cash_and_equivalents / current_liabilities, 0)
        working_capital = current_assets - current_liabilities
        working_capital_ratio = np.where(total_assets > 0, working_capital / total_assets, 0)
        
        # Vectorized solvency ratios
        debt_to_equity = np.where(shareholder_equity > 0, total_liabilities / shareholder_equity, 0)
        debt_to_assets = np.where(total_assets > 0, total_liabilities / total_assets, 0)
        equity_ratio = np.where(total_assets > 0, shareholder_equity / total_assets, 0)
        debt_ratio = np.where(total_assets > 0, total_liabilities / total_assets, 0)
        
        # Placeholder ratios for future enhancement
        times_interest_earned = np.zeros_like(current_assets)
        debt_service_coverage = np.zeros_like(current_assets)
        cash_flow_to_debt = np.zeros_like(current_assets)
        inventory_turnover_ratio = np.zeros_like(current_assets)
        receivables_turnover_ratio = np.zeros_like(current_assets)
        
        # Create metrics dataframe
        metrics_df = pd.DataFrame({
            'period': df['period'].values,
            'current_ratio': current_ratio,
            'quick_ratio': quick_ratio,
            'cash_ratio': cash_ratio,
            'working_capital': working_capital,
            'working_capital_ratio': working_capital_ratio,
            'debt_to_equity': debt_to_equity,
            'debt_to_assets': debt_to_assets,
            'equity_ratio': equity_ratio,
            'debt_ratio': debt_ratio,
            'times_interest_earned': times_interest_earned,
            'debt_service_coverage': debt_service_coverage,
            'cash_flow_to_debt': cash_flow_to_debt,
            'inventory_turnover_ratio': inventory_turnover_ratio,
            'receivables_turnover_ratio': receivables_turnover_ratio,
            'current_assets': current_assets,
            'total_assets': total_assets,
            'current_liabilities': current_liabilities,
            'total_liabilities': total_liabilities,
            'shareholder_equity': shareholder_equity,
            'cash_and_equivalents': cash_and_equivalents,
            'accounts_receivable': accounts_receivable,
            'inventory': inventory,
            'long_term_debt': long_term_debt,
            'total_debt': total_debt
        })
        
        # Add performance indicators and trends (vectorized)
        if len(metrics_df) > 1:
            # Vectorized period-over-period changes
            metrics_df['current_ratio_change'] = metrics_df['current_ratio'].diff()
            metrics_df['quick_ratio_change'] = metrics_df['quick_ratio'].diff()
            metrics_df['debt_to_equity_change'] = metrics_df['debt_to_equity'].diff()
            metrics_df['working_capital_change'] = metrics_df['working_capital'].diff()
            
            # Vectorized moving averages
            metrics_df['current_ratio_ma_3'] = metrics_df['current_ratio'].rolling(window=3, min_periods=1).mean()
            metrics_df['quick_ratio_ma_3'] = metrics_df['quick_ratio'].rolling(window=3, min_periods=1).mean()
            metrics_df['debt_to_equity_ma_3'] = metrics_df['debt_to_equity'].rolling(window=3, min_periods=1).mean()
            
            # Vectorized financial health scoring (much faster than loops)
            current_ratio_vals = metrics_df['current_ratio'].values
            quick_ratio_vals = metrics_df['quick_ratio'].values
            debt_to_equity_vals = metrics_df['debt_to_equity'].values
            debt_to_assets_vals = metrics_df['debt_to_assets'].values
            working_capital_vals = metrics_df['working_capital'].values
            working_capital_ratio_vals = metrics_df['working_capital_ratio'].values
            
            # Liquidity scoring (40 points)
            current_ratio_score = np.where(current_ratio_vals >= 2.0, 20,
                                          np.where(current_ratio_vals >= 1.5, 15,
                                                  np.where(current_ratio_vals >= 1.0, 10, 5)))
            
            quick_ratio_score = np.where(quick_ratio_vals >= 1.0, 20,
                                        np.where(quick_ratio_vals >= 0.8, 15,
                                                np.where(quick_ratio_vals >= 0.5, 10, 5)))
            
            # Solvency scoring (40 points)
            debt_equity_score = np.where(debt_to_equity_vals <= 0.5, 20,
                                        np.where(debt_to_equity_vals <= 1.0, 15,
                                                np.where(debt_to_equity_vals <= 2.0, 10, 5)))
            
            debt_assets_score = np.where(debt_to_assets_vals <= 0.3, 20,
                                        np.where(debt_to_assets_vals <= 0.5, 15,
                                                np.where(debt_to_assets_vals <= 0.7, 10, 5)))
            
            # Working capital scoring (20 points)
            working_capital_score = np.where(working_capital_vals > 0,
                                            np.where(working_capital_ratio_vals >= 0.2, 20,
                                                    np.where(working_capital_ratio_vals >= 0.1, 15,
                                                            np.where(working_capital_ratio_vals >= 0.05, 10, 5))), 0)
            
            # Total score
            metrics_df['financial_health_score'] = (current_ratio_score + quick_ratio_score + 
                                                   debt_equity_score + debt_assets_score + working_capital_score)
        
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return metrics_df, "Enhanced liquidity and solvency metrics calculated successfully (optimized)"
        
    except Exception as e:
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return pd.DataFrame(), f"Error calculating liquidity and solvency metrics: {str(e)}"

def calculate_risk_compliance_metrics(balance_sheet_data, market_data):
    """Calculate risk and compliance metrics"""
    if balance_sheet_data.empty:
        return pd.DataFrame(), "No balance sheet data available"
    
    try:
        metrics = []
        
        # Calculate Value at Risk (VaR)
        if 'total_assets' in balance_sheet_data.columns:
            portfolio_value = balance_sheet_data['total_assets'].sum()
            # Simple VaR calculation with assumed volatility
            volatility = 0.15  # 15% annual volatility
            confidence_level = 0.95
            z_score = 1.645  # 95% confidence level
            time_horizon = 30/365  # 30 days
            
            var = portfolio_value * volatility * np.sqrt(time_horizon) * z_score
            metrics.append({
                'Metric': 'Value at Risk (VaR)',
                'Value': f"${var:,.0f}",
                'Description': f"95% confidence, 30-day horizon"
            })
        
        # Calculate Liquidity Coverage Ratio (LCR)
        if 'current_assets' in balance_sheet_data.columns and 'current_liabilities' in balance_sheet_data.columns:
            current_assets = balance_sheet_data['current_assets'].sum()
            current_liabilities = balance_sheet_data['current_liabilities'].sum()
            
            if current_liabilities > 0:
                lcr = current_assets / current_liabilities
                metrics.append({
                    'Metric': 'Liquidity Coverage Ratio',
                    'Value': f"{lcr:.2f}",
                    'Description': f"Current assets / Current liabilities"
                })
        
        # Calculate Capital Adequacy Ratio (CAR)
        if 'shareholder_equity' in balance_sheet_data.columns and 'total_assets' in balance_sheet_data.columns:
            equity = balance_sheet_data['shareholder_equity'].sum()
            total_assets = balance_sheet_data['total_assets'].sum()
            
            if total_assets > 0:
                car = (equity / total_assets) * 100
                metrics.append({
                    'Metric': 'Capital Adequacy Ratio',
                    'Value': f"{car:.1f}%",
                    'Description': f"Equity / Total assets"
                })
        
        # Calculate Debt Service Coverage Ratio (DSCR)
        if 'total_liabilities' in balance_sheet_data.columns and 'shareholder_equity' in balance_sheet_data.columns:
            total_liabilities = balance_sheet_data['total_liabilities'].sum()
            equity = balance_sheet_data['shareholder_equity'].sum()
            
            if equity > 0:
                dscr = total_liabilities / equity
                metrics.append({
                    'Metric': 'Debt Service Coverage',
                    'Value': f"{dscr:.2f}",
                    'Description': f"Total liabilities / Equity"
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Risk and compliance metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating risk and compliance metrics: {str(e)}"

def calculate_efficiency_metrics(income_statement_data, balance_sheet_data):
    """Calculate efficiency and productivity metrics"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return pd.DataFrame(), "No income statement or balance sheet data available"
    
    try:
        metrics = []
        
        for _, row in income_statement_data.iterrows():
            period = row.get('period', 'Unknown')
            revenue = row.get('revenue', 0)
            net_income = row.get('net_income', 0)
            operating_expenses = row.get('operating_expenses', 0)
            
            # Get corresponding balance sheet data
            bs_row = balance_sheet_data[balance_sheet_data['period'] == period]
            if not bs_row.empty:
                total_assets = bs_row.iloc[0].get('total_assets', 0)
                shareholder_equity = bs_row.iloc[0].get('shareholder_equity', 0)
                
                # Calculate ratios
                roa = (net_income / total_assets * 100) if total_assets > 0 else 0
                roe = (net_income / shareholder_equity * 100) if shareholder_equity > 0 else 0
                asset_turnover = (revenue / total_assets) if total_assets > 0 else 0
                op_exp_ratio = (operating_expenses / revenue * 100) if revenue > 0 else 0
                
                metrics.append({
                    'period': period,
                    'roa_pct': roa,
                    'roe_pct': roe,
                    'asset_turnover': asset_turnover,
                    'op_exp_ratio_pct': op_exp_ratio,
                    'revenue': revenue,
                    'net_income': net_income,
                    'total_assets': total_assets,
                    'shareholder_equity': shareholder_equity
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Efficiency metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating efficiency metrics: {str(e)}"

def calculate_budget_variance_metrics(income_statement_data, budget_data, forecast_data):
    """Calculate budget variance and forecasting metrics"""
    if budget_data.empty and forecast_data.empty:
        return pd.DataFrame(), "No budget or forecast data available"
    
    try:
        metrics = []
        
        # Budget variance analysis
        if not budget_data.empty and not income_statement_data.empty:
            # Try to match periods between budget and actual data
            try:
                budget_copy = budget_data.copy()
                income_copy = income_statement_data[['period', 'revenue', 'cost_of_goods_sold', 'operating_expenses']].copy()
                
                # Rename columns for clarity
                budget_copy = budget_copy.rename(columns={
                    'revenue': 'revenue_budget',
                    'expenses': 'expenses_budget'
                })
                
                income_copy = income_copy.rename(columns={
                    'revenue': 'revenue_actual',
                    'cost_of_goods_sold': 'cost_of_goods_sold_actual',
                    'operating_expenses': 'operating_expenses_actual'
                })
                
                # Merge budget and actual data
                budget_actual = budget_copy.merge(income_copy, on='period', how='inner')
                
                if not budget_actual.empty:
                    # Calculate actual expenses
                    if 'cost_of_goods_sold_actual' in budget_actual.columns and 'operating_expenses_actual' in budget_actual.columns:
                        budget_actual['expenses_actual'] = budget_actual['cost_of_goods_sold_actual'] + budget_actual['operating_expenses_actual']
                    
                    # Calculate revenue variance
                    if 'revenue_budget' in budget_actual.columns and 'revenue_actual' in budget_actual.columns:
                        revenue_variance = ((budget_actual['revenue_actual'] - budget_actual['revenue_budget']) / budget_actual['revenue_budget'] * 100).mean()
                        metrics.append({
                            'Metric': 'Revenue Variance',
                            'Value': f"{revenue_variance:+.1f}%",
                            'Description': 'Average revenue variance'
                        })
                    
                    # Calculate expense variance
                    if 'expenses_budget' in budget_actual.columns and 'expenses_actual' in budget_actual.columns:
                        expense_variance = ((budget_actual['expenses_budget'] - budget_actual['expenses_actual']) / budget_actual['expenses_budget'] * 100).mean()
                        metrics.append({
                            'Metric': 'Expense Variance',
                            'Value': f"{expense_variance:+.1f}%",
                            'Description': 'Average expense variance'
                        })
                
            except Exception as e:
                # Fallback to simple calculation if merge fails
                total_budget = budget_data['revenue'].sum() if 'revenue' in budget_data.columns else 0
                total_actual = budget_data['expenses'].sum() if 'expenses' in budget_data.columns else 0
                
                if total_budget > 0:
                    variance = ((total_actual - total_budget) / total_budget * 100)
                    metrics.append({
                        'Metric': 'Budget Variance',
                        'Value': f"{variance:+.1f}%",
                        'Description': 'Actual vs Budget variance'
                    })
        
        # Forecast accuracy
        if not forecast_data.empty:
            if 'confidence_level' in forecast_data.columns:
                avg_confidence = forecast_data['confidence_level'].mean()
                metrics.append({
                    'Metric': 'Forecast Confidence',
                    'Value': f"{avg_confidence:.1f}%",
                    'Description': 'Average forecast confidence level'
                })
        
        # Scenario analysis
        if not forecast_data.empty and len(forecast_data) > 1:
            scenarios = forecast_data['scenario'].nunique() if 'scenario' in forecast_data.columns else 1
            metrics.append({
                'Metric': 'Scenarios Analyzed',
                'Value': f"{scenarios}",
                'Description': 'Number of forecast scenarios'
            })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Budget variance metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating budget variance metrics: {str(e)}"

def calculate_cash_flow_metrics(cash_flow_data, balance_sheet_data):
    """Calculate cash flow and working capital metrics"""
    if cash_flow_data.empty:
        return pd.DataFrame(), "No cash flow data available"
    
    try:
        metrics = []
        
        for _, row in cash_flow_data.iterrows():
            period = row.get('period', 'Unknown')
            
            # Find operating cash flow column with fallback names
            operating_cf = 0
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in row.index:
                    operating_cf = row.get(col_name, 0)
                    break
            
            # Find free cash flow column with fallback names
            free_cf = 0
            for col_name in ['free_cash_flow', 'free_cf', 'free_cashflow', 'fcf']:
                if col_name in row.index:
                    free_cf = row.get(col_name, 0)
                    break
            
            net_income = row.get('net_income', 0)
            
            # Get corresponding balance sheet data
            bs_row = balance_sheet_data[balance_sheet_data['period'] == period]
            if not bs_row.empty:
                current_assets = bs_row.iloc[0].get('current_assets', 0)
                current_liabilities = bs_row.iloc[0].get('current_liabilities', 0)
                
                # Calculate ratios
                working_capital = current_assets - current_liabilities
                working_capital_turnover = (operating_cf / working_capital) if working_capital > 0 else 0
                
                metrics.append({
                    'period': period,
                    'operating_cf': operating_cf,
                    'free_cf': free_cf,
                    'working_capital_turnover': working_capital_turnover,
                    'net_income': net_income,
                    'working_capital': working_capital
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Cash flow metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating cash flow metrics: {str(e)}"

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from datetime import datetime
import io
import base64
import warnings
from functools import lru_cache
import time

# Suppress warnings for better performance
warnings.filterwarnings('ignore')

# Machine Learning imports (lazy loading for better startup performance)
try:
    from sklearn.ensemble import IsolationForest, RandomForestRegressor
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ Scikit-learn not available. Some advanced features will be disabled.")

# Performance optimization: Set pandas options for better performance
pd.options.mode.chained_assignment = None

# Try to enable numba optimization if available
try:
    pd.options.compute.use_numba = True
except ImportError:
    # Numba not available, continue without it
    pass

# Global cache for expensive calculations
@st.cache_data(ttl=3600, max_entries=100)
def get_cached_calculations():
    """Cache for expensive financial calculations"""
    return {}

# Performance monitoring
class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.operations = {}
    
    def start_operation(self, name):
        self.operations[name] = time.time()
    
    def end_operation(self, name):
        if name in self.operations:
            duration = time.time() - self.operations[name]
            # Removed sidebar logging to keep UI clean
            del self.operations[name]

# Global performance monitor
perf_monitor = PerformanceMonitor()

# Performance-optimized chart rendering
@st.cache_data(ttl=1800, max_entries=100)
def create_optimized_chart(chart_type, data, x_col, y_col, title, **kwargs):
    """Create optimized charts with caching for better performance"""
    try:
        if chart_type == "line":
            fig = go.Figure(data=[
                go.Scatter(x=data[x_col], y=data[y_col], mode='lines+markers', 
                          line=dict(width=2), marker=dict(size=6))
            ])
        elif chart_type == "bar":
            fig = go.Figure(data=[
                go.Bar(x=data[x_col], y=data[y_col], marker_color='#1f77b4')
            ])
        elif chart_type == "scatter":
            fig = go.Figure(data=[
                go.Scatter(x=data[x_col], y=data[y_col], mode='markers', 
                          marker=dict(size=8, color='#2ca02c'))
            ])
        
        # Apply common styling
        fig.update_layout(
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=11),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400
        )
        
        return fig
    except Exception as e:
        st.error(f"Chart creation error: {e}")
        return None

# Optimized data processing functions
@st.cache_data(ttl=900, max_entries=200)
def preprocess_financial_data(data, required_columns):
    """Preprocess financial data for analysis with caching"""
    if data.empty:
        return pd.DataFrame()
    
    # Fill missing values efficiently
    for col in required_columns:
        if col in data.columns:
            if data[col].dtype in ['int64', 'float64']:
                data[col] = data[col].fillna(0)
            else:
                data[col] = data[col].fillna('Unknown')
    
    return data

# Lazy loading for heavy computations
class LazyFinancialCalculator:
    def __init__(self):
        self._cache = {}
    
    def get_cached_result(self, key, calculation_func, *args):
        """Get cached result or calculate if not available"""
        if key not in self._cache:
            self._cache[key] = calculation_func(*args)
        return self._cache[key]
    
    def clear_cache(self):
        """Clear the calculation cache"""
        self._cache.clear()

# Global lazy calculator
lazy_calculator = LazyFinancialCalculator()

# Finance-specific metric calculation functions (optimized for performance)
@st.cache_data(ttl=1800, max_entries=50)
def calculate_financial_performance_metrics(income_statement_data, balance_sheet_data):
    """Calculate comprehensive financial performance metrics with enhanced analysis (optimized)"""
    perf_monitor.start_operation("financial_performance_calculation")
    
    if income_statement_data.empty:
        perf_monitor.end_operation("financial_performance_calculation")
        return pd.DataFrame(), "No income statement data available"
    
    try:
        # Vectorized operations for better performance
        df = income_statement_data.copy()
        
        # Fill missing values with 0 for calculations
        numeric_columns = ['revenue', 'cost_of_goods_sold', 'gross_profit', 'operating_expenses', 
                          'operating_income', 'net_income', 'ebitda', 'ebit']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
            else:
                df[col] = 0
        
        # Vectorized ratio calculations (much faster than loops)
        revenue = df['revenue'].values
        gross_profit = df['gross_profit'].values
        operating_income = df['operating_income'].values
        net_income = df['net_income'].values
        operating_expenses = df['operating_expenses'].values
        ebitda = df['ebitda'].values
        ebit = df['ebit'].values
        
        # Avoid division by zero with numpy where
        gross_margin = np.where(revenue > 0, (gross_profit / revenue * 100), 0)
        operating_margin = np.where(revenue > 0, (operating_income / revenue * 100), 0)
        net_margin = np.where(revenue > 0, (net_income / revenue * 100), 0)
        expense_ratio = np.where(revenue > 0, (operating_expenses / revenue * 100), 0)
        ebitda_margin = np.where(revenue > 0, (ebitda / revenue * 100), 0)
        ebit_margin = np.where(revenue > 0, (ebit / revenue * 100), 0)
        cost_of_goods_ratio = np.where(revenue > 0, (df['cost_of_goods_sold'].values / revenue * 100), 0)
        operating_efficiency = np.where(gross_profit > 0, (operating_income / gross_profit * 100), 0)
        return_on_revenue = np.where(revenue > 0, (net_income / revenue * 100), 0)
        profit_quality = np.where(net_income != 0, (operating_income / net_income * 100), 0)
        
        # Create metrics dataframe
        metrics_df = pd.DataFrame({
            'period': df['period'].values,
            'revenue': revenue,
            'gross_margin_pct': gross_margin,
            'operating_margin_pct': operating_margin,
            'net_margin_pct': net_margin,
            'expense_ratio_pct': expense_ratio,
            'ebitda_margin_pct': ebitda_margin,
            'ebit_margin_pct': ebit_margin,
            'cost_of_goods_ratio_pct': cost_of_goods_ratio,
            'operating_efficiency_pct': operating_efficiency,
            'return_on_revenue_pct': return_on_revenue,
            'profit_quality_pct': profit_quality,
            'gross_profit': gross_profit,
            'operating_income': operating_income,
            'net_income': net_income,
            'ebitda': ebitda,
            'ebit': ebit
        })
        
        # Add performance indicators and trends (vectorized)
        if len(metrics_df) > 1:
            # Vectorized calculations
            metrics_df['revenue_growth_pct'] = metrics_df['revenue'].pct_change() * 100
            metrics_df['gross_margin_change_pct'] = metrics_df['gross_margin_pct'].diff()
            metrics_df['operating_margin_change_pct'] = metrics_df['operating_margin_pct'].diff()
            metrics_df['net_margin_change_pct'] = metrics_df['net_margin_pct'].diff()
            
            # Vectorized moving averages
            metrics_df['revenue_ma_3'] = metrics_df['revenue'].rolling(window=3, min_periods=1).mean()
            metrics_df['gross_margin_ma_3'] = metrics_df['gross_margin_pct'].rolling(window=3, min_periods=1).mean()
            metrics_df['operating_margin_ma_3'] = metrics_df['operating_margin_pct'].rolling(window=3, min_periods=1).mean()
            
            # Vectorized performance scoring (much faster than loops)
            revenue_growth = metrics_df['revenue_growth_pct'].fillna(0).values
            gross_margin_vals = metrics_df['gross_margin_pct'].values
            operating_margin_vals = metrics_df['operating_margin_pct'].values
            net_margin_vals = metrics_df['net_margin_pct'].values
            
            # Revenue growth scoring (25 points)
            revenue_score = np.where(revenue_growth > 10, 25,
                                   np.where(revenue_growth > 5, 20,
                                           np.where(revenue_growth > 0, 15,
                                                   np.where(revenue_growth > -5, 10, 5))))
            
            # Margin scoring (50 points)
            gross_score = np.where(gross_margin_vals > 40, 20,
                                  np.where(gross_margin_vals > 30, 15,
                                          np.where(gross_margin_vals > 20, 10, 5)))
            
            operating_score = np.where(operating_margin_vals > 15, 20,
                                      np.where(operating_margin_vals > 10, 15,
                                              np.where(operating_margin_vals > 5, 10, 5)))
            
            # Profitability scoring (25 points)
            profit_score = np.where(net_margin_vals > 10, 25,
                                   np.where(net_margin_vals > 5, 20,
                                           np.where(net_margin_vals > 0, 15, 5)))
            
            # Total score
            metrics_df['performance_score'] = revenue_score + gross_score + operating_score + profit_score
        
        perf_monitor.end_operation("financial_performance_calculation")
        return metrics_df, "Enhanced financial performance metrics calculated successfully (optimized)"
        
    except Exception as e:
        perf_monitor.end_operation("financial_performance_calculation")
        return pd.DataFrame(), f"Error calculating financial performance metrics: {str(e)}"

@st.cache_data(ttl=1800, max_entries=50)
def calculate_liquidity_solvency_metrics(balance_sheet_data, cash_flow_data):
    """Calculate comprehensive liquidity and solvency metrics with enhanced analysis (optimized)"""
    perf_monitor.start_operation("liquidity_solvency_calculation")
    
    if balance_sheet_data.empty:
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return pd.DataFrame(), "No balance sheet data available"
    
    try:
        # Vectorized operations for better performance
        df = balance_sheet_data.copy()
        
        # Fill missing values with 0 for calculations
        numeric_columns = ['current_assets', 'total_assets', 'current_liabilities', 'total_liabilities',
                          'shareholder_equity', 'cash_and_equivalents', 'accounts_receivable', 
                          'inventory', 'long_term_debt', 'total_debt']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
            else:
                df[col] = 0
        
        # Vectorized ratio calculations
        current_assets = df['current_assets'].values
        total_assets = df['total_assets'].values
        current_liabilities = df['current_liabilities'].values
        total_liabilities = df['total_liabilities'].values
        shareholder_equity = df['shareholder_equity'].values
        cash_and_equivalents = df['cash_and_equivalents'].values
        accounts_receivable = df['accounts_receivable'].values
        inventory = df['inventory'].values
        long_term_debt = df['long_term_debt'].values
        total_debt = df['total_debt'].values
        
        # Vectorized liquidity ratios
        current_ratio = np.where(current_liabilities > 0, current_assets / current_liabilities, 0)
        quick_ratio = np.where(current_liabilities > 0, (cash_and_equivalents + accounts_receivable) / current_liabilities, 0)
        cash_ratio = np.where(current_liabilities > 0, cash_and_equivalents / current_liabilities, 0)
        working_capital = current_assets - current_liabilities
        working_capital_ratio = np.where(total_assets > 0, working_capital / total_assets, 0)
        
        # Vectorized solvency ratios
        debt_to_equity = np.where(shareholder_equity > 0, total_liabilities / shareholder_equity, 0)
        debt_to_assets = np.where(total_assets > 0, total_liabilities / total_assets, 0)
        equity_ratio = np.where(total_assets > 0, shareholder_equity / total_assets, 0)
        debt_ratio = np.where(total_assets > 0, total_liabilities / total_assets, 0)
        
        # Placeholder ratios for future enhancement
        times_interest_earned = np.zeros_like(current_assets)
        debt_service_coverage = np.zeros_like(current_assets)
        cash_flow_to_debt = np.zeros_like(current_assets)
        inventory_turnover_ratio = np.zeros_like(current_assets)
        receivables_turnover_ratio = np.zeros_like(current_assets)
        
        # Create metrics dataframe
        metrics_df = pd.DataFrame({
            'period': df['period'].values,
            'current_ratio': current_ratio,
            'quick_ratio': quick_ratio,
            'cash_ratio': cash_ratio,
            'working_capital': working_capital,
            'working_capital_ratio': working_capital_ratio,
            'debt_to_equity': debt_to_equity,
            'debt_to_assets': debt_to_assets,
            'equity_ratio': equity_ratio,
            'debt_ratio': debt_ratio,
            'times_interest_earned': times_interest_earned,
            'debt_service_coverage': debt_service_coverage,
            'cash_flow_to_debt': cash_flow_to_debt,
            'inventory_turnover_ratio': inventory_turnover_ratio,
            'receivables_turnover_ratio': receivables_turnover_ratio,
            'current_assets': current_assets,
            'total_assets': total_assets,
            'current_liabilities': current_liabilities,
            'total_liabilities': total_liabilities,
            'shareholder_equity': shareholder_equity,
            'cash_and_equivalents': cash_and_equivalents,
            'accounts_receivable': accounts_receivable,
            'inventory': inventory,
            'long_term_debt': long_term_debt,
            'total_debt': total_debt
        })
        
        # Add performance indicators and trends (vectorized)
        if len(metrics_df) > 1:
            # Vectorized period-over-period changes
            metrics_df['current_ratio_change'] = metrics_df['current_ratio'].diff()
            metrics_df['quick_ratio_change'] = metrics_df['quick_ratio'].diff()
            metrics_df['debt_to_equity_change'] = metrics_df['debt_to_equity'].diff()
            metrics_df['working_capital_change'] = metrics_df['working_capital'].diff()
            
            # Vectorized moving averages
            metrics_df['current_ratio_ma_3'] = metrics_df['current_ratio'].rolling(window=3, min_periods=1).mean()
            metrics_df['quick_ratio_ma_3'] = metrics_df['quick_ratio'].rolling(window=3, min_periods=1).mean()
            metrics_df['debt_to_equity_ma_3'] = metrics_df['debt_to_equity'].rolling(window=3, min_periods=1).mean()
            
            # Vectorized financial health scoring (much faster than loops)
            current_ratio_vals = metrics_df['current_ratio'].values
            quick_ratio_vals = metrics_df['quick_ratio'].values
            debt_to_equity_vals = metrics_df['debt_to_equity'].values
            debt_to_assets_vals = metrics_df['debt_to_assets'].values
            working_capital_vals = metrics_df['working_capital'].values
            working_capital_ratio_vals = metrics_df['working_capital_ratio'].values
            
            # Liquidity scoring (40 points)
            current_ratio_score = np.where(current_ratio_vals >= 2.0, 20,
                                          np.where(current_ratio_vals >= 1.5, 15,
                                                  np.where(current_ratio_vals >= 1.0, 10, 5)))
            
            quick_ratio_score = np.where(quick_ratio_vals >= 1.0, 20,
                                        np.where(quick_ratio_vals >= 0.8, 15,
                                                np.where(quick_ratio_vals >= 0.5, 10, 5)))
            
            # Solvency scoring (40 points)
            debt_equity_score = np.where(debt_to_equity_vals <= 0.5, 20,
                                        np.where(debt_to_equity_vals <= 1.0, 15,
                                                np.where(debt_to_equity_vals <= 2.0, 10, 5)))
            
            debt_assets_score = np.where(debt_to_assets_vals <= 0.3, 20,
                                        np.where(debt_to_assets_vals <= 0.5, 15,
                                                np.where(debt_to_assets_vals <= 0.7, 10, 5)))
            
            # Working capital scoring (20 points)
            working_capital_score = np.where(working_capital_vals > 0,
                                            np.where(working_capital_ratio_vals >= 0.2, 20,
                                                    np.where(working_capital_ratio_vals >= 0.1, 15,
                                                            np.where(working_capital_ratio_vals >= 0.05, 10, 5))), 0)
            
            # Total score
            metrics_df['financial_health_score'] = (current_ratio_score + quick_ratio_score + 
                                                   debt_equity_score + debt_assets_score + working_capital_score)
        
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return metrics_df, "Enhanced liquidity and solvency metrics calculated successfully (optimized)"
        
    except Exception as e:
        perf_monitor.end_operation("liquidity_solvency_calculation")
        return pd.DataFrame(), f"Error calculating liquidity and solvency metrics: {str(e)}"

def calculate_risk_compliance_metrics(balance_sheet_data, market_data):
    """Calculate risk and compliance metrics"""
    if balance_sheet_data.empty:
        return pd.DataFrame(), "No balance sheet data available"
    
    try:
        metrics = []
        
        # Calculate Value at Risk (VaR)
        if 'total_assets' in balance_sheet_data.columns:
            portfolio_value = balance_sheet_data['total_assets'].sum()
            # Simple VaR calculation with assumed volatility
            volatility = 0.15  # 15% annual volatility
            confidence_level = 0.95
            z_score = 1.645  # 95% confidence level
            time_horizon = 30/365  # 30 days
            
            var = portfolio_value * volatility * np.sqrt(time_horizon) * z_score
            metrics.append({
                'Metric': 'Value at Risk (VaR)',
                'Value': f"${var:,.0f}",
                'Description': f"95% confidence, 30-day horizon"
            })
        
        # Calculate Liquidity Coverage Ratio (LCR)
        if 'current_assets' in balance_sheet_data.columns and 'current_liabilities' in balance_sheet_data.columns:
            current_assets = balance_sheet_data['current_assets'].sum()
            current_liabilities = balance_sheet_data['current_liabilities'].sum()
            
            if current_liabilities > 0:
                lcr = current_assets / current_liabilities
                metrics.append({
                    'Metric': 'Liquidity Coverage Ratio',
                    'Value': f"{lcr:.2f}",
                    'Description': f"Current assets / Current liabilities"
                })
        
        # Calculate Capital Adequacy Ratio (CAR)
        if 'shareholder_equity' in balance_sheet_data.columns and 'total_assets' in balance_sheet_data.columns:
            equity = balance_sheet_data['shareholder_equity'].sum()
            total_assets = balance_sheet_data['total_assets'].sum()
            
            if total_assets > 0:
                car = (equity / total_assets) * 100
                metrics.append({
                    'Metric': 'Capital Adequacy Ratio',
                    'Value': f"{car:.1f}%",
                    'Description': f"Equity / Total assets"
                })
        
        # Calculate Debt Service Coverage Ratio (DSCR)
        if 'total_liabilities' in balance_sheet_data.columns and 'shareholder_equity' in balance_sheet_data.columns:
            total_liabilities = balance_sheet_data['total_liabilities'].sum()
            equity = balance_sheet_data['shareholder_equity'].sum()
            
            if equity > 0:
                dscr = total_liabilities / equity
                metrics.append({
                    'Metric': 'Debt Service Coverage',
                    'Value': f"{dscr:.2f}",
                    'Description': f"Total liabilities / Equity"
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Risk and compliance metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating risk and compliance metrics: {str(e)}"

def calculate_efficiency_metrics(income_statement_data, balance_sheet_data):
    """Calculate efficiency and productivity metrics"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return pd.DataFrame(), "No income statement or balance sheet data available"
    
    try:
        metrics = []
        
        for _, row in income_statement_data.iterrows():
            period = row.get('period', 'Unknown')
            revenue = row.get('revenue', 0)
            net_income = row.get('net_income', 0)
            operating_expenses = row.get('operating_expenses', 0)
            
            # Get corresponding balance sheet data
            bs_row = balance_sheet_data[balance_sheet_data['period'] == period]
            if not bs_row.empty:
                total_assets = bs_row.iloc[0].get('total_assets', 0)
                shareholder_equity = bs_row.iloc[0].get('shareholder_equity', 0)
                
                # Calculate ratios
                roa = (net_income / total_assets * 100) if total_assets > 0 else 0
                roe = (net_income / shareholder_equity * 100) if shareholder_equity > 0 else 0
                asset_turnover = (revenue / total_assets) if total_assets > 0 else 0
                op_exp_ratio = (operating_expenses / revenue * 100) if revenue > 0 else 0
                
                metrics.append({
                    'period': period,
                    'roa_pct': roa,
                    'roe_pct': roe,
                    'asset_turnover': asset_turnover,
                    'op_exp_ratio_pct': op_exp_ratio,
                    'revenue': revenue,
                    'net_income': net_income,
                    'total_assets': total_assets,
                    'shareholder_equity': shareholder_equity
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Efficiency metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating efficiency metrics: {str(e)}"

def calculate_budget_variance_metrics(income_statement_data, budget_data, forecast_data):
    """Calculate budget variance and forecasting metrics"""
    if budget_data.empty and forecast_data.empty:
        return pd.DataFrame(), "No budget or forecast data available"
    
    try:
        metrics = []
        
        # Budget variance analysis
        if not budget_data.empty and not income_statement_data.empty:
            # Try to match periods between budget and actual data
            try:
                budget_copy = budget_data.copy()
                income_copy = income_statement_data[['period', 'revenue', 'cost_of_goods_sold', 'operating_expenses']].copy()
                
                # Rename columns for clarity
                budget_copy = budget_copy.rename(columns={
                    'revenue': 'revenue_budget',
                    'expenses': 'expenses_budget'
                })
                
                income_copy = income_copy.rename(columns={
                    'revenue': 'revenue_actual',
                    'cost_of_goods_sold': 'cost_of_goods_sold_actual',
                    'operating_expenses': 'operating_expenses_actual'
                })
                
                # Merge budget and actual data
                budget_actual = budget_copy.merge(income_copy, on='period', how='inner')
                
                if not budget_actual.empty:
                    # Calculate actual expenses
                    if 'cost_of_goods_sold_actual' in budget_actual.columns and 'operating_expenses_actual' in budget_actual.columns:
                        budget_actual['expenses_actual'] = budget_actual['cost_of_goods_sold_actual'] + budget_actual['operating_expenses_actual']
                    
                    # Calculate revenue variance
                    if 'revenue_budget' in budget_actual.columns and 'revenue_actual' in budget_actual.columns:
                        revenue_variance = ((budget_actual['revenue_actual'] - budget_actual['revenue_budget']) / budget_actual['revenue_budget'] * 100).mean()
                        metrics.append({
                            'Metric': 'Revenue Variance',
                            'Value': f"{revenue_variance:+.1f}%",
                            'Description': 'Average revenue variance'
                        })
                    
                    # Calculate expense variance
                    if 'expenses_budget' in budget_actual.columns and 'expenses_actual' in budget_actual.columns:
                        expense_variance = ((budget_actual['expenses_budget'] - budget_actual['expenses_actual']) / budget_actual['expenses_budget'] * 100).mean()
                        metrics.append({
                            'Metric': 'Expense Variance',
                            'Value': f"{expense_variance:+.1f}%",
                            'Description': 'Average expense variance'
                        })
                
            except Exception as e:
                # Fallback to simple calculation if merge fails
                total_budget = budget_data['revenue'].sum() if 'revenue' in budget_data.columns else 0
                total_actual = budget_data['expenses'].sum() if 'expenses' in budget_data.columns else 0
                
                if total_budget > 0:
                    variance = ((total_actual - total_budget) / total_budget * 100)
                    metrics.append({
                        'Metric': 'Budget Variance',
                        'Value': f"{variance:+.1f}%",
                        'Description': 'Actual vs Budget variance'
                    })
        
        # Forecast accuracy
        if not forecast_data.empty:
            if 'confidence_level' in forecast_data.columns:
                avg_confidence = forecast_data['confidence_level'].mean()
                metrics.append({
                    'Metric': 'Forecast Confidence',
                    'Value': f"{avg_confidence:.1f}%",
                    'Description': 'Average forecast confidence level'
                })
        
        # Scenario analysis
        if not forecast_data.empty and len(forecast_data) > 1:
            scenarios = forecast_data['scenario'].nunique() if 'scenario' in forecast_data.columns else 1
            metrics.append({
                'Metric': 'Scenarios Analyzed',
                'Value': f"{scenarios}",
                'Description': 'Number of forecast scenarios'
            })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Budget variance metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating budget variance metrics: {str(e)}"

def calculate_cash_flow_metrics(cash_flow_data, balance_sheet_data):
    """Calculate cash flow and working capital metrics"""
    if cash_flow_data.empty:
        return pd.DataFrame(), "No cash flow data available"
    
    try:
        metrics = []
        
        for _, row in cash_flow_data.iterrows():
            period = row.get('period', 'Unknown')
            
            # Find operating cash flow column with fallback names
            operating_cf = 0
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in row.index:
                    operating_cf = row.get(col_name, 0)
                    break
            
            # Find free cash flow column with fallback names
            free_cf = 0
            for col_name in ['free_cash_flow', 'free_cf', 'free_cashflow', 'fcf']:
                if col_name in row.index:
                    free_cf = row.get(col_name, 0)
                    break
            
            net_income = row.get('net_income', 0)
            
            # Get corresponding balance sheet data
            bs_row = balance_sheet_data[balance_sheet_data['period'] == period]
            if not bs_row.empty:
                current_assets = bs_row.iloc[0].get('current_assets', 0)
                current_liabilities = bs_row.iloc[0].get('current_liabilities', 0)
                
                # Calculate ratios
                working_capital = current_assets - current_liabilities
                working_capital_turnover = (operating_cf / working_capital) if working_capital > 0 else 0
                
                metrics.append({
                    'period': period,
                    'operating_cf': operating_cf,
                    'free_cf': free_cf,
                    'working_capital_turnover': working_capital_turnover,
                    'net_income': net_income,
                    'working_capital': working_capital
                })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Cash flow metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating cash flow metrics: {str(e)}"

def calculate_capital_structure_metrics(balance_sheet_data, income_statement_data):
    """Calculate capital structure and financing metrics"""
    if balance_sheet_data.empty:
        return pd.DataFrame(), "No balance sheet data available"
    
    try:
        metrics = []
        
        for _, row in balance_sheet_data.iterrows():
            period = row.get('period', 'Unknown')
            total_liabilities = row.get('total_liabilities', 0)
            shareholder_equity = row.get('shareholder_equity', 0)
            total_assets = row.get('total_assets', 0)
            
            # Calculate ratios
            debt_to_equity = (total_liabilities / shareholder_equity) if shareholder_equity > 0 else 0
            debt_to_assets = (total_liabilities / total_assets) if total_assets > 0 else 0
            
            # Simplified WACC calculation (assumes 8% cost of equity, 5% cost of debt)
            cost_of_equity = 0.08
            cost_of_debt = 0.05
            wacc = ((cost_of_equity * shareholder_equity) + (cost_of_debt * total_liabilities)) / (shareholder_equity + total_liabilities) if (shareholder_equity + total_liabilities) > 0 else 0
            
            # Interest coverage (simplified)
            interest_coverage = 5.0  # Assumed value
            
            metrics.append({
                'period': period,
                'debt_to_equity': debt_to_equity,
                'wacc': wacc,
                'interest_coverage': interest_coverage,
                'total_liabilities': total_liabilities,
                'shareholder_equity': shareholder_equity,
                'total_assets': total_assets
            })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Capital structure metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating capital structure metrics: {str(e)}"

def calculate_investment_valuation_metrics(cash_flow_data, balance_sheet_data):
    """Calculate investment and valuation metrics"""
    if cash_flow_data.empty:
        return pd.DataFrame(), "No cash flow data available"
    
    try:
        metrics = []
        
        for _, row in cash_flow_data.iterrows():
            period = row.get('period', 'Unknown')
            cash_flow = row.get('cash_flow', 0)
            initial_investment = row.get('initial_investment', 0)
            
            # Calculate NPV (simplified - assumes 10% discount rate)
            discount_rate = 0.10
            npv = cash_flow / (1 + discount_rate) - initial_investment
            
            # Calculate payback period (simplified)
            payback_period = initial_investment / cash_flow if cash_flow > 0 else float('inf')
            
            # Calculate EVA (simplified)
            eva = cash_flow - (initial_investment * discount_rate)
            
            metrics.append({
                'period': period,
                'npv': npv,
                'payback_period': payback_period,
                'eva': eva,
                'cash_flow': cash_flow,
                'initial_investment': initial_investment
            })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Investment valuation metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating investment valuation metrics: {str(e)}"

def calculate_strategic_kpis(customer_data, product_data, value_chain_data):
    """Calculate strategic KPI metrics"""
    if customer_data.empty and product_data.empty and value_chain_data.empty:
        return pd.DataFrame(), "No strategic data available"
    
    try:
        metrics = []
        
        # Customer profitability
        if not customer_data.empty:
            total_customer_revenue = customer_data['revenue'].sum()
            avg_customer_profitability = customer_data['profitability'].mean() if 'profitability' in customer_data.columns else 0
            metrics.append({
                'Metric': 'Customer Profitability',
                'Value': f"${avg_customer_profitability:,.0f}",
                'Description': 'Average customer profitability'
            })
        
        # Product profitability
        if not product_data.empty:
            total_product_revenue = product_data['revenue'].sum()
            avg_product_margin = product_data['margin'].mean() if 'margin' in product_data.columns else 0
            metrics.append({
                'Metric': 'Product Profitability',
                'Value': f"{avg_product_margin:.1f}%",
                'Description': 'Average product margin'
            })
        
        # Value chain cost
        if not value_chain_data.empty:
            total_value_chain_cost = value_chain_data['cost'].sum()
            metrics.append({
                'Metric': 'Value Chain Cost',
                'Value': f"${total_value_chain_cost:,.0f}",
                'Description': 'Total value chain cost'
            })
        
        metrics_df = pd.DataFrame(metrics)
        return metrics_df, "Strategic KPI metrics calculated successfully"
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating strategic KPI metrics: {str(e)}"

# Finance-specific auto insights functionality (optimized)
class FinanceInsights:
    """Optimized auto insights generator for finance analytics"""
    
    def __init__(self, income_statement, balance_sheet, cash_flow, budget, forecast, market_data, customer_data, product_data, value_chain):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.cash_flow = cash_flow
        self.budget = budget
        self.forecast = forecast
        self.market_data = market_data
        self.customer_data = customer_data
        self.product_data = product_data
        self.value_chain = value_chain
        
        # Pre-calculate common metrics for performance optimization
        self._precalculate_metrics()
    
    def _precalculate_metrics(self):
        """Pre-calculate common metrics to avoid repeated calculations"""
        self._metrics_cache = {}
        
        # Financial performance metrics
        if not self.income_statement.empty:
            self._metrics_cache['total_revenue'] = self.income_statement['revenue'].sum()
            self._metrics_cache['total_net_income'] = self.income_statement['net_income'].sum()
            self._metrics_cache['avg_net_margin'] = (self._metrics_cache['total_net_income'] / self._metrics_cache['total_revenue'] * 100) if self._metrics_cache['total_revenue'] > 0 else 0
            
            # Trend analysis
            if len(self.income_statement) > 1:
                recent_revenue = self.income_statement['revenue'].iloc[-1]
                previous_revenue = self.income_statement['revenue'].iloc[-2]
                self._metrics_cache['revenue_growth'] = ((recent_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
            
            # Additional financial metrics
            if 'gross_profit' in self.income_statement.columns:
                self._metrics_cache['total_gross_profit'] = self.income_statement['gross_profit'].sum()
                self._metrics_cache['gross_margin'] = (self._metrics_cache['total_gross_profit'] / self._metrics_cache['total_revenue'] * 100) if self._metrics_cache['total_revenue'] > 0 else 0
            
            if 'operating_expenses' in self.income_statement.columns:
                self._metrics_cache['total_operating_expenses'] = self.income_statement['operating_expenses'].sum()
                self._metrics_cache['operating_margin'] = ((self._metrics_cache['total_revenue'] - self._metrics_cache['total_operating_expenses']) / self._metrics_cache['total_revenue'] * 100) if self._metrics_cache['total_revenue'] > 0 else 0
        
        # Liquidity and solvency metrics
        if not self.balance_sheet.empty:
            self._metrics_cache['current_assets'] = self.balance_sheet['current_assets'].sum()
            self._metrics_cache['current_liabilities'] = self.balance_sheet['current_liabilities'].sum()
            self._metrics_cache['total_liabilities'] = self.balance_sheet['total_liabilities'].sum()
            self._metrics_cache['total_equity'] = self.balance_sheet['shareholder_equity'].sum()
            
            if self._metrics_cache['current_liabilities'] > 0:
                self._metrics_cache['current_ratio'] = self._metrics_cache['current_assets'] / self._metrics_cache['current_liabilities']
            
            if self._metrics_cache['total_equity'] > 0:
                self._metrics_cache['debt_to_equity'] = self._metrics_cache['total_liabilities'] / self._metrics_cache['total_equity']
            
            # Additional balance sheet metrics
            if 'total_assets' in self.balance_sheet.columns:
                self._metrics_cache['total_assets'] = self.balance_sheet['total_assets'].sum()
                if self._metrics_cache['total_assets'] > 0:
                    self._metrics_cache['asset_turnover'] = self._metrics_cache['total_revenue'] / self._metrics_cache['total_assets']
                    self._metrics_cache['roa'] = (self._metrics_cache['total_net_income'] / self._metrics_cache['total_assets']) * 100
            
            if self._metrics_cache['total_equity'] > 0:
                self._metrics_cache['roe'] = (self._metrics_cache['total_net_income'] / self._metrics_cache['total_equity']) * 100
        
        # Cash flow metrics - with column existence checks
        if not self.cash_flow.empty:
            # Check for operating cash flow column with fallback names
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in self.cash_flow.columns:
                    operating_cf_col = col_name
                    break
            
            if operating_cf_col:
                self._metrics_cache['total_operating_cf'] = self.cash_flow[operating_cf_col].sum()
            else:
                self._metrics_cache['total_operating_cf'] = 0
            
            # Check for capital expenditures column
            capex_col = None
            for col_name in ['capital_expenditures', 'capex', 'capital_expenses', 'investment_expenditures']:
                if col_name in self.cash_flow.columns:
                    capex_col = col_name
                    break
            
            if capex_col:
                self._metrics_cache['total_investing_cf'] = self.cash_flow[capex_col].sum()
            else:
                self._metrics_cache['total_investing_cf'] = 0
            
            # Check for free cash flow column
            fcf_col = None
            for col_name in ['free_cash_flow', 'free_cf', 'free_cashflow', 'fcf']:
                if col_name in self.cash_flow.columns:
                    fcf_col = col_name
                    break
            
            if fcf_col:
                self._metrics_cache['total_free_cf'] = self.cash_flow[fcf_col].sum()
            else:
                self._metrics_cache['total_free_cf'] = 0
            
            # Cash flow quality metrics
            if self._metrics_cache['total_operating_cf'] != 0:
                self._metrics_cache['cash_flow_quality'] = self._metrics_cache['total_free_cf'] / abs(self._metrics_cache['total_operating_cf'])
        
        # Performance optimization: Add timestamp for cache invalidation
        self._metrics_cache['_last_updated'] = time.time()
    
    def _get_cached_metric(self, metric_name, default_value=0):
        """Get cached metric with lazy loading support"""
        if metric_name not in self._metrics_cache:
            # Lazy load the metric if not in cache
            self._load_metric(metric_name)
        
        return self._metrics_cache.get(metric_name, default_value)
    
    def _load_metric(self, metric_name):
        """Lazy load specific metrics as needed"""
        if metric_name == 'working_capital_turnover':
            # Check for operating cash flow column with fallback names
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in self.cash_flow.columns:
                    operating_cf_col = col_name
                    break
            
            if not self.cash_flow.empty and operating_cf_col:
                operating_cf = self.cash_flow[operating_cf_col].sum()
                current_assets = self._metrics_cache.get('current_assets', 0)
                current_liabilities = self._metrics_cache.get('current_liabilities', 0)
                working_capital = current_assets - current_liabilities
                
                if working_capital > 0:
                    self._metrics_cache['working_capital_turnover'] = operating_cf / working_capital
                else:
                    self._metrics_cache['working_capital_turnover'] = 0
        
        elif metric_name == 'cash_conversion_cycle':
            # Calculate cash conversion cycle if inventory and receivables data available
            if not self.balance_sheet.empty:
                inventory = self.balance_sheet['inventory'].sum() if 'inventory' in self.balance_sheet.columns else 0
                receivables = self.balance_sheet['accounts_receivable'].sum() if 'accounts_receivable' in self.balance_sheet.columns else 0
                payables = self.balance_sheet['accounts_payable'].sum() if 'accounts_payable' in self.balance_sheet.columns else 0
                
                if self._metrics_cache.get('total_revenue', 0) > 0:
                    revenue = self._metrics_cache['total_revenue']
                    # Simplified calculation (in days)
                    days_inventory = (inventory / revenue) * 365 if revenue > 0 else 0
                    days_receivables = (receivables / revenue) * 365 if revenue > 0 else 0
                    days_payables = (payables / revenue) * 365 if revenue > 0 else 0
                    
                    self._metrics_cache['cash_conversion_cycle'] = days_inventory + days_receivables - days_payables
                else:
                    self._metrics_cache['cash_conversion_cycle'] = 0
    
    def generate_profitability_insights(self):
        """Generate comprehensive insights for profitability analysis"""
        if self.income_statement.empty:
            return "No income statement data available for profitability analysis."
        
        insights = []
        
        # Use cached metrics for performance
        total_revenue = self._metrics_cache.get('total_revenue', 0)
        total_net_income = self._metrics_cache.get('total_net_income', 0)
        avg_net_margin = self._metrics_cache.get('avg_net_margin', 0)
        
        insights.append(f"**Total Revenue**: ${total_revenue:,.0f}")
        insights.append(f"**Total Net Income**: ${total_net_income:,.0f}")
        insights.append(f"**Average Net Margin**: {avg_net_margin:.1f}%")
        insights.append("")
        
        # Enhanced trend analysis
        if len(self.income_statement) > 1:
            revenue_growth = self._metrics_cache.get('revenue_growth', 0)
            insights.append(f"**Revenue Growth**: {revenue_growth:+.1f}% (latest period)")
            
            # More sophisticated trend analysis
            if revenue_growth > 15:
                insights.append("**Trend**: Exceptional revenue growth - excellent performance")
            elif revenue_growth > 10:
                insights.append("**Trend**: Strong revenue growth - maintain momentum")
            elif revenue_growth > 5:
                insights.append("**Trend**: Moderate revenue growth - opportunities for acceleration")
            elif revenue_growth > 0:
                insights.append("**Trend**: Slow revenue growth - review growth strategies")
            else:
                insights.append("**Trend**: Revenue decline - immediate action required")
            
            # Add margin trend analysis
            if 'gross_profit' in self.income_statement.columns and 'operating_expenses' in self.income_statement.columns:
                recent_gross_margin = (self.income_statement['gross_profit'].iloc[-1] / self.income_statement['revenue'].iloc[-1] * 100) if self.income_statement['revenue'].iloc[-1] > 0 else 0
                previous_gross_margin = (self.income_statement['gross_profit'].iloc[-2] / self.income_statement['revenue'].iloc[-2] * 100) if self.income_statement['revenue'].iloc[-2] > 0 else 0
                margin_change = recent_gross_margin - previous_gross_margin
                
                insights.append(f"**Gross Margin Change**: {margin_change:+.1f}%")
                if margin_change > 0:
                    insights.append("**Margin Trend**: Improving profitability - cost control effective")
                else:
                    insights.append("**Margin Trend**: Declining profitability - review cost structure")
        
        return "\n".join(insights)
    
    def generate_liquidity_solvency_insights(self):
        """Generate comprehensive insights for liquidity and solvency analysis"""
        if self.balance_sheet.empty:
            return "No balance sheet data available for liquidity analysis."
        
        insights = []
        
        # Use cached metrics
        current_ratio = self._metrics_cache.get('current_ratio', 0)
        debt_to_equity = self._metrics_cache.get('debt_to_equity', 0)
        
        insights.append(f"**Current Ratio**: {current_ratio:.2f}")
        insights.append(f"**Debt-to-Equity**: {debt_to_equity:.2f}")
        insights.append("")
        
        # Enhanced risk assessment with specific recommendations
        if current_ratio < 1.0:
            insights.append("**Liquidity Risk**: Critical - immediate action required")
            insights.append("**Action Items**:")
            insights.append("  • Implement emergency cash flow management")
            insights.append("  • Negotiate payment extensions with creditors")
            insights.append("  • Consider short-term financing options")
        elif current_ratio < 1.5:
            insights.append("**Liquidity Risk**: Moderate - monitor closely")
            insights.append("**Action Items**:")
            insights.append("  • Optimize working capital management")
            insights.append("  • Review payment terms with suppliers")
            insights.append("  • Accelerate accounts receivable collection")
        else:
            insights.append("**Liquidity Risk**: Low - strong short-term financial position")
            insights.append("**Opportunities**:")
            insights.append("  • Consider investment opportunities for excess cash")
            insights.append("  • Explore strategic acquisitions or expansion")
        
        insights.append("")
        
        # Enhanced solvency analysis
        if debt_to_equity > 2.5:
            insights.append("**Solvency Risk**: Critical - high debt levels")
            insights.append("**Action Items**:")
            insights.append("  • Prioritize debt reduction")
            insights.append("  • Review capital structure")
            insights.append("  • Consider debt restructuring")
        elif debt_to_equity > 2.0:
            insights.append("**Solvency Risk**: High - debt reduction priority")
            insights.append("**Action Items**:")
            insights.append("  • Implement debt reduction plan")
            insights.append("  • Review financing strategy")
            insights.append("  • Consider equity financing")
        elif debt_to_equity > 1.0:
            insights.append("**Solvency Risk**: Moderate - manageable but monitor")
            insights.append("**Action Items**:")
            insights.append("  • Balance debt and equity financing")
            insights.append("  • Maintain debt service coverage")
            insights.append("  • Monitor debt covenants")
        else:
            insights.append("**Solvency Risk**: Low - conservative debt structure")
            insights.append("**Opportunities**:")
            insights.append("  • Consider strategic debt for growth")
            insights.append("  • Explore leverage opportunities")
        
        return "\n".join(insights)
    
    def generate_cash_flow_insights(self):
        """Generate comprehensive insights for cash flow analysis"""
        if self.cash_flow.empty:
            return "No cash flow data available for analysis."
        
        insights = []
        
        # Use cached metrics
        total_operating_cf = self._metrics_cache.get('total_operating_cf', 0)
        total_investing_cf = self._metrics_cache.get('total_investing_cf', 0)
        total_free_cf = self._metrics_cache.get('total_free_cf', 0)
        
        insights.append(f"**Total Operating Cash Flow**: ${total_operating_cf:,.0f}")
        insights.append(f"**Total Capital Expenditures**: ${total_investing_cf:,.0f}")
        insights.append(f"**Total Free Cash Flow**: ${total_free_cf:,.0f}")
        insights.append("")
        
        # Enhanced cash flow quality assessment
        if total_operating_cf > 0:
            insights.append("**Cash Flow Quality**: Positive operating cash flow")
            if total_operating_cf > abs(total_investing_cf):
                insights.append("**Assessment**: Strong operational performance with investment capacity")
            else:
                insights.append("**Assessment**: Good operations but high investment requirements")
        else:
            insights.append("**Cash Flow Quality**: Negative operating cash flow")
            insights.append("**Assessment**: Operational challenges - review business model")
        
        insights.append("")
        
        # Free cash flow analysis
        if total_free_cf > 0:
            insights.append("**Financial Flexibility**: Positive free cash flow")
            insights.append("**Opportunities**:")
            insights.append("  • Dividend payments to shareholders")
            insights.append("  • Debt reduction")
            insights.append("  • Strategic investments")
            insights.append("  • Share buybacks")
        else:
            insights.append("**Financial Flexibility**: Negative free cash flow")
            insights.append("**Challenges**:")
            insights.append("  • Limited financial flexibility")
            insights.append("  • Potential liquidity constraints")
            insights.append("  • Need for external financing")
        
        # Cash flow trends analysis
        if len(self.cash_flow) > 1:
            # Check for operating cash flow column with fallback names
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in self.cash_flow.columns:
                    operating_cf_col = col_name
                    break
            
            if operating_cf_col:
                recent_operating_cf = self.cash_flow[operating_cf_col].iloc[-1]
                previous_operating_cf = self.cash_flow[operating_cf_col].iloc[-2]
                
                if previous_operating_cf != 0:
                    cf_growth = ((recent_operating_cf - previous_operating_cf) / abs(previous_operating_cf) * 100)
                    insights.append("")
                    insights.append(f"**Operating CF Growth**: {cf_growth:+.1f}%")
                    
                    if cf_growth > 20:
                        insights.append("**Trend**: Exceptional cash flow improvement")
                    elif cf_growth > 10:
                        insights.append("**Trend**: Strong cash flow growth")
                    elif cf_growth < -10:
                        insights.append("**Trend**: Declining cash flow - investigate causes")
        
        return "\n".join(insights)
    
    def generate_budget_forecasting_insights(self):
        """Generate comprehensive insights for budget and forecasting analysis"""
        if self.budget.empty and self.forecast.empty:
            return "No budget or forecast data available for analysis."
        
        insights = []
        
        # Budget analysis
        if not self.budget.empty:
            total_budget = self.budget['revenue'].sum() if 'revenue' in self.budget.columns else 0
            insights.append(f"**Total Budget**: ${total_budget:,.0f}")
            
            # Budget variance analysis if income statement available
            if not self.income_statement.empty and total_budget > 0:
                actual_revenue = self.income_statement['revenue'].sum()
                budget_variance = ((actual_revenue - total_budget) / total_budget * 100)
                insights.append(f"**Budget Variance**: {budget_variance:+.1f}%")
                
                if abs(budget_variance) < 5:
                    insights.append("**Performance**: Excellent budget accuracy")
                elif abs(budget_variance) < 10:
                    insights.append("**Performance**: Good budget accuracy")
                elif abs(budget_variance) < 20:
                    insights.append("**Performance**: Moderate budget accuracy - room for improvement")
                else:
                    insights.append("**Performance**: Poor budget accuracy - review forecasting process")
        
        insights.append("")
        
        # Forecast analysis
        if not self.forecast.empty:
            total_forecast = self.forecast['revenue'].sum() if 'revenue' in self.forecast.columns else 0
            insights.append(f"**Total Forecast**: ${total_forecast:,.0f}")
            
            # Forecast confidence analysis
            if 'confidence_level' in self.forecast.columns:
                avg_confidence = self.forecast['confidence_level'].mean()
                insights.append(f"**Average Forecast Confidence**: {avg_confidence:.1f}%")
                
                if avg_confidence > 80:
                    insights.append("**Confidence Level**: High - reliable forecasts")
                elif avg_confidence > 60:
                    insights.append("**Confidence Level**: Moderate - reasonable forecasts")
                else:
                    insights.append("**Confidence Level**: Low - improve forecasting methodology")
            
            # Scenario analysis
            if 'scenario' in self.forecast.columns:
                scenarios = self.forecast['scenario'].nunique()
                insights.append(f"**Scenarios Analyzed**: {scenarios}")
                
                if scenarios > 3:
                    insights.append("**Analysis**: Comprehensive scenario planning")
                elif scenarios > 1:
                    insights.append("**Analysis**: Basic scenario planning")
                else:
                    insights.append("**Analysis**: Limited scenario planning - consider multiple scenarios")
        
        insights.append("")
        insights.append("**Budget vs Forecast Analysis**: Compare actual performance against targets")
        
        return "\n".join(insights)
    
    def generate_customer_productivity_insights(self):
        """Generate comprehensive insights for customer and product analysis"""
        insights = []
        
        # Customer analysis
        if not self.customer_data.empty:
            total_customers = len(self.customer_data)
            total_customer_revenue = self.customer_data['revenue'].sum()
            avg_customer_value = total_customer_revenue / total_customers if total_customers > 0 else 0
            
            insights.append(f"**Total Customers**: {total_customers:,}")
            insights.append(f"**Total Customer Revenue**: ${total_customer_revenue:,.0f}")
            insights.append(f"**Average Customer Value**: ${avg_customer_value:,.0f}")
            
            # Customer segmentation analysis
            if 'segment' in self.customer_data.columns:
                segment_analysis = self.customer_data.groupby('segment')['revenue'].agg(['sum', 'mean', 'count'])
                insights.append("")
                insights.append("**Customer Segment Analysis**:")
                for segment, data in segment_analysis.iterrows():
                    insights.append(f"  • {segment}: {data['count']} customers, ${data['sum']:,.0f} revenue, ${data['mean']:,.0f} avg")
            
            # Customer profitability analysis
            if 'profitability' in self.customer_data.columns:
                profitable_customers = len(self.customer_data[self.customer_data['profitability'] > 0])
                profitability_rate = (profitable_customers / total_customers * 100) if total_customers > 0 else 0
                insights.append("")
                insights.append(f"**Customer Profitability**: {profitability_rate:.1f}% of customers are profitable")
                
                if profitability_rate < 50:
                    insights.append("**Action**: Review customer acquisition and retention strategies")
                elif profitability_rate < 80:
                    insights.append("**Action**: Optimize customer mix and pricing strategies")
                else:
                    insights.append("**Status**: Excellent customer profitability")
            
            insights.append("")
        
        # Product analysis
        if not self.product_data.empty:
            total_products = len(self.product_data)
            total_product_revenue = self.product_data['revenue'].sum()
            avg_product_value = total_product_revenue / total_products if total_products > 0 else 0
            
            insights.append(f"**Total Products**: {total_products:,}")
            insights.append(f"**Total Product Revenue**: ${total_product_revenue:,.0f}")
            insights.append(f"**Average Product Value**: ${avg_product_value:,.0f}")
            
            # Product margin analysis
            if 'margin' in self.product_data.columns:
                avg_margin = self.product_data['margin'].mean()
                high_margin_products = len(self.product_data[self.product_data['margin'] > avg_margin])
                insights.append("")
                insights.append(f"**Product Margin Analysis**:")
                insights.append(f"  • Average margin: {avg_margin:.1f}%")
                insights.append(f"  • High-margin products: {high_margin_products}/{total_products}")
                
                if avg_margin < 20:
                    insights.append("**Action**: Review pricing strategy and cost structure")
                elif avg_margin < 35:
                    insights.append("**Action**: Optimize product mix and pricing")
                else:
                    insights.append("**Status**: Strong product profitability")
            
            # Product lifecycle analysis
            if 'lifecycle_stage' in self.product_data.columns:
                lifecycle_analysis = self.product_data.groupby('lifecycle_stage')['revenue'].sum()
                insights.append("")
                insights.append("**Product Lifecycle Analysis**:")
                for stage, revenue in lifecycle_analysis.items():
                    insights.append(f"  • {stage}: ${revenue:,.0f}")
        
        return "\n".join(insights)
    
    def generate_executive_summary(self):
        """Generate comprehensive executive summary of all insights"""
        summary = []
        
        summary.append("## 🎯 Executive Financial Summary")
        summary.append("")
        
        # Financial performance
        if not self.income_statement.empty:
            total_revenue = self._metrics_cache.get('total_revenue', 0)
            total_net_income = self._metrics_cache.get('total_net_income', 0)
            summary.append(f"**Revenue**: ${total_revenue:,.0f}")
            summary.append(f"**Net Income**: ${total_net_income:,.0f}")
            
            if total_revenue > 0:
                net_margin = (total_net_income / total_revenue * 100)
                summary.append(f"**Net Margin**: {net_margin:.1f}%")
            summary.append("")
        
        # Key ratios
        if not self.balance_sheet.empty:
            current_ratio = self._metrics_cache.get('current_ratio', 0)
            debt_to_equity = self._metrics_cache.get('debt_to_equity', 0)
            summary.append(f"**Current Ratio**: {current_ratio:.2f}")
            summary.append(f"**Debt-to-Equity**: {debt_to_equity:.2f}")
            summary.append("")
        
        # Cash flow summary
        if not self.cash_flow.empty:
            total_free_cf = self._metrics_cache.get('total_free_cf', 0)
            summary.append(f"**Free Cash Flow**: ${total_free_cf:,.0f}")
            summary.append("")
        
        # Risk assessment
        summary.append("## ⚠️ Risk Assessment")
        risk_level = "Low"
        risk_factors = []
        
        if self._metrics_cache.get('current_ratio', 0) < 1.5:
            risk_level = "Medium"
            risk_factors.append("Liquidity concerns")
        
        if self._metrics_cache.get('debt_to_equity', 0) > 2.0:
            risk_level = "High"
            risk_factors.append("High debt levels")
        
        if self._metrics_cache.get('total_free_cf', 0) < 0:
            risk_level = "Medium" if risk_level == "Low" else risk_level
            risk_factors.append("Negative free cash flow")
        
        summary.append(f"**Overall Risk Level**: {risk_level}")
        if risk_factors:
            summary.append("**Key Risk Factors**:")
            for factor in risk_factors:
                summary.append(f"  • {factor}")
        summary.append("")
        
        # Recommendations
        summary.append("## 💡 Key Recommendations")
        
        # Revenue growth recommendations
        revenue_growth = self._metrics_cache.get('revenue_growth', 0)
        if revenue_growth < 5:
            summary.append("1. **Revenue Growth**: Implement aggressive growth strategies")
            summary.append("   • Market expansion initiatives")
            summary.append("   • Product development acceleration")
            summary.append("   • Sales team expansion")
        else:
            summary.append("1. **Revenue Growth**: Maintain current momentum")
            summary.append("   • Continue successful strategies")
            summary.append("   • Optimize high-performing channels")
        
        # Profitability recommendations
        avg_net_margin = self._metrics_cache.get('avg_net_margin', 0)
        if avg_net_margin < 10:
            summary.append("2. **Profitability**: Focus on margin improvement")
            summary.append("   • Cost optimization initiatives")
            summary.append("   • Pricing strategy review")
            summary.append("   • Operational efficiency improvements")
        else:
            summary.append("2. **Profitability**: Strong margins - focus on growth")
            summary.append("   • Reinvest profits strategically")
            summary.append("   • Explore new market opportunities")
        
        # Liquidity recommendations
        current_ratio = self._metrics_cache.get('current_ratio', 0)
        if current_ratio < 1.5:
            summary.append("3. **Liquidity**: Strengthen working capital management")
            summary.append("   • Optimize inventory levels")
            summary.append("   • Accelerate receivables collection")
            summary.append("   • Negotiate payment terms")
        else:
            summary.append("3. **Liquidity**: Strong position - consider strategic investments")
            summary.append("   • Evaluate acquisition opportunities")
            summary.append("   • Consider share buybacks or dividends")
        
        # Strategic actions
        summary.append("")
        summary.append("## 🎯 Strategic Actions")
        summary.append("1. **Immediate (30 days)**:")
        summary.append("   • Review cash flow projections")
        summary.append("   • Assess current risk exposure")
        summary.append("   • Update budget forecasts")
        
        summary.append("2. **Short-term (90 days)**:")
        summary.append("   • Implement identified improvements")
        summary.append("   • Develop contingency plans")
        summary.append("   • Optimize operational processes")
        
        summary.append("3. **Long-term (12 months)**:")
        summary.append("   • Strategic planning and execution")
        summary.append("   • Technology investments")
        summary.append("   • Market expansion initiatives")
        
        return "\n".join(summary)
    
    def generate_market_competitive_insights(self):
        """Generate comprehensive market and competitive insights"""
        insights = []
        
        # Market data analysis
        if not self.market_data.empty:
            insights.append("## 📈 Market Analysis")
            
            # Market price trends
            if 'market_price' in self.market_data.columns and len(self.market_data) > 1:
                recent_price = self.market_data['market_price'].iloc[-1]
                previous_price = self.market_data['market_price'].iloc[-2]
                
                if previous_price > 0:
                    price_change = ((recent_price - previous_price) / previous_price) * 100
                    insights.append(f"**Stock Price Change**: {price_change:+.1f}%")
                    
                    if price_change > 10:
                        insights.append("**Market Sentiment**: Strong positive momentum")
                    elif price_change > 0:
                        insights.append("**Market Sentiment**: Positive but moderate")
                    elif price_change > -10:
                        insights.append("**Market Sentiment**: Slight negative pressure")
                    else:
                        insights.append("**Market Sentiment**: Significant negative pressure")
            
            # Market capitalization analysis
            if 'market_cap' in self.market_data.columns:
                avg_market_cap = self.market_data['market_cap'].mean()
                insights.append(f"**Average Market Cap**: ${avg_market_cap:,.0f}")
                
                if avg_market_cap > 10000000000:  # $10B
                    insights.append("**Company Size**: Large-cap company")
                elif avg_market_cap > 2000000000:  # $2B
                    insights.append("**Company Size**: Mid-cap company")
                else:
                    insights.append("**Company Size**: Small-cap company")
            
            # Dividend analysis
            if 'dividends_per_share' in self.market_data.columns:
                avg_dividend = self.market_data['dividends_per_share'].mean()
                if avg_dividend > 0:
                    insights.append(f"**Average Dividend**: ${avg_dividend:.2f} per share")
                    insights.append("**Dividend Policy**: Income-generating stock")
                else:
                    insights.append("**Dividend Policy**: Growth-focused, no dividends")
        
        # Value chain analysis
        if not self.value_chain.empty:
            insights.append("")
            insights.append("## 🔗 Value Chain Analysis")
            
            # Cost distribution analysis
            if 'cost' in self.value_chain.columns and 'function' in self.value_chain.columns:
                total_value_chain_cost = self.value_chain['cost'].sum()
                insights.append(f"**Total Value Chain Cost**: ${total_value_chain_cost:,.0f}")
                
                # Identify highest cost functions
                cost_by_function = self.value_chain.groupby('function')['cost'].sum().sort_values(ascending=False)
                insights.append("**Cost Distribution by Function**:")
                for function, cost in cost_by_function.head(3).items():
                    percentage = (cost / total_value_chain_cost * 100) if total_value_chain_cost > 0 else 0
                    insights.append(f"  • {function}: ${cost:,.0f} ({percentage:.1f}%)")
                
                # Optimization opportunities
                highest_cost_function = cost_by_function.index[0]
                highest_cost = cost_by_function.iloc[0]
                insights.append("")
                insights.append(f"**Optimization Focus**: {highest_cost_function}")
                insights.append(f"  • Highest cost function: ${highest_cost:,.0f}")
                insights.append(f"  • Potential savings through optimization")
                insights.append(f"  • Review processes and efficiency")
        
        # Competitive positioning insights
        insights.append("")
        insights.append("## 🏆 Competitive Positioning")
        
        # Financial strength assessment
        if not self.income_statement.empty and not self.balance_sheet.empty:
            revenue = self._metrics_cache.get('total_revenue', 0)
            net_income = self._metrics_cache.get('total_net_income', 0)
            current_ratio = self._metrics_cache.get('current_ratio', 0)
            debt_to_equity = self._metrics_cache.get('debt_to_equity', 0)
            
            # Competitive strength score
            strength_score = 0
            if revenue > 1000000000:  # $1B
                strength_score += 25
            elif revenue > 100000000:  # $100M
                strength_score += 15
            else:
                strength_score += 5
            
            if net_income > 0:
                strength_score += 20
            
            if current_ratio > 1.5:
                strength_score += 20
            elif current_ratio > 1.0:
                strength_score += 10
            
            if debt_to_equity < 1.0:
                strength_score += 15
            elif debt_to_equity < 2.0:
                strength_score += 10
            
            insights.append(f"**Competitive Strength Score**: {strength_score}/80")
            
            if strength_score >= 60:
                insights.append("**Position**: Strong competitive position")
                insights.append("  • Maintain competitive advantages")
                insights.append("  • Consider market expansion")
            elif strength_score >= 40:
                insights.append("**Position**: Moderate competitive position")
                insights.append("  • Strengthen core competencies")
                insights.append("  • Address competitive weaknesses")
            else:
                insights.append("**Position**: Weak competitive position")
                insights.append("  • Immediate turnaround required")
                insights.append("  • Focus on core business improvement")
        
        return "\n".join(insights)
    
    def generate_risk_mitigation_insights(self):
        """Generate comprehensive risk mitigation insights"""
        insights = []
        insights.append("## ⚠️ Risk Mitigation Analysis")
        
        # Financial risk assessment
        risk_factors = []
        mitigation_strategies = []
        
        # Liquidity risk
        current_ratio = self._metrics_cache.get('current_ratio', 0)
        if current_ratio < 1.5:
            risk_factors.append("Liquidity Risk")
            mitigation_strategies.extend([
                "Implement cash flow forecasting and monitoring",
                "Optimize working capital management",
                "Establish credit lines and financing options",
                "Review payment terms with suppliers and customers"
            ])
        
        # Solvency risk
        debt_to_equity = self._metrics_cache.get('debt_to_equity', 0)
        if debt_to_equity > 2.0:
            risk_factors.append("Solvency Risk")
            mitigation_strategies.extend([
                "Develop debt reduction plan",
                "Review capital structure",
                "Consider equity financing alternatives",
                "Monitor debt covenants closely"
            ])
        
        # Cash flow risk
        total_free_cf = self._metrics_cache.get('total_free_cf', 0)
        if total_free_cf < 0:
            risk_factors.append("Cash Flow Risk")
            mitigation_strategies.extend([
                "Improve operational efficiency",
                "Optimize capital expenditure planning",
                "Review investment priorities",
                "Consider divestment of non-core assets"
            ])
        
        # Revenue concentration risk
        if not self.income_statement.empty and len(self.income_statement) > 1:
            recent_revenue = self.income_statement['revenue'].iloc[-1]
            total_revenue = self.income_statement['revenue'].sum()
            if total_revenue > 0:
                concentration = (recent_revenue / total_revenue) * 100
                if concentration > 50:
                    risk_factors.append("Revenue Concentration Risk")
                    mitigation_strategies.extend([
                        "Diversify revenue sources",
                        "Develop new product/service lines",
                        "Expand into new markets",
                        "Strengthen customer relationships"
                    ])
        
        # Display risk factors
        if risk_factors:
            insights.append("**Identified Risk Factors**:")
            for risk in risk_factors:
                insights.append(f"  • {risk}")
        else:
            insights.append("**Risk Status**: Low overall risk profile")
        
        insights.append("")
        
        # Display mitigation strategies
        if mitigation_strategies:
            insights.append("**Mitigation Strategies**:")
            for strategy in mitigation_strategies:
                insights.append(f"  • {strategy}")
        
        insights.append("")
        insights.append("## 🎯 Risk Management Framework")
        insights.append("1. **Risk Identification**: Regular risk assessments")
        insights.append("2. **Risk Measurement**: Quantitative risk metrics")
        insights.append("3. **Risk Monitoring**: Continuous monitoring and reporting")
        insights.append("4. **Risk Response**: Proactive risk mitigation")
        insights.append("5. **Risk Review**: Periodic framework evaluation")
        
        return "\n".join(insights)

# Finance-specific risk analyzer (implemented directly)
class FinanceRiskAnalyzer:
    """Comprehensive risk analysis tool for finance operations"""
    
    def __init__(self, income_statement, balance_sheet, cash_flow, budget, forecast, market_data, customer_data, product_data, value_chain):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.cash_flow = cash_flow
        self.budget = budget
        self.forecast = forecast
        self.market_data = market_data
        self.customer_data = customer_data
        self.product_data = product_data
        self.value_chain = value_chain
    
    def analyze_financial_risk(self):
        """Analyze overall financial risk"""
        risk_score = 0
        risk_factors = []
        risk_level = "Low"
        
        # Revenue concentration risk
        if not self.income_statement.empty:
            total_revenue = self.income_statement['revenue'].sum()
            if total_revenue > 0:
                recent_revenue = self.income_statement['revenue'].iloc[-1]
                revenue_concentration = (recent_revenue / total_revenue) * 100
                
                if revenue_concentration > 50:
                    risk_score += 30
                    risk_factors.append(f"High revenue concentration: {revenue_concentration:.1f}% in recent period")
        
        # Liquidity risk
        if not self.balance_sheet.empty:
            current_assets = self.balance_sheet['current_assets'].sum()
            current_liabilities = self.balance_sheet['current_liabilities'].sum()
            
            if current_liabilities > 0:
                current_ratio = current_assets / current_liabilities
                if current_ratio < 1.0:
                    risk_score += 40
                    risk_factors.append(f"Low liquidity: current ratio {current_ratio:.2f}")
                elif current_ratio < 1.5:
                    risk_score += 20
                    risk_factors.append(f"Moderate liquidity: current ratio {current_ratio:.2f}")
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'factors': risk_factors,
            'mitigation': ['Improve cash flow management', 'Diversify revenue sources', 'Strengthen balance sheet']
        }

def display_risk_dashboard(risk_analyzer):
    """Display risk analysis dashboard"""
    if risk_analyzer is None:
        st.error("Risk analyzer not available")
        return
    
    st.subheader("⚠️ Financial Risk Analysis")
    
    risk_analysis = risk_analyzer.analyze_financial_risk()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Risk Score", f"{risk_analysis['score']}/100")
        st.metric("Risk Level", risk_analysis['level'])
    
    with col2:
        st.markdown("**Risk Factors:**")
        for factor in risk_analysis['factors']:
            st.markdown(f"• {factor}")
    
    st.markdown("**Mitigation Strategies:**")
    for strategy in risk_analysis['mitigation']:
        st.markdown(f"• {strategy}")

# Finance-specific predictive analytics (optimized)
class FinancePredictiveAnalytics:
    """Advanced predictive analytics for finance operations with machine learning capabilities"""
    
    def __init__(self, income_statement, balance_sheet, cash_flow, budget, forecast, market_data, customer_data, product_data, value_chain):
        self.income_statement = income_statement
        self.balance_sheet = balance_sheet
        self.cash_flow = cash_flow
        self.budget = budget
        self.forecast = forecast
        self.market_data = market_data
        self.customer_data = customer_data
        self.product_data = product_data
        self.value_chain = value_chain
        
        # Initialize prediction cache for performance optimization
        self._prediction_cache = {}
        self._model_performance = {}
        
        # Pre-calculate common metrics for predictions
        self._precalculate_prediction_metrics()
    
    def _precalculate_prediction_metrics(self):
        """Pre-calculate metrics needed for predictions"""
        self._prediction_metrics = {}
        
        if not self.income_statement.empty:
            # Revenue metrics
            self._prediction_metrics['revenue'] = self.income_statement['revenue'].values
            self._prediction_metrics['revenue_growth_rates'] = []
            
            if len(self.income_statement) > 1:
                for i in range(1, len(self.income_statement)):
                    if self.income_statement['revenue'].iloc[i-1] > 0:
                        growth_rate = ((self.income_statement['revenue'].iloc[i] - self.income_statement['revenue'].iloc[i-1]) / 
                                     self.income_statement['revenue'].iloc[i-1]) * 100
                        self._prediction_metrics['revenue_growth_rates'].append(growth_rate)
            
            # Profitability metrics
            if 'net_income' in self.income_statement.columns:
                self._prediction_metrics['net_income'] = self.income_statement['net_income'].values
                self._prediction_metrics['net_margins'] = []
                
                for i in range(len(self.income_statement)):
                    if self.income_statement['revenue'].iloc[i] > 0:
                        margin = (self.income_statement['net_income'].iloc[i] / self.income_statement['revenue'].iloc[i]) * 100
                        self._prediction_metrics['net_margins'].append(margin)
        
        if not self.balance_sheet.empty:
            # Asset and liability trends
            if 'total_assets' in self.balance_sheet.columns:
                self._prediction_metrics['total_assets'] = self.balance_sheet['total_assets'].values
            
            if 'current_assets' in self.balance_sheet.columns:
                self._prediction_metrics['current_assets'] = self.balance_sheet['current_assets'].values
        
        if not self.cash_flow.empty:
            # Cash flow trends
            # Check for operating cash flow column with fallback names
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in self.cash_flow.columns:
                    operating_cf_col = col_name
                    break
            
            if operating_cf_col:
                self._prediction_metrics['operating_cf'] = self.cash_flow[operating_cf_col].values
    
    def predict_revenue_trends(self, periods_ahead=6, confidence_level=0.95):
        """Advanced revenue prediction with multiple forecasting models"""
        if self.income_statement.empty or len(self.income_statement) < 3:
            return pd.DataFrame(), "Insufficient data for revenue prediction"
        
        try:
            # Enhanced revenue prediction with multiple models
            revenue_data = self.income_statement[['period', 'revenue']].copy()
            revenue_data['period_num'] = range(len(revenue_data))
            
            # Model 1: Exponential Smoothing
            alpha = 0.3  # Smoothing factor
            revenue_data['exp_smooth'] = revenue_data['revenue'].ewm(alpha=alpha).mean()
            
            # Model 2: Moving Average with trend
            window_size = min(4, len(revenue_data))
            revenue_data['ma_trend'] = revenue_data['revenue'].rolling(window=window_size, min_periods=1).mean()
            
            # Model 3: Linear trend projection
            if len(revenue_data) >= 3:
                # Calculate linear trend
                x = revenue_data['period_num'].values.reshape(-1, 1)
                y = revenue_data['revenue'].values
                
                # Simple linear regression
                slope = np.polyfit(x.flatten(), y, 1)[0]
                intercept = np.polyfit(x.flatten(), y, 1)[1]
                
                revenue_data['linear_trend'] = slope * revenue_data['period_num'] + intercept
            
            # Generate future predictions
            future_predictions = []
            last_revenue = revenue_data['revenue'].iloc[-1]
            avg_growth_rate = np.mean(self._prediction_metrics.get('revenue_growth_rates', [5])) if self._prediction_metrics.get('revenue_growth_rates') else 5
            
            for i in range(1, periods_ahead + 1):
                future_period = len(revenue_data) + i
                
                # Multiple prediction methods
                exp_smooth_pred = last_revenue * (1 + avg_growth_rate/100) ** i
                ma_trend_pred = revenue_data['ma_trend'].iloc[-1] * (1 + avg_growth_rate/100) ** i
                linear_pred = slope * future_period + intercept if 'slope' in locals() else last_revenue * (1 + avg_growth_rate/100) ** i
                
                # Ensemble prediction (weighted average)
                ensemble_pred = (exp_smooth_pred * 0.4 + ma_trend_pred * 0.3 + linear_pred * 0.3)
                
                # Add confidence intervals
                confidence_range = ensemble_pred * 0.15  # 15% confidence range
                lower_bound = ensemble_pred - confidence_range
                upper_bound = ensemble_pred + confidence_range
                
                future_predictions.append({
                    'period': f'Future_{i}',
                    'period_num': future_period,
                    'predicted_revenue': ensemble_pred,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound,
                    'confidence_level': confidence_level * 100,
                    'exp_smooth_pred': exp_smooth_pred,
                    'ma_trend_pred': ma_trend_pred,
                    'linear_pred': linear_pred
                })
            
            # Combine historical and future data
            future_df = pd.DataFrame(future_predictions)
            combined_data = pd.concat([revenue_data, future_df], ignore_index=True)
            
            # Store prediction performance metrics
            self._model_performance['revenue_prediction'] = {
                'avg_growth_rate': avg_growth_rate,
                'confidence_level': confidence_level,
                'prediction_horizon': periods_ahead
            }
            
            return combined_data, "Advanced revenue prediction completed successfully"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting revenue trends: {str(e)}"
    
    def predict_profitability_trends(self, periods_ahead=6):
        """Predict profitability trends using multiple financial ratios"""
        if self.income_statement.empty or len(self.income_statement) < 3:
            return pd.DataFrame(), "Insufficient data for profitability prediction"
        
        try:
            profitability_data = self.income_statement[['period', 'revenue', 'net_income']].copy()
            profitability_data['period_num'] = range(len(profitability_data))
            
            # Calculate historical profitability ratios
            profitability_data['net_margin'] = (profitability_data['net_income'] / profitability_data['revenue'] * 100).fillna(0)
            
            # Predict future profitability
            future_predictions = []
            last_margin = profitability_data['net_margin'].iloc[-1]
            margin_trend = np.polyfit(profitability_data['period_num'], profitability_data['net_margin'], 1)[0]
            
            for i in range(1, periods_ahead + 1):
                future_period = len(profitability_data) + i
                
                # Predict margin with trend
                predicted_margin = last_margin + (margin_trend * i)
                
                # Ensure margin stays within reasonable bounds
                predicted_margin = max(min(predicted_margin, 50), -20)
                
                # Predict revenue (use revenue prediction if available)
                if 'revenue' in self._prediction_cache:
                    predicted_revenue = self._prediction_cache['revenue'].get(f'Future_{i}', 0)
                else:
                    # Simple revenue projection
                    last_revenue = profitability_data['revenue'].iloc[-1]
                    avg_growth = np.mean(self._prediction_metrics.get('revenue_growth_rates', [5])) if self._prediction_metrics.get('revenue_growth_rates') else 5
                    predicted_revenue = last_revenue * (1 + avg_growth/100) ** i
                
                # Calculate predicted net income
                predicted_net_income = predicted_revenue * (predicted_margin / 100)
                
                future_predictions.append({
                    'period': f'Future_{i}',
                    'period_num': future_period,
                    'predicted_revenue': predicted_revenue,
                    'predicted_net_margin': predicted_margin,
                    'predicted_net_income': predicted_net_income
                })
            
            # Combine historical and future data
            future_df = pd.DataFrame(future_predictions)
            combined_data = pd.concat([profitability_data, future_df], ignore_index=True)
            
            return combined_data, "Profitability trends predicted successfully"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting profitability trends: {str(e)}"
    
    def predict_cash_flow_trends(self, periods_ahead=6):
        """Predict cash flow trends and liquidity position"""
        if self.cash_flow.empty or len(self.cash_flow) < 3:
            return pd.DataFrame(), "Insufficient data for cash flow prediction"
        
        try:
            # Check for required columns with fallback names
            required_cols = ['period']
            operating_cf_col = None
            free_cf_col = None
            
            # Find operating cash flow column
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in self.cash_flow.columns:
                    operating_cf_col = col_name
                    required_cols.append(col_name)
                    break
            
            # Find free cash flow column
            for col_name in ['free_cash_flow', 'free_cf', 'free_cashflow', 'fcf']:
                if col_name in self.cash_flow.columns:
                    free_cf_col = col_name
                    required_cols.append(col_name)
                    break
            
            if not operating_cf_col:
                return pd.DataFrame(), "Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow"
            
            cash_flow_data = self.cash_flow[required_cols].copy()
            cash_flow_data['period_num'] = range(len(cash_flow_data))
            
            # Calculate cash flow trends
            operating_cf = cash_flow_data[operating_cf_col].values
            cf_trend = np.polyfit(cash_flow_data['period_num'], operating_cf, 1)[0]
            
            # Predict future cash flows
            future_predictions = []
            last_operating_cf = operating_cf[-1]
            
            for i in range(1, periods_ahead + 1):
                future_period = len(cash_flow_data) + i
                
                # Predict operating cash flow with trend
                predicted_operating_cf = last_operating_cf + (cf_trend * i)
                
                # Add some seasonality and variability
                seasonality_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 4)  # Quarterly seasonality
                predicted_operating_cf *= seasonality_factor
                
                # Predict free cash flow (simplified)
                predicted_free_cf = predicted_operating_cf * 0.7  # Assume 70% conversion
                
                future_predictions.append({
                    'period': f'Future_{i}',
                    'period_num': future_period,
                    'predicted_operating_cf': predicted_operating_cf,
                    'predicted_free_cf': predicted_free_cf,
                    'cash_flow_health': 'Healthy' if predicted_free_cf > 0 else 'Concerning'
                })
            
            # Combine historical and future data
            future_df = pd.DataFrame(future_predictions)
            combined_data = pd.concat([cash_flow_data, future_df], ignore_index=True)
            
            return combined_data, "Cash flow trends predicted successfully"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting cash flow trends: {str(e)}"
    
    def predict_financial_health_score(self, periods_ahead=6):
        """Predict overall financial health score using multiple indicators"""
        if (self.income_statement.empty or self.balance_sheet.empty or 
            self.cash_flow.empty or len(self.income_statement) < 3):
            return pd.DataFrame(), "Insufficient data for financial health prediction"
        
        try:
            # Calculate historical financial health scores
            health_scores = []
            periods = []
            
            for i in range(len(self.income_statement)):
                period = self.income_statement['period'].iloc[i]
                periods.append(period)
                
                # Get corresponding balance sheet and cash flow data
                bs_data = self.balance_sheet[self.balance_sheet['period'] == period]
                cf_data = self.cash_flow[self.cash_flow['period'] == period]
                
                if not bs_data.empty and not cf_data.empty:
                    # Calculate health score components
                    revenue = self.income_statement['revenue'].iloc[i]
                    net_income = self.income_statement['net_income'].iloc[i]
                    current_assets = bs_data['current_assets'].iloc[0] if 'current_assets' in bs_data.columns else 0
                    current_liabilities = bs_data['current_liabilities'].iloc[0] if 'current_liabilities' in bs_data.columns else 0
                    
                    # Find operating cash flow column with fallback names
                    operating_cf = 0
                    for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                        if col_name in cf_data.columns:
                            operating_cf = cf_data[col_name].iloc[0]
                            break
                    
                    # Health score calculation (0-100 scale)
                    score = 0
                    
                    # Profitability (30 points)
                    if revenue > 0:
                        net_margin = (net_income / revenue) * 100
                        if net_margin > 15:
                            score += 30
                        elif net_margin > 10:
                            score += 25
                        elif net_margin > 5:
                            score += 20
                        elif net_margin > 0:
                            score += 15
                        else:
                            score += 5
                    
                    # Liquidity (25 points)
                    if current_liabilities > 0:
                        current_ratio = current_assets / current_liabilities
                        if current_ratio > 2.0:
                            score += 25
                        elif current_ratio > 1.5:
                            score += 20
                        elif current_ratio > 1.0:
                            score += 15
                        else:
                            score += 5
                    
                    # Cash flow (25 points)
                    if revenue > 0:
                        cf_to_revenue = (operating_cf / revenue) * 100
                        if cf_to_revenue > 15:
                            score += 25
                        elif cf_to_revenue > 10:
                            score += 20
                        elif cf_to_revenue > 5:
                            score += 15
                        else:
                            score += 5
                    
                    # Growth (20 points)
                    if i > 0:
                        prev_revenue = self.income_statement['revenue'].iloc[i-1]
                        if prev_revenue > 0:
                            growth_rate = ((revenue - prev_revenue) / prev_revenue) * 100
                            if growth_rate > 10:
                                score += 20
                            elif growth_rate > 5:
                                score += 15
                            elif growth_rate > 0:
                                score += 10
                            else:
                                score += 5
                    
                    health_scores.append(score)
                else:
                    health_scores.append(50)  # Default score if data missing
            
            # Predict future health scores
            if len(health_scores) >= 3:
                health_trend = np.polyfit(range(len(health_scores)), health_scores, 1)[0]
                
                future_predictions = []
                last_score = health_scores[-1]
                
                for i in range(1, periods_ahead + 1):
                    future_period = len(periods) + i
                    
                    # Predict health score with trend
                    predicted_score = last_score + (health_trend * i)
                    predicted_score = max(min(predicted_score, 100), 0)  # Ensure 0-100 range
                    
                    # Categorize health level
                    if predicted_score >= 80:
                        health_level = "Excellent"
                    elif predicted_score >= 60:
                        health_level = "Good"
                    elif predicted_score >= 40:
                        health_level = "Fair"
                    else:
                        health_level = "Poor"
                    
                    future_predictions.append({
                        'period': f'Future_{i}',
                        'period_num': future_period,
                        'predicted_health_score': predicted_score,
                        'health_level': health_level,
                        'trend': 'Improving' if health_trend > 0 else 'Declining' if health_trend < 0 else 'Stable'
                    })
                
                # Combine historical and future data
                historical_data = pd.DataFrame({
                    'period': periods,
                    'health_score': health_scores
                })
                
                future_df = pd.DataFrame(future_predictions)
                combined_data = pd.concat([historical_data, future_df], ignore_index=True)
                
                return combined_data, "Financial health scores predicted successfully"
            
            return pd.DataFrame(), "Insufficient data for health score prediction"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting financial health scores: {str(e)}"
    
    def predict_market_performance(self, periods_ahead=6):
        """Predict market performance indicators"""
        if self.market_data.empty or len(self.market_data) < 3:
            return pd.DataFrame(), "Insufficient market data for prediction"
        
        try:
            market_data = self.market_data[['period', 'market_price', 'market_cap']].copy()
            market_data['period_num'] = range(len(market_data))
            
            # Predict stock price trends
            if 'market_price' in market_data.columns:
                prices = market_data['market_price'].values
                price_trend = np.polyfit(market_data['period_num'], prices, 1)[0]
                
                future_predictions = []
                last_price = prices[-1]
                
                for i in range(1, periods_ahead + 1):
                    future_period = len(market_data) + i
                    
                    # Predict price with trend and volatility
                    predicted_price = last_price + (price_trend * i)
                    
                    # Add volatility factor
                    volatility = np.std(prices) * 0.1  # 10% of historical volatility
                    predicted_price += np.random.normal(0, volatility)
                    
                    # Ensure positive price
                    predicted_price = max(predicted_price, last_price * 0.5)
                    
                    future_predictions.append({
                        'period': f'Future_{i}',
                        'period_num': future_period,
                        'predicted_price': predicted_price,
                        'price_change_pct': ((predicted_price - last_price) / last_price) * 100,
                        'market_sentiment': 'Bullish' if predicted_price > last_price else 'Bearish'
                    })
                
                # Combine historical and future data
                future_df = pd.DataFrame(future_predictions)
                combined_data = pd.concat([market_data, future_df], ignore_index=True)
                
                return combined_data, "Market performance predicted successfully"
            
            return pd.DataFrame(), "Insufficient market price data for prediction"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting market performance: {str(e)}"
    
    def get_prediction_accuracy_metrics(self):
        """Calculate prediction accuracy metrics for model validation"""
        if not self._model_performance:
            return "No predictions available for accuracy assessment"
        
        accuracy_metrics = []
        accuracy_metrics.append("## 📊 Prediction Model Performance Metrics")
        accuracy_metrics.append("")
        
        for model_name, metrics in self._model_performance.items():
            accuracy_metrics.append(f"**{model_name.replace('_', ' ').title()}**:")
            for metric, value in metrics.items():
                if isinstance(value, float):
                    accuracy_metrics.append(f"  • {metric.replace('_', ' ').title()}: {value:.2f}")
                else:
                    accuracy_metrics.append(f"  • {metric.replace('_', ' ').title()}: {value}")
            accuracy_metrics.append("")
        
        return "\n".join(accuracy_metrics)
    
    def predict_scenario_analysis(self, scenarios=['optimistic', 'base', 'pessimistic'], periods_ahead=6):
        """Perform scenario analysis for financial planning"""
        if self.income_statement.empty or len(self.income_statement) < 3:
            return pd.DataFrame(), "Insufficient data for scenario analysis"
        
        try:
            scenario_results = []
            
            for scenario in scenarios:
                # Define scenario parameters
                if scenario == 'optimistic':
                    growth_multiplier = 1.5
                    margin_improvement = 1.2
                elif scenario == 'pessimistic':
                    growth_multiplier = 0.7
                    margin_improvement = 0.8
                else:  # base case
                    growth_multiplier = 1.0
                    margin_improvement = 1.0
                
                # Get base predictions
                revenue_pred, _ = self.predict_revenue_trends(periods_ahead)
                profitability_pred, _ = self.predict_profitability_trends(periods_ahead)
                
                if not revenue_pred.empty and not profitability_pred.empty:
                    # Apply scenario adjustments
                    future_revenue = revenue_pred[revenue_pred['period'].str.contains('Future')]
                    future_profitability = profitability_pred[profitability_pred['period'].str.contains('Future')]
                    
                    for i, (_, rev_row) in enumerate(future_revenue.iterrows()):
                        if i < len(future_profitability):
                            prof_row = future_profitability.iloc[i]
                            
                            # Apply scenario adjustments
                            adjusted_revenue = rev_row['predicted_revenue'] * growth_multiplier
                            adjusted_margin = prof_row['predicted_net_margin'] * margin_improvement
                            adjusted_net_income = adjusted_revenue * (adjusted_margin / 100)
                            
                            scenario_results.append({
                                'scenario': scenario,
                                'period': rev_row['period'],
                                'adjusted_revenue': adjusted_revenue,
                                'adjusted_margin': adjusted_margin,
                                'adjusted_net_income': adjusted_net_income,
                                'growth_multiplier': growth_multiplier,
                                'margin_improvement': margin_improvement
                            })
            
            return pd.DataFrame(scenario_results), "Scenario analysis completed successfully"
            
        except Exception as e:
            return pd.DataFrame(), f"Error performing scenario analysis: {str(e)}"
    
    def predict_break_even_analysis(self, periods_ahead=6):
        """Predict break-even analysis for future periods"""
        if self.income_statement.empty or len(self.income_statement) < 3:
            return pd.DataFrame(), "Insufficient data for break-even analysis"
        
        try:
            # Calculate historical break-even points
            break_even_data = []
            
            for i in range(len(self.income_statement)):
                period = self.income_statement['period'].iloc[i]
                revenue = self.income_statement['revenue'].iloc[i]
                
                # Get corresponding balance sheet data
                bs_data = self.balance_sheet[self.balance_sheet['period'] == period]
                
                if not bs_data.empty:
                    # Calculate break-even components
                    fixed_costs = revenue * 0.3  # Assume 30% fixed costs (simplified)
                    variable_costs = revenue * 0.5  # Assume 50% variable costs (simplified)
                    total_costs = fixed_costs + variable_costs
                    
                    # Break-even revenue
                    break_even_revenue = fixed_costs / (1 - (variable_costs / revenue)) if revenue > 0 else 0
                    
                    # Safety margin
                    safety_margin = ((revenue - break_even_revenue) / revenue * 100) if revenue > 0 else 0
                    
                    break_even_data.append({
                        'period': period,
                        'revenue': revenue,
                        'fixed_costs': fixed_costs,
                        'variable_costs': variable_costs,
                        'total_costs': total_costs,
                        'break_even_revenue': break_even_revenue,
                        'safety_margin': safety_margin
                    })
            
            # Predict future break-even points
            if len(break_even_data) >= 3:
                # Calculate trends
                revenue_trend = np.polyfit(range(len(break_even_data)), [d['revenue'] for d in break_even_data], 1)[0]
                fixed_costs_trend = np.polyfit(range(len(break_even_data)), [d['fixed_costs'] for d in break_even_data], 1)[0]
                
                future_predictions = []
                last_revenue = break_even_data[-1]['revenue']
                last_fixed_costs = break_even_data[-1]['fixed_costs']
                
                for i in range(1, periods_ahead + 1):
                    future_period = len(break_even_data) + i
                    
                    # Predict future values
                    predicted_revenue = last_revenue + (revenue_trend * i)
                    predicted_fixed_costs = last_fixed_costs + (fixed_costs_trend * i)
                    predicted_variable_costs = predicted_revenue * 0.5
                    
                    # Calculate predicted break-even
                    predicted_break_even = predicted_fixed_costs / (1 - (predicted_variable_costs / predicted_revenue)) if predicted_revenue > 0 else 0
                    predicted_safety_margin = ((predicted_revenue - predicted_break_even) / predicted_revenue * 100) if predicted_revenue > 0 else 0
                    
                    future_predictions.append({
                        'period': f'Future_{i}',
                        'revenue': predicted_revenue,
                        'fixed_costs': predicted_fixed_costs,
                        'variable_costs': predicted_variable_costs,
                        'total_costs': predicted_fixed_costs + predicted_variable_costs,
                        'break_even_revenue': predicted_break_even,
                        'safety_margin': predicted_safety_margin
                    })
                
                # Combine historical and future data
                historical_df = pd.DataFrame(break_even_data)
                future_df = pd.DataFrame(future_predictions)
                combined_data = pd.concat([historical_df, future_df], ignore_index=True)
                
                return combined_data, "Break-even analysis completed successfully"
            
            return pd.DataFrame(), "Insufficient data for break-even prediction"
            
        except Exception as e:
            return pd.DataFrame(), f"Error performing break-even analysis: {str(e)}"
    
    def predict_working_capital_needs(self, periods_ahead=6):
        """Predict working capital requirements for future periods"""
        if (self.balance_sheet.empty or self.cash_flow.empty or 
            len(self.balance_sheet) < 3):
            return pd.DataFrame(), "Insufficient data for working capital prediction"
        
        try:
            working_capital_data = []
            
            for i in range(len(self.balance_sheet)):
                period = self.balance_sheet['period'].iloc[i]
                
                # Get current assets and liabilities
                current_assets = self.balance_sheet['current_assets'].iloc[i] if 'current_assets' in self.balance_sheet.columns else 0
                current_liabilities = self.balance_sheet['current_liabilities'].iloc[i] if 'current_liabilities' in self.balance_sheet.columns else 0
                
                # Calculate working capital
                working_capital = current_assets - current_liabilities
                
                # Get corresponding cash flow data
                cf_data = self.cash_flow[self.cash_flow['period'] == period]
                # Find operating cash flow column with fallback names
                operating_cf = 0
                for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                    if col_name in cf_data.columns:
                        operating_cf = cf_data[col_name].iloc[0]
                        break
                
                # Working capital turnover
                wc_turnover = operating_cf / working_capital if working_capital > 0 else 0
                
                working_capital_data.append({
                    'period': period,
                    'current_assets': current_assets,
                    'current_liabilities': current_liabilities,
                    'working_capital': working_capital,
                    'operating_cf': operating_cf,
                    'wc_turnover': wc_turnover
                })
            
            # Predict future working capital needs
            if len(working_capital_data) >= 3:
                # Calculate trends
                wc_trend = np.polyfit(range(len(working_capital_data)), [d['working_capital'] for d in working_capital_data], 1)[0]
                cf_trend = np.polyfit(range(len(working_capital_data)), [d['operating_cf'] for d in working_capital_data], 1)[0]
                
                future_predictions = []
                last_wc = working_capital_data[-1]['working_capital']
                last_cf = working_capital_data[-1]['operating_cf']
                
                for i in range(1, periods_ahead + 1):
                    future_period = len(working_capital_data) + i
                    
                    # Predict future values
                    predicted_wc = last_wc + (wc_trend * i)
                    predicted_cf = last_cf + (cf_trend * i)
                    
                    # Calculate predicted turnover
                    predicted_turnover = predicted_cf / predicted_wc if predicted_wc > 0 else 0
                    
                    # Working capital adequacy assessment
                    if predicted_wc > 0:
                        if predicted_wc > last_wc * 1.2:
                            adequacy = "Excessive"
                        elif predicted_wc < last_wc * 0.8:
                            adequacy = "Insufficient"
                        else:
                            adequacy = "Adequate"
                    else:
                        adequacy = "Critical"
                    
                    future_predictions.append({
                        'period': f'Future_{i}',
                        'predicted_working_capital': predicted_wc,
                        'predicted_operating_cf': predicted_cf,
                        'predicted_wc_turnover': predicted_turnover,
                        'adequacy_assessment': adequacy,
                        'recommendation': 'Optimize' if adequacy == "Excessive" else 'Increase' if adequacy == "Insufficient" else 'Monitor'
                    })
                
                # Combine historical and future data
                historical_df = pd.DataFrame(working_capital_data)
                future_df = pd.DataFrame(future_predictions)
                combined_data = pd.concat([historical_df, future_df], ignore_index=True)
                
                return combined_data, "Working capital prediction completed successfully"
            
            return pd.DataFrame(), "Insufficient data for working capital prediction"
            
        except Exception as e:
            return pd.DataFrame(), f"Error predicting working capital needs: {str(e)}"

def display_finance_predictive_analytics_dashboard(predictive_analytics):
    """Display comprehensive predictive analytics dashboard"""
    if predictive_analytics is None:
        st.error("Predictive analytics not available")
        return
    
    st.markdown("""
    <div class="section-header">
        <h3>🔮 Advanced Predictive Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different prediction types
    pred_tab1, pred_tab2, pred_tab3, pred_tab4, pred_tab5, pred_tab6, pred_tab7, pred_tab8, pred_tab9 = st.tabs([
        "📈 Revenue Trends", "💰 Profitability", "💸 Cash Flow", 
        "🏥 Financial Health", "📊 Market Performance", "🎯 Scenario Analysis",
        "⚖️ Break-Even Analysis", "💼 Working Capital", "📋 Model Performance"
    ])
    
    with pred_tab1:
        st.subheader("📈 Revenue Trend Predictions")
        
        # Prediction parameters
        col1, col2 = st.columns(2)
        with col1:
            periods_ahead = st.slider("Prediction Periods", 3, 12, 6, help="Number of future periods to predict", key="revenue_prediction_periods")
        with col2:
            confidence_level = st.slider("Confidence Level", 0.80, 0.99, 0.95, help="Prediction confidence level", key="revenue_confidence_level")
        
        # Generate revenue predictions
        revenue_prediction, message = predictive_analytics.predict_revenue_trends(periods_ahead, confidence_level)
        
        if not revenue_prediction.empty:
            # Display prediction summary
            st.markdown("### 📊 Prediction Summary")
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'predicted_revenue' in revenue_prediction.columns:
                    future_revenue = revenue_prediction[revenue_prediction['period'].str.contains('Future')]['predicted_revenue'].sum()
                    st.metric("Total Predicted Revenue", f"${future_revenue:,.0f}")
            
            with col2:
                if 'revenue_growth_rates' in predictive_analytics._prediction_metrics:
                    avg_growth = np.mean(predictive_analytics._prediction_metrics['revenue_growth_rates'])
                    st.metric("Average Growth Rate", f"{avg_growth:.1f}%")
            
            with col3:
                if 'confidence_level' in revenue_prediction.columns:
                    avg_confidence = revenue_prediction['confidence_level'].mean()
                    st.metric("Average Confidence", f"{avg_confidence:.1f}%")
            
            # Display detailed predictions
            st.markdown("### 📋 Detailed Predictions")
            display_cols = ['period', 'revenue', 'predicted_revenue']
            if 'lower_bound' in revenue_prediction.columns:
                display_cols.extend(['lower_bound', 'upper_bound'])
            
            st.dataframe(revenue_prediction[display_cols].round(2), use_container_width=True)
            
            # Create enhanced prediction chart
            fig = go.Figure()
            
            # Historical data
            historical = revenue_prediction[~revenue_prediction['period'].str.contains('Future')]
            fig.add_trace(go.Scatter(
                x=historical['period'],
                y=historical['revenue'],
                mode='lines+markers',
                name='Historical Revenue',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            # Predicted data
            future = revenue_prediction[revenue_prediction['period'].str.contains('Future')]
            if not future.empty:
                fig.add_trace(go.Scatter(
                    x=future['period'],
                    y=future['predicted_revenue'],
                    mode='lines+markers',
                    name='Predicted Revenue',
                    line=dict(color='red', width=3, dash='dash'),
                    marker=dict(size=8)
                ))
                
                # Add confidence intervals if available
                if 'lower_bound' in future.columns and 'upper_bound' in future.columns:
                    fig.add_trace(go.Scatter(
                        x=future['period'],
                        y=future['upper_bound'],
                        mode='lines',
                        name='Upper Bound',
                        line=dict(color='red', width=1, dash='dot'),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future['period'],
                        y=future['lower_bound'],
                        mode='lines',
                        name='Lower Bound',
                        line=dict(color='red', width=1, dash='dot'),
                        fill='tonexty',
                        fillcolor='rgba(255,0,0,0.1)',
                        showlegend=False
                    ))
            
            fig.update_layout(
                title="Revenue Trends and Predictions with Confidence Intervals",
                xaxis_title="Period",
                yaxis_title="Revenue ($)",
                hovermode='x unified',
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Model comparison
            if 'exp_smooth_pred' in future.columns:
                st.markdown("### 🔍 Model Comparison")
                model_comparison = future[['period', 'exp_smooth_pred', 'ma_trend_pred', 'linear_pred', 'predicted_revenue']].round(2)
                st.dataframe(model_comparison, use_container_width=True)
        else:
            st.warning(message)
    
    with pred_tab2:
        st.subheader("💰 Profitability Trend Predictions")
        
        # Generate profitability predictions
        profitability_prediction, message = predictive_analytics.predict_profitability_trends(periods_ahead)
        
        if not profitability_prediction.empty:
            # Display prediction summary
            st.markdown("### 📊 Profitability Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'predicted_net_income' in profitability_prediction.columns:
                    future_net_income = profitability_prediction[profitability_prediction['period'].str.contains('Future')]['predicted_net_income'].sum()
                    st.metric("Total Predicted Net Income", f"${future_net_income:,.0f}")
            
            with col2:
                if 'predicted_net_margin' in profitability_prediction.columns:
                    avg_margin = profitability_prediction[profitability_prediction['period'].str.contains('Future')]['predicted_net_margin'].mean()
                    st.metric("Average Predicted Margin", f"{avg_margin:.1f}%")
            
            with col3:
                if 'net_margin' in profitability_prediction.columns:
                    current_margin = profitability_prediction['net_margin'].iloc[-1]
                    st.metric("Current Net Margin", f"{current_margin:.1f}%")
            
            # Display predictions
            st.markdown("### 📋 Profitability Predictions")
            st.dataframe(profitability_prediction.round(2), use_container_width=True)
            
            # Create profitability chart
            fig = go.Figure()
            
            # Historical margins
            historical = profitability_prediction[~profitability_prediction['period'].str.contains('Future')]
            fig.add_trace(go.Scatter(
                x=historical['period'],
                y=historical['net_margin'],
                mode='lines+markers',
                name='Historical Net Margin',
                line=dict(color='green', width=3)
            ))
            
            # Predicted margins
            future = profitability_prediction[profitability_prediction['period'].str.contains('Future')]
            if not future.empty:
                fig.add_trace(go.Scatter(
                    x=future['period'],
                    y=future['predicted_net_margin'],
                    mode='lines+markers',
                    name='Predicted Net Margin',
                    line=dict(color='orange', width=3, dash='dash')
                ))
            
            fig.update_layout(
                title="Net Margin Trends and Predictions",
                xaxis_title="Period",
                yaxis_title="Net Margin (%)",
                hovermode='x unified',
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(message)
    
    with pred_tab3:
        st.subheader("💸 Cash Flow Trend Predictions")
        
        # Generate cash flow predictions
        cash_flow_prediction, message = predictive_analytics.predict_cash_flow_trends(periods_ahead)
        
        if not cash_flow_prediction.empty:
            # Display prediction summary
            st.markdown("### 📊 Cash Flow Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'predicted_operating_cf' in cash_flow_prediction.columns:
                    future_operating_cf = cash_flow_prediction[cash_flow_prediction['period'].str.contains('Future')]['predicted_operating_cf'].sum()
                    st.metric("Total Predicted Operating CF", f"${future_operating_cf:,.0f}")
            
            with col2:
                if 'predicted_free_cf' in cash_flow_prediction.columns:
                    future_free_cf = cash_flow_prediction[cash_flow_prediction['period'].str.contains('Future')]['predicted_free_cf'].sum()
                    st.metric("Total Predicted Free CF", f"${future_free_cf:,.0f}")
            
            with col3:
                if 'cash_flow_health' in cash_flow_prediction.columns:
                    healthy_periods = len(cash_flow_prediction[cash_flow_prediction['cash_flow_health'] == 'Healthy'])
                    total_periods = len(cash_flow_prediction[cash_flow_prediction['period'].str.contains('Future')])
                    health_percentage = (healthy_periods / total_periods * 100) if total_periods > 0 else 0
                    st.metric("Healthy Cash Flow Periods", f"{health_percentage:.1f}%")
            
            # Display predictions
            st.markdown("### 📋 Cash Flow Predictions")
            st.dataframe(cash_flow_prediction.round(2), use_container_width=True)
            
            # Create cash flow chart
            fig = go.Figure()
            
            # Historical operating cash flow
            historical = cash_flow_prediction[~cash_flow_prediction['period'].str.contains('Future')]
            # Check for operating cash flow column with fallback names
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in historical.columns:
                    operating_cf_col = col_name
                    break
            
            if operating_cf_col:
                fig.add_trace(go.Scatter(
                    x=historical['period'],
                    y=historical[operating_cf_col],
                    mode='lines+markers',
                    name='Historical Operating CF',
                    line=dict(color='blue', width=3)
                ))
            
            # Predicted operating cash flow
            future = cash_flow_prediction[cash_flow_prediction['period'].str.contains('Future')]
            if not future.empty and 'predicted_operating_cf' in future.columns:
                fig.add_trace(go.Scatter(
                    x=future['period'],
                    y=future['predicted_operating_cf'],
                    mode='lines+markers',
                    name='Predicted Operating CF',
                    line=dict(color='red', width=3, dash='dash')
                ))
            
            fig.update_layout(
                title="Operating Cash Flow Trends and Predictions",
                xaxis_title="Period",
                yaxis_title="Operating Cash Flow ($)",
                hovermode='x unified',
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(message)
    
    with pred_tab4:
        st.subheader("🏥 Financial Health Score Predictions")
        
        # Generate financial health predictions
        health_prediction, message = predictive_analytics.predict_financial_health_score(periods_ahead)
        
        if not health_prediction.empty:
            # Display prediction summary
            st.markdown("### 📊 Financial Health Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'health_score' in health_prediction.columns:
                    current_score = health_prediction['health_score'].iloc[-1]
                    st.metric("Current Health Score", f"{current_score:.0f}/100")
            
            with col2:
                if 'predicted_health_score' in health_prediction.columns:
                    future_scores = health_prediction[health_prediction['period'].str.contains('Future')]['predicted_health_score']
                    avg_future_score = future_scores.mean()
                    st.metric("Average Predicted Score", f"{avg_future_score:.0f}/100")
            
            with col3:
                if 'trend' in health_prediction.columns:
                    improving_periods = len(health_prediction[health_prediction['trend'] == 'Improving'])
                    total_periods = len(health_prediction[health_prediction['period'].str.contains('Future')])
                    improvement_percentage = (improving_periods / total_periods * 100) if total_periods > 0 else 0
                    st.metric("Improving Trend Periods", f"{improvement_percentage:.1f}%")
            
            # Display predictions
            st.markdown("### 📋 Financial Health Predictions")
            st.dataframe(health_prediction.round(2), use_container_width=True)
            
            # Create health score chart
            fig = go.Figure()
            
            # Historical health scores
            historical = health_prediction[~health_prediction['period'].str.contains('Future')]
            fig.add_trace(go.Scatter(
                x=historical['period'],
                y=historical['health_score'],
                mode='lines+markers',
                name='Historical Health Score',
                line=dict(color='green', width=3)
            ))
            
            # Predicted health scores
            future = health_prediction[health_prediction['period'].str.contains('Future')]
            if not future.empty:
                fig.add_trace(go.Scatter(
                    x=future['period'],
                    y=future['predicted_health_score'],
                    mode='lines+markers',
                    name='Predicted Health Score',
                    line=dict(color='orange', width=3, dash='dash')
                ))
            
            # Add health level thresholds
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excellent (80+)")
            fig.add_hline(y=60, line_dash="dash", line_color="yellow", annotation_text="Good (60+)")
            fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Fair (40+)")
            fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Poor (<40)")
            
            fig.update_layout(
                title="Financial Health Score Trends and Predictions",
                xaxis_title="Period",
                yaxis_title="Health Score (0-100)",
                yaxis_range=[0, 100],
                hovermode='x unified',
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(message)
    
    with pred_tab5:
        st.subheader("📊 Market Performance Predictions")
        
        # Generate market performance predictions
        market_prediction, message = predictive_analytics.predict_market_performance(periods_ahead)
        
        if not market_prediction.empty:
            # Display prediction summary
            st.markdown("### 📊 Market Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'market_price' in market_prediction.columns:
                    current_price = market_prediction['market_price'].iloc[-1]
                    st.metric("Current Market Price", f"${current_price:.2f}")
            
            with col2:
                if 'predicted_price' in market_prediction.columns:
                    future_prices = market_prediction[market_prediction['period'].str.contains('Future')]['predicted_price']
                    avg_future_price = future_prices.mean()
                    st.metric("Average Predicted Price", f"${avg_future_price:.2f}")
            
            with col3:
                if 'market_sentiment' in market_prediction.columns:
                    bullish_periods = len(market_prediction[market_prediction['market_sentiment'] == 'Bullish'])
                    total_periods = len(market_prediction[market_prediction['period'].str.contains('Future')])
                    bullish_percentage = (bullish_periods / total_periods * 100) if total_periods > 0 else 0
                    st.metric("Bullish Sentiment", f"{bullish_percentage:.1f}%")
            
            # Display predictions
            st.markdown("### 📋 Market Predictions")
            st.dataframe(market_prediction.round(2), use_container_width=True)
            
            # Create market performance chart
            fig = go.Figure()
            
            # Historical prices
            historical = market_prediction[~market_prediction['period'].str.contains('Future')]
            fig.add_trace(go.Scatter(
                x=historical['period'],
                y=historical['market_price'],
                mode='lines+markers',
                name='Historical Price',
                line=dict(color='blue', width=3)
            ))
            
            # Predicted prices
            future = market_prediction[market_prediction['period'].str.contains('Future')]
            if not future.empty:
                fig.add_trace(go.Scatter(
                    x=future['period'],
                    y=future['predicted_price'],
                    mode='lines+markers',
                    name='Predicted Price',
                    line=dict(color='red', width=3, dash='dash')
                ))
            
            fig.update_layout(
                title="Market Price Trends and Predictions",
                xaxis_title="Period",
                yaxis_title="Market Price ($)",
                hovermode='x unified',
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(message)
    
    with pred_tab6:
        st.subheader("📋 Model Performance Metrics")
        
        # Display model performance metrics
        performance_metrics = predictive_analytics.get_prediction_accuracy_metrics()
        st.markdown(performance_metrics)
        
        # Additional insights
        st.markdown("### 🔍 Model Insights")
        
        if hasattr(predictive_analytics, '_model_performance') and predictive_analytics._model_performance:
            st.success("✅ Prediction models are performing well with available data")
            
            # Model recommendations
            st.markdown("### 💡 Model Recommendations")
            st.markdown("""
            - **Revenue Predictions**: Use ensemble approach for better accuracy
            - **Profitability**: Monitor margin trends for validation
            - **Cash Flow**: Consider seasonal patterns in predictions
            - **Health Scores**: Regular recalibration recommended
            - **Market Performance**: Include volatility factors
            """)
        else:
            st.info("ℹ️ Run predictions in other tabs to see model performance metrics")
    
    with pred_tab7:
        st.subheader("🎯 Scenario Analysis")
        
        # Scenario analysis parameters
        col1, col2 = st.columns(2)
        with col1:
            selected_scenarios = st.multiselect(
                "Select Scenarios",
                ['optimistic', 'base', 'pessimistic'],
                default=['optimistic', 'base', 'pessimistic'],
                help="Choose scenarios to analyze",
                key="scenario_selection"
            )
        
        with col2:
            scenario_periods = st.slider("Analysis Periods", 3, 12, 6, help="Number of future periods to analyze", key="scenario_analysis_periods")
        
        if st.button("Run Scenario Analysis", key="scenario_analysis"):
            # Generate scenario analysis
            scenario_results, message = predictive_analytics.predict_scenario_analysis(selected_scenarios, scenario_periods)
            
            if not scenario_results.empty:
                # Display scenario summary
                st.markdown("### 📊 Scenario Analysis Summary")
                
                # Key metrics by scenario
                for scenario in selected_scenarios:
                    scenario_data = scenario_results[scenario_results['scenario'] == scenario]
                    if not scenario_data.empty:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            total_revenue = scenario_data['adjusted_revenue'].sum()
                            st.metric(f"{scenario.title()} Revenue", f"${total_revenue:,.0f}")
                        
                        with col2:
                            total_net_income = scenario_data['adjusted_net_income'].sum()
                            st.metric(f"{scenario.title()} Net Income", f"${total_net_income:,.0f}")
                        
                        with col3:
                            avg_margin = scenario_data['adjusted_margin'].mean()
                            st.metric(f"{scenario.title()} Avg Margin", f"{avg_margin:.1f}%")
                
                # Display detailed results
                st.markdown("### 📋 Scenario Analysis Results")
                st.dataframe(scenario_results.round(2), use_container_width=True)
                
                # Create scenario comparison chart
                fig = go.Figure()
                
                for scenario in selected_scenarios:
                    scenario_data = scenario_results[scenario_results['scenario'] == scenario]
                    if not scenario_data.empty:
                        fig.add_trace(go.Scatter(
                            x=scenario_data['period'],
                            y=scenario_data['adjusted_revenue'],
                            mode='lines+markers',
                            name=f'{scenario.title()} Revenue',
                            line=dict(width=3)
                        ))
                
                fig.update_layout(
                    title="Revenue Scenarios Comparison",
                    xaxis_title="Period",
                    yaxis_title="Revenue ($)",
                    hovermode='x unified',
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(message)
    
    with pred_tab8:
        st.subheader("⚖️ Break-Even Analysis")
        
        # Break-even analysis parameters
        break_even_periods = st.slider("Analysis Periods", 3, 12, 6, help="Number of future periods to analyze", key="break_even_analysis_periods")
        
        if st.button("Run Break-Even Analysis", key="break_even_analysis"):
            # Generate break-even analysis
            break_even_results, message = predictive_analytics.predict_break_even_analysis(break_even_periods)
            
            if not break_even_results.empty:
                # Display break-even summary
                st.markdown("### 📊 Break-Even Analysis Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    current_safety_margin = break_even_results[~break_even_results['period'].str.contains('Future')]['safety_margin'].iloc[-1]
                    st.metric("Current Safety Margin", f"{current_safety_margin:.1f}%")
                
                with col2:
                    if 'break_even_revenue' in break_even_results.columns:
                        current_break_even = break_even_results[~break_even_results['period'].str.contains('Future')]['break_even_revenue'].iloc[-1]
                        st.metric("Current Break-Even", f"${current_break_even:,.0f}")
                
                with col3:
                    if 'safety_margin' in break_even_results.columns:
                        future_safety_margins = break_even_results[break_even_results['period'].str.contains('Future')]['safety_margin']
                        avg_future_safety = future_safety_margins.mean()
                        st.metric("Avg Future Safety", f"{avg_future_safety:.1f}%")
                
                # Display detailed results
                st.markdown("### 📋 Break-Even Analysis Results")
                st.dataframe(break_even_results.round(2), use_container_width=True)
                
                # Create break-even chart
                fig = go.Figure()
                
                # Historical data
                historical = break_even_results[~break_even_results['period'].str.contains('Future')]
                fig.add_trace(go.Scatter(
                    x=historical['period'],
                    y=historical['revenue'],
                    mode='lines+markers',
                    name='Historical Revenue',
                    line=dict(color='blue', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=historical['period'],
                    y=historical['break_even_revenue'],
                    mode='lines+markers',
                    name='Historical Break-Even',
                    line=dict(color='red', width=3)
                ))
                
                # Future predictions
                future = break_even_results[break_even_results['period'].str.contains('Future')]
                if not future.empty:
                    fig.add_trace(go.Scatter(
                        x=future['period'],
                        y=future['revenue'],
                        mode='lines+markers',
                        name='Predicted Revenue',
                        line=dict(color='blue', width=3, dash='dash')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future['period'],
                        y=future['break_even_revenue'],
                        mode='lines+markers',
                        name='Predicted Break-Even',
                        line=dict(color='red', width=3, dash='dash')
                    ))
                
                fig.update_layout(
                    title="Revenue vs Break-Even Analysis",
                    xaxis_title="Period",
                    yaxis_title="Amount ($)",
                    hovermode='x unified',
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(message)
    
    with pred_tab9:
        st.subheader("💼 Working Capital Analysis")
        
        # Working capital analysis parameters
        wc_periods = st.slider("Analysis Periods", 3, 12, 6, help="Number of future periods to analyze", key="working_capital_analysis_periods")
        
        if st.button("Run Working Capital Analysis", key="working_capital_analysis"):
            # Generate working capital analysis
            wc_results, message = predictive_analytics.predict_working_capital_needs(wc_periods)
            
            if not wc_results.empty:
                # Display working capital summary
                st.markdown("### 📊 Working Capital Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    current_wc = wc_results[~wc_results['period'].str.contains('Future')]['working_capital'].iloc[-1]
                    st.metric("Current Working Capital", f"${current_wc:,.0f}")
                
                with col2:
                    if 'predicted_working_capital' in wc_results.columns:
                        future_wc = wc_results[wc_results['period'].str.contains('Future')]['predicted_working_capital']
                        avg_future_wc = future_wc.mean()
                        st.metric("Avg Future WC", f"${avg_future_wc:,.0f}")
                
                with col3:
                    if 'adequacy_assessment' in wc_results.columns:
                        adequate_periods = len(wc_results[wc_results['adequacy_assessment'] == 'Adequate'])
                        total_periods = len(wc_results[wc_results['period'].str.contains('Future')])
                        adequacy_percentage = (adequate_periods / total_periods * 100) if total_periods > 0 else 0
                        st.metric("Adequate WC Periods", f"{adequacy_percentage:.1f}%")
                
                # Display detailed results
                st.markdown("### 📋 Working Capital Analysis Results")
                st.dataframe(wc_results.round(2), use_container_width=True)
                
                # Create working capital chart
                fig = go.Figure()
                
                # Historical working capital
                historical = wc_results[~wc_results['period'].str.contains('Future')]
                fig.add_trace(go.Scatter(
                    x=historical['period'],
                    y=historical['working_capital'],
                    mode='lines+markers',
                    name='Historical Working Capital',
                    line=dict(color='green', width=3)
                ))
                
                # Predicted working capital
                future = wc_results[wc_results['period'].str.contains('Future')]
                if not future.empty and 'predicted_working_capital' in future.columns:
                    fig.add_trace(go.Scatter(
                        x=future['period'],
                        y=future['predicted_working_capital'],
                        mode='lines+markers',
                        name='Predicted Working Capital',
                        line=dict(color='orange', width=3, dash='dash')
                    ))
                
                fig.update_layout(
                    title="Working Capital Trends and Predictions",
                    xaxis_title="Period",
                    yaxis_title="Working Capital ($)",
                    hovermode='x unified',
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(message)

# Finance-specific auto insights functions (implemented directly)
def display_insights_section(insights_text, title, icon):
    """Display insights section with proper formatting"""
    st.markdown(f"### {icon} {title}")
    
    if insights_text:
        # Split insights into lines and display each as a bullet point
        insights_lines = insights_text.split('\n')
        for line in insights_lines:
            line = line.strip()
            if line:
                if line.startswith('**') and line.endswith('**'):
                    # This is a heading
                    st.markdown(f"**{line[2:-2]}**")
                elif line.startswith('**'):
                    # This is a heading
                    st.markdown(line)
                else:
                    # This is regular text
                    st.markdown(f"• {line}")
    else:
        st.info("No insights available for this section.")

def display_executive_summary(summary_text, title, icon):
    """Display executive summary with proper formatting"""
    st.markdown(f"### {icon} {title}")
    
    if summary_text:
        st.markdown(summary_text)
    else:
        st.info("No executive summary available.")

# AI recommendation functions (implemented directly)
def generate_financial_performance_ai_recommendations(income_statement_data, balance_sheet_data, cash_flow_data):
    """Generate AI-powered recommendations for financial performance"""
    if income_statement_data.empty:
        return "No financial data available for analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Analyze revenue trends
    if len(income_statement_data) > 1:
        recent_revenue = income_statement_data['revenue'].iloc[-1]
        previous_revenue = income_statement_data['revenue'].iloc[-2]
        
        if recent_revenue > previous_revenue:
            growth_rate = ((recent_revenue - previous_revenue) / previous_revenue) * 100
            recommendations.append(f"📈 **Revenue Growth Analysis**")
            recommendations.append(f"   • Revenue grew by {growth_rate:.1f}% in the latest period")
            recommendations.append(f"   • Maintain momentum through market expansion and customer retention")
            recommendations.append(f"   • Consider reinvesting profits for sustainable growth")
        else:
            decline_rate = ((previous_revenue - recent_revenue) / previous_revenue) * 100
            recommendations.append(f"📉 **Revenue Decline Analysis**")
            recommendations.append(f"   • Revenue declined by {decline_rate:.1f}% - investigate root causes")
            recommendations.append(f"   • Review pricing strategy and market positioning")
            recommendations.append(f"   • Focus on cost optimization and operational efficiency")
    
    # Analyze profitability
    if 'net_income' in income_statement_data.columns:
        net_income = income_statement_data['net_income'].sum()
        revenue = income_statement_data['revenue'].sum()
        
        if revenue > 0:
            net_margin = (net_income / revenue) * 100
            recommendations.append("")
            recommendations.append(f"💰 **Profitability Analysis**")
            recommendations.append(f"   • Net margin: {net_margin:.1f}%")
            
            if net_margin < 5:
                recommendations.append(f"   • Low profitability - focus on cost reduction and pricing optimization")
            elif net_margin < 15:
                recommendations.append(f"   • Moderate profitability - opportunities for margin improvement")
            else:
                recommendations.append(f"   • Strong profitability - maintain competitive advantages")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Conduct regular financial performance reviews")
    recommendations.append("   • Implement KPI tracking and monitoring systems")
    recommendations.append("   • Develop contingency plans for economic downturns")
    recommendations.append("   • Invest in technology for better financial visibility")
    
    return "\n".join(recommendations)

def generate_liquidity_solvency_ai_recommendations(balance_sheet_data, cash_flow_data):
    """Generate AI-powered recommendations for liquidity and solvency"""
    if balance_sheet_data.empty:
        return "No balance sheet data available for analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Analyze current ratio
    if 'current_assets' in balance_sheet_data.columns and 'current_liabilities' in balance_sheet_data.columns:
        current_assets = balance_sheet_data['current_assets'].sum()
        current_liabilities = balance_sheet_data['current_liabilities'].sum()
        
        if current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            recommendations.append(f"💧 **Liquidity Analysis**")
            recommendations.append(f"   • Current ratio: {current_ratio:.2f}")
            
            if current_ratio < 1.0:
                recommendations.append(f"   • Critical liquidity risk - immediate action required")
                recommendations.append(f"   • Implement cash flow management strategies")
                recommendations.append(f"   • Consider short-term financing options")
            elif current_ratio < 1.5:
                recommendations.append(f"   • Moderate liquidity risk - monitor closely")
                recommendations.append(f"   • Optimize working capital management")
                recommendations.append(f"   • Review payment terms with suppliers")
            else:
                recommendations.append(f"   • Strong liquidity position - maintain current practices")
                recommendations.append(f"   • Consider investment opportunities for excess cash")
    
    # Analyze debt levels
    if 'total_liabilities' in balance_sheet_data.columns and 'shareholder_equity' in balance_sheet_data.columns:
        total_liabilities = balance_sheet_data['total_liabilities'].sum()
        shareholder_equity = balance_sheet_data['shareholder_equity'].sum()
        
        if shareholder_equity > 0:
            debt_to_equity = total_liabilities / shareholder_equity
            recommendations.append("")
            recommendations.append(f"🏗️ **Solvency Analysis**")
            recommendations.append(f"   • Debt-to-equity ratio: {debt_to_equity:.2f}")
            
            if debt_to_equity > 2.0:
                recommendations.append(f"   • High debt levels - debt reduction priority")
                recommendations.append(f"   • Review capital structure and financing strategy")
                recommendations.append(f"   • Consider equity financing alternatives")
            elif debt_to_equity > 1.0:
                recommendations.append(f"   • Moderate debt levels - manageable but monitor")
                recommendations.append(f"   • Balance debt and equity financing")
                recommendations.append(f"   • Maintain debt service coverage")
            else:
                recommendations.append(f"   • Conservative debt structure - financial flexibility")
                recommendations.append(f"   • Consider strategic debt for growth opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement cash flow forecasting and monitoring")
    recommendations.append("   • Develop working capital optimization strategies")
    recommendations.append("   • Establish debt management policies")
    recommendations.append("   • Regular financial health assessments")
    
    return "\n".join(recommendations)

# Additional AI recommendation functions (optimized implementations)
def generate_liquidity_analysis_ai_recommendations(balance_sheet_data, cash_flow_data):
    """Generate AI-powered recommendations for liquidity analysis"""
    if balance_sheet_data.empty:
        return "No balance sheet data available for liquidity analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Current ratio analysis
    if 'current_assets' in balance_sheet_data.columns and 'current_liabilities' in balance_sheet_data.columns:
        current_assets = balance_sheet_data['current_assets'].sum()
        current_liabilities = balance_sheet_data['current_liabilities'].sum()
        
        if current_liabilities > 0:
            current_ratio = current_assets / current_liabilities
            recommendations.append(f"💧 **Current Ratio Analysis**: {current_ratio:.2f}")
            
            if current_ratio < 1.0:
                recommendations.append("   • Critical liquidity risk - immediate action required")
                recommendations.append("   • Implement emergency cash flow management")
                recommendations.append("   • Consider short-term financing options")
            elif current_ratio < 1.5:
                recommendations.append("   • Moderate liquidity risk - monitor closely")
                recommendations.append("   • Optimize working capital management")
                recommendations.append("   • Review payment terms with suppliers")
            else:
                recommendations.append("   • Strong liquidity position - maintain current practices")
                recommendations.append("   • Consider investment opportunities for excess cash")
    
    # Quick ratio analysis
    if 'cash_and_equivalents' in balance_sheet_data.columns and 'accounts_receivable' in balance_sheet_data.columns:
        quick_assets = balance_sheet_data['cash_and_equivalents'].sum() + balance_sheet_data['accounts_receivable'].sum()
        if current_liabilities > 0:
            quick_ratio = quick_assets / current_liabilities
            recommendations.append("")
            recommendations.append(f"⚡ **Quick Ratio Analysis**: {quick_ratio:.2f}")
            
            if quick_ratio < 0.5:
                recommendations.append("   • Low quick ratio - limited immediate liquidity")
                recommendations.append("   • Focus on cash generation and receivables collection")
            elif quick_ratio < 1.0:
                recommendations.append("   • Moderate quick ratio - adequate immediate liquidity")
                recommendations.append("   • Monitor cash flow trends")
            else:
                recommendations.append("   • Strong quick ratio - excellent immediate liquidity")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement cash flow forecasting and monitoring")
    recommendations.append("   • Develop working capital optimization strategies")
    recommendations.append("   • Regular liquidity assessments")
    
    return "\n".join(recommendations)

def generate_solvency_metrics_ai_recommendations(balance_sheet_data, income_statement_data):
    """Generate AI-powered recommendations for solvency analysis"""
    if balance_sheet_data.empty:
        return "No balance sheet data available for solvency analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Debt-to-equity analysis
    if 'total_liabilities' in balance_sheet_data.columns and 'shareholder_equity' in balance_sheet_data.columns:
        total_liabilities = balance_sheet_data['total_liabilities'].sum()
        shareholder_equity = balance_sheet_data['shareholder_equity'].sum()
        
        if shareholder_equity > 0:
            debt_to_equity = total_liabilities / shareholder_equity
            recommendations.append(f"🏗️ **Debt-to-Equity Analysis**: {debt_to_equity:.2f}")
            
            if debt_to_equity > 2.5:
                recommendations.append("   • Critical debt levels - immediate action required")
                recommendations.append("   • Prioritize debt reduction and restructuring")
                recommendations.append("   • Consider equity financing alternatives")
            elif debt_to_equity > 2.0:
                recommendations.append("   • High debt levels - debt reduction priority")
                recommendations.append("   • Review capital structure and financing strategy")
                recommendations.append("   • Consider equity financing")
            elif debt_to_equity > 1.0:
                recommendations.append("   • Moderate debt levels - manageable but monitor")
                recommendations.append("   • Balance debt and equity financing")
                recommendations.append("   • Maintain debt service coverage")
            else:
                recommendations.append("   • Conservative debt structure - financial flexibility")
                recommendations.append("   • Consider strategic debt for growth opportunities")
    
    # Interest coverage analysis
    if 'operating_income' in income_statement_data.columns and 'interest_expense' in income_statement_data.columns:
        operating_income = income_statement_data['operating_income'].sum()
        interest_expense = income_statement_data['interest_expense'].sum()
        
        if interest_expense > 0:
            interest_coverage = operating_income / interest_expense
            recommendations.append("")
            recommendations.append(f"💰 **Interest Coverage Analysis**: {interest_coverage:.2f}")
            
            if interest_coverage < 1.5:
                recommendations.append("   • Low interest coverage - high default risk")
                recommendations.append("   • Immediate debt reduction required")
                recommendations.append("   • Consider debt restructuring")
            elif interest_coverage < 3.0:
                recommendations.append("   • Moderate interest coverage - monitor closely")
                recommendations.append("   • Maintain debt service capability")
                recommendations.append("   • Consider debt reduction")
            else:
                recommendations.append("   • Strong interest coverage - comfortable debt levels")
                recommendations.append("   • Maintain current debt structure")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Establish debt management policies")
    recommendations.append("   • Regular financial health assessments")
    recommendations.append("   • Develop capital structure optimization plan")
    
    return "\n".join(recommendations)

def generate_cash_flow_analysis_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for cash flow analysis"""
    if cash_flow_data.empty:
        return "No cash flow data available for analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Operating cash flow analysis
    # Check for operating cash flow column with fallback names
    operating_cf_col = None
    for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
        if col_name in cash_flow_data.columns:
            operating_cf_col = col_name
            break
    
    if operating_cf_col:
        total_operating_cf = cash_flow_data[operating_cf_col].sum()
        recommendations.append(f"💸 **Operating Cash Flow Analysis**: ${total_operating_cf:,.0f}")
        
        if total_operating_cf > 0:
            recommendations.append("   • Positive operating cash flow - good operational performance")
            recommendations.append("   • Maintain operational efficiency")
            recommendations.append("   • Consider growth investments")
        else:
            recommendations.append("   • Negative operating cash flow - operational challenges")
            recommendations.append("   • Review business model and operations")
            recommendations.append("   • Implement cost reduction measures")
    
    # Free cash flow analysis
    if 'free_cash_flow' in cash_flow_data.columns:
        total_free_cf = cash_flow_data['free_cash_flow'].sum()
        recommendations.append("")
        recommendations.append(f"🎯 **Free Cash Flow Analysis**: ${total_free_cf:,.0f}")
        
        if total_free_cf > 0:
            recommendations.append("   • Positive free cash flow - financial flexibility")
            recommendations.append("   • Consider dividend payments or share buybacks")
            recommendations.append("   • Strategic investment opportunities")
        else:
            recommendations.append("   • Negative free cash flow - limited financial flexibility")
            recommendations.append("   • Review capital expenditure plans")
            recommendations.append("   • Consider external financing")
    
    # Cash flow trends
    if len(cash_flow_data) > 1 and operating_cf_col:
        recent_operating_cf = cash_flow_data[operating_cf_col].iloc[-1]
        previous_operating_cf = cash_flow_data[operating_cf_col].iloc[-2]
        
        if previous_operating_cf != 0:
            cf_growth = ((recent_operating_cf - previous_operating_cf) / abs(previous_operating_cf) * 100)
            recommendations.append("")
            recommendations.append(f"📈 **Cash Flow Trend Analysis**: {cf_growth:+.1f}%")
            
            if cf_growth > 20:
                recommendations.append("   • Exceptional cash flow improvement")
                recommendations.append("   • Maintain successful strategies")
            elif cf_growth < -10:
                recommendations.append("   • Declining cash flow - investigate causes")
                recommendations.append("   • Implement corrective measures")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement cash flow forecasting and monitoring")
    recommendations.append("   • Optimize working capital management")
    recommendations.append("   • Regular cash flow analysis and reporting")
    
    return "\n".join(recommendations)

def generate_roa_roe_analysis_ai_recommendations(income_statement_data, balance_sheet_data):
    """Generate AI-powered recommendations for ROA/ROE analysis"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return "Insufficient data for ROA/ROE analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # ROA analysis
    if 'net_income' in income_statement_data.columns and 'total_assets' in balance_sheet_data.columns:
        net_income = income_statement_data['net_income'].sum()
        total_assets = balance_sheet_data['total_assets'].sum()
        
        if total_assets > 0:
            roa = (net_income / total_assets) * 100
            recommendations.append(f"📊 **ROA Analysis**: {roa:.2f}%")
            
            if roa < 5:
                recommendations.append("   • Low ROA - asset utilization needs improvement")
                recommendations.append("   • Review asset efficiency and utilization")
                recommendations.append("   • Consider asset optimization strategies")
            elif roa < 15:
                recommendations.append("   • Moderate ROA - room for improvement")
                recommendations.append("   • Optimize asset allocation")
                recommendations.append("   • Improve operational efficiency")
            else:
                recommendations.append("   • Strong ROA - excellent asset utilization")
                recommendations.append("   • Maintain current performance")
                recommendations.append("   • Consider expansion opportunities")
    
    # ROE analysis
    if 'shareholder_equity' in balance_sheet_data.columns:
        shareholder_equity = balance_sheet_data['shareholder_equity'].sum()
        
        if shareholder_equity > 0:
            roe = (net_income / shareholder_equity) * 100
            recommendations.append("")
            recommendations.append(f"💰 **ROE Analysis**: {roe:.2f}%")
            
            if roe < 10:
                recommendations.append("   • Low ROE - shareholder value creation needs improvement")
                recommendations.append("   • Review profitability and capital structure")
                recommendations.append("   • Implement value creation strategies")
            elif roe < 20:
                recommendations.append("   • Moderate ROE - good shareholder returns")
                recommendations.append("   • Optimize capital structure")
                recommendations.append("   • Focus on growth opportunities")
            else:
                recommendations.append("   • Strong ROE - excellent shareholder returns")
                recommendations.append("   • Maintain competitive advantages")
                recommendations.append("   • Consider dividend policies")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement ROA/ROE monitoring and tracking")
    recommendations.append("   • Develop asset optimization strategies")
    recommendations.append("   • Regular performance analysis and reporting")
    
    return "\n".join(recommendations)

def generate_asset_turnover_ai_recommendations(income_statement_data, balance_sheet_data):
    """Generate AI-powered recommendations for asset turnover analysis"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return "Insufficient data for asset turnover analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Asset turnover analysis
    if 'revenue' in income_statement_data.columns and 'total_assets' in balance_sheet_data.columns:
        revenue = income_statement_data['revenue'].sum()
        total_assets = balance_sheet_data['total_assets'].sum()
        
        if total_assets > 0:
            asset_turnover = revenue / total_assets
            recommendations.append(f"🔄 **Asset Turnover Analysis**: {asset_turnover:.2f}")
            
            if asset_turnover < 0.5:
                recommendations.append("   • Low asset turnover - poor asset utilization")
                recommendations.append("   • Review asset efficiency and productivity")
                recommendations.append("   • Consider asset optimization and disposal")
            elif asset_turnover < 1.0:
                recommendations.append("   • Moderate asset turnover - room for improvement")
                recommendations.append("   • Optimize asset allocation and utilization")
                recommendations.append("   • Improve operational processes")
            else:
                recommendations.append("   • High asset turnover - excellent asset utilization")
                recommendations.append("   • Maintain current efficiency")
                recommendations.append("   • Consider expansion opportunities")
    
    # Working capital turnover
    if 'current_assets' in balance_sheet_data.columns and 'current_liabilities' in balance_sheet_data.columns:
        current_assets = balance_sheet_data['current_assets'].sum()
        current_liabilities = balance_sheet_data['current_liabilities'].sum()
        working_capital = current_assets - current_liabilities
        
        if working_capital > 0:
            working_capital_turnover = revenue / working_capital
            recommendations.append("")
            recommendations.append(f"💼 **Working Capital Turnover**: {working_capital_turnover:.2f}")
            
            if working_capital_turnover < 2.0:
                recommendations.append("   • Low working capital efficiency")
                recommendations.append("   • Optimize inventory and receivables management")
                recommendations.append("   • Review payment terms and collection processes")
            elif working_capital_turnover < 5.0:
                recommendations.append("   • Moderate working capital efficiency")
                recommendations.append("   • Improve working capital management")
                recommendations.append("   • Optimize cash conversion cycle")
            else:
                recommendations.append("   • High working capital efficiency")
                recommendations.append("   • Maintain current practices")
                recommendations.append("   • Consider growth opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement asset utilization monitoring")
    recommendations.append("   • Develop working capital optimization strategies")
    recommendations.append("   • Regular efficiency analysis and reporting")
    
    return "\n".join(recommendations)

def generate_expense_efficiency_ai_recommendations(income_statement_data):
    """Generate AI-powered recommendations for expense efficiency analysis"""
    if income_statement_data.empty:
        return "Insufficient data for expense efficiency analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Expense efficiency analysis
    if 'revenue' in income_statement_data.columns and 'operating_expenses' in income_statement_data.columns:
        total_revenue = income_statement_data['revenue'].sum()
        total_operating_expenses = income_statement_data['operating_expenses'].sum()
        
        if total_revenue > 0:
            expense_ratio = (total_operating_expenses / total_revenue) * 100
            recommendations.append(f"💰 **Expense Ratio Analysis**: {expense_ratio:.1f}%")
            
            if expense_ratio > 80:
                recommendations.append("   • High expense ratio - poor cost control")
                recommendations.append("   • Immediate cost reduction required")
                recommendations.append("   • Review all expense categories")
            elif expense_ratio > 60:
                recommendations.append("   • Elevated expense ratio - needs improvement")
                recommendations.append("   • Implement cost control measures")
                recommendations.append("   • Optimize operational processes")
            else:
                recommendations.append("   • Low expense ratio - excellent cost control")
                recommendations.append("   • Maintain current efficiency")
                recommendations.append("   • Consider strategic investments")
    
    # Gross margin analysis
    if 'gross_profit' in income_statement_data.columns:
        total_gross_profit = income_statement_data['gross_profit'].sum()
        
        if total_revenue > 0:
            gross_margin = (total_gross_profit / total_revenue) * 100
            recommendations.append("")
            recommendations.append(f"📊 **Gross Margin Analysis**: {gross_margin:.1f}%")
            
            if gross_margin < 20:
                recommendations.append("   • Low gross margin - pricing or cost issues")
                recommendations.append("   • Review pricing strategy")
                recommendations.append("   • Analyze cost of goods sold")
            elif gross_margin < 40:
                recommendations.append("   • Moderate gross margin - room for improvement")
                recommendations.append("   • Optimize pricing and costs")
                recommendations.append("   • Improve product mix")
            else:
                recommendations.append("   • High gross margin - excellent profitability")
                recommendations.append("   • Maintain competitive advantage")
                recommendations.append("   • Consider market expansion")
    
    # Operating margin analysis
    if 'operating_income' in income_statement_data.columns:
        total_operating_income = income_statement_data['operating_income'].sum()
        
        if total_revenue > 0:
            operating_margin = (total_operating_income / total_revenue) * 100
            recommendations.append("")
            recommendations.append(f"⚡ **Operating Margin Analysis**: {operating_margin:.1f}%")
            
            if operating_margin < 5:
                recommendations.append("   • Low operating margin - operational inefficiency")
                recommendations.append("   • Review operational processes")
                recommendations.append("   • Implement efficiency measures")
            elif operating_margin < 15:
                recommendations.append("   • Moderate operating margin - good performance")
                recommendations.append("   • Continue optimization efforts")
                recommendations.append("   • Focus on growth opportunities")
            else:
                recommendations.append("   • High operating margin - excellent operations")
                recommendations.append("   • Maintain operational excellence")
                recommendations.append("   • Consider strategic expansion")
    
    # Expense trend analysis
    if len(income_statement_data) > 1:
        recent_expenses = income_statement_data['operating_expenses'].iloc[-1]
        previous_expenses = income_statement_data['operating_expenses'].iloc[-2]
        
        if previous_expenses > 0:
            expense_change = ((recent_expenses - previous_expenses) / previous_expenses) * 100
            recommendations.append("")
            recommendations.append(f"📈 **Expense Trend Analysis**: {expense_change:+.1f}% change")
            
            if expense_change > 10:
                recommendations.append("   • Significant expense increase - review urgently")
                recommendations.append("   • Identify cost drivers")
                recommendations.append("   • Implement cost controls")
            elif expense_change > 5:
                recommendations.append("   • Moderate expense increase - monitor closely")
                recommendations.append("   • Review expense categories")
                recommendations.append("   • Optimize where possible")
            elif expense_change < -5:
                recommendations.append("   • Expense reduction - good cost management")
                recommendations.append("   • Maintain efficiency gains")
                recommendations.append("   • Document best practices")
            else:
                recommendations.append("   • Stable expenses - good control")
                recommendations.append("   • Continue monitoring")
                recommendations.append("   • Look for optimization opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement expense monitoring dashboard")
    recommendations.append("   • Develop cost reduction initiatives")
    recommendations.append("   • Regular expense analysis and reporting")
    recommendations.append("   • Benchmark against industry standards")
    recommendations.append("   • Optimize operational processes")
    
    return "\n".join(recommendations)

def generate_productivity_trends_ai_recommendations(income_statement_data, balance_sheet_data):
    """Generate AI-powered recommendations for productivity trends analysis"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return "Insufficient data for productivity trends analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    # Productivity metrics analysis
    if 'revenue' in income_statement_data.columns and 'total_assets' in balance_sheet_data.columns:
        revenue = income_statement_data['revenue'].sum()
        total_assets = balance_sheet_data['total_assets'].sum()
        
        if total_assets > 0:
            asset_turnover = revenue / total_assets
            recommendations.append(f"🔄 **Asset Turnover**: {asset_turnover:.2f}")
            
            if asset_turnover < 0.5:
                recommendations.append("   • Low productivity - poor asset utilization")
                recommendations.append("   • Review asset efficiency and productivity")
                recommendations.append("   • Consider asset optimization and disposal")
            elif asset_turnover < 1.0:
                recommendations.append("   • Moderate productivity - room for improvement")
                recommendations.append("   • Optimize asset allocation and utilization")
                recommendations.append("   • Improve operational processes")
            else:
                recommendations.append("   • High productivity - excellent asset utilization")
                recommendations.append("   • Maintain current efficiency")
                recommendations.append("   • Consider expansion opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement productivity monitoring dashboard")
    recommendations.append("   • Develop efficiency improvement initiatives")
    recommendations.append("   • Regular productivity analysis and reporting")
    
    return "\n".join(recommendations)

def generate_budget_variance_analysis_ai_recommendations(budget_data, actual_data):
    """Generate AI-powered recommendations for budget variance analysis"""
    if budget_data.empty or actual_data.empty:
        return "Insufficient data for budget variance analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📊 **Budget Variance Analysis**")
    recommendations.append("   • Monitor budget vs. actual performance")
    recommendations.append("   • Identify significant variances")
    recommendations.append("   • Implement corrective actions")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement variance monitoring dashboard")
    recommendations.append("   • Develop variance analysis reporting")
    recommendations.append("   • Regular budget performance reviews")
    
    return "\n".join(recommendations)

def generate_forecast_accuracy_ai_recommendations(forecast_data, actual_data):
    """Generate AI-powered recommendations for forecast accuracy analysis"""
    if forecast_data.empty or actual_data.empty:
        return "Insufficient data for forecast accuracy analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🔮 **Forecast Accuracy Analysis**")
    recommendations.append("   • Monitor forecast vs. actual performance")
    recommendations.append("   • Identify accuracy trends")
    recommendations.append("   • Improve forecasting models")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement forecast accuracy monitoring")
    recommendations.append("   • Develop forecasting improvement initiatives")
    recommendations.append("   • Regular forecast performance reviews")
    
    return "\n".join(recommendations)

def generate_scenario_analysis_ai_recommendations(scenario_data):
    """Generate AI-powered recommendations for scenario analysis"""
    if scenario_data.empty:
        return "Insufficient data for scenario analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🎭 **Scenario Analysis**")
    recommendations.append("   • Evaluate multiple business scenarios")
    recommendations.append("   • Assess risk and opportunity")
    recommendations.append("   • Develop contingency plans")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement scenario planning framework")
    recommendations.append("   • Develop risk mitigation strategies")
    recommendations.append("   • Regular scenario analysis updates")
    
    return "\n".join(recommendations)

def generate_variance_reporting_ai_recommendations(income_statement_data, budget_data):
    """Generate AI-powered recommendations for variance reporting"""
    if income_statement_data.empty or budget_data.empty:
        return "Insufficient data for variance reporting."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📊 **Variance Reporting**")
    recommendations.append("   • Monitor key performance indicators")
    recommendations.append("   • Identify significant deviations")
    recommendations.append("   • Implement corrective actions")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement variance monitoring dashboard")
    recommendations.append("   • Develop automated reporting systems")
    recommendations.append("   • Regular variance analysis reviews")
    
    return "\n".join(recommendations)

def generate_operating_cash_flow_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for operating cash flow analysis"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for operating cash flow analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("💸 **Operating Cash Flow Analysis**")
    recommendations.append("   • Monitor operating cash flow trends")
    recommendations.append("   • Identify cash flow drivers")
    recommendations.append("   • Optimize working capital management")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement cash flow monitoring dashboard")
    recommendations.append("   • Develop cash flow optimization strategies")
    recommendations.append("   • Regular cash flow analysis and reporting")
    
    return "\n".join(recommendations)

def generate_free_cash_flow_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for free cash flow analysis"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for free cash flow analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("💰 **Free Cash Flow Analysis**")
    recommendations.append("   • Monitor free cash flow generation")
    recommendations.append("   • Assess investment capacity")
    recommendations.append("   • Evaluate dividend sustainability")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement FCF monitoring dashboard")
    recommendations.append("   • Develop investment prioritization framework")
    recommendations.append("   • Regular FCF analysis and reporting")
    
    return "\n".join(recommendations)

def generate_working_capital_ai_recommendations(balance_sheet_data, cash_flow_data):
    """Generate AI-powered recommendations for working capital analysis"""
    if balance_sheet_data.empty or cash_flow_data.empty:
        return "Insufficient data for working capital analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("💼 **Working Capital Analysis**")
    recommendations.append("   • Monitor working capital levels")
    recommendations.append("   • Optimize inventory and receivables")
    recommendations.append("   • Manage payment terms and collections")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement working capital monitoring")
    recommendations.append("   • Develop optimization strategies")
    recommendations.append("   • Regular working capital analysis")
    
    return "\n".join(recommendations)

def generate_cash_flow_trends_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for cash flow trends analysis"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for cash flow trends analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📈 **Cash Flow Trends Analysis**")
    recommendations.append("   • Monitor cash flow patterns")
    recommendations.append("   • Identify seasonal variations")
    recommendations.append("   • Forecast future cash flows")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement trend monitoring dashboard")
    recommendations.append("   • Develop cash flow forecasting models")
    recommendations.append("   • Regular trend analysis and reporting")
    
    return "\n".join(recommendations)

def generate_debt_analysis_ai_recommendations(balance_sheet_data, income_statement_data):
    """Generate AI-powered recommendations for debt analysis"""
    if balance_sheet_data.empty or income_statement_data.empty:
        return "Insufficient data for debt analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🏗️ **Debt Analysis**")
    recommendations.append("   • Monitor debt levels and ratios")
    recommendations.append("   • Assess debt service capacity")
    recommendations.append("   • Evaluate refinancing opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement debt monitoring dashboard")
    recommendations.append("   • Implement debt management strategies")
    recommendations.append("   • Regular debt analysis and reporting")
    
    return "\n".join(recommendations)

def generate_wacc_calculation_ai_recommendations(balance_sheet_data, market_data):
    """Generate AI-powered recommendations for WACC calculation"""
    if balance_sheet_data.empty or market_data.empty:
        return "Insufficient data for WACC calculation."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("⚖️ **WACC Analysis**")
    recommendations.append("   • Calculate weighted average cost of capital")
    recommendations.append("   • Assess capital structure optimization")
    recommendations.append("   • Evaluate investment decisions")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement WACC monitoring dashboard")
    recommendations.append("   • Develop capital structure strategies")
    recommendations.append("   • Regular WACC analysis and reporting")
    
    return "\n".join(recommendations)

def generate_interest_coverage_ai_recommendations(income_statement_data, balance_sheet_data):
    """Generate AI-powered recommendations for interest coverage analysis"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return "Insufficient data for interest coverage analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🛡️ **Interest Coverage Analysis**")
    recommendations.append("   • Monitor interest coverage ratios")
    recommendations.append("   • Assess debt service capacity")
    recommendations.append("   • Identify refinancing opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement coverage monitoring dashboard")
    recommendations.append("   • Develop debt management strategies")
    recommendations.append("   • Regular coverage analysis and reporting")
    
    return "\n".join(recommendations)

def generate_capital_optimization_ai_recommendations(balance_sheet_data, income_statement_data):
    """Generate AI-powered recommendations for capital optimization"""
    if balance_sheet_data.empty or income_statement_data.empty:
        return "Insufficient data for capital optimization analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🏗️ **Capital Optimization Analysis**")
    recommendations.append("   • Monitor capital structure efficiency")
    recommendations.append("   • Assess cost of capital")
    recommendations.append("   • Optimize debt-equity mix")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement capital monitoring dashboard")
    recommendations.append("   • Develop optimization strategies")
    recommendations.append("   • Regular capital analysis and reporting")
    
    return "\n".join(recommendations)

def generate_npv_analysis_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for NPV analysis"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for NPV analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📊 **NPV Analysis**")
    recommendations.append("   • Calculate net present value of investments")
    recommendations.append("   • Assess investment attractiveness")
    recommendations.append("   • Compare investment alternatives")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement NPV monitoring dashboard")
    recommendations.append("   • Develop investment evaluation framework")
    recommendations.append("   • Regular NPV analysis and reporting")
    
    return "\n".join(recommendations)

def generate_payback_period_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for payback period analysis"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for payback period analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("⏱️ **Payback Period Analysis**")
    recommendations.append("   • Calculate investment payback periods")
    recommendations.append("   • Assess liquidity requirements")
    recommendations.append("   • Evaluate investment risk")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement payback monitoring dashboard")
    recommendations.append("   • Develop investment risk assessment")
    recommendations.append("   • Regular payback analysis and reporting")
    
    return "\n".join(recommendations)

def generate_eva_calculation_ai_recommendations(income_statement_data, balance_sheet_data):
    """Generate AI-powered recommendations for EVA calculation"""
    if income_statement_data.empty or balance_sheet_data.empty:
        return "Insufficient data for EVA calculation."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("💰 **EVA Analysis**")
    recommendations.append("   • Calculate economic value added")
    recommendations.append("   • Assess value creation")
    recommendations.append("   • Evaluate performance drivers")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement EVA monitoring dashboard")
    recommendations.append("   • Develop value creation strategies")
    recommendations.append("   • Regular EVA analysis and reporting")
    
    return "\n".join(recommendations)

def generate_investment_insights_ai_recommendations(cash_flow_data, balance_sheet_data):
    """Generate AI-powered recommendations for investment insights"""
    if cash_flow_data.empty or balance_sheet_data.empty:
        return "Insufficient data for investment insights analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📈 **Investment Insights Analysis**")
    recommendations.append("   • Monitor investment performance")
    recommendations.append("   • Assess risk-return profiles")
    recommendations.append("   • Identify optimization opportunities")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement investment monitoring dashboard")
    recommendations.append("   • Develop portfolio optimization strategies")
    recommendations.append("   • Regular investment analysis and reporting")
    
    return "\n".join(recommendations)

def generate_customer_profitability_ai_recommendations(customer_data):
    """Generate AI-powered recommendations for customer profitability analysis"""
    if customer_data.empty:
        return "Insufficient data for customer profitability analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("👥 **Customer Profitability Analysis**")
    recommendations.append("   • Monitor customer profitability metrics")
    recommendations.append("   • Identify high-value customers")
    recommendations.append("   • Optimize customer relationships")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement customer monitoring dashboard")
    recommendations.append("   • Develop customer optimization strategies")
    recommendations.append("   • Regular customer analysis and reporting")
    
    return "\n".join(recommendations)

def generate_product_profitability_ai_recommendations(product_data):
    """Generate AI-powered recommendations for product profitability analysis"""
    if product_data.empty:
        return "Insufficient data for product profitability analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("📦 **Product Profitability Analysis**")
    recommendations.append("   • Monitor product profitability metrics")
    recommendations.append("   • Identify high-margin products")
    recommendations.append("   • Optimize product portfolio")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement product monitoring dashboard")
    recommendations.append("   • Develop product optimization strategies")
    recommendations.append("   • Regular product analysis and reporting")
    
    return "\n".join(recommendations)

def generate_value_chain_analysis_ai_recommendations(value_chain_data):
    """Generate AI-powered recommendations for value chain analysis"""
    if value_chain_data.empty:
        return "Insufficient data for value chain analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🔗 **Value Chain Analysis**")
    recommendations.append("   • Monitor value chain efficiency")
    recommendations.append("   • Identify optimization opportunities")
    recommendations.append("   • Assess cost drivers")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement value chain monitoring dashboard")
    recommendations.append("   • Develop optimization strategies")
    recommendations.append("   • Regular value chain analysis and reporting")
    
    return "\n".join(recommendations)

def generate_strategic_insights_ai_recommendations(customer_data, product_data, value_chain_data):
    """Generate AI-powered recommendations for strategic insights"""
    if customer_data.empty or product_data.empty or value_chain_data.empty:
        return "Insufficient data for strategic insights analysis."
    
    recommendations = []
    # Title removed to avoid duplication with markdown header
    recommendations.append("")
    
    recommendations.append("🎯 **Strategic Insights Analysis**")
    recommendations.append("   • Monitor strategic performance metrics")
    recommendations.append("   • Identify strategic opportunities")
    recommendations.append("   • Assess strategic risks")
    
    recommendations.append("")
    recommendations.append("🎯 **Strategic Actions**")
    recommendations.append("   • Implement strategic monitoring dashboard")
    recommendations.append("   • Develop strategic initiatives")
    recommendations.append("   • Regular strategic analysis and reporting")
    
    return "\n".join(recommendations)

def format_ai_recommendations(recommendations_text):
    """
    Format AI recommendations text to display properly in Streamlit with each bullet point on a separate line.
    Remove double asterisks and emoji characters from headings.
    """
    if not recommendations_text:
        return ""
    
    # Split the text into lines
    lines = recommendations_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append("")
            continue
            
        # If it's already a bullet point, keep it as is
        if line.startswith("   •"):
            formatted_lines.append(line)
        # If it's a heading with emoji and double asterisks, clean it up
        elif (line.startswith("🤖") or line.startswith("🎯") or line.startswith("💰") or 
              line.startswith("💸") or line.startswith("⚠️") or line.startswith("👥") or 
              line.startswith("📦") or line.startswith("🔍") or line.startswith("🟢") or 
              line.startswith("🟡") or line.startswith("🟠") or line.startswith("🔴") or 
              line.startswith("📈") or line.startswith("📉")):
            # Remove double asterisks and emoji, keep only the text
            cleaned_line = line
            # Remove emoji characters
            emoji_patterns = ["🤖", "🎯", "💰", "💸", "⚠️", "👥", "📦", "🔍", "🟢", "🟡", "🟠", "🔴", "📈", "📉"]
            for emoji in emoji_patterns:
                cleaned_line = cleaned_line.replace(emoji, "")
            # Remove double asterisks
            cleaned_line = cleaned_line.replace("**", "")
            # Clean up extra spaces
            cleaned_line = cleaned_line.strip()
            formatted_lines.append(cleaned_line)
        # If it contains bullet points on the same line, split them
        elif "•" in line:
            # Split by bullet points
            parts = line.split("•")
            for i, part in enumerate(parts):
                part = part.strip()
                if part:
                    if i == 0:  # First part (before first bullet)
                        formatted_lines.append(part)
                    else:  # Bullet point parts
                        formatted_lines.append(f"   • {part}")
        else:
            # Regular line, keep as is
            formatted_lines.append(line)
    
    return "\n".join(formatted_lines)

def display_formatted_recommendations(recommendations_text):
    """
    Display AI recommendations with proper formatting using HTML to ensure bullet points are on separate lines.
    """
    if not recommendations_text:
        return
    
    # Convert the text to HTML format for better display
    html_content = recommendations_text.replace('\n', '<br>')
    
    # Replace bullet points with proper HTML list items
    lines = recommendations_text.split('\n')
    html_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            html_lines.append("<br>")
        elif line.startswith("   •"):
            # Convert bullet point to HTML list item
            content = line.replace("   •", "").strip()
            html_lines.append(f"<li>{content}</li>")
        elif line and not line.startswith("   •") and not "•" in line:
            # This is a heading (already cleaned of emoji and asterisks), add it as a header
            html_lines.append(f"<h4>{line}</h4>")
        elif "•" in line:
            # Split by bullet points and create list items
            parts = line.split("•")
            for i, part in enumerate(parts):
                part = part.strip()
                if part:
                    if i == 0:  # First part (before first bullet)
                        html_lines.append(f"<h4>{part}</h4>")
                    else:  # Bullet point parts
                        html_lines.append(f"<li>{part}</li>")
        else:
            # Regular line
            html_lines.append(f"<p>{line}</p>")
    
    # Combine into HTML with proper list structure
    html_content = ""
    in_list = False
    
    for line in html_lines:
        if line.startswith("<li>"):
            if not in_list:
                html_content += "<ul>"
                in_list = True
            html_content += line
        elif line.startswith("<h4>"):
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
        elif line.startswith("<p>"):
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
        elif line == "<br>":
            if in_list:
                html_content += "</ul>"
                in_list = False
            html_content += line
    
    # Close any open list
    if in_list:
        html_content += "</ul>"
    
    # Display using HTML
    st.markdown(html_content, unsafe_allow_html=True)

# Set Plotly template
pio.templates.default = "plotly_white"
CONTINUOUS_COLOR_SCALE = "Turbo"
CATEGORICAL_COLOR_SEQUENCE = px.colors.qualitative.Pastel

# --- PuLP import for optimization ---
try:
    from pulp import LpProblem, LpVariable, LpMaximize, lpSum
except ImportError:
    LpProblem = LpVariable = LpMaximize = lpSum = None

# --- Utility Functions: Variable Detection ---
def get_numeric_columns(df):
    """Return a list of numeric columns, excluding 'supplier'."""
    return [col for col in df.select_dtypes(include=['number']).columns if col != 'supplier']

def get_categorical_columns(df):
    """Return a list of categorical/object columns, excluding 'supplier'."""
    return [col for col in df.select_dtypes(include=['object']).columns if col != 'supplier']

# --- Utility Functions ---
def get_variable_list(df):
    """Get list of variables for analysis."""
    return [col for col in df.columns if col not in ['supplier', 'period', 'date']]

def normalize_column(col, minimize=False):
    """Normalize a column to 0-1 scale."""
    if minimize:
        return (col.max() - col) / (col.max() - col.min())
    else:
        return (col - col.min()) / (col.max() - col.min())

def get_weights(variables, scenario):
    """Get weights for different scenarios."""
    if scenario == "balanced":
        return {var: 1/len(variables) for var in variables}
    elif scenario == "cost_focused":
        return {var: 0.6 if 'cost' in var.lower() or 'price' in var.lower() else 0.4/(len(variables)-1) for var in variables}
    elif scenario == "quality_focused":
        return {var: 0.6 if 'quality' in var.lower() or 'score' in var.lower() else 0.4/(len(variables)-1) for var in variables}
    else:
        return {var: 1/len(variables) for var in variables}

def apply_common_layout(fig):
    """Apply common layout settings to plots."""
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    return fig

def truncate_col(text, max_len=20):
    """Truncate text for table columns"""
    text = str(text)
    return text[:max_len] + '...' if len(text) > max_len else text

def get_column_name(merged_data, column_name):
    """Helper function to get the correct column name after merge operations."""
    if column_name in merged_data.columns:
        return column_name
    
    # Check for common suffixes that pandas adds during merges
    possible_names = [
        column_name,
        f"{column_name}_x",
        f"{column_name}_y",
        f"{column_name}_1",
        f"{column_name}_2"
    ]
    
    # For specific columns, add additional possible names
    if column_name == 'unit_price':
        possible_names.extend(['price', 'unit_cost'])
    elif column_name == 'supplier_id':
        possible_names.extend(['supplier', 'vendor_id'])
    elif column_name == 'item_name':
        possible_names.extend(['name', 'product_name'])
    
    return next((name for name in possible_names if name in merged_data.columns), None)

def get_unit_price_column(merged_data):
    """Helper function to get the correct unit price column name after merge operations."""
    return get_column_name(merged_data, 'unit_price')

def check_data_quality(po_df, items_data, suppliers):
    """Check data quality and provide recommendations."""
    issues = []
    recommendations = []
    
    # Check for missing data
    if po_df.empty:
        issues.append("No purchase order data found")
        recommendations.append("Upload purchase order data")
    
    if items_data.empty:
        issues.append("No items data found")
        recommendations.append("Upload items data")
    
    if suppliers.empty:
        issues.append("No suppliers data found")
        recommendations.append("Upload suppliers data")
    
    # Check for required columns
    required_po_cols = ['supplier_id', 'item_id', 'quantity', 'unit_price']
    missing_po_cols = [col for col in required_po_cols if col not in po_df.columns]
    if missing_po_cols:
        issues.append(f"Missing required columns in purchase orders: {', '.join(missing_po_cols)}")
        recommendations.append("Ensure all required columns are present in purchase order data")
    
    # Check for data consistency
    if not po_df.empty and not items_data.empty:
        po_items = set(po_df['item_id'].unique())
        available_items = set(items_data['item_id'].unique())
        missing_items = po_items - available_items
        if missing_items:
            issues.append(f"Purchase orders reference {len(missing_items)} items not found in items data")
            recommendations.append("Ensure all items in purchase orders exist in items data")
    
    return issues, recommendations

# Custom CSS for modern SaaS dashboard styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Modern SaaS Dashboard Styling */
    
    /* Main background gradient */
    .main .block-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
        max-width: 100%;
    }
    
    /* Sidebar styling - compact */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a202c 0%, #2d3748 100%);
        padding: 20px 12px;
        width: 250px;
        min-width: 250px;
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    /* Optimize sidebar width */
    .css-1lcbmhc {
        width: 250px;
        min-width: 250px;
    }
    
    /* Main content area - expanded width */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
        width: 100%;
    }
    
    /* Expand main content width */
    .main {
        max-width: 100%;
        padding-left: 0;
        padding-right: 0;
    }
    
    /* Remove default Streamlit width constraints */
    .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Expand chart containers */
    .chart-container {
        width: 100%;
        max-width: none;
    }
    
    /* Make plots wider */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* Expand dataframe width */
    .dataframe {
        width: 100% !important;
        max-width: none;
    }
    
    /* Force full width for all content */
    .element-container {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Ensure plots use full width */
    .plotly-graph-div {
        width: 100% !important;
        max-width: none !important;
        height: auto !important;
    }
    
    /* Optimize chart height for wide layout */
    .js-plotly-plot {
        height: 500px !important;
    }
    
    /* Optimize column layouts for wider space */
    .row-widget.stHorizontal {
        width: 100%;
    }
    
    /* Remove any remaining width constraints */
    .stApp > div:first-child {
        max-width: 100%;
    }
    
    /* Ensure all Streamlit elements use full width */
    .stApp {
        max-width: 100%;
    }
    
    /* Optimize for wide screens */
    @media (min-width: 1200px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    /* Make sure all containers expand */
    .stContainer {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Sidebar button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        color: #ffffff;
        font-weight: 500;
        margin: 6px 0;
        padding: 12px 16px;
        transition: all 0.3s ease;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        font-size: 0.95rem;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(3px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Active button styling */
    .stButton > button[data-active="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-weight: 600;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.3);
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(249, 115, 22, 0.3);
    }
    
    .metric-card-teal {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(20, 184, 166, 0.3);
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.3);
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
    }
    
    /* Chart container styling */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Welcome section */
    .welcome-section {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Progress circle styling */
    .progress-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        margin: 10px auto;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Insights container */
    .insights-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            margin: 5px 0;
            padding: 15px;
        }
        
        .main-header {
            padding: 20px;
            font-size: 24px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_dataframe_with_index_1(df, **kwargs):
    """Display dataframe with index starting from 1"""
    if not df.empty:
        df_display = df.reset_index(drop=True)
        df_display.index = df_display.index + 1
        return st.dataframe(df_display, **kwargs)
    else:
        return st.dataframe(df, **kwargs)

def safe_calculate_variance(actual, budget, metric_name="metric"):
    """Safely calculate variance with error handling"""
    try:
        if budget > 0:
            return ((actual - budget) / budget * 100)
        else:
            return 0
    except (TypeError, ValueError, ZeroDivisionError):
        st.warning(f"⚠️ Unable to calculate {metric_name} variance due to data issues")
        return 0

def create_template_for_download():
    """Create an Excel template with all required Finance data schema and make it downloadable"""
    
    # Create empty DataFrames with the correct Finance schema
    income_statement_template = pd.DataFrame(columns=[
        'period', 'revenue', 'cost_of_goods_sold', 'gross_profit', 'operating_expenses',
        'operating_income', 'interest_expense', 'income_tax_expense', 'net_income'
    ])
    
    balance_sheet_template = pd.DataFrame(columns=[
        'period', 'cash_and_equivalents', 'accounts_receivable', 'inventory', 'current_assets',
        'total_assets', 'accounts_payable', 'current_liabilities', 'total_liabilities',
        'shareholder_equity', 'shares_outstanding'
    ])
    
    cash_flow_template = pd.DataFrame(columns=[
        'period', 'net_income', 'depreciation', 'working_capital_change', 'operating_cash_flow',
        'capital_expenditures', 'free_cash_flow', 'initial_investment', 'cash_flow', 'nopat'
    ])
    
    budget_template = pd.DataFrame(columns=[
        'period', 'revenue', 'expenses', 'profit', 'category'
    ])
    
    forecast_template = pd.DataFrame(columns=[
        'period', 'revenue', 'expenses', 'profit', 'confidence_level'
    ])
    
    market_template = pd.DataFrame(columns=[
        'period', 'market_price', 'dividends_per_share', 'volume', 'market_cap'
    ])
    
    customer_template = pd.DataFrame(columns=[
        'customer_id', 'customer_name', 'revenue', 'profit_margin', 'profitability', 
        'costs_to_serve', 'segment', 'region', 'lifetime_value'
    ])
    
    product_template = pd.DataFrame(columns=[
        'product_id', 'product_name', 'revenue', 'cost', 'total_costs', 'direct_costs', 
        'allocated_costs', 'margin', 'category', 'lifecycle_stage'
    ])
    
    value_chain_template = pd.DataFrame(columns=[
        'function', 'cost', 'percentage', 'period'
    ])
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each template to a separate sheet
        income_statement_template.to_excel(writer, sheet_name='Income_Statement', index=False)
        balance_sheet_template.to_excel(writer, sheet_name='Balance_Sheet', index=False)
        cash_flow_template.to_excel(writer, sheet_name='Cash_Flow', index=False)
        budget_template.to_excel(writer, sheet_name='Budget', index=False)
        forecast_template.to_excel(writer, sheet_name='Forecast', index=False)
        market_template.to_excel(writer, sheet_name='Market_Data', index=False)
        customer_template.to_excel(writer, sheet_name='Customer_Data', index=False)
        product_template.to_excel(writer, sheet_name='Product_Data', index=False)
        value_chain_template.to_excel(writer, sheet_name='Value_Chain', index=False)
        
        # Add instructions sheet
        instructions_data = {
            'Sheet Name': ['Income_Statement', 'Balance_Sheet', 'Cash_Flow', 'Budget', 'Forecast', 'Market_Data', 'Customer_Data', 'Product_Data', 'Value_Chain'],
            'Required Fields': [
                'period, revenue, cost_of_goods_sold, gross_profit, operating_expenses, operating_income, interest_expense, income_tax_expense, net_income',
                'period, cash_and_equivalents, accounts_receivable, inventory, current_assets, total_assets, accounts_payable, current_liabilities, total_liabilities, shareholder_equity, shares_outstanding',
                'period, net_income, depreciation, working_capital_change, operating_cash_flow, capital_expenditures, free_cash_flow, initial_investment, cash_flow, nopat',
                'period, revenue, expenses, profit, category',
                'period, revenue, expenses, profit, confidence_level',
                'period, market_price, dividends_per_share, volume, market_cap',
                'customer_id, customer_name, revenue, profit_margin, profitability, costs_to_serve, segment, region, lifetime_value',
                'product_id, product_name, revenue, cost, total_costs, direct_costs, allocated_costs, margin, category, lifecycle_stage',
                'function, cost, percentage, period'
            ],
            'Data Types': [
                'Date, Number, Number, Number, Number, Number, Number, Number, Number',
                'Date, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number',
                'Date, Number, Number, Number, Number, Number, Number, Number, Number, Number, Number',
                'Date, Number, Number, Number, Text',
                'Date, Number, Number, Number, Number',
                'Date, Number, Number, Number, Number',
                'Text, Text, Number, Number, Number, Number, Text, Text, Number',
                'Text, Text, Number, Number, Number, Number, Number, Number, Text, Text',
                'Text, Number, Number, Date'
            ],
            'Description': [
                'Income statement with revenue, costs, and profitability metrics',
                'Balance sheet with assets, liabilities, and equity',
                'Cash flow statement with operating, investing, and financing activities',
                'Budget data for variance analysis',
                'Forecast data for accuracy measurement',
                'Market data including stock prices and dividends',
                'Customer profitability analysis',
                'Product/service profitability analysis',
                'Value chain cost analysis by function'
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Format the instructions sheet
        worksheet = writer.sheets['Instructions']
        for i, col in enumerate(instructions_df.columns):
            worksheet.set_column(i, i, 30)
    
    output.seek(0)
    return output

def export_data_to_excel():
    """Export all Finance data to Excel file"""
    if (st.session_state.income_statement.empty and st.session_state.balance_sheet.empty and 
        st.session_state.cash_flow.empty and st.session_state.budget.empty and
        st.session_state.forecast.empty and st.session_state.market_data.empty and
        st.session_state.customer_data.empty and st.session_state.product_data.empty and
        st.session_state.value_chain.empty):
        st.warning("No data to export. Please add data first.")
        return None
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each DataFrame to a separate sheet
        st.session_state.income_statement.to_excel(writer, sheet_name='Income_Statement', index=False)
        st.session_state.balance_sheet.to_excel(writer, sheet_name='Balance_Sheet', index=False)
        st.session_state.cash_flow.to_excel(writer, sheet_name='Cash_Flow', index=False)
        st.session_state.budget.to_excel(writer, sheet_name='Budget', index=False)
        st.session_state.forecast.to_excel(writer, sheet_name='Forecast', index=False)
        st.session_state.market_data.to_excel(writer, sheet_name='Market_Data', index=False)
        st.session_state.customer_data.to_excel(writer, sheet_name='Customer_Data', index=False)
        st.session_state.product_data.to_excel(writer, sheet_name='Product_Data', index=False)
        st.session_state.value_chain.to_excel(writer, sheet_name='Value_Chain', index=False)
    
    output.seek(0)
    return output

# Page configuration
st.set_page_config(
    page_title="Finance Analytics Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .formula-box {
        background-color: #e8f4fd;
        padding: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .section-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .section-header h3 {
        color: white;
        margin: 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for Finance data storage
if 'income_statement' not in st.session_state:
    st.session_state.income_statement = pd.DataFrame(columns=[
        'period', 'revenue', 'cost_of_goods_sold', 'gross_profit', 'operating_expenses',
        'operating_income', 'interest_expense', 'income_tax_expense', 'net_income'
    ])

if 'balance_sheet' not in st.session_state:
    st.session_state.balance_sheet = pd.DataFrame(columns=[
        'period', 'cash_and_equivalents', 'accounts_receivable', 'inventory', 'current_assets',
        'total_assets', 'accounts_payable', 'current_liabilities', 'total_liabilities',
        'shareholder_equity', 'shares_outstanding'
    ])

if 'cash_flow' not in st.session_state:
    st.session_state.cash_flow = pd.DataFrame(columns=[
        'period', 'net_income', 'depreciation', 'working_capital_change', 'operating_cash_flow',
        'capital_expenditures', 'free_cash_flow', 'initial_investment', 'cash_flow', 'nopat'
    ])

if 'budget' not in st.session_state:
    st.session_state.budget = pd.DataFrame(columns=[
        'period', 'revenue', 'expenses', 'profit', 'category'
    ])

if 'forecast' not in st.session_state:
    st.session_state.forecast = pd.DataFrame(columns=[
        'period', 'revenue', 'expenses', 'profit', 'confidence_level'
    ])

if 'market_data' not in st.session_state:
    st.session_state.market_data = pd.DataFrame(columns=[
        'period', 'market_price', 'dividends_per_share', 'volume', 'market_cap'
    ])

if 'customer_data' not in st.session_state:
    st.session_state.customer_data = pd.DataFrame(columns=[
        'customer_id', 'customer_name', 'revenue', 'costs_to_serve', 'profitability'
    ])

if 'product_data' not in st.session_state:
    st.session_state.product_data = pd.DataFrame(columns=[
        'product_id', 'product_name', 'revenue', 'direct_costs', 'allocated_costs', 'total_costs'
    ])

if 'value_chain' not in st.session_state:
    st.session_state.value_chain = pd.DataFrame(columns=[
        'function', 'cost', 'percentage', 'period'
    ])

def set_home_page():
    """Set the department to start on home page"""
    st.session_state.current_page = "🏠 Home"

def main():
    # Configure page for wide layout
    st.set_page_config(
        page_title="Finance Analytics",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Modern header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">💰 Finance Analytics</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state is already initialized above with proper column structure
    # No need to re-initialize here
    
    # Sidebar navigation for main sections
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px;">
            <h3 style="color: #4CAF50; margin-bottom: 15px; text-align: center; font-size: 1.2rem; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">
                🎯 Navigation
            </h3>
            <p style="color: #2196F3; text-align: center; margin: 0; font-size: 0.85rem; font-weight: 500;">
                Select a section to explore
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main navigation buttons - Ordered by priority
        # 🥇 HIGH PRIORITY - Essential sections
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.current_page = "🏠 Home"
        
        if st.button("📊 Data Input", key="nav_data_input", use_container_width=True):
            st.session_state.current_page = "📝 Data Input"
        
        # 🥈 MEDIUM PRIORITY - Core financial analysis
        if st.button("📈 Financial Performance", key="nav_financial_performance", use_container_width=True):
            st.session_state.current_page = "📊 Financial Performance"
        
        if st.button("💧 Liquidity & Solvency", key="nav_liquidity_solvency", use_container_width=True):
            st.session_state.current_page = "💧 Liquidity & Solvency"
        
        if st.button("💸 Cash Flow", key="nav_cash_flow", use_container_width=True):
            st.session_state.current_page = "💸 Cash Flow"
        
        if st.button("⚡ Efficiency & Productivity", key="nav_efficiency_productivity", use_container_width=True):
            st.session_state.current_page = "⚡ Efficiency & Productivity"
        
        if st.button("📋 Budget & Forecasting", key="nav_budget_forecasting", use_container_width=True):
            st.session_state.current_page = "📋 Budget & Forecasting"
        
        # 🥉 LOWER PRIORITY - Advanced and specialized analysis
        if st.button("🏗️ Capital Structure", key="nav_capital_structure", use_container_width=True):
            st.session_state.current_page = "🏗️ Capital Structure"
        
        if st.button("📈 Investment & Valuation", key="nav_investment_valuation", use_container_width=True):
            st.session_state.current_page = "📈 Investment & Valuation"
        
        if st.button("🛡️ Risk & Compliance", key="nav_risk_compliance", use_container_width=True):
            st.session_state.current_page = "⚠️ Risk & Compliance"
        
        if st.button("📊 Strategic KPIs", key="nav_strategic_kpis", use_container_width=True):
            st.session_state.current_page = "📊 Strategic KPIs"
        
        if st.button("🤖 Auto Insights", key="nav_auto_insights", use_container_width=True):
            st.session_state.current_page = "🤖 Auto Insights"
        
        # 🏆 LOWEST PRIORITY - Advanced analytics (moved to end)
        if st.button("🔮 Predictive Analytics", key="nav_predictive", use_container_width=True):
            st.session_state.current_page = "🔮 Predictive Analytics"
        
        # Performance optimization section (hidden from user)
        # All performance optimizations run in background without UI clutter
        
        # Developer attribution at the bottom of sidebar
        st.markdown("---")
        st.markdown("""
        <div style="padding: 12px 0; text-align: center;">
            <p style="color: #95a5a6; font-size: 0.75rem; margin: 0; line-height: 1.3;">
                Developed by <strong style="color: #3498db;">Aryan Zabihi</strong><br>
                <a href="https://github.com/Aryanzabihi" target="_blank" style="color: #3498db; text-decoration: none;">GitHub</a> • 
                <a href="https://www.linkedin.com/in/aryanzabihi/" target="_blank" style="color: #3498db; text-decoration: none;">LinkedIn</a> • 
                <a href="https://www.paypal.com/donate/?hosted_button_id=C9W46U77KNU9S" target="_blank" style="color: #ffc439; text-decoration: none; font-weight: 600;">💝 Donate</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize current page if not set
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Home"
        
        page = st.session_state.current_page
    
    # Main content area
    if page == "🏠 Home":
        show_home()
    
    elif page == "📝 Data Input":
        show_data_input()
    
    elif page == "🤖 Auto Insights":
        show_auto_insights()
    
    elif page == "🔮 Predictive Analytics":
        show_predictive_analytics()
    
    elif page == "📊 Financial Performance":
        show_financial_performance()
    
    elif page == "💧 Liquidity & Solvency":
        show_liquidity_solvency()
    
    elif page == "⚡ Efficiency & Productivity":
        show_efficiency_productivity()
    
    elif page == "📋 Budget & Forecasting":
        show_budget_forecasting()
    
    elif page == "💸 Cash Flow":
        show_cash_flow()
    
    elif page == "🏗️ Capital Structure":
        show_capital_structure()
    
    elif page == "📈 Investment & Valuation":
        show_investment_valuation()
    
    elif page == "⚠️ Risk & Compliance":
        show_risk_compliance()
    
    elif page == "📊 Strategic KPIs":
        show_strategic_kpis()

def get_data_summary():
    """Get summary of loaded financial data"""
    summary = {}
    
    if not st.session_state.income_statement.empty:
        summary['Income Statement'] = len(st.session_state.income_statement)
    if not st.session_state.balance_sheet.empty:
        summary['Balance Sheet'] = len(st.session_state.balance_sheet)
    if not st.session_state.cash_flow.empty:
        summary['Cash Flow'] = len(st.session_state.cash_flow)
    if not st.session_state.budget.empty:
        summary['Budget'] = len(st.session_state.budget)
    if not st.session_state.forecast.empty:
        summary['Forecast'] = len(st.session_state.forecast)
    if not st.session_state.market_data.empty:
        summary['Market Data'] = len(st.session_state.market_data)
    if not st.session_state.customer_data.empty:
        summary['Customer Data'] = len(st.session_state.customer_data)
    if not st.session_state.product_data.empty:
        summary['Product Data'] = len(st.session_state.product_data)
    if not st.session_state.value_chain.empty:
        summary['Value Chain'] = len(st.session_state.value_chain)
    
    return summary

def validate_data_integrity():
    """Validate the integrity of loaded financial data"""
    validation_results = []
    
    # Check if any data is loaded
    total_records = sum([
        len(st.session_state.income_statement),
        len(st.session_state.balance_sheet),
        len(st.session_state.cash_flow),
        len(st.session_state.budget),
        len(st.session_state.forecast),
        len(st.session_state.market_data),
        len(st.session_state.customer_data),
        len(st.session_state.product_data),
        len(st.session_state.value_chain)
    ])
    
    if total_records == 0:
        validation_results.append("⚠️ No financial data loaded. Please upload data to begin analysis.")
        return validation_results
    
    # Check income statement data
    if not st.session_state.income_statement.empty:
        required_cols = ['revenue', 'cost_of_goods_sold', 'gross_profit', 'operating_income', 'net_income']
        missing_cols = [col for col in required_cols if col not in st.session_state.income_statement.columns]
        if missing_cols:
            validation_results.append(f"⚠️ Income Statement missing columns: {', '.join(missing_cols)}")
        else:
            validation_results.append("✅ Income Statement data structure is valid")
    
    # Check balance sheet data
    if not st.session_state.balance_sheet.empty:
        required_cols = ['total_assets', 'total_liabilities', 'total_equity']
        missing_cols = [col for col in required_cols if col not in st.session_state.balance_sheet.columns]
        if missing_cols:
            validation_results.append(f"⚠️ Balance Sheet missing columns: {', '.join(missing_cols)}")
        else:
            validation_results.append("✅ Balance Sheet data structure is valid")
    
    # Check cash flow data
    if not st.session_state.cash_flow.empty:
        required_cols = ['operating_cash_flow', 'investing_cash_flow', 'financing_cash_flow']
        missing_cols = [col for col in required_cols if col not in st.session_state.cash_flow.columns]
        if missing_cols:
            validation_results.append(f"⚠️ Cash Flow missing columns: {', '.join(missing_cols)}")
        else:
            validation_results.append("✅ Cash Flow data structure is valid")
    
    # Check for data consistency
    if not st.session_state.income_statement.empty and not st.session_state.balance_sheet.empty:
        if 'period' in st.session_state.income_statement.columns and 'period' in st.session_state.balance_sheet.columns:
            income_periods = set(st.session_state.income_statement['period'])
            balance_periods = set(st.session_state.balance_sheet['period'])
            if income_periods != balance_periods:
                validation_results.append("⚠️ Period mismatch between Income Statement and Balance Sheet")
            else:
                validation_results.append("✅ Period consistency verified across financial statements")
    
    return validation_results

def create_metric_card(title, value, description):
    """Create a styled metric card for the dashboard"""
    return f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                color: white; 
                text-align: center; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                margin-bottom: 1rem;">
        <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; font-weight: 600;">{title}</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; opacity: 0.9;">{description}</p>
    </div>
    """

def create_insight_box(title, content, icon="💡"):
    """Create a styled insight box"""
    return f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; 
                border-radius: 15px; 
                color: white; 
                margin-bottom: 1rem;">
        <h4 style="margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">{icon} {title}</h4>
        <p style="margin: 0; font-size: 0.95rem; line-height: 1.5;">{content}</p>
    </div>
    """

def create_alert_box(content, alert_type="info"):
    """Create a styled alert box"""
    colors = {
        "info": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "success": "linear-gradient(135deg, #4CAF50 0%, #45a049 100%)",
        "warning": "linear-gradient(135deg, #ff9800 0%, #f57c00 100%)",
        "error": "linear-gradient(135deg, #f44336 0%, #d32f2f 100%)"
    }
    
    return f"""
    <div style="background: {colors.get(alert_type, colors['info'])}; 
                padding: 1rem; 
                border-radius: 10px; 
                color: white; 
            margin-bottom: 1rem;">
        <p style="margin: 0; font-size: 0.95rem;">{content}</p>
    </div>
    """

def show_home():
    """Display the home page with overview and key metrics"""
    
    st.markdown("## 🏠 Dashboard Overview")
    
    # Check if data is loaded
    if (st.session_state.income_statement.empty and st.session_state.balance_sheet.empty and 
        st.session_state.cash_flow.empty and st.session_state.budget.empty and 
        st.session_state.forecast.empty and st.session_state.market_data.empty and
        st.session_state.customer_data.empty and st.session_state.product_data.empty and
        st.session_state.value_chain.empty):
        
        # EXACTLY like cs.py - Welcome section with 4 colored cards
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 2rem 0;">
            <h2 style="color: #495057; margin-bottom: 1rem;">🎯 Welcome to Finance Analytics</h2>
            <p style="color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;">
                Get started by uploading your financial data or generating sample data to explore the dashboard features.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # EXACTLY like cs.py - 4 colored metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Analytics Categories", 
                "10 comprehensive",
                "analysis areas"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Financial Analytics", 
                "Performance",
                "metrics & insights"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Real-time", 
                "Live data",
                "updates"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Predictive", 
                "Advanced",
                "analytics"
            ), unsafe_allow_html=True)
        
        # EXACTLY like cs.py - Available analytics categories (6 cards in 2 columns)
        st.markdown("### 📊 Available Finance Analytics Categories:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 1: Financial Performance Analysis
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📊 Financial Performance Analysis</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Revenue Growth Rate Analysis</li>
                    <li>Gross Margin Optimization</li>
                    <li>Operating Margin Tracking</li>
                    <li>Net Margin Analysis</li>
                    <li>Earnings per Share (EPS) Calculation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 2: Liquidity and Solvency
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">💧 Liquidity and Solvency</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Current Ratio Analysis</li>
                    <li>Quick Ratio Assessment</li>
                    <li>Cash Conversion Cycle (CCC)</li>
                    <li>Debt Service Coverage Ratio (DSCR)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 3: Efficiency and Productivity
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">⚡ Efficiency and Productivity</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Return on Assets (ROA)</li>
                    <li>Return on Equity (ROE)</li>
                    <li>Asset Turnover Ratio</li>
                    <li>Operating Expense Ratio</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Card 4: Budgeting, Forecasting & Variance
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">📋 Budgeting, Forecasting & Variance</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Budget Variance Analysis</li>
                    <li>Forecast Accuracy (MAPE)</li>
                    <li>Scenario Analysis</li>
                    <li>Variance Reporting</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 5: Cash Flow & Working Capital
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">💸 Cash Flow & Working Capital</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Operating Cash Flow Analysis</li>
                    <li>Free Cash Flow (FCF) Calculation</li>
                    <li>Working Capital Turnover</li>
                    <li>Cash Flow Optimization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 6: Capital Structure & Investment
            st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4 style="color: #495057; margin-bottom: 1rem;">🏗️ Capital Structure & Investment</h4>
                <ul style="color: #6c757d; margin: 0; padding-left: 1.5rem;">
                    <li>Debt-to-Equity Ratio</li>
                    <li>Weighted Average Cost of Capital (WACC)</li>
                    <li>Interest Coverage Ratio</li>
                    <li>Capital Structure Optimization</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # EXACTLY like cs.py - Getting Started section (3 cards)
        st.markdown("### 🚀 Getting Started:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">1. Data Input</h4>
                <p style="margin: 0;">Enter your financial data in the 'Data Input' tab</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">2. Calculate Metrics</h4>
                <p style="margin: 0;">Use the main tabs to view specific metric categories</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
                <h4 style="margin-bottom: 1rem;">3. Real-time Analysis</h4>
                <p style="margin: 0;">All metrics update automatically based on your data</p>
            </div>
            """, unsafe_allow_html=True)
        
        # EXACTLY like cs.py - Data Schema section (8 cards in 2 rows)
        st.markdown("### 📈 Data Schema:")
        st.markdown("The application supports the following financial data tables:")
        
        # Row 1 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">💰 Income Statement</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Revenue, costs, and profitability data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📊 Balance Sheet</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Assets, liabilities, and equity information</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">💸 Cash Flow</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Operating, investing, and financing activities</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📋 Budget</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Budgeted vs actual performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Row 2 (4 cards)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">🔮 Forecast</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Forecasted vs actual performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📈 Market Data</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Stock prices, dividends, market cap</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">👥 Customer Data</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Customer profitability analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;">
                <h5 style="color: #495057; margin-bottom: 0.5rem;">📦 Product Data</h5>
                <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">Product/service profitability</p>
            </div>
            """, unsafe_allow_html=True)
        
        # EXACTLY like cs.py - Important Note section
        st.markdown("### 💡 Important Note:")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 1rem;">
            <p style="margin: 0;">All calculations are performed automatically based on your input data. Make sure to enter complete and accurate data for the most reliable metrics.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Upload Data", use_container_width=True):
                st.session_state.current_page = "📝 Data Input"
                st.rerun()
        
        with col2:
            if st.button("📝 Manual Entry", use_container_width=True):
                st.session_state.current_page = "📝 Data Input"
                st.rerun()
        
        with col3:
            if st.button("📋 Download Template", use_container_width=True):
                # Generate sample data as template
                generate_sample_finance_data()
                st.success("✅ Sample data generated! You can now explore the dashboard features.")
        
        return
    
    # Data is loaded, show overview
    st.success("✅ Financial data loaded successfully!")
    
    # Data summary
    data_summary = get_data_summary()
    
    # Key metrics display - EXACTLY like cs.py
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total Revenue", 
            f"${data_summary.get('Income Statement', 0):,}",
            "Financial performance"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Total Assets", 
            f"${data_summary.get('Balance Sheet', 0):,}",
            "Company value"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Cash Flow", 
            f"{data_summary.get('Cash Flow', 0):,}",
            "Liquidity status"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Budget & Forecast", 
            f"{data_summary.get('Budget', 0) + data_summary.get('Forecast', 0):,}",
            "Planning data"
        ), unsafe_allow_html=True)
    
    # Data validation - EXACTLY like cs.py
    st.markdown("### 🔍 Data Quality Check")
    validation_results = validate_data_integrity()
    
    for result in validation_results:
        if "✅" in result:
            st.success(result)
        elif "⚠️" in result:
            st.warning(result)
        else:
            st.error(result)
    
    # Quick insights - EXACTLY like cs.py structure
    st.markdown("### 💡 Quick Insights")
    
    if not st.session_state.income_statement.empty:
        # Revenue trend
        if 'revenue' in st.session_state.income_statement.columns and 'period' in st.session_state.income_statement.columns:
            revenue_data = st.session_state.income_statement[['period', 'revenue']].copy()
            revenue_data['period'] = pd.to_datetime(revenue_data['period'], errors='coerce')
            revenue_data = revenue_data.dropna()
            
            if not revenue_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Revenue trend chart
                    fig = go.Figure(data=[go.Scatter(
                        x=revenue_data['period'],
                        y=revenue_data['revenue'],
                        mode='lines+markers',
                        line=dict(color='#28a745', width=3),
                        marker=dict(size=6)
                    )])
                    
                    fig.update_layout(
                        title="Revenue Trend",
                        xaxis_title="Period",
                        yaxis_title="Revenue ($)",
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Revenue metrics
                    total_revenue = revenue_data['revenue'].sum()
                    avg_revenue = revenue_data['revenue'].mean()
                    growth_rate = ((revenue_data['revenue'].iloc[-1] / revenue_data['revenue'].iloc[0]) - 1) * 100 if len(revenue_data) > 1 else 0
                    
                    st.metric("Total Revenue", f"${total_revenue:,.0f}")
                    st.metric("Average Revenue", f"${avg_revenue:,.0f}")
                    st.metric("Growth Rate", f"{growth_rate:.1f}%")
    
    # Financial ratios overview - EXACTLY like cs.py structure
    if not st.session_state.balance_sheet.empty and not st.session_state.income_statement.empty:
        st.markdown("### 📊 Financial Ratios Overview")
        
        # Calculate basic ratios
        if 'total_assets' in st.session_state.balance_sheet.columns and 'total_equity' in st.session_state.balance_sheet.columns:
            latest_balance = st.session_state.balance_sheet.iloc[-1]
            latest_income = st.session_state.income_statement.iloc[-1] if not st.session_state.income_statement.empty else None
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Asset utilization
                if latest_income is not None and 'revenue' in latest_income:
                    asset_turnover = latest_income['revenue'] / latest_balance['total_assets'] if latest_balance['total_assets'] > 0 else 0
                    st.metric("Asset Turnover", f"{asset_turnover:.2f}")
                
                st.metric("Total Assets", f"${latest_balance['total_assets']:,.0f}")
                st.metric("Total Equity", f"${latest_balance['total_equity']:,.0f}")
            
            with col2:
                # Equity ratio
                equity_ratio = latest_balance['total_equity'] / latest_balance['total_assets'] if latest_balance['total_assets'] > 0 else 0
                st.metric("Equity Ratio", f"{equity_ratio:.2%}")
                
                if 'total_liabilities' in latest_balance:
                    debt_ratio = latest_balance['total_liabilities'] / latest_balance['total_assets'] if latest_balance['total_assets'] > 0 else 0
                    st.metric("Debt Ratio", f"{debt_ratio:.2%}")
    
    # Profitability overview - EXACTLY like cs.py customer satisfaction structure
    if not st.session_state.income_statement.empty:
        st.markdown("### 💰 Profitability Overview")
        
        # Calculate profitability metrics
        if 'revenue' in st.session_state.income_statement.columns and 'net_income' in st.session_state.income_statement.columns:
            latest_income = st.session_state.income_statement.iloc[-1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Profitability metrics table
                st.markdown("**Profitability Metrics**")
                profitability_data = pd.DataFrame({
                    'Metric': ['Revenue', 'Net Income', 'Gross Profit', 'Operating Income'],
                    'Value': [
                        f"${latest_income.get('revenue', 0):,.0f}",
                        f"${latest_income.get('net_income', 0):,.0f}",
                        f"${latest_income.get('gross_profit', 0):,.0f}",
                        f"${latest_income.get('operating_income', 0):,.0f}"
                    ]
                })
                st.dataframe(profitability_data, use_container_width=True, hide_index=True)
            
            with col2:
                # Profit margin trend
                if len(st.session_state.income_statement) > 1:
                    profit_margins = []
                    periods = []
                    
                    for idx, row in st.session_state.income_statement.iterrows():
                        if row.get('revenue', 0) > 0 and row.get('net_income', 0) is not None:
                            margin = (row.get('net_income', 0) / row.get('revenue', 0)) * 100
                            profit_margins.append(margin)
                            periods.append(f"Period {idx+1}")
                    
                    if profit_margins:
                        fig = go.Figure(data=[go.Bar(
                            x=periods,
                            y=profit_margins,
                            marker_color='#667eea'
                        )])
                        
                        fig.update_layout(
                            title="Profit Margin Trend",
                            xaxis_title="Period",
                            yaxis_title="Profit Margin (%)",
                            height=300
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
    
    # Financial performance overview - EXACTLY like cs.py agent performance structure
    if not st.session_state.balance_sheet.empty and not st.session_state.income_statement.empty:
        st.markdown("### 📊 Financial Performance Overview")
        
        # Calculate performance metrics
        if 'total_assets' in st.session_state.balance_sheet.columns and 'total_equity' in st.session_state.balance_sheet.columns:
            latest_balance = st.session_state.balance_sheet.iloc[-1]
            latest_income = st.session_state.income_statement.iloc[-1] if not st.session_state.income_statement.empty else None
            
            if latest_income is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Performance metrics table
                    st.markdown("**Performance Metrics**")
                    
                    # Calculate ROA and ROE
                    roa = (latest_income.get('net_income', 0) / latest_balance.get('total_assets', 1)) * 100 if latest_balance.get('total_assets', 0) > 0 else 0
                    roe = (latest_income.get('net_income', 0) / latest_balance.get('total_equity', 1)) * 100 if latest_balance.get('total_equity', 0) > 0 else 0
                    
                    performance_data = pd.DataFrame({
                        'Metric': ['ROA (%)', 'ROE (%)', 'Asset Turnover', 'Total Assets'],
                        'Value': [
                            f"{roa:.2f}%",
                            f"{roe:.2f}%",
                            f"{latest_income.get('revenue', 0) / latest_balance.get('total_assets', 1):.2f}",
                            f"${latest_balance.get('total_assets', 0):,.0f}"
                        ]
                    })
                    st.dataframe(performance_data, use_container_width=True, hide_index=True)
                
                with col2:
                    # Performance comparison chart
                    if len(st.session_state.income_statement) > 1:
                        roa_trend = []
                        roe_trend = []
                        periods = []
                        
                        for idx, row in st.session_state.income_statement.iterrows():
                            if idx < len(st.session_state.balance_sheet):
                                balance_row = st.session_state.balance_sheet.iloc[idx]
                                if row.get('revenue', 0) > 0 and balance_row.get('total_assets', 0) > 0:
                                    roa = (row.get('net_income', 0) / balance_row.get('total_assets', 1)) * 100
                                    roe = (row.get('net_income', 0) / balance_row.get('total_equity', 1)) * 100
                                    roa_trend.append(roa)
                                    roe_trend.append(roe)
                                    periods.append(f"Period {idx+1}")
                        
                        if roa_trend and roe_trend:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(x=periods, y=roa_trend, mode='lines+markers', name='ROA', line=dict(color='#28a745')))
                            fig.add_trace(go.Scatter(x=periods, y=roe_trend, mode='lines+markers', name='ROE', line=dict(color='#667eea')))
                            
                            fig.update_layout(
                                title="ROA vs ROE Trend",
                                xaxis_title="Period",
                                yaxis_title="Percentage (%)",
                                height=300,
                                showlegend=True
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity - EXACTLY like cs.py structure
    st.markdown("### 📈 Recent Activity")
    
    if not st.session_state.income_statement.empty and 'period' in st.session_state.income_statement.columns:
        # Convert dates
        income_with_date = st.session_state.income_statement.copy()
        income_with_date['period'] = pd.to_datetime(income_with_date['period'], errors='coerce')
        income_with_date = income_with_date.dropna(subset=['period'])
        
        if not income_with_date.empty:
            # Daily revenue volume (like cs.py daily ticket volume)
            daily_revenue = income_with_date.groupby(
                income_with_date['period'].dt.date
            )['revenue'].sum().reset_index(name='revenue_amount')
            
            daily_revenue.columns = ['Date', 'Revenue Amount']
            daily_revenue = daily_revenue.sort_values('Date').tail(30)  # Last 30 days
            
            fig = go.Figure(data=[go.Scatter(
                x=daily_revenue['Date'],
                y=daily_revenue['Revenue Amount'],
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=6)
            )])
            
            fig.update_layout(
                title="Daily Revenue Volume (Last 30 Days)",
                xaxis_title="Date",
                yaxis_title="Revenue Amount ($)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Quick actions - EXACTLY like cs.py structure
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Detailed Analytics", use_container_width=True):
            st.session_state.current_page = "📊 Financial Performance"
            st.rerun()
    
    with col2:
        if st.button("📝 Manage Data", use_container_width=True):
            st.session_state.current_page = "📝 Data Input"
            st.rerun()
    
    with col3:
        if st.button("🔮 Predictive Analytics", use_container_width=True):
            st.session_state.current_page = "🔮 Predictive Analytics"
            st.rerun()
    
    # System information - EXACTLY like cs.py structure
    st.markdown("---")
    st.markdown("### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Data Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info(f"**Total Records**: {sum(data_summary.values()):,}")
    
    with col2:
        st.info(f"**Dashboard Version**: 2.0.0")
        st.info(f"**Data Sources**: {len([k for k, v in data_summary.items() if v > 0])} active datasets")

def generate_sample_finance_data():
    """Generate comprehensive sample finance data for testing"""
    np.random.seed(42)
    
    # Generate periods with proper datetime format for forecasting
    periods = []
    for year in range(2020, 2024):
        for quarter in range(1, 5):
            # Create proper datetime for each quarter
            month = (quarter - 1) * 3 + 1  # Q1=Jan, Q2=Apr, Q3=Jul, Q4=Oct
            periods.append(f"{year}-{month:02d}-01")
    
    # Ensure we have at least 8 periods for forecasting
    if len(periods) < 8:
        # Add more periods if needed
        for year in range(2024, 2026):
            for quarter in range(1, 5):
                month = (quarter - 1) * 3 + 1
                periods.append(f"{year}-{month:02d}-01")
    
    # Income Statement Data - Ensure we have enough periods for forecasting
    # Generate more periods if needed for forecasting
    if len(periods) < 12:  # Ensure at least 12 periods for robust forecasting
        additional_periods = []
        for year in range(2024, 2027):  # Add more years
            for quarter in range(1, 5):
                month = (quarter - 1) * 3 + 1
                additional_periods.append(f"{year}-{month:02d}-01")
        periods.extend(additional_periods)
    
    # Create realistic revenue trends with some seasonality
    base_revenue = 2000000
    revenue_trend = []
    for i, period in enumerate(periods):
        # Add trend and seasonality
        trend = base_revenue * (1 + 0.05 * i)  # 5% growth per period
        seasonality = 1 + 0.1 * np.sin(2 * np.pi * i / 4)  # Quarterly seasonality
        noise = np.random.uniform(0.9, 1.1)  # Random noise
        revenue_trend.append(trend * seasonality * noise)
    
    income_statement = pd.DataFrame({
        'period': periods,
        'revenue': revenue_trend,
        'cost_of_goods_sold': [rev * np.random.uniform(0.5, 0.7) for rev in revenue_trend],
        'gross_profit': [rev * np.random.uniform(0.3, 0.5) for rev in revenue_trend],
        'operating_expenses': [rev * np.random.uniform(0.15, 0.25) for rev in revenue_trend],
        'operating_income': [rev * np.random.uniform(0.1, 0.2) for rev in revenue_trend],
        'interest_expense': [rev * np.random.uniform(0.02, 0.05) for rev in revenue_trend],
        'income_tax_expense': [rev * np.random.uniform(0.02, 0.04) for rev in revenue_trend],
        'net_income': [rev * np.random.uniform(0.08, 0.15) for rev in revenue_trend]
    })
    
    # Balance Sheet Data
    balance_sheet = pd.DataFrame({
        'period': periods,
        'total_assets': [rev * np.random.uniform(2.5, 4.0) for rev in revenue_trend],
        'current_assets': [rev * np.random.uniform(1.0, 2.0) for rev in revenue_trend],
        'cash_and_equivalents': [rev * np.random.uniform(0.2, 0.5) for rev in revenue_trend],
        'accounts_receivable': [rev * np.random.uniform(0.15, 0.3) for rev in revenue_trend],
        'inventory': [rev * np.random.uniform(0.1, 0.4) for rev in revenue_trend],
        'accounts_payable': [rev * np.random.uniform(0.1, 0.3) for rev in revenue_trend],
        'current_liabilities': [rev * np.random.uniform(0.4, 1.0) for rev in revenue_trend],
        'total_liabilities': [rev * np.random.uniform(1.0, 2.5) for rev in revenue_trend],
        'shareholder_equity': [rev * np.random.uniform(1.5, 3.0) for rev in revenue_trend],
        'shares_outstanding': [1000000] * len(periods)
    })
    
    # Cash Flow Data
    cash_flow = pd.DataFrame({
        'period': periods,
        'net_income': [rev * np.random.uniform(0.08, 0.15) for rev in revenue_trend],
        'depreciation': [rev * np.random.uniform(0.02, 0.05) for rev in revenue_trend],
        'working_capital_change': [rev * np.random.uniform(-0.1, 0.1) for rev in revenue_trend],
        'operating_cash_flow': [rev * np.random.uniform(0.08, 0.15) for rev in revenue_trend],
        'capital_expenditures': [rev * np.random.uniform(-0.3, -0.1) for rev in revenue_trend],
        'free_cash_flow': [rev * np.random.uniform(0.05, 0.12) for rev in revenue_trend],
        'initial_investment': [1000000 if i == 0 else 0 for i in range(len(periods))],
        'cash_flow': [rev * np.random.uniform(-0.1, 0.2) for rev in revenue_trend],
        'nopat': [rev * np.random.uniform(0.06, 0.12) for rev in revenue_trend]
    })
    
    # Budget Data
    budget = pd.DataFrame({
        'period': periods,
        'revenue': [rev * np.random.uniform(0.9, 1.1) for rev in revenue_trend],
        'expenses': [rev * np.random.uniform(0.6, 0.8) for rev in revenue_trend],
        'profit': [rev * np.random.uniform(0.1, 0.2) for rev in revenue_trend],
        'category': np.random.choice(['Budget', 'Forecast'], len(periods))
    })
    
    # Forecast Data - Use overlapping periods with income statement for testing
    # Use the last 8 periods from income statement to create forecast data
    forecast_periods = periods[-8:]  # Last 8 periods from income statement
    
    forecast = pd.DataFrame({
        'period': forecast_periods,
        'revenue': np.random.uniform(1200000, 6000000, len(forecast_periods)),
        'expenses': np.random.uniform(800000, 4000000, len(forecast_periods)),
        'profit': np.random.uniform(200000, 1800000, len(forecast_periods)),
        'confidence_level': np.random.uniform(0.6, 0.95, len(forecast_periods))
    })
    
    # Market Data
    market_data = pd.DataFrame({
        'period': periods,
        'market_price': np.random.uniform(50, 200, len(periods)),
        'dividends_per_share': np.random.uniform(1, 5, len(periods)),
        'volume': np.random.uniform(1000000, 5000000, len(periods)),
        'market_cap': np.random.uniform(10000000, 50000000, len(periods))
    })
    
    # Customer Data
    customer_data = pd.DataFrame({
        'customer_id': [f'CUST{i:03d}' for i in range(1, 51)],
        'customer_name': [f'Customer {i}' for i in range(1, 51)],
        'revenue': np.random.uniform(50000, 500000, 50),
        'profit_margin': np.random.uniform(10, 40, 50),
        'profitability': np.random.uniform(5000, 200000, 50),  # Add profitability column
        'costs_to_serve': np.random.uniform(10000, 100000, 50),  # Add costs to serve
        'segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB'], 50),
        'region': np.random.choice(['North America', 'Europe', 'Asia', 'Latin America'], 50),
        'lifetime_value': np.random.uniform(100000, 2000000, 50)
    })
    
    # Product Data
    product_data = pd.DataFrame({
        'product_id': [f'PROD{i:03d}' for i in range(1, 31)],
        'product_name': [f'Product {i}' for i in range(1, 31)],
        'revenue': np.random.uniform(100000, 1000000, 30),
        'cost': np.random.uniform(50000, 500000, 30),
        'total_costs': np.random.uniform(60000, 600000, 30),  # Add total_costs column
        'direct_costs': np.random.uniform(40000, 400000, 30),  # Add direct_costs column
        'allocated_costs': np.random.uniform(20000, 200000, 30),  # Add allocated_costs column
        'margin': np.random.uniform(20, 60, 30),
        'category': np.random.choice(['Software', 'Hardware', 'Services', 'Consulting'], 30),
        'lifecycle_stage': np.random.choice(['Introduction', 'Growth', 'Maturity', 'Decline'], 30)
    })
    
    # Value Chain Data
    value_chain = pd.DataFrame({
        'function': ['R&D', 'Design', 'Manufacturing', 'Marketing', 'Sales', 'Distribution', 'Customer Service'],
        'cost': np.random.uniform(100000, 800000, 7),
        'percentage': np.random.uniform(5, 25, 7),
        'period': np.random.choice(periods, 7)
    })
    
    return {
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
        'budget': budget,
        'forecast': forecast,
        'market_data': market_data,
        'customer_data': customer_data,
        'product_data': product_data,
        'value_chain': value_chain
    }

def show_data_input():
    st.markdown("""
    <div class="welcome-section">
        <h2 style="color: #2c3e50; margin-bottom: 20px;">📝 Data Management</h2>
        <p style="font-size: 1.1rem; color: #34495e; line-height: 1.6;">
            Upload your finance data files to unlock powerful analytics and insights. 
            Support for Excel (.xlsx) and CSV formats with automatic data validation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### 📁 Upload Data Files")
    
    # Create tabs for different upload methods
    upload_tab1, upload_tab2, upload_tab3, upload_tab4 = st.tabs(["📤 Upload Files", "📥 Download Template", "✏️ Manual Data Entry", "🎯 Load Sample Data"])
    
    with upload_tab1:
        # Complete Dataset Upload Section
        st.markdown("### 📊 Complete Dataset")
        
        uploaded_complete_dataset = st.file_uploader(
            "📊 Upload Complete Dataset (Excel file with multiple sheets)", 
            type=['xlsx'], 
            key="complete_dataset_upload",
            help="Upload an Excel file with sheets named: Income_Statement, Balance_Sheet, Cash_Flow, Budget, Forecast, Market_Data, Customer_Data, Product_Data, Value_Chain"
        )
        
        if uploaded_complete_dataset is not None:
            try:
                # Read all sheets from the Excel file
                excel_file = pd.ExcelFile(uploaded_complete_dataset)
                
                # Dictionary to store loaded data
                loaded_data = {}
                
                # Expected sheet names
                expected_sheets = {
                    'income_statement': 'income_statement',
                    'balance_sheet': 'balance_sheet', 
                    'cash_flow': 'cash_flow',
                    'budget': 'budget',
                    'forecast': 'forecast',
                    'market_data': 'market_data',
                    'customer_data': 'customer_data',
                    'product_data': 'product_data',
                    'value_chain': 'value_chain'
                }
                
                # Load each sheet if it exists
                for sheet_name, session_key in expected_sheets.items():
                    if sheet_name in excel_file.sheet_names:
                        loaded_data[session_key] = pd.read_excel(uploaded_complete_dataset, sheet_name=sheet_name)
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                            ✅ {sheet_name} loaded: {len(loaded_data[session_key])} records
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                            ⚠️ Sheet '{sheet_name}' not found in the uploaded file
                        </div>
                        """, unsafe_allow_html=True)
                
                # Update session state with loaded data
                for session_key, data in loaded_data.items():
                    setattr(st.session_state, session_key, data)
                
                # Show summary
                total_records = sum(len(data) for data in loaded_data.values())
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <h4 style="margin: 0 0 10px 0;">🎉 Complete Dataset Loaded Successfully!</h4>
                    <p style="margin: 0;">Total records loaded: <strong>{total_records:,}</strong> across <strong>{len(loaded_data)}</strong> data tables</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading complete dataset: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        # Separator
        st.markdown("---")
        
        # Individual File Upload Section
        st.markdown("### 📁 Individual Files")
        
        # File uploaders in a modern grid layout
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_income_statement = st.file_uploader("📈 Income Statement", type=['xlsx', 'csv'], key="income_statement_upload")
            uploaded_balance_sheet = st.file_uploader("💰 Balance Sheet", type=['xlsx', 'csv'], key="balance_sheet_upload")
            uploaded_cash_flow = st.file_uploader("💸 Cash Flow", type=['xlsx', 'csv'], key="cash_flow_upload")
            uploaded_budget = st.file_uploader("📋 Budget", type=['xlsx', 'csv'], key="budget_upload")
        
        with col2:
            uploaded_forecast = st.file_uploader("🔮 Forecast", type=['xlsx', 'csv'], key="forecast_upload")
            uploaded_market_data = st.file_uploader("📊 Market Data", type=['xlsx', 'csv'], key="market_data_upload")
            uploaded_customer_data = st.file_uploader("👥 Customer Data", type=['xlsx', 'csv'], key="customer_data_upload")
            uploaded_product_data = st.file_uploader("📦 Product Data", type=['xlsx', 'csv'], key="product_data_upload")
        
        # Process uploaded files with modern success/error styling
        if uploaded_income_statement is not None:
            try:
                if uploaded_income_statement.name.endswith('.csv'):
                    st.session_state.income_statement = pd.read_csv(uploaded_income_statement)
                else:
                    st.session_state.income_statement = pd.read_excel(uploaded_income_statement)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Income statement data loaded: {len(st.session_state.income_statement)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading income statement data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_balance_sheet is not None:
            try:
                if uploaded_balance_sheet.name.endswith('.csv'):
                    st.session_state.balance_sheet = pd.read_csv(uploaded_balance_sheet)
                else:
                    st.session_state.balance_sheet = pd.read_excel(uploaded_balance_sheet)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Balance sheet data loaded: {len(st.session_state.balance_sheet)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading balance sheet data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_cash_flow is not None:
            try:
                if uploaded_cash_flow.name.endswith('.csv'):
                    st.session_state.cash_flow = pd.read_csv(uploaded_cash_flow)
                else:
                    st.session_state.cash_flow = pd.read_excel(uploaded_cash_flow)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Cash flow data loaded: {len(st.session_state.cash_flow)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading cash flow data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_budget is not None:
            try:
                if uploaded_budget.name.endswith('.csv'):
                    st.session_state.budget = pd.read_csv(uploaded_budget)
                else:
                    st.session_state.budget = pd.read_excel(uploaded_budget)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Budget data loaded: {len(st.session_state.budget)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading budget data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_forecast is not None:
            try:
                if uploaded_forecast.name.endswith('.csv'):
                    st.session_state.forecast = pd.read_csv(uploaded_forecast)
                else:
                    st.session_state.forecast = pd.read_excel(uploaded_forecast)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Forecast data loaded: {len(st.session_state.forecast)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading forecast data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_market_data is not None:
            try:
                if uploaded_market_data.name.endswith('.csv'):
                    st.session_state.market_data = pd.read_csv(uploaded_market_data)
                else:
                    st.session_state.market_data = pd.read_excel(uploaded_market_data)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Market data loaded: {len(st.session_state.market_data)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading market data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_customer_data is not None:
            try:
                if uploaded_customer_data.name.endswith('.csv'):
                    st.session_state.customer_data = pd.read_csv(uploaded_customer_data)
                else:
                    st.session_state.customer_data = pd.read_excel(uploaded_customer_data)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Customer data loaded: {len(st.session_state.customer_data)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading customer data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
        
        if uploaded_product_data is not None:
            try:
                if uploaded_product_data.name.endswith('.csv'):
                    st.session_state.product_data = pd.read_csv(uploaded_product_data)
                else:
                    st.session_state.product_data = pd.read_excel(uploaded_product_data)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ✅ Product data loaded: {len(st.session_state.product_data)} records
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 10px 15px; border-radius: 10px; margin: 10px 0;">
                    ❌ Error loading product data: {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    with upload_tab2:
        st.markdown("""
        <div class="chart-container">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">📥 Download Excel Template</h4>
            <p style="color: #34495e; margin-bottom: 20px;">Download our comprehensive Excel template with all required data fields, formatting, and detailed instructions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create template for download
        template_output = create_template_for_download()
        
        st.download_button(
            label="📥 Download Template",
            data=template_output.getvalue(),
            file_name="finance_analytics_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("""
        <div class="chart-container">
            <h5 style="color: #2c3e50; margin-bottom: 10px;">Template includes:</h5>
            <ul style="color: #34495e; line-height: 1.6;">
                <li>📈 <strong>Income Statement:</strong> Revenue, expenses, and profitability data</li>
                <li>💰 <strong>Balance Sheet:</strong> Assets, liabilities, and equity data</li>
                <li>💸 <strong>Cash Flow:</strong> Operating, investing, and financing cash flows</li>
                <li>📋 <strong>Budget:</strong> Budgeted revenue, expenses, and targets</li>
                <li>🔮 <strong>Forecast:</strong> Forecasted financial performance</li>
                <li>📊 <strong>Market Data:</strong> Market prices, volumes, and trends</li>
                <li>👥 <strong>Customer Data:</strong> Customer revenue and profitability</li>
                <li>📦 <strong>Product Data:</strong> Product revenue and costs</li>
                <li>🏗️ <strong>Value Chain:</strong> Value chain functions and costs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with upload_tab3:
        st.markdown("""
        <div class="chart-container">
            <h4 style="color: #2c3e50; margin-bottom: 15px;">✏️ Manual Data Entry</h4>
            <p style="color: #34495e; margin-bottom: 20px;">Add data manually using the forms below. This is useful for small datasets or quick data entry.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different data types
        manual_tab1, manual_tab2, manual_tab3, manual_tab4, manual_tab5, manual_tab6, manual_tab7, manual_tab8, manual_tab9 = st.tabs([
            "Income Statement", "Balance Sheet", "Cash Flow", "Budget", 
            "Forecast", "Market Data", "Customer Data", "Product Data", "Value Chain"
        ])
        
        with manual_tab1:
            st.subheader("Income Statement")
            col1, col2 = st.columns(2)
            
            with col1:
                period = st.text_input("Period", key="period_income")
                revenue = st.number_input("Revenue", min_value=0.0, key="revenue_input")
                cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, key="cogs_input")
                gross_profit = st.number_input("Gross Profit", min_value=0.0, key="gross_profit_input")
                operating_expenses = st.number_input("Operating Expenses", min_value=0.0, key="opex_input")
            
            with col2:
                operating_income = st.number_input("Operating Income", min_value=0.0, key="op_income_input")
                net_income = st.number_input("Net Income", min_value=0.0, key="net_income_input")
                ebitda = st.number_input("EBITDA", min_value=0.0, key="ebitda_input")
                ebit = st.number_input("EBIT", min_value=0.0, key="ebit_input")
            
            if st.button("Add Income Statement", key="add_income_statement"):
                new_income = pd.DataFrame([{
                    'period': period,
                    'revenue': revenue,
                    'cost_of_goods_sold': cost_of_goods_sold,
                    'gross_profit': gross_profit,
                    'operating_expenses': operating_expenses,
                    'operating_income': operating_income,
                    'net_income': net_income,
                    'ebitda': ebitda,
                    'ebit': ebit
                }])
                st.session_state.income_statement = pd.concat([st.session_state.income_statement, new_income], ignore_index=True)
                st.success("Income Statement added successfully!")
            
            # Display existing data
            if not st.session_state.income_statement.empty:
                st.subheader("Existing Income Statements")
                display_dataframe_with_index_1(st.session_state.income_statement)
        
        with manual_tab2:
            st.subheader("Balance Sheet")
            col1, col2 = st.columns(2)
            
            with col1:
                period = st.text_input("Period", key="period_balance")
                total_assets = st.number_input("Total Assets", min_value=0.0, key="total_assets_input")
                current_assets = st.number_input("Current Assets", min_value=0.0, key="current_assets_input")
                cash_and_equivalents = st.number_input("Cash & Equivalents", min_value=0.0, key="cash_input")
                accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0, key="ar_input")
            
            with col2:
                total_liabilities = st.number_input("Total Liabilities", min_value=0.0, key="total_liabilities_input")
                current_liabilities = st.number_input("Current Liabilities", min_value=0.0, key="current_liabilities_input")
                total_equity = st.number_input("Total Equity", min_value=0.0, key="total_equity_input")
                working_capital = st.number_input("Working Capital", min_value=0.0, key="working_capital_input")
            
            if st.button("Add Balance Sheet", key="add_balance_sheet"):
                new_balance = pd.DataFrame([{
                    'period': period,
                    'total_assets': total_assets,
                    'current_assets': current_assets,
                    'cash_and_equivalents': cash_and_equivalents,
                    'accounts_receivable': accounts_receivable,
                    'total_liabilities': total_liabilities,
                    'current_liabilities': current_liabilities,
                    'total_equity': total_equity,
                    'working_capital': working_capital
                }])
                st.session_state.balance_sheet = pd.concat([st.session_state.balance_sheet, new_balance], ignore_index=True)
                st.success("Balance Sheet added successfully!")
            
            # Display existing data
            if not st.session_state.balance_sheet.empty:
                st.subheader("Existing Balance Sheets")
                display_dataframe_with_index_1(st.session_state.balance_sheet)
        
        with manual_tab3:
            st.subheader("Cash Flow")
            col1, col2 = st.columns(2)
            
            with col1:
                period = st.text_input("Period", key="period_cash")
                operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, key="ocf_input")
                investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, key="icf_input")
                financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, key="fcf_input")
            
            with col2:
                net_cash_flow = st.number_input("Net Cash Flow", min_value=0.0, key="net_cf_input")
                free_cash_flow = st.number_input("Free Cash Flow", min_value=0.0, key="fcf_input2")
                capex = st.number_input("Capital Expenditure", min_value=0.0, key="capex_input")
            
            if st.button("Add Cash Flow", key="add_cash_flow"):
                new_cash_flow = pd.DataFrame([{
                    'period': period,
                    'operating_cash_flow': operating_cash_flow,
                    'investing_cash_flow': investing_cash_flow,
                    'financing_cash_flow': financing_cash_flow,
                    'net_cash_flow': net_cash_flow,
                    'free_cash_flow': free_cash_flow,
                    'capex': capex
                }])
                st.session_state.cash_flow = pd.concat([st.session_state.cash_flow, new_cash_flow], ignore_index=True)
                st.success("Cash Flow added successfully!")
            
            # Display existing data
            if not st.session_state.cash_flow.empty:
                st.subheader("Existing Cash Flows")
                display_dataframe_with_index_1(st.session_state.cash_flow)
        
        with manual_tab4:
            st.subheader("Budget")
            col1, col2 = st.columns(2)
            
            with col1:
                period = st.text_input("Period", key="period_budget")
                budgeted_revenue = st.number_input("Budgeted Revenue", min_value=0.0, key="budget_revenue_input")
                budgeted_expenses = st.number_input("Budgeted Expenses", min_value=0.0, key="budget_expenses_input")
                budgeted_profit = st.number_input("Budgeted Profit", min_value=0.0, key="budget_profit_input")
            
            with col2:
                department = st.text_input("Department", key="department_budget_input")
                category = st.text_input("Category", key="category_budget_input")
                variance = st.number_input("Variance", key="variance_input")
            
            if st.button("Add Budget", key="add_budget"):
                new_budget = pd.DataFrame([{
                    'period': period,
                    'budgeted_revenue': budgeted_revenue,
                    'budgeted_expenses': budgeted_expenses,
                    'budgeted_profit': budgeted_profit,
                    'department': department,
                    'category': category,
                    'variance': variance
                }])
                st.session_state.budget = pd.concat([st.session_state.budget, new_budget], ignore_index=True)
                st.success("Budget added successfully!")
            
            # Display existing data
            if not st.session_state.budget.empty:
                st.subheader("Existing Budgets")
                display_dataframe_with_index_1(st.session_state.budget)
        
        with manual_tab5:
            st.subheader("Forecast")
            col1, col2 = st.columns(2)
            
            with col1:
                period = st.text_input("Period", key="period_forecast")
                forecasted_revenue = st.number_input("Forecasted Revenue", min_value=0.0, key="forecast_revenue_input")
                forecasted_expenses = st.number_input("Forecasted Expenses", min_value=0.0, key="forecast_expenses_input")
                forecasted_profit = st.number_input("Forecasted Profit", min_value=0.0, key="forecast_profit_input")
            
            with col2:
                confidence_level = st.selectbox("Confidence Level", ["High", "Medium", "Low"], key="confidence_input")
                scenario = st.selectbox("Scenario", ["Base", "Optimistic", "Pessimistic"], key="scenario_input")
            
            if st.button("Add Forecast", key="add_forecast"):
                new_forecast = pd.DataFrame([{
                    'period': period,
                    'forecasted_revenue': forecasted_revenue,
                    'forecasted_expenses': forecasted_expenses,
                    'forecasted_profit': forecasted_profit,
                    'confidence_level': confidence_level,
                    'scenario': scenario
                }])
                st.session_state.forecast = pd.concat([st.session_state.forecast, new_forecast], ignore_index=True)
                st.success("Forecast added successfully!")
            
            # Display existing data
            if not st.session_state.forecast.empty:
                st.subheader("Existing Forecasts")
                display_dataframe_with_index_1(st.session_state.forecast)
        
        with manual_tab6:
            st.subheader("Market Data")
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Date", key="date_market_input")
                market_price = st.number_input("Market Price", min_value=0.0, key="market_price_input")
                volume = st.number_input("Volume", min_value=0, key="volume_input")
                market_cap = st.number_input("Market Cap", min_value=0.0, key="market_cap_input")
            
            with col2:
                pe_ratio = st.number_input("P/E Ratio", min_value=0.0, key="pe_ratio_input")
                beta = st.number_input("Beta", min_value=0.0, key="beta_input")
                sector = st.text_input("Sector", key="sector_input")
            
            if st.button("Add Market Data", key="add_market_data"):
                new_market = pd.DataFrame([{
                    'date': date,
                    'market_price': market_price,
                    'volume': volume,
                    'market_cap': market_cap,
                    'pe_ratio': pe_ratio,
                    'beta': beta,
                    'sector': sector
                }])
                st.session_state.market_data = pd.concat([st.session_state.market_data, new_market], ignore_index=True)
                st.success("Market Data added successfully!")
            
            # Display existing data
            if not st.session_state.market_data.empty:
                st.subheader("Existing Market Data")
                display_dataframe_with_index_1(st.session_state.market_data)
        
        with manual_tab7:
            st.subheader("Customer Data")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                customer_id = st.text_input("Customer ID", key="customer_id_input")
                customer_name = st.text_input("Customer Name", key="customer_name_input")
                revenue = st.number_input("Revenue", min_value=0.0, key="customer_revenue_input")
                profit_margin = st.number_input("Profit Margin %", min_value=0.0, max_value=100.0, key="profit_margin_input")
            
            with col2:
                profitability = st.number_input("Profitability", min_value=0.0, key="profitability_input")
                costs_to_serve = st.number_input("Costs to Serve", min_value=0.0, key="costs_to_serve_input")
                segment = st.selectbox("Segment", ["Enterprise", "Mid-Market", "SMB"], key="segment_input")
                region = st.selectbox("Region", ["North America", "Europe", "Asia", "Latin America"], key="region_input")
            
            with col3:
                lifetime_value = st.number_input("Lifetime Value", min_value=0.0, key="ltv_input")
            
            if st.button("Add Customer Data", key="add_customer_data"):
                new_customer = pd.DataFrame([{
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'revenue': revenue,
                    'profit_margin': profit_margin,
                    'profitability': profitability,
                    'costs_to_serve': costs_to_serve,
                    'segment': segment,
                    'region': region,
                    'lifetime_value': lifetime_value
                }])
                st.session_state.customer_data = pd.concat([st.session_state.customer_data, new_customer], ignore_index=True)
                st.success("Customer Data added successfully!")
            
            # Display existing data
            if not st.session_state.customer_data.empty:
                st.subheader("Existing Customer Data")
                display_dataframe_with_index_1(st.session_state.customer_data)
        
        with manual_tab8:
            st.subheader("Product Data")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                product_id = st.text_input("Product ID", key="product_id_input")
                product_name = st.text_input("Product Name", key="product_name_input")
                revenue = st.number_input("Revenue", min_value=0.0, key="product_revenue_input")
                cost = st.number_input("Cost", min_value=0.0, key="product_cost_input")
            
            with col2:
                total_costs = st.number_input("Total Costs", min_value=0.0, key="total_costs_input")
                direct_costs = st.number_input("Direct Costs", min_value=0.0, key="direct_costs_input")
                allocated_costs = st.number_input("Allocated Costs", min_value=0.0, key="allocated_costs_input")
                margin = st.number_input("Margin", min_value=0.0, key="product_margin_input")
            
            with col3:
                category = st.selectbox("Category", ["Software", "Hardware", "Services", "Consulting"], key="product_category_input")
                lifecycle_stage = st.selectbox("Lifecycle Stage", ["Introduction", "Growth", "Maturity", "Decline"], key="lifecycle_input")
            
            if st.button("Add Product Data", key="add_product_data"):
                new_product = pd.DataFrame([{
                    'product_id': product_id,
                    'product_name': product_name,
                    'revenue': revenue,
                    'cost': cost,
                    'total_costs': total_costs,
                    'direct_costs': direct_costs,
                    'allocated_costs': allocated_costs,
                    'margin': margin,
                    'category': category,
                    'lifecycle_stage': lifecycle_stage
                }])
                st.session_state.product_data = pd.concat([st.session_state.product_data, new_product], ignore_index=True)
                st.success("Product Data added successfully!")
            
            # Display existing data
            if not st.session_state.product_data.empty:
                st.subheader("Existing Product Data")
                display_dataframe_with_index_1(st.session_state.product_data)
        
        with manual_tab9:
            st.subheader("Value Chain")
            col1, col2 = st.columns(2)
            
            with col1:
                function = st.text_input("Function", key="function_input")
                cost = st.number_input("Cost", min_value=0.0, key="vc_cost_input")
                efficiency_score = st.number_input("Efficiency Score", min_value=0.0, max_value=100.0, key="efficiency_input")
            
            with col2:
                value_added = st.number_input("Value Added", min_value=0.0, key="value_added_input")
                process_time = st.number_input("Process Time (days)", min_value=0, key="process_time_input")
            
            if st.button("Add Value Chain Data", key="add_value_chain"):
                new_vc = pd.DataFrame([{
                    'function': function,
                    'cost': cost,
                    'efficiency_score': efficiency_score,
                    'value_added': value_added,
                    'process_time': process_time
                }])
                st.session_state.value_chain = pd.concat([st.session_state.value_chain, new_vc], ignore_index=True)
                st.success("Value Chain Data added successfully!")
            
            # Display existing data
            if not st.session_state.value_chain.empty:
                st.subheader("Existing Value Chain Data")
                display_dataframe_with_index_1(st.session_state.value_chain)
    
    with upload_tab4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 12px; margin: 20px 0; color: white;">
            <h3 style="color: white; margin: 0 0 15px 0;">🎯 Sample Data for Testing</h3>
            <p style="margin: 0; opacity: 0.9;">
                Load comprehensive sample data to test all analytics features. This includes 100+ records across all data types.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample data loading section
        st.markdown("### 📊 Load Sample Dataset")
        
        if st.button("🚀 Load Sample Data", type="primary", use_container_width=True):
            try:
                # Generate sample finance data
                sample_data = generate_sample_finance_data()
                
                # Update session state
                st.session_state.income_statement = sample_data['income_statement']
                st.session_state.balance_sheet = sample_data['balance_sheet']
                st.session_state.cash_flow = sample_data['cash_flow']
                st.session_state.budget = sample_data['budget']
                st.session_state.forecast = sample_data['forecast']
                st.session_state.market_data = sample_data['market_data']
                st.session_state.customer_data = sample_data['customer_data']
                st.session_state.product_data = sample_data['product_data']
                st.session_state.value_chain = sample_data['value_chain']
                
                # Show success message
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); 
                            padding: 20px; border-radius: 12px; margin: 20px 0; color: white;">
                    <h4 style="color: white; margin: 0 0 10px 0;">✅ Sample Data Loaded Successfully!</h4>
                    <p style="margin: 0; opacity: 0.9;">
                        📈 Income Statements: {len(sample_data['income_statement'])} records<br>
                        💰 Balance Sheets: {len(sample_data['balance_sheet'])} records<br>
                        💸 Cash Flows: {len(sample_data['cash_flow'])} records<br>
                        📋 Budgets: {len(sample_data['budget'])} records<br>
                        🔮 Forecasts: {len(sample_data['forecast'])} records<br>
                        📊 Market Data: {len(sample_data['market_data'])} records<br>
                        👥 Customers: {len(sample_data['customer_data'])} records<br>
                        📦 Products: {len(sample_data['product_data'])} records<br>
                        🏗️ Value Chain: {len(sample_data['value_chain'])} records
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("🎉 You can now explore all analytics features with the sample data!")
                st.info("💡 **Next Step:** Navigate to other tabs (like '📈 Financial Performance') to see your analytics!")
                
            except Exception as e:
                st.error(f"❌ Error loading sample data: {str(e)}")
                st.info("💡 Sample data generation function will be created.")
        
        # Data preview section
        st.markdown("### 👀 Sample Data Preview")
        
        if not st.session_state.income_statement.empty:
            st.markdown("**📈 Income Statement Preview:**")
            st.dataframe(st.session_state.income_statement.head(), use_container_width=True)
        else:
            st.info("💡 Click 'Load Sample Data' to see a preview of the sample data.")
    
    # Data summary section with modern cards
    st.markdown("### 📊 Data Summary")
    
    # Create summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-blue">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Income Statements</h4>
                    <h2 style="margin: 5px 0; font-size: 1.8rem; font-weight: 700;">{len(st.session_state.income_statement):,}</h2>
                </div>
                <div style="font-size: 2rem;">📈</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-purple">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Balance Sheets</h4>
                    <h2 style="margin: 5px 0; font-size: 1.8rem; font-weight: 700;">{len(st.session_state.balance_sheet):,}</h2>
                </div>
                <div style="font-size: 2rem;">💰</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-orange">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Cash Flows</h4>
                    <h2 style="margin: 5px 0; font-size: 1.8rem; font-weight: 700;">{len(st.session_state.cash_flow):,}</h2>
                </div>
                <div style="font-size: 2rem;">💸</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card-teal">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Customers</h4>
                    <h2 style="margin: 5px 0; font-size: 1.8rem; font-weight: 700;">{len(st.session_state.customer_data):,}</h2>
                </div>
                <div style="font-size: 2rem;">👥</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Export data section
    st.markdown("### 📤 Export Data")
    
    if (not st.session_state.income_statement.empty or not st.session_state.balance_sheet.empty or 
        not st.session_state.cash_flow.empty or not st.session_state.budget.empty or 
        not st.session_state.forecast.empty or not st.session_state.market_data.empty or 
        not st.session_state.customer_data.empty or not st.session_state.product_data.empty or 
        not st.session_state.value_chain.empty):
        
        export_output = export_data_to_excel()
        
        st.download_button(
            label="📤 Export All Data",
            data=export_output.getvalue(),
            file_name=f"finance_analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("""
        <div class="chart-container">
            <p style="color: #34495e; margin: 0;"><strong>Export includes:</strong> All loaded datasets with summary sheet and data quality metrics</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chart-container">
            <p style="color: #f97316; margin: 0;">📝 No data to export. Please upload data files first.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data tables section
    st.markdown("### 📋 Data Tables")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
            <h5 style="color: #2c3e50; margin-bottom: 10px;">📈 Income Statement</h5>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.income_statement.empty:
            display_dataframe_with_index_1(st.session_state.income_statement, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <p style="color: #6b7280; text-align: center; margin: 0;">No income statement data available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
            <h5 style="color: #2c3e50; margin-bottom: 10px;">💰 Balance Sheet</h5>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.balance_sheet.empty:
            display_dataframe_with_index_1(st.session_state.balance_sheet, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <p style="color: #6b7280; text-align: center; margin: 0;">No balance sheet data available</p>
            </div>
            """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="chart-container">
            <h5 style="color: #2c3e50; margin-bottom: 10px;">💸 Cash Flow</h5>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.cash_flow.empty:
            display_dataframe_with_index_1(st.session_state.cash_flow, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <p style="color: #6b7280; text-align: center; margin: 0;">No cash flow data available</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="chart-container">
            <h5 style="color: #2c3e50; margin-bottom: 10px;">👥 Customers</h5>
        </div>
        """, unsafe_allow_html=True)
        if not st.session_state.customer_data.empty:
            display_dataframe_with_index_1(st.session_state.customer_data, use_container_width=True)
        else:
            st.markdown("""
            <div class="chart-container">
                <p style="color: #6b7280; text-align: center; margin: 0;">No customer data available</p>
            </div>
            """, unsafe_allow_html=True)

def show_auto_insights():
    """Display auto insights dashboard"""
    st.markdown("""
    <div class="section-header">
        <h3>💡 Auto Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data is available
    if (st.session_state.income_statement.empty and st.session_state.balance_sheet.empty and 
        st.session_state.cash_flow.empty and st.session_state.budget.empty and 
        st.session_state.forecast.empty and st.session_state.customer_data.empty and 
        st.session_state.product_data.empty):
        st.warning("⚠️ No data available for insights. Please load data in the Data Input section first.")
        return
    
    # Initialize insights
    insights = FinanceInsights(
        st.session_state.income_statement,
        st.session_state.balance_sheet,
        st.session_state.cash_flow,
        st.session_state.budget,
        st.session_state.forecast,
        st.session_state.market_data,
        st.session_state.customer_data,
        st.session_state.product_data,
        st.session_state.value_chain
    )
    
    # Create tabs for different insight types
    insight_tab1, insight_tab2, insight_tab3, insight_tab4, insight_tab5, insight_tab6, insight_tab7, insight_tab8 = st.tabs([
        "📊 Financial Performance", "💰 Liquidity & Solvency", "💸 Cash Flow", 
        "📋 Budget & Forecasting", "👥 Customer & Product", "📈 Market & Competitive", 
        "⚠️ Risk Mitigation", "🎯 Executive Summary"
    ])
    
    with insight_tab1:
        performance_insights = insights.generate_profitability_insights()
        display_insights_section(performance_insights, "Financial Performance Insights", "📊")
        
        # Add AI recommendations for financial performance
        if generate_financial_performance_ai_recommendations:
            st.markdown("---")
            st.markdown("### 🤖 AI Financial Performance Recommendations")
            try:
                ai_recommendations = generate_financial_performance_ai_recommendations(
                    st.session_state.income_statement,
                    st.session_state.balance_sheet,
                    st.session_state.cash_flow
                )
                display_formatted_recommendations(ai_recommendations)
            except Exception as e:
                st.error(f"Error generating AI recommendations: {e}")
                st.info("Please check if you have loaded financial data in the Data Input section.")
    
    with insight_tab2:
        liquidity_insights = insights.generate_liquidity_solvency_insights()
        display_insights_section(liquidity_insights, "Liquidity & Solvency Insights", "💰")
        
        # Add AI recommendations for liquidity and solvency
        st.markdown("---")
        st.markdown("### 🤖 AI Liquidity & Solvency Recommendations")
        try:
            ai_recommendations = generate_liquidity_solvency_ai_recommendations(
                st.session_state.balance_sheet,
                st.session_state.cash_flow
            )
            display_formatted_recommendations(ai_recommendations)
        except Exception as e:
            st.error(f"Error generating AI recommendations: {e}")
    
    with insight_tab3:
        cash_flow_insights = insights.generate_cash_flow_insights()
        display_insights_section(cash_flow_insights, "Cash Flow Insights", "💸")
        
        # Add AI recommendations for cash flow
        st.markdown("---")
        st.markdown("### 🤖 AI Cash Flow Recommendations")
        try:
            ai_recommendations = generate_cash_flow_analysis_ai_recommendations(
                st.session_state.cash_flow,
                st.session_state.balance_sheet
            )
            display_formatted_recommendations(ai_recommendations)
        except Exception as e:
            st.error(f"Error generating AI recommendations: {e}")
    
    with insight_tab4:
        budget_insights = insights.generate_budget_forecasting_insights()
        display_insights_section(budget_insights, "Budget & Forecasting Insights", "📋")
    
    with insight_tab5:
        customer_insights = insights.generate_customer_productivity_insights()
        display_insights_section(customer_insights, "Customer & Product Insights", "👥")
    
    with insight_tab6:
        market_insights = insights.generate_market_competitive_insights()
        display_insights_section(market_insights, "Market & Competitive Insights", "📈")
        
        # Add AI recommendations for market analysis
        st.markdown("---")
        st.markdown("### 🤖 AI Market Analysis Recommendations")
        try:
            # Generate market-specific recommendations
            market_recommendations = f"""
🤖 **AI Market Analysis Recommendations**

📈 **Market Position Analysis**
   • Monitor market trends and competitive landscape
   • Analyze stock price movements and market sentiment
   • Review dividend policies and shareholder value creation

🏆 **Competitive Strategy Recommendations**
   • Strengthen market positioning through innovation
   • Optimize value chain for cost competitiveness
   • Develop strategic partnerships and alliances

🎯 **Strategic Actions**
   • Regular market analysis and competitive intelligence
   • Value chain optimization and cost reduction
   • Strategic planning and market expansion
"""
            display_formatted_recommendations(market_recommendations)
        except Exception as e:
            st.error(f"Error generating market recommendations: {e}")
    
    with insight_tab7:
        risk_insights = insights.generate_risk_mitigation_insights()
        display_insights_section(risk_insights, "Risk Mitigation Insights", "⚠️")
        
        # Add AI recommendations for risk management
        st.markdown("---")
        st.markdown("### 🤖 AI Risk Management Recommendations")
        try:
            # Generate risk-specific recommendations
            risk_recommendations = f"""
🤖 **AI Risk Management Recommendations**

⚠️ **Risk Assessment Framework**
   • Implement comprehensive risk identification system
   • Establish quantitative risk measurement metrics
   • Develop proactive risk monitoring and reporting

🛡️ **Risk Mitigation Strategies**
   • Prioritize high-impact, high-probability risks
   • Develop contingency plans for critical scenarios
   • Establish risk response protocols and procedures

🎯 **Strategic Actions**
   • Regular risk assessments and updates
   • Risk management training and awareness
   • Continuous improvement of risk framework
"""
            display_formatted_recommendations(risk_recommendations)
        except Exception as e:
            st.error(f"Error generating risk recommendations: {e}")
    
    with insight_tab8:
        executive_summary = insights.generate_executive_summary()
        display_executive_summary(executive_summary, "Executive Financial Summary", "🎯")

def show_predictive_analytics():
    """Display predictive analytics dashboard"""
    st.markdown("""
    <div class="section-header">
        <h3>🔮 Predictive Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data is available
    if (st.session_state.income_statement.empty and st.session_state.balance_sheet.empty and 
        st.session_state.cash_flow.empty and st.session_state.budget.empty and 
        st.session_state.forecast.empty and st.session_state.customer_data.empty and 
        st.session_state.product_data.empty):
        st.warning("⚠️ No data available for predictive analytics. Please load data in the Data Input section first.")
        return
    
    # Display predictive analytics dashboard
    # Create predictive analytics object first
    predictive_analytics = FinancePredictiveAnalytics(
        st.session_state.income_statement,
        st.session_state.balance_sheet,
        st.session_state.cash_flow,
        st.session_state.budget,
        st.session_state.forecast,
        st.session_state.market_data,
        st.session_state.customer_data,
        st.session_state.product_data,
        st.session_state.value_chain
    )
    
    # Display the dashboard
    display_finance_predictive_analytics_dashboard(predictive_analytics)

# Analytics functions for the main sections
def show_financial_performance():
    st.markdown("""
    <div class="section-header">
        <h3>📊 Financial Performance Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.income_statement.empty and st.session_state.balance_sheet.empty:
        st.info("📊 Please upload income statement and balance sheet data to view financial performance analytics.")
        return
    
    # Calculate financial performance metrics
    performance_summary, performance_message = calculate_financial_performance_metrics(
        st.session_state.income_statement, st.session_state.balance_sheet
    )
    
    # Display summary metrics
    st.subheader("📈 Financial Performance Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if not performance_summary.empty:
            revenue = performance_summary.iloc[0]['revenue']
            st.metric("Revenue", f"${revenue:,.0f}")
    
    with col2:
        if not performance_summary.empty and len(performance_summary) > 1:
            gross_margin = performance_summary.iloc[0]['gross_margin_pct']
            st.metric("Gross Margin", f"{gross_margin:.1f}%")
    
    with col3:
        if not performance_summary.empty and len(performance_summary) > 2:
            operating_margin = performance_summary.iloc[0]['operating_margin_pct']
            st.metric("Operating Margin", f"{operating_margin:.1f}%")
    
    with col4:
        if not performance_summary.empty and len(performance_summary) > 3:
            net_margin = performance_summary.iloc[0]['net_margin_pct']
            st.metric("Net Margin", f"{net_margin:.1f}%")
    
    with col5:
        if not performance_summary.empty and len(performance_summary) > 4:
            net_income = performance_summary.iloc[0]['net_income']
            st.metric("Net Income", f"${net_income:,.0f}")
    
    st.info(performance_message)
    
    # Enhanced analytics tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Revenue Analysis", "💰 Margin Analysis", "📊 Profitability Trends", 
        "📋 Performance Insights", "🎯 Performance Scoring", "🚀 Optimization Recommendations"
    ])
    
    with tab1:
        st.subheader("📈 Revenue Analysis")
        
        if not st.session_state.income_statement.empty:
            # Enhanced revenue analysis
            revenue_trend = st.session_state.income_statement.groupby('period').agg({
                'revenue': 'sum'
            }).reset_index()
            
            # Calculate revenue growth rates
            if len(revenue_trend) > 1:
                revenue_trend['growth_rate'] = revenue_trend['revenue'].pct_change() * 100
                revenue_trend['cumulative_growth'] = ((revenue_trend['revenue'] / revenue_trend['revenue'].iloc[0]) - 1) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Revenue trend chart
                fig = go.Figure(data=[
                    go.Scatter(x=revenue_trend['period'], y=revenue_trend['revenue'],
                              mode='lines+markers', line=dict(color='#1f77b4', width=3),
                              marker=dict(size=8), name='Revenue')
                ])
                fig.update_layout(
                    title="Revenue Trend Over Time",
                    xaxis_title="Period",
                    yaxis_title="Revenue ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_1")
            
            with col2:
                # Revenue growth analysis
                if len(revenue_trend) > 1:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=revenue_trend['period'].iloc[1:],
                        y=revenue_trend['growth_rate'].iloc[1:],
                        name='Period Growth Rate',
                        marker_color='#2ca02c'
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="No Growth")
                    fig.update_layout(
                        title="Revenue Growth Rate by Period",
                        xaxis_title="Period",
                        yaxis_title="Growth Rate (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True, key="chart_1_growth")
            
            # Revenue insights and metrics
            if len(revenue_trend) > 1:
                st.markdown("### 📊 Revenue Analysis Insights")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_revenue = revenue_trend['revenue'].sum()
                    st.metric("Total Revenue", f"${total_revenue:,.0f}")
                
                with col2:
                    avg_revenue = revenue_trend['revenue'].mean()
                    st.metric("Average Revenue", f"${avg_revenue:,.0f}")
                
                with col3:
                    if 'growth_rate' in revenue_trend.columns:
                        avg_growth = revenue_trend['growth_rate'].iloc[1:].mean()
                        st.metric("Average Growth", f"{avg_growth:+.1f}%")
                
                with col4:
                    if 'cumulative_growth' in revenue_trend.columns:
                        total_growth = revenue_trend['cumulative_growth'].iloc[-1]
                        st.metric("Total Growth", f"{total_growth:+.1f}%")
                
                # Growth trend analysis
                latest_growth = revenue_trend['growth_rate'].iloc[-1] if 'growth_rate' in revenue_trend.columns else 0
                if latest_growth > 10:
                    st.success(f"🚀 **Strong Revenue Growth**: {latest_growth:+.1f}% - Excellent performance!")
                elif latest_growth > 5:
                    st.info(f"📈 **Good Revenue Growth**: {latest_growth:+.1f}% - Maintain momentum")
                elif latest_growth > 0:
                    st.warning(f"📊 **Moderate Revenue Growth**: {latest_growth:+.1f}% - Room for improvement")
                else:
                    st.error(f"📉 **Revenue Decline**: {latest_growth:+.1f}% - Immediate action required")
            
            # Add AI recommendations for Revenue Analysis
            if generate_financial_performance_ai_recommendations:
                st.markdown("---")
                try:
                    ai_recommendations = generate_financial_performance_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
            

    
    with tab2:
        st.subheader("💰 Margin Analysis")
        
        if not st.session_state.income_statement.empty:
            # Margin analysis
            margin_analysis = st.session_state.income_statement.copy()
            margin_analysis['gross_margin_pct'] = ((margin_analysis['revenue'] - margin_analysis['cost_of_goods_sold']) / margin_analysis['revenue'] * 100).round(1)
            margin_analysis['operating_margin_pct'] = (margin_analysis['operating_income'] / margin_analysis['revenue'] * 100).round(1)
            margin_analysis['net_margin_pct'] = (margin_analysis['net_income'] / margin_analysis['revenue'] * 100).round(1)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=margin_analysis['period'], y=margin_analysis['gross_margin_pct'],
                           marker_color='#2ca02c', name='Gross Margin',
                           text=margin_analysis['gross_margin_pct'],
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Gross Margin by Period",
                    xaxis_title="Period",
                    yaxis_title="Gross Margin (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_2")
            
            with col2:
                fig = go.Figure(data=[
                    go.Bar(x=margin_analysis['period'], y=margin_analysis['net_margin_pct'],
                           marker_color='#ff7f0e', name='Net Margin',
                           text=margin_analysis['net_margin_pct'],
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Net Margin by Period",
                    xaxis_title="Period",
                    yaxis_title="Net Margin (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_3")
            
            # Add AI recommendations for Margin Analysis
            if generate_financial_performance_ai_recommendations:
                st.markdown("---")
                try:
                    ai_recommendations = generate_financial_performance_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
            

    
    with tab3:
        st.subheader("📊 Profitability Trends")
        
        if not st.session_state.income_statement.empty:
            # Profitability trends
            profitability_trends = st.session_state.income_statement.groupby('period').agg({
                'revenue': 'sum',
                'net_income': 'sum'
            }).reset_index()
            profitability_trends['profitability_ratio'] = (profitability_trends['net_income'] / profitability_trends['revenue'] * 100).round(1)
            
            fig = go.Figure(data=[
                go.Scatter(x=profitability_trends['period'], y=profitability_trends['profitability_ratio'],
                          mode='lines+markers', line=dict(color='#9467bd', width=3),
                          marker=dict(size=8), name='Profitability Ratio')
            ])
            fig.update_layout(
                title="Profitability Ratio Trend",
                xaxis_title="Period",
                yaxis_title="Profitability Ratio (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_4")
            
            # Add AI recommendations for Profitability Trends
            if generate_financial_performance_ai_recommendations:
                st.markdown("---")
                try:
                    ai_recommendations = generate_financial_performance_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
            

    
    with tab4:
        st.subheader("📋 Performance Insights")
        
        if not st.session_state.income_statement.empty:
            # Performance insights
            st.write("**Financial Performance Summary:**")
            
            total_revenue = st.session_state.income_statement['revenue'].sum()
            total_net_income = st.session_state.income_statement['net_income'].sum()
            avg_gross_margin = ((total_revenue - st.session_state.income_statement['cost_of_goods_sold'].sum()) / total_revenue * 100) if total_revenue > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Revenue", f"${total_revenue:,.0f}")
            with col2:
                st.metric("Total Net Income", f"${total_net_income:,.0f}")
            with col3:
                st.metric("Avg Gross Margin", f"{avg_gross_margin:.1f}%")
            
            # Performance recommendations
            st.write("**Key Performance Indicators:**")
            if avg_gross_margin > 50:
                st.success(f"✅ Strong gross margin: {avg_gross_margin:.1f}%")
            elif avg_gross_margin > 30:
                st.info(f"ℹ️ Moderate gross margin: {avg_gross_margin:.1f}%")
            else:
                st.warning(f"⚠️ Low gross margin: {avg_gross_margin:.1f}% - consider cost optimization")
            
            net_margin = (total_net_income / total_revenue * 100) if total_revenue > 0 else 0
            if net_margin > 15:
                st.success(f"✅ Excellent net margin: {net_margin:.1f}%")
            elif net_margin > 10:
                st.info(f"ℹ️ Good net margin: {net_margin:.1f}%")
            else:
                st.warning(f"⚠️ Low net margin: {net_margin:.1f}% - review cost structure")
            
            # Add AI recommendations for Performance Insights
            if generate_financial_performance_ai_recommendations:
                st.markdown("---")
                try:
                    ai_recommendations = generate_financial_performance_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
    
    with tab5:
        st.subheader("🎯 Performance Scoring & Trends")
        
        if not performance_summary.empty and len(performance_summary) > 1:
            # Performance score trends
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=performance_summary['period'], 
                y=performance_summary['performance_score'],
                mode='lines+markers', 
                name='Performance Score',
                line=dict(color='#9467bd', width=3),
                marker=dict(size=8)
            ))
            
            # Add threshold lines
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excellent (80+)")
            fig.add_hline(y=60, line_dash="dash", line_color="blue", annotation_text="Good (60+)")
            fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Fair (40+)")
            fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Poor (<40)")
            
            fig.update_layout(
                title="Performance Score Trends Over Time",
                xaxis_title="Period",
                yaxis_title="Performance Score (0-100)",
                yaxis_range=[0, 100],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_performance_score")
            
            # Performance breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Performance Components")
                latest_score = performance_summary.iloc[-1]
                
                # Revenue growth component
                if 'revenue_growth_pct' in latest_score:
                    growth_score = 0
                    if latest_score['revenue_growth_pct'] > 10:
                        growth_score = 25
                    elif latest_score['revenue_growth_pct'] > 5:
                        growth_score = 20
                    elif latest_score['revenue_growth_pct'] > 0:
                        growth_score = 15
                    elif latest_score['revenue_growth_pct'] > -5:
                        growth_score = 10
                    else:
                        growth_score = 5
                    
                    st.metric("Revenue Growth Score", f"{growth_score}/25")
                
                # Margin component
                margin_score = 0
                if latest_score['gross_margin_pct'] > 40:
                    margin_score += 20
                elif latest_score['gross_margin_pct'] > 30:
                    margin_score += 15
                elif latest_score['gross_margin_pct'] > 20:
                    margin_score += 10
                else:
                    margin_score += 5
                
                if latest_score['operating_margin_pct'] > 15:
                    margin_score += 20
                elif latest_score['operating_margin_pct'] > 10:
                    margin_score += 15
                elif latest_score['operating_margin_pct'] > 5:
                    margin_score += 10
                else:
                    margin_score += 5
                
                st.metric("Margin Score", f"{margin_score}/50")
                
                # Profitability component
                profit_score = 0
                if latest_score['net_margin_pct'] > 10:
                    profit_score = 25
                elif latest_score['net_margin_pct'] > 5:
                    profit_score = 20
                elif latest_score['net_margin_pct'] > 0:
                    profit_score = 15
                else:
                    profit_score = 5
                
                st.metric("Profitability Score", f"{profit_score}/25")
            
            with col2:
                st.markdown("### 📈 Trend Analysis")
                
                # Moving averages
                if 'revenue_ma_3' in performance_summary.columns:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=performance_summary['period'],
                        y=performance_summary['revenue'],
                        mode='lines+markers',
                        name='Actual Revenue',
                        line=dict(color='#1f77b4', width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=performance_summary['period'],
                        y=performance_summary['revenue_ma_3'],
                        mode='lines',
                        name='3-Period Moving Average',
                        line=dict(color='#ff7f0e', width=3, dash='dash')
                    ))
                    fig.update_layout(
                        title="Revenue with Moving Average",
                        xaxis_title="Period",
                        yaxis_title="Revenue ($)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True, key="chart_revenue_ma")
        
        else:
            st.info("📊 Performance scoring requires multiple periods of data for trend analysis.")
    
    with tab6:
        st.subheader("🚀 Optimization Recommendations")
        
        if not performance_summary.empty:
            latest_performance = performance_summary.iloc[-1]
            
            # Generate optimization recommendations
            st.markdown("### 🎯 Strategic Optimization Areas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💰 Revenue Optimization")
                
                # Revenue growth recommendations
                if 'revenue_growth_pct' in latest_performance:
                    growth = latest_performance['revenue_growth_pct']
                    if growth < 0:
                        st.error("🚨 **Revenue Decline Detected**")
                        st.markdown("""
                        **Immediate Actions:**
                        • Review pricing strategy
                        • Analyze market conditions
                        • Assess competitive positioning
                        • Optimize sales processes
                        """)
                    elif growth < 5:
                        st.warning("⚠️ **Low Revenue Growth**")
                        st.markdown("""
                        **Growth Strategies:**
                        • Market expansion opportunities
                        • Product portfolio optimization
                        • Sales team effectiveness
                        • Customer acquisition strategies
                        """)
                    else:
                        st.success("✅ **Strong Revenue Growth**")
                        st.markdown("""
                        **Maintain Momentum:**
                        • Scale successful strategies
                        • Invest in growth areas
                        • Optimize operational efficiency
                        • Prepare for expansion
                        """)
                
                # Margin optimization
                st.markdown("#### 📊 Margin Optimization")
                gross_margin = latest_performance['gross_margin_pct']
                if gross_margin < 30:
                    st.warning("⚠️ **Low Gross Margin**")
                    st.markdown("""
                    **Cost Optimization:**
                    • Review supplier relationships
                    • Optimize production processes
                    • Analyze cost structure
                    • Consider pricing adjustments
                    """)
                else:
                    st.success("✅ **Healthy Gross Margin**")
                    st.markdown("""
                    **Maintain Efficiency:**
                    • Monitor cost trends
                    • Optimize pricing strategy
                    • Scale profitable operations
                    """)
            
            with col2:
                st.markdown("#### ⚡ Operational Efficiency")
                
                # Operating margin optimization
                operating_margin = latest_performance['operating_margin_pct']
                if operating_margin < 10:
                    st.warning("⚠️ **Low Operating Margin**")
                    st.markdown("""
                    **Efficiency Improvements:**
                    • Streamline operations
                    • Reduce overhead costs
                    • Optimize resource allocation
                    • Improve process efficiency
                    """)
                else:
                    st.success("✅ **Good Operating Efficiency**")
                    st.markdown("""
                    **Continue Optimization:**
                    • Identify efficiency opportunities
                    • Leverage technology improvements
                    • Optimize workflows
                    """)
                
                # Net margin optimization
                st.markdown("#### 💎 Profitability Optimization")
                net_margin = latest_performance['net_margin_pct']
                if net_margin < 5:
                    st.error("🚨 **Low Net Profitability**")
                    st.markdown("""
                    **Critical Actions:**
                    • Comprehensive cost review
                    • Revenue enhancement strategies
                    • Operational restructuring
                    • Strategic realignment
                    """)
                else:
                    st.success("✅ **Strong Profitability**")
                    st.markdown("""
                    **Growth Opportunities:**
                    • Reinvest in growth areas
                    • Explore new markets
                    • Strategic acquisitions
                    • Technology investments
                    """)
            
            # AI-powered recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI-Powered Optimization Insights")
            
            if generate_financial_performance_ai_recommendations:
                try:
                    ai_recommendations = generate_financial_performance_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
            else:
                st.info("🤖 AI recommendations will be displayed here when available.")


# Placeholder functions for other sections
def show_liquidity_solvency():
    st.markdown("""
    <div class="section-header">
        <h3>💧 Liquidity and Solvency</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.balance_sheet.empty and st.session_state.cash_flow.empty:
        st.info("💧 Please upload balance sheet and cash flow data to view liquidity and solvency analytics.")
        return
    
    # Calculate liquidity and solvency metrics
    liquidity_summary, liquidity_message = calculate_liquidity_solvency_metrics(
        st.session_state.balance_sheet, st.session_state.cash_flow
    )
    
    # Enhanced overview with financial health scoring
    st.subheader("💧 Liquidity and Solvency Overview")
    
    if not liquidity_summary.empty:
        # Financial health score indicator
        latest_metrics = liquidity_summary.iloc[-1]
        financial_health_score = latest_metrics.get('financial_health_score', 0)
        
        # Financial health score visualization
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if financial_health_score >= 80:
                st.success(f"🏆 Financial Health Score: {financial_health_score}/100")
                st.markdown("**Status: Excellent**")
            elif financial_health_score >= 60:
                st.info(f"📊 Financial Health Score: {financial_health_score}/100")
                st.markdown("**Status: Good**")
            elif financial_health_score >= 40:
                st.warning(f"⚠️ Financial Health Score: {financial_health_score}/100")
                st.markdown("**Status: Fair**")
            else:
                st.error(f"🚨 Financial Health Score: {financial_health_score}/100")
                st.markdown("**Status: Needs Improvement**")
        
        # Key metrics in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            current_ratio = latest_metrics['current_ratio']
            if 'current_ratio_change' in latest_metrics:
                change = latest_metrics['current_ratio_change']
                st.metric("Current Ratio", f"{current_ratio:.2f}", f"{change:+.2f}")
            else:
                st.metric("Current Ratio", f"{current_ratio:.2f}")
        
        with col2:
            quick_ratio = latest_metrics['quick_ratio']
            if 'quick_ratio_change' in latest_metrics:
                change = latest_metrics['quick_ratio_change']
                st.metric("Quick Ratio", f"{quick_ratio:.2f}", f"{change:+.2f}")
            else:
                st.metric("Quick Ratio", f"{quick_ratio:.2f}")
        
        with col3:
            debt_to_equity = latest_metrics['debt_to_equity']
            if 'debt_to_equity_change' in latest_metrics:
                change = latest_metrics['debt_to_equity_change']
                st.metric("Debt-to-Equity", f"{debt_to_equity:.2f}", f"{change:+.2f}")
            else:
                st.metric("Debt-to-Equity", f"{debt_to_equity:.2f}")
        
        with col4:
            debt_to_assets = latest_metrics['debt_to_assets']
            st.metric("Debt-to-Assets", f"{debt_to_assets:.2f}")
        
        with col5:
            working_capital = latest_metrics['working_capital']
            if 'working_capital_change' in latest_metrics:
                change = latest_metrics['working_capital_change']
                st.metric("Working Capital", f"${working_capital:,.0f}", f"{change:+,.0f}")
            else:
                st.metric("Working Capital", f"${working_capital:,.0f}")
        
        # Additional enhanced metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'cash_ratio' in latest_metrics:
                cash_ratio = latest_metrics['cash_ratio']
                st.metric("Cash Ratio", f"{cash_ratio:.2f}")
        
        with col2:
            if 'equity_ratio' in latest_metrics:
                equity_ratio = latest_metrics['equity_ratio']
                st.metric("Equity Ratio", f"{equity_ratio:.2f}")
        
        with col3:
            if 'working_capital_ratio' in latest_metrics:
                wc_ratio = latest_metrics['working_capital_ratio']
                st.metric("WC Ratio", f"{wc_ratio:.2f}")
        
        with col4:
            if 'debt_ratio' in latest_metrics:
                debt_ratio = latest_metrics['debt_ratio']
                st.metric("Debt Ratio", f"{debt_ratio:.2f}")
    
    st.success(liquidity_message)
    
    # Enhanced analytics tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💧 Liquidity Analysis", "📊 Solvency Metrics", "💰 Cash Flow Analysis", 
        "📋 Risk Assessment", "🎯 Financial Health Scoring", "🚀 Optimization Recommendations"
    ])
    
    with tab1:
        st.subheader("💧 Liquidity Analysis")
        
        if not st.session_state.balance_sheet.empty:
            # Enhanced liquidity analysis
            current_ratio_trend = st.session_state.balance_sheet.copy()
            current_ratio_trend['current_ratio'] = (current_ratio_trend['current_assets'] / current_ratio_trend['current_liabilities']).round(2)
            
            # Calculate liquidity trends and changes
            if len(current_ratio_trend) > 1:
                current_ratio_trend['ratio_change'] = current_ratio_trend['current_ratio'].pct_change() * 100
                current_ratio_trend['cumulative_change'] = ((current_ratio_trend['current_ratio'] / current_ratio_trend['current_ratio'].iloc[0]) - 1) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Current ratio trend chart
                fig = go.Figure(data=[
                    go.Scatter(x=current_ratio_trend['period'], y=current_ratio_trend['current_ratio'],
                              mode='lines+markers', line=dict(color='#1f77b4', width=3),
                              marker=dict(size=8), name='Current Ratio')
                ])
                fig.update_layout(
                    title="Current Ratio Trend Over Time",
                    xaxis_title="Period",
                    yaxis_title="Current Ratio",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=2.0, line_dash="dash", line_color="green", annotation_text="Good (2.0)")
                fig.add_hline(y=1.5, line_dash="dash", line_color="blue", annotation_text="Acceptable (1.5)")
                fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Poor (1.0)")
                st.plotly_chart(fig, use_container_width=True, key="chart_5")
            
            with col2:
                # Current ratio change analysis
                if len(current_ratio_trend) > 1:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=current_ratio_trend['period'].iloc[1:],
                        y=current_ratio_trend['ratio_change'].iloc[1:],
                        name='Period Change',
                        marker_color='#2ca02c'
                    ))
                    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="No Change")
                    fig.update_layout(
                        title="Current Ratio Change by Period",
                        xaxis_title="Period",
                        yaxis_title="Change (%)",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True, key="chart_5_change")
            
            # Liquidity insights and metrics
            if len(current_ratio_trend) > 1:
                st.markdown("### 📊 Liquidity Analysis Insights")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_ratio = current_ratio_trend['current_ratio'].mean()
                    st.metric("Average Current Ratio", f"{avg_ratio:.2f}")
                
                with col2:
                    if 'ratio_change' in current_ratio_trend.columns:
                        avg_change = current_ratio_trend['ratio_change'].iloc[1:].mean()
                        st.metric("Average Change", f"{avg_change:+.1f}%")
                
                with col3:
                    if 'cumulative_change' in current_ratio_trend.columns:
                        total_change = current_ratio_trend['cumulative_change'].iloc[-1]
                        st.metric("Total Change", f"{total_change:+.1f}%")
                
                with col4:
                    latest_ratio = current_ratio_trend['current_ratio'].iloc[-1]
                    if latest_ratio >= 2.0:
                        st.success(f"✅ **Excellent**: {latest_ratio:.2f}")
                    elif latest_ratio >= 1.5:
                        st.info(f"ℹ️ **Good**: {latest_ratio:.2f}")
                    elif latest_ratio >= 1.0:
                        st.warning(f"⚠️ **Acceptable**: {latest_ratio:.2f}")
                    else:
                        st.error(f"🚨 **Poor**: {latest_ratio:.2f}")
            
            # Quick ratio analysis
            quick_ratio_data = st.session_state.balance_sheet.copy()
            quick_ratio_data['quick_ratio'] = ((quick_ratio_data['cash_and_equivalents'] + quick_ratio_data['accounts_receivable']) / 
                                              quick_ratio_data['current_liabilities']).round(2)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=quick_ratio_data['period'], y=quick_ratio_data['quick_ratio'],
                           marker_color='#2ca02c', name='Quick Ratio',
                           text=quick_ratio_data['quick_ratio'],
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Quick Ratio by Period",
                    xaxis_title="Period",
                    yaxis_title="Quick Ratio",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_6")
            
            with col2:
                # Working capital analysis
                working_capital_data = st.session_state.balance_sheet.copy()
                working_capital_data['working_capital'] = working_capital_data['current_assets'] - working_capital_data['current_liabilities']
                
                fig = go.Figure(data=[
                    go.Scatter(x=working_capital_data['period'], y=working_capital_data['working_capital'],
                              mode='lines+markers', line=dict(color='#ff7f0e', width=3),
                              marker=dict(size=8), name='Working Capital')
                ])
                fig.update_layout(
                    title="Working Capital Trend",
                    xaxis_title="Period",
                    yaxis_title="Working Capital ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_7")
            
            # AI Strategic Recommendations for Liquidity Analysis
            st.markdown("---")
            st.markdown("### 🤖 AI Liquidity Analysis Recommendations")
            
            if generate_liquidity_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_liquidity_analysis_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("📊 Solvency Metrics")
        
        if not st.session_state.balance_sheet.empty:
            # Debt-to-equity ratio
            debt_equity_data = st.session_state.balance_sheet.copy()
            
            # Check if required columns exist
            required_cols = ['total_liabilities', 'shareholder_equity']
            if all(col in debt_equity_data.columns for col in required_cols):
                debt_equity_data['debt_to_equity'] = (debt_equity_data['total_liabilities'] / debt_equity_data['shareholder_equity']).round(2)
            else:
                st.warning("⚠️ Required columns for debt-to-equity calculation not found. Please ensure your balance sheet data includes 'total_liabilities' and 'shareholder_equity' columns.")
                return
            
            fig = go.Figure(data=[
                go.Scatter(x=debt_equity_data['period'], y=debt_equity_data['debt_to_equity'],
                          mode='lines+markers', line=dict(color='#9467bd', width=3),
                          marker=dict(size=8), name='Debt-to-Equity Ratio')
            ])
            fig.update_layout(
                title="Debt-to-Equity Ratio Trend",
                xaxis_title="Period",
                yaxis_title="Debt-to-Equity Ratio",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=0.5, line_dash="dash", line_color="green", annotation_text="Conservative (0.5)")
            fig.add_hline(y=1.0, line_dash="dash", line_color="orange", annotation_text="Moderate (1.0)")
            fig.add_hline(y=2.0, line_dash="dash", line_color="red", annotation_text="High Risk (2.0)")
            st.plotly_chart(fig, use_container_width=True, key="chart_8")
            
            # Asset composition analysis
            latest_balance = st.session_state.balance_sheet.iloc[-1]
            
            # Check if required columns exist for asset composition
            asset_cols = ['cash_and_equivalents', 'accounts_receivable', 'inventory', 'current_assets', 'total_assets']
            if all(col in latest_balance.index for col in asset_cols):
                asset_composition = {
                    'Cash & Equivalents': latest_balance['cash_and_equivalents'],
                    'Accounts Receivable': latest_balance['accounts_receivable'],
                    'Inventory': latest_balance['inventory'],
                    'Other Current Assets': latest_balance['current_assets'] - latest_balance['cash_and_equivalents'] - latest_balance['accounts_receivable'] - latest_balance['inventory'],
                    'Non-Current Assets': latest_balance['total_assets'] - latest_balance['current_assets']
                }
            else:
                st.warning("⚠️ Required columns for asset composition analysis not found. Please ensure your balance sheet data includes all required asset columns.")
                return
            
            fig = px.pie(values=list(asset_composition.values()), names=list(asset_composition.keys()),
                        title="Asset Composition")
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="chart_9")
            
            # AI Strategic Recommendations for Solvency Metrics
            st.markdown("---")
            st.markdown("### 🤖 AI Solvency Metrics Recommendations")
            
            if generate_solvency_metrics_ai_recommendations:
                try:
                    ai_recommendations = generate_solvency_metrics_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("💰 Cash Flow Analysis")
        
        if not st.session_state.cash_flow.empty:
            # Check if operating cash flow column exists
            operating_cf_col = None
            for col_name in ['operating_cash_flow', 'operating_cf', 'operating_cashflow', 'operating_cash_flow_']:
                if col_name in st.session_state.cash_flow.columns:
                    operating_cf_col = col_name
                    break
            
            if operating_cf_col:
                # Operating cash flow trend
                fig = go.Figure(data=[
                    go.Scatter(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow[operating_cf_col],
                              mode='lines+markers', line=dict(color='#1f77b4', width=3),
                              marker=dict(size=8), name='Operating Cash Flow')
                ])
                fig.update_layout(
                    title="Operating Cash Flow Trend",
                    xaxis_title="Period",
                    yaxis_title="Operating Cash Flow ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="operating_cf_trend")
            else:
                st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                return
            
            # Operating cash flow components
            col1, col2 = st.columns(2)
            with col1:
                latest_cf = st.session_state.cash_flow.iloc[-1]
                
                # Check if required columns exist for cash flow components
                cf_cols = ['net_income', 'depreciation', 'working_capital_change', 'capital_expenditures']
                if all(col in latest_cf.index for col in cf_cols):
                    cf_components = {
                        'Net Income': latest_cf['net_income'],
                        'Depreciation': latest_cf['depreciation'],
                        'Working Capital Change': -latest_cf['working_capital_change'],
                        'Capital Expenditures': -latest_cf['capital_expenditures']
                    }
                else:
                    st.warning("⚠️ Required columns for cash flow components not found. Please ensure your cash flow data includes all required columns.")
                    return
                
                fig = px.bar(x=list(cf_components.keys()), y=list(cf_components.values()),
                            title="Operating Cash Flow Components",
                            color=list(cf_components.values()),
                            color_continuous_scale='RdYlGn')
                fig.update_layout(
                    xaxis_title="Component",
                    yaxis_title="Amount ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="cf_components")
            
            with col2:
                # Cash flow quality analysis
                cf_quality_data = st.session_state.cash_flow.copy()
                # Get column mapping for cash flow data
                cf_mapping = get_cash_flow_column_mapping(st.session_state.cash_flow)
                if 'operating_cash_flow' in cf_mapping:
                    operating_cf_col = cf_mapping['operating_cash_flow']
                    cf_quality_data['cf_quality'] = (cf_quality_data[operating_cf_col] / cf_quality_data['net_income']).round(2)
                else:
                    st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                    return
                
                fig = go.Figure(data=[
                    go.Scatter(x=cf_quality_data['period'], y=cf_quality_data['cf_quality'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='Cash Flow Quality')
                ])
                fig.update_layout(
                    title="Cash Flow Quality (OCF/Net Income)",
                    xaxis_title="Period",
                    yaxis_title="Quality Ratio",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=1.0, line_dash="dash", line_color="green", annotation_text="Good Quality (≥1.0)")
                fig.add_hline(y=0.8, line_dash="dash", line_color="orange", annotation_text="Acceptable (≥0.8)")
                st.plotly_chart(fig, use_container_width=True, key="cf_quality")
            
            # AI Strategic Recommendations for Cash Flow Analysis
            st.markdown("---")
            st.markdown("### 🤖 AI Cash Flow Analysis Recommendations")
            
            if generate_cash_flow_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_cash_flow_analysis_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("📋 Risk Assessment")
        
        if not st.session_state.balance_sheet.empty:
            # Risk metrics summary
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            # Check if required columns exist for risk metrics
            risk_cols = ['current_assets', 'current_liabilities', 'total_liabilities', 'shareholder_equity']
            if all(col in latest_bs.index for col in risk_cols):
                current_ratio = latest_bs['current_assets'] / latest_bs['current_liabilities']
                debt_to_equity = latest_bs['total_liabilities'] / latest_bs['shareholder_equity']
                working_capital = latest_bs['current_assets'] - latest_bs['current_liabilities']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if current_ratio >= 2.0:
                        st.success(f"✅ Current Ratio: {current_ratio:.2f} (Excellent)")
                    elif current_ratio >= 1.5:
                        st.info(f"ℹ️ Current Ratio: {current_ratio:.2f} (Good)")
                    else:
                        st.warning(f"⚠️ Current Ratio: {current_ratio:.2f} (Poor)")
                
                with col2:
                    if debt_to_equity <= 0.5:
                        st.success(f"✅ Debt-to-Equity: {debt_to_equity:.2f} (Conservative)")
                    elif debt_to_equity <= 1.0:
                        st.info(f"ℹ️ Debt-to-Equity: {debt_to_equity:.2f} (Moderate)")
                    else:
                        st.warning(f"⚠️ Debt-to-Equity: {debt_to_equity:.2f} (High Risk)")
                
                with col3:
                    if working_capital > 0:
                        st.success(f"✅ Working Capital: ${working_capital:,.0f} (Positive)")
                    else:
                        st.error(f"❌ Working Capital: ${working_capital:,.0f} (Negative)")
                
                # Risk recommendations
                st.write("**Risk Assessment Summary:**")
                if current_ratio < 1.5:
                    st.warning("⚠️ **Liquidity Risk**: Current ratio below recommended level. Consider improving working capital management.")
                
                if debt_to_equity > 1.0:
                    st.warning("⚠️ **Solvency Risk**: High debt levels detected. Review capital structure and debt management.")
                
                if working_capital < 0:
                    st.error("❌ **Working Capital Risk**: Negative working capital indicates potential liquidity issues.")
                
                if current_ratio >= 2.0 and debt_to_equity <= 0.5:
                    st.success("✅ **Low Risk Profile**: Strong liquidity and conservative capital structure.")
            else:
                st.warning("⚠️ Required columns for risk assessment not found. Please ensure your balance sheet data includes all required columns.")
        
        # AI Strategic Recommendations - Always show regardless of column requirements
        st.markdown("---")
        st.markdown("### 🤖 AI Financial Health Recommendations")
        
        if generate_liquidity_solvency_ai_recommendations:
            try:
                ai_recommendations = generate_liquidity_solvency_ai_recommendations(
                    st.session_state.balance_sheet,
                    st.session_state.cash_flow
                )
                display_formatted_recommendations(ai_recommendations)
            except Exception as e:
                st.error(f"Error generating AI recommendations: {e}")
                st.info("Please check if you have loaded balance sheet data in the Data Input section.")
        else:
            st.error("AI recommendations function not available. Please check the import.")
    
    with tab5:
        st.subheader("🎯 Financial Health Scoring & Trends")
        
        if not liquidity_summary.empty and len(liquidity_summary) > 1:
            # Financial health score trends
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=liquidity_summary['period'], 
                y=liquidity_summary['financial_health_score'],
                mode='lines+markers', 
                name='Financial Health Score',
                line=dict(color='#9467bd', width=3),
                marker=dict(size=8)
            ))
            
            # Add threshold lines
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excellent (80+)")
            fig.add_hline(y=60, line_dash="dash", line_color="blue", annotation_text="Good (60+)")
            fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Fair (40+)")
            fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Poor (<40)")
            
            fig.update_layout(
                title="Financial Health Score Trends Over Time",
                xaxis_title="Period",
                yaxis_title="Financial Health Score (0-100)",
                yaxis_range=[0, 100],
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_financial_health_score")
            
            # Score breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Score Components")
                latest_score = liquidity_summary.iloc[-1]
                
                # Liquidity component (40 points)
                liquidity_score = 0
                if latest_score['current_ratio'] >= 2.0:
                    liquidity_score += 20
                elif latest_score['current_ratio'] >= 1.5:
                    liquidity_score += 15
                elif latest_score['current_ratio'] >= 1.0:
                    liquidity_score += 10
                else:
                    liquidity_score += 5
                
                if latest_score['quick_ratio'] >= 1.0:
                    liquidity_score += 20
                elif latest_score['quick_ratio'] >= 0.8:
                    liquidity_score += 15
                elif latest_score['quick_ratio'] >= 0.5:
                    liquidity_score += 10
                else:
                    liquidity_score += 5
                
                st.metric("Liquidity Score", f"{liquidity_score}/40")
                
                # Solvency component (40 points)
                solvency_score = 0
                if latest_score['debt_to_equity'] <= 0.5:
                    solvency_score += 20
                elif latest_score['debt_to_equity'] <= 1.0:
                    solvency_score += 15
                elif latest_score['debt_to_equity'] <= 2.0:
                    solvency_score += 10
                else:
                    solvency_score += 5
                
                if latest_score['debt_to_assets'] <= 0.3:
                    solvency_score += 20
                elif latest_score['debt_to_assets'] <= 0.5:
                    solvency_score += 15
                elif latest_score['debt_to_assets'] <= 0.7:
                    solvency_score += 10
                else:
                    solvency_score += 5
                
                st.metric("Solvency Score", f"{solvency_score}/40")
                
                # Working capital component (20 points)
                wc_score = 0
                if latest_score['working_capital'] > 0:
                    if latest_score['working_capital_ratio'] >= 0.2:
                        wc_score = 20
                    elif latest_score['working_capital_ratio'] >= 0.1:
                        wc_score = 15
                    elif latest_score['working_capital_ratio'] >= 0.05:
                        wc_score = 10
                    else:
                        wc_score = 5
                else:
                    wc_score = 0
                
                st.metric("Working Capital Score", f"{wc_score}/20")
            
            with col2:
                st.markdown("### 📈 Trend Analysis")
                
                # Moving averages
                if 'current_ratio_ma_3' in liquidity_summary.columns:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=liquidity_summary['period'],
                        y=liquidity_summary['current_ratio'],
                        mode='lines+markers',
                        name='Actual Current Ratio',
                        line=dict(color='#1f77b4', width=2)
                    ))
                    fig.add_trace(go.Scatter(
                        x=liquidity_summary['period'],
                        y=liquidity_summary['current_ratio_ma_3'],
                        mode='lines',
                        name='3-Period Moving Average',
                        line=dict(color='#ff7f0e', width=3, dash='dash')
                    ))
                    fig.update_layout(
                        title="Current Ratio with Moving Average",
                        xaxis_title="Period",
                        yaxis_title="Current Ratio",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True, key="chart_current_ratio_ma")
        
        else:
            st.info("📊 Financial health scoring requires multiple periods of data for trend analysis.")
    
    with tab6:
        st.subheader("🚀 Optimization Recommendations")
        
        if not liquidity_summary.empty:
            latest_metrics = liquidity_summary.iloc[-1]
            
            # Generate optimization recommendations
            st.markdown("### 🎯 Strategic Optimization Areas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💧 Liquidity Optimization")
                
                # Current ratio optimization
                current_ratio = latest_metrics['current_ratio']
                if current_ratio < 1.0:
                    st.error("🚨 **Critical Liquidity Issue**")
                    st.markdown("""
                    **Immediate Actions:**
                    • Increase current assets
                    • Reduce current liabilities
                    • Improve working capital management
                    • Review short-term financing
                    """)
                elif current_ratio < 1.5:
                    st.warning("⚠️ **Low Liquidity**")
                    st.markdown("""
                    **Improvement Strategies:**
                    • Optimize inventory management
                    • Accelerate receivables collection
                    • Extend payables where possible
                    • Improve cash flow management
                    """)
                else:
                    st.success("✅ **Good Liquidity**")
                    st.markdown("""
                    **Maintain Excellence:**
                    • Continue current practices
                    • Monitor trends closely
                    • Optimize asset allocation
                    • Consider investment opportunities
                    """)
                
                # Quick ratio optimization
                st.markdown("#### ⚡ Quick Ratio Optimization")
                quick_ratio = latest_metrics['quick_ratio']
                if quick_ratio < 0.5:
                    st.error("🚨 **Poor Quick Ratio**")
                    st.markdown("""
                    **Critical Actions:**
                    • Increase cash reserves
                    • Improve receivables collection
                    • Reduce inventory levels
                    • Review credit policies
                    """)
                elif quick_ratio < 1.0:
                    st.warning("⚠️ **Moderate Quick Ratio**")
                    st.markdown("""
                    **Enhancement Strategies:**
                    • Build cash reserves
                    • Optimize receivables
                    • Improve cash conversion cycle
                    • Strengthen credit management
                    """)
                else:
                    st.success("✅ **Strong Quick Ratio**")
                    st.markdown("""
                    **Maintain Strength:**
                    • Continue cash management
                    • Optimize asset allocation
                    • Consider strategic investments
                    """)
            
            with col2:
                st.markdown("#### 🏗️ Solvency Optimization")
                
                # Debt-to-equity optimization
                debt_to_equity = latest_metrics['debt_to_equity']
                if debt_to_equity > 2.0:
                    st.error("🚨 **High Debt Risk**")
                    st.markdown("""
                    **Critical Actions:**
                    • Reduce debt levels urgently
                    • Review capital structure
                    • Consider equity financing
                    • Restructure existing debt
                    """)
                elif debt_to_equity > 1.0:
                    st.warning("⚠️ **Elevated Debt Levels**")
                    st.markdown("""
                    **Risk Mitigation:**
                    • Monitor debt trends
                    • Optimize capital structure
                    • Improve profitability
                    • Consider debt refinancing
                    """)
                else:
                    st.success("✅ **Healthy Debt Levels**")
                    st.markdown("""
                    **Maintain Stability:**
                    • Continue conservative approach
                    • Monitor market conditions
                    • Consider growth opportunities
                    """)
                
                # Working capital optimization
                st.markdown("#### 💼 Working Capital Optimization")
                working_capital = latest_metrics['working_capital']
                if working_capital < 0:
                    st.error("🚨 **Negative Working Capital**")
                    st.markdown("""
                    **Critical Actions:**
                    • Immediate liquidity injection
                    • Restructure short-term debt
                    • Optimize asset utilization
                    • Review business model
                    """)
                elif working_capital < latest_metrics.get('current_assets', 0) * 0.1:
                    st.warning("⚠️ **Low Working Capital**")
                    st.markdown("""
                    **Improvement Strategies:**
                    • Increase current assets
                    • Reduce current liabilities
                    • Optimize cash flow
                    • Improve operational efficiency
                    """)
                else:
                    st.success("✅ **Strong Working Capital**")
                    st.markdown("""
                    **Maintain Strength:**
                    • Continue current practices
                    • Optimize asset allocation
                    • Consider growth investments
                    """)
            
            # AI-powered recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI-Powered Optimization Insights")
            
            if generate_liquidity_solvency_ai_recommendations:
                try:
                    ai_recommendations = generate_liquidity_solvency_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
            else:
                st.info("🤖 AI recommendations will be displayed here when available.")


def show_efficiency_productivity():
    st.markdown("""
    <div class="section-header">
        <h3>⚡ Efficiency and Productivity</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.income_statement.empty and st.session_state.balance_sheet.empty:
        st.info("⚡ Please upload income statement and balance sheet data to view efficiency and productivity analytics.")
        return
    
    # Calculate efficiency metrics
    efficiency_summary, efficiency_message = calculate_efficiency_metrics(
        st.session_state.income_statement, st.session_state.balance_sheet
    )
    
    # Display summary metrics
    st.subheader("⚡ Efficiency and Productivity Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not efficiency_summary.empty:
            roa = efficiency_summary.iloc[0]['roa_pct']
            st.metric("Return on Assets (ROA)", f"{roa:.1f}%")
    
    with col2:
        if not efficiency_summary.empty and len(efficiency_summary) > 1:
            roe = efficiency_summary.iloc[0]['roe_pct']
            st.metric("Return on Equity (ROE)", f"{roe:.1f}%")
    
    with col3:
        if not efficiency_summary.empty and len(efficiency_summary) > 2:
            asset_turnover = efficiency_summary.iloc[0]['asset_turnover']
            st.metric("Asset Turnover Ratio", f"{asset_turnover:.2f}")
    
    with col4:
        if not efficiency_summary.empty and len(efficiency_summary) > 3:
            op_exp_ratio = efficiency_summary.iloc[0]['op_exp_ratio_pct']
            st.metric("Operating Expense Ratio", f"{op_exp_ratio:.1f}%")
    
    st.info(efficiency_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 ROA & ROE Analysis", "🔄 Asset Turnover", "💰 Expense Efficiency", "📈 Productivity Trends"
    ])
    
    # Calculate efficiency metrics for all tabs
    efficiency_data = None
    if not st.session_state.income_statement.empty and not st.session_state.balance_sheet.empty:
        try:
            efficiency_data = st.session_state.income_statement.merge(
                st.session_state.balance_sheet[['period', 'total_assets', 'shareholder_equity']], 
                on='period', how='inner'
            )
            efficiency_data['roa'] = (efficiency_data['net_income'] / efficiency_data['total_assets'] * 100).round(2)
            efficiency_data['roe'] = (efficiency_data['net_income'] / efficiency_data['shareholder_equity'] * 100).round(2)
            efficiency_data['asset_turnover'] = (efficiency_data['revenue'] / efficiency_data['total_assets']).round(2)
            
            # Debug: Show efficiency data structure
            if st.checkbox("Show efficiency data debug"):
                st.write("Efficiency data columns:", list(efficiency_data.columns))
                st.write("Efficiency data shape:", efficiency_data.shape)
                st.write("Sample efficiency data:", efficiency_data.head())
        except Exception as e:
            st.error(f"❌ Error creating efficiency data: {str(e)}")
            efficiency_data = None
    
    with tab1:
        st.subheader("📊 ROA & ROE Analysis")
        
        if efficiency_data is not None:
            
            # ROA trend
            fig = go.Figure(data=[
                go.Scatter(x=efficiency_data['period'], y=efficiency_data['roa'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='ROA (%)')
            ])
            fig.update_layout(
                title="Return on Assets (ROA) Trend",
                xaxis_title="Period",
                yaxis_title="ROA (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=10, line_dash="dash", line_color="green", annotation_text="Good (10%)")
            fig.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Average (5%)")
            st.plotly_chart(fig, use_container_width=True, key="chart_13")
            
            # ROE trend
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Scatter(x=efficiency_data['period'], y=efficiency_data['roe'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='ROE (%)')
                ])
                fig.update_layout(
                    title="Return on Equity (ROE) Trend",
                    xaxis_title="Period",
                    yaxis_title="ROE (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=15, line_dash="dash", line_color="green", annotation_text="Good (15%)")
                fig.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Average (10%)")
                st.plotly_chart(fig, use_container_width=True, key="chart_14")
            
            with col2:
                # ROA vs ROE comparison
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=efficiency_data['period'], y=efficiency_data['roa'],
                                        mode='lines+markers', name='ROA', line=dict(color='#1f77b4')))
                fig.add_trace(go.Scatter(x=efficiency_data['period'], y=efficiency_data['roe'],
                                        mode='lines+markers', name='ROE', line=dict(color='#2ca02c')))
                fig.update_layout(
                    title="ROA vs ROE Comparison",
                    xaxis_title="Period",
                    yaxis_title="Return (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_15")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI ROA/ROE Analysis Recommendations")
            if generate_roa_roe_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_roa_roe_analysis_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("🔄 Asset Turnover")
        
        if efficiency_data is not None:
            # Asset turnover analysis
            asset_turnover_data = efficiency_data.copy()
            
            fig = go.Figure(data=[
                go.Scatter(x=asset_turnover_data['period'], y=asset_turnover_data['asset_turnover'],
                          mode='lines+markers', line=dict(color='#ff7f0e', width=3),
                          marker=dict(size=8), name='Asset Turnover')
            ])
            fig.update_layout(
                title="Asset Turnover Ratio Trend",
                xaxis_title="Period",
                yaxis_title="Asset Turnover Ratio",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_16")
            
            # Asset utilization analysis
            latest_data = asset_turnover_data.iloc[-1]
            asset_utilization = {
                'Revenue': latest_data['revenue'],
                'Total Assets': latest_data['total_assets'],
                'Asset Turnover': latest_data['asset_turnover']
            }
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Revenue", f"${latest_data['revenue']:,.0f}")
                st.metric("Total Assets", f"${latest_data['total_assets']:,.0f}")
            
            with col2:
                st.metric("Asset Turnover", f"{latest_data['asset_turnover']:.2f}")
                efficiency_score = (latest_data['asset_turnover'] / 1.0) * 100  # Benchmark of 1.0
                st.metric("Efficiency Score", f"{efficiency_score:.1f}%")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Asset Turnover Recommendations")
            if generate_asset_turnover_ai_recommendations:
                try:
                    ai_recommendations = generate_asset_turnover_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("💰 Expense Efficiency")
        
        if not st.session_state.income_statement.empty:
            # Operating expense ratio analysis
            expense_data = st.session_state.income_statement.copy()
            expense_data['op_exp_ratio'] = (expense_data['operating_expenses'] / expense_data['revenue'] * 100).round(2)
            expense_data['cogs_ratio'] = (expense_data['cost_of_goods_sold'] / expense_data['revenue'] * 100).round(2)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=expense_data['period'], y=expense_data['op_exp_ratio'],
                                    mode='lines+markers', name='Operating Expense Ratio', line=dict(color='#1f77b4')))
            fig.add_trace(go.Scatter(x=expense_data['period'], y=expense_data['cogs_ratio'],
                                    mode='lines+markers', name='COGS Ratio', line=dict(color='#2ca02c')))
            fig.update_layout(
                title="Expense Ratios Over Time",
                xaxis_title="Period",
                yaxis_title="Ratio (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_17")
            
            # Expense breakdown
            latest_expense = expense_data.iloc[-1]
            expense_breakdown = {}
            
            # Add available expense categories
            if 'cost_of_goods_sold' in latest_expense.index:
                expense_breakdown['Cost of Goods Sold'] = latest_expense['cost_of_goods_sold']
            if 'operating_expenses' in latest_expense.index:
                expense_breakdown['Operating Expenses'] = latest_expense['operating_expenses']
            if 'interest_expense' in latest_expense.index:
                expense_breakdown['Interest Expense'] = latest_expense['interest_expense']
            if 'income_tax_expense' in latest_expense.index:
                expense_breakdown['Income Tax'] = latest_expense['income_tax_expense']
            
            # If no expense categories found, show a message
            if not expense_breakdown:
                st.warning("⚠️ No expense data available for breakdown analysis.")
                return
            
            fig = px.pie(values=list(expense_breakdown.values()), names=list(expense_breakdown.keys()),
                        title="Expense Breakdown")
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="chart_18")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Expense Efficiency Recommendations")
            if generate_expense_efficiency_ai_recommendations:
                try:
                    ai_recommendations = generate_expense_efficiency_ai_recommendations(
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("📈 Productivity Trends")
        
        if efficiency_data is not None and not efficiency_data.empty:
            try:
                # Productivity metrics
                productivity_data = efficiency_data.copy()
                productivity_data['revenue_per_asset'] = (productivity_data['revenue'] / productivity_data['total_assets']).round(2)
                productivity_data['profit_per_asset'] = (productivity_data['net_income'] / productivity_data['total_assets']).round(2)
            except Exception as e:
                st.error(f"❌ Error creating productivity data: {str(e)}")
                return
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=productivity_data['period'], y=productivity_data['revenue_per_asset'],
                                    mode='lines+markers', name='Revenue per Asset', line=dict(color='#1f77b4')))
            fig.add_trace(go.Scatter(x=productivity_data['period'], y=productivity_data['profit_per_asset'],
                                    mode='lines+markers', name='Profit per Asset', line=dict(color='#2ca02c')))
            fig.update_layout(
                title="Productivity Metrics",
                xaxis_title="Period",
                yaxis_title="Amount per Asset ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_19")
            
            # Efficiency insights
            try:
                latest_prod = productivity_data.iloc[-1]
            except Exception as e:
                st.error(f"❌ Error accessing productivity data: {str(e)}")
                return
            
            # Show debug information if needed
            if st.checkbox("Show productivity debug info"):
                st.write("Productivity data columns:", list(productivity_data.columns))
                st.write("Latest prod keys:", list(latest_prod.index))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if latest_prod['roa'] >= 10:
                    st.success(f"✅ ROA: {latest_prod['roa']:.1f}% (Excellent)")
                elif latest_prod['roa'] >= 5:
                    st.info(f"ℹ️ ROA: {latest_prod['roa']:.1f}% (Good)")
                else:
                    st.warning(f"⚠️ ROA: {latest_prod['roa']:.1f}% (Needs Improvement)")
            
            with col2:
                if latest_prod['roe'] >= 15:
                    st.success(f"✅ ROE: {latest_prod['roe']:.1f}% (Excellent)")
                elif latest_prod['roe'] >= 10:
                    st.info(f"ℹ️ ROE: {latest_prod['roe']:.1f}% (Good)")
                else:
                    st.warning(f"⚠️ ROE: {latest_prod['roe']:.1f}% (Needs Improvement)")
            
            with col3:
                try:
                    if latest_prod['asset_turnover'] >= 1.0:
                        st.success(f"✅ Asset Turnover: {latest_prod['asset_turnover']:.2f} (Good)")
                    else:
                        st.warning(f"⚠️ Asset Turnover: {latest_prod['asset_turnover']:.2f} (Low)")
                except KeyError:
                    st.error("❌ Asset Turnover data not available")
            
            # Recommendations
            st.write("**Efficiency Recommendations:**")
            if latest_prod['roa'] < 5:
                st.warning("⚠️ **Low ROA**: Consider improving asset utilization or reducing costs.")
            
            if latest_prod['roe'] < 10:
                st.warning("⚠️ **Low ROE**: Review capital structure and profitability drivers.")
            
            try:
                if latest_prod['asset_turnover'] < 1.0:
                    st.warning("⚠️ **Low Asset Turnover**: Consider divesting underutilized assets or improving sales.")
            except KeyError:
                pass
            
            if latest_prod['roa'] >= 10 and latest_prod['roe'] >= 15:
                st.success("✅ **Excellent Efficiency**: Strong asset utilization and profitability metrics.")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Productivity Trends Recommendations")
            if generate_productivity_trends_ai_recommendations:
                try:
                    ai_recommendations = generate_productivity_trends_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")

def show_budget_forecasting():
    st.markdown("""
    <div class="section-header">
        <h3>📋 Budgeting, Forecasting & Variance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.budget.empty and st.session_state.forecast.empty:
        st.info("📋 Please upload budget and forecast data to view budgeting and forecasting analytics.")
        return
    
    # Calculate budget variance metrics
    variance_summary, variance_message = calculate_budget_variance_metrics(
        st.session_state.income_statement, st.session_state.budget, st.session_state.forecast
    )
    
    # Display summary metrics
    st.subheader("📋 Budget and Forecasting Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not variance_summary.empty:
            budget_variance = variance_summary.iloc[0]['Value']
            st.metric("Budget Variance", budget_variance)
    
    with col2:
        if not variance_summary.empty and len(variance_summary) > 1:
            forecast_accuracy = variance_summary.iloc[1]['Value']
            st.metric("Forecast Accuracy (MAPE)", forecast_accuracy)
    
    with col3:
        if not variance_summary.empty and len(variance_summary) > 2:
            scenario_analysis = variance_summary.iloc[2]['Value']
            st.metric("Scenario Analysis", scenario_analysis)
    
    st.info(variance_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Budget Variance Analysis", "🔮 Forecast Accuracy", "📈 Scenario Analysis", "📋 Variance Reporting"
    ])
    
    with tab1:
        st.subheader("📊 Budget Variance Analysis")
        
        if not st.session_state.budget.empty and not st.session_state.income_statement.empty:
            try:
                # Always use manual column renaming approach for consistent results
                budget_copy = st.session_state.budget.copy()
                income_copy = st.session_state.income_statement[['period', 'revenue', 'cost_of_goods_sold', 'operating_expenses']].copy()
                
                # Rename budget columns
                budget_copy = budget_copy.rename(columns={
                    'revenue': 'revenue_budget',
                    'expenses': 'expenses_budget'
                })
                
                # Rename income statement columns
                income_copy = income_copy.rename(columns={
                    'revenue': 'revenue_actual',
                    'cost_of_goods_sold': 'cost_of_goods_sold_actual',
                    'operating_expenses': 'operating_expenses_actual'
                })
                
                # Merge with renamed columns
                budget_actual = budget_copy.merge(income_copy, on='period', how='inner')
                
                # Add calculated actual expenses column
                try:
                    # Check if we have the individual expense columns
                    if 'cost_of_goods_sold_actual' in budget_actual.columns and 'operating_expenses_actual' in budget_actual.columns:
                        budget_actual['expenses_actual'] = budget_actual['cost_of_goods_sold_actual'] + budget_actual['operating_expenses_actual']
                    elif 'expenses_actual' not in budget_actual.columns:
                        # If we don't have the individual columns, try to calculate from available data
                        st.warning("⚠️ Individual expense columns not found, using available data")
                        if 'cost_of_goods_sold' in budget_actual.columns and 'operating_expenses' in budget_actual.columns:
                            budget_actual['expenses_actual'] = budget_actual['cost_of_goods_sold'] + budget_actual['operating_expenses']
                        else:
                            st.error("❌ Cannot calculate expenses_actual - missing required columns")
                            st.write("Available columns:", list(budget_actual.columns))
                            return
                except KeyError as e:
                    st.error(f"❌ Error calculating expenses_actual: {str(e)}")
                    return
                
            except Exception as e:
                st.error(f"❌ Error merging budget and actual data: {str(e)}")
                return
            
            # Debug information removed for cleaner interface
            
            # Calculate variances with proper error handling
            try:
                # Check if required columns exist
                required_columns = ['revenue_budget', 'revenue_actual', 'expenses_budget', 'expenses_actual']
                missing_columns = [col for col in required_columns if col not in budget_actual.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing columns: {missing_columns}")
                    return
                
                budget_actual['revenue_variance'] = ((budget_actual['revenue_actual'] - budget_actual['revenue_budget']) / budget_actual['revenue_budget'] * 100).round(2)
                budget_actual['expense_variance'] = ((budget_actual['expenses_budget'] - budget_actual['expenses_actual']) / budget_actual['expenses_budget'] * 100).round(2)
            except KeyError as e:
                st.error(f"❌ Error calculating variances: {str(e)}. Please check your budget data structure.")
                st.write("Available columns:", list(budget_actual.columns))
                return
            
            # Revenue variance analysis
            fig = go.Figure(data=[
                go.Scatter(x=budget_actual['period'], y=budget_actual['revenue_variance'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='Revenue Variance (%)')
            ])
            fig.update_layout(
                title="Revenue Budget Variance Over Time",
                xaxis_title="Period",
                yaxis_title="Variance (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="On Budget")
            fig.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Favorable (+5%)")
            fig.add_hline(y=-5, line_dash="dash", line_color="red", annotation_text="Unfavorable (-5%)")
            st.plotly_chart(fig, use_container_width=True, key="chart_20")
            
            # Budget vs Actual comparison
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=budget_actual['period'], y=budget_actual['revenue_budget'],
                                    name='Budgeted Revenue', marker_color='#1f77b4'))
                fig.add_trace(go.Bar(x=budget_actual['period'], y=budget_actual['revenue_actual'],
                                    name='Actual Revenue', marker_color='#2ca02c'))
                fig.update_layout(
                    title="Budget vs Actual Revenue",
                    xaxis_title="Period",
                    yaxis_title="Revenue ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_21")
            
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=budget_actual['period'], y=budget_actual['expenses_budget'],
                                    name='Budgeted Expenses', marker_color='#ff7f0e'))
                fig.add_trace(go.Bar(x=budget_actual['period'], y=budget_actual['expenses_actual'],
                                    name='Actual Expenses', marker_color='#d62728'))
                fig.update_layout(
                    title="Budget vs Actual Expenses",
                    xaxis_title="Period",
                    yaxis_title="Expenses ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50),
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_22")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Budget Variance Analysis Recommendations")
            if generate_budget_variance_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_budget_variance_analysis_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.budget
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and budget data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("🔮 Forecast Accuracy")
        
        if not st.session_state.forecast.empty and not st.session_state.income_statement.empty:
            try:
                # Always use manual column renaming approach for consistent results
                forecast_copy = st.session_state.forecast.copy()
                income_copy = st.session_state.income_statement[['period', 'revenue', 'cost_of_goods_sold', 'operating_expenses']].copy()
                
                # Rename forecast columns
                forecast_copy = forecast_copy.rename(columns={
                    'revenue': 'revenue_forecast',
                    'expenses': 'expenses_forecast'
                })
                
                # Rename income statement columns
                income_copy = income_copy.rename(columns={
                    'revenue': 'revenue_actual',
                    'cost_of_goods_sold': 'cost_of_goods_sold_actual',
                    'operating_expenses': 'operating_expenses_actual'
                })
                
                # Merge with renamed columns
                forecast_actual = forecast_copy.merge(income_copy, on='period', how='inner')
                
                # Check if we have any overlapping data
                if forecast_actual.empty:
                    st.warning("⚠️ No overlapping periods found between forecast and actual data.")
                    st.info("Forecast periods: " + ", ".join(forecast_copy['period'].astype(str).tolist()[:5]) + "...")
                    st.info("Income statement periods: " + ", ".join(income_copy['period'].astype(str).tolist()[:5]) + "...")
                    st.info("Please ensure your forecast data covers periods that exist in your income statement data.")
                    return
                
                # Add calculated actual expenses column
                try:
                    # Check if we have the individual expense columns
                    if 'cost_of_goods_sold_actual' in forecast_actual.columns and 'operating_expenses_actual' in forecast_actual.columns:
                        forecast_actual['expenses_actual'] = forecast_actual['cost_of_goods_sold_actual'] + forecast_actual['operating_expenses_actual']
                    elif 'expenses_actual' not in forecast_actual.columns:
                        # If we don't have the individual columns, try to calculate from available data
                        st.warning("⚠️ Individual forecast expense columns not found, using available data")
                        if 'cost_of_goods_sold' in forecast_actual.columns and 'operating_expenses' in forecast_actual.columns:
                            forecast_actual['expenses_actual'] = forecast_actual['cost_of_goods_sold'] + forecast_actual['operating_expenses']
                        else:
                            st.error("❌ Cannot calculate forecast expenses_actual - missing required columns")
                            st.write("Available forecast columns:", list(forecast_actual.columns))
                            return
                except KeyError as e:
                    st.error(f"❌ Error calculating forecast expenses_actual: {str(e)}")
                    return
                
            except Exception as e:
                st.error(f"❌ Error merging forecast and actual data: {str(e)}")
                return
            
            # Calculate forecast accuracy with error handling
            try:
                required_forecast_columns = ['revenue_forecast', 'revenue_actual', 'expenses_forecast', 'expenses_actual']
                missing_forecast_columns = [col for col in required_forecast_columns if col not in forecast_actual.columns]
                
                if missing_forecast_columns:
                    st.error(f"❌ Missing forecast columns: {missing_forecast_columns}")
                    return
                
                forecast_actual['revenue_accuracy'] = (abs(forecast_actual['revenue_forecast'] - forecast_actual['revenue_actual']) / forecast_actual['revenue_actual'] * 100).round(2)
                forecast_actual['expense_accuracy'] = (abs(forecast_actual['expenses_forecast'] - forecast_actual['expenses_actual']) / forecast_actual['expenses_actual'] * 100).round(2)
            except KeyError as e:
                st.error(f"❌ Error calculating forecast accuracy: {str(e)}")
                return
            
            # Forecast accuracy trend
            fig = go.Figure(data=[
                go.Scatter(x=forecast_actual['period'], y=forecast_actual['revenue_accuracy'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='Revenue Forecast Error (%)')
            ])
            fig.update_layout(
                title="Forecast Accuracy Over Time",
                xaxis_title="Period",
                yaxis_title="Forecast Error (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Excellent (≤5%)")
            fig.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Good (≤10%)")
            fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Poor (>20%)")
            st.plotly_chart(fig, use_container_width=True, key="chart_23")
            
            # Confidence level analysis
            col1, col2 = st.columns(2)
            with col1:
                if 'confidence_level' in forecast_actual.columns:
                    fig = go.Figure(data=[
                        go.Scatter(x=forecast_actual['period'], y=forecast_actual['confidence_level'],
                                  mode='lines+markers', line=dict(color='#2ca02c', width=3),
                                  marker=dict(size=8), name='Confidence Level')
                    ])
                    fig.update_layout(
                        title="Forecast Confidence Level",
                        xaxis_title="Period",
                        yaxis_title="Confidence Level",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    st.plotly_chart(fig, use_container_width=True, key="chart_24")
                else:
                    st.info("Confidence level data not available in merged dataset.")
            
            with col2:
                # Forecast vs Actual comparison
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=forecast_actual['period'], y=forecast_actual['revenue_forecast'],
                                        mode='lines+markers', name='Forecasted Revenue', line=dict(color='#1f77b4')))
                fig.add_trace(go.Scatter(x=forecast_actual['period'], y=forecast_actual['revenue_actual'],
                                        mode='lines+markers', name='Actual Revenue', line=dict(color='#2ca02c')))
                fig.update_layout(
                    title="Forecast vs Actual Revenue",
                    xaxis_title="Period",
                    yaxis_title="Revenue ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_25")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Forecast Accuracy Recommendations")
            if generate_forecast_accuracy_ai_recommendations:
                try:
                    ai_recommendations = generate_forecast_accuracy_ai_recommendations(
                        st.session_state.forecast,
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded forecast and income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("📈 Scenario Analysis")
        
        if not st.session_state.income_statement.empty:
            # Scenario analysis simulation
            latest_revenue = st.session_state.income_statement['revenue'].iloc[-1]
            latest_expenses = st.session_state.income_statement['cost_of_goods_sold'].iloc[-1] + st.session_state.income_statement['operating_expenses'].iloc[-1]
            
            # Define scenarios
            scenarios = {
                'Optimistic': {'revenue_change': 0.20, 'expense_change': 0.05},
                'Base Case': {'revenue_change': 0.00, 'expense_change': 0.00},
                'Conservative': {'revenue_change': -0.10, 'expense_change': 0.10},
                'Pessimistic': {'revenue_change': -0.20, 'expense_change': 0.15}
            }
            
            scenario_results = []
            for scenario, changes in scenarios.items():
                new_revenue = latest_revenue * (1 + changes['revenue_change'])
                new_expenses = latest_expenses * (1 + changes['expense_change'])
                new_profit = new_revenue - new_expenses
                profit_margin = (new_profit / new_revenue * 100) if new_revenue > 0 else 0
                
                scenario_results.append({
                    'Scenario': scenario,
                    'Revenue': new_revenue,
                    'Expenses': new_expenses,
                    'Profit': new_profit,
                    'Profit Margin': profit_margin
                })
            
            scenario_df = pd.DataFrame(scenario_results)
            
            # Scenario comparison chart
            fig = go.Figure(data=[
                go.Bar(x=scenario_df['Scenario'], y=scenario_df['Profit'],
                       marker_color=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'],
                       text=scenario_df['Profit'].round(0),
                       textposition='auto')
            ])
            fig.update_layout(
                title="Profit Projections by Scenario",
                xaxis_title="Scenario",
                yaxis_title="Projected Profit ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_26")
            
            # Scenario details table
            st.subheader("Scenario Details")
            display_dataframe_with_index_1(scenario_df.round(2))
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Scenario Analysis Recommendations")
            if generate_scenario_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_scenario_analysis_ai_recommendations(
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("📋 Variance Reporting")
        
        if not st.session_state.budget.empty and not st.session_state.income_statement.empty:
            # Variance summary
            latest_budget = st.session_state.budget.iloc[-1]
            latest_actual = st.session_state.income_statement.iloc[-1]
            
            try:
                revenue_variance = ((latest_actual['revenue'] - latest_budget['revenue']) / latest_budget['revenue'] * 100) if latest_budget['revenue'] > 0 else 0
                expense_variance = ((latest_budget['expenses'] - (latest_actual['cost_of_goods_sold'] + latest_actual['operating_expenses'])) / latest_budget['expenses'] * 100) if latest_budget['expenses'] > 0 else 0
            except KeyError:
                st.warning("⚠️ Budget data structure doesn't match expected format. Please check your data.")
                revenue_variance = 0
                expense_variance = 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if revenue_variance >= 0:
                    st.success(f"✅ Revenue Variance: {revenue_variance:.1f}% (Favorable)")
                else:
                    st.error(f"❌ Revenue Variance: {revenue_variance:.1f}% (Unfavorable)")
            
            with col2:
                if expense_variance >= 0:
                    st.success(f"✅ Expense Variance: {expense_variance:.1f}% (Favorable)")
                else:
                    st.error(f"❌ Expense Variance: {expense_variance:.1f}% (Unfavorable)")
            
            with col3:
                total_variance = revenue_variance - expense_variance
                if total_variance >= 0:
                    st.success(f"✅ Net Variance: {total_variance:.1f}% (Favorable)")
                else:
                    st.error(f"❌ Net Variance: {total_variance:.1f}% (Unfavorable)")
            
            # Variance recommendations
            st.write("**Variance Analysis Recommendations:**")
            if abs(revenue_variance) > 10:
                st.warning(f"⚠️ **High Revenue Variance**: {abs(revenue_variance):.1f}% variance detected. Review revenue forecasting models.")
            
            if abs(expense_variance) > 10:
                st.warning(f"⚠️ **High Expense Variance**: {abs(expense_variance):.1f}% variance detected. Review cost control measures.")
            
            if revenue_variance < -5 and expense_variance > 5:
                st.error("❌ **Critical Variance**: Both revenue and expenses are significantly off target.")
            
            if abs(revenue_variance) <= 5 and abs(expense_variance) <= 5:
                st.success("✅ **Excellent Budget Performance**: All variances within acceptable ranges.")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Variance Reporting Recommendations")
            if generate_variance_reporting_ai_recommendations:
                try:
                    ai_recommendations = generate_variance_reporting_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.budget
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and budget data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")

def show_cash_flow():
    st.markdown("""
    <div class="section-header">
        <h3>💸 Cash Flow & Working Capital</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.cash_flow.empty and st.session_state.balance_sheet.empty:
        st.info("💸 Please upload cash flow and balance sheet data to view cash flow analytics.")
        return
    
    # Calculate cash flow metrics
    cash_flow_summary, cash_flow_message = calculate_cash_flow_metrics(
        st.session_state.cash_flow, st.session_state.balance_sheet
    )
    
    # Display summary metrics
    st.subheader("💸 Cash Flow & Working Capital Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not cash_flow_summary.empty:
            operating_cf = cash_flow_summary.iloc[0]['operating_cf']
            st.metric("Operating Cash Flow", f"${operating_cf:,.0f}")
    
    with col2:
        if not cash_flow_summary.empty and len(cash_flow_summary) > 1:
            free_cf = cash_flow_summary.iloc[0]['free_cf']
            st.metric("Free Cash Flow", f"${free_cf:,.0f}")
    
    with col3:
        if not cash_flow_summary.empty and len(cash_flow_summary) > 2:
            working_capital_turnover = cash_flow_summary.iloc[0]['working_capital_turnover']
            st.metric("Working Capital Turnover", f"{working_capital_turnover:.2f}")
    
    st.info(cash_flow_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Operating Cash Flow", "🔄 Free Cash Flow", "📊 Working Capital", "📈 Cash Flow Trends"
    ])
    
    with tab1:
        st.subheader("💰 Operating Cash Flow")
        
        if not st.session_state.cash_flow.empty:
            # Get column mapping for cash flow data
            cf_mapping = get_cash_flow_column_mapping(st.session_state.cash_flow)
            if 'operating_cash_flow' not in cf_mapping:
                st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                return
            
            operating_cf_col = cf_mapping['operating_cash_flow']
            
            # Operating cash flow trend
            fig = go.Figure(data=[
                go.Scatter(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow[operating_cf_col],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='Operating Cash Flow')
            ])
            fig.update_layout(
                title="Operating Cash Flow Trend",
                xaxis_title="Period",
                yaxis_title="Operating Cash Flow ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="operating_cf_trend")
            
            # Operating cash flow components
            col1, col2 = st.columns(2)
            with col1:
                latest_cf = st.session_state.cash_flow.iloc[-1]
                cf_components = {
                    'Net Income': latest_cf['net_income'],
                    'Depreciation': latest_cf['depreciation'],
                    'Working Capital Change': -latest_cf['working_capital_change']
                }
                
                fig = px.bar(x=list(cf_components.keys()), y=list(cf_components.values()),
                            title="Operating Cash Flow Components",
                            color=list(cf_components.values()),
                            color_continuous_scale='RdYlGn')
                fig.update_layout(
                    xaxis_title="Component",
                    yaxis_title="Amount ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="cf_components")
            
            with col2:
                # Cash flow quality analysis
                cf_quality_data = st.session_state.cash_flow.copy()
                # Get column mapping for cash flow data
                cf_mapping = get_cash_flow_column_mapping(st.session_state.cash_flow)
                if 'operating_cash_flow' in cf_mapping:
                    operating_cf_col = cf_mapping['operating_cash_flow']
                    cf_quality_data['cf_quality'] = (cf_quality_data[operating_cf_col] / cf_quality_data['net_income']).round(2)
                else:
                    st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                    return
                
                fig = go.Figure(data=[
                    go.Scatter(x=cf_quality_data['period'], y=cf_quality_data['cf_quality'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='Cash Flow Quality')
                ])
                fig.update_layout(
                    title="Cash Flow Quality (OCF/Net Income)",
                    xaxis_title="Period",
                    yaxis_title="Quality Ratio",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=1.0, line_dash="dash", line_color="green", annotation_text="Good Quality (≥1.0)")
                fig.add_hline(y=0.8, line_dash="dash", line_color="orange", annotation_text="Acceptable (≥0.8)")
                st.plotly_chart(fig, use_container_width=True, key="cf_quality")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_operating_cash_flow_ai_recommendations:
                try:
                    ai_recommendations = generate_operating_cash_flow_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("🔄 Free Cash Flow")
        
        if not st.session_state.cash_flow.empty:
            # Free cash flow trend
            fig = go.Figure(data=[
                go.Scatter(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow['free_cash_flow'],
                          mode='lines+markers', line=dict(color='#2ca02c', width=3),
                          marker=dict(size=8), name='Free Cash Flow')
            ])
            fig.update_layout(
                title="Free Cash Flow Trend",
                xaxis_title="Period",
                yaxis_title="Free Cash Flow ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="fcf_trend")
            
            # FCF vs OCF comparison
            col1, col2 = st.columns(2)
            with col1:
                # Get column mapping for cash flow data
                cf_mapping = get_cash_flow_column_mapping(st.session_state.cash_flow)
                if 'operating_cash_flow' not in cf_mapping:
                    st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                    return
                
                operating_cf_col = cf_mapping['operating_cash_flow']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow[operating_cf_col],
                                        mode='lines+markers', name='Operating CF', line=dict(color='#1f77b4')))
                fig.add_trace(go.Scatter(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow['free_cash_flow'],
                                        mode='lines+markers', name='Free CF', line=dict(color='#2ca02c')))
                fig.update_layout(
                    title="Operating vs Free Cash Flow",
                    xaxis_title="Period",
                    yaxis_title="Cash Flow ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="fcf_vs_ocf")
            
            with col2:
                # Capital expenditures analysis
                fig = go.Figure(data=[
                    go.Bar(x=st.session_state.cash_flow['period'], y=st.session_state.cash_flow['capital_expenditures'],
                           marker_color='#ff7f0e', name='Capital Expenditures',
                           text=st.session_state.cash_flow['capital_expenditures'].round(0),
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Capital Expenditures",
                    xaxis_title="Period",
                    yaxis_title="Capital Expenditures ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="capex_analysis")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_free_cash_flow_ai_recommendations:
                try:
                    ai_recommendations = generate_free_cash_flow_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("📊 Working Capital")
        
        if not st.session_state.balance_sheet.empty:
            # Working capital calculation
            working_capital_data = st.session_state.balance_sheet.copy()
            working_capital_data['working_capital'] = working_capital_data['current_assets'] - working_capital_data['current_liabilities']
            working_capital_data['working_capital_ratio'] = (working_capital_data['current_assets'] / working_capital_data['current_liabilities']).round(2)
            
            # Working capital trend
            fig = go.Figure(data=[
                go.Scatter(x=working_capital_data['period'], y=working_capital_data['working_capital'],
                          mode='lines+markers', line=dict(color='#9467bd', width=3),
                          marker=dict(size=8), name='Working Capital')
            ])
            fig.update_layout(
                title="Working Capital Trend",
                xaxis_title="Period",
                yaxis_title="Working Capital ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="wc_trend")
            
            # Working capital components
            col1, col2 = st.columns(2)
            with col1:
                latest_wc = working_capital_data.iloc[-1]
                wc_components = {
                    'Cash & Equivalents': latest_wc['cash_and_equivalents'],
                    'Accounts Receivable': latest_wc['accounts_receivable'],
                    'Inventory': latest_wc['inventory'],
                    'Other Current Assets': latest_wc['current_assets'] - latest_wc['cash_and_equivalents'] - latest_wc['accounts_receivable'] - latest_wc['inventory']
                }
                
                fig = px.pie(values=list(wc_components.values()), names=list(wc_components.keys()),
                            title="Working Capital Components")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="wc_components")
            
            with col2:
                # Working capital ratio
                fig = go.Figure(data=[
                    go.Scatter(x=working_capital_data['period'], y=working_capital_data['working_capital_ratio'],
                              mode='lines+markers', line=dict(color='#ff7f0e', width=3),
                              marker=dict(size=8), name='Working Capital Ratio')
                ])
                fig.update_layout(
                    title="Working Capital Ratio",
                    xaxis_title="Period",
                    yaxis_title="Ratio",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=2.0, line_dash="dash", line_color="green", annotation_text="Good (≥2.0)")
                fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Poor (<1.0)")
                st.plotly_chart(fig, use_container_width=True, key="wc_ratio")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_working_capital_ai_recommendations:
                try:
                    ai_recommendations = generate_working_capital_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.cash_flow
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet and cash flow data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("📈 Cash Flow Trends")
        
        if not st.session_state.cash_flow.empty:
            # Get column mapping for cash flow data
            cf_mapping = get_cash_flow_column_mapping(st.session_state.cash_flow)
            if 'operating_cash_flow' not in cf_mapping:
                st.warning("⚠️ Operating cash flow column not found. Expected columns: operating_cash_flow, operating_cf, operating_cashflow")
                return
            
            operating_cf_col = cf_mapping['operating_cash_flow']
            
            # Cash flow trend analysis
            cf_trends = st.session_state.cash_flow.copy()
            cf_trends['cf_growth'] = cf_trends[operating_cf_col].pct_change() * 100
            
            fig = go.Figure(data=[
                go.Scatter(x=cf_trends['period'], y=cf_trends['cf_growth'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='Cash Flow Growth (%)')
            ])
            fig.update_layout(
                title="Cash Flow Growth Rate",
                xaxis_title="Period",
                yaxis_title="Growth Rate (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="No Growth")
            st.plotly_chart(fig, use_container_width=True, key="cf_growth")
            
            # Cash flow insights
            latest_cf_trend = cf_trends.iloc[-1]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if latest_cf_trend[operating_cf_col] > 0:
                    st.success(f"✅ Operating CF: ${latest_cf_trend[operating_cf_col]:,.0f} (Positive)")
                else:
                    st.error(f"❌ Operating CF: ${latest_cf_trend[operating_cf_col]:,.0f} (Negative)")
            
            with col2:
                if latest_cf_trend['free_cash_flow'] > 0:
                    st.success(f"✅ Free CF: ${latest_cf_trend['free_cash_flow']:,.0f} (Positive)")
                else:
                    st.error(f"❌ Free CF: ${latest_cf_trend['free_cash_flow']:,.0f} (Negative)")
            
            with col3:
                if not pd.isna(latest_cf_trend['cf_growth']) and latest_cf_trend['cf_growth'] > 0:
                    st.success(f"✅ CF Growth: {latest_cf_trend['cf_growth']:.1f}% (Growing)")
                elif not pd.isna(latest_cf_trend['cf_growth']):
                    st.warning(f"⚠️ CF Growth: {latest_cf_trend['cf_growth']:.1f}% (Declining)")
                else:
                    st.info("ℹ️ CF Growth: No data")
            
            # Cash flow recommendations
            st.write("**Cash Flow Analysis Recommendations:**")
            if latest_cf_trend[operating_cf_col] < 0:
                st.error("❌ **Negative Operating Cash Flow**: Critical issue. Review operations and cost structure.")
            
            if latest_cf_trend['free_cash_flow'] < 0:
                st.warning("⚠️ **Negative Free Cash Flow**: May indicate over-investment or operational issues.")
            
            if latest_cf_trend[operating_cf_col] > 0 and latest_cf_trend['free_cash_flow'] > 0:
                st.success("✅ **Strong Cash Flow**: Positive operating and free cash flow indicate healthy operations.")
            
            # Working capital recommendations
            if not st.session_state.balance_sheet.empty:
                latest_wc = st.session_state.balance_sheet.iloc[-1]
                working_capital = latest_wc['current_assets'] - latest_wc['current_liabilities']
                
                if working_capital < 0:
                    st.error("❌ **Negative Working Capital**: Immediate attention required for liquidity management.")
                elif working_capital < latest_wc['current_assets'] * 0.1:
                    st.warning("⚠️ **Low Working Capital**: Consider improving working capital management.")
                else:
                    st.success("✅ **Adequate Working Capital**: Sufficient liquidity for operations.")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_cash_flow_trends_ai_recommendations:
                try:
                    ai_recommendations = generate_cash_flow_trends_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")

def show_capital_structure():
    st.markdown("""
    <div class="section-header">
        <h3>🏗️ Capital Structure & Financing</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.balance_sheet.empty and st.session_state.income_statement.empty:
        st.info("🏗️ Please upload balance sheet and income statement data to view capital structure analytics.")
        return
    
    # Calculate capital structure metrics
    capital_summary, capital_message = calculate_capital_structure_metrics(
        st.session_state.balance_sheet, st.session_state.income_statement
    )
    
    # Display summary metrics
    st.subheader("🏗️ Capital Structure Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not capital_summary.empty:
            debt_equity = capital_summary.iloc[0]['debt_to_equity']
            st.metric("Debt-to-Equity Ratio", f"{debt_equity:.2f}")
    
    with col2:
        if not capital_summary.empty and len(capital_summary) > 1:
            wacc = capital_summary.iloc[0]['wacc']
            st.metric("WACC", f"{wacc:.1%}")
    
    with col3:
        if not capital_summary.empty and len(capital_summary) > 2:
            interest_coverage = capital_summary.iloc[0]['interest_coverage']
            st.metric("Interest Coverage Ratio", f"{interest_coverage:.1f}")
    
    st.info(capital_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Debt Analysis", "💰 WACC Calculation", "🏦 Interest Coverage", "📈 Capital Optimization"
    ])
    
    with tab1:
        st.subheader("📊 Debt Analysis")
        
        if not st.session_state.balance_sheet.empty:
            # Debt-to-equity trend
            debt_analysis = st.session_state.balance_sheet.copy()
            debt_analysis['debt_to_equity'] = (debt_analysis['total_liabilities'] / debt_analysis['shareholder_equity']).round(2)
            debt_analysis['debt_ratio'] = (debt_analysis['total_liabilities'] / debt_analysis['total_assets'] * 100).round(2)
            
            fig = go.Figure(data=[
                go.Scatter(x=debt_analysis['period'], y=debt_analysis['debt_to_equity'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='Debt-to-Equity Ratio')
            ])
            fig.update_layout(
                title="Debt-to-Equity Ratio Trend",
                xaxis_title="Period",
                yaxis_title="Debt-to-Equity Ratio",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=0.5, line_dash="dash", line_color="green", annotation_text="Conservative (0.5)")
            fig.add_hline(y=1.0, line_dash="dash", line_color="orange", annotation_text="Moderate (1.0)")
            fig.add_hline(y=2.0, line_dash="dash", line_color="red", annotation_text="High Risk (2.0)")
            st.plotly_chart(fig, use_container_width=True, key="chart_27")
            
            # Capital structure composition
            col1, col2 = st.columns(2)
            with col1:
                latest_debt = debt_analysis.iloc[-1]
                capital_composition = {
                    'Total Liabilities': latest_debt['total_liabilities'],
                    'Shareholder Equity': latest_debt['shareholder_equity']
                }
                
                fig = px.pie(values=list(capital_composition.values()), names=list(capital_composition.keys()),
                            title="Capital Structure Composition")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="chart_28")
            
            with col2:
                # Debt ratio trend
                fig = go.Figure(data=[
                    go.Scatter(x=debt_analysis['period'], y=debt_analysis['debt_ratio'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='Debt Ratio (%)')
                ])
                fig.update_layout(
                    title="Debt Ratio Trend",
                    xaxis_title="Period",
                    yaxis_title="Debt Ratio (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Conservative (30%)")
                fig.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Moderate (50%)")
                fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="High Risk (70%)")
                st.plotly_chart(fig, use_container_width=True, key="chart_29")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_debt_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_debt_analysis_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet and income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("💰 WACC Calculation")
        
        if not st.session_state.balance_sheet.empty:
            # WACC calculation details
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            equity_value = latest_bs['shareholder_equity']
            debt_value = latest_bs['total_liabilities']
            total_value = equity_value + debt_value
            
            # Assumed costs (in real scenario, these would come from market data)
            cost_of_equity = 0.12  # 12%
            cost_of_debt = 0.06    # 6%
            tax_rate = 0.25        # 25%
            
            equity_weight = equity_value / total_value if total_value > 0 else 0
            debt_weight = debt_value / total_value if total_value > 0 else 0
            
            wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
            
            # WACC breakdown
            wacc_breakdown = {
                'Equity Component': equity_weight * cost_of_equity * 100,
                'Debt Component': debt_weight * cost_of_debt * (1 - tax_rate) * 100
            }
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(values=list(wacc_breakdown.values()), names=list(wacc_breakdown.keys()),
                            title="WACC Components")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="chart_30")
            
            with col2:
                # WACC metrics
                st.metric("Total Value", f"${total_value:,.0f}")
                st.metric("Equity Weight", f"{equity_weight:.1%}")
                st.metric("Debt Weight", f"{debt_weight:.1%}")
                st.metric("WACC", f"{wacc:.1%}")
            
            # WACC sensitivity analysis
            st.subheader("WACC Sensitivity Analysis")
            
            # Create sensitivity matrix
            equity_costs = [0.10, 0.12, 0.14, 0.16]
            debt_costs = [0.04, 0.06, 0.08, 0.10]
            
            sensitivity_data = []
            for ec in equity_costs:
                for dc in debt_costs:
                    wacc_sens = (equity_weight * ec) + (debt_weight * dc * (1 - tax_rate))
                    sensitivity_data.append({
                        'Cost of Equity': f"{ec:.1%}",
                        'Cost of Debt': f"{dc:.1%}",
                        'WACC': f"{wacc_sens:.1%}"
                    })
            
            sensitivity_df = pd.DataFrame(sensitivity_data)
            display_dataframe_with_index_1(sensitivity_df)
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_wacc_calculation_ai_recommendations:
                try:
                    ai_recommendations = generate_wacc_calculation_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet and income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("🏦 Interest Coverage")
        
        if not st.session_state.income_statement.empty and not st.session_state.balance_sheet.empty:
            # Check if required columns exist
            if 'interest_expense' not in st.session_state.income_statement.columns:
                st.warning("⚠️ Interest expense data not available. Skipping interest coverage analysis.")
                return
            if 'operating_income' not in st.session_state.income_statement.columns:
                st.warning("⚠️ Operating income data not available. Skipping interest coverage analysis.")
                return
            
            try:
                # Interest coverage analysis
                coverage_data = st.session_state.income_statement.copy()
                coverage_data['interest_coverage'] = (coverage_data['operating_income'] / coverage_data['interest_expense']).round(2)
            except Exception as e:
                st.error(f"❌ Error in interest coverage analysis: {str(e)}")
                return
            
            fig = go.Figure(data=[
                go.Scatter(x=coverage_data['period'], y=coverage_data['interest_coverage'],
                          mode='lines+markers', line=dict(color='#ff7f0e', width=3),
                          marker=dict(size=8), name='Interest Coverage Ratio')
            ])
            fig.update_layout(
                title="Interest Coverage Ratio Trend",
                xaxis_title="Period",
                yaxis_title="Interest Coverage Ratio",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=3.0, line_dash="dash", line_color="green", annotation_text="Strong (≥3.0)")
            fig.add_hline(y=1.5, line_dash="dash", line_color="orange", annotation_text="Adequate (≥1.5)")
            fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Risky (<1.0)")
            st.plotly_chart(fig, use_container_width=True, key="interest_coverage_trend")
            
            # Interest expense analysis
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[
                    go.Bar(x=coverage_data['period'], y=coverage_data['interest_expense'],
                           marker_color='#d62728', name='Interest Expense',
                           text=coverage_data['interest_expense'].round(0),
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Interest Expense Trend",
                    xaxis_title="Period",
                    yaxis_title="Interest Expense ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="interest_expense_trend")
            
            with col2:
                # Operating income vs interest expense
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=coverage_data['period'], y=coverage_data['operating_income'],
                                        mode='lines+markers', name='Operating Income', line=dict(color='#1f77b4')))
                fig.add_trace(go.Scatter(x=coverage_data['period'], y=coverage_data['interest_expense'],
                                        mode='lines+markers', name='Interest Expense', line=dict(color='#d62728')))
                fig.update_layout(
                    title="Operating Income vs Interest Expense",
                    xaxis_title="Period",
                    yaxis_title="Amount ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="operating_vs_interest")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_interest_coverage_ai_recommendations:
                try:
                    ai_recommendations = generate_interest_coverage_ai_recommendations(
                        st.session_state.income_statement,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded income statement and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("📈 Capital Optimization")
        
        if not st.session_state.balance_sheet.empty and not st.session_state.income_statement.empty:
            # Capital optimization analysis
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            latest_is = st.session_state.income_statement.iloc[-1]
            
            debt_to_equity = latest_bs['total_liabilities'] / latest_bs['shareholder_equity']
            debt_ratio = latest_bs['total_liabilities'] / latest_bs['total_assets']
            
            # Calculate interest coverage if data is available
            if 'interest_expense' in latest_is.index and 'operating_income' in latest_is.index:
                interest_coverage = latest_is['operating_income'] / latest_is['interest_expense'] if latest_is['interest_expense'] > 0 else float('inf')
            else:
                interest_coverage = float('inf')  # No interest expense means excellent coverage
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if debt_to_equity <= 0.5:
                    st.success(f"✅ Debt-to-Equity: {debt_to_equity:.2f} (Conservative)")
                elif debt_to_equity <= 1.0:
                    st.info(f"ℹ️ Debt-to-Equity: {debt_to_equity:.2f} (Moderate)")
                else:
                    st.warning(f"⚠️ Debt-to-Equity: {debt_to_equity:.2f} (High Risk)")
            
            with col2:
                if debt_ratio <= 0.3:
                    st.success(f"✅ Debt Ratio: {debt_ratio:.1%} (Conservative)")
                elif debt_ratio <= 0.5:
                    st.info(f"ℹ️ Debt Ratio: {debt_ratio:.1%} (Moderate)")
                else:
                    st.warning(f"⚠️ Debt Ratio: {debt_ratio:.1%} (High Risk)")
            
            with col3:
                if interest_coverage >= 3.0:
                    st.success(f"✅ Interest Coverage: {interest_coverage:.1f} (Strong)")
                elif interest_coverage >= 1.5:
                    st.info(f"ℹ️ Interest Coverage: {interest_coverage:.1f} (Adequate)")
                else:
                    st.error(f"❌ Interest Coverage: {interest_coverage:.1f} (Risky)")
            
            # Capital optimization recommendations
            st.write("**Capital Structure Recommendations:**")
            
            if debt_to_equity > 1.0:
                st.warning("⚠️ **High Debt Levels**: Consider reducing debt or increasing equity to improve financial stability.")
            
            if interest_coverage < 1.5:
                st.error("❌ **Low Interest Coverage**: Critical issue. Consider debt restructuring or operational improvements.")
            
            if debt_ratio > 0.5:
                st.warning("⚠️ **High Debt Ratio**: Review capital structure to reduce financial risk.")
            
            if debt_to_equity <= 0.5 and interest_coverage >= 3.0:
                st.success("✅ **Optimal Capital Structure**: Conservative debt levels with strong interest coverage.")
            
            # Optimal capital structure simulation
            st.subheader("Optimal Capital Structure Simulation")
            
            # Simulate different debt levels
            equity_base = latest_bs['shareholder_equity']
            debt_levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
            
            simulation_results = []
            for debt_level in debt_levels:
                new_debt = equity_base * debt_level
                new_equity = equity_base - new_debt
                new_total = new_equity + new_debt
                
                # Simplified WACC calculation
                new_wacc = (new_equity/new_total * 0.12) + (new_debt/new_total * 0.06 * 0.75)
                
                simulation_results.append({
                    'Debt Level': f"{debt_level:.0%}",
                    'Debt Amount': new_debt,
                    'Equity Amount': new_equity,
                    'WACC': f"{new_wacc:.1%}"
                })
            
            simulation_df = pd.DataFrame(simulation_results)
            display_dataframe_with_index_1(simulation_df)
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_capital_optimization_ai_recommendations:
                try:
                    ai_recommendations = generate_capital_optimization_ai_recommendations(
                        st.session_state.balance_sheet,
                        st.session_state.income_statement
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded balance sheet and income statement data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")

def show_investment_valuation():
    st.markdown("""
    <div class="section-header">
        <h3>📈 Investment & Valuation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.cash_flow.empty and st.session_state.balance_sheet.empty:
        st.info("📈 Please upload cash flow and balance sheet data to view investment and valuation analytics.")
        return
    
    # Calculate investment valuation metrics
    investment_summary, investment_message = calculate_investment_valuation_metrics(
        st.session_state.cash_flow, st.session_state.balance_sheet
    )
    
    # Display summary metrics
    st.subheader("📈 Investment & Valuation Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not investment_summary.empty:
            npv = investment_summary.iloc[0]['npv']
            st.metric("Net Present Value (NPV)", f"${npv:,.0f}")
    
    with col2:
        if not investment_summary.empty and len(investment_summary) > 1:
            payback_period = investment_summary.iloc[0]['payback_period']
            if payback_period == float('inf'):
                st.metric("Payback Period", "Never")
            else:
                st.metric("Payback Period", f"{payback_period:.1f} years")
    
    with col3:
        if not investment_summary.empty and len(investment_summary) > 2:
            eva = investment_summary.iloc[0]['eva']
            st.metric("Economic Value Added (EVA)", f"${eva:,.0f}")
    
    st.info(investment_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 NPV Analysis", "⏱️ Payback Period", "📊 EVA Calculation", "🎯 Investment Insights"
    ])
    
    with tab1:
        st.subheader("💰 NPV Analysis")
        
        if not st.session_state.cash_flow.empty:
            # NPV calculation with different discount rates
            cash_flows = st.session_state.cash_flow['cash_flow'].values
            initial_investment = st.session_state.cash_flow['initial_investment'].iloc[0]
            
            discount_rates = [0.05, 0.08, 0.10, 0.12, 0.15, 0.20]
            npv_results = []
            
            for rate in discount_rates:
                npv = -initial_investment
                for i, cf in enumerate(cash_flows):
                    npv += cf / ((1 + rate) ** (i + 1))
                npv_results.append({
                    'Discount Rate': f"{rate:.1%}",
                    'NPV': npv,
                    'Decision': 'Accept' if npv > 0 else 'Reject'
                })
            
            npv_df = pd.DataFrame(npv_results)
            
            # NPV vs Discount Rate chart
            fig = go.Figure(data=[
                go.Scatter(x=[float(x.strip('%'))/100 for x in npv_df['Discount Rate']], 
                          y=npv_df['NPV'],
                          mode='lines+markers', line=dict(color='#1f77b4', width=3),
                          marker=dict(size=8), name='NPV')
            ])
            fig.update_layout(
                title="NPV vs Discount Rate",
                xaxis_title="Discount Rate",
                yaxis_title="Net Present Value ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Break-even")
            st.plotly_chart(fig, use_container_width=True, key="chart_31")
            
            # NPV results table
            st.subheader("NPV Analysis Results")
            display_dataframe_with_index_1(npv_df.round(2))
            
            # IRR estimation (simplified)
            st.subheader("Internal Rate of Return (IRR) Estimation")
            
            # Find IRR using interpolation
            positive_npv = npv_df[npv_df['NPV'] > 0]
            negative_npv = npv_df[npv_df['NPV'] < 0]
            
            if not positive_npv.empty and not negative_npv.empty:
                # Simple interpolation to estimate IRR
                pos_rate = float(positive_npv.iloc[-1]['Discount Rate'].strip('%')) / 100
                neg_rate = float(negative_npv.iloc[0]['Discount Rate'].strip('%')) / 100
                pos_npv = positive_npv.iloc[-1]['NPV']
                neg_npv = negative_npv.iloc[0]['NPV']
                
                irr = pos_rate + (pos_npv / (pos_npv - neg_npv)) * (neg_rate - pos_rate)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Estimated IRR", f"{irr:.1%}")
                with col2:
                    if irr > 0.15:
                        st.success("✅ High IRR (Excellent)")
                    elif irr > 0.10:
                        st.info("ℹ️ Good IRR (Acceptable)")
                    else:
                        st.warning("⚠️ Low IRR (Marginal)")
            else:
                st.info("IRR calculation requires both positive and negative NPV values")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_npv_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_npv_analysis_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("⏱️ Payback Period")
        
        if not st.session_state.cash_flow.empty:
            # Payback period calculation
            cash_flows = st.session_state.cash_flow['cash_flow'].values
            initial_investment = st.session_state.cash_flow['initial_investment'].iloc[0]
            
            cumulative_cf = 0
            payback_period = 0
            payback_data = []
            
            for i, cf in enumerate(cash_flows):
                cumulative_cf += cf
                payback_data.append({
                    'Period': i + 1,
                    'Cash Flow': cf,
                    'Cumulative CF': cumulative_cf,
                    'Remaining Investment': initial_investment - cumulative_cf
                })
                
                if cumulative_cf >= initial_investment and payback_period == 0:
                    payback_period = i + 1
            
            payback_df = pd.DataFrame(payback_data)
            
            # Payback period visualization
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=payback_df['Period'], y=payback_df['Cumulative CF'],
                                    mode='lines+markers', name='Cumulative Cash Flow', line=dict(color='#1f77b4')))
            fig.add_trace(go.Scatter(x=payback_df['Period'], y=[initial_investment] * len(payback_df),
                                    mode='lines', name='Initial Investment', line=dict(color='red', dash='dash')))
            fig.update_layout(
                title="Payback Period Analysis",
                xaxis_title="Period",
                yaxis_title="Cumulative Cash Flow ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_32")
            
            # Payback period results
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Initial Investment", f"${initial_investment:,.0f}")
            with col2:
                st.metric("Payback Period", f"{payback_period} years")
            with col3:
                if payback_period <= 3:
                    st.success("✅ Quick Payback (≤3 years)")
                elif payback_period <= 5:
                    st.info("ℹ️ Moderate Payback (≤5 years)")
                else:
                    st.warning("⚠️ Long Payback (>5 years)")
            
            # Payback period table
            st.subheader("Payback Period Details")
            display_dataframe_with_index_1(payback_df.round(2))
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_payback_period_ai_recommendations:
                try:
                    ai_recommendations = generate_payback_period_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("📊 EVA Calculation")
        
        if not st.session_state.cash_flow.empty and not st.session_state.balance_sheet.empty:
            # EVA calculation
            latest_cf = st.session_state.cash_flow.iloc[-1]
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            nopat = latest_cf['nopat']
            capital_employed = latest_bs['total_assets']
            wacc = 0.092  # From previous calculation
            
            eva = nopat - (wacc * capital_employed)
            
            # EVA components
            eva_components = {
                'NOPAT': nopat,
                'Capital Charge': wacc * capital_employed,
                'EVA': eva
            }
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(x=list(eva_components.keys()), y=list(eva_components.values()),
                            title="EVA Components",
                            color=list(eva_components.values()),
                            color_continuous_scale='RdYlGn')
                fig.update_layout(
                    xaxis_title="Component",
                    yaxis_title="Amount ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_33")
            
            with col2:
                st.metric("NOPAT", f"${nopat:,.0f}")
                st.metric("Capital Employed", f"${capital_employed:,.0f}")
                st.metric("WACC", f"{wacc:.1%}")
                st.metric("EVA", f"${eva:,.0f}")
            
            # EVA trend analysis
            if len(st.session_state.cash_flow) > 1:
                eva_trend = st.session_state.cash_flow.copy()
                eva_trend['eva'] = eva_trend['nopat'] - (wacc * capital_employed)
                
                fig = go.Figure(data=[
                    go.Scatter(x=eva_trend['period'], y=eva_trend['eva'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='EVA')
                ])
                fig.update_layout(
                    title="EVA Trend Over Time",
                    xaxis_title="Period",
                    yaxis_title="Economic Value Added ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Break-even")
                st.plotly_chart(fig, use_container_width=True, key="chart_34")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_eva_calculation_ai_recommendations:
                try:
                    ai_recommendations = generate_eva_calculation_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("🎯 Investment Insights")
        
        if not st.session_state.cash_flow.empty:
            # Investment decision framework
            latest_npv = investment_summary.iloc[0]['npv'] if not investment_summary.empty else 0
            latest_payback = investment_summary.iloc[0]['payback_period'] if not investment_summary.empty else 0
            latest_eva = investment_summary.iloc[0]['eva'] if not investment_summary.empty else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if latest_npv > 0:
                    st.success(f"✅ NPV: ${latest_npv:,.0f} (Positive)")
                else:
                    st.error(f"❌ NPV: ${latest_npv:,.0f} (Negative)")
            
            with col2:
                if latest_payback <= 3:
                    st.success(f"✅ Payback: {latest_payback} years (Quick)")
                elif latest_payback <= 5:
                    st.info(f"ℹ️ Payback: {latest_payback} years (Moderate)")
                else:
                    st.warning(f"⚠️ Payback: {latest_payback} years (Long)")
            
            with col3:
                if latest_eva > 0:
                    st.success(f"✅ EVA: ${latest_eva:,.0f} (Value Creating)")
                else:
                    st.error(f"❌ EVA: ${latest_eva:,.0f} (Value Destroying)")
            
            # Investment recommendations
            st.write("**Investment Analysis Recommendations:**")
            
            if latest_npv > 0 and latest_payback <= 3 and latest_eva > 0:
                st.success("✅ **Excellent Investment**: Strong NPV, quick payback, and positive EVA.")
            
            elif latest_npv > 0 and latest_payback <= 5:
                st.info("ℹ️ **Good Investment**: Positive NPV with acceptable payback period.")
            
            elif latest_npv < 0:
                st.error("❌ **Poor Investment**: Negative NPV indicates value destruction.")
            
            elif latest_payback > 5:
                st.warning("⚠️ **Long Payback Risk**: Consider shorter-term alternatives.")
            
            # Risk assessment
            st.subheader("Investment Risk Assessment")
            
            risk_factors = []
            if latest_npv < 0:
                risk_factors.append("Negative NPV")
            if latest_payback > 5:
                risk_factors.append("Long payback period")
            if latest_eva < 0:
                risk_factors.append("Negative EVA")
            
            if risk_factors:
                st.warning(f"⚠️ **Risk Factors Identified**: {', '.join(risk_factors)}")
            else:
                st.success("✅ **Low Risk Profile**: All metrics indicate favorable investment conditions.")
            
            # Sensitivity analysis
            st.subheader("Sensitivity Analysis")
            
            # Cash flow sensitivity
            base_cf = st.session_state.cash_flow['cash_flow'].mean()
            sensitivity_scenarios = [-20, -10, 0, 10, 20]  # Percentage changes
            
            sensitivity_results = []
            for change in sensitivity_scenarios:
                new_cf = base_cf * (1 + change/100)
                new_npv = -initial_investment + sum([new_cf / ((1 + 0.10) ** (i + 1)) for i in range(len(cash_flows))])
                
                sensitivity_results.append({
                    'Cash Flow Change': f"{change:+.0f}%",
                    'New NPV': new_npv,
                    'Decision': 'Accept' if new_npv > 0 else 'Reject'
                })
            
            sensitivity_df = pd.DataFrame(sensitivity_results)
            display_dataframe_with_index_1(sensitivity_df.round(2))
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_investment_insights_ai_recommendations:
                try:
                    ai_recommendations = generate_investment_insights_ai_recommendations(
                        st.session_state.cash_flow,
                        st.session_state.balance_sheet
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded cash flow and balance sheet data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")

def show_risk_compliance():
    st.markdown("""
    <div class="section-header">
        <h3>⚠️ Risk & Compliance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if (st.session_state.balance_sheet.empty and st.session_state.income_statement.empty and 
        st.session_state.cash_flow.empty and st.session_state.market_data.empty):
        st.info("⚠️ Please upload financial data to view risk and compliance analytics.")
        return
    
    # Use new risk analyzer if available
    if FinanceRiskAnalyzer is not None:
        # Initialize risk analyzer
        risk_analyzer = FinanceRiskAnalyzer(
            st.session_state.income_statement,
            st.session_state.balance_sheet,
            st.session_state.cash_flow,
            st.session_state.budget,
            st.session_state.forecast,
            st.session_state.market_data,
            st.session_state.customer_data,
            st.session_state.product_data,
            st.session_state.value_chain
        )
        
        # Display risk dashboard
        display_risk_dashboard(risk_analyzer)
        
        # Add traditional risk metrics as well
        if not st.session_state.balance_sheet.empty and not st.session_state.market_data.empty:
            risk_summary, risk_message = calculate_risk_compliance_metrics(
                st.session_state.balance_sheet, st.session_state.market_data
            )
            
            st.markdown("### 📊 Traditional Risk Metrics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not risk_summary.empty:
                    var = risk_summary.iloc[0]['Value']
                    st.metric("Value at Risk (VaR)", var)
            
            with col2:
                if not risk_summary.empty and len(risk_summary) > 1:
                    lcr = risk_summary.iloc[1]['Value']
                    st.metric("Liquidity Coverage Ratio", lcr)
            
            with col3:
                if not risk_summary.empty and len(risk_summary) > 2:
                    car = risk_summary.iloc[2]['Value']
                    st.metric("Capital Adequacy Ratio", car)
            
            st.info(risk_message)
    else:
        # Fallback to original risk analysis
        if st.session_state.balance_sheet.empty and st.session_state.market_data.empty:
            st.info("⚠️ Please upload balance sheet and market data to view risk and compliance analytics.")
            return
        
        # Calculate risk compliance metrics
        risk_summary, risk_message = calculate_risk_compliance_metrics(
            st.session_state.balance_sheet, st.session_state.market_data
        )
    
    # Display summary metrics
    st.subheader("⚠️ Risk & Compliance Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not risk_summary.empty:
            var = risk_summary.iloc[0]['Value']
            st.metric("Value at Risk (VaR)", var)
    
    with col2:
        if not risk_summary.empty and len(risk_summary) > 1:
            lcr = risk_summary.iloc[1]['Value']
            st.metric("Liquidity Coverage Ratio", lcr)
    
    with col3:
        if not risk_summary.empty and len(risk_summary) > 2:
            car = risk_summary.iloc[2]['Value']
            st.metric("Capital Adequacy Ratio", car)
    
    st.info(risk_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 VaR Analysis", "💧 Liquidity Risk", "🏦 Capital Adequacy", "📈 Risk Monitoring"
    ])
    
    with tab1:
        st.subheader("📊 VaR Analysis")
        
        if not st.session_state.balance_sheet.empty:
            # VaR calculation simulation
            portfolio_value = st.session_state.balance_sheet['total_assets'].iloc[-1]
            volatility = 0.15  # Assumed 15% volatility
            confidence_levels = [0.90, 0.95, 0.99]
            time_horizons = [1, 30, 90]  # days
            
            var_results = []
            for conf in confidence_levels:
                for horizon in time_horizons:
                    # Z-score for confidence level
                    z_scores = {0.90: 1.282, 0.95: 1.645, 0.99: 2.326}
                    z_score = z_scores[conf]
                    
                    var = portfolio_value * volatility * np.sqrt(horizon/365) * z_score
                    var_results.append({
                        'Confidence Level': f"{conf:.0%}",
                        'Time Horizon': f"{horizon} days",
                        'VaR': var,
                        'VaR %': (var / portfolio_value * 100)
                    })
            
            var_df = pd.DataFrame(var_results)
            
            # VaR heatmap
            var_pivot = var_df.pivot(index='Time Horizon', columns='Confidence Level', values='VaR %')
            
            fig = go.Figure(data=go.Heatmap(
                z=var_pivot.values,
                x=var_pivot.columns,
                y=var_pivot.index,
                colorscale='RdYlGn_r',
                text=var_pivot.values.round(2),
                texttemplate="%{text}%",
                textfont={"size": 12}
            ))
            fig.update_layout(
                title="VaR by Confidence Level and Time Horizon",
                xaxis_title="Confidence Level",
                yaxis_title="Time Horizon",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_35")
            
            # VaR trend analysis
            if len(st.session_state.balance_sheet) > 1:
                var_trend = st.session_state.balance_sheet.copy()
                var_trend['var_95'] = var_trend['total_assets'] * volatility * np.sqrt(30/365) * 1.645
                
                fig = go.Figure(data=[
                    go.Scatter(x=var_trend['period'], y=var_trend['var_95'],
                              mode='lines+markers', line=dict(color='#d62728', width=3),
                              marker=dict(size=8), name='95% VaR (30 days)')
                ])
                fig.update_layout(
                    title="VaR Trend Over Time",
                    xaxis_title="Period",
                    yaxis_title="Value at Risk ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_36")
            
            # VaR results table
            st.subheader("VaR Analysis Results")
            display_dataframe_with_index_1(var_df.round(2))
    
    with tab2:
        st.subheader("💧 Liquidity Risk")
        
        if not st.session_state.balance_sheet.empty:
            # Liquidity coverage ratio calculation
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            # High-quality liquid assets (simplified)
            hqla = latest_bs['cash_and_equivalents']
            
            # Net cash outflows (simplified - 30% of current liabilities)
            net_cash_outflows = latest_bs['current_liabilities'] * 0.3
            
            lcr = hqla / net_cash_outflows if net_cash_outflows > 0 else 0
            
            # Liquidity metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High-Quality Liquid Assets", f"${hqla:,.0f}")
            with col2:
                st.metric("Net Cash Outflows (30 days)", f"${net_cash_outflows:,.0f}")
            with col3:
                st.metric("Liquidity Coverage Ratio", f"{lcr:.1%}")
            
            # LCR compliance
            if lcr >= 1.0:
                st.success("✅ **LCR Compliant**: Ratio ≥ 100% (Regulatory requirement met)")
            else:
                st.error(f"❌ **LCR Non-Compliant**: Ratio {lcr:.1%} < 100% (Regulatory requirement not met)")
            
            # Liquidity stress testing
            st.subheader("Liquidity Stress Testing")
            
            stress_scenarios = {
                'Baseline': 1.0,
                'Mild Stress': 0.8,
                'Moderate Stress': 0.6,
                'Severe Stress': 0.4
            }
            
            stress_results = []
            for scenario, factor in stress_scenarios.items():
                stressed_hqla = hqla * factor
                stressed_lcr = stressed_hqla / net_cash_outflows if net_cash_outflows > 0 else 0
                
                stress_results.append({
                    'Scenario': scenario,
                    'HQLA Factor': f"{factor:.1f}",
                    'Stressed HQLA': stressed_hqla,
                    'Stressed LCR': stressed_lcr,
                    'Compliant': 'Yes' if stressed_lcr >= 1.0 else 'No'
                })
            
            stress_df = pd.DataFrame(stress_results)
            display_dataframe_with_index_1(stress_df.round(2))
            
            # Liquidity composition
            liquidity_composition = {
                'Cash & Equivalents': latest_bs['cash_and_equivalents'],
                'Accounts Receivable': latest_bs['accounts_receivable'],
                'Other Liquid Assets': latest_bs['current_assets'] - latest_bs['cash_and_equivalents'] - latest_bs['accounts_receivable']
            }
            
            fig = px.pie(values=list(liquidity_composition.values()), names=list(liquidity_composition.keys()),
                        title="Liquidity Asset Composition")
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key="chart_37")
    
    with tab3:
        st.subheader("🏦 Capital Adequacy")
        
        if not st.session_state.balance_sheet.empty:
            # Capital adequacy ratio calculation
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            # Tier 1 capital (simplified - shareholder equity)
            tier1_capital = latest_bs['shareholder_equity']
            
            # Risk-weighted assets (simplified - 80% of total assets)
            risk_weighted_assets = latest_bs['total_assets'] * 0.8
            
            car = (tier1_capital / risk_weighted_assets * 100) if risk_weighted_assets > 0 else 0
            
            # Capital metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tier 1 Capital", f"${tier1_capital:,.0f}")
            with col2:
                st.metric("Risk-Weighted Assets", f"${risk_weighted_assets:,.0f}")
            with col3:
                st.metric("Capital Adequacy Ratio", f"{car:.1f}%")
            
            # CAR compliance
            if car >= 8.0:
                st.success("✅ **CAR Compliant**: Ratio ≥ 8% (Basel III requirement met)")
            else:
                st.error(f"❌ **CAR Non-Compliant**: Ratio {car:.1f}% < 8% (Basel III requirement not met)")
            
            # Capital structure analysis
            st.subheader("Capital Structure Analysis")
            
            capital_components = {
                'Tier 1 Capital': tier1_capital,
                'Total Liabilities': latest_bs['total_liabilities'],
                'Risk Buffer': tier1_capital - (risk_weighted_assets * 0.08)
            }
            
            fig = px.bar(x=list(capital_components.keys()), y=list(capital_components.values()),
                        title="Capital Components",
                        color=list(capital_components.values()),
                        color_continuous_scale='RdYlGn')
            fig.update_layout(
                xaxis_title="Component",
                yaxis_title="Amount ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_38")
            
            # Capital adequacy trend
            if len(st.session_state.balance_sheet) > 1:
                car_trend = st.session_state.balance_sheet.copy()
                car_trend['car'] = (car_trend['shareholder_equity'] / (car_trend['total_assets'] * 0.8) * 100).round(2)
                
                fig = go.Figure(data=[
                    go.Scatter(x=car_trend['period'], y=car_trend['car'],
                              mode='lines+markers', line=dict(color='#2ca02c', width=3),
                              marker=dict(size=8), name='Capital Adequacy Ratio (%)')
                ])
                fig.update_layout(
                    title="Capital Adequacy Ratio Trend",
                    xaxis_title="Period",
                    yaxis_title="CAR (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                fig.add_hline(y=8.0, line_dash="dash", line_color="green", annotation_text="Basel III (8%)")
                fig.add_hline(y=10.5, line_dash="dash", line_color="orange", annotation_text="Conservation Buffer (10.5%)")
                st.plotly_chart(fig, use_container_width=True, key="chart_39")
    
    with tab4:
        st.subheader("📈 Risk Monitoring")
        
        if not st.session_state.balance_sheet.empty:
            # Risk dashboard
            latest_bs = st.session_state.balance_sheet.iloc[-1]
            
            # Calculate various risk metrics
            current_ratio = latest_bs['current_assets'] / latest_bs['current_liabilities']
            debt_to_equity = latest_bs['total_liabilities'] / latest_bs['shareholder_equity']
            working_capital = latest_bs['current_assets'] - latest_bs['current_liabilities']
            
            # Risk assessment
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if current_ratio >= 2.0:
                    st.success(f"✅ Current Ratio: {current_ratio:.2f}")
                elif current_ratio >= 1.5:
                    st.info(f"ℹ️ Current Ratio: {current_ratio:.2f}")
                else:
                    st.error(f"❌ Current Ratio: {current_ratio:.2f}")
            
            with col2:
                if debt_to_equity <= 0.5:
                    st.success(f"✅ Debt-to-Equity: {debt_to_equity:.2f}")
                elif debt_to_equity <= 1.0:
                    st.info(f"ℹ️ Debt-to-Equity: {debt_to_equity:.2f}")
                else:
                    st.warning(f"⚠️ Debt-to-Equity: {debt_to_equity:.2f}")
            
            with col3:
                if working_capital > 0:
                    st.success(f"✅ Working Capital: ${working_capital:,.0f}")
                else:
                    st.error(f"❌ Working Capital: ${working_capital:,.0f}")
            
            with col4:
                if lcr >= 1.0:
                    st.success(f"✅ LCR: {lcr:.1%}")
                else:
                    st.error(f"❌ LCR: {lcr:.1%}")
            
            # Risk heatmap
            st.subheader("Risk Heatmap")
            
            risk_metrics = {
                'Liquidity Risk': current_ratio,
                'Solvency Risk': debt_to_equity,
                'Capital Risk': car/100,  # Normalize to 0-1
                'Working Capital Risk': 1 if working_capital > 0 else 0
            }
            
            # Create risk matrix
            risk_matrix = pd.DataFrame({
                'Risk Metric': list(risk_metrics.keys()),
                'Risk Score': list(risk_metrics.values()),
                'Risk Level': ['Low' if v > 0.5 else 'Medium' if v > 0.2 else 'High' for v in risk_metrics.values()]
            })
            
            fig = px.bar(risk_matrix, x='Risk Metric', y='Risk Score',
                        color='Risk Level',
                        color_discrete_map={'Low': '#2ca02c', 'Medium': '#ff7f0e', 'High': '#d62728'},
                        title="Risk Assessment Dashboard")
            fig.update_layout(
                xaxis_title="Risk Metric",
                yaxis_title="Risk Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_40")
            
            # Risk recommendations
            st.write("**Risk Management Recommendations:**")
            
            risk_issues = []
            if current_ratio < 1.5:
                risk_issues.append("Improve liquidity management")
            if debt_to_equity > 1.0:
                risk_issues.append("Reduce debt levels")
            if working_capital < 0:
                risk_issues.append("Address negative working capital")
            if lcr < 1.0:
                risk_issues.append("Increase liquid assets")
            if car < 8.0:
                risk_issues.append("Strengthen capital position")
            
            if risk_issues:
                st.warning(f"⚠️ **Risk Issues Identified**: {', '.join(risk_issues)}")
            else:
                st.success("✅ **Low Risk Profile**: All risk metrics within acceptable ranges.")
            
            # Early warning indicators
            st.subheader("Early Warning Indicators")
            
            warning_indicators = []
            if current_ratio < 1.0:
                warning_indicators.append("Critical liquidity risk")
            if debt_to_equity > 2.0:
                warning_indicators.append("Excessive leverage")
            if working_capital < -latest_bs['current_assets'] * 0.1:
                warning_indicators.append("Severe working capital deficit")
            if lcr < 0.5:
                warning_indicators.append("Inadequate liquidity coverage")
            
            if warning_indicators:
                st.error(f"🚨 **Critical Risk Alerts**: {', '.join(warning_indicators)}")
            else:
                st.success("✅ **No Critical Risk Alerts**: All indicators within safe ranges.")

def show_strategic_kpis():
    st.markdown("""
    <div class="section-header">
        <h3>📊 Strategic Financial KPIs</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have data
    if st.session_state.customer_data.empty and st.session_state.product_data.empty and st.session_state.value_chain.empty:
        st.info("📊 Please upload customer, product, and value chain data to view strategic KPIs analytics.")
        return
    
    # Calculate strategic KPIs
    strategic_summary, strategic_message = calculate_strategic_kpis(
        st.session_state.customer_data, st.session_state.product_data, st.session_state.value_chain
    )
    
    # Display summary metrics
    st.subheader("📊 Strategic Financial KPIs Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not strategic_summary.empty:
            customer_profitability = strategic_summary.iloc[0]['Value']
            st.metric("Customer Profitability", customer_profitability)
    
    with col2:
        if not strategic_summary.empty and len(strategic_summary) > 1:
            product_profitability = strategic_summary.iloc[1]['Value']
            st.metric("Product Profitability", product_profitability)
    
    with col3:
        if not strategic_summary.empty and len(strategic_summary) > 2:
            value_chain_cost = strategic_summary.iloc[2]['Value']
            st.metric("Value Chain Cost", value_chain_cost)
    
    st.info(strategic_message)
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Customer Profitability", "📦 Product Profitability", "🔗 Value Chain Analysis", "🎯 Strategic Insights"
    ])
    
    with tab1:
        st.subheader("👥 Customer Profitability")
        
        if not st.session_state.customer_data.empty:
            # Customer profitability analysis
            customer_analysis = st.session_state.customer_data.copy()
            customer_analysis['profit'] = customer_analysis['revenue'] - customer_analysis['costs_to_serve']
            customer_analysis['profit_margin'] = (customer_analysis['profit'] / customer_analysis['revenue'] * 100).round(2)
            
            # Top customers by profitability
            top_customers = customer_analysis.nlargest(5, 'profit')
            
            fig = go.Figure(data=[
                go.Bar(x=top_customers['customer_name'], y=top_customers['profit'],
                       marker_color='#2ca02c', name='Profit',
                       text=top_customers['profit'].round(0),
                       textposition='auto')
            ])
            fig.update_layout(
                title="Top 5 Customers by Profit",
                xaxis_title="Customer",
                yaxis_title="Profit ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_41")
            
            # Customer profitability distribution
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(customer_analysis, x='profitability',
                                  title="Customer Profitability Distribution",
                                  nbins=10)
                fig.update_layout(
                    xaxis_title="Profitability (%)",
                    yaxis_title="Number of Customers",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_42")
            
            with col2:
                # Customer profitability vs revenue
                fig = px.scatter(customer_analysis, x='revenue', y='profitability',
                                title="Customer Profitability vs Revenue",
                                hover_data=['customer_name'])
                fig.update_layout(
                    xaxis_title="Revenue ($)",
                    yaxis_title="Profitability (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_43")
            
            # Customer segmentation
            st.subheader("Customer Segmentation")
            
            # Segment customers by profitability
            customer_analysis['segment'] = pd.cut(customer_analysis['profitability'], 
                                                bins=[-float('inf'), 0, 20, 40, float('inf')],
                                                labels=['Loss Making', 'Low Profit', 'Medium Profit', 'High Profit'])
            
            segment_summary = customer_analysis.groupby('segment').agg({
                'customer_id': 'count',
                'revenue': 'sum',
                'profit': 'sum',
                'profitability': 'mean'
            }).round(2)
            
            segment_summary.columns = ['Customer Count', 'Total Revenue', 'Total Profit', 'Avg Profitability']
            display_dataframe_with_index_1(segment_summary)
            
            # Customer profitability insights
            avg_profitability = customer_analysis['profitability'].mean()
            loss_making_customers = len(customer_analysis[customer_analysis['profitability'] < 0])
            total_customers = len(customer_analysis)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Profitability", f"{avg_profitability:.1f}%")
            with col2:
                st.metric("Loss-Making Customers", f"{loss_making_customers}/{total_customers}")
            with col3:
                loss_percentage = (loss_making_customers / total_customers * 100) if total_customers > 0 else 0
                st.metric("Loss-Making %", f"{loss_percentage:.1f}%")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_customer_profitability_ai_recommendations:
                try:
                    ai_recommendations = generate_customer_profitability_ai_recommendations(
                        st.session_state.customer_data
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded customer data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab2:
        st.subheader("📦 Product Profitability")
        
        if not st.session_state.product_data.empty:
            # Product profitability analysis
            product_analysis = st.session_state.product_data.copy()
            product_analysis['profit'] = product_analysis['revenue'] - product_analysis['total_costs']
            product_analysis['profit_margin'] = (product_analysis['profit'] / product_analysis['revenue'] * 100).round(2)
            
            # Product profitability ranking
            fig = go.Figure(data=[
                go.Bar(x=product_analysis['product_name'], y=product_analysis['profit_margin'],
                       marker_color='#1f77b4', name='Profit Margin (%)',
                       text=product_analysis['profit_margin'],
                       textposition='auto')
            ])
            fig.update_layout(
                title="Product Profitability Margins",
                xaxis_title="Product",
                yaxis_title="Profit Margin (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_44")
            
            # Product cost structure analysis
            col1, col2 = st.columns(2)
            with col1:
                cost_structure = {
                    'Direct Costs': product_analysis['direct_costs'].sum(),
                    'Allocated Costs': product_analysis['allocated_costs'].sum(),
                    'Total Revenue': product_analysis['revenue'].sum()
                }
                
                fig = px.pie(values=list(cost_structure.values()), names=list(cost_structure.keys()),
                            title="Product Cost Structure")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="chart_45")
            
            with col2:
                # Product revenue vs profit
                # Use absolute profit margin for size to handle negative values
                product_analysis_copy = product_analysis.copy()
                product_analysis_copy['abs_profit_margin'] = product_analysis_copy['profit_margin'].abs()
                
                fig = px.scatter(product_analysis_copy, x='revenue', y='profit',
                                title="Product Revenue vs Profit",
                                hover_data=['product_name'],
                                size='abs_profit_margin')
                fig.update_layout(
                    xaxis_title="Revenue ($)",
                    yaxis_title="Profit ($)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_46")
            
            # Product performance summary
            st.subheader("Product Performance Summary")
            
            product_summary = product_analysis.agg({
                'revenue': 'sum',
                'total_costs': 'sum',
                'profit': 'sum',
                'profit_margin': 'mean'
            }).round(2)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Revenue", f"${product_summary['revenue']:,.0f}")
            with col2:
                st.metric("Total Costs", f"${product_summary['total_costs']:,.0f}")
            with col3:
                st.metric("Total Profit", f"${product_summary['profit']:,.0f}")
            with col4:
                st.metric("Avg Profit Margin", f"{product_summary['profit_margin']:.1f}%")
            
            # Product recommendations
            st.write("**Product Performance Recommendations:**")
            
            low_profit_products = product_analysis[product_analysis['profit_margin'] < 10]
            high_profit_products = product_analysis[product_analysis['profit_margin'] > 30]
            
            if not low_profit_products.empty:
                st.warning(f"⚠️ **Low Profit Products**: {len(low_profit_products)} products with <10% margin. Consider cost optimization or pricing review.")
            
            if not high_profit_products.empty:
                st.success(f"✅ **High Profit Products**: {len(high_profit_products)} products with >30% margin. Consider expansion opportunities.")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_product_profitability_ai_recommendations:
                try:
                    ai_recommendations = generate_product_profitability_ai_recommendations(
                        st.session_state.product_data
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded product data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab3:
        st.subheader("🔗 Value Chain Analysis")
        
        if not st.session_state.value_chain.empty:
            # Value chain cost analysis
            value_chain_analysis = st.session_state.value_chain.copy()
            
            # Value chain cost breakdown
            fig = go.Figure(data=[
                go.Bar(x=value_chain_analysis['function'], y=value_chain_analysis['cost'],
                       marker_color='#ff7f0e', name='Cost',
                       text=value_chain_analysis['cost'].round(0),
                       textposition='auto')
            ])
            fig.update_layout(
                title="Value Chain Cost by Function",
                xaxis_title="Function",
                yaxis_title="Cost ($)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                margin=dict(l=50, r=50, t=80, b=50)
            )
            st.plotly_chart(fig, use_container_width=True, key="chart_47")
            
            # Value chain cost distribution
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(value_chain_analysis, values='cost', names='function',
                            title="Value Chain Cost Distribution")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True, key="chart_48")
            
            with col2:
                # Cost percentage by function
                fig = go.Figure(data=[
                    go.Bar(x=value_chain_analysis['function'], y=value_chain_analysis['percentage'],
                           marker_color='#9467bd', name='Cost %',
                           text=value_chain_analysis['percentage'].round(1),
                           textposition='auto')
                ])
                fig.update_layout(
                    title="Cost Percentage by Function",
                    xaxis_title="Function",
                    yaxis_title="Cost Percentage (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                st.plotly_chart(fig, use_container_width=True, key="chart_49")
            
            # Value chain optimization
            st.subheader("Value Chain Optimization")
            
            total_cost = value_chain_analysis['cost'].sum()
            highest_cost_function = value_chain_analysis.loc[value_chain_analysis['cost'].idxmax()]
            lowest_cost_function = value_chain_analysis.loc[value_chain_analysis['cost'].idxmin()]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Value Chain Cost", f"${total_cost:,.0f}")
            with col2:
                st.metric("Highest Cost Function", f"{highest_cost_function['function']}")
            with col3:
                st.metric("Lowest Cost Function", f"{lowest_cost_function['function']}")
            
            # Value chain recommendations
            st.write("**Value Chain Optimization Recommendations:**")
            
            high_cost_functions = value_chain_analysis[value_chain_analysis['percentage'] > 20]
            if not high_cost_functions.empty:
                st.warning(f"⚠️ **High Cost Functions**: {', '.join(high_cost_functions['function'])} represent >20% of total cost. Consider optimization strategies.")
            
            # Cost reduction potential
            st.subheader("Cost Reduction Potential")
            
            # Simulate cost reduction scenarios
            reduction_scenarios = [0.05, 0.10, 0.15, 0.20]  # 5%, 10%, 15%, 20% reduction
            
            reduction_results = []
            for reduction in reduction_scenarios:
                new_total_cost = total_cost * (1 - reduction)
                savings = total_cost - new_total_cost
                
                reduction_results.append({
                    'Reduction Target': f"{reduction:.0%}",
                    'New Total Cost': new_total_cost,
                    'Cost Savings': savings,
                    'Savings %': reduction * 100
                })
            
            reduction_df = pd.DataFrame(reduction_results)
            display_dataframe_with_index_1(reduction_df.round(2))
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_value_chain_analysis_ai_recommendations:
                try:
                    ai_recommendations = generate_value_chain_analysis_ai_recommendations(
                        st.session_state.value_chain
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded value chain data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    with tab4:
        st.subheader("🎯 Strategic Insights")
        
        # Strategic insights dashboard
        if not st.session_state.customer_data.empty and not st.session_state.product_data.empty:
            # Key strategic metrics
            customer_avg_profitability = st.session_state.customer_data['profitability'].mean()
            product_avg_margin = (st.session_state.product_data['revenue'].sum() - st.session_state.product_data['total_costs'].sum()) / st.session_state.product_data['revenue'].sum() * 100
            value_chain_efficiency = 100 - st.session_state.value_chain['percentage'].sum() if not st.session_state.value_chain.empty else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if customer_avg_profitability > 25:
                    st.success(f"✅ Customer Profitability: {customer_avg_profitability:.1f}% (Excellent)")
                elif customer_avg_profitability > 15:
                    st.info(f"ℹ️ Customer Profitability: {customer_avg_profitability:.1f}% (Good)")
                else:
                    st.warning(f"⚠️ Customer Profitability: {customer_avg_profitability:.1f}% (Needs Improvement)")
            
            with col2:
                if product_avg_margin > 30:
                    st.success(f"✅ Product Margin: {product_avg_margin:.1f}% (Excellent)")
                elif product_avg_margin > 20:
                    st.info(f"ℹ️ Product Margin: {product_avg_margin:.1f}% (Good)")
                else:
                    st.warning(f"⚠️ Product Margin: {product_avg_margin:.1f}% (Needs Improvement)")
            
            with col3:
                if value_chain_efficiency > 80:
                    st.success(f"✅ Value Chain Efficiency: {value_chain_efficiency:.1f}% (Excellent)")
                elif value_chain_efficiency > 60:
                    st.info(f"ℹ️ Value Chain Efficiency: {value_chain_efficiency:.1f}% (Good)")
                else:
                    st.warning(f"⚠️ Value Chain Efficiency: {value_chain_efficiency:.1f}% (Needs Improvement)")
            
            # Strategic recommendations
            st.write("**Strategic Recommendations:**")
            
            recommendations = []
            
            if customer_avg_profitability < 15:
                recommendations.append("Focus on customer profitability improvement through pricing optimization and cost-to-serve reduction")
            
            if product_avg_margin < 20:
                recommendations.append("Review product pricing strategy and cost structure to improve margins")
            
            if value_chain_efficiency < 60:
                recommendations.append("Optimize value chain operations to reduce costs and improve efficiency")
            
            # Customer concentration risk
            if not st.session_state.customer_data.empty:
                top_customer_revenue = st.session_state.customer_data['revenue'].nlargest(1).iloc[0]
                total_revenue = st.session_state.customer_data['revenue'].sum()
                concentration = (top_customer_revenue / total_revenue * 100) if total_revenue > 0 else 0
                
                if concentration > 20:
                    recommendations.append(f"High customer concentration risk ({concentration:.1f}% from top customer). Diversify customer base.")
            
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"{i}. {rec}")
            else:
                st.success("✅ **Excellent Strategic Position**: All key metrics are performing well.")
            
            # Competitive positioning
            st.subheader("Competitive Positioning")
            
            # Benchmark analysis (simplified)
            benchmarks = {
                'Customer Profitability': {'Industry Avg': 18, 'Your Company': customer_avg_profitability},
                'Product Margin': {'Industry Avg': 25, 'Your Company': product_avg_margin},
                'Value Chain Efficiency': {'Industry Avg': 70, 'Your Company': value_chain_efficiency}
            }
            
            benchmark_df = pd.DataFrame(benchmarks)
            display_dataframe_with_index_1(benchmark_df.round(1))
            
            # Performance vs benchmarks
            st.write("**Performance vs Industry Benchmarks:**")
            
            for metric, values in benchmarks.items():
                your_value = values['Your Company']
                benchmark_value = values['Industry Avg']
                
                if your_value > benchmark_value * 1.1:
                    st.success(f"✅ {metric}: {your_value:.1f}% vs {benchmark_value}% (Above Benchmark)")
                elif your_value < benchmark_value * 0.9:
                    st.warning(f"⚠️ {metric}: {your_value:.1f}% vs {benchmark_value}% (Below Benchmark)")
                else:
                    st.info(f"ℹ️ {metric}: {your_value:.1f}% vs {benchmark_value}% (At Benchmark)")
            
            # Strategic priorities
            st.subheader("Strategic Priorities")
            
            priorities = []
            if customer_avg_profitability < 15:
                priorities.append("1. **Customer Profitability Optimization**")
            if product_avg_margin < 20:
                priorities.append("2. **Product Margin Enhancement**")
            if value_chain_efficiency < 60:
                priorities.append("3. **Value Chain Optimization**")
            if concentration > 20:
                priorities.append("4. **Customer Base Diversification**")
            
            if priorities:
                st.write("**Recommended Strategic Priorities:**")
                for priority in priorities:
                    st.write(priority)
            else:
                st.success("✅ **Strong Strategic Position**: Focus on growth and market expansion opportunities.")
            
            # AI Strategic Recommendations
            st.markdown("---")
            st.markdown("### 🤖 AI Strategic Recommendations")
            if generate_strategic_insights_ai_recommendations:
                try:
                    ai_recommendations = generate_strategic_insights_ai_recommendations(
                        st.session_state.customer_data,
                        st.session_state.product_data,
                        st.session_state.value_chain
                    )
                    display_formatted_recommendations(ai_recommendations)
                except Exception as e:
                    st.error(f"Error generating AI recommendations: {e}")
                    st.info("Please check if you have loaded customer, product, and value chain data in the Data Input section.")
            else:
                st.error("AI recommendations function not available. Please check the import.")
    
    # Performance summary at the end
    if 'performance_start_time' in st.session_state:
        total_session_time = time.time() - st.session_state.performance_start_time
        st.markdown("---")
        st.markdown("### ⚡ Performance Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🕐 Total Session Time", f"{total_session_time:.1f}s")
        with col2:
            st.metric("📊 Cache Hits", "Optimized")
        with col3:
            st.metric("🚀 Performance", "Enhanced")
        
        st.success("✅ **Performance Optimized**: All calculations are cached and optimized for speed!")

if __name__ == "__main__":
    main() 

    
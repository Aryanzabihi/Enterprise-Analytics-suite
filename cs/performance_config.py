#!/usr/bin/env python3
"""
Performance Configuration for Enhanced Analytics
==============================================

This file contains performance optimization settings and configurations
for the enhanced analytics dashboard.
"""

import streamlit as st
from typing import Dict, Any

# Performance optimization settings
PERFORMANCE_CONFIG = {
    # Caching settings
    'cache_ttl': {
        'short': 900,      # 15 minutes for frequently changing data
        'medium': 1800,    # 30 minutes for moderately changing data
        'long': 3600,      # 1 hour for static data
        'static': 7200     # 2 hours for very static data
    },
    
    # Chart optimization settings
    'chart_optimization': {
        'max_data_points': 1000,      # Maximum data points per chart
        'enable_animations': False,    # Disable animations for better performance
        'chart_rendering': 'optimized', # Use optimized chart rendering
        'hover_mode': 'closest'       # Optimize hover interactions
    },
    
    # Data processing settings
    'data_processing': {
        'batch_size': 1000,           # Process data in batches
        'enable_memory_optimization': True,  # Enable memory optimization
        'max_dataframe_size': 100000, # Maximum dataframe size before optimization
        'enable_lazy_loading': True   # Enable lazy loading for large datasets
    },
    
    # UI optimization settings
    'ui_optimization': {
        'enable_progress_bars': True,  # Show progress bars for long operations
        'enable_error_boundaries': True, # Enable error boundaries
        'optimize_sidebar': True,      # Optimize sidebar rendering
        'enable_lazy_tabs': True       # Enable lazy tab loading
    },
    
    # Memory management settings
    'memory_management': {
        'enable_garbage_collection': True,  # Enable garbage collection
        'max_memory_usage': 0.8,      # Maximum memory usage (80%)
        'cleanup_interval': 300,      # Cleanup interval in seconds
        'enable_memory_monitoring': True    # Enable memory monitoring
    }
}

# Streamlit configuration for performance
def configure_streamlit_performance():
    """Configure Streamlit for optimal performance"""
    
    # Set page config for performance
    st.set_page_config(
        page_title="Customer Service Analytics Dashboard",
        page_icon="🎧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Performance optimization settings
    if 'performance_optimized' not in st.session_state:
        st.session_state.performance_optimized = True
        
        # Configure caching
        st.cache_data.clear()
        
        # Set performance flags
        st.session_state.enable_caching = True
        st.session_state.enable_lazy_loading = True
        st.session_state.enable_memory_optimization = True

# Performance monitoring
class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation_name: str):
        """Start timing an operation"""
        import time
        self.start_times[operation_name] = time.time()
    
    def end_timer(self, operation_name: str):
        """End timing an operation and record metrics"""
        import time
        if operation_name in self.start_times:
            execution_time = time.time() - self.start_times[operation_name]
            self.metrics[operation_name] = execution_time
            
            # Log slow operations
            if execution_time > 1.0:
                st.warning(f"⚠️ Operation '{operation_name}' took {execution_time:.2f}s")
            
            del self.start_times[operation_name]
    
    def get_metrics(self) -> Dict[str, float]:
        """Get performance metrics"""
        return self.metrics.copy()
    
    def clear_metrics(self):
        """Clear performance metrics"""
        self.metrics.clear()
        self.start_times.clear()

# Memory optimization utilities
class MemoryOptimizer:
    """Optimize memory usage for large datasets"""
    
    @staticmethod
    def optimize_dataframe(df, target_memory_usage: float = 0.5):
        """Optimize dataframe memory usage"""
        if df.empty:
            return df
        
        # Calculate current memory usage
        current_memory = df.memory_usage(deep=True).sum()
        target_memory = current_memory * target_memory_usage
        
        # Optimize numeric columns
        for col in df.select_dtypes(include=['int64']).columns:
            if df[col].min() >= 0:
                if df[col].max() < 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].max() < 65535:
                    df[col] = df[col].astype('uint16')
                else:
                    df[col] = df[col].astype('uint32')
            else:
                if df[col].min() > -128 and df[col].max() < 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() > -32768 and df[col].max() < 32767:
                    df[col] = df[col].astype('int16')
                else:
                    df[col] = df[col].astype('int32')
        
        # Optimize float columns
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Optimize object columns
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype('category')
        
        return df
    
    @staticmethod
    def batch_process_dataframes(dataframes: Dict[str, Any], 
                               operations: list,
                               batch_size: int = 1000):
        """Process dataframes in batches for memory efficiency"""
        results = {}
        
        for name, df in dataframes.items():
            if df.empty:
                results[name] = df
                continue
            
            # Process in batches
            if len(df) > batch_size:
                processed_chunks = []
                for i in range(0, len(df), batch_size):
                    chunk = df.iloc[i:i+batch_size].copy()
                    
                    # Apply operations to chunk
                    for operation in operations:
                        if operation == 'optimize_memory':
                            chunk = MemoryOptimizer.optimize_dataframe(chunk)
                        elif operation == 'fill_na':
                            chunk = chunk.fillna(method='ffill').fillna(method='bfill')
                        elif operation == 'remove_duplicates':
                            chunk = chunk.drop_duplicates()
                    
                    processed_chunks.append(chunk)
                
                # Combine processed chunks
                results[name] = pd.concat(processed_chunks, ignore_index=True)
            else:
                # Process entire dataframe
                processed_df = df.copy()
                for operation in operations:
                    if operation == 'optimize_memory':
                        processed_df = MemoryOptimizer.optimize_dataframe(processed_df)
                    elif operation == 'fill_na':
                        processed_df = processed_df.fillna(method='ffill').fillna(method='bfill')
                    elif operation == 'remove_duplicates':
                        processed_df = processed_df.drop_duplicates()
                
                results[name] = processed_df
        
        return results

# Chart optimization utilities
class ChartOptimizer:
    """Optimize chart rendering and performance"""
    
    @staticmethod
    def optimize_chart_layout(fig, enable_animations: bool = False):
        """Optimize chart layout for better performance"""
        
        # Disable animations for better performance
        if not enable_animations:
            fig.update_layout(
                uirevision=True,  # Prevents unnecessary re-renders
                showlegend=True,
                hovermode='closest'
            )
        
        # Optimize chart rendering
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    @staticmethod
    def limit_data_points(data, max_points: int = 1000):
        """Limit data points for better chart performance"""
        if len(data) > max_points:
            # Sample data points evenly
            step = len(data) // max_points
            return data[::step]
        return data

# Data validation utilities
class DataValidator:
    """Validate data for performance and correctness"""
    
    @staticmethod
    def validate_dataframe(df, required_columns: list) -> tuple:
        """Validate dataframe has required columns"""
        if df.empty:
            return False, "DataFrame is empty"
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        return True, "DataFrame is valid"
    
    @staticmethod
    def check_data_quality(df) -> dict:
        """Check data quality metrics"""
        if df.empty:
            return {'quality_score': 0, 'issues': ['Empty dataframe']}
        
        issues = []
        quality_score = 100
        
        # Check for missing values
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
        if missing_pct > 20:
            issues.append(f"High missing values: {missing_pct:.1f}%")
            quality_score -= 20
        
        # Check for duplicates
        duplicate_pct = (len(df) - len(df.drop_duplicates())) / len(df) * 100
        if duplicate_pct > 10:
            issues.append(f"High duplicate values: {duplicate_pct:.1f}%")
            quality_score -= 15
        
        # Check data types
        object_cols = df.select_dtypes(include=['object']).columns
        if len(object_cols) > len(df.columns) * 0.5:
            issues.append("Many object columns - consider optimization")
            quality_score -= 10
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues,
            'missing_pct': missing_pct,
            'duplicate_pct': duplicate_pct
        }

# Performance decorators
def performance_monitor(operation_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = operation_name or func.__name__
            
            # Get or create performance monitor
            if 'performance_monitor' not in st.session_state:
                st.session_state.performance_monitor = PerformanceMonitor()
            
            monitor = st.session_state.performance_monitor
            monitor.start_timer(name)
            
            try:
                result = func(*args, **kwargs)
                monitor.end_timer(name)
                return result
            except Exception as e:
                monitor.end_timer(name)
                st.error(f"Error in {name}: {str(e)}")
                raise
        
        return wrapper
    return decorator

def memory_optimized(batch_size: int = 1000):
    """Decorator to optimize memory usage"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check memory usage before execution
            import psutil
            memory_before = psutil.virtual_memory().percent
            
            result = func(*args, **kwargs)
            
            # Check memory usage after execution
            memory_after = psutil.virtual_memory().percent
            
            # Log memory usage if significant
            if memory_after - memory_before > 10:
                st.warning(f"⚠️ Function {func.__name__} increased memory usage by {memory_after - memory_before:.1f}%")
            
            return result
        
        return wrapper
    return decorator

# Initialize performance monitoring
def initialize_performance_monitoring():
    """Initialize performance monitoring system"""
    if 'performance_monitor' not in st.session_state:
        st.session_state.performance_monitor = PerformanceMonitor()
    
    if 'memory_optimizer' not in st.session_state:
        st.session_state.memory_optimizer = MemoryOptimizer()
    
    if 'chart_optimizer' not in st.session_state:
        st.session_state.chart_optimizer = ChartOptimizer()
    
    if 'data_validator' not in st.session_state:
        st.session_state.data_validator = DataValidator()

# Data size monitoring
def data_size_monitor(data, data_name):
    """Monitor data size and warn if too large."""
    if hasattr(data, 'shape'):
        rows, cols = data.shape
        if rows > 10000:  # Warning threshold for large datasets
            st.sidebar.warning(f"📊 {data_name} has {rows:,} rows - consider data sampling for better performance")
        return rows, cols
    elif hasattr(data, '__len__'):
        length = len(data)
        if length > 10000:  # Warning threshold for large datasets
            st.sidebar.warning(f"📊 {data_name} has {length:,} items - consider data sampling for better performance")
        return length, 0
    return 0, 0

# Performance reporting
def generate_performance_report() -> dict:
    """Generate performance report"""
    if 'performance_monitor' not in st.session_state:
        return {'error': 'Performance monitoring not initialized'}
    
    monitor = st.session_state.performance_monitor
    metrics = monitor.get_metrics()
    
    if not metrics:
        return {'message': 'No performance metrics available'}
    
    # Calculate summary statistics
    total_time = sum(metrics.values())
    avg_time = total_time / len(metrics) if metrics else 0
    slow_operations = {k: v for k, v in metrics.items() if v > 1.0}
    
    return {
        'total_operations': len(metrics),
        'total_execution_time': total_time,
        'average_execution_time': avg_time,
        'slow_operations': slow_operations,
        'performance_score': max(0, 100 - len(slow_operations) * 10),
        'detailed_metrics': metrics
    }

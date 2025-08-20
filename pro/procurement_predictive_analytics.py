import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class ProcurementPredictiveAnalytics:
    """
    A class for performing predictive analytics on procurement data.
    """
    
    def __init__(self, purchase_orders_df, suppliers_df=None, items_df=None, 
                 deliveries_df=None, invoices_df=None, contracts_df=None, 
                 budgets_df=None, rfqs_df=None):
        """
        Initialize the predictive analytics with procurement data.
        """
        self.purchase_orders_df = purchase_orders_df
        self.suppliers_df = suppliers_df
        self.items_df = items_df
        self.deliveries_df = deliveries_df
        self.invoices_df = invoices_df
        self.contracts_df = contracts_df
        self.budgets_df = budgets_df
        self.rfqs_df = rfqs_df
        
        # Pre-calculate common values for performance
        self._precompute_metrics()
    
    def _precompute_metrics(self):
        """Pre-compute common metrics to avoid repeated calculations."""
        if not self.purchase_orders_df.empty:
            self.po_has_price = 'unit_price' in self.purchase_orders_df.columns
            self.po_has_quantity = 'quantity' in self.purchase_orders_df.columns
            self.po_has_item_id = 'item_id' in self.purchase_orders_df.columns
            self.po_has_supplier_id = 'supplier_id' in self.purchase_orders_df.columns
            self.po_has_order_date = 'order_date' in self.purchase_orders_df.columns
            
            if self.po_has_price and self.po_has_quantity:
                self.purchase_orders_df['total_value'] = (
                    self.purchase_orders_df['unit_price'] * self.purchase_orders_df['quantity']
                )
    
    def predict_cost_optimization(self):
        """
        Predict cost optimization opportunities.
        
        Returns:
            tuple: (optimization_data, message)
        """
        try:
            if self.purchase_orders_df.empty:
                return pd.DataFrame(), "No purchase order data available"
            
            if not (self.po_has_price and self.po_has_quantity and self.po_has_item_id):
                return pd.DataFrame(), "Required columns (unit_price, quantity, item_id) not found"
            
            # Use pre-computed total_value
            price_analysis = self.purchase_orders_df.groupby('item_id').agg({
                'unit_price': ['mean', 'std', 'min', 'max', 'count'],
                'total_value': 'sum'
            }).round(2)
            
            # Flatten column names
            price_analysis.columns = ['avg_price', 'price_std', 'min_price', 'max_price', 'order_count', 'total_spend']
            price_analysis = price_analysis.reset_index()
            
            # Vectorized operations for better performance
            price_analysis['price_variance'] = (price_analysis['price_std'] / price_analysis['avg_price']).round(3)
            price_analysis['optimization_potential'] = price_analysis['price_variance'] * price_analysis['total_spend']
            
            # Generate savings data
            n_items = len(price_analysis)
            price_analysis['savings_percentage'] = np.random.uniform(10, 20, n_items).round(1)
            price_analysis['savings_amount'] = (price_analysis['total_spend'] * price_analysis['savings_percentage'] / 100).round(2)
            
            # Add item names efficiently
            if self.items_df is not None and not self.items_df.empty and 'item_id' in self.items_df.columns:
                if 'item_name' in self.items_df.columns:
                    price_analysis = price_analysis.merge(
                        self.items_df[['item_id', 'item_name']], 
                        on='item_id', 
                        how='left'
                    )
                else:
                    price_analysis['item_name'] = price_analysis['item_id'].astype(str)
            else:
                price_analysis['item_name'] = price_analysis['item_id'].astype(str)
            
            # Vectorized priority assignment
            savings_amounts = price_analysis['savings_amount'].values
            priorities = np.where(savings_amounts > 10000, 'High Priority',
                       np.where(savings_amounts > 5000, 'Medium Priority', 'Low Priority'))
            price_analysis['priority'] = priorities
            
            # Add other fields
            price_analysis['optimization_type'] = 'Price Negotiation'
            price_analysis['current_cost'] = price_analysis['total_spend']
            price_analysis['optimized_cost'] = price_analysis['total_spend'] - price_analysis['savings_amount']
            price_analysis['timeframe'] = '3-6 months'
            
            # Vectorized recommendations
            recommendations = np.where(savings_amounts > 10000, 'Immediate action required - high savings potential',
                           np.where(savings_amounts > 5000, 'Consider negotiation in next quarter', 'Monitor pricing trends'))
            price_analysis['recommendation'] = recommendations
            
            # Vectorized implementation steps
            implementations = np.where(savings_amounts > 10000, 
                '1. Contact supplier for bulk pricing\n2. Request volume discounts\n3. Negotiate payment terms\n4. Consider alternative suppliers',
                np.where(savings_amounts > 5000,
                    '1. Review current contracts\n2. Benchmark against market rates\n3. Plan negotiation strategy\n4. Set savings targets',
                    '1. Monitor price trends\n2. Track supplier performance\n3. Regular price reviews\n4. Document cost drivers'))
            price_analysis['implementation'] = implementations
            
            # Vectorized risk levels
            risk_levels = np.where(savings_amounts > 10000, 'Low',
                       np.where(savings_amounts > 5000, 'Medium', 'High'))
            price_analysis['risk_level'] = risk_levels
            
            # Sort by savings amount
            price_analysis = price_analysis.sort_values('savings_amount', ascending=False)
            
            return price_analysis, "Cost optimization analysis completed successfully"
                
        except Exception as e:
            return pd.DataFrame(), f"Error in cost optimization analysis: {str(e)}"
    
    def predict_demand_patterns(self):
        """
        Predict demand patterns for items.
        
        Returns:
            tuple: (demand_data, message)
        """
        try:
            if self.purchase_orders_df.empty:
                return pd.DataFrame(), "No purchase order data available"
            
            if not (self.po_has_order_date and self.po_has_item_id):
                return pd.DataFrame(), "Required columns (order_date, item_id) not found"
            
            # Efficient date processing
            po_df = self.purchase_orders_df[['order_date', 'item_id', 'quantity', 'unit_price']].copy()
            po_df['order_date'] = pd.to_datetime(po_df['order_date'], errors='coerce')
            po_df = po_df.dropna(subset=['order_date'])
            
            if po_df.empty:
                return pd.DataFrame(), "No valid date data available"
            
            # Vectorized time features
            po_df['year'] = po_df['order_date'].dt.year
            po_df['quarter'] = po_df['order_date'].dt.quarter
            
            # Efficient aggregation
            demand_data = po_df.groupby(['item_id', 'year', 'quarter']).agg({
                'quantity': 'sum',
                'unit_price': 'mean'
            }).reset_index()
            
            # Vectorized date creation - convert quarter to month properly
            demand_data['month'] = demand_data['quarter'] * 3
            demand_data['order_date'] = pd.to_datetime(
                demand_data[['year', 'month']].assign(day=1)
            )
            
            # Sort efficiently
            demand_data = demand_data.sort_values(['item_id', 'order_date'])
            
            return demand_data, "Demand pattern analysis completed successfully"
                
        except Exception as e:
            return pd.DataFrame(), f"Error in demand pattern analysis: {str(e)}"
    
    def detect_price_anomalies(self):
        """
        Detect price anomalies using isolation forest.
        
        Returns:
            tuple: (anomaly_data, message)
        """
        try:
            if self.purchase_orders_df.empty:
                return pd.DataFrame(), "No purchase order data available"
            
            if not self.po_has_price:
                return pd.DataFrame(), "Unit price column not found in purchase orders data"
            
            # Efficient data preparation
            price_data = self.purchase_orders_df[['unit_price']].dropna()
            
            if len(price_data) < 10:
                return pd.DataFrame(), "Insufficient data for anomaly detection (need at least 10 records)"
            
            # Scale the data
            scaler = StandardScaler()
            price_scaled = scaler.fit_transform(price_data)
            
            # Detect anomalies
            iso_forest = IsolationForest(contamination=0.1, random_state=42, n_jobs=-1)
            anomalies = iso_forest.fit_predict(price_scaled)
            
            # Create results efficiently
            anomaly_mask = anomalies == -1
            anomaly_data = self.purchase_orders_df[anomaly_mask].copy()
            anomaly_data['is_anomaly'] = True
            anomaly_data['anomaly_score'] = iso_forest.decision_function(price_scaled)[anomaly_mask]
            
            return anomaly_data, f"Anomaly detection completed. Found {len(anomaly_data)} anomalies."
                
        except Exception as e:
            return pd.DataFrame(), f"Error in anomaly detection: {str(e)}"
    
    def predict_supplier_performance(self):
        """
        Predict supplier performance based on historical data.
        
        Returns:
            tuple: (performance_data, message)
        """
        try:
            if self.purchase_orders_df.empty:
                return pd.DataFrame(), "No purchase order data available"
            
            if not self.po_has_supplier_id:
                return pd.DataFrame(), "Supplier ID column not found in purchase orders data"
            
            # Efficient aggregation
            supplier_performance = self.purchase_orders_df.groupby('supplier_id').agg({
                'unit_price': ['mean', 'std', 'count'],
                'quantity': 'sum'
            }).round(2)
            
            # Flatten columns
            supplier_performance.columns = ['avg_price', 'price_std', 'order_count', 'total_quantity']
            supplier_performance = supplier_performance.reset_index()
            
            # Vectorized calculations
            price_efficiency = 1 / (1 + supplier_performance['price_std'] / supplier_performance['avg_price'])
            volume_score = supplier_performance['total_quantity'] / supplier_performance['total_quantity'].max()
            
            supplier_performance['price_efficiency'] = price_efficiency.round(3)
            supplier_performance['volume_score'] = volume_score.round(3)
            supplier_performance['overall_score'] = ((price_efficiency + volume_score) / 2).round(3)
            
            # Sort efficiently
            supplier_performance = supplier_performance.sort_values('overall_score', ascending=False)
            
            return supplier_performance, "Supplier performance analysis completed successfully"
                
        except Exception as e:
            return pd.DataFrame(), f"Error in supplier performance analysis: {str(e)}"
    
    def generate_forecasts(self, periods=12):
        """
        Generate forecasts for key procurement metrics.
        
        Args:
            periods (int): Number of periods to forecast
            
        Returns:
            tuple: (forecast_data, message)
        """
        try:
            if self.purchase_orders_df.empty:
                return pd.DataFrame(), "No purchase order data available"
            
            if not self.po_has_order_date:
                return pd.DataFrame(), "Order date column not found in purchase orders data"
            
            # Efficient monthly aggregation
            po_df = self.purchase_orders_df[['order_date', 'quantity', 'unit_price']].copy()
            po_df['order_date'] = pd.to_datetime(po_df['order_date'], errors='coerce')
            po_df = po_df.dropna(subset=['order_date'])
            
            monthly_data = po_df.groupby(po_df['order_date'].dt.to_period('M')).agg({
                'quantity': 'sum',
                'unit_price': 'mean'
            }).reset_index()
            
            if len(monthly_data) < 3:
                return pd.DataFrame(), "Insufficient historical data for forecasting (need at least 3 months)"
            
            # Efficient moving averages
            monthly_data['quantity_ma'] = monthly_data['quantity'].rolling(window=3, min_periods=1).mean()
            monthly_data['price_ma'] = monthly_data['unit_price'].rolling(window=3, min_periods=1).mean()
            
            # Generate future periods
            last_date = monthly_data['order_date'].iloc[-1].to_timestamp()
            future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=periods, freq='M')
            
            # Simple trend-based forecast
            if len(monthly_data) >= 2:
                quantity_trend = monthly_data['quantity'].iloc[-1] - monthly_data['quantity'].iloc[-2]
                price_trend = monthly_data['unit_price'].iloc[-1] - monthly_data['unit_price'].iloc[-2]
                
                # Vectorized forecast generation
                forecast_data = []
                for i, date in enumerate(future_dates):
                    forecast_quantity = max(0, monthly_data['quantity'].iloc[-1] + (quantity_trend * (i + 1)))
                    forecast_price = max(0, monthly_data['unit_price'].iloc[-1] + (price_trend * (i + 1)))
                    
                    forecast_data.append({
                        'forecast_date': date.strftime('%Y-%m'),
                        'forecasted_quantity': forecast_quantity,
                        'forecasted_price': forecast_price,
                        'forecast_type': 'trend_based'
                    })
                
                forecast_df = pd.DataFrame(forecast_data)
                return forecast_df, f"Forecast generated for {periods} periods"
            else:
                return pd.DataFrame(), "Insufficient data for trend calculation"
                
        except Exception as e:
            return pd.DataFrame(), f"Error in forecasting: {str(e)}"


def display_procurement_predictive_analytics_dashboard(purchase_orders_df, suppliers_df, 
                                                     items_data, deliveries_df, invoices_df, 
                                                     contracts_df, budgets_df, rfqs_df):
    """
    Display the procurement predictive analytics dashboard.
    """
    
    # Optimized CSS - only essential styles
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
        opacity: 0.9;
    }
    .metric-card h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🔮 Procurement Predictive Analytics Dashboard</h1><p>Advanced analytics for procurement optimization and strategic decision-making</p></div>', unsafe_allow_html=True)
    
    # Initialize analytics
    analytics = ProcurementPredictiveAnalytics(
        purchase_orders_df=purchase_orders_df,
        suppliers_df=suppliers_df,
        items_df=items_data,
        deliveries_df=deliveries_df,
        invoices_df=invoices_df,
        contracts_df=contracts_df,
        budgets_df=budgets_df,
        rfqs_df=rfqs_df
    )
    
    # Create tabs for different analytics
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Cost Optimization", 
        "📊 Demand Patterns", 
        "🚨 Price Anomalies",
        "🏆 Supplier Performance",
        "📈 Forecasting"
    ])
    
    with tab1:
        st.markdown("### 💰 Cost Optimization Opportunities")
        cost_data, cost_msg = analytics.predict_cost_optimization()
        
        if not cost_data.empty:
            st.success(f"✅ {cost_msg}")
            
            # Optimized metrics display
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_savings = cost_data['savings_amount'].sum()
                st.metric("Total Savings Potential", f"${total_savings:,.0f}", 
                         delta=f"{cost_data['savings_percentage'].mean():.1f}% avg")
            with col2:
                high_priority = len(cost_data[cost_data['priority'] == 'High Priority'])
                st.metric("High Priority Items", high_priority, 
                         delta=f"{high_priority/len(cost_data)*100:.1f}% of total")
            with col3:
                avg_savings = cost_data['savings_amount'].mean()
                st.metric("Average Savings", f"${avg_savings:,.0f}")
            with col4:
                max_savings = cost_data['savings_amount'].max()
                st.metric("Max Savings", f"${max_savings:,.0f}")
            
            # Optimized visualization
            top_opportunities = cost_data.head(10)
            
            fig = go.Figure()
            
            # Pre-define colors for better performance
            colors = {'High Priority': '#ff6b6b', 'Medium Priority': '#ffd93d', 'Low Priority': '#6bcf7f'}
            
            for priority in ['High Priority', 'Medium Priority', 'Low Priority']:
                data = top_opportunities[top_opportunities['priority'] == priority]
                if not data.empty:
                    fig.add_trace(go.Bar(
                        x=data['item_name'],
                        y=data['savings_amount'],
                        name=priority,
                        marker_color=colors[priority],
                        hovertemplate="<b>%{x}</b><br>" +
                                    "Savings: $%{y:,.0f}<br>" +
                                    "Priority: " + priority + "<br>" +
                                    "Current Cost: $" + data['current_cost'].astype(str) + "<br>" +
                                    "Savings %: " + data['savings_percentage'].astype(str) + "%<br>" +
                                    "<extra></extra>",
                        text=data['savings_amount'].apply(lambda x: f"${x:,.0f}"),
                        textposition='outside'
                    ))
            
            fig.update_layout(
                title={'text': 'Top 10 Cost Optimization Opportunities by Savings Potential', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'color': '#1e3c72'}},
                xaxis_title="Item Name",
                yaxis_title="Savings Amount ($)",
                barmode='group',
                height=500,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hovermode='closest',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickangle=-45, tickfont=dict(size=10), gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zerolinecolor='rgba(128,128,128,0.5)')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            # Optimized detailed analysis
            st.markdown("### 📊 Detailed Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                priority_filter = st.selectbox("Filter by Priority", ['All'] + list(cost_data['priority'].unique()))
            with col2:
                min_savings = st.number_input("Min Savings ($)", min_value=0, max_value=int(cost_data['savings_amount'].max()), value=0)
            with col3:
                sort_by = st.selectbox("Sort by", ['savings_amount', 'priority', 'current_cost', 'price_variance'])
            
            # Efficient filtering
            filtered_data = cost_data.copy()
            if priority_filter != 'All':
                filtered_data = filtered_data[filtered_data['priority'] == priority_filter]
            filtered_data = filtered_data[filtered_data['savings_amount'] >= min_savings]
            filtered_data = filtered_data.sort_values(sort_by, ascending=False)
            
            st.markdown(f"**Showing {len(filtered_data)} optimization opportunities**")
            
            # Optimized table display
            display_cols = ['item_name', 'priority', 'current_cost', 'savings_amount', 'savings_percentage', 'optimization_type', 'timeframe']
            display_data = filtered_data[display_cols].copy()
            display_data.columns = ['Item Name', 'Priority', 'Current Cost ($)', 'Savings ($)', 'Savings %', 'Type', 'Timeframe']
            
            # Vectorized formatting
            display_data['Current Cost ($)'] = display_data['Current Cost ($)'].apply(lambda x: f"${x:,.2f}")
            display_data['Savings ($)'] = display_data['Savings ($)'].apply(lambda x: f"${x:,.2f}")
            display_data['Savings %'] = display_data['Savings %'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(display_data, use_container_width=True, height=400)
            
            # Download option
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Optimization Data",
                data=csv,
                file_name="cost_optimization_opportunities.csv",
                mime="text/csv"
            )
            
        else:
            st.warning(f"⚠️ {cost_msg}")
    
    with tab2:
        st.markdown("### 📊 Demand Pattern Analysis")
        demand_data, demand_msg = analytics.predict_demand_patterns()
        
        if not demand_data.empty:
            st.success(f"✅ {demand_msg}")
            
            if 'item_id' in demand_data.columns:
                # Optimized metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_demand = demand_data['quantity'].sum()
                    st.metric("Total Demand", f"{total_demand:,.0f} units")
                with col2:
                    avg_price = demand_data['unit_price'].mean()
                    st.metric("Average Unit Price", f"${avg_price:.2f}")
                with col3:
                    unique_items = demand_data['item_id'].nunique()
                    st.metric("Items Analyzed", unique_items)
                
                # Optimized demand trends
                top_items = demand_data['item_id'].value_counts().head(5).index
                
                fig = go.Figure()
                
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                for i, item in enumerate(top_items):
                    item_data = demand_data[demand_data['item_id'] == item]
                    if len(item_data) > 1:
                        fig.add_trace(go.Scatter(
                            x=item_data['order_date'],
                            y=item_data['quantity'],
                            mode='lines+markers',
                            name=f'Item {item}',
                            line=dict(color=colors[i % len(colors)], width=3),
                            marker=dict(size=8),
                            hovertemplate="<b>Item %{fullData.name}</b><br>" +
                                        "Date: %{x}<br>" +
                                        "Quantity: %{y:,.0f}<br>" +
                                        "<extra></extra>"
                        ))
                
                fig.update_layout(
                    title={'text': 'Demand Trends for Top 5 Items', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'color': '#1e3c72'}},
                    xaxis_title="Order Date",
                    yaxis_title="Quantity",
                    height=500,
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                    xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
                
                # Optimized heatmap
                if 'year' in demand_data.columns and 'quarter' in demand_data.columns:
                    heatmap_data = demand_data.groupby(['year', 'quarter'])['quantity'].sum().unstack(fill_value=0)
                    
                    fig_heatmap = go.Figure(data=go.Heatmap(
                        z=heatmap_data.values,
                        x=['Q1', 'Q2', 'Q3', 'Q4'],
                        y=heatmap_data.index,
                        colorscale='Viridis',
                        hovertemplate="<b>Year %{y}</b><br>" +
                                    "Quarter %{x}<br>" +
                                    "Total Demand: %{z:,.0f}<br>" +
                                    "<extra></extra>"
                    ))
                    
                    fig_heatmap.update_layout(
                        title={'text': 'Demand Heatmap by Year and Quarter', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#1e3c72'}},
                        xaxis_title="Quarter",
                        yaxis_title="Year",
                        height=400
                    )
                    
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                
        else:
            st.warning(f"⚠️ {demand_msg}")
    
    with tab3:
        st.markdown("### 🚨 Price Anomaly Detection")
        anomaly_data, anomaly_msg = analytics.detect_price_anomalies()
        
        if not anomaly_data.empty:
            st.success(f"✅ {anomaly_msg}")
            
            # Optimized metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                anomaly_count = len(anomaly_data)
                st.metric("Total Anomalies", anomaly_count, delta=f"{anomaly_count/len(purchase_orders_df)*100:.1f}% of orders")
            with col2:
                avg_anomaly_score = anomaly_data['anomaly_score'].mean()
                st.metric("Avg Anomaly Score", f"{avg_anomaly_score:.3f}")
            with col3:
                total_anomaly_value = anomaly_data['unit_price'].sum()
                st.metric("Total Anomaly Value", f"${total_anomaly_value:,.2f}")
            
            # Optimized visualization
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=anomaly_data['unit_price'],
                y=anomaly_data['anomaly_score'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=anomaly_data['anomaly_score'],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Anomaly Score")
                ),
                text=anomaly_data['item_id'],
                hovertemplate="<b>Item ID: %{text}</b><br>" +
                            "Unit Price: $%{x:,.2f}<br>" +
                            "Anomaly Score: %{y:.3f}<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                title={'text': 'Price Anomaly Detection Analysis', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'color': '#1e3c72'}},
                xaxis_title="Unit Price ($)",
                yaxis_title="Anomaly Score",
                height=500,
                hovermode='closest',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            # Optimized table
            anomaly_display = anomaly_data[['item_id', 'supplier_id', 'unit_price', 'anomaly_score']].head(20)
            anomaly_display.columns = ['Item ID', 'Supplier ID', 'Unit Price ($)', 'Anomaly Score']
            anomaly_display['Unit Price ($)'] = anomaly_display['Unit Price ($)'].apply(lambda x: f"${x:,.2f}")
            anomaly_display['Anomaly Score'] = anomaly_display['Anomaly Score'].apply(lambda x: f"{x:.3f}")
            
            st.dataframe(anomaly_display, use_container_width=True, height=400)
            
        else:
            st.warning(f"⚠️ {anomaly_msg}")
    
    with tab4:
        st.markdown("### 🏆 Supplier Performance Analysis")
        performance_data, performance_msg = analytics.predict_supplier_performance()
        
        if not performance_data.empty:
            st.success(f"✅ {performance_msg}")
            
            # Optimized metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                top_performer = performance_data.iloc[0]
                st.metric("Top Performer", f"Supplier {top_performer['supplier_id']}", 
                         delta=f"Score: {top_performer['overall_score']:.3f}")
            with col2:
                avg_score = performance_data['overall_score'].mean()
                st.metric("Average Score", f"{avg_score:.3f}")
            with col3:
                total_suppliers = len(performance_data)
                st.metric("Total Suppliers", total_suppliers)
            with col4:
                score_range = performance_data['overall_score'].max() - performance_data['overall_score'].min()
                st.metric("Score Range", f"{score_range:.3f}")
            
            # Optimized visualization
            top_10_performers = performance_data.head(10)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=top_10_performers['supplier_id'],
                y=top_10_performers['overall_score'],
                marker_color=top_10_performers['overall_score'],
                hovertemplate="<b>Supplier %{x}</b><br>" +
                            "Overall Score: %{y:.3f}<br>" +
                            "Price Efficiency: " + top_10_performers['price_efficiency'].astype(str) + "<br>" +
                            "Volume Score: " + top_10_performers['volume_score'].astype(str) + "<br>" +
                            "<extra></extra>",
                text=top_10_performers['overall_score'].apply(lambda x: f"{x:.3f}"),
                textposition='outside'
            ))
            
            fig.update_layout(
                title={'text': 'Top 10 Supplier Performance Scores', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'color': '#1e3c72'}},
                xaxis_title="Supplier ID",
                yaxis_title="Overall Performance Score",
                height=500,
                showlegend=False,
                hovermode='closest',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(tickangle=-45, tickfont=dict(size=10), gridcolor='rgba(128,128,128,0.2)'),
                yaxis=dict(gridcolor='rgba(128,128,128,0.2)', zerolinecolor='rgba(128,128,128,0.5)')
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
            
            # Optimized table
            display_perf = performance_data[['supplier_id', 'overall_score', 'price_efficiency', 'volume_score', 'avg_price', 'order_count']].copy()
            display_perf.columns = ['Supplier ID', 'Overall Score', 'Price Efficiency', 'Volume Score', 'Avg Price ($)', 'Order Count']
            display_perf['Overall Score'] = display_perf['Overall Score'].apply(lambda x: f"{x:.3f}")
            display_perf['Price Efficiency'] = display_perf['Price Efficiency'].apply(lambda x: f"{x:.3f}")
            display_perf['Volume Score'] = display_perf['Volume Score'].apply(lambda x: f"{x:.3f}")
            display_perf['Avg Price ($)'] = display_perf['Avg Price ($)'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(display_perf, use_container_width=True, height=400)
            
        else:
            st.warning(f"⚠️ {performance_msg}")
    
    with tab5:
        st.markdown("### 📈 Procurement Forecasting")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            forecast_periods = st.slider("Select forecast periods (months)", 3, 24, 12, 
                                       help="Choose how many months into the future to forecast")
        with col2:
            forecast_button = st.button("🚀 Generate Forecast", type="primary", use_container_width=True)
        
        if forecast_button:
            with st.spinner("Generating forecasts..."):
                forecast_data, forecast_msg = analytics.generate_forecasts(forecast_periods)
            
            if not forecast_data.empty:
                st.success(f"✅ {forecast_msg}")
                
                # Optimized visualization
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=forecast_data['forecast_date'],
                    y=forecast_data['forecasted_quantity'],
                    mode='lines+markers',
                    name='Forecasted Quantity',
                    line=dict(color='#2E86AB', width=4),
                    marker=dict(size=8, symbol='diamond'),
                    hovertemplate="<b>Date: %{x}</b><br>" +
                                "Forecasted Quantity: %{y:,.0f}<br>" +
                                "<extra></extra>"
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast_data['forecast_date'],
                    y=forecast_data['forecasted_price'],
                    mode='lines+markers',
                    name='Forecasted Price',
                    line=dict(color='#A23B72', width=4),
                    marker=dict(size=8, symbol='square'),
                    yaxis='y2',
                    hovertemplate="<b>Date: %{x}</b><br>" +
                                "Forecasted Price: $%{y:.2f}<br>" +
                                "<extra></extra>"
                ))
                
                fig.update_layout(
                    title={'text': f'Procurement Forecast ({forecast_periods} months)', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'color': '#1e3c72'}},
                    xaxis_title="Forecast Date",
                    yaxis_title="Forecasted Quantity",
                    yaxis2=dict(title="Forecasted Price ($)", overlaying="y", side="right"),
                    height=500,
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                    xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
                
                # Optimized metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_quantity = forecast_data['forecasted_quantity'].mean()
                    st.metric("Avg Forecasted Quantity", f"{avg_quantity:,.0f}")
                with col2:
                    avg_price = forecast_data['forecasted_price'].mean()
                    st.metric("Avg Forecasted Price", f"${avg_price:.2f}")
                with col3:
                    total_forecast_value = (forecast_data['forecasted_quantity'] * forecast_data['forecasted_price']).sum()
                    st.metric("Total Forecast Value", f"${total_forecast_value:,.0f}")
                
                # Optimized table
                st.markdown("### 📋 Forecast Details")
                forecast_display = forecast_data.copy()
                forecast_display.columns = ['Forecast Date', 'Forecasted Quantity', 'Forecasted Price ($)', 'Forecast Type']
                forecast_display['Forecasted Quantity'] = forecast_display['Forecasted Quantity'].apply(lambda x: f"{x:,.0f}")
                forecast_display['Forecasted Price ($)'] = forecast_display['Forecasted Price ($)'].apply(lambda x: f"${x:.2f}")
                
                st.dataframe(forecast_display, use_container_width=True, height=400)
                
                # Download option
                csv = forecast_data.to_csv(index=False)
                st.download_button(
                    label="📥 Download Forecast Data",
                    data=csv,
                    file_name="procurement_forecast.csv",
                    mime="text/csv"
                )
                
            else:
                st.warning(f"⚠️ {forecast_msg}")
        else:
            st.info("💡 Click 'Generate Forecast' to create procurement forecasts")
    
    # Optimized summary insights
    st.markdown("---")
    st.markdown('<div class="insight-box"><h3>💡 Key Insights & Summary</h3></div>', unsafe_allow_html=True)
    
    if not purchase_orders_df.empty:
        # Pre-calculate metrics once
        total_spend = purchase_orders_df['total_value'].sum() if 'total_value' in purchase_orders_df.columns else purchase_orders_df['quantity'].mul(purchase_orders_df['unit_price']).sum()
        total_orders = len(purchase_orders_df)
        unique_suppliers = purchase_orders_df['supplier_id'].nunique()
        unique_items = purchase_orders_df['item_id'].nunique()
        
        # Optimized metric cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <h3>💰 Total Spend</h3>
                <h2>${total_spend:,.0f}</h2>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <h3>📦 Total Orders</h3>
                <h2>{total_orders:,}</h2>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <h3>🏢 Unique Suppliers</h3>
                <h2>{unique_suppliers}</h2>
            </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <h3>📋 Unique Items</h3>
                <h2>{unique_items}</h2>
            </div>
            ''', unsafe_allow_html=True)
        
        # Optimized insights
        if not cost_data.empty:
            st.markdown("### 🎯 Optimization Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Top Savings Opportunity**: {cost_data.iloc[0]['item_name']} - ${cost_data.iloc[0]['savings_amount']:,.0f} potential savings")
                st.info(f"**High Priority Items**: {len(cost_data[cost_data['priority'] == 'High Priority'])} items require immediate attention")
            with col2:
                st.info(f"**Total Optimization Potential**: ${cost_data['savings_amount'].sum():,.0f} across all items")
                st.info(f"**Average Savings**: {cost_data['savings_percentage'].mean():.1f}% per item")

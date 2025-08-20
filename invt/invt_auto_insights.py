import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# INVENTORY INSIGHTS CLASS
# ============================================================================

class InventoryInsights:
    """Class for generating automated inventory insights and recommendations."""
    
    def __init__(self, data):
        """
        Initialize with inventory data.
        
        Args:
            data (pd.DataFrame): Inventory data
        """
        self.data = data.copy()
        self.insights = []
        self.recommendations = []
        self.risk_alerts = []
        self.optimization_opportunities = []
        
    def generate_all_insights(self):
        """Generate all types of insights."""
        self._analyze_stock_levels()
        self._analyze_turnover_patterns()
        self._analyze_supplier_performance()
        self._analyze_cost_efficiency()
        self._analyze_warehouse_operations()
        self._analyze_demand_patterns()
        self._identify_optimization_opportunities()
        self._generate_risk_alerts()
        
        return {
            'insights': self.insights,
            'recommendations': self.recommendations,
            'risk_alerts': self.risk_alerts,
            'optimization_opportunities': self.optimization_opportunities
        }
    
    def _analyze_stock_levels(self):
        """Analyze stock levels and identify issues."""
        if self.data.empty:
            return
        
        # Stockout risk analysis
        if 'current_stock' in self.data.columns and 'reorder_point' in self.data.columns:
            low_stock_items = self.data[self.data['current_stock'] <= self.data['reorder_point']]
            
            if not low_stock_items.empty:
                self.insights.append({
                    'type': 'stockout_risk',
                    'severity': 'high',
                    'message': f"🚨 {len(low_stock_items)} items are below reorder point",
                    'details': f"Critical items: {', '.join(low_stock_items['item_name'].head(3).tolist())}"
                })
                
                self.recommendations.append({
                    'priority': 'high',
                    'action': 'Immediate reorder required',
                    'items': low_stock_items['item_name'].tolist()
                })
        
        # Overstock analysis
        if 'max_stock' in self.data.columns:
            overstock_items = self.data[self.data['current_stock'] > self.data['max_stock'] * 1.2]
            
            if not overstock_items.empty:
                self.insights.append({
                    'type': 'overstock',
                    'severity': 'medium',
                    'message': f"📦 {len(overstock_items)} items exceed maximum stock levels",
                    'details': f"Overstock items: {', '.join(overstock_items['item_name'].head(3).tolist())}"
                })
                
                self.recommendations.append({
                    'priority': 'medium',
                    'action': 'Review stocking strategy for overstock items',
                    'items': overstock_items['item_name'].tolist()
                })
    
    def _analyze_turnover_patterns(self):
        """Analyze inventory turnover patterns."""
        if self.data.empty or 'turnover_rate' not in self.data.columns:
            return
        
        # Low turnover items
        low_turnover_threshold = self.data['turnover_rate'].quantile(0.25)
        low_turnover_items = self.data[self.data['turnover_rate'] < low_turnover_threshold]
        
        if not low_turnover_items.empty:
            self.insights.append({
                'type': 'low_turnover',
                'severity': 'medium',
                'message': f"📉 {len(low_turnover_items)} items have low turnover rates",
                'details': f"Average turnover: {low_turnover_items['turnover_rate'].mean():.2f}"
            })
            
            self.recommendations.append({
                'priority': 'medium',
                'action': 'Review stocking strategy for low turnover items',
                'items': low_turnover_items['item_name'].head(5).tolist()
            })
        
        # High turnover items
        high_turnover_threshold = self.data['turnover_rate'].quantile(0.75)
        high_turnover_items = self.data[self.data['turnover_rate'] > high_turnover_threshold]
        
        if not high_turnover_items.empty:
            self.insights.append({
                'type': 'high_turnover',
                'severity': 'low',
                'message': f"🚀 {len(high_turnover_items)} items have excellent turnover rates",
                'details': f"Average turnover: {high_turnover_items['turnover_rate'].mean():.2f}"
            })
    
    def _analyze_supplier_performance(self):
        """Analyze supplier performance and identify issues."""
        if self.data.empty or 'supplier_id' not in self.data.columns:
            return
        
        # Supplier performance analysis
        if 'supplier_performance' in self.data.columns:
            poor_performers = self.data[self.data['supplier_performance'] < 60]
            
            if not poor_performers.empty:
                suppliers = poor_performers['supplier_id'].unique()
                self.insights.append({
                    'type': 'supplier_performance',
                    'severity': 'high',
                    'message': f"⚠️ {len(suppliers)} suppliers showing poor performance",
                    'details': f"Low performing suppliers: {', '.join(suppliers[:3])}"
                })
                
                self.recommendations.append({
                    'priority': 'high',
                    'action': 'Review supplier relationships and consider alternatives',
                    'suppliers': suppliers.tolist()
                })
        
        # Lead time analysis
        if 'lead_time' in self.data.columns:
            high_lead_time_threshold = self.data['lead_time'].quantile(0.75)
            high_lead_time_items = self.data[self.data['lead_time'] > high_lead_time_threshold]
            
            if not high_lead_time_items.empty:
                self.insights.append({
                    'type': 'lead_time',
                    'severity': 'medium',
                    'message': f"⏰ {len(high_lead_time_items)} items have long lead times",
                    'details': f"Average lead time: {high_lead_time_items['lead_time'].mean():.1f} days"
                })
    
    def _analyze_cost_efficiency(self):
        """Analyze cost efficiency and identify savings opportunities."""
        if self.data.empty:
            return
        
        # Holding cost analysis
        if 'annual_holding_cost' in self.data.columns:
            total_holding_cost = self.data['annual_holding_cost'].sum()
            
            if total_holding_cost > 0:
                self.insights.append({
                    'type': 'holding_cost',
                    'severity': 'medium',
                    'message': f"💰 Total annual holding cost: ${total_holding_cost:,.2f}",
                    'details': f"Average holding cost per item: ${total_holding_cost/len(self.data):,.2f}"
                })
                
                # Identify high holding cost items
                high_holding_items = self.data.nlargest(5, 'annual_holding_cost')
                self.optimization_opportunities.append({
                    'type': 'holding_cost_reduction',
                    'potential_savings': f"${high_holding_items['annual_holding_cost'].sum() * 0.2:,.2f}",
                    'items': high_holding_items['item_name'].tolist(),
                    'action': 'Review stocking levels for high holding cost items'
                })
        
        # ABC analysis insights
        if 'abc_category' in self.data.columns:
            abc_counts = self.data['abc_category'].value_counts()
            
            if 'C' in abc_counts and abc_counts['C'] > len(self.data) * 0.5:
                self.insights.append({
                    'type': 'abc_analysis',
                    'severity': 'medium',
                    'message': f"🔍 C-category items represent {abc_counts['C']/len(self.data)*100:.1f}% of inventory",
                    'details': "Consider reducing C-category items to optimize space and costs"
                })
    
    def _analyze_warehouse_operations(self):
        """Analyze warehouse operations and efficiency."""
        if self.data.empty:
            return
        
        # Space utilization analysis
        if 'space_utilization' in self.data.columns:
            low_utilization = self.data[self.data['space_utilization'] < 50]
            high_utilization = self.data[self.data['space_utilization'] > 90]
            
            if not low_utilization.empty:
                self.insights.append({
                    'type': 'space_utilization',
                    'severity': 'low',
                    'message': f"📏 {len(low_utilization)} items have low space utilization",
                    'details': f"Average utilization: {low_utilization['space_utilization'].mean():.1f}%"
                })
            
            if not high_utilization.empty:
                self.insights.append({
                    'type': 'space_utilization',
                    'severity': 'medium',
                    'message': f"⚠️ {len(high_utilization)} items have very high space utilization",
                    'details': f"Risk of space constraints in warehouse"
                })
        
        # Pick efficiency analysis
        if 'pick_efficiency' in self.data.columns:
            low_pick_efficiency = self.data[self.data['pick_efficiency'] < 60]
            
            if not low_pick_efficiency.empty:
                self.insights.append({
                    'type': 'pick_efficiency',
                    'severity': 'medium',
                    'message': f"🤖 {len(low_pick_efficiency)} items have low pick efficiency",
                    'details': f"Average pick efficiency: {low_pick_efficiency['pick_efficiency'].mean():.1f}%"
                })
                
                self.optimization_opportunities.append({
                    'type': 'pick_route_optimization',
                    'potential_improvement': f"{100 - low_pick_efficiency['pick_efficiency'].mean():.1f}%",
                    'items': low_pick_efficiency['item_name'].tolist(),
                    'action': 'Optimize pick routes and warehouse layout'
                })
    
    def _analyze_demand_patterns(self):
        """Analyze demand patterns and forecasting accuracy."""
        if self.data.empty:
            return
        
        # Demand volatility analysis
        if 'demand_volatility' in self.data.columns:
            high_volatility = self.data[self.data['demand_volatility'] > 0.5]
            
            if not high_volatility.empty:
                self.insights.append({
                    'type': 'demand_volatility',
                    'severity': 'medium',
                    'message': f"📊 {len(high_volatility)} items show high demand volatility",
                    'details': f"Average volatility: {high_volatility['demand_volatility'].mean():.2f}"
                })
                
                self.recommendations.append({
                    'priority': 'medium',
                    'action': 'Implement safety stock for high volatility items',
                    'items': high_volatility['item_name'].head(5).tolist()
                })
        
        # Seasonality analysis
        if 'seasonality_score' in self.data.columns:
            seasonal_items = self.data[self.data['seasonality_score'] > 0.7]
            
            if not seasonal_items.empty:
                self.insights.append({
                    'type': 'seasonality',
                    'severity': 'low',
                    'message': f"🌱 {len(seasonal_items)} items show strong seasonal patterns",
                    'details': f"Average seasonality score: {seasonal_items['seasonality_score'].mean():.2f}"
                })
        
        # Forecast accuracy analysis
        if 'forecast_accuracy' in self.data.columns:
            low_accuracy = self.data[self.data['forecast_accuracy'] < 80]
            
            if not low_accuracy.empty:
                self.insights.append({
                    'type': 'forecast_accuracy',
                    'severity': 'medium',
                    'message': f"📈 {len(low_accuracy)} items have low forecast accuracy",
                    'details': f"Average accuracy: {low_accuracy['forecast_accuracy'].mean():.1f}%"
                })
                
                self.recommendations.append({
                    'priority': 'medium',
                    'action': 'Review and improve forecasting models',
                    'items': low_accuracy['item_name'].head(5).tolist()
                })
    
    def _identify_optimization_opportunities(self):
        """Identify specific optimization opportunities."""
        if self.data.empty:
            return
        
        # EOQ optimization
        if 'eoq' in self.data.columns and 'current_stock' in self.data.columns:
            # Items where current stock is significantly different from EOQ
            stock_eoq_ratio = self.data['current_stock'] / self.data['eoq']
            optimization_candidates = self.data[
                (stock_eoq_ratio < 0.5) | (stock_eoq_ratio > 2.0)
            ]
            
            if not optimization_candidates.empty:
                self.optimization_opportunities.append({
                    'type': 'eoq_optimization',
                    'potential_savings': 'Significant cost reduction',
                    'items': optimization_candidates['item_name'].head(5).tolist(),
                    'action': 'Adjust order quantities to match EOQ recommendations'
                })
        
        # Supplier consolidation
        if 'supplier_id' in self.data.columns and 'supplier_performance' in self.data.columns:
            supplier_performance = self.data.groupby('supplier_id')['supplier_performance'].mean()
            poor_suppliers = supplier_performance[supplier_performance < 60]
            
            if not poor_suppliers.empty:
                self.optimization_opportunities.append({
                    'type': 'supplier_consolidation',
                    'potential_savings': 'Improved reliability and cost',
                    'suppliers': poor_suppliers.index.tolist(),
                    'action': 'Consolidate orders with high-performing suppliers'
                })
    
    def _generate_risk_alerts(self):
        """Generate risk alerts based on various factors."""
        if self.data.empty:
            return
        
        # Stockout risk alerts
        if 'stockout_risk_score' in self.data.columns:
            high_risk_items = self.data[self.data['stockout_risk_score'] >= 80]
            
            if not high_risk_items.empty:
                self.risk_alerts.append({
                    'type': 'stockout_risk',
                    'severity': 'critical',
                    'message': f"🚨 {len(high_risk_items)} items at critical stockout risk",
                    'items': high_risk_items['item_name'].tolist(),
                    'action': 'Immediate reorder required'
                })
        
        # Supplier risk alerts
        if 'supplier_risk_score' in self.data.columns:
            critical_supplier_risk = self.data[self.data['supplier_risk_score'] >= 80]
            
            if not critical_supplier_risk.empty:
                suppliers = critical_supplier_risk['supplier_id'].unique()
                self.risk_alerts.append({
                    'type': 'supplier_risk',
                    'severity': 'high',
                    'message': f"⚠️ {len(suppliers)} suppliers pose critical risk",
                    'suppliers': suppliers.tolist(),
                    'action': 'Develop backup supplier relationships'
                })
        
        # Cost risk alerts
        if 'annual_holding_cost' in self.data.columns:
            high_cost_threshold = self.data['annual_holding_cost'].quantile(0.9)
            high_cost_items = self.data[self.data['annual_holding_cost'] > high_cost_threshold]
            
            if not high_cost_items.empty:
                self.risk_alerts.append({
                    'type': 'cost_risk',
                    'severity': 'medium',
                    'message': f"💰 {len(high_cost_items)} items have excessive holding costs",
                    'items': high_cost_items['item_name'].tolist(),
                    'action': 'Review stocking levels and reorder strategies'
                })

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_insights_section(data):
    """Display the insights section in the main dashboard."""
    if data is None or data.empty:
        st.warning("📊 No data available for insights generation.")
        return
    
    st.subheader("🧠 AI-Powered Insights & Recommendations")
    
    # Generate insights
    insights_engine = InventoryInsights(data)
    all_insights = insights_engine.generate_all_insights()
    
    # Display insights in tabs
    tab_names = ["🔍 Insights", "💡 Recommendations", "⚠️ Risk Alerts", "🚀 Optimization"]
    tabs = st.tabs(tab_names)
    
    with tabs[0]:  # Insights tab
        display_insights_tab(all_insights['insights'])
    
    with tabs[1]:  # Recommendations tab
        display_recommendations_tab(all_insights['recommendations'])
    
    with tabs[2]:  # Risk Alerts tab
        display_risk_alerts_tab(all_insights['risk_alerts'])
    
    with tabs[3]:  # Optimization tab
        display_optimization_tab(all_insights['optimization_opportunities'])

def display_insights_tab(insights):
    """Display insights in a dedicated tab."""
    if not insights:
        st.info("✅ No significant insights to display at this time.")
        return
    
    # Group insights by severity
    severity_colors = {
        'critical': '🔴',
        'high': '🟠', 
        'medium': '🟡',
        'low': '🟢'
    }
    
    for insight in insights:
        severity_icon = severity_colors.get(insight['severity'], '⚪')
        
        with st.expander(f"{severity_icon} {insight['message']}", expanded=True):
            st.write(f"**Type:** {insight['type'].replace('_', ' ').title()}")
            st.write(f"**Severity:** {insight['severity'].title()}")
            st.write(f"**Details:** {insight['details']}")

def display_recommendations_tab(recommendations):
    """Display recommendations in a dedicated tab."""
    if not recommendations:
        st.info("✅ No specific recommendations at this time.")
        return
    
    # Group recommendations by priority
    priority_colors = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    for rec in recommendations:
        priority_icon = priority_colors.get(rec['priority'], '⚪')
        
        with st.expander(f"{priority_icon} {rec['action']}", expanded=True):
            st.write(f"**Priority:** {rec['priority'].title()}")
            st.write(f"**Action Required:** {rec['action']}")
            
            if 'items' in rec:
                st.write(f"**Affected Items:** {', '.join(rec['items'][:5])}")
                if len(rec['items']) > 5:
                    st.write(f"... and {len(rec['items']) - 5} more items")
            
            if 'suppliers' in rec:
                st.write(f"**Affected Suppliers:** {', '.join(rec['suppliers'][:3])}")
                if len(rec['suppliers']) > 3:
                    st.write(f"... and {len(rec['suppliers']) - 3} more suppliers")

def display_risk_alerts_tab(risk_alerts):
    """Display risk alerts in a dedicated tab."""
    if not risk_alerts:
        st.info("✅ No risk alerts at this time.")
        return
    
    # Group alerts by severity
    severity_colors = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    for alert in risk_alerts:
        severity_icon = severity_colors.get(alert['severity'], '⚪')
        
        with st.expander(f"{severity_icon} {alert['message']}", expanded=True):
            st.write(f"**Type:** {alert['type'].replace('_', ' ').title()}")
            st.write(f"**Severity:** {alert['severity'].title()}")
            st.write(f"**Action Required:** {alert['action']}")
            
            if 'items' in alert:
                st.write(f"**Affected Items:** {', '.join(alert['items'][:5])}")
                if len(alert['items']) > 5:
                    st.write(f"... and {len(alert['items']) - 5} more items")
            
            if 'suppliers' in alert:
                st.write(f"**Affected Suppliers:** {', '.join(alert['suppliers'][:3])}")
                if len(alert['suppliers']) > 3:
                    st.write(f"... and {len(alert['suppliers']) - 3} more suppliers")

def display_optimization_tab(optimization_opportunities):
    """Display optimization opportunities in a dedicated tab."""
    if not optimization_opportunities:
        st.info("✅ No optimization opportunities identified at this time.")
        return
    
    for opp in optimization_opportunities:
        with st.expander(f"🚀 {opp['action']}", expanded=True):
            st.write(f"**Type:** {opp['type'].replace('_', ' ').title()}")
            st.write(f"**Potential Impact:** {opp['potential_savings']}")
            st.write(f"**Action:** {opp['action']}")
            
            if 'items' in opp:
                st.write(f"**Items to Review:** {', '.join(opp['items'][:5])}")
                if len(opp['items']) > 5:
                    st.write(f"... and {len(opp['items']) - 5} more items")
            
            if 'suppliers' in opp:
                st.write(f"**Suppliers to Review:** {', '.join(opp['suppliers'][:3])}")
                if len(opp['suppliers']) > 3:
                    st.write(f"... and {len(opp['suppliers']) - 3} more suppliers")

def generate_insights_summary(data):
    """Generate a summary of all insights for reporting."""
    if data is None or data.empty:
        return "No data available for insights generation."
    
    insights_engine = InventoryInsights(data)
    all_insights = insights_engine.generate_all_insights()
    
    summary = []
    summary.append("INVENTORY INTELLIGENCE INSIGHTS SUMMARY")
    summary.append("=" * 50)
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")
    
    # Insights summary
    summary.append("KEY INSIGHTS")
    summary.append("-" * 20)
    for insight in all_insights['insights'][:10]:  # Top 10 insights
        summary.append(f"• {insight['message']}")
    summary.append("")
    
    # Recommendations summary
    summary.append("PRIORITY RECOMMENDATIONS")
    summary.append("-" * 30)
    for rec in all_insights['recommendations'][:5]:  # Top 5 recommendations
        summary.append(f"• [{rec['priority'].upper()}] {rec['action']}")
    summary.append("")
    
    # Risk alerts summary
    summary.append("RISK ALERTS")
    summary.append("-" * 15)
    for alert in all_insights['risk_alerts'][:5]:  # Top 5 alerts
        summary.append(f"• [{alert['severity'].upper()}] {alert['message']}")
    summary.append("")
    
    # Optimization opportunities summary
    summary.append("OPTIMIZATION OPPORTUNITIES")
    summary.append("-" * 30)
    for opp in all_insights['optimization_opportunities'][:5]:  # Top 5 opportunities
        summary.append(f"• {opp['action']} - {opp['potential_savings']}")
    
    return "\n".join(summary)

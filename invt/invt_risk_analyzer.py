import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# INVENTORY RISK ANALYZER CLASS
# ============================================================================

class InventoryRiskAnalyzer:
    """Class for comprehensive inventory risk analysis and assessment."""
    
    def __init__(self, data):
        """
        Initialize with inventory data.
        
        Args:
            data (pd.DataFrame): Inventory data
        """
        self.data = data.copy()
        self.risk_scores = {}
        self.risk_categories = {}
        self.mitigation_strategies = {}
        
    def analyze_all_risks(self):
        """Perform comprehensive risk analysis across all categories."""
        if self.data.empty:
            return {}
        
        # Calculate all risk metrics
        self._calculate_stockout_risks()
        self._calculate_supplier_risks()
        self._calculate_cost_risks()
        self._calculate_operational_risks()
        self._calculate_market_risks()
        self._calculate_quality_risks()
        self._calculate_compliance_risks()
        
        # Generate overall risk assessment
        self._generate_overall_risk_assessment()
        
        return {
            'risk_scores': self.risk_scores,
            'risk_categories': self.risk_categories,
            'mitigation_strategies': self.mitigation_strategies,
            'overall_risk_level': self.overall_risk_level
        }
    
    def _calculate_stockout_risks(self):
        """Calculate stockout and inventory availability risks."""
        if 'current_stock' in self.data.columns and 'reorder_point' in self.data.columns:
            # Stockout probability
            stockout_probability = len(self.data[self.data['current_stock'] <= self.data['reorder_point']]) / len(self.data)
            
            # Days until stockout
            if 'daily_demand' in self.data.columns:
                days_until_stockout = self.data['current_stock'] / self.data['daily_demand']
                avg_days_until_stockout = days_until_stockout.mean()
            else:
                avg_days_until_stockout = 0
            
            # Stockout risk score (0-100)
            stockout_risk_score = min(100, stockout_probability * 100 + (30 - avg_days_until_stockout) * 2)
            
            self.risk_scores['stockout_risk'] = stockout_risk_score
            self.risk_categories['stockout_risk'] = {
                'probability': stockout_probability,
                'avg_days_until_stockout': avg_days_until_stockout,
                'critical_items': self.data[self.data['current_stock'] <= self.data['reorder_point']]['item_name'].tolist()
            }
            
            # Mitigation strategies
            if stockout_risk_score > 70:
                self.mitigation_strategies['stockout_risk'] = [
                    "Implement safety stock for critical items",
                    "Establish backup supplier relationships",
                    "Improve demand forecasting accuracy",
                    "Set up automated reorder triggers"
                ]
            elif stockout_risk_score > 40:
                self.mitigation_strategies['stockout_risk'] = [
                    "Review reorder points and lead times",
                    "Monitor stock levels more frequently",
                    "Consider vendor-managed inventory"
                ]
            else:
                self.mitigation_strategies['stockout_risk'] = [
                    "Maintain current inventory management practices",
                    "Regular review of reorder parameters"
                ]
    
    def _calculate_supplier_risks(self):
        """Calculate supplier-related risks."""
        if 'supplier_id' in self.data.columns:
            supplier_risks = {}
            
            # Supplier concentration risk
            supplier_counts = self.data['supplier_id'].value_counts()
            concentration_risk = 1 - (len(supplier_counts) / len(self.data))
            
            # Supplier performance risk
            if 'supplier_performance' in self.data.columns:
                poor_performers = self.data[self.data['supplier_performance'] < 60]
                performance_risk = len(poor_performers) / len(self.data) * 100
            else:
                performance_risk = 0
            
            # Lead time variance risk
            if 'lead_time' in self.data.columns:
                lead_time_variance = self.data.groupby('supplier_id')['lead_time'].var().fillna(0)
                avg_lead_time_variance = lead_time_variance.mean()
                lead_time_risk = min(100, avg_lead_time_variance / 10)  # Normalize to 0-100
            else:
                lead_time_risk = 0
            
            # Overall supplier risk
            supplier_risk_score = (concentration_risk * 30 + performance_risk * 40 + lead_time_risk * 30) / 100
            
            self.risk_scores['supplier_risk'] = supplier_risk_score
            self.risk_categories['supplier_risk'] = {
                'concentration_risk': concentration_risk,
                'performance_risk': performance_risk,
                'lead_time_risk': lead_time_risk,
                'poor_performing_suppliers': self.data[self.data['supplier_performance'] < 60]['supplier_id'].unique().tolist() if 'supplier_performance' in self.data.columns else []
            }
            
            # Mitigation strategies
            if supplier_risk_score > 70:
                self.mitigation_strategies['supplier_risk'] = [
                    "Develop multiple supplier relationships",
                    "Implement supplier performance monitoring",
                    "Establish backup supplier agreements",
                    "Consider supplier development programs"
                ]
            elif supplier_risk_score > 40:
                self.mitigation_strategies['supplier_risk'] = [
                    "Diversify supplier base",
                    "Improve supplier communication",
                    "Set performance improvement targets"
                ]
            else:
                self.mitigation_strategies['supplier_risk'] = [
                    "Maintain current supplier relationships",
                    "Regular supplier performance reviews"
                ]
    
    def _calculate_cost_risks(self):
        """Calculate cost-related risks."""
        cost_risks = {}
        
        # Holding cost risk
        if 'annual_holding_cost' in self.data.columns:
            total_holding_cost = self.data['annual_holding_cost'].sum()
            avg_holding_cost_per_item = total_holding_cost / len(self.data)
            
            # Compare to industry benchmarks (assuming 20% of inventory value is reasonable)
            if 'stock_value' in self.data.columns:
                total_stock_value = self.data['stock_value'].sum()
                benchmark_holding_cost = total_stock_value * 0.2
                holding_cost_risk = min(100, (total_holding_cost / benchmark_holding_cost) * 50)
            else:
                holding_cost_risk = 0
        else:
            holding_cost_risk = 0
        
        # Price volatility risk
        if 'unit_cost' in self.data.columns:
            cost_volatility = self.data['unit_cost'].std() / self.data['unit_cost'].mean()
            price_volatility_risk = min(100, cost_volatility * 100)
        else:
            price_volatility_risk = 0
        
        # Overall cost risk
        cost_risk_score = (holding_cost_risk * 60 + price_volatility_risk * 40) / 100
        
        self.risk_scores['cost_risk'] = cost_risk_score
        self.risk_categories['cost_risk'] = {
            'holding_cost_risk': holding_cost_risk,
            'price_volatility_risk': price_volatility_risk,
            'total_holding_cost': total_holding_cost if 'annual_holding_cost' in self.data.columns else 0
        }
        
        # Mitigation strategies
        if cost_risk_score > 70:
            self.mitigation_strategies['cost_risk'] = [
                "Implement just-in-time inventory",
                "Negotiate better supplier terms",
                "Optimize order quantities using EOQ",
                "Consider bulk purchasing discounts"
            ]
        elif cost_risk_score > 40:
            self.mitigation_strategies['cost_risk'] = [
                "Review stocking levels",
                "Optimize reorder frequencies",
                "Monitor price trends"
            ]
        else:
            self.mitigation_strategies['cost_risk'] = [
                "Maintain current cost management practices",
                "Regular cost analysis and benchmarking"
            ]
    
    def _calculate_operational_risks(self):
        """Calculate operational and efficiency risks."""
        operational_risks = {}
        
        # Space utilization risk
        if 'space_utilization' in self.data.columns:
            low_utilization = len(self.data[self.data['space_utilization'] < 50])
            high_utilization = len(self.data[self.data['space_utilization'] > 90])
            
            space_risk = (low_utilization * 0.3 + high_utilization * 0.7) / len(self.data) * 100
        else:
            space_risk = 0
        
        # Pick efficiency risk
        if 'pick_efficiency' in self.data.columns:
            low_pick_efficiency = len(self.data[self.data['pick_efficiency'] < 60])
            pick_efficiency_risk = (low_pick_efficiency / len(self.data)) * 100
        else:
            pick_efficiency_risk = 0
        
        # Turnover risk
        if 'turnover_rate' in self.data.columns:
            low_turnover = len(self.data[self.data['turnover_rate'] < self.data['turnover_rate'].quantile(0.25)])
            turnover_risk = (low_turnover / len(self.data)) * 100
        else:
            turnover_risk = 0
        
        # Overall operational risk
        operational_risk_score = (space_risk * 30 + pick_efficiency_risk * 40 + turnover_risk * 30) / 100
        
        self.risk_scores['operational_risk'] = operational_risk_score
        self.risk_categories['operational_risk'] = {
            'space_risk': space_risk,
            'pick_efficiency_risk': pick_efficiency_risk,
            'turnover_risk': turnover_risk
        }
        
        # Mitigation strategies
        if operational_risk_score > 70:
            self.mitigation_strategies['operational_risk'] = [
                "Optimize warehouse layout and storage",
                "Implement automated picking systems",
                "Review and optimize pick routes",
                "Improve inventory turnover through better forecasting"
            ]
        elif operational_risk_score > 40:
            self.mitigation_strategies['operational_risk'] = [
                "Analyze space utilization patterns",
                "Optimize pick processes",
                "Review slow-moving inventory"
            ]
        else:
            self.mitigation_strategies['operational_risk'] = [
                "Maintain current operational practices",
                "Regular efficiency monitoring"
            ]
    
    def _calculate_market_risks(self):
        """Calculate market and demand-related risks."""
        market_risks = {}
        
        # Demand volatility risk
        if 'demand_volatility' in self.data.columns:
            high_volatility = len(self.data[self.data['demand_volatility'] > 0.5])
            demand_volatility_risk = (high_volatility / len(self.data)) * 100
        else:
            demand_volatility_risk = 0
        
        # Forecast accuracy risk
        if 'forecast_accuracy' in self.data.columns:
            low_accuracy = len(self.data[self.data['forecast_accuracy'] < 80])
            forecast_accuracy_risk = (low_accuracy / len(self.data)) * 100
        else:
            forecast_accuracy_risk = 0
        
        # Seasonality risk
        if 'seasonality_score' in self.data.columns:
            high_seasonality = len(self.data[self.data['seasonality_score'] > 0.7])
            seasonality_risk = (high_seasonality / len(self.data)) * 50  # Seasonality itself isn't always risky
        else:
            seasonality_risk = 0
        
        # Overall market risk
        market_risk_score = (demand_volatility_risk * 40 + forecast_accuracy_risk * 40 + seasonality_risk * 20) / 100
        
        self.risk_scores['market_risk'] = market_risk_score
        self.risk_categories['market_risk'] = {
            'demand_volatility_risk': demand_volatility_risk,
            'forecast_accuracy_risk': forecast_accuracy_risk,
            'seasonality_risk': seasonality_risk
        }
        
        # Mitigation strategies
        if market_risk_score > 70:
            self.mitigation_strategies['market_risk'] = [
                "Improve demand forecasting models",
                "Implement safety stock for volatile items",
                "Develop flexible supply chain strategies",
                "Monitor market trends and adjust accordingly"
            ]
        elif market_risk_score > 40:
            self.mitigation_strategies['market_risk'] = [
                "Enhance forecasting accuracy",
                "Implement demand planning processes",
                "Review seasonal inventory strategies"
            ]
        else:
            self.mitigation_strategies['market_risk'] = [
                "Maintain current forecasting practices",
                "Regular market trend analysis"
            ]
    
    def _calculate_quality_risks(self):
        """Calculate quality and compliance risks."""
        quality_risks = {}
        
        # Quality score risk
        if 'quality_score' in self.data.columns:
            low_quality = len(self.data[self.data['quality_score'] < 80])
            quality_risk = (low_quality / len(self.data)) * 100
        else:
            quality_risk = 0
        
        # Expiry risk (if applicable)
        if 'expiry_date' in self.data.columns:
            current_date = datetime.now()
            expiring_soon = len(self.data[pd.to_datetime(self.data['expiry_date']) < current_date + timedelta(days=30)])
            expiry_risk = (expiring_soon / len(self.data)) * 100
        else:
            expiry_risk = 0
        
        # Overall quality risk
        quality_risk_score = (quality_risk * 70 + expiry_risk * 30) / 100
        
        self.risk_scores['quality_risk'] = quality_risk_score
        self.risk_categories['quality_risk'] = {
            'quality_risk': quality_risk,
            'expiry_risk': expiry_risk
        }
        
        # Mitigation strategies
        if quality_risk_score > 70:
            self.mitigation_strategies['quality_risk'] = [
                "Implement quality control procedures",
                "Review supplier quality standards",
                "Establish quality monitoring systems",
                "Consider alternative suppliers for low-quality items"
            ]
        elif quality_risk_score > 40:
            self.mitigation_strategies['quality_risk'] = [
                "Enhance quality monitoring",
                "Review quality standards",
                "Improve supplier communication"
            ]
        else:
            self.mitigation_strategies['quality_risk'] = [
                "Maintain current quality standards",
                "Regular quality assessments"
            ]
    
    def _calculate_compliance_risks(self):
        """Calculate compliance and regulatory risks."""
        compliance_risks = {}
        
        # Basic compliance risk (placeholder for industry-specific requirements)
        compliance_risk = 0  # This would be customized based on industry requirements
        
        # Documentation risk
        missing_fields = 0
        required_fields = ['item_name', 'current_stock', 'unit_cost']
        for field in required_fields:
            if field in self.data.columns:
                missing_fields += self.data[field].isna().sum()
        
        documentation_risk = (missing_fields / (len(self.data) * len(required_fields))) * 100
        
        # Overall compliance risk
        compliance_risk_score = (compliance_risk * 30 + documentation_risk * 70) / 100
        
        self.risk_scores['compliance_risk'] = compliance_risk_score
        self.risk_categories['compliance_risk'] = {
            'compliance_risk': compliance_risk,
            'documentation_risk': documentation_risk,
            'missing_data_points': missing_fields
        }
        
        # Mitigation strategies
        if compliance_risk_score > 70:
            self.mitigation_strategies['compliance_risk'] = [
                "Implement data validation procedures",
                "Establish data quality standards",
                "Regular compliance audits",
                "Staff training on compliance requirements"
            ]
        elif compliance_risk_score > 40:
            self.mitigation_strategies['compliance_risk'] = [
                "Improve data collection processes",
                "Implement data quality checks",
                "Regular compliance reviews"
            ]
        else:
            self.mitigation_strategies['compliance_risk'] = [
                "Maintain current compliance practices",
                "Regular compliance monitoring"
            ]
    
    def _generate_overall_risk_assessment(self):
        """Generate overall risk assessment and scoring."""
        if not self.risk_scores:
            self.overall_risk_level = 'Unknown'
            return
        
        # Calculate weighted average risk score
        risk_weights = {
            'stockout_risk': 0.25,
            'supplier_risk': 0.20,
            'cost_risk': 0.20,
            'operational_risk': 0.15,
            'market_risk': 0.10,
            'quality_risk': 0.05,
            'compliance_risk': 0.05
        }
        
        overall_score = 0
        total_weight = 0
        
        for risk_type, weight in risk_weights.items():
            if risk_type in self.risk_scores:
                overall_score += self.risk_scores[risk_type] * weight
                total_weight += weight
        
        if total_weight > 0:
            overall_score = overall_score / total_weight
        else:
            overall_score = 0
        
        # Determine overall risk level
        if overall_score >= 80:
            self.overall_risk_level = 'Critical'
        elif overall_score >= 60:
            self.overall_risk_level = 'High'
        elif overall_score >= 40:
            self.overall_risk_level = 'Medium'
        elif overall_score >= 20:
            self.overall_risk_level = 'Low'
        else:
            self.overall_risk_level = 'Very Low'
        
        self.overall_risk_score = overall_score

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_risk_dashboard(data):
    """Display comprehensive risk analysis dashboard."""
    if data is None or data.empty:
        st.warning("📊 No data available for risk analysis.")
        return
    
    st.subheader("⚠️ Risk Analysis & Assessment Dashboard")
    
    # Initialize risk analyzer
    risk_analyzer = InventoryRiskAnalyzer(data)
    risk_results = risk_analyzer.analyze_all_risks()
    
    if not risk_results:
        st.error("❌ Unable to perform risk analysis.")
        return
    
    # Display overall risk assessment
    display_overall_risk_assessment(risk_results)
    
    # Display detailed risk breakdown
    display_detailed_risk_breakdown(risk_results)
    
    # Display risk mitigation strategies
    display_risk_mitigation_strategies(risk_results)
    
    # Display risk trends and patterns
    display_risk_trends(data, risk_results)

def display_overall_risk_assessment(risk_results):
    """Display overall risk assessment summary."""
    st.subheader("🎯 Overall Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        overall_score = risk_results.get('overall_risk_score', 0)
        overall_level = risk_results.get('overall_risk_level', 'Unknown')
        
        # Risk level color coding
        risk_colors = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢',
            'Very Low': '🟢'
        }
        
        risk_icon = risk_colors.get(overall_level, '⚪')
        
        st.metric(
            label="Overall Risk Level",
            value=f"{risk_icon} {overall_level}",
            delta=f"Score: {overall_score:.1f}/100"
        )
    
    with col2:
        # Count of high-risk categories
        high_risk_categories = sum(1 for score in risk_results['risk_scores'].values() if score > 60)
        
        st.metric(
            label="High-Risk Categories",
            value=high_risk_categories,
            delta="Categories requiring attention"
        )
    
    with col3:
        # Average risk score
        avg_risk_score = np.mean(list(risk_results['risk_scores'].values()))
        
        st.metric(
            label="Average Risk Score",
            value=f"{avg_risk_score:.1f}",
            delta="Across all categories"
        )
    
    # Risk level description
    risk_descriptions = {
        'Critical': "Immediate action required. Multiple high-risk areas identified.",
        'High': "Significant risks present. Prioritized mitigation needed.",
        'Medium': "Moderate risks identified. Regular monitoring recommended.",
        'Low': "Minimal risks present. Standard monitoring sufficient.",
        'Very Low': "Excellent risk management. Continue current practices."
    }
    
    description = risk_descriptions.get(overall_level, "Risk assessment completed.")
    st.info(f"**Risk Assessment Summary:** {description}")

def display_detailed_risk_breakdown(risk_results):
    """Display detailed breakdown of all risk categories."""
    st.subheader("📊 Detailed Risk Breakdown")
    
    # Create risk score comparison chart
    risk_types = list(risk_results['risk_scores'].keys())
    risk_scores = list(risk_results['risk_scores'].values())
    
    # Color coding based on risk levels
    colors = []
    for score in risk_scores:
        if score >= 80:
            colors.append('#d62728')  # Red for critical
        elif score >= 60:
            colors.append('#ff7f0e')  # Orange for high
        elif score >= 40:
            colors.append('#ffdc00')  # Yellow for medium
        else:
            colors.append('#2ca02c')  # Green for low
    
    # Risk score bar chart
    fig_risk_scores = go.Figure(data=[
        go.Bar(
            x=risk_types,
            y=risk_scores,
            marker_color=colors,
            text=[f"{score:.1f}" for score in risk_scores],
            textposition='auto'
        )
    ])
    
    fig_risk_scores.update_layout(
        title="Risk Scores by Category",
        xaxis_title="Risk Category",
        yaxis_title="Risk Score (0-100)",
        yaxis_range=[0, 100],
        showlegend=False
    )
    
    st.plotly_chart(fig_risk_scores, use_container_width=True)
    
    # Detailed risk information in expandable sections
    for risk_type, risk_score in risk_results['risk_scores'].items():
        risk_name = risk_type.replace('_', ' ').title()
        
        with st.expander(f"📋 {risk_name} - Score: {risk_score:.1f}/100", expanded=False):
            # Risk details
            if risk_type in risk_results['risk_categories']:
                risk_details = risk_results['risk_categories'][risk_type]
                st.write("**Risk Factors:**")
                for factor, value in risk_details.items():
                    if isinstance(value, list):
                        st.write(f"- {factor.replace('_', ' ').title()}: {len(value)} items")
                    else:
                        st.write(f"- {factor.replace('_', ' ').title()}: {value:.2f}")
            
            # Risk level interpretation
            if risk_score >= 80:
                st.error("**Risk Level: Critical** - Immediate action required")
            elif risk_score >= 60:
                st.warning("**Risk Level: High** - Prioritized mitigation needed")
            elif risk_score >= 40:
                st.info("**Risk Level: Medium** - Regular monitoring recommended")
            else:
                st.success("**Risk Level: Low** - Standard monitoring sufficient")

def display_risk_mitigation_strategies(risk_results):
    """Display risk mitigation strategies and recommendations."""
    st.subheader("🛡️ Risk Mitigation Strategies")
    
    if 'mitigation_strategies' not in risk_results:
        st.info("No specific mitigation strategies available.")
        return
    
    # Group strategies by priority
    high_priority = []
    medium_priority = []
    low_priority = []
    
    for risk_type, strategies in risk_results['mitigation_strategies'].items():
        risk_score = risk_results['risk_scores'].get(risk_type, 0)
        
        if risk_score >= 60:
            high_priority.append((risk_type, strategies))
        elif risk_score >= 40:
            medium_priority.append((risk_type, strategies))
        else:
            low_priority.append((risk_type, strategies))
    
    # Display high priority strategies
    if high_priority:
        st.subheader("🔴 High Priority Actions")
        for risk_type, strategies in high_priority:
            risk_name = risk_type.replace('_', ' ').title()
            with st.expander(f"⚠️ {risk_name}", expanded=True):
                for i, strategy in enumerate(strategies, 1):
                    st.write(f"{i}. {strategy}")
    
    # Display medium priority strategies
    if medium_priority:
        st.subheader("🟡 Medium Priority Actions")
        for risk_type, strategies in medium_priority:
            risk_name = risk_type.replace('_', ' ').title()
            with st.expander(f"📋 {risk_name}", expanded=False):
                for i, strategy in enumerate(strategies, 1):
                    st.write(f"{i}. {strategy}")
    
    # Display low priority strategies
    if low_priority:
        st.subheader("🟢 Low Priority Actions")
        for risk_type, strategies in low_priority:
            risk_name = risk_type.replace('_', ' ').title()
            with st.expander(f"✅ {risk_name}", expanded=False):
                for i, strategy in enumerate(strategies, 1):
                    st.write(f"{i}. {strategy}")

def display_risk_trends(data, risk_results):
    """Display risk trends and patterns over time."""
    st.subheader("📈 Risk Trends & Patterns")
    
    # This section can be expanded to show risk trends over time
    # For now, display current risk distribution
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk distribution pie chart
        risk_levels = []
        risk_counts = []
        
        for score in risk_results['risk_scores'].values():
            if score >= 80:
                risk_levels.append('Critical')
            elif score >= 60:
                risk_levels.append('High')
            elif score >= 40:
                risk_levels.append('Medium')
            else:
                risk_levels.append('Low')
        
        risk_distribution = pd.Series(risk_levels).value_counts()
        
        fig_risk_dist = px.pie(
            values=risk_distribution.values,
            names=risk_distribution.index,
            title="Risk Level Distribution",
            color_discrete_sequence=['#d62728', '#ff7f0e', '#ffdc00', '#2ca02c']
        )
        
        st.plotly_chart(fig_risk_dist, use_container_width=True)
    
    with col2:
        # Top risk factors
        st.subheader("🔍 Top Risk Factors")
        
        # Sort risks by score
        sorted_risks = sorted(risk_results['risk_scores'].items(), key=lambda x: x[1], reverse=True)
        
        for i, (risk_type, score) in enumerate(sorted_risks[:5], 1):
            risk_name = risk_type.replace('_', ' ').title()
            
            if score >= 80:
                st.error(f"{i}. {risk_name}: {score:.1f}")
            elif score >= 60:
                st.warning(f"{i}. {risk_name}: {score:.1f}")
            elif score >= 40:
                st.info(f"{i}. {risk_name}: {score:.1f}")
            else:
                st.success(f"{i}. {risk_name}: {score:.1f}")

def generate_risk_report(data):
    """Generate a comprehensive risk report."""
    if data is None or data.empty:
        return "No data available for risk analysis."
    
    risk_analyzer = InventoryRiskAnalyzer(data)
    risk_results = risk_analyzer.analyze_all_risks()
    
    if not risk_results:
        return "Unable to generate risk report."
    
    report = []
    report.append("INVENTORY RISK ANALYSIS REPORT")
    report.append("=" * 50)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Overall assessment
    report.append("OVERALL RISK ASSESSMENT")
    report.append("-" * 30)
    report.append(f"Risk Level: {risk_results.get('overall_risk_level', 'Unknown')}")
    report.append(f"Overall Score: {risk_results.get('overall_risk_score', 0):.1f}/100")
    report.append("")
    
    # Risk breakdown
    report.append("RISK BREAKDOWN BY CATEGORY")
    report.append("-" * 35)
    for risk_type, score in risk_results['risk_scores'].items():
        risk_name = risk_type.replace('_', ' ').title()
        report.append(f"{risk_name}: {score:.1f}/100")
    report.append("")
    
    # High-risk areas
    high_risk_areas = [risk_type for risk_type, score in risk_results['risk_scores'].items() if score >= 60]
    if high_risk_areas:
        report.append("HIGH-RISK AREAS REQUIRING IMMEDIATE ATTENTION")
        report.append("-" * 55)
        for area in high_risk_areas:
            report.append(f"• {area.replace('_', ' ').title()}")
        report.append("")
    
    # Mitigation strategies
    report.append("MITIGATION STRATEGIES")
    report.append("-" * 25)
    for risk_type, strategies in risk_results['mitigation_strategies'].items():
        risk_name = risk_type.replace('_', ' ').title()
        report.append(f"{risk_name}:")
        for strategy in strategies:
            report.append(f"  - {strategy}")
        report.append("")
    
    return "\n".join(report)

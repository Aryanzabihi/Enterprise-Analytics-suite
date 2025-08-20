import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_innovation_metrics(projects_data, products_data, prototypes_data):
    """
    Calculate innovation and product development metrics
    """
    try:
        if projects_data.empty and products_data.empty and prototypes_data.empty:
            return pd.DataFrame(), "No data available for innovation metrics calculation"
        
        metrics = []
        
        # Project Success Rate
        if not projects_data.empty:
            total_projects = len(projects_data)
            completed_projects = len(projects_data[projects_data['status'] == 'Completed'])
            success_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
            metrics.append(['Project Success Rate', f"{success_rate:.1f}%"])
        
        # Time to Market (if we have both projects and products)
        if not projects_data.empty and not products_data.empty:
            try:
                # Merge projects and products
                merged_data = projects_data.merge(products_data, on='project_id', how='inner')
                if not merged_data.empty:
                    # Convert dates to datetime
                    merged_data['start_date'] = pd.to_datetime(merged_data['start_date'], errors='coerce')
                    merged_data['launch_date'] = pd.to_datetime(merged_data['launch_date'], errors='coerce')
                    
                    # Calculate time to market
                    valid_dates = merged_data.dropna(subset=['start_date', 'launch_date'])
                    if not valid_dates.empty:
                        time_to_market = (valid_dates['launch_date'] - valid_dates['start_date']).dt.days.mean()
                        metrics.append(['Avg Time-to-Market', f"{time_to_market:.0f} days"])
                    else:
                        metrics.append(['Avg Time-to-Market', 'N/A'])
                else:
                    metrics.append(['Avg Time-to-Market', 'N/A'])
            except:
                metrics.append(['Avg Time-to-Market', 'N/A'])
        else:
            metrics.append(['Avg Time-to-Market', 'N/A'])
        
        # Revenue Contribution
        if not products_data.empty:
            total_revenue = products_data['revenue_generated'].sum() if 'revenue_generated' in products_data.columns else 0
            metrics.append(['Revenue Contribution', f"${total_revenue:,.0f}"])
        else:
            metrics.append(['Revenue Contribution', '$0'])
        
        # Product Failure Rate
        if not products_data.empty:
            total_products = len(products_data)
            failed_products = len(products_data[products_data['status'] == 'Failed']) if 'status' in products_data.columns else 0
            failure_rate = (failed_products / total_products * 100) if total_products > 0 else 0
            metrics.append(['Product Failure Rate', f"{failure_rate:.1f}%"])
        else:
            metrics.append(['Product Failure Rate', '0%'])
        
        # Prototyping Efficiency
        if not prototypes_data.empty:
            total_prototypes = len(prototypes_data)
            successful_prototypes = len(prototypes_data[prototypes_data['status'] == 'Completed']) if 'status' in prototypes_data.columns else 0
            prototype_success_rate = (successful_prototypes / total_prototypes * 100) if total_prototypes > 0 else 0
            metrics.append(['Prototype Success Rate', f"{prototype_success_rate:.1f}%"])
        else:
            metrics.append(['Prototype Success Rate', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Innovation Overview: {metrics_df.iloc[0]['Value']} project success rate, {len(products_data)} products launched"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating innovation metrics: {str(e)}"

def calculate_resource_allocation_metrics(projects_data, researchers_data, equipment_data):
    """
    Calculate resource allocation and utilization metrics
    """
    try:
        if projects_data.empty and researchers_data.empty and equipment_data.empty:
            return pd.DataFrame(), "No data available for resource allocation metrics calculation"
        
        metrics = []
        
        # Budget Utilization
        if not projects_data.empty:
            total_budget = projects_data['budget'].sum() if 'budget' in projects_data.columns else 0
            total_spend = projects_data['actual_spend'].sum() if 'actual_spend' in projects_data.columns else 0
            budget_utilization = (total_spend / total_budget * 100) if total_budget > 0 else 0
            metrics.append(['Budget Utilization', f"{budget_utilization:.1f}%"])
        else:
            metrics.append(['Budget Utilization', 'N/A'])
        
        # R&D Expenditure Percentage (assuming total company budget)
        if not projects_data.empty:
            total_rd_spend = projects_data['actual_spend'].sum() if 'actual_spend' in projects_data.columns else 0
            # Assume total company budget (this would come from external data)
            assumed_total_budget = 10000000  # $10M assumption
            rd_expenditure_pct = (total_rd_spend / assumed_total_budget * 100) if assumed_total_budget > 0 else 0
            metrics.append(['R&D Expenditure %', f"{rd_expenditure_pct:.1f}%"])
        else:
            metrics.append(['R&D Expenditure %', 'N/A'])
        
        # Researcher Efficiency
        if not researchers_data.empty:
            total_researchers = len(researchers_data)
            active_researchers = len(researchers_data[researchers_data['status'] == 'Active']) if 'status' in researchers_data.columns else total_researchers
            researcher_efficiency = (active_researchers / total_researchers * 100) if total_researchers > 0 else 0
            metrics.append(['Researcher Efficiency', f"{researcher_efficiency:.1f}%"])
        else:
            metrics.append(['Researcher Efficiency', 'N/A'])
        
        # Equipment Utilization
        if not equipment_data.empty:
            total_hours = equipment_data['total_hours'].sum() if 'total_hours' in equipment_data.columns else 0
            utilized_hours = equipment_data['utilized_hours'].sum() if 'utilized_hours' in equipment_data.columns else 0
            equipment_utilization = (utilized_hours / total_hours * 100) if total_hours > 0 else 0
            metrics.append(['Equipment Utilization', f"{equipment_utilization:.1f}%"])
        else:
            metrics.append(['Equipment Utilization', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Resource Overview: {metrics_df.iloc[0]['Value']} budget utilization, {len(researchers_data)} researchers, {len(equipment_data)} equipment items"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating resource allocation metrics: {str(e)}"

def calculate_ip_management_metrics(patents_data, products_data):
    """
    Calculate intellectual property management metrics
    """
    try:
        if patents_data.empty and products_data.empty:
            return pd.DataFrame(), "No data available for IP management metrics calculation"
        
        metrics = []
        
        # Patent Filing Success Rate
        if not patents_data.empty:
            total_patents = len(patents_data)
            granted_patents = len(patents_data[patents_data['status'] == 'Granted']) if 'status' in patents_data.columns else 0
            patent_success_rate = (granted_patents / total_patents * 100) if total_patents > 0 else 0
            metrics.append(['Patent Success Rate', f"{patent_success_rate:.1f}%"])
        else:
            metrics.append(['Patent Success Rate', 'N/A'])
        
        # IP Portfolio Value
        if not patents_data.empty:
            total_ip_value = patents_data['estimated_value'].sum() if 'estimated_value' in patents_data.columns else 0
            metrics.append(['IP Portfolio Value', f"${total_ip_value:,.0f}"])
        else:
            metrics.append(['IP Portfolio Value', '$0'])
        
        # Patent Revenue Contribution
        if not patents_data.empty:
            total_licensing_revenue = patents_data['licensing_revenue'].sum() if 'licensing_revenue' in patents_data.columns else 0
            metrics.append(['Patent Revenue', f"${total_licensing_revenue:,.0f}"])
        else:
            metrics.append(['Patent Revenue', '$0'])
        
        # IP to Product Conversion
        if not patents_data.empty and not products_data.empty:
            patents_with_products = patents_data.merge(products_data, left_on='patent_id', right_on='patent_id', how='inner')
            conversion_rate = (len(patents_with_products) / len(patents_data) * 100) if len(patents_data) > 0 else 0
            metrics.append(['IP to Product Conversion', f"{conversion_rate:.1f}%"])
        else:
            metrics.append(['IP to Product Conversion', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"IP Management: {metrics_df.iloc[0]['Value']} patent success rate, {len(patents_data)} patents in portfolio"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating IP management metrics: {str(e)}"

def calculate_risk_management_metrics(projects_data, products_data, prototypes_data):
    """
    Calculate risk management and failure analysis metrics
    """
    try:
        if projects_data.empty and products_data.empty and prototypes_data.empty:
            return pd.DataFrame(), "No data available for risk management metrics calculation"
        
        metrics = []
        
        # Project Failure Rate
        if not projects_data.empty:
            total_projects = len(projects_data)
            failed_projects = len(projects_data[projects_data['status'].isin(['Failed', 'Cancelled'])]) if 'status' in projects_data.columns else 0
            project_failure_rate = (failed_projects / total_projects * 100) if total_projects > 0 else 0
            metrics.append(['Project Failure Rate', f"{project_failure_rate:.1f}%"])
        else:
            metrics.append(['Project Failure Rate', 'N/A'])
        
        # Cost of Failed Projects
        if not projects_data.empty:
            failed_projects_data = projects_data[projects_data['status'].isin(['Failed', 'Cancelled'])] if 'status' in projects_data.columns else pd.DataFrame()
            if not failed_projects_data.empty:
                cost_of_failures = failed_projects_data['actual_spend'].sum() if 'actual_spend' in failed_projects_data.columns else 0
                metrics.append(['Cost of Failed Projects', f"${cost_of_failures:,.0f}"])
            else:
                metrics.append(['Cost of Failed Projects', '$0'])
        else:
            metrics.append(['Cost of Failed Projects', 'N/A'])
        
        # Prototype Failure Rate
        if not prototypes_data.empty:
            total_prototypes = len(prototypes_data)
            failed_prototypes = len(prototypes_data[prototypes_data['status'] == 'Failed']) if 'status' in prototypes_data.columns else 0
            prototype_failure_rate = (failed_prototypes / total_prototypes * 100) if total_prototypes > 0 else 0
            metrics.append(['Prototype Failure Rate', f"{prototype_failure_rate:.1f}%"])
        else:
            metrics.append(['Prototype Failure Rate', 'N/A'])
        
        # Technology Obsolescence Risk (based on project age)
        if not projects_data.empty:
            try:
                projects_data['start_date'] = pd.to_datetime(projects_data['start_date'], errors='coerce')
                current_date = pd.Timestamp.now()
                avg_project_age = (current_date - projects_data['start_date']).dt.days.mean()
                if pd.notna(avg_project_age):
                    obsolescence_risk = "High" if avg_project_age > 1000 else "Medium" if avg_project_age > 500 else "Low"
                    metrics.append(['Obsolescence Risk', obsolescence_risk])
                else:
                    metrics.append(['Obsolescence Risk', 'N/A'])
            except:
                metrics.append(['Obsolescence Risk', 'N/A'])
        else:
            metrics.append(['Obsolescence Risk', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Risk Management: {metrics_df.iloc[0]['Value']} project failure rate, monitoring {len(projects_data)} active projects"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating risk management metrics: {str(e)}"

def calculate_collaboration_metrics(collaborations_data, projects_data):
    """
    Calculate collaboration and external partnership metrics
    """
    try:
        if collaborations_data.empty and projects_data.empty:
            return pd.DataFrame(), "No data available for collaboration metrics calculation"
        
        metrics = []
        
        # Active Collaborations
        if not collaborations_data.empty:
            total_collaborations = len(collaborations_data)
            active_collaborations = len(collaborations_data[collaborations_data['status'] == 'Active']) if 'status' in collaborations_data.columns else 0
            metrics.append(['Active Collaborations', active_collaborations])
        else:
            metrics.append(['Active Collaborations', 0])
        
        # Collaboration Investment
        if not collaborations_data.empty:
            total_investment = collaborations_data['investment_amount'].sum() if 'investment_amount' in collaborations_data.columns else 0
            metrics.append(['Total Investment', f"${total_investment:,.0f}"])
        else:
            metrics.append(['Total Investment', '$0'])
        
        # Collaboration Revenue
        if not collaborations_data.empty:
            total_revenue = collaborations_data['revenue_generated'].sum() if 'revenue_generated' in collaborations_data.columns else 0
            metrics.append(['Collaboration Revenue', f"${total_revenue:,.0f}"])
        else:
            metrics.append(['Collaboration Revenue', '$0'])
        
        # Collaboration ROI
        if not collaborations_data.empty:
            total_investment = collaborations_data['investment_amount'].sum() if 'investment_amount' in collaborations_data.columns else 0
            total_revenue = collaborations_data['revenue_generated'].sum() if 'revenue_generated' in collaborations_data.columns else 0
            if total_investment > 0:
                collaboration_roi = ((total_revenue - total_investment) / total_investment * 100)
                metrics.append(['Collaboration ROI', f"{collaboration_roi:.1f}%"])
            else:
                metrics.append(['Collaboration ROI', 'N/A'])
        else:
            metrics.append(['Collaboration ROI', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Collaboration Overview: {metrics_df.iloc[0]['Value']} active collaborations, ${total_investment:,.0f} total investment"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating collaboration metrics: {str(e)}"

def calculate_employee_performance_metrics(researchers_data, training_data, projects_data):
    """
    Calculate employee performance and innovation culture metrics
    """
    try:
        if researchers_data.empty and training_data.empty and projects_data.empty:
            return pd.DataFrame(), "No data available for employee performance metrics calculation"
        
        metrics = []
        
        # Employee Innovation Contribution
        if not researchers_data.empty:
            total_researchers = len(researchers_data)
            active_researchers = len(researchers_data[researchers_data['status'] == 'Active']) if 'status' in researchers_data.columns else total_researchers
            metrics.append(['Active Researchers', active_researchers])
        else:
            metrics.append(['Active Researchers', 0])
        
        # Training Effectiveness
        if not training_data.empty:
            if 'pre_performance_score' in training_data.columns and 'post_performance_score' in training_data.columns:
                pre_scores = training_data['pre_performance_score'].dropna()
                post_scores = training_data['post_performance_score'].dropna()
                if len(pre_scores) > 0 and len(post_scores) > 0:
                    avg_improvement = (post_scores.mean() - pre_scores.mean()) if len(pre_scores) > 0 else 0
                    metrics.append(['Avg Training Improvement', f"{avg_improvement:.1f} points"])
                else:
                    metrics.append(['Avg Training Improvement', 'N/A'])
            else:
                metrics.append(['Avg Training Improvement', 'N/A'])
        else:
            metrics.append(['Avg Training Improvement', 'N/A'])
        
        # Team Collaboration (based on projects per researcher)
        if not projects_data.empty and not researchers_data.empty:
            total_projects = len(projects_data)
            total_researchers = len(researchers_data)
            projects_per_researcher = total_projects / total_researchers if total_researchers > 0 else 0
            metrics.append(['Projects per Researcher', f"{projects_per_researcher:.1f}"])
        else:
            metrics.append(['Projects per Researcher', 'N/A'])
        
        # R&D Staff Productivity
        if not projects_data.empty and not researchers_data.empty:
            total_projects = len(projects_data)
            total_researchers = len(researchers_data)
            productivity_score = (total_projects / total_researchers * 100) if total_researchers > 0 else 0
            metrics.append(['R&D Staff Productivity', f"{productivity_score:.1f}%"])
        else:
            metrics.append(['R&D Staff Productivity', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Employee Performance: {metrics_df.iloc[0]['Value']} active researchers, {len(training_data)} training records"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating employee performance metrics: {str(e)}"

def calculate_technology_analysis_metrics(projects_data, prototypes_data, equipment_data):
    """
    Calculate technology and trend analysis metrics
    """
    try:
        if projects_data.empty and prototypes_data.empty and equipment_data.empty:
            return pd.DataFrame(), "No data available for technology analysis metrics calculation"
        
        metrics = []
        
        # Technology Readiness Level (TRL) Analysis
        if not projects_data.empty and 'trl_level' in projects_data.columns:
            avg_trl = projects_data['trl_level'].mean()
            if pd.notna(avg_trl):
                metrics.append(['Average TRL Level', f"{avg_trl:.1f}"])
            else:
                metrics.append(['Average TRL Level', 'N/A'])
        else:
            metrics.append(['Average TRL Level', 'N/A'])
        
        # Technology Areas Distribution
        if not projects_data.empty and 'technology_area' in projects_data.columns:
            tech_areas = projects_data['technology_area'].value_counts()
            top_tech_area = tech_areas.index[0] if len(tech_areas) > 0 else 'N/A'
            metrics.append(['Top Technology Area', top_tech_area])
        else:
            metrics.append(['Top Technology Area', 'N/A'])
        
        # Innovation Pipeline Health
        if not projects_data.empty:
            total_projects = len(projects_data)
            active_projects = len(projects_data[projects_data['status'] == 'Active']) if 'status' in projects_data.columns else 0
            pipeline_health = (active_projects / total_projects * 100) if total_projects > 0 else 0
            metrics.append(['Innovation Pipeline Health', f"{pipeline_health:.1f}%"])
        else:
            metrics.append(['Innovation Pipeline Health', 'N/A'])
        
        # Equipment Technology Status
        if not equipment_data.empty:
            total_equipment = len(equipment_data)
            active_equipment = len(equipment_data[equipment_data['status'] == 'Active']) if 'status' in equipment_data.columns else total_equipment
            equipment_health = (active_equipment / total_equipment * 100) if total_equipment > 0 else 0
            metrics.append(['Equipment Technology Health', f"{equipment_health:.1f}%"])
        else:
            metrics.append(['Equipment Technology Health', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Technology Analysis: {metrics_df.iloc[0]['Value']} average TRL, {len(projects_data)} technology projects"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating technology analysis metrics: {str(e)}"

def calculate_customer_centric_metrics(products_data, projects_data):
    """
    Calculate customer-centric R&D metrics
    """
    try:
        if products_data.empty and projects_data.empty:
            return pd.DataFrame(), "No data available for customer-centric metrics calculation"
        
        metrics = []
        
        # Customer Satisfaction
        if not products_data.empty and 'customer_satisfaction' in products_data.columns:
            avg_satisfaction = products_data['customer_satisfaction'].mean()
            if pd.notna(avg_satisfaction):
                metrics.append(['Avg Customer Satisfaction', f"{avg_satisfaction:.1f}/5.0"])
            else:
                metrics.append(['Avg Customer Satisfaction', 'N/A'])
        else:
            metrics.append(['Avg Customer Satisfaction', 'N/A'])
        
        # Market Response
        if not products_data.empty and 'market_response' in products_data.columns:
            avg_market_response = products_data['market_response'].mean()
            if pd.notna(avg_market_response):
                metrics.append(['Avg Market Response', f"{avg_market_response:.1f}/5.0"])
            else:
                metrics.append(['Avg Market Response', 'N/A'])
        else:
            metrics.append(['Avg Market Response', 'N/A'])
        
        # Feature Adoption (based on product success)
        if not products_data.empty:
            total_products = len(products_data)
            successful_products = len(products_data[products_data['revenue_generated'] > 0]) if 'revenue_generated' in products_data.columns else 0
            feature_adoption_rate = (successful_products / total_products * 100) if total_products > 0 else 0
            metrics.append(['Feature Adoption Rate', f"{feature_adoption_rate:.1f}%"])
        else:
            metrics.append(['Feature Adoption Rate', 'N/A'])
        
        # R&D Impact on Customer Retention
        if not products_data.empty:
            total_revenue = products_data['revenue_generated'].sum() if 'revenue_generated' in products_data.columns else 0
            if total_revenue > 0:
                metrics.append(['R&D Revenue Impact', f"${total_revenue:,.0f}"])
            else:
                metrics.append(['R&D Revenue Impact', '$0'])
        else:
            metrics.append(['R&D Revenue Impact', '$0'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Customer-Centric R&D: {metrics_df.iloc[0]['Value']} customer satisfaction, {len(products_data)} customer-facing products"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating customer-centric metrics: {str(e)}"

def calculate_strategic_metrics(projects_data, products_data, patents_data):
    """
    Calculate strategic and financial metrics
    """
    try:
        if projects_data.empty and products_data.empty and patents_data.empty:
            return pd.DataFrame(), "No data available for strategic metrics calculation"
        
        metrics = []
        
        # Return on R&D Investment (RORI)
        if not projects_data.empty and not products_data.empty:
            total_rd_investment = projects_data['actual_spend'].sum() if 'actual_spend' in projects_data.columns else 0
            total_revenue = products_data['revenue_generated'].sum() if 'revenue_generated' in products_data.columns else 0
            if total_rd_investment > 0:
                rori = ((total_revenue - total_rd_investment) / total_rd_investment * 100)
                metrics.append(['Return on R&D Investment', f"{rori:.1f}%"])
            else:
                metrics.append(['Return on R&D Investment', 'N/A'])
        else:
            metrics.append(['Return on R&D Investment', 'N/A'])
        
        # R&D-Driven Product Profitability
        if not products_data.empty:
            total_revenue = products_data['revenue_generated'].sum() if 'revenue_generated' in products_data.columns else 0
            total_cost = products_data['development_cost'].sum() if 'development_cost' in products_data.columns else 0
            if total_cost > 0:
                profitability = ((total_revenue - total_cost) / total_cost * 100)
                metrics.append(['Product Profitability', f"{profitability:.1f}%"])
            else:
                metrics.append(['Product Profitability', 'N/A'])
        else:
            metrics.append(['Product Profitability', 'N/A'])
        
        # Competitive Advantage (based on patent portfolio)
        if not patents_data.empty:
            total_patents = len(patents_data)
            granted_patents = len(patents_data[patents_data['status'] == 'Granted']) if 'status' in patents_data.columns else 0
            patent_strength = (granted_patents / total_patents * 100) if total_patents > 0 else 0
            metrics.append(['Patent Portfolio Strength', f"{patent_strength:.1f}%"])
        else:
            metrics.append(['Patent Portfolio Strength', 'N/A'])
        
        # Market Share Gains (based on product success)
        if not products_data.empty:
            successful_products = len(products_data[products_data['revenue_generated'] > 0]) if 'revenue_generated' in products_data.columns else 0
            total_products = len(products_data)
            market_share_potential = (successful_products / total_products * 100) if total_products > 0 else 0
            metrics.append(['Market Share Potential', f"{market_share_potential:.1f}%"])
        else:
            metrics.append(['Market Share Potential', 'N/A'])
        
        # Create DataFrame
        metrics_df = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        
        message = f"Strategic Overview: {metrics_df.iloc[0]['Value']} RORI, {len(products_data)} strategic products"
        
        return metrics_df, message
        
    except Exception as e:
        return pd.DataFrame(), f"Error calculating strategic metrics: {str(e)}"

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Test the Auto Insights functionality
def test_auto_insights():
    """Test the Auto Insights system with sample data."""
    
    print("🧪 Testing Auto Insights System...")
    
    try:
        # Import the InsightManager
        from utils.insight_manager import InsightManager
        print("✅ InsightManager imported successfully!")
        
        # Create sample data
        print("📊 Creating sample data...")
        
        # Sample employees
        employees_data = []
        for i in range(50):
            employees_data.append({
                'employee_id': f'EMP{i+1:03d}',
                'first_name': f'Employee{i+1}',
                'last_name': f'Last{i+1}',
                'department': random.choice(['Engineering', 'Sales', 'Marketing', 'HR']),
                'performance_rating': round(random.uniform(2.0, 5.0), 1),
                'tenure_days': random.randint(30, 1000),
                'status': 'Active'
            })
        
        employees_df = pd.DataFrame(employees_data)
        
        # Sample performance data
        performance_data = []
        for i in range(100):
            performance_data.append({
                'review_id': f'REV{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'review_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                'performance_rating': round(random.uniform(2.0, 5.0), 1),
                'goal_achievement_rate': round(random.uniform(0.5, 1.2), 2),
                'productivity_score': round(random.uniform(60, 100), 1),
                'skills_assessment': round(random.uniform(2.0, 5.0), 1),
                'review_cycle': random.choice(['Q1', 'Q2', 'Q3', 'Q4', 'Annual'])
            })
        
        performance_df = pd.DataFrame(performance_data)
        
        # Sample engagement data
        engagement_data = []
        for i in range(50):
            engagement_data.append({
                'survey_id': f'SURV{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'survey_date': (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
                'engagement_score': round(random.uniform(1.0, 5.0), 1),
                'satisfaction_score': round(random.uniform(1.0, 5.0), 1),
                'work_life_balance_score': round(random.uniform(1.0, 5.0), 1),
                'recommendation_score': round(random.uniform(1.0, 5.0), 1),
                'survey_type': random.choice(['Quarterly', 'Annual', 'Pulse'])
            })
        
        engagement_df = pd.DataFrame(engagement_data)
        
        # Sample compensation data
        compensation_data = []
        for i in range(50):
            compensation_data.append({
                'compensation_id': f'COMP{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'effective_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                'base_salary': random.randint(40000, 150000),
                'bonus_amount': random.randint(0, 20000),
                'benefits_value': random.randint(5000, 25000),
                'total_compensation': 0,
                'pay_grade': random.choice(['P1', 'P2', 'P3', 'P4', 'P5']),
                'compensation_reason': random.choice(['Annual Review', 'Promotion', 'Market Adjustment'])
            })
        
        # Calculate total compensation
        for comp in compensation_data:
            comp['total_compensation'] = comp['base_salary'] + comp['bonus_amount'] + comp['benefits_value']
        
        compensation_df = pd.DataFrame(compensation_data)
        
        # Sample training data
        training_data = []
        for i in range(30):
            training_data.append({
                'training_id': f'TRAIN{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'training_program': random.choice(['Leadership Skills', 'Technical Training', 'Communication']),
                'start_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                'completion_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'training_cost': random.randint(500, 5000),
                'skills_improvement': round(random.uniform(1.0, 5.0), 1),
                'performance_impact': round(random.uniform(0.1, 0.5), 2),
                'training_type': random.choice(['Online', 'In-person', 'Hybrid'])
            })
        
        training_df = pd.DataFrame(training_data)
        
        # Sample turnover data
        turnover_data = []
        for i in range(5):
            turnover_data.append({
                'turnover_id': f'TURN{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'separation_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
                'separation_reason': random.choice(['Resignation', 'Termination', 'Retirement']),
                'turnover_reason_detail': random.choice(['Better opportunity', 'Career change', 'Personal reasons']),
                'exit_interview_score': round(random.uniform(1.0, 5.0), 1),
                'rehire_eligibility': random.choice(['Yes', 'No', 'Maybe']),
                'knowledge_transfer_completed': random.choice(['Yes', 'No', 'Partial']),
                'replacement_hired': random.choice(['Yes', 'No', 'In Progress']),
                'turnover_cost': random.randint(5000, 50000),
                'notice_period_days': random.randint(0, 30)
            })
        
        turnover_df = pd.DataFrame(turnover_data)
        
        # Sample benefits data
        benefits_data = []
        for i in range(50):
            benefits_data.append({
                'benefit_id': f'BEN{i+1:03d}',
                'employee_id': random.choice(employees_df['employee_id'].tolist()),
                'benefit_type': random.choice(['Health Insurance', 'Dental Insurance', '401k', 'Life Insurance']),
                'enrollment_date': (datetime.now() - timedelta(days=random.randint(0, 1095))).strftime('%Y-%m-%d'),
                'utilization_rate': round(random.uniform(0.0, 1.0), 2),
                'benefit_cost': random.randint(100, 5000),
                'provider': random.choice(['Blue Cross', 'Aetna', 'Cigna']),
                'coverage_level': random.choice(['Individual', 'Family', 'Employee + Spouse'])
            })
        
        benefits_df = pd.DataFrame(benefits_data)
        
        # Sample recruitment data
        recruitment_data = []
        for i in range(20):
            recruitment_data.append({
                'job_posting_id': f'POST{i+1:03d}',
                'position_title': random.choice(['Software Engineer', 'Sales Representative', 'Marketing Specialist']),
                'department': random.choice(['Engineering', 'Sales', 'Marketing']),
                'posting_date': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
                'closing_date': (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
                'applications_received': random.randint(10, 200),
                'candidates_interviewed': random.randint(3, 15),
                'offers_made': random.randint(1, 5),
                'hires_made': random.randint(0, 3),
                'recruitment_source': random.choice(['LinkedIn', 'Indeed', 'Referral']),
                'recruitment_cost': random.randint(1000, 10000),
                'time_to_hire_days': random.randint(15, 90)
            })
        
        recruitment_df = pd.DataFrame(recruitment_data)
        
        print(f"✅ Sample data created:")
        print(f"   • {len(employees_df)} employees")
        print(f"   • {len(performance_df)} performance reviews")
        print(f"   • {len(engagement_df)} engagement surveys")
        print(f"   • {len(compensation_df)} compensation records")
        print(f"   • {len(training_df)} training records")
        print(f"   • {len(turnover_df)} turnover records")
        print(f"   • {len(benefits_df)} benefit records")
        print(f"   • {len(recruitment_df)} recruitment records")
        
        # Test InsightManager
        print("\n🤖 Testing InsightManager...")
        insight_manager = InsightManager()
        print("✅ InsightManager initialized successfully!")
        
        # Generate insights
        print("📊 Generating insights...")
        insights_data = insight_manager.generate_all_insights(
            employees_df, recruitment_df, performance_df, compensation_df,
            training_df, engagement_df, turnover_df, benefits_df
        )
        print("✅ Insights generated successfully!")
        
        # Check insights structure
        print(f"\n📋 Insights structure:")
        for category, insights in insights_data.items():
            if isinstance(insights, list):
                print(f"   • {category}: {len(insights)} items")
            else:
                print(f"   • {category}: {type(insights)}")
        
        print("\n🎉 Auto Insights system test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Auto Insights: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_auto_insights()

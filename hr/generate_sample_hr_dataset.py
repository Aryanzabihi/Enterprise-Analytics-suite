import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_hr_dataset():
    """Generate a comprehensive sample HR dataset for testing the HR Analytics Dashboard."""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Sample data lists
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'IT', 'Legal']
    job_titles = {
        'Engineering': ['Software Engineer', 'Senior Developer', 'Tech Lead', 'Architect', 'QA Engineer'],
        'Sales': ['Sales Representative', 'Account Manager', 'Sales Director', 'Business Development'],
        'Marketing': ['Marketing Specialist', 'Content Creator', 'Digital Marketing Manager', 'Brand Manager'],
        'HR': ['HR Specialist', 'Recruiter', 'HR Manager', 'Talent Acquisition'],
        'Finance': ['Financial Analyst', 'Accountant', 'Finance Manager', 'Controller'],
        'Operations': ['Operations Manager', 'Process Analyst', 'Project Manager', 'Coordinator'],
        'IT': ['IT Support', 'System Administrator', 'Network Engineer', 'IT Manager'],
        'Legal': ['Legal Counsel', 'Paralegal', 'Compliance Officer', 'Legal Assistant']
    }
    
    locations = ['New York', 'San Francisco', 'Chicago', 'Austin', 'Seattle', 'Boston', 'Denver', 'Atlanta']
    genders = ['Male', 'Female', 'Non-binary']
    ethnicities = ['White', 'Hispanic', 'Black', 'Asian', 'Other']
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD']
    
    # Generate Employees dataset (150 records)
    employees_data = []
    for i in range(150):
        dept = random.choice(departments)
        job_title = random.choice(job_titles[dept])
        hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))  # 1 month to 10 years
        tenure_days = (datetime.now() - hire_date).days
        age = random.randint(22, 65)
        
        employees_data.append({
            'employee_id': f'EMP{i+1:03d}',
            'first_name': f'Employee{i+1}',
            'last_name': f'Last{i+1}',
            'email': f'employee{i+1}@company.com',
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'department': dept,
            'job_title': job_title,
            'salary': random.randint(40000, 150000),
            'manager_id': f'EMP{random.randint(1, 20):03d}' if i > 19 else None,
            'location': random.choice(locations),
            'gender': random.choice(genders),
            'age': age,
            'ethnicity': random.choice(ethnicities),
            'education_level': random.choice(education_levels),
            'performance_rating': round(random.uniform(2.0, 5.0), 1),
            'tenure_days': tenure_days,
            'status': 'Active'
        })
    
    employees_df = pd.DataFrame(employees_data)
    
    # Generate Recruitment dataset (50 records)
    recruitment_data = []
    for i in range(50):
        posting_date = datetime.now() - timedelta(days=random.randint(30, 180))
        closing_date = posting_date + timedelta(days=random.randint(14, 60))
        time_to_hire = random.randint(15, 90)
        
        recruitment_data.append({
            'job_posting_id': f'POST{i+1:03d}',
            'position_title': random.choice([job for jobs in job_titles.values() for job in jobs]),
            'department': random.choice(departments),
            'posting_date': posting_date.strftime('%Y-%m-%d'),
            'closing_date': closing_date.strftime('%Y-%m-%d'),
            'applications_received': random.randint(10, 200),
            'candidates_interviewed': random.randint(3, 15),
            'offers_made': random.randint(1, 5),
            'hires_made': random.randint(0, 3),
            'recruitment_source': random.choice(['LinkedIn', 'Indeed', 'Referral', 'Company Website', 'Job Board']),
            'recruitment_cost': random.randint(1000, 10000),
            'time_to_hire_days': time_to_hire
        })
    
    recruitment_df = pd.DataFrame(recruitment_data)
    
    # Generate Performance dataset (200 records)
    performance_data = []
    for i in range(200):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        review_date = datetime.now() - timedelta(days=random.randint(0, 365))
        
        performance_data.append({
            'review_id': f'REV{i+1:03d}',
            'employee_id': employee_id,
            'review_date': review_date.strftime('%Y-%m-%d'),
            'reviewer_id': random.choice(employees_df['employee_id'].tolist()),
            'performance_rating': round(random.uniform(2.0, 5.0), 1),
            'goal_achievement_rate': round(random.uniform(0.5, 1.2), 2),
            'productivity_score': round(random.uniform(60, 100), 1),
            'skills_assessment': round(random.uniform(2.0, 5.0), 1),
            'review_cycle': random.choice(['Q1', 'Q2', 'Q3', 'Q4', 'Annual'])
        })
    
    performance_df = pd.DataFrame(performance_data)
    
    # Generate Compensation dataset (150 records)
    compensation_data = []
    for i in range(150):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        employee_salary = employees_df[employees_df['employee_id'] == employee_id]['salary'].iloc[0]
        effective_date = datetime.now() - timedelta(days=random.randint(0, 365))
        
        compensation_data.append({
            'compensation_id': f'COMP{i+1:03d}',
            'employee_id': employee_id,
            'effective_date': effective_date.strftime('%Y-%m-%d'),
            'base_salary': employee_salary,
            'bonus_amount': random.randint(0, int(employee_salary * 0.3)),
            'benefits_value': random.randint(5000, 25000),
            'total_compensation': 0,  # Will be calculated
            'pay_grade': random.choice(['P1', 'P2', 'P3', 'P4', 'P5']),
            'compensation_reason': random.choice(['Annual Review', 'Promotion', 'Market Adjustment', 'Retention'])
        })
    
    # Calculate total compensation
    for comp in compensation_data:
        comp['total_compensation'] = comp['base_salary'] + comp['bonus_amount'] + comp['benefits_value']
    
    compensation_df = pd.DataFrame(compensation_data)
    
    # Generate Training dataset (100 records)
    training_data = []
    for i in range(100):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        start_date = datetime.now() - timedelta(days=random.randint(30, 365))
        completion_date = start_date + timedelta(days=random.randint(1, 30))
        
        training_data.append({
            'training_id': f'TRAIN{i+1:03d}',
            'employee_id': employee_id,
            'training_program': random.choice(['Leadership Skills', 'Technical Training', 'Communication', 'Project Management', 'Sales Training']),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'completion_date': completion_date.strftime('%Y-%m-%d'),
            'training_cost': random.randint(500, 5000),
            'skills_improvement': round(random.uniform(1.0, 5.0), 1),
            'performance_impact': round(random.uniform(0.1, 0.5), 2),
            'training_type': random.choice(['Online', 'In-person', 'Hybrid', 'Workshop'])
        })
    
    training_df = pd.DataFrame(training_data)
    
    # Generate Engagement dataset (120 records)
    engagement_data = []
    for i in range(120):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        survey_date = datetime.now() - timedelta(days=random.randint(0, 90))
        
        engagement_data.append({
            'survey_id': f'SURV{i+1:03d}',
            'employee_id': employee_id,
            'survey_date': survey_date.strftime('%Y-%m-%d'),
            'engagement_score': round(random.uniform(1.0, 5.0), 1),
            'satisfaction_score': round(random.uniform(1.0, 5.0), 1),
            'work_life_balance_score': round(random.uniform(1.0, 5.0), 1),
            'recommendation_score': round(random.uniform(1.0, 5.0), 1),
            'survey_type': random.choice(['Quarterly', 'Annual', 'Pulse', 'Exit'])
        })
    
    engagement_df = pd.DataFrame(engagement_data)
    
    # Generate Turnover dataset (18 records)
    turnover_data = []
    for i in range(18):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        separation_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        turnover_data.append({
            'turnover_id': f'TURN{i+1:03d}',
            'employee_id': employee_id,
            'separation_date': separation_date.strftime('%Y-%m-%d'),
            'separation_reason': random.choice(['Resignation', 'Termination', 'Retirement', 'Layoff', 'End of Contract']),
            'turnover_reason_detail': random.choice(['Better opportunity', 'Career change', 'Personal reasons', 'Performance issues', 'Company restructuring']),
            'exit_interview_score': round(random.uniform(1.0, 5.0), 1),
            'rehire_eligibility': random.choice(['Yes', 'No', 'Maybe']),
            'knowledge_transfer_completed': random.choice(['Yes', 'No', 'Partial']),
            'replacement_hired': random.choice(['Yes', 'No', 'In Progress']),
            'turnover_cost': random.randint(5000, 50000),
            'notice_period_days': random.randint(0, 30)
        })
    
    turnover_df = pd.DataFrame(turnover_data)
    
    # Generate Benefits dataset (200 records)
    benefits_data = []
    for i in range(200):
        employee_id = random.choice(employees_df['employee_id'].tolist())
        enrollment_date = datetime.now() - timedelta(days=random.randint(0, 1095))  # Up to 3 years
        
        benefits_data.append({
            'benefit_id': f'BEN{i+1:03d}',
            'employee_id': employee_id,
            'benefit_type': random.choice(['Health Insurance', 'Dental Insurance', 'Vision Insurance', '401k', 'Life Insurance', 'Disability']),
            'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
            'utilization_rate': round(random.uniform(0.0, 1.0), 2),
            'benefit_cost': random.randint(100, 5000),
            'provider': random.choice(['Blue Cross', 'Aetna', 'Cigna', 'UnitedHealth', 'Kaiser']),
            'coverage_level': random.choice(['Individual', 'Family', 'Employee + Spouse', 'Employee + Children'])
        })
    
    benefits_df = pd.DataFrame(benefits_data)
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter('hr.xlsx', engine='openpyxl') as writer:
        employees_df.to_excel(writer, sheet_name='Employees', index=False)
        recruitment_df.to_excel(writer, sheet_name='Recruitment', index=False)
        performance_df.to_excel(writer, sheet_name='Performance', index=False)
        compensation_df.to_excel(writer, sheet_name='Compensation', index=False)
        training_df.to_excel(writer, sheet_name='Training', index=False)
        engagement_df.to_excel(writer, sheet_name='Engagement', index=False)
        turnover_df.to_excel(writer, sheet_name='Turnover', index=False)
        benefits_df.to_excel(writer, sheet_name='Benefits', index=False)
    
    print("✅ Sample HR dataset generated successfully!")
    print(f"📊 Dataset Summary:")
    print(f"• Employees: {len(employees_df)} records")
    print(f"• Recruitment: {len(recruitment_df)} records")
    print(f"• Performance: {len(performance_df)} records")
    print(f"• Compensation: {len(compensation_df)} records")
    print(f"• Training: {len(training_df)} records")
    print(f"• Engagement: {len(engagement_df)} records")
    print(f"• Turnover: {len(turnover_df)} records")
    print(f"• Benefits: {len(benefits_df)} records")
    print(f"\n📁 File saved as: hr.xlsx")
    
    return {
        'Employees': employees_df,
        'Recruitment': recruitment_df,
        'Performance': performance_df,
        'Compensation': compensation_df,
        'Training': training_df,
        'Engagement': engagement_df,
        'Turnover': turnover_df,
        'Benefits': benefits_df
    }

if __name__ == "__main__":
    generate_sample_hr_dataset()

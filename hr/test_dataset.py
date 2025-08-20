import pandas as pd
import os

try:
    # Load data from hr.xlsx file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file_path = os.path.join(current_dir, 'hr.xlsx')
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)
    
    print("✅ Sample dataset loaded successfully!")
    print(f"📊 Sheets found: {list(excel_data.keys())}")
    print(f"👥 Employees: {len(excel_data['Employees'])} records")
    print(f"🎯 Recruitment: {len(excel_data['Recruitment'])} records")
    print(f"📊 Performance: {len(excel_data['Performance'])} records")
    print(f"💰 Compensation: {len(excel_data['Compensation'])} records")
    print(f"🎓 Training: {len(excel_data['Training'])} records")
    print(f"😊 Engagement: {len(excel_data['Engagement'])} records")
    print(f"🔄 Turnover: {len(excel_data['Turnover'])} records")
    print(f"🏥 Benefits: {len(excel_data['Benefits'])} records")
    
    print("\n🎯 Sample data preview:")
    print("\nEmployees (first 3 records):")
    print(excel_data['Employees'].head(3))
    
    print("\nRecruitment (first 3 records):")
    print(excel_data['Recruitment'].head(3))
    
except Exception as e:
    print(f"❌ Error loading sample dataset: {str(e)}")
    print("Please ensure the hr.xlsx file is available in the hr directory.")

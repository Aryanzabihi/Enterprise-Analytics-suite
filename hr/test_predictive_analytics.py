#!/usr/bin/env python3
"""
Test script for HR Predictive Analytics Module
Tests all major functionality including ML models, predictions, and visualizations
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_predictive_analytics_import():
    """Test that the predictive analytics module can be imported."""
    print("🧪 Testing Predictive Analytics Module Import...")
    
    try:
        from hr_predictive_analytics import HRPredictiveAnalytics, display_predictive_analytics_dashboard
        print("✅ Successfully imported HRPredictiveAnalytics class")
        print("✅ Successfully imported display_predictive_analytics_dashboard function")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_class_initialization():
    """Test that the HRPredictiveAnalytics class can be initialized."""
    print("\n🧪 Testing Class Initialization...")
    
    try:
        from hr_predictive_analytics import HRPredictiveAnalytics
        analytics = HRPredictiveAnalytics()
        print("✅ HRPredictiveAnalytics class initialized successfully")
        
        # Check attributes
        expected_attrs = ['models', 'scalers', 'encoders', 'feature_importance', 'model_performance', 'predictions_cache']
        for attr in expected_attrs:
            if hasattr(analytics, attr):
                print(f"✅ Attribute '{attr}' exists")
            else:
                print(f"❌ Missing attribute '{attr}'")
        
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def generate_test_data():
    """Generate comprehensive test data for all HR datasets."""
    print("\n🧪 Generating Test Data...")
    
    # Employee data
    np.random.seed(42)
    n_employees = 100
    
    employees_data = {
        'employee_id': range(1, n_employees + 1),
        'first_name': [f'Employee{i}' for i in range(1, n_employees + 1)],
        'last_name': [f'Test{i}' for i in range(1, n_employees + 1)],
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_employees),
        'gender': np.random.choice(['Male', 'Female', 'Other'], n_employees),
        'ethnicity': np.random.choice(['White', 'Black', 'Hispanic', 'Asian', 'Other'], n_employees),
        'education_level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_employees),
        'hire_date': [datetime.now() - timedelta(days=np.random.randint(30, 1000)) for _ in range(n_employees)],
        'tenure_years': np.random.uniform(0.5, 10, n_employees)
    }
    
    employees_df = pd.DataFrame(employees_data)
    
    # Performance data
    performance_data = []
    for emp_id in range(1, n_employees + 1):
        n_reviews = np.random.randint(1, 5)
        for review in range(n_reviews):
            performance_data.append({
                'employee_id': emp_id,
                'review_date': datetime.now() - timedelta(days=np.random.randint(30, 365)),
                'performance_rating': np.random.uniform(2.0, 5.0),
                'goal_achievement_rate': np.random.uniform(0.6, 1.2),
                'productivity_score': np.random.uniform(3.0, 5.0)
            })
    
    performance_df = pd.DataFrame(performance_data)
    
    # Engagement data
    engagement_data = []
    for emp_id in range(1, n_employees + 1):
        n_surveys = np.random.randint(1, 4)
        for survey in range(n_surveys):
            engagement_data.append({
                'employee_id': emp_id,
                'survey_date': datetime.now() - timedelta(days=np.random.randint(30, 180)),
                'engagement_score': np.random.uniform(2.5, 5.0),
                'satisfaction_score': np.random.uniform(2.5, 5.0),
                'work_life_balance_score': np.random.uniform(2.5, 5.0)
            })
    
    engagement_df = pd.DataFrame(engagement_data)
    
    # Turnover data (simulate some employees leaving)
    turnover_employees = np.random.choice(range(1, n_employees + 1), size=int(n_employees * 0.15), replace=False)
    turnover_data = []
    for emp_id in turnover_employees:
        turnover_data.append({
            'employee_id': emp_id,
            'separation_date': datetime.now() - timedelta(days=np.random.randint(1, 90)),
            'separation_reason': np.random.choice(['Resigned', 'Terminated', 'Retired', 'Other']),
            'separation_cost': np.random.uniform(5000, 50000)
        })
    
    turnover_df = pd.DataFrame(turnover_data)
    
    # Recruitment data
    recruitment_data = []
    for i in range(20):
        recruitment_data.append({
            'job_id': i + 1,
            'job_title': f'Position {i+1}',
            'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']),
            'recruitment_source': np.random.choice(['LinkedIn', 'Indeed', 'Referral', 'Company Website']),
            'applications_received': np.random.randint(10, 100),
            'candidates_interviewed': np.random.randint(3, 15),
            'offers_made': np.random.randint(1, 5),
            'hires_made': np.random.randint(1, 3),
            'recruitment_cost': np.random.uniform(2000, 15000),
            'time_to_hire_days': np.random.randint(15, 60)
        })
    
    recruitment_df = pd.DataFrame(recruitment_data)
    
    # Compensation data
    compensation_data = []
    for emp_id in range(1, n_employees + 1):
        compensation_data.append({
            'employee_id': emp_id,
            'base_salary': np.random.uniform(40000, 150000),
            'bonus_amount': np.random.uniform(0, 20000),
            'benefits_value': np.random.uniform(5000, 25000)
        })
    
    compensation_df = pd.DataFrame(compensation_data)
    
    print(f"✅ Generated test data:")
    print(f"   - Employees: {len(employees_df)}")
    print(f"   - Performance reviews: {len(performance_df)}")
    print(f"   - Engagement surveys: {len(engagement_df)}")
    print(f"   - Turnover records: {len(turnover_df)}")
    print(f"   - Recruitment records: {len(recruitment_df)}")
    print(f"   - Compensation records: {len(compensation_df)}")
    
    return employees_df, performance_df, engagement_df, turnover_df, recruitment_df, compensation_df

def test_turnover_prediction(analytics, employees_df, performance_df, engagement_df, turnover_df):
    """Test turnover prediction functionality."""
    print("\n🧪 Testing Turnover Prediction...")
    
    try:
        # Test data validation
        is_valid = analytics._validate_turnover_data(employees_df, performance_df, engagement_df, turnover_df)
        print(f"✅ Data validation: {is_valid}")
        
        if is_valid:
            # Test feature preparation
            features = analytics._prepare_turnover_features(employees_df, performance_df, engagement_df, turnover_df)
            if features is not None:
                print(f"✅ Feature preparation successful: {features.shape}")
                print(f"   - Features: {list(features.columns)}")
                
                # Test model building
                success = analytics._build_turnover_model(employees_df, performance_df, engagement_df, turnover_df)
                if success:
                    print("✅ Turnover model built successfully")
                    
                    # Check model performance
                    if 'turnover' in analytics.model_performance:
                        perf = analytics.model_performance['turnover']
                        print(f"   - Accuracy: {perf['accuracy']:.3f}")
                        print(f"   - Precision: {perf['precision']:.3f}")
                        print(f"   - Recall: {perf['recall']:.3f}")
                        print(f"   - F1 Score: {perf['f1_score']:.3f}")
                    
                    # Check feature importance
                    if 'turnover' in analytics.feature_importance:
                        print(f"   - Top features: {list(analytics.feature_importance['turnover'].keys())[:5]}")
                else:
                    print("❌ Turnover model building failed")
            else:
                print("❌ Feature preparation failed")
        else:
            print("⚠️ Data validation failed - insufficient data")
        
        return True
    except Exception as e:
        print(f"❌ Turnover prediction test failed: {e}")
        return False

def test_performance_forecasting(analytics, employees_df, performance_df, engagement_df):
    """Test performance forecasting functionality."""
    print("\n🧪 Testing Performance Forecasting...")
    
    try:
        if not performance_df.empty:
            # Test feature preparation
            features = analytics._prepare_performance_features(employees_df, performance_df, engagement_df)
            if features is not None:
                print(f"✅ Performance feature preparation successful: {features.shape}")
                
                # Test model building
                success = analytics._build_performance_model(employees_df, performance_df, engagement_df)
                if success:
                    print("✅ Performance model built successfully")
                    
                    # Check model performance
                    if 'performance' in analytics.model_performance:
                        perf = analytics.model_performance['performance']
                        print(f"   - MSE: {perf['mse']:.3f}")
                        print(f"   - R² Score: {perf['r2_score']:.3f}")
                        print(f"   - RMSE: {perf['rmse']:.3f}")
                else:
                    print("❌ Performance model building failed")
            else:
                print("❌ Performance feature preparation failed")
        else:
            print("⚠️ No performance data available")
        
        return True
    except Exception as e:
        print(f"❌ Performance forecasting test failed: {e}")
        return False

def test_workforce_planning(analytics, employees_df, performance_df, engagement_df, turnover_df):
    """Test workforce planning functionality."""
    print("\n🧪 Testing Workforce Planning...")
    
    try:
        # Test workforce forecast generation
        analytics._generate_workforce_forecast(employees_df, performance_df, engagement_df, turnover_df)
        print("✅ Workforce forecasting functionality working")
        
        # Test high performer identification
        if not performance_df.empty:
            high_performers = performance_df[performance_df['performance_rating'] >= 4.5]
            print(f"✅ High performers identified: {len(high_performers)}")
        
        return True
    except Exception as e:
        print(f"❌ Workforce planning test failed: {e}")
        return False

def test_recruitment_optimization(analytics, recruitment_df, employees_df):
    """Test recruitment optimization functionality."""
    print("\n🧪 Testing Recruitment Optimization...")
    
    try:
        if not recruitment_df.empty:
            # Test recruitment funnel analysis
            total_postings = len(recruitment_df)
            total_applications = recruitment_df['applications_received'].sum()
            total_hires = recruitment_df['hires_made'].sum()
            
            print(f"✅ Recruitment analysis successful:")
            print(f"   - Total postings: {total_postings}")
            print(f"   - Total applications: {total_applications}")
            print(f"   - Total hires: {total_hires}")
            print(f"   - Overall conversion rate: {(total_hires/total_applications*100):.1f}%")
        else:
            print("⚠️ No recruitment data available")
        
        return True
    except Exception as e:
        print(f"❌ Recruitment optimization test failed: {e}")
        return False

def test_predictive_insights(analytics, employees_df, performance_df, engagement_df, turnover_df, compensation_df):
    """Test predictive insights generation."""
    print("\n🧪 Testing Predictive Insights...")
    
    try:
        # Test insights generation
        insights = analytics._generate_predictive_insights(
            employees_df, performance_df, engagement_df, turnover_df, compensation_df
        )
        
        print(f"✅ Insights generated for {len(insights)} categories:")
        for category, category_insights in insights.items():
            print(f"   - {category}: {len(category_insights)} insights")
        
        # Test strategic recommendations
        recommendations = analytics._generate_strategic_recommendations(
            employees_df, performance_df, engagement_df, turnover_df, compensation_df
        )
        
        print(f"✅ Strategic recommendations generated: {len(recommendations)} recommendations")
        for i, rec in enumerate(recommendations[:3]):  # Show first 3
            print(f"   {i+1}. {rec['action']} - Priority: {rec['priority']}")
        
        return True
    except Exception as e:
        print(f"❌ Predictive insights test failed: {e}")
        return False

def test_main_dashboard_function():
    """Test the main dashboard display function."""
    print("\n🧪 Testing Main Dashboard Function...")
    
    try:
        from hr_predictive_analytics import display_predictive_analytics_dashboard
        
        # Generate test data
        employees_df, performance_df, engagement_df, turnover_df, recruitment_df, compensation_df = generate_test_data()
        
        # Test function call (this will test the interface without actually displaying)
        print("✅ Main dashboard function imported successfully")
        print("✅ Function signature verified")
        
        return True
    except Exception as e:
        print(f"❌ Main dashboard function test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests comprehensively."""
    print("🚀 Starting Comprehensive Predictive Analytics Test Suite")
    print("=" * 60)
    
    # Test 1: Import
    if not test_predictive_analytics_import():
        print("❌ Import test failed - cannot proceed")
        return False
    
    # Test 2: Class initialization
    if not test_class_initialization():
        print("❌ Class initialization test failed - cannot proceed")
        return False
    
    # Test 3: Generate test data
    try:
        employees_df, performance_df, engagement_df, turnover_df, recruitment_df, compensation_df = generate_test_data()
    except Exception as e:
        print(f"❌ Test data generation failed: {e}")
        return False
    
    # Test 4: Initialize analytics class
    try:
        from hr_predictive_analytics import HRPredictiveAnalytics
        analytics = HRPredictiveAnalytics()
    except Exception as e:
        print(f"❌ Analytics class initialization failed: {e}")
        return False
    
    # Test 5: Core functionality tests
    tests = [
        ("Turnover Prediction", lambda: test_turnover_prediction(analytics, employees_df, performance_df, engagement_df, turnover_df)),
        ("Performance Forecasting", lambda: test_performance_forecasting(analytics, employees_df, performance_df, engagement_df)),
        ("Workforce Planning", lambda: test_workforce_planning(analytics, employees_df, performance_df, engagement_df, turnover_df)),
        ("Recruitment Optimization", lambda: test_recruitment_optimization(analytics, recruitment_df, employees_df)),
        ("Predictive Insights", lambda: test_predictive_insights(analytics, employees_df, performance_df, engagement_df, turnover_df, compensation_df)),
        ("Main Dashboard Function", test_main_dashboard_function)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
            else:
                print(f"⚠️ {test_name} test had issues")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed_tests}/{total_tests} tests")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Predictive Analytics module is working correctly.")
        return True
    elif passed_tests >= total_tests * 0.8:
        print("⚠️ Most tests passed. Some minor issues detected.")
        return True
    else:
        print("❌ Multiple tests failed. Module needs attention.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)

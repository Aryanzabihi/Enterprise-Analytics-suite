#!/usr/bin/env python3
"""
Sample Dataset Generator for Customer Service Dashboard
=====================================================

This script generates a comprehensive Excel file with sample data
for all customer service data tables. This provides users with:

1. A reference for the expected data structure
2. Test data for file upload functionality
3. Backup option if memory generation fails
4. Documentation of the data schema

Usage:
    python generate_sample_dataset.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_dataset():
    """Generate comprehensive sample dataset for customer service analytics"""
    
    print("🎧 Generating Customer Service Sample Dataset...")
    
    # Set random seed for reproducible data
    np.random.seed(42)
    
    # Generate sample customers
    print("📊 Generating customers data...")
    customers_data = {
        'customer_id': [f'CUST_{i:03d}' for i in range(1, 101)],
        'customer_name': [f'Customer {i}' for i in range(1, 101)],
        'email': [f'customer{i}@example.com' for i in range(1, 101)],
        'phone': [f'+1-555-{i:03d}-{i:04d}' for i in range(1, 101)],
        'company': [f'Company {i}' for i in range(1, 101)],
        'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 'Education', 'Consulting'], 100),
        'region': np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'], 100),
        'country': np.random.choice(['USA', 'UK', 'Germany', 'Japan', 'Canada', 'Australia', 'France'], 100),
        'customer_segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Startup'], 100, p=[0.2, 0.3, 0.3, 0.2]),
        'acquisition_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'status': np.random.choice(['Active', 'Inactive', 'Prospect'], 100, p=[0.7, 0.2, 0.1]),
        'lifetime_value': np.random.uniform(1000, 100000, 100),
        'last_interaction_date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'preferred_channel': np.random.choice(['Email', 'Phone', 'Chat', 'Social Media', 'Portal'], 100),
        'customer_satisfaction_score': np.random.uniform(1.0, 5.0, 100),
        'total_orders': np.random.randint(1, 50, 100),
        'support_tickets_count': np.random.randint(0, 20, 100)
    }
    
    # Generate sample agents
    print("👥 Generating agents data...")
    agents_data = {
        'agent_id': [f'AGENT_{i:03d}' for i in range(1, 21)],
        'first_name': np.random.choice(['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Tom', 'Emma', 'Alex', 'Maria'], 20),
        'last_name': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'], 20),
        'email': [f'agent{i}@company.com' for i in range(1, 21)],
        'department': np.random.choice(['Support', 'Sales', 'Technical', 'Customer Success', 'Operations'], 20),
        'team': np.random.choice(['Team A', 'Team B', 'Team C', 'Team D'], 20),
        'hire_date': pd.date_range(start='2021-01-01', periods=20, freq='M'),
        'status': np.random.choice(['Active', 'Inactive', 'Training'], 20, p=[0.8, 0.1, 0.1]),
        'manager_id': [f'AGENT_{np.random.randint(1, 6):03d}' for _ in range(20)],
        'specialization': np.random.choice(['General', 'Technical', 'Billing', 'Product', 'Account Management'], 20),
        'performance_score': np.random.uniform(7.0, 10.0, 20),
        'average_response_time_hours': np.random.uniform(1.0, 24.0, 20),
        'satisfaction_score': np.random.uniform(3.5, 5.0, 20),
        'tickets_resolved': np.random.randint(50, 500, 20)
    }
    
    # Generate sample tickets
    print("🎫 Generating tickets data...")
    tickets_data = {
        'ticket_id': [f'TICKET_{i:06d}' for i in range(1, 1001)],
        'customer_id': np.random.choice(customers_data['customer_id'], 1000),
        'agent_id': np.random.choice(agents_data['agent_id'], 1000),
        'ticket_type': np.random.choice(['Support', 'Billing', 'Technical', 'Feature Request', 'Account', 'General'], 1000),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 1000, p=[0.4, 0.35, 0.2, 0.05]),
        'status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated'], 1000, p=[0.15, 0.25, 0.4, 0.15, 0.05]),
        'created_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
        'first_response_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
        'resolved_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
        'escalated_date': [pd.NaT if np.random.random() > 0.1 else pd.Timestamp.now() for _ in range(1000)],
        'channel': np.random.choice(['Email', 'Phone', 'Chat', 'Portal', 'Social Media'], 1000),
        'category': np.random.choice(['Account', 'Technical', 'Billing', 'General', 'Product', 'Access'], 1000),
        'subcategory': np.random.choice(['Login', 'Password', 'Payment', 'Access', 'Feature', 'Bug', 'Question'], 1000),
        'description': [f'Customer reported issue with {np.random.choice(["login", "billing", "access", "feature", "performance"])} - Ticket {i}' for i in range(1, 1001)],
        'resolution_notes': [f'Issue resolved by {np.random.choice(["restart", "update", "configuration", "training", "escalation"])} - Ticket {i}' for i in range(1, 1001)],
        'sla_target_hours': np.random.choice([2, 4, 8, 24, 48], 1000),
        'actual_resolution_hours': np.random.uniform(1, 72, 1000),
        'satisfaction_score': np.random.uniform(1.0, 5.0, 1000),
        'escalation_count': np.random.randint(0, 3, 1000)
    }
    
    # Generate sample interactions
    print("💬 Generating interactions data...")
    interactions_data = {
        'interaction_id': [f'INT_{i:06d}' for i in range(1, 2001)],
        'ticket_id': np.random.choice(tickets_data['ticket_id'], 2000),
        'customer_id': np.random.choice(customers_data['customer_id'], 2000),
        'agent_id': np.random.choice(agents_data['agent_id'], 2000),
        'interaction_type': np.random.choice(['Call', 'Email', 'Chat', 'Note', 'Follow-up'], 2000),
        'start_time': pd.date_range(start='2023-01-01', periods=2000, freq='30min'),
        'end_time': pd.date_range(start='2023-01-01', periods=2000, freq='30min'),
        'duration_minutes': np.random.uniform(5, 120, 2000),
        'channel': np.random.choice(['Email', 'Phone', 'Chat', 'Social Media', 'Portal'], 2000),
        'satisfaction_score': np.random.uniform(1, 5, 2000),
        'notes': [f'Interaction notes for ticket {np.random.choice(tickets_data["ticket_id"])} - {np.random.choice(["resolved", "escalated", "follow-up required"])}' for _ in range(2000)],
        'outcome': np.random.choice(['Resolved', 'Escalated', 'Follow-up Required', 'Information Provided'], 2000),
        'customer_sentiment': np.random.choice(['Positive', 'Neutral', 'Negative', 'Frustrated'], 2000, p=[0.6, 0.25, 0.1, 0.05]),
        'resolution_attempts': np.random.randint(1, 5, 2000)
    }
    
    # Generate sample feedback
    print("😊 Generating feedback data...")
    feedback_data = {
        'feedback_id': [f'FB_{i:06d}' for i in range(1, 501)],
        'ticket_id': np.random.choice(tickets_data['ticket_id'], 500),
        'customer_id': np.random.choice(customers_data['customer_id'], 500),
        'agent_id': np.random.choice(agents_data['agent_id'], 500),
        'feedback_type': np.random.choice(['Satisfaction Survey', 'Follow-up', 'Complaint', 'Compliment', 'Suggestion'], 500),
        'rating': np.random.randint(1, 6, 500),
        'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 500, p=[0.6, 0.3, 0.1]),
        'comments': [f'Customer feedback: {np.random.choice(["Great service", "Could be better", "Excellent support", "Needs improvement", "Very helpful"])} for ticket {i}' for i in range(1, 501)],
        'submitted_date': pd.date_range(start='2023-01-01', periods=500, freq='2H'),
        'response_date': pd.date_range(start='2023-01-01', periods=500, freq='2H'),
        'response_time_hours': np.random.uniform(1, 48, 500),
        'customer_effort_score': np.random.randint(1, 6, 500),
        'nps_score': np.random.randint(0, 10, 500)
    }
    
    # Generate sample SLA
    print("⏱️ Generating SLA data...")
    sla_data = {
        'sla_id': [f'SLA_{i:03d}' for i in range(1, 21)],
        'ticket_type': np.random.choice(['Support', 'Billing', 'Technical', 'Feature Request', 'Account', 'General'], 20),
        'priority': np.random.choice(['Low', 'Medium', 'High', 'Critical'], 20),
        'first_response_target_hours': np.random.choice([1, 2, 4, 8, 24], 20),
        'resolution_target_hours': np.random.choice([4, 8, 24, 48, 72], 20),
        'business_hours_only': np.random.choice([True, False], 20),
        'description': [f'SLA for {np.random.choice(["Support", "Billing", "Technical", "Feature Request"])} tickets with {np.random.choice(["Low", "Medium", "High", "Critical"])} priority' for _ in range(20)],
        'penalty_amount': np.random.uniform(0, 1000, 20),
        'grace_period_hours': np.random.choice([0, 1, 2, 4], 20),
        'auto_escalation_hours': np.random.choice([4, 8, 12, 24], 20)
    }
    
    # Generate sample knowledge base
    print("📚 Generating knowledge base data...")
    kb_data = {
        'kb_id': [f'KB_{i:04d}' for i in range(1, 101)],
        'title': [f'How to {np.random.choice(["reset password", "update profile", "contact support", "access features", "troubleshoot issues", "manage account"])} - Article {i}' for i in range(1, 101)],
        'category': np.random.choice(['General', 'Technical', 'Billing', 'Account', 'Product', 'Troubleshooting'], 100),
        'content': [f'This article explains how to {np.random.choice(["reset password", "update profile", "contact support", "access features", "troubleshoot issues", "manage account"])}. Follow these steps: 1) First step, 2) Second step, 3) Third step. If you need help, contact support.' for _ in range(100)],
        'created_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'updated_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'author_id': np.random.choice(agents_data['agent_id'], 100),
        'views': np.random.randint(10, 5000, 100),
        'helpful_votes': np.random.randint(0, 200, 100),
        'status': np.random.choice(['Published', 'Draft', 'Archived', 'Under Review'], 100, p=[0.7, 0.15, 0.1, 0.05]),
        'tags': [f'{np.random.choice(["beginner", "advanced", "troubleshooting", "how-to", "faq"])}, {np.random.choice(["account", "technical", "billing", "product"])}' for _ in range(100)],
        'last_reviewed_date': pd.date_range(start='2023-01-01', periods=100, freq='W')
    }
    
    # Generate sample training
    print("🎓 Generating training data...")
    training_data = {
        'training_id': [f'TRAIN_{i:04d}' for i in range(1, 51)],
        'agent_id': np.random.choice(agents_data['agent_id'], 50),
        'training_type': np.random.choice(['Product', 'Process', 'Soft Skills', 'Technical', 'Compliance', 'Customer Service'], 50),
        'start_date': pd.date_range(start='2023-01-01', periods=50, freq='W'),
        'completion_date': pd.date_range(start='2023-01-01', periods=50, freq='W'),
        'score': np.random.uniform(60, 100, 50),
        'status': np.random.choice(['Completed', 'In Progress', 'Not Started', 'Failed'], 50, p=[0.7, 0.2, 0.08, 0.02]),
        'trainer_id': np.random.choice(agents_data['agent_id'], 50),
        'notes': [f'Training notes: {np.random.choice(["Excellent progress", "Good understanding", "Needs improvement", "Outstanding performance"])} in {np.random.choice(["Product", "Process", "Soft Skills", "Technical"])} training' for _ in range(50)],
        'duration_hours': np.random.uniform(2, 40, 50),
        'certification_earned': np.random.choice([True, False], 50, p=[0.8, 0.2]),
        'next_training_date': pd.date_range(start='2024-01-01', periods=50, freq='M')
    }
    
    # Create DataFrames
    print("📊 Creating DataFrames...")
    customers_df = pd.DataFrame(customers_data)
    agents_df = pd.DataFrame(agents_data)
    tickets_df = pd.DataFrame(tickets_data)
    interactions_df = pd.DataFrame(interactions_data)
    feedback_df = pd.DataFrame(feedback_data)
    sla_df = pd.DataFrame(sla_data)
    kb_df = pd.DataFrame(kb_data)
    training_df = pd.DataFrame(training_data)
    
    # Create Excel file with multiple sheets
    print("💾 Saving to Excel file...")
    output_file = 'customer_service_sample_dataset.xlsx'
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        customers_df.to_excel(writer, sheet_name='Customers', index=False)
        tickets_df.to_excel(writer, sheet_name='Tickets', index=False)
        agents_df.to_excel(writer, sheet_name='Agents', index=False)
        interactions_df.to_excel(writer, sheet_name='Interactions', index=False)
        feedback_df.to_excel(writer, sheet_name='Feedback', index=False)
        sla_df.to_excel(writer, sheet_name='SLA', index=False)
        kb_df.to_excel(writer, sheet_name='Knowledge_Base', index=False)
        training_df.to_excel(writer, sheet_name='Training', index=False)
        
        # Add an Instructions sheet
        instructions_data = {
            'Sheet Name': ['Customers', 'Tickets', 'Agents', 'Interactions', 'Feedback', 'SLA', 'Knowledge_Base', 'Training'],
            'Purpose': [
                'Customer information and demographics',
                'Support tickets and their details',
                'Support team member information',
                'Customer-agent interactions',
                'Customer satisfaction and feedback',
                'Service level agreements',
                'Help articles and documentation',
                'Agent training records'
            ],
            'Key Columns': [
                'customer_id, customer_name, email, industry, region',
                'ticket_id, customer_id, agent_id, status, priority',
                'agent_id, first_name, last_name, department, team',
                'interaction_id, ticket_id, customer_id, agent_id',
                'feedback_id, ticket_id, rating, sentiment, customer_effort_score, nps_score',
                'sla_id, ticket_type, priority, target_hours',
                'kb_id, title, content, category, status',
                'training_id, agent_id, training_type, score, status'
            ],
            'Record Count': [
                len(customers_df),
                len(tickets_df),
                len(agents_df),
                len(interactions_df),
                len(feedback_df),
                len(sla_df),
                len(kb_df),
                len(training_df)
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f"✅ Sample dataset created successfully: {output_file}")
    print(f"📊 Dataset contains:")
    print(f"   • {len(customers_df)} customers")
    print(f"   • {len(tickets_df)} tickets")
    print(f"   • {len(agents_df)} agents")
    print(f"   • {len(interactions_df)} interactions")
    print(f"   • {len(feedback_df)} feedback records")
    print(f"   • {len(sla_df)} SLA records")
    print(f"   • {len(kb_df)} knowledge base articles")
    print(f"   • {len(training_df)} training records")
    print(f"   • Instructions sheet with usage guidelines")
    
    return output_file

def main():
    """Main function"""
    try:
        output_file = generate_sample_dataset()
        
        print("\n🎯 Next Steps:")
        print("1. Use this file to test the 'Upload Data' functionality")
        print("2. Reference the data structure for your own datasets")
        print("3. The dashboard can also generate sample data in memory")
        print(f"4. File saved as: {output_file}")
        
        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # Convert to MB
            print(f"5. File size: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"❌ Error generating sample dataset: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)

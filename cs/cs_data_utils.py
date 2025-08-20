import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime, timedelta

def display_dataframe_with_index_1(df, **kwargs):
    """Display dataframe with index starting from 1"""
    if not df.empty:
        df_display = df.reset_index(drop=True)
        df_display.index = df_display.index + 1
        return st.dataframe(df_display, **kwargs)
    else:
        return st.dataframe(df, **kwargs)

def create_template_for_download():
    """Create an Excel template with all required customer service data schema and make it downloadable"""
    
    # Create empty DataFrames with the correct customer service schema
    customers_template = pd.DataFrame(columns=[
        'customer_id', 'customer_name', 'email', 'phone', 'company', 'industry', 
        'region', 'country', 'customer_segment', 'acquisition_date', 'status',
        'lifetime_value', 'last_interaction_date', 'preferred_channel'
    ])
    
    tickets_template = pd.DataFrame(columns=[
        'ticket_id', 'customer_id', 'agent_id', 'ticket_type', 'priority', 'status',
        'created_date', 'first_response_date', 'resolved_date', 'escalated_date',
        'channel', 'category', 'subcategory', 'description', 'resolution_notes'
    ])
    
    agents_template = pd.DataFrame(columns=[
        'agent_id', 'first_name', 'last_name', 'email', 'department', 'team',
        'hire_date', 'status', 'manager_id', 'specialization', 'performance_score'
    ])
    
    interactions_template = pd.DataFrame(columns=[
        'interaction_id', 'ticket_id', 'customer_id', 'agent_id', 'interaction_type',
        'start_time', 'end_time', 'duration_minutes', 'channel', 'satisfaction_score',
        'notes', 'outcome'
    ])
    
    feedback_template = pd.DataFrame(columns=[
        'feedback_id', 'ticket_id', 'customer_id', 'agent_id', 'feedback_type',
        'rating', 'sentiment', 'comments', 'submitted_date', 'response_date',
        'customer_effort_score', 'nps_score'
    ])
    
    sla_template = pd.DataFrame(columns=[
        'sla_id', 'ticket_type', 'priority', 'first_response_target_hours',
        'resolution_target_hours', 'business_hours_only', 'description'
    ])
    
    knowledge_base_template = pd.DataFrame(columns=[
        'kb_id', 'title', 'category', 'content', 'created_date', 'updated_date',
        'author_id', 'views', 'helpful_votes', 'status'
    ])
    
    training_template = pd.DataFrame(columns=[
        'training_id', 'agent_id', 'training_type', 'start_date', 'completion_date',
        'score', 'status', 'trainer_id', 'notes'
    ])
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Write each template to a separate sheet
        customers_template.to_excel(writer, sheet_name='Customers', index=False)
        tickets_template.to_excel(writer, sheet_name='Tickets', index=False)
        agents_template.to_excel(writer, sheet_name='Agents', index=False)
        interactions_template.to_excel(writer, sheet_name='Interactions', index=False)
        feedback_template.to_excel(writer, sheet_name='Feedback', index=False)
        sla_template.to_excel(writer, sheet_name='SLA', index=False)
        knowledge_base_template.to_excel(writer, sheet_name='Knowledge_Base', index=False)
        training_template.to_excel(writer, sheet_name='Training', index=False)
        
        # Get the workbook for formatting
        workbook = writer.book
        
        # Add instructions sheet
        instructions_data = {
            'Sheet Name': ['Customers', 'Tickets', 'Agents', 'Interactions', 'Feedback', 'SLA', 'Knowledge_Base', 'Training'],
            'Required Fields': [
                'customer_id, customer_name, email, phone, company, industry, region, country, customer_segment, acquisition_date, status, lifetime_value, last_interaction_date, preferred_channel',
                'ticket_id, customer_id, agent_id, ticket_type, priority, status, created_date, first_response_date, resolved_date, escalated_date, channel, category, subcategory, description, resolution_notes',
                'agent_id, first_name, last_name, email, department, team, hire_date, status, manager_id, specialization, performance_score',
                'interaction_id, ticket_id, customer_id, agent_id, interaction_type, start_time, end_time, duration_minutes, channel, satisfaction_score, notes, outcome',
                'feedback_id, ticket_id, customer_id, agent_id, feedback_type, rating, sentiment, comments, submitted_date, response_date, customer_effort_score, nps_score',
                'sla_id, ticket_type, priority, first_response_target_hours, resolution_target_hours, business_hours_only, description',
                'kb_id, title, category, content, created_date, updated_date, author_id, views, helpful_votes, status',
                'training_id, agent_id, training_type, start_date, completion_date, score, status, trainer_id, notes'
            ],
            'Data Types': [
                'Text, Text, Text, Text, Text, Text, Text, Text, Text, Date, Text, Number, Date, Text',
                'Text, Text, Text, Text, Text, Text, Date, Date, Date, Date, Text, Text, Text, Text, Text',
                'Text, Text, Text, Text, Text, Text, Date, Text, Text, Text, Number',
                'Text, Text, Text, Text, Text, DateTime, DateTime, Number, Text, Number, Text, Text',
                'Text, Text, Text, Text, Text, Number, Text, Text, Date, Date',
                'Text, Text, Text, Number, Number, Boolean, Text',
                'Text, Text, Text, Text, Date, Date, Text, Number, Number, Text',
                'Text, Text, Text, Date, Date, Number, Text, Text, Text'
            ]
        }
        
        instructions_df = pd.DataFrame(instructions_data)
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
    
    # Prepare for download
    output.seek(0)
    return output.getvalue()

def process_uploaded_excel(uploaded_file):
    """Process uploaded Excel file and load data into session state"""
    try:
        # Read all sheets from the Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        
        # Debug: Print what we found
        print(f"🔍 Debug: Found sheets: {list(excel_data.keys())}")
        
        # Check if all required sheets are present
        required_sheets = ['Customers', 'Tickets', 'Agents', 'Interactions', 'Feedback', 'SLA', 'Knowledge_Base', 'Training']
        missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
        
        if missing_sheets:
            return False, f"Missing required sheets: {', '.join(missing_sheets)}"
        
        # Load data into session state with verification
        st.session_state.customers = excel_data['Customers'].copy()
        st.session_state.tickets = excel_data['Tickets'].copy()
        st.session_state.agents = excel_data['Agents'].copy()
        st.session_state.interactions = excel_data['Interactions'].copy()
        st.session_state.feedback = excel_data['Feedback'].copy()
        st.session_state.sla = excel_data['SLA'].copy()
        st.session_state.knowledge_base = excel_data['Knowledge_Base'].copy()
        st.session_state.training = excel_data['Training'].copy()
        
        # Verify data was loaded correctly
        print(f"🔍 Debug: Session state after loading:")
        print(f"   Customers: {len(st.session_state.customers)} rows")
        print(f"   Tickets: {len(st.session_state.tickets)} rows")
        print(f"   Agents: {len(st.session_state.agents)} rows")
        print(f"   Feedback: {len(st.session_state.feedback)} rows")
        print(f"   Feedback columns: {list(st.session_state.feedback.columns)}")
        
        # Double-check critical columns exist
        if 'customer_effort_score' not in st.session_state.feedback.columns:
            return False, "Feedback data missing 'customer_effort_score' column"
        if 'nps_score' not in st.session_state.feedback.columns:
            return False, "Feedback data missing 'nps_score' column"
        
        return True, f"All customer service data loaded successfully! Loaded {len(st.session_state.customers)} customers, {len(st.session_state.tickets)} tickets, {len(st.session_state.agents)} agents, {len(st.session_state.feedback)} feedback records, and more..."
        
    except Exception as e:
        print(f"🔍 Debug: Error in process_uploaded_excel: {str(e)}")
        return False, f"Error reading Excel file: {str(e)}"

def load_sample_dataset(file_path):
    """Load sample dataset from Excel file for testing purposes"""
    try:
        # Read all sheets from the sample Excel file
        excel_data = pd.read_excel(file_path, sheet_name=None)
        
        # Check if all required sheets are present
        required_sheets = ['Customers', 'Tickets', 'Agents', 'Interactions', 'Feedback', 'SLA', 'Knowledge_Base', 'Training']
        missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_data.keys()]
        
        if missing_sheets:
            return False, f"Missing required sheets in sample dataset: {', '.join(missing_sheets)}"
        
        # Load data into session state
        st.session_state.customers = excel_data['Customers']
        st.session_state.tickets = excel_data['Tickets']
        st.session_state.agents = excel_data['Agents']
        st.session_state.interactions = excel_data['Interactions']
        st.session_state.feedback = excel_data['Feedback']
        st.session_state.sla = excel_data['SLA']
        st.session_state.knowledge_base = excel_data['Knowledge_Base']
        st.session_state.training = excel_data['Training']
        
        return True, f"Sample dataset loaded successfully! Loaded {len(st.session_state.customers)} customers, {len(st.session_state.tickets)} tickets, {len(st.session_state.agents)} agents, {len(st.session_state.interactions)} interactions, {len(st.session_state.feedback)} feedback records, {len(st.session_state.sla)} SLA records, {len(st.session_state.knowledge_base)} knowledge base articles, and {len(st.session_state.training)} training records."
        
    except Exception as e:
        return False, f"Error loading sample dataset: {str(e)}"

def export_data_to_excel():
    """Exports all customer service data from session state to a single Excel file."""
    with pd.ExcelWriter('customer_service_data_export.xlsx', engine='xlsxwriter') as writer:
        if not st.session_state.customers.empty:
            st.session_state.customers.to_excel(writer, sheet_name='Customers', index=False)
        if not st.session_state.tickets.empty:
            st.session_state.tickets.to_excel(writer, sheet_name='Tickets', index=False)
        if not st.session_state.agents.empty:
            st.session_state.agents.to_excel(writer, sheet_name='Agents', index=False)
        if not st.session_state.interactions.empty:
            st.session_state.interactions.to_excel(writer, sheet_name='Interactions', index=False)
        if not st.session_state.feedback.empty:
            st.session_state.feedback.to_excel(writer, sheet_name='Feedback', index=False)
        if not st.session_state.sla.empty:
            st.session_state.sla.to_excel(writer, sheet_name='SLA', index=False)
        if not st.session_state.knowledge_base.empty:
            st.session_state.knowledge_base.to_excel(writer, sheet_name='Knowledge_Base', index=False)
        if not st.session_state.training.empty:
            st.session_state.training.to_excel(writer, sheet_name='Training', index=False)
        
        st.success("Customer service data exported successfully as 'customer_service_data_export.xlsx'")

def initialize_session_state():
    """Initialize session state variables for customer service data"""
    if 'customers' not in st.session_state:
        st.session_state.customers = pd.DataFrame()
    if 'tickets' not in st.session_state:
        st.session_state.tickets = pd.DataFrame()
    if 'agents' not in st.session_state:
        st.session_state.agents = pd.DataFrame()
    if 'interactions' not in st.session_state:
        st.session_state.interactions = pd.DataFrame()
    if 'feedback' not in st.session_state:
        st.session_state.feedback = pd.DataFrame()
    if 'sla' not in st.session_state:
        st.session_state.sla = pd.DataFrame()
    if 'knowledge_base' not in st.session_state:
        st.session_state.knowledge_base = pd.DataFrame()
    if 'training' not in st.session_state:
        st.session_state.training = pd.DataFrame()

def validate_data_integrity():
    """Validate the integrity of loaded customer service data"""
    validation_results = []
    
    # Check for required columns in each dataset
    required_columns = {
        'customers': ['customer_id', 'customer_name'],
        'tickets': ['ticket_id', 'customer_id', 'status'],
        'agents': ['agent_id', 'first_name', 'last_name'],
        'interactions': ['interaction_id', 'ticket_id'],
        'feedback': ['feedback_id', 'ticket_id', 'rating'],
        'sla': ['sla_id', 'ticket_type', 'priority'],
        'knowledge_base': ['kb_id', 'title', 'content'],
        'training': ['training_id', 'agent_id', 'training_type']
    }
    
    for dataset_name, required_cols in required_columns.items():
        if dataset_name in st.session_state and not st.session_state[dataset_name].empty:
            dataset = st.session_state[dataset_name]
            missing_cols = [col for col in required_cols if col not in dataset.columns]
            if missing_cols:
                validation_results.append(f"❌ {dataset_name.title()}: Missing columns {', '.join(missing_cols)}")
            else:
                validation_results.append(f"✅ {dataset_name.title()}: All required columns present")
        else:
            validation_results.append(f"⚠️ {dataset_name.title()}: No data loaded")
    
    # Check for data relationships
    if not st.session_state.customers.empty and not st.session_state.tickets.empty:
        customer_ids_in_tickets = set(st.session_state.tickets['customer_id'].unique())
        customer_ids_in_customers = set(st.session_state.customers['customer_id'].unique())
        orphaned_tickets = customer_ids_in_tickets - customer_ids_in_customers
        
        if orphaned_tickets:
            validation_results.append(f"⚠️ Found {len(orphaned_tickets)} tickets with non-existent customer IDs")
        else:
            validation_results.append("✅ All tickets have valid customer IDs")
    
    return validation_results

def get_data_summary():
    """Get a summary of all loaded customer service data"""
    summary = {}
    
    datasets = {
        'customers': 'Customers',
        'tickets': 'Tickets', 
        'agents': 'Agents',
        'interactions': 'Interactions',
        'feedback': 'Feedback',
        'sla': 'SLA Records',
        'knowledge_base': 'Knowledge Base Articles',
        'training': 'Training Records'
    }
    
    for key, display_name in datasets.items():
        if key in st.session_state and not st.session_state[key].empty:
            summary[display_name] = len(st.session_state[key])
        else:
            summary[display_name] = 0
    
    return summary

def clean_and_prepare_data():
    """Clean and prepare customer service data for analysis"""
    try:
        # Clean customers data
        if not st.session_state.customers.empty:
            # Remove duplicates
            st.session_state.customers = st.session_state.customers.drop_duplicates()
            
            # Clean customer names
            if 'customer_name' in st.session_state.customers.columns:
                st.session_state.customers['customer_name'] = st.session_state.customers['customer_name'].str.strip()
            
            # Convert dates
            date_columns = ['acquisition_date', 'last_interaction_date']
            for col in date_columns:
                if col in st.session_state.customers.columns:
                    st.session_state.customers[col] = pd.to_datetime(st.session_state.customers[col], errors='coerce')
        
        # Clean tickets data
        if not st.session_state.tickets.empty:
            # Remove duplicates
            st.session_state.tickets = st.session_state.tickets.drop_duplicates()
            
            # Convert dates
            date_columns = ['created_date', 'first_response_date', 'resolved_date', 'escalated_date']
            for col in date_columns:
                if col in st.session_state.tickets.columns:
                    st.session_state.tickets[col] = pd.to_datetime(st.session_state.tickets[col], errors='coerce')
            
            # Clean status values
            if 'status' in st.session_state.tickets.columns:
                st.session_state.tickets['status'] = st.session_state.tickets['status'].str.lower().str.strip()
        
        # Clean interactions data
        if not st.session_state.interactions.empty:
            # Remove duplicates
            st.session_state.interactions = st.session_state.interactions.drop_duplicates()
            
            # Convert dates
            date_columns = ['start_time', 'end_time']
            for col in date_columns:
                if col in st.session_state.interactions.columns:
                    st.session_state.interactions[col] = pd.to_datetime(st.session_state.interactions[col], errors='coerce')
            
            # Calculate duration if not present
            if 'start_time' in st.session_state.interactions.columns and 'end_time' in st.session_state.interactions.columns:
                st.session_state.interactions['duration_minutes'] = (
                    st.session_state.interactions['end_time'] - st.session_state.interactions['start_time']
                ).dt.total_seconds() / 60
        
        # Clean feedback data
        if not st.session_state.feedback.empty:
            # Remove duplicates
            st.session_state.feedback = st.session_state.feedback.drop_duplicates()
            
            # Convert dates
            date_columns = ['submitted_date', 'response_date']
            for col in date_columns:
                if col in st.session_state.feedback.columns:
                    st.session_state.feedback[col] = pd.to_datetime(st.session_state.feedback[col], errors='coerce')
            
            # Clean sentiment values
            if 'sentiment' in st.session_state.feedback.columns:
                st.session_state.feedback['sentiment'] = st.session_state.feedback['sentiment'].str.lower().str.strip()
        
        return True, "Data cleaned and prepared successfully"
        
    except Exception as e:
        return False, f"Error cleaning data: {str(e)}"

def generate_sample_data():
    """Generate sample customer service data for testing purposes"""
    try:
        # Generate sample customers
        customers_data = {
            'customer_id': [f'CUST_{i:03d}' for i in range(1, 101)],
            'customer_name': [f'Customer {i}' for i in range(1, 101)],
            'email': [f'customer{i}@example.com' for i in range(1, 101)],
            'phone': [f'+1-555-{i:03d}-{i:04d}' for i in range(1, 101)],
            'company': [f'Company {i}' for i in range(1, 101)],
            'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing'], 100),
            'region': np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], 100),
            'country': np.random.choice(['USA', 'UK', 'Germany', 'Japan', 'Canada'], 100),
            'customer_segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB'], 100),
            'acquisition_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
            'status': np.random.choice(['Active', 'Inactive'], 100, p=[0.8, 0.2]),
            'lifetime_value': np.random.uniform(1000, 50000, 100),
            'last_interaction_date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
            'preferred_channel': np.random.choice(['Email', 'Phone', 'Chat', 'Social Media'], 100)
        }
        
        # Generate sample agents
        agents_data = {
            'agent_id': [f'AGENT_{i:03d}' for i in range(1, 21)],
            'first_name': [f'Agent{i}' for i in range(1, 21)],
            'last_name': [f'Smith{i}' for i in range(1, 21)],
            'email': [f'agent{i}@company.com' for i in range(1, 21)],
            'department': np.random.choice(['Support', 'Sales', 'Technical'], 20),
            'team': np.random.choice(['Team A', 'Team B', 'Team C'], 20),
            'hire_date': pd.date_range(start='2021-01-01', periods=20, freq='M'),
            'status': np.random.choice(['Active', 'Inactive'], 20, p=[0.9, 0.1]),
            'manager_id': [f'AGENT_{np.random.randint(1, 6):03d}' for _ in range(20)],
            'specialization': np.random.choice(['General', 'Technical', 'Billing', 'Product'], 20),
            'performance_score': np.random.uniform(7.0, 10.0, 20)
        }
        
        # Generate sample tickets
        tickets_data = {
            'ticket_id': [f'TICKET_{i:06d}' for i in range(1, 1001)],
            'customer_id': np.random.choice(customers_data['customer_id'], 1000),
            'agent_id': np.random.choice(agents_data['agent_id'], 1000),
            'ticket_type': np.random.choice(['Support', 'Billing', 'Technical', 'Feature Request'], 1000),
            'priority': np.random.choice(['Low', 'Medium', 'High'], 1000, p=[0.5, 0.3, 0.2]),
            'status': np.random.choice(['Open', 'In Progress', 'Resolved', 'Closed'], 1000, p=[0.2, 0.3, 0.4, 0.1]),
            'created_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
            'first_response_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
            'resolved_date': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
            'escalated_date': [pd.NaT if np.random.random() > 0.1 else pd.Timestamp.now() for _ in range(1000)],
            'channel': np.random.choice(['Email', 'Phone', 'Chat', 'Portal'], 1000),
            'category': np.random.choice(['Account', 'Technical', 'Billing', 'General'], 1000),
            'subcategory': np.random.choice(['Login', 'Password', 'Payment', 'Access'], 1000),
            'description': [f'Ticket description {i}' for i in range(1, 1001)],
            'resolution_notes': [f'Resolution notes for ticket {i}' for i in range(1, 1001)]
        }
        
        # Generate sample interactions
        interactions_data = {
            'interaction_id': [f'INT_{i:06d}' for i in range(1, 2001)],
            'ticket_id': np.random.choice(tickets_data['ticket_id'], 2000),
            'customer_id': np.random.choice(customers_data['customer_id'], 2000),
            'agent_id': np.random.choice(agents_data['agent_id'], 2000),
            'interaction_type': np.random.choice(['Call', 'Email', 'Chat', 'Note'], 2000),
            'start_time': pd.date_range(start='2023-01-01', periods=2000, freq='30min'),
            'end_time': pd.date_range(start='2023-01-01', periods=2000, freq='30min'),
            'duration_minutes': np.random.uniform(5, 120, 2000),
            'channel': np.random.choice(['Email', 'Phone', 'Chat', 'Social Media'], 2000),
            'satisfaction_score': np.random.uniform(1, 5, 2000),
            'notes': [f'Interaction notes {i}' for i in range(1, 2001)],
            'outcome': np.random.choice(['Resolved', 'Escalated', 'Follow-up Required'], 2000)
        }
        
        # Generate sample feedback
        feedback_data = {
            'feedback_id': [f'FB_{i:06d}' for i in range(1, 501)],
            'ticket_id': np.random.choice(tickets_data['ticket_id'], 500),
            'customer_id': np.random.choice(customers_data['customer_id'], 500),
            'agent_id': np.random.choice(agents_data['agent_id'], 500),
            'feedback_type': np.random.choice(['Satisfaction Survey', 'Follow-up', 'Complaint', 'CES', 'NPS'], 500),
            'rating': np.random.randint(1, 6, 500),
            'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 500, p=[0.6, 0.3, 0.1]),
            'comments': [f'Feedback comment {i}' for i in range(1, 501)],
            'submitted_date': pd.date_range(start='2023-01-01', periods=500, freq='2H'),
            'response_date': pd.date_range(start='2023-01-01', periods=500, freq='2H'),
            'customer_effort_score': np.random.randint(1, 7, 500),
            'nps_score': np.random.randint(0, 11, 500)
        }
        
        # Generate sample SLA
        sla_data = {
            'sla_id': [f'SLA_{i:03d}' for i in range(1, 21)],
            'ticket_type': np.random.choice(['Support', 'Billing', 'Technical', 'Feature Request'], 20),
            'priority': np.random.choice(['Low', 'Medium', 'High'], 20),
            'first_response_target_hours': np.random.choice([2, 4, 8, 24], 20),
            'resolution_target_hours': np.random.choice([8, 24, 48, 72], 20),
            'business_hours_only': np.random.choice([True, False], 20),
            'description': [f'SLA description {i}' for i in range(1, 21)]
        }
        
        # Generate sample knowledge base
        kb_data = {
            'kb_id': [f'KB_{i:04d}' for i in range(1, 101)],
            'title': [f'Knowledge Base Article {i}' for i in range(1, 101)],
            'category': np.random.choice(['General', 'Technical', 'Billing', 'Account'], 100),
            'content': [f'Content for KB article {i}' for i in range(1, 101)],
            'created_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
            'updated_date': pd.date_range(start='2022-01-01', periods=100, freq='D'),
            'author_id': np.random.choice(agents_data['agent_id'], 100),
            'views': np.random.randint(10, 1000, 100),
            'helpful_votes': np.random.randint(0, 100, 100),
            'status': np.random.choice(['Published', 'Draft', 'Archived'], 100, p=[0.8, 0.15, 0.05])
        }
        
        # Generate sample training
        training_data = {
            'training_id': [f'TRAIN_{i:04d}' for i in range(1, 51)],
            'agent_id': np.random.choice(agents_data['agent_id'], 50),
            'training_type': np.random.choice(['Product', 'Process', 'Soft Skills', 'Technical'], 50),
            'start_date': pd.date_range(start='2023-01-01', periods=50, freq='W'),
            'completion_date': pd.date_range(start='2023-01-01', periods=50, freq='W'),
            'score': np.random.uniform(60, 100, 50),
            'status': np.random.choice(['Completed', 'In Progress', 'Not Started'], 50, p=[0.7, 0.2, 0.1]),
            'trainer_id': np.random.choice(agents_data['agent_id'], 50),
            'notes': [f'Training notes {i}' for i in range(1, 51)]
        }
        
        # Create DataFrames
        st.session_state.customers = pd.DataFrame(customers_data)
        st.session_state.agents = pd.DataFrame(agents_data)
        st.session_state.tickets = pd.DataFrame(tickets_data)
        st.session_state.interactions = pd.DataFrame(interactions_data)
        st.session_state.feedback = pd.DataFrame(feedback_data)
        st.session_state.sla = pd.DataFrame(sla_data)
        st.session_state.knowledge_base = pd.DataFrame(kb_data)
        st.session_state.training = pd.DataFrame(training_data)
        
        return True, "Sample data generated successfully"
        
    except Exception as e:
        return False, f"Error generating sample data: {str(e)}"

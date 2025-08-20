import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime
from ..cs_data_utils import (
    process_uploaded_excel, 
    create_template_for_download, 
    generate_sample_data,
    export_data_to_excel,
    clean_and_prepare_data,
    get_data_summary,
    load_sample_dataset
)
from ..cs_styling import create_metric_card, create_alert_box

def show_data_input():
    """Display the data input and management page"""
    
    st.markdown("## 📝 Data Input & Management")
    
    # Create tabs for different data management functions
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📤 Upload Data", 
        "📝 Manual Entry", 
        "📁 Load Sample File",
        "📋 Download Template",
        "📊 Data Overview",
        "🔧 Data Management"
    ])
    
    with tab1:
        st.markdown("### 📤 Upload Customer Service Data")
        
        st.info("""
        **Required Data Structure:**
        - **Customers**: Customer information and demographics
        - **Tickets**: Support tickets and their details
        - **Agents**: Support team member information
        - **Interactions**: Customer-agent interactions
        - **Feedback**: Customer satisfaction and feedback
        - **SLA**: Service level agreements
        - **Knowledge Base**: Help articles and documentation
        - **Training**: Agent training records
        """)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an Excel file with customer service data",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with multiple sheets for different data types",
            key="upload_customer_service_data"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Process the uploaded file
            if st.button("🔄 Process Uploaded File", type="primary"):
                with st.spinner("Processing uploaded file..."):
                    success, message = process_uploaded_excel(uploaded_file)
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Data validation after upload
        if not st.session_state.customers.empty or not st.session_state.tickets.empty:
            st.markdown("### ✅ Data Validation Results")
            
            # Check data integrity
            from cs_data_utils import validate_data_integrity
            validation_results = validate_data_integrity()
            
            for result in validation_results:
                if "✅" in result:
                    st.success(result)
                elif "⚠️" in result:
                    st.warning(result)
                else:
                    st.error(result)
    
    with tab2:
        st.markdown("### 📝 Manual Data Entry")
        
        st.info("""
        **Manually enter customer service data** for small datasets or when you need to add specific records.
        This is ideal for testing or when you have a few records to add manually.
        """)
        
        # Create subtabs for different data types
        entry_tab1, entry_tab2, entry_tab3, entry_tab4, entry_tab5, entry_tab6, entry_tab7, entry_tab8 = st.tabs([
            "👤 Customer", "🎫 Ticket", "👥 Agent", "😊 Feedback", "📋 SLA", "💬 Interactions", "📚 Knowledge Base", "🎓 Training"
        ])
        
        # Customer Entry Tab
        with entry_tab1:
            st.subheader("👤 Add Customer")
            col1, col2 = st.columns(2)
            
            with col1:
                customer_id = st.text_input("Customer ID", placeholder="CUST_001", key="customer_entry_id")
                customer_name = st.text_input("Customer Name", placeholder="John Doe", key="customer_entry_name")
                email = st.text_input("Email", placeholder="john@example.com", key="customer_entry_email")
                phone = st.text_input("Phone", placeholder="+1-555-0123", key="customer_entry_phone")
            
            with col2:
                company = st.text_input("Company", placeholder="Acme Corp", key="customer_entry_company")
                industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance", "Retail", "Other"], key="customer_entry_industry")
                region = st.selectbox("Region", ["North America", "Europe", "Asia", "Other"], key="customer_entry_region")
                customer_type = st.selectbox("Customer Type", ["New", "Existing", "VIP"], key="customer_entry_type")
            
            if st.button("➕ Add Customer", type="primary", key="customer_entry_button"):
                if customer_id and customer_name:
                    # Create new customer record
                    new_customer = pd.DataFrame([{
                        'customer_id': customer_id,
                        'customer_name': customer_name,
                        'email': email,
                        'phone': phone,
                        'company': company,
                        'industry': industry,
                        'region': region,
                        'customer_type': customer_type,
                        'acquisition_date': pd.Timestamp.now(),
                        'last_interaction_date': pd.Timestamp.now()
                    }])
                    
                    # Add to session state
                    if 'customers' in st.session_state and not st.session_state.customers.empty:
                        st.session_state.customers = pd.concat([st.session_state.customers, new_customer], ignore_index=True)
                    else:
                        st.session_state.customers = new_customer
                    
                    st.success(f"✅ Customer {customer_name} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Customer ID and Name are required!")
        
        # Ticket Entry Tab
        with entry_tab2:
            st.subheader("🎫 Add Support Ticket")
            col1, col2 = st.columns(2)
            
            with col1:
                ticket_id = st.text_input("Ticket ID", placeholder="TICKET_001", key="ticket_entry_id")
                customer_id = st.text_input("Customer ID", placeholder="CUST_001", key="ticket_entry_customer_id")
                subject = st.text_input("Subject", placeholder="Technical Issue", key="ticket_entry_subject")
                description = st.text_area("Description", placeholder="Describe the issue...", key="ticket_entry_description")
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="ticket_entry_priority")
            
            with col2:
                category = st.selectbox("Category", ["Technical", "Billing", "General", "Feature Request"], key="ticket_entry_category")
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], key="ticket_entry_status")
                agent_id = st.text_input("Agent ID", placeholder="AGENT_001", key="ticket_entry_agent_id")
                created_date = st.date_input("Created Date", value=pd.Timestamp.now().date(), key="ticket_entry_date")
            
            if st.button("➕ Add Ticket", type="primary", key="ticket_entry_button"):
                if ticket_id and customer_id and subject:
                    # Create new ticket record
                    new_ticket = pd.DataFrame([{
                        'ticket_id': ticket_id,
                        'customer_id': customer_id,
                        'subject': subject,
                        'description': description,
                        'priority': priority,
                        'category': category,
                        'status': status,
                        'agent_id': agent_id,
                        'created_date': pd.Timestamp(created_date),
                        'first_response_date': None,
                        'resolved_date': None
                    }])
                    
                    # Add to session state
                    if 'tickets' in st.session_state and not st.session_state.tickets.empty:
                        st.session_state.tickets = pd.concat([st.session_state.tickets, new_ticket], ignore_index=True)
                    else:
                        st.session_state.tickets = new_ticket
                    
                    st.success(f"✅ Ticket {ticket_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Ticket ID, Customer ID, and Subject are required!")
        
        # Agent Entry Tab
        with entry_tab3:
            st.subheader("👥 Add Agent")
            col1, col2 = st.columns(2)
            
            with col1:
                agent_id = st.text_input("Agent ID", placeholder="AGENT_001", key="agent_entry_id")
                first_name = st.text_input("First Name", placeholder="John", key="agent_entry_first_name")
                last_name = st.text_input("Last Name", placeholder="Smith", key="agent_entry_last_name")
                email = st.text_input("Email", placeholder="john.smith@company.com", key="agent_entry_email")
            
            with col2:
                department = st.selectbox("Department", ["Support", "Sales", "Technical", "Management"], key="agent_entry_department")
                team = st.selectbox("Team", ["Tier 1", "Tier 2", "Tier 3", "Specialist"], key="agent_entry_team")
                hire_date = st.date_input("Hire Date", value=pd.Timestamp.now().date(), key="agent_entry_hire_date")
                experience_level = st.selectbox("Experience Level", ["Junior", "Mid-level", "Senior", "Lead"], key="agent_entry_experience")
            
            if st.button("➕ Add Agent", type="primary", key="agent_entry_button"):
                if agent_id and first_name and last_name:
                    # Create new agent record
                    new_agent = pd.DataFrame([{
                        'agent_id': agent_id,
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'department': department,
                        'team': team,
                        'hire_date': pd.Timestamp(hire_date),
                        'experience_level': experience_level
                    }])
                    
                    # Add to session state
                    if 'agents' in st.session_state and not st.session_state.agents.empty:
                        st.session_state.agents = pd.concat([st.session_state.agents, new_agent], ignore_index=True)
                    else:
                        st.session_state.agents = new_agent
                    
                    st.success(f"✅ Agent {first_name} {last_name} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Agent ID, First Name, and Last Name are required!")
        
        # Feedback Entry Tab
        with entry_tab4:
            st.subheader("😊 Add Customer Feedback")
            col1, col2 = st.columns(2)
            
            with col1:
                feedback_id = st.text_input("Feedback ID", placeholder="FB_001", key="feedback_entry_id")
                ticket_id = st.text_input("Ticket ID", placeholder="TICKET_001", key="feedback_entry_ticket_id")
                customer_id = st.text_input("Customer ID", placeholder="CUST_001", key="feedback_entry_customer_id")
                rating = st.slider("Rating (1-5)", 1, 5, 4, key="feedback_entry_rating")
                nps_score = st.slider("NPS Score (0-10)", 0, 10, 8, key="feedback_entry_nps")
            
            with col2:
                customer_effort_score = st.slider("Effort Score (1-6)", 1, 6, 2, key="feedback_entry_effort")
                sentiment = st.selectbox("Sentiment", ["Positive", "Neutral", "Negative"], key="feedback_entry_sentiment")
                feedback_type = st.selectbox("Feedback Type", ["Compliment", "Complaint", "Suggestion", "Question"], key="feedback_entry_type")
                submitted_date = st.date_input("Submitted Date", value=pd.Timestamp.now().date(), key="feedback_entry_date")
            
            comments = st.text_area("Comments", placeholder="Additional feedback...", key="feedback_entry_comments")
            
            if st.button("➕ Add Feedback", type="primary", key="feedback_entry_button"):
                if feedback_id and ticket_id and customer_id:
                    # Create new feedback record
                    new_feedback = pd.DataFrame([{
                        'feedback_id': feedback_id,
                        'ticket_id': ticket_id,
                        'customer_id': customer_id,
                        'rating': rating,
                        'nps_score': nps_score,
                        'customer_effort_score': customer_effort_score,
                        'sentiment': sentiment,
                        'feedback_type': feedback_type,
                        'comments': comments,
                        'submitted_date': pd.Timestamp(submitted_date)
                    }])
                    
                    # Add to session state
                    if 'feedback' in st.session_state and not st.session_state.feedback.empty:
                        st.session_state.feedback = pd.concat([st.session_state.feedback, new_feedback], ignore_index=True)
                    else:
                        st.session_state.feedback = new_feedback
                    
                    st.success(f"✅ Feedback {feedback_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Feedback ID, Ticket ID, and Customer ID are required!")
        
        # SLA Entry Tab
        with entry_tab5:
            st.subheader("📋 Add SLA Record")
            col1, col2 = st.columns(2)
            
            with col1:
                sla_id = st.text_input("SLA ID", placeholder="SLA_001", key="sla_entry_id")
                ticket_type = st.selectbox("Ticket Type", ["Technical", "Billing", "General", "Feature Request"], key="sla_entry_ticket_type")
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="sla_entry_priority")
                response_time_hours = st.number_input("Response Time (Hours)", min_value=1, value=4, key="sla_entry_response_time")
            
            with col2:
                resolution_time_hours = st.number_input("Resolution Time (Hours)", min_value=1, value=24, key="sla_entry_resolution_time")
                sla_status = st.selectbox("SLA Status", ["Active", "Inactive", "Suspended"], key="sla_entry_status")
                business_hours = st.checkbox("Business Hours Only", value=True, key="sla_entry_business_hours")
                auto_escalate = st.checkbox("Auto-escalate", value=False, key="sla_entry_auto_escalate")
            
            if st.button("➕ Add SLA Record", type="primary", key="sla_entry_button"):
                if sla_id and ticket_type and priority:
                    # Create new SLA record
                    new_sla = pd.DataFrame([{
                        'sla_id': sla_id,
                        'ticket_type': ticket_type,
                        'priority': priority,
                        'response_time_hours': response_time_hours,
                        'resolution_time_hours': resolution_time_hours,
                        'sla_status': sla_status,
                        'business_hours': business_hours,
                        'auto_escalate': auto_escalate
                    }])
                    
                    # Add to session state
                    if 'sla' in st.session_state and not st.session_state.sla.empty:
                        st.session_state.sla = pd.concat([st.session_state.sla, new_sla], ignore_index=True)
                    else:
                        st.session_state.sla = new_sla
                    
                    st.success(f"✅ SLA Record {sla_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ SLA ID, Ticket Type, and Priority are required!")
        
        # Interactions Entry Tab
        with entry_tab6:
            st.subheader("💬 Add Customer Interaction")
            col1, col2 = st.columns(2)
            
            with col1:
                interaction_id = st.text_input("Interaction ID", placeholder="INT_001", key="interaction_entry_id")
                ticket_id = st.text_input("Ticket ID", placeholder="TICKET_001", key="interaction_entry_ticket_id")
                customer_id = st.text_input("Customer ID", placeholder="CUST_001", key="interaction_entry_customer_id")
                agent_id = st.text_input("Agent ID", placeholder="AGENT_001", key="interaction_entry_agent_id")
                interaction_type = st.selectbox("Interaction Type", ["Phone", "Email", "Chat", "In-Person", "Video Call"], key="interaction_entry_type")
            
            with col2:
                channel = st.selectbox("Channel", ["Phone", "Email", "Live Chat", "Social Media", "Portal", "Mobile App"], key="interaction_entry_channel")
                direction = st.selectbox("Direction", ["Inbound", "Outbound"], key="interaction_entry_direction")
                duration_minutes = st.number_input("Duration (Minutes)", min_value=1, value=15, key="interaction_entry_duration")
                interaction_date = st.date_input("Interaction Date", value=pd.Timestamp.now().date(), key="interaction_entry_date")
            
            notes = st.text_area("Interaction Notes", placeholder="Summary of the interaction...", key="interaction_entry_notes")
            
            if st.button("➕ Add Interaction", type="primary", key="interaction_entry_button"):
                if interaction_id and ticket_id and customer_id and agent_id:
                    # Create new interaction record
                    new_interaction = pd.DataFrame([{
                        'interaction_id': interaction_id,
                        'ticket_id': ticket_id,
                        'customer_id': customer_id,
                        'agent_id': agent_id,
                        'interaction_type': interaction_type,
                        'channel': channel,
                        'direction': direction,
                        'duration_minutes': duration_minutes,
                        'interaction_date': pd.Timestamp(interaction_date),
                        'notes': notes
                    }])
                    
                    # Add to session state
                    if 'interactions' in st.session_state and not st.session_state.interactions.empty:
                        st.session_state.interactions = pd.concat([st.session_state.interactions, new_interaction], ignore_index=True)
                    else:
                        st.session_state.interactions = new_interaction
                    
                    st.success(f"✅ Interaction {interaction_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Interaction ID, Ticket ID, Customer ID, and Agent ID are required!")
        
        # Knowledge Base Entry Tab
        with entry_tab7:
            st.subheader("📚 Add Knowledge Base Article")
            col1, col2 = st.columns(2)
            
            with col1:
                kb_id = st.text_input("KB ID", placeholder="KB_001", key="kb_entry_id")
                title = st.text_input("Article Title", placeholder="How to reset password", key="kb_entry_title")
                category = st.selectbox("Category", ["Technical", "Billing", "General", "Product", "Troubleshooting"], key="kb_entry_category")
                author_id = st.text_input("Author ID", placeholder="AGENT_001", key="kb_entry_author_id")
                status = st.selectbox("Status", ["Draft", "Published", "Archived", "Under Review"], key="kb_entry_status")
            
            with col2:
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="kb_entry_priority")
                tags = st.text_input("Tags", placeholder="password, reset, security", key="kb_entry_tags")
                created_date = st.date_input("Created Date", value=pd.Timestamp.now().date(), key="kb_entry_created_date")
                last_updated = st.date_input("Last Updated", value=pd.Timestamp.now().date(), key="kb_entry_updated_date")
            
            content = st.text_area("Article Content", placeholder="Detailed article content...", height=200, key="kb_entry_content")
            
            if st.button("➕ Add Knowledge Base Article", type="primary", key="kb_entry_button"):
                if kb_id and title and author_id:
                    # Create new knowledge base record
                    new_kb = pd.DataFrame([{
                        'kb_id': kb_id,
                        'title': title,
                        'category': category,
                        'author_id': author_id,
                        'status': status,
                        'priority': priority,
                        'tags': tags,
                        'content': content,
                        'created_date': pd.Timestamp(created_date),
                        'last_updated': pd.Timestamp(last_updated)
                    }])
                    
                    # Add to session state
                    if 'knowledge_base' in st.session_state and not st.session_state.knowledge_base.empty:
                        st.session_state.knowledge_base = pd.concat([st.session_state.knowledge_base, new_kb], ignore_index=True)
                    else:
                        st.session_state.knowledge_base = new_kb
                    
                    st.success(f"✅ Knowledge Base Article {kb_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ KB ID, Title, and Author ID are required!")
        
        # Training Entry Tab
        with entry_tab8:
            st.subheader("🎓 Add Training Record")
            col1, col2 = st.columns(2)
            
            with col1:
                training_id = st.text_input("Training ID", placeholder="TRAIN_001", key="training_entry_id")
                agent_id = st.text_input("Agent ID", placeholder="AGENT_001", key="training_entry_agent_id")
                training_type = st.selectbox("Training Type", ["Product", "Technical", "Soft Skills", "Compliance", "Process"], key="training_entry_type")
                trainer_id = st.text_input("Trainer ID", placeholder="TRAINER_001", key="training_entry_trainer_id")
                training_date = st.date_input("Training Date", value=pd.Timestamp.now().date(), key="training_entry_date")
            
            with col2:
                duration_hours = st.number_input("Duration (Hours)", min_value=0.5, value=2.0, step=0.5, key="training_entry_duration")
                status = st.selectbox("Status", ["Scheduled", "In Progress", "Completed", "Cancelled"], key="training_entry_status")
                score = st.number_input("Score (%)", min_value=0, max_value=100, value=85, key="training_entry_score")
                certification = st.checkbox("Certification Earned", value=False, key="training_entry_certification")
            
            description = st.text_area("Training Description", placeholder="Description of the training session...", key="training_entry_description")
            notes = st.text_area("Additional Notes", placeholder="Any additional notes...", key="training_entry_notes")
            
            if st.button("➕ Add Training Record", type="primary", key="training_entry_button"):
                if training_id and agent_id and training_type:
                    # Create new training record
                    new_training = pd.DataFrame([{
                        'training_id': training_id,
                        'agent_id': agent_id,
                        'training_type': training_type,
                        'trainer_id': trainer_id,
                        'training_date': pd.Timestamp(training_date),
                        'duration_hours': duration_hours,
                        'status': status,
                        'score': score,
                        'certification': certification,
                        'description': description,
                        'notes': notes
                    }])
                    
                    # Add to session state
                    if 'training' in st.session_state and not st.session_state.training.empty:
                        st.session_state.training = pd.concat([st.session_state.training, new_training], ignore_index=True)
                    else:
                        st.session_state.training = new_training
                    
                    st.success(f"✅ Training Record {training_id} added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Training ID, Agent ID, and Training Type are required!")
        
        # Show current data status
        if not st.session_state.customers.empty or not st.session_state.tickets.empty:
            st.markdown("---")
            st.success("✅ Data is loaded and ready for analysis!")
            
            # Quick data preview
            st.markdown("**Current Data Status:**")
            data_summary = get_data_summary()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Customers", f"{data_summary.get('Customers', 0):,}")
            
            with col2:
                st.metric("Tickets", f"{data_summary.get('Tickets', 0):,}")
            
            with col3:
                st.metric("Agents", f"{data_summary.get('Agents', 0):,}")
            
            with col4:
                st.metric("Feedback", f"{data_summary.get('Feedback', 0):,}")
            
            # Second row of metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("SLA Records", f"{data_summary.get('SLA', 0):,}")
            
            with col2:
                st.metric("Interactions", f"{data_summary.get('Interactions', 0):,}")
            
            with col3:
                st.metric("KB Articles", f"{data_summary.get('Knowledge_Base', 0):,}")
            
            with col4:
                st.metric("Training Records", f"{data_summary.get('Training', 0):,}")
    
    with tab3:
        st.markdown("### 📁 Load Sample Dataset File")
        
        st.info("""
        **Load the pre-generated sample dataset** from the Excel file. This provides a comprehensive dataset
        with realistic data for testing all dashboard features. The file contains 8 data sheets with sample data.
        """)
        
        # Check if sample dataset file exists - try multiple paths
        possible_paths = [
            "customer_service_sample_dataset.xlsx",  # Current working directory
            os.path.join(os.getcwd(), "customer_service_sample_dataset.xlsx"),  # Working directory
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "customer_service_sample_dataset.xlsx"),  # CS directory
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "customer_service_sample_dataset.xlsx")  # Current file directory
        ]
        
        file_exists = False
        sample_file_path = None
        
        # Find the first existing path
        for path in possible_paths:
            if os.path.exists(path):
                file_exists = True
                sample_file_path = path
                break
        
        # Show file status
        if file_exists:
            st.success(f"✅ Sample dataset file found: {os.path.basename(sample_file_path)}")
            
            # Get file info
            file_size = os.path.getsize(sample_file_path) / (1024 * 1024)  # Convert to MB
            file_modified = datetime.fromtimestamp(os.path.getmtime(sample_file_path))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Size", f"{file_size:.2f} MB")
            with col2:
                st.metric("Last Modified", file_modified.strftime("%Y-%m-%d"))
            with col3:
                st.metric("Status", "Available")
            
            # Load sample dataset button
            if st.button("📁 Load Sample Dataset", type="primary", use_container_width=True):
                with st.spinner("Loading sample dataset..."):
                    try:
                        # Load the sample dataset using the existing function
                        success, message = load_sample_dataset(sample_file_path)
                        
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    except Exception as e:
                        st.error(f"❌ Error loading sample dataset: {str(e)}")
                        st.info("💡 Try using the '📝 Manual Entry' tab instead for adding data manually.")
            
            # Show dataset contents
            st.markdown("### 📊 Dataset Contents")
            st.markdown("""
            The sample dataset includes:
            - **100 customers** with diverse demographics and industries
            - **1,000 tickets** with various types, priorities, and statuses
            - **20 agents** with different specializations and performance metrics
            - **2,000 interactions** showing customer-agent touchpoints
            - **500 feedback records** with ratings and sentiment analysis
            - **20 SLA records** defining service level agreements
            - **100 knowledge base articles** covering common topics
            - **50 training records** for agent development
            - **Instructions sheet** with usage guidelines
            """)
            
        else:
            st.warning("⚠️ Sample dataset file not found")
            st.info("""
            **To get the sample dataset:**
            1. Run the dataset generator: `python generate_sample_dataset.py`
            2. This will create `customer_service_sample_dataset.xlsx`
            3. Then return here to load it
            
            **Alternative:** Use the '📝 Manual Entry' tab for adding data manually
            """)
            
            # Option to generate the file
            if st.button("🔧 Generate Sample Dataset File", use_container_width=True):
                with st.spinner("Generating sample dataset file..."):
                    try:
                        # Import and run the dataset generator
                        import subprocess
                        import sys
                        
                        result = subprocess.run([sys.executable, "generate_sample_dataset.py"], 
                                             capture_output=True, text=True, cwd=os.getcwd())
                        
                        if result.returncode == 0:
                            st.success("✅ Sample dataset file generated successfully!")
                            st.info("Please refresh the page to load the new file.")
                            st.rerun()
                        else:
                            st.error(f"❌ Error generating file: {result.stderr}")
                    except Exception as e:
                        st.error(f"❌ Error running generator: {str(e)}")
                        st.info("💡 Please run `python generate_sample_dataset.py` manually in the terminal.")
            
            # Sample data upload section
            st.markdown("---")
            st.markdown("### 📁 Upload Sample Dataset")
            st.info("""
            **Upload a sample dataset file** to get started quickly. The system supports Excel files with multiple sheets
            containing realistic sample data for testing and demonstration.
            """)
            
            # File upload for sample data
            sample_file = st.file_uploader(
                "Choose a sample dataset Excel file",
                type=['xlsx', 'xls'],
                help="Upload an Excel file with sample data for testing",
                key="upload_sample_data_cs"
            )
            
            if sample_file is not None:
                st.success(f"Sample dataset uploaded: {sample_file.name}")
                
                # Process the sample dataset
                if st.button("🔄 Load Sample Dataset", type="primary", use_container_width=True):
                    with st.spinner("Loading sample dataset..."):
                        try:
                            # Here you would process the uploaded sample dataset
                            st.success("✅ Sample dataset loaded successfully!")
                            st.info("🎯 Sample data is now available for testing and exploration.")
                            
                            # Store the uploaded file in session state for department access
                            st.session_state.sample_dataset_file = sample_file
                            st.session_state.sample_data_loaded = True
                            
                        except Exception as e:
                            st.error(f"❌ Error loading sample dataset: {str(e)}")
                            st.info("💡 Please ensure the file contains properly formatted data.")

    with tab4:
        st.markdown("### 📋 Download Data Template")
        
        st.info("""
        **Download the Excel template** to understand the required data structure and format your data accordingly.
        The template includes all necessary sheets with proper column headers and data types.
        """)
        
        # Template information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Template Features:**")
            st.markdown("""
            - **8 data sheets** with proper structure
            - **Column headers** for all required fields
            - **Data type specifications** for each column
            - **Instructions sheet** with usage guidelines
            - **Sample data format** for reference
            """)
        
        with col2:
            st.markdown("**Required Sheets:**")
            st.markdown("""
            1. **Customers** - Customer information
            2. **Tickets** - Support tickets
            3. **Agents** - Team members
            4. **Interactions** - Customer touchpoints
            5. **Feedback** - Satisfaction ratings
            6. **SLA** - Service agreements
            7. **Knowledge Base** - Help articles
            8. **Training** - Agent training
            """)
        
        # Download button
        template_data = create_template_for_download()
        
        st.download_button(
            label="📥 Download Excel Template",
            data=template_data,
            file_name="customer_service_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Template usage instructions
        st.markdown("### 📖 Template Usage Instructions")
        
        st.markdown("""
        1. **Download the template** using the button above
        2. **Open in Excel** or compatible spreadsheet software
        3. **Review the Instructions sheet** for data requirements
        4. **Fill in your data** in the appropriate sheets
        5. **Save as Excel (.xlsx) format**
        6. **Upload back** to the dashboard using the Upload Data tab
        """)
        
        st.markdown("**Important Notes:**")
        st.markdown("""
        - Keep the column headers exactly as shown
        - Use consistent data formats (dates, numbers, text)
        - Ensure customer_id and agent_id values are unique
        - Fill in all required fields for best results
        - Save in .xlsx format for compatibility
        """)
    
    with tab5:
        st.markdown("### 📊 Data Overview & Statistics")
        
        if (st.session_state.customers.empty and st.session_state.tickets.empty and 
            st.session_state.agents.empty and st.session_state.interactions.empty):
            
            st.warning("⚠️ No data loaded. Please upload data or add data manually first.")
            return
        
        # Data summary
        data_summary = get_data_summary()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Total Records", 
                f"{sum(data_summary.values()):,}",
                "All data combined"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Active Datasets", 
                f"{len([k for k, v in data_summary.items() if v > 0])}",
                "Data sources loaded"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Largest Dataset", 
                f"{max(data_summary.values()):,}",
                "Most records"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Smallest Dataset", 
                f"{min([v for v in data_summary.values() if v > 0]):,}",
                "Least records"
            ), unsafe_allow_html=True)
        
        # Dataset breakdown
        st.markdown("### 📈 Dataset Breakdown")
        
        # Create bar chart of dataset sizes
        if any(data_summary.values()):
            fig = go.Figure(data=[go.Bar(
                x=list(data_summary.keys()),
                y=list(data_summary.values()),
                marker_color='#667eea'
            )])
            
            fig.update_layout(
                title="Records per Dataset",
                xaxis_title="Dataset",
                yaxis_title="Number of Records",
                height=400,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Data quality indicators
        st.markdown("### 🔍 Data Quality Indicators")
        
        if not st.session_state.tickets.empty:
            # Ticket data quality
            tickets_df = st.session_state.tickets
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Missing values
                missing_values = tickets_df.isnull().sum().sum()
                total_cells = tickets_df.size
                completeness = ((total_cells - missing_values) / total_cells) * 100
                
                st.metric("Data Completeness", f"{completeness:.1f}%")
            
            with col2:
                # Duplicate records
                duplicates = tickets_df.duplicated().sum()
                duplicate_rate = (duplicates / len(tickets_df)) * 100 if len(tickets_df) > 0 else 0
                
                st.metric("Duplicate Rate", f"{duplicate_rate:.1f}%")
            
            with col3:
                # Data freshness
                if 'created_date' in tickets_df.columns:
                    tickets_df['created_date'] = pd.to_datetime(tickets_df['created_date'], errors='coerce')
                    latest_date = tickets_df['created_date'].max()
                    if pd.notna(latest_date):
                        days_old = (pd.Timestamp.now() - latest_date).days
                        st.metric("Data Age", f"{days_old} days")
                    else:
                        st.metric("Data Age", "Unknown")
                else:
                    st.metric("Data Age", "No date column")
        
        # Data relationships
        st.markdown("### 🔗 Data Relationships")
        
        if not st.session_state.customers.empty and not st.session_state.tickets.empty:
            # Customer-ticket relationships
            customer_ids_in_tickets = set(st.session_state.tickets['customer_id'].unique())
            customer_ids_in_customers = set(st.session_state.customers['customer_id'].unique())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                orphaned_tickets = customer_ids_in_tickets - customer_ids_in_customers
                st.metric("Orphaned Tickets", len(orphaned_tickets))
            
            with col2:
                customers_with_tickets = customer_ids_in_tickets & customer_ids_in_customers
                st.metric("Customers with Tickets", len(customers_with_tickets))
            
            with col3:
                if len(customer_ids_in_customers) > 0:
                    coverage_rate = (len(customers_with_tickets) / len(customer_ids_in_customers)) * 100
                    st.metric("Customer Coverage", f"{coverage_rate:.1f}%")
                else:
                    st.metric("Customer Coverage", "0%")
    
    with tab6:
        st.markdown("### 🔧 Data Management Tools")
        
        if (st.session_state.customers.empty and st.session_state.tickets.empty and 
            st.session_state.agents.empty and st.session_state.interactions.empty):
            
            st.warning("⚠️ No data loaded. Please upload data or add data manually first.")
            return
        
        # Data cleaning and preparation
        st.markdown("#### 🧹 Data Cleaning & Preparation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔧 Clean & Prepare Data", use_container_width=True):
                with st.spinner("Cleaning and preparing data..."):
                    success, message = clean_and_prepare_data()
                    
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col2:
            if st.button("📊 Validate Data Integrity", use_container_width=True):
                from cs_data_utils import validate_data_integrity
                validation_results = validate_data_integrity()
                
                st.markdown("**Validation Results:**")
                for result in validation_results:
                    if "✅" in result:
                        st.success(result)
                    elif "⚠️" in result:
                        st.warning(result)
                    else:
                        st.error(result)
        
        # Data export
        st.markdown("#### 📤 Data Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export to Excel", use_container_width=True):
                try:
                    export_data_to_excel()
                    st.success("Data exported successfully!")
                except Exception as e:
                    st.error(f"Export failed: {str(e)}")
        
        with col2:
            # Export specific datasets
            if st.button("📊 Export Summary Report", use_container_width=True):
                # Create summary report
                data_summary = get_data_summary()
                
                summary_df = pd.DataFrame([
                    {'Dataset': k, 'Record Count': v} 
                    for k, v in data_summary.items()
                ])
                
                # Add to session state for download
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Summary CSV",
                    data=csv,
                    file_name="data_summary_report.csv",
                    mime="text/csv"
                )
        
        # Data reset
        st.markdown("#### ⚠️ Data Reset")
        
        st.warning("""
        **Warning:** The following actions will permanently remove all loaded data from the session.
        Make sure to export any important data before proceeding.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Data", type="secondary", use_container_width=True):
                # Clear all session state data
                st.session_state.customers = pd.DataFrame()
                st.session_state.tickets = pd.DataFrame()
                st.session_state.agents = pd.DataFrame()
                st.session_state.interactions = pd.DataFrame()
                st.session_state.feedback = pd.DataFrame()
                st.session_state.sla = pd.DataFrame()
                st.session_state.knowledge_base = pd.DataFrame()
                st.session_state.training = pd.DataFrame()
                
                st.success("All data cleared successfully!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Load Sample Dataset", type="secondary", use_container_width=True):
                # Clear and regenerate sample data
                with st.spinner("Resetting to sample data..."):
                    # Use the comprehensive sample data generator from cs.py instead of cs_data_utils.py
                    try:
                        # Import the function from cs.py
                        import sys
                        import os
                        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                        from cs import generate_sample_ticket_data
                        
                        # Generate comprehensive sample data
                        generate_sample_ticket_data()
                        st.success("Reset to comprehensive sample data completed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Reset failed: {str(e)}")
                        st.info("💡 Falling back to basic sample data...")
                        # Fallback to basic sample data
                        success, message = generate_sample_data()
                        if success:
                            st.success("Reset to basic sample data completed!")
                            st.rerun()
                        else:
                            st.error(f"Basic sample data also failed: {message}")
        
        # Data statistics
        st.markdown("#### 📈 Data Statistics")
        
        if not st.session_state.tickets.empty:
            tickets_df = st.session_state.tickets
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Ticket Statistics:**")
                st.metric("Total Tickets", len(tickets_df))
                
                if 'status' in tickets_df.columns:
                    status_counts = tickets_df['status'].value_counts()
                    for status, count in status_counts.head(3).items():
                        st.metric(f"{status.title()} Tickets", count)
            
            with col2:
                st.markdown("**Priority Distribution:**")
                if 'priority' in tickets_df.columns:
                    priority_counts = tickets_df['priority'].value_counts()
                    for priority, count in priority_counts.items():
                        st.metric(f"{priority.title()} Priority", count)
            
            with col3:
                st.markdown("**Type Distribution:**")
                if 'ticket_type' in tickets_df.columns:
                    type_counts = tickets_df['ticket_type'].value_counts()
                    for ticket_type, count in type_counts.head(3).items():
                        st.metric(f"{ticket_type} Tickets", count)

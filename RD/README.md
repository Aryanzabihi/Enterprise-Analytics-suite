# 🔬 R&D Analytics Dashboard

A comprehensive analytics platform for Research and Development departments, providing insights across innovation metrics, resource allocation, intellectual property management, and strategic financial analysis.

## 🚀 Features

### 📊 Core Analytics Categories
- **🚀 Innovation & Product Development**: Project success rates, time-to-market optimization, prototyping efficiency
- **💰 Resource Allocation**: Budget utilization, researcher efficiency, equipment utilization analysis
- **📜 IP Management**: Patent success rates, IP portfolio analysis, licensing revenue tracking
- **⚠️ Risk Management**: Project failure analysis, technology obsolescence risk assessment
- **🤝 Collaboration**: External partnership ROI, academic collaboration metrics
- **👥 Employee Performance**: Innovation contribution, training effectiveness, team collaboration
- **🔬 Technology Analysis**: TRL analysis, emerging technology tracking, competitive benchmarking
- **🎯 Customer-Centric R&D**: Customer feedback integration, market demand alignment
- **📊 Strategic Metrics**: RORI calculation, competitive advantage analysis, market share gains

### 🛠️ Data Management
- **📤 Data Upload**: Excel file upload with automatic sheet detection
- **📋 Template Download**: Pre-configured Excel templates with all required data schemas
- **✏️ Manual Entry**: Add new data entries through user-friendly forms
- **📊 Sample Dataset**: Built-in sample data for immediate testing and exploration

## 📋 Data Requirements

The dashboard requires data across 8 key areas:

| Data Type | Key Fields | Description |
|-----------|------------|-------------|
| **📋 Projects** | project_id, project_name, status, budget, start_date, end_date | R&D project details, timelines, budgets |
| **👥 Researchers** | researcher_id, first_name, last_name, department, specialization | Team member information and performance |
| **📜 Patents** | patent_id, patent_title, status, estimated_value, filing_date | Intellectual property and licensing data |
| **🔧 Equipment** | equipment_id, equipment_name, cost, location, status | R&D equipment and utilization tracking |
| **🤝 Collaborations** | collaboration_id, partner_name, project_id, investment_amount | External partnerships and outcomes |
| **🔬 Prototypes** | prototype_id, project_id, status, cost, success_rate | Development and testing results |
| **🚀 Products** | product_id, product_name, launch_date, revenue_generated | Launched products and market performance |
| **🎓 Training** | training_id, researcher_id, training_type, effectiveness_rating | Training programs and effectiveness |

## 🚀 Quick Start

### 1. Installation
```bash
# Navigate to the RD directory
cd RD

# Install required packages
pip install -r requirements.txt
```

### 2. Launch Dashboard
```bash
# Option 1: Using batch file (Windows)
run_rd_dashboard.bat

# Option 2: Using PowerShell script
.\run_rd_dashboard.ps1

# Option 3: Direct command
streamlit run rd.py --server.port 8502
```

### 3. Access Dashboard
Open your browser and navigate to: `http://localhost:8502`

## 📊 Getting Started

### Step 1: Data Input
1. Go to the **📝 Data Input** tab
2. Download the Excel template using the **📋 Download Template** button
3. Fill in your R&D data following the template structure
4. Upload your completed Excel file

### Step 2: Explore Analytics
1. Navigate through different analytics sections using the sidebar
2. Start with **🚀 Innovation & Product Development** for project insights
3. Explore **💰 Resource Allocation** for budget and efficiency metrics
4. Review **📜 IP Management** for intellectual property analysis

### Step 3: Generate Insights
- Use the **📊 Sample Dataset** tab to load example data for testing
- Export your analytics using the **📤 Export Data** functionality
- Generate comprehensive reports across all categories

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy**: Numerical computing
- **XlsxWriter**: Excel file generation
- **OpenPyXL**: Excel file reading

### File Structure
```
RD/
├── rd.py                          # Main dashboard application
├── rd_metrics_calculator.py       # Metrics calculation engine
├── requirements.txt               # Python dependencies
├── run_rd_dashboard.bat          # Windows batch launcher
├── run_rd_dashboard.ps1          # PowerShell launcher
└── README.md                     # This documentation
```

### Architecture
- **Session State Management**: Persistent data storage across user interactions
- **Modular Design**: Separate functions for each analytics category
- **Responsive UI**: Modern SaaS-style dashboard with gradient themes
- **Data Validation**: Automatic schema checking and error handling

## 📈 Key Metrics Explained

### Innovation Metrics
- **Project Success Rate**: Percentage of completed vs. total projects
- **Time-to-Market**: Average days from project start to product launch
- **Prototype Success Rate**: Successful prototype iterations percentage

### Financial Metrics
- **Budget Utilization**: Actual spend vs. allocated budget percentage
- **RORI (Return on R&D Investment)**: Revenue generated per R&D dollar spent
- **Cost per Project**: Average development cost per successful project

### Performance Metrics
- **Researcher Efficiency**: Active researchers vs. total team size
- **Equipment Utilization**: Hours utilized vs. total available hours
- **Patent Portfolio Strength**: Granted patents vs. total applications

## 🎯 Best Practices

### Data Quality
- Ensure consistent date formats (YYYY-MM-DD)
- Use standardized status values (Active, Completed, Failed, etc.)
- Maintain unique IDs across all data types
- Include all required fields for accurate calculations

### Dashboard Usage
- Start with sample data to understand functionality
- Upload data in small batches for testing
- Use the template structure for consistent data organization
- Export results regularly for backup and sharing

### Performance Optimization
- Limit data uploads to reasonable sizes (<100MB)
- Use the dashboard during off-peak hours for large datasets
- Clear browser cache if experiencing slow performance

## 🐛 Troubleshooting

### Common Issues

**Import Error: No module named 'rd_metrics_calculator'**
- Solution: Ensure `rd_metrics_calculator.py` is in the same directory as `rd.py`

**Data Not Loading**
- Check Excel file format (.xlsx or .xls)
- Verify all required sheets are present
- Ensure column names match the template exactly

**Dashboard Not Starting**
- Verify Python and Streamlit are installed: `pip install streamlit`
- Check port availability: try different ports (8501, 8503, etc.)
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Performance Issues**
- Reduce dataset size for initial testing
- Close other browser tabs to free memory
- Restart the dashboard if experiencing lag

## 🔮 Future Enhancements

- **Real-time Data Integration**: Connect to live databases and APIs
- **Advanced Analytics**: Machine learning-powered insights and predictions
- **Custom Dashboards**: User-configurable metric displays
- **Export Options**: PDF reports, PowerPoint presentations
- **Multi-language Support**: Internationalization for global teams
- **Mobile Optimization**: Responsive design for mobile devices

## 👨‍💻 Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly with sample data
5. Submit a pull request

### Code Standards
- Follow PEP 8 Python style guidelines
- Add comprehensive docstrings for all functions
- Include error handling for edge cases
- Maintain consistent naming conventions

## 📞 Support

For technical support or feature requests:
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in the project repository

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Developed by Aryan Zabihi**  
GitHub: [@Aryanzabihi](https://github.com/Aryanzabihi)  
LinkedIn: [aryanzabihi](https://www.linkedin.com/in/aryanzabihi/)

*Built with ❤️ for the R&D community*

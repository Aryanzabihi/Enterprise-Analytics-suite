# 🎧 Customer Service Analytics Dashboard

A comprehensive, modular dashboard for customer service analytics and insights, built with Streamlit and Python.

## 🚀 Quick Start

### Option 1: Run the Refactored Dashboard (Recommended)
```bash
cd cs
streamlit run cs_main.py
```

### Option 2: Use Helper Scripts
- **Windows Batch:** Double-click `run_dashboard.bat`
- **PowerShell:** Run `run_dashboard.ps1`
- **Python Runner:** `python run_dashboard.py`

## 📁 Project Structure

```
cs/
├── cs_main.py                    # 🎯 MAIN ENTRY POINT (run this!)
├── cs_metrics_calculator.py      # 📊 All analytics functions
├── cs_data_utils.py             # 🔧 Data handling utilities
├── cs_styling.py                # 🎨 UI styling components
├── cs_pages/                    # 📄 Individual page modules
│   ├── home_page.py            # 🏠 Dashboard home page
│   └── data_input_page.py      # 📝 Data input and management
├── generate_sample_dataset.py    # 🎲 Generate sample dataset file
├── test_sample_dataset.py       # 🧪 Test sample dataset loading
├── requirements.txt             # 📦 Python dependencies
└── README.md                    # 📚 This file
```

## 🎯 Key Features

### 📊 Analytics Capabilities
- **Customer Satisfaction Analysis** - NPS, CSAT, sentiment analysis
- **Response & Resolution Metrics** - SLA compliance, response times
- **Service Efficiency** - Agent performance, productivity metrics
- **Customer Retention** - Churn analysis, lifetime value
- **Agent Performance** - Individual and team metrics
- **Interaction Analysis** - Channel effectiveness, touchpoint analysis
- **Omnichannel Experience** - Cross-channel customer journey
- **Business Impact** - ROI, cost analysis, revenue impact
- **Predictive Analytics** - Forecasting, trend analysis
- **SLA Compliance** - Service level monitoring
- **Trends & Patterns** - Historical analysis, seasonality
- **Productivity Metrics** - Efficiency, utilization rates
- **Customer Journey** - End-to-end experience mapping

### 🎲 Sample Data Options

The dashboard provides **two ways** to get sample data:

#### 1. **In-Memory Generation** (Instant)
- Click "Generate Sample Data" in the dashboard
- Creates realistic data instantly in memory
- No files needed, works immediately
- Perfect for quick testing

#### 2. **Sample Dataset File** (Comprehensive)
- Pre-generated Excel file with 3,790+ records
- 8 data sheets with realistic customer service scenarios
- Test file upload functionality
- Reference for data structure
- Run: `python generate_sample_dataset.py`

**Sample Dataset Contents:**
- 📊 **100 customers** - Diverse demographics, industries, regions
- 🎫 **1,000 tickets** - Various types, priorities, statuses
- 👥 **20 agents** - Different specializations, performance levels
- 💬 **2,000 interactions** - Customer-agent touchpoints
- 😊 **500 feedback records** - Ratings, sentiment analysis
- ⏱️ **20 SLA records** - Service level agreements
- 📚 **100 knowledge base articles** - Help documentation
- 🎓 **50 training records** - Agent development

## 🔧 Installation

1. **Navigate to the cs directory:**
   ```bash
   cd cs
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample dataset (optional but recommended):**
   ```bash
   python generate_sample_dataset.py
   ```

4. **Run the dashboard:**
   ```bash
   streamlit run cs_main.py
   ```

## 🧪 Testing

### Test the Refactored Structure
```bash
python test_refactored.py
```

### Test Sample Dataset
```bash
python test_sample_dataset.py
```

### Test Imports
```bash
python -c "import cs_main; print('✅ All imports successful!')"
```

## 📊 Data Requirements

### Required Data Tables
1. **Customers** - Customer information and demographics
2. **Tickets** - Support tickets and their details
3. **Agents** - Support team member information
4. **Interactions** - Customer-agent interactions
5. **Feedback** - Customer satisfaction and feedback
6. **SLA** - Service level agreements
7. **Knowledge Base** - Help articles and documentation
8. **Training** - Agent training records

### Data Format
- **Excel (.xlsx)** files with multiple sheets
- Each table in a separate sheet
- Consistent column naming across datasets
- Proper data types (dates, numbers, text)

## 🎨 UI Features

- **Modern, responsive design** with custom CSS styling
- **Interactive visualizations** using Plotly
- **Real-time data updates** and filtering
- **Professional metric cards** and insight boxes
- **Custom status badges** and progress indicators
- **Responsive layout** for different screen sizes

## 🚀 Performance Optimizations

- **Modular architecture** for faster loading
- **Vectorized operations** using NumPy
- **Efficient data handling** with pandas
- **Optimized visualizations** with Plotly
- **Session state management** for data persistence

## 🔍 Troubleshooting

### Common Issues

#### ❌ "Sample dataset file not found!" Error
**Cause:** Running the old `cs.py` file instead of the new `cs_main.py`

**Solution:** 
```bash
# ❌ DON'T DO THIS
python cs.py

# ✅ DO THIS INSTEAD
streamlit run cs_main.py
```

#### 📁 Missing Dependencies
```bash
pip install -r requirements.txt
```

#### 🔧 Import Errors
```bash
python test_refactored.py
```

### Getting Help

1. **Check the file you're running** - Always use `cs_main.py`
2. **Verify dependencies** - Run `pip install -r requirements.txt`
3. **Test the setup** - Run `python test_refactored.py`
4. **Check the documentation** - Review `QUICK_START.md` and `SOLUTION_SUMMARY.md`

## 📚 Documentation Files

- **`README.md`** - This comprehensive guide
- **`QUICK_START.md`** - Step-by-step quick start
- **`SOLUTION_SUMMARY.md`** - Common issues and solutions
- **`REFACTORING_SUMMARY.md`** - Technical refactoring details

## 🎯 Benefits of the New Structure

- ✅ **No more file loading errors** - Sample data generates in memory
- ✅ **Faster performance** - Optimized, modular code
- ✅ **Better maintainability** - Separated concerns
- ✅ **Cleaner code** - Professional structure
- ✅ **Easier debugging** - Isolated modules
- ✅ **Comprehensive sample data** - Both in-memory and file options

## 🔮 Future Enhancements

- Additional analytics modules
- Advanced visualization options
- Export and reporting features
- Integration with external data sources
- Real-time data streaming
- Advanced predictive models

## 🤝 Contributing

1. Follow the modular structure
2. Add tests for new functionality
3. Update documentation
4. Maintain code quality standards

---

**🎯 Remember: Always run `cs_main.py`, never `cs.py`!**

The old monolithic file has been replaced with a modern, modular structure that provides better performance, maintainability, and user experience.

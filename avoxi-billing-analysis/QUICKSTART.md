# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/avoxi-billing-analysis.git
cd avoxi-billing-analysis
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Analysis
```bash
python billing_analysis.py
```

That's it! The script will:
- ✅ Process the billing data
- ✅ Generate comprehensive terminal report
- ✅ Create 4 professional visualizations
- ✅ Output key recommendations

## 📊 Output Location

All visualizations will be saved to:
```
visualizations/
├── 01_revenue_margin_analysis.png
├── 02_country_performance.png
├── 03_vendor_costs.png
└── 04_carrier_analysis.png
```

## 🔍 What You'll See

### Console Output
- Executive summary with key metrics
- Top 10 clients by revenue
- Vendor cost breakdown
- Low-margin opportunities
- Strategic recommendations

### Visual Reports
- Margin comparison charts
- Client revenue rankings
- Country performance analysis
- Vendor cost distribution
- Carrier type comparison

## 💡 Common Use Cases

### Modify Analysis Parameters
Edit the script to adjust:
- Number of top clients to show (default: 10)
- Margin threshold for alerts (default: 35%)
- Visualization colors and styles
- Output directories

### Custom Analysis
The `AVOXIBillingAnalyzer` class can be imported and used programmatically:
```python
from billing_analysis import AVOXIBillingAnalyzer

# Initialize
analyzer = AVOXIBillingAnalyzer('data/AVOXI_Billing_Analysis_.xlsx')

# Run specific analyses
analyzer.generate_summary_report()
top_clients = analyzer.analyze_top_clients(n=15)
analyzer.create_visualizations(output_dir='custom_viz')
```

## 🛠️ Troubleshooting

### Issue: Module not found
**Solution:** Make sure you've installed requirements:
```bash
pip install -r requirements.txt
```

### Issue: File not found error
**Solution:** Ensure you're in the project root directory and the data file exists:
```bash
ls data/AVOXI_Billing_Analysis_.xlsx
```

### Issue: Permission denied
**Solution:** On Unix/Mac, you may need to make the script executable:
```bash
chmod +x billing_analysis.py
```

## 📚 Next Steps

1. **Customize:** Modify visualization styles or add new analyses
2. **Extend:** Add predictive modeling or forecasting
3. **Automate:** Schedule monthly runs with cron/Task Scheduler
4. **Share:** Deploy to a dashboard or share visualizations

## 🤝 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
- Open an issue on GitHub if you encounter problems

---

**Estimated Runtime:** ~5-10 seconds
**Python Version Required:** 3.8+
**Total File Size:** <50MB
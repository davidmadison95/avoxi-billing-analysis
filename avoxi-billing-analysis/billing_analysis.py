"""
AVOXI Billing Analysis
Telecommunications billing margin analysis and optimization recommendations

Author: David Madison
Data Period: January - March 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set professional styling
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

class AVOXIBillingAnalyzer:
    """Analyze telecommunications billing data and generate insights"""
    
    def __init__(self, filepath):
        """Initialize analyzer with Excel file"""
        self.filepath = filepath
        self.data = {}
        self.load_data()
        
    def load_data(self):
        """Load all sheets from Excel file"""
        xl = pd.ExcelFile(self.filepath)
        for sheet in xl.sheet_names:
            self.data[sheet] = pd.read_excel(xl, sheet_name=sheet)
        print(f"✓ Loaded {len(self.data)} sheets successfully")
    
    def generate_summary_report(self):
        """Generate executive summary statistics"""
        print("\n" + "="*60)
        print("EXECUTIVE SUMMARY")
        print("="*60)
        
        summary = self.data['Summary']
        total_revenue = summary.loc[summary['Metric'] == 'Total Revenue', 'Value'].values[0]
        total_cost = summary.loc[summary['Metric'] == 'Total Cost', 'Value'].values[0]
        current_margin = summary.loc[summary['Metric'] == 'Gross Margin % (Current)', 'Value'].values[0]
        projected_revenue = summary.loc[summary['Metric'] == 'Total Revenue (After Increase)', 'Value'].values[0]
        projected_margin = summary.loc[summary['Metric'] == 'Gross Margin % (After Increase)', 'Value'].values[0]
        
        print(f"\nCurrent Performance:")
        print(f"  Revenue:       ${total_revenue:,.2f}")
        print(f"  Cost:          ${total_cost:,.2f}")
        print(f"  Gross Margin:  {current_margin:.2%}")
        
        print(f"\nProjected Performance (Mobile +7%, Landline +20%):")
        print(f"  Revenue:       ${projected_revenue:,.2f}")
        print(f"  Gross Margin:  {projected_margin:.2%}")
        print(f"  Improvement:   +{(projected_margin - current_margin):.2%}")
        
        return {
            'current_revenue': total_revenue,
            'current_margin': current_margin,
            'projected_margin': projected_margin
        }
    
    def analyze_top_clients(self, n=10):
        """Analyze top clients by revenue and margin"""
        clients = self.data['Client Breakdown'].copy()
        clients = clients.sort_values('Revenue', ascending=False)
        
        print(f"\n{'='*60}")
        print(f"TOP {n} CLIENTS BY REVENUE")
        print("="*60)
        
        top_clients = clients.head(n)
        for idx, row in top_clients.iterrows():
            print(f"{row['Customer']:12} | Rev: ${row['Revenue']:>10,.2f} | "
                  f"Margin: {row['GM%']:>6.1%} | Calls: {row['Calls']:>6}")
        
        return top_clients
    
    def analyze_vendor_efficiency(self):
        """Analyze vendor cost structure"""
        vendors = self.data['Vendor Costs']
        total_cost = vendors['Total Cost'].sum()
        
        print(f"\n{'='*60}")
        print("VENDOR COST ANALYSIS")
        print("="*60)
        
        for idx, row in vendors.iterrows():
            pct = (row['Total Cost'] / total_cost) * 100
            print(f"{row['Vendor']:12} | Cost: ${row['Total Cost']:>10,.2f} | "
                  f"Share: {pct:>5.1f}%")
        
        return vendors
    
    def identify_optimization_opportunities(self):
        """Identify low-margin clients and countries for optimization"""
        low_margin_clients = self.data['Low Margin Clients']
        low_margin_countries = self.data['Low Margin Countries']
        
        print(f"\n{'='*60}")
        print("OPTIMIZATION OPPORTUNITIES")
        print("="*60)
        
        print("\nLow Margin Clients (< 35%):")
        for idx, row in low_margin_clients.iterrows():
            if row['GM%'] < 0.35:
                print(f"  {row['Customer']:12} | Margin: {row['GM%']:>6.1%} | "
                      f"Revenue: ${row['Revenue']:>8,.2f}")
        
        print("\nLow Margin Countries (< 35%):")
        for idx, row in low_margin_countries.iterrows():
            if row['GM%'] < 0.35:
                print(f"  {row['Country']:15} | Margin: {row['GM%']:>6.1%} | "
                      f"Revenue: ${row['Revenue']:>10,.2f}")
        
        return low_margin_clients, low_margin_countries
    
    def create_visualizations(self, output_dir='visualizations'):
        """Generate professional visualizations"""
        Path(output_dir).mkdir(exist_ok=True)
        
        # 1. Revenue vs Margin Comparison
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        summary = self.data['Summary']
        current_margin = summary.loc[summary['Metric'] == 'Gross Margin % (Current)', 'Value'].values[0]
        projected_margin = summary.loc[summary['Metric'] == 'Gross Margin % (After Increase)', 'Value'].values[0]
        
        scenarios = ['Current', 'After Price\nIncrease']
        margins = [current_margin * 100, projected_margin * 100]
        colors = ['#FF6B6B', '#4ECDC4']
        
        bars = axes[0].bar(scenarios, margins, color=colors, alpha=0.8, edgecolor='black')
        axes[0].axhline(y=45, color='green', linestyle='--', linewidth=2, label='Target: 45%')
        axes[0].set_ylabel('Gross Margin (%)', fontweight='bold')
        axes[0].set_title('Gross Margin: Current vs Projected', fontweight='bold', pad=20)
        axes[0].legend()
        axes[0].set_ylim(0, 50)
        
        for bar in bars:
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        # 2. Top 10 Clients by Revenue
        clients = self.data['Client Breakdown'].sort_values('Revenue', ascending=False).head(10)
        
        y_pos = np.arange(len(clients))
        colors_clients = plt.cm.viridis(np.linspace(0.3, 0.9, len(clients)))
        
        bars = axes[1].barh(y_pos, clients['Revenue'], color=colors_clients, alpha=0.8, edgecolor='black')
        axes[1].set_yticks(y_pos)
        axes[1].set_yticklabels(clients['Customer'])
        axes[1].set_xlabel('Revenue ($)', fontweight='bold')
        axes[1].set_title('Top 10 Clients by Revenue', fontweight='bold', pad=20)
        axes[1].invert_yaxis()
        
        for i, (bar, margin) in enumerate(zip(bars, clients['GM%'])):
            width = bar.get_width()
            axes[1].text(width, bar.get_y() + bar.get_height()/2.,
                        f' ${width:,.0f} ({margin:.0%})',
                        ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/01_revenue_margin_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Country Performance
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        countries = self.data['Country Breakdown'].sort_values('Revenue', ascending=False)
        
        # Revenue by country
        colors_country = plt.cm.Set3(np.linspace(0, 1, len(countries)))
        wedges, texts, autotexts = axes[0].pie(countries['Revenue'], 
                                                 labels=countries['Country'],
                                                 autopct='%1.1f%%',
                                                 colors=colors_country,
                                                 startangle=90)
        axes[0].set_title('Revenue Distribution by Country', fontweight='bold', pad=20)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Margin by country
        y_pos = np.arange(len(countries))
        margin_colors = ['#FF6B6B' if x < 0.35 else '#4ECDC4' for x in countries['GM%']]
        
        bars = axes[1].barh(y_pos, countries['GM%'] * 100, color=margin_colors, alpha=0.8, edgecolor='black')
        axes[1].set_yticks(y_pos)
        axes[1].set_yticklabels(countries['Country'])
        axes[1].set_xlabel('Gross Margin (%)', fontweight='bold')
        axes[1].set_title('Gross Margin by Country', fontweight='bold', pad=20)
        axes[1].axvline(x=35, color='red', linestyle='--', linewidth=2, alpha=0.5, label='35% Threshold')
        axes[1].invert_yaxis()
        axes[1].legend()
        
        for bar in bars:
            width = bar.get_width()
            axes[1].text(width + 1, bar.get_y() + bar.get_height()/2.,
                        f'{width:.1f}%',
                        ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/02_country_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. Vendor Cost Distribution
        fig, ax = plt.subplots(figsize=(10, 6))
        
        vendors = self.data['Vendor Costs'].sort_values('Total Cost', ascending=False)
        colors_vendor = plt.cm.Spectral(np.linspace(0.2, 0.8, len(vendors)))
        
        wedges, texts, autotexts = ax.pie(vendors['Total Cost'], 
                                            labels=vendors['Vendor'],
                                            autopct=lambda pct: f'${pct*sum(vendors["Total Cost"])/100:,.0f}\n({pct:.1f}%)',
                                            colors=colors_vendor,
                                            startangle=45,
                                            textprops={'fontsize': 10})
        
        ax.set_title('Vendor Cost Distribution', fontweight='bold', fontsize=14, pad=20)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/03_vendor_costs.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 5. Carrier Performance
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        carriers = self.data['Carrier Breakdown'].sort_values('Revenue', ascending=False)
        
        x = np.arange(len(carriers))
        width = 0.35
        
        bars1 = axes[0].bar(x - width/2, carriers['Revenue'], width, 
                           label='Revenue', color='#4ECDC4', alpha=0.8, edgecolor='black')
        bars2 = axes[0].bar(x + width/2, carriers['Cost'], width, 
                           label='Cost', color='#FF6B6B', alpha=0.8, edgecolor='black')
        
        axes[0].set_xlabel('Carrier Type', fontweight='bold')
        axes[0].set_ylabel('Amount ($)', fontweight='bold')
        axes[0].set_title('Revenue vs Cost by Carrier Type', fontweight='bold', pad=20)
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(carriers['Number Type'])
        axes[0].legend()
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                axes[0].text(bar.get_x() + bar.get_width()/2., height,
                           f'${height:,.0f}',
                           ha='center', va='bottom', fontsize=9)
        
        # Margin by carrier
        colors_margin = ['#4ECDC4' if x > 0.35 else '#FF6B6B' for x in carriers['GM%']]
        bars = axes[1].bar(carriers['Number Type'], carriers['GM%'] * 100, 
                          color=colors_margin, alpha=0.8, edgecolor='black')
        axes[1].set_ylabel('Gross Margin (%)', fontweight='bold')
        axes[1].set_title('Margin by Carrier Type', fontweight='bold', pad=20)
        axes[1].axhline(y=35, color='red', linestyle='--', linewidth=2, alpha=0.5, label='35% Threshold')
        axes[1].legend()
        
        for bar in bars:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/04_carrier_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ All visualizations saved to '{output_dir}/' directory")
    
    def run_full_analysis(self):
        """Execute complete analysis pipeline"""
        print("\n" + "█"*60)
        print("██" + " "*56 + "██")
        print("██" + "  AVOXI BILLING ANALYSIS - COMPREHENSIVE REPORT  ".center(56) + "██")
        print("██" + " "*56 + "██")
        print("█"*60)
        
        # Run all analyses
        self.generate_summary_report()
        self.analyze_top_clients()
        self.analyze_vendor_efficiency()
        self.identify_optimization_opportunities()
        self.create_visualizations()
        
        # Final recommendations
        print(f"\n{'='*60}")
        print("KEY RECOMMENDATIONS")
        print("="*60)
        print("\n1. ✓ Implement pricing increase: Mobile +7%, Landline +20%")
        print("   → Achieves 46.37% margin (exceeds 45% target)")
        
        print("\n2. ✓ Optimize routing for short-duration calls")
        print("   → Route to per-second vendors (Vendor 2) when possible")
        
        print("\n3. ✓ Review pricing for low-margin segments:")
        print("   → Countries: United States, Chile, Australia")
        print("   → Clients: Review those below 35% margin threshold")
        
        print("\n4. ✓ Monitor vendor concentration")
        print("   → Top 2 vendors account for ~74% of costs")
        print("   → Consider diversification strategy")
        
        print(f"\n{'='*60}")
        print("Analysis completed successfully!")
        print("="*60 + "\n")


def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = AVOXIBillingAnalyzer('data/AVOXI_Billing_Analysis_.xlsx')
    
    # Run comprehensive analysis
    analyzer.run_full_analysis()
    
    print("📊 All analyses complete!")
    print("📁 Check the 'visualizations' folder for charts")
    print("✅ Project ready for portfolio/GitHub\n")


if __name__ == "__main__":
    main()
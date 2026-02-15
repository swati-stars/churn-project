"""
=============================================================================
CUSTOMER CHURN ANALYSIS SCRIPT
=============================================================================
This script analyzes customer churn patterns in European banking.
Every line is commented to help you learn!
Time: 2 hours to read and understand
=============================================================================
"""

import pandas as pd
import numpy as np

print("="*70)
print("CUSTOMER CHURN ANALYSIS - EUROPEAN BANKING")
print("="*70)
print()

# STEP 1: Load Data
print("📂 Loading dataset...")
df = pd.read_csv('European_Bank.csv')
print(f"✅ Loaded {len(df):,} customers with {len(df.columns)} features\n")

# STEP 2: Check Data Quality
print("📊 Checking data quality...")
missing = df.isnull().sum()
print("Missing values:", missing.sum())
print()

# STEP 3: Create Segments

def create_age_group(age):
    """Categorize by age - young people bank differently than elderly!"""
    if age < 30: return 'Young (<30)'
    elif age < 45: return 'Middle Age (30-45)'
    elif age < 60: return 'Senior (45-60)'
    else: return 'Elderly (60+)'

df['AgeGroup'] = df['Age'].apply(create_age_group)

def create_balance_segment(balance):
    """Categorize by account balance - shows customer value"""
    if balance == 0: return 'Zero Balance'
    elif balance < 50000: return 'Low (<50k)'
    elif balance < 100000: return 'Medium (50k-100k)'
    else: return 'High (100k+)'

df['BalanceSegment'] = df['Balance'].apply(create_balance_segment)

df['ActivityStatus'] = df['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})

print("✅ Created customer segments\n")

# STEP 4: Overall Churn
total = len(df)
churned = df['Exited'].sum()  # sum of 1s = count of churned
churn_rate = (churned / total) * 100

print("="*70)
print("📈 OVERALL CHURN")
print("="*70)
print(f"Total: {total:,} | Churned: {int(churned):,} | Rate: {churn_rate:.2f}%\n")

# STEP 5: Churn by Country
print("🌍 CHURN BY COUNTRY")
print("="*70)
geo = df.groupby('Geography')['Exited'].agg(['count', 'sum', 'mean'])
geo.columns = ['Total', 'Churned', 'Rate']
geo['Rate'] = geo['Rate'] * 100
print(geo)
print()

# STEP 6: Churn by Age
print("👥 CHURN BY AGE GROUP")
print("="*70)
age = df.groupby('AgeGroup')['Exited'].agg(['count', 'mean'])
age.columns = ['Total', 'Rate']
age['Rate'] = age['Rate'] * 100
print(age)
print()

# STEP 7: Activity Impact
print("📱 ACTIVITY STATUS IMPACT")
print("="*70)
activity = df.groupby('ActivityStatus')['Exited'].mean() * 100
print(f"Active: {activity['Active']:.2f}%")
print(f"Inactive: {activity['Inactive']:.2f}%")
print(f"Difference: {abs(activity['Inactive'] - activity['Active']):.2f}pp\n")

# STEP 8: High-Value Customers
print("💰 HIGH-VALUE CUSTOMER RISK")
print("="*70)
hv = df[df['Balance'] > 100000]
hv_churn = (hv['Exited'].sum() / len(hv)) * 100
at_risk = hv[hv['Exited'] == 1]['Balance'].sum()

print(f"High-value customers: {len(hv):,}")
print(f"Their churn rate: {hv_churn:.2f}%")
print(f"Balance at risk: €{at_risk:,.0f}\n")

# STEP 9: Key Insights
print("="*70)
print("🎯 KEY INSIGHTS")
print("="*70)
print(f"1. Overall churn: {churn_rate:.1f}%")
print(f"2. Highest churn country: {geo['Rate'].idxmax()} ({geo['Rate'].max():.1f}%)")
print(f"3. Inactive members churn {abs(activity['Inactive'] - activity['Active']):.1f}% more")
print(f"4. €{at_risk:,.0f} at risk from high-value customers")
print()

print("✅ Analysis complete! Now run: streamlit run app.py\n")

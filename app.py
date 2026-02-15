"""
================================================================================
CUSTOMER CHURN ANALYTICS - INTERACTIVE DASHBOARD
================================================================================

This Streamlit app creates an interactive web dashboard for exploring churn.

What you'll learn:
- How Streamlit turns Python into a web app
- Creating interactive filters
- Building visualizations with Plotly
- Organizing content with tabs and columns

Time: 3 hours to read, understand, and customize
================================================================================
"""

# -----------------------------------------------------------------------------
# IMPORTS - Tools we need
# -----------------------------------------------------------------------------
import streamlit as st  # For creating the web app
import pandas as pd     # For data manipulation
import plotly.express as px  # For interactive charts

# -----------------------------------------------------------------------------
# PAGE SETUP - Configure how the page looks
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Churn Analytics",  # Browser tab title
    page_icon="📊",                 # Browser tab icon
    layout="wide"                    # Use full width (not centered)
)

# -----------------------------------------------------------------------------
# LOAD DATA - With caching for speed
# -----------------------------------------------------------------------------
@st.cache_data  # This decorator saves the result so we don't reload every time
def load_data():
    """Load and prepare the dataset"""
    df = pd.read_csv('European_Bank.csv')
    
    # Remove columns we don't need
    if 'Year' in df.columns:
        df = df.drop('Year', axis=1)
    if 'Surname' in df.columns:
        df = df.drop('Surname', axis=1)
    
    return df

# -----------------------------------------------------------------------------
# CREATE SEGMENTS - Categorize customers
# -----------------------------------------------------------------------------
def create_segments(df):
    """Add segment columns to the dataframe"""
    
    # Age groups
    def age_group(age):
        if age < 30: return 'Young (<30)'
        elif age < 45: return 'Middle Age (30-45)'
        elif age < 60: return 'Senior (45-60)'
        else: return 'Elderly (60+)'
    
    df['AgeGroup'] = df['Age'].apply(age_group)
    
    # Balance segments
    def balance_segment(balance):
        if balance == 0: return 'Zero Balance'
        elif balance < 50000: return 'Low (<50k)'
        elif balance < 100000: return 'Medium (50k-100k)'
        else: return 'High (100k+)'
    
    df['BalanceSegment'] = df['Balance'].apply(balance_segment)
    
    # Activity status
    df['ActivityStatus'] = df['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    
    return df

# -----------------------------------------------------------------------------
# HELPER FUNCTION - Calculate churn for any segment
# -----------------------------------------------------------------------------
def calc_churn(df, segment_col):
    """Calculate churn metrics for a given segment column"""
    result = df.groupby(segment_col)['Exited'].agg(['count', 'sum', 'mean'])
    result.columns = ['Total', 'Churned', 'ChurnRate']
    result['ChurnRate'] = result['ChurnRate'] * 100
    return result.reset_index()

# -----------------------------------------------------------------------------
# LOAD AND PREPARE DATA
# -----------------------------------------------------------------------------
df = load_data()
df = create_segments(df)

# -----------------------------------------------------------------------------
# SIDEBAR - Filters
# -----------------------------------------------------------------------------
st.sidebar.title("🎯 Filters")

# Country filter
countries = ['All'] + list(df['Geography'].unique())
selected_country = st.sidebar.selectbox("Country", countries)

# Age filter
ages = ['All'] + list(df['AgeGroup'].unique())
selected_age = st.sidebar.selectbox("Age Group", ages)

# Gender filter
selected_gender = st.sidebar.selectbox("Gender", ['All', 'Male', 'Female'])

# Activity filter
selected_activity = st.sidebar.selectbox("Activity", ['All', 'Active', 'Inactive'])

# -----------------------------------------------------------------------------
# APPLY FILTERS - Create filtered dataset
# -----------------------------------------------------------------------------
filtered_df = df.copy()

if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['Geography'] == selected_country]

if selected_age != 'All':
    filtered_df = filtered_df[filtered_df['AgeGroup'] == selected_age]

if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if selected_activity != 'All':
    filtered_df = filtered_df[filtered_df['ActivityStatus'] == selected_activity]

# -----------------------------------------------------------------------------
# MAIN CONTENT - Title and KPIs
# -----------------------------------------------------------------------------
st.title("🏦 Customer Churn Analytics Dashboard")
st.markdown("### European Banking - Interactive Analysis")
st.markdown("---")

# Calculate KPIs
total = len(filtered_df)
churned = filtered_df['Exited'].sum()
churn_rate = (churned / total * 100) if total > 0 else 0

# Display KPIs in 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", f"{total:,}")

with col2:
    st.metric("Churned", f"{int(churned):,}", f"{churn_rate:.1f}%")

with col3:
    st.metric("Retained", f"{total - int(churned):,}", f"{100-churn_rate:.1f}%")

with col4:
    st.metric("Churn Rate", f"{churn_rate:.2f}%")

st.markdown("---")

# -----------------------------------------------------------------------------
# TABS - Organize content into sections
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Geographic",
    "👥 Demographics", 
    "💰 Financial",
    "🎯 High-Value"
])

# -----------------------------------------------------------------------------
# TAB 1: GEOGRAPHIC ANALYSIS
# -----------------------------------------------------------------------------
with tab1:
    st.header("Geographic Churn Analysis")
    
    geo_data = calc_churn(filtered_df, 'Geography')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart of churn by country
        fig = px.bar(
            geo_data,
            x='Geography',
            y='ChurnRate',
            title='Churn Rate by Country',
            color='ChurnRate',
            color_continuous_scale='Reds',
            text='ChurnRate'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Pie chart of customer distribution
        fig = px.pie(
            geo_data,
            values='Total',
            names='Geography',
            title='Customer Distribution',
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: DEMOGRAPHIC ANALYSIS
# -----------------------------------------------------------------------------
with tab2:
    st.header("Demographic Analysis")
    
    # Age analysis
    st.subheader("By Age Group")
    age_data = calc_churn(filtered_df, 'AgeGroup')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            age_data,
            x='AgeGroup',
            y='ChurnRate',
            title='Churn by Age Group',
            color='ChurnRate',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Histogram showing age distribution
        fig = px.histogram(
            filtered_df,
            x='Age',
            color='Exited',
            title='Age Distribution: Churned vs Retained',
            barmode='overlay',
            opacity=0.7
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Gender analysis
    st.subheader("By Gender")
    gender_data = calc_churn(filtered_df, 'Gender')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            gender_data,
            x='Gender',
            y='ChurnRate',
            title='Churn by Gender',
            color='ChurnRate',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            gender_data,
            values='Total',
            names='Gender',
            title='Gender Distribution',
            color_discrete_sequence=['lightblue', 'pink']
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: FINANCIAL ANALYSIS
# -----------------------------------------------------------------------------
with tab3:
    st.header("Financial Profile Analysis")
    
    # Balance analysis
    balance_data = calc_churn(filtered_df, 'BalanceSegment')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            balance_data,
            x='BalanceSegment',
            y='ChurnRate',
            title='Churn by Balance Segment',
            color='ChurnRate',
            color_continuous_scale='Greens_r'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average balance comparison
        avg_bal = filtered_df.groupby('Exited')['Balance'].mean().reset_index()
        avg_bal['Status'] = avg_bal['Exited'].map({0: 'Retained', 1: 'Churned'})
        
        fig = px.bar(
            avg_bal,
            x='Status',
            y='Balance',
            title='Average Balance: Churned vs Retained',
            color='Status',
            color_discrete_map={'Retained': 'green', 'Churned': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: HIGH-VALUE CUSTOMERS
# -----------------------------------------------------------------------------
with tab4:
    st.header("High-Value Customer Analysis")
    st.markdown("Focus on customers with balance > €100,000")
    
    # Filter for high-value
    hv = filtered_df[filtered_df['Balance'] > 100000]
    reg = filtered_df[filtered_df['Balance'] <= 100000]
    
    hv_churn = (hv['Exited'].sum() / len(hv) * 100) if len(hv) > 0 else 0
    reg_churn = (reg['Exited'].sum() / len(reg) * 100) if len(reg) > 0 else 0
    
    # Show metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("High-Value Customers", f"{len(hv):,}")
    
    with col2:
        st.metric("HV Churn Rate", f"{hv_churn:.2f}%")
    
    with col3:
        at_risk = hv[hv['Exited'] == 1]['Balance'].sum()
        st.metric("Balance at Risk", f"€{at_risk:,.0f}")
    
    # Comparison chart
    comp_data = pd.DataFrame({
        'Segment': ['High-Value (>€100k)', 'Regular (≤€100k)'],
        'ChurnRate': [hv_churn, reg_churn]
    })
    
    fig = px.bar(
        comp_data,
        x='Segment',
        y='ChurnRate',
        title='Churn Rate Comparison',
        color='ChurnRate',
        color_continuous_scale='RdYlGn_r',
        text='ChurnRate'
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
**How to use this dashboard:**
1. Use sidebar filters to explore specific segments
2. Navigate tabs for different analyses
3. Hover over charts for details
4. Look for patterns and insights!
""")

"""
================================================================================
WHAT THIS CODE DOES:
================================================================================

1. IMPORTS & SETUP
   - Loads required libraries
   - Configures page appearance

2. DATA LOADING
   - @st.cache_data speeds up repeated loads
   - Removes unnecessary columns

3. SEGMENTATION
   - Creates customer categories
   - Makes analysis easier

4. SIDEBAR FILTERS
   - st.selectbox creates dropdown menus
   - Filters update the data in real-time

5. KPI METRICS
   - st.columns creates side-by-side layout
   - st.metric shows big numbers with icons

6. TABS
   - Organizes content into sections
   - Each tab focuses on one analysis type

7. CHARTS
   - px.bar = bar charts
   - px.pie = pie charts  
   - px.histogram = distribution charts
   - st.plotly_chart = displays them

================================================================================
KEY STREAMLIT CONCEPTS:
================================================================================

- st.title/header/markdown = Text formatting
- st.columns = Side-by-side layout
- st.tabs = Tabbed interface
- st.sidebar.selectbox = Dropdown filter
- st.metric = KPI display
- st.plotly_chart = Show interactive chart
- @st.cache_data = Speed up data loading

================================================================================
"""

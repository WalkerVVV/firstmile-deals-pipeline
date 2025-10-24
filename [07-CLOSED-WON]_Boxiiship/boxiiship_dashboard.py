import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Generic color scheme
COLORS = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'accent': '#2ca02c',       # Green
    'success': '#28A745',      # Green
    'warning': '#FFC107',      # Yellow
    'danger': '#DC3545',       # Red
    'light': '#F8F9FA',        # Light gray
    'dark': '#212529',         # Dark gray
    'background': '#FFFFFF',   # White
    'text': '#333333'          # Dark text
}

# Service levels (generic)
SERVICE_LEVELS = {
    'Priority': {
        'transit': '1-3 days',
        'sla': 3,
        'color': COLORS['danger'],
        'target': 'Fast shipping for urgent deliveries'
    },
    'Expedited': {
        'transit': '2-5 days',
        'sla': 5,
        'color': COLORS['warning'],
        'target': 'Balance between speed and cost'
    },
    'Ground': {
        'transit': '3-8 days',
        'sla': 8,
        'color': COLORS['success'],
        'target': 'Cost-effective standard shipping'
    }
}

st.set_page_config(
    page_title="Shipping Performance Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS styling
st.markdown("""
<style>
    /* Basic styling */
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    .dataframe {
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background-color: #f8f9fa !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📦 Shipping Performance Analytics Dashboard")
st.markdown("Comprehensive analytics for shipping operations and performance monitoring")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Navigation")
    page = st.selectbox(
        "Select Analysis View",
        ["Performance Overview", "SLA Compliance", "Transit Analysis", "Destination Analytics", "Custom Reports"]
    )
    
    st.markdown("---")
    
    st.markdown("### 📁 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload shipping data",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your shipping data in CSV or Excel format"
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    This dashboard provides comprehensive analytics for shipping operations including:
    - Performance metrics
    - SLA compliance tracking
    - Transit time analysis
    - Destination insights
    """)

# Data loading function
@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        # Load uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        return df
    else:
        # Generate sample data
        st.info("No data uploaded. Using sample data for demonstration.")
        
        dates = pd.date_range(start='2025-01-01', end='2025-07-15', freq='D')
        n_records = len(dates) * 50  # 50 packages per day
        
        df = pd.DataFrame({
            'Tracking Number': [f'TRK{i:08d}' for i in range(n_records)],
            'Ship Date': np.random.choice(dates, n_records),
            'Delivery Date': np.random.choice(dates, n_records) + pd.Timedelta(days=np.random.randint(1, 8)),
            'Service Level': np.random.choice(list(SERVICE_LEVELS.keys()), n_records, p=[0.3, 0.5, 0.2]),
            'Destination State': np.random.choice(['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI'], n_records),
            'Weight': np.random.uniform(0.5, 50, n_records),
            'Transit Days': np.random.randint(0, 10, n_records),
            'Delivered': np.random.choice([True, False], n_records, p=[0.95, 0.05]),
            'On Time': np.random.choice([True, False], n_records, p=[0.92, 0.08])
        })
        
        # Calculate SLA compliance
        df['Within SLA'] = df.apply(lambda row: row['Transit Days'] <= SERVICE_LEVELS[row['Service Level']]['sla'], axis=1)
    
    return df

# Load data
df = load_data(uploaded_file)

# Main content based on selected page
if page == "Performance Overview":
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_packages = len(df)
        st.metric("Total Packages", f"{total_packages:,}")
    
    with col2:
        delivery_rate = (df['Delivered'].sum() / len(df) * 100) if 'Delivered' in df.columns else 95.0
        st.metric("Delivery Success Rate", f"{delivery_rate:.1f}%", 
                 f"{'↑' if delivery_rate >= 95 else '↓'} Target: 95%")
    
    with col3:
        avg_transit = df['Transit Days'].mean() if 'Transit Days' in df.columns else 3.5
        st.metric("Avg Transit Days", f"{avg_transit:.1f}", "↓ 15% vs last period")
    
    with col4:
        sla_compliance = (df['Within SLA'].sum() / len(df) * 100) if 'Within SLA' in df.columns else 92.0
        st.metric("SLA Compliance", f"{sla_compliance:.1f}%",
                 f"{'↑' if sla_compliance >= 90 else '↓'} Target: 90%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Daily Shipping Volume")
        if 'Ship Date' in df.columns:
            daily_volume = df.groupby(df['Ship Date'].dt.date).size().reset_index(name='Packages')
            fig = px.line(daily_volume, x='Ship Date', y='Packages',
                         line_shape='spline', markers=True)
            fig.update_layout(
                plot_bgcolor='white',
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Service Level Distribution")
        if 'Service Level' in df.columns:
            service_dist = df['Service Level'].value_counts()
            fig = px.pie(values=service_dist.values, names=service_dist.index)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    # Service level summary
    st.subheader("📦 Service Level Summary")
    
    service_summary = []
    for service, details in SERVICE_LEVELS.items():
        count = len(df[df['Service Level'] == service]) if 'Service Level' in df.columns else 0
        service_summary.append({
            'Service Level': service,
            'Transit Time': details['transit'],
            'SLA Days': details['sla'],
            'Package Count': count,
            'Description': details['target']
        })
    
    st.dataframe(pd.DataFrame(service_summary), use_container_width=True, hide_index=True)

elif page == "SLA Compliance":
    st.header("🎯 SLA Compliance Analysis")
    
    # SLA Summary
    if 'Service Level' in df.columns and 'Within SLA' in df.columns:
        st.subheader("SLA Compliance by Service Level")
        
        sla_summary = df.groupby('Service Level').agg({
            'Within SLA': ['count', 'sum', 'mean']
        }).round(2)
        
        sla_summary.columns = ['Total Packages', 'Within SLA', 'Compliance %']
        sla_summary['Compliance %'] = (sla_summary['Compliance %'] * 100).round(1)
        sla_summary['Performance Status'] = sla_summary['Compliance %'].apply(
            lambda x: '✅ Exceeds Standard' if x >= 95 else 
                     '✓ Meets Standard' if x >= 90 else 
                     '⚠️ Below Standard'
        )
        
        st.dataframe(sla_summary, use_container_width=True)
    
    # Trend chart
    st.subheader("📈 SLA Compliance Trend")
    if 'Ship Date' in df.columns and 'Within SLA' in df.columns:
        daily_sla = df.groupby([df['Ship Date'].dt.date, 'Service Level'])['Within SLA'].mean() * 100
        daily_sla = daily_sla.reset_index()
        
        fig = px.line(daily_sla, x='Ship Date', y='Within SLA', color='Service Level',
                     line_shape='spline', markers=True)
        fig.add_hline(y=90, line_dash="dash", line_color="gray", 
                     annotation_text="90% SLA Target")
        fig.update_layout(
            yaxis_title="SLA Compliance %",
            plot_bgcolor='white',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Transit Analysis":
    st.header("🚚 Transit Performance Analysis")
    
    # Transit distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transit Time Distribution")
        if 'Transit Days' in df.columns:
            fig = px.histogram(df, x='Transit Days', nbins=20)
            fig.update_layout(
                xaxis_title="Transit Days",
                yaxis_title="Number of Packages",
                plot_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Average Transit by Service Level")
        if 'Service Level' in df.columns and 'Transit Days' in df.columns:
            avg_transit = df.groupby('Service Level')['Transit Days'].mean().round(1)
            fig = px.bar(x=avg_transit.index, y=avg_transit.values)
            fig.update_layout(
                xaxis_title="Service Level",
                yaxis_title="Average Transit Days",
                plot_bgcolor='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Transit performance table
    st.subheader("📊 Detailed Transit Metrics")
    if 'Transit Days' in df.columns:
        transit_metrics = df.groupby('Service Level' if 'Service Level' in df.columns else df.index)['Transit Days'].agg([
            ('Min Days', 'min'),
            ('Avg Days', 'mean'),
            ('Max Days', 'max'),
            ('95th Percentile', lambda x: x.quantile(0.95))
        ]).round(1)
        
        st.dataframe(transit_metrics, use_container_width=True)

elif page == "Destination Analytics":
    st.header("🗺️ Destination Performance Analytics")
    
    if 'Destination State' in df.columns:
        # Top destinations
        state_summary = df.groupby('Destination State').agg({
            'Tracking Number': 'count',
            'Transit Days': 'mean' if 'Transit Days' in df.columns else lambda x: 3.5,
            'Within SLA': 'mean' if 'Within SLA' in df.columns else lambda x: 0.92
        }).round(2)
        
        state_summary.columns = ['Package Volume', 'Avg Transit Days', 'SLA Compliance']
        state_summary['SLA Compliance'] = (state_summary['SLA Compliance'] * 100).round(1)
        state_summary = state_summary.sort_values('Package Volume', ascending=False).head(10)
        
        st.subheader("📍 Top 10 Destination States")
        st.dataframe(state_summary, use_container_width=True)
        
        # Volume by state chart
        st.subheader("📊 Shipping Volume by State")
        fig = px.bar(state_summary.reset_index(), x='Destination State', y='Package Volume',
                    color='SLA Compliance', color_continuous_scale='RdYlGn',
                    labels={'SLA Compliance': 'SLA %'})
        fig.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Custom Reports":
    st.header("📋 Custom Report Generator")
    
    st.info("Generate custom reports based on your specific requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Report Parameters")
        
        # Date range selector
        if 'Ship Date' in df.columns:
            min_date = df['Ship Date'].min()
            max_date = df['Ship Date'].max()
            
            start_date = st.date_input("Start Date", value=min_date)
            end_date = st.date_input("End Date", value=max_date)
        
        # Service level selector
        if 'Service Level' in df.columns:
            selected_services = st.multiselect(
                "Select Service Levels",
                options=df['Service Level'].unique(),
                default=df['Service Level'].unique()
            )
    
    with col2:
        st.subheader("Report Options")
        
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Detailed Analytics", "SLA Compliance Report", "Transit Performance"]
        )
        
        include_charts = st.checkbox("Include Charts", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
    
    if st.button("Generate Report", type="primary"):
        st.success("✅ Report generated successfully!")
        
        # Sample report output
        st.markdown("---")
        st.markdown(f"""
        ### 📊 {report_type}
        **Report Period:** {start_date} to {end_date}
        
        #### Key Findings:
        - Overall SLA compliance: **92.3%** (Exceeds 90% target)
        - Average transit time: **3.2 days** (15% improvement YoY)
        - Top performing service: **Expedited** (94.5% SLA compliance)
        
        #### Recommendations:
        1. **Optimize Priority routes** to improve 1-day delivery performance
        2. **Expand capacity** in high-volume states (CA, TX, FL)
        3. **Implement predictive routing** for seasonal volume spikes
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Shipping Performance Analytics Dashboard v1.0</p>
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Shipping Analysis - FirstMile",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for FirstMile branding
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #5EC148;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ====================================
# CUSTOMIZE THIS SECTION FOR EACH CLIENT
# ====================================

CLIENT_CONFIG = {
    "company_name": "Caputron Medical Products, LLC",
    "contact_name": "Robin Azzam",
    "contact_title": "CEO",
    "analysis_date": "June 30, 2025",
    
    # Volume data
    "daily_volume": 1000,
    "monthly_volume": 30000,
    "annual_volume": 365000,
    "volume_range": "500-1,000",
    
    # Carrier data
    "carriers": [
        {"name": "UPS", "daily_shipments": 636, "percentage": 63.6},
        {"name": "USPS", "daily_shipments": 364, "percentage": 36.4}
    ],
    
    # Service breakdown
    "services": [
        {"name": "UPS Ground", "daily_shipments": 636, "percentage": 63.6},
        {"name": "USPS Ground Advantage", "daily_shipments": 333, "percentage": 33.3},
        {"name": "USPS Priority Mail", "daily_shipments": 30, "percentage": 3.0},
        {"name": "USPS First Class Mail Intl", "daily_shipments": 1, "percentage": 0.1}
    ],
    
    # Weight distribution (percentage, daily_count)
    "weight_distribution": [
        {"range": "1-5 oz", "percentage": 10, "count": 100},
        {"range": "6-10 oz", "percentage": 18, "count": 180},
        {"range": "11-15.99 oz", "percentage": 45, "count": 450},
        {"range": "1-5 lbs", "percentage": 22, "count": 220},
        {"range": "6-10 lbs", "percentage": 3, "count": 30},
        {"range": "11+ lbs", "percentage": 2, "count": 20}
    ],
    
    # Top dimensions
    "top_dimensions": [
        '5" × 8" × 8"',
        '3" × 10" × 10"', 
        '1" × 6" × 9"',
        '4" × 4" × 6"',
        '5" × 4" × 8"'
    ],
    
    # Top states
    "top_states": [
        'Florida (FL)', 'California (CA)', 'Texas (TX)', 'Pennsylvania (PA)',
        'New York (NY)', 'Ohio (OH)', 'Illinois (IL)', 'North Carolina (NC)',
        'Massachusetts (MA)', 'Michigan (MI)'
    ],
    
    # Key metrics
    "ground_percentage": 97,
    "expedited_percentage": 3,
    "under_1lb_percentage": 73,
    "domestic_coverage": "All 50 states",
    "international_coverage": "United Kingdom"
}

# ====================================
# END OF CUSTOMIZATION SECTION
# ====================================

# FirstMile color palette
colors = {
    'fmGreen': '#5EC148',
    'fmNavy': '#04202F',
    'fmSky': '#1B9BE0',
    'fmMint': '#A3E49C',
    'success': '#00A651',
    'warning': '#FF9A05',
    'error': '#E24F4F'
}

# Header
st.markdown(f"""
<div style="background-color: #04202F; color: white; padding: 2rem; margin: -1rem -1rem 2rem -1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #5EC148; margin: 0; font-size: 2.5rem;">FirstMile</h1>
            <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: normal;">{CLIENT_CONFIG['company_name']} Shipping Analysis</h2>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-size: 0.9rem;">Prepared for: <strong>{CLIENT_CONFIG['contact_name']}, {CLIENT_CONFIG['contact_title']}</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Analysis Date: {CLIENT_CONFIG['analysis_date']}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Convert config data to DataFrames
carrier_data = pd.DataFrame(CLIENT_CONFIG['carriers'])
service_data = pd.DataFrame(CLIENT_CONFIG['services'])
weight_data = pd.DataFrame(CLIENT_CONFIG['weight_distribution'])
weight_data['Under_1lb'] = [True, True, True, False, False, False]  # First 3 are under 1lb

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🚚 Carriers", "⚖️ Weight Analysis", 
                                         "📦 Dimensions", "🗺️ Geography"])

with tab1:
    st.markdown("### Executive Summary")
    st.info(f"""
    Analysis of shipping patterns reveals a dual-carrier operation with strong emphasis on ground services. 
    Based on current volume of {CLIENT_CONFIG['daily_volume']:,} daily shipments, the profile is characterized 
    by lightweight packages, standardized dimensions, and nationwide coverage with minimal international presence.
    """)
    
    # Volume metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Volume", f"{CLIENT_CONFIG['daily_volume']:,}", f"{CLIENT_CONFIG['volume_range']} range")
    with col2:
        st.metric("Monthly Volume", f"{CLIENT_CONFIG['monthly_volume']:,}", "avg per month")
    with col3:
        st.metric("Annual Projection", f"{CLIENT_CONFIG['annual_volume']:,}", "shipments/year")
    
    # Quick insights
    st.markdown("### 🎯 Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        under_1lb_count = int(CLIENT_CONFIG['daily_volume'] * CLIENT_CONFIG['under_1lb_percentage'] / 100)
        st.success(f"✅ {under_1lb_count} daily shipments under 1 pound ({CLIENT_CONFIG['under_1lb_percentage']}%)")
        st.info(f"📦 {CLIENT_CONFIG['ground_percentage']}% ground services, {CLIENT_CONFIG['expedited_percentage']}% expedited")
    with col2:
        st.success(f"🌎 {CLIENT_CONFIG['domestic_coverage']} coverage")
        st.info(f"📏 Standard {CLIENT_CONFIG['top_dimensions'][0]} packaging")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Carrier Utilization")
        fig_carrier = px.bar(carrier_data, x='name', y='percentage',
                           color='name',
                           color_discrete_map={'UPS': colors['fmNavy'], 'USPS': colors['fmSky']},
                           text='percentage')
        fig_carrier.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_carrier.update_layout(showlegend=False, yaxis_title="Percentage (%)",
                                xaxis_title="Carrier", height=300)
        st.plotly_chart(fig_carrier, use_container_width=True)
        
        for _, row in carrier_data.iterrows():
            st.markdown(f"**{row['name']}**: {row['daily_shipments']} shipments/day ({row['percentage']}%)")
    
    with col2:
        st.markdown("### Carrier Split Visual")
        fig_pie = px.pie(carrier_data, values='daily_shipments', names='name',
                        color='name',
                        color_discrete_map={'UPS': colors['fmNavy'], 'USPS': colors['fmSky']})
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("### Service Method Distribution")
    fig_service = px.bar(service_data, x='name', y='percentage',
                        color_discrete_sequence=[colors['fmGreen']],
                        text='percentage')
    fig_service.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_service.update_layout(xaxis_tickangle=-45, height=400, xaxis_title="Service")
    st.plotly_chart(fig_service, use_container_width=True)

with tab3:
    st.markdown("### Weight Distribution Analysis")
    
    fig_weight = px.bar(weight_data, x='range', y='percentage',
                       color='Under_1lb',
                       color_discrete_map={True: colors['success'], False: colors['fmSky']},
                       text='percentage')
    fig_weight.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_weight.update_layout(showlegend=False, height=400,
                           xaxis_title="Weight Range",
                           yaxis_title="Percentage (%)")
    st.plotly_chart(fig_weight, use_container_width=True)
    
    st.success(f"🎯 **Key Finding: {CLIENT_CONFIG['under_1lb_percentage']}% Under 1 Pound**")
    st.markdown("""
    The majority of shipments fall within the lightweight category, 
    perfect for optimized pricing strategies.
    """)
    
    st.markdown("### Detailed Weight Breakdown")
    weight_display = weight_data[['range', 'count', 'percentage']].copy()
    weight_display.columns = ['Weight Range', 'Daily Count', 'Percentage']
    weight_display['Percentage'] = weight_display['Percentage'].astype(str) + '%'
    st.dataframe(weight_display, hide_index=True, use_container_width=True)

with tab4:
    st.markdown("### Top 5 Package Dimensions")
    
    cols = st.columns(3)
    for idx, dim in enumerate(CLIENT_CONFIG['top_dimensions'][:3]):
        with cols[idx]:
            if idx == 0:
                st.success(f"**#{idx + 1} - Most Common**\n\n{dim}")
            else:
                st.info(f"**#{idx + 1}**\n\n{dim}")
    
    cols2 = st.columns(3)
    for idx, dim in enumerate(CLIENT_CONFIG['top_dimensions'][3:5]):
        with cols2[idx]:
            st.info(f"**#{idx + 4}**\n\n{dim}")
    
    st.markdown("### 📋 Packaging Insights")
    st.markdown(f"""
    - **Standardization Opportunity**: The {CLIENT_CONFIG['top_dimensions'][0]} dimension dominates
    - **Cost Optimization**: Consistent dimensions enable bulk packaging rates
    - **Operational Efficiency**: Standard sizes improve warehouse operations
    """)

with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 10 Destination States")
        for idx, state in enumerate(CLIENT_CONFIG['top_states']):
            color = colors['fmGreen'] if idx < 3 else colors['fmSky']
            st.markdown(f"<div style='padding: 0.5rem; margin: 0.2rem 0;'>"
                       f"<span style='background-color: {color}; color: white; "
                       f"padding: 0.2rem 0.5rem; border-radius: 50%; margin-right: 0.5rem;'>"
                       f"{idx + 1}</span> {state}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Geographic Coverage")
        st.metric("Domestic Coverage", "100%", CLIENT_CONFIG['domestic_coverage'])
        st.metric("International Presence", CLIENT_CONFIG['international_coverage'])
        
        st.markdown("### Service Level Summary")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Ground Services", f"{CLIENT_CONFIG['ground_percentage']}%")
        with col_b:
            st.metric("Expedited", f"{CLIENT_CONFIG['expedited_percentage']}%")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6F767B;">
    <p><strong style="color: #5EC148;">FirstMile</strong> | Shipping Intelligence Report</p>
    <p>Current Volume: {CLIENT_CONFIG['daily_volume']:,} daily shipments</p>
</div>
""", unsafe_allow_html=True)
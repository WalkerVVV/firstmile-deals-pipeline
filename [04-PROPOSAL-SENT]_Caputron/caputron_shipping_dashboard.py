import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Caputron Shipping Analysis - FirstMile",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .header-section {
        background-color: #04202F;
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0;
    }
</style>
""", unsafe_allow_html=True)

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

# Load FirstMile rates data
@st.cache_data
def load_firstmile_rates():
    """Load FirstMile Xparcel rates from Excel file"""
    rates_file = "Caputron Medical Products, LLC._FirstMile_Xparcel_07-24-25.xlsx"
    if os.path.exists(rates_file):
        try:
            # Read the rates sheets
            xparcel_priority = pd.read_excel(rates_file, sheet_name='Xparcel Priority', header=1)
            xparcel_expedited = pd.read_excel(rates_file, sheet_name='Xparcel Expedited', header=1)
            xparcel_ground = pd.read_excel(rates_file, sheet_name='Xparcel Ground', header=1)
            return {
                'priority': xparcel_priority,
                'expedited': xparcel_expedited,
                'ground': xparcel_ground
            }
        except Exception as e:
            st.error(f"Error loading rates file: {str(e)}")
            return None
    return None

# Sidebar for data source selection and calculator
with st.sidebar:
    st.markdown("## 📊 Data Configuration")
    data_source = st.radio(
        "Select Data Source:",
        ["Demo Data", "Live Rates Analysis"],
        index=0
    )
    
    if data_source == "Live Rates Analysis":
        rates_data = load_firstmile_rates()
        if rates_data:
            st.success("✅ Rates loaded successfully")
            selected_service = st.selectbox(
                "Select Service Level:",
                ["Xparcel Priority", "Xparcel Expedited", "Xparcel Ground"]
            )
        else:
            st.error("❌ Could not load rates file")
            data_source = "Demo Data"
    
    # Shipment Cost Calculator
    st.markdown("---")
    st.markdown("## 🧮 Quick Rate Calculator")
    
    calc_weight = st.number_input("Package Weight (lbs):", min_value=0.1, max_value=70.0, value=1.0, step=0.5)
    calc_zone = st.selectbox("Destination Zone:", options=[1, 2, 3, 4, 5, 6, 7, 8], index=4)
    
    if data_source == "Live Rates Analysis" and rates_data:
        calc_service = st.selectbox(
            "Service Level:",
            ["Xparcel Priority", "Xparcel Expedited", "Xparcel Ground"]
        )
        
        # Calculate rate
        service_key = {"Xparcel Priority": "priority", "Xparcel Expedited": "expedited", "Xparcel Ground": "ground"}
        df = rates_data[service_key[calc_service]]
        
        if f'Zone {calc_zone}' in df.columns:
            # Find closest weight
            if df.index.name == 'Weight' or 'Weight' in df.columns:
                weights = df.index if df.index.name == 'Weight' else df['Weight']
                closest_idx = np.abs(weights - calc_weight).argmin()
                rate = df.iloc[closest_idx][f'Zone {calc_zone}']
                
                st.success(f"**Estimated Rate: ${rate:.2f}**")
                
                # Quick comparison
                if st.checkbox("Compare with current rate"):
                    current = st.number_input("Current Rate ($):", value=10.00, step=0.50)
                    savings = current - rate
                    if savings > 0:
                        st.metric("Savings per Package", f"${savings:.2f}", f"-{(savings/current)*100:.1f}%")
                    else:
                        st.metric("Difference", f"${abs(savings):.2f}", f"+{(abs(savings)/current)*100:.1f}%")

# Header
st.markdown("""
<div class="header-section">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: #5EC148; margin: 0; font-size: 2.5rem;">FirstMile</h1>
            <h2 style="color: white; margin: 0; font-size: 1.5rem; font-weight: normal;">Caputron Shipping Analysis</h2>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; font-size: 0.9rem;">Prepared for: <strong>Robin Azzam, CEO</strong></p>
            <p style="margin: 0; font-size: 0.9rem;">Analysis Date: {}</p>
        </div>
    </div>
</div>
""".format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

# Data setup
volume_data = {
    'Daily': 1000,
    'Monthly': 30000,
    'Annual': 365000
}

carrier_data = pd.DataFrame({
    'Carrier': ['UPS', 'USPS'],
    'Daily_Shipments': [636, 364],
    'Percentage': [63.6, 36.4]
})

service_data = pd.DataFrame({
    'Service': ['UPS Ground', 'USPS Ground Advantage', 'USPS Priority Mail', 'USPS First Class Mail Intl'],
    'Daily_Shipments': [636, 333, 30, 1],
    'Percentage': [63.6, 33.3, 3.0, 0.1]
})

weight_data = pd.DataFrame({
    'Weight_Range': ['1-5 oz', '6-10 oz', '11-15.99 oz', '1-5 lbs', '6-10 lbs', '11+ lbs'],
    'Percentage': [10, 18, 45, 22, 3, 2],
    'Daily_Count': [100, 180, 450, 220, 30, 20],
    'Under_1lb': [True, True, True, False, False, False]
})

dimensions_data = ['5" × 8" × 8"', '3" × 10" × 10"', '1" × 6" × 9"', '4" × 4" × 6"', '5" × 4" × 8"']

top_states = ['Florida (FL)', 'California (CA)', 'Texas (TX)', 'Pennsylvania (PA)', 
              'New York (NY)', 'Ohio (OH)', 'Illinois (IL)', 'North Carolina (NC)',
              'Massachusetts (MA)', 'Michigan (MI)']

# Create tabs
if data_source == "Demo Data":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🚚 Carriers", "⚖️ Weight Analysis", 
                                             "📦 Dimensions", "🗺️ Geography"])
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Overview", "🚚 Carriers", "⚖️ Weight Analysis", 
                                                   "📦 Dimensions", "🗺️ Geography", "💰 Rate Analysis"])

with tab1:
    st.markdown("### Executive Summary")
    st.info("""
    Analysis of shipping patterns reveals a dual-carrier operation with strong emphasis on ground services. 
    Based on current volume of 1,000 daily shipments, the profile is characterized by lightweight packages, 
    standardized dimensions, and nationwide coverage with minimal international presence.
    """)
    
    # Volume metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Volume", "1,000", "500-1,000 range")
    with col2:
        st.metric("Monthly Volume", "30,000", "avg per month")
    with col3:
        st.metric("Annual Projection", "365,000", "shipments/year")
    
    # Quick insights
    st.markdown("### 🎯 Quick Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ 730 daily shipments under 1 pound (73%)")
        st.info("📦 97% ground services, 3% expedited")
    with col2:
        st.success("🌎 All 50 states + UK coverage")
        st.info("📏 Standard 5\"×8\"×8\" packaging")

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Carrier Utilization")
        # Carrier bar chart
        fig_carrier = px.bar(carrier_data, x='Carrier', y='Percentage',
                           color='Carrier',
                           color_discrete_map={'UPS': colors['fmNavy'], 'USPS': colors['fmSky']},
                           text='Percentage')
        fig_carrier.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_carrier.update_layout(showlegend=False, yaxis_title="Percentage (%)",
                                height=300)
        st.plotly_chart(fig_carrier, use_container_width=True)
        
        for _, row in carrier_data.iterrows():
            st.markdown(f"**{row['Carrier']}**: {row['Daily_Shipments']} shipments/day ({row['Percentage']}%)")
    
    with col2:
        st.markdown("### Carrier Split Visual")
        # Pie chart
        fig_pie = px.pie(carrier_data, values='Daily_Shipments', names='Carrier',
                        color='Carrier',
                        color_discrete_map={'UPS': colors['fmNavy'], 'USPS': colors['fmSky']})
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Service breakdown
    st.markdown("### Service Method Distribution")
    fig_service = px.bar(service_data, x='Service', y='Percentage',
                        color_discrete_sequence=[colors['fmGreen']],
                        text='Percentage')
    fig_service.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_service.update_layout(xaxis_tickangle=-45, height=400)
    st.plotly_chart(fig_service, use_container_width=True)

with tab3:
    st.markdown("### Weight Distribution Analysis")
    
    # Create color mapping for weight ranges
    weight_colors = ['#00A651' if under_1lb else '#1B9BE0' 
                     for under_1lb in weight_data['Under_1lb']]
    
    fig_weight = px.bar(weight_data, x='Weight_Range', y='Percentage',
                       color='Under_1lb',
                       color_discrete_map={True: colors['success'], False: colors['fmSky']},
                       text='Percentage')
    fig_weight.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_weight.update_layout(showlegend=False, height=400,
                           xaxis_title="Weight Range",
                           yaxis_title="Percentage (%)")
    st.plotly_chart(fig_weight, use_container_width=True)
    
    # Key finding highlight
    st.success(f"🎯 **Key Finding: 73% Under 1 Pound**")
    st.markdown("""
    The majority of shipments fall within the lightweight category, 
    with the 11-15.99 oz range representing the highest concentration at 45%.
    """)
    
    # Weight details table
    st.markdown("### Detailed Weight Breakdown")
    weight_display = weight_data[['Weight_Range', 'Daily_Count', 'Percentage']].copy()
    weight_display['Percentage'] = weight_display['Percentage'].astype(str) + '%'
    st.dataframe(weight_display, hide_index=True, use_container_width=True)

with tab4:
    st.markdown("### Top 5 Package Dimensions")
    
    # Create dimension cards
    cols = st.columns(3)
    for idx, dim in enumerate(dimensions_data[:3]):
        with cols[idx]:
            if idx == 0:
                st.success(f"**#{idx + 1} - Most Common**\n\n{dim}")
            else:
                st.info(f"**#{idx + 1}**\n\n{dim}")
    
    # Remaining dimensions
    cols2 = st.columns(3)
    for idx, dim in enumerate(dimensions_data[3:5]):
        with cols2[idx]:
            st.info(f"**#{idx + 4}**\n\n{dim}")
    
    st.markdown("### 📋 Packaging Insights")
    st.markdown("""
    - **Standardization Opportunity**: The 5"×8"×8" dimension dominates
    - **Cost Optimization**: Consistent dimensions enable bulk packaging rates
    - **Operational Efficiency**: Standard sizes improve warehouse operations
    """)

with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 10 Destination States")
        states_df = pd.DataFrame({
            'State': top_states,
            'Rank': range(1, 11)
        })
        
        # Create a simple bar chart for visual representation
        fig_states = px.bar(x=range(10, 0, -1), y=top_states[::-1], 
                          orientation='h',
                          color=[1,1,1,2,2,2,2,3,3,3],
                          color_continuous_scale=[colors['fmGreen'], colors['fmSky'], colors['fmMint']])
        fig_states.update_layout(showlegend=False, 
                               xaxis_title="Relative Volume",
                               yaxis_title="",
                               coloraxis_showscale=False,
                               height=400)
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col2:
        st.markdown("### Geographic Coverage")
        
        # Coverage metrics
        st.metric("Domestic Coverage", "100%", "All 50 states served")
        st.metric("International Presence", "United Kingdom", "Tower Hamlets, London")
        
        # Service level summary
        st.markdown("### Service Level Summary")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Ground Services", "97%")
        with col_b:
            st.metric("Expedited", "3%")

# Rate Analysis Tab (only shown when Live Rates Analysis is selected)
if data_source == "Live Rates Analysis" and rates_data:
    with tab6:
        st.markdown("### 💰 FirstMile Xparcel Rate Analysis")
        
        # Service selection
        service_map = {
            "Xparcel Priority": "priority",
            "Xparcel Expedited": "expedited", 
            "Xparcel Ground": "ground"
        }
        
        selected_df = rates_data[service_map[selected_service]]
        
        # Weight range slider
        col1, col2 = st.columns(2)
        with col1:
            weight_range = st.slider(
                "Select Weight Range (lbs):",
                min_value=0.0,
                max_value=20.0,
                value=(0.0, 5.0),
                step=0.5
            )
        
        with col2:
            zones = st.multiselect(
                "Select Zones:",
                options=[1, 2, 3, 4, 5, 6, 7, 8],
                default=[1, 2, 3, 4, 5]
            )
        
        # Filter data based on weight range
        weight_cols = []
        for col in selected_df.columns:
            if col.startswith('Zone'):
                weight_cols.append(col)
        
        # Extract weight from index if available
        if 'Weight' in selected_df.columns or selected_df.index.name == 'Weight':
            weights = selected_df.index if selected_df.index.name == 'Weight' else selected_df['Weight']
            mask = (weights >= weight_range[0]) & (weights <= weight_range[1])
            filtered_df = selected_df[mask]
        else:
            filtered_df = selected_df
        
        # Create rate visualization
        st.markdown(f"#### {selected_service} Rates by Zone")
        
        if not filtered_df.empty:
            # Prepare data for visualization
            zone_cols = [f'Zone {z}' for z in zones if f'Zone {z}' in filtered_df.columns]
            
            if zone_cols:
                # Create line chart for rates by weight and zone
                fig_rates = go.Figure()
                
                for zone_col in zone_cols:
                    if zone_col in filtered_df.columns:
                        fig_rates.add_trace(go.Scatter(
                            x=filtered_df.index,
                            y=filtered_df[zone_col],
                            mode='lines+markers',
                            name=zone_col,
                            line=dict(width=2)
                        ))
                
                fig_rates.update_layout(
                    xaxis_title="Weight (lbs)",
                    yaxis_title="Rate ($)",
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_rates, use_container_width=True)
                
                # Show data table
                st.markdown("#### Rate Table")
                display_cols = ['Weight'] + zone_cols if 'Weight' in filtered_df.columns else zone_cols
                st.dataframe(
                    filtered_df[display_cols] if 'Weight' in filtered_df.columns else filtered_df[zone_cols],
                    use_container_width=True
                )
                
                # Cost savings analysis
                st.markdown("### 💡 Potential Savings Analysis")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_weight = st.number_input("Average Package Weight (lbs):", value=1.0, step=0.5)
                with col2:
                    current_rate = st.number_input("Current Avg Rate ($):", value=8.50, step=0.50)
                with col3:
                    monthly_volume = st.number_input("Monthly Volume:", value=30000, step=1000)
                
                # Calculate savings
                if zone_cols and avg_weight <= filtered_df.index.max():
                    # Find closest weight in the rate table
                    closest_weight = filtered_df.index[np.abs(filtered_df.index - avg_weight).argmin()]
                    avg_fm_rate = filtered_df.loc[closest_weight, zone_cols].mean()
                    
                    monthly_savings = (current_rate - avg_fm_rate) * monthly_volume
                    annual_savings = monthly_savings * 12
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("FirstMile Rate", f"${avg_fm_rate:.2f}", f"-${current_rate - avg_fm_rate:.2f}")
                    with col2:
                        st.metric("Monthly Savings", f"${monthly_savings:,.0f}")
                    with col3:
                        st.metric("Annual Savings", f"${annual_savings:,.0f}")
                    
                    if monthly_savings > 0:
                        st.success(f"🎯 **Potential savings of {(1 - avg_fm_rate/current_rate)*100:.1f}% per shipment!**")
            else:
                st.warning("No zone data available for the selected range.")
        else:
            st.warning("No data available for the selected weight range.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6F767B;">
    <p><strong style="color: #5EC148;">FirstMile</strong> | Shipping Intelligence Report</p>
    <p>Current Volume: 1,000 daily shipments</p>
</div>
""", unsafe_allow_html=True)
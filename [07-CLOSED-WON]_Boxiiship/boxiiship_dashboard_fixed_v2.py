import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from PIL import Image
import numpy as np

st.set_page_config(page_title="FirstMile Xparcel Analytics Dashboard", layout="wide")

# Custom CSS for FirstMile branding with fixed tab visibility
st.markdown("""
<style>
    .main {padding-top: 0;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    .metric-row {display: flex; justify-content: space-between; margin-bottom: 20px;}
    
    /* Fix for white tabs issue */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        color: #1a1a1a;
        font-weight: 500;
        border: 1px solid #e0e0e0;
        margin: 0 0.25rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Clean table styling */
    .dataframe {
        font-size: 0.9rem;
        border: 1px solid #e0e0e0;
    }
    
    .dataframe th {
        background-color: #f0f2f6 !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 0.75rem !important;
    }
    
    .dataframe td {
        padding: 0.5rem !important;
        border-bottom: 1px solid #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('BoxiiShip_AF_Make_Wellness_Jan_1_to_July_15_2025.xlsx')
        df['Request Date'] = pd.to_datetime(df['Request Date'])
        return df
    except FileNotFoundError:
        # Generate sample data if Excel file not found
        st.warning("Excel file not found. Using sample data for demonstration.")
        dates = pd.date_range(start='2025-01-01', end='2025-07-15', freq='D')
        sample_data = []
        
        for i, date in enumerate(dates):
            for j in range(np.random.randint(5, 25)):  # Random number of shipments per day
                sample_data.append({
                    'Request Date': date,
                    'Tracking Number': f'926129033973760418{str(i*100+j).zfill(4)}',
                    'Xparcel Type': np.random.choice(['Direct Call', 'Expedited', 'Ground'], p=[0.3, 0.4, 0.3]),
                    'Days In Transit': np.random.randint(0, 12),
                    'Destination State': np.random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']),
                    'Delivered Status': np.random.choice(['Delivered', 'In Transit'], p=[0.9, 0.1])
                })
        
        return pd.DataFrame(sample_data)

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Request Date'].min(), df['Request Date'].max()),
    min_value=df['Request Date'].min(),
    max_value=df['Request Date'].max()
)

# Service level filter with updated names
service_levels = st.sidebar.multiselect(
    "Select Service Levels",
    options=['Direct Call', 'Expedited', 'Ground'],
    default=['Direct Call', 'Expedited', 'Ground']
)

# State filter
states = st.sidebar.multiselect(
    "Select States",
    options=sorted(df['Destination State'].unique()),
    default=None
)

# Apply filters
filtered_df = df[
    (df['Request Date'].dt.date >= date_range[0]) &
    (df['Request Date'].dt.date <= date_range[1]) &
    (df['Xparcel Type'].isin(service_levels))
]

if states:
    filtered_df = filtered_df[filtered_df['Destination State'].isin(states)]

# Header
st.title("FirstMile Xparcel Performance Analytics Dashboard")
st.markdown(f"**Customer:** BoxiiShip-System Beauty Logistics | **Report Date:** {datetime.now().strftime('%B %d, %Y')}")

# Define color palette
COLORS = {
    'primary_blue': '#1f77b4',
    'primary_orange': '#ff7f0e',
    'secondary_blue': '#17becf',
    'secondary_orange': '#ff9896',
    'green': '#2ca02c',
    'red': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2',
    'gray': '#7f7f7f',
    'light_gray': '#f0f2f6',
    'dark_gray': '#4d4d4d'
}

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["SLA Performance", "Trends", "Geographic", "Detailed View", "Export Center", "Image Center"])

with tab1:
    st.header("SLA Compliance - Primary Metric")
    
    delivered_df = filtered_df[filtered_df['Delivered Status'] == 'Delivered']
    
    col1, col2, col3 = st.columns(3)
    
    # Updated service configurations with correct SLA days
    service_configs = [
        ('Direct Call', 'Xparcel Priority (Exp Plus)', 3, col1),  # 1-3 days
        ('Expedited', 'Xparcel Expedited', 5, col2),  # 2-5 days
        ('Ground', 'Xparcel Ground', 8, col3)  # 3-8 days
    ]
    
    for xtype, display_name, sla_days, column in service_configs:
        service_df = delivered_df[delivered_df['Xparcel Type'] == xtype]
        if len(service_df) > 0:
            within_sla = len(service_df[service_df['Days In Transit'] <= sla_days])
            compliance = (within_sla / len(service_df)) * 100
            
            with column:
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = compliance,
                    title = {'text': f"{display_name}<br>{sla_days}-Day SLA"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    delta = {'reference': 95},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkgreen" if compliance >= 95 else "orange" if compliance >= 90 else "red"},
                        'steps': [
                            {'range': [0, 90], 'color': "lightgray"},
                            {'range': [90, 95], 'color': "lightyellow"},
                            {'range': [95, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 95
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.metric("Total Delivered", f"{len(service_df):,}")
                st.metric("Within SLA", f"{within_sla:,}")

with tab2:
    st.header("Performance Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly trend with improved visualization
        monthly_df = filtered_df.copy()
        monthly_df['Month'] = monthly_df['Request Date'].dt.to_period('M').astype(str)
        
        monthly_stats = monthly_df.groupby('Month').agg({
            'Tracking Number': 'count',
            'Days In Transit': 'mean'
        }).reset_index()
        
        fig1 = go.Figure()
        
        # Add bar chart for volume
        fig1.add_trace(go.Bar(
            x=monthly_stats['Month'],
            y=monthly_stats['Tracking Number'],
            name='Shipment Volume',
            yaxis='y',
            marker_color=COLORS['primary_blue'],
            opacity=0.7
        ))
        
        # Add line chart for transit time
        fig1.add_trace(go.Scatter(
            x=monthly_stats['Month'],
            y=monthly_stats['Days In Transit'],
            name='Avg Transit Days',
            yaxis='y2',
            line=dict(color=COLORS['primary_orange'], width=3),
            mode='lines+markers'
        ))
        
        # Update layout with correct syntax
        fig1.update_layout(
            title='Monthly Performance Trends',
            xaxis=dict(title='Month'),
            yaxis=dict(
                title='Shipment Volume',
                tickfont=dict(color=COLORS['primary_blue'])
            ),
            yaxis2=dict(
                title='Average Transit Days',
                tickfont=dict(color=COLORS['primary_orange']),
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            legend=dict(x=0.1, y=0.95)
        )
        
        # Update colors directly in layout
        fig1.update_layout(
            yaxis=dict(title_font=dict(color=COLORS['primary_blue'])),
            yaxis2=dict(title_font=dict(color=COLORS['primary_orange']))
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Improved transit time distribution
        delivered_df = filtered_df[filtered_df['Delivered Status'] == 'Delivered']
        
        if len(delivered_df) > 0:
            # Create individual bars for each day
            max_days = int(delivered_df['Days In Transit'].max())
            day_counts = []
            
            for day in range(max_days + 1):
                count = len(delivered_df[delivered_df['Days In Transit'] == day])
                day_counts.append({
                    'Day': f"Day {day}",
                    'Count': count,
                    'DayNum': day
                })
            
            day_df = pd.DataFrame(day_counts)
            
            # Create color list based on day
            colors = []
            for day in day_df['DayNum']:
                if day <= 2:
                    colors.append(COLORS['green'])
                elif day <= 4:
                    colors.append(COLORS['primary_orange'])
                else:
                    colors.append(COLORS['red'])
            
            fig2 = px.bar(day_df, x='Day', y='Count', 
                          title='Transit Time Distribution',
                          labels={'Count': 'Number of Packages'})
            
            fig2.update_traces(marker_color=colors)
            fig2.update_layout(showlegend=False)
            
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Geographic Distribution")
    
    state_stats = filtered_df.groupby('Destination State').agg({
        'Tracking Number': 'count',
        'Days In Transit': 'mean'
    }).reset_index()
    state_stats.columns = ['State', 'Shipments', 'Avg Transit Days']
    state_stats = state_stats.sort_values('Shipments', ascending=False)
    
    # Map with blue/orange color scheme
    fig3 = px.choropleth(state_stats, 
                        locations='State', 
                        locationmode="USA-states",
                        color='Shipments',
                        scope="usa",
                        title="Shipments by State",
                        color_continuous_scale=[[0, COLORS['primary_blue']], 
                                              [0.5, COLORS['secondary_blue']], 
                                              [1, COLORS['primary_orange']]],
                        labels={'Shipments': 'Package Volume'})
    
    fig3.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='albers usa'
        )
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Top 10 states as table instead of bar chart
    st.subheader("Top 10 Destination States")
    top_states = state_stats.head(10).copy()
    top_states['Percentage'] = (top_states['Shipments'] / state_stats['Shipments'].sum() * 100).round(2)
    top_states['Avg Transit Days'] = top_states['Avg Transit Days'].round(1)
    
    # Format the table
    styled_table = top_states.style.format({
        'Shipments': '{:,.0f}',
        'Avg Transit Days': '{:.1f}',
        'Percentage': '{:.2f}%'
    })
    
    st.dataframe(styled_table, use_container_width=True, hide_index=True)

with tab4:
    st.header("Detailed Data View")
    
    # Simplified column selection
    default_columns = ['Tracking Number', 'Xparcel Type', 'Days In Transit', 'Destination State', 'Delivered Status', 'Request Date']
    available_columns = [col for col in default_columns if col in filtered_df.columns]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        delivered_count = len(filtered_df[filtered_df['Delivered Status'] == 'Delivered'])
        st.metric("Delivered", f"{delivered_count:,}")
    with col3:
        in_transit_count = len(filtered_df[filtered_df['Delivered Status'] == 'In Transit'])
        st.metric("In Transit", f"{in_transit_count:,}")
    with col4:
        avg_transit = filtered_df['Days In Transit'].mean()
        st.metric("Avg Transit Days", f"{avg_transit:.1f}")
    
    # Display data
    st.subheader("Shipment Details")
    st.dataframe(filtered_df[available_columns].sort_values('Request Date', ascending=False), 
                use_container_width=True, 
                hide_index=True)

with tab5:
    st.header("Export Center")
    st.markdown("Generate and download customized reports based on your current filter selections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Options")
        
        export_type = st.selectbox(
            "Select Report Type",
            ["SLA Compliance Report", "Monthly Performance", "State Analysis", "Full Dataset"]
        )
        
        file_format = st.radio("File Format", ["Excel (.xlsx)", "CSV (.csv)"])
        
        include_summary = st.checkbox("Include Summary Statistics", value=True)
    
    with col2:
        st.subheader("Generate Report")
        
        if st.button("Create Export", type="primary"):
            
            if export_type == "SLA Compliance Report":
                # Create SLA compliance data
                delivered_df = filtered_df[filtered_df['Delivered Status'] == 'Delivered']
                sla_data = []
                
                for xtype, display_name, sla_days in [
                    ('Direct Call', 'Xparcel Priority (Exp Plus)', 3),
                    ('Expedited', 'Xparcel Expedited', 5),
                    ('Ground', 'Xparcel Ground', 8)
                ]:
                    service_df = delivered_df[delivered_df['Xparcel Type'] == xtype]
                    if len(service_df) > 0:
                        within_sla = len(service_df[service_df['Days In Transit'] <= sla_days])
                        compliance = (within_sla / len(service_df)) * 100
                        sla_data.append({
                            'Service Level': display_name,
                            'SLA Window': f"{sla_days} days",
                            'Total Packages': len(service_df),
                            'Within SLA': within_sla,
                            'Outside SLA': len(service_df) - within_sla,
                            'Compliance %': round(compliance, 2)
                        })
                export_df = pd.DataFrame(sla_data)
                
            elif export_type == "Monthly Performance":
                monthly_df = filtered_df.copy()
                monthly_df['Month'] = monthly_df['Request Date'].dt.to_period('M').astype(str)
                export_df = monthly_df.groupby(['Month', 'Xparcel Type']).agg({
                    'Tracking Number': 'count',
                    'Days In Transit': ['mean', 'min', 'max']
                }).round(2).reset_index()
                export_df.columns = ['Month', 'Service Level', 'Total Packages', 'Avg Transit Days', 'Min Transit Days', 'Max Transit Days']
                
            elif export_type == "State Analysis":
                export_df = filtered_df.groupby(['Destination State', 'Xparcel Type']).agg({
                    'Tracking Number': 'count',
                    'Days In Transit': 'mean'
                }).round(2).reset_index()
                export_df.columns = ['State', 'Service Level', 'Package Count', 'Avg Transit Days']
                export_df = export_df.sort_values('Package Count', ascending=False)
                
            else:  # Full dataset
                export_df = filtered_df
            
            # Create download
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if "Excel" in file_format:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, sheet_name='Data', index=False)
                    
                    if include_summary:
                        summary_df = pd.DataFrame({
                            'Metric': ['Total Records', 'Date Range', 'Services Included', 'States Included'],
                            'Value': [
                                len(filtered_df),
                                f"{date_range[0]} to {date_range[1]}",
                                ', '.join(service_levels),
                                ', '.join(states) if states else 'All States'
                            ]
                        })
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
                        
                buffer.seek(0)
                
                st.download_button(
                    label="Download Excel Report",
                    data=buffer,
                    file_name=f"FirstMile_{export_type.replace(' ', '_')}_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:  # CSV
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV Report",
                    data=csv,
                    file_name=f"FirstMile_{export_type.replace(' ', '_')}_{timestamp}.csv",
                    mime="text/csv"
                )
            
            st.success("Export generated successfully!")

with tab6:
    st.header("Image Center")
    st.markdown("Manage screenshots and images for documentation and analysis")
    
    # Image upload section
    uploaded_files = st.file_uploader(
        "Upload Images", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Select one or more image files to upload"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            
            # Store image info
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            image_info = {
                'name': uploaded_file.name,
                'image': image,
                'timestamp': timestamp,
                'size': f"{image.size[0]}x{image.size[1]}"
            }
            
            if image_info not in st.session_state.uploaded_images:
                st.session_state.uploaded_images.append(image_info)
    
    # Image management
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.session_state.uploaded_images:
            st.subheader(f"Stored Images ({len(st.session_state.uploaded_images)})")
            
            # Display images in a grid
            cols = st.columns(3)
            for idx, img_info in enumerate(st.session_state.uploaded_images):
                with cols[idx % 3]:
                    st.image(img_info['image'], caption=img_info['name'], use_column_width=True)
                    st.caption(f"Uploaded: {img_info['timestamp']}")
                    
                    # Delete button for individual image
                    if st.button(f"Remove", key=f"remove_{idx}"):
                        st.session_state.uploaded_images.pop(idx)
                        st.rerun()
        else:
            st.info("No images uploaded yet. Use the file uploader above to add images.")
    
    with col2:
        st.subheader("Actions")
        
        if st.session_state.uploaded_images:
            # Clear all button
            if st.button("Clear All Images", type="secondary", use_container_width=True):
                st.session_state.uploaded_images = []
                st.rerun()
            
            st.markdown("---")
            
            # Export options
            st.markdown("**Export Options**")
            
            if st.button("Generate Image Report", type="primary", use_container_width=True):
                # Create HTML report
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>FirstMile Image Report</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h1 {{ color: #1f77b4; }}
                        .image-section {{ margin: 20px 0; border: 1px solid #ddd; padding: 15px; }}
                        .metadata {{ color: #666; font-size: 14px; }}
                    </style>
                </head>
                <body>
                    <h1>FirstMile Xparcel Image Documentation</h1>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Total Images: {len(st.session_state.uploaded_images)}</p>
                    <hr>
                """
                
                for i, img_info in enumerate(st.session_state.uploaded_images):
                    html_content += f"""
                    <div class="image-section">
                        <h3>Image {i+1}: {img_info['name']}</h3>
                        <p class="metadata">
                            Timestamp: {img_info['timestamp']}<br>
                            Dimensions: {img_info['size']}
                        </p>
                    </div>
                    """
                
                html_content += """
                </body>
                </html>
                """
                
                st.download_button(
                    label="Download HTML Report",
                    data=html_content,
                    file_name=f"FirstMile_Images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )

# Footer
st.markdown("---")
st.markdown("**FirstMile Xparcel Performance Analytics** | Network Intelligence Platform")
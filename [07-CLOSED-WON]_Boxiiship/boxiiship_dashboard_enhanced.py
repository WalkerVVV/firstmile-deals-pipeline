import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from PIL import Image

st.set_page_config(page_title="FirstMile Xparcel Analytics Dashboard", layout="wide")

# Custom CSS for FirstMile branding and image paste functionality
st.markdown("""
<style>
    .main {padding-top: 0;}
    .stMetric {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    .metric-row {display: flex; justify-content: space-between; margin-bottom: 20px;}
    
    .paste-area {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        background-color: #f8f9fa;
        min-height: 200px;
        transition: all 0.3s ease;
    }
    
    .paste-area:hover {
        border-color: #007bff;
        background-color: #e7f3ff;
    }
    
    .paste-instructions {
        color: #666;
        font-size: 16px;
        margin-bottom: 10px;
    }
    
    .image-gallery {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin: 20px 0;
    }
    
    .image-container {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>

<script>
function handlePaste() {
    document.addEventListener('paste', function(e) {
        var items = e.clipboardData.items;
        for (var i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                var file = items[i].getAsFile();
                var reader = new FileReader();
                reader.onload = function(event) {
                    // Send image data to Streamlit
                    var imageData = event.target.result;
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: imageData
                    }, '*');
                };
                reader.readAsDataURL(file);
                break;
            }
        }
    });
}
handlePaste();
</script>
""", unsafe_allow_html=True)

# Initialize session state for images
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
        st.warning("⚠️ Excel file not found. Using sample data for demonstration.")
        dates = pd.date_range(start='2025-01-01', end='2025-07-15', freq='D')
        sample_data = []
        
        for i, date in enumerate(dates):
            for j in range(np.random.randint(5, 25)):  # Random number of shipments per day
                sample_data.append({
                    'Request Date': date,
                    'Tracking Number': f'926129033973760418{str(i*100+j).zfill(4)}',
                    'Xparcel Type': np.random.choice(['Direct Call', 'Expedited', 'Ground']),
                    'Days In Transit': np.random.randint(0, 12),
                    'Destination State': np.random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']),
                    'Delivered Status': np.random.choice(['Delivered', 'In Transit'], p=[0.8, 0.2])
                })
        
        return pd.DataFrame(sample_data)

# Import numpy for sample data generation
try:
    import numpy as np
except ImportError:
    # If numpy not available, create minimal sample data
    sample_data = [
        {'Request Date': pd.to_datetime('2025-07-01'), 'Tracking Number': '926129033973760418001', 
         'Xparcel Type': 'Expedited', 'Days In Transit': 2, 'Destination State': 'CA', 'Delivered Status': 'Delivered'},
        {'Request Date': pd.to_datetime('2025-07-02'), 'Tracking Number': '926129033973760418002', 
         'Xparcel Type': 'Ground', 'Days In Transit': 5, 'Destination State': 'NY', 'Delivered Status': 'Delivered'},
    ]
    def load_data():
        return pd.DataFrame(sample_data)

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Request Date'].min(), df['Request Date'].max()),
    min_value=df['Request Date'].min(),
    max_value=df['Request Date'].max()
)

# Service level filter
service_levels = st.sidebar.multiselect(
    "Select Service Levels",
    options=['Direct Call', 'Expedited', 'Ground'],
    default=['Direct Call', 'Expedited', 'Ground']
)

# State filter
states = st.sidebar.multiselect(
    "Select States",
    options=df['Destination State'].unique(),
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
st.title("🚚 FirstMile Xparcel Performance Analytics Dashboard")
st.markdown(f"**Customer:** BoxiiShip-System Beauty Logistics | **Report Date:** {datetime.now().strftime('%B %d, %Y')}")

# Tab layout - Added Image Center tab
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 SLA Performance", "📈 Trends", "🗺️ Geographic", "📋 Detailed View", "💾 Export Center", "📸 Image Center"])

with tab1:
    st.header("SLA Compliance - Primary Metric")
    
    delivered_df = filtered_df[filtered_df['Delivered Status'] == 'Delivered']
    
    col1, col2, col3 = st.columns(3)
    
    # Calculate SLA metrics
    service_configs = [
        ('Direct Call', 'Xparcel Priority', 3, col1),
        ('Expedited', 'Xparcel Expedited', 5, col2),
        ('Ground', 'Xparcel Ground', 8, col3)
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
    
    # Monthly trend
    monthly_df = filtered_df.copy()
    monthly_df['Month'] = monthly_df['Request Date'].dt.to_period('M').astype(str)
    
    monthly_stats = monthly_df.groupby('Month').agg({
        'Tracking Number': 'count',
        'Days In Transit': 'mean'
    }).reset_index()
    
    fig1 = px.line(monthly_stats, x='Month', y='Tracking Number', 
                   title='Monthly Shipment Volume',
                   labels={'Tracking Number': 'Shipment Count'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Transit time distribution
    fig2 = px.histogram(delivered_df, x='Days In Transit', 
                       title='Transit Time Distribution',
                       labels={'count': 'Package Count'})
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Geographic Distribution")
    
    state_stats = filtered_df['Destination State'].value_counts().reset_index()
    state_stats.columns = ['State', 'Shipments']
    
    fig3 = px.choropleth(state_stats, 
                        locations='State', 
                        locationmode="USA-states",
                        color='Shipments',
                        scope="usa",
                        title="Shipments by State",
                        color_continuous_scale="Blues")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Top 10 states bar chart
    top_states = state_stats.head(10)
    fig4 = px.bar(top_states, x='State', y='Shipments', 
                  title='Top 10 Destination States')
    st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.header("Detailed Data View")
    
    # Show filtered data with column selection
    columns_to_show = st.multiselect(
        "Select columns to display",
        options=filtered_df.columns.tolist(),
        default=['Tracking Number', 'Xparcel Type', 'Days In Transit', 'Destination State', 'Delivered Status']
    )
    
    st.dataframe(filtered_df[columns_to_show], use_container_width=True)
    
    st.metric("Total Records", f"{len(filtered_df):,}")

with tab5:
    st.header("Export Center")
    st.markdown("Download customized reports based on your current filter selections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Export Options")
        
        export_type = st.selectbox(
            "Select Export Type",
            ["SLA Compliance Report", "Monthly Breakdown", "State Analysis", "Full Filtered Dataset"]
        )
        
        file_format = st.radio("File Format", ["Excel", "CSV"])
    
    with col2:
        st.subheader("📥 Download")
        
        if st.button("Generate Export", type="primary"):
            
            if export_type == "SLA Compliance Report":
                # Create SLA compliance data
                sla_data = []
                for xtype, display_name, sla_days in [
                    ('Direct Call', 'Xparcel Priority', 3),
                    ('Expedited', 'Xparcel Expedited', 5),
                    ('Ground', 'Xparcel Ground', 8)
                ]:
                    service_df = delivered_df[delivered_df['Xparcel Type'] == xtype]
                    if len(service_df) > 0:
                        within_sla = len(service_df[service_df['Days In Transit'] <= sla_days])
                        compliance = (within_sla / len(service_df)) * 100
                        sla_data.append({
                            'Service Level': display_name,
                            'SLA Window (Days)': sla_days,
                            'Total Delivered': len(service_df),
                            'Within SLA': within_sla,
                            'SLA Compliance %': f"{compliance:.2f}%"
                        })
                export_df = pd.DataFrame(sla_data)
                
            elif export_type == "Monthly Breakdown":
                monthly_df = filtered_df.copy()
                monthly_df['Month'] = monthly_df['Request Date'].dt.to_period('M').astype(str)
                export_df = monthly_df.groupby('Month').agg({
                    'Tracking Number': 'count',
                    'Days In Transit': 'mean'
                }).round(2).reset_index()
                export_df.columns = ['Month', 'Total Shipments', 'Avg Transit Days']
                
            elif export_type == "State Analysis":
                export_df = filtered_df['Destination State'].value_counts().reset_index()
                export_df.columns = ['State', 'Shipment Count']
                export_df['Percentage'] = (export_df['Shipment Count'] / export_df['Shipment Count'].sum() * 100).round(2)
                
            else:  # Full dataset
                export_df = filtered_df
            
            # Create download
            if file_format == "Excel":
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, index=False)
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Excel Report",
                    data=buffer,
                    file_name=f"FirstMile_{export_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:  # CSV
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv,
                    file_name=f"FirstMile_{export_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            st.success("✅ Export generated successfully!")

with tab6:
    st.header("📸 Image Center")
    st.markdown("Upload screenshots, images, or paste directly from clipboard for analysis and documentation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Image Upload & Paste")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose image files", 
            accept_multiple_files=True, 
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                
                # Add timestamp to image info
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                image_info = {
                    'name': uploaded_file.name,
                    'image': image,
                    'timestamp': timestamp,
                    'size': f"{image.size[0]}x{image.size[1]}"
                }
                
                if image_info not in st.session_state.uploaded_images:
                    st.session_state.uploaded_images.append(image_info)
        
        # Paste area with instructions
        st.markdown("""
        <div class="paste-area" id="paste-area">
            <div class="paste-instructions">
                📋 <strong>Paste Screenshot Here</strong><br>
                Press <kbd>Ctrl+V</kbd> or <kbd>Cmd+V</kbd> to paste from clipboard<br>
                Or drag and drop image files above
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Manual paste input as backup
        st.markdown("**Manual Paste (if automatic doesn't work):**")
        pasted_data = st.text_area(
            "Paste base64 image data here", 
            placeholder="Right-click -> Paste image data here as backup method",
            height=100
        )
        
        if pasted_data and pasted_data.startswith('data:image'):
            try:
                # Decode base64 image
                header, encoded = pasted_data.split(',', 1)
                image_data = base64.b64decode(encoded)
                image = Image.open(io.BytesIO(image_data))
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                image_info = {
                    'name': f'pasted_image_{timestamp}.png',
                    'image': image,
                    'timestamp': timestamp,
                    'size': f"{image.size[0]}x{image.size[1]}"
                }
                
                if image_info not in st.session_state.uploaded_images:
                    st.session_state.uploaded_images.append(image_info)
                    st.success("✅ Image pasted successfully!")
                    st.experimental_rerun()
                    
            except Exception as e:
                st.error(f"Error processing pasted image: {str(e)}")
    
    with col2:
        st.subheader("Quick Actions")
        
        # Clear all images
        if st.button("🗑️ Clear All Images", type="secondary"):
            st.session_state.uploaded_images = []
            st.experimental_rerun()
        
        # Image count
        st.metric("Images Stored", len(st.session_state.uploaded_images))
        
        # Export images
        if st.session_state.uploaded_images:
            if st.button("📥 Export Image Report"):
                # Create a simple HTML report with images
                html_content = f"""
                <html>
                <head><title>FirstMile Image Report - {datetime.now().strftime('%Y-%m-%d')}</title></head>
                <body>
                <h1>FirstMile Image Documentation Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total Images: {len(st.session_state.uploaded_images)}</p>
                """
                
                for i, img_info in enumerate(st.session_state.uploaded_images):
                    html_content += f"""
                    <h3>Image {i+1}: {img_info['name']}</h3>
                    <p>Uploaded: {img_info['timestamp']} | Size: {img_info['size']}</p>
                    """
                
                html_content += "</body></html>"
                
                st.download_button(
                    label="📥 Download HTML Report",
                    data=html_content,
                    file_name=f"FirstMile_Image_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
    
    # Display uploaded images
    if st.session_state.uploaded_images:
        st.subheader("📋 Uploaded Images")
        
        for i, img_info in enumerate(st.session_state.uploaded_images):
            with st.expander(f"📷 {img_info['name']} - {img_info['timestamp']}", expanded=True):
                col_img, col_info = st.columns([3, 1])
                
                with col_img:
                    st.image(img_info['image'], caption=img_info['name'], use_column_width=True)
                
                with col_info:
                    st.write(f"**Uploaded:** {img_info['timestamp']}")
                    st.write(f"**Size:** {img_info['size']}")
                    st.write(f"**Name:** {img_info['name']}")
                    
                    # Add annotation text area
                    annotation = st.text_area(
                        "Add notes/annotations:", 
                        key=f"annotation_{i}",
                        height=100
                    )
                    
                    # Delete individual image
                    if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                        st.session_state.uploaded_images.pop(i)
                        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("**FirstMile Xparcel Performance Analytics** | Powered by Network Intelligence")

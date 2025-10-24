import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configure page
st.set_page_config(
    page_title="Shipping Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple, clean styling
st.markdown("""
<style>
    /* Clean, minimal styling */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Metric containers */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1A1A1A;
        font-weight: 600;
    }
    
    /* Data tables */
    .dataframe {
        font-size: 0.875rem;
        border: 1px solid #E0E0E0;
    }
    
    .dataframe th {
        background-color: #F5F5F5 !important;
        font-weight: 600 !important;
        text-align: left !important;
        padding: 0.75rem !important;
    }
    
    .dataframe td {
        padding: 0.75rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📦 Shipping Analytics Dashboard")
st.markdown("Track and analyze shipping performance metrics")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    
    page = st.radio(
        "Select View",
        ["Overview", "Performance", "Analytics", "Reports"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # File upload
    st.subheader("Data Input")
    uploaded_file = st.file_uploader(
        "Upload shipping data",
        type=['csv', 'xlsx'],
        help="CSV or Excel format"
    )
    
    st.markdown("---")
    
    # Date filter
    st.subheader("Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End", datetime.now())

# Data loading and processing
@st.cache_data
def load_data(file):
    if file is not None:
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            return df
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return None
    
    # Generate sample data if no file uploaded
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-07-15', freq='D')
    n_records = 10000
    
    df = pd.DataFrame({
        'tracking_number': [f'PKG{i:08d}' for i in range(n_records)],
        'ship_date': np.random.choice(dates, n_records),
        'delivery_date': np.random.choice(dates, n_records) + pd.Timedelta(days=np.random.randint(1, 8)),
        'service': np.random.choice(['Standard', 'Express', 'Priority'], n_records, p=[0.5, 0.3, 0.2]),
        'destination_state': np.random.choice(['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA'], n_records),
        'weight': np.random.exponential(5, n_records) + 0.5,
        'cost': np.random.uniform(5, 50, n_records),
        'status': np.random.choice(['Delivered', 'In Transit', 'Exception'], n_records, p=[0.85, 0.10, 0.05])
    })
    
    # Calculate transit days
    df['transit_days'] = (df['delivery_date'] - df['ship_date']).dt.days
    df['on_time'] = df['transit_days'] <= df['service'].map({'Priority': 2, 'Express': 3, 'Standard': 5})
    
    return df

# Load data
df = load_data(uploaded_file)

if df is None:
    st.info("📊 Using sample data for demonstration")
    df = load_data(None)

# Filter by date range if applicable
if 'ship_date' in df.columns:
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    mask = (df['ship_date'].dt.date >= start_date) & (df['ship_date'].dt.date <= end_date)
    df = df[mask]

# Main content
if page == "Overview":
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_shipments = len(df)
        st.metric(
            label="Total Shipments",
            value=f"{total_shipments:,}"
        )
    
    with col2:
        if 'status' in df.columns:
            delivered = len(df[df['status'] == 'Delivered'])
            delivery_rate = (delivered / total_shipments * 100) if total_shipments > 0 else 0
            st.metric(
                label="Delivery Rate",
                value=f"{delivery_rate:.1f}%",
                delta=f"{delivery_rate - 85:.1f}%" if delivery_rate >= 85 else f"{delivery_rate - 85:.1f}%"
            )
    
    with col3:
        if 'transit_days' in df.columns:
            avg_transit = df['transit_days'].mean()
            st.metric(
                label="Avg Transit Days",
                value=f"{avg_transit:.1f}",
                delta="-0.3 days"
            )
    
    with col4:
        if 'cost' in df.columns:
            total_cost = df['cost'].sum()
            st.metric(
                label="Total Cost",
                value=f"${total_cost:,.0f}",
                delta="+5.2%"
            )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Daily Volume Trend")
        if 'ship_date' in df.columns:
            daily_volume = df.groupby(df['ship_date'].dt.date).size().reset_index(name='count')
            fig = px.line(
                daily_volume, 
                x='ship_date', 
                y='count',
                labels={'ship_date': 'Date', 'count': 'Shipments'}
            )
            fig.update_traces(line_color='#1f77b4')
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
                yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Service Distribution")
        if 'service' in df.columns:
            service_counts = df['service'].value_counts()
            fig = px.pie(
                values=service_counts.values,
                names=service_counts.index,
                color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent shipments table
    st.subheader("Recent Shipments")
    if len(df) > 0:
        recent = df.nlargest(10, 'ship_date')[['tracking_number', 'ship_date', 'service', 'destination_state', 'status']]
        st.dataframe(recent, use_container_width=True, hide_index=True)

elif page == "Performance":
    st.header("Performance Metrics")
    
    # Performance summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("On-Time Performance")
        if 'on_time' in df.columns:
            on_time_rate = (df['on_time'].sum() / len(df) * 100) if len(df) > 0 else 0
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=on_time_rate,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "On-Time Delivery %"},
                delta={'reference': 90},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2ca02c" if on_time_rate >= 90 else "#ff7f0e"},
                    'steps': [
                        {'range': [0, 80], 'color': "#E0E0E0"},
                        {'range': [80, 90], 'color': "#F0F0F0"},
                        {'range': [90, 100], 'color': "#F8F8F8"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Service Level Performance")
        if 'service' in df.columns and 'on_time' in df.columns:
            service_performance = df.groupby('service')['on_time'].agg(['sum', 'count'])
            service_performance['rate'] = (service_performance['sum'] / service_performance['count'] * 100).round(1)
            
            fig = px.bar(
                x=service_performance.index,
                y=service_performance['rate'],
                labels={'x': 'Service Level', 'y': 'On-Time Rate (%)'},
                color=service_performance['rate'],
                color_continuous_scale=['#ff7f0e', '#ffdd00', '#2ca02c'],
                range_color=[80, 100]
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Transit time analysis
    st.subheader("Transit Time Distribution")
    if 'transit_days' in df.columns:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.histogram(
                df,
                x='transit_days',
                nbins=20,
                labels={'transit_days': 'Transit Days', 'count': 'Number of Shipments'}
            )
            fig.update_traces(marker_color='#1f77b4')
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
                yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Transit Statistics")
            st.metric("Average", f"{df['transit_days'].mean():.1f} days")
            st.metric("Median", f"{df['transit_days'].median():.0f} days")
            st.metric("95th Percentile", f"{df['transit_days'].quantile(0.95):.0f} days")

elif page == "Analytics":
    st.header("Shipping Analytics")
    
    # Analysis selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Destination Analysis", "Cost Analysis", "Service Comparison", "Trend Analysis"]
    )
    
    if analysis_type == "Destination Analysis":
        st.subheader("Top Shipping Destinations")
        
        if 'destination_state' in df.columns:
            state_summary = df.groupby('destination_state').agg({
                'tracking_number': 'count',
                'transit_days': 'mean',
                'cost': 'mean'
            }).round(2)
            
            state_summary.columns = ['Shipments', 'Avg Transit Days', 'Avg Cost']
            state_summary = state_summary.sort_values('Shipments', ascending=False).head(10)
            
            # Bar chart
            fig = px.bar(
                state_summary,
                x=state_summary.index,
                y='Shipments',
                labels={'x': 'State', 'Shipments': 'Number of Shipments'}
            )
            fig.update_traces(marker_color='#1f77b4')
            fig.update_layout(
                plot_bgcolor='white',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary table
            st.dataframe(
                state_summary.style.format({
                    'Shipments': '{:,.0f}',
                    'Avg Transit Days': '{:.1f}',
                    'Avg Cost': '${:.2f}'
                }),
                use_container_width=True
            )
    
    elif analysis_type == "Cost Analysis":
        st.subheader("Shipping Cost Analysis")
        
        if 'cost' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Cost by service
                if 'service' in df.columns:
                    avg_cost_by_service = df.groupby('service')['cost'].mean().sort_values()
                    fig = px.bar(
                        x=avg_cost_by_service.values,
                        y=avg_cost_by_service.index,
                        orientation='h',
                        labels={'x': 'Average Cost ($)', 'y': 'Service Level'}
                    )
                    fig.update_traces(marker_color='#2ca02c')
                    fig.update_layout(
                        title="Average Cost by Service",
                        plot_bgcolor='white',
                        xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
                        yaxis=dict(showgrid=False)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Cost distribution
                fig = px.box(
                    df,
                    y='cost',
                    labels={'cost': 'Cost ($)'}
                )
                fig.update_traces(marker_color='#ff7f0e')
                fig.update_layout(
                    title="Cost Distribution",
                    plot_bgcolor='white',
                    yaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Cost summary statistics
            st.markdown("##### Cost Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Cost", f"${df['cost'].sum():,.0f}")
            with col2:
                st.metric("Average Cost", f"${df['cost'].mean():.2f}")
            with col3:
                st.metric("Median Cost", f"${df['cost'].median():.2f}")
            with col4:
                st.metric("Std Deviation", f"${df['cost'].std():.2f}")
    
    elif analysis_type == "Service Comparison":
        st.subheader("Service Level Comparison")
        
        if 'service' in df.columns:
            # Create comparison metrics
            service_metrics = df.groupby('service').agg({
                'tracking_number': 'count',
                'transit_days': ['mean', 'std'],
                'cost': ['mean', 'std'],
                'on_time': 'mean'
            }).round(2)
            
            # Flatten column names
            service_metrics.columns = ['Count', 'Avg Transit', 'Transit Std', 'Avg Cost', 'Cost Std', 'On-Time Rate']
            service_metrics['On-Time Rate'] = (service_metrics['On-Time Rate'] * 100).round(1)
            
            # Display comparison table
            st.dataframe(
                service_metrics.style.format({
                    'Count': '{:,.0f}',
                    'Avg Transit': '{:.1f} days',
                    'Transit Std': '{:.1f}',
                    'Avg Cost': '${:.2f}',
                    'Cost Std': '${:.2f}',
                    'On-Time Rate': '{:.1f}%'
                }),
                use_container_width=True
            )
            
            # Radar chart for comparison
            categories = ['Volume', 'Speed', 'Reliability', 'Cost Efficiency']
            
            fig = go.Figure()
            
            for service in service_metrics.index:
                values = [
                    service_metrics.loc[service, 'Count'] / service_metrics['Count'].max() * 100,
                    (1 - service_metrics.loc[service, 'Avg Transit'] / service_metrics['Avg Transit'].max()) * 100,
                    service_metrics.loc[service, 'On-Time Rate'],
                    (1 - service_metrics.loc[service, 'Avg Cost'] / service_metrics['Avg Cost'].max()) * 100
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=service
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Service Level Performance Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif analysis_type == "Trend Analysis":
        st.subheader("Shipping Trends Over Time")
        
        if 'ship_date' in df.columns:
            # Time aggregation
            time_group = st.radio("Time Period", ["Daily", "Weekly", "Monthly"], horizontal=True)
            
            if time_group == "Daily":
                df['period'] = df['ship_date'].dt.date
            elif time_group == "Weekly":
                df['period'] = df['ship_date'].dt.to_period('W').astype(str)
            else:
                df['period'] = df['ship_date'].dt.to_period('M').astype(str)
            
            # Volume trend
            trend_data = df.groupby('period').agg({
                'tracking_number': 'count',
                'cost': 'sum',
                'transit_days': 'mean'
            }).reset_index()
            
            # Multi-metric trend chart
            fig = go.Figure()
            
            # Add volume bars
            fig.add_trace(go.Bar(
                x=trend_data['period'],
                y=trend_data['tracking_number'],
                name='Volume',
                yaxis='y',
                marker_color='#1f77b4',
                opacity=0.7
            ))
            
            # Add cost line
            fig.add_trace(go.Scatter(
                x=trend_data['period'],
                y=trend_data['cost'],
                name='Total Cost',
                yaxis='y2',
                line=dict(color='#ff7f0e', width=3)
            ))
            
            fig.update_layout(
                title=f"{time_group} Shipping Trends",
                xaxis=dict(title="Period"),
                yaxis=dict(
                    title="Shipment Volume",
                    titlefont=dict(color='#1f77b4'),
                    tickfont=dict(color='#1f77b4')
                ),
                yaxis2=dict(
                    title="Total Cost ($)",
                    titlefont=dict(color='#ff7f0e'),
                    tickfont=dict(color='#ff7f0e'),
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)

elif page == "Reports":
    st.header("Generate Reports")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Executive Summary", "Performance Report", "Cost Analysis", "Custom Report"]
    )
    
    if report_type == "Executive Summary":
        st.subheader("Executive Summary Report")
        
        # Report parameters
        col1, col2 = st.columns(2)
        with col1:
            report_period = st.selectbox("Report Period", ["Last 7 Days", "Last 30 Days", "Last Quarter", "Custom"])
        with col2:
            if report_period == "Custom":
                custom_start = st.date_input("Start Date", datetime.now() - timedelta(days=30))
                custom_end = st.date_input("End Date", datetime.now())
        
        if st.button("Generate Report", type="primary"):
            # Generate executive summary
            st.markdown("---")
            st.markdown("### 📊 Executive Summary")
            st.markdown(f"**Report Period**: {report_period}")
            st.markdown(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Key metrics summary
            total_shipments = len(df)
            total_cost = df['cost'].sum() if 'cost' in df.columns else 0
            avg_transit = df['transit_days'].mean() if 'transit_days' in df.columns else 0
            on_time_rate = (df['on_time'].mean() * 100) if 'on_time' in df.columns else 0
            
            st.markdown("#### Key Performance Indicators")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Shipments", f"{total_shipments:,}")
            with col2:
                st.metric("Total Spend", f"${total_cost:,.0f}")
            with col3:
                st.metric("Avg Transit Time", f"{avg_transit:.1f} days")
            with col4:
                st.metric("On-Time Rate", f"{on_time_rate:.1f}%")
            
            # Insights
            st.markdown("#### Key Insights")
            st.markdown(f"""
            - Shipping volume: **{total_shipments:,}** packages processed
            - Cost efficiency: Average cost per shipment is **${(total_cost/total_shipments):.2f}**
            - Service performance: **{on_time_rate:.1f}%** on-time delivery rate
            - Transit efficiency: Average delivery in **{avg_transit:.1f}** days
            """)
            
            # Recommendations
            st.markdown("#### Recommendations")
            if on_time_rate < 90:
                st.markdown("- ⚠️ On-time performance below target. Review carrier performance.")
            if avg_transit > 4:
                st.markdown("- 📦 Consider upgrading service levels for time-sensitive shipments.")
            st.markdown("- 💰 Explore volume discounts for high-traffic shipping lanes.")
            st.markdown("- 📊 Implement predictive analytics for demand forecasting.")
    
    elif report_type == "Custom Report":
        st.subheader("Custom Report Builder")
        
        # Report configuration
        st.markdown("#### Select Report Components")
        
        col1, col2 = st.columns(2)
        with col1:
            include_summary = st.checkbox("Executive Summary", value=True)
            include_performance = st.checkbox("Performance Metrics", value=True)
            include_cost = st.checkbox("Cost Analysis", value=True)
        with col2:
            include_destinations = st.checkbox("Destination Analysis", value=False)
            include_trends = st.checkbox("Trend Analysis", value=False)
            include_recommendations = st.checkbox("Recommendations", value=True)
        
        # Export format
        export_format = st.selectbox("Export Format", ["PDF", "Excel", "CSV"])
        
        if st.button("Generate Custom Report", type="primary"):
            st.success("✅ Report generated successfully!")
            st.info(f"Report will be exported as {export_format} format.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.875rem;'>
        Shipping Analytics Dashboard | Real-time Performance Tracking
    </div>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Global Death Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main theme */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        color: #a0aec0;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #a0aec0;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 0 10px 10px 0;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    # Load risk factors dataset
    df_risk = pd.read_csv('data/death rate of countries and its causes.csv')
    
    # Load causes of death dataset
    df_causes = pd.read_csv('data/cause_of_deaths2.csv')
    
    return df_risk, df_causes

# Load the data
try:
    df_risk, df_causes = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

if data_loaded:
    # Header
    st.markdown('<h1 class="main-header">🌍 Global Death Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive visualization of global mortality data • Risk Factors & Causes of Death (1990-2019)</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Dataset selection
    dataset_choice = st.sidebar.radio(
        "📊 Select Dataset",
        ["Risk Factors", "Causes of Death", "Compare Both"],
        help="Choose which dataset to explore"
    )
    
    # Get common columns for risk factors
    risk_factors = [col for col in df_risk.columns if col not in ['Entity', 'Code', 'Year']]
    
    # Get cause columns for causes of death
    cause_columns = [col for col in df_causes.columns if col not in ['Country/Territory', 'Code', 'Year']]
    
    # Country filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Geographic Filter")
    
    # Get unique countries from both datasets
    countries_risk = df_risk['Entity'].unique().tolist()
    countries_causes = df_causes['Country/Territory'].unique().tolist()
    all_countries = sorted(list(set(countries_risk) & set(countries_causes)))
    
    # Select All Countries option
    select_all_countries = st.sidebar.checkbox("🌍 Select All Countries", value=False)
    
    if select_all_countries:
        selected_countries = all_countries
        st.sidebar.info(f"✅ All {len(all_countries)} countries selected")
    else:
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            options=all_countries,
            default=['France', 'Germany', 'United States', 'Japan', 'Brazil'][:min(5, len(all_countries))] if len(all_countries) > 0 else all_countries[:5],
            help="Select countries to compare"
        )
    
    # Year range filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Time Period")
    
    min_year = max(df_risk['Year'].min(), df_causes['Year'].min())
    max_year = min(df_risk['Year'].max(), df_causes['Year'].max())
    
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(min_year),
        max_value=int(max_year),
        value=(1990, 2019),
        help="Filter data by year range"
    )
    
    # Causes/Risk Factors filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏥 Causes & Risk Factors")
    
    # Select causes to display
    selected_causes = st.sidebar.multiselect(
        "Select Causes of Death",
        options=cause_columns,
        default=['Cardiovascular Diseases', 'Neoplasms', 'Lower Respiratory Infections', 'Diabetes Mellitus', 'Chronic Kidney Disease'][:min(5, len(cause_columns))],
        help="Select causes of death to analyze"
    )
    
    # Select risk factors to display
    selected_risk_factors = st.sidebar.multiselect(
        "Select Risk Factors",
        options=risk_factors,
        default=['Smoking', 'High systolic blood pressure', 'Air pollution', 'High body mass index', 'High fasting plasma glucose'][:min(5, len(risk_factors))],
        help="Select risk factors to analyze"
    )
    
    # ========================================
    # RISK FACTORS ANALYSIS
    # ========================================
    if dataset_choice in ["Risk Factors", "Compare Both"]:
        st.markdown("## 📈 Risk Factors Analysis")
        st.markdown('<div class="info-box">This dataset shows deaths attributable to various risk factors like air pollution, smoking, diet, and lifestyle choices.</div>', unsafe_allow_html=True)
        
        # Filter data
        df_risk_filtered = df_risk[
            (df_risk['Entity'].isin(selected_countries)) & 
            (df_risk['Year'] >= year_range[0]) & 
            (df_risk['Year'] <= year_range[1])
        ]
        
        if len(df_risk_filtered) > 0:
            # Top row - Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            latest_year = df_risk_filtered['Year'].max()
            latest_data = df_risk_filtered[df_risk_filtered['Year'] == latest_year]
            
            with col1:
                total_deaths = latest_data[risk_factors].sum().sum()
                st.metric(
                    label="🔴 Total Deaths (Latest Year)",
                    value=f"{total_deaths:,.0f}",
                    delta=f"Year {latest_year}"
                )
            
            with col2:
                top_risk = latest_data[risk_factors].sum().idxmax()
                st.metric(
                    label="⚠️ Top Risk Factor",
                    value=top_risk[:25] + "..." if len(top_risk) > 25 else top_risk
                )
            
            with col3:
                num_countries = len(selected_countries)
                st.metric(
                    label="🌍 Countries Analyzed",
                    value=num_countries
                )
            
            with col4:
                years_covered = year_range[1] - year_range[0] + 1
                st.metric(
                    label="📅 Years Covered",
                    value=years_covered
                )
            
            st.markdown("---")
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "🗺️ Comparison", "🌍 World Map", "🔍 Analysis"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Top Risk Factors")
                    
                    # Aggregate risk factors
                    risk_totals = df_risk_filtered[risk_factors].sum().sort_values(ascending=True).tail(10)
                    
                    fig = px.bar(
                        x=risk_totals.values,
                        y=risk_totals.index,
                        orientation='h',
                        color=risk_totals.values,
                        color_continuous_scale='Viridis',
                        labels={'x': 'Total Deaths', 'y': 'Risk Factor'}
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500,
                        showlegend=False,
                        coloraxis_showscale=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### Risk Factor Distribution")
                    
                    # Pie chart of top 8 risk factors
                    top_risks = df_risk_filtered[risk_factors].sum().sort_values(ascending=False).head(8)
                    
                    fig = px.pie(
                        values=top_risks.values,
                        names=top_risks.index,
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500,
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.markdown("### Risk Factor Trends Over Time")
                
                # Select risk factors to trend
                selected_risks = st.multiselect(
                    "Select Risk Factors to Track",
                    options=risk_factors[:20],  # Limit options for performance
                    default=risk_factors[:3] if len(risk_factors) >= 3 else risk_factors,
                    key="risk_trend_select"
                )
                
                if selected_risks:
                    # Group by year and sum
                    trend_data = df_risk_filtered.groupby('Year')[selected_risks].sum().reset_index()
                    
                    fig = px.line(
                        trend_data,
                        x='Year',
                        y=selected_risks,
                        labels={'value': 'Deaths', 'variable': 'Risk Factor'},
                        markers=True
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500,
                        hovermode='x unified'
                    )
                    fig.update_traces(line=dict(width=3))
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.markdown("### Country Comparison")
                
                # Heatmap of risk factors by country
                country_risk = df_risk_filtered.groupby('Entity')[risk_factors[:15]].sum()
                
                fig = px.imshow(
                    country_risk.values,
                    x=country_risk.columns,
                    y=country_risk.index,
                    color_continuous_scale='RdYlBu_r',
                    aspect='auto'
                )
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    xaxis_tickangle=45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.markdown("### Detailed Risk Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Select a specific risk factor
                    selected_risk = st.selectbox(
                        "Select Risk Factor",
                        options=risk_factors,
                        key="risk_analysis_select"
                    )
                    
                    # Show trend for this risk factor across countries
                    risk_by_country = df_risk_filtered.pivot_table(
                        index='Year',
                        columns='Entity',
                        values=selected_risk,
                        aggfunc='sum'
                    ).reset_index()
                    
                    fig = px.area(
                        risk_by_country,
                        x='Year',
                        y=selected_countries,
                        labels={'value': 'Deaths', 'variable': 'Country'}
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Box plot of risk factor distribution
                    st.markdown(f"**Distribution of {selected_risk}**")
                    
                    fig = px.box(
                        df_risk_filtered,
                        x='Entity',
                        y=selected_risk,
                        color='Entity',
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected filters. Please adjust your selection.")
    
    # ========================================
    # CAUSES OF DEATH ANALYSIS
    # ========================================
    if dataset_choice in ["Causes of Death", "Compare Both"]:
        if dataset_choice == "Compare Both":
            st.markdown("---")
        
        st.markdown("## 💀 Causes of Death Analysis")
        st.markdown('<div class="info-box">This dataset shows deaths by specific medical causes like cardiovascular diseases, cancer, infectious diseases, and more.</div>', unsafe_allow_html=True)
        
        # Filter data
        df_causes_filtered = df_causes[
            (df_causes['Country/Territory'].isin(selected_countries)) & 
            (df_causes['Year'] >= year_range[0]) & 
            (df_causes['Year'] <= year_range[1])
        ]
        
        if len(df_causes_filtered) > 0:
            # Top row - Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            latest_year = df_causes_filtered['Year'].max()
            latest_data = df_causes_filtered[df_causes_filtered['Year'] == latest_year]
            
            with col1:
                total_deaths = latest_data[cause_columns].sum().sum()
                st.metric(
                    label="💀 Total Deaths (Latest Year)",
                    value=f"{total_deaths:,.0f}",
                    delta=f"Year {latest_year}"
                )
            
            with col2:
                top_cause = latest_data[cause_columns].sum().idxmax()
                st.metric(
                    label="🏥 Leading Cause",
                    value=top_cause[:25] + "..." if len(top_cause) > 25 else top_cause
                )
            
            with col3:
                # Calculate cardiovascular deaths percentage
                cardio_cols = [c for c in cause_columns if 'Cardio' in c or 'Heart' in c]
                if cardio_cols:
                    cardio_deaths = latest_data[cardio_cols].sum().sum()
                    cardio_pct = (cardio_deaths / total_deaths * 100) if total_deaths > 0 else 0
                    st.metric(
                        label="❤️ Cardiovascular %",
                        value=f"{cardio_pct:.1f}%"
                    )
                else:
                    st.metric(label="❤️ Countries", value=len(selected_countries))
            
            with col4:
                # Cancer deaths
                cancer_cols = [c for c in cause_columns if 'Neoplasm' in c or 'Cancer' in c]
                if cancer_cols:
                    cancer_deaths = latest_data[cancer_cols].sum().sum()
                    st.metric(
                        label="🎗️ Cancer Deaths",
                        value=f"{cancer_deaths:,.0f}"
                    )
                else:
                    st.metric(label="📊 Causes Tracked", value=len(cause_columns))
            
            st.markdown("---")
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🗺️ Geographic", "🔬 Deep Dive"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Leading Causes of Death")
                    
                    # Aggregate causes
                    cause_totals = df_causes_filtered[cause_columns].sum().sort_values(ascending=True).tail(12)
                    
                    fig = px.bar(
                        x=cause_totals.values,
                        y=cause_totals.index,
                        orientation='h',
                        color=cause_totals.values,
                        color_continuous_scale='Reds',
                        labels={'x': 'Total Deaths', 'y': 'Cause of Death'}
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500,
                        showlegend=False,
                        coloraxis_showscale=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### Death Cause Categories")
                    
                    # Sunburst chart
                    top_causes = df_causes_filtered[cause_columns].sum().sort_values(ascending=False).head(10)
                    
                    fig = px.pie(
                        values=top_causes.values,
                        names=top_causes.index,
                        hole=0.5,
                        color_discrete_sequence=px.colors.sequential.RdBu
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500
                    )
                    fig.update_traces(textposition='inside', textinfo='percent')
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.markdown("### Death Cause Trends Over Time")
                
                # Select causes to trend
                selected_causes = st.multiselect(
                    "Select Causes to Track",
                    options=cause_columns,
                    default=['Cardiovascular Diseases', 'Neoplasms', 'Lower Respiratory Infections'][:min(3, len(cause_columns))],
                    key="cause_trend_select"
                )
                
                if selected_causes:
                    # Group by year and sum
                    trend_data = df_causes_filtered.groupby('Year')[selected_causes].sum().reset_index()
                    
                    fig = px.line(
                        trend_data,
                        x='Year',
                        y=selected_causes,
                        labels={'value': 'Deaths', 'variable': 'Cause'},
                        markers=True
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=500,
                        hovermode='x unified'
                    )
                    fig.update_traces(line=dict(width=3))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show percentage change
                    st.markdown("#### Year-over-Year Change")
                    for cause in selected_causes[:3]:
                        first_year_val = trend_data[trend_data['Year'] == year_range[0]][cause].values
                        last_year_val = trend_data[trend_data['Year'] == year_range[1]][cause].values
                        if len(first_year_val) > 0 and len(last_year_val) > 0 and first_year_val[0] > 0:
                            change = ((last_year_val[0] - first_year_val[0]) / first_year_val[0]) * 100
                            st.write(f"**{cause}**: {'📈' if change > 0 else '📉'} {change:+.1f}%")
            
            with tab3:
                st.markdown("### Geographic Distribution")
                
                # Select a cause to visualize
                geo_cause = st.selectbox(
                    "Select Cause of Death",
                    options=cause_columns,
                    index=cause_columns.index('Cardiovascular Diseases') if 'Cardiovascular Diseases' in cause_columns else 0,
                    key="geo_cause_select"
                )
                
                # Bar chart by country
                country_cause = df_causes_filtered.groupby('Country/Territory')[geo_cause].sum().sort_values(ascending=True)
                
                fig = px.bar(
                    x=country_cause.values,
                    y=country_cause.index,
                    orientation='h',
                    color=country_cause.values,
                    color_continuous_scale='Turbo',
                    labels={'x': f'Total Deaths from {geo_cause}', 'y': 'Country'}
                )
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Treemap
                st.markdown("### Proportional View")
                treemap_data = df_causes_filtered.groupby('Country/Territory')[cause_columns[:10]].sum().reset_index()
                treemap_melted = treemap_data.melt(id_vars=['Country/Territory'], var_name='Cause', value_name='Deaths')
                
                fig = px.treemap(
                    treemap_melted,
                    path=['Country/Territory', 'Cause'],
                    values='Deaths',
                    color='Deaths',
                    color_continuous_scale='RdYlGn_r'
                )
                fig.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.markdown("### Deep Dive Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Correlation Between Causes")
                    
                    # Correlation matrix
                    corr_causes = cause_columns[:10]  # Limit for readability
                    corr_data = df_causes_filtered[corr_causes].corr()
                    
                    fig = px.imshow(
                        corr_data,
                        color_continuous_scale='RdBu',
                        aspect='auto'
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=450
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Year-by-Year Breakdown")
                    
                    # Select country for detailed view
                    detail_country = st.selectbox(
                        "Select Country",
                        options=selected_countries,
                        key="detail_country"
                    )
                    
                    country_data = df_causes_filtered[df_causes_filtered['Country/Territory'] == detail_country]
                    top_5_causes = country_data[cause_columns].sum().sort_values(ascending=False).head(5).index.tolist()
                    
                    fig = px.area(
                        country_data,
                        x='Year',
                        y=top_5_causes,
                        labels={'value': 'Deaths', 'variable': 'Cause'}
                    )
                    fig.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        title=f"Top 5 Causes in {detail_country}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected filters. Please adjust your selection.")
    
    # ========================================
    # COMPARISON SECTION (Both Datasets)
    # ========================================
    if dataset_choice == "Compare Both":
        st.markdown("---")
        st.markdown("## 🔗 Risk Factors vs Causes Correlation")
        st.markdown('<div class="info-box">Explore the relationship between risk factors and actual causes of death.</div>', unsafe_allow_html=True)
        
        # Merge datasets for comparison
        df_risk_agg = df_risk[df_risk['Entity'].isin(selected_countries)].groupby(['Entity', 'Year'])[risk_factors[:5]].sum().reset_index()
        df_causes_agg = df_causes[df_causes['Country/Territory'].isin(selected_countries)].groupby(['Country/Territory', 'Year'])[cause_columns[:5]].sum().reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Risk Factors Summary")
            risk_summary = df_risk_agg[risk_factors[:5]].sum()
            
            fig = px.bar(
                x=risk_summary.index,
                y=risk_summary.values,
                color=risk_summary.values,
                color_continuous_scale='Viridis',
                labels={'x': 'Risk Factor', 'y': 'Total Deaths'}
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350,
                coloraxis_showscale=False,
                xaxis_tickangle=45
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Causes Summary")
            cause_summary = df_causes_agg[cause_columns[:5]].sum()
            
            fig = px.bar(
                x=cause_summary.index,
                y=cause_summary.values,
                color=cause_summary.values,
                color_continuous_scale='Reds',
                labels={'x': 'Cause', 'y': 'Total Deaths'}
            )
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350,
                coloraxis_showscale=False,
                xaxis_tickangle=45
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0aec0; padding: 2rem 0;">
        <p>📊 Global Death Analysis Dashboard | Data from 1990-2019</p>
        <p style="font-size: 0.8rem;">Built with Streamlit & Plotly | Data sources: Global Health Statistics</p>
    </div>
    """, unsafe_allow_html=True)

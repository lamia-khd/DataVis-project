# 🏗️ Application Architecture

## Code Structure Breakdown

This document provides a detailed explanation of the `app.py` file structure.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT APPLICATION                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │   SIDEBAR   │  │           MAIN CONTENT              │   │
│  │             │  │                                     │   │
│  │ • Dataset   │  │  ┌─────────────────────────────┐   │   │
│  │   Selector  │  │  │     HEADER & METRICS        │   │   │
│  │             │  │  └─────────────────────────────┘   │   │
│  │ • Country   │  │                                     │   │
│  │   Filter    │  │  ┌─────────────────────────────┐   │   │
│  │             │  │  │    TABBED VISUALIZATIONS    │   │   │
│  │ • Year      │  │  │                             │   │   │
│  │   Range     │  │  │  Tab 1 │ Tab 2 │ Tab 3 │ Tab 4   │
│  │             │  │  │                             │   │   │
│  └─────────────┘  │  └─────────────────────────────┘   │   │
│                   └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Code Sections (Line by Line)

### 1️⃣ **Imports & Configuration** (Lines 1-30)

```python
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
```

**Purpose**: 
- Import required libraries
- Configure Streamlit page settings (title, icon, layout)

---

### 2️⃣ **Custom CSS Styling** (Lines 31-95)

```python
st.markdown("""
<style>
    .main { background: linear-gradient(...); }
    .main-header { ... }
    .metric-card { ... }
    .stTabs { ... }
</style>
""", unsafe_allow_html=True)
```

**Purpose**:
- Define custom dark theme colors
- Style headers, metrics, tabs, and sidebar
- Add glassmorphism and gradient effects

**Key CSS Classes**:
| Class | Purpose |
|-------|---------|
| `.main-header` | Gradient text for title |
| `.metric-card` | Styled metric containers |
| `.info-box` | Blue info boxes |
| `.stTabs` | Custom tab styling |

---

### 3️⃣ **Data Loading Function** (Lines 96-110)

```python
@st.cache_data
def load_data():
    df_risk = pd.read_csv('data/death rate of countries and its causes.csv')
    df_causes = pd.read_csv('data/cause_of_deaths2.csv')
    return df_risk, df_causes

df_risk, df_causes = load_data()
```

**Purpose**:
- Load both CSV datasets
- `@st.cache_data` decorator caches data to avoid reloading on each interaction

**Data Flow**:
```
CSV Files → load_data() → Pandas DataFrames → Visualizations
```

---

### 4️⃣ **Sidebar Controls** (Lines 115-165)

```python
# Dataset selection
dataset_choice = st.sidebar.radio(
    "📊 Select Dataset",
    ["Risk Factors", "Causes of Death", "Compare Both"]
)

# Country filter
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=all_countries,
    default=['France', 'Germany', 'United States', 'Japan', 'Brazil']
)

# Year range
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=1990,
    max_value=2019,
    value=(1990, 2019)
)
```

**Purpose**:
- Provide user controls for filtering data
- Radio buttons for dataset selection
- Multi-select dropdown for countries
- Slider for year range

---

### 5️⃣ **Risk Factors Section** (Lines 170-350)

```python
if dataset_choice in ["Risk Factors", "Compare Both"]:
    # Filter data
    df_risk_filtered = df_risk[
        (df_risk['Entity'].isin(selected_countries)) & 
        (df_risk['Year'] >= year_range[0]) & 
        (df_risk['Year'] <= year_range[1])
    ]
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Deaths", value=...)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Trends", ...])
    
    with tab1:
        # Bar chart
        fig = px.bar(x=..., y=..., color=...)
        st.plotly_chart(fig)
```

**Visualizations in this section**:
1. **Overview Tab**: Bar chart + Pie chart
2. **Trends Tab**: Multi-line chart
3. **Comparison Tab**: Heatmap
4. **Analysis Tab**: Area chart + Box plot

---

### 6️⃣ **Causes of Death Section** (Lines 355-550)

```python
if dataset_choice in ["Causes of Death", "Compare Both"]:
    # Similar structure to Risk Factors
    df_causes_filtered = df_causes[...]
    
    # Four tabs: Overview, Trends, Geographic, Deep Dive
    tab1, tab2, tab3, tab4 = st.tabs([...])
```

**Visualizations in this section**:
1. **Overview Tab**: Bar chart + Pie chart
2. **Trends Tab**: Line chart with YoY analysis
3. **Geographic Tab**: Country bars + Treemap
4. **Deep Dive Tab**: Correlation matrix + Area chart

---

### 7️⃣ **Comparison Section** (Lines 555-620)

```python
if dataset_choice == "Compare Both":
    # Summary visualizations for both datasets side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Risk Factors Summary")
        # Bar chart
    
    with col2:
        st.markdown("### Causes Summary")
        # Bar chart
```

---

## 🔄 Data Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   CSV Files  │────▶│  DataFrames  │────▶│   Filters    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Display    │◀────│   Plotly     │◀────│   Filtered   │
│              │     │   Figures    │     │   Data       │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## 🎨 Plotly Figure Pattern

All visualizations follow this pattern:

```python
# 1. Create figure with Plotly Express
fig = px.bar(
    x=data.values,
    y=data.index,
    color=data.values,
    color_continuous_scale='Viridis'
)

# 2. Update layout for dark theme
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=500,
    showlegend=False
)

# 3. Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
```

---

## 📊 Visualization Types Used

| Plotly Function | Chart Type | Used For |
|-----------------|------------|----------|
| `px.bar()` | Bar Chart | Rankings, comparisons |
| `px.pie()` | Pie/Donut | Distributions |
| `px.line()` | Line Chart | Time series |
| `px.area()` | Stacked Area | Cumulative trends |
| `px.imshow()` | Heatmap | Correlations, matrices |
| `px.treemap()` | Treemap | Hierarchical proportions |
| `px.box()` | Box Plot | Statistical distribution |

---

## 🔧 Key Streamlit Components

| Component | Usage |
|-----------|-------|
| `st.columns()` | Create side-by-side layouts |
| `st.tabs()` | Organize content in tabs |
| `st.metric()` | Display KPI metrics |
| `st.sidebar` | Side navigation panel |
| `st.selectbox()` | Single selection dropdown |
| `st.multiselect()` | Multiple selection |
| `st.slider()` | Range/value slider |
| `st.plotly_chart()` | Render Plotly figures |
| `st.markdown()` | Custom HTML/text |
| `@st.cache_data` | Data caching decorator |

---

## 📱 Responsive Design

The layout adapts to screen sizes:

```python
# Wide layout enabled
st.set_page_config(layout="wide")

# Flexible columns
col1, col2 = st.columns(2)  # 50-50 split

# Full-width charts
st.plotly_chart(fig, use_container_width=True)
```

---

## 🔒 Error Handling

```python
try:
    df_risk, df_causes = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

if data_loaded:
    # Continue with visualizations
```

---

## 🚀 Performance Optimizations

1. **Caching**: `@st.cache_data` prevents reloading CSVs
2. **Lazy Loading**: Tabs only render when selected
3. **Limited Columns**: Only top N columns shown in heatmaps
4. **Filtered Data**: Aggregations done on filtered subsets

---

*This architecture documentation explains how the code is organized and why.*

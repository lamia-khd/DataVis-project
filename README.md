# 🌍 Global Death Analysis Dashboard

A comprehensive, interactive web-based data visualization dashboard built with **Streamlit** and **Plotly** for exploring global mortality data from 1990-2019.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Datasets](#datasets)
- [Code Architecture](#code-architecture)
- [Visualizations](#visualizations)
- [Technologies Used](#technologies-used)
- [Screenshots](#screenshots)

---

## 🎯 Overview

This project provides an interactive dashboard for analyzing global death statistics across countries and time periods. It combines two comprehensive datasets:

1. **Risk Factors Dataset**: Deaths attributable to lifestyle and environmental risk factors
2. **Causes of Death Dataset**: Deaths categorized by specific medical causes

The dashboard allows users to:
- Explore mortality trends over time (1990-2019)
- Compare statistics across multiple countries
- Analyze correlations between risk factors and causes
- Generate interactive visualizations

---

## ✨ Features

### 🎛️ Interactive Controls
- **Dataset Selection**: Switch between Risk Factors, Causes of Death, or Compare Both
- **Country Filter**: Multi-select countries for comparison
- **Year Range Slider**: Filter data by time period (1990-2019)

### 📊 Visualizations
- **Bar Charts**: Top risk factors and leading causes of death
- **Pie/Donut Charts**: Distribution of death causes
- **Line Charts**: Trends over time with year-over-year analysis
- **Heatmaps**: Country comparison matrices
- **Area Charts**: Stacked trends by country
- **Treemaps**: Hierarchical proportional views
- **Correlation Matrices**: Relationships between causes
- **Box Plots**: Statistical distributions

### 🎨 Design
- Modern glassmorphism dark theme
- Gradient colors and smooth animations
- Responsive layout for all screen sizes
- Tabbed navigation for organized content

---

## 📁 Project Structure

```
DataVis project/
│
├── app.py                    # Main Streamlit application (600+ lines)
│   ├── Configuration         # Page setup, CSS styling
│   ├── Data Loading          # Cached data loading functions
│   ├── Sidebar Controls      # User input widgets
│   ├── Risk Factors Section  # Visualizations for dataset 1
│   ├── Causes Section        # Visualizations for dataset 2
│   └── Comparison Section    # Combined analysis
│
├── data/
│   ├── death rate of countries and its causes.csv
│   │   └── Risk factors (28 columns): Air pollution, Smoking, Diet, etc.
│   │
│   └── cause_of_deaths2.csv
│       └── Medical causes (31 columns): Cardiovascular, Cancer, etc.
│
├── README.md                 # This documentation file
└── requirements.txt          # Python dependencies
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download the project**
   ```bash
   cd "DataVis project"
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas plotly numpy
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - Or use the Network URL to access from other devices

---

## 🖥️ Usage

### Basic Workflow

1. **Select Dataset**: Use the sidebar radio button to choose:
   - `Risk Factors` - Analyze lifestyle/environmental factors
   - `Causes of Death` - Analyze medical causes
   - `Compare Both` - Side-by-side analysis

2. **Filter Countries**: Select one or more countries from the dropdown

3. **Adjust Time Period**: Use the year range slider (1990-2019)

4. **Explore Tabs**: Navigate through different visualization tabs:
   - 📊 **Overview** - Summary charts and metrics
   - 📈 **Trends** - Time-series analysis
   - 🗺️ **Geographic/Comparison** - Country comparisons
   - 🔍 **Analysis/Deep Dive** - Detailed breakdowns

---

## 📊 Datasets

### Dataset 1: Risk Factors
**File**: `death rate of countries and its causes.csv`

| Column | Description |
|--------|-------------|
| Entity | Country name |
| Code | ISO country code |
| Year | 1990-2019 |
| Outdoor air pollution | Deaths from outdoor pollution |
| High systolic blood pressure | Hypertension-related deaths |
| Smoking | Tobacco-related deaths |
| Diet high in sodium | Salt-related deaths |
| ... | (28 risk factor columns total) |

### Dataset 2: Causes of Death
**File**: `cause_of_deaths2.csv`

| Column | Description |
|--------|-------------|
| Country/Territory | Country name |
| Code | ISO country code |
| Year | 1990-2019 |
| Meningitis | Deaths from meningitis |
| Cardiovascular Diseases | Heart disease deaths |
| Neoplasms | Cancer deaths |
| ... | (31 cause columns total) |

---

## 🏗️ Code Architecture

### Main Components

```python
# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Death Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

# 2. CUSTOM CSS STYLING
st.markdown("<style>...</style>", unsafe_allow_html=True)

# 3. DATA LOADING (Cached)
@st.cache_data
def load_data():
    df_risk = pd.read_csv('data/death rate of countries and its causes.csv')
    df_causes = pd.read_csv('data/cause_of_deaths2.csv')
    return df_risk, df_causes

# 4. SIDEBAR CONTROLS
dataset_choice = st.sidebar.radio("Select Dataset", [...])
selected_countries = st.sidebar.multiselect("Select Countries", [...])
year_range = st.sidebar.slider("Select Year Range", ...)

# 5. VISUALIZATION SECTIONS
# - Risk Factors Analysis (tabs: Overview, Trends, Comparison, Analysis)
# - Causes of Death Analysis (tabs: Overview, Trends, Geographic, Deep Dive)
# - Combined Comparison Section
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `load_data()` | Load and cache CSV datasets |
| `px.bar()` | Create bar charts |
| `px.pie()` | Create pie/donut charts |
| `px.line()` | Create line trends |
| `px.imshow()` | Create heatmaps |
| `px.area()` | Create stacked area charts |
| `px.treemap()` | Create hierarchical treemaps |
| `px.box()` | Create box plots |

---

## 📈 Visualizations

### Risk Factors Section
| Tab | Visualizations |
|-----|---------------|
| Overview | Top 10 risk factors bar chart, Distribution pie chart |
| Trends | Multi-line time series with markers |
| Comparison | Country-risk factor heatmap |
| Analysis | Area chart by country, Box plot distributions |

### Causes of Death Section
| Tab | Visualizations |
|-----|---------------|
| Overview | Leading causes bar chart, Category pie chart |
| Trends | Line chart with YoY change calculations |
| Geographic | Country comparison bars, Treemap |
| Deep Dive | Correlation matrix, Country-specific area chart |

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Streamlit** | 1.52+ | Web application framework |
| **Pandas** | 2.0+ | Data manipulation and analysis |
| **Plotly** | 5.0+ | Interactive visualizations |
| **NumPy** | 1.24+ | Numerical computations |

---

## 🎨 Theme & Styling

The dashboard uses a custom dark theme with:

- **Primary Colors**: Purple gradient (#667eea → #764ba2)
- **Background**: Dark blue gradient (#1a1a2e → #16213e → #0f3460)
- **Accent Colors**: Viridis, Plasma, RdBu color scales
- **Effects**: Glassmorphism, blur, subtle animations

---

## 📸 Key Metrics Displayed

- **Total Deaths**: Aggregated death count for selected period
- **Top Risk Factor/Leading Cause**: Highest contributor
- **Countries Analyzed**: Number of selected countries
- **Years Covered**: Duration of analysis period
- **Percentage Breakdowns**: Category distributions
- **Year-over-Year Changes**: Trend indicators

---

## 🔧 Customization

### Adding New Countries
The dashboard automatically detects countries present in both datasets.

### Modifying Color Schemes
Edit the `color_continuous_scale` parameter in Plotly figures:
```python
color_continuous_scale='Viridis'  # Options: Plasma, RdBu, Turbo, etc.
```

### Adjusting Chart Sizes
Modify the `height` parameter in figure layouts:
```python
fig.update_layout(height=500)
```

---

## 📝 License

This project is for educational and analytical purposes.

---

## 👤 Author

Created for the **Développer des visualisations pour le Web** project.

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

*Last Updated: December 2024*
"# DataVis-project" 
"# DataVis-project" 

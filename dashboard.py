import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np

# Set page configuration (at the top of your script)
# Set page configuration (at the top of your script)
st.set_page_config(
    page_title="Mr. Life Okey Dashboard",
    page_icon="images/logo.png",
    layout="wide",
)

# 👇 Add this right after st.set_page_config()
hide_default_ui = """
<style>
    #MainMenu {visibility: hidden;}  /* Hides the three-dot menu (⋮) */
    header {visibility: hidden;}     /* Hides the GitHub fork button (🎯) & settings (⚙️) */
    footer {visibility: hidden;}     /* Optional: Hides "Made with Streamlit" */
</style>
"""
st.markdown(hide_default_ui, unsafe_allow_html=True)
######################################
# Custom Styling with Background
######################################
def set_custom_style(background_image_path):
    """
    Set custom styling for the dashboard including background
    """
    with open(background_image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .main .block-container {{
        padding: 2rem;
    }}

    /* Make all text black */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {{
        color: black !important;
    }}

    /* Style for metric values and labels */
    [data-testid="stMetricLabel"] {{
        color: black !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: black !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricDelta"] {{
        color: black !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    /* Make graph text black */
    .js-plotly-plot .plotly .gtitle, 
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {{
        color: black !important;
        fill: black !important;
    }}

    /* Make select boxes and input text black */
    .stSelectbox label, 
    .stMultiSelect label,
    .stSelectbox span,
    .stMultiSelect span {{
        color: black !important;
    }}

    /* Make sidebar text black */
    .stSidebar [data-testid="stSidebarNav"] {{
        color: black !important;
    }}

    /* Make all headers black */
    .kpi-title {{
        color: black !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }}

    /* Add spacing between columns */
    [data-testid="column"] {{
        padding: 0.5rem !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def plot_defaults():
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'black', 'size': 12, 'family': 'Arial, sans-serif'},
        'title': {'font': {'color': 'black', 'size': 14, 'weight': 'bold'}},
        'xaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black', 'size': 12},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5,
            'tickcolor': 'black',
            'linecolor': 'black'
        },
        'yaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black', 'size': 12},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5,
            'tickcolor': 'black',
            'linecolor': 'black'
        },
        'legend': {
            'font': {'color': 'black', 'size': 12},
            'title': {'font': {'color': 'black', 'size': 12}}
        },
        'margin': {'l': 20, 'r': 20, 't': 40, 'b': 20}
    }

######################################
# Dummy Data
######################################
def generate_dummy_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    sales_data = pd.DataFrame({
        'date': dates,
        'sales': np.random.normal(1000, 200, len(dates)),
        'returns': np.random.normal(50, 10, len(dates)),
        'new_customers': np.random.poisson(20, len(dates))
    })

    categories = ['T-Shirts', 'Jeans', 'Shirts', 'Jackets', 'Accessories']
    category_data = pd.DataFrame({
        'category': categories,
        'sales': np.random.randint(1000, 5000, len(categories)),
        'inventory': np.random.randint(500, 2000, len(categories)),
        'profit_margin': np.random.uniform(0.2, 0.4, len(categories))
    })

    return sales_data, category_data

######################################
# KPI + Line Chart
######################################
def show_metrics_line_chart(sales_data):
    st.markdown('<div class="kpi-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    total_sales = sales_data['sales'].sum()
    avg_daily_sales = sales_data['sales'].mean()
    total_customers = sales_data['new_customers'].sum()
    return_rate = (sales_data['returns'].sum() / total_sales) * 100

    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Sales", f"${total_sales:,.0f}", "↑ 12%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Avg Daily Sales", f"${avg_daily_sales:,.0f}", "↑ 5%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Customers", f"{total_customers:,}", "↑ 8%")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Return Rate", f"{return_rate:.1f}%", "↓ 2%")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: black;">Sales Trend</h3>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.line(sales_data, x='date', y=['sales', 'returns'],
                      title='Daily Sales and Returns',
                      labels={'value': 'Amount ($)', 'date': 'Date'},
                      template='plotly_white')
        fig.update_layout(**plot_defaults())
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

######################################
# Category Analysis
######################################
def show_category_analysis(category_data):
    st.markdown('<h3 style="color: black;">Category Performance</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1 = px.bar(category_data, x='category', y='sales',
                      title='Sales by Category',
                      labels={'sales': 'Total Sales ($)', 'category': 'Category'},
                      template='plotly_white')
        layout = plot_defaults()
        layout.update(bargap=0.3)
        fig1.update_layout(**layout)
        fig1.update_traces(marker=dict(
            color='rgba(0, 128, 255, 0.8)',
            line=dict(color='rgba(0, 128, 255, 0.8)', width=0)
        ))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2 = px.pie(category_data, values='sales', names='category',
                      title='Sales Distribution',
                      template='plotly_white',
                      hole=0.4)
        fig2.update_layout(**plot_defaults())
        fig2.update_traces(
            textfont={'color': 'black', 'size': 12},
            textinfo='percent+label'
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

######################################
# Inventory Analysis
######################################
def show_inventory_analysis(category_data):
    st.markdown('### Inventory Management')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1 = px.bar(category_data, x='category', y='inventory',
                      title='Current Inventory Levels',
                      labels={'inventory': 'Units in Stock', 'category': 'Category'},
                      template='plotly_white')
        fig1.update_layout(**plot_defaults())
        fig1.update_traces(marker=dict(
            color='rgba(0, 128, 255, 0.8)',
            line=dict(color='rgba(0, 128, 255, 0.8)', width=0)
        ))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2 = px.scatter(category_data, x='sales', y='inventory',
                          size='profit_margin', color='category',
                          title='Sales vs Inventory Analysis',
                          labels={'sales': 'Total Sales ($)', 'inventory': 'Units in Stock'},
                          template='plotly_white')
        fig2.update_layout(**plot_defaults())
        fig2.update_traces(marker=dict(
            line=dict(width=1, color='black')
        ))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

######################################
# Main
######################################
def main():
    sales_data, category_data = generate_dummy_data()
    set_custom_style("images/background_image.avif")

    with st.sidebar:
        st.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
        st.image("images/logo.png", width=200)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<h2 style="color: black;">Filters</h2>', unsafe_allow_html=True)
        date_range = st.date_input(
            "Select Date Range",
            value=(sales_data['date'].min(), sales_data['date'].max())
        )
        selected_categories = st.multiselect(
            "Select Categories",
            options=category_data['category'].unique(),
            default=category_data['category'].unique()
        )

    st.markdown('<h1 style="text-align: center; color: black;">Mr. Life Okey Clothing Brand Dashboard</h1>', unsafe_allow_html=True)

    show_metrics_line_chart(sales_data)
    show_category_analysis(category_data)
    show_inventory_analysis(category_data)

if __name__ == '__main__':
    main()

# Embed CSS directly in the Python file
css = """
<style>
/* Container for the Metrics section */
.metrics-section {
    margin-bottom: 2rem;  /* Space below the section */
}

/* Styling for the metric cards */
.metrics-section .stMetric {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 5px;
    border-left: 0.5rem solid #9AD8E1;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    margin: 0 10px;  /* Add spacing between cards */
}

/* Styling for the metric label */
.metrics-section .stMetric label {
    color: #36b9cc;
    font-weight: 700;
    text-transform: uppercase;
}

/* Styling for the metric value */
.metrics-section .stMetric [data-testid="stMetricValue"] {
    font-size: 1.5rem;
    font-weight: bold;
}

/* Styling for the metric delta */
.metrics-section .stMetric [data-testid="stMetricDelta"] {
    font-size: 0.9rem;
}

/* Ensure positive delta is green */
.metrics-section .stMetric [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaArrowUp"] {
    fill: #2ECC71;  /* Green for positive delta */
}

/* Ensure negative delta is red */
.metrics-section .stMetric [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaArrowDown"] {
    fill: #E74C3C;  /* Red for negative delta */
}

/* Adjust column spacing */
.metrics-section .stColumns > div {
    display: flex;
    justify-content: center;
}
</style>
"""

# Inject the CSS into the app
st.markdown(css, unsafe_allow_html=True)

# Create the Metrics section
st.markdown('<div class="metrics-section">', unsafe_allow_html=True)
st.markdown('### Metrics')

# Create three columns for the metric cards
col1, col2, col3 = st.columns(3)

# Add metric cards to each column
with col1:
    st.metric("Temperature", "70 °F", "1.2 °F")

with col2:
    st.metric("Wind", "9 mph", "-8%")

with col3:
    st.metric("Humidity", "86%", "4%")

st.markdown('</div>', unsafe_allow_html=True)
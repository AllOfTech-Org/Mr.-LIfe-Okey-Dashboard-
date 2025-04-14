import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Mr. Life Okey Dashboard",
    page_icon="images/logo.png",
    layout="wide",
)

# Hide default UI elements
hide_default_ui = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_default_ui, unsafe_allow_html=True)

######################################
# Custom Styling with Background
######################################
def set_custom_style(background_image_path, sidebar_image_path):
    with open(background_image_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    with open(sidebar_image_path, "rb") as sidebar_img:
        sidebar_encoded = base64.b64encode(sidebar_img.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid=stSidebar] {{
        background-image: url("data:image/png;base64,{sidebar_encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .stSidebar .sidebar-content {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(5px);
        padding: 1rem;
        border-radius: 10px;
    }}

    .main .block-container {{
        padding: 2rem;
    }}

    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {{
        color: black !important;
    }}

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

    .js-plotly-plot .plotly .gtitle, 
    .js-plotly-plot .plotly .xtitle,
    .js-plotly-plot .plotly .ytitle,
    .js-plotly-plot .plotly .xtick text,
    .js-plotly-plot .plotly .ytick text {{
        color: black !important;
        fill: black !important;
    }}

    .stSelectbox label, 
    .stMultiSelect label,
    .stSelectbox span,
    .stMultiSelect span {{
        color: black !important;
    }}

    .stSidebar [data-testid="stSidebarNav"] {{
        color: black !important;
    }}

    .kpi-title {{
        color: black !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }}

    [data-testid="column"] {{
        padding: 0.5rem !important;
    }}

    .sidebar-logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }}

    .sidebar-logo {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 2px solid #00000033;
        object-fit: cover;
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

    col1.metric("Total Sales", f"${total_sales:,.0f}", "↑ 12%")
    col2.metric("Avg Daily Sales", f"${avg_daily_sales:,.0f}", "↑ 5%")
    col3.metric("Total Customers", f"{total_customers:,}", "↑ 8%")
    col4.metric("Return Rate", f"{return_rate:.1f}%", "↓ 2%")

    st.markdown('<h3 style="color: black;">Sales Trend</h3>', unsafe_allow_html=True)
    with st.container():
        fig = px.line(sales_data, x='date', y=['sales', 'returns'],
                      title='Daily Sales and Returns',
                      labels={'value': 'Amount ($)', 'date': 'Date'},
                      template='plotly_white')
        fig.update_layout(**plot_defaults())
        st.plotly_chart(fig, use_container_width=True)

######################################
# Category Analysis
######################################
def show_category_analysis(category_data):
    st.markdown('<h3 style="color: black;">Category Performance</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
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

######################################
# Inventory Analysis
######################################
def show_inventory_analysis(category_data):
    st.markdown('### Inventory Management')
    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
        fig2 = px.scatter(category_data, x='sales', y='inventory',
                          size='profit_margin', color='category',
                          title='Sales vs Inventory Analysis',
                          labels={'sales': 'Total Sales ($)', 'inventory': 'Units in Stock'},
                          template='plotly_white')
        fig2.update_layout(**plot_defaults())
        fig2.update_traces(marker=dict(line=dict(width=1, color='black')))
        st.plotly_chart(fig2, use_container_width=True)

######################################
# Main App
######################################
def main():
    sales_data, category_data = generate_dummy_data()
    set_custom_style("images/background_image.avif", "images/sidebar2.jpg")

    with st.sidebar:
        st.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
        logo_encoded = base64.b64encode(open("images/logo.png", "rb").read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{logo_encoded}" class="sidebar-logo"/>', unsafe_allow_html=True)
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

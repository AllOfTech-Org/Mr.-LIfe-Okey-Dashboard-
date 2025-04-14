import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Mr. Life Okey Dashboard",
    page_icon="👕",
    layout="wide"
)

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
        color: black !important;
    }}

    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        color: black !important;
    }}

    .metric-container {{
        background-color: black !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }}

    .metric-container .stMetric {{
        color: white !important;
    }}

    .metric-container .stMetric label {{
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}

    .metric-container .stMetric [data-testid="stMetricValue"] {{
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }}

    .metric-container .stMetric [data-testid="stMetricDelta"] {{
        color: white !important;
    }}

    .metric-container .stMetric [data-testid="stMetricDelta"] svg {{
        color: white !important;
    }}

    .metric-container .stMetric [data-testid="stMetricDelta"].positive {{
        color: #4CAF50 !important;
    }}

    .metric-container .stMetric [data-testid="stMetricDelta"].negative {{
        color: #f44336 !important;
    }}

    .kpi-title {{
        color: black !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        padding-left: 0.5rem !important;
    }}

    .chart-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
        color: black !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def plot_defaults():
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'black', 'size': 12},
        'title': {'font': {'color': 'black', 'size': 14, 'weight': 'bold'}},
        'xaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black'},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5
        },
        'yaxis': {
            'title': {'font': {'color': 'black', 'size': 12}},
            'tickfont': {'color': 'black'},
            'gridcolor': 'rgba(128,128,128,0.1)',
            'gridwidth': 0.5
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

    with st.container():
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
        fig2.update_traces(textfont={'color': 'black'})
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
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.1)'),
            margin=dict(l=20, r=20, t=40, b=20),
            bargap=0.3
        )
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
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.1)'),
            yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.1)'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig2.update_traces(marker=dict(
            line=dict(width=1, color='white')
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

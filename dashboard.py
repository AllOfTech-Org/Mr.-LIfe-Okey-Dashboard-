import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import numpy as np

# Text Configuration - This will be automatically updated by text_editor.py
TEXT_CONFIG = {
    "metrics": {
        "title": "Key Performance Indicators Analysis",
        "content": "Based on the current data, we observe strong performance in total sales and customer acquisition. The return rate is within acceptable limits, suggesting good product quality and customer satisfaction."
    },
    "sales_trend": {
        "title": "Sales Trend Analysis",
        "content": "The sales trend shows consistent growth with some seasonal variations. Returns are stable, indicating good product quality control."
    },
    "order_analysis": {
        "title": "Order Source Analysis",
        "content": "Website and social media channels are performing well as order sources. Consider increasing marketing efforts on high-performing channels."
    },
    "inventory": {
        "title": "Inventory Management Insights",
        "content": "Current inventory levels are well-balanced across categories. Consider adjusting stock levels based on sales velocity and seasonal trends."
    },
    "category": {
        "title": "Category Performance Review",
        "content": "T-Shirts and Jeans are leading categories in terms of sales. Consider expanding these product lines and analyzing underperforming categories."
    },
    "profitability": {
        "title": "Profitability Assessment",
        "content": "Profit margins are healthy across all categories. Focus on maintaining quality while optimizing production costs."
    },
    "customer_insights": {
        "title": "Customer Behavior Analysis",
        "content": "Customer acquisition is growing steadily. Implement loyalty programs to increase customer retention and repeat purchases."
    },
    "growth": {
        "title": "Growth and Value Analysis",
        "content": "Both customer base and average order value are showing positive trends. Consider upselling strategies to further increase average order value."
    }
}

def create_text_container(title, content):
    return f"""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-top: 10px;'>
    <h4>{title}</h4>
    <p>{content}</p>
    </div>
    """

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

def generate_dummy_product_data():
    # Create dummy data for 20 products
    np.random.seed(42)
    products = [f"Product {i}" for i in range(1, 21)]
    sales = np.random.randint(5000, 20000, size=20)
    product_data = pd.DataFrame({
       "product": products,
       "sales": sales
    })
    return product_data

def generate_order_source_data():
    # Create dummy data for order sources
    sources = ['Facebook', 'Instagram', 'Website', 'Direct']
    orders = np.random.randint(1000, 5000, size=len(sources))
    order_data = pd.DataFrame({
        "source": sources,
        "orders": orders
    })
    return order_data

######################################
# KPI + Time Series Chart
######################################
def show_metrics_chart(sales_data, text_content=""):
    st.markdown('<div class="kpi-title">Key Performance Indicators</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    total_sales = sales_data['sales'].sum()
    avg_daily_sales = sales_data['sales'].mean()
    total_customers = sales_data['new_customers'].sum()
    return_rate = (sales_data['returns'].sum() / total_sales) * 100

    # Apply white background with black text to each metric box
    with col1:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Total Sales</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">${total_sales:,.0f}</p>'
            '<p style="color: green; margin: 0; font-size: 0.9rem;">↑ 12%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Avg Daily Sales</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">${avg_daily_sales:,.0f}</p>'
            '<p style="color: green; margin: 0; font-size: 0.9rem;">↑ 5%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Total Customers</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{total_customers:,}</p>'
            '<p style="color: green; margin: 0; font-size: 0.9rem;">↑ 8%</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            '<div style="border: 2px solid black; background-color: black; padding: 10px; border-radius: 10px; height: 100%;">'
            f'<p style="color: white; margin: 0; font-size: 1rem;">Return Rate</p>'
            f'<p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">{return_rate:.1f}%</p>'
            '<p style="color: red; margin: 0; font-size: 0.9rem;">↓ 2%</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_line_chart(sales_data, text_content=""):
    st.markdown('<h3 style="color: black;">Sales Trend</h3>', unsafe_allow_html=True)
    with st.container():
        fig = px.line(sales_data, x='date', y=['sales', 'returns'],
                      title='Daily Sales and Returns',
                      labels={'value': 'Amount ($)', 'date': 'Date'},
                      template='plotly_white')
        fig.update_layout(**plot_defaults())
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(text_content, unsafe_allow_html=True)

# ######################################
# # Order Source Analysis
# ######################################
# def show_order_source_analysis(order_data):
#     st.markdown('<h3 style="color: black;">Order Sources</h3>', unsafe_allow_html=True)
#     fig = px.pie(order_data, values='orders', names='source',
#                  title='Customer Orders by Source',
#                  template='plotly_white',
#                  hole=0.3)
#     fig.update_layout(**plot_defaults())
#     fig.update_traces(
#         textfont={'color': 'black', 'size': 12},
#         textinfo='percent+label',
#         marker=dict(line=dict(color='black', width=1))
#     )
#     st.plotly_chart(fig, use_container_width=True)

# ######################################
# # Top Products Analysis
# ######################################
# def show_top_products(product_data):
#     st.markdown('<h3 style="color: black;">Top 10 Products</h3>', unsafe_allow_html=True)
#     # Sort and select top 10 products by sales
#     top_products = product_data.sort_values("sales", ascending=False).head(10)
#     fig = px.bar(top_products, x="sales", y="product", orientation="h",
#                  title="Top 10 Products",
#                  labels={"sales": "Sales ($)", "product": "Product"},
#                  template="plotly_white")
#     # Get the default layout and update the yaxis settings
#     layout = plot_defaults()
#     layout["yaxis"].update({'categoryorder': 'total ascending'})
#     fig.update_layout(**layout)
#     st.plotly_chart(fig, use_container_width=True)
def show_order_source_and_top_products(order_data, product_data, text_content=""):
    st.markdown('<h3 style="color: black;">Order Overview</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    # ======== Order Sources Pie Chart ========
    with col1:
        fig1 = px.pie(order_data, values='orders', names='source',
                      title='Customer Orders by Source',
                      template='plotly_white',
                      hole=0.3)
        fig1.update_layout(**plot_defaults())
        fig1.update_traces(
            textfont={'color': 'black', 'size': 12},
            textinfo='percent+label',
            marker=dict(line=dict(color='black', width=1))
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ======== Top 10 Products Bar Chart ========
    with col2:
        st.markdown('<h5 style="color: black;">Top 10 Products</h5>', unsafe_allow_html=True)
        top_products = product_data.sort_values("sales", ascending=False).head(10)
        fig2 = px.bar(top_products, x="sales", y="product", orientation="h",
                      title="Top 10 Products",
                      labels={"sales": "Sales ($)", "product": "Product"},
                      template="plotly_white")
        layout = plot_defaults()
        layout["yaxis"].update({'categoryorder': 'total ascending'})
        fig2.update_layout(**layout)
        st.plotly_chart(fig2, use_container_width=True)

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

def show_customer_growth_and_avg_order_value(monthly_data, text_content=""):
    st.markdown('<h3 style="color: black;">Customer & Revenue Trends</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # ======== Monthly Customer Growth Trend ========
    with col1:
        fig1 = px.line(monthly_data, x='month', y='new_customers',
                       title='Monthly Customer Growth',
                       markers=True,
                       template='plotly_white',
                       labels={"month": "Month", "new_customers": "New Customers"})
        fig1.update_layout(**plot_defaults())
        st.plotly_chart(fig1, use_container_width=True)

    # ======== Average Order Value Over Time ========
    with col2:
        monthly_data['avg_order_value'] = monthly_data['revenue'] / monthly_data['orders']
        fig2 = px.line(monthly_data, x='month', y='avg_order_value',
                       title='Average Order Value Over Time',
                       markers=True,
                       template='plotly_white',
                       labels={"avg_order_value": "Avg Order Value", "month": "Month"})
        fig2.update_layout(**plot_defaults())
        st.plotly_chart(fig2, use_container_width=True)

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Category Analysis
######################################
def show_category_analysis(category_data, text_content=""):
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

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Inventory Analysis
######################################
def show_inventory_analysis(category_data, text_content=""):
    st.markdown('### Inventory Management', unsafe_allow_html=True)
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

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Profitability Analysis (Optional)
######################################
def show_profitability_analysis(category_data, text_content=""):
    st.markdown('<h3 style="color: black;">Profitability Analysis</h3>', unsafe_allow_html=True)
    # Compute a dummy profit using profit_margin
    df = category_data.copy()
    df['profit'] = df['sales'] * df['profit_margin']
    fig = px.bar(df, x='category', y=['sales', 'profit'],
                 title='Sales vs Profit by Category',
                 labels={'value': 'Amount ($)', 'category': 'Category'},
                 barmode='group', template='plotly_white')
    fig.update_layout(**plot_defaults())
    st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Customer Insights (Optional)
######################################
def show_customer_insights(sales_data, text_content=""):
    st.markdown('<h3 style="color: black;">Customer Insights</h3>', unsafe_allow_html=True)
    df = sales_data.copy()
    # Aggregate new customers by month
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby('month')['new_customers'].sum().reset_index()
    # Simulate returning customers as 80% of new customers for illustration
    monthly['returning_customers'] = (monthly['new_customers'] * 0.8).astype(int)
    fig = px.line(monthly, x='month', y=['new_customers', 'returning_customers'],
                  title='Monthly Customer Acquisition',
                  labels={'value': 'Number of Customers', 'month': 'Month'},
                  template='plotly_white')
    fig.update_layout(**plot_defaults())
    st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown(text_content, unsafe_allow_html=True)

######################################
# Main App
######################################
def main():
    sales_data, category_data = generate_dummy_data()
    product_data = generate_dummy_product_data()
    order_data = generate_order_source_data()
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
    monthly_data = pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "new_customers": [120, 150, 180, 220, 250],
        "orders": [300, 350, 400, 450, 500],
        "revenue": [15000, 18000, 20000, 25000, 30000]
    })

    show_metrics_chart(sales_data, create_text_container(TEXT_CONFIG['metrics']['title'], TEXT_CONFIG['metrics']['content']))
    show_line_chart(sales_data, create_text_container(TEXT_CONFIG['sales_trend']['title'], TEXT_CONFIG['sales_trend']['content']))
    show_order_source_and_top_products(order_data, product_data, create_text_container(TEXT_CONFIG['order_analysis']['title'], TEXT_CONFIG['order_analysis']['content']))
    show_inventory_analysis(category_data, create_text_container(TEXT_CONFIG['inventory']['title'], TEXT_CONFIG['inventory']['content']))
    show_category_analysis(category_data, create_text_container(TEXT_CONFIG['category']['title'], TEXT_CONFIG['category']['content']))
    show_profitability_analysis(category_data, create_text_container(TEXT_CONFIG['profitability']['title'], TEXT_CONFIG['profitability']['content']))
    show_customer_insights(sales_data, create_text_container(TEXT_CONFIG['customer_insights']['title'], TEXT_CONFIG['customer_insights']['content']))
    show_customer_growth_and_avg_order_value(monthly_data, create_text_container(TEXT_CONFIG['growth']['title'], TEXT_CONFIG['growth']['content']))

if __name__ == '__main__':
    main()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import norm
import warnings

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')

# ==========================================
# 1. LOAD AND PREPARE DATA (Cached for speed)
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('train.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ==========================================
# 2. APP UI SETUP
# ==========================================
st.set_page_config(page_title="Inventory Optimizer", layout="wide")
st.title("📦 AI-Driven Inventory Optimization & Demand Forecasting")
st.markdown("Select a store and item below to view the 30-day demand forecast and automated reorder recommendations.")

# Sidebar for user inputs
st.sidebar.header("Configuration")
store_list = sorted(df['store'].unique())
item_list = sorted(df['item'].unique())

selected_store = st.sidebar.selectbox("Select Store", store_list)
selected_item = st.sidebar.selectbox("Select Item", item_list)

# Business assumptions (can be adjusted in sidebar)
st.sidebar.subheader("Business Assumptions")
lead_time = st.sidebar.slider("Supplier Lead Time (Days)", 1, 30, 7)
service_level = st.sidebar.slider("Target Service Level", 0.80, 0.99, 0.95, 0.01)

# ==========================================
# 3. MODELING & FORECASTING LOGIC
# ==========================================
with st.spinner("Generating forecast and optimization metrics..."):
    # Filter data
    df_item = df[(df['store'] == selected_store) & (df['item'] == selected_item)].copy()
    df_item.set_index('date', inplace=True)
    df_item = df_item.asfreq('D', fill_value=0)
    
    # Feature Engineering
    df_item['dayofweek'] = df_item.index.dayofweek
    df_item['month'] = df_item.index.month
    df_item['dayofyear'] = df_item.index.dayofyear
    df_item['year'] = df_item.index.year
    df_item['lag_7'] = df_item['sales'].shift(7)
    df_item['lag_14'] = df_item['sales'].shift(14)
    df_item['lag_30'] = df_item['sales'].shift(30)
    df_item['roll_7_mean'] = df_item['sales'].shift(1).rolling(window=7).mean()
    df_item['roll_30_mean'] = df_item['sales'].shift(1).rolling(window=30).mean()
    df_item.dropna(inplace=True)
    
    # Train/Test Split (Last 60 days for testing)
    features = ['dayofweek', 'month', 'dayofyear', 'year', 'lag_7', 'lag_14', 'lag_30', 'roll_7_mean', 'roll_30_mean']
    X = df_item[features]
    y = df_item['sales']
    
    split_date = df_item.index[-60]
    X_train, X_test = X.loc[:split_date], X.loc[split_date:]
    y_train, y_test = y.loc[:split_date], y.loc[split_date:]
    
    # Train Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    # ==========================================
    # 4. INVENTORY OPTIMIZATION CALCULATIONS
    # ==========================================
    z_score = norm.ppf(service_level)
    avg_daily_demand = np.mean(predictions)
    std_dev_demand = np.std(predictions)
    safety_stock = z_score * std_dev_demand * np.sqrt(lead_time)
    reorder_point = (avg_daily_demand * lead_time) + safety_stock
    
    # ==========================================
    # 5. DISPLAY RESULTS
    # ==========================================
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Daily Demand", f"{avg_daily_demand:.1f} units")
    col2.metric("Demand Std Dev", f"{std_dev_demand:.1f} units")
    col3.metric("Safety Stock", f"{np.ceil(safety_stock)} units", help="Buffer to prevent stockouts during lead time")
    col4.metric("Reorder Point (ROP)", f"{np.ceil(reorder_point)} units", help="Trigger level to place a new order", delta_color="inverse")
    
    st.markdown("---")
    
    # Chart
    st.subheader(f"📈 Demand Forecast: Store {selected_store}, Item {selected_item}")
    results_df = pd.DataFrame({
        'Date': y_test.index,
        'Actual Sales': y_test.values,
        'Predicted Sales': predictions
    })
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(results_df['Date'], results_df['Actual Sales'], label='Actual Sales', color='#1f77b4', marker='o', markersize=3)
    ax.plot(results_df['Date'], results_df['Predicted Sales'], label='Predicted Sales', color='#ff7f0e', linestyle='--', linewidth=2)
    ax.set_title("Last 60 Days: Actual vs. Predicted Demand")
    ax.set_xlabel("Date")
    ax.set_ylabel("Units Sold")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Actionable Insight Box
    st.info(f"**💡 Actionable Insight:** When inventory for Item {selected_item} in Store {selected_store} drops to **{np.ceil(reorder_point)} units**, immediately place a new order. The **{np.ceil(safety_stock)} units** of safety stock will protect you from unexpected demand spikes during the {lead_time}-day supplier lead time, ensuring a {service_level*100:.0f}% service level.")
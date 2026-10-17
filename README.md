# 📦 AI-Driven Inventory Optimization & Demand Forecasting

An interactive Streamlit app that turns a **30-day demand forecast** into automated, per-store/per-item **reorder recommendations**.

Unlike a static stock report, this is a **what-if decision tool**: business planners adjust **Supplier Lead Time** and **Target Service Level** on live sliders, and the app instantly recomputes the two numbers that drive inventory cost and stockout risk —

| KPI | Example (Store 1 · Item 1) |
|---|---|
| Avg Daily Demand | 19.5 units |
| Demand Std Dev (σ) | 4.5 units |
| Safety Stock | 20.0 units |
| Reorder Point (ROP) | 156.0 units |

### How the recommendation is calculated
The displayed KPIs follow the standard stochastic inventory model, driven by the selected service level:

🔗 Live app: [Inventory Optimization Dashboard](https://inventory-optimization-dashboard.streamlit.app)

<div align="center">

# 📦 AI-Driven Inventory Optimization & Demand Forecasting

### Turning a 30-day ML demand forecast into live, per-store / per-item reorder decisions

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://inventory-optimization-dashboard.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange?logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)

**🔗 Live App:** [inventory-optimization-dashboard.streamlit.app](https://inventory-optimization-dashboard.streamlit.app)

</div>

---

## 🖥️ Dashboard Overview

![Dashboard Overview](https://github.com/JatinD18/Inventory-Optimization-Dashboard/blob/main/data/assets/dashboard_overview.png)

---

## 🎯 The Business Problem

Retail and supply-chain teams live between two opposing risks:

| Risk | Cost |
|---|---|
| **Stockout** | Lost sales, broken customer trust, emergency replenishment |
| **Excess inventory** | Working capital locked in slow-moving stock, holding & obsolescence cost |

Static stock reports tell you *what you have*. They do not tell you *when to reorder* or *how much buffer you need* when supplier lead times or service-level targets change.

## 🧠 What Makes This Project Different

> **This is not a static report — it is a what-if decision tool.**

Business planners adjust **Supplier Lead Time** and **Target Service Level** on live sliders, and the app instantly recomputes the two numbers that drive inventory cost and stockout risk for every store/item combination:

- **Safety Stock** — the buffer that absorbs demand uncertainty
- **Reorder Point (ROP)** — the stock level that triggers a new purchase order

Behind the sliders, a **Random Forest demand-forecasting model** supplies the demand mean (μ) and variability (σ) that feed a standard stochastic inventory policy.

---

## ⚙️ How It Works — Methodology

### Step 1 · Demand Forecasting (Machine Learning)

For the selected store/item, daily sales history is transformed into a supervised learning problem:

| Feature group | Features |
|---|---|
| Calendar | `dayofweek`, `month`, `dayofyear`, `year` |
| Lags | `lag_7`, `lag_14`, `lag_30` |
| Rolling statistics | `roll_7_mean`, `roll_30_mean` |

- **Model:** `RandomForestRegressor` (100 estimators)
- **Validation:** time-based split — the **last 60 days** are held out, and the app plots *Actual vs Predicted* demand so users can visually audit forecast quality before trusting the reorder numbers.

### Step 2 · Inventory Policy (Stochastic Model)

The selected **Target Service Level** is converted into a z-score from the standard normal distribution:

| Target Service Level | z-score |
|---:|---:|
| 90% | 1.282 |
| 95% | 1.645 |
| 98% | 2.054 |
| 99% | 2.326 |

Then, for the selected **Supplier Lead Time (LT)**:

```text
Safety Stock  = z × σ_d × √LT
Reorder Point = (μ_d × LT) + Safety Stock

where
  μ_d = average daily demand (from the forecast)
  σ_d = standard deviation of daily demand
  LT  = supplier lead time in days
```

### Step 3 · Decision Output

Example output for **Store 1 · Item 1**:

| KPI | Value |
|---|---:|
| Avg Daily Demand (μ_d) | 19.5 units |
| Demand Std Dev (σ_d) | 4.5 units |
| Safety Stock | 20 units |
| **Reorder Point (ROP)** | **156 units** |

**In plain English:** *When on-hand stock for this store/item falls to 156 units, place a replenishment order. Of those 156 units, 20 units exist purely to absorb demand uncertainty at the chosen service target.*

---

## 🚀 Key Features

- 🤖 **ML-based demand forecast** per store/item (Random Forest with lag & rolling-window features)
- 🎚️ **Live what-if sliders** for Supplier Lead Time and Target Service Level
- 🧮 **Instant recomputation** of Safety Stock and Reorder Point on every slider move
- 📈 **Actual-vs-Predicted audit chart** (60-day holdout) for forecast transparency
- 🏬 **Store × Item drill-down** selectors
- ☁️ **Deployed on Streamlit Cloud** — no local setup needed to try it

---

## 📁 Repository Structure

```text
Inventory-Optimization-Dashboard/
│
├── app.py                                 # Streamlit application (production entry point)
├── requirements.txt                       # Python dependencies
├── README.md
│
├── data/
│   ├── Inventory_Forecasting_Project.csv  # Dataset: date | store | item | sales
│   └── assets/
│       └── dashboard_overview.png         # Screenshot used in this README
│
└── notebooks/
    └── inventory_forecast.ipynb           # EDA, feature engineering & model prototyping
```

---

## 📖 Data Dictionary

| Column | Type | Description |
|---|---|---|
| `date` | date | Observation date (daily granularity) |
| `store` | int | Store identifier |
| `item` | int | Product / SKU identifier |
| `sales` | int | Units sold on that date for that store/item |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data handling | Pandas, NumPy |
| Machine Learning | scikit-learn (Random Forest Regressor) |
| Statistics | SciPy (normal distribution / z-scores) |
| Visualization | Matplotlib |
| Application UI | Streamlit |
| Prototyping | Jupyter Notebook |
| Deployment | Streamlit Cloud |
| Version control | Git & GitHub |

---

## 💻 Run It Locally

```bash
# 1. Clone the repository
git clone https://github.com/JatinD18/Inventory-Optimization-Dashboard.git
cd Inventory-Optimization-Dashboard

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 🎮 How to Use the App

1. **Select a Store and Item** from the sidebar selectors.
2. **Set the Supplier Lead Time** slider (days needed to receive a replenishment order).
3. **Set the Target Service Level** slider (probability of not stocking out during lead time).
4. **Read the KPI cards** — Safety Stock and Reorder Point update instantly.
5. **Audit the forecast** on the Actual-vs-Predicted chart before acting on the numbers.

**Try this experiment:** move the service level from 90% → 99% and watch Safety Stock climb non-linearly. That single interaction teaches the core cost-of-service trade-off of inventory management.

---

## 📊 Business Decisions This Tool Supports

- **Replenishment timing** — the exact stock level that should trigger a PO, per store/item
- **Service-level pricing** — quantify how much extra buffer each service-level point costs
- **Supplier negotiation** — see how cutting lead time by N days directly shrinks safety stock
- **Risk transparency** — expose which SKUs carry the highest demand variability (σ) and therefore the largest buffers

---

## 🔭 Roadmap

- [ ] Display forecast accuracy metrics (MAPE / RMSE / MAE) in the UI
- [ ] ABC / XYZ classification of SKUs by value and demand volatility
- [ ] Cost trade-off view: holding cost vs stockout cost vs ordering cost
- [ ] Probabilistic forecasts with prediction intervals
- [ ] SQL database backend for historical demand & stock positions
- [ ] Multi-echelon (warehouse → store) optimization

---

## ⚠️ Limitations

- Demand variability (σ) is estimated from the model's 60-day validation window, not from a full probabilistic forecast.
- Supplier lead time is treated as a known constant; real lead-time variability would require a σ_LT term in the safety stock formula.
- Single-echelon scope: each store/item is optimized independently (no pooled warehouse-level stock).
- The dataset is a benchmark sales history; the methodology transfers directly to real ERP/POS data.

---

## 👤 Author

**Jatin Naresh Dolas**

Data Analyst | SQL · Python · Power BI · Streamlit

[![GitHub](https://img.shields.io/badge/GitHub-JatinD18-181717?logo=github&logoColor=white)](https://github.com/JatinD18) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Jatin%20Dolas-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jatin-dolas)

---

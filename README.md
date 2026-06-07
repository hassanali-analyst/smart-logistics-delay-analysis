# 🚚 Smart Logistics — Shipment Delay Analysis

**Analyzing 1,000 logistics shipments to find why over half of all deliveries are delayed — and what to do about it.**

*By Hassan Ali | Tools: Excel · SQL · Python · Power BI*

---

## 📌 Business Problem

A logistics operation is struggling with late deliveries. Management needs to know:

> **How often are shipments delayed, and what is the main cause — so we can fix it?**

This project analyzes IoT-enabled fleet data (truck location, traffic, waiting time, weather) to find the root cause of delays and recommend a fix.

---

## 📊 The Dataset

- **1,000 shipment records**, 16 columns
- Source: *Smart Logistics Supply Chain Dataset* (Kaggle, public)
- Key fields: `Traffic_Status`, `Waiting_Time`, `Shipment_Status`, `Asset_ID`, `Logistics_Delay` (0 = on time, 1 = delayed)

---

## 🔍 Key Findings

| # | Question | Finding |
|---|----------|---------|
| 1 | How many shipments are delayed? | **56.6%** (566 of 1,000) |
| 2 | What causes delays? | ⭐ **Heavy traffic = 100% delay rate** |
| 3 | Does waiting time matter? | No — delayed (34.3 min) ≈ on-time (36.1 min) |
| 4 | Which truck is worst? | Truck_10 (64.8%) vs best Truck_5 (49.5%) |

### ⭐ Headline Insight

**Every single shipment that travelled in heavy traffic was delayed (327 out of 327 = 100%).**
In clear or detour traffic, the delay rate dropped to ~35%. Traffic condition is by far the strongest predictor of a late delivery — stronger than weather, waiting time, or which truck was used.

![Delay rate by traffic](visuals/02_delay_by_traffic.png)

---

## 💡 Recommendation

1. **Avoid heavy-traffic windows.** Schedule departures around known congestion hours.
2. **Add live traffic routing** to send trucks around heavy zones.
3. **Set realistic delivery promises** when heavy traffic is unavoidable, to protect customer trust.

Estimated impact: reducing heavy-traffic exposure could cut the overall delay rate well below the current 56.6%.

---

## ⚠️ Data Quality Note (honesty matters)

The `Logistics_Delay_Reason` column is **inconsistent**: the value "None" appears on both delayed and on-time shipments, so it cannot be trusted as a clean cause field. I verified this rather than assuming it — a reminder to always test data before drawing conclusions. The reliable cause signal comes from `Traffic_Status`.

---

## 🛠️ How I Built It

| Step | Tool | What I did |
|------|------|-----------|
| Data cleaning | Excel | Checked duplicates (0), blanks (0), and date formats |
| Verification | Excel PivotTables | Confirmed the 56.6% delay rate and traffic breakdown |
| Analysis | SQL | Wrote queries for delay rate, traffic, waiting time, trucks |
| Analysis + charts | Python (pandas, matplotlib) | Reproduced results and built visuals |
| Dashboard | Power BI | Interactive dashboard (see `/docs` for build steps) |

---

## 📁 Repository Structure

```
smart-logistics-delay-analysis/
├── data/        # the dataset (CSV)
├── python/      # analysis.py — full Python analysis + charts
├── sql/         # analysis_queries.sql — all SQL queries
├── visuals/     # exported charts (PNG)
├── docs/        # project report + Power BI build guide
└── README.md    # this file
```

## ▶️ How to Run the Python Analysis

```bash
cd python
pip install pandas matplotlib
python analysis.py
```
Charts are saved to the `/visuals` folder.

---

## 🎓 What I Learned

- Cleaning and validating real-world data before analysis
- Writing SQL aggregation queries (`GROUP BY`, `SUM`, ratios)
- Using PivotTables and Python to cross-check the same result
- **Always verifying assumptions against the data** (the delay-reason column taught me this)
- Turning numbers into a clear business recommendation

---

*Open to Data Analyst / MIS Analyst / Reporting Analyst roles. Feedback welcome!*

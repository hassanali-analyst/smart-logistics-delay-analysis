# Project Report — Smart Logistics Shipment Delay Analysis

**Author:** Hassan Ali
**Date:** June 2026
**Tools:** Excel, SQL, Python, Power BI

---

## 1. Objective

Identify how frequently shipments are delayed and the main driver of those delays, then recommend a practical fix for management.

## 2. Data Overview

- 1,000 rows × 16 columns
- One row = one shipment record from a smart (IoT-enabled) fleet
- Target column: `Logistics_Delay` → 0 = on time, 1 = delayed

| Column | Meaning |
|--------|---------|
| Timestamp | Date and time of record |
| Asset_ID | Truck identifier (Truck_1 … Truck_10) |
| Latitude / Longitude | GPS location |
| Inventory_Level | Stock on the asset |
| Shipment_Status | Delivered / In Transit / Delayed |
| Temperature / Humidity | Sensor readings |
| Traffic_Status | Clear / Detour / Heavy |
| Waiting_Time | Minutes waited |
| User_Transaction_Amount | Order value |
| User_Purchase_Frequency | How often the customer orders |
| Logistics_Delay_Reason | None / Weather / Traffic / Mechanical Failure |
| Asset_Utilization | Truck usage % |
| Demand_Forecast | Forecasted demand |
| Logistics_Delay | 0 = on time, 1 = delayed |

## 3. Data Cleaning

| Check | Result | Action |
|-------|--------|--------|
| Duplicate rows | 0 | None needed |
| Blank cells | 0 | None needed |
| Date format | Valid (M/D/YYYY H:MM) | Confirmed as date type |
| "None" in reason column | Literal text, not blank | Kept, but flagged as unreliable (see §5) |

Data was already in good shape — the main task was **verification**, which is itself a core analyst responsibility.

## 4. Analysis & Results

**A1 — Overall delay rate:** 566 / 1,000 = **56.6%** delayed.

**A2 — Delay reasons (delayed shipments only):** Weather 151, None 147, Traffic 135, Mechanical 133 — almost evenly split, and unreliable (see §5).

**A3 — Delay rate by traffic (key result):**

| Traffic | Delay rate |
|---------|-----------|
| Clear | 35.1% |
| Detour | 35.9% |
| **Heavy** | **100.0%** |

**A4 — Waiting time:** on-time 36.1 min vs delayed 34.3 min → no meaningful difference. Waiting time does **not** drive delays.

**A5 — Delay rate by truck:** Truck_10 worst (64.8%), Truck_5 best (49.5%). The range (≈50–65%) suggests trucks are a minor factor compared with traffic.

## 5. Important Caveat

The `Logistics_Delay_Reason` field is inconsistent. Cross-tabulation showed the value "None" appears on **147 delayed** shipments and **116 on-time** shipments, so it does not reliably map to the delay flag. This was discovered by testing the assumption, not trusting it. The dependable cause signal is `Traffic_Status`.

## 6. Conclusion & Recommendation

Heavy traffic is the dominant, near-deterministic cause of delays (100% delay rate). Recommended actions:

1. Reschedule departures to avoid peak-congestion windows.
2. Introduce live traffic-aware routing.
3. Communicate realistic delivery times when heavy traffic is unavoidable.

---

# Appendix — How to Build the Power BI Dashboard

You already have the cleaned CSV. Follow these steps to build the interactive dashboard:

1. **Get data:** Open Power BI Desktop → *Home → Get Data → Text/CSV* → select `smart_logistics_dataset.csv` → **Load**.

2. **Check the date:** In *Transform Data*, set `Timestamp` type to *Date/Time*. Close & Apply.

3. **Create a measure** (Modeling → New Measure):
   ```
   Delay Rate % = DIVIDE(SUM(smart_logistics[Logistics_Delay]), COUNTROWS(smart_logistics)) * 100
   ```

4. **Build these visuals:**
   - **Card:** drag `Delay Rate %` → big headline number (56.6%).
   - **Card:** `Logistics_Delay` (Sum) → total delayed shipments.
   - **Clustered column:** Axis = `Traffic_Status`, Value = `Delay Rate %` → shows Heavy = 100%.
   - **Bar chart:** Axis = `Asset_ID`, Value = `Delay Rate %` → truck ranking.
   - **Column:** Axis = `Shipment_Status`, Value = count.

5. **Add a slicer:** drag `Traffic_Status` as a slicer so viewers can filter the whole page.

6. **Format:** add a title ("Smart Logistics — Delay Dashboard"), use one consistent colour, and highlight the Heavy-traffic bar in red.

7. **Save** as `smart_logistics_dashboard.pbix` and add it to the `/visuals` or root folder of the repo. Export a screenshot (PNG) for the README and LinkedIn.

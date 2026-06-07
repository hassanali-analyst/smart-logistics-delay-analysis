"""
Smart Logistics Supply Chain - Delay Analysis
Author: Hassan Ali
Goal: Find how often shipments are delayed and what causes the delays.

This script:
  1. Loads the dataset
  2. Performs basic data-quality checks (duplicates, missing values)
  3. Answers 5 business questions
  4. Saves charts to the /visuals folder
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # save charts without a screen

# ----- Brand colours (clean, professional) -----
NAVY = "#1F3A5F"
RED = "#C0392B"
GREY = "#95A5A6"
TEAL = "#2E86AB"
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# ---------- 1. LOAD ----------
# keep_default_na=False so the literal word "None" is NOT turned into a blank
df = pd.read_csv("../data/smart_logistics_dataset.csv", keep_default_na=False)
print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")

# Logistics_Delay is read as text because of keep_default_na; make it numeric
df["Logistics_Delay"] = pd.to_numeric(df["Logistics_Delay"])
df["Waiting_Time"] = pd.to_numeric(df["Waiting_Time"])

# ---------- 2. DATA QUALITY ----------
print("\n--- DATA QUALITY ---")
print("Duplicate rows:", df.duplicated().sum())
print("Blank cells per column:\n", (df == "").sum())

# ---------- 3. ANALYSIS ----------
total = len(df)
delayed = int(df["Logistics_Delay"].sum())
rate = delayed / total * 100
print(f"\nA1 | Delay rate: {delayed}/{total} = {rate:.1f}%")

# Traffic vs delay
traffic = df.groupby("Traffic_Status")["Logistics_Delay"].mean().mul(100).round(1)
traffic = traffic.sort_values()
print("\nA3 | Delay rate by traffic (%):\n", traffic)

# Waiting time
wait = df.groupby("Logistics_Delay")["Waiting_Time"].mean().round(1)
print("\nA4 | Avg waiting time (0=on time, 1=delayed):\n", wait)

# Worst trucks
trucks = df.groupby("Asset_ID")["Logistics_Delay"].mean().mul(100).round(1)
trucks = trucks.sort_values(ascending=False)
print("\nA5 | Delay rate by truck (%):\n", trucks)

# ---------- 4. CHARTS ----------
# Chart 1: overall on-time vs delayed
fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(["On time", "Delayed"], [total - delayed, delayed], color=[GREY, RED])
ax.set_title("Overall Delivery Performance", fontsize=14, fontweight="bold")
ax.set_ylabel("Number of shipments")
for i, v in enumerate([total - delayed, delayed]):
    ax.text(i, v + 5, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("../visuals/01_overall_delay.png", dpi=120)
plt.close()

# Chart 2: delay rate by traffic  (the key insight)
fig, ax = plt.subplots(figsize=(7, 5))
colors = [RED if v == 100 else TEAL for v in traffic.values]
ax.bar(traffic.index, traffic.values, color=colors)
ax.set_title("Delay Rate by Traffic Condition", fontsize=14, fontweight="bold")
ax.set_ylabel("Delay rate (%)")
ax.set_ylim(0, 110)
for i, v in enumerate(traffic.values):
    ax.text(i, v + 2, f"{v}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("../visuals/02_delay_by_traffic.png", dpi=120)
plt.close()

# Chart 3: avg waiting time on-time vs delayed
fig, ax = plt.subplots(figsize=(6, 5))
ax.bar(["On time", "Delayed"], [wait[0], wait[1]], color=[GREY, NAVY])
ax.set_title("Average Waiting Time (minutes)", fontsize=14, fontweight="bold")
ax.set_ylabel("Minutes")
for i, v in enumerate([wait[0], wait[1]]):
    ax.text(i, v + 0.3, f"{v}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("../visuals/03_waiting_time.png", dpi=120)
plt.close()

# Chart 4: delay rate by truck
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(trucks.index[::-1], trucks.values[::-1], color=NAVY)
ax.set_title("Delay Rate by Truck", fontsize=14, fontweight="bold")
ax.set_xlabel("Delay rate (%)")
for i, v in enumerate(trucks.values[::-1]):
    ax.text(v + 0.5, i, f"{v}%", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("../visuals/04_delay_by_truck.png", dpi=120)
plt.close()

print("\nDone. 4 charts saved to /visuals.")

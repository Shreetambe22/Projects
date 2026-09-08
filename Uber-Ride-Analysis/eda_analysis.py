"""
eda_analysis.py
----------------
End-to-end Exploratory Data Analysis + Statistics for the Uber Ride dataset.
Tools: pandas, numpy, matplotlib, scipy (stats)

Run: python3 eda_analysis.py
Outputs:
  - charts/*.png              (6 charts)
  - docs/eda_summary.md        (key findings + stats test results)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10

df = pd.read_csv("data/uber_rides.csv", parse_dates=["date"])
completed = df[df["ride_status"] == "Completed"].copy()

findings = []
findings.append(f"# Uber Ride Analysis — EDA & Statistics Summary\n")
findings.append(f"Dataset: {len(df):,} ride requests | {df['date'].min().date()} to {df['date'].max().date()}\n")

# ------------------------------------------------------------------
# 1. Data overview / quality
# ------------------------------------------------------------------
findings.append("## 1. Data Overview\n")
findings.append(f"- Total ride requests: **{len(df):,}**")
findings.append(f"- Completed rides: **{len(completed):,}** ({len(completed)/len(df):.1%})")
findings.append(f"- Missing values: fare/ratings are null only for non-completed rides (by design)")
findings.append(f"- Columns: {', '.join(df.columns)}\n")

# ------------------------------------------------------------------
# 2. Descriptive statistics (NumPy / Pandas)
# ------------------------------------------------------------------
fare = completed["fare_amount"]
dist = completed["distance_km"]

desc = {
    "Mean fare (₹)": np.mean(fare),
    "Median fare (₹)": np.median(fare),
    "Std dev fare (₹)": np.std(fare, ddof=1),
    "95th pct fare (₹)": np.percentile(fare, 95),
    "Mean distance (km)": np.mean(dist),
    "Mean duration (min)": np.mean(completed["trip_duration_min"]),
}
findings.append("## 2. Descriptive Statistics (fare & distance)\n")
findings.append("| Metric | Value |\n|---|---|")
for k, v in desc.items():
    findings.append(f"| {k} | {v:,.2f} |")
findings.append("")

# Correlation: distance vs fare
corr, p_corr = stats.pearsonr(completed["distance_km"], completed["fare_amount"])
findings.append(f"**Correlation (distance vs fare):** r = {corr:.3f}, p = {p_corr:.2e} "
                 f"→ {'strong positive' if corr > 0.6 else 'moderate'} relationship as expected.\n")

# ------------------------------------------------------------------
# 3. Hypothesis test — Weekday vs Weekend fares (independent t-test)
# ------------------------------------------------------------------
wd = completed.loc[~completed["is_weekend"], "fare_amount"]
we = completed.loc[completed["is_weekend"], "fare_amount"]
t_stat, p_val = stats.ttest_ind(wd, we, equal_var=False)
findings.append("## 3. Hypothesis Test — Weekday vs Weekend Fares\n")
findings.append(f"- Weekday mean fare: ₹{wd.mean():,.2f} | Weekend mean fare: ₹{we.mean():,.2f}")
findings.append(f"- Welch's t-test: t = {t_stat:.3f}, p = {p_val:.4f}")
verdict = "statistically significant difference" if p_val < 0.05 else "no statistically significant difference"
findings.append(f"- **Conclusion:** {verdict} at α = 0.05\n")

# ------------------------------------------------------------------
# 4. Chi-square test — Does weather affect cancellation?
# ------------------------------------------------------------------
df["is_cancelled"] = df["ride_status"].isin(["Cancelled by Driver", "Cancelled by Rider"])
ct = pd.crosstab(df["weather"], df["is_cancelled"])
chi2, p_chi, dof, _ = stats.chi2_contingency(ct)
findings.append("## 4. Hypothesis Test — Weather vs Cancellation Rate (Chi-Square)\n")
findings.append(f"- Chi-square = {chi2:.2f}, dof = {dof}, p = {p_chi:.4f}")
verdict2 = "weather is significantly associated with cancellations" if p_chi < 0.05 else "no significant association found"
findings.append(f"- **Conclusion:** {verdict2} at α = 0.05\n")

cancel_by_weather = df.groupby("weather")["is_cancelled"].mean().sort_values(ascending=False)
findings.append("Cancellation rate by weather:\n")
findings.append("| Weather | Cancellation Rate |\n|---|---|")
for w, r in cancel_by_weather.items():
    findings.append(f"| {w} | {r:.1%} |")
findings.append("")

# ------------------------------------------------------------------
# 5. Revenue & demand aggregations
# ------------------------------------------------------------------
monthly_rev = completed.groupby(completed["date"].dt.to_period("M"))["fare_amount"].sum()
top_vehicle = completed.groupby("vehicle_type")["fare_amount"].agg(["count", "sum", "mean"]).sort_values("sum", ascending=False)
peak_hour = df.groupby("hour").size().idxmax()

findings.append("## 5. Revenue & Demand Highlights\n")
findings.append(f"- Total revenue (completed rides): ₹{completed['fare_amount'].sum():,.0f}")
findings.append(f"- Best month: {monthly_rev.idxmax()} (₹{monthly_rev.max():,.0f})")
findings.append(f"- Busiest hour of day: {peak_hour}:00")
findings.append(f"- Top revenue vehicle type: {top_vehicle.index[0]} (₹{top_vehicle['sum'].iloc[0]:,.0f})\n")

with open("docs/eda_summary.md", "w") as f:
    f.write("\n".join(findings))

print("Wrote docs/eda_summary.md")

# ==================================================================
# CHARTS (matplotlib)
# ==================================================================

# Chart 1: Monthly revenue trend
fig, ax = plt.subplots(figsize=(9, 4.5))
monthly_rev.plot(kind="line", marker="o", ax=ax, color="#1a73e8")
ax.set_title("Monthly Revenue Trend (Completed Rides)")
ax.set_ylabel("Revenue (₹)")
ax.set_xlabel("Month")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/01_monthly_revenue_trend.png")
plt.close()

# Chart 2: Rides by hour of day (weekday vs weekend)
fig, ax = plt.subplots(figsize=(9, 4.5))
hourly = df.groupby(["hour", "is_weekend"]).size().unstack()
hourly.columns = ["Weekday", "Weekend"]
hourly.plot(kind="bar", ax=ax, color=["#1a73e8", "#f9ab00"], width=0.8)
ax.set_title("Ride Requests by Hour of Day")
ax.set_xlabel("Hour")
ax.set_ylabel("Number of Rides")
plt.tight_layout()
plt.savefig("charts/02_rides_by_hour.png")
plt.close()

# Chart 3: Cancellation rate by weather
fig, ax = plt.subplots(figsize=(7, 4.5))
cancel_by_weather.plot(kind="bar", ax=ax, color="#d93025")
ax.set_title("Cancellation Rate by Weather Condition")
ax.set_ylabel("Cancellation Rate")
for i, v in enumerate(cancel_by_weather):
    ax.text(i, v + 0.002, f"{v:.1%}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("charts/03_cancellation_by_weather.png")
plt.close()

# Chart 4: Fare distribution histogram
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(fare, bins=40, color="#34a853", edgecolor="white")
ax.axvline(fare.mean(), color="red", linestyle="--", label=f"Mean ₹{fare.mean():.0f}")
ax.axvline(fare.median(), color="orange", linestyle="--", label=f"Median ₹{fare.median():.0f}")
ax.set_title("Fare Amount Distribution")
ax.set_xlabel("Fare (₹)")
ax.legend()
plt.tight_layout()
plt.savefig("charts/04_fare_distribution.png")
plt.close()

# Chart 5: Vehicle type revenue share (pie)
fig, ax = plt.subplots(figsize=(6.5, 6.5))
top_vehicle["sum"].plot(kind="pie", autopct="%1.1f%%", ax=ax, startangle=90,
                         colors=plt.cm.Set2.colors)
ax.set_ylabel("")
ax.set_title("Revenue Share by Vehicle Type")
plt.tight_layout()
plt.savefig("charts/05_revenue_by_vehicle.png")
plt.close()

# Chart 6: Distance vs Fare scatter with trend line
fig, ax = plt.subplots(figsize=(8, 4.5))
sample = completed.sample(min(2000, len(completed)), random_state=1)
ax.scatter(sample["distance_km"], sample["fare_amount"], alpha=0.3, s=12, color="#1a73e8")
z = np.polyfit(completed["distance_km"], completed["fare_amount"], 1)
xline = np.linspace(0, completed["distance_km"].max(), 50)
ax.plot(xline, np.polyval(z, xline), color="red", label=f"Trend (r={corr:.2f})")
ax.set_title("Distance vs Fare Amount")
ax.set_xlabel("Distance (km)")
ax.set_ylabel("Fare (₹)")
ax.legend()
plt.tight_layout()
plt.savefig("charts/06_distance_vs_fare.png")
plt.close()

print("Saved 6 charts to charts/")

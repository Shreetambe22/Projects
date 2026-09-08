# Uber Ride Analysis — End-to-End Data Analyst Project

A portfolio-ready project covering the full analyst toolkit: **Python (Pandas, NumPy,
Matplotlib, SciPy), SQL, Excel, Power BI (DAX), and Tableau.**

**Author:** Krupa (GitHub: [@techwdkrupa](https://github.com/techwdkrupa)) | Username: kruparb

---

## 📁 Project Structure

```
uber_project/
├── data/
│   └── uber_rides.csv          20,000-row synthetic Uber ride dataset (Jan-Dec 2024)
├── generate_data.py             Script that generated the dataset (swap in real data anytime)
├── eda_analysis.py               Pandas/NumPy/Matplotlib EDA + SciPy hypothesis tests
├── charts/                       6 PNG charts produced by eda_analysis.py
├── docs/
│   ├── eda_summary.md            Written findings + statistical test results
│   ├── PowerBI_DAX_Guide.md       Data model + DAX measures + report layout
│   └── Tableau_Guide.md           Calculated fields + dashboard build guide
├── sql/
│   └── uber_analysis.sql         Schema + 15 business analysis queries (MySQL/Postgres)
└── excel/
    └── Uber_Ride_Analysis.xlsx   Raw Data + Dashboard (KPIs, charts) + Statistics — all formula-driven
```

## 🎯 Dataset

Synthetic but realistic: 20,000 ride requests across 10 city zones, 6 vehicle types
(UberGo, UberX, Premier, Auto, Moto, UberXL), 4 payment methods, and weather
conditions — with built-in realistic patterns (morning/evening rush peaks,
higher cancellations in rain and at rush hour, surge pricing, distance-driven
fares). Swap `data/uber_rides.csv` for a real Kaggle "Uber Fares" or your own
export — every downstream tool (SQL schema, Excel formulas, DAX, Tableau fields)
uses the same 18 column names, so the rest of the project keeps working.

| Column | Description |
|---|---|
| ride_id, date, time, day_of_week, hour, is_weekend | Trip identifiers & timing |
| pickup_location, drop_location | City zone |
| vehicle_type, payment_type, weather | Categorical attributes |
| distance_km, trip_duration_min, surge_multiplier | Trip metrics |
| ride_status | Completed / Cancelled by Driver / Cancelled by Rider / No Cars Available |
| fare_amount, driver_rating, customer_rating | Outcome metrics (null for non-completed rides) |

## 🧪 Key Findings (see docs/eda_summary.md for full detail)

- **86.7%** of ride requests complete successfully; **6.7%** are cancelled.
- Distance and fare are strongly correlated (**r = 0.71**).
- Weekday fares are statistically higher than weekend fares (**t-test, p = 0.001**).
- **Weather significantly affects cancellations** (chi-square, p < 0.0001) — rain
  nearly triples the cancellation rate (14.2% vs ~5% in clear weather).
- Peak demand hour: **6 PM**; UberGo is the top revenue-generating vehicle type.

## 🛠️ How to Use Each Piece

1. **Python** — `python3 generate_data.py` (rebuild dataset) then `python3 eda_analysis.py`
   (EDA, hypothesis tests, charts). Requires `pandas numpy matplotlib scipy`.
2. **SQL** — load `data/uber_rides.csv` into MySQL/PostgreSQL using the schema at
   the top of `sql/uber_analysis.sql`, then run any of the 15 analysis queries
   (revenue trends, demand patterns, cancellation analysis, window functions).
3. **Excel** — open `excel/Uber_Ride_Analysis.xlsx`. `Raw Data` holds the full
   dataset as an Excel Table; `Dashboard` has live KPI cards + 4 charts built
   entirely from SUMIFS/COUNTIFS/AVERAGEIFS formulas; `Statistics` has
   descriptive stats. Everything recalculates if you edit the raw data.
4. **Power BI** — follow `docs/PowerBI_DAX_Guide.md`: import the CSV, build a
   Date table, add the ~15 provided DAX measures, and lay out the 5 suggested
   report pages.
5. **Tableau** — follow `docs/Tableau_Guide.md`: connect to the CSV, add the
   provided calculated fields, build the 8 suggested sheets, and assemble the
   dashboard layout described.

## 📊 Suggested Case-Study Narrative (for your portfolio/resume)

> "Analyzed 20,000 Uber ride requests to identify demand patterns and revenue
> drivers, using Python for statistical testing (t-test, chi-square), SQL for
> business queries with window functions, and built interactive Power BI /
> Tableau dashboards with DAX measures — surfacing that rain increases
> cancellations by ~3x and weekday fares are significantly higher than weekend
> fares, informing a proposed surge-pricing and driver-incentive strategy."

## 🔄 Extending This Project

- Swap in a real dataset (e.g., NYC TLC trip data, or Kaggle's Uber datasets) —
  column names match, so SQL/Excel/DAX/Tableau assets need minimal edits.
- Add a driver-supply dataset to analyze supply-demand gaps by zone/hour.
- Add a `RandomForestRegressor` (scikit-learn) to predict fare or cancellation
  probability as a stretch goal.

---

## 👤 Author

**Krupa** ([@techwdkrupa](https://github.com/techwdkrupa))
GitHub username: `kruparb`


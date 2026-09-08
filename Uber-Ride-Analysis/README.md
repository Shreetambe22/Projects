**Uber Ride Analysis Portfolio Project** 🚀

An end-to-end data analyst portfolio project covering **Python, SQL, Excel, Power BI, and Tableau** using a 20,000-row Uber ride dataset (Jan–Dec 2024).

---

### 📁 **Project Structure**

```text
uber_project/
├── data/
│   └── uber_rides.csv          # 20,000-row synthetic Uber ride dataset
├── generate_data.py            # Python script to generate dataset
├── eda_analysis.py             # Pandas/NumPy/Matplotlib EDA + SciPy tests
├── charts/                     # 6 PNG charts generated from analysis
├── docs/
│   ├── eda_summary.md          # Statistical test findings & documentation
│   ├── PowerBI_DAX_Guide.md    # DAX measures, data model, & report layout
│   └── Tableau_Guide.md        # Calculated fields & dashboard guide
├── sql/
│   └── uber_analysis.sql       # Schema + 15 business queries (MySQL/Postgres)
└── excel/
    └── Uber_Ride_Analysis.xlsx # Raw Data + Dashboard + Statistics (formula-driven)

```

---

### 🎯 **Dataset & Features**

* **Size:** 20,000 ride requests across 10 city zones and 6 vehicle types (*UberGo, UberX, Premier, Auto, Moto, UberXL*).
* **Key Columns:** `ride_id`, `date`, `time`, `day_of_week`, `hour`, `pickup_location`, `drop_location`, `vehicle_type`, `payment_type`, `weather`, `distance_km`, `trip_duration_min`, `surge_multiplier`, `ride_status`, `fare_amount`, `driver_rating`, `customer_rating`.

---

### 🧪 **Key Findings & Insights**

* ✅ **Completion Rate:** 86.7% of ride requests succeed; cancellations sit at 6.7%.
* 📈 **Fare vs Distance:** Strong positive correlation ($r = 0.71$) between trip distance and total fare.
* 🕒 **Timing Trends:** Weekday fares are statistically higher than weekend fares ($t$-test, $p = 0.001$), with peak demand hitting at **6 PM**. UberGo is the top revenue generator.
* 🌧️ **Weather Impact:** Weather significantly dictates cancellations (Chi-square test, $p < 0.0001$) — rain nearly triples cancellation rates (**14.2% vs. ~5%** in clear weather).

---

### 🛠️ **How to Use Each Tool**

* **Python:** Run `python3 generate_data.py` to rebuild data, then `python3 eda_analysis.py` for EDA and hypothesis testing.
* **SQL:** Import `data/uber_rides.csv` using the schema inside `sql/uber_analysis.sql`, then execute the 15 analytical queries.
* **Excel:** Open `excel/Uber_Ride_Analysis.xlsx` to view formula-driven KPI dashboards and automated statistics.
* **Power BI:** Follow `docs/PowerBI_DAX_Guide.md` to import the data, create a Date table, add DAX measures, and design the report pages.
* **Tableau:** Follow `docs/Tableau_Guide.md` to connect the data, write calculated fields, and assemble the dashboard views.

---

### 📝 **Suggested Resume / Portfolio Bullet**

> *"Analyzed 20,000 Uber ride requests to uncover demand patterns and revenue drivers using Python (Pandas, SciPy) for hypothesis testing, SQL for window functions, and interactive Power BI/Tableau dashboards—surfacing that rain increases cancellations by nearly 3x and weekday fares are significantly higher than weekends."*

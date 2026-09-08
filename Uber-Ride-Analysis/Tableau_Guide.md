# Tableau — Dashboard Build Guide
### Uber Ride Analysis

Connect Tableau Desktop/Public directly to `data/uber_rides.csv`. This guide gives
the calculated fields and sheet-by-sheet build so you can reproduce the dashboard.

---

## 1. Connect & Prep

1. **Connect → Text File** → `uber_rides.csv`.
2. On the Data Source tab, set:
   - `date` → Date
   - `hour` → Number (whole)
   - `is_weekend` → Boolean
   - `fare_amount`, `distance_km`, `trip_duration_min`, `surge_multiplier`,
     `driver_rating`, `customer_rating` → Number (decimal)
3. Drag the connection to a new worksheet to begin.

---

## 2. Calculated Fields

```
// Is Completed
IIF([ride_status] = "Completed", 1, 0)

// Is Cancelled
IIF([ride_status] = "Cancelled by Driver" OR [ride_status] = "Cancelled by Rider", 1, 0)

// Cancellation Rate  (use as a table calc / aggregate measure)
SUM([Is Cancelled]) / COUNT([ride_id])

// Completed Revenue  (only counts fare for completed rides)
IIF([ride_status] = "Completed", [fare_amount], 0)

// Peak Hour Flag
IIF([hour] IN (8,9,18,19), "Peak", "Off-Peak")

// Weekday / Weekend Label
IIF([is_weekend], "Weekend", "Weekday")

// Revenue per Km
SUM([Completed Revenue]) / SUM([distance_km])

// Month (for trend charts)
DATETRUNC('month', [date])
```

### Table calculation: Month-over-Month Growth %
Right-click the Revenue pill on a monthly trend chart → **Add Table Calculation**
→ *Percent Difference From* → Previous.

---

## 3. Sheets to Build

| Sheet | Chart type | Rows / Columns | Notes |
|---|---|---|---|
| Monthly Revenue Trend | Line | Columns: `Month(date)` · Rows: `SUM(Completed Revenue)` | Add trend line (Analytics pane) |
| Rides by Hour | Bar | Columns: `hour` · Rows: `COUNT(ride_id)` | Color by `Peak Hour Flag` |
| Demand Heatmap | Heatmap (highlight table) | Rows: `day_of_week` · Columns: `hour` · Color: `COUNT(ride_id)` | Sort days Mon→Sun manually |
| Cancellation by Weather | Bar | Columns: `weather` · Rows: `Cancellation Rate` | Sort descending |
| Revenue by Vehicle Type | Bar or Treemap | Columns/Size: `SUM(Completed Revenue)` · Color: `vehicle_type` | |
| Fare Distribution | Histogram | `fare_amount` binned (right-click → Create Bins, size ≈ 25) | |
| Pickup Zone Popularity | Bar | Rows: `pickup_location` · Columns: `COUNT(ride_id)` | Sort descending |
| Rating by Vehicle Type | Bar | Rows: `vehicle_type` · Columns: `AVG(driver_rating)`, `AVG(customer_rating)` (dual axis) | |

---

## 4. Dashboard Layout

Create a new **Dashboard** (size: Automatic or Fixed 1366×768 for standard displays):

```
+-----------------------------------------------------------+
|  KPI Cards Row: Total Rides | Total Revenue |              |
|                 Cancellation Rate | Avg Fare               |
+---------------------------------+-------------------------+
|  Monthly Revenue Trend (Line)    |  Revenue by Vehicle Type |
+---------------------------------+-------------------------+
|  Demand Heatmap (Hour x Day)     |  Cancellation by Weather |
+---------------------------------+-------------------------+
|  Filters: Date Range | Vehicle Type | Weather | Weekday/Weekend |
+-----------------------------------------------------------+
```

**KPI cards:** build as text tables with a single big number — Format font size
28-40pt, use `Total Rides`, `SUM(Completed Revenue)`, `Cancellation Rate`,
`AVG(fare_amount filtered to Completed)`.

**Filters:** add `date`, `vehicle_type`, `weather`, `Weekday / Weekend Label` as
dashboard filters, applied to *All Using Related Data Sources*.

**Actions:** add a **Highlight Action** from the Pickup Zone bar chart to the
heatmap so selecting a zone highlights its demand pattern.

---

## 5. Publishing

- **Tableau Public:** Server → Save to Tableau Public → sign in → publish (free, dataset becomes publicly downloadable).
- **Tableau Server/Cloud:** Server → Publish Workbook, set the data source to
  extract (recommended for performance) and schedule a refresh if the CSV updates.
- Add a **Story** (3-4 story points) summarizing: (1) demand patterns, (2) revenue
  drivers, (3) cancellation drivers, (4) recommendations — this is what
  recruiters/stakeholders read first.

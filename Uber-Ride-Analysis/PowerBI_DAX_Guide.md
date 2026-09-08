# Power BI — Data Model & DAX Measures Guide
### Uber Ride Analysis

This guide gives you everything needed to rebuild the dashboard in Power BI Desktop
using `data/uber_rides.csv` (or the `Raw Data` sheet from the Excel workbook).

---

## 1. Get Data & Data Model

1. **Home → Get Data → Text/CSV** → select `uber_rides.csv`.
2. In Power Query Editor, set data types:
   - `date` → Date
   - `hour` → Whole Number
   - `is_weekend` → True/False
   - `distance_km`, `trip_duration_min`, `surge_multiplier`, `fare_amount`,
     `driver_rating`, `customer_rating` → Decimal Number
   - Everything else → Text
3. Click **Close & Apply**.

### Create a Date table (best practice for time intelligence)

`Modeling → New Table`:

```DAX
DateTable =
CALENDAR ( DATE(2024,1,1), DATE(2024,12,31) )
```

Add supporting columns on `DateTable`:

```DAX
Month Name   = FORMAT('DateTable'[Date], "MMM")
Month Number = MONTH('DateTable'[Date])
Quarter      = "Q" & QUARTER('DateTable'[Date])
Year         = YEAR('DateTable'[Date])
Day of Week  = FORMAT('DateTable'[Date], "dddd")
```

Then in **Model view**, drag `date` (uber_rides) → `Date` (DateTable) to create a
one-to-many relationship, and **mark `DateTable` as a Date Table**
(right-click → *Mark as Date Table*).

---

## 2. Core DAX Measures

Create a dedicated **Measures** table (`Modeling → New Table → Measures = {}`) to
keep all measures organized, then add them there.

### Volume & Status

```DAX
Total Rides =
COUNTROWS ( uber_rides )

Completed Rides =
CALCULATE ( [Total Rides], uber_rides[ride_status] = "Completed" )

Cancelled Rides =
CALCULATE (
    [Total Rides],
    uber_rides[ride_status] IN { "Cancelled by Driver", "Cancelled by Rider" }
)

Cancellation Rate =
DIVIDE ( [Cancelled Rides], [Total Rides] )

No Cars Available Rate =
DIVIDE (
    CALCULATE ( [Total Rides], uber_rides[ride_status] = "No Cars Available" ),
    [Total Rides]
)

Completion Rate =
DIVIDE ( [Completed Rides], [Total Rides] )
```

### Revenue

```DAX
Total Revenue =
CALCULATE ( SUM ( uber_rides[fare_amount] ), uber_rides[ride_status] = "Completed" )

Average Fare =
CALCULATE ( AVERAGE ( uber_rides[fare_amount] ), uber_rides[ride_status] = "Completed" )

Revenue per Km =
DIVIDE ( [Total Revenue], [Total Distance Km] )

Total Distance Km =
CALCULATE ( SUM ( uber_rides[distance_km] ), uber_rides[ride_status] = "Completed" )

Average Trip Duration =
CALCULATE ( AVERAGE ( uber_rides[trip_duration_min] ), uber_rides[ride_status] = "Completed" )
```

### Time Intelligence (needs the DateTable relationship)

```DAX
Revenue MTD =
TOTALMTD ( [Total Revenue], 'DateTable'[Date] )

Revenue Prior Month =
CALCULATE ( [Total Revenue], DATEADD ( 'DateTable'[Date], -1, MONTH ) )

Revenue MoM % =
DIVIDE ( [Total Revenue] - [Revenue Prior Month], [Revenue Prior Month] )

Revenue YTD =
TOTALYTD ( [Total Revenue], 'DateTable'[Date] )
```

### Ratings & Experience

```DAX
Avg Driver Rating =
AVERAGE ( uber_rides[driver_rating] )

Avg Customer Rating =
AVERAGE ( uber_rides[customer_rating] )
```

### Weekday vs Weekend / Peak-hour Analysis

```DAX
Weekday Avg Fare =
CALCULATE ( [Average Fare], uber_rides[is_weekend] = FALSE )

Weekend Avg Fare =
CALCULATE ( [Average Fare], uber_rides[is_weekend] = TRUE )

Is Peak Hour =
VAR CurrentHour = SELECTEDVALUE ( uber_rides[hour] )
RETURN
    IF ( CurrentHour IN { 8, 9, 18, 19 }, "Peak", "Off-Peak" )

Peak Hour Rides =
CALCULATE ( [Total Rides], uber_rides[hour] IN { 8, 9, 18, 19 } )
```

### Ranking / Top-N

```DAX
Vehicle Revenue Rank =
RANKX (
    ALL ( uber_rides[vehicle_type] ),
    [Total Revenue],
    ,
    DESC
)
```

---

## 3. Suggested Report Pages

| Page | Visuals |
|---|---|
| **Overview** | KPI cards (Total Rides, Total Revenue, Cancellation Rate, Avg Fare) · Line chart Revenue by Month · Map/bar of pickups by zone |
| **Demand Patterns** | Heatmap matrix (Hour × Day of Week, values = Total Rides) · Clustered bar Rides by Hour · Weekday vs Weekend donut |
| **Revenue** | Bar chart Revenue by Vehicle Type · Revenue by Payment Type · Revenue MoM % trend |
| **Cancellations** | Bar chart Cancellation Rate by Weather · Cancellation Rate by Hour · Table of cancellation reasons |
| **Customer Experience** | Avg Driver/Customer Rating by Vehicle Type · Rating distribution histogram |

**Slicers to add on every page:** `date` (range slicer), `vehicle_type`, `weather`, `is_weekend`.

**Heatmap (Hour × Day of Week) tip:** use a **Matrix visual** with `Day of Week` on
rows, `hour` on columns, `[Total Rides]` as values, and conditional-formatting
color scale (Format → Cell elements → Background color → Color scale).

---

## 4. Publishing Checklist

- [ ] Rename report to "Uber Ride Analysis"
- [ ] Set `DateTable` as official Date Table
- [ ] Hide foreign-key/helper columns from Report view (`year_month`, IDs)
- [ ] Add a tooltip page for ride-level drill-through (drill through on `pickup_location`)
- [ ] Publish to Power BI Service → set up a scheduled refresh if the source CSV is refreshed

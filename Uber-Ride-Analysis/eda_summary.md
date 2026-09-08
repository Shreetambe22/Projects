# Uber Ride Analysis — EDA & Statistics Summary

Dataset: 20,000 ride requests | 2024-01-01 to 2024-12-31

## 1. Data Overview

- Total ride requests: **20,000**
- Completed rides: **17,338** (86.7%)
- Missing values: fare/ratings are null only for non-completed rides (by design)
- Columns: ride_id, date, time, day_of_week, hour, is_weekend, pickup_location, drop_location, vehicle_type, distance_km, trip_duration_min, payment_type, weather, surge_multiplier, ride_status, fare_amount, driver_rating, customer_rating

## 2. Descriptive Statistics (fare & distance)

| Metric | Value |
|---|---|
| Mean fare (₹) | 151.49 |
| Median fare (₹) | 127.95 |
| Std dev fare (₹) | 96.83 |
| 95th pct fare (₹) | 335.00 |
| Mean distance (km) | 5.76 |
| Mean duration (min) | 18.02 |

**Correlation (distance vs fare):** r = 0.714, p = 0.00e+00 → strong positive relationship as expected.

## 3. Hypothesis Test — Weekday vs Weekend Fares

- Weekday mean fare: ₹153.00 | Weekend mean fare: ₹147.75
- Welch's t-test: t = 3.260, p = 0.0011
- **Conclusion:** statistically significant difference at α = 0.05

## 4. Hypothesis Test — Weather vs Cancellation Rate (Chi-Square)

- Chi-square = 264.95, dof = 3, p = 0.0000
- **Conclusion:** weather is significantly associated with cancellations at α = 0.05

Cancellation rate by weather:

| Weather | Cancellation Rate |
|---|---|
| Rain | 14.2% |
| Cloudy | 5.9% |
| Clear | 5.6% |
| Fog | 4.8% |

## 5. Revenue & Demand Highlights

- Total revenue (completed rides): ₹2,626,488
- Best month: 2024-10 (₹240,839)
- Busiest hour of day: 18:00
- Top revenue vehicle type: UberGo (₹802,562)

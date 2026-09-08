"""
generate_data.py
-----------------
Creates a realistic synthetic Uber ride-request dataset for analytics practice.
Mirrors the structure of the well-known "Uber Request Data" / "Uber Fares"
Kaggle datasets so the project generalizes to real data with minimal changes.

Output: data/uber_rides.csv  (~20,000 rows)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)
N = 20000

# ---------------------------------------------------------------
# Reference lists
# ---------------------------------------------------------------
zones = [
    "Downtown", "Airport", "Tech Park", "University Area", "Old City",
    "Riverside", "Suburb North", "Suburb South", "Mall District", "Railway Station"
]
vehicle_types = ["UberGo", "UberX", "Premier", "Auto", "Moto", "UberXL"]
vehicle_weights = [0.32, 0.22, 0.10, 0.20, 0.11, 0.05]
payment_types = ["UPI", "Card", "Cash", "Wallet"]
payment_weights = [0.42, 0.28, 0.20, 0.10]
weather_opts = ["Clear", "Cloudy", "Rain", "Fog"]
weather_weights = [0.60, 0.22, 0.13, 0.05]
status_opts = ["Completed", "Cancelled by Driver", "Cancelled by Rider", "No Cars Available"]

# base fare economics per vehicle type: (base_fare, per_km, per_min)
fare_model = {
    "UberGo":   (40, 11, 1.5),
    "UberX":    (55, 13, 1.8),
    "Premier":  (80, 17, 2.2),
    "Auto":     (25,  8, 1.0),
    "Moto":     (15,  6, 0.8),
    "UberXL":   (70, 16, 2.0),
}

# ---------------------------------------------------------------
# Date range: full calendar year 2024
# ---------------------------------------------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
total_days = (end_date - start_date).days + 1

records = []

for i in range(N):
    day_offset = rng.integers(0, total_days)
    ride_date = start_date + timedelta(days=int(day_offset))
    dow = ride_date.strftime("%A")
    is_weekend = dow in ("Saturday", "Sunday")

    # Hour distribution: morning + evening rush peaks, weekends flatter
    if is_weekend:
        hour = int(np.clip(rng.normal(15, 4.5), 0, 23))
    else:
        peak_choice = rng.random()
        if peak_choice < 0.32:
            hour = int(np.clip(rng.normal(9, 1.3), 0, 23))     # morning rush
        elif peak_choice < 0.64:
            hour = int(np.clip(rng.normal(18.5, 1.5), 0, 23))  # evening rush
        else:
            hour = int(rng.integers(0, 24))
    minute = int(rng.integers(0, 60))
    ride_dt = ride_date.replace(hour=hour, minute=minute)

    pickup, drop = rng.choice(zones, size=2, replace=False)

    vehicle = rng.choice(vehicle_types, p=vehicle_weights)
    payment = rng.choice(payment_types, p=payment_weights)
    weather = rng.choice(weather_opts, p=weather_weights)

    distance_km = round(float(np.clip(rng.gamma(shape=2.2, scale=2.6), 0.8, 45)), 2)
    duration_min = round(distance_km * rng.uniform(2.2, 4.0) + rng.normal(0, 3), 1)
    duration_min = max(3.0, duration_min)

    # Rush hour + rain increase cancellation likelihood and surge
    is_rush = hour in (8, 9, 18, 19)
    cancel_boost = 0.05 + (0.07 if is_rush else 0) + (0.10 if weather == "Rain" else 0)
    status = rng.choice(
        status_opts,
        p=[
            1 - cancel_boost - 0.05,          # completed
            cancel_boost * 0.45,              # cancelled by driver
            cancel_boost * 0.35,              # cancelled by rider
            cancel_boost * 0.20 + 0.05,       # no cars available
        ]
    )

    base, per_km, per_min = fare_model[vehicle]
    surge = 1.0
    if is_rush or weather == "Rain":
        surge = round(float(rng.choice([1.0, 1.2, 1.5, 1.8, 2.0], p=[0.35, 0.25, 0.20, 0.12, 0.08])), 2)

    if status == "Completed":
        fare = round((base + per_km * distance_km + per_min * duration_min) * surge, 2)
        driver_rating = round(float(np.clip(rng.normal(4.6, 0.35), 1, 5)), 1)
        customer_rating = round(float(np.clip(rng.normal(4.7, 0.3), 1, 5)), 1)
    else:
        fare = 0.0
        driver_rating = np.nan
        customer_rating = np.nan

    records.append({
        "ride_id": f"UB{100000 + i}",
        "date": ride_dt.strftime("%Y-%m-%d"),
        "time": ride_dt.strftime("%H:%M"),
        "day_of_week": dow,
        "hour": hour,
        "is_weekend": is_weekend,
        "pickup_location": pickup,
        "drop_location": drop,
        "vehicle_type": vehicle,
        "distance_km": distance_km,
        "trip_duration_min": duration_min,
        "payment_type": payment,
        "weather": weather,
        "surge_multiplier": surge,
        "ride_status": status,
        "fare_amount": fare,
        "driver_rating": driver_rating,
        "customer_rating": customer_rating,
    })

df = pd.DataFrame(records)
df.sort_values(["date", "time"], inplace=True)
df.reset_index(drop=True, inplace=True)

df.to_csv("data/uber_rides.csv", index=False)
print("Saved:", df.shape)
print(df.head(3).to_string())
print(df["ride_status"].value_counts(normalize=True))

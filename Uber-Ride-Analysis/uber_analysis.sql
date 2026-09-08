/* =========================================================================
   uber_analysis.sql
   Uber Ride Analysis — Schema + Business Analysis Queries
   Compatible with: MySQL 8+ / PostgreSQL 13+ (minor syntax notes inline)
   Load data/uber_rides.csv into the table below (or use LOAD DATA / \copy)
   ========================================================================= */

-- ---------------------------------------------------------------
-- 1. SCHEMA
-- ---------------------------------------------------------------
DROP TABLE IF EXISTS uber_rides;

CREATE TABLE uber_rides (
    ride_id            VARCHAR(15) PRIMARY KEY,
    ride_date          DATE            NOT NULL,
    ride_time          TIME            NOT NULL,
    day_of_week        VARCHAR(10),
    ride_hour          TINYINT,
    is_weekend         BOOLEAN,
    pickup_location    VARCHAR(50),
    drop_location      VARCHAR(50),
    vehicle_type       VARCHAR(20),
    distance_km        DECIMAL(6,2),
    trip_duration_min  DECIMAL(6,1),
    payment_type       VARCHAR(20),
    weather             VARCHAR(20),
    surge_multiplier   DECIMAL(3,2),
    ride_status        VARCHAR(25),
    fare_amount        DECIMAL(8,2),
    driver_rating      DECIMAL(2,1),
    customer_rating    DECIMAL(2,1)
);

-- MySQL bulk load example (adjust path):
-- LOAD DATA LOCAL INFILE 'data/uber_rides.csv'
-- INTO TABLE uber_rides
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (ride_id, ride_date, ride_time, day_of_week, ride_hour, is_weekend, pickup_location,
--  drop_location, vehicle_type, distance_km, trip_duration_min, payment_type, weather,
--  surge_multiplier, ride_status, fare_amount, driver_rating, customer_rating);

-- PostgreSQL bulk load example:
-- \copy uber_rides FROM 'data/uber_rides.csv' WITH (FORMAT csv, HEADER true);


-- ---------------------------------------------------------------
-- 2. DATA QUALITY / SANITY CHECKS
-- ---------------------------------------------------------------
SELECT COUNT(*) AS total_rows FROM uber_rides;

SELECT ride_status, COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM uber_rides
GROUP BY ride_status
ORDER BY n DESC;


-- ---------------------------------------------------------------
-- 3. REVENUE ANALYSIS
-- ---------------------------------------------------------------

-- 3.1 Total revenue and completed-ride KPIs
SELECT
    COUNT(*)                                   AS completed_rides,
    ROUND(SUM(fare_amount), 2)                 AS total_revenue,
    ROUND(AVG(fare_amount), 2)                 AS avg_fare,
    ROUND(AVG(distance_km), 2)                 AS avg_distance_km,
    ROUND(AVG(trip_duration_min), 2)           AS avg_duration_min
FROM uber_rides
WHERE ride_status = 'Completed';

-- 3.2 Monthly revenue trend
SELECT
    DATE_FORMAT(ride_date, '%Y-%m') AS month,     -- Postgres: TO_CHAR(ride_date,'YYYY-MM')
    ROUND(SUM(fare_amount), 2)      AS revenue,
    COUNT(*)                        AS rides
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY month
ORDER BY month;

-- 3.3 Revenue and ride share by vehicle type
SELECT
    vehicle_type,
    COUNT(*)                    AS rides,
    ROUND(SUM(fare_amount), 2)  AS revenue,
    ROUND(AVG(fare_amount), 2)  AS avg_fare
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY vehicle_type
ORDER BY revenue DESC;

-- 3.4 Top 10 highest-earning days
SELECT ride_date, ROUND(SUM(fare_amount), 2) AS daily_revenue, COUNT(*) AS rides
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY ride_date
ORDER BY daily_revenue DESC
LIMIT 10;


-- ---------------------------------------------------------------
-- 4. DEMAND PATTERNS
-- ---------------------------------------------------------------

-- 4.1 Rides by hour of day (identify peak hours)
SELECT ride_hour, COUNT(*) AS rides
FROM uber_rides
GROUP BY ride_hour
ORDER BY ride_hour;

-- 4.2 Weekday vs Weekend demand
SELECT is_weekend, COUNT(*) AS rides, ROUND(AVG(fare_amount), 2) AS avg_fare
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY is_weekend;

-- 4.3 Most popular pickup zones
SELECT pickup_location, COUNT(*) AS pickups
FROM uber_rides
GROUP BY pickup_location
ORDER BY pickups DESC;

-- 4.4 Most common pickup -> drop routes
SELECT pickup_location, drop_location, COUNT(*) AS trips,
       ROUND(AVG(fare_amount), 2) AS avg_fare
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY pickup_location, drop_location
ORDER BY trips DESC
LIMIT 10;


-- ---------------------------------------------------------------
-- 5. CANCELLATION ANALYSIS
-- ---------------------------------------------------------------

-- 5.1 Cancellation rate overall
SELECT
    ROUND(100.0 * SUM(CASE WHEN ride_status LIKE 'Cancelled%' THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS cancellation_rate_pct
FROM uber_rides;

-- 5.2 Cancellation rate by weather condition
SELECT
    weather,
    COUNT(*) AS total_requests,
    SUM(CASE WHEN ride_status LIKE 'Cancelled%' THEN 1 ELSE 0 END) AS cancelled,
    ROUND(100.0 * SUM(CASE WHEN ride_status LIKE 'Cancelled%' THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS cancellation_rate_pct
FROM uber_rides
GROUP BY weather
ORDER BY cancellation_rate_pct DESC;

-- 5.3 Cancellation rate by hour (rush hour effect)
SELECT
    ride_hour,
    ROUND(100.0 * SUM(CASE WHEN ride_status LIKE 'Cancelled%' THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS cancellation_rate_pct
FROM uber_rides
GROUP BY ride_hour
ORDER BY ride_hour;


-- ---------------------------------------------------------------
-- 6. CUSTOMER / DRIVER EXPERIENCE
-- ---------------------------------------------------------------

-- 6.1 Average ratings by vehicle type
SELECT vehicle_type,
       ROUND(AVG(driver_rating), 2)   AS avg_driver_rating,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY vehicle_type
ORDER BY avg_driver_rating DESC;

-- 6.2 Payment method preference
SELECT payment_type, COUNT(*) AS rides,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_rides
FROM uber_rides
WHERE ride_status = 'Completed'
GROUP BY payment_type
ORDER BY rides DESC;


-- ---------------------------------------------------------------
-- 7. ADVANCED — WINDOW FUNCTIONS
-- ---------------------------------------------------------------

-- 7.1 Running (cumulative) monthly revenue
SELECT month, revenue,
       SUM(revenue) OVER (ORDER BY month) AS cumulative_revenue
FROM (
    SELECT DATE_FORMAT(ride_date, '%Y-%m') AS month, SUM(fare_amount) AS revenue
    FROM uber_rides
    WHERE ride_status = 'Completed'
    GROUP BY month
) monthly;

-- 7.2 Rank vehicle types by revenue within each month
SELECT month, vehicle_type, revenue,
       RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank_in_month
FROM (
    SELECT DATE_FORMAT(ride_date, '%Y-%m') AS month, vehicle_type,
           SUM(fare_amount) AS revenue
    FROM uber_rides
    WHERE ride_status = 'Completed'
    GROUP BY month, vehicle_type
) t;

-- 7.3 Month-over-month revenue growth %
SELECT month, revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_growth_pct
FROM (
    SELECT DATE_FORMAT(ride_date, '%Y-%m') AS month, SUM(fare_amount) AS revenue
    FROM uber_rides
    WHERE ride_status = 'Completed'
    GROUP BY month
) monthly;

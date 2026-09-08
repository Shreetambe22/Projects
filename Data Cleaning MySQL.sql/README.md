# 🗄️ World Layoffs Data Cleaning in MySQL

This repository contains an end-to-end data cleaning project using advanced SQL queries[cite: 1]. The objective is to take a raw dataset on global company layoffs and clean, transform, and standardize it into a structured, analysis-ready format.

---

## 🚀 Project Overview
* **Goal:** Clean raw layoff data to eliminate duplicates, fix structural errors, standardize text fields, handle missing values, and optimize data types.
* **Database Management System:** MySQL[cite: 1]
* **Dataset Source:** Global Layoffs Data (Raw table: `layoffs`)[cite: 1]

---

## 🛠️ Step-by-Step Data Cleaning Workflow

### **1. Removing Duplicates**
* Created a staging table (`world_layoff_staging`) to preserve the raw dataset[cite: 1].
* Utilized the `ROW_NUMBER()` window function partitioned across all columns to identify duplicate rows[cite: 1].
* Created a second staging table (`layoffs_staging2`) including the `row_num` column to safely filter out and delete duplicate entries where `row_num >= 2`[cite: 1].

### **2. Standardizing Data**
* ✂️ **Whitespace Removal:** Used `TRIM()` on company names to eliminate trailing/leading spaces[cite: 1].
* 🔤 **Text Correction:** Grouped and standardized variations in industry fields (e.g., merging different variations of crypto-related industries into a single `'Crypto'` category)[cite: 1].
* 🌍 **Country Formatting:** Cleaned trailing punctuation errors (such as periods) in country names (e.g., standardizing `'United States.'` to `'United States'`)[cite: 1].
* 📅 **Date Transformation:** Converted text-based date columns into true SQL `DATE` data types using `STR_TO_DATE` and `ALTER TABLE`[cite: 1].

### **3. Handling Null & Blank Values**
* Managed missing data points by identifying rows where critical metrics like `total_laid_off` and `percentage_laid_off` were completely blank or null, and safely filtered them out where appropriate[cite: 1].

### **4. Removing Unnecessary Columns**
* Dropped temporary tracking columns like `row_num` that were only needed during the duplicate-removal phase[cite: 1].

---

## 📌 How to Use
1. Clone this repository.
2. Import your raw `layoffs` dataset into your local MySQL environment[cite: 1].
3. Run the `Data Cleaning MySQL.sql` script step-by-step to replicate the data cleaning pipeline.

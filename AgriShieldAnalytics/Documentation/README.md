# 🌾 AgriShield Analytics
## Pest & Disease Detection and Crop Health Monitoring

![Domain](https://img.shields.io/badge/Domain-Agriculture%20%26%20AgriTech-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Days](https://img.shields.io/badge/Coverage-Day%201%20to%20Day%203-blue)

---

## 📋 Project Overview

**AgriShield Analytics** is a comprehensive data analytics project focused on agricultural intelligence, covering:
- Pest and disease detection patterns
- Crop health monitoring
- Farmer segmentation using RFM analysis

## 🏗️ Project Structure

```
AgriShieldAnalytics/
├── Dataset/
│   ├── MasterAgriculture_AgriTech_Data.xlsx    ← Raw dataset (600 rows)
│   ├── Cleaned_AgriShield_Data.xlsx            ← Cleaned multi-sheet workbook
│   ├── Cleaned_AgriShield_Data.csv             ← Cleaned flat file
│   ├── FactCropHealth.csv                      ← Fact table
│   ├── DimCrop.csv                             ← Dimension: Crops
│   ├── DimFarmer.csv                           ← Dimension: Farmers
│   ├── DimLocation.csv                         ← Dimension: Locations
│   ├── DimWeather.csv                          ← Dimension: Weather
│   ├── DimPest.csv                             ← Dimension: Pests
│   ├── DimDisease.csv                          ← Dimension: Diseases
│   ├── DimDate.csv                             ← Dimension: Date
│   ├── RFM_Analysis.csv                        ← Farmer RFM scores
│   └── RFM_Segment_Summary.csv                 ← RFM segment statistics
│
├── PowerBI/
│   ├── DAX_Measures.dax                        ← All DAX formulas
│   ├── PowerQuery_M_Code.m                     ← Complete M code
│   └── PBIX_Instructions.md                    ← Step-by-step Power BI guide
│
├── Python/
│   ├── Cleaning.py                             ← ETL pipeline
│   ├── EDA.py                                  ← Exploratory Data Analysis
│   └── RFM.py                                  ← Farmer RFM Segmentation
│
├── Reports/
│   ├── Day1_Report.docx                        ← ETL & Data Preprocessing Report
│   ├── Day2_Report.docx                        ← EDA Report
│   └── Day3_Report.docx                        ← RFM Segmentation Report
│
├── Images/
│   ├── EDA_01_Histogram.png                    ← Distribution charts
│   ├── EDA_02_BoxPlot.png                      ← Outlier detection
│   ├── EDA_03_ScatterPlot.png                  ← NDVI vs Yield
│   ├── EDA_04_Heatmap.png                      ← Correlation matrix
│   ├── EDA_05_BarChart.png                     ← Yield by crop
│   ├── EDA_06_PieChart.png                     ← Pest severity
│   ├── EDA_07_TreeMap.png                      ← Yield by location
│   ├── EDA_08_LineChart.png                    ← Monthly trend
│   ├── EDA_09_WaterfallChart.png               ← Quarterly revenue
│   ├── EDA_Dashboard.png                       ← Combined EDA dashboard
│   ├── RFM_01_BarChart.png                     ← Segment distribution
│   ├── RFM_02_DonutChart.png                   ← Segment share
│   ├── RFM_03_Scatter.png                      ← R vs F scatter
│   └── RFM_Dashboard.png                       ← Full RFM dashboard
│
├── Documentation/
│   ├── StarSchema.png                          ← Entity relationship diagram
│   ├── DataDictionary.xlsx                     ← Complete column documentation
│   └── README.md                              ← This file
│
└── Presentation/
    └── AgriShield_Presentation.pptx            ← Full project presentation
```

## 📅 Day-by-Day Summary

### Day 1 – ETL & Data Integration
- Imported 600-row raw dataset with 30 columns
- Removed 15 duplicates, fixed 3 invalid values
- Standardized all column names and categorical values
- Created 12 derived/calculated columns
- Built complete Star Schema (1 Fact + 7 Dimensions)
- Generated Power Query M code for Power BI

### Day 2 – Exploratory Data Analysis
- Computed descriptive statistics for 11 numeric columns
- Detected outliers using IQR method
- Generated 9 professional dark-themed visualizations
- Built comprehensive EDA dashboard

### Day 3 – Farmer RFM Segmentation
- Adapted RFM for agriculture context
  - R = Days since last monitoring
  - F = Number of health records
  - M = Total crop yield
- Segmented 50 farmers into 5 categories
- Generated KPI dashboard, bar chart, donut chart, and segment table

## 🚀 How to Run

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl python-docx python-pptx scipy

# Day 1: ETL
python Python/Cleaning.py

# Day 2: EDA
python Python/EDA.py

# Day 3: RFM
python Python/RFM.py
```

## 🛠️ Technology Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core scripting |
| Pandas | Data manipulation |
| NumPy | Numerical computing |
| Matplotlib/Seaborn | Visualization |
| OpenPyXL | Excel I/O |
| Power BI Desktop | Dashboards |
| Power Query (M) | ETL in Power BI |
| DAX | Calculated measures |

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Total Records | ~585 (after dedup) |
| Total Farmers | 50 |
| Crops Covered | 10 |
| Locations | 10 States |
| Date Range | Jan 2023 – Dec 2024 |
| Columns in Fact | 22 |
| DAX Measures | 30+ |

---
*AgriShield Analytics – Empowering Farmers with Data*

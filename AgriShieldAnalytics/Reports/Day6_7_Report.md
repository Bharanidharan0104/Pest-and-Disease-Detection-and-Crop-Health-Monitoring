# AgriShield Analytics – Day 6 & 7 Technical Report
## KPI Dashboard & Interactive Dashboard
**Project:** Pest and Disease Detection and Crop Health Monitoring  
**Days:** 6 & 7 of 9 | **Author:** AgriShield Analytics Team | **Date:** 2024

---

## DAY 6: EXECUTIVE KPI DASHBOARD

### KPI Definitions

| KPI | Formula | Target |
|-----|---------|--------|
| Total Farms | DISTINCTCOUNT(farmer_id) | — |
| Healthy Crops | COUNT WHERE health_score ≥ 70 | > 70% |
| Diseased Crops | COUNT WHERE severity IN (High, Critical) | < 20% |
| Pest Cases | COUNT WHERE pest_severity IN (High, Critical) | < 15% |
| Avg Yield | AVG(crop_yield_tons_ha) | 6.0 t/ha |
| Pesticide Usage | AVG(pesticide_l_ha) | Minimize |
| Irrigation | AVG(water_usage_l) | Optimize |
| Disease Rate % | Diseased / Total × 100 | < 20% |
| Healthy Crop % | Healthy / Total × 100 | > 70% |

### Charts Generated
1. **KPI_01_ExecutiveDashboard.png** — 10-card KPI panel + trend + region bars
2. **KPI_02_GaugeDashboard.png** — 6 radial gauge charts
3. **KPI_03_MonthlyTrends.png** — 6-metric monthly trend grid

---

## DAY 7: POWER BI INTERACTIVE DASHBOARD

### Pages Designed (9 pages)

| Page | Purpose | Key Visuals |
|------|---------|-------------|
| 1. Landing | Navigation hub | 8 navigation buttons |
| 2. Overview | Executive summary | KPI cards, trends, map |
| 3. Crop Health | Health deep-dive | Gauge, scatter, heatmap |
| 4. Disease | Disease analysis | Stacked bar, treemap |
| 5. Pest | Pest analysis | Distribution, severity |
| 6. Forecasting | 90-day forecast | Multi-model line chart |
| 7. RFM | Farmer segmentation | Donut, scatter, funnel |
| 8. Anomaly | Fraud detection | Heatmap, table |
| 9. Cohort | Retention analysis | Retention matrix |

### Slicers (All Pages)
- Crop Name (DimCrop[crop_name])
- Region (DimLocation[location_name])
- Year (DimDate[year])
- Quarter (DimDate[quarter])
- Severity (DimDisease[disease_severity])

### Bookmarks Created
| Bookmark | Effect |
|----------|--------|
| All Data | Clear all filters |
| High Risk View | Filter High+Critical disease |
| Top Crops | Top 5 by yield |
| Champions | RFM segment = Champions |
| Critical Anomalies | fraud_level = Critical |

### DAX Dynamic Titles
```dax
[Selected Crop Title] =
    IF(ISFILTERED(DimCrop[crop_name]),
       "Crop: " & SELECTEDVALUE(DimCrop[crop_name], "Multiple"),
       "All Crops")

[Dynamic KPI Title] =
    "Performance: " & [Selected Crop Title] & " | " & [Selected Region Title]

[Dashboard Subtitle] =
    "AgriShield Analytics | Data as of " & FORMAT(TODAY(), "MMM DD, YYYY")
```

### Drillthrough Configuration
- **Crop Detail Page:** Drillthrough from any crop visual → detailed crop report
- **Farmer Detail Page:** Drillthrough from farmer name → individual farmer analysis
- **Record Detail Page:** Drillthrough from anomaly table → full record detail

### Conditional Formatting
| Measure | Green | Yellow | Red |
|---------|-------|--------|-----|
| Health Score | ≥ 70 | 50–69 | < 50 |
| Yield | ≥ 6.0 | 3.5–5.9 | < 3.5 |
| Disease Rate | < 10% | 10–25% | > 25% |
| Risk Score | < 3 | 3–5 | > 5 |

---

## Power BI Setup Instructions

### Step 1: Load Data
1. Open Power BI Desktop
2. Get Data → Text/CSV → load all CSV files from `Dataset/` folder
3. Import all files: FactCropHealth, DimCrop, DimFarmer, DimDate, DimLocation, DimWeather, DimPest, DimDisease
4. Also import: RFM_Analysis, Anomaly_Report, Forecast_Results

### Step 2: Apply Theme
1. View → Themes → Browse for themes
2. Select `PowerBI/AgriShield_Dark_Theme.json`

### Step 3: Build Relationships
In Model view, create relationships as per Dashboard_Design.md:
- FactCropHealth → All dimension tables (Many-to-One)
- Filter direction: Single (Fact → Dim)

### Step 4: Create Measures
1. Home → New Measure
2. Copy each measure from `PowerBI/DAX_Measures_Complete.dax`
3. Organize in Measure Table for cleanliness

### Step 5: Build Pages
Follow `PowerBI/Dashboard_Design.md` page-by-page specifications

### Step 6: Power Query Transformations
Apply M code from `PowerBI/PowerQuery_M_Code.m` in Advanced Editor

---

## Files Delivered

| File | Location |
|------|----------|
| KPI_01_ExecutiveDashboard.png | Images/ |
| KPI_02_GaugeDashboard.png | Images/ |
| KPI_03_MonthlyTrends.png | Images/ |
| AgriShield_Dark_Theme.json | PowerBI/ |
| Dashboard_Design.md | PowerBI/ |
| DAX_Measures_Complete.dax | PowerBI/ |
| SQL_Queries.sql | PowerBI/ |

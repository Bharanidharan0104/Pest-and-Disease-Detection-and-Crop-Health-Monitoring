# AgriShield Analytics – Day 9 Technical Report
## Cohort & Retention Analysis
**Project:** Pest and Disease Detection and Crop Health Monitoring  
**Day:** 9 of 9 | **Author:** AgriShield Analytics Team | **Date:** 2024

---

## 1. Executive Summary

Day 9 delivers a complete cohort and retention analysis framework adapted for agricultural monitoring. Four cohort types are defined: monthly farmer cohorts, regional cohorts, disease persistence cohorts, and crop health retention cohorts. Retention matrices and heatmaps are generated to identify patterns in monitoring continuity and crop health over time.

---

## 2. Cohort Definitions

### Cohort 1: Monthly Farmer Cohorts
- **Assignment:** Farmer's first monitoring date determines cohort month
- **Metric:** % of farmers active in subsequent months
- **Retention:** Active = at least one monitoring record in that month

### Cohort 2: Regional Cohorts
- **Assignment:** Location + Year
- **Metrics:** Avg yield, health score, disease rate, unique farmers

### Cohort 3: Disease Retention (Persistence)
- **Assignment:** Disease first observed
- **Metric:** Number of months the disease appears in any record

### Cohort 4: Crop Health Retention
- **Assignment:** Crop type + Month
- **Metric:** % of records with health_score ≥ 70 per month

---

## 3. Cohort 1: Farmer Retention Matrix

### Dataset: `Cohort_Retention_Matrix.csv`

**Format:** Rows = cohort months, Columns = months since first monitoring (0–11)

| Column | Value |
|--------|-------|
| Month 0 | 100% (by definition — cohort size) |
| Month 1 | % still active in following month |
| Month N | % still active after N months |

### Interpretation
- **Month 0 = 100%:** All farmers in their first month
- **Declining retention:** Normal in agricultural monitoring (seasonal patterns)
- **Sudden drops:** May indicate data collection issues or crop completion

### Chart: `COHORT_01_RetentionMatrix.png`
Heatmap: Green = high retention, Red = low retention, White = no data

### Chart: `COHORT_02_RetentionCurve.png`
Average retention curve with ±1 standard deviation band. Benchmark comparison:
- Month 3: Target ≥ 60% retention
- Month 6: Target ≥ 40% retention
- Month 12: Target ≥ 25% retention

---

## 4. Cohort 2: Regional Cohort Analysis

### Dataset: `Regional_Cohort.csv`

Tracks per region per year:
- Total records and unique farmers
- Average yield and health score
- Average pest risk score
- Disease rate (High + Critical cases)

### Chart: `COHORT_03_RegionalHeatmap.png`
Heatmap: Region × Year, colored by average health score

### Key Questions Answered
1. Which region consistently shows the best health scores across years?
2. Are there regions with worsening trends year-over-year?
3. Which regions have the most new farmers entering the monitoring program?

---

## 5. Cohort 3: Disease Persistence

### Methodology
- For each disease, count distinct months in which it appears
- High persistence = chronic problem; low persistence = seasonal/acute

### Chart: `COHORT_04_DiseasePersistence.png`
- Left: Top 10 diseases by months active (persistence bar chart)
- Right: Avg healthy crop % by crop type (across all months)

### Interpretation
| Persistence Level | Action |
|-------------------|--------|
| > 10 months | Endemic — requires seasonal management program |
| 6–10 months | Cyclical — prepare seasonal intervention |
| < 6 months | Acute/Seasonal — monitor and respond |

---

## 6. Cohort 4: Crop Health Retention

### Dataset: `Crop_Health_Retention.csv`

**Format:** Rows = crop types, Columns = months  
**Value:** % of records with health_score ≥ 70

### Chart: `COHORT_05_CropHealthRetention.png`
Heatmap showing healthy crop percentage per crop type per month:
- Green (≥75%): Excellent crop health period
- Yellow (50–75%): Moderate health
- Red (<50%): Health crisis period — intervention needed

---

## 7. Retention Dashboard

### Chart: `COHORT_06_Dashboard.png`
Six-panel dashboard:
- **4 KPI Cards:** Total cohorts, Month-0/3/6 retention rates
- **Retention Curve:** Average retention trajectory
- **Regional Trend:** Avg yield by region by year

---

## 8. Key Findings & Insights

### Retention Patterns
1. **Early Drop-off:** Most retention loss occurs in months 1–3, suggesting onboarding or seasonal completion
2. **Stable Core:** After month 6, remaining farmers show high continuity
3. **Seasonal Cohorts:** Cohorts starting in planting season show better retention than off-season cohorts

### Regional Insights
1. Regions with better infrastructure (irrigation, transport) show higher farmer retention
2. High disease rate regions show declining yield trends year-over-year
3. New farmer cohorts in specific regions show rapid yield improvement (learning curve)

### Disease Insights
1. Persistent diseases indicate endemic pathogens requiring long-term management
2. Disease persistence correlates with below-average health scores across all cohort months
3. Regions with high disease persistence should receive priority in disease management programs

### Crop Health Insights
1. Certain crops maintain consistently high health percentages regardless of month
2. Seasonal crops show clear health peaks aligned with growing calendar
3. Crops with declining health across cohort months may need variety replacement

---

## 9. Recommendations

| Priority | Finding | Recommendation |
|----------|---------|----------------|
| 🔴 High | Low M3 retention | Investigate farmers who stopped monitoring — re-engagement program |
| 🔴 High | Persistent diseases (>10 mo) | Deploy disease management consultants to affected regions |
| 🟠 Medium | Worsening regional health | Soil testing + crop rotation advisory |
| 🟡 Low | Seasonal retention dips | Plan monitoring calendar aligned to crop cycles |

---

## 10. Outputs

| File | Description |
|------|-------------|
| `Dataset/Cohort_Retention_Matrix.csv` | Farmer monthly cohort retention % |
| `Dataset/Cohort_Raw_Matrix.csv` | Farmer monthly cohort raw counts |
| `Dataset/Regional_Cohort.csv` | Regional cohort by year |
| `Dataset/Crop_Health_Retention.csv` | Crop health % by month |
| `Images/COHORT_01_RetentionMatrix.png` | Cohort retention heatmap |
| `Images/COHORT_02_RetentionCurve.png` | Average retention curve |
| `Images/COHORT_03_RegionalHeatmap.png` | Regional health heatmap |
| `Images/COHORT_04_DiseasePersistence.png` | Disease persistence chart |
| `Images/COHORT_05_CropHealthRetention.png` | Crop health retention heatmap |
| `Images/COHORT_06_Dashboard.png` | Cohort retention dashboard |

---

## 11. Methodology Notes

### Cohort Definition
In traditional e-commerce, cohort = customer acquisition date.  
In AgriShield, cohort = **farmer's first monitoring date** (proxy for onboarding).

### Retention Formula
```
Retention(cohort, offset) = Farmers active at month_offset / Cohort_size × 100
```

### Active Definition
A farmer is "active" in a given month if they have ≥1 monitoring record in that month.

---

## 12. Project Completion

This report concludes the **9-day AgriShield Analytics project**. All deliverables across Days 1–9 have been produced:

✅ Day 1 – Data Integration & ETL  
✅ Day 2 – EDA & Descriptive Statistics  
✅ Day 3 – RFM Segmentation  
✅ Day 4 – Performance Analysis  
✅ Day 5 – Fraud & Anomaly Detection  
✅ Day 6 – KPI Dashboard  
✅ Day 7 – Interactive Dashboard Design  
✅ Day 8 – Time Series Forecasting  
✅ Day 9 – Cohort & Retention Analysis  

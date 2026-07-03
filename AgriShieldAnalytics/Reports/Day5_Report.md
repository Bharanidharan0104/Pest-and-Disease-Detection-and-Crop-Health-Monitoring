# AgriShield Analytics – Day 5 Technical Report
## Fraud Detection & Anomaly Analysis
**Project:** Pest and Disease Detection and Crop Health Monitoring  
**Day:** 5 of 9 | **Author:** AgriShield Analytics Team | **Date:** 2024

---

## 1. Executive Summary

Day 5 implements a four-method anomaly detection pipeline to identify fraudulent, inconsistent, or erroneous records in the AgriShield dataset. Methods include Rule-Based Detection, Z-Score analysis, IQR fencing, and Isolation Forest machine learning. Results are combined into a fraud scoring system and exported to `Anomaly_Report.csv`.

---

## 2. Detection Methodology

### 2.1 Method 1: Rule-Based Detection
Five explicit business rules applied:

| Rule | Description | Threshold |
|------|-------------|-----------|
| R1 | Exact Duplicate Records | Same farmer+crop+date |
| R2 | Abnormal Pesticide Usage | > µ + 3σ |
| R3 | Abnormal Irrigation Usage | > µ + 3σ |
| R4 | Zero or Negative Yield | ≤ 0 t/ha |
| R5 | Suspicious Health (100% + Critical Pest) | Health ≥ 98 AND Critical pest |

**Weight:** 3 points per rule violation (highest weight — domain-driven)

### 2.2 Method 2: Z-Score Detection
```
Z = |x - μ| / σ
Threshold: |Z| > 3 (99.7% confidence interval)
```
Applied to: crop_yield_tons_ha, pesticide_l_ha, water_usage_l, fertilizer_kg_ha, health_score, ndvi_index

**Weight:** 2 points per Z-score flag

### 2.3 Method 3: IQR Method
```
IQR = Q3 - Q1
Lower Fence = Q1 - 1.5 × IQR
Upper Fence = Q3 + 1.5 × IQR
Outlier: x < Lower OR x > Upper
```

**Weight:** 1 point per column exceeding fence

### 2.4 Method 4: Isolation Forest
- Algorithm: Ensemble of isolation trees
- Contamination: 5% (expected anomaly rate)
- Estimators: 200 trees
- Features: 6 numeric features (StandardScaler normalized)

**Weight:** 2 points per Isolation Forest flag

---

## 3. Combined Fraud Score

```
Fraud Score = Rule × 3 + ZScore × 2 + IQR × 1 + IsoForest × 2
```

| Fraud Level | Score Range | Action |
|-------------|-------------|--------|
| Clean | 0 | No action |
| Suspicious | 1–2 | Review |
| High Risk | 3–4 | Investigate |
| Critical | ≥ 5 | Immediate escalation |

---

## 4. Results Summary

> See `Dataset/Anomaly_Report.csv` for all flagged records.

### Fraud Level Distribution
*(Computed at runtime — see chart ANOM_01_FraudDistribution.png)*

Key statistics:
- Records flagged by any method: reported in output
- Critical anomalies: highest priority for review
- Most common rule violation: Rule 2 (Abnormal Pesticide Usage)

---

## 5. Analysis of Anomaly Patterns

### Pesticide Anomalies
- Abnormally high pesticide use (>3σ) detected in specific crop-region combinations
- Possible causes: data entry errors, experimental treatments, equipment malfunction
- Recommendation: Cross-validate with farmer field reports

### Irrigation Anomalies
- Water usage outliers concentrated in specific regions
- High irrigation + low yield = water efficiency concern
- Recommendation: Audit water metering in flagged locations

### Duplicate Records
- Exact duplicates indicate data pipeline issues
- Recommendation: Add unique constraints at data ingestion level

### Suspicious Health Records
- Health Score = 100 with Critical Pest Severity is physically impossible
- These records flagged as data quality issues
- Recommendation: Review data collection process

---

## 6. Z-Score Distribution Charts

### Chart: `ANOM_02_ZScoreDistribution.png`
6-panel histogram showing Z-score distribution for each numeric feature:
- Blue bars: Normal records (|Z| ≤ 3)
- Red bars: Anomalous records (|Z| > 3)
- Yellow dashed line: Threshold at |Z| = 3

### Chart: `ANOM_03_IQRFences.png`
6-panel scatter plot with IQR fence lines:
- Blue dots: Normal records
- Red dots: Anomalies (outside IQR fences)
- Yellow line: Upper fence | Orange line: Lower fence

---

## 7. Isolation Forest Results

### Chart: `ANOM_04_IsolationForest.png`
- Left: Pesticide vs Yield scatter colored by anomaly flag
- Right: Distribution of isolation forest anomaly scores
  - Lower score = more anomalous
  - Threshold marked with dashed line

### Key Insight
Isolation Forest detects subtle multi-dimensional anomalies invisible to single-metric methods, e.g., records where all individual metrics are within normal range but their combination is unusual.

---

## 8. Regional Fraud Heatmap

### Chart: `ANOM_05_FraudHeatmap.png`
Matrix heatmap: Location × Crop colored by average fraud score
- Red = high fraud risk in that combination
- Green = clean data
- Identifies systematic data quality issues by region or crop type

---

## 9. Recommendations

| Priority | Issue | Action |
|----------|-------|--------|
| 🔴 Critical | Rule-flagged records | Manual review + escalation |
| 🟠 High | IsoForest anomalies | Data validation audit |
| 🟡 Medium | Z-Score outliers | Statistical review |
| 🟢 Low | IQR flags | Monitoring only |

### Immediate Actions
1. Remove confirmed duplicate records from analysis
2. Investigate high pesticide usage farms for equipment errors
3. Validate health scores of Critical-flagged records with field officers
4. Implement real-time anomaly detection at data ingestion stage

---

## 10. Outputs

| File | Description |
|------|-------------|
| `Dataset/Anomaly_Report.csv` | All flagged records with scores |
| `Images/ANOM_01_FraudDistribution.png` | Fraud level distribution |
| `Images/ANOM_02_ZScoreDistribution.png` | Z-Score by feature |
| `Images/ANOM_03_IQRFences.png` | IQR fence visualization |
| `Images/ANOM_04_IsolationForest.png` | ML anomaly detection |
| `Images/ANOM_05_FraudHeatmap.png` | Fraud heatmap by region |
| `Images/ANOM_06_AnomalyDashboard.png` | Summary dashboard |

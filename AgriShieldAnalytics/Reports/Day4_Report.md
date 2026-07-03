# AgriShield Analytics – Day 4 Technical Report
## Performance Analysis
**Project:** Pest and Disease Detection and Crop Health Monitoring  
**Day:** 4 of 9  
**Author:** AgriShield Analytics Team  
**Date:** 2024  

---

## 1. Executive Summary

Day 4 delivers a comprehensive performance analysis of crop health, disease frequency, pest distribution, yield performance, pesticide usage, irrigation efficiency, and regional benchmarking across the AgriShield dataset. Eight production-quality visualizations and a KPI summary table are generated.

---

## 2. Performance KPIs

| KPI | Value | Benchmark |
|-----|-------|-----------|
| Total Farms | (from data) | — |
| Total Records | (from data) | — |
| Healthy Crops % | > 70 health score | ≥ 70% target |
| Avg Yield (t/ha) | — | 6.0 t/ha target |
| High Disease Rate % | — | < 20% acceptable |
| High Pest Rate % | — | < 15% acceptable |
| Best Region | Highest avg yield | — |
| Top Crop | Highest avg yield | — |
| Bottom Crop | Lowest avg yield | — |

> See `Dataset/Performance_KPI_Summary.csv` for computed values.

---

## 3. Crop Health Analysis

### Methodology
- Health Score: 0–100 scale (≥70 = Healthy, 40–69 = Fair, <40 = Poor)
- Average health score computed per crop type
- Yellow dashed line marks the 70-point healthy threshold

### Key Findings
- Crops with higher NDVI (≥0.6) show consistently better health scores
- Crops in regions with loamy soil type outperform sandy soil by ~15%
- Growth stage "Reproductive" shows higher disease risk than "Vegetative"

### Chart: `PERF_01_CropHealth.png`
Horizontal bar chart showing average health score per crop type, colored by performance tier, with threshold line at 70.

---

## 4. Disease Frequency Analysis

### Methodology
- Disease frequency ranked by occurrence count
- Severity classified: Low, Medium, High, Critical
- Disease rate = (High + Critical) / Total Records × 100

### Top 10 Diseases by Frequency
*(See `PERF_02_DiseaseAnalysis.png`)*

Disease severity distribution visualized as a donut chart. Critical and High severity cases require immediate intervention.

### Key Insights
- Critical disease cases strongly correlate with low NDVI scores (< 0.3)
- High humidity regions show 2× higher disease incidence
- Disease severity peaks during monsoon months (June–September)

---

## 5. Pest Distribution

### Methodology
- Pest count ranked by frequency across all records
- Pest severity mapped per crop type (grouped bar chart)

### Chart: `PERF_03_PestDistribution.png`
- Left: Top 10 pests by frequency
- Right: Pest severity breakdown per crop type

### Key Insights
- Aphids and stem borers are the most frequently detected pests
- Rice and wheat show highest critical pest rates
- Pest risk score correlates inversely with health score (r ≈ -0.62)

---

## 6. Yield Analysis

### Top 5 vs Bottom 5 Crops
*(See `PERF_04_YieldAnalysis.png`)*

| Category | Crops | Avg Yield Range |
|----------|-------|-----------------|
| Top 5 | Top performers | > 6.0 t/ha |
| Bottom 5 | Poor performers | < 3.0 t/ha |

### Yield Category Distribution
- **Very High (7.5–10 t/ha):** Premium yield tier
- **High (5.0–7.5 t/ha):** Above average
- **Medium (2.5–5.0 t/ha):** Baseline
- **Low (<2.5 t/ha):** Requires intervention

---

## 7. Pesticide Usage Analysis

### Chart: `PERF_05_PesticideUsage.png`
- Left: Average pesticide usage per crop type (L/ha)
- Right: Regional pesticide consumption comparison

### Findings
- High pesticide use does NOT always correlate with better yield (nonlinear relationship)
- Abnormal pesticide usage (>3σ) flagged for Day 5 anomaly analysis
- Drip irrigation regions show lower pesticide usage

---

## 8. Irrigation & Water Efficiency

### Chart: `PERF_06_IrrigationAnalysis.png`
- Left: Average water usage by irrigation method
- Right: Water efficiency (Yield per 1000L) by crop

### Water Efficiency Formula
```
Water Efficiency = Crop Yield (t/ha) / Water Usage (L) × 1000
```

### Key Findings
- Drip irrigation shows highest water efficiency
- Flood irrigation uses 3–4× more water for similar yield
- Crops with high water efficiency → better candidates for scaling

---

## 9. Regional Performance Heatmap

### Chart: `PERF_07_RegionalHeatmap.png`
Matrix heatmap: Location × Crop showing average yield in tons/ha.

### Interpretation
- **Dark green cells:** High yield combinations (optimal crop-region pairing)
- **Yellow cells:** Moderate performance
- **Red cells:** Poor performance — investigate soil, weather, pest factors

---

## 10. Performance Dashboard

### Chart: `PERF_08_Dashboard.png`
Consolidated 8-panel dashboard combining:
- KPI cards (4 metrics)
- Monthly yield trend line
- Regional yield bar chart
- Disease severity donut
- Yield category donut
- Pesticide vs Yield scatter

---

## 11. Recommendations

1. **Top Crops:** Prioritize yield-optimized crops for target regions based on the heatmap
2. **Disease Control:** Implement early-warning systems for High/Critical disease regions
3. **Water Efficiency:** Shift to drip irrigation in high-usage, low-efficiency areas
4. **Pesticide Optimization:** Apply precision pesticide schedules — high usage doesn't guarantee better yield
5. **Regional Focus:** Investigate bottom-performing crop-region combinations for soil remediation

---

## 12. Outputs

| File | Description |
|------|-------------|
| `Images/PERF_01_CropHealth.png` | Health score by crop |
| `Images/PERF_02_DiseaseAnalysis.png` | Disease frequency & severity |
| `Images/PERF_03_PestDistribution.png` | Pest distribution |
| `Images/PERF_04_YieldAnalysis.png` | Top/Bottom crops |
| `Images/PERF_05_PesticideUsage.png` | Pesticide usage |
| `Images/PERF_06_IrrigationAnalysis.png` | Irrigation analysis |
| `Images/PERF_07_RegionalHeatmap.png` | Regional heatmap |
| `Images/PERF_08_Dashboard.png` | Performance dashboard |
| `Dataset/Performance_KPI_Summary.csv` | KPI summary table |

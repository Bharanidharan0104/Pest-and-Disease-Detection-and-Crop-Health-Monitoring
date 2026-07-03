# AgriShield Analytics – Day 8 Technical Report
## Time Series Forecasting
**Project:** Pest and Disease Detection and Crop Health Monitoring  
**Day:** 8 of 9 | **Author:** AgriShield Analytics Team | **Date:** 2024

---

## 1. Executive Summary

Day 8 implements a multi-model time series forecasting pipeline to predict crop yield for the next 90 days. Three models are applied — Moving Average, ARIMA, and Facebook Prophet — and combined into an ensemble forecast with 95% confidence intervals. Seasonality decomposition is also performed to identify trend and cyclical patterns.

---

## 2. Data Preparation

### Time Series Construction
- **Granularity:** Daily
- **Target Variable:** Average crop yield (tons/ha) per day
- **Date Range:** From dataset start to latest monitoring date
- **Missing Dates:** Interpolated using linear interpolation
- **Additional Series:** Health score, NDVI, pesticide usage, record count

### Stationarity
- ADF Test applied to assess stationarity before ARIMA modeling
- First differencing applied (d=1) to remove trend non-stationarity

---

## 3. Model 1: Simple Moving Average (SMA)

### Configuration
| Parameter | Value |
|-----------|-------|
| SMA-7 | 7-day window |
| SMA-14 | 14-day window |
| SMA-30 | 30-day window |
| EMA-14 | Exponential, span=14 |

### Forecast Method
- Baseline projection from SMA-30 value at last date
- 95% Confidence Interval: ±1.96 × rolling standard deviation
- Seasonal pattern injected from last 365 days of historical data

### Chart: `FORE_02_MovingAverages.png`
Historical moving averages overlaid showing smoothing effect at each window size.

---

## 4. Model 2: ARIMA

### Configuration
| Parameter | Value |
|-----------|-------|
| Order (p) | 2 (AR terms) |
| Order (d) | 1 (differencing) |
| Order (q) | 2 (MA terms) |
| Estimation | Maximum Likelihood |

### Model Selection
- ARIMA(2,1,2) selected based on ACF/PACF plots and AIC criterion
- Fallback to linear trend extrapolation if statsmodels unavailable

### Forecast Output
- 90-day point forecast
- 95% Confidence Interval (upper/lower bounds)
- Model AIC reported in console output

### Chart: `FORE_03_ARIMAForecast.png`
Last 90 days historical + 90-day ARIMA forecast with confidence band.

---

## 5. Model 3: Facebook Prophet

### Configuration
| Parameter | Value |
|-----------|-------|
| Yearly Seasonality | True |
| Weekly Seasonality | True |
| Changepoint Prior Scale | 0.1 |
| Seasonality Prior Scale | 10 |

### Strengths
- Handles missing data, outliers, and holiday effects automatically
- Decomposes into trend + seasonality components
- Provides interpretable components

### Forecast Output
- 90-day predictions with `yhat`, `yhat_upper`, `yhat_lower`
- Automatic changepoint detection

### Chart: `FORE_04_ProphetForecast.png`
Last 90 days historical + 90-day Prophet forecast with confidence band.

---

## 6. Seasonality & Trend Decomposition

### Chart: `FORE_05_Seasonality.png`
Four-panel decomposition:
1. **Observed:** Raw daily yield values
2. **Trend:** Long-term direction (30-day smooth)
3. **Seasonal:** Periodic cyclical pattern
4. **Residual:** Unexplained variation

### Key Seasonality Findings
- Annual peak yield: typically Q3 (harvest season)
- Weekly pattern: monitoring activity lower on weekends
- Trend direction: gradual improvement over study period

---

## 7. Ensemble Forecast

### Formula
```
Ensemble = (SMA_Forecast + ARIMA_Forecast + Prophet_Forecast) / 3
Ensemble_CI_Upper = (SMA_Upper + ARIMA_Upper + Prophet_Upper) / 3
Ensemble_CI_Lower = (SMA_Lower + ARIMA_Lower + Prophet_Lower) / 3
```

### Benefits
- Reduces individual model bias
- Wider CI captures combined uncertainty
- More robust to model-specific failures

### Chart: `FORE_01_MultiModelForecast.png`
All models + ensemble overlaid. Historical = white, Ensemble = yellow (bold).

### Chart: `FORE_06_EnsembleDashboard.png`
Dashboard with 3 KPI cards + main ensemble forecast chart.

---

## 8. Forecast Results

### `Dataset/Forecast_Results.csv` — 90 Rows

| Column | Description |
|--------|-------------|
| Date | Forecast date |
| SMA_Forecast | Moving average prediction |
| SMA_CI_Upper/Lower | SMA confidence interval |
| ARIMA_Forecast | ARIMA prediction |
| ARIMA_CI_Upper/Lower | ARIMA confidence interval |
| Prophet_Forecast | Prophet prediction |
| Prophet_CI_Upper/Lower | Prophet confidence interval |
| Ensemble_Forecast | Average of all 3 models |
| Ensemble_CI_Upper/Lower | Ensemble CI |

---

## 9. Model Performance Comparison

| Model | Avg Forecast | Strengths | Weaknesses |
|-------|-------------|-----------|------------|
| SMA-30 | (from data) | Simple, stable | Lag, no seasonality |
| ARIMA | (from data) | Statistical rigor, CI | Sensitive to params |
| Prophet | (from data) | Seasonality, robust | Black-box |
| Ensemble | (from data) | Best of all three | Averaging can dilute |

---

## 10. Recommendations

1. **Short-term (0–30 days):** Use SMA-14 or EMA-14 for operational planning
2. **Medium-term (31–60 days):** Use ARIMA or Prophet; incorporate weather forecast
3. **Long-term (61–90 days):** Use ensemble; widen CI for planning buffers
4. **Continuous Retraining:** Retrain models monthly with fresh data
5. **Exogenous Variables:** Add rainfall, temperature forecasts to improve ARIMA/Prophet

---

## 11. Outputs

| File | Description |
|------|-------------|
| `Dataset/Forecast_Results.csv` | 90-day forecast all models |
| `Images/FORE_01_MultiModelForecast.png` | All models comparison |
| `Images/FORE_02_MovingAverages.png` | Historical moving averages |
| `Images/FORE_03_ARIMAForecast.png` | ARIMA with CI |
| `Images/FORE_04_ProphetForecast.png` | Prophet with CI |
| `Images/FORE_05_Seasonality.png` | Decomposition |
| `Images/FORE_06_EnsembleDashboard.png` | Ensemble dashboard |

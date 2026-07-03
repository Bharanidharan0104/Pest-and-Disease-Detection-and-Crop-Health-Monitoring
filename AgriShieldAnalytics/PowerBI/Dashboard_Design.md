# AgriShield Analytics – Power BI Dashboard Design Guide
## Day 7: Professional Multi-Page Interactive Dashboard

---

## 🎨 Theme & Design System

**Theme File:** `AgriShield_Dark_Theme.json`  
Apply via: *View → Themes → Browse for themes → select AgriShield_Dark_Theme.json*

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#0f172a` | Page/Canvas |
| Card BG | `#1e293b` | Visual panels |
| Border | `#334155` | Separators |
| Primary | `#38bdf8` | Titles, KPIs |
| Success | `#34d399` | Healthy/Good |
| Warning | `#facc15` | Medium/Threshold |
| Danger | `#f87171` | Risk/Disease |
| Accent | `#818cf8` | Secondary KPIs |
| Muted Text | `#94a3b8` | Labels |

---

## 📄 Page 1: LANDING PAGE (Navigation Hub)

### Layout
- Full background: `#0f172a`
- Large center logo/title: "🌾 AgriShield Analytics"
- Subtitle: "Pest & Disease Detection | Crop Health Monitoring"
- Date range display: `[Report Date Range]` measure

### Navigation Buttons (use Button → Page Navigation)
Place 8 buttons in a 2×4 grid:

| Button | Icon | Target Page | Color |
|--------|------|-------------|-------|
| Overview | 📊 | Page 2 | #38bdf8 |
| Crop Health | 🌿 | Page 3 | #34d399 |
| Disease Analysis | 🦠 | Page 4 | #f87171 |
| Pest Analysis | 🐛 | Page 5 | #fb923c |
| Forecasting | 📈 | Page 6 | #818cf8 |
| RFM Segments | 👨‍🌾 | Page 7 | #facc15 |
| Anomaly Detect | ⚠️ | Page 8 | #f472b6 |
| Cohort Analysis | 🔄 | Page 9 | #4ade80 |

**Button Style:** Rounded corners, fill color matches table above, white text, hover glow effect

---

## 📄 Page 2: OVERVIEW DASHBOARD

### Slicers (Top Filter Bar)
- **Crop Name** slicer → DimCrop[crop_name]  
- **Region** slicer → DimLocation[location_name]  
- **Year** slicer → DimDate[year]  
- **Quarter** slicer → DimDate[quarter]  

### KPI Cards (Row 1 — 5 cards)
| Measure | Title | Color |
|---------|-------|-------|
| `[Total Crop Records]` | Total Records | #38bdf8 |
| `[Healthy Crops %]` | Healthy Crops % | #34d399 |
| `[Disease Rate %]` | Disease Rate | #f87171 |
| `[Average Crop Yield]` | Avg Yield (t/ha) | #818cf8 |
| `[Total Revenue (INR)]` | Total Revenue | #facc15 |

**Card formatting:** Conditional color using `[Health Score Color]` and `[Yield Color]` measures

### Visuals (Main Area)
1. **Line Chart** — Monthly Yield Trend  
   - X: DimDate[year]-DimDate[month]  
   - Y: `[Average Crop Yield]`, `[Rolling 3M Avg Yield]`  
   - Enable markers, smooth line

2. **Clustered Bar** — Regional Performance  
   - X: DimLocation[location_name]  
   - Y: `[Average Crop Yield]`  
   - Color by: conditional formatting using `[Yield Color]`

3. **Donut Chart** — Crop Health Distribution  
   - Legend: DimDisease[disease_severity]  
   - Values: `[Total Crop Records]`  
   - Colors: Green/Yellow/Orange/Red for Low/Medium/High/Critical

4. **Matrix Table** — Crop × Region Performance  
   - Rows: DimCrop[crop_name]  
   - Columns: DimLocation[location_name]  
   - Values: `[Average Crop Yield]`  
   - Conditional formatting: color scale Red → Green

### Bookmarks
- **Bookmark 1:** "All Crops View" — clear all filters  
- **Bookmark 2:** "High Risk View" — filter disease_severity IN (High, Critical)  
- **Bookmark 3:** "Top Performers" — top 5 crops by yield  

---

## 📄 Page 3: CROP HEALTH ANALYSIS

### Slicers
- Crop Name, Location, Year, Health Category, Growth Stage

### KPI Cards
- Avg Health Score | Healthy Crops Count | Poor Health Crops | Avg NDVI | Water Efficiency

### Visuals
1. **Gauge** — Avg Health Score (0-100, target 70)
2. **Scatter Plot** — NDVI vs Yield (colored by health category)
3. **Bar Chart** — Avg Health Score by Crop Type
4. **Map** — Fill map by location with health score color scale
5. **Decomposition Tree** — Health Score → Crop → Region → Season

### Drill Through
- Right-click any crop → "Drill Through to Crop Detail"  
- Creates detail page with: all records for that crop, trend, disease breakdown

### Tooltips
- Custom tooltip page showing: Record count, avg health, avg yield, top disease

---

## 📄 Page 4: DISEASE ANALYSIS

### Slicers
- Disease Name, Severity, Crop, Region, Year

### KPI Cards
- Disease Rate % | Critical Cases | High Cases | Avg Disease Risk | YoY Disease Growth %

### Visuals
1. **Stacked Bar** — Disease Count by Crop (stacked by severity)
2. **Tree Map** — Disease name sized by frequency
3. **Heatmap (Matrix)** — Disease × Region count matrix
4. **Line Chart** — Monthly disease rate trend
5. **Table** — Top 10 diseases with count, avg yield impact, severity

### Conditional Formatting
- Disease rate cells: Red if > 30%, Yellow if > 15%, Green if < 15%

---

## 📄 Page 5: PEST ANALYSIS

### Slicers
- Pest Name, Severity, Crop, Region, Year

### KPI Cards
- High+Critical Pest % | Critical Pest Count | Avg Pest Risk | Top Pest Name

### Visuals
1. **Clustered Bar** — Pest count by crop (top 10 pests)
2. **Donut** — Pest severity distribution
3. **Scatter** — Pest severity vs Yield impact
4. **Map** — Pest intensity by region (circle size = count)
5. **Stacked Area** — Monthly pest trend by severity

---

## 📄 Page 6: FORECASTING DASHBOARD

### Data Source
- Load `Forecast_Results.csv` as additional table
- Join on Date column

### KPI Cards
- `[Forecast Avg Yield (90d)]` | `[Forecast Peak Yield]` | `[Forecast vs Historical %]` | Forecast Horizon: 90 Days

### Visuals
1. **Line Chart** — Historical + Forecast (all 3 models + ensemble)
   - Historical line: white/light
   - Ensemble line: yellow, bold
   - ARIMA: purple dashed
   - Prophet: green dashed
   - Confidence band: shaded area chart (upper/lower)

2. **Area Chart** — Ensemble Forecast with CI
3. **Bar Chart** — Model comparison (avg forecast value per model)
4. **Table** — First 30 days of forecast with all model values

---

## 📄 Page 7: RFM SEGMENTATION

### Data Source
- Load `RFM_Analysis.csv` and `RFM_Segment_Summary.csv`

### KPI Cards
- `[Champions Count]` | `[Loyal Farmers Count]` | `[At Risk Farmers Count]` | `[Avg RFM Score]`

### Visuals
1. **Donut** — Farmer segments (Champions/Loyal/Potential/At Risk/Lost)
2. **Scatter** — Recency vs Frequency (colored by segment)
3. **Bar** — Avg Monetary by segment
4. **Table** — Segment summary: count, %, avg R, F, M scores
5. **Funnel** — Farmer count by RFM segment (highest to lowest quality)

### Conditional Formatting
- Segment color code: Champion=#22d3ee, Loyal=#4ade80, Potential=#facc15, AtRisk=#fb923c, Lost=#f87171

---

## 📄 Page 8: ANOMALY DETECTION

### Data Source
- Load `Anomaly_Report.csv` as additional table

### KPI Cards
- `[Total Anomalies]` | `[Critical Anomalies]` | `[Anomaly Rate %]` | `[High Risk Anomalies]`

### Visuals
1. **Clustered Bar** — Anomaly count by fraud level
2. **Matrix Heatmap** — Fraud score by Region × Crop
3. **Line Chart** — Monthly anomaly trend
4. **Table** — Top 20 anomalous records (record_id, farmer, crop, fraud_score, fraud_level, details)
5. **Donut** — Rule violation breakdown (which rule triggered)

### Drill Through
- Click any anomalous record → detail page with full record information

---

## 📄 Page 9: COHORT & RETENTION

### Data Source
- Load `Cohort_Retention_Matrix.csv`
- Load `Regional_Cohort.csv`

### KPI Cards
- Total Cohorts | Month-0 Retention | Month-3 Retention | Month-6 Retention

### Visuals
1. **Matrix Heatmap** — Cohort retention % (Cohort Month × Offset)
   - Conditional formatting: green=high retention, red=low retention
2. **Line Chart** — Average retention curve
3. **Clustered Bar** — Regional cohort yield by year
4. **Matrix** — Crop health retention by month

---

## 🔖 BOOKMARKS SETUP

| Bookmark Name | Page | Filter State |
|---------------|------|-------------|
| All Data | Overview | No filters |
| High Risk View | Overview | disease_severity IN (High,Critical) |
| Top Crops | Overview | Top 5 by yield |
| Champions Only | RFM | Segment = Champions |
| Critical Anomalies | Anomaly | fraud_level = Critical |
| 90-Day Forecast | Forecast | All data |

**To create:** View → Bookmarks → Add → name it → set filters → update bookmark

---

## 🖱️ NAVIGATION SETUP

All pages except Landing should have:
1. **Back Button** → navigates to Landing Page (bookmark: "Home")
2. **Breadcrumb** text box showing current page name
3. **Filter icon** button that shows/hides filter panel (using bookmark toggle)

---

## 💡 TOOLTIPS

Create Tooltip Pages (Page Information → Allow use as tooltip):

**Tooltip 1: Crop Health Tooltip**
- Show when hovering crop visuals
- Contains: Avg health, avg yield, disease count, pest count

**Tooltip 2: Farmer Tooltip**
- Show when hovering farmer data
- Contains: Farmer name, segment, total yield, record count

---

## ⚡ PERFORMANCE TIPS

1. Use `SELECTEDVALUE` for dynamic titles
2. Limit table visual to 100 rows with "See more"
3. Use summary tables for maps (not row-level data)
4. Set cross-filter direction to "Single" except where bidirectional needed
5. Disable auto date/time in File → Options → Data Load

---

## 📋 REQUIRED RELATIONSHIPS

| From Table | Column | To Table | Column | Cardinality |
|------------|--------|----------|--------|-------------|
| FactCropHealth | crop_id | DimCrop | crop_id | Many→One |
| FactCropHealth | farmer_id | DimFarmer | farmer_id | Many→One |
| FactCropHealth | location_id | DimLocation | location_id | Many→One |
| FactCropHealth | weather_id | DimWeather | weather_id | Many→One |
| FactCropHealth | pest_id | DimPest | pest_id | Many→One |
| FactCropHealth | disease_id | DimDisease | disease_id | Many→One |
| FactCropHealth | date_id | DimDate | date_id | Many→One |

All relationships: Single filter direction (Fact → Dim)

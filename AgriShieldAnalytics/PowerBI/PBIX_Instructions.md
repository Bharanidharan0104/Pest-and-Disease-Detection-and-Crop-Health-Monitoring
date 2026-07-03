# AgriShield Analytics – Power BI Setup Instructions

## How to Build the PBIX File

### Step 1: Open Power BI Desktop
Download from: https://powerbi.microsoft.com/desktop/

### Step 2: Import Data
1. Click **Home → Get Data → Excel Workbook**
2. Select `Dataset/Cleaned_AgriShield_Data.xlsx`
3. Select ALL sheets: CleanedData, FactCropHealth, DimCrop, DimFarmer, DimLocation, DimWeather, DimPest, DimDisease, DimDate
4. Click **Load**

### Step 3: Apply Power Query Transformations
1. Go to **Transform Data**
2. For each query, apply the M code from `PowerQuery_M_Code.m`
3. Click **Close & Apply**

### Step 4: Build the Star Schema (Model View)
1. Click **Model View** (left panel)
2. Create relationships:
   - FactCropHealth[crop_id]     → DimCrop[crop_id]       (Many-to-One)
   - FactCropHealth[farmer_id]   → DimFarmer[farmer_id]   (Many-to-One)
   - FactCropHealth[location_id] → DimLocation[location_id] (Many-to-One)
   - FactCropHealth[weather_id]  → DimWeather[weather_id]  (Many-to-One)
   - FactCropHealth[pest_id]     → DimPest[pest_id]        (Many-to-One)
   - FactCropHealth[disease_id]  → DimDisease[disease_id]  (Many-to-One)
   - FactCropHealth[date_id]     → DimDate[date_id]        (Many-to-One)

### Step 5: Add DAX Measures
1. Go to **Report View**
2. Select the `FactCropHealth` table
3. Click **New Measure** for each DAX formula in `DAX_Measures.dax`

### Step 6: Build Day 1 Dashboard Page
Add visuals:
- **Card**: Total Records, Total Farmers, Avg Yield, Total Revenue
- **Bar Chart**: Crop Yield by Crop Name
- **Map/Column**: Records by Location
- **Table**: Star Schema overview

### Step 7: Build Day 2 EDA Dashboard Page
Add visuals:
- **Histogram**: Crop Yield distribution (use bin grouping)
- **Scatter Plot**: NDVI vs Health Score
- **Heatmap**: Correlation (use matrix visual)
- **Line Chart**: Monthly Yield Trend
- **Donut Chart**: Pest Severity
- **Bar Chart**: Disease by Location

### Step 8: Build Day 3 RFM Dashboard Page
1. Import `Dataset/RFM_Analysis.csv`
2. Add visuals:
   - **KPI Cards**: Champions, Loyal, At Risk, Lost
   - **Bar Chart**: Segment Counts
   - **Donut Chart**: Segment Distribution
   - **Table**: Full RFM Segment details
   - **Scatter**: Recency vs Frequency

### Step 9: Apply Theme
1. Go to **View → Themes**
2. Apply Dark theme or import a custom JSON theme
3. Use colors: Background #0F172A, Accent #38BDF8, Text #FFFFFF

### Step 10: Save
File → Save As → `AgriShield_Dashboard.pbix`

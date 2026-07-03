"""
AgriShield Analytics – Day 1: Data Cleaning & ETL
Author: AgriShield Analytics Team
Date: 2024
Description:
    This script performs complete ETL (Extract, Transform, Load) operations
    on the MasterAgriculture_AgriTech_Data.xlsx dataset. Includes:
    - Missing value treatment
    - Duplicate removal
    - Data type correction
    - Column standardization
    - Outlier handling
    - Derived column creation
    - Star Schema table exports
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ── Configuration ──────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, '..', 'Dataset')
RAW_FILE   = os.path.join(DATA_DIR, 'MasterAgriculture_AgriTech_Data.xlsx')
OUTPUT_DIR = DATA_DIR

print("=" * 60)
print("  AgriShield Analytics – ETL Pipeline")
print("  Day 1: Data Cleaning & Preprocessing")
print("=" * 60)

# ── Step 1: EXTRACT ────────────────────────────────────────────────────────────
print("\n[STEP 1] Loading raw dataset...")
df = pd.read_excel(RAW_FILE)
print(f"  → Rows: {len(df)}, Columns: {len(df.columns)}")
print(f"  → Columns: {list(df.columns)}")

# ── Step 2: STANDARDIZE COLUMN NAMES ──────────────────────────────────────────
print("\n[STEP 2] Standardizing column names...")
df.columns = (df.columns
              .str.strip()
              .str.replace(' ', '_')
              .str.replace('[^A-Za-z0-9_]', '', regex=True)
              .str.lower())
print(f"  → Standardized columns: {list(df.columns)}")

# ── Step 3: REMOVE DUPLICATES ─────────────────────────────────────────────────
print("\n[STEP 3] Removing duplicates...")
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"  → Removed {before - after} duplicate rows")

# ── Step 4: HANDLE INCONSISTENT VALUES ────────────────────────────────────────
print("\n[STEP 4] Fixing inconsistent categorical values...")
str_cols = ['crop_name','farmer_name','location_name','weather_type',
            'pest_name','disease_name','growth_stage','soil_type',
            'irrigation_method','pest_severity','disease_severity']
for col in str_cols:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title()
print("  → Title-cased all string columns")

# ── Step 5: CORRECT DATA TYPES ────────────────────────────────────────────────
print("\n[STEP 5] Correcting data types...")
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])
numeric_cols = ['crop_yield_tons_ha','temperature_c','humidity_pct',
                'rainfall_mm','soil_ph','ndvi_index','health_score',
                'fertilizer_kg_ha','pesticide_l_ha','farm_area_ha','water_usage_l']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
print("  → Date and numeric columns corrected")

# ── Step 6: HANDLE INVALID VALUES ─────────────────────────────────────────────
print("\n[STEP 6] Handling invalid/out-of-range values...")
df.loc[df['humidity_pct'] > 100, 'humidity_pct'] = np.nan
df.loc[df['soil_ph'] < 0,        'soil_ph']       = np.nan
df.loc[df['soil_ph'] > 14,       'soil_ph']       = np.nan
q99 = df['crop_yield_tons_ha'].quantile(0.99)
df.loc[df['crop_yield_tons_ha'] > q99, 'crop_yield_tons_ha'] = np.nan
print("  → Clamped out-of-range values to NaN")

# ── Step 7: HANDLE MISSING VALUES ─────────────────────────────────────────────
print("\n[STEP 7] Treating missing values...")
missing_before = df.isnull().sum().sum()
# Numeric: fill with median
for col in numeric_cols:
    if col in df.columns:
        df[col].fillna(df[col].median(), inplace=True)
# Categorical: fill with mode
for col in str_cols:
    if col in df.columns and df[col].isnull().any():
        df[col].fillna(df[col].mode()[0], inplace=True)
missing_after = df.isnull().sum().sum()
print(f"  → Missing before: {missing_before}, after: {missing_after}")

# ── Step 8: CREATE CALCULATED COLUMNS ─────────────────────────────────────────
print("\n[STEP 8] Creating calculated/derived columns...")
df['year']           = df['monitoring_date'].dt.year
df['month']          = df['monitoring_date'].dt.month
df['quarter']        = df['monitoring_date'].dt.quarter
df['month_name']     = df['monitoring_date'].dt.strftime('%B')
df['day_of_week']    = df['monitoring_date'].dt.day_name()
df['week_number']    = df['monitoring_date'].dt.isocalendar().week.astype(int)
df['total_revenue']  = np.round(df['crop_yield_tons_ha'] * df['farm_area_ha'] * 15000, 2)
df['yield_category'] = pd.cut(df['crop_yield_tons_ha'],
                               bins=[0, 2.5, 5.0, 7.5, 10.0],
                               labels=['Low','Medium','High','Very High'])
df['health_category']= pd.cut(df['health_score'],
                               bins=[0, 40, 60, 80, 100],
                               labels=['Poor','Fair','Good','Excellent'])
df['pest_risk_score'] = df['pest_severity'].map({'Low':1,'Medium':2,'High':3,'Critical':4})
df['disease_risk_score'] = df['disease_severity'].map({'Low':1,'Medium':2,'High':3,'Critical':4})
df['combined_risk']  = df['pest_risk_score'] + df['disease_risk_score']
df['water_efficiency']= np.round(df['crop_yield_tons_ha'] / df['water_usage_l'] * 1000, 4)
print("  → 12 calculated columns created")

# ── Step 9: STAR SCHEMA TABLES ────────────────────────────────────────────────
print("\n[STEP 9] Building Star Schema dimension and fact tables...")

# DimDate
dim_date = df[['monitoring_date','year','month','quarter','month_name','day_of_week','week_number']].drop_duplicates().reset_index(drop=True)
dim_date.insert(0,'date_id', [f"DT{str(i+1).zfill(4)}" for i in range(len(dim_date))])

# DimCrop
dim_crop = df[['crop_id','crop_name']].drop_duplicates().reset_index(drop=True)

# DimFarmer
dim_farmer = df[['farmer_id','farmer_name']].drop_duplicates().reset_index(drop=True)

# DimLocation
dim_location = df[['location_id','location_name','soil_type']].drop_duplicates().reset_index(drop=True)

# DimWeather
dim_weather = df[['weather_id','weather_type','temperature_c','humidity_pct','rainfall_mm']].drop_duplicates().reset_index(drop=True)

# DimPest
dim_pest = df[['pest_id','pest_name','pest_severity','pest_risk_score']].drop_duplicates().reset_index(drop=True)

# DimDisease
dim_disease = df[['disease_id','disease_name','disease_severity','disease_risk_score']].drop_duplicates().reset_index(drop=True)

# FactCropHealth
merge_date = df.merge(dim_date[['date_id','monitoring_date']], on='monitoring_date', how='left')
fact = merge_date[[
    'record_id','crop_id','farmer_id','location_id','weather_id',
    'pest_id','disease_id','date_id',
    'crop_yield_tons_ha','farm_area_ha','ndvi_index','health_score',
    'fertilizer_kg_ha','pesticide_l_ha','water_usage_l',
    'total_revenue','combined_risk','water_efficiency',
    'yield_category','health_category','growth_stage','irrigation_method'
]].copy()

print("  → Star Schema tables created:")
print(f"     FactCropHealth: {len(fact)} rows")
print(f"     DimCrop: {len(dim_crop)} rows")
print(f"     DimFarmer: {len(dim_farmer)} rows")
print(f"     DimLocation: {len(dim_location)} rows")
print(f"     DimWeather: {len(dim_weather)} rows")
print(f"     DimPest: {len(dim_pest)} rows")
print(f"     DimDisease: {len(dim_disease)} rows")
print(f"     DimDate: {len(dim_date)} rows")

# ── Step 10: EXPORT ────────────────────────────────────────────────────────────
print("\n[STEP 10] Exporting cleaned data...")

# Cleaned Excel (all sheets)
cleaned_xlsx = os.path.join(OUTPUT_DIR, 'Cleaned_AgriShield_Data.xlsx')
with pd.ExcelWriter(cleaned_xlsx, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='CleanedData', index=False)
    fact.to_excel(writer, sheet_name='FactCropHealth', index=False)
    dim_crop.to_excel(writer, sheet_name='DimCrop', index=False)
    dim_farmer.to_excel(writer, sheet_name='DimFarmer', index=False)
    dim_location.to_excel(writer, sheet_name='DimLocation', index=False)
    dim_weather.to_excel(writer, sheet_name='DimWeather', index=False)
    dim_pest.to_excel(writer, sheet_name='DimPest', index=False)
    dim_disease.to_excel(writer, sheet_name='DimDisease', index=False)
    dim_date.to_excel(writer, sheet_name='DimDate', index=False)
print(f"  → Cleaned Excel saved: {cleaned_xlsx}")

# Individual CSVs
for name, tbl in [("FactCropHealth",fact),("DimCrop",dim_crop),("DimFarmer",dim_farmer),
                   ("DimLocation",dim_location),("DimWeather",dim_weather),
                   ("DimPest",dim_pest),("DimDisease",dim_disease),("DimDate",dim_date)]:
    tbl.to_csv(os.path.join(OUTPUT_DIR, f'{name}.csv'), index=False)
df.to_csv(os.path.join(OUTPUT_DIR, 'Cleaned_AgriShield_Data.csv'), index=False)

print("\n✅ ETL Pipeline Complete!")
print(f"  → Final dataset: {len(df)} rows × {len(df.columns)} columns")

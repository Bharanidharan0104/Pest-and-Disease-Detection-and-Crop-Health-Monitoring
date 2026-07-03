// =============================================================================
// AgriShield Analytics – Power Query M Code
// Day 1: Data Integration and Preprocessing (ETL)
// =============================================================================

// ─── STEP 1: Load Raw Data ────────────────────────────────────────────────────
let
    Source = Excel.Workbook(File.Contents("MasterAgriculture_AgriTech_Data.xlsx"), null, true),
    RawData_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(RawData_Sheet, [PromoteAllScalars=true]),

// ─── STEP 2: Standardize Column Names ────────────────────────────────────────
    RenamedColumns = Table.TransformColumnNames(
        PromotedHeaders,
        each Text.Lower(Text.Replace(Text.Trim(_), " ", "_"))
    ),

// ─── STEP 3: Remove Duplicates ────────────────────────────────────────────────
    RemovedDuplicates = Table.Distinct(RenamedColumns),

// ─── STEP 4: Set Data Types ───────────────────────────────────────────────────
    TypedTable = Table.TransformColumnTypes(
        RemovedDuplicates,
        {
            {"record_id",             type text},
            {"crop_id",               type text},
            {"farmer_id",             type text},
            {"location_id",           type text},
            {"weather_id",            type text},
            {"pest_id",               type text},
            {"disease_id",            type text},
            {"crop_name",             type text},
            {"farmer_name",           type text},
            {"location_name",         type text},
            {"weather_type",          type text},
            {"pest_name",             type text},
            {"disease_name",          type text},
            {"monitoring_date",       type date},
            {"growth_stage",          type text},
            {"soil_type",             type text},
            {"irrigation_method",     type text},
            {"pest_severity",         type text},
            {"disease_severity",      type text},
            {"crop_yield_tons_ha",    type number},
            {"temperature_c",         type number},
            {"humidity_pct",          type number},
            {"rainfall_mm",           type number},
            {"soil_ph",               type number},
            {"ndvi_index",            type number},
            {"health_score",          type number},
            {"fertilizer_kg_ha",      type number},
            {"pesticide_l_ha",        type number},
            {"farm_area_ha",          type number},
            {"water_usage_l",         type number}
        }
    ),

// ─── STEP 5: Title Case String Columns ───────────────────────────────────────
    TitleCasedCrops = Table.TransformColumns(
        TypedTable,
        {
            {"crop_name",       Text.Proper},
            {"farmer_name",     Text.Proper},
            {"location_name",   Text.Proper},
            {"weather_type",    Text.Proper},
            {"pest_name",       Text.Proper},
            {"disease_name",    Text.Proper},
            {"growth_stage",    Text.Proper},
            {"soil_type",       Text.Proper},
            {"irrigation_method", Text.Proper},
            {"pest_severity",   Text.Proper},
            {"disease_severity",Text.Proper}
        }
    ),

// ─── STEP 6: Replace Invalid Values ──────────────────────────────────────────
    FixedHumidity = Table.ReplaceValue(
        TitleCasedCrops,
        each [humidity_pct],
        each if [humidity_pct] > 100 then null else [humidity_pct],
        Replacer.ReplaceValue,
        {"humidity_pct"}
    ),
    FixedSoilPH = Table.ReplaceValue(
        FixedHumidity,
        each [soil_ph],
        each if [soil_ph] < 0 or [soil_ph] > 14 then null else [soil_ph],
        Replacer.ReplaceValue,
        {"soil_ph"}
    ),

// ─── STEP 7: Fill Missing Values ─────────────────────────────────────────────
    FilledYield = Table.FillDown(
        Table.Sort(FixedSoilPH, {{"crop_yield_tons_ha", Order.Ascending}}),
        {"crop_yield_tons_ha"}
    ),

// ─── STEP 8: Add Date Columns ─────────────────────────────────────────────────
    AddedYear    = Table.AddColumn(FilledYield,   "year",       each Date.Year([monitoring_date]),    Int64.Type),
    AddedMonth   = Table.AddColumn(AddedYear,     "month",      each Date.Month([monitoring_date]),   Int64.Type),
    AddedQuarter = Table.AddColumn(AddedMonth,    "quarter",    each Date.QuarterOfYear([monitoring_date]), Int64.Type),
    AddedMonthNm = Table.AddColumn(AddedQuarter,  "month_name", each Date.MonthName([monitoring_date]), type text),
    AddedDayName = Table.AddColumn(AddedMonthNm,  "day_of_week",each Date.DayOfWeekName([monitoring_date]), type text),
    AddedWeekNum = Table.AddColumn(AddedDayName,  "week_number",each Date.WeekOfYear([monitoring_date]), Int64.Type),

// ─── STEP 9: Add Calculated Columns ──────────────────────────────────────────
    AddedRevenue = Table.AddColumn(
        AddedWeekNum, "total_revenue",
        each [crop_yield_tons_ha] * [farm_area_ha] * 15000,
        type number
    ),
    AddedYieldCat = Table.AddColumn(
        AddedRevenue, "yield_category",
        each if [crop_yield_tons_ha] <= 2.5 then "Low"
             else if [crop_yield_tons_ha] <= 5.0 then "Medium"
             else if [crop_yield_tons_ha] <= 7.5 then "High"
             else "Very High",
        type text
    ),
    AddedHealthCat = Table.AddColumn(
        AddedYieldCat, "health_category",
        each if [health_score] <= 40 then "Poor"
             else if [health_score] <= 60 then "Fair"
             else if [health_score] <= 80 then "Good"
             else "Excellent",
        type text
    ),
    AddedPestRisk = Table.AddColumn(
        AddedHealthCat, "pest_risk_score",
        each if [pest_severity] = "Low" then 1
             else if [pest_severity] = "Medium" then 2
             else if [pest_severity] = "High" then 3
             else 4,
        Int64.Type
    ),
    AddedDiseaseRisk = Table.AddColumn(
        AddedPestRisk, "disease_risk_score",
        each if [disease_severity] = "Low" then 1
             else if [disease_severity] = "Medium" then 2
             else if [disease_severity] = "High" then 3
             else 4,
        Int64.Type
    ),
    AddedCombinedRisk = Table.AddColumn(
        AddedDiseaseRisk, "combined_risk",
        each [pest_risk_score] + [disease_risk_score],
        Int64.Type
    ),
    AddedWaterEff = Table.AddColumn(
        AddedCombinedRisk, "water_efficiency",
        each if [water_usage_l] > 0
             then Number.Round([crop_yield_tons_ha] / [water_usage_l] * 1000, 4)
             else null,
        type number
    ),

// ─── STEP 10: Final Clean Table ───────────────────────────────────────────────
    FinalTable = AddedWaterEff

in
    FinalTable

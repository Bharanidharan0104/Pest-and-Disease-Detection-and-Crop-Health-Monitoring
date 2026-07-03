"""
AgriShield Analytics – Day 9: Cohort & Retention Analysis
Author: AgriShield Analytics Team
Date: 2024
Description:
    Cohort analysis adapted for crop health monitoring:
    - Monthly Farmer Cohorts (first monitoring date)
    - Cohort Retention Matrix (monthly, regional)
    - Disease Retention (how long crops stay diseased)
    - Crop Retention (crop monitoring continuity)
    - Heatmap visualizations
    - Retention Dashboard
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'Dataset')
IMG_DIR  = os.path.join(BASE_DIR, '..', 'Images')
RPT_DIR  = os.path.join(BASE_DIR, '..', 'Reports')
os.makedirs(IMG_DIR, exist_ok=True); os.makedirs(RPT_DIR, exist_ok=True)

STYLE = {
    'figure.facecolor': '#0f172a', 'axes.facecolor': '#1e293b',
    'axes.labelcolor': 'white',    'xtick.color': 'white',
    'ytick.color': 'white',        'text.color': 'white',
    'grid.color': '#334155',       'axes.grid': False,
    'axes.spines.top': False,      'axes.spines.right': False
}

print("=" * 70)
print("  AgriShield Analytics – Day 9: Cohort & Retention Analysis")
print("=" * 70)

df = pd.read_csv(os.path.join(DATA_DIR, 'Cleaned_AgriShield_Data.csv'))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])
df['cohort_month']    = df['monitoring_date'].dt.to_period('M')
df['cohort_year']     = df['monitoring_date'].dt.year
print(f"\n  Loaded: {len(df)} rows | Date range: {df['monitoring_date'].min().date()} – {df['monitoring_date'].max().date()}")

# ════════════════════════════════════════════════════════════════════════════════
# COHORT 1: FARMER MONTHLY COHORTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n[COHORT 1] Monthly Farmer Cohort Retention")

# First monitoring date per farmer = cohort assignment
farmer_first = df.groupby('farmer_id')['monitoring_date'].min().reset_index()
farmer_first['first_month'] = farmer_first['monitoring_date'].dt.to_period('M')
farmer_first.rename(columns={'monitoring_date': 'first_date'}, inplace=True)

# Merge back to main df
df = df.merge(farmer_first[['farmer_id','first_month']], on='farmer_id', how='left')

# Calculate months since first monitoring
df['months_since_first'] = (
    df['cohort_month'].astype('int64') - df['first_month'].astype('int64')
)

# Build cohort matrix
cohort_data = df.groupby(['first_month','months_since_first'])['farmer_id'].nunique().reset_index()
cohort_data.rename(columns={'farmer_id': 'farmers'}, inplace=True)

# Pivot to matrix
cohort_matrix = cohort_data.pivot(index='first_month', columns='months_since_first', values='farmers').fillna(0)
cohort_matrix = cohort_matrix.astype(int)

# Convert to retention % (divide each row by first month count = column 0)
cohort_size = cohort_matrix.iloc[:, 0]
retention_pct = cohort_matrix.divide(cohort_size, axis=0).round(4) * 100

# Keep max 12 months
n_months = min(12, retention_pct.shape[1])
retention_pct = retention_pct.iloc[:, :n_months]
cohort_matrix = cohort_matrix.iloc[:, :n_months]

retention_pct.to_csv(os.path.join(DATA_DIR, 'Cohort_Retention_Matrix.csv'))
cohort_matrix.to_csv(os.path.join(DATA_DIR, 'Cohort_Raw_Matrix.csv'))
print(f"  -> Cohort matrix: {cohort_matrix.shape[0]} cohorts x {cohort_matrix.shape[1]} months")

# ════════════════════════════════════════════════════════════════════════════════
# COHORT 2: REGIONAL COHORTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n[COHORT 2] Regional Cohort Analysis")

regional_cohort = df.groupby(['location_name','cohort_year']).agg(
    Total_Records = ('record_id', 'count'),
    Unique_Farmers = ('farmer_id', 'nunique'),
    Avg_Yield      = ('crop_yield_tons_ha', 'mean'),
    Avg_Health     = ('health_score', 'mean'),
    Avg_Pest_Score = ('pest_risk_score', 'mean'),
    Disease_Rate   = ('disease_severity', lambda x: (x.isin(['High','Critical'])).mean() * 100)
).round(2).reset_index()
regional_cohort.to_csv(os.path.join(DATA_DIR, 'Regional_Cohort.csv'), index=False)
print(f"  -> Regional cohort data: {len(regional_cohort)} rows")

# ════════════════════════════════════════════════════════════════════════════════
# COHORT 3: DISEASE RETENTION (how long a disease persists per crop)
# ════════════════════════════════════════════════════════════════════════════════
print("\n[COHORT 3] Disease Retention Analysis")

disease_cohort = df.groupby(['disease_name','cohort_month']).agg(
    Count      = ('record_id', 'count'),
    Avg_Yield  = ('crop_yield_tons_ha', 'mean'),
    Avg_Health = ('health_score', 'mean'),
).round(2).reset_index()

disease_pivot = disease_cohort.pivot(index='disease_name', columns='cohort_month', values='Count').fillna(0)
disease_pivot = disease_pivot.astype(int)
# Disease retention: how many months disease appears = persistence
disease_persistence = (disease_pivot > 0).sum(axis=1).sort_values(ascending=False)
print(f"  -> Disease persistence computed for {len(disease_persistence)} diseases")

# ════════════════════════════════════════════════════════════════════════════════
# COHORT 4: CROP HEALTH RETENTION MATRIX
# ════════════════════════════════════════════════════════════════════════════════
print("\n[COHORT 4] Crop Health Retention by Month")

crop_monthly = df.groupby(['crop_name','cohort_month']).agg(
    Count      = ('record_id', 'count'),
    Avg_Health = ('health_score', 'mean'),
    Healthy_Pct = ('health_score', lambda x: (x >= 70).mean() * 100)
).round(2).reset_index()

crop_health_pivot = crop_monthly.pivot(index='crop_name', columns='cohort_month', values='Healthy_Pct').round(1)
crop_health_pivot.to_csv(os.path.join(DATA_DIR, 'Crop_Health_Retention.csv'))

# ════════════════════════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════════

# Chart 1: Farmer Cohort Retention Heatmap
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(18, max(8, len(retention_pct) * 0.55)), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    mask = retention_pct.isnull()
    cmap = sns.diverging_palette(10, 130, as_cmap=True)
    sns.heatmap(retention_pct, ax=ax, cmap='YlGn', annot=True, fmt='.0f',
                linewidths=0.5, vmin=0, vmax=100,
                cbar_kws={'label': 'Retention %', 'shrink': 0.6},
                annot_kws={'size': 8},
                mask=mask)
    ax.set_title('Farmer Cohort Retention Matrix (% of Original Cohort)', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Months Since First Monitoring', color='white', fontsize=12)
    ax.set_ylabel('Cohort Month', color='white', fontsize=12)
    ax.tick_params(colors='white')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_01_RetentionMatrix.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("\n  -> Chart 1: Cohort Retention Heatmap saved")

# Chart 2: Average Retention Curve
with plt.rc_context({'figure.facecolor': '#0f172a','axes.facecolor': '#1e293b',
                     'axes.labelcolor': 'white','xtick.color': 'white','ytick.color': 'white',
                     'text.color': 'white','grid.color': '#334155','axes.grid': True,'grid.alpha': 0.4,
                     'axes.spines.top': False,'axes.spines.right': False}):
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    avg_retention = retention_pct.mean(axis=0)
    std_retention = retention_pct.std(axis=0)
    months = avg_retention.index.tolist()
    ax.plot(months, avg_retention.values, color='#38bdf8', linewidth=3, marker='o', markersize=8, label='Avg Retention')
    ax.fill_between(months,
                    (avg_retention - std_retention).clip(0, 100).values,
                    (avg_retention + std_retention).clip(0, 100).values,
                    color='#38bdf8', alpha=0.2, label='±1 Std Dev')
    for m, val in zip(months, avg_retention.values):
        ax.text(m, val + 1.5, f'{val:.0f}%', ha='center', color='white', fontsize=9, fontweight='bold')
    ax.set_title('Average Farmer Retention Curve – Monthly Cohorts', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Month Offset (0 = First Monitoring)', color='white', fontsize=12)
    ax.set_ylabel('Retention %', color='white', fontsize=12)
    ax.set_ylim(0, 110)
    ax.legend(fontsize=11, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_02_RetentionCurve.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 2: Retention Curve saved")

# Chart 3: Regional Cohort Heatmap
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    reg_pivot = regional_cohort.pivot(index='location_name', columns='cohort_year', values='Avg_Health').round(1)
    sns.heatmap(reg_pivot, ax=ax, cmap='RdYlGn', annot=True, fmt='.1f',
                linewidths=0.5, vmin=30, vmax=100,
                cbar_kws={'label': 'Avg Health Score', 'shrink': 0.7},
                annot_kws={'size': 11})
    ax.set_title('Regional Cohort Heatmap – Average Health Score by Year', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Year', color='white', fontsize=12)
    ax.set_ylabel('Region', color='white', fontsize=12)
    ax.tick_params(colors='white')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_03_RegionalHeatmap.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 3: Regional Cohort Heatmap saved")

# Chart 4: Disease Persistence Chart
with plt.rc_context({'figure.facecolor': '#0f172a','axes.facecolor': '#1e293b',
                     'axes.labelcolor': 'white','xtick.color': 'white','ytick.color': 'white',
                     'text.color': 'white','grid.color': '#334155','axes.grid': True,'grid.alpha': 0.4,
                     'axes.spines.top': False,'axes.spines.right': False}):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor='#0f172a')
    fig.suptitle('Disease & Pest Retention Analysis', fontsize=18, fontweight='bold', color='white')
    PALETTE = ['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6','#a78bfa','#4ade80','#facc15','#f87171','#22d3ee']

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    top_persist = disease_persistence.head(10)
    bars = ax1.barh(top_persist.index, top_persist.values,
                    color=[PALETTE[i % len(PALETTE)] for i in range(len(top_persist))],
                    edgecolor='none', height=0.65)
    for bar in bars:
        ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                 f'{int(bar.get_width())} mo', va='center', color='white', fontsize=9)
    ax1.set_title('Disease Persistence (Months Active)', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Months Observed', color='white')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    crop_health_avg = crop_health_pivot.mean(axis=1).sort_values()
    colors_ch = ['#f87171' if v < 60 else '#facc15' if v < 75 else '#34d399' for v in crop_health_avg.values]
    bars2 = ax2.barh(crop_health_avg.index, crop_health_avg.values, color=colors_ch, edgecolor='none', height=0.65)
    ax2.axvline(x=70, color='#facc15', linewidth=2, linestyle='--', label='Health Threshold (70%)')
    for bar in bars2:
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                 f'{bar.get_width():.1f}%', va='center', color='white', fontsize=9)
    ax2.set_title('Avg Healthy Crop % by Crop Type (All Months)', fontsize=13, fontweight='bold', color='white')
    ax2.set_xlabel('Healthy Crop % (health_score >= 70)', color='white')
    ax2.legend(fontsize=10, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_04_DiseasePersistence.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 4: Disease Persistence saved")

# Chart 5: Crop Health Retention Heatmap
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(max(18, crop_health_pivot.shape[1] * 0.9),
                                    max(6, crop_health_pivot.shape[0] * 0.6)), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    # show last 12 months
    ch_display = crop_health_pivot.iloc[:, -min(12, crop_health_pivot.shape[1]):]
    sns.heatmap(ch_display, ax=ax, cmap='RdYlGn', annot=True, fmt='.0f',
                linewidths=0.5, vmin=0, vmax=100,
                cbar_kws={'label': 'Healthy Crop %', 'shrink': 0.7},
                annot_kws={'size': 8})
    ax.set_title('Crop Health Retention Heatmap (% Healthy per Month)', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Month', color='white', fontsize=12)
    ax.set_ylabel('Crop Type', color='white', fontsize=12)
    ax.tick_params(colors='white')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_05_CropHealthRetention.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 5: Crop Health Retention Heatmap saved")

# Chart 6: Cohort Retention Dashboard
with plt.rc_context({'figure.facecolor': '#0f172a','axes.facecolor': '#1e293b',
                     'axes.labelcolor': 'white','xtick.color': 'white','ytick.color': 'white',
                     'text.color': 'white','grid.color': '#334155','axes.grid': True,'grid.alpha': 0.4,
                     'axes.spines.top': False,'axes.spines.right': False}):
    fig = plt.figure(figsize=(22, 12), facecolor='#0f172a')
    fig.suptitle('AgriShield Analytics – Cohort & Retention Dashboard | Day 9',
                 fontsize=20, fontweight='bold', color='white')
    gs = GridSpec(2, 4, figure=fig, hspace=0.5, wspace=0.4)

    # KPI Cards
    m0_ret = float(avg_retention.iloc[0]) if len(avg_retention) > 0 else 100
    m3_ret = float(avg_retention.iloc[3]) if len(avg_retention) > 3 else float(avg_retention.iloc[-1])
    m6_ret = float(avg_retention.iloc[6]) if len(avg_retention) > 6 else float(avg_retention.iloc[-1])
    total_cohorts = len(retention_pct)
    kpis = [
        ('Total Cohorts',    str(total_cohorts),    '#38bdf8'),
        ('Month-0 Retention', f"{m0_ret:.0f}%",    '#34d399'),
        ('Month-3 Retention', f"{m3_ret:.0f}%",    '#818cf8'),
        ('Month-6 Retention', f"{m6_ret:.0f}%",    '#fb923c'),
    ]
    for i, (label, value, color) in enumerate(kpis):
        ax_k = fig.add_subplot(gs[0, i])
        ax_k.set_facecolor('#1e293b')
        ax_k.set_xlim(0, 1); ax_k.set_ylim(0, 1)
        ax_k.text(0.5, 0.62, value, ha='center', va='center', fontsize=26, fontweight='bold', color=color)
        ax_k.text(0.5, 0.25, label, ha='center', va='center', fontsize=10, color='#94a3b8')
        for spine in ax_k.spines.values():
            spine.set_edgecolor(color); spine.set_linewidth(2)
        ax_k.set_xticks([]); ax_k.set_yticks([])

    # Retention curve (bottom left 2 cols)
    ax_rc = fig.add_subplot(gs[1, :2])
    ax_rc.set_facecolor('#1e293b')
    ax_rc.plot(months, avg_retention.values, color='#38bdf8', linewidth=3, marker='o', markersize=7)
    ax_rc.fill_between(months,
                       (avg_retention - std_retention).clip(0, 100).values,
                       (avg_retention + std_retention).clip(0, 100).values,
                       color='#38bdf8', alpha=0.2)
    for m, val in zip(months, avg_retention.values):
        ax_rc.text(m, val + 2, f'{val:.0f}%', ha='center', color='white', fontsize=8)
    ax_rc.set_title('Avg Cohort Retention Curve', fontsize=12, fontweight='bold', color='white')
    ax_rc.set_xlabel('Month Offset', color='white', fontsize=10)
    ax_rc.set_ylabel('Retention %', color='white', fontsize=10)
    ax_rc.set_ylim(0, 115)

    # Regional yield by year (bottom right 2 cols)
    ax_reg = fig.add_subplot(gs[1, 2:])
    ax_reg.set_facecolor('#1e293b')
    reg_yield_pivot = regional_cohort.pivot(index='location_name', columns='cohort_year', values='Avg_Yield')
    for i, col in enumerate(reg_yield_pivot.columns):
        ax_reg.plot(reg_yield_pivot.index, reg_yield_pivot[col],
                    marker='o', linewidth=2, label=str(col),
                    color=PALETTE[i % len(PALETTE)])
    plt.setp(ax_reg.xaxis.get_majorticklabels(), rotation=20, ha='right')
    ax_reg.set_title('Regional Avg Yield by Year (Cohort)', fontsize=12, fontweight='bold', color='white')
    ax_reg.set_xlabel('Region', color='white', fontsize=10)
    ax_reg.set_ylabel('Avg Yield (t/ha)', color='white', fontsize=10)
    ax_reg.legend(fontsize=9, framealpha=0.3, title='Year', title_fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'COHORT_06_Dashboard.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 6: Cohort Dashboard saved")

print("\n✅ Day 9 – Cohort & Retention Analysis Complete! (6 charts + 4 CSV files)")

"""
AgriShield Analytics – Day 4: Performance Analysis
Author: AgriShield Analytics Team
Date: 2024
Description:
    Comprehensive performance analysis including:
    - Crop Health Performance
    - Disease Frequency Analysis
    - Pest Distribution
    - Yield Analysis (top/bottom crops)
    - Pesticide & Irrigation Usage
    - Regional Performance
    - Water Efficiency
    - KPI Summary Table
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'Dataset')
IMG_DIR  = os.path.join(BASE_DIR, '..', 'Images')
RPT_DIR  = os.path.join(BASE_DIR, '..', 'Reports')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(RPT_DIR, exist_ok=True)

STYLE = {
    'figure.facecolor': '#0f172a', 'axes.facecolor': '#1e293b',
    'axes.labelcolor': 'white',    'xtick.color': 'white',
    'ytick.color': 'white',        'text.color': 'white',
    'grid.color': '#334155',       'axes.grid': True,
    'grid.alpha': 0.4,             'axes.spines.top': False,
    'axes.spines.right': False
}

PALETTE = ['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6',
           '#a78bfa','#4ade80','#facc15','#f87171','#22d3ee',
           '#e879f9','#60a5fa','#fbbf24','#a3e635','#2dd4bf']

print("=" * 70)
print("  AgriShield Analytics – Day 4: Performance Analysis")
print("=" * 70)

# ── Load Data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, 'Cleaned_AgriShield_Data.csv'))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])
print(f"\n  Loaded: {len(df)} rows x {len(df.columns)} columns")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 1: Crop Health Score by Crop Type (Horizontal Bar)
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    crop_health = df.groupby('crop_name')['health_score'].mean().sort_values()
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(crop_health))]
    bars = ax.barh(crop_health.index, crop_health.values, color=colors, edgecolor='none', height=0.65)
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                f'{width:.1f}', va='center', color='white', fontsize=9, fontweight='bold')
    ax.axvline(x=70, color='#facc15', linestyle='--', linewidth=1.5, alpha=0.8, label='Healthy Threshold (70)')
    ax.set_title('Average Health Score by Crop Type', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Average Health Score (0–100)', color='white', fontsize=12)
    ax.legend(fontsize=10, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_01_CropHealth.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 1: Crop Health Score saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 2: Disease Frequency Analysis
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor='#0f172a')
    fig.suptitle('Disease Frequency & Severity Analysis', fontsize=18, fontweight='bold', color='white')

    # Left: Disease count bar
    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    disease_cnt = df['disease_name'].value_counts().head(10)
    bars = ax1.bar(range(len(disease_cnt)), disease_cnt.values,
                   color=PALETTE[:len(disease_cnt)], edgecolor='none', width=0.7)
    ax1.set_xticks(range(len(disease_cnt)))
    ax1.set_xticklabels(disease_cnt.index, rotation=35, ha='right', fontsize=9)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 str(int(bar.get_height())), ha='center', color='white', fontsize=9, fontweight='bold')
    ax1.set_title('Top 10 Diseases by Frequency', fontsize=13, fontweight='bold', color='white')
    ax1.set_ylabel('Count', color='white')

    # Right: Disease severity donut
    ax2 = axes[1]; ax2.set_facecolor('#0f172a')
    sev_cnt = df['disease_severity'].value_counts()
    sev_colors = {'Low': '#4ade80', 'Medium': '#facc15', 'High': '#fb923c', 'Critical': '#f87171'}
    colors_sev = [sev_colors.get(s, '#818cf8') for s in sev_cnt.index]
    wedges, texts, autotexts = ax2.pie(sev_cnt.values, labels=sev_cnt.index,
                                       autopct='%1.1f%%', colors=colors_sev,
                                       startangle=90,
                                       wedgeprops=dict(width=0.6, edgecolor='#0f172a', linewidth=2),
                                       pctdistance=0.8)
    for t in texts + autotexts:
        t.set_color('white'); t.set_fontsize(11)
    ax2.set_title('Disease Severity Distribution', fontsize=13, fontweight='bold', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_02_DiseaseAnalysis.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 2: Disease Frequency saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 3: Pest Distribution
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor='#0f172a')
    fig.suptitle('Pest Distribution & Severity Analysis', fontsize=18, fontweight='bold', color='white')

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    pest_cnt = df['pest_name'].value_counts().head(10)
    bars = ax1.bar(range(len(pest_cnt)), pest_cnt.values,
                   color=PALETTE[:len(pest_cnt)], edgecolor='none', width=0.7)
    ax1.set_xticks(range(len(pest_cnt)))
    ax1.set_xticklabels(pest_cnt.index, rotation=35, ha='right', fontsize=9)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 str(int(bar.get_height())), ha='center', color='white', fontsize=9, fontweight='bold')
    ax1.set_title('Top 10 Pests by Frequency', fontsize=13, fontweight='bold', color='white')
    ax1.set_ylabel('Count', color='white')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    pest_crop = df.groupby(['crop_name','pest_severity']).size().unstack(fill_value=0)
    sev_order = [c for c in ['Low','Medium','High','Critical'] if c in pest_crop.columns]
    pest_crop = pest_crop[sev_order]
    x = np.arange(len(pest_crop.index)); width = 0.2
    bar_colors = {'Low':'#4ade80','Medium':'#facc15','High':'#fb923c','Critical':'#f87171'}
    for i, sev in enumerate(sev_order):
        bars2 = ax2.bar(x + i*width, pest_crop[sev], width, label=sev,
                        color=bar_colors.get(sev,'#818cf8'), edgecolor='none')
    ax2.set_xticks(x + width * (len(sev_order)-1) / 2)
    ax2.set_xticklabels(pest_crop.index, rotation=35, ha='right', fontsize=8)
    ax2.set_title('Pest Severity by Crop Type', fontsize=13, fontweight='bold', color='white')
    ax2.legend(fontsize=10, framealpha=0.3)
    ax2.set_ylabel('Count', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_03_PestDistribution.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 3: Pest Distribution saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 4: Yield Analysis – Top & Bottom Crops
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), facecolor='#0f172a')
    fig.suptitle('Crop Yield Performance – Top vs Bottom Performers', fontsize=18, fontweight='bold', color='white')

    crop_yield = df.groupby('crop_name')['crop_yield_tons_ha'].mean().sort_values(ascending=False)
    top5 = crop_yield.head(5)
    bot5 = crop_yield.tail(5)

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    bars1 = ax1.bar(top5.index, top5.values, color='#34d399', edgecolor='none', width=0.65)
    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f'{bar.get_height():.2f}t', ha='center', color='white', fontsize=10, fontweight='bold')
    ax1.set_title('🏆 Top 5 Performing Crops', fontsize=14, fontweight='bold', color='#34d399')
    ax1.set_ylabel('Avg Yield (tons/ha)', color='white'); ax1.set_xlabel('Crop', color='white')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=20, ha='right')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    bars2 = ax2.bar(bot5.index, bot5.values, color='#f87171', edgecolor='none', width=0.65)
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f'{bar.get_height():.2f}t', ha='center', color='white', fontsize=10, fontweight='bold')
    ax2.set_title('⚠️ Bottom 5 Performing Crops', fontsize=14, fontweight='bold', color='#f87171')
    ax2.set_ylabel('Avg Yield (tons/ha)', color='white'); ax2.set_xlabel('Crop', color='white')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_04_YieldAnalysis.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 4: Yield Analysis saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 5: Pesticide Usage Analysis
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), facecolor='#0f172a')
    fig.suptitle('Pesticide Usage Analysis', fontsize=18, fontweight='bold', color='white')

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    pest_usage = df.groupby('crop_name')['pesticide_l_ha'].mean().sort_values(ascending=False)
    bars = ax1.bar(pest_usage.index, pest_usage.values,
                   color=[PALETTE[i % len(PALETTE)] for i in range(len(pest_usage))],
                   edgecolor='none', width=0.7)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f'{bar.get_height():.1f}', ha='center', color='white', fontsize=8)
    ax1.set_title('Avg Pesticide Usage by Crop (L/ha)', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Crop', color='white'); ax1.set_ylabel('Pesticide (L/ha)', color='white')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=35, ha='right')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    pest_loc = df.groupby('location_name')['pesticide_l_ha'].mean().sort_values(ascending=False)
    colors_loc = [PALETTE[i % len(PALETTE)] for i in range(len(pest_loc))]
    bars2 = ax2.barh(pest_loc.index, pest_loc.values, color=colors_loc, edgecolor='none', height=0.65)
    for bar in bars2:
        ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                 f'{bar.get_width():.1f}', va='center', color='white', fontsize=9)
    ax2.set_title('Avg Pesticide Usage by Region (L/ha)', fontsize=13, fontweight='bold', color='white')
    ax2.set_xlabel('Pesticide (L/ha)', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_05_PesticideUsage.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 5: Pesticide Usage saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 6: Irrigation / Water Usage Analysis
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), facecolor='#0f172a')
    fig.suptitle('Irrigation & Water Usage Analysis', fontsize=18, fontweight='bold', color='white')

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    irr_method = df.groupby('irrigation_method')['water_usage_l'].mean().sort_values(ascending=False)
    bars = ax1.bar(irr_method.index, irr_method.values,
                   color=['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6'][:len(irr_method)],
                   edgecolor='none', width=0.65)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                 f'{bar.get_height():,.0f}L', ha='center', color='white', fontsize=10, fontweight='bold')
    ax1.set_title('Avg Water Usage by Irrigation Method', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Irrigation Method', color='white'); ax1.set_ylabel('Avg Water (L)', color='white')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=20, ha='right')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    water_crop = df.groupby('crop_name')['water_efficiency'].mean().sort_values()
    colors_eff = ['#f87171' if v < water_crop.median() else '#34d399' for v in water_crop.values]
    ax2.barh(water_crop.index, water_crop.values, color=colors_eff, edgecolor='none', height=0.65)
    ax2.axvline(x=water_crop.median(), color='#facc15', linestyle='--', linewidth=2, label='Median')
    ax2.set_title('Water Efficiency by Crop (Yield/1000L)', fontsize=13, fontweight='bold', color='white')
    ax2.set_xlabel('Efficiency Score', color='white')
    ax2.legend(fontsize=10, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_06_IrrigationAnalysis.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 6: Irrigation Analysis saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 7: Regional Performance Heatmap
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    regional_pivot = df.pivot_table(
        values='crop_yield_tons_ha',
        index='location_name',
        columns='crop_name',
        aggfunc='mean'
    ).round(2)
    sns.heatmap(regional_pivot, ax=ax, cmap='YlOrRd', annot=True, fmt='.1f',
                linewidths=0.5, cbar_kws={'label': 'Avg Yield (tons/ha)', 'shrink': 0.8},
                annot_kws={'size': 8, 'color': 'black'})
    ax.set_title('Regional Crop Yield Heatmap (tons/ha)', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Crop Type', color='white', fontsize=12)
    ax.set_ylabel('Region', color='white', fontsize=12)
    ax.tick_params(colors='white')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'PERF_07_RegionalHeatmap.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 7: Regional Heatmap saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 8: Comprehensive KPI Dashboard Panel
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    fig = plt.figure(figsize=(20, 11), facecolor='#0f172a')
    fig.suptitle('AgriShield Analytics – Performance Dashboard | Day 4',
                 fontsize=20, fontweight='bold', color='white', y=1.0)
    gs = GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.35)

    # KPI Cards (top row)
    kpis = [
        ('Total Records',    f"{len(df):,}",           '#38bdf8'),
        ('Avg Yield (t/ha)', f"{df['crop_yield_tons_ha'].mean():.2f}", '#34d399'),
        ('Avg Health Score', f"{df['health_score'].mean():.1f}",       '#818cf8'),
        ('Healthy Crops %',  f"{(df['health_score'] >= 70).mean()*100:.1f}%", '#4ade80'),
    ]
    for i, (label, value, color) in enumerate(kpis):
        ax_kpi = fig.add_subplot(gs[0, i])
        ax_kpi.set_facecolor('#1e293b')
        ax_kpi.set_xlim(0, 1); ax_kpi.set_ylim(0, 1)
        ax_kpi.text(0.5, 0.62, value, ha='center', va='center',
                    fontsize=26, fontweight='bold', color=color)
        ax_kpi.text(0.5, 0.25, label, ha='center', va='center',
                    fontsize=10, color='#94a3b8')
        for spine in ax_kpi.spines.values():
            spine.set_edgecolor(color); spine.set_linewidth(2)
        ax_kpi.set_xticks([]); ax_kpi.set_yticks([])

    # Monthly Yield Trend
    ax_trend = fig.add_subplot(gs[1, :2])
    ax_trend.set_facecolor('#1e293b')
    monthly = df.groupby(['year','month'])['crop_yield_tons_ha'].mean().reset_index()
    monthly['period'] = monthly['year'].astype(str) + '-M' + monthly['month'].astype(str).str.zfill(2)
    ax_trend.plot(monthly['period'], monthly['crop_yield_tons_ha'],
                  color='#38bdf8', linewidth=2.5, marker='o', markersize=5)
    ax_trend.fill_between(range(len(monthly)), monthly['crop_yield_tons_ha'],
                          alpha=0.2, color='#38bdf8')
    ax_trend.set_xticks(range(0, len(monthly), 3))
    ax_trend.set_xticklabels(monthly['period'].iloc[::3], rotation=30, ha='right', fontsize=7)
    ax_trend.set_title('Monthly Yield Trend', fontsize=12, fontweight='bold', color='white')
    ax_trend.set_ylabel('Avg Yield', color='white', fontsize=9)

    # Region performance bar
    ax_reg = fig.add_subplot(gs[1, 2:])
    ax_reg.set_facecolor('#1e293b')
    reg_perf = df.groupby('location_name')['crop_yield_tons_ha'].mean().sort_values(ascending=False)
    bars = ax_reg.bar(reg_perf.index, reg_perf.values,
                      color=[PALETTE[i % len(PALETTE)] for i in range(len(reg_perf))],
                      edgecolor='none', width=0.7)
    ax_reg.set_title('Regional Average Yield', fontsize=12, fontweight='bold', color='white')
    ax_reg.set_ylabel('Avg Yield (t/ha)', color='white', fontsize=9)
    plt.setp(ax_reg.xaxis.get_majorticklabels(), rotation=25, ha='right', fontsize=8)

    # Disease severity pie
    ax_dsev = fig.add_subplot(gs[2, 0])
    ax_dsev.set_facecolor('#0f172a')
    sev_cnt = df['disease_severity'].value_counts()
    sev_colors = {'Low': '#4ade80', 'Medium': '#facc15', 'High': '#fb923c', 'Critical': '#f87171'}
    clrs = [sev_colors.get(s, '#818cf8') for s in sev_cnt.index]
    ax_dsev.pie(sev_cnt.values, labels=sev_cnt.index, autopct='%1.1f%%',
                colors=clrs, startangle=90,
                wedgeprops=dict(width=0.55, edgecolor='#0f172a'))
    ax_dsev.set_title('Disease Severity', fontsize=11, fontweight='bold', color='white')

    # Yield category donut
    ax_ycat = fig.add_subplot(gs[2, 1])
    ax_ycat.set_facecolor('#0f172a')
    if 'yield_category' in df.columns:
        ycat = df['yield_category'].value_counts()
        ycat_colors = {'Low':'#f87171','Medium':'#facc15','High':'#4ade80','Very High':'#38bdf8'}
        yc = [ycat_colors.get(str(k), '#818cf8') for k in ycat.index]
        ax_ycat.pie(ycat.values, labels=ycat.index, autopct='%1.1f%%',
                    colors=yc, startangle=90,
                    wedgeprops=dict(width=0.55, edgecolor='#0f172a'))
    ax_ycat.set_title('Yield Category', fontsize=11, fontweight='bold', color='white')

    # Pesticide scatter: yield vs pesticide
    ax_ps = fig.add_subplot(gs[2, 2:])
    ax_ps.set_facecolor('#1e293b')
    sc = ax_ps.scatter(df['pesticide_l_ha'], df['crop_yield_tons_ha'],
                       c=df['health_score'], cmap='plasma', alpha=0.4, s=25)
    ax_ps.set_xlabel('Pesticide (L/ha)', color='white', fontsize=9)
    ax_ps.set_ylabel('Crop Yield (t/ha)', color='white', fontsize=9)
    ax_ps.set_title('Pesticide vs Yield (colored by Health Score)', fontsize=11, fontweight='bold', color='white')
    cbar = plt.colorbar(sc, ax=ax_ps)
    cbar.set_label('Health Score', color='white', fontsize=8)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.savefig(os.path.join(IMG_DIR, 'PERF_08_Dashboard.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 8: Performance Dashboard saved")

# ── KPI Summary ───────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("  KEY PERFORMANCE INDICATORS – SUMMARY")
print("─" * 60)
total_farms   = df['farmer_id'].nunique()
total_records = len(df)
healthy_pct   = (df['health_score'] >= 70).mean() * 100
avg_yield     = df['crop_yield_tons_ha'].mean()
avg_pesticide = df['pesticide_l_ha'].mean()
avg_water     = df['water_usage_l'].mean()
disease_rate  = (df['disease_severity'].isin(['High','Critical'])).mean() * 100
pest_rate     = (df['pest_severity'].isin(['High','Critical'])).mean() * 100
top_crop      = df.groupby('crop_name')['crop_yield_tons_ha'].mean().idxmax()
bot_crop      = df.groupby('crop_name')['crop_yield_tons_ha'].mean().idxmin()
top_region    = df.groupby('location_name')['crop_yield_tons_ha'].mean().idxmax()

kpi_data = {
    'KPI': ['Total Farms','Total Records','Healthy Crops %','Avg Yield (t/ha)',
            'Avg Pesticide (L/ha)','Avg Water Usage (L)','High Disease Rate %',
            'High Pest Rate %','Top Crop','Bottom Crop','Best Region'],
    'Value': [total_farms, total_records, f"{healthy_pct:.1f}%",
              f"{avg_yield:.2f}", f"{avg_pesticide:.2f}", f"{avg_water:,.0f}",
              f"{disease_rate:.1f}%", f"{pest_rate:.1f}%",
              top_crop, bot_crop, top_region]
}
kpi_df = pd.DataFrame(kpi_data)
kpi_df.to_csv(os.path.join(DATA_DIR, 'Performance_KPI_Summary.csv'), index=False)
print(kpi_df.to_string(index=False))

print("\n✅ Day 4 – Performance Analysis Complete! (8 charts saved)")

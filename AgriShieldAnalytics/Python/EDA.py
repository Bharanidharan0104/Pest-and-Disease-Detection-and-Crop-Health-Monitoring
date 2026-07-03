"""
AgriShield Analytics – Day 2: Exploratory Data Analysis
Author: AgriShield Analytics Team
Date: 2024
Description:
    Comprehensive EDA including:
    - Descriptive statistics
    - Outlier detection (IQR method)
    - Missing value analysis
    - Distribution analysis
    - Correlation matrix
    - 9 professional visualizations
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, '..', 'Dataset')
IMG_DIR   = os.path.join(BASE_DIR, '..', 'Images')
os.makedirs(IMG_DIR, exist_ok=True)

print("=" * 60)
print("  AgriShield Analytics – Day 2: EDA")
print("=" * 60)

df = pd.read_csv(os.path.join(DATA_DIR, "Cleaned_AgriShield_Data.csv"))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])

num_cols = ['crop_yield_tons_ha','temperature_c','humidity_pct','rainfall_mm',
            'soil_ph','ndvi_index','health_score','fertilizer_kg_ha',
            'pesticide_l_ha','farm_area_ha','water_usage_l']

STYLE = {'figure.facecolor': '#0f172a', 'axes.facecolor': '#1e293b',
         'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white',
         'text.color': 'white', 'grid.color': '#334155', 'axes.grid': True}

# ── 1. Descriptive Statistics ─────────────────────────────────────────────────
print("\n[1] Descriptive Statistics")
stats_df = df[num_cols].agg(['mean','median','std','var','min','max']).round(3)
stats_df.loc['mode'] = df[num_cols].mode().iloc[0].round(3)
stats_df.loc['Q1']  = df[num_cols].quantile(0.25).round(3)
stats_df.loc['Q3']  = df[num_cols].quantile(0.75).round(3)
stats_df.loc['IQR'] = (df[num_cols].quantile(0.75) - df[num_cols].quantile(0.25)).round(3)
print(stats_df.to_string())

# ── 2. Outlier Detection ──────────────────────────────────────────────────────
print("\n[2] Outlier Detection (IQR Method)")
outlier_summary = {}
for col in num_cols:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
    n_out = ((df[col] < lower) | (df[col] > upper)).sum()
    outlier_summary[col] = n_out
    print(f"  {col}: {n_out} outliers")

# ── 3. Missing Value Analysis ─────────────────────────────────────────────────
print("\n[3] Missing Value Analysis")
miss = df.isnull().sum()
miss_pct = (miss / len(df) * 100).round(2)
print(pd.DataFrame({'Missing Count': miss[miss>0], 'Missing %': miss_pct[miss>0]}))

# ══════════════════════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
palette = ['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6',
           '#a78bfa','#4ade80','#facc15','#f87171','#22d3ee']

# ── Chart 1: Histogram ─────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(3, 4, figsize=(18, 12), facecolor='#0f172a')
    fig.suptitle('Distribution Analysis – AgriShield Analytics', fontsize=18,
                 fontweight='bold', color='white', y=1.01)
    axes = axes.flatten()
    for i, col in enumerate(num_cols):
        axes[i].hist(df[col].dropna(), bins=30, color=palette[i % len(palette)], alpha=0.85, edgecolor='none')
        axes[i].set_title(col.replace('_',' ').title(), color='white', fontsize=10, fontweight='bold')
        axes[i].set_facecolor('#1e293b')
    for j in range(len(num_cols), len(axes)):
        axes[j].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_01_Histogram.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Histogram saved")

# ── Chart 2: Box Plot ──────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(16, 7), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    bp = ax.boxplot([df[c].dropna() for c in num_cols], patch_artist=True,
                    medianprops=dict(color='#facc15', linewidth=2))
    for patch, color in zip(bp['boxes'], palette):
        patch.set_facecolor(color); patch.set_alpha(0.8)
    ax.set_xticklabels([c.replace('_','\n').title() for c in num_cols], fontsize=8, color='white')
    ax.set_title('Box Plot – Outlier Detection', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_ylabel('Value', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_02_BoxPlot.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Box Plot saved")

# ── Chart 3: Scatter Plot ──────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    sc = ax.scatter(df['ndvi_index'], df['crop_yield_tons_ha'],
                    c=df['health_score'], cmap='plasma', alpha=0.6, s=40)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Health Score', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    ax.set_xlabel('NDVI Index', color='white', fontsize=12)
    ax.set_ylabel('Crop Yield (tons/ha)', color='white', fontsize=12)
    ax.set_title('NDVI vs Crop Yield (colored by Health Score)', fontsize=15, fontweight='bold', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_03_ScatterPlot.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Scatter Plot saved")

# ── Chart 4: Heatmap (Correlation Matrix) ─────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(13, 10), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    corr = df[num_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                ax=ax, annot_kws={'size':8}, linewidths=0.5,
                cbar_kws={'shrink':0.8})
    ax.set_title('Correlation Matrix – Numeric Features', fontsize=15, fontweight='bold', color='white', pad=15)
    ax.tick_params(colors='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_04_Heatmap.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Heatmap saved")

# ── Chart 5: Bar Chart ─────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    crop_yield = df.groupby('crop_name')['crop_yield_tons_ha'].mean().sort_values(ascending=False)
    bars = ax.bar(crop_yield.index, crop_yield.values, color=palette[:len(crop_yield)], edgecolor='none', width=0.65)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
                f'{bar.get_height():.2f}', ha='center', va='bottom', color='white', fontsize=9)
    ax.set_title('Average Crop Yield by Crop Type', fontsize=15, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Crop Name', color='white'); ax.set_ylabel('Avg Yield (tons/ha)', color='white')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_05_BarChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Bar Chart saved")

# ── Chart 6: Pie Chart ─────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(9, 8), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    pest_cnt = df['pest_severity'].value_counts()
    wedges, texts, autotexts = ax.pie(pest_cnt.values, labels=pest_cnt.index,
                                      autopct='%1.1f%%', colors=palette[:len(pest_cnt)],
                                      startangle=140, pctdistance=0.8,
                                      wedgeprops=dict(width=0.6, edgecolor='#0f172a', linewidth=2))
    for t in texts+autotexts:
        t.set_color('white'); t.set_fontsize(12)
    ax.set_title('Pest Severity Distribution', fontsize=15, fontweight='bold', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_06_PieChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Pie Chart saved")

# ── Chart 7: Tree Map ─────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    loc_yield = df.groupby('location_name')['crop_yield_tons_ha'].sum().sort_values(ascending=False)
    sizes = loc_yield.values
    labels = [f"{loc}\n{val:.1f}T" for loc, val in zip(loc_yield.index, sizes)]
    try:
        import squarify
        squarify.plot(sizes=sizes, label=labels, color=palette[:len(sizes)],
                      alpha=0.85, ax=ax, text_kwargs={'color':'white','fontsize':11,'fontweight':'bold'})
    except ImportError:
        # Fallback: horizontal bar chart styled as treemap
        ax.barh(loc_yield.index, sizes, color=palette[:len(sizes)])
        ax.set_xlabel('Total Yield (tons)', color='white')
        for i, (idx, val) in enumerate(zip(loc_yield.index, sizes)):
            ax.text(val*0.01, i, f'{val:.1f}T', va='center', color='white', fontsize=10)
    ax.set_title('Total Crop Yield by Location (Tree Map)', fontsize=15, fontweight='bold', color='white', pad=15)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_07_TreeMap.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Tree Map saved")

# ── Chart 8: Line Chart ────────────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(14, 6), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    monthly = df.groupby(['year','month'])['crop_yield_tons_ha'].mean().reset_index()
    monthly['period'] = monthly['year'].astype(str)+'-'+monthly['month'].astype(str).str.zfill(2)
    for yr, grp in monthly.groupby('year'):
        ax.plot(grp['period'], grp['crop_yield_tons_ha'], marker='o', linewidth=2.5,
                label=str(yr), color=palette[list(monthly['year'].unique()).index(yr)])
    ax.set_title('Monthly Average Crop Yield Trend', fontsize=15, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Month', color='white'); ax.set_ylabel('Avg Yield (tons/ha)', color='white')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax.legend(fontsize=11, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_08_LineChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Line Chart saved")

# ── Chart 9: Waterfall Chart ──────────────────────────────────────────────────
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    qtr_yield = df.groupby(['year','quarter'])['total_revenue'].sum()/1e6
    qtr_yield = qtr_yield.reset_index()
    qtr_yield['label'] = 'Q'+qtr_yield['quarter'].astype(str)+' '+qtr_yield['year'].astype(str)
    values = qtr_yield['total_revenue'].values
    running = 0; bottoms = []; colors_wf = []
    for v in values:
        bottoms.append(running)
        colors_wf.append('#34d399' if v >= 0 else '#f87171')
        running += v
    ax.bar(qtr_yield['label'], values, bottom=bottoms, color=colors_wf, width=0.6, edgecolor='none')
    for i, (b, v) in enumerate(zip(bottoms, values)):
        ax.text(i, b+v+(running*0.005), f'{v:.1f}M', ha='center', va='bottom',
                color='white', fontsize=9, fontweight='bold')
    ax.set_title('Quarterly Revenue Waterfall Chart (INR Millions)', fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel('Quarter', color='white'); ax.set_ylabel('Revenue (₹M)', color='white')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'EDA_09_WaterfallChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → Waterfall Chart saved")

print("\n✅ EDA Complete – 9 charts saved to Images/")

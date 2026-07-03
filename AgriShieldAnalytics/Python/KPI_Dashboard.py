"""
AgriShield Analytics – Day 6: KPI Dashboard Charts
Author: AgriShield Analytics Team
Date: 2024
Description:
    Generates all KPI visuals for the Executive Dashboard:
    - 9 KPI metric cards
    - Monthly trend line
    - Regional performance bars
    - Disease rate gauges
    - Healthy crop % donut
    - Interactive filter simulation
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'Dataset')
IMG_DIR  = os.path.join(BASE_DIR, '..', 'Images')
os.makedirs(IMG_DIR, exist_ok=True)

STYLE = {
    'figure.facecolor': '#0f172a', 'axes.facecolor': '#1e293b',
    'axes.labelcolor': 'white',    'xtick.color': 'white',
    'ytick.color': 'white',        'text.color': 'white',
    'grid.color': '#334155',       'axes.grid': True,
    'grid.alpha': 0.35,            'axes.spines.top': False,
    'axes.spines.right': False
}
PALETTE = ['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6',
           '#a78bfa','#4ade80','#facc15','#f87171','#22d3ee']

print("=" * 70)
print("  AgriShield Analytics – Day 6: KPI Dashboard")
print("=" * 70)

df = pd.read_csv(os.path.join(DATA_DIR, 'Cleaned_AgriShield_Data.csv'))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])

# ── Compute all KPIs ───────────────────────────────────────────────────────────
total_farms      = df['farmer_id'].nunique()
total_records    = len(df)
healthy_count    = (df['health_score'] >= 70).sum()
diseased_count   = (df['disease_severity'].isin(['High','Critical'])).sum()
pest_cases       = (df['pest_severity'].isin(['High','Critical'])).sum()
avg_yield        = df['crop_yield_tons_ha'].mean()
avg_pesticide    = df['pesticide_l_ha'].mean()
avg_irrigation   = df['water_usage_l'].mean()
disease_rate     = diseased_count / total_records * 100
healthy_pct      = healthy_count / total_records * 100
total_revenue    = df['total_revenue'].sum()
avg_ndvi         = df['ndvi_index'].mean()
avg_health_score = df['health_score'].mean()

print(f"\n  {'KPI':<35} {'Value':>15}")
print("  " + "─" * 52)
kpi_labels = [
    ('Total Farms',            f"{total_farms:,}"),
    ('Total Records',          f"{total_records:,}"),
    ('Healthy Crops',          f"{healthy_count:,}"),
    ('Diseased Crops (Hi/Cr)', f"{diseased_count:,}"),
    ('Pest Cases (Hi/Cr)',     f"{pest_cases:,}"),
    ('Average Yield (t/ha)',   f"{avg_yield:.2f}"),
    ('Avg Pesticide (L/ha)',   f"{avg_pesticide:.2f}"),
    ('Avg Irrigation (L)',     f"{avg_irrigation:,.0f}"),
    ('Disease Rate %',         f"{disease_rate:.1f}%"),
    ('Healthy Crop %',         f"{healthy_pct:.1f}%"),
    ('Total Revenue (INR)',    f"₹{total_revenue/1e6:.1f}M"),
    ('Avg NDVI Index',         f"{avg_ndvi:.3f}"),
    ('Avg Health Score',       f"{avg_health_score:.1f}"),
]
for label, value in kpi_labels:
    print(f"  {label:<35} {value:>15}")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 1: Executive KPI Cards Dashboard
# ════════════════════════════════════════════════════════════════════════════════
def draw_kpi_card(ax, title, value, subtitle, color, icon=''):
    ax.set_facecolor('#1e293b')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    # Top color bar
    ax.add_patch(mpatches.FancyBboxPatch((0, 0.88), 1, 0.12, boxstyle="square",
                                          facecolor=color, linewidth=0, transform=ax.transAxes))
    ax.text(0.5, 0.94, icon + ' ' + title, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.56, value, ha='center', va='center',
            fontsize=22, fontweight='bold', color=color, transform=ax.transAxes)
    ax.text(0.5, 0.22, subtitle, ha='center', va='center',
            fontsize=8, color='#94a3b8', transform=ax.transAxes)
    for spine in ax.spines.values():
        spine.set_edgecolor('#334155'); spine.set_linewidth(1)
    ax.set_xticks([]); ax.set_yticks([])

with plt.rc_context(STYLE):
    fig = plt.figure(figsize=(22, 14), facecolor='#0f172a')
    fig.suptitle('AgriShield Analytics – Executive KPI Dashboard',
                 fontsize=24, fontweight='bold', color='white', y=0.97)
    fig.text(0.5, 0.94, f'Crop Health Monitoring | Total Records: {total_records:,} | Revenue: ₹{total_revenue/1e6:.1f}M',
             ha='center', fontsize=12, color='#94a3b8')
    gs = GridSpec(3, 5, figure=fig, hspace=0.55, wspace=0.35, top=0.91, bottom=0.35)

    cards = [
        ('Total Farms',         f"{total_farms:,}",       'Active farmer accounts',      '#38bdf8', '🌾'),
        ('Healthy Crops',       f"{healthy_count:,}",     f'Health Score >= 70',          '#34d399', '✅'),
        ('Diseased Crops',      f"{diseased_count:,}",    'High/Critical severity',      '#f87171', '🦠'),
        ('Pest Cases',          f"{pest_cases:,}",        'High/Critical infestations',  '#fb923c', '🐛'),
        ('Avg Yield',           f"{avg_yield:.2f} t/ha",  'Per hectare average',         '#818cf8', '📊'),
        ('Pesticide Usage',     f"{avg_pesticide:.1f} L", 'Average per hectare',         '#f472b6', '💊'),
        ('Irrigation Usage',    f"{avg_irrigation:,.0f}L",'Average water per record',    '#22d3ee', '💧'),
        ('Disease Rate',        f"{disease_rate:.1f}%",   'Hi/Cr cases / total',         '#f87171', '📉'),
        ('Healthy Crop %',      f"{healthy_pct:.1f}%",    'Score >= 70 / total',          '#4ade80', '📈'),
        ('NDVI Index',          f"{avg_ndvi:.3f}",        'Vegetation health index',     '#a78bfa', '🌿'),
    ]
    for i, (title, value, subtitle, color, icon) in enumerate(cards):
        r, c = divmod(i, 5)
        ax = fig.add_subplot(gs[r, c])
        draw_kpi_card(ax, title, value, subtitle, color, icon)

    # Bottom section: Monthly trend + Regional bars
    gs2 = GridSpec(1, 2, figure=fig, hspace=0.4, wspace=0.35, top=0.30, bottom=0.06)

    ax_trend = fig.add_subplot(gs2[0, 0])
    ax_trend.set_facecolor('#1e293b')
    monthly = df.groupby(['year','month'])['crop_yield_tons_ha'].mean().reset_index()
    monthly['period'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
    ax_trend.plot(range(len(monthly)), monthly['crop_yield_tons_ha'],
                  color='#38bdf8', linewidth=2.5, marker='o', markersize=5)
    ax_trend.fill_between(range(len(monthly)), monthly['crop_yield_tons_ha'],
                          alpha=0.2, color='#38bdf8')
    step = max(1, len(monthly) // 8)
    ax_trend.set_xticks(range(0, len(monthly), step))
    ax_trend.set_xticklabels(monthly['period'].iloc[::step], rotation=30, ha='right', fontsize=8)
    ax_trend.set_title('Monthly Yield Trend', fontsize=13, fontweight='bold', color='white', pad=10)
    ax_trend.set_ylabel('Avg Yield (t/ha)', color='white', fontsize=10)
    for spine in ax_trend.spines.values():
        spine.set_edgecolor('#334155')

    ax_reg = fig.add_subplot(gs2[0, 1])
    ax_reg.set_facecolor('#1e293b')
    reg_perf = df.groupby('location_name')['crop_yield_tons_ha'].mean().sort_values(ascending=False)
    bars = ax_reg.bar(reg_perf.index, reg_perf.values,
                      color=[PALETTE[i % len(PALETTE)] for i in range(len(reg_perf))],
                      edgecolor='none', width=0.7)
    for bar in bars:
        ax_reg.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'{bar.get_height():.1f}', ha='center', color='white', fontsize=8)
    ax_reg.set_title('Regional Performance (Avg Yield)', fontsize=13, fontweight='bold', color='white', pad=10)
    ax_reg.set_xlabel('Region', color='white', fontsize=10)
    ax_reg.set_ylabel('Avg Yield (t/ha)', color='white', fontsize=10)
    plt.setp(ax_reg.xaxis.get_majorticklabels(), rotation=20, ha='right')
    for spine in ax_reg.spines.values():
        spine.set_edgecolor('#334155')

    plt.savefig(os.path.join(IMG_DIR, 'KPI_01_ExecutiveDashboard.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("\n  -> Chart 1: Executive KPI Dashboard saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 2: Disease & Pest Rate Gauges (Radial/Gauge Charts)
# ════════════════════════════════════════════════════════════════════════════════
def draw_gauge(ax, value, max_val, title, color, bgcolor='#1e293b'):
    ax.set_facecolor('#0f172a')
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-0.5, 1.3)
    ax.set_aspect('equal'); ax.axis('off')
    theta_bg = np.linspace(np.pi, 0, 200)
    ax.fill_between(np.cos(theta_bg), np.sin(theta_bg)*0,
                    np.sin(theta_bg), color='#1e293b', zorder=1)
    # Background arc
    ax.plot(np.cos(theta_bg)*1.0, np.sin(theta_bg)*1.0,
            color='#334155', linewidth=12, solid_capstyle='round', zorder=2)
    # Value arc
    ratio     = min(value / max_val, 1.0)
    theta_val = np.linspace(np.pi, np.pi - ratio * np.pi, 200)
    ax.plot(np.cos(theta_val)*1.0, np.sin(theta_val)*1.0,
            color=color, linewidth=12, solid_capstyle='round', zorder=3)
    ax.text(0, 0.25, f'{value:.1f}%', ha='center', va='center',
            fontsize=22, fontweight='bold', color=color)
    ax.text(0, -0.15, title, ha='center', va='center',
            fontsize=9, color='#94a3b8')

with plt.rc_context(STYLE):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor='#0f172a')
    fig.suptitle('AgriShield – KPI Gauge Dashboard', fontsize=20, fontweight='bold', color='white', y=1.0)
    gauge_data = [
        (healthy_pct,   100, 'Healthy Crop %',    '#34d399'),
        (disease_rate,  100, 'Disease Rate %',    '#f87171'),
        (pest_cases/total_records*100, 100, 'High Pest Rate %', '#fb923c'),
        (avg_ndvi*100,  100, 'NDVI Index (x100)', '#818cf8'),
        (avg_yield/10*100, 100, 'Yield Achievement %\n(Target: 10 t/ha)', '#38bdf8'),
        (avg_health_score, 100, 'Avg Health Score', '#4ade80'),
    ]
    for ax, (value, max_val, title, color) in zip(axes.flatten(), gauge_data):
        draw_gauge(ax, value, max_val, title, color)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'KPI_02_GaugeDashboard.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 2: Gauge Dashboard saved")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 3: Monthly KPI Trends (multi-metric)
# ════════════════════════════════════════════════════════════════════════════════
with plt.rc_context(STYLE):
    monthly_kpi = df.groupby(['year','month']).agg(
        Avg_Yield     = ('crop_yield_tons_ha', 'mean'),
        Avg_Health    = ('health_score', 'mean'),
        Avg_Pesticide = ('pesticide_l_ha', 'mean'),
        Avg_NDVI      = ('ndvi_index', 'mean'),
        Disease_Rate  = ('disease_severity', lambda x: (x.isin(['High','Critical'])).mean()*100),
        Healthy_Pct   = ('health_score', lambda x: (x >= 70).mean()*100),
    ).reset_index()
    monthly_kpi['period'] = monthly_kpi['year'].astype(str) + '-' + monthly_kpi['month'].astype(str).str.zfill(2)

    fig, axes = plt.subplots(3, 2, figsize=(18, 14), facecolor='#0f172a')
    fig.suptitle('Monthly KPI Trend Analysis – AgriShield Analytics', fontsize=18, fontweight='bold', color='white')
    axes = axes.flatten()
    metrics = [
        ('Avg_Yield',     'Avg Crop Yield (t/ha)',      '#38bdf8'),
        ('Avg_Health',    'Avg Health Score',            '#34d399'),
        ('Avg_Pesticide', 'Avg Pesticide (L/ha)',        '#fb923c'),
        ('Avg_NDVI',      'Avg NDVI Index',              '#818cf8'),
        ('Disease_Rate',  'Disease Rate %',              '#f87171'),
        ('Healthy_Pct',   'Healthy Crop %',              '#4ade80'),
    ]
    step = max(1, len(monthly_kpi) // 8)
    for ax, (col, label, color) in zip(axes, metrics):
        ax.set_facecolor('#1e293b')
        ax.plot(range(len(monthly_kpi)), monthly_kpi[col], color=color, linewidth=2.5, marker='o', markersize=5)
        ax.fill_between(range(len(monthly_kpi)), monthly_kpi[col], alpha=0.2, color=color)
        ax.set_xticks(range(0, len(monthly_kpi), step))
        ax.set_xticklabels(monthly_kpi['period'].iloc[::step], rotation=30, ha='right', fontsize=7)
        ax.set_title(label, fontsize=12, fontweight='bold', color='white')
        ax.set_ylabel(label, color='white', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'KPI_03_MonthlyTrends.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 3: Monthly KPI Trends saved")

print("\n✅ Day 6 – KPI Dashboard Complete! (3 charts)")

"""
AgriShield Analytics – Day 5: Fraud & Anomaly Detection
Author: AgriShield Analytics Team
Date: 2024
Description:
    Multi-method anomaly detection including:
    - Rule-Based Detection (duplicates, range violations)
    - Statistical Methods: Z-Score, IQR
    - Machine Learning: Isolation Forest
    - Combined Fraud Scoring
    - Anomaly Dashboard Charts
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
from scipy import stats
import os, warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("  [WARNING] sklearn not available – Isolation Forest skipped")

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

print("=" * 70)
print("  AgriShield Analytics – Day 5: Fraud & Anomaly Detection")
print("=" * 70)

df = pd.read_csv(os.path.join(DATA_DIR, 'Cleaned_AgriShield_Data.csv'))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])
print(f"\n  Loaded: {len(df)} rows x {len(df.columns)} columns")

TARGET_COLS = ['crop_yield_tons_ha', 'pesticide_l_ha', 'water_usage_l',
               'fertilizer_kg_ha', 'health_score', 'ndvi_index']

# ════════════════════════════════════════════════════════════════════════════════
# METHOD 1: RULE-BASED DETECTION
# ════════════════════════════════════════════════════════════════════════════════
print("\n[METHOD 1] Rule-Based Detection")

# Rule 1: Exact duplicate records
rule1_dupes = df.duplicated(subset=['farmer_id','crop_id','monitoring_date'], keep=False)
print(f"  -> Rule 1 (Exact Duplicates): {rule1_dupes.sum()} records")

# Rule 2: Pesticide > 3x mean
pest_mean = df['pesticide_l_ha'].mean()
pest_std  = df['pesticide_l_ha'].std()
rule2_pest = df['pesticide_l_ha'] > (pest_mean + 3 * pest_std)
print(f"  -> Rule 2 (Abnormal Pesticide >{pest_mean+3*pest_std:.1f}L/ha): {rule2_pest.sum()} records")

# Rule 3: Water usage > 3x mean
water_mean = df['water_usage_l'].mean()
water_std  = df['water_usage_l'].std()
rule3_water = df['water_usage_l'] > (water_mean + 3 * water_std)
print(f"  -> Rule 3 (Abnormal Irrigation >{water_mean+3*water_std:.0f}L): {rule3_water.sum()} records")

# Rule 4: Negative or impossible yield
rule4_yield = df['crop_yield_tons_ha'] <= 0
print(f"  -> Rule 4 (Zero/Negative Yield): {rule4_yield.sum()} records")

# Rule 5: Health score = 100 with Critical pest (suspicious)
rule5_suspicious = (df['health_score'] >= 98) & (df['pest_severity'] == 'Critical')
print(f"  -> Rule 5 (Health=100 + Critical Pest): {rule5_suspicious.sum()} records")

df['rule_based_flag'] = (rule1_dupes | rule2_pest | rule3_water | rule4_yield | rule5_suspicious).astype(int)
df['rule_details'] = ''
df.loc[rule1_dupes,     'rule_details'] += 'DuplicateRecord;'
df.loc[rule2_pest,      'rule_details'] += 'AbnormalPesticide;'
df.loc[rule3_water,     'rule_details'] += 'AbnormalIrrigation;'
df.loc[rule4_yield,     'rule_details'] += 'ZeroYield;'
df.loc[rule5_suspicious,'rule_details'] += 'SuspiciousHealth;'

# ════════════════════════════════════════════════════════════════════════════════
# METHOD 2: Z-SCORE
# ════════════════════════════════════════════════════════════════════════════════
print("\n[METHOD 2] Z-Score Anomaly Detection (threshold = ±3)")
z_scores = pd.DataFrame()
for col in TARGET_COLS:
    z_scores[f'z_{col}'] = np.abs(stats.zscore(df[col].fillna(df[col].median())))
df['zscore_max'] = z_scores.max(axis=1)
df['zscore_flag'] = (df['zscore_max'] > 3).astype(int)
print(f"  -> Z-Score anomalies (|z| > 3): {df['zscore_flag'].sum()} records")
print(f"  -> Max Z-score: {df['zscore_max'].max():.2f}")

# ════════════════════════════════════════════════════════════════════════════════
# METHOD 3: IQR METHOD
# ════════════════════════════════════════════════════════════════════════════════
print("\n[METHOD 3] IQR Anomaly Detection (1.5 x IQR fence)")
iqr_flags = pd.DataFrame(index=df.index)
iqr_summary = {}
for col in TARGET_COLS:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    flag  = (df[col] < lower) | (df[col] > upper)
    iqr_flags[col] = flag.astype(int)
    iqr_summary[col] = {'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
                         'Lower_Fence': lower, 'Upper_Fence': upper,
                         'Anomalies': flag.sum()}
    print(f"  -> {col}: {flag.sum()} anomalies (fence: [{lower:.2f}, {upper:.2f}])")

df['iqr_flag']   = (iqr_flags.sum(axis=1) > 0).astype(int)
df['iqr_count']  = iqr_flags.sum(axis=1)
print(f"  -> Total IQR-flagged records: {df['iqr_flag'].sum()}")

# ════════════════════════════════════════════════════════════════════════════════
# METHOD 4: ISOLATION FOREST
# ════════════════════════════════════════════════════════════════════════════════
print("\n[METHOD 4] Isolation Forest (sklearn)")
if SKLEARN_AVAILABLE:
    feat_cols = TARGET_COLS
    X = df[feat_cols].fillna(df[feat_cols].median())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    iso_forest = IsolationForest(n_estimators=200, contamination=0.05, random_state=42, n_jobs=-1)
    df['iso_pred']  = iso_forest.fit_predict(X_scaled)
    df['iso_score'] = iso_forest.decision_function(X_scaled)
    df['iso_flag']  = (df['iso_pred'] == -1).astype(int)
    print(f"  -> Isolation Forest anomalies (5% contamination): {df['iso_flag'].sum()} records")
else:
    df['iso_pred']  = 1
    df['iso_score'] = 0.0
    df['iso_flag']  = 0
    print("  -> Isolation Forest skipped (sklearn not available)")

# ════════════════════════════════════════════════════════════════════════════════
# COMBINED FRAUD SCORE
# ════════════════════════════════════════════════════════════════════════════════
df['fraud_score'] = (
    df['rule_based_flag'] * 3 +
    df['zscore_flag']     * 2 +
    df['iqr_flag']        * 1 +
    df['iso_flag']        * 2
)
_max_score = max(df['fraud_score'].max(), 9)  # ensure bins are always distinct
df['fraud_level'] = pd.cut(
    df['fraud_score'],
    bins=[-1, 0, 2, 4, _max_score + 1],
    labels=['Clean', 'Suspicious', 'High Risk', 'Critical'],
    duplicates='drop'
)
df['fraud_level'] = df['fraud_level'].cat.add_categories(['Clean']).fillna('Clean') if df['fraud_level'].isnull().any() else df['fraud_level']

fraud_summary = df['fraud_level'].value_counts().reset_index()
fraud_summary.columns = ['Fraud Level','Count']
fraud_summary['%'] = (fraud_summary['Count'] / len(df) * 100).round(2)
print("\n  COMBINED FRAUD SCORE DISTRIBUTION:")
print(fraud_summary.to_string(index=False))

# Export flagged records
flagged = df[df['fraud_score'] > 0][[
    'record_id', 'farmer_id', 'crop_name', 'location_name', 'monitoring_date',
    'pesticide_l_ha', 'water_usage_l', 'crop_yield_tons_ha', 'health_score',
    'rule_based_flag', 'rule_details', 'zscore_flag', 'zscore_max',
    'iqr_flag', 'iqr_count', 'iso_flag', 'iso_score', 'fraud_score', 'fraud_level'
]].sort_values('fraud_score', ascending=False)

flagged.to_csv(os.path.join(DATA_DIR, 'Anomaly_Report.csv'), index=False)
print(f"\n  -> Anomaly_Report.csv saved: {len(flagged)} flagged records")

# ════════════════════════════════════════════════════════════════════════════════
# VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════════

PALETTE = ['#38bdf8','#818cf8','#34d399','#fb923c','#f472b6',
           '#a78bfa','#4ade80','#facc15','#f87171','#22d3ee']

# Chart 1: Fraud Level Distribution
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#0f172a')
    fig.suptitle('Fraud & Anomaly Detection – Distribution Analysis', fontsize=17, fontweight='bold', color='white')
    fl_colors = {'Clean':'#4ade80','Suspicious':'#facc15','High Risk':'#fb923c','Critical':'#f87171'}

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    fl_cnt = df['fraud_level'].value_counts()
    bars = ax1.bar(fl_cnt.index, fl_cnt.values,
                   color=[fl_colors.get(str(k),'#818cf8') for k in fl_cnt.index],
                   edgecolor='none', width=0.65)
    for bar in bars:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{int(bar.get_height())}', ha='center', color='white', fontweight='bold', fontsize=12)
    ax1.set_title('Records by Fraud Level', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Fraud Level', color='white'); ax1.set_ylabel('Count', color='white')

    ax2 = axes[1]; ax2.set_facecolor('#0f172a')
    wedges, texts, autotexts = ax2.pie(fl_cnt.values, labels=fl_cnt.index,
                                       autopct='%1.1f%%',
                                       colors=[fl_colors.get(str(k),'#818cf8') for k in fl_cnt.index],
                                       startangle=90, wedgeprops=dict(width=0.6, edgecolor='#0f172a'))
    for t in texts + autotexts:
        t.set_color('white'); t.set_fontsize(11)
    ax2.set_title('Fraud Level Proportions', fontsize=13, fontweight='bold', color='white')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'ANOM_01_FraudDistribution.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("\n  -> Chart 1: Fraud Distribution saved")

# Chart 2: Z-Score Distribution per Feature
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor='#0f172a')
    fig.suptitle('Z-Score Distribution by Feature – Anomaly Highlights', fontsize=16, fontweight='bold', color='white')
    axes = axes.flatten()
    for i, col in enumerate(TARGET_COLS):
        ax = axes[i]; ax.set_facecolor('#1e293b')
        z_col = np.abs(stats.zscore(df[col].fillna(df[col].median())))
        normal = z_col[z_col <= 3]
        anomaly = z_col[z_col > 3]
        ax.hist(normal, bins=40, color='#38bdf8', alpha=0.8, label='Normal', edgecolor='none')
        ax.hist(anomaly, bins=40, color='#f87171', alpha=0.9, label='Anomaly', edgecolor='none')
        ax.axvline(x=3, color='#facc15', linestyle='--', linewidth=2)
        ax.set_title(col.replace('_',' ').title(), color='white', fontsize=10, fontweight='bold')
        ax.set_xlabel('|Z-Score|', color='white', fontsize=8)
        ax.legend(fontsize=8, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'ANOM_02_ZScoreDistribution.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 2: Z-Score Distribution saved")

# Chart 3: IQR Fence Visualization
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), facecolor='#0f172a')
    fig.suptitle('IQR Anomaly Detection – Box Plot with Fences', fontsize=16, fontweight='bold', color='white')
    axes = axes.flatten()
    for i, col in enumerate(TARGET_COLS):
        ax = axes[i]; ax.set_facecolor('#1e293b')
        Q1  = df[col].quantile(0.25)
        Q3  = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        normal_data  = df[col][(df[col] >= lower) & (df[col] <= upper)]
        anomaly_data = df[col][(df[col] < lower)  | (df[col] > upper)]
        ax.scatter(range(len(normal_data)), normal_data.values, s=8, color='#38bdf8', alpha=0.4, label='Normal')
        ax.scatter(anomaly_data.index, anomaly_data.values, s=30, color='#f87171', alpha=0.8, zorder=5, label=f'Anomaly ({len(anomaly_data)})')
        ax.axhline(y=upper, color='#facc15', linestyle='--', linewidth=1.5, label=f'Upper ({upper:.1f})')
        ax.axhline(y=lower, color='#fb923c', linestyle='--', linewidth=1.5, label=f'Lower ({lower:.1f})')
        ax.set_title(col.replace('_',' ').title(), color='white', fontsize=10, fontweight='bold')
        ax.legend(fontsize=7, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'ANOM_03_IQRFences.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 3: IQR Fences saved")

# Chart 4: Isolation Forest Score Plot
with plt.rc_context(STYLE):
    fig, axes = plt.subplots(1, 2, figsize=(18, 7), facecolor='#0f172a')
    fig.suptitle('Isolation Forest Anomaly Detection', fontsize=17, fontweight='bold', color='white')

    ax1 = axes[0]; ax1.set_facecolor('#1e293b')
    colors_iso = ['#f87171' if f == 1 else '#38bdf8' for f in df['iso_flag']]
    ax1.scatter(df['pesticide_l_ha'], df['crop_yield_tons_ha'],
                c=colors_iso, s=20, alpha=0.5)
    normal_patch  = mpatches.Patch(color='#38bdf8', label='Normal')
    anomaly_patch = mpatches.Patch(color='#f87171', label='Anomaly')
    ax1.legend(handles=[normal_patch, anomaly_patch], fontsize=10, framealpha=0.3)
    ax1.set_title('Pesticide vs Yield – Isolation Forest', fontsize=13, fontweight='bold', color='white')
    ax1.set_xlabel('Pesticide (L/ha)', color='white'); ax1.set_ylabel('Yield (t/ha)', color='white')

    ax2 = axes[1]; ax2.set_facecolor('#1e293b')
    ax2.hist(df['iso_score'], bins=50, color='#818cf8', alpha=0.8, edgecolor='none')
    ax2.axvline(x=df[df['iso_flag']==1]['iso_score'].max(), color='#f87171', linewidth=2,
                linestyle='--', label='Anomaly Threshold')
    ax2.set_title('Isolation Forest Anomaly Score Distribution', fontsize=13, fontweight='bold', color='white')
    ax2.set_xlabel('Anomaly Score (lower = more anomalous)', color='white')
    ax2.set_ylabel('Count', color='white')
    ax2.legend(fontsize=10, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'ANOM_04_IsolationForest.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 4: Isolation Forest saved")

# Chart 5: Fraud Score Heatmap by Region & Crop
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    fraud_pivot = df.pivot_table(values='fraud_score', index='location_name',
                                 columns='crop_name', aggfunc='mean').round(2)
    sns.heatmap(fraud_pivot, ax=ax, cmap='RdYlGn_r', annot=True, fmt='.1f',
                linewidths=0.5, cbar_kws={'label': 'Avg Fraud Score', 'shrink': 0.8},
                annot_kws={'size': 8})
    ax.set_title('Fraud Score Heatmap – Region x Crop', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Crop Type', color='white'); ax.set_ylabel('Region', color='white')
    ax.tick_params(colors='white')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, 'ANOM_05_FraudHeatmap.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 5: Fraud Heatmap saved")

# Chart 6: Anomaly Dashboard Summary
with plt.rc_context(STYLE):
    fig = plt.figure(figsize=(20, 10), facecolor='#0f172a')
    fig.suptitle('AgriShield Analytics – Anomaly Detection Dashboard | Day 5',
                 fontsize=20, fontweight='bold', color='white')
    gs = GridSpec(2, 4, figure=fig, hspace=0.5, wspace=0.4)

    # KPI cards
    kpis = [
        ('Total Records',   f"{len(df):,}",                     '#38bdf8'),
        ('Rule Violations', f"{df['rule_based_flag'].sum():,}",  '#fb923c'),
        ('Z-Score Flags',   f"{df['zscore_flag'].sum():,}",      '#f472b6'),
        ('ISO Forest Flags',f"{df['iso_flag'].sum():,}",         '#f87171'),
    ]
    for i, (label, value, color) in enumerate(kpis):
        ax_k = fig.add_subplot(gs[0, i])
        ax_k.set_facecolor('#1e293b')
        ax_k.set_xlim(0, 1); ax_k.set_ylim(0, 1)
        ax_k.text(0.5, 0.62, value, ha='center', va='center',
                  fontsize=26, fontweight='bold', color=color)
        ax_k.text(0.5, 0.25, label, ha='center', va='center', fontsize=10, color='#94a3b8')
        for spine in ax_k.spines.values():
            spine.set_edgecolor(color); spine.set_linewidth(2)
        ax_k.set_xticks([]); ax_k.set_yticks([])

    # Fraud level by location
    ax_loc = fig.add_subplot(gs[1, :2])
    ax_loc.set_facecolor('#1e293b')
    loc_fraud = df.groupby('location_name')['fraud_score'].mean().sort_values(ascending=False)
    bars = ax_loc.bar(loc_fraud.index, loc_fraud.values,
                      color=[PALETTE[i % len(PALETTE)] for i in range(len(loc_fraud))],
                      edgecolor='none', width=0.7)
    ax_loc.set_title('Avg Fraud Score by Region', fontsize=12, fontweight='bold', color='white')
    ax_loc.set_xlabel('Region', color='white'); ax_loc.set_ylabel('Avg Fraud Score', color='white')
    plt.setp(ax_loc.xaxis.get_majorticklabels(), rotation=20, ha='right')

    # Monthly anomaly trend
    ax_trend = fig.add_subplot(gs[1, 2:])
    ax_trend.set_facecolor('#1e293b')
    monthly_fraud = df.groupby(['year','month'])['fraud_score'].sum().reset_index()
    monthly_fraud['period'] = monthly_fraud['year'].astype(str) + '-M' + monthly_fraud['month'].astype(str).str.zfill(2)
    ax_trend.fill_between(range(len(monthly_fraud)), monthly_fraud['fraud_score'],
                          color='#f87171', alpha=0.5)
    ax_trend.plot(range(len(monthly_fraud)), monthly_fraud['fraud_score'],
                  color='#f87171', linewidth=2)
    ax_trend.set_xticks(range(0, len(monthly_fraud), 3))
    ax_trend.set_xticklabels(monthly_fraud['period'].iloc[::3], rotation=30, ha='right', fontsize=7)
    ax_trend.set_title('Monthly Anomaly Score Trend', fontsize=12, fontweight='bold', color='white')
    ax_trend.set_ylabel('Total Fraud Score', color='white', fontsize=9)

    plt.savefig(os.path.join(IMG_DIR, 'ANOM_06_AnomalyDashboard.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  -> Chart 6: Anomaly Dashboard saved")

print("\n✅ Day 5 – Fraud & Anomaly Detection Complete! (6 charts + Anomaly_Report.csv)")

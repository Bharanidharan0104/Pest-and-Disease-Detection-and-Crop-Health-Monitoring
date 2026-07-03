"""
AgriShield Analytics – Day 3: Farmer RFM Segmentation
Author: AgriShield Analytics Team
Date: 2024
Description:
    RFM Analysis adapted for Agriculture:
    R (Recency)   = Days since Last Crop Monitoring Date
    F (Frequency) = Number of Crop Health Records
    M (Monetary)  = Total Crop Yield (tons)
    Segments: Champions, Loyal Farmers, Potential Farmers, At Risk, Lost Farmers
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'Dataset')
IMG_DIR  = os.path.join(BASE_DIR, '..', 'Images')
os.makedirs(IMG_DIR, exist_ok=True)

print("=" * 60)
print("  AgriShield Analytics – Day 3: RFM Segmentation")
print("=" * 60)

df = pd.read_csv(os.path.join(DATA_DIR, 'Cleaned_AgriShield_Data.csv'))
df['monitoring_date'] = pd.to_datetime(df['monitoring_date'])

# ── Compute RFM Metrics ────────────────────────────────────────────────────────
snapshot_date = df['monitoring_date'].max() + pd.Timedelta(days=1)
rfm = df.groupby('farmer_id').agg(
    Recency   = ('monitoring_date', lambda x: (snapshot_date - x.max()).days),
    Frequency = ('record_id', 'count'),
    Monetary  = ('crop_yield_tons_ha', 'sum')
).reset_index()
rfm['Monetary'] = rfm['Monetary'].round(2)

print(f"\n  Farmers analyzed: {len(rfm)}")
print(rfm.describe().round(2).to_string())

# ── RFM Scoring (1–5 scale) ───────────────────────────────────────────────────
rfm['R_Score'] = pd.qcut(rfm['Recency'],   q=5, labels=[5,4,3,2,1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'),  q=5, labels=[1,2,3,4,5]).astype(int)
rfm['RFM_Score']   = rfm['R_Score']*100 + rfm['F_Score']*10 + rfm['M_Score']
rfm['RFM_Total']   = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']
rfm['RFM_Average'] = (rfm['RFM_Total'] / 3).round(2)

# ── Segmentation ──────────────────────────────────────────────────────────────
def segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:   return 'Champions'
    elif r >= 3 and f >= 3:            return 'Loyal Farmers'
    elif r >= 3 and f < 3:             return 'Potential Farmers'
    elif r < 3 and f >= 3:             return 'At Risk'
    else:                              return 'Lost Farmers'

rfm['Segment'] = rfm.apply(segment, axis=1)
seg_counts = rfm['Segment'].value_counts()
print("\n  Segment Distribution:")
print(seg_counts.to_string())

# ── Segment Summary Table ─────────────────────────────────────────────────────
seg_summary = rfm.groupby('Segment').agg(
    Count     = ('farmer_id', 'count'),
    Avg_Recency   = ('Recency', 'mean'),
    Avg_Frequency = ('Frequency', 'mean'),
    Avg_Monetary  = ('Monetary', 'mean'),
    Avg_RFM_Score = ('RFM_Average', 'mean')
).round(2).reset_index()
seg_summary['Pct'] = (seg_summary['Count']/len(rfm)*100).round(1)
print("\n  Segment Summary:")
print(seg_summary.to_string(index=False))

rfm.to_csv(os.path.join(DATA_DIR, 'RFM_Analysis.csv'), index=False)
seg_summary.to_csv(os.path.join(DATA_DIR, 'RFM_Segment_Summary.csv'), index=False)

# ── VISUALIZATIONS ────────────────────────────────────────────────────────────
STYLE = {'figure.facecolor':'#0f172a','axes.facecolor':'#1e293b',
         'axes.labelcolor':'white','xtick.color':'white','ytick.color':'white',
         'text.color':'white','grid.color':'#334155','axes.grid':True}
seg_colors = {'Champions':'#22d3ee','Loyal Farmers':'#4ade80',
              'Potential Farmers':'#facc15','At Risk':'#fb923c','Lost Farmers':'#f87171'}
color_list = [seg_colors.get(s,'#818cf8') for s in seg_counts.index]

# Chart 1: Bar Chart
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(12,6), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    bars = ax.bar(seg_counts.index, seg_counts.values, color=color_list, edgecolor='none', width=0.6)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                str(int(bar.get_height())), ha='center', va='bottom', color='white', fontweight='bold', fontsize=12)
    ax.set_title('Farmer Segment Distribution – RFM Analysis', fontsize=16, fontweight='bold', color='white', pad=15)
    ax.set_xlabel('Segment', color='white', fontsize=12)
    ax.set_ylabel('Number of Farmers', color='white', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR,'RFM_01_BarChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → RFM Bar Chart saved")

# Chart 2: Donut Chart
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(9,8), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    wedges, texts, autotexts = ax.pie(
        seg_counts.values, labels=seg_counts.index,
        autopct='%1.1f%%', colors=color_list, startangle=90,
        wedgeprops=dict(width=0.55, edgecolor='#0f172a', linewidth=2),
        pctdistance=0.78)
    for t in texts+autotexts:
        t.set_color('white'); t.set_fontsize(11)
    ax.text(0, 0, f'{len(rfm)}\nFarmers', ha='center', va='center',
            fontsize=16, fontweight='bold', color='white')
    ax.set_title('Farmer RFM Segments – Donut Chart', fontsize=15, fontweight='bold', color='white', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR,'RFM_02_DonutChart.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → RFM Donut Chart saved")

# Chart 3: RFM Scatter (R vs F, colored by segment)
with plt.rc_context(STYLE):
    fig, ax = plt.subplots(figsize=(11,8), facecolor='#0f172a')
    ax.set_facecolor('#1e293b')
    for seg, grp in rfm.groupby('Segment'):
        ax.scatter(grp['Recency'], grp['Frequency'],
                   c=seg_colors.get(seg,'#818cf8'), label=seg, alpha=0.75, s=80)
    ax.set_xlabel('Recency (days)', color='white', fontsize=12)
    ax.set_ylabel('Frequency (records)', color='white', fontsize=12)
    ax.set_title('RFM Scatter – Recency vs Frequency by Segment', fontsize=14, fontweight='bold', color='white')
    ax.legend(fontsize=10, framealpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR,'RFM_03_Scatter.png'), dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.close()
    print("  → RFM Scatter saved")

print("\n✅ RFM Analysis Complete!")

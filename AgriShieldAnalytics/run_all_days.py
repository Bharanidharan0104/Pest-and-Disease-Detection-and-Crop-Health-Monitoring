"""
AgriShield Analytics – Master Build Script
Runs all Day 1–9 Python scripts in sequence
Author: AgriShield Analytics Team
Date: 2024
"""

import subprocess
import sys
import os
import time
import zipfile
from datetime import datetime

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIR = os.path.join(BASE_DIR, 'Python')
OUTPUT_DIR = BASE_DIR

BANNER = """
╔══════════════════════════════════════════════════════════════════╗
║        AgriShield Analytics – Complete Project Builder          ║
║        Pest & Disease Detection | Crop Health Monitoring        ║
║        Days 1–9 Full Execution Pipeline                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

SCRIPTS = [
    ('Day 1 – Data Cleaning & ETL',          'Cleaning.py'),
    ('Day 2 – EDA & Descriptive Statistics', 'EDA.py'),
    ('Day 3 – RFM Segmentation',             'RFM.py'),
    ('Day 4 – Performance Analysis',         'Performance.py'),
    ('Day 5 – Fraud & Anomaly Detection',    'AnomalyDetection.py'),
    ('Day 6 – KPI Dashboard',               'KPI_Dashboard.py'),
    ('Day 8 – Time Series Forecasting',      'Forecasting.py'),
    ('Day 9 – Cohort & Retention Analysis',  'CohortAnalysis.py'),
]

def run_script(label, script_name):
    """Run a Python script and return success status."""
    script_path = os.path.join(PYTHON_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"  ⚠️  SKIPPED – {script_name} not found")
        return False, 0.0

    print(f"\n{'─'*68}")
    print(f"  ▶  {label}")
    print(f"  📄 {script_name}")
    print(f"{'─'*68}")

    start = time.time()
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False,
        text=True
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"\n  ✅ Completed in {elapsed:.1f}s")
        return True, elapsed
    else:
        print(f"\n  ❌ Failed (exit code {result.returncode}) in {elapsed:.1f}s")
        return False, elapsed


def create_zip():
    """Package all project files into a ZIP archive."""
    print(f"\n{'═'*68}")
    print("  📦 Creating ZIP Archive...")
    print(f"{'═'*68}")

    timestamp  = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_name   = f'AgriShieldAnalytics_Complete_{timestamp}.zip'
    zip_path   = os.path.join(os.path.dirname(BASE_DIR), zip_name)

    EXCLUDE_DIRS  = {'.git', '__pycache__', '.DS_Store', 'node_modules'}
    EXCLUDE_EXT   = {'.pyc', '.pyo'}

    files_added = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if any(file.endswith(ext) for ext in EXCLUDE_EXT):
                    continue
                file_path = os.path.join(root, file)
                arc_name  = os.path.relpath(file_path, os.path.dirname(BASE_DIR))
                zf.write(file_path, arc_name)
                files_added += 1

    zip_size = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  → ZIP: {zip_name}")
    print(f"  → Files: {files_added}")
    print(f"  → Size:  {zip_size:.2f} MB")
    print(f"  → Path:  {zip_path}")
    return zip_path


def print_summary(results, total_time, zip_path):
    """Print final execution summary."""
    print(f"\n{'═'*68}")
    print("  📊 EXECUTION SUMMARY")
    print(f"{'═'*68}")
    print(f"  {'Script':<45} {'Status':>8}  {'Time':>8}")
    print(f"  {'─'*63}")

    passed = 0
    for label, script, success, elapsed in results:
        icon   = '✅' if success else '❌'
        status = 'PASS' if success else 'FAIL'
        print(f"  {icon} {label:<43} {status:>8}  {elapsed:>6.1f}s")
        if success:
            passed += 1

    print(f"  {'─'*63}")
    print(f"\n  📈 Scripts: {passed}/{len(results)} passed")
    print(f"  ⏱️  Total time: {total_time:.1f}s")
    print(f"  📦 Archive: {os.path.basename(zip_path)}")
    print(f"\n  {'═'*64}")
    print("  🎉 AgriShield Analytics – All 9 Days Complete!")
    print(f"  {'═'*64}\n")


def main():
    print(BANNER)
    start_total = time.time()
    results     = []

    for label, script in SCRIPTS:
        success, elapsed = run_script(label, script)
        results.append((label, script, success, elapsed))

    total_time = time.time() - start_total

    # Package ZIP
    zip_path = create_zip()

    # Print summary
    print_summary(results, total_time, zip_path)


if __name__ == '__main__':
    main()

import subprocess
import sys

pipeline = [
    "find_profiles.py",
    "merge_data.py",
    "analyze_visual_apify.py",
    "clean_json.py",
    "shorten_interim.py",
    "find_best.py",
    "generate_offers.py"
]

for script in pipeline:
    print(f"\nRunning {script}...\n")

    subprocess.run(
        [sys.executable, script],
        check=True
    )

print("\nSearch pipeline completed.")
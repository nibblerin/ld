import subprocess
import sys

pipeline = [
    "get_data.py",
    "run_apify.py",
    "merge_data.py",
    "analyze_visual_apify.py",
    "clean_json.py",
    "shorten_interim.py",
    "ask_llm_for_ideal.py",
    "ask_llm_for_queries.py"
]

for script in pipeline:
    print(f"\nRunning {script}...\n")

    subprocess.run(
        [sys.executable, script],
        check=True
    )

print("\nIdeal pipeline completed.")
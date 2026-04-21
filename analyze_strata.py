import sys
import os
import glob
import csv

# -----------------------------
# Hardcoded model parameters
# -----------------------------
# Average commits per tenant per day
C = 50   # adjust if you want

# Number of tenants of this type
N = 100  # adjust if you want

if len(sys.argv) < 2:
    print("Usage: python analyze_strata.py <directory_with_strata_csv>")
    print("adding code for debugging")
    print("Adding code for creating a conflict during merge")
    sys.exit(1)

directory = sys.argv[1]

csv_files = sorted(glob.glob(os.path.join(directory, "strata*.csv")))
if not csv_files:
    print("No strata*.csv files found in:", directory)
    sys.exit(1)

print(f"Found {len(csv_files)} strata CSV files in {directory}\n")

print("Assumptions:")
print(f"  Commits per tenant per day (C): {C}")
print(f"  Number of tenants (N):          {N}")
print()

print(
    f"{'File':25} {'Commits':8} {'Init_MB':8} {'Final_MB':9} "
    f"{'Slope_MB/commit':16} {'Daily_MB/tenant':16} {'Daily_MB_all_tenants':22}"
)

print("-" * 110)

for csv_file in csv_files:
    commit_numbers = []
    sizes_mb = []

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            commit_numbers.append(int(row["commit_no"]))
            sizes_mb.append(int(row["git_size_bytes"]) / (1024 * 1024))

    if len(commit_numbers) < 2:
        continue

    initial_mb = sizes_mb[0]
    final_mb = sizes_mb[-1]
    num_commits = commit_numbers[-1] - commit_numbers[0] + 1

    # Slope: Δsize / (commits - 1)
    slope = (final_mb - initial_mb) / (num_commits - 1)

    # Daily growth per tenant and across N tenants
    daily_per_tenant = slope * C
    daily_all = daily_per_tenant * N

    print(
        f"{os.path.basename(csv_file):25} "
        f"{num_commits:8d} "
        f"{initial_mb:8.2f} "
        f"{final_mb:9.2f} "
        f"{slope:16.4f} "
        f"{daily_per_tenant:16.2f} "
        f"{daily_all:22.2f}"
    )


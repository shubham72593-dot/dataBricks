import sys
import matplotlib.pyplot as plt
import csv

if len(sys.argv) < 2:
    print("Usage: python plot_git_growth.py <csvfile>")
    sys.exit(1)

csv_file = sys.argv[1]

commit_numbers = []
git_sizes_mb = []
loose_objs = []
#packfiles = []

with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        commit_numbers.append(int(row["commit_no"]))
        git_sizes_mb.append(int(row["git_size_bytes"]) / (1024 * 1024))
        loose_objs.append(int(row["loose_objs"]))
#        packfiles.append(int(row["packfiles"]))

plt.figure(figsize=(10, 6))

# Primary curve: Git size in MB
plt.plot(commit_numbers, git_sizes_mb, marker='o', label=".git size (MB)")

# Loose objects (scaled for visibility)
plt.plot(commit_numbers, loose_objs, linestyle='--', label="Loose objects (count)")

# Packfiles count
#plt.plot(commit_numbers, packfiles, linestyle=':', label="Packfiles (count)")

plt.title(f"Git Storage Growth: {csv_file}")
plt.xlabel("Commit Number")
plt.ylabel("Storage (MB) / Object Count")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# precompute_PPI_distances

Computes the shortest path distance between all pairs based on the Human PPI network and saves it as a distance matrix for use in the proximity computation step.

-------------------------------------------------------------------------------------------

## Contents
```
precompute_PPI_distances/                     
├── input/
│   └── Human_PPI.pkl                         # Human PPI network (pickled NetworkX graph)
└── src/
    └── saving_the_all_pair_distance_matrix.py
```
--------------------------------------------------------------------------------------------

What it does

1. Loads the Human PPI network from [Human_PPI.pkl](./input/Human_PPI.pkl)
2. Extracts the Largest Connected Component (LCC) to ensure all nodes are reachable
3. Computes all-pair shortest path distances using "netmedpy.all_pair_distances()"
4. Saves the distance matrix to "proximity_computation/input/shortest_path_distances_Human_PPI.pkl"

---------------------------------------------------------------------------------------------

Usage

Bash Command

```bash
cd src
python saving_the_all_pair_distance_matrix.py
````

Key parameters (edit inside the script)

| Parameter | Default | Description |
|-----------|---------|-------------|
| "n_procs" | "12" | Number of parallel CPU processes — set to at least 5 |
| "n_tasks" | "1000" | Number of tasks to split the computation into |
| "distance" | "shortest_path" | Distance metric passed to "netmedpy" |

-----------------------------------------------------------------------------------------------

Runtime & Resources

| Resource | Requirement |
|----------|-------------|
| CPUs | ≥ 5 (12 recommended) |
| Disk space | ~3 GB for output file |
| Runtime | ~5 minutes at 12 CPUs |

---------------------------------------------------------------------------------------------------

## Output

| File | Destination |
|------|-------------|
| "shortest_path_distances_Human_PPI.pkl" | "proximity_computation/input/" |

> This file is written directly into the `proximity_computation/input/` directory and is required before running Step 2.




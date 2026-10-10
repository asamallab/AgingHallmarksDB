# AgingHallmarksDB - Network Proximity Analysis

This repository computes network proximity between aging hallmark genes and age-related disease genes on the Human Protein-Protein Interaction (PPI) network, using the [netmedpy](https://github.com/menicgiulia/NetMedPy) library. The computation runs in two sequential steps: 
- precomputing the shortest path distances between all-pairs on the PPI graph
- scoring proximity for each disease–aging hallmark pair


## Contributors

- [Rahul Tiwari](https://github.com/rtiwari-compbio)
- Priyotosh Sil

-----------------------------------------------------------------------------------------------------------------------------

## Reference

This repository is associated with the manuscript:  
Rahul Tiwari, Mridhula Balaji, Nikhil Chivukula, Priyotosh Sil, and Areejit Samal\*,<br>
[An integrated resource for systems-level analysis of aging hallmarks and associated genes](https://doi.org/10.1007/s10522-026-10520-2), Biogerontology, 27: 173 (2026).<br>
(\* Corresponding author: [asamal@imsc.res.in](mailto:asamal@imsc.res.in))  

-----------------------------------------------------------------------------------------------------------------------------

## Repository Structure

```
.
├── requirements.txt                              # Top-level dependencies for the full computation
├── precompute_PPI_distances/     
│   ├── input/
│   │   └── Human_PPI.pkl                         # Human PPI network (pickled NetworkX graph)
│   └── src/
│       └── saving_the_all_pair_distance_matrix.py
│
└── proximity_computation/                    
    ├── input/
    │   ├── aging_hallmark_consensus.csv           # Aging hallmark gene sets (Entrez ID + Aging Hallmark)
    │   ├── disease_associated_gene.csv            # Disease–gene associations (Entrez ID + Disease)
    │   ├── Human_PPI.pkl                          # Human PPI network
    │   └── shortest_path_distances_Human_PPI.pkl  # Output from Step 1 (~3 GB)
    ├── src/
    │   └── proximity_computation.py
    └── output/
        └── proximity_<Disease>_vs_Aging.tsv       # One TSV per disease
```

--------------------------------------------------------------------------------------------------------------------------

## Computation Overview
```
Human_PPI.pkl
      │
      ▼
[Step 1] saving_the_all_pair_distance_matrix.py
      │  Extracts LCC, computes shortest distances between all pairs (netmedpy)
      │  Runtime: ~5 min | CPUs: 12 | Output: ~3 GB
      │
      ▼
shortest_path_distances_Human_PPI.pkl ───────────┐
                                                 │
aging_hallmark_consensus.csv ──┐                 │
disease_associated_gene.csv ───┤                 │
Human_PPI.pkl ─────────────────┤                 │
                               ▼                 ▼
                    [Step 2] proximity_computation.py
                         netmedpy.screening()
                         null model: log_binning
                         metrics: raw_amspl, z_score, p_value
                               │
                               ▼
               proximity_<Disease>_vs_Aging.tsv (per disease)
```

---------------------------------------------------------------------------------------------------------------------------

### Step 1 — Precompute PPI Distances

>Must be run before Step 2.

Loads the Human PPI network, extracts its Largest Connected Component (LCC), and computes the shortest path distances between all pairs and stores it as a distance matrix. The result is saved as a pickle file and used as input in Step 2.

### Step 2 - Proximity computation

Loads Human PPI and shortest path distance matrix file to calculate the network proximity between two subnetworks.

-------------------------------------------------------------------------------------------------------------------------

## Dependencies

To ensure that the dependencies for this computation do not conflict with your system packages, it is highly recommended to run this project inside a virtual environment.

1. Create a python virtual environment

```bash
python -m venv venv
```

2. In macOS and linux

```bash
source venv/bin/activate
```

3. Install requirements.txt

```bash
pip install -r requirements.txt
```

----------------------------------------------------------------------------------------------------------------------------

## Notes

- Both scripts restrict the PPI network to its Largest Connected Component (LCC) before any computation.
- Gene IDs (Entrez ID) are matched as strings.
- The distance matrix (.pkl) file is written directly into "proximity_computation/input/" after Step 1.

------------------------------------------------------------------------------------------------------------------------------

## Citation

If you use the code or data in this repository, please cite the following manuscript:

Rahul Tiwari, Mridhula Balaji, Nikhil Chivukula, Priyotosh Sil, and Areejit Samal,<br>
[An integrated resource for systems-level analysis of aging hallmarks and associated genes](https://doi.org/10.64898/2026.05.29.728838), bioRxiv 2026.05.29.728838 (2026).

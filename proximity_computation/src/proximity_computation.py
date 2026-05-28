import os
import pandas as pd
import pickle as pkl
import networkx as nx
import netmedpy

properties_to_compute = ["raw_amspl", "z_score", "p_value_single_tail"]
null_model = 'log_binning'
symmetric = False
n_procs = 5

ppi_path = '../input/Human_PPI.pkl'
sp_dist_path = '../input/shortest_path_distances_Human_PPI.pkl'
aging_file_path = '../input/aging_hallmark_consensus.csv'
disease_file_path = '../input/disease_associated_gene.csv' 
output_folder_path = '../output'

os.makedirs(output_folder_path, exist_ok=True)

print("Loading PPI network...")
with open(ppi_path, 'rb') as file1:
    ppi = pkl.load(file1)
    
lcc_nodes = max(nx.connected_components(ppi), key=len)
ppi = ppi.subgraph(lcc_nodes).copy()
ppi_nodes_set = set(ppi.nodes)

print("Loading shortest path distances...")
with open(sp_dist_path, 'rb') as file4:
    sp_distance = pkl.load(file4)

print("Processing aging targets...")
aging_df = pd.read_csv(aging_file_path, sep=None, engine='python', dtype=str)
aging_df.columns = aging_df.columns.str.strip()

if "Entrez ID" not in aging_df.columns or "Aging Hallmark" not in aging_df.columns:
    print(f"Detected columns: {aging_df.columns.tolist()}")
    raise ValueError("Aging CSV must contain 'Entrez ID' and 'Aging Hallmark' columns.")

aging_df_clean = aging_df.dropna(subset=["Entrez ID"])
aging_target_dict = aging_df_clean.groupby("Aging Hallmark")["Entrez ID"].apply(set).to_dict()

aging_target_data = {
    hallmark: targets & ppi_nodes_set 
    for hallmark, targets in aging_target_dict.items() 
    if len(targets & ppi_nodes_set) > 0
}

print("Processing disease targets...")
disease_df = pd.read_csv(disease_file_path, sep=None, engine='python', dtype=str)
disease_df.columns = disease_df.columns.str.strip()

if "Entrez ID" not in disease_df.columns or "Disease" not in disease_df.columns:
    print(f"Detected columns: {disease_df.columns.tolist()}")
    raise ValueError("Disease CSV must contain 'Entrez ID' and 'Disease' columns.")

disease_df_clean = disease_df.dropna(subset=["Entrez ID", "Disease"])

disease_target_dict = {}
for _, row in disease_df_clean.iterrows():
    entrez_id = row["Entrez ID"]
    if entrez_id not in ppi_nodes_set:
        continue 
    
    diseases = [d.strip() for d in row["Disease"].split('|')]
    
    for d in diseases:
        if d not in disease_target_dict:
            disease_target_dict[d] = set()
        disease_target_dict[d].add(entrez_id)

if not disease_target_dict:
    raise ValueError("No valid disease targets found in the PPI network.")

print(f"Found {len(disease_target_dict)} unique diseases in the file.")

for disease_name, disease_targets in disease_target_dict.items():
    print(f"\n--- Calculating proximity for {len(aging_target_data)} Hallmarks against {disease_name} ---")
    
    current_disease_data = {disease_name: disease_targets}
    
    screen_data = netmedpy.screening(
        aging_target_data, 
        current_disease_data, 
        ppi, 
        sp_distance, 
        score="proximity", 
        properties=properties_to_compute,
        null_model=null_model,
        symmetric=symmetric,
        n_iter=1000, 
        n_procs=n_procs
    )

    renamed_dfs = [
        df.rename(columns={disease_name: key})
        for key, df in screen_data.items()
    ]

    final_df = pd.concat(renamed_dfs, axis=1)
    final_df = final_df.reset_index()
    final_df = final_df.rename(columns={"index": "Aging_Hallmark"})
    final_df.columns = ["Aging_Hallmark"] + properties_to_compute

    safe_disease_name = disease_name.replace(" ", "_").replace("/", "_")
    output_filename = f"../output/proximity_{safe_disease_name}_vs_Aging.tsv"
    
    final_df.to_csv(output_filename, sep='\t', index=False)
    print(f"Saved results to: {output_filename}")

print("\nAll proximity calculations completed successfully.")

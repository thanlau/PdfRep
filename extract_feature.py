# Extract Paths from PDF Files and Generate Graph Features

# This script extracts object paths from PDF files using the pdf_genome library 
# and computes graph-based features from these paths.

# How to Use:
# 1. Replace the `folder_path` variable with the path to your PDF files.
# 2. Replace the existing pdf_genome.py file in the pdfrw library path with the pdf_genome.py in this repo.

import pickle
import os
import numpy as np
import networkx as nx
from pdf_genome import PdfGenome

def is_picklable(obj):
    """Check if an object can be pickled."""
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError):
        return False

def extract_graph_features_root(result):
    """
    Use the extracted paths to create a directed graph and compute various graph features.

    Parameters:
    result (dict): A dictionary containing the filename and the extracted paths.

    Returns:
    dict: A dictionary of computed graph features, including filename.
    """
    G = nx.DiGraph()
    filename = result["filename"]
    edges_list = result["paths"]

    # Add edges to the graph from the paths.
    for edge in edges_list:
        for i in range(len(edge) - 1):
            G.add_edge(edge[i], edge[i + 1])

    children_count = [degree for _, degree in G.out_degree()]

    # Compute graph-based features.
    features = {
        'num_nodes': G.number_of_nodes(),
        'avg_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
        'density': nx.density(G),
        'avg_clustering_coefficient': nx.average_clustering(G.to_undirected()),
        'avg_shortest_path': nx.average_shortest_path_length(G),
        'degree_assortativity': nx.degree_assortativity_coefficient(G.to_undirected()),
        'num_leaves': sum(1 for node in G.out_degree() if node[1] == 0),
        'avg_children': np.mean(children_count),
        'median_children': np.median(children_count),
        'var_children': np.var(children_count),
    }

    features["filename"] = filename
    return features

# Set the folder path to the directory containing your PDF files.
folder_path = "/home/pluto/ran/data/MALWARE_PDF_PRE_04-2011_10982_files"

# Initialize an empty list to store results.
res = []

# Iterate through each file in the specified folder.
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        try:
            # Load the PDF genome and extract paths.
            pdf_obj = PdfGenome.load_genome(file_path, pickleable=True)
            paths = PdfGenome.get_object_paths(pdf_obj)

            # If paths are picklable, store the result.
            if is_picklable(paths):
                result = {
                    "filename": filename,
                    "paths": paths
                }
                res.append(result)
        except Exception as e:
            # Skip files that cause exceptions during processing.
            continue

# Extract graph features from the paths and store them in a list.
graph_features = [extract_graph_features_root(result) for result in res]

# Save the graph features to a pickle file.
with open('maliciousPaths_features.pkl', 'wb') as file:
    pickle.dump(graph_features, file)

import pandas as pd
import json
import os
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

def cluster_reviews():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    input_file = os.path.join(data_dir, "clean_reviews.csv")
    
    if not os.path.exists(input_file):
        print("Clean data not found! Please run process_data.py first.")
        return
        
    df = pd.read_csv(input_file)
    if df.empty:
        print("No records to cluster.")
        return
        
    # We only care about the clean_text column for clustering
    docs = df['clean_text'].tolist()
    print(f"Loaded {len(docs)} clean reviews for clustering.")
    
    # 1. Generate Embeddings
    print("Generating sentence embeddings (this may take a minute or two on CPU)...")
    # Using a fast, lightweight model perfect for this scale
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(docs, show_progress_bar=True)
    
    # 2. Dimensionality Reduction (UMAP)
    # HDBSCAN works much better on low-dimensional data
    print("Reducing dimensions with UMAP...")
    umap_model = umap.UMAP(n_neighbors=15, 
                           n_components=5, 
                           metric='cosine', 
                           random_state=42)
    reduced_embeddings = umap_model.fit_transform(embeddings)
    
    # 3. Clustering (HDBSCAN)
    # min_cluster_size dictates the smallest number of reviews that can form a theme
    print("Clustering with HDBSCAN...")
    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=10, 
                                    metric='euclidean', 
                                    cluster_selection_method='eom')
    clusters = hdbscan_model.fit_predict(reduced_embeddings)
    
    df['cluster'] = clusters
    
    # 4. Extract Representative Themes
    # We will format this into a JSON structure that the Groq LLM can easily read in Phase 4
    clustered_themes = {}
    
    # -1 is the "noise" cluster in HDBSCAN. We ignore it.
    unique_clusters = set(clusters)
    for c in unique_clusters:
        if c == -1:
            continue
            
        cluster_data = df[df['cluster'] == c]
        
        # Grab a sample of 10 quotes to represent the theme
        quotes = cluster_data['clean_text'].head(10).tolist()
        
        clustered_themes[f"Cluster_{c}"] = {
            "size": len(cluster_data),
            "sample_quotes": quotes
        }
        
    print(f"Identified {len(clustered_themes)} distinct themes/clusters (ignoring noise).")
    
    # 5. Save the output
    output_path = os.path.join(data_dir, "clustered_themes.json")
    with open(output_path, 'w') as f:
        json.dump(clustered_themes, f, indent=4)
        
    print(f"Saved clustered themes to {output_path}")

if __name__ == "__main__":
    cluster_reviews()

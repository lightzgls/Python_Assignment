import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# === Load and preprocess ===
df = pd.read_csv("result.csv")
stats = df.iloc[:, 4:]  # Assuming stats start from 5th column
stats = stats.apply(pd.to_numeric, errors='coerce').fillna(0)

# Save feature names
feature_names = stats.columns.tolist()

# === Standardize ===
scaler = StandardScaler()
scaled_stats = scaler.fit_transform(stats)

# === Cluster and plot ===
n_clusters_list = [13,14,15]

for k in n_clusters_list:
    # KMeans
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(scaled_stats)

    # PCA
    pca = PCA(n_components=2)
    pca_stats = pca.fit_transform(scaled_stats)

    # Plot clusters in 2D PCA space
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(pca_stats[:, 0], pca_stats[:, 1], c=labels, cmap='tab20', s=50)
    plt.title(f"K-means Clustering (k={k}) with PCA Projection")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.colorbar(scatter, label='Cluster')

    # Draw larger arrows (feature vectors)
    scale_factor = 100  # Increase this to scale arrows further
    for i, feature in enumerate(feature_names):
        x_vector = pca.components_[0, i]
        y_vector = pca.components_[1, i]
        plt.arrow(0, 0, x_vector * scale_factor, y_vector * scale_factor, 
                  color='red', alpha=0.7, head_width=0.2, length_includes_head=True)
        plt.text(x_vector * scale_factor * 1.1, y_vector * scale_factor * 1.1, feature, color='red', fontsize=9)

    plt.grid(True)
    plt.axhline(0, color='gray', lw=1)
    plt.axvline(0, color='gray', lw=1)
    plt.tight_layout()
    plt.show()

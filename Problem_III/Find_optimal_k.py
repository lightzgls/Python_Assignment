import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator

# Load data
df = pd.read_csv("results.csv")
df = df.iloc[:, 4:]  # Select columns starting from the 5th column

# Change NaN value
df = df.apply(pd.to_numeric, errors='coerce')
df = df.fillna(0)

# Select only numeric columns
data = df.select_dtypes(include=[float, int])

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Try different values of k
range_n_clusters = range(2, df.shape[0])

inertias = []
silhouette_avgs = []

for k in range_n_clusters:
    kmeans = KMeans(n_clusters=k, random_state=k).fit(data_scaled)
    cluster_labels = kmeans.labels_
    inertias.append(kmeans.inertia_)
    silhouette_avgs.append(silhouette_score(data_scaled, cluster_labels))

# Determine the optimal k using the elbow method (KneeLocator)
kelbow = KneeLocator(range_n_clusters, inertias, curve='convex', direction="decreasing")
optimal_k = kelbow.knee
print("Optimal k (Elbow/Inertia):", optimal_k)

# Plot
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Elbow plot (inertia)
ax[0].plot(range_n_clusters, inertias, marker='o')
ax[0].axvline(optimal_k, linestyle='--', color='red', label=f'Optimal k = {optimal_k}')
# Add the optimal_k text in a box at the top-right corner
ax[0].text(0.95, 0.95, f'Optimal k = {optimal_k}', transform=ax[0].transAxes, 
           fontsize=12, color='red', ha='right', va='top',
           bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.3'))

ax[0].set_title("Elbow Method (Inertia)")
ax[0].set_xlabel("Number of Clusters (k)")
ax[0].set_ylabel("Inertia (WCSS)")

# Silhouette plot
ax[1].plot(range_n_clusters, silhouette_avgs, marker='o', color='green')
ax[1].set_title("Silhouette Score")
ax[1].set_xlabel("Number of Clusters (k)")
ax[1].set_ylabel("Average Silhouette Score")

plt.suptitle("Choosing Optimal k: Elbow & Silhouette Method", fontsize=16)
plt.tight_layout()
plt.show()
